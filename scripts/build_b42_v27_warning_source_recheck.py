#!/usr/bin/env python3
"""v27 part 2: independent rejoin of every original 474 unresolved warnings to TileDef and PNG index.
All source rows and prior visual evidence copied from v26. Zero warnings are auto-cleared.
"""
from pathlib import Path
from collections import defaultdict,Counter
import csv,json,sqlite3,zipfile,hashlib
R=Path(__file__).resolve().parents[1]
O=R/"analysis/furniture_full_b42/2026-11-05/missing_atlas_warning_v27"
DB=O/"B42_FURNITURE_SOURCE_AUDIT_V27.sqlite"
PACK=O/"B42_FURNITURE_SOURCE_AUDIT_V27.zip"
def qr(c,q):return [dict(r) for r in c.execute(q)]
def cnt(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def add(c,t,row):
 cols=list(row);c.execute("INSERT INTO "+t+"("+",".join(cols)+") VALUES("+",".join("?" for _ in cols)+")",list(row.values()))
def csvout(n,items):
 assert items,n
 with (O/n).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
def J(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def main():
 assert DB.is_file() and not PACK.exists()
 stage=json.loads((O/"V27_PNG_STAGE_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["source_group_count"]==23 and stage["original_missing_source_tile_keys"]==89
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,n in {"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,
  "registry_entry":2231,"wiki_furniture":1268,"v12_template_proof":3840,
  "v12_tile_proof":8219,"v13_warning_case":474,"v13_storage_link":1855,
  "v14_source_only_ledger":963,"v20_23_original_atlas_filename_audit":23,
  "v26_all_820_source_direction_grid_visual_evidence":820,
  "v27_missing_atlas_group":23,"v27_missing_atlas_source_key":89,
  "v27_three_absent_atlas_filenames":3}.items():
  assert cnt(c,t)==n,(t,cnt(c,t),n)
 warn=qr(c,"SELECT * FROM v13_warning_case ORDER BY priority,group_id,Facing,warning_code")
 original={(r["group_id"],r["Facing"],r["issue"]) for r in qr(c,
  "SELECT group_id,Facing,issue FROM v12_warning_proof")}
 assert len(original)==len(warn)==474
 bypart=defaultdict(list)
 for r in qr(c,"SELECT group_id,Facing,warning_code,source_key,raw_grid FROM v13_warning_part"):
  bypart[(r["group_id"],r["Facing"],r["warning_code"])].append(r)
 tile={r["source_key"]:r for r in qr(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 raw={(r["group_id"],r["Facing"],r["source_key"]):r for r in qr(c,
  "SELECT group_id,Facing,source_key,original_grid FROM v12_tile_proof")}
 indexed=defaultdict(set)
 for r in qr(c,"SELECT tileset,local_id,png_path FROM image_cells WHERE tileset IS NOT NULL AND local_id IS NOT NULL"):
  try:key=f'{r["tileset"]}/{int(r["local_id"])}'
  except (TypeError,ValueError):continue
  indexed[key].add(r["png_path"])
 required={
  "MULTIPLE_CONTAINER_TYPES":("SOURCE_CONTAINER_TYPE_CONFLICT","GAME_OBJECT_CONTAINER_LOGIC_OR_STATE_PROOF"),
  "MULTIPLE_RAW_CAPACITIES":("SOURCE_CAPACITY_CONFLICT","GAME_OBJECT_CONTAINER_LOGIC_OR_STATE_PROOF"),
  "DUPLICATE_POSITION":("SOURCE_DUPLICATE_GRID_POSITION","STATE_VARIANT_ALTERNATIVES_OR_RUNTIME_SPRITEGRID"),
  "MISSING_GRID":("SOURCE_MULTISPRITE_MISSING_COORDINATES","ACTUAL_GAME_OBJECT_PART_RULES"),
  "INCOMPLETE_GRID":("SOURCE_RECTANGLE_WITH_HOLES","ACTUAL_IN_GAME_SHAPE_AND_SOURCE_SPRITEGRID"),
  "MULTIPLE_EXACT_WIKI_ROWS":("WIKI_REUSES_SOURCE_ANCHOR","EDITED_WIKI_PROVENANCE_AND_GAME_OBJECT_IDENTIFIER"),
  "MULTIPLE_NO_GRID":("SOURCE_MULTISPRITES_WITHOUT_GRID","ACTUAL_IN_GAME_OBJECT_ASSEMBLY_RULES")
 }
 c.executescript("""
 CREATE TABLE v27_warning_source_recheck(
  group_id TEXT,Facing TEXT,warning_code TEXT,original_priority INTEGER,
  original_custom_name TEXT,original_tileset TEXT,
  source_tile_count INTEGER,source_keys_json TEXT,
  number_tile_parts_individually_crosschecked INTEGER,
  source_keys_with_original_image_index INTEGER,
  source_keys_without_image_index INTEGER,
  original_indexed_png_paths_json TEXT,
  original_geometry_status TEXT,original_holes_json TEXT,
  original_collisions_json TEXT,exact_original_wiki_anchors_json TEXT,
  issue_source_interpretation TEXT,required_independent_evidence TEXT,
  original_warning_status TEXT DEFAULT 'UNRESOLVED',
  exact_in_game_furniture_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,warning_code));
 CREATE TABLE v27_warning_type_evidence_matrix(
  warning_code TEXT PRIMARY KEY,case_count INTEGER,
  source_tile_part_rows_in_cases INTEGER,distinct_original_groups INTEGER,
  cases_with_all_tiles_image_indexed INTEGER,
  cases_with_zero_tiles_image_indexed INTEGER,
  cases_with_partial_tile_image_index INTEGER,
  cases_resolved INTEGER DEFAULT 0,required_next_evidence TEXT);
 CREATE TABLE v27_source_scoped_progress(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,percent REAL,
  evidence_category TEXT,scope_limit TEXT);
 """)
 cases=[];bycode=defaultdict(list)
 for w in warn:
  key=(w["group_id"],w["Facing"],w["warning_code"])
  assert key in original and w["warning_code"] in required
  parts=bypart[key]
  keys=json.loads(w["source_keys_json"])
  assert len(keys)==len(parts)==w["source_tile_count"],(key,len(keys),len(parts),w["source_tile_count"])
  assert set(keys)=={p["source_key"] for p in parts}
  assert all(k in tile and tile[k]["group_id"]==w["group_id"] for k in keys)
  assert all((w["group_id"],w["Facing"],k) in raw for k in keys)
  for p in parts:
   a=raw[(w["group_id"],w["Facing"],p["source_key"])]
   assert (p["raw_grid"] or "")==(a["original_grid"] or "")==(tile[p["source_key"]]["SpriteGridPos"] or "")
  indexedparts=sum(bool(indexed.get(k)) for k in keys)
  linkedpng=sorted({p for k in keys for p in indexed.get(k,[]) if p})
  meaning,need=required[w["warning_code"]]
  r=dict(group_id=w["group_id"],Facing=w["Facing"],warning_code=w["warning_code"],
   original_priority=int(w["priority"]),original_custom_name=w["CustomName"] or "",
   original_tileset=w["tileset"] or "",
   source_tile_count=len(keys),source_keys_json=J(keys),
   number_tile_parts_individually_crosschecked=len(parts),
   source_keys_with_original_image_index=indexedparts,
   source_keys_without_image_index=len(keys)-indexedparts,
   original_indexed_png_paths_json=J(linkedpng),
   original_geometry_status=w["geometry_status"] or "",
   original_holes_json=w["geometry_holes_json"] or "[]",
   original_collisions_json=w["geometry_collisions_json"] or "[]",
   exact_original_wiki_anchors_json=w["exact_wiki_anchors_json"] or "[]",
   issue_source_interpretation=meaning,required_independent_evidence=need)
  add(c,"v27_warning_source_recheck",r);cases.append(r);bycode[w["warning_code"]].append(r)
 assert len(cases)==474 and set(bycode)==set(required)
 expect={"MULTIPLE_CONTAINER_TYPES":1,"MULTIPLE_RAW_CAPACITIES":5,"DUPLICATE_POSITION":27,
  "MISSING_GRID":52,"INCOMPLETE_GRID":14,"MULTIPLE_EXACT_WIKI_ROWS":125,
  "MULTIPLE_NO_GRID":250}
 assert {k:len(v) for k,v in bycode.items()}==expect
 matrix=[]
 for code,records in sorted(bycode.items()):
  a=sum(r["source_keys_without_image_index"]==0 for r in records)
  z=sum(r["source_keys_with_original_image_index"]==0 for r in records)
  p=sum(0<r["source_keys_with_original_image_index"]<r["source_tile_count"] for r in records)
  assert a+z+p==len(records)
  row=dict(warning_code=code,case_count=len(records),
   source_tile_part_rows_in_cases=sum(r["source_tile_count"] for r in records),
   distinct_original_groups=len({r["group_id"] for r in records}),
   cases_with_all_tiles_image_indexed=a,
   cases_with_zero_tiles_image_indexed=z,
   cases_with_partial_tile_image_index=p,
   required_next_evidence=required[code][1])
  add(c,"v27_warning_type_evidence_matrix",row);matrix.append(row)
 metrics=[
  ("original_source_multitile_grid_image_review",820,820,"DIRECT_PNG","Only geometry candidate images"),
  ("source_only_original_one_cell_image_review",940,963,"DIRECT_PNG","Missing original atlas for 23 groups"),
  ("missing_png_source_groups_filenames_proven_absent",23,23,"GIT_FILENAME_AND_TILEDEF","Not recovered or resolved"),
  ("missing_original_atlas_tile_keys_traced",89,89,"SOURCE_TILEDEF","Pixel source not available"),
  ("original_warning_cases_individually_evidence_checked",474,474,"SOURCE_RECHECK","Not resolved"),
  ("original_warning_cases_certified_resolved",0,474,"UNRESOLVED","No independent game-object evidence"),
  ("missing_original_atlas_group_mappings_recovered",0,23,"UNRESOLVED","3 exact source atlas PNG still unavailable"),
  ("exact_runtime_furniture_object_identity_verified",0,0,"UNKNOWN_TOTAL","No runtime registry evidence")
 ]
 scores=[]
 for k,n,den,kind,limit in metrics:
  r=dict(metric_key=k,numerator=n,denominator=den,percent=round(100*n/den,2) if den else None,
   evidence_category=kind,scope_limit=limit)
  add(c,"v27_source_scoped_progress",r);scores.append(r)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for table,n in {"v27_warning_source_recheck":474,"v27_warning_type_evidence_matrix":7,
  "v27_source_scoped_progress":8,"v27_missing_atlas_group":23,
  "v27_missing_atlas_source_key":89,"v26_all_820_source_direction_grid_visual_evidence":820}.items():
  assert cnt(c,table)==n,table
 assert c.execute("SELECT COUNT(*) FROM v27_warning_source_recheck WHERE original_warning_status!='UNRESOLVED'").fetchone()[0]==0
 c.close()
 csvout("V27_474_UNRESOLVED_WARNING_SOURCE_PROOFS.csv",cases)
 csvout("V27_7_WARNING_TYPE_ACTION_MATRIX.csv",matrix)
 csvout("V27_8_SCOPE_LIMITED_PROGRESS.csv",scores)
 manifest=dict(version="v27",
  source_v26_full_db_hash=stage["original_v26_zip_sha256"],
  retained_TileDef_original_properties=195265,retained_source_raw_slots=73644,
  retained_all_source_candidate_tile_keys=8219,
  retained_current_registered_Wiki_and_source_rows=2231,
  all_multitile_source_group_facing_visual_reviews=820,
  source_only_one_original_png_sprite_reviewed=940,
  missing_source_png_groups=23,missing_exact_atlas_filenames=3,
  affected_source_tile_keys=89,missing_by_atlas=stage["groups_by_atlas"],
  missing_source_tile_keys_by_atlas=stage["tile_keys_by_atlas"],
  original_warning_cases_independently_crosschecked=474,
  original_warning_cases_by_code=expect,
  warning_cases_with_every_part_image_indexed=sum(r["source_keys_without_image_index"]==0 for r in cases),
  warning_cases_with_no_parts_image_indexed=sum(r["source_keys_with_original_image_index"]==0 for r in cases),
  warning_cases_with_partial_image_index=sum(0<r["source_keys_with_original_image_index"]<r["source_tile_count"] for r in cases),
  exact_source_png_assets_recovered=0,original_warning_cases_resolved=0,
  original_Wiki_can_be_outdated_or_missing=True,
  candidate_registry_not_same_as_unique_game_furniture_census=True,
  runtime_object_identity_certified=0,
  Lua_TMX_Minecraft_not_started=True,
  sqlite_integrity="ok",zip_crc="ok")
 (O/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 (O/"README_KO.md").write_text(
 "# B42 가구 원본 근거 검증 v27: 미연결 23그룹·89타일 및 경고 474건\n\n"
 "기존 v26 전체 SQLite와 원본 TileDef·Wiki 연결 증거·이미지 820건 및 초기 속성 195,265행을 그대로 보존했습니다. 신규 해결 건수를 부풀리지 않습니다.\n\n"
 "현재 원본 Git 및 사용자 Drive의 Tiles/2x에서 정확한 PNG 파일명 3종이 누락돼 있습니다.\n"
 "- crafted_03.png: source-only 17그룹 / 17 원본 타일\n"
 "- lighting_indoor_01_on.png: source-only 5그룹 / 24 원본 타일 (lighting_indoor_01.png 임의 대체 금지)\n"
 "- e_newsnow_ground_1.png: source-only 1그룹 / 48 원본 타일 (가구인지 의문이 있는 눈 지면 타일셋)\n"
 "3종 PNG의 정확한 원본 파일 확보 전에는 픽셀·가구 정체를 인증할 수 없습니다.\n\n"
 "경고 474건: MULTIPLE_NO_GRID 250, MULTIPLE_EXACT_WIKI_ROWS 125, MISSING_GRID 52, DUPLICATE_POSITION 27, INCOMPLETE_GRID 14, MULTIPLE_RAW_CAPACITIES 5, MULTIPLE_CONTAINER_TYPES 1.\n"
 "매 경고별로 source_key/원본 SpriteGridPos/이미지 인덱스/추가 확인이 필요한 규칙을 다시 대조해 CSV 및 SQLite로 정리했습니다. 해결 판정 0/474, 원본 PNG 미연결 해결 0/23.\n"
 "위키 최신성은 확인되지 않았으며, 외형이나 이름만으로 실제 게임 객체의 동일성을 인증하지 않습니다. 마인크래프트 구현, Lua loot/TMX 맵 작업 보류.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(O.iterdir()):
   if f.is_file() and f not in (PACK,DB):z.write(f,f.name)
  z.write(DB,DB.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V27_23_MISSING_PNG_89_KEYS_3_ATLASES_474_ORIGINAL_SOURCE_WARNINGS_INDIVIDUALLY_AUDITED_FULL_SQLITE_ZIP_CRC_PASS",J(manifest))
if __name__=="__main__":main()
