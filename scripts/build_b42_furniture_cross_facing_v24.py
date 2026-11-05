#!/usr/bin/env python3
"""PZ B42 v24 complete original-source cross-facing visual DB.
80 NEW groups, 160 previously unseen group×Facing candidates, original pixels only.
Neither a Wiki label, SpriteGridPos rectangle, nor related appearance certifies a game object.
"""
import csv,hashlib,json,shutil,sqlite3,zipfile
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v23/B42_FURNITURE_CROSS_FACING_REVIEW_V23.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v24"
DB=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V24.sqlite"
PACK=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V24.zip"
def rows(c,q,p=()):return [dict(x) for x in c.execute(q,p)]
def count(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def JS(v):return json.dumps(v,sort_keys=True,ensure_ascii=False)
def csvin(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def csvout(name,recs):
 assert recs,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(recs[0]));w.writeheader();w.writerows(recs)
def insert(c,table,obj):
 names=list(obj)
 c.execute("INSERT INTO "+table+" ("+",".join(names)+") VALUES ("+",".join("?" for _ in names)+")",list(obj.values()))
def main():
 assert BASE.is_file() and OUT.is_dir() and not DB.exists()
 stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["previous_direct_grid_visual_candidates"]==320
 assert stage["new_distinct_pair_groups"]==80 and stage["new_direction_candidates"]==160
 assert stage["new_direction_overlaps_with_v21_v22_v23"]==0
 assert stage["new_group_overlaps_with_v21_v22_v23"]==0
 assert stage["all_new_source_tile_crops_verified"]==466
 assert stage["actual_pair_contact_page_count"]==8
 pairrows=csvin("V24_80_PAIR_SELECTION_SOURCE_ONLY.csv")
 facings=csvin("V24_160_FACING_GRID_CANDIDATES.csv")
 partrows=csvin("V24_SELECTED_ORIGINAL_PART_POSITIONS.csv")
 pixrows=csvin("V24_DIRECT_ORIGINAL_SOURCE_PIXEL_SHA256.csv")
 labels=csvin("V24_80_DIRECT_PAIRED_VISUAL_CLASSIFICATIONS.csv")
 assert len(pairrows)==len(labels)==80
 assert len(facings)==160 and len(partrows)==len(pixrows)==466
 pairs={int(r["pair_no"]):r for r in pairrows}
 labs={int(r["pair_no"]):r for r in labels}
 assert set(pairs)==set(labs)==set(range(1,81))
 for i in range(1,81):
  assert labs[i]["observation_scope"]=="DIRECT_VIEW_OF_TWO_ORIGINAL_PNG_SOURCE_DIRECTION_GRIDS"
  assert labs[i]["visual_similarity_scope"]=="CANDIDATE_RELATED_DESIGN_NOT_GAME_OBJECT_PROOF"
  assert labs[i]["confirmed_exact_game_object_identity"]=="0"
 assert len({r["group_id"] for r in pairrows})==80
 assert all(r["prior_v21_v22_v23_visual_group_overlap"]=="0" for r in pairrows)
 contacts=stage["original_pair_contact_sha256"]
 assert len(contacts)==8
 for fn,sha in contacts.items():
  assert hashlib.sha256((OUT/fn).read_bytes()).hexdigest()==sha,(fn,"contact_sheet_changed")

 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CROSS_FACING_REVIEW_V23.sqlite") as a,DB.open("wb") as b:
   shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 old_counts={
  "source_attributes":195265,"source_slots":73644,
  "registry_entry":2231,"wiki_furniture":1268,"furniture_tile":8219,
  "v12_template_proof":3840,"v13_warning_case":474,"v14_source_only_ledger":963,
  "v20_master_furniture_registry":2231,"v20_source_only_review_coverage":963,
  "v21_all_source_rectangle_template":843,"v21_source_tile_positioned_png":2221,
  "v21_direct_multisprite_grid_visual_observation":80,
  "v21_reviewed_multisprite_pixel_sha":335,
  "v22_direct_two_facing_visual_comparison":60,"v22_new_facing_original_grid":120,
  "v22_original_sprite_pixel_sha":258,
  "v23_direct_two_facing_visual_comparison":60,
  "v23_new_facing_original_source":120,
  "v23_source_original_pixel_proof":256,
  "v23_entire_820_multitile_candidate_coverage":820,
  "v23_remaining_500_multitile_candidate_queue":500
 }
 for t,num in old_counts.items():assert count(c,t)==num,(t,count(c,t),num)
 old21={(r["group_id"],r["Facing"]) for r in rows(c,"SELECT group_id,Facing FROM v21_direct_multisprite_grid_visual_observation")}
 old22={(r["group_id"],r["Facing"]) for r in rows(c,"SELECT group_id,Facing FROM v22_new_facing_original_grid")}
 old23={(r["group_id"],r["Facing"]) for r in rows(c,"SELECT group_id,Facing FROM v23_new_facing_original_source")}
 assert len(old21)==80 and len(old22)==len(old23)==120
 old=old21|old22|old23
 assert len(old)==320
 oldgroups={g for g,_ in old}
 assert len(oldgroups)==200
 pending23={(r["group_id"],r["Facing"]) for r in rows(c,"SELECT group_id,Facing FROM v23_remaining_500_multitile_candidate_queue")}
 assert len(pending23)==500 and not pending23.intersection(old)
 rect={(r["group_id"],r["Facing"]):r for r in rows(c,
  "SELECT group_id,Facing,raw_sprite_part_count,grid_w,grid_h,source_only_group,original_png_parts_mapped FROM v21_all_source_rectangle_template WHERE raw_sprite_part_count>=2")}
 assert len(rect)==820
 raw={(r["group_id"],r["Facing"],r["source_key"]):r for r in rows(c,
  "SELECT group_id,Facing,source_key,raw_sprite_grid_pos,relative_x,relative_y,original_png_path,atlas_col,atlas_row,original_cell_w,original_cell_h FROM v21_source_tile_positioned_png")}
 baseproof={(r["group_id"],r["Facing"],r["source_key"]):r for r in rows(c,
  "SELECT group_id,Facing,source_key,original_grid,relative_x_when_available,relative_y_when_available FROM v12_tile_proof")}
 sourcetile={r["source_key"]:r for r in rows(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 c.executescript("""
 CREATE TABLE v24_direct_two_facing_visual_comparison(
  pair_no INTEGER PRIMARY KEY,group_id TEXT UNIQUE,original_display_name TEXT,
  source_only_group INTEGER,Facing_A TEXT,Facing_B TEXT,grid_A TEXT,grid_B TEXT,
  parts_A INTEGER,parts_B INTEGER,broad_visible_subject TEXT,
  observed_two_facing_relation TEXT,provisional_type_scope TEXT,
  dimensions_swapped_between_facings INTEGER,
  original_pair_visual_viewed INTEGER NOT NULL DEFAULT 1,
  actual_same_game_object_certified INTEGER NOT NULL DEFAULT 0,
  exact_runtime_game_object_ID_certified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v24_new_facing_original_source(
  pair_no INTEGER,group_id TEXT,Facing TEXT,face_slot TEXT,
  width INTEGER,height INTEGER,original_part_count INTEGER,
  source_keys_json TEXT,original_position_crosschecked INTEGER NOT NULL DEFAULT 1,
  runtime_furniture_ID_certified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v24_source_original_pixel_proof(
  pair_no INTEGER,face_slot TEXT,group_id TEXT,Facing TEXT,source_key TEXT,
  raw_sprite_grid_pos TEXT,relative_x INTEGER,relative_y INTEGER,
  original_png_path TEXT,original_png_sha256 TEXT,original_crop_pixel_sha256 TEXT,
  atlas_column INTEGER,atlas_row INTEGER,cell_width INTEGER,cell_height INTEGER,
  pixel_cropped_from_original_png INTEGER NOT NULL DEFAULT 1,
  official_game_furniture_identity_certified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v24_entire_820_multitile_candidate_coverage(
  group_id TEXT,Facing TEXT,raw_part_count INTEGER,grid_w INTEGER,grid_h INTEGER,
  source_only_group INTEGER,visual_review_origin TEXT,original_grid_visually_viewed INTEGER,
  two_facing_comparison_visually_viewed INTEGER,
  exact_game_furniture_identity_certified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v24_remaining_340_multitile_candidate_queue(
  group_id TEXT,Facing TEXT,raw_part_count INTEGER,grid_w INTEGER,grid_h INTEGER,
  source_only_group INTEGER,original_png_cell_count INTEGER,
  runtime_object_verified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v24_progress_scope(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,percent REAL,
  evidence_type TEXT,interpretation TEXT);
 """)
 reports=[];newgroups=set()
 for i in range(1,81):
  p=pairs[i];lab=labs[i];g=p["group_id"]
  a,b=p["Facing_A"],p["Facing_B"]
  assert g not in oldgroups and g not in newgroups and a!=b
  assert (g,a) in pending23 and (g,b) in pending23
  aw,ah=map(int,p["original_grid_A"].split("x"))
  bw,bh=map(int,p["original_grid_B"].split("x"))
  assert (aw,ah)==(rect[(g,a)]["grid_w"],rect[(g,a)]["grid_h"])
  assert (bw,bh)==(rect[(g,b)]["grid_w"],rect[(g,b)]["grid_h"])
  assert int(p["source_part_count_A"])==rect[(g,a)]["raw_sprite_part_count"]
  assert int(p["source_part_count_B"])==rect[(g,b)]["raw_sprite_part_count"]
  is_wall_graphic=int(lab["observed_broad_visual_subject"] in (
   "SHOP_SIGN_MENU_OR_WALL_GRAPHIC","PUBLIC_SIGN_FLAG_OR_MAP","WALL_PAINTING"))
  scope="POSSIBLE_WALL_GRAPHIC_OR_SIGN_NOT_CONFIRMED_FURNITURE" if is_wall_graphic else "VISIBLE_FIXTURE_OR_DECOR_NOT_RUNTIME_CERTIFIED"
  rec=dict(pair_no=i,group_id=g,original_display_name=p["original_name"],
   source_only_group=int(p["source_only_group"]),Facing_A=a,Facing_B=b,
   grid_A=p["original_grid_A"],grid_B=p["original_grid_B"],
   parts_A=int(p["source_part_count_A"]),parts_B=int(p["source_part_count_B"]),
   broad_visible_subject=lab["observed_broad_visual_subject"],
   observed_two_facing_relation=lab["observed_two_facing_relation"],
   provisional_type_scope=scope,
   dimensions_swapped_between_facings=int(aw==bh and ah==bw and (aw,ah)!=(bw,bh)))
  insert(c,"v24_direct_two_facing_visual_comparison",rec)
  reports.append(rec);newgroups.add(g)
 assert len(reports)==80 and len(newgroups)==80
 source_parts=defaultdict(set)
 for p in partrows:
  g,f,key=p["group_id"],p["Facing"],p["source_key"]
  loc=(g,f,key)
  assert loc in raw and loc in baseproof and key in sourcetile
  orig=raw[loc];bp=baseproof[loc];s=sourcetile[key]
  assert p["raw_sprite_grid_pos"]==orig["raw_sprite_grid_pos"]==bp["original_grid"]==s["SpriteGridPos"]
  assert s["group_id"]==g
  assert int(p["relative_x"])==orig["relative_x"]==bp["relative_x_when_available"]
  assert int(p["relative_y"])==orig["relative_y"]==bp["relative_y_when_available"]
  assert p["original_png_path"]==orig["original_png_path"]
  assert int(p["atlas_col"])==orig["atlas_col"] and int(p["atlas_row"])==orig["atlas_row"]
  assert int(p["original_cell_w"])==orig["original_cell_w"] and int(p["original_cell_h"])==orig["original_cell_h"]
  assert key not in source_parts[(g,f)],(g,f,key)
  source_parts[(g,f)].add(key)
 assert len(source_parts)==160
 seen=set();faceout=[]
 for p in facings:
  g,f=p["group_id"],p["Facing"];i=int(p["pair_no"]);slot=p["face_slot"]
  assert i in pairs and pairs[i]["group_id"]==g
  assert slot in ("A","B") and pairs[i]["Facing_"+slot]==f
  assert (g,f) in pending23 and (g,f) not in seen
  t=rect[(g,f)]
  assert int(p["width"])==t["grid_w"] and int(p["height"])==t["grid_h"]
  assert int(p["original_parts"])==t["raw_sprite_part_count"]
  assert set(json.loads(p["original_keys_json"]))==source_parts[(g,f)]
  rec=dict(pair_no=i,group_id=g,Facing=f,face_slot=slot,
   width=int(p["width"]),height=int(p["height"]),
   original_part_count=int(p["original_parts"]),source_keys_json=p["original_keys_json"])
  insert(c,"v24_new_facing_original_source",rec);faceout.append(rec);seen.add((g,f))
 assert len(faceout)==len(seen)==160 and not seen.intersection(old)
 pxkeys=set();pxout=[]
 for p in pixrows:
  g,f,key=p["group_id"],p["Facing"],p["source_key"]
  loc=(g,f,key)
  assert (g,f) in seen and key in source_parts[(g,f)] and loc not in pxkeys
  assert p["actual_original_pixels_cropped"]=="1" and p["actual_in_game_object_certified"]=="0"
  assert p["raw_grid"]==raw[loc]["raw_sprite_grid_pos"]
  assert int(p["relative_x"])==raw[loc]["relative_x"]
  assert int(p["relative_y"])==raw[loc]["relative_y"]
  assert p["png_path"]==raw[loc]["original_png_path"]
  assert int(p["atlas_col"])==raw[loc]["atlas_col"] and int(p["atlas_row"])==raw[loc]["atlas_row"]
  assert len(p["original_png_sha256"])==len(p["png_cell_pixel_sha256"])==64
  rec=dict(pair_no=int(p["pair_no"]),face_slot=p["face_slot"],group_id=g,
   Facing=f,source_key=key,raw_sprite_grid_pos=p["raw_grid"],
   relative_x=int(p["relative_x"]),relative_y=int(p["relative_y"]),
   original_png_path=p["png_path"],
   original_png_sha256=p["original_png_sha256"],
   original_crop_pixel_sha256=p["png_cell_pixel_sha256"],
   atlas_column=int(p["atlas_col"]),atlas_row=int(p["atlas_row"]),
   cell_width=int(p["cell_w"]),cell_height=int(p["cell_h"]))
  insert(c,"v24_source_original_pixel_proof",rec);pxout.append(rec);pxkeys.add(loc)
 assert len(pxout)==466 and pxkeys=={(g,f,key) for (g,f),keys in source_parts.items() for key in keys}
 coverage=[];pending=[]
 for (g,f),r in sorted(rect.items()):
  if (g,f) in old21:status="DIRECTLY_VIEWED_V21"
  elif (g,f) in old22:status="DIRECTLY_VIEWED_V22_PAIRED"
  elif (g,f) in old23:status="DIRECTLY_VIEWED_V23_PAIRED"
  elif (g,f) in seen:status="DIRECTLY_VIEWED_V24_PAIRED"
  else:status="NOT_YET_VISUALLY_REVIEWED"
  viewed=int(status!="NOT_YET_VISUALLY_REVIEWED")
  paired=int(status in ("DIRECTLY_VIEWED_V22_PAIRED","DIRECTLY_VIEWED_V23_PAIRED","DIRECTLY_VIEWED_V24_PAIRED"))
  rec=dict(group_id=g,Facing=f,raw_part_count=r["raw_sprite_part_count"],
   grid_w=r["grid_w"],grid_h=r["grid_h"],
   source_only_group=r["source_only_group"],
   visual_review_origin=status,original_grid_visually_viewed=viewed,
   two_facing_comparison_visually_viewed=paired)
  insert(c,"v24_entire_820_multitile_candidate_coverage",rec);coverage.append(rec)
  if not viewed:
   q=dict(group_id=g,Facing=f,raw_part_count=r["raw_sprite_part_count"],
    grid_w=r["grid_w"],grid_h=r["grid_h"],
    source_only_group=r["source_only_group"],
    original_png_cell_count=r["original_png_parts_mapped"])
   insert(c,"v24_remaining_340_multitile_candidate_queue",q);pending.append(q)
 assert len(coverage)==820 and len(pending)==340
 assert sum(x["original_grid_visually_viewed"] for x in coverage)==480
 assert sum(x["two_facing_comparison_visually_viewed"] for x in coverage)==400
 all_group={g for g,f in rect}
 viewed_group={g for g,f in old|seen}
 assert len(all_group)==346 and len(viewed_group)==280
 bygroup=defaultdict(set)
 for g,f in rect:bygroup[g].add(f)
 pair_eligible=sum(len(v)>=2 for v in bygroup.values())
 assert pair_eligible==274
 old_pair_ids={x["group_id"] for x in rows(c,"SELECT group_id FROM v22_direct_two_facing_visual_comparison UNION ALL SELECT group_id FROM v23_direct_two_facing_visual_comparison")}
 assert len(old_pair_ids)==120 and not old_pair_ids.intersection(newgroups)
 pair_total=len(old_pair_ids|newgroups)
 assert pair_total==200
 category=Counter(x["broad_visible_subject"] for x in reports)
 group_kind=Counter(x["provisional_type_scope"] for x in reports)
 assert sum(category.values())==sum(group_kind.values())==80
 metrics=[
 ("known_registered_Wiki_and_source_candidate_rows",2231,2231,"REGISTERED_SOURCE_ROWS","not entire confirmed unique furniture collection"),
 ("single_original_sprite_source_only_direct_reviews",940,963,"DIRECT_SINGLE_PIXEL_CELL","23 source png mappings unresolved"),
 ("directional_source_geometry_templates",3840,3840,"TILEDEF_SOURCE","not runtime furniture assembly"),
 ("multitile_rectangular_group_facing_candidates",820,820,"ORIGINAL_SOURCE_GRID","includes signs/paintings, not necessarily physical furniture"),
 ("cumulative_directly_viewed_multitile_facing_grids",480,820,"DIRECT_TWO_FACING_IMAGE","80 v21 +120 v22 +120 v23 +160 v24"),
 ("v24_new_direct_two_facing_grid_image_views",160,820,"DIRECT_ORIGINAL_PNG","80 unique source groups"),
 ("unique_multitile_groups_at_least_one_grid_viewed",280,346,"GROUP_COVERAGE","not confirmed game furniture"),
 ("source_groups_with_two_facing_direct_image_comparison",200,274,"VISUAL_FACE_COMPARISON","v22 60 + v23 60 + v24 80"),
 ("v24_original_source_crop_pixel_hash",466,466,"ORIGINAL_PNG_SHA","every new part pixel cropped"),
 ("unresolved_original_warning_cases",0,474,"UNRESOLVED","not cleared"),
 ("original_png_unlinked_source_groups_resolved",0,23,"UNRESOLVED","not cleared"),
 ("runtime_same_game_object_identity_certified",0,0,"UNKNOWN","cannot calculate entire furniture completion")
 ]
 prog=[]
 for key,n,den,typ,description in metrics:
  rec=dict(metric_key=key,numerator=n,denominator=den,
   percent=round(100*n/den,2) if den else None,evidence_type=typ,interpretation=description)
  insert(c,"v24_progress_scope",rec);prog.append(rec)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
 for t,n in {**old_counts,"v24_direct_two_facing_visual_comparison":80,
   "v24_new_facing_original_source":160,
   "v24_source_original_pixel_proof":466,
   "v24_entire_820_multitile_candidate_coverage":820,
   "v24_remaining_340_multitile_candidate_queue":340,
   "v24_progress_scope":12}.items():
  assert count(c,t)==n,(t,count(c,t),n)
 assert c.execute("""SELECT COUNT(*) FROM v24_direct_two_facing_visual_comparison WHERE
 actual_same_game_object_certified!=0 OR exact_runtime_game_object_ID_certified!=0""").fetchone()[0]==0
 c.close()
 csvout("V24_80_NEW_DIRECT_TWO_FACING_VISUAL_COMPARISONS.csv",reports)
 csvout("V24_160_NEW_ORIGINAL_FACING_SOURCE_COORDINATES.csv",faceout)
 csvout("V24_466_ORIGINAL_PNG_CROP_SHA256.csv",pxout)
 csvout("V24_ALL_820_MULTITILE_FACING_VISUAL_COVERAGE.csv",coverage)
 csvout("V24_340_STILL_UNREVIEWED_DIRECTION_QUEUE.csv",pending)
 csvout("V24_12_SCOPED_PROGRESS.csv",prog)
 summary=dict(version="v24",
  original_v23_full_sqlite_zip_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
  original_source_raw_property_rows=195265,original_source_slots=73644,
  candidate_registry_rows=2231,source_candidate_tile_keys=8219,
  source_directional_geometry_templates=3840,
  source_complete_rectangle_candidates_including_1x1=843,
  source_multitile_group_facing_candidates=820,
  previous_multitile_original_png_grids_reviewed=320,
  new_group_facing_grids_directly_viewed=160,
  new_unique_group_pairs_directly_viewed=80,
  new_original_sprite_crops_individually_sha_verified=466,
  new_original_png_atlases_used=stage["distinct_original_png_sha_sources"],
  new_source_only_group_pairs=stage["selected_source_only_groups"],
  new_wiki_linked_group_pairs=stage["selected_wiki_linked_groups"],
  cumulative_original_multitile_grid_views=480,
  cumulative_multitile_visual_coverage_pct=round(100*480/820,2),
  remaining_group_facing_candidate_images_to_review=340,
  unique_groups_with_source_multitile_templates=346,
  distinct_groups_with_at_least_one_multitile_visual_review=280,
  unique_multitile_group_representative_visual_review_pct=round(100*280/346,2),
  multi_facing_eligible_group_count=274,
  cumulative_groups_with_two_facings_directly_compared=200,
  two_facing_direct_comparison_pct=round(100*200/274,2),
  v24_provisional_visible_subject_counts=dict(sorted(category.items())),
  v24_visually_wall_graphic_like_count=group_kind["POSSIBLE_WALL_GRAPHIC_OR_SIGN_NOT_CONFIRMED_FURNITURE"],
  v24_visual_fixture_or_decor_not_verified_count=group_kind["VISIBLE_FIXTURE_OR_DECOR_NOT_RUNTIME_CERTIFIED"],
  v24_grid_dimensions_swapped_count=sum(x["dimensions_swapped_between_facings"] for x in reports),
  old_source_only_single_sprite_image_reviews=940,
  original_Wiki_may_be_stale_or_incomplete=True,
  old_474_original_warning_cases_still_unresolved=True,
  old_23_original_png_mapping_gaps_still_unresolved=True,
  prior_Work_107_group_574_tile_reported_unconfirmed_IDs_not_counted=True,
  source_grid_not_equal_exact_in_game_isometric_assembly=True,
  source_visual_similarity_not_runtime_identity=True,
  certified_complete_physical_furniture_assemblies=0,
  certified_same_game_object_across_facings=0,
  certified_exact_runtime_game_object_IDs=0,
  Lua_TMX_Minecraft_not_started=True,
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
  "# Project Zomboid B42 가구 원본 방향 비교 v24 — 신규 80그룹·160방향·466원본 픽셀\n\n"
  "v23 전체 SQLite의 원본 수집 정보와 v21~v23 시각 검수 이력을 보존하면서 v24 원본 PNG 방향 비교를 추가했습니다.\n"
  "v21~v23에서 시각 검수한 고유 원본 200그룹을 제외하고 새 80그룹을 선정하여 두 방향씩 총 160개 기하 후보의 원본 그리드를 직접 비교했습니다.\n"
  "접촉시트 8장, 원본 PNG 40개 아틀라스, 원본 스프라이트 부품 466개의 실제 픽셀 해시를 기록했습니다.\n"
  "누적 다중 타일 기하 후보 이미지 검수 480/820(58.54%). 남은 340개 방향별 이미지 검수 큐를 생성했습니다.\n"
  "고유 346그룹 중 280그룹에서 최소 한 방향을 직접 보았고, 274개 다방향 후보 그룹 중 200그룹에서 두 방향을 직접 비교했습니다.\n"
  "이번 v24 접촉시트에는 가구 후보 이외에 다수의 간판·회화·표지판이 섞여 있어 외형만 광의 분류하고 원본 후보 원장에서 자동 삭제하지 않았습니다.\n"
  "SpriteGridPos 그리드 및 유사 이미지가 게임에서 실제 하나의 가구 오브젝트이거나 모든 방향에서 동일한 객체임을 증명하지 않습니다.\n"
  "위키는 오래됐거나 불완전할 수 있는 참고 자료이고 TileDef와 원본 PNG를 우선했습니다.\n"
  "기존 원본 경고 474건, PNG 아틀라스 미연결 23그룹 및 이전 Work 보고분은 그대로 보존·구분했습니다.\n"
  "게임 오브젝트 정체/완성 가구/4방향 확정 0건, Lua loot/TMX/마크 구현 미진행.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if (f.is_file() and f!=PACK and not f.name.startswith("STAGED_") and
     not f.name.endswith("_BASE64.txt") and not f.name.startswith("_required_")):
    z.write(f,f.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V24_SOURCE_80_PAIR_160_FACING_466_PNG_CROPS_480_OF_820_SCOPED_DIRECT_VISUAL_COMPLETE",
  JS(summary),flush=True)
if __name__=="__main__":
 main()
