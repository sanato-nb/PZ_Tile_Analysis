"""Audit restaurant sign slots 40–57 and their tile-layer placements in repository TMX maps."""
import base64
import csv
import gzip
import json
import shutil
import sqlite3
import struct
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import zlib
from collections import Counter
from pathlib import Path

ATLAS = "location_restaurant_generic_01"
ROOT = Path("analysis/furniture_full_b42/2026-11-06")
OUT = ROOT / "restaurant_signs_v33"
OUT.mkdir(parents=True, exist_ok=True)
ids = range(40, 58)
keys = {f"{ATLAS}/{n}" for n in ids}


def decode(node, encoding, compression):
    if encoding == "csv":
        return [int(v) for v in (node.text or "").strip().strip(",").split(",")]
    if encoding == "base64":
        payload = base64.b64decode(node.text or "")
        if compression:
            payload = {"zlib": zlib.decompress, "gzip": gzip.decompress}[compression](payload)
        return [v for (v,) in struct.iter_unpack("<I", payload)]
    if encoding is None:
        return [int(t.attrib["gid"]) for t in node.findall("tile")]
    raise ValueError(encoding)


def sheet_name(path, ts):
    external = ts.get("source")
    if external:
        target = path.parent / external.replace("\\", "/")
        if target.exists():
            ts = ET.parse(target).getroot()
        else:
            return Path(external.replace("\\", "/")).stem
    return ts.get("name") or Path(ts.find("image").get("source")).stem


def placements(path):
    root = ET.parse(path).getroot()
    sheets = [(int(t.attrib["firstgid"]), sheet_name(path, t)) for t in root.findall("tileset")]
    wanted = {start + n: n for start, name in sheets if name == ATLAS for n in ids
              if not any(start < other <= start + n for other, _ in sheets)}
    found = []
    if wanted:
        for layer in root.iter("layer"):
            data = layer.find("data")
            for chunk in data.findall("chunk") or [data]:
                width = int(chunk.get("width", layer.attrib["width"]))
                height = int(chunk.get("height", layer.attrib["height"]))
                values = decode(chunk, data.get("encoding"), data.get("compression"))
                assert len(values) == width * height, path
                for i, value in enumerate(values):
                    gid = value & 0x0fffffff
                    if gid in wanted:
                        x = int(layer.get("x", 0)) + int(chunk.get("x", 0)) + i % width
                        y = int(layer.get("y", 0)) + int(chunk.get("y", 0)) + i // width
                        found.append([str(path), layer.get("id",""), layer.get("name",""), x, y, wanted[gid]])
    return bool(wanted), found


def main():
    with tempfile.TemporaryDirectory() as temp:
        pack = ROOT / "geometry_warning_v30/B42_FURNITURE_GEOMETRY_WARNINGS_V30.zip"
        with zipfile.ZipFile(pack) as z:
            name, = [n for n in z.namelist() if n.endswith(".sqlite")]
            with z.open(name) as src, open(Path(temp)/"db", "wb") as dest:
                shutil.copyfileobj(src, dest)
        db = sqlite3.connect(Path(temp)/"db")
        db.row_factory = sqlite3.Row
        properties = {}
        for table in ["furniture_tile", "source_slots", "source_attributes"]:
            selected = []
            for row in db.execute("select * from " + table):
                r = dict(row)
                if any(isinstance(v,str) and v in keys for v in r.values()) or (
                    ATLAS in r.values() and any(str(r.get(c)) in {str(n) for n in ids}
                    for c in ["local_id","tile_id","tile_index","local_index"])):
                    selected.append(r)
            properties[table] = selected
        assert len(properties["furniture_tile"]) >= 16
        (OUT/"V33_SOURCE_PROPERTIES.json").write_text(json.dumps(properties, ensure_ascii=False, indent=1))
    results, maps = [], []
    for path in sorted(Path(".").rglob("*.tmx")):
        included, rows = placements(path)
        maps.append([str(path), int(included), len(rows)])
        results.extend(rows)
    assert maps
    for name, header, rows in [
        ("MAP_COVERAGE", ["map","atlas_referenced","target_placements"], maps),
        ("PLACEMENTS", ["map","layer_id","layer_name","x","y","local_id"], results)
    ]:
        with (OUT/f"V33_{name}.csv").open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows(rows)
    print(len(maps), Counter(r[-1] for r in results), {k:len(v) for k,v in properties.items()})


if __name__ == "__main__":
    main()
