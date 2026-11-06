"""Check the v33 placements against original TMX levels and source sign grids."""
import csv
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("analysis/furniture_full_b42/2026-11-06")
OUT = ROOT / "restaurant_signs_v34"
TILESET = "location_restaurant_generic_01"
SERIES = [
    ("BUFFET", "S", 40, 42), ("BUFFET", "E", 43, 45),
    ("BURGERS", "S", 48, 51), ("BURGERS", "E", 52, 55),
    ("CAFE", "S", 56, 57),
]


def save(name, columns, rows):
    with (OUT / name).open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(rows)


def main():
    with (ROOT / "restaurant_signs_v33/V33_PLACEMENTS.csv").open() as stream:
        previous = list(csv.DictReader(stream))
    maps = sorted({row["map"] for row in previous})
    found = []
    for path in maps:
        root = ET.parse(path).getroot()
        first, = [int(ts.attrib["firstgid"]) for ts in root.findall("tileset")
                  if ts.get("name") == TILESET]
        for index, layer in enumerate(root.iter("layer")):
            width = int(layer.attrib["width"])
            data = layer.find("data")
            assert data.get("encoding") == "csv"
            assert not any(int(layer.get(k, 0)) for k in ("x", "y", "offsetx", "offsety"))
            gids = data.text.strip().rstrip(",").split(",")
            assert len(gids) == width * int(layer.attrib["height"])
            for i, raw in enumerate(gids):
                gid = int(raw)
                local = (gid & 0x0fffffff) - first
                if 40 <= local <= 57:
                    assert gid == (gid & 0x0fffffff)
                    found.append((path, int(layer.attrib["level"]), index, layer.get("name"),
                                  i % width, i // width, local))
    assert Counter((p, name, x, y, n) for p, _, _, name, x, y, n in found) == Counter(
        (r["map"], r["layer_name"], int(r["x"]), int(r["y"]), int(r["local_id"]))
        for r in previous)
    assert len(found) == 100 and len(maps) == 16
    OUT.mkdir(parents=True, exist_ok=True)
    save("V34_LEVEL_PLACEMENTS.csv", ["map","level","layer_index","layer_name","x","y","local_id"], found)
    groups = defaultdict(list)
    for path, level, index, layer, x, y, local in found:
        for label, facing, start, end in SERIES:
            if start <= local <= end:
                k = local - start
                anchor = (x-k, y) if facing == "S" else (x, y+k)
                groups[path,level,label,facing,start,end,*anchor].append((local,index,layer))
    rows = []
    for (path,level,label,facing,start,end,x,y), parts in sorted(groups.items()):
        ids = {n for n,_,_ in parts}
        complete = len(ids) == end-start+1
        assert len(ids) == len(parts), (path, parts)
        layers = {index for _,index,_ in parts}
        status = "partial" if not complete else ("one_layer" if len(layers)==1 else "multiple_layers")
        rows.append((path,level,label,facing,start,end,x,y,status,
                     "|".join(f"{n}@{idx}/{layer}" for n,idx,layer in sorted(parts))))
    save("V34_SIGN_ASSEMBLIES.csv", ["map","level","lettering","facing","first_id","last_id",
         "first_piece_x","first_piece_y","status","ids_and_layers"], rows)


if __name__ == "__main__":
    main()
