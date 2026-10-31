#!/usr/bin/env python3
"""v246: exhaustively scan all 84 genuine source TMX maps for every held source key.
Source provenance, real repeated positions, original GID and exposure risk. No invented scenes.
"""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,json,re,bisect,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
TROOT=ROOT/"B4220.3_MapExport_256/tmx"
OUT=ROOT/"review/v246_held439_real_alt_TMX_2026-10-30"
OUT.mkdir(parents=True,exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
 return h.hexdigest()
def readcsv(p):
 with p.open(encoding="utf-8-sig",newline='') as f:return list(csv.DictReader(f))
def csvwrite(p,rows,fields):
 with p.open('w',encoding="utf-8-sig",newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
v117=json.loads((ROOT/"review/v117_A_candidates_10042/MANIFEST.json").read_text("utf8"))
tmxs=v117["source_tmx"]
assert len(tmxs)==84 and len({x["tmx"] for x in tmxs})==84
held=readcsv(ROOT/"review/v238_integrated_master_2026-10-29/MASTER_HELD_439_SOURCE_VERIFIED.csv")
assert len(held)==439
held_by_key={(r["tile_set_name"],int(r["local_id"])):r for r in held}
assert len(held_by_key)==439
source_meta={}
for name in ("0000_0879","0880_1679","1680_2479","2480_3279","3280_3839","3840_4319","4320_4632"):
 for r in readcsv(ROOT/f"review/v238_integrated_master_2026-10-29/MASTER_NEW_A_BC_{name}.csv"):
  k=(r["tile_set_name"],int(r["local_id"]))
  if k in held_by_key:source_meta[k]=r
assert len(source_meta)==439
index=defaultdict(list); scanned=0; match_places=0
for file_idx,src in enumerate(tmxs):
 p=TROOT/src["tmx"]
 assert p.stat().st_size==src["filesize_bytes"],str(p)
 assert sha(p)==src["sha256"],str(p)
 root=ET.parse(p).getroot()
 width,height=int(root.get("width","256")),int(root.get("height","256"))
 ts=sorted((int(t.get("firstgid")),t.get("name")) for t in root.findall("tileset") if t.get("name"))
 first=[x[0] for x in ts]; name_to_first={}
 for g,name in ts:
  if name in name_to_first and name_to_first[name]!=g: raise RuntimeError("ambiguous repeated tileset name "+name)
  name_to_first[name]=g
 # resolve target raw local gid from tileset declarations of each actual TMX
 wanted={}
 for (name,local),h in held_by_key.items():
  if name in name_to_first: wanted[name_to_first[name]+local]=(name,local)
 if not wanted:continue
 layers=[]
 for layer_idx,lay in enumerate(root.iter("layer")):
  data=lay.find("data")
  if data is None:continue
  assert data.get("encoding")=="csv"
  level=lay.get("level")
  if level is None:
   prop=lay.find("properties/property[@name='level']")
   level=(prop.get("value") or prop.text) if prop is not None else "0"
  vals=[int(x) for x in re.findall(r"\d+",data.text or "")]
  assert len(vals)==width*height,(src["tmx"],layer_idx,len(vals))
  layers.append((layer_idx,int(level),vals))
 assert len(layers)==src["tile_layers"],(src["tmx"],len(layers),src["tile_layers"])
 for pos,(layer_idx,level,vals) in enumerate(layers):
  for cell,raw in enumerate(vals):
   if not raw:continue
   gid=raw & 0x0fffffff
   key=wanted.get(gid)
   if key is None:continue
   x=cell%width;y=cell//width
   upper=sum(1 for ix,lvl,arr in layers[pos+1:] if lvl==level and arr[cell]!=0)
   # Base ranking: prioritize a scene with no tile above same cell and enough interior margin for 5x5.
   margin=min(x,y,width-1-x,height-1-y)
   original=source_meta[key]
   istheoriginal=(src["tmx"]==original["B_original_TMX"] and 
       layer_idx==int(original["B_layer_index"] or -1) and x==int(original["B_x"] or -999) and
       y==int(original["B_y"] or -999) and level==int(original["B_level"] or -999))
   index[key].append(dict(source_index=int(held_by_key[key]["source_index"]),source_key=key[0]+"/"+str(key[1]),
      tmx=src["tmx"],tmx_sha256=src["sha256"],layer_index=layer_idx,level=level,x=x,y=y,
      raw_gid=raw,base_gid=gid,transform_flags=(raw&0xf0000000),map_margin_cells=margin,
      same_cell_higher_layers=upper,original_record_position=int(istheoriginal)))
   match_places+=1
 scanned+=1
 if (file_idx+1)%12==0:print("verified TMX",file_idx+1,"/84", "occurrences",match_places,flush=True)
# output every actual observed TMX use, cap only best candidates file
counts=[];best=[];unresolved=[]
for k,r in held_by_key.items():
 items=index.get(k,[])
 unique={(x["tmx"],x["layer_index"],x["x"],x["y"]) for x in items}
 assert len(unique)==len(items),(k,"duplicate cell")
 alt=[i for i in items if not i["original_record_position"]]
 alt.sort(key=lambda x:(x["map_margin_cells"]<3,x["same_cell_higher_layers"],-min(x["map_margin_cells"],20),x["tmx"],x["layer_index"],x["y"],x["x"]))
 inbounds=[x for x in alt if x["map_margin_cells"]>=2]
 counts.append(dict(source_index=int(r["source_index"]),source_key=k[0]+"/"+str(k[1]),
   historical_reason=r["original_held_reason"],total_real_occurrences=len(items),alternative_real_positions=len(alt),
   alternative_inbounds_5x5=len(inbounds),
   best_alternate_tmx=alt[0]["tmx"] if alt else "",
   best_alt_layer=alt[0]["layer_index"] if alt else "",
   best_alt_level=alt[0]["level"] if alt else "",
   best_alt_x=alt[0]["x"] if alt else "",best_alt_y=alt[0]["y"] if alt else "",
   best_alt_raw_gid=alt[0]["raw_gid"] if alt else "",
   best_alt_upper_same_cell=alt[0]["same_cell_higher_layers"] if alt else "",
   best_alt_inside=bool(alt and alt[0]["map_margin_cells"]>=2),
   all_source_tmx_checked=84, source_A_already_png_RGBA_verified_v245=1,
   alternative_BC_newly_rendered_in_census=0,
   mapping_verified=0,tilezed_verified=0,certified=0))
 if not alt:unresolved.append(k)
 for rank,q in enumerate(alt[:5],1):best.append({**q,"rank":rank})
all_cols=["source_index","source_key","tmx","tmx_sha256","layer_index","level","x","y","raw_gid","base_gid","transform_flags","map_margin_cells","same_cell_higher_layers","original_record_position"]
flat=[x for entries in index.values() for x in entries]
flat.sort(key=lambda r:(r["source_index"],r["tmx"],r["level"],r["layer_index"],r["y"],r["x"]))
csvwrite(OUT/"ALL_HELD_REAL_TMX_OCCURRENCES.csv",flat,all_cols)
csvwrite(OUT/"HELD439_ALTERNATE_SITE_CENSUS.csv",counts,list(counts[0]))
csvwrite(OUT/"BEST_FIVE_REAL_ALTERNATE_SITES.csv",best,all_cols+["rank"])
m=dict(version="v246",date="2026-10-30",original_TMX_verified=84,original_held_keys=439,
 total_real_TMX_key_placements=len(flat),keys_with_another_real_position=sum(x["alternative_real_positions"]>0 for x in counts),
 keys_with_inbounds_alternative=sum(x["alternative_inbounds_5x5"]>0 for x in counts),
 keys_without_alternative=len(unresolved),source_key_duplicates=0,
 per_key_full_occurrences="ALL_HELD_REAL_TMX_OCCURRENCES.csv",
 recommended_best_five="BEST_FIVE_REAL_ALTERNATE_SITES.csv",
 per_key_census="HELD439_ALTERNATE_SITE_CENSUS.csv",
 original_TMX_checksum_verified_for_all_84=True,
 same_cell_upper_layer_count_is_only_preliminary_occlusion_risk=True,
 other_cells_walls_or_above_floor_occlusion_proven=False,
 new_actual_original_B_C_images_rendered=0,final_identity_certification=0,
 previous_held439_exclusions_unchanged=True,user_exclusions_unchanged=True,
 source_PNG_TMX_and_prior_SQLite_untouched=True)
(OUT/"MANIFEST.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(m,ensure_ascii=False),flush=True)
