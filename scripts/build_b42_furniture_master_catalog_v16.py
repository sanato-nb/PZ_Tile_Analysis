#!/usr/bin/env python3
"""B42 v16: new independent 160 original-sprite visual observations + 2231 inventory evidence matrix.
Wiki may be stale or missing items. A screenshot/visual form never certifies in-game object ID.
"""
import csv,hashlib,json,shutil,sqlite3,zipfile
from pathlib import Path
from collections import Counter,defaultdict
R=Path(__file__).resolve().parents[1]
INZIP=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v15/B42_FURNITURE_COARSE_VISUAL_REVIEW_V15.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v16"
DB=OUT/"B42_FURNITURE_MASTER_INVENTORY_V16.sqlite"
PACK=OUT/"B42_FURNITURE_MASTER_INVENTORY_V16.zip"
GROUPS={"FURNITURE_TABLE_OR_COUNTER_PART":[161,163,164,165,166,167,168,173,174,186,282,301,302,303,304],"FURNITURE_SEATING_PART":[162,170],"FURNITURE_STORAGE_OR_SHELVING_PART":[193,235,236,244,285,286,291,292,300],"STRUCTURE_OR_ARCHITECTURAL_PART":[171,172,178,180,188,189,216,222,223,224,269,270,271,272,277,297,298,299],"SIGN_POSTER_WALL_GRAPHIC":[169,176,191,192,208,209,210,211,212,215,225,226,227,228,230,231,232,241,242,249,250,257,263,264,278,279,305,306,307,308,316,317],"EQUIPMENT_OR_APPLIANCE":[177,181,182,183,184,185,194,195,196,234,237,238,239,240,245,262,280,281,289,290,293,296],"LIGHTING_OR_STRING_LIGHT":[197,198,199,200,201,202,203,204,205],"SHELTER_PART":[187,190,219,220,221,283],"RUG_OR_GROUND_DECOR":[179,207,217,218,248,284],"DECORATIVE_SCULPTURE_OR_BUNTING":[213,229,246,247,276,294,295],"MATERIAL_OR_LOOSE_ITEM":[206,233,243,256,287],"NATURAL_BOULDER_OR_VEGETATION":[251,252,253,254,255,258,259,260,261,273,274,275,318,319,320],"AGRICULTURE_SOIL_OR_CROP_ROW":[265,266,267,268,288,309,310,311,312,313,314,315],"VISUALLY_INDETERMINATE":[214],"PLUMBING_SINK_OR_FIXTURE":[175]}
def allrows(c,sql):return [dict(x) for x in c.execute(sql)]
def emit(name,records):
 if not records:raise ValueError("empty "+name)
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
def ins(c,t,row):
 c.execute("INSERT INTO "+t+"("+",".join(row)+") VALUES("+",".join("?" for _ in row)+")",list(row.values()))
def J(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def main():
 assert INZIP.exists() and not DB.exists()
 with zipfile.ZipFile(INZIP) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_COARSE_VISUAL_REVIEW_V15.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 with (OUT/"V16_160_NEW_ORIGINAL_PNG_CROP_SHA256.csv").open("r",encoding="utf-8-sig",newline="") as f:
  staged=list(csv.DictReader(f))
 assert len(staged)==160
 staged_manifest=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert staged_manifest["original_png_pixel_crops_ok"]==160 and staged_manifest["overlap_with_v15"]==0
 old_head=hashlib.sha256(INZIP.read_bytes()).hexdigest()
 labels={}
 for cat,ids in GROUPS.items():
  for idx in ids:
   assert 161<=idx<=320 and idx not in labels,(cat,idx)
   labels[idx]=cat
 assert set(labels)==set(range(161,321)),("missing",set(range(161,321))-set(labels))
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for table,n in {"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,
  "registry_entry":2231,"wiki_furniture":1268,"v13_warning_case":474,
  "v13_storage_link":1855,"v14_source_only_ledger":963,
  "v14_wiki_reference_audit":1268,"v15_visual_part_observation":160}.items():
  assert c.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]==n,table
 c.executescript("""
 CREATE TABLE v16_visual_part_observation(
  sample_index INTEGER PRIMARY KEY,entry_id TEXT,source_group_id TEXT,source_key TEXT,
  original_name TEXT,png_path TEXT,source_png_sha256 TEXT,
  original_crop_pixel_sha256 TEXT,contact_sheet_no INTEGER,contact_sheet_sha256 TEXT,
  broad_visual_shape_class TEXT,confidence_scope TEXT,
  visually_viewed_one_original_sprite INTEGER NOT NULL DEFAULT 1,
  assembled_furniture_object_verified INTEGER NOT NULL DEFAULT 0,
  orientation_4way_verified INTEGER NOT NULL DEFAULT 0,
  game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE INDEX v16_viewed_group ON v16_visual_part_observation(source_group_id);
 CREATE TABLE v16_master_furniture_registry(
  entry_id TEXT PRIMARY KEY,registry_source TEXT,original_name TEXT,
  wiki_id TEXT,source_group_id TEXT,original_category TEXT,original_subcategory TEXT,
  original_identity_status TEXT,original_source_tile_links INTEGER,
  directly_verified_wiki_image_id_links INTEGER,
  name_only_unverified_source_expansion_links INTEGER,
  source_only_tile_links INTEGER,original_source_keys_json TEXT,
  original_facing_values_json TEXT,original_container_raw_json TEXT,
  original_capacity_raw_values_json TEXT,
  original_source_group_count INTEGER,
  legacy_129_group_image_review_reference_count INTEGER,
  direct_1cell_source_image_visual_review_rows INTEGER,
  direct_1cell_visual_broad_class TEXT,
  wiki_reference_freshness_confirmed INTEGER NOT NULL DEFAULT 0,
  exact_game_object_identity_confirmed INTEGER NOT NULL DEFAULT 0,
  review_scope_status TEXT);
 CREATE TABLE v16_source_only_review_coverage(
  entry_id TEXT PRIMARY KEY,source_group_id TEXT,original_name TEXT,
  original_sprite_tiles INTEGER,source_sprite_png_mapping_available INTEGER,
  direct_one_cell_visual_reviewed INTEGER,first_direct_visual_review_version TEXT,
  broad_visible_shape TEXT,wiki_name_only_overlap_json TEXT,
  full_furniture_group_assembly_verified INTEGER NOT NULL DEFAULT 0,
  game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v16_scope_progress(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,
  percent REAL,scope_note TEXT,status_kind TEXT);
 """)
 oldv=allrows(c,"SELECT * FROM v15_visual_part_observation ORDER BY sample_index")
 old_ids={r["entry_id"] for r in oldv}
 assert len(old_ids)==160
 source_groups={r["entry_id"]:r for r in allrows(c,"SELECT * FROM v14_source_only_ledger")}
 prev149={r["group_id"] for r in allrows(c,"SELECT * FROM v12_129_visual_reference")}
 assert len(prev149)==129
 ref_index=defaultdict(set)
 for row in allrows(c,"SELECT entry_id,source_group_id FROM registry_entry_group"):
  ref_index[row["entry_id"]].add(row["source_group_id"])
 rawlinks=defaultdict(list)
 for row in allrows(c,"SELECT * FROM registry_entry_tile"):
  rawlinks[row["entry_id"]].append(row)
 containers=defaultdict(list)
 for row in allrows(c,"SELECT * FROM v9_container_evidence"):
  containers[row["entry_id"]].append(row)
 inspected=[]
 now_seen=set()
 for row in staged:
  idx=int(row["sample_index"])
  assert 161<=idx<=320 and idx not in now_seen
  assert row["crop_status"]=="OK" and len(row["png_sha256"])==64 and len(row["crop_pixel_sha256"])==64
  assert row["visually_inspected"]=="0" and row["game_identity_certified"]=="0"
  entry=row["entry_id"]
  assert entry in source_groups and entry not in old_ids
  src=source_groups[entry]
  assert row["group_id"]==src["group_id"]
  assert row["source_key"]==src["original_png_tile_key"]
  sheet=(idx-161)//40+1
  sh=staged_manifest["contact_sheet_sha256"][str(sheet)]
  label=labels[idx]
  conf=("LOW_AMBIGUOUS_SINGLE_SPRITE" if label=="VISUALLY_INDETERMINATE"
   else "MODERATE_SHAPE_ONLY" if label.startswith(("FURNITURE_","EQUIPMENT_","MATERIAL_",
    "STRUCTURE_","PLUMBING_")) else "HIGH_ONLY_FOR_COARSE_VISUAL_SHAPE")
  rec=dict(sample_index=idx,entry_id=entry,source_group_id=src["group_id"],
   source_key=row["source_key"],original_name=src["original_name"],png_path=row["png_path"],
   source_png_sha256=row["png_sha256"],original_crop_pixel_sha256=row["crop_pixel_sha256"],
   contact_sheet_no=sheet,contact_sheet_sha256=sh,
   broad_visual_shape_class=label,confidence_scope=conf)
  ins(c,"v16_visual_part_observation",rec)
  inspected.append(rec)
  now_seen.add(idx)
 assert len(inspected)==160
 assert len({x["entry_id"] for x in inspected})==160
 combined=(oldv+inspected)
 assert len({x["entry_id"] for x in combined})==320
 reviewed={r["entry_id"]:r["observed_broad_part_class"] for r in oldv}
 for r in inspected:reviewed[r["entry_id"]]=r["broad_visual_shape_class"]
 coverage=[]
 for entry,src in sorted(source_groups.items()):
  did=int(entry in reviewed)
  rec=dict(entry_id=entry,source_group_id=src["group_id"],
   original_name=src["original_name"],original_sprite_tiles=src["original_tile_count"],
   source_sprite_png_mapping_available=src["image_mapping_present"],
   direct_one_cell_visual_reviewed=did,
   first_direct_visual_review_version=("v15" if entry in old_ids else "v16" if did else "NONE"),
   broad_visible_shape=reviewed.get(entry,""),
   wiki_name_only_overlap_json=src["same_normalized_name_wiki_candidates_json"])
  ins(c,"v16_source_only_review_coverage",rec);coverage.append(rec)
 assert sum(x["direct_one_cell_visual_reviewed"] for x in coverage)==320
 entries=allrows(c,"SELECT * FROM registry_entry ORDER BY entry_id")
 assert len(entries)==2231
 master=[];known_wiki=0
 for e in entries:
  eid=e["entry_id"];l=rawlinks[eid];direct=[x for x in l if x["evidence"]=="EXACT_WIKI_IMAGE_SPRITE_KEY"]
  expanded=[x for x in l if x["evidence"]=="SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED"]
  only=[x for x in l if x["evidence"]=="SOURCE_ONLY_TILEDEF_GROUP"]
  assert len(l)==len(direct)+len(expanded)+len(only)
  if e["source_system"]=="WIKI" and direct:known_wiki+=1
  r=containers[eid]
  legacy=len(ref_index[eid].intersection(prev149))
  is_source=e["source_system"]!="WIKI"
  inspection=int(eid in reviewed)
  if is_source:state="ONE_RAW_TILE_VISUAL_REVIEWED_NOT_WHOLE_FURNITURE" if inspection else "WAITING_FOR_SOURCE_ONLY_SINGLE_TILE_VISUAL_REVIEW"
  elif direct:state="WIKI_IMAGE_ID_LINKED_NOT_GAME_OBJECT_CERTIFIED"
  else:state="WIKI_ITEM_SOURCE_ID_NOT_FOUND"
  record=dict(entry_id=eid,registry_source=e["source_system"],
   original_name=e["display_name"],wiki_id=e["wiki_id"],
   source_group_id=e["source_group_id"],original_category=e["category"],original_subcategory=e["subcategory"],
   original_identity_status=e["identity_status"],original_source_tile_links=len(l),
   directly_verified_wiki_image_id_links=len(direct),
   name_only_unverified_source_expansion_links=len(expanded),
   source_only_tile_links=len(only),
   original_source_keys_json=J(sorted({x["source_key"] for x in l})),
   original_facing_values_json=J(sorted({x["source_sprite_facing"] for x in l if x["source_sprite_facing"]})),
   original_container_raw_json=J(sorted({x["container_type"] for x in r if x["container_type"]})),
   original_capacity_raw_values_json=J(sorted({str(x["capacity_raw"]) for x in r if x["capacity_raw"] not in ("",None)})),
   original_source_group_count=len(ref_index[eid]),
   legacy_129_group_image_review_reference_count=legacy,
   direct_1cell_source_image_visual_review_rows=inspection,
   direct_1cell_visual_broad_class=reviewed.get(eid,""),review_scope_status=state)
  ins(c,"v16_master_furniture_registry",record);master.append(record)
 assert known_wiki==1257,known_wiki
 assert sum(x["registry_source"]=="WIKI" for x in master)==1268
 assert sum(x["registry_source"]!="WIKI" for x in master)==963
 # Archived Work figures as audit only: no 107 actual keys, so do not merge into verified unique 320.
 metrics=[
  ("known_entries_registered",2231,2231,"100% of currently collected candidate rows, not all game furniture", "CATALOG"),
  ("wiki_reference_rows_registered",1268,1268,"Wiki is potentially stale/incomplete", "REFERENCE"),
  ("wiki_image_source_tile_ID_connected",1257,1268,"Wiki image IDs linked to source; does not prove unique furniture", "CROSSWALK"),
  ("source_only_groups_registered",963,963,"Source-only = without exact Wiki image ID crosswalk, not proven Wiki absence", "CATALOG"),
  ("source_only_single_original_sprite_direct_visual_view",320,963,"160 v15 + 160 NEW v16, disjoint verified original tile crop images", "SINGLE_SPRITE_VISUAL"),
  ("prior_129_shared_groups_review_reference",129,129,"Prior group-level visual reference, NOT runtime object identity", "LEGACY_VISUAL"),
  ("original_furniture_candidate_tile_provenance",8219,8219,"Original tile-level attributes and source positions preserved", "SOURCE"),
  ("source_facing_assembly_candidate_geometry",3840,3840,"Group×Facing geometric candidates, not confirmed complete objects", "GEOMETRY"),
  ("storage_tile_source_original_join",1855,1855,"Original storage attributes cross-checked, not Lua loot contents", "STORAGE"),
  ("unresolved_474_original_warnings",0,474,"No warning certified resolved", "OPEN"),
  ("game_object_identification_verified",0,0,"Full in-game object count unknown; percent intentionally undefined", "UNKNOWN_DENOMINATOR")
 ]
 scoped=[]
 for key,num,den,desc,kind in metrics:
  rec=dict(metric_key=key,numerator=num,denominator=den,percent=round(100*num/den,2) if den else None,
   scope_note=desc,status_kind=kind)
  ins(c,"v16_scope_progress",rec);scoped.append(rec)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for table,num in {"source_attributes":195265,"source_slots":73644,"registry_entry":2231,
  "v13_warning_case":474,"v14_source_only_ledger":963,"v15_visual_part_observation":160,
  "v16_visual_part_observation":160,"v16_master_furniture_registry":2231,
  "v16_source_only_review_coverage":963,"v16_scope_progress":len(scoped)}.items():
  assert c.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]==num,(table,num)
 assert c.execute("SELECT COUNT(*) FROM v16_visual_part_observation WHERE assembled_furniture_object_verified!=0 OR orientation_4way_verified!=0 OR game_object_identity_certified!=0").fetchone()[0]==0
 c.close()
 emit("V16_160_NEW_ACTUAL_PNG_VISUAL_PART_CLASSES.csv",inspected)
 emit("V16_2231_MASTER_FURNITURE_CANDIDATE_LIST.csv",master)
 emit("V16_963_SOURCE_ONLY_VISUAL_REVIEW_PROGRESS.csv",coverage)
 emit("V16_11_SCOPED_PROGRESS_METRICS.csv",scoped)
 class_counts=Counter()
 for x in oldv:class_counts[x["observed_broad_part_class"]]+=1
 for x in inspected:class_counts[x["broad_visual_shape_class"]]+=1
 emit("V16_COMBINED_320_COARSE_VISUAL_CLASS_COUNTS.csv",[
  dict(broad_visual_class=k,source_one_tile_samples=n,certified_complete_furniture_count=0)
  for k,n in sorted(class_counts.items())])
 m=dict(version="v16",v15_source_zip_sha256=old_head,
  known_registry_rows=2231,wiki_reference_rows=1268,source_only_candidate_rows=963,
  wiki_source_image_ID_linked_rows=1257,wiki_unlinked_rows=11,
  total_original_source_furniture_candidate_tile_keys=8219,
  source_facing_templates=3840,storage_source_evidence_links=1855,
  original_raw_tile_attributes=195265,original_raw_source_slots=73644,
  v15_prior_visually_reviewed_single_sprite_groups=160,
  v16_new_directly_viewed_disjoint_one_sprite_groups=160,
  combined_confirmed_unique_source_only_one_sprite_groups=320,
  source_only_one_sprite_visual_coverage_pct=round(320/963*100,2),
  source_only_groups_without_single_sprite_visual_review=643,
  prior_v8_129_image_review_groups=129,
  prior_Work_107_group_574_sprite_unverified_overlap_and_individual_db_rows=True,
  prior_Work_reported_group_count=107,prior_Work_reported_sprite_count=574,
  possible_unique_covered_source_only_group_lower_bound=320,
  possible_unique_covered_source_only_group_upper_bound=427,
  unique_coverage_upper_percent=round(427/963*100,2),
  images_160_checked_against_original_png_sha=True,
  v16_new_visual_shape_counts=dict(sorted(Counter(x["broad_visual_shape_class"] for x in inspected).items())),
  v15_and_v16_total_visual_shape_counts=dict(sorted(class_counts.items())),
  source_only_furniture_type_verified=0,assembled_multitile_furniture_verified=0,
  orientation_identity_certified=0,game_object_identities_certified=0,
  unresolved_original_warnings=474,wiki_reference_is_fallible=True,
  original_source_data_preserved=True,lua_tmx_minecraft_not_started=True,
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 v16 — 2,231행 전체 가구 후보 목록 + 원본 PNG 추가 160개 직접 관찰\n\n"
 "위키는 오래되었거나 누락되었을 수 있습니다. 2,231행은 위키 스냅샷 1,268행 + TileDef 원본 전용 후보 963행으로, 고유 게임 가구 수가 아닙니다.\n"
 "위키의 모든 가구를 찾았다는 100% 지표가 아니라 **현재 확보된 목록을 모두 DB 행으로 등록했다는 범위 한정 100%**입니다.\n"
 "위키 이미지 타일 ID 연결 1,257/1,268, 원본 타일 8,219, 방향 템플릿 3,840, 수납 원본 속성 연결 1,855을 보존했습니다.\n"
 "원본 PNG를 직접 보면서 단일 대표 스프라이트 한 장의 넓은 형태를 새로 160건 분류했고, v15 160건과 타일 그룹 중복이 없음(총 320/963 = 33.23%).\n"
 "이는 후보당 단일 타일의 광의 이미지 형태 관찰 범위이며, 320개 가구 전체를 조립하거나 게임 오브젝트 동일성을 인증했다는 뜻이 아닙니다.\n"
 "Work 107그룹/574타일은 개별 그룹 ID/DB 저장 증거 미확인으로 중복 제거/추가 합산을 하지 않고 가능 범위 상한 427/963만 표시합니다.\n"
 "기존 중복 위키 공유 그룹 129의 이미지 검수 참조는 보존했으며, 게임 오브젝트 인증 0건입니다.\n"
 "원본 경고 474건 해결 인증 0, Lua loot/TMX/마크 구현은 진행하지 않음. 실제 원본 TileDef/PNG 중심 검증 계속 필요.\n",
 encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for file in sorted(OUT.iterdir()):
   if file.is_file() and file!=PACK and not file.name.startswith("STAGED_") and
     file.name not in ("_v16_required_png_atlases.txt",) and not file.name.endswith("_BASE64.txt"):
    z.write(file,file.name)
  with zipfile.ZipFile(INZIP) as oldzip:
   for i in range(1,5):
    original="V14_SOURCE_ONLY_ORIGINAL_CONTACT_%02d.png"%i
    z.writestr("V15_PREVIOUS_"+original,oldzip.read(original))
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V16_MASTER2231_SOURCE_REVIEW320_FULL_SQLITE_VERIFIED",json.dumps(m,ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
