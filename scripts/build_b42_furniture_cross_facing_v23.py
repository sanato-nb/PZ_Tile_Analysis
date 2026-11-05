#!/usr/bin/env python3
"""Project Zomboid B42 v23: new 60 two-facing visual reviews, independent source crosschecks.
Input: full v22 SQLite ZIP + directly inspected six original-PNG contact sheets.
Never claim that related pixels or Wiki names certify a runtime game object.
"""
import csv,hashlib,json,shutil,sqlite3,zipfile
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v22/B42_FURNITURE_CROSS_FACING_REVIEW_V22.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v23"
DB=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V23.sqlite"
PACK=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V23.zip"
def qr(c,sql,args=()):return [dict(x) for x in c.execute(sql,args)]
def cnt(c,table):return c.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
def js(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def put(c,tab,row):
 keys=list(row)
 c.execute("INSERT INTO "+tab+"("+",".join(keys)+") VALUES("+",".join("?" for _ in keys)+")",list(row.values()))
def csv_in(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def csv_out(name,records):
 assert records,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
def main():
 assert OLD.is_file() and OUT.is_dir() and not DB.exists()
 staging=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert staging["previous_direct_grid_visual_candidates"]==200
 assert staging["new_distinct_pair_groups"]==60 and staging["new_direction_candidates"]==120
 assert staging["new_direction_overlaps_with_v21_v22"]==0
 assert staging["new_group_overlaps_with_v21_v22"]==0
 assert staging["all_new_source_tile_crops_verified"]==256
 pairs=csv_in("V23_60_PAIR_SELECTION_SOURCE_ONLY.csv")
 facing=csv_in("V23_120_FACING_GRID_CANDIDATES.csv")
 parts=csv_in("V23_SELECTED_ORIGINAL_PART_POSITIONS.csv")
 pixels=csv_in("V23_DIRECT_ORIGINAL_SOURCE_PIXEL_SHA256.csv")
 labels=csv_in("V23_60_DIRECT_PAIRED_VISUAL_CLASSIFICATIONS.csv")
 assert len(pairs)==len(labels)==60
 assert len(facing)==120
 assert len(parts)==len(pixels)==256
 bypair={int(x["pair_no"]):x for x in pairs}
 bylab={int(x["pair_no"]):x for x in labels}
 assert set(bypair)==set(bylab)==set(range(1,61))
 for lab in labels:
  assert lab["observation_scope"]=="DIRECT_VIEW_OF_TWO_ORIGINAL_PNG_SOURCE_DIRECTION_GRIDS"
  assert lab["confirmed_exact_game_object_identity"]=="0"
  assert lab["visual_similarity_scope"]=="CANDIDATE_RELATED_DESIGN_NOT_GAME_OBJECT_PROOF"
 contact_shas=staging["original_pair_contact_sha256"]
 assert len(contact_shas)==6
 for fn,sha in contact_shas.items():
  assert hashlib.sha256((OUT/fn).read_bytes()).hexdigest()==sha,(fn,"contact_sheet_sha_changed")
 with zipfile.ZipFile(OLD) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CROSS_FACING_REVIEW_V22.sqlite") as a,DB.open("wb") as b:
   shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 preserved={
  "source_attributes":195265,"source_slots":73644,"furniture_tile":8219,
  "registry_entry":2231,"wiki_furniture":1268,"v12_template_proof":3840,
  "v13_warning_case":474,"v14_source_only_ledger":963,
  "v20_master_furniture_registry":2231,
  "v21_all_source_rectangle_template":843,
  "v21_source_tile_positioned_png":2221,
  "v21_direct_multisprite_grid_visual_observation":80,
  "v21_reviewed_multisprite_pixel_sha":335,
  "v22_direct_two_facing_visual_comparison":60,
  "v22_new_facing_original_grid":120,
  "v22_original_sprite_pixel_sha":258,
  "v22_remaining_multitile_direction_queue":620
 }
 for t,n in preserved.items():assert cnt(c,t)==n,(t,cnt(c,t),n)
 old21=qr(c,"SELECT group_id,Facing FROM v21_direct_multisprite_grid_visual_observation")
 old22=qr(c,"SELECT group_id,Facing FROM v22_new_facing_original_grid")
 oldpairs=qr(c,"SELECT group_id FROM v22_direct_two_facing_visual_comparison")
 old_seen={(x["group_id"],x["Facing"]) for x in old21+old22}
 old_groups={x["group_id"] for x in old21+old22}
 assert len(old_seen)==200 and len(old_groups)==140
 prior22_group={x["group_id"] for x in oldpairs}
 assert len(prior22_group)==60
 source_rect={(x["group_id"],x["Facing"]):x for x in qr(c,
  "SELECT group_id,Facing,raw_sprite_part_count,grid_w,grid_h,source_only_group,original_png_parts_mapped FROM v21_all_source_rectangle_template WHERE raw_sprite_part_count>=2")}
 assert len(source_rect)==820
 original_parts={(x["group_id"],x["Facing"],x["source_key"]):x for x in qr(c,
  "SELECT group_id,Facing,source_key,raw_sprite_grid_pos,relative_x,relative_y,original_png_path,atlas_col,atlas_row,original_cell_w,original_cell_h FROM v21_source_tile_positioned_png")}
 original_tile={x["source_key"]:x for x in qr(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 original_grid={(x["group_id"],x["Facing"],x["source_key"]):x for x in qr(c,
  "SELECT group_id,Facing,source_key,original_grid,relative_x_when_available,relative_y_when_available FROM v12_tile_proof")}
 v22_queue={(x["group_id"],x["Facing"]) for x in qr(c,"SELECT group_id,Facing FROM v22_remaining_multitile_direction_queue")}
 assert len(v22_queue)==620
 c.executescript("""
 CREATE TABLE v23_direct_two_facing_visual_comparison(
  pair_no INTEGER PRIMARY KEY,group_id TEXT UNIQUE,original_display_name TEXT,
  source_only_group INTEGER,Facing_A TEXT,Facing_B TEXT,
  grid_A TEXT,grid_B TEXT,parts_A INTEGER,parts_B INTEGER,
  broad_visible_subject TEXT,observed_two_facing_relation TEXT,
  direct_original_pair_viewed INTEGER DEFAULT 1,
  visual_similarity_not_runtime_proof INTEGER DEFAULT 1,
  dimensions_swapped_between_facings INTEGER DEFAULT 0,
  same_game_object_certified INTEGER DEFAULT 0,
  exact_runtime_game_object_ID_certified INTEGER DEFAULT 0);
 CREATE TABLE v23_new_facing_original_source(
  pair_no INTEGER,group_id TEXT,Facing TEXT,face_slot TEXT,
  width INTEGER,height INTEGER,original_part_count INTEGER,
  source_keys_json TEXT,all_source_positions_individually_verified INTEGER DEFAULT 1,
  official_object_identity_verified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v23_source_original_pixel_proof(
  pair_no INTEGER,face_slot TEXT,group_id TEXT,Facing TEXT,source_key TEXT,
  raw_sprite_grid_pos TEXT,relative_x INTEGER,relative_y INTEGER,
  original_png_path TEXT,original_png_sha256 TEXT,original_crop_pixel_sha256 TEXT,
  atlas_column INTEGER,atlas_row INTEGER,cell_width INTEGER,cell_height INTEGER,
  directly_cropped_from_source_png INTEGER DEFAULT 1,
  official_game_object_identity_verified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v23_entire_820_multitile_candidate_coverage(
  group_id TEXT,Facing TEXT,raw_part_count INTEGER,
  grid_w INTEGER,grid_h INTEGER,source_only_group INTEGER,
  representative_sprite_grid_visual_status TEXT,
  directly_viewed_grid INTEGER DEFAULT 0,
  visual_two_facing_comparison_available INTEGER DEFAULT 0,
  exact_game_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v23_remaining_500_multitile_candidate_queue(
  group_id TEXT,Facing TEXT,raw_part_count INTEGER,grid_w INTEGER,grid_h INTEGER,
  source_only_group INTEGER,original_png_cell_count INTEGER,
  whole_game_object_identified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v23_progress_scope(
  metric_key TEXT PRIMARY KEY,done INTEGER,total INTEGER,percentage REAL,
  scope TEXT,interpretation TEXT);
 """)
 seen_new=set();seen_new_groups=set();reports=[];facerecs=[];pixrecs=[]
 for i in range(1,61):
  p=bypair[i];lab=bylab[i];g=p["group_id"]
  assert g not in old_groups and g not in seen_new_groups
  f1,f2=p["Facing_A"],p["Facing_B"]
  assert f1!=f2 and (g,f1) in source_rect and (g,f2) in source_rect
  assert (g,f1) in v22_queue and (g,f2) in v22_queue
  assert int(p["source_part_count_A"])==source_rect[(g,f1)]["raw_sprite_part_count"]
  assert int(p["source_part_count_B"])==source_rect[(g,f2)]["raw_sprite_part_count"]
  aw,ah=map(int,p["original_grid_A"].split("x"))
  bw,bh=map(int,p["original_grid_B"].split("x"))
  assert (aw,ah)==(source_rect[(g,f1)]["grid_w"],source_rect[(g,f1)]["grid_h"])
  assert (bw,bh)==(source_rect[(g,f2)]["grid_w"],source_rect[(g,f2)]["grid_h"])
  swapped=int(aw==bh and ah==bw and (aw,ah)!=(bw,bh))
  r=dict(pair_no=i,group_id=g,original_display_name=p["original_name"],
   source_only_group=int(p["source_only_group"]),Facing_A=f1,Facing_B=f2,
   grid_A=p["original_grid_A"],grid_B=p["original_grid_B"],
   parts_A=int(p["source_part_count_A"]),parts_B=int(p["source_part_count_B"]),
   broad_visible_subject=lab["observed_broad_visual_subject"],
   observed_two_facing_relation=lab["observed_two_facing_relation"],
   dimensions_swapped_between_facings=swapped)
  put(c,"v23_direct_two_facing_visual_comparison",r);reports.append(r)
  seen_new_groups.add(g)
 assert len(reports)==60
 expected_part_keys=defaultdict(set)
 for part in parts:
  g,f,key=part["group_id"],part["Facing"],part["source_key"]
  loc=(g,f,key)
  assert loc in original_parts and loc in original_grid
  ref=original_parts[loc];old=original_grid[loc];source=original_tile[key]
  assert part["raw_sprite_grid_pos"]==ref["raw_sprite_grid_pos"]==old["original_grid"]==source["SpriteGridPos"]
  assert int(part["relative_x"])==ref["relative_x"]==old["relative_x_when_available"]
  assert int(part["relative_y"])==ref["relative_y"]==old["relative_y_when_available"]
  assert part["original_png_path"]==ref["original_png_path"]
  assert int(part["atlas_col"])==ref["atlas_col"] and int(part["atlas_row"])==ref["atlas_row"]
  assert int(part["original_cell_w"])==ref["original_cell_w"]
  assert int(part["original_cell_h"])==ref["original_cell_h"]
  assert source["group_id"]==g
  assert key not in expected_part_keys[(g,f)]
  expected_part_keys[(g,f)].add(key)
 assert len(expected_part_keys)==120
 for f in facing:
  group,face=f["group_id"],f["Facing"];pairno=int(f["pair_no"]);slot=f["face_slot"]
  assert slot in ("A","B") and pairno in bypair
  assert bypair[pairno]["group_id"]==group
  assert face==bypair[pairno]["Facing_"+slot]
  assert (group,face) not in old_seen and (group,face) not in seen_new
  rect=source_rect[(group,face)]
  assert int(f["width"])==rect["grid_w"] and int(f["height"])==rect["grid_h"]
  assert int(f["original_parts"])==rect["raw_sprite_part_count"]
  assert set(json.loads(f["original_keys_json"]))==expected_part_keys[(group,face)]
  record=dict(pair_no=pairno,group_id=group,Facing=face,face_slot=slot,
   width=int(f["width"]),height=int(f["height"]),
   original_part_count=int(f["original_parts"]),source_keys_json=f["original_keys_json"])
  put(c,"v23_new_facing_original_source",record);facerecs.append(record)
  seen_new.add((group,face))
 assert len(seen_new)==120 and len({g for g,f in seen_new})==60
 assert not old_seen.intersection(seen_new)
 px_ids=set()
 for p in pixels:
  group,face,key=p["group_id"],p["Facing"],p["source_key"]
  loc=(group,face,key)
  assert (group,face) in seen_new
  assert key in expected_part_keys[(group,face)] and loc not in px_ids
  assert p["actual_original_pixels_cropped"]=="1" and p["actual_in_game_object_certified"]=="0"
  assert p["raw_grid"]==original_parts[loc]["raw_sprite_grid_pos"]
  assert int(p["relative_x"])==original_parts[loc]["relative_x"]
  assert int(p["relative_y"])==original_parts[loc]["relative_y"]
  assert p["png_path"]==original_parts[loc]["original_png_path"]
  assert len(p["original_png_sha256"])==64 and len(p["png_cell_pixel_sha256"])==64
  record=dict(pair_no=int(p["pair_no"]),face_slot=p["face_slot"],
   group_id=group,Facing=face,source_key=key,raw_sprite_grid_pos=p["raw_grid"],
   relative_x=int(p["relative_x"]),relative_y=int(p["relative_y"]),
   original_png_path=p["png_path"],original_png_sha256=p["original_png_sha256"],
   original_crop_pixel_sha256=p["png_cell_pixel_sha256"],
   atlas_column=int(p["atlas_col"]),atlas_row=int(p["atlas_row"]),
   cell_width=int(p["cell_w"]),cell_height=int(p["cell_h"]))
  put(c,"v23_source_original_pixel_proof",record);pixrecs.append(record)
  px_ids.add(loc)
 assert px_ids=={(g,f,k) for (g,f),ks in expected_part_keys.items() for k in ks}
 assert len(pixrecs)==256
 coverage=[];pending=[]
 for (g,f),rec in sorted(source_rect.items()):
  if (g,f) in old_seen:
   status="PREVIOUS_V21_SINGLE_FACING_VIEW" if (g,f) in {(x["group_id"],x["Facing"]) for x in old21} else "PREVIOUS_V22_PAIRED_FACING_VIEW"
  elif (g,f) in seen_new:status="CURRENT_V23_PAIRED_FACING_VIEW"
  else:status="NOT_DIRECTLY_VISUALLY_REVIEWED"
  viewed=int((g,f) in old_seen or (g,f) in seen_new)
  paired=int(status in ("PREVIOUS_V22_PAIRED_FACING_VIEW","CURRENT_V23_PAIRED_FACING_VIEW"))
  row=dict(group_id=g,Facing=f,raw_part_count=rec["raw_sprite_part_count"],
   grid_w=rec["grid_w"],grid_h=rec["grid_h"],source_only_group=rec["source_only_group"],
   representative_sprite_grid_visual_status=status,directly_viewed_grid=viewed,
   visual_two_facing_comparison_available=paired)
  put(c,"v23_entire_820_multitile_candidate_coverage",row);coverage.append(row)
  if not viewed:
   p=dict(group_id=g,Facing=f,raw_part_count=rec["raw_sprite_part_count"],
    grid_w=rec["grid_w"],grid_h=rec["grid_h"],
    source_only_group=rec["source_only_group"],
    original_png_cell_count=rec["original_png_parts_mapped"])
   put(c,"v23_remaining_500_multitile_candidate_queue",p);pending.append(p)
 assert len(coverage)==820 and len(pending)==500
 assert sum(x["directly_viewed_grid"] for x in coverage)==320
 assert sum(x["visual_two_facing_comparison_available"] for x in coverage)==240
 all_groups={g for g,f in source_rect}
 assert len(all_groups)==346
 by_groups=defaultdict(set)
 for g,f in source_rect:by_groups[g].add(f)
 multi_facings=sum(len(facings)>=2 for facings in by_groups.values())
 assert multi_facings==274
 all_view_groups={g for g,f in old_seen|seen_new}
 assert len(all_view_groups)==200
 new_class=Counter(x["broad_visible_subject"] for x in reports)
 assert sum(new_class.values())==60
 metrics=[
  ("currently_collected_candidate_registry_rows",2231,2231,"SOURCE_REGISTRY_ONLY","not game furniture census"),
  ("source_only_representative_single_sprite_review",940,963,"ONE_SOURCE_PIXEL_CELL","23 source-only atlas mappings missing"),
  ("original_source_grid_direction_templates",3840,3840,"SOURCE_GEOMETRY_ONLY","group x facing candidates"),
  ("genuine_multitile_rectangle_source_candidates",820,820,"TWO_OR_MORE_PARTS","includes non-furniture graphics"),
  ("all_v21_v22_v23_direct_original_grid_views",320,820,"DIRECT_GRID_IMAGE_REVIEW","not identity certification"),
  ("new_v23_direction_grid_views",120,820,"DIRECT_TWO_FACING_VIEW","60 new groups x 2 directions"),
  ("multi_tile_groups_with_at_least_one_visual_grid",200,346,"GROUP_REPRESENTATIVE_COVERAGE","not confirmed unique game furniture"),
  ("multi_facing_groups_with_two_facing_direct_comparison",120,274,"DIRECT_DIRECTION_COMPARISON","v22 60 groups + v23 60 groups"),
  ("new_v23_source_sprite_pixel_sha",256,256,"ORIGINAL_PNG_CROP_HASH","exact original tile cells"),
  ("old_original_collision_warnings_resolved",0,474,"UNRESOLVED","no source warning certified closed"),
  ("original_png_mapping_gap_resolved",0,23,"UNRESOLVED","TileDef names without matched PNG asset"),
  ("same_game_object_certified",0,0,"UNKNOWN_DENOMINATOR","needs runtime evidence")
 ]
 progress=[]
 for key,n,d,typ,meaning in metrics:
  row=dict(metric_key=key,done=n,total=d,percentage=round(100*n/d,2) if d else None,
   scope=typ,interpretation=meaning)
  put(c,"v23_progress_scope",row);progress.append(row)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for t,n in {**preserved,
   "v23_direct_two_facing_visual_comparison":60,
   "v23_new_facing_original_source":120,
   "v23_source_original_pixel_proof":256,
   "v23_entire_820_multitile_candidate_coverage":820,
   "v23_remaining_500_multitile_candidate_queue":500,
   "v23_progress_scope":12}.items():
  assert cnt(c,t)==n,(t,cnt(c,t),n)
 assert cnt(c,"v23_direct_two_facing_visual_comparison")==60
 assert c.execute("SELECT COUNT(*) FROM v23_direct_two_facing_visual_comparison WHERE exact_runtime_game_object_ID_certified!=0 OR same_game_object_certified!=0").fetchone()[0]==0
 c.close()
 csv_out("V23_60_DIRECT_TWO_FACING_VISUAL_COMPARISONS.csv",reports)
 csv_out("V23_120_ORIGINAL_FACING_SOURCE_COORDINATES.csv",facerecs)
 csv_out("V23_256_ORIGINAL_PNG_CELL_SHA256.csv",pixrecs)
 csv_out("V23_ALL_820_FACING_VISUAL_REVIEW_COVERAGE.csv",coverage)
 csv_out("V23_500_UNREVIEWED_DIRECTION_QUEUE.csv",pending)
 csv_out("V23_12_SCOPE_LIMITED_PROGRESS.csv",progress)
 manifest=dict(
  version="v23",source_v22_zip_sha256=hashlib.sha256(OLD.read_bytes()).hexdigest(),
  preserved_raw_property_rows=195265,preserved_source_slots=73644,
  source_and_wiki_registry_candidate_rows=2231,preserved_source_tiles=8219,
  prior_geometry_templates=3840,prior_rectangle_candidates=843,
  actual_multitile_geometry_candidates=820,
  prior_200_direct_source_grid_views=200,new_120_direct_source_grid_views=120,
  cumulative_direct_multitile_facing_views=320,
  current_multitile_facing_direct_visual_coverage_pct=round(320/820*100,2),
  remaining_unreviewed_multitile_direction_candidates=500,
  v23_new_pair_groups=60,previous_v22_pair_groups=60,
  pair_reviewed_groups_cumulative=120,
  cross_facing_comparison_eligible_original_groups=274,
  paired_group_comparison_pct=round(120/274*100,2),
  grouped_multitile_source_candidates=346,
  original_groups_with_at_least_one_viewed_grid=200,
  groups_with_viewed_multitile_grid_pct=round(200/346*100,2),
  original_PNG_sprite_pixel_CRC_verified=256,
  original_sprite_png_atlases=staging["distinct_original_png_sha_sources"],
  new_paired_source_only=staging["selected_source_only_groups"],
  new_paired_wiki_linked=staging["selected_wiki_linked_groups"],
  v23_new_visual_subject_counts=dict(sorted(new_class.items())),
  v23_Grid_dimensions_swapped_groups=sum(x["dimensions_swapped_between_facings"] for x in reports),
  original_source_only_single_sprite_view_count=940,
  inherited_Wiki_reference_may_be_outdated_or_incomplete=True,
  inherited_474_unresolved_source_warnings=True,
  inherited_23_unresolved_source_PNG_mapping_gaps=True,
  prior_Work_107_groups_574_tiles_without_group_id_not_added=True,
  visually_similar_does_not_certify_same_game_object=True,
  game_object_identity_certified=0,same_game_object_cross_facing_certified=0,
  full_game_isometric_furniture_assembly_certified=0,
  Lua_TMX_Minecraft_not_started=True,
  sqlite_integrity="ok",zip_crc="ok"
 )
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 가구 방향 실물 이미지 검수 v23 — 60쌍/120방향/256원본 PNG셀 직접 검수\n\n"
 "v22의 전체 SQLite를 원본 그대로 복제하고, v21 80/단일 방향 및 v22 120/양방향의 실제 시각 검수와 원본 속성을 보존했습니다.\n"
 "이미 검수한 원본 그룹 140개와 겹치지 않는 새 60개 그룹에서 E/S 등 두 개 방향의 정확한 원본 SpriteGridPos 및 PNG 픽셀을 교차 대조했습니다.\n"
 "6장 원본 접촉시트 60개 페어를 직접 열어 넓은 시각 카테고리 및 두 방향 외형 관계를 기록했습니다.\n"
 "총 방향 이미지 검수: v21 80 + v22 120 + v23 120 = 320/820(39.02%). 검수 대기 500/820.\n"
 "방향 2개 이상이 있는 원본 그룹 274개 중 두 방향을 직접 비교한 그룹 120개(43.80%). 이들은 고유 가구 120종 인증이 아닙니다.\n"
 "다중 타일 기하 후보를 가진 고유 원본 그룹 346개 가운데 최소 한 방향의 이미지 검수 증거를 남긴 그룹은 200개(57.80%).\n"
 "원본 Wiki는 오래되었거나 불완전할 수 있는 참고 자료로만 취급합니다.\n"
 "직사각형 좌표·유사 외형·동일 Wiki 이름만으로 게임에서 실제 같은 가구라는 결론을 내리지 않았습니다.\n"
 "원본 경고 474건·원본 PNG 연결 미해결 23개 유지, 게임 객체 정체 인증 0, 마크/Lua/TMX 구현 미착수.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if (f.is_file() and f!=PACK and not f.name.startswith("STAGED_") and not f.name.endswith("_BASE64.txt") and not f.name.startswith("_required_")):
    z.write(f,f.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V23_320_OF_820_MULTITILE_VISUAL_GRID_120_PAIRED_GROUPS_256_ORIGINAL_SOURCE_PIXEL_SHA_SQLITE_CRC_PASS",js(manifest),flush=True)
if __name__=="__main__":main()
