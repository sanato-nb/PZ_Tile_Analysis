#!/usr/bin/env python3
"""B42 v21: full SQLite original-source multipart GRID matrices with direct PNG evidence.
Neither rectangular SpriteGridPos nor similar pixels proves an actual single game furniture object.
"""
import csv,json,sqlite3,hashlib,shutil,zipfile
from collections import Counter,defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1]
BASE=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v20/B42_FURNITURE_MASTER_INVENTORY_V20.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-04/multipart_grid_v21"
DB=OUT/"B42_FURNITURE_MULTIPART_GRID_V21.sqlite"
PACK=OUT/"B42_FURNITURE_MULTIPART_GRID_V21.zip"
def rows(c,sql,args=()):return [dict(x) for x in c.execute(sql,args)]
def cnt(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def J(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def ins(c,table,rec):
 ks=list(rec);c.execute("INSERT INTO "+table+"("+",".join(ks)+") VALUES ("+",".join("?" for _ in ks)+")",list(rec.values()))
def csvread(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def csvwrite(name,arr):
 assert arr,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)
def main():
 assert BASE.is_file() and OUT.is_dir() and not DB.exists()
 stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["v21_rectangular_geometry_templates"]==843
 assert stage["source_geometry_single_tile_rectangles"]==23
 assert stage["source_geometry_actual_multi_tile_rectangles"]==820
 assert stage["rectangle_with_all_source_png_cells"]==843
 assert stage["selected_preview_parts"]==335
 assert stage["rendered_original_multisprite_group_direction_contact_candidates"]==80
 assert stage["source_png_verified_and_cropped_parts"]==335
 assert stage["selected_atlas_pngs"]==29
 rect=csvread("V21_843_ALL_COMPLETE_RECTANGLE_TEMPLATE_SOURCE_AUDIT.csv")
 parts=csvread("V21_ALL_RECTANGLE_EXACT_SOURCE_TILE_POSITION_AND_PNG_MAP.csv")
 preview=csvread("V21_SELECTED_ORIGINAL_MULTIPART_PREVIEW_QUEUE.csv")
 pixel=csvread("V21_SELECTED_PARTS_ORIGINAL_PIXEL_SHA256.csv")
 labels=csvread("V21_80_DIRECT_GRID_CONTACT_VISUAL_OBSERVATIONS.csv")
 assert len(rect)==843 and len(preview)==len(labels)==80 and len(pixel)==335
 assert sum(int(x["original_tile_count"]) for x in rect)==len(parts)
 assert sum(int(x["original_tile_count"])==1 for x in rect)==23
 assert sum(int(x["original_tile_count"])>=2 for x in rect)==820
 assert len({(x["group_id"],x["Facing"]) for x in rect})==843
 assert all(int(x["image_cell_grid_fully_mapped"])==1 and int(x["png_missing_part_count"])==0 for x in rect)
 assert all(x["png_path"].startswith("Tiles/") and x["png_path"].endswith(".png") for x in parts)
 bypreview={int(x["preview_no"]):x for x in preview}
 bylabels={int(x["preview_no"]):x for x in labels}
 assert set(bypreview)==set(bylabels)==set(range(1,81))
 assert len({x["group_id"] for x in preview})==80
 assert len({(x["group_id"],x["Facing"],x["source_key"]) for x in pixel})==335
 for name,sha in stage["contact_sheet_sha256"].items():
  assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==sha,(name,"HASH_DIFFERS")
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_MASTER_INVENTORY_V20.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 baseline={"source_attributes":195265,"source_slots":73644,"registry_entry":2231,
  "wiki_furniture":1268,"furniture_tile":8219,"v12_template_proof":3840,
  "v12_tile_proof":8219,"v13_warning_case":474,"v13_storage_link":1855,
  "v14_source_only_ledger":963,"v20_master_furniture_registry":2231,
  "v20_visual_part_observation":140,"v20_23_original_atlas_filename_audit":23}
 for table,num in baseline.items():assert cnt(c,table)==num,(table,cnt(c,table),num)
 # Crossvalidate geometry and image mapping against independent source tables.
 originalparts={(x["group_id"],x["Facing"],x["source_key"]):x for x in rows(c,
  "SELECT group_id,Facing,source_key,original_grid,relative_x_when_available,relative_y_when_available,source_container,source_capacity_raw FROM v12_tile_proof")}
 originals={(x["group_id"],x["Facing"]):x for x in rows(c,
  "SELECT group_id,Facing,pieces,grid_w,grid_h,reproduced_status FROM v12_template_proof")}
 sources={x["source_key"]:x for x in rows(c,"SELECT source_key,group_id,SpriteGridPos,container_type,ContainerCapacity FROM furniture_tile")}
 for t in rect:
  key=(t["group_id"],t["Facing"]);old=originals[key]
  assert old["reproduced_status"]=="COMPLETE_RECTANGLE"
  assert old["pieces"]==int(t["original_tile_count"])
  assert old["grid_w"]==int(t["raw_grid_width"]) and old["grid_h"]==int(t["raw_grid_height"])
 for p in parts:
  key=(p["group_id"],p["Facing"],p["source_key"])
  t=originalparts[key];source=sources[p["source_key"]]
  assert t["original_grid"]==p["raw_sprite_grid_pos"]==source["SpriteGridPos"]
  assert t["relative_x_when_available"]==int(p["relative_x"])
  assert t["relative_y_when_available"]==int(p["relative_y"])
  assert source["group_id"]==p["group_id"]
  assert (t["source_container"] or "")==p["source_container_raw"]
  assert (t["source_capacity_raw"] or "")==p["source_capacity_raw"]
  assert p["identity_certified"]=="0" and p["whole_furniture_assembly_visual_certified"]=="0"
 c.executescript("""
 CREATE TABLE v21_all_source_rectangle_template(
  group_id TEXT,Facing TEXT,grid_w INTEGER,grid_h INTEGER,
  raw_sprite_part_count INTEGER,source_only_group INTEGER,source_display_name TEXT,
  direct_wiki_group_reference_count INTEGER,original_png_parts_mapped INTEGER,
  original_png_parts_missing INTEGER,
  positional_rectangle_source_verified INTEGER DEFAULT 1,
  actual_one_game_object_certified INTEGER DEFAULT 0,
  completed_in_game_isometric_assembly_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v21_source_tile_positioned_png(
  group_id TEXT,Facing TEXT,source_key TEXT,raw_sprite_grid_pos TEXT,
  raw_x INTEGER,raw_y INTEGER,relative_x INTEGER,relative_y INTEGER,
  raw_source_tileset TEXT,raw_local_id INTEGER,original_png_path TEXT,
  atlas_col INTEGER,atlas_row INTEGER,original_cell_w INTEGER,original_cell_h INTEGER,
  container_type_original TEXT,container_capacity_original TEXT,
  original_source_facing TEXT,
  positional_source_verified INTEGER DEFAULT 1,
  actual_game_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v21_direct_multisprite_grid_visual_observation(
  preview_no INTEGER PRIMARY KEY,group_id TEXT,Facing TEXT,
  raw_sprite_part_count INTEGER,raw_grid_w INTEGER,raw_grid_h INTEGER,
  source_only_group INTEGER,source_name_original TEXT,
  contact_png_filename TEXT,contact_png_sha256 TEXT,
  observed_broad_visible_subject TEXT,observed_grid_visual_pattern TEXT,
  visual_confidence_scope TEXT,observed_direct_original_grid INTEGER DEFAULT 1,
  visual_scope TEXT,
  isometric_game_object_assembled_and_verified INTEGER DEFAULT 0,
  same_game_object_across_facing_certified INTEGER DEFAULT 0,
  exact_game_object_identity_certified INTEGER DEFAULT 0);
 CREATE UNIQUE INDEX v21_grid_review_group_face ON v21_direct_multisprite_grid_visual_observation(group_id,Facing);
 CREATE TABLE v21_reviewed_multisprite_pixel_sha(
  group_id TEXT,Facing TEXT,source_key TEXT,original_png_path TEXT,
  original_png_sha256 TEXT,original_sprite_pixels_sha256 TEXT,
  raw_relative_x INTEGER,raw_relative_y INTEGER,
  original_png_cell_w INTEGER,original_png_cell_h INTEGER,
  sprite_pixels_directly_cropped INTEGER DEFAULT 1,
  exact_game_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v21_cross_facing_source_group_summary(
  group_id TEXT PRIMARY KEY,original_direction_templates INTEGER,
  original_direction_values_json TEXT,
  complete_rectangle_direction_candidates INTEGER,
  complete_rectangle_facing_values_json TEXT,
  distinct_rectangle_shapes_json TEXT,
  all_rectangles_source_grid_proven INTEGER DEFAULT 1,
  actual_same_game_object_across_facings_certified INTEGER DEFAULT 0);
 CREATE TABLE v21_progress_scope(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,percent REAL,
  evidence_scope TEXT,note TEXT);
 """)
 rowdata=[]; partdata=[]
 for row in rect:
  rec=dict(group_id=row["group_id"],Facing=row["Facing"],grid_w=int(row["raw_grid_width"]),
   grid_h=int(row["raw_grid_height"]),raw_sprite_part_count=int(row["original_tile_count"]),
   source_only_group=int(row["source_only_group"]),source_display_name=row["display_name"],
   direct_wiki_group_reference_count=int(row["direct_wiki_group_reference_count"]),
   original_png_parts_mapped=int(row["png_mapped_part_count"]),
   original_png_parts_missing=int(row["png_missing_part_count"]))
  ins(c,"v21_all_source_rectangle_template",rec);rowdata.append(rec)
 for row in parts:
  rec=dict(group_id=row["group_id"],Facing=row["Facing"],source_key=row["source_key"],
   raw_sprite_grid_pos=row["raw_sprite_grid_pos"],raw_x=int(row["raw_x"]),raw_y=int(row["raw_y"]),
   relative_x=int(row["relative_x"]),relative_y=int(row["relative_y"]),
   raw_source_tileset=row["source_tileset"],raw_local_id=int(row["source_local_id"]),
   original_png_path=row["png_path"],atlas_col=int(row["atlas_column"]),
   atlas_row=int(row["atlas_row"]),original_cell_w=int(row["atlas_cell_width"]),
   original_cell_h=int(row["atlas_cell_height"]),
   container_type_original=row["source_container_raw"],
   container_capacity_original=row["source_capacity_raw"],
   original_source_facing=row["source_facing_raw"])
  ins(c,"v21_source_tile_positioned_png",rec);partdata.append(rec)
 visual=[];picked=Counter()
 for i in range(1,81):
  group=bypreview[i];label=bylabels[i]
  assert label["observation_scope"]=="DIRECT_VIEW_OF_POSITIONED_ORIGINAL_PNG_CELLS_NOT_IN_GAME_ASSEMBLY"
  assert label["physical_single_game_object_certified"]=="0"
  page=(i-1)//10+1;fn="V21_MULTIPART_ORIGINAL_SPRITES_GRID_CONTACT_%02d.png"%page
  record=dict(preview_no=i,group_id=group["group_id"],Facing=group["Facing"],
   raw_sprite_part_count=int(group["original_tile_count"]),
   raw_grid_w=int(group["raw_grid_width"]),raw_grid_h=int(group["raw_grid_height"]),
   source_only_group=int(group["source_only_group"]),
   source_name_original=group["display_name"],
   contact_png_filename=fn,contact_png_sha256=stage["contact_sheet_sha256"][fn],
   observed_broad_visible_subject=label["broad_visible_subject"],
   observed_grid_visual_pattern=label["grid_visual_pattern"],
   visual_confidence_scope=label["confidence_scope"],
   visual_scope=label["observation_scope"])
  ins(c,"v21_direct_multisprite_grid_visual_observation",record)
  visual.append(record);picked[record["observed_broad_visible_subject"]]+=1
 images=[]
 for r in pixel:
  rec=dict(group_id=r["group_id"],Facing=r["Facing"],source_key=r["source_key"],
   original_png_path=r["png_path"],original_png_sha256=r["png_sha256"],
   original_sprite_pixels_sha256=r["source_pixel_sha256"],
   raw_relative_x=int(r["relative_x"]),raw_relative_y=int(r["relative_y"]),
   original_png_cell_w=int(r["cell_width"]),original_png_cell_h=int(r["cell_height"]))
  assert len(rec["original_png_sha256"])==len(rec["original_sprite_pixels_sha256"])==64
  ins(c,"v21_reviewed_multisprite_pixel_sha",rec);images.append(rec)
 # Important: a direction's rectangular placement does not certify same object across other directions.
 complete_by_group=defaultdict(list)
 for t in rect:complete_by_group[t["group_id"]].append(t)
 all_by_group=defaultdict(list)
 for t in rows(c,"SELECT group_id,Facing FROM v12_template_proof"):
  all_by_group[t["group_id"]].append(t["Facing"])
 groupface=[]
 for g,tt in sorted(complete_by_group.items()):
  values=sorted(set(x["Facing"] for x in tt))
  allfacings=sorted(set(all_by_group[g]))
  rr=dict(group_id=g,original_direction_templates=len(allfacings),
    original_direction_values_json=J(allfacings),
    complete_rectangle_direction_candidates=len(tt),
    complete_rectangle_facing_values_json=J(values),
    distinct_rectangle_shapes_json=J(sorted({str(x["raw_grid_width"])+"x"+str(x["raw_grid_height"]) for x in tt})))
  ins(c,"v21_cross_facing_source_group_summary",rr);groupface.append(rr)
 multi=sum(x["raw_sprite_part_count"]>=2 for x in rowdata)
 singles=sum(x["raw_sprite_part_count"]==1 for x in rowdata)
 assert (multi,singles)==(820,23)
 assert sum(x["source_only_group"] for x in rowdata)==239
 assert sum(x["original_png_parts_missing"] for x in rowdata)==0
 assert len({(x["group_id"],x["Facing"]) for x in visual})==80
 assert sum(x["source_only_group"] for x in visual)==74
 assert sum(picked.values())==80 and len(images)==335
 metrics=[
 ("all_currently_collected_candidate_registry_rows",2231,2231,"REGISTERED_ONLY","not all game furniture; Wiki may be incomplete"),
 ("source_only_single_sprite_original_image_review",940,963,"ONE_PNG_CELL","23 lack mapped PNG; not full furniture identity"),
 ("directional_source_template_geometry_checked",3840,3840,"SOURCE_GRID","group×Facing candidates only"),
 ("rectangle_with_grid_and_png_source",843,843,"RECTANGLE_SOURCE_ONLY","includes 23 single tile rectangles; not a single object proof"),
 ("multi_part_rectangle_templates_identified",820,820,"MULTI_TILE_CANDIDATES","count only 2+ tile source grid rectangles, not certified furniture"),
 ("direct_multisprite_grid_visual_review",80,820,"DIRECT_ORIGINAL_PNG_GRID","one facing per group, candidate not game object"),
 ("original_parts_with_actual_pixel_sha_record",335,335,"ORIGINAL_PIXEL_HASH","within 80 reviewed grids"),
 ("game_object_identifications_certified",0,0,"UNKNOWN","denominator unknown"),
 ("old_original_warnings_certified_resolved",0,474,"OPEN","all remain unresolved"),
 ("source_only_original_PNG_missing_mapping_resolved",0,23,"OPEN","atlas matches not repaired")
 ]
 prog=[]
 for k,n,den,grade,desc in metrics:
  item=dict(metric_key=k,numerator=n,denominator=den,
   percent=round(100*n/den,2) if den else None,
   evidence_scope=grade,note=desc)
  ins(c,"v21_progress_scope",item);prog.append(item)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for t,n in {**baseline,"v21_all_source_rectangle_template":843,
  "v21_source_tile_positioned_png":len(parts),"v21_direct_multisprite_grid_visual_observation":80,
  "v21_reviewed_multisprite_pixel_sha":335,
  "v21_cross_facing_source_group_summary":len(groupface),"v21_progress_scope":len(metrics)}.items():
  assert cnt(c,t)==n,(t,cnt(c,t),n)
 assert c.execute("""SELECT COUNT(*) FROM v21_direct_multisprite_grid_visual_observation
  WHERE isometric_game_object_assembled_and_verified!=0 OR
  same_game_object_across_facing_certified!=0 OR exact_game_object_identity_certified!=0""").fetchone()[0]==0
 c.close()
 csvwrite("V21_843_RECTANGLES_SOURCE_CROSSCHECKED.csv",rowdata)
 csvwrite("V21_820_ACTUAL_MULTITILE_GEOMETRY_CANDIDATES.csv",[v for v in rowdata if v["raw_sprite_part_count"]>=2])
 csvwrite("V21_23_SINGLE_TILE_RECTANGLE_EXCEPTIONS.csv",[v for v in rowdata if v["raw_sprite_part_count"]==1])
 csvwrite("V21_ALL_RECTANGLE_SOURCE_PARTS_POSITIONED_PNG.csv",partdata)
 csvwrite("V21_80_DIRECT_MULTISPRITE_GRID_VISUAL_REVIEW.csv",visual)
 csvwrite("V21_335_DIRECT_REVIEWED_ORIGINAL_TILE_PIXEL_SHA.csv",images)
 csvwrite("V21_GROUP_FACING_RECTANGLE_COVERAGE.csv",groupface)
 csvwrite("V21_10_SCOPE_LIMITED_PROGRESS.csv",prog)
 summary=dict(version="v21",base_v20_zip_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
  current_candidate_registry_rows=2231,
  original_raw_source_attributes=195265,original_source_slots=73644,
  original_candidate_tile_keys=8219,
  original_directional_geometry_templates=3840,
  source_complete_rectangle_direction_candidates=843,
  source_single_tile_rectangle_direction_candidates=23,
  source_multitile_rectangle_direction_candidates=820,
  geometry_png_index_mapped_rectangles=843,
  source_only_rectangle_direction_candidates=239,
  unique_groups_with_rectangles=len(groupface),
  groups_with_two_or_more_rectangle_facings=sum(x["complete_rectangle_direction_candidates"]>=2 for x in groupface),
  source_geometry_part_rows=len(partdata),
  first_direct_grid_visual_review_group_direction_count=80,
  first_direct_grid_visual_review_unique_group_count=len({x["group_id"] for x in visual}),
  reviewed_source_only_groups=74,reviewed_direct_grid_source_parts=335,
  reviewed_multi_grid_candidates_percent=round(100*80/820,2),
  directly_observed_visual_subject_counts=dict(sorted(picked.items())),
  old_one_sprite_review_source_only_count=940,
  original_source_only_missing_png_group_count=23,
  existing_474_original_warnings_unresolved=True,
  prior_129_visual_review_references_preserved=True,
  prior_Work_107_groups_574_tiles_lacking_individual_source_ids_not_combined=True,
  source_rectangular_grid_does_not_imply_sprites_are_same_object=True,
  original_wiki_reference_may_be_stale_incomplete=True,
  certified_complete_isometric_game_furniture=0,
  certified_cross_direction_same_object=0,
  certified_game_object_identity=0,
  lua_tmx_minecraft_not_started=True,sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# Project Zomboid B42 가구 DB v21 — 정확한 SpriteGridPos를 이용한 부품 이미지 그리드 검증\n\n"
 "v20 전체 SQLite 복제. 원본 TileDef, 속성 195,265, 원본 슬롯 73,644, 후보 타일 8,219, Wiki 근거/940 대표 이미지 검수/474 경고/23 PNG 미연결 근거를 그대로 보존합니다.\n"
 "기존 COMPLETE_RECTANGLE 843건 중 23건은 사실 **단일 타일 1×1**, 정확히 820건이 **두 타일 이상으로 구성된 기하학적 직사각형 후보**임을 독립적으로 확인했습니다.\n"
 "843건 전부의 source_key→SpriteGridPos x/y→원본 png 아틀라스의 cell row/column 연결을 개별 타일마다 검증하여 CSV/SQLite에 저장했습니다.\n"
 "다중 타일 그룹×Facing 후보 820건 중 80건(고유 그룹 80개)의 원본 335개 셀 이미지를 직접 crop 및 SHA 검증하고, 각자의 원본 좌표 그리드 형태로 접촉시트 8장에 배치해 모두 실제 시각 관찰했습니다.\n"
 "일부 그리드는 포스터·간판·바위·동물 가죽과 같이 보이는 유형이어서 **직사각형=게임 내 단일 가구의 부품 조립 확정**이라고 판단할 수 없습니다.\n"
 "80건에 대한 직접 시각 관찰과 '여러 타일의 외형 차이/반복 패턴'만 기록, 정확한 PZ 런타임 오브젝트 이름/4방향 동일성 인증은 하지 않았습니다.\n"
 "중요: 각 이미지는 원본 SpriteGridPos를 반영한 **부품 격자 표시**이며 인게임의 정밀 아이소메트릭 합성도 아니고 하나의 완성 가구 인증도 아닙니다.\n"
 "위키는 오래되거나 누락된 정보가 있을 수 있는 부자료이며 원본(TileDef와 PNG)이 우선입니다. source-only 963건을 고유 가구 963종으로 확정하지 않습니다.\n"
 "기존 474 경고 미해결, 23 PNG 미연결 미해결, 게임 오브젝트 정체 인증 0, Lua/TMX/마인크래프트 구현 보류.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for file in sorted(OUT.iterdir()):
   if (file.is_file() and file!=PACK and not file.name.startswith("STAGED_") and
    not file.name.startswith("_required_") and not file.name.endswith("_BASE64.txt")):
    z.write(file,file.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V21_843_RECTANGLE_GEOMETRY_80_REAL_GRID_CONTACTS_335_ORIGINAL_PNG_PIXELS_FULL_DB_PASSED",
 J(summary),flush=True)
if __name__=="__main__":main()
