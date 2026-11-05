#!/usr/bin/env python3
"""v30: exact source-key coordinate topology for 41 unresolved B42 geometry warnings."""
from pathlib import Path
from collections import Counter,defaultdict
import csv,sqlite3,zipfile,shutil,json,hashlib
R=Path(__file__).resolve().parents[1]
SOURCE=R/"analysis/furniture_full_b42/2026-11-06/container_source_v29/B42_FURNITURE_CONTAINER_SOURCE_V29.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-06/geometry_warning_v30"
DB=OUT/"B42_FURNITURE_GEOMETRY_WARNINGS_V30.sqlite"
PACK=OUT/"B42_FURNITURE_GEOMETRY_WARNINGS_V30.zip"
def q(c,sql):return [dict(x) for x in c.execute(sql)]
def n(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def J(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def ins(c,t,rec):
 ks=list(rec);c.execute("INSERT INTO "+t+"("+",".join(ks)+") VALUES("+",".join("?" for _ in ks)+")",list(rec.values()))
def save(fn,arr):
 assert arr
 with (OUT/fn).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert SOURCE.exists() and not DB.exists() and not PACK.exists()
 OUT.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CONTAINER_SOURCE_V29.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 previous_sha=sha(DB)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
 expected={"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,
 "registry_entry":2231,"v12_tile_proof":8219,"v12_template_proof":3840,
 "v13_warning_case":474,"v13_warning_part":3826,"v27_warning_source_recheck":474,
 "v27_missing_atlas_group":23,"v27_missing_atlas_source_key":89,
 "v26_all_820_source_direction_grid_visual_evidence":820,
 "v28_274_cross_facing_source_metadata":274,"v29_274_storage_completeness":274,
 "v29_12_variation_per_facing":48,"v29_12_variation_per_part":100}
 for t,x in expected.items():assert n(c,t)==x,(t,x,n(c,t))
 template={(r["group_id"],r["Facing"]):r for r in q(c,"SELECT * FROM v12_template_proof")}
 parts=defaultdict(list)
 for p in q(c,"SELECT group_id,Facing,source_key,original_grid,raw_x,raw_y,"
             "source_container,source_capacity_raw FROM v12_tile_proof"):
  parts[(p["group_id"],p["Facing"])].append(p)
 tiles={r["source_key"]:r for r in q(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 wp=defaultdict(set)
 for p in q(c,"SELECT group_id,Facing,warning_code,source_key,raw_grid FROM v13_warning_part"):
  wp[(p["group_id"],p["Facing"],p["warning_code"])].add((p["source_key"],p["raw_grid"]))
 ix=defaultdict(set)
 for p in q(c,"SELECT tileset,local_id,png_path FROM image_cells "
             "WHERE tileset IS NOT NULL AND local_id IS NOT NULL AND png_path IS NOT NULL"):
  try:ix[p["tileset"]+"/"+str(int(p["local_id"]))].add(p["png_path"])
  except (TypeError,ValueError):pass
 warnings=q(c,"SELECT group_id,Facing,warning_code,original_priority,source_tile_count,source_keys_json,"
             "original_warning_status,required_independent_evidence FROM v27_warning_source_recheck")
 assert len(warnings)==474
 selected=[w for w in warnings if w["warning_code"] in ("DUPLICATE_POSITION","INCOMPLETE_GRID")]
 assert Counter(w["warning_code"] for w in selected)=={"DUPLICATE_POSITION":27,"INCOMPLETE_GRID":14}
 c.executescript("""
 CREATE TABLE v30_exact_41_case_topology(
 group_id TEXT,Facing TEXT,warning_code TEXT,raw_part_count INTEGER,
 raw_min_x INTEGER,raw_min_y INTEGER,bbox_width INTEGER,bbox_height INTEGER,
 bbox_cell_count INTEGER,single_occupied_count INTEGER,collision_cell_count INTEGER,
 empty_cell_count INTEGER,extra_source_keys_in_collisions INTEGER,
 collisions_original_coords_json TEXT,holes_original_coords_json TEXT,
 source_keys_at_each_occupied_cell_json TEXT,
 source_part_keys_with_image_index INTEGER,source_part_keys_without_image_index INTEGER,
 other_facing_count INTEGER,other_complete_rectangle_facing_count INTEGER,
 original_warning_resolved INTEGER NOT NULL DEFAULT 0,
 runtime_same_game_object_certified INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(group_id,Facing,warning_code));
 CREATE TABLE v30_exact_source_part_ledger(
 group_id TEXT,Facing TEXT,warning_code TEXT,source_key TEXT,
 original_grid_text TEXT,original_x INTEGER,original_y INTEGER,
 source_keys_at_same_position INTEGER,
 source_container_type_original TEXT,source_container_capacity_original TEXT,
 png_index_paths_json TEXT,png_index_exists INTEGER,
 official_runtime_object_identity_certified INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(group_id,Facing,warning_code,source_key));
 CREATE TABLE v30_source_coordinate_cells(
 group_id TEXT,Facing TEXT,warning_code TEXT,raw_x INTEGER,raw_y INTEGER,
 state TEXT,source_part_count INTEGER,source_keys_json TEXT,
 confirmed_in_game_assembly INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(group_id,Facing,warning_code,raw_x,raw_y));
 CREATE TABLE v30_original_474_warning_action_ledger(
 group_id TEXT,Facing TEXT,warning_code TEXT,original_priority INTEGER,
 new_exact_grid_topology_proof INTEGER,source_part_count INTEGER,
 required_next_evidence TEXT,status TEXT NOT NULL DEFAULT 'UNRESOLVED',
 runtime_object_identity_certified INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(group_id,Facing,warning_code));
 CREATE TABLE v30_other_facing_source_geometry(
 group_id TEXT,warning_facing TEXT,warning_code TEXT,other_facing TEXT,
 source_status TEXT,original_part_count INTEGER,grid_width INTEGER,grid_height INTEGER,
 runtime_furniture_equivalence_certified INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(group_id,warning_facing,warning_code,other_facing));
 """)
 cases=[];tileout=[];cells=[];siblings=[]
 for w in selected:
  g,f,code=w["group_id"],w["Facing"],w["warning_code"]
  assert w["original_warning_status"]=="UNRESOLVED"
  template_row=template[(g,f)]
  # Coordinates are always read from the exact tile/source-key record.
  # A key sorted separately from a position is never used.
  source=parts[(g,f)];assert len(source)==w["source_tile_count"]==template_row["pieces"]
  assert {x["source_key"] for x in source}==set(json.loads(w["source_keys_json"]))
  assert wp[(g,f,code)]=={(x["source_key"],x["original_grid"]) for x in source}
  pos=defaultdict(list)
  for s in source:
   assert s["raw_x"] is not None and s["raw_y"] is not None,(g,f,s["source_key"])
   assert tiles[s["source_key"]]["group_id"]==g
   assert tiles[s["source_key"]]["SpriteGridPos"]==s["original_grid"]
   pos[(s["raw_x"],s["raw_y"])].append(s)
  xmin=min(x for x,y in pos);xmax=max(x for x,y in pos)
  ymin=min(y for x,y in pos);ymax=max(y for x,y in pos)
  width=xmax-xmin+1;height=ymax-ymin+1
  assert width*height<=10000 and (width,height)==(template_row["grid_w"],template_row["grid_h"])
  universe={(x,y) for x in range(xmin,xmax+1) for y in range(ymin,ymax+1)}
  holes=sorted(universe-set(pos))
  collision=sorted((x,y,len(v)) for (x,y),v in pos.items() if len(v)>1)
  stored_holes=sorted(tuple(z) for z in json.loads(template_row["holes_json"]))
  stored_collision=sorted(tuple(z) for z in json.loads(template_row["collisions_json"]))
  assert holes==stored_holes,(g,f,"hole data mismatch")
  assert collision==stored_collision,(g,f,"collision data mismatch")
  if code=="DUPLICATE_POSITION":assert collision,(g,f)
  else:assert code=="INCOMPLETE_GRID" and holes and not collision,(g,f)
  indexed=0
  for s in source:
   paths=sorted(ix[s["source_key"]]);indexed+=bool(paths)
   part=dict(group_id=g,Facing=f,warning_code=code,source_key=s["source_key"],
    original_grid_text=s["original_grid"],original_x=s["raw_x"],original_y=s["raw_y"],
    source_keys_at_same_position=len(pos[(s["raw_x"],s["raw_y"])]),
    source_container_type_original=s["source_container"] or "",
    source_container_capacity_original=s["source_capacity_raw"] or "",
    png_index_paths_json=J(paths),png_index_exists=int(bool(paths)))
   ins(c,"v30_exact_source_part_ledger",part);tileout.append(part)
  for x,y in sorted(universe):
   occupants=pos.get((x,y),[])
   cell=dict(group_id=g,Facing=f,warning_code=code,raw_x=x,raw_y=y,
    state="HOLE" if not occupants else "COLLISION" if len(occupants)>1 else "SINGLE",
    source_part_count=len(occupants),source_keys_json=J(sorted(o["source_key"] for o in occupants)))
   ins(c,"v30_source_coordinate_cells",cell);cells.append(cell)
  other=[r for (gg,ff),r in template.items() if gg==g and ff!=f]
  for o in other:
   r=dict(group_id=g,warning_facing=f,warning_code=code,other_facing=o["Facing"],
    source_status=o["reproduced_status"],original_part_count=o["pieces"],
    grid_width=o["grid_w"],grid_height=o["grid_h"])
   ins(c,"v30_other_facing_source_geometry",r);siblings.append(r)
  record=dict(group_id=g,Facing=f,warning_code=code,raw_part_count=len(source),
   raw_min_x=xmin,raw_min_y=ymin,bbox_width=width,bbox_height=height,
   bbox_cell_count=len(universe),
   single_occupied_count=sum(len(p)==1 for p in pos.values()),
   collision_cell_count=len(collision),empty_cell_count=len(holes),
   extra_source_keys_in_collisions=len(source)-len(pos),
   collisions_original_coords_json=J(collision),
   holes_original_coords_json=J(holes),
   source_keys_at_each_occupied_cell_json=J({f"{x},{y}":sorted(t["source_key"] for t in v) for (x,y),v in sorted(pos.items())}),
   source_part_keys_with_image_index=indexed,
   source_part_keys_without_image_index=len(source)-indexed,
   other_facing_count=len(other),
   other_complete_rectangle_facing_count=sum(o["reproduced_status"]=="COMPLETE_RECTANGLE" for o in other))
  ins(c,"v30_exact_41_case_topology",record);cases.append(record)
 assert len(cases)==41 and len(tileout)==sum(x["raw_part_count"] for x in cases)
 assert len(cells)==sum(x["bbox_cell_count"] for x in cases)
 allqueue=[]
 verified={(x["group_id"],x["Facing"],x["warning_code"]) for x in cases}
 for w in warnings:
  rec=dict(group_id=w["group_id"],Facing=w["Facing"],warning_code=w["warning_code"],
   original_priority=w["original_priority"],
   new_exact_grid_topology_proof=int((w["group_id"],w["Facing"],w["warning_code"]) in verified),
   source_part_count=w["source_tile_count"],required_next_evidence=w["required_independent_evidence"])
  ins(c,"v30_original_474_warning_action_ledger",rec);allqueue.append(rec)
 assert sum(x["new_exact_grid_topology_proof"] for x in allqueue)==41
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for t,cnt in {**expected,"v30_exact_41_case_topology":41,
 "v30_exact_source_part_ledger":len(tileout),"v30_source_coordinate_cells":len(cells),
 "v30_original_474_warning_action_ledger":474,"v30_other_facing_source_geometry":len(siblings)}.items():
  assert n(c,t)==cnt,(t,n(c,t),cnt)
 assert c.execute("SELECT COUNT(*) FROM v30_original_474_warning_action_ledger WHERE status!='UNRESOLVED'").fetchone()[0]==0
 c.close()
 save("V30_41_EXACT_GEOMETRY_CASES.csv",cases)
 save("V30_EXACT_SOURCE_KEY_POSITION_PNG_INDEX.csv",tileout)
 save("V30_PER_CELL_COLLISIONS_AND_HOLES.csv",cells)
 save("V30_474_WARNING_NEXT_EVIDENCE_QUEUE.csv",allqueue)
 if siblings:save("V30_OTHER_DIRECTION_RAW_SHAPES.csv",siblings)
 mani=dict(version="v30",parent_v29_sqlite_sha256=previous_sha,parent_v29_zip_sha256=sha(SOURCE),
 preserved_raw_properties=195265,preserved_raw_source_slots=73644,
 preserved_raw_furniture_tile_keys=8219,preserved_registry_entries=2231,
 previously_directly_screened_multitile_grid_views=820,
 previous_storage_metadata_variation_groups=12,
 total_original_warning_cases=474,original_warnings_resolved=0,
 newly_detailed_raw_geometry_warning_cases=41,
 raw_grid_position_collision_cases=27,raw_grid_rectangle_hole_cases=14,
 source_part_records=len(tileout),position_occupancy_records=len(cells),
 companion_facing_rows=len(siblings),
 raw_duplicated_occupied_coordinates=sum(x["collision_cell_count"] for x in cases),
 raw_hole_coordinates=sum(x["empty_cell_count"] for x in cases),
 raw_parts_with_png_index=sum(x["source_part_keys_with_image_index"] for x in cases),
 raw_parts_without_png_index=sum(x["source_part_keys_without_image_index"] for x in cases),
 collision_cases_with_other_facing_complete_rectangle=sum(x["other_complete_rectangle_facing_count"]>0 for x in cases),
 source_warning_cases_still_unresolved=474,original_png_atlas_missing_groups_still_unresolved=23,
 new_direct_image_reviews=0,game_object_identity_certifications=0,
 isometric_runtime_assembly_certifications=0,sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(mani,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 가구 v30 — 원본 좌표 충돌·빈 칸 개별 원장\n\n"
 "v29 전체 SQLite를 복제하여 기존의 195,265개 원본 속성과 모든 검수·수납·경고 테이블을 유지했습니다.\n\n"
 "기존 474건 경고 중 DUPLICATE_POSITION 27건, INCOMPLETE_GRID 14건 총 41건에 대해 원본 source_key와 해당 원본 SpriteGridPos의 정확한 raw_x/raw_y를 결합한 새 SQLite 원장을 생성했습니다.\n"
 "각 사건의 실제 좌표별 소스 키 목록, 충돌이 있는 셀, 빈 직사각형 셀, 원본 이미지 인덱스 경로, 다른 Facing의 원본 기하 상태를 CSV에도 기록했습니다.\n"
 "이는 출처/기하 증거 추가이지 실제 런타임 상태별 대체 타일 분류 또는 완성 아이소메트릭 가구 인증이 아닙니다. 겹친 좌표의 소스 키를 삭제하거나 병합하지 않았습니다.\n"
 "474건 경고와 23건 PNG 미연결 문제는 해결하지 않았습니다. 신규 시각 관찰 0건, 게임 객체 동일성 인증 0건. Wiki 누락 가능성 유지, TMX/마크 모드 선정 보류.\n",
 encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for fp in sorted(OUT.iterdir()):
   if fp.is_file() and fp!=PACK:z.write(fp,fp.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V30_SOURCE_GEOMETRY_41_CASES_474_WARNINGS_FULL_DB_OK",J(mani),flush=True)
if __name__=="__main__":main()
