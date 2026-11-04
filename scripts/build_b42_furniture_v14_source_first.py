#!/usr/bin/env python3
"""v14 source-first audit: Wiki is a fallible reference, never an authoritative census."""
import csv,hashlib,json,re,shutil,sqlite3,zipfile
from pathlib import Path
from collections import Counter,defaultdict
R=Path(__file__).resolve().parents[1]
SRC=R/"analysis/furniture_full_b42/2026-11-04/conflict_triage_v13/B42_FURNITURE_CONFLICT_TRIAGE_V13.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-04/source_first_v14"
DB=OUT/"B42_FURNITURE_SOURCE_FIRST_V14.sqlite"
def allrows(c,sql):
 return [dict(x) for x in c.execute(sql)]
def j(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def write(name,rows):
 if not rows:raise ValueError(name)
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def norm(s):return re.sub(r"[^a-z0-9가-힣]","",(s or "").lower())
def main():
 assert SRC.exists() and not OUT.exists()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(SRC) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CONFLICT_TRIAGE_V13.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 old={"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,
      "registry_entry":2231,"wiki_furniture":1268,"v12_template_proof":3840,
      "v13_warning_case":474,"v13_storage_link":1855}
 for t,n in old.items():assert c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]==n,(t,n)
 entries=allrows(c,"SELECT * FROM registry_entry ORDER BY entry_id")
 wiki=[x for x in entries if x["source_system"]=="WIKI"]
 sources=[x for x in entries if x["source_system"]!="WIKI"]
 assert len(wiki)==1268 and len(sources)==963,(len(wiki),len(sources))
 groups={x["group_id"]:x for x in allrows(c,"SELECT * FROM furniture_group")}
 tiles={x["source_key"]:x for x in allrows(c,"SELECT * FROM furniture_tile")}
 links=defaultdict(list)
 for x in allrows(c,"SELECT * FROM registry_entry_tile"):links[x["entry_id"]].append(x)
 directions=defaultdict(list)
 for x in allrows(c,"SELECT * FROM v12_template_proof"):directions[x["group_id"]].append(x)
 storage=defaultdict(list)
 for x in allrows(c,"SELECT * FROM v9_container_evidence"):storage[x["entry_id"]].append(x)
 wiki_names=defaultdict(list)
 for x in wiki:wiki_names[norm(x["display_name"])].append(x["wiki_id"])
 image=defaultdict(list)
 for r in allrows(c,"SELECT i.tileset,i.local_id,i.png_path,i.column_index,i.row_index,i.has_visible_pixels,a.cell_width,a.cell_height FROM image_cells i JOIN image_atlases a ON a.png_path=i.png_path WHERE i.tileset IS NOT NULL AND i.local_id IS NOT NULL"):
  image[(r["tileset"].lower(),r["local_id"])].append(r)
 for data in image.values():data.sort(key=lambda x:(-int(bool(x["has_visible_pixels"])),x["png_path"]))
 c.executescript("""
 CREATE TABLE v14_source_only_ledger(
 entry_id TEXT PRIMARY KEY,group_id TEXT,original_name TEXT,tileset TEXT,
 source_grouping_basis TEXT,original_tile_count INTEGER,original_tile_ids_json TEXT,
 original_facing_json TEXT,original_grid_positions_json TEXT,direction_templates INTEGER,
 geometrically_rectangular_candidates INTEGER,container_types_raw_json TEXT,
 capacity_raw_json TEXT,original_source_files_json TEXT,
 original_png_path TEXT,original_png_tile_key TEXT,image_mapping_present INTEGER,
 same_normalized_name_wiki_candidates_json TEXT,wiki_reference_status TEXT,
 wiki_missing_in_game_proven INTEGER DEFAULT 0,game_object_certified INTEGER DEFAULT 0);
 CREATE TABLE v14_wiki_reference_audit(
 wiki_id TEXT PRIMARY KEY,wiki_name TEXT,original_wiki_capacity_raw TEXT,
 original_wiki_size_raw TEXT,exact_image_tile_count INTEGER,
 direct_source_container_tiles INTEGER,direct_source_capacity_values_json TEXT,
 reference_gap_status TEXT,wiki_snapshot_up_to_date_verified INTEGER DEFAULT 0,
 game_object_certified INTEGER DEFAULT 0);
 CREATE TABLE v14_source_tile_wiki_coverage(
 source_key TEXT PRIMARY KEY,source_group_id TEXT,tileset TEXT,local_id INTEGER,
 original_Facing TEXT,original_SpriteGridPos TEXT,
 original_container_type TEXT,original_capacity TEXT,
 exact_wiki_image_id_anchors_json TEXT,original_png_evidence_json TEXT,
 auto_game_object_identity_certified INTEGER DEFAULT 0);
 CREATE TABLE v14_original_png_crop(
 crop_queue_number INTEGER PRIMARY KEY,entry_id TEXT,source_key TEXT,png_path TEXT,
 cell_width INTEGER,cell_height INTEGER,column_index INTEGER,row_index INTEGER,
 png_sha256 TEXT DEFAULT '',crop_pixel_sha256 TEXT DEFAULT '',
 crop_status TEXT DEFAULT 'NOT_RENDERED_YET',
 image_visual_identity_reviewed INTEGER DEFAULT 0,game_object_certified INTEGER DEFAULT 0);
 """)
 bykey=defaultdict(list)
 for r in allrows(c,"SELECT wiki_id,source_key FROM wiki_image_tile WHERE matching_status='SOURCE_ID_FOUND'"):
  bykey[r["source_key"].casefold()].append(r["wiki_id"])
 source_rows=[];coverage=[]
 for e in sources:
  eid=e["entry_id"];gid=e["source_group_id"];g=groups[gid];ll=links[eid]
  assert ll and all(x["source_group_id"]==gid for x in ll)
  kk=sorted({x["source_key"] for x in ll})
  tt=directions[gid]
  assert tt
  loc=sorted({x["source_sprite_grid_pos"] for x in ll if x["source_sprite_grid_pos"]})
  types=sorted({x["container_type"] for x in storage[eid] if x["container_type"]})
  caps=sorted({str(x["capacity_raw"]) for x in storage[eid] if x["capacity_raw"] not in (None,"")})
  files=sorted({x["original_tiledef_source_files"] for x in ll})
  opts=[]
  for key in kk:
   t=tiles[key]
   for a in image.get((t["tileset"].lower(),t["local_id"]),[]):
    if a["png_path"] and a["png_path"].startswith("Tiles/") and a["png_path"].endswith(".png"):
     opts.append((int(bool(a["has_visible_pixels"])),key,a))
  opts.sort(key=lambda x:(-x[0],x[2]["png_path"],x[1]))
  rep=opts[0] if opts else None
  same=sorted(wiki_names.get(norm(e["display_name"]),[]))
  obj=dict(entry_id=eid,group_id=gid,original_name=e["display_name"],tileset=g["tileset"],
   source_grouping_basis=g["grouping_basis"],original_tile_count=len(kk),
   original_tile_ids_json=j(kk),original_facing_json=j(sorted({x["Facing"] for x in tt})),
   original_grid_positions_json=j(loc),direction_templates=len(tt),
   geometrically_rectangular_candidates=sum(x["reproduced_status"]=="COMPLETE_RECTANGLE" for x in tt),
   container_types_raw_json=j(types),capacity_raw_json=j(caps),
   original_source_files_json=j(files),original_png_path=rep[2]["png_path"] if rep else "",
   original_png_tile_key=rep[1] if rep else "",image_mapping_present=int(bool(rep)),
   same_normalized_name_wiki_candidates_json=j(same),
   wiki_reference_status=("WIKI_NAME_ONLY_CANDIDATE_NOT_LINKED" if same else
                          "NO_EXACT_WIKI_IMAGE_ID_LINK_WIKI_ABSENCE_UNKNOWN"))
  c.execute("INSERT INTO v14_source_only_ledger("+",".join(obj)+") VALUES ("+",".join("?" for _ in obj)+")",list(obj.values()))
  source_rows.append(obj)
 for t in tiles.values():
  key=t["source_key"]
  a=image.get((t["tileset"].lower(),t["local_id"]),[])
  obj=dict(source_key=key,source_group_id=t["group_id"],tileset=t["tileset"],local_id=t["local_id"],
   original_Facing=t["Facing"],original_SpriteGridPos=t["SpriteGridPos"],
   original_container_type=t["container_type"],original_capacity=t["ContainerCapacity"],
   exact_wiki_image_id_anchors_json=j(sorted(set(bykey[key.casefold()]))),
   original_png_evidence_json=j(sorted(set(z["png_path"] for z in a))),
   auto_game_object_identity_certified=0)
  c.execute("INSERT INTO v14_source_tile_wiki_coverage VALUES(?,?,?,?,?,?,?,?,?,?,?)",list(obj.values()))
  coverage.append(obj)
 gaps=Counter();wiki_rows=[]
 for e in wiki:
  linked=[x for x in links[e["entry_id"]] if x["evidence"]=="EXACT_WIKI_IMAGE_SPRITE_KEY"]
  ct=[x for x in linked if x["container_type_raw"] or x["capacity_raw"]]
  rawcap=sorted({str(x["capacity_raw"]) for x in ct if x["capacity_raw"] not in (None,"")})
  wikicap=e["wiki_capacity_raw"] or ""
  if rawcap and not wikicap:state="TILEDEF_DIRECT_CAPACITY_BUT_WIKI_FIELD_BLANK"
  elif rawcap and wikicap:state="BOTH_RAW_VALUES_SEMANTICS_UNVERIFIED"
  elif wikicap:state="WIKI_VALUE_WITHOUT_DIRECT_TILEDEF_CAPACITY"
  else:state="INSUFFICIENT_STORAGE_EVIDENCE"
  obj=dict(wiki_id=e["wiki_id"],wiki_name=e["display_name"],
   original_wiki_capacity_raw=wikicap,original_wiki_size_raw=e["wiki_size_raw"] or "",
   exact_image_tile_count=len(linked),direct_source_container_tiles=len(ct),
   direct_source_capacity_values_json=j(rawcap),reference_gap_status=state)
  c.execute("INSERT INTO v14_wiki_reference_audit("+",".join(obj)+") VALUES ("+",".join("?" for _ in obj)+")",list(obj.values()))
  wiki_rows.append(obj);gaps[state]+=1
 # Image crop queue: deterministic high-priority source-only samples, spread across atlases.
 candidates=[r for r in source_rows if r["original_png_path"]]
 candidates.sort(key=lambda x:(-int(x["geometrically_rectangular_candidates"]>0),
  -min(x["direction_templates"],4),-int(bool(json.loads(x["container_types_raw_json"]))),
  -x["original_tile_count"],x["entry_id"]))
 picked=[];byatlas=Counter();seen=set()
 for max_per_atlas in (4,8,9999):
  for r in candidates:
   if len(picked)>=160:break
   if r["entry_id"] in seen or byatlas[r["original_png_path"]]>=max_per_atlas:continue
   a=image[(tiles[r["original_png_tile_key"]]["tileset"].lower(),
            tiles[r["original_png_tile_key"]]["local_id"]) ]
   aa=next((z for z in a if z["png_path"]==r["original_png_path"]),None)
   if not aa or not all(aa.get(k) is not None for k in ("cell_width","cell_height","column_index","row_index")):continue
   item=dict(crop_queue_number=len(picked)+1,entry_id=r["entry_id"],
    source_key=r["original_png_tile_key"],png_path=r["original_png_path"],
    cell_width=aa["cell_width"],cell_height=aa["cell_height"],
    column_index=aa["column_index"],row_index=aa["row_index"])
   c.execute("INSERT INTO v14_original_png_crop("+",".join(item)+") VALUES ("+",".join("?" for _ in item)+")",list(item.values()))
   picked.append(item);seen.add(r["entry_id"]);byatlas[r["original_png_path"]]+=1
 assert len(picked)==160,("preview candidates",len(picked))
 (OUT/"_required_original_png_paths.txt").write_text("\n".join(sorted(byatlas))+"\n",encoding="utf8")
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("SELECT COUNT(*) FROM v14_source_only_ledger").fetchone()[0]==963
 assert c.execute("SELECT COUNT(*) FROM v14_wiki_reference_audit").fetchone()[0]==1268
 assert c.execute("SELECT COUNT(*) FROM v14_source_tile_wiki_coverage").fetchone()[0]==8219
 assert c.execute("SELECT COUNT(*) FROM v14_original_png_crop").fetchone()[0]==160
 c.close()
 write("V14_963_SOURCE_ONLY_TILEDEF_LEDGER.csv",source_rows)
 write("V14_1268_WIKI_REFERENCE_GAPS.csv",wiki_rows)
 write("V14_8219_SOURCE_TILE_WIKI_COVERAGE.csv",coverage)
 write("V14_160_SOURCE_ONLY_ORIGINAL_PNG_QUEUE.csv",picked)
 summary=dict(version="v14",source_only_candidate_groups=963,wiki_reference_rows=1268,
   source_tile_rows=8219,wiki_storage_field_gap_types=dict(sorted(gaps.items())),
   source_only_same_normalized_name_wiki_not_verified=sum(bool(json.loads(r["same_normalized_name_wiki_candidates_json"])) for r in source_rows),
   source_only_with_original_png_cell_mapping=sum(r["image_mapping_present"] for r in source_rows),
   exact_wiki_image_connected_source_tile_count=sum(bool(json.loads(r["exact_wiki_image_id_anchors_json"])) for r in coverage),
   original_png_crop_queue_count=len(picked),unique_png_atlases=len(byatlas),
   game_object_identifications_confirmed=0,wiki_absence_confirmed=0,
   original_warnings_still_open=474,wiki_is_authoritative=False,
   wikipedia_or_pzwiki_freshness_unverified=True,
   raw_source_attributes_preserved=195265,raw_source_slots_preserved=73644,
   original_tile_keys_preserved=8219,storage_links_preserved=1855,
   sqlite_integrity="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print("V14_SOURCE_FIRST_DB_CREATED",json.dumps(summary,ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
