"""Compare same-facing desk components in B42 TMX maps with original SpriteGridPos."""
import csv
import json
import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("analysis/furniture_full_b42/2026-11-06")
OUT = ROOT / "office_desks_v35"
INDEX = ROOT / "geometry_warning_v30/V30_EXACT_SOURCE_KEY_POSITION_PNG_INDEX.csv"
ATLAS = "location_business_office_generic_01"
GROUPS = {"FUR-1BAEC04A10AC7D72", "FUR-93A2BAF20FE07365"}


def write(name, header, rows):
    with (OUT / name).open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def normalized(parts):
    x0 = min(x for _, x, y in parts)
    y0 = min(y for _, x, y in parts)
    return sorted((n, x-x0, y-y0) for n,x,y in parts)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {}
    expected = defaultdict(list)
    with INDEX.open(encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            g = row["group_id"]
            if g not in GROUPS:
                continue
            sheet, num = row["source_key"].split("/")
            assert sheet == ATLAS
            n = int(num)
            face = row["Facing"]
            meta[n] = (g, face)
            expected[g, face].append((n, int(row["original_x"]), int(row["original_y"])))
    assert len(meta) == 40 and len(expected) == 8
    found = []
    by_floor = defaultdict(lambda: defaultdict(list))
    maps = []
    for path in sorted(Path("B4220.3_MapExport_256").rglob("*.tmx")):
        tree = ET.parse(path).getroot()
        sheets = [t for t in tree.findall("tileset") if t.get("name") == ATLAS]
        if not sheets:
            assert not any(t.get("source") for t in tree.findall("tileset"))
            maps.append((str(path),0,0))
            continue
        first, = [int(t.attrib["firstgid"]) for t in sheets]
        width, height = int(tree.attrib["width"]), int(tree.attrib["height"])
        assert (width,height) == (256,256)
        cx,cy = map(int,path.stem.split("_"))
        first_after = min((int(t.attrib["firstgid"]) for t in tree.findall("tileset")
                           if int(t.attrib["firstgid"]) > first), default=2**28)
        assert first + max(meta) < first_after
        lookup = np.zeros(max(meta)+1, dtype=bool)
        lookup[list(meta)] = True
        count = 0
        for layer_index, layer in enumerate(tree.iter("layer")):
            data = layer.find("data")
            assert data.get("encoding") == "csv" and not data.findall("chunk")
            assert not any(int(layer.get(k,0)) for k in ("x","y","offsetx","offsety"))
            raw = data.text.strip().rstrip(",")
            level = int(layer.attrib["level"])
            assert (int(layer.attrib["width"]),int(layer.attrib["height"])) == (width,height)
            values = np.fromstring(raw, sep=",", dtype=np.uint32)
            assert len(values) == width * height
            local = (values & 0x0fffffff) - first
            for index in np.flatnonzero(local <= max(meta)):
                n = int(local[index])
                if not lookup[n]:
                    continue
                gid = int(values[index])
                index = int(index)
                g,face = meta[n]
                x,y = index % width,index // width
                assert y < height
                wx,wy = cx*width+x,cy*height+y
                found.append((str(path),level,layer_index,layer.get("name"),x,y,wx,wy,g,face,n,gid>>28))
                by_floor[g,face,level][wx,wy].append((n,gid>>28))
                count += 1
        maps.append((str(path),1,count))
    assert len(maps)==4914
    components = []
    for (g,face,level),cells in sorted(by_floor.items()):
        pending = set(cells)
        while pending:
            seed = min(pending)
            pending.remove(seed)
            stack = [seed]
            members = []
            flags = []
            while stack:
                x,y = stack.pop()
                for n,flag in cells[x,y]:
                    members.append((n,x,y))
                    flags.append(flag)
                for neighbor in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if neighbor in pending:
                        pending.remove(neighbor)
                        stack.append(neighbor)
            shape = normalized(members)
            complete = Counter(n for n,x,y in members) == Counter(n for n,x,y in expected[g,face])
            exact = complete and not any(flags) and shape == normalized(expected[g,face])
            components.append((g,face,level,min(x for n,x,y in members),min(y for n,x,y in members),
                               len(members),len(set((x,y) for n,x,y in members)),int(complete),
                               int(any(flags)),int(exact),json.dumps(shape,separators=(",",":"))))
    assert sum(x[2] for x in maps)==sum(x[5] for x in components)==len(found)
    write("V35_MAP_COVERAGE.csv", ["map","atlas_referenced","placements"], maps)
    write("V35_PLACEMENTS.csv", ["map","level","layer_index","layer","x","y","world_x","world_y","group","facing","local_id","flags"],found)
    write("V35_COMPONENTS.csv", ["group","facing","level","min_world_x","min_world_y","parts","cells","five_distinct_source_parts","has_flags","matches_source_coordinates","normalized_parts"],components)


if __name__ == "__main__":
    main()
