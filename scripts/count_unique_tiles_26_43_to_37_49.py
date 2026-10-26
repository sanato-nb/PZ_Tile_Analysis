#!/usr/bin/env python3
"""Count distinct USED B42 tile IDs in TMX rectangle x=26..37, y=43..49.

Deduplication identity: (TMX tileset name, zero-based local tile ID).
Every tile layer on every level is included; raw GID is not a stable cross-map identity.
Source TMX file SHA-256 recorded for reproducible review. Does not mutate analysis DB.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import bisect, csv, hashlib, json, re, struct, gzip, zlib, base64
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
MAPS=ROOT/"B4220.3_MapExport_256/tmx"
OUT=ROOT/"audits/map_range_26_43_to_37_49"
OUT.mkdir(parents=True,exist_ok=True)
names=[f"{x}_{y}.tmx" for x in range(26,38) for y in range(43,50)]
assert len(names)==84 and len(set(names))==84
absent=[x for x in names if not (MAPS/x).is_file()]
assert not absent, f"TMX missing in requested rectangle: {absent}"

all_layer_keys=set()
all_tile_object_keys=set()
key_maps=Counter()
map_detail=[]
set_usage=Counter()
unknown=[]
encodings=Counter()
total_occurrences=0
total_tile_object_occurrences=0
all_tileset_sources={}
for index,filename in enumerate(names):
    path=MAPS/filename
    raw=path.read_bytes()
    root=ET.fromstring(raw)
    tw=int(root.attrib.get("tilewidth","0"))
    th=int(root.attrib.get("tileheight","0"))
    tilesets=[]
    for t in root.findall("tileset"):
        if t.get("name"):
            tileset_name=t.get("name")
        else:
            # A TSX without inlined tileset name cannot safely be assigned a local identity.
            raise RuntimeError(f"external tileset without name in {filename}: {t.attrib}")
        first=int(t.attrib["firstgid"])
        image=t.find("image")
        img_src=image.get("source") if image is not None else "(no-image)"
        all_tileset_sources.setdefault(tileset_name,set()).add(img_src)
        tilesets.append((first,tileset_name))
    tilesets.sort()
    firsts=[i for i,_ in tilesets]
    assert len(firsts)==len(set(firsts)) and firsts,filename
    keys=set(); obj_keys=set()
    layer_count=0; layer_tiles=0
    for layer in root.iter("layer"):
        layer_count+=1
        data=layer.find("data")
        if data is None:
            raise ValueError(f"missing layer data: {filename}, {layer.get('name')}")
        encoding=data.get("encoding","xml")
        encodings[encoding+(("/"+data.get("compression")) if data.get("compression") else "")]+=1
        width=int(layer.get("width",root.get("width","0")))
        height=int(layer.get("height",root.get("height","0")))
        if encoding=="csv":
            values=(int(s) for s in re.findall(r"\d+",data.text or ""))
        elif encoding=="base64":
            b=base64.b64decode("".join((data.text or "").split()))
            compression=data.get("compression")
            if compression=="zlib":b=zlib.decompress(b)
            elif compression=="gzip":b=gzip.decompress(b)
            elif compression is None:pass
            else:raise ValueError(f"unknown compression {compression} in {filename}")
            assert len(b)%4==0
            values=(v[0] for v in struct.iter_unpack("<I",b))
        elif encoding=="xml":
            values=(int(t.attrib.get("gid","0")) for t in data.findall("tile"))
        else:
            raise ValueError(f"unsupported layer encoding {encoding!r}: {filename}")
        n=0
        for raw_gid in values:
            n+=1
            gid=raw_gid&0x0fffffff # Tiled's four highest GID bits are flags.
            if gid==0:continue
            ix=bisect.bisect_right(firsts,gid)-1
            if ix<0:
                unknown.append((filename,layer.get("name"),raw_gid))
                continue
            first,name=tilesets[ix]
            local_id=gid-first
            if local_id<0:raise AssertionError((filename,gid))
            keys.add((name,local_id))
            layer_tiles+=1
        assert n==width*height, (filename,layer.get("name"),n,width,height)
    for obj in root.iter("object"):
        if "gid" not in obj.attrib:continue
        total_tile_object_occurrences+=1
        gid=int(obj.get("gid"))&0x0fffffff
        if not gid:continue
        ix=bisect.bisect_right(firsts,gid)-1
        if ix<0:
            unknown.append((filename,"object",gid))
            continue
        first,name=tilesets[ix]
        obj_keys.add((name,gid-first))
    for key in keys:key_maps[key]+=1
    all_layer_keys.update(keys)
    all_tile_object_keys.update(obj_keys)
    total_occurrences+=layer_tiles
    for tile_set,_ in keys:set_usage[tile_set]+=1
    map_detail.append(dict(tmx=filename,sha256=hashlib.sha256(raw).hexdigest(),
                           filesize_bytes=len(raw),tilesets_declared=len(tilesets),
                           tile_layers=layer_count,occupied_layer_positions=layer_tiles,
                           distinct_used_tile_keys=len(keys),
                           tile_object_keys=len(obj_keys)))
    if (index+1)%14==0:print("PROGRESS",index+1,"/84", "current unique layer keys",len(all_layer_keys),flush=True)
assert not unknown, f"Unresolved raw tile GIDs (sample): {unknown[:20]}"
assert len(map_detail)==84
combined=all_layer_keys|all_tile_object_keys
obj_only=all_tile_object_keys-all_layer_keys
report={
    "source":"GitHub repo sanato-nb/PZ_Tile_Analysis, B4220.3_MapExport_256/tmx",
    "range":{"x_min":26,"x_max":37,"y_min":43,"y_max":49,"inclusive":True},
    "files_expected":84,"files_present":len(map_detail),"files_missing":absent,
    "distinct_tile_keys_tile_layers":len(all_layer_keys),
    "distinct_tile_keys_tile_layers_plus_tile_objects":len(combined),
    "unique_tile_object_only_keys":len(obj_only),
    "distinct_tileset_names_used":len({k[0] for k in all_layer_keys}),
    "total_occupied_layer_positions_before_deduplication":total_occurrences,
    "tile_object_occurrences":total_tile_object_occurrences,
    "normalization":"(tileset_name, local_id=gid_without_4_high_flags-firstgid), across all 84 maps and all tile layers",
    "encodings":dict(encodings),
    "multiple_image_sources_for_same_tileset_name":{
      name:sorted(sources) for name,sources in all_tileset_sources.items() if len(sources)>1
    },
    "per_map":map_detail,
    "tileset_distinct_key_counts":dict(sorted(Counter(k[0] for k in all_layer_keys).items())),
    "distinct_tile_keys_sha256":hashlib.sha256(
       "".join(f"{a}\t{b}\n" for a,b in sorted(all_layer_keys)).encode()).hexdigest()
}
(OUT/"SUMMARY.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
with (OUT/"DISTINCT_TILE_KEYS.csv").open("w",encoding="utf-8-sig",newline="") as f:
    writer=csv.writer(f);writer.writerow(["tile_set_name","local_id","maps_using_tile_key"])
    for name,lid in sorted(all_layer_keys):
        writer.writerow([name,lid,key_maps[name,lid]])
with (OUT/"PER_MAP.csv").open("w",encoding="utf-8-sig",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=list(map_detail[0]))
    writer.writeheader();writer.writerows(map_detail)
print("FINAL DISTINCT TILE-LAYER KEYS",len(all_layer_keys))
print("WITH TILE OBJECT GIDS",len(combined),"object-only",len(obj_only))
print("TMX",len(map_detail),"layers used",sum(m["tile_layers"] for m in map_detail))
print("SHA",report["distinct_tile_keys_sha256"])
