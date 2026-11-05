#!/usr/bin/env python3
"""B42 v29: exact source-level storage variation triage, no runtime object identity claims.
Preserves v28 SQLite tables byte-identically by copying base into an independent new DB.
Only joins exact (source group_id, Facing, source_key), never separately sorted IDs/positions.
"""
from pathlib import Path
import csv,hashlib,json,sqlite3,shutil,zipfile
from collections import defaultdict,Counter

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_structure_v28/B42_FURNITURE_CROSS_FACING_STRUCTURE_V28.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-06/container_source_v29"
DB=OUT/"B42_FURNITURE_CONTAINER_SOURCE_V29.sqlite"
ZIP=OUT/"B42_FURNITURE_CONTAINER_SOURCE_V29.zip"
MEMBER="B42_FURNITURE_CROSS_FACING_STRUCTURE_V28.sqlite"
def rows(c,q): return [dict(x) for x in c.execute(q)]
def count(c,name):return c.execute("SELECT COUNT(*) FROM "+name).fetchone()[0]
def j(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def normalize(x):return "" if x is None else str(x).strip()
def insert(c,t,record):
 cols=list(record)
 c.execute("INSERT INTO "+t+"("+",".join(cols)+") VALUES("+",".join("?" for _ in cols)+")",list(record.values()))
def csvsave(name,records):
 assert records,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as fp:
  w=csv.DictWriter(fp,fieldnames=list(records[0]))
  w.writeheader();w.writerows(records)
def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def main():
 assert BASE.is_file() and not DB.exists() and not ZIP.exists()
 OUT.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(BASE) as source:
  assert source.testzip() is None
  assert MEMBER in source.namelist()
  with source.open(MEMBER) as f,DB.open("wb") as dst:shutil.copyfileobj(f,dst)
 base_sqlite_sha=sha(DB)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 preserved={
  "source_attributes":195265, "source_slots":73644,
  "furniture_tile":8219, "registry_entry":2231,
  "wiki_furniture":1268,"v12_template_proof":3840,
  "v13_warning_case":474,"v13_storage_link":1855,
  "v21_all_source_rectangle_template":843,
  "v21_source_tile_positioned_png":2221,
  "v26_all_820_source_direction_grid_visual_evidence":820,
  "v27_missing_atlas_group":23,
  "v27_missing_atlas_source_key":89,
  "v27_warning_source_recheck":474,
  "v28_820_source_facing_structure":820,
  "v28_274_cross_facing_source_metadata":274,
 }
 for table,n in preserved.items():assert count(c,table)==n,(table,count(c,table),n)
 multi=rows(c,"SELECT group_id,source_facing_count,original_container_metadata_same,source_structure_comparison_category FROM v28_274_cross_facing_source_metadata")
 rect={(r["group_id"],r["Facing"]):r for r in rows(c,
   "SELECT group_id,Facing,raw_sprite_part_count,grid_w,grid_h FROM v21_all_source_rectangle_template WHERE raw_sprite_part_count>=2")}
 tile={x["source_key"]:x for x in rows(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 proofs={(x["group_id"],x["Facing"],x["source_key"]):x for x in rows(c,
   "SELECT group_id,Facing,source_key,original_grid,relative_x_when_available,relative_y_when_available FROM v12_tile_proof")}
 parts=defaultdict(list)
 for x in rows(c,"SELECT group_id,Facing,source_key,raw_sprite_grid_pos,relative_x,relative_y,original_png_path,atlas_col,atlas_row,container_type_original,container_capacity_original FROM v21_source_tile_positioned_png"):
  parts[(x["group_id"],x["Facing"])].append(x)
 warning=rows(c,"SELECT group_id,Facing,warning_code,original_priority,original_warning_status,original_geometry_status FROM v27_warning_source_recheck")
 bywarn=defaultdict(list)
 for x in warning:bywarn[x["group_id"]].append(x)
 assert len(warning)==474
 missing=rows(c,"SELECT entry_id,group_id,source_tileset,source_part_count FROM v27_missing_atlas_group")
 missing_group={x["group_id"] for x in missing}
 assert len(missing)==23
 v28={x["group_id"]:x for x in multi}
 assert len(multi)==len(v28)==274
 prev_var={x["group_id"] for x in multi if not x["original_container_metadata_same"]}
 assert len(prev_var)==12
 c.executescript("""
 CREATE TABLE v29_274_storage_completeness(
  group_id TEXT PRIMARY KEY,source_facing_count INTEGER,
  source_tile_part_rows INTEGER,
  all_direction_values_json TEXT,
  storage_source_status TEXT,
  facing_with_any_source_storage INTEGER,
  facing_without_source_storage INTEGER,
  distinct_nonempty_container_types_json TEXT,
  distinct_nonempty_container_capacities_json TEXT,
  within_facing_multiple_values INTEGER DEFAULT 0,
  inherited_v28_cross_facing_variation INTEGER,
  warning_rows_same_group INTEGER,
  missing_original_atlas_in_same_group INTEGER DEFAULT 0,
  game_object_identity_certified INTEGER DEFAULT 0,
  effective_game_container_storage_certified INTEGER DEFAULT 0);
 CREATE TABLE v29_12_variation_per_facing(
  group_id TEXT,Facing TEXT,source_part_count INTEGER,
  facing_source_type_values_json TEXT,
  facing_source_capacity_values_json TEXT,
  source_tiles_with_type INTEGER,
  source_tiles_with_capacity INTEGER,
  source_parts_json TEXT,
  source_png_atlases_json TEXT,
  source_metadata_present INTEGER,
  normalized_game_object_container_proven INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v29_12_variation_per_part(
  group_id TEXT,Facing TEXT,source_key TEXT,
  original_sprite_grid_pos TEXT,relative_x INTEGER,relative_y INTEGER,
  original_png_path TEXT,original_png_atlas_column INTEGER,
  original_png_atlas_row INTEGER,
  exact_source_container_type TEXT,exact_source_container_capacity TEXT,
  type_field_present INTEGER,capacity_field_present INTEGER,
  source_sprite_mapping_verified INTEGER DEFAULT 1,
  source_field_is_runtime_effective INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v29_474_warning_overlap_index(
  group_id TEXT,Facing TEXT,warning_code TEXT,original_priority INTEGER,
  original_geometry_status TEXT,original_warning_status TEXT,
  belongs_to_12_cross_facing_container_variations INTEGER,
  original_source_warning_resolved INTEGER DEFAULT 0,
  game_object_facing_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,warning_code));
 CREATE TABLE v29_23_missing_png_overlap_index(
  entry_id TEXT PRIMARY KEY,group_id TEXT,source_tileset TEXT,source_part_count INTEGER,
  belongs_to_12_container_variations INTEGER,
  original_png_recovered INTEGER DEFAULT 0);
 CREATE TABLE v29_progress_scope(
  metric TEXT PRIMARY KEY,number_checked INTEGER,denominator INTEGER,
  percentage REAL,evidence_scope TEXT,identity_certified INTEGER DEFAULT 0);
 """)
 details=[];face_details=[];summary=[];classification=Counter()
 for rec in sorted(multi,key=lambda x:x["group_id"]):
  group=rec["group_id"]
  allface=sorted([f for (g,f) in parts if g==group])
  assert len(allface)==rec["source_facing_count"]
  face_values=[];face_flags=[];alltype=set();allcaps=set();multivalue=0
  original_tiles=0
  for f in allface:
   rr=rect[(group,f)]
   pp=sorted(parts[(group,f)],key=lambda x:(x["relative_y"],x["relative_x"],x["source_key"]))
   assert len(pp)==rr["raw_sprite_part_count"]>=2
   original_tiles+=len(pp)
   coords=set()
   types=set();caps=set();type_n=cap_n=0
   detailparts=[]
   for p in pp:
    key=(group,f,p["source_key"])
    assert key in proofs and p["source_key"] in tile
    assert tile[p["source_key"]]["group_id"]==group
    assert normalize(p["raw_sprite_grid_pos"])==normalize(tile[p["source_key"]]["SpriteGridPos"])==normalize(proofs[key]["original_grid"])
    assert p["relative_x"]==proofs[key]["relative_x_when_available"] and p["relative_y"]==proofs[key]["relative_y_when_available"]
    assert (p["relative_x"],p["relative_y"]) not in coords
    coords.add((p["relative_x"],p["relative_y"]))
    typ=normalize(p["container_type_original"])
    cap=normalize(p["container_capacity_original"])
    if typ:types.add(typ);type_n+=1
    if cap:caps.add(cap);cap_n+=1
    part=dict(source_key=p["source_key"],
     raw_sprite_grid_pos=p["raw_sprite_grid_pos"],
     relative_x=p["relative_x"],relative_y=p["relative_y"],
     original_png_path=p["original_png_path"],
     original_atlas_column=p["atlas_col"],original_atlas_row=p["atlas_row"],
     original_container_type=typ,original_container_capacity=cap)
    detailparts.append(part)
    if group in prev_var:
     detail=dict(group_id=group,Facing=f,source_key=p["source_key"],
      original_sprite_grid_pos=p["raw_sprite_grid_pos"],
      relative_x=p["relative_x"],relative_y=p["relative_y"],
      original_png_path=p["original_png_path"],
      original_png_atlas_column=p["atlas_col"],original_png_atlas_row=p["atlas_row"],
      exact_source_container_type=typ,exact_source_container_capacity=cap,
      type_field_present=int(bool(typ)),capacity_field_present=int(bool(cap)))
     insert(c,"v29_12_variation_per_part",detail);details.append(detail)
   assert coords=={(x,y) for x in range(rr["grid_w"]) for y in range(rr["grid_h"])}
   assert len(types)<=1 and len(caps)<=1,(group,f,"multiple distinct values within facing",types,caps)
   multivalue|=int(len(types)>1 or len(caps)>1)
   flag=int(bool(types or caps))
   face_flags.append(flag)
   alltype|=types;allcaps|=caps
   value={"Facing":f,"source_keys":sorted(x["source_key"] for x in pp),
          "raw_types":sorted(types),"raw_capacities":sorted(caps),
          "type_labeled_parts":type_n,"capacity_labeled_parts":cap_n,
          "part_count":len(pp)}
   face_values.append(value)
   if group in prev_var:
    face=dict(group_id=group,Facing=f,source_part_count=len(pp),
     facing_source_type_values_json=j(sorted(types)),
     facing_source_capacity_values_json=j(sorted(caps)),
     source_tiles_with_type=type_n,source_tiles_with_capacity=cap_n,
     source_parts_json=j(detailparts),
     source_png_atlases_json=j(sorted({p["original_png_path"] for p in pp})),
     source_metadata_present=flag)
    insert(c,"v29_12_variation_per_facing",face);face_details.append(face)
  cap_signatures={(tuple(v["raw_types"]),tuple(v["raw_capacities"])) for v in face_values}
  varies=int(len(cap_signatures)>1)
  assert varies==int(group in prev_var),(group,varies)
  if not any(face_flags):
   status="NO_ORIGINAL_STORAGE_FIELDS"
   assert not varies
  elif varies:
   status="DIRECTIONAL_SOURCE_FIELD_MISSING" if not all(face_flags) else "DIRECTIONAL_NONEMPTY_VALUE_CONFLICT"
  else:
   status="CONSISTENT_NONEMPTY_SOURCE_FIELDS"
  classification[status]+=1
  s=dict(group_id=group,source_facing_count=len(allface),
   source_tile_part_rows=original_tiles,all_direction_values_json=j(face_values),
   storage_source_status=status,
   facing_with_any_source_storage=sum(face_flags),
   facing_without_source_storage=len(allface)-sum(face_flags),
   distinct_nonempty_container_types_json=j(sorted(alltype)),
   distinct_nonempty_container_capacities_json=j(sorted(allcaps)),
   within_facing_multiple_values=multivalue,
   inherited_v28_cross_facing_variation=varies,
   warning_rows_same_group=len(bywarn[group]),
   missing_original_atlas_in_same_group=int(group in missing_group))
  insert(c,"v29_274_storage_completeness",s);summary.append(s)
 assert len(summary)==274 and sum(classification.values())==274
 assert len(face_details)==sum(x["source_facing_count"] for x in multi if x["group_id"] in prev_var)
 assert len(face_details)==48
 assert len(details)==sum(x["source_part_count"] for x in face_details)
 assert classification["DIRECTIONAL_SOURCE_FIELD_MISSING"]+classification["DIRECTIONAL_NONEMPTY_VALUE_CONFLICT"]==12
 warnrecords=[];warn_overlap=0
 for w in warning:
  flag=int(w["group_id"] in prev_var);warn_overlap+=flag
  record=dict(group_id=w["group_id"],Facing=w["Facing"],warning_code=w["warning_code"],
   original_priority=w["original_priority"],
   original_geometry_status=w["original_geometry_status"],
   original_warning_status=w["original_warning_status"],
   belongs_to_12_cross_facing_container_variations=flag)
  insert(c,"v29_474_warning_overlap_index",record);warnrecords.append(record)
 missingrecords=[]
 for x in missing:
  record=dict(entry_id=x["entry_id"],group_id=x["group_id"],
    source_tileset=x["source_tileset"],source_part_count=x["source_part_count"],
    belongs_to_12_container_variations=int(x["group_id"] in prev_var))
  insert(c,"v29_23_missing_png_overlap_index",record);missingrecords.append(record)
 metrics=[
 ("all_source_multifacing_groups_storage_audited",274,274,"ORIGINAL_SOURCE_STORAGE_ONLY"),
 ("v28_storage_variations_exactly_traced",12,12,"RAW_PROPERTY_DIFFERENCE_NOT_ERROR"),
 ("all_variation_facing_sets_exactly_traced",len(face_details),len(face_details),"SOURCE_GROUP_FACING"),
 ("all_variation_parts_exactly_joined",len(details),len(details),"TILE_SOURCE_KEY_SPRITEGRIDPOS"),
 ("original_warning_rows_crosschecked",474,474,"WARNING_PRESERVED_UNRESOLVED"),
 ("original_absent_atlas_groups_crosschecked",23,23,"MISSING_ASSET_NOT_CLEARED"),
 ("direct_original_image_grids_inherited",820,820,"PREVIOUS_V26_NOT_NEW_INSPECTION"),
 ("runtime_game_object_identity_certified",0,0,"DENOMINATOR_UNKNOWN"),
 ]
 mrows=[]
 for name,done,denom,scope in metrics:
  r=dict(metric=name,number_checked=done,denominator=denom,
   percentage=round(100*done/denom,2) if denom else None,evidence_scope=scope)
  insert(c,"v29_progress_scope",r);mrows.append(r)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for table,n in {**preserved,"v29_274_storage_completeness":274,
  "v29_12_variation_per_facing":len(face_details),
  "v29_12_variation_per_part":len(details),
  "v29_474_warning_overlap_index":474,
  "v29_23_missing_png_overlap_index":23,"v29_progress_scope":len(metrics)}.items():
  assert count(c,table)==n,(table,n,count(c,table))
 assert c.execute("SELECT COUNT(*) FROM v29_274_storage_completeness WHERE game_object_identity_certified<>0 OR effective_game_container_storage_certified<>0").fetchone()[0]==0
 c.close()
 csvsave("V29_274_GROUP_STORAGE_EVIDENCE_COVERAGE.csv",summary)
 csvsave("V29_48_VARIATION_FACING_STORAGE_SOURCE.csv",face_details)
 csvsave("V29_12_VARIATION_ALL_TILE_SOURCE_VALUES.csv",details)
 csvsave("V29_474_WARNINGS_STORAGE_GROUP_CROSSWALK.csv",warnrecords)
 csvsave("V29_23_MISSING_ATLAS_STORAGE_GROUP_CROSSWALK.csv",missingrecords)
 csvsave("V29_8_PROGRESS_METRICS.csv",mrows)
 categories=[dict(storage_source_status=name,group_count=n,
                  actual_game_storage_certified=0) for name,n in sorted(classification.items())]
 csvsave("V29_SOURCE_STORAGE_COVERAGE_CATEGORIES.csv",categories)
 manifest=dict(version="v29",source_v28_zip_sha256=sha(BASE),source_v28_sqlite_sha256=base_sqlite_sha,
  originals_preserved=preserved,
  multi_facing_source_groups_audited=274,source_storage_evidence_classification=dict(classification),
  varying_original_storage_groups=12,
  verified_original_direction_rows_for_12=48,
  exact_source_part_rows_in_12_variations=len(details),
  original_warning_rows_crosschecked=474,
  original_warnings_overlapping_12_variation_groups=warn_overlap,
  original_distinct_warning_groups_overlapping_12_variations=len({w["group_id"] for w in warning if w["group_id"] in prev_var}),
  original_absent_png_groups_crosschecked=23,
  original_absent_png_groups_overlapping_12_variations=sum(x["belongs_to_12_container_variations"] for x in missingrecords),
  prior_direct_source_image_grid_reviews_inherited=820,
  new_direct_image_reviews=0,
  game_runtime_furniture_identifications=0,effective_runtime_container_rules_certified=0,
  source_original_warnings_resolved=0,source_original_png_gaps_resolved=0,
  wiki_reference_may_be_incomplete=True,
  original_source_fields_not_final_runtime_storage=True,
  sqlite_integrity="ok",foreign_key_check="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 summary_ko=(
  "# B42 가구 v29 — 수납 원본 속성의 방향별 누락과 실제 동일성 인증 구분\n\n"
  "기준: 성공한 v28 SQLite ZIP을 **새 파일로 복제**했고 기존 원본 테이블과 이전 증거는 건드리지 않았습니다.\n\n"
  "검수: 다방향 기하 그룹 274개를 각 Facing의 정확한 원본 source_key/SpriteGridPos에 개별 연결하여 원본 ContainerType/ContainerCapacity의 **존재 여부와 값**을 확인했습니다.\n"
  f"- 그룹별 분류: \`{j(dict(classification))}\`.\n"
  f"- v28의 12개 예외: 48개 Facing, 원본 부품 {len(details)}개. 각 원본 부품의 용량·타입 유무, 좌표·아틀라스·방향을 CSV/SQLite에 보존했습니다.\n"
  f"- 기존 원본 경고 474건 중 해당 12그룹과 group_id가 겹치는 경고 {warn_overlap}건. 같은 그룹이라는 것만으로 동일 원인/게임 오류라고 결론내리지 않았습니다.\n"
  "- 누락 PNG 23그룹도 원본 키를 유지하면서 교차대조. 누락된 파일이나 원본 경고를 임의 해결 처리하지 않았습니다.\n"
  "- 원본 PNG 위치 정보가 있다는 사실과 실제 게임 오브젝트가 무엇인지/수납 용량이 실제 얼마인지 확정하는 것은 별개입니다.\n"
  "- 실제 런타임 오브젝트와 방향별 동일성 인증 0건, 신규 이미지 검수 0건. 게임 내부 SpriteGrid/Container 규칙의 독립 증거가 필요합니다.\n"
  "- 위키가 최신이거나 완전하다고 간주하지 않고, 외형·이름만으로 그룹을 합치지 않았습니다. TMX/마인크래프트 모드와 모델 선택은 보류합니다.\n")
 (OUT/"README_KO.md").write_text(summary_ko,encoding="utf8")
 with zipfile.ZipFile(ZIP,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if f.is_file() and f!=ZIP:z.write(f,f.name)
 with zipfile.ZipFile(ZIP) as z:assert z.testzip() is None and DB.name in z.namelist()
 print("V29_ALL_274_GROUPS_12_ORIGINAL_STORAGE_VARIATIONS_48_FACINGS_FULL_SOURCE_SQLITE_VERIFIED",j(manifest),flush=True)
if __name__=="__main__": main()
