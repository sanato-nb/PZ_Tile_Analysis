#!/usr/bin/env python3
"""B42 v25: entire source-first furniture SQLite, 74 last paired-group image observations.
A source SpriteGridPos rectangle is NOT a game-object ID or isometric game rendering.
Previous 43 facing images are reused for comparison, never counted as 43 new inspections.
"""
from collections import defaultdict,Counter
from pathlib import Path
import csv,sqlite3,zipfile,shutil,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v24/B42_FURNITURE_CROSS_FACING_REVIEW_V24.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v25"
DB=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V25.sqlite"
ZIP=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V25.zip"
def qr(c,s,p=()):return [dict(r) for r in c.execute(s,p)]
def cnt(c,table):return c.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
def J(v):return json.dumps(v,sort_keys=True,ensure_ascii=False)
def read(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(name,items):
 assert items,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
def put(c,t,r):
 keys=list(r)
 c.execute("INSERT INTO "+t+"("+",".join(keys)+") VALUES("+",".join("?" for _ in keys)+")",list(r.values()))
def main():
 assert BASE.is_file() and OUT.is_dir() and not DB.exists()
 stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["v25_pair_groups"]==74
 assert stage["source_multifacing_groups"]==274
 assert stage["previously_paired_direct_visual_groups"]==200
 assert stage["new_group_facing_views"]==105
 assert stage["previous_facing_reused_count"]==43
 assert stage["new_source_groups_with_no_prior_facing_views"]==31
 assert stage["existing_once_viewed_source_groups"]==43
 assert stage["original_png_sprites_reextracted"]==476
 assert stage["new_facing_part_pixel_hash_rows"]==300
 assert stage["reused_previous_facing_part_pixel_hash_rows"]==176
 assert stage["new_after_v25_direct_visual_total"]==585
 assert stage["contact_pages"]==10
 pairs=read("V25_74_SOURCE_FACING_PAIR_PLANS.csv")
 faceplan=read("V25_148_DIRECTION_GRIDS_AND_PRIOR_REUSE_FLAGS.csv")
 partrows=read("V25_148_DIRECTION_ORIGINAL_PART_SOURCE_COORDINATES.csv")
 pngpixels=read("V25_ALL_PAIRED_SOURCE_PNG_PIXEL_SHA256.csv")
 labels=read("V25_74_DIRECT_PAIRED_VISUAL_CLASSIFICATIONS.csv")
 assert len(pairs)==len(labels)==74
 assert len(faceplan)==148 and len(partrows)==len(pngpixels)==476
 idpairs={int(r["pair_no"]):r for r in pairs}
 labs={int(r["pair_no"]):r for r in labels}
 assert set(idpairs)==set(labs)==set(range(1,75))
 assert len({r["group_id"] for r in pairs})==74
 for label in labels:
  assert label["direct_visual_review_scope"]=="DIRECT_TWO_ORIGINAL_PNG_POSITIONAL_GRIDS_VISUALLY_INSPECTED"
  assert label["runtime_object_identity_certified"]=="0"
  assert label["observed_two_facing_visual_relation"]=="RELATED_SOURCE_SPRITE_FORMS_WITH_DIFFERENT_FACING_VIEWS_NOT_IN_GAME_IDENTITY"
 assert len(stage["contact_sheet_original_png_sha256"])==10
 for name,sha in stage["contact_sheet_original_png_sha256"].items():
  assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==sha,(name,"source PNG contact hash mismatch")
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CROSS_FACING_REVIEW_V24.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 preserved={"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,
  "registry_entry":2231,"wiki_furniture":1268,"v12_template_proof":3840,
  "v13_warning_case":474,"v14_source_only_ledger":963,
  "v20_master_furniture_registry":2231,
  "v20_source_only_review_coverage":963,
  "v21_all_source_rectangle_template":843,
  "v21_source_tile_positioned_png":2221,
  "v21_direct_multisprite_grid_visual_observation":80,
  "v22_direct_two_facing_visual_comparison":60,
  "v22_new_facing_original_grid":120,
  "v23_direct_two_facing_visual_comparison":60,
  "v23_new_facing_original_source":120,
  "v24_direct_two_facing_visual_comparison":80,
  "v24_new_facing_original_source":160,
  "v24_source_original_pixel_proof":466,
  "v24_entire_820_multitile_candidate_coverage":820,
  "v24_remaining_340_multitile_candidate_queue":340}
 for t,n in preserved.items():assert cnt(c,t)==n,(t,cnt(c,t),n)
 old_source={}
 for version,table in [(21,"v21_direct_multisprite_grid_visual_observation"),
                       (22,"v22_new_facing_original_grid"),
                       (23,"v23_new_facing_original_source"),
                       (24,"v24_new_facing_original_source")]:
  for r in qr(c,"SELECT group_id,Facing FROM "+table):
   key=(r["group_id"],r["Facing"])
   assert key not in old_source,key
   old_source[key]=version
 assert len(old_source)==480
 paired_before={}
 for version,table in [(22,"v22_direct_two_facing_visual_comparison"),
                       (23,"v23_direct_two_facing_visual_comparison"),
                       (24,"v24_direct_two_facing_visual_comparison")]:
  for r in qr(c,"SELECT group_id FROM "+table):
   assert r["group_id"] not in paired_before
   paired_before[r["group_id"]]=version
 assert len(paired_before)==200
 rect={(r["group_id"],r["Facing"]):r for r in qr(c,
  "SELECT group_id,Facing,raw_sprite_part_count,grid_w,grid_h,source_only_group,original_png_parts_mapped FROM v21_all_source_rectangle_template WHERE raw_sprite_part_count>=2")}
 assert len(rect)==820
 bygroup=defaultdict(set)
 for g,f in rect:bygroup[g].add(f)
 assert len(bygroup)==346
 multi={g for g,faces in bygroup.items() if len(faces)>=2}
 assert len(multi)==274 and set(paired_before).issubset(multi)
 assert {r["group_id"] for r in pairs}==multi-set(paired_before)
 prev24=qr(c,"SELECT group_id,Facing,original_grid_visually_viewed FROM v24_entire_820_multitile_candidate_coverage")
 assert len(prev24)==820 and sum(r["original_grid_visually_viewed"] for r in prev24)==480
 tile={r["source_key"]:r for r in qr(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 raw={(r["group_id"],r["Facing"],r["source_key"]):r for r in qr(c,
  "SELECT group_id,Facing,source_key,original_grid,relative_x_when_available,relative_y_when_available FROM v12_tile_proof")}
 partproof={(r["group_id"],r["Facing"],r["source_key"]):r for r in qr(c,
  "SELECT group_id,Facing,source_key,raw_sprite_grid_pos,relative_x,relative_y,original_png_path,atlas_col,atlas_row,original_cell_w,original_cell_h,container_type_original,container_capacity_original FROM v21_source_tile_positioned_png")}
 c.executescript("""
 CREATE TABLE v25_direct_paired_visual_observation(
  pair_no INTEGER PRIMARY KEY,group_id TEXT UNIQUE,original_reference_name TEXT,
  source_only_group INTEGER,Facing_A TEXT,Facing_B TEXT,
  raw_grid_A TEXT,raw_grid_B TEXT,parts_A INTEGER,parts_B INTEGER,
  facing_A_previously_seen INTEGER,facing_B_previously_seen INTEGER,
  newly_viewed_direction_count INTEGER,
  broad_visible_subject TEXT,visual_category_scope TEXT,
  visual_relation_and_uncertainty TEXT,
  source_png_pair_visually_inspected INTEGER DEFAULT 1,
  real_game_object_same_as_other_facing_certified INTEGER DEFAULT 0,
  official_runtime_game_furniture_ID_certified INTEGER DEFAULT 0);
 CREATE TABLE v25_pair_facing_source_grid(
  pair_no INTEGER,group_id TEXT,Facing TEXT,face_slot TEXT,
  grid_w INTEGER,grid_h INTEGER,original_tile_part_count INTEGER,
  original_source_keys_json TEXT,previously_directly_viewed INTEGER,
  newly_viewed_v25 INTEGER,
  real_game_object_ID_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v25_per_sprite_original_png_sha256(
  pair_no INTEGER,face_slot TEXT,group_id TEXT,Facing TEXT,source_key TEXT,
  original_source_grid TEXT,relative_x INTEGER,relative_y INTEGER,
  original_png_path TEXT,original_png_sha256 TEXT,original_pixel_crop_sha256 TEXT,
  atlas_column INTEGER,atlas_row INTEGER,png_cell_w INTEGER,png_cell_h INTEGER,
  pixel_crop_completed INTEGER DEFAULT 1,
  previously_reviewed_facing_reused INTEGER,
  newly_reviewed_v25_facing INTEGER,
  exact_runtime_object_ID_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v25_all_820_multitile_direction_visual_ledger(
  group_id TEXT,Facing TEXT,original_sprite_parts INTEGER,
  original_grid_w INTEGER,original_grid_h INTEGER,source_only_group INTEGER,
  image_review_source_version TEXT,source_grid_pixels_visually_checked INTEGER,
  paired_two_facing_visual_comparison_completed INTEGER,
  exact_game_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v25_235_remaining_direction_queue(
  group_id TEXT,Facing TEXT,source_parts INTEGER,raw_grid_w INTEGER,raw_grid_h INTEGER,
  source_only_group INTEGER,original_png_indexed_parts INTEGER,
  game_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v25_all_274_multifacing_group_pair_coverage(
  group_id TEXT PRIMARY KEY,original_multitile_facing_count INTEGER,
  source_group_pair_observation_version TEXT,
  original_png_two_facing_grids_directly_visually_compared INTEGER DEFAULT 1,
  in_game_same_object_across_directions_certified INTEGER DEFAULT 0);
 CREATE TABLE v25_scope_limited_progress(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,percent REAL,
  evidence_scope TEXT,interpretation TEXT);
 """)
 paired=[];newfacings=set();reused=set()
 for i in range(1,75):
  p=idpairs[i];lab=labs[i];g=p["group_id"]
  assert g not in paired_before and g in multi
  a,b=p["Facing_A"],p["Facing_B"]
  assert a!=b and (g,a) in rect and (g,b) in rect
  aw,ah=map(int,p["grid_A"].split("x"))
  bw,bh=map(int,p["grid_B"].split("x"))
  assert (aw,ah)==(rect[(g,a)]["grid_w"],rect[(g,a)]["grid_h"])
  assert (bw,bh)==(rect[(g,b)]["grid_w"],rect[(g,b)]["grid_h"])
  assert int(p["part_count_A"])==rect[(g,a)]["raw_sprite_part_count"]
  assert int(p["part_count_B"])==rect[(g,b)]["raw_sprite_part_count"]
  status_a=int((g,a) in old_source);status_b=int((g,b) in old_source)
  assert status_a==int(p["A_previously_viewed"]) and status_b==int(p["B_previously_viewed"])
  assert status_a+status_b in (0,1)
  assert int(p["number_new_facing_views"])==2-status_a-status_b
  info=dict(pair_no=i,group_id=g,original_reference_name=p["original_reference_name"],
   source_only_group=int(p["source_only_group"]),Facing_A=a,Facing_B=b,
   raw_grid_A=p["grid_A"],raw_grid_B=p["grid_B"],
   parts_A=int(p["part_count_A"]),parts_B=int(p["part_count_B"]),
   facing_A_previously_seen=status_a,facing_B_previously_seen=status_b,
   newly_viewed_direction_count=int(p["number_new_facing_views"]),
   broad_visible_subject=lab["observed_broad_subject"],
   visual_category_scope=lab["visual_category_scope"],
   visual_relation_and_uncertainty=lab["observed_two_facing_visual_relation"])
  put(c,"v25_direct_paired_visual_observation",info);paired.append(info)
 part_group=defaultdict(set)
 for p in partrows:
  g,f,key=p["group_id"],p["Facing"],p["source_key"]
  loc=(g,f,key)
  assert loc in raw and loc in partproof and key in tile
  proof=partproof[loc];o=raw[loc];s=tile[key]
  assert p["raw_sprite_grid_pos"]==proof["raw_sprite_grid_pos"]==o["original_grid"]==s["SpriteGridPos"]
  assert s["group_id"]==g
  assert int(p["relative_x"])==proof["relative_x"]==o["relative_x_when_available"]
  assert int(p["relative_y"])==proof["relative_y"]==o["relative_y_when_available"]
  assert p["original_png_path"]==proof["original_png_path"]
  assert int(p["atlas_col"])==proof["atlas_col"] and int(p["atlas_row"])==proof["atlas_row"]
  assert int(p["original_cell_w"])==proof["original_cell_w"] and int(p["original_cell_h"])==proof["original_cell_h"]
  assert p["container_type_original"]==(proof["container_type_original"] or "")
  assert p["container_capacity_original"]==(proof["container_capacity_original"] or "")
  assert key not in part_group[(g,f)]
  part_group[(g,f)].add(key)
 assert len(part_group)==148
 facesout=[]
 for p in faceplan:
  i=int(p["pair_no"]);g=p["group_id"];f=p["Facing"];slot=p["face_slot"]
  assert i in idpairs and idpairs[i]["group_id"]==g and f==idpairs[i]["Facing_"+slot]
  assert (g,f) in rect and len(part_group[(g,f)])==rect[(g,f)]["raw_sprite_part_count"]
  assert set(json.loads(p["source_keys_json"]))==part_group[(g,f)]
  old=int((g,f) in old_source)
  assert old==int(p["previously_directly_viewed"]) and 1-old==int(p["new_v25_view"])
  rec=dict(pair_no=i,group_id=g,Facing=f,face_slot=slot,
    grid_w=int(p["width"]),grid_h=int(p["height"]),
    original_tile_part_count=int(p["source_parts"]),
    original_source_keys_json=p["source_keys_json"],
    previously_directly_viewed=old,newly_viewed_v25=1-old)
  assert (rec["grid_w"],rec["grid_h"])==(rect[(g,f)]["grid_w"],rect[(g,f)]["grid_h"])
  put(c,"v25_pair_facing_source_grid",rec);facesout.append(rec)
  if old:
   assert (g,f) not in reused;reused.add((g,f))
  else:
   assert (g,f) not in newfacings;newfacings.add((g,f))
 assert len(facesout)==148 and len(reused)==43 and len(newfacings)==105
 assert not newfacings.intersection(old_source) and reused.issubset(old_source)
 pixids=set();pixout=[]
 for p in pngpixels:
  i=int(p["pair_no"]);g,f,key=p["group_id"],p["Facing"],p["source_key"]
  loc=(g,f,key)
  assert i in idpairs and g==idpairs[i]["group_id"]
  assert loc in partproof and loc not in pixids and key in part_group[(g,f)]
  assert p["official_game_furniture_identity_certified"]=="0"
  assert len(p["exact_original_png_sha256"])==len(p["exact_pixel_cell_sha256"])==64
  original=partproof[loc]
  assert p["raw_sprite_grid_pos"]==original["raw_sprite_grid_pos"]
  assert p["original_png_path"]==original["original_png_path"]
  assert int(p["relative_x"])==original["relative_x"] and int(p["relative_y"])==original["relative_y"]
  assert int(p["atlas_col"])==original["atlas_col"] and int(p["atlas_row"])==original["atlas_row"]
  old=int((g,f) in old_source)
  assert old==int(p["previously_viewed_at_prior_version"])
  assert 1-old==int(p["counted_new_facing_v25"])
  rec=dict(pair_no=i,face_slot=p["face_slot"],group_id=g,Facing=f,source_key=key,
   original_source_grid=p["raw_sprite_grid_pos"],
   relative_x=int(p["relative_x"]),relative_y=int(p["relative_y"]),
   original_png_path=p["original_png_path"],
   original_png_sha256=p["exact_original_png_sha256"],
   original_pixel_crop_sha256=p["exact_pixel_cell_sha256"],
   atlas_column=int(p["atlas_col"]),atlas_row=int(p["atlas_row"]),
   png_cell_w=int(p["original_cell_w"]),png_cell_h=int(p["original_cell_h"]),
   previously_reviewed_facing_reused=old,newly_reviewed_v25_facing=1-old)
  put(c,"v25_per_sprite_original_png_sha256",rec);pixout.append(rec);pixids.add(loc)
 assert len(pixout)==476 and pixids=={(g,f,key) for (g,f),keys in part_group.items() for key in keys}
 assert sum(p["newly_reviewed_v25_facing"] for p in pixout)==300
 assert sum(p["previously_reviewed_facing_reused"] for p in pixout)==176
 allseen=set(old_source)|newfacings
 assert len(allseen)==585
 assert len({g for g,f in allseen})==311
 prevpaired=set(paired_before)
 newpaired={p["group_id"] for p in paired}
 assert len(newpaired)==74 and not (newpaired&prevpaired)
 assert newpaired|prevpaired==multi and len(newpaired|prevpaired)==274
 complete=[];pending=[]
 for (g,f),r in sorted(rect.items()):
  if (g,f) in old_source:status="DIRECT_ORIGINAL_GRID_V"+str(old_source[(g,f)])
  elif (g,f) in newfacings:status="NEW_DIRECT_ORIGINAL_GRID_V25"
  else:status="NO_DIRECT_ORIGINAL_GRID_REVIEW"
  viewed=int((g,f) in allseen)
  cmp=int(g in prevpaired or g in newpaired)
  rec=dict(group_id=g,Facing=f,original_sprite_parts=r["raw_sprite_part_count"],
   original_grid_w=r["grid_w"],original_grid_h=r["grid_h"],
   source_only_group=r["source_only_group"],image_review_source_version=status,
   source_grid_pixels_visually_checked=viewed,
   paired_two_facing_visual_comparison_completed=cmp)
  put(c,"v25_all_820_multitile_direction_visual_ledger",rec);complete.append(rec)
  if not viewed:
   q=dict(group_id=g,Facing=f,source_parts=r["raw_sprite_part_count"],
    raw_grid_w=r["grid_w"],raw_grid_h=r["grid_h"],
    source_only_group=r["source_only_group"],
    original_png_indexed_parts=r["original_png_parts_mapped"])
   put(c,"v25_235_remaining_direction_queue",q);pending.append(q)
 assert len(complete)==820 and len(pending)==235
 assert sum(x["source_grid_pixels_visually_checked"] for x in complete)==585
 assert sum(x["paired_two_facing_visual_comparison_completed"] for x in complete)==sum(len(bygroup[g]) for g in multi)
 grouprecs=[]
 for g in sorted(multi):
  version=paired_before.get(g,25)
  rec=dict(group_id=g,original_multitile_facing_count=len(bygroup[g]),
   source_group_pair_observation_version="V"+str(version))
  put(c,"v25_all_274_multifacing_group_pair_coverage",rec);grouprecs.append(rec)
 assert len(grouprecs)==274
 category=Counter(p["broad_visible_subject"] for p in paired)
 kind=Counter(p["visual_category_scope"] for p in paired)
 assert sum(category.values())==sum(kind.values())==74
 metrics=[
  ("currently_indexed_Wiki_and_TileDef_candidate_registry",2231,2231,"REGISTRY_ROWS_ONLY","Wiki possibly stale; not game furniture census"),
  ("source_only_one_original_sprite_direct_visual",940,963,"ONE_ORIGINAL_SPRITE","23 sprite atlas links unresolved"),
  ("source_direction_grid_geometry_templates",3840,3840,"RAW_GEOMETRY","not game object identity"),
  ("genuine_multitile_rectangle_group_facing_candidates",820,820,"SOURCE_GRID_CANDIDATES","may include signs, hides and non-furniture"),
  ("direct_multitile_direction_grid_visual_review",585,820,"DIRECT_ORIGINAL_PNG_GRID","105 new v25, excludes 43 reused previous facings"),
  ("new_distinct_v25_facing_grid_visual_review",105,820,"NEW_IMAGE_REVIEW","74 group pairs containing 43 reused previous facings"),
  ("original_multitile_source_groups_with_at_least_one_review",311,346,"SOURCE_GROUP","not unique game furniture identities"),
  ("multi_facing_source_groups_with_two_directly_compared_facings",274,274,"SOURCE_PAIR_COVERAGE","not in-game facing equivalence"),
  ("original_png_part_pixel_sha_records_v25",476,476,"ORIGINAL_PIXEL_CROP","300 from newly reviewed facings, 176 reused"),
  ("original_warning_cases_resolved",0,474,"UNRESOLVED","no source warnings cleared"),
  ("source_only_png_atlas_mapping_gaps_resolved",0,23,"UNRESOLVED","not cleared"),
  ("official_runtime_game_object_identity_certified",0,0,"UNKNOWN_DENOMINATOR","needs independent in-game provenance")
 ]
 metricrecs=[]
 for k,n,den,scope,note in metrics:
  rec=dict(metric_key=k,numerator=n,denominator=den,percent=round(100*n/den,2) if den else None,
   evidence_scope=scope,interpretation=note)
  put(c,"v25_scope_limited_progress",rec);metricrecs.append(rec)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
 for tab,n in {**preserved,"v25_direct_paired_visual_observation":74,
  "v25_pair_facing_source_grid":148,"v25_per_sprite_original_png_sha256":476,
  "v25_all_820_multitile_direction_visual_ledger":820,
  "v25_235_remaining_direction_queue":235,
  "v25_all_274_multifacing_group_pair_coverage":274,
  "v25_scope_limited_progress":12}.items():
  assert cnt(c,tab)==n,(tab,cnt(c,tab),n)
 assert c.execute("""SELECT COUNT(*) FROM v25_direct_paired_visual_observation
 WHERE real_game_object_same_as_other_facing_certified!=0 OR official_runtime_game_furniture_ID_certified!=0""").fetchone()[0]==0
 c.close()
 write("V25_74_DIRECT_TWO_FACING_VISUAL_COMPARISONS.csv",paired)
 write("V25_148_DIRECTION_PROOF_WITH_43_REUSED.csv",facesout)
 write("V25_476_ORIGINAL_SPRITE_PIXEL_SHA256.csv",pixout)
 write("V25_ALL_820_DIRECTION_REVIEW_LEDGER.csv",complete)
 write("V25_235_UNREVIEWED_DIRECTION_QUEUE.csv",pending)
 write("V25_274_MULTIFACING_GROUP_PAIR_COVERAGE.csv",grouprecs)
 write("V25_12_SCOPED_PROGRESS.csv",metricrecs)
 manifest=dict(version="v25",
  input_v24_complete_sqlite_zip_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
  original_TileDef_raw_property_rows=195265,original_source_slots=73644,
  current_registered_candidate_rows=2231,source_candidate_tile_keys=8219,
  source_direction_geometry_templates=3840,multitile_source_group_facing_candidates=820,
  source_multitile_unique_groups=346,eligible_two_plus_facing_source_groups=274,
  previous_directly_viewed_group_facing_candidates=480,
  v25_new_distinct_group_facing_views=105,
  v25_previous_views_reused_for_pair_comparison=43,
  v25_total_pair_contact_source_grid_views=148,
  v25_new_source_group_pairs=74,v25_prior_source_group_pairs=200,
  v25_completely_new_source_groups_before_review=31,
  v25_existing_once_reviewed_source_groups_before_review=43,
  v25_directly_cropped_original_png_tile_cells=476,
  v25_original_png_tile_cells_from_newly_reviewed_facing_grids=300,
  v25_original_png_tile_cells_from_reused_previous_facing_grids=176,
  v25_original_png_atlases_sha_verified=stage["original_png_atlases_verified"],
  v25_ten_direct_contact_images_sha_verified=True,
  cumulative_directly_reviewed_multitile_group_facing_candidates=585,
  source_multitile_direct_grid_image_review_percent=round(100*585/820,2),
  source_multitile_direction_candidates_remaining=235,
  source_multitile_unique_groups_at_least_one_facing_reviewed=311,
  source_multitile_group_representative_visual_coverage_pct=round(100*311/346,2),
  multi_facing_source_groups_with_two_directions_compared=274,
  multi_facing_source_group_pair_visual_review_percent=100.0,
  v25_broad_visual_subject_counts=dict(sorted(category.items())),
  v25_visual_category_scope_counts=dict(sorted(kind.items())),
  old_source_only_one_cell_direct_visual_reviewed=940,
  old_474_raw_warnings_unresolved=True,old_23_png_mapping_gaps_unresolved=True,
  original_wiki_can_be_stale_or_incomplete=True,
  prior_Work_107_groups_574_tiles_without_group_ID_evidence_not_included=True,
  first_party_game_object_identification_certified=0,
  isometric_complete_game_object_assembly_certified=0,
  actual_game_object_cross_facing_equivalence_certified=0,
  Lua_TMX_Minecraft_not_started=True,
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
  "# PZ B42 가구 원본 방향 검수 v25 — 274/274 다방향 그룹의 2방향 직접 이미지 비교 완료\n\n"
  "v24 전체 SQLite/원본 TileDef·Wiki 참고·840이 아닌 **820**개 2+ 타일 방향 후보·기존 모든 원본과 경고 근거를 복제 보존.\n"
  "남은 두 방향 미비교 그룹 74개를 원본 PNG 그리드 148개로 시각 검사함. 31개 그룹은 둘 다 신규(62방향), 43개 그룹은 이미 본 A방향을 비교 이미지에 재사용하고 B방향만 신규(43방향).\n"
  "따라서 **신규 방향 시각 검수는 105건**이며, 중복 43개를 추가 실적에 합산하지 않았음. 기존 480+신규 105=**585/820(71.34%)**, 나머지 235개 방향 후보를 신규 원본 개별 큐에 보존.\n"
  "최소 한 방향 이미지가 검수된 원본 그룹은 311/346=89.88%, 두 방향 이상 가진 그룹의 두 방향 시각 비교는 274/274=100%.\n"
  "10개 원본 접촉 시트·476개의 개별 원본 타일 이미지 픽셀 해시·33개 원본 PNG 아틀라스 출처를 남김. 이전 조회 43방향에 해당하는 176개 픽셀 해시도 중복임을 별도 표기.\n"
  "선정된 그룹에는 의료침대, 치과설비, 테이블, 텐트, 포스터, 간판, 동물 가죽과 바닥 러그 등 여러 유형이 섞여 있음. 분류는 외형 관찰에 한정.\n"
  "원본 SpriteGridPos 직사각형, 비슷한 그림, 위키 설명만으로 같은 런타임 게임 오브젝트라고 인증하지 않음. 4방향 동등성/완성 가구 런타임 검증은 0.\n"
  "위키 최신성/완전성 미보장. 474개 원본 경고, 23개 PNG 매핑 미연결은 미해결 유지. Lua/TMX/Minecraft 구현 보류.\n",encoding="utf8")
 with zipfile.ZipFile(ZIP,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for fp in sorted(OUT.iterdir()):
   if fp.is_file() and fp!=ZIP and not fp.name.startswith("STAGED_") and not fp.name.endswith("_BASE64.txt") and not fp.name.startswith("_required_"):
    z.write(fp,fp.name)
 with zipfile.ZipFile(ZIP) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V25_ALL_274_MULTI_FACE_GROUPS_COMPARE_105_NEW_FACE_GRIDS_585_OF_820_REVIEWED_476_ORIGINAL_TILE_SHA_SQLITE_ZIP_PASSED",J(manifest),flush=True)
if __name__=="__main__":main()
