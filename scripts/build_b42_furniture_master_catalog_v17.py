#!/usr/bin/env python3
"""B42 v17: directly observed 160 additional ORIGINAL sprite images; full source-first furniture list.
Wiki may be out of date or missing: only an advisory source.
No human/image classification is official in-game furniture identity certification.
"""
import csv,hashlib,json,shutil,sqlite3,zipfile
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
SOURCE=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v16/B42_FURNITURE_MASTER_INVENTORY_V16.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v17"
DB=OUT/"B42_FURNITURE_MASTER_INVENTORY_V17.sqlite"
PACK=OUT/"B42_FURNITURE_MASTER_INVENTORY_V17.zip"
CLASSES={"FURNITURE_TABLE_OR_COUNTER_PART":[321,322,323,324,346,372,373,374,431,462,463,464],"FURNITURE_BED_OR_CRIB_PART":[326],"FURNITURE_STORAGE_OR_SHELVING_PART":[329,367,368,413,430,432,433,435,438],"EQUIPMENT_OR_APPLIANCE":[325,327,328,396,470],"INDUSTRIAL_EQUIPMENT_OR_MACHINE":[348,363,454,456,458,459,460,461,465,466,467,468],"LIGHTING_OR_STRING_LIGHT":[330,331,332,333,397,398,399,400,469],"SHELTER_OR_AWNING_PART":[334,335,336,337,406],"SIGN_POSTER_WALL_GRAPHIC":[338,339,340,342,343,344,345,349,350,355,356,369,370,371,375,376,377,378,388,389,392,415,418,419],"STRUCTURE_OR_ARCHITECTURAL_PART":[341,383,395,401,402,417,471,472,473,474],"DECORATIVE_SCULPTURE_OR_ORNAMENT":[347],"FLOOR_OR_GROUND_TEXTURE":[365,366,412,420,421,422,423,443,444,445,446,447,448,449],"RUG_OR_GROUND_DECOR":[390,391,450,451,452,453,479,480],"MATERIAL_OR_LOOSE_ITEM":[357,393,394,411,416,434,436,437,439,441,442,455,457,475,476,477,478],"AGRICULTURE_SOIL_OR_CROP_ROW":[351,352,353,354,379,380,381,382],"NATURAL_BOULDER_OR_VEGETATION":[384,385,386,387,407,408,409,410,424,425,426,427,440],"PLUMBING_SINK_OR_FIXTURE":[361,364,428,429],"OUTDOOR_FIRE_OR_WELL":[358,359,360,403,404,405],"VISUALLY_INDETERMINATE":[362,414]}
def rows(c,sql,args=()):
 return [dict(x) for x in c.execute(sql,args)]
def ct(c,t):
 return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def j(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def write(name,arr):
 assert arr,("empty",name)
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)
def ins(c,table,row):
 cols=list(row);c.execute("INSERT INTO "+table+"("+",".join(cols)+") VALUES("+",".join("?" for _ in cols)+")",list(row.values()))
def main():
 assert OUT.is_dir() and SOURCE.is_file() and not DB.exists()
 assert sorted(i for a in CLASSES.values() for i in a)==list(range(321,481))
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_MASTER_INVENTORY_V16.sqlite") as a, DB.open("wb") as b:
   shutil.copyfileobj(a,b)
 with (OUT/"V17_160_NEW_ORIGINAL_PNG_CROP_SHA256.csv").open("r",encoding="utf-8-sig",newline="") as f:
  stage=list(csv.DictReader(f))
 stage_manifest=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert len(stage)==160 and stage_manifest["original_png_pixel_crops_ok"]==160
 assert stage_manifest["overlap_with_v15_v16"]==0
 assert stage_manifest["distinct_source_only_samples"]==480
 label_by_sample={k:cat for cat,keys in CLASSES.items() for k in keys}
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 before={"source_attributes":195265,"source_slots":73644,"registry_entry":2231,
   "furniture_tile":8219,"wiki_furniture":1268,"v12_template_proof":3840,
   "v13_warning_case":474,"v13_storage_link":1855,
   "v14_source_only_ledger":963,"v15_visual_part_observation":160,
   "v16_visual_part_observation":160,"v16_master_furniture_registry":2231,
   "v16_source_only_review_coverage":963}
 for t,n in before.items():assert ct(c,t)==n,(t,ct(c,t),n)
 prev_v15=rows(c,"SELECT entry_id,group_id,source_key,observed_broad_part_class AS visual_class FROM v15_visual_part_observation")
 prev_v16=rows(c,"SELECT entry_id,source_group_id AS group_id,source_key,broad_visual_shape_class AS visual_class FROM v16_visual_part_observation")
 old_v=prev_v15+prev_v16
 oldentries={x["entry_id"] for x in old_v}
 oldgroups={x["group_id"] for x in old_v}
 assert len(oldentries)==320 and len(oldgroups)==320
 source={x["entry_id"]:x for x in rows(c,"SELECT * FROM v14_source_only_ledger")}
 c.executescript("""
 CREATE TABLE v17_visual_part_observation(
  sample_index INTEGER PRIMARY KEY,entry_id TEXT NOT NULL,source_group_id TEXT,source_key TEXT,
  original_name TEXT,png_path TEXT,source_png_sha256 TEXT,
  original_crop_pixel_sha256 TEXT,contact_sheet_no INTEGER,contact_sheet_sha256 TEXT,
  broad_visual_shape_class TEXT,confidence_scope TEXT,visual_evidence_scope TEXT,
  visually_viewed_one_original_sprite INTEGER NOT NULL DEFAULT 1,
  whole_group_furniture_assembled INTEGER NOT NULL DEFAULT 0,
  same_object_across_4_facings_verified INTEGER NOT NULL DEFAULT 0,
  official_game_object_identity_verified INTEGER NOT NULL DEFAULT 0);
 CREATE UNIQUE INDEX v17_observation_group ON v17_visual_part_observation(source_group_id);
 CREATE TABLE v17_master_furniture_registry AS SELECT * FROM v16_master_furniture_registry WHERE 0;
 INSERT INTO v17_master_furniture_registry SELECT * FROM v16_master_furniture_registry;
 CREATE UNIQUE INDEX v17_master_entry ON v17_master_furniture_registry(entry_id);
 CREATE TABLE v17_source_only_review_coverage AS SELECT * FROM v16_source_only_review_coverage WHERE 0;
 INSERT INTO v17_source_only_review_coverage SELECT * FROM v16_source_only_review_coverage;
 CREATE UNIQUE INDEX v17_source_coverage_entry ON v17_source_only_review_coverage(entry_id);
 CREATE TABLE v17_next_unreviewed_source_queue(
  entry_id TEXT PRIMARY KEY,group_id TEXT,original_name TEXT,
  original_tile_count INTEGER,image_mapping_present INTEGER,representative_source_key TEXT,
  representative_original_png TEXT,direction_template_count INTEGER,
  geometric_rectangular_candidate_count INTEGER,
  original_container_type_json TEXT,source_only_wiki_name_overlap_json TEXT,
  source_image_review_status TEXT NOT NULL DEFAULT 'NOT_YET_SINGLE_CELL_VISUALLY_REVIEWED',
  game_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v17_progress_scope(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,percent REAL,
  evidence_basis TEXT,meaning TEXT);
 """)
 observed=[];newentries=set();newgroups=set()
 for r in stage:
  idx=int(r["sample_index"]);eid=r["entry_id"];group=r["group_id"]
  assert 321<=idx<=480 and eid in source and group==source[eid]["group_id"]
  assert eid not in oldentries and group not in oldgroups
  assert eid not in newentries and group not in newgroups
  assert r["crop_status"]=="OK" and r["prior_v15_v16_review_overlap"]=="0"
  assert r["visually_inspected"]=="0" and r["game_identity_certified"]=="0"
  assert len(r["png_sha256"])==64 and len(r["crop_pixel_sha256"])==64
  assert r["source_key"]==source[eid]["original_png_tile_key"]
  sheet=(idx-321)//40+1
  label=label_by_sample[idx]
  confidence=("LOW_AMBIGUOUS" if label=="VISUALLY_INDETERMINATE" else
              "MODERATE_BROAD_SHAPE_ONLY" if label.startswith(("FURNITURE","INDUSTRIAL","EQUIPMENT","PLUMBING")) else
              "HIGH_ONLY_FOR_VISIBLE_BROAD_SHAPE")
  rec=dict(sample_index=idx,entry_id=eid,source_group_id=group,source_key=r["source_key"],
   original_name=source[eid]["original_name"],png_path=r["png_path"],
   source_png_sha256=r["png_sha256"],original_crop_pixel_sha256=r["crop_pixel_sha256"],
   contact_sheet_no=sheet,contact_sheet_sha256=stage_manifest["contact_sheet_sha256"][str(sheet)],
   broad_visual_shape_class=label,confidence_scope=confidence,
   visual_evidence_scope="ONE_ORIGINAL_TILE_PIXEL_CROP_NOT_WHOLE_ASSEMBLED_FURNITURE")
  ins(c,"v17_visual_part_observation",rec);observed.append(rec)
  c.execute("""UPDATE v17_master_furniture_registry SET
   direct_1cell_source_image_visual_review_rows=1,
   direct_1cell_visual_broad_class=?,
   review_scope_status='ONE_RAW_TILE_VISUAL_REVIEWED_NOT_WHOLE_FURNITURE'
   WHERE entry_id=? AND direct_1cell_source_image_visual_review_rows=0""",(label,eid))
  assert c.execute("SELECT changes()").fetchone()[0]==1,(eid,"master")
  c.execute("""UPDATE v17_source_only_review_coverage SET
   direct_one_cell_visual_reviewed=1,
   first_direct_visual_review_version='v17',
   broad_visible_shape=?
   WHERE entry_id=? AND direct_one_cell_visual_reviewed=0""",(label,eid))
  assert c.execute("SELECT changes()").fetchone()[0]==1,(eid,"coverage")
  newentries.add(eid);newgroups.add(group)
 assert len(observed)==160 and len(newentries)==160
 assert ct(c,"v17_master_furniture_registry")==2231
 assert ct(c,"v17_source_only_review_coverage")==963
 assert c.execute("SELECT SUM(direct_one_cell_visual_reviewed) FROM v17_source_only_review_coverage").fetchone()[0]==480
 assert c.execute("SELECT SUM(direct_1cell_source_image_visual_review_rows) FROM v17_master_furniture_registry").fetchone()[0]==480
 unreviewed=[]
 still=rows(c,"SELECT * FROM v17_source_only_review_coverage WHERE direct_one_cell_visual_reviewed=0 ORDER BY entry_id")
 assert len(still)==483
 for row in still:
  src=source[row["entry_id"]]
  rec=dict(entry_id=row["entry_id"],group_id=src["group_id"],
   original_name=src["original_name"],original_tile_count=src["original_tile_count"],
   image_mapping_present=src["image_mapping_present"],representative_source_key=src["original_png_tile_key"],
   representative_original_png=src["original_png_path"],direction_template_count=src["direction_templates"],
   geometric_rectangular_candidate_count=src["geometrically_rectangular_candidates"],
   original_container_type_json=src["container_types_raw_json"],
   source_only_wiki_name_overlap_json=src["same_normalized_name_wiki_candidates_json"])
  ins(c,"v17_next_unreviewed_source_queue",rec);unreviewed.append(rec)
 prior_classes=Counter(x["visual_class"] for x in old_v)
 newclasses=Counter(x["broad_visual_shape_class"] for x in observed)
 allclasses=prior_classes+newclasses
 assert sum(allclasses.values())==480
 progress=[
  ("known_catalog_records_registered",2231,2231,"registry 1,268 Wiki references + 963 source-only candidates","collected entries, NOT all unique furniture in game"),
  ("wiki_references_registered",1268,1268,"Wiki snapshot may be old/incomplete","reference row capture only"),
  ("wiki_image_source_id_crosswalk",1257,1268,"PZwiki image source keys","crosswalk not runtime identity"),
  ("source_only_candidate_groups_captured",963,963,"TileDef-only candidates lack exact Wiki image ID link","963 not necessarily distinct furniture"),
  ("source_only_one_sprite_visual_review",480,963,"v15 160 + v16 160 + v17 160, disjoint original source groups","representative 1-cell appearance only"),
  ("visual_review_unreviewed_source_only_groups",0,483,"unreviewed unique source group queue, not total item count","483 remain, review count completed 0 in subset"),
  ("prior_duplicate_shared_group_image_reference",129,129,"v8 prior direct image review reference","not in-game identity"),
  ("original_furniture_candidate_tile_ids_provenance",8219,8219,"TileDef original IDs and positions","not full-game furniture completion"),
  ("directional_template_geometry_audited",3840,3840,"group x facing geometry","not certified object assembly"),
  ("source_storage_original_value_crosschecked",1855,1855,"source container/capacity raw linkage","not Lua item loot"),
  ("remaining_474_original_warnings_resolved",0,474,"all original warning cases remain","unresolved"),
  ("in_game_furniture_identity_certified",0,0,"ground truth furniture count unknown","do not calculate total completion")
 ]
 prog=[]
 for key,n,d,evidence,meaning in progress:
  r=dict(metric_key=key,numerator=n,denominator=d,percent=round(100*n/d,2) if d else None,
   evidence_basis=evidence,meaning=meaning)
  ins(c,"v17_progress_scope",r);prog.append(r)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
 for t,n in {**before,"v17_visual_part_observation":160,"v17_master_furniture_registry":2231,
  "v17_source_only_review_coverage":963,"v17_next_unreviewed_source_queue":483,
  "v17_progress_scope":len(progress)}.items():
  assert ct(c,t)==n,(t,ct(c,t),n)
 assert c.execute("""SELECT COUNT(*) FROM v17_visual_part_observation WHERE
  whole_group_furniture_assembled!=0 OR same_object_across_4_facings_verified!=0
  OR official_game_object_identity_verified!=0""").fetchone()[0]==0
 registry=rows(c,"SELECT * FROM v17_master_furniture_registry ORDER BY entry_id")
 coverage=rows(c,"SELECT * FROM v17_source_only_review_coverage ORDER BY entry_id")
 c.close()
 write("V17_160_DIRECT_SOURCE_PNG_VISUAL_PART_CLASSIFICATIONS.csv",observed)
 write("V17_2231_FULL_FURNITURE_CANDIDATE_MASTER.csv",registry)
 write("V17_963_SOURCE_ONLY_PER_GROUP_REVIEW_STATUS.csv",coverage)
 write("V17_483_UNREVIEWED_SOURCE_ONLY_QUEUE.csv",unreviewed)
 write("V17_480_COMBINED_IMAGE_SHAPE_COUNTS.csv",[
  dict(observed_broad_part_class=k,one_original_sprite_per_source_group_count=v,
   full_game_furniture_assemblies_certified=0) for k,v in sorted(allclasses.items())])
 write("V17_12_SCOPED_PROGRESS.csv",prog)
 status=dict(version="v17",source_v16_zip_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
  known_catalog_rows=2231,wiki_reference_rows=1268,source_only_group_candidates=963,
  wiki_image_source_id_linked=1257,wiki_image_id_unlinked=11,
  original_raw_tiledef_property_rows=195265,original_source_slots=73644,
  candidate_tile_keys=8219,directional_template_candidates=3840,
  raw_container_source_links=1855,
  prior_visual_v15_groups=160,prior_visual_v16_groups=160,v17_new_direct_visual_groups=160,
  verified_disjoint_unique_single_sprite_visual_groups=480,
  reviewed_source_only_single_sprite_pct=round(100*480/963,2),
  source_only_groups_awaiting_single_sprite_visual_review=483,
  v17_new_visual_part_shape_counts=dict(sorted(newclasses.items())),
  all_480_single_sprite_part_shape_counts=dict(sorted(allclasses.items())),
  previous_work_107_groups_574_tiles_reported_without_confirmed_ID_rows=True,
  previous_work_reported_groups=107,previous_work_reported_tiles=574,
  distinct_review_lower_bound=480,distinct_review_max_if_all_Work_groups_disjoint=587,
  max_possible_coverage_pct_if_all_Work_disjoint=round(100*587/963,2),
  prior_129_duplicate_group_image_references=129,
  source_only_963_not_proven_missing_from_Wiki=True,
  wiki_is_potentially_outdated_or_incomplete=True,
  visual_review_is_only_one_tile_not_whole_furniture=True,
  whole_assembled_furniture_certified=0,exact_game_object_identities_verified=0,
  unresolved_original_warnings=474,lua_loot_TMX_minecraft_implementation_unstarted=True,
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(status,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 가구 원장 v17 — 2,231 현재 수집 목록 + 원본 단일 타일 시각 검수 480그룹\n\n"
 "게임 원본 TileDef·PNG 우선, 위키는 최신·완전성이 검증되지 않은 참고 자료입니다.\n"
 "현재 확보된 목록 2,231행의 자료 등록은 완료했지만 고유 게임 가구 2,231종 확정은 아닙니다.\n"
 "원본 전용 그룹 963개도 '위키에 없다'거나 고유 가구라는 뜻이 아니며 건축·자연·기계 등이 포함됩니다.\n"
 "v15/v16 320그룹과 교차하지 않는 새 원본 PNG 160개의 실제 단일 타일 이미지를 시각적으로 관찰해 임시 광의 분류를 추가했습니다.\n"
 "DB에 개별 원본 PNG SHA256, 픽셀 SHA256, 접촉시트 SHA256를 기록합니다. 합산 480/963=49.84%, 미검수 483.\n"
 "이 수치는 대표 스프라이트 한 장의 광의 형태 관찰 범위이며 완성 가구 조립/4방향 정체/게임 오브젝트 인증이 아닙니다.\n"
 "Work 107그룹/574타일 보고분은 행별 그룹ID를 확인하지 못해 실제 고유 480에 합산하지 않았습니다.\n"
 "이전 중복 위키 공유 129그룹의 시각 검수 참조는 계속 보존, 원본 474 경고 아직 미해결, Lua loot/TMX/마인크래프트 구현 미진행.\n",
 encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if f.is_file() and f!=PACK and not f.name.startswith("STAGED_") and
     not f.name.endswith("_BASE64.txt") and not f.name.startswith("_v17_required"):
    z.write(f,f.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V17_MASTER2231_UNIQUE480_SOURCE_VISUAL_REVIEW_FULL_DB_VALIDATED",json.dumps(status,ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
