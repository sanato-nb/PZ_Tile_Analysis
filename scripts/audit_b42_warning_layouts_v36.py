"""Compare coordinate-warning components in B42 TMX maps with original SpriteGridPos."""
import csv
import json
import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("analysis/furniture_full_b42/2026-11-06")
OUT = ROOT / "warning_layouts_v36"
INDEX = ROOT / "geometry_warning_v30/V30_EXACT_SOURCE_KEY_POSITION_PNG_INDEX.csv"


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
    meta = defaultdict(dict)
    atlas_by_group = {}
    expected = defaultdict(list)
    with INDEX.open(encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            g = row["group_id"]
            sheet, num = row["source_key"].split("/")
            assert atlas_by_group.setdefault(g, sheet) == sheet
            n = int(num)
            face = row["Facing"]
            assert n not in meta[sheet]
            meta[sheet][n] = (g, face)
            expected[g, face].append((n, int(row["original_x"]), int(row["original_y"])))
    assert sum(map(len, meta.values())) == 257 and len(expected) == 41
    found = []
    by_floor = defaultdict(lambda: defaultdict(list))
    maps = []
    for path in sorted(Path("B4220.3_MapExport_256").rglob("*.tmx")):
        tree = ET.parse(path).getroot()
        tilesets = sorted((int(t.attrib["firstgid"]), t.attrib["name"]) for t in tree.findall("tileset"))
        slots = {}
        for i, (start, name) in enumerate(tilesets):
            if name not in meta:
                continue
            limit = tilesets[i+1][0] if i+1 < len(tilesets) else 2**28
            for local_id,(group,face) in meta[name].items():
                assert start + local_id < limit
                slots[start+local_id] = (group, face, local_id)
        if not slots:
            maps.append((str(path),0,0))
            continue
        width, height = int(tree.attrib["width"]), int(tree.attrib["height"])
        assert (width,height) == (256,256)
        cx,cy = map(int,path.stem.split("_"))
        # Use a sentinel for all non-target GIDs, including GIDs beyond the last target.
        lookup = np.zeros(max(slots)+2,dtype=bool)
        lookup[list(slots)] = True
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
            masked = values & 0x0fffffff
            for index in np.flatnonzero(lookup[np.minimum(masked,len(lookup)-1)]):
                index = int(index)
                gid = int(values[index])
                g,face,n = slots[gid & 0x0fffffff]
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
    write("V36_MAP_COVERAGE.csv", ["map","atlas_referenced","placements"], maps)
    write("V36_PLACEMENTS.csv", ["map","level","layer_index","layer","x","y","world_x","world_y","group","facing","local_id","flags"],found)
    write("V36_COMPONENTS.csv", ["group","facing","level","min_world_x","min_world_y","parts","cells","complete_source_multiset","has_flags","matches_source_coordinates","normalized_parts"],components)

    summary = []
    for (group, face), template in sorted(expected.items()):
        subset = [r for r in components if r[:2] == (group,face)]
        full = [r for r in subset if r[7] and not r[8]]
        exact_count = sum(r[9] for r in full)
        alternative = Counter(r[10] for r in full if not r[9])
        summary.append((group,face,atlas_by_group[group],len(template),
                        sum(r[5] for r in subset),len(subset),len(full),exact_count,
                        len(full)-exact_count,max(alternative.values(),default=0),
                        sum(r[8] for r in subset)))
    write("V36_DIRECTION_SUMMARY.csv", ["group","facing","atlas","source_parts","placements",
        "connected_sets","complete_untransformed","exact","different","most_frequent_different",
        "sets_with_transform"],summary)


if __name__ == "__main__":
    main()
