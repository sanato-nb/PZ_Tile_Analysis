#!/usr/bin/env python3
"""B42 v26 full SQLite: direct original-PNG source-grid image observations for ALL 820 eligible
multi-tile group×Facing rectangular geometric candidates. None certifies runtime furniture identity.
Preserve original 195265 property lines/73644 source slots/8219 candidate source tiles and prior v25 DB.
"""
import csv,json,sqlite3,zipfile,shutil,hashlib
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v25/B42_FURNITURE_CROSS_FACING_REVIEW_V25.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-05/all_multitile_visual_v26"
DB=OUT/"B42_FURNITURE_SOURCE_GRID_VISUAL_V26.sqlite"
PACK=OUT/"B42_FURNITURE_SOURCE_GRID_VISUAL_V26.zip"
def qr(c,sql,args=()):return [dict(r) for r in c.execute(sql,args)]
def cnt(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def J(o):return json.dumps(o,ensure_ascii=False,sort_keys=True)
def read(name):
 with (OUT/name).open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(name,items):
 assert items,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
def insert(c,tab,row):
 keys=list(row)
 c.execute("INSERT INTO "+tab+"("+",".join(keys)+") VALUES("+",".join("?" for _ in keys)+")",list(row.values()))
def main():
 assert BASE.is_file() and OUT.is_dir() and not DB.exists()
 stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["old_directly_viewed_facing_grids"]==585
 assert stage["new_unreviewed_unique_source_facing_grid_count"]==235
 assert stage["source_pixel_crops_completed"]==583
 assert stage["original_atlases_sha_verified"]==55
 assert stage["contact_sheet_count"]==24
 assert stage["new_unique_source_groups_without_prior_any_facing"]==35
 assert stage["unique_source_groups_in_selected_grid_queue"]==135
 candidates=read("V26_235_SOURCE_FACING_TO_VISUALLY_REVIEW.csv")
 partmap=read("V26_ALL_RAW_SOURCE_PARTS_POSITION_AND_ATLAS_MAP.csv")
 sha=read("V26_ALL_NEW_SPRITE_PIXEL_SHA256.csv")
 labels=read("V26_235_DIRECT_VISUAL_GROUP_SHAPE_OBSERVATIONS.csv")
 assert len(candidates)==len(labels)==235
 assert len(partmap)==len(sha)==583
 byindex={int(x["sample_index"]):x for x in candidates}
 labelindex={int(x["sample_index"]):x for x in labels}
 assert set(byindex)==set(labelindex)==set(range(1,236))
 assert all(x["visual_observation_evidence"]=="DIRECT_SOURCE_PNG_CONTACT_CELL_GRID_MANUALLY_VIEWED_NOT_RUNTIME_IDENTITY" for x in labels)
 assert all(x["exact_game_object_identity_certified"]=="0" for x in labels)
 assert len(stage["original_contact_sheet_sha256"])==24
 for png,hash_value in stage["original_contact_sheet_sha256"].items():
  assert hashlib.sha256((OUT/png).read_bytes()).hexdigest()==hash_value,png
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CROSS_FACING_REVIEW_V25.sqlite") as a,DB.open("wb") as b:
   shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 originals={
  "source_attributes":195265,"source_slots":73644,"registry_entry":2231,
  "wiki_furniture":1268,"furniture_tile":8219,
  "v12_template_proof":3840,"v12_tile_proof":8219,
  "v13_warning_case":474,"v13_storage_link":1855,
  "v14_source_only_ledger":963,"v20_master_furniture_registry":2231,
  "v20_source_only_review_coverage":963,
  "v21_all_source_rectangle_template":843,
  "v21_source_tile_positioned_png":2221,
  "v21_direct_multisprite_grid_visual_observation":80,
  "v22_new_facing_original_grid":120,
  "v23_new_facing_original_source":120,
  "v24_new_facing_original_source":160,
  "v25_pair_facing_source_grid":148,
  "v25_all_820_multitile_direction_visual_ledger":820,
  "v25_235_remaining_direction_queue":235,
  "v25_all_274_multifacing_group_pair_coverage":274
 }
 for t,n in originals.items():assert cnt(c,t)==n,(t,n,cnt(c,t))
 prev=qr(c,"SELECT * FROM v25_all_820_multitile_direction_visual_ledger")
 source_rect={(r["group_id"],r["Facing"]):r for r in qr(c,
   "SELECT group_id,Facing,raw_sprite_part_count,grid_w,grid_h,source_only_group,original_png_parts_mapped FROM v21_all_source_rectangle_template WHERE raw_sprite_part_count>=2")}
 assert len(source_rect)==820 and len(prev)==820
 prior_seen={(p["group_id"],p["Facing"]) for p in prev if p["source_grid_pixels_visually_checked"]}
 assert len(prior_seen)==585
 no_prev={(p["group_id"],p["Facing"]) for p in prev if not p["source_grid_pixels_visually_checked"]}
 assert len(no_prev)==235 and prior_seen.isdisjoint(no_prev) and prior_seen|no_prev==set(source_rect)
 asserted_queue={(r["group_id"],r["Facing"]) for r in qr(c,"SELECT group_id,Facing FROM v25_235_remaining_direction_queue")}
 assert asserted_queue==no_prev
 new={(r["group_id"],r["Facing"]) for r in candidates}
 assert len(new)==235 and new==asserted_queue
 sourcetile={r["source_key"]:r for r in qr(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 raw={(r["group_id"],r["Facing"],r["source_key"]):r for r in qr(c,
   "SELECT group_id,Facing,source_key,original_grid,relative_x_when_available,relative_y_when_available FROM v12_tile_proof")}
 indexed={(r["group_id"],r["Facing"],r["source_key"]):r for r in qr(c,
   "SELECT group_id,Facing,source_key,raw_sprite_grid_pos,relative_x,relative_y,original_png_path,atlas_col,atlas_row,original_cell_w,original_cell_h,container_type_original,container_capacity_original FROM v21_source_tile_positioned_png")}
 for i,x in byindex.items():
  assert x["prior_facing_directly_reviewed"]=="0"
  assert x["exact_game_object_identity_certified"]=="0"
  assert x["original_atlas_cell_all_indexed"]=="1"
  assert labelindex[i]["group_id"]==x["group_id"]
  assert labelindex[i]["Facing"]==x["Facing"]
  assert labelindex[i]["original_group_reference_name"]==x["original_name"]
  rec=source_rect[(x["group_id"],x["Facing"])]
  assert rec["raw_sprite_part_count"]==int(x["source_parts"])
  assert rec["grid_w"]==int(x["grid_w"]) and rec["grid_h"]==int(x["grid_h"])
  assert rec["original_png_parts_mapped"]==int(x["source_parts"])
 c.executescript("""
 CREATE TABLE v26_new_direct_original_png_grid_visual(
  sample_index INTEGER PRIMARY KEY,group_id TEXT,Facing TEXT,
  source_group_original_reference_name TEXT,source_only_group INTEGER,
  original_source_part_count INTEGER,original_grid_w INTEGER,original_grid_h INTEGER,
  contact_png_file TEXT,contact_png_sha256 TEXT,
  broad_visible_shape_observation TEXT,provisional_scope TEXT,
  source_tileset_png_location_verified INTEGER DEFAULT 1,
  all_original_sprite_cells_in_contact_view INTEGER DEFAULT 1,
  original_source_sprite_grid_directly_viewed INTEGER DEFAULT 1,
  runtime_game_object_identity_certified INTEGER DEFAULT 0,
  same_furniture_across_other_facings_certified INTEGER DEFAULT 0,
  UNIQUE(group_id,Facing));
 CREATE TABLE v26_direct_original_sprite_pixels(
  sample_index INTEGER,group_id TEXT,Facing TEXT,source_key TEXT,
  raw_source_sprite_grid_pos TEXT,relative_x INTEGER,relative_y INTEGER,
  original_png_path TEXT,original_png_sha256 TEXT,original_png_cell_pixel_sha256 TEXT,
  original_atlas_col INTEGER,original_atlas_row INTEGER,
  original_sprite_cell_width INTEGER,original_sprite_cell_height INTEGER,
  raw_container_type TEXT,raw_container_capacity TEXT,
  original_source_join_exact INTEGER DEFAULT 1,
  direct_original_sprite_pixel_sha_record INTEGER DEFAULT 1,
  whole_game_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v26_all_820_source_direction_grid_visual_evidence(
  group_id TEXT,Facing TEXT,source_part_count INTEGER,source_grid_w INTEGER,
  source_grid_h INTEGER,source_only_group INTEGER,
  direct_original_png_visual_review_version TEXT,
  direct_png_contact_grid_visually_reviewed INTEGER DEFAULT 1,
  source_sprite_grid_positions_checked INTEGER DEFAULT 1,
  geometry_only_multisprite_rectangle INTEGER DEFAULT 1,
  complete_isometric_assembly_game_verified INTEGER DEFAULT 0,
  same_runtime_furniture_across_facings_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v26_all_346_source_multitile_group_coverage(
  group_id TEXT PRIMARY KEY,source_multitile_facing_template_count INTEGER,
  direct_viewed_facing_grid_count INTEGER,
  all_indexed_source_facing_images_seen INTEGER DEFAULT 1,
  geometry_candidate_contains_2_or_more_tile_parts INTEGER DEFAULT 1,
  runtime_object_identity_certified INTEGER DEFAULT 0);
 CREATE TABLE v26_unreviewed_multitile_direction_candidates(
  group_id TEXT,Facing TEXT,source_key TEXT,original_png_path TEXT);
 CREATE TABLE v26_progress_scope(
  metric_key TEXT PRIMARY KEY,done INTEGER,total INTEGER,percent REAL,
  evidence_category TEXT,narrow_definition TEXT);
 """)
 visual_rows=[];categories=Counter();provisional=Counter();new_groups=set()
 for i in range(1,236):
  x=byindex[i];label=labelindex[i]
  g,f=x["group_id"],x["Facing"]
  sheet=(i-1)//10+1
  fn=f"V26_ORIGINAL_MULTITILE_SOURCE_CONTACT_{sheet:02d}.png"
  r=dict(sample_index=i,group_id=g,Facing=f,
   source_group_original_reference_name=x["original_name"],
   source_only_group=int(x["source_only_group"]),
   original_source_part_count=int(x["source_parts"]),
   original_grid_w=int(x["grid_w"]),original_grid_h=int(x["grid_h"]),
   contact_png_file=fn,contact_png_sha256=stage["original_contact_sheet_sha256"][fn],
   broad_visible_shape_observation=label["observed_visible_shape_group"],
   provisional_scope=label["provisional_scope"])
  insert(c,"v26_new_direct_original_png_grid_visual",r);visual_rows.append(r)
  categories[r["broad_visible_shape_observation"]]+=1
  provisional[r["provisional_scope"]]+=1
  new_groups.add(g)
 assert len(new_groups)==135
 rawposition=defaultdict(set);group_parts=defaultdict(set)
 for p in partmap:
  i=int(p["sample_index"]);g,f,key=p["group_id"],p["Facing"],p["source_key"]
  loc=(g,f,key);x=byindex[i]
  assert (g,f)==(x["group_id"],x["Facing"])
  assert loc in raw and loc in indexed and key in sourcetile
  ref=indexed[loc];r=raw[loc];src=sourcetile[key]
  assert p["raw_sprite_grid_pos"]==ref["raw_sprite_grid_pos"]==r["original_grid"]==src["SpriteGridPos"]
  assert int(p["relative_x"])==ref["relative_x"]==r["relative_x_when_available"]
  assert int(p["relative_y"])==ref["relative_y"]==r["relative_y_when_available"]
  assert int(p["atlas_col"])==ref["atlas_col"] and int(p["atlas_row"])==ref["atlas_row"]
  assert p["original_png_path"]==ref["original_png_path"]
  assert int(p["original_cell_w"])==ref["original_cell_w"]
  assert int(p["original_cell_h"])==ref["original_cell_h"]
  assert src["group_id"]==g
  assert (int(p["relative_x"]),int(p["relative_y"])) not in rawposition[(g,f)]
  rawposition[(g,f)].add((int(p["relative_x"]),int(p["relative_y"])))
  assert key not in group_parts[(g,f)];group_parts[(g,f)].add(key)
 assert len(group_parts)==235
 new_pixels=[];seen_pixel=set()
 for p in sha:
  i=int(p["sample_index"]);g,f,key=p["group_id"],p["Facing"],p["source_key"]
  loc=(g,f,key);q=indexed[loc]
  assert loc not in seen_pixel and key in group_parts[(g,f)]
  assert p["new_v26_direct_sprite_visual_observation"]=="1"
  assert p["originally_unreviewed_facing"]=="1"
  assert p["exact_in_game_object_identity_certified"]=="0"
  assert p["original_sprite_grid_pos"]==q["raw_sprite_grid_pos"]
  assert p["original_png_path"]==q["original_png_path"]
  assert int(p["atlas_col"])==q["atlas_col"] and int(p["atlas_row"])==q["atlas_row"]
  assert int(p["source_relative_x"])==q["relative_x"] and int(p["source_relative_y"])==q["relative_y"]
  assert len(p["original_atlas_png_sha256"])==len(p["original_cropped_cell_pixel_sha256"])==64
  rec=dict(sample_index=i,group_id=g,Facing=f,source_key=key,
   raw_source_sprite_grid_pos=p["original_sprite_grid_pos"],
   relative_x=int(p["source_relative_x"]),relative_y=int(p["source_relative_y"]),
   original_png_path=p["original_png_path"],
   original_png_sha256=p["original_atlas_png_sha256"],
   original_png_cell_pixel_sha256=p["original_cropped_cell_pixel_sha256"],
   original_atlas_col=int(p["atlas_col"]),original_atlas_row=int(p["atlas_row"]),
   original_sprite_cell_width=int(p["cell_w"]),original_sprite_cell_height=int(p["cell_h"]),
   raw_container_type=q["container_type_original"] or "",
   raw_container_capacity=q["container_capacity_original"] or "")
  insert(c,"v26_direct_original_sprite_pixels",rec);new_pixels.append(rec)
  seen_pixel.add(loc)
 assert len(new_pixels)==583 and seen_pixel=={(g,f,key) for (g,f),keys in group_parts.items() for key in keys}
 for (g,f),keys in group_parts.items():
  t=source_rect[(g,f)]
  assert len(keys)==t["raw_sprite_part_count"]
  assert len(rawposition[(g,f)])==t["grid_w"]*t["grid_h"]
  assert set(rawposition[(g,f)])=={(x,y) for x in range(t["grid_w"]) for y in range(t["grid_h"])}
 prior_origin={(x["group_id"],x["Facing"]):x["image_review_source_version"] for x in prev if x["source_grid_pixels_visually_checked"]}
 all_820=[];bygroup=defaultdict(list)
 for (g,f),rec in sorted(source_rect.items()):
  if (g,f) in prior_origin:version=prior_origin[(g,f)]
  else:
   assert (g,f) in new
   version="DIRECT_ORIGINAL_GRID_V26"
  record=dict(group_id=g,Facing=f,source_part_count=rec["raw_sprite_part_count"],
   source_grid_w=rec["grid_w"],source_grid_h=rec["grid_h"],
   source_only_group=rec["source_only_group"],
   direct_original_png_visual_review_version=version)
  insert(c,"v26_all_820_source_direction_grid_visual_evidence",record);all_820.append(record)
  bygroup[g].append(f)
 assert len(all_820)==820 and len(bygroup)==346
 all_346=[]
 for g,faces in sorted(bygroup.items()):
  record=dict(group_id=g,source_multitile_facing_template_count=len(faces),
   direct_viewed_facing_grid_count=len(faces))
  insert(c,"v26_all_346_source_multitile_group_coverage",record);all_346.append(record)
 assert len(all_346)==346
 multi_groups={g for g,fs in bygroup.items() if len(fs)>=2}
 assert len(multi_groups)==274
 metrics=[
  ("registered_Wiki_and_source_candidate_rows",2231,2231,"REGISTERED_ROWS","not final game furniture census; Wiki may be incomplete"),
  ("source_only_one_sprite_direct_original_png_visual_group_count",940,963,"SINGLE_SPRITE_REPRESENTATIVE","23 source PNG mapping blockers"),
  ("all_source_directional_grid_geometry_templates",3840,3840,"SOURCE_GEOMETRY","not runtime object"),
  ("source_multitile_rectangle_group_facing_image_visual_review",820,820,"DIRECT_ORIGINAL_PNG_GRID","not proven same actual furniture across directions"),
  ("unique_multitile_source_groups_with_all_indexed_facing_grids_seen",346,346,"SOURCE_GROUP_IMAGE_COVERAGE","not final unique in-game furniture"),
  ("source_groups_with_2_or_more_eligible_facings_compared",274,274,"TWO_DIRECTION_VISUAL","does not establish same in-game object"),
  ("new_v26_source_group_facing_image_reviews",235,235,"NEW_DIRECT_IMAGE_GRID","no overlap with previous 585"),
  ("new_v26_original_source_sprite_pixel_SHA_records",583,583,"ORIGINAL_IMAGE_PIXELS","each source tile original atlas checked"),
  ("old_original_source_property_warnings_resolved",0,474,"UNRESOLVED_WARNINGS","cannot claim 474 were fixed"),
  ("source_only_no_original_PNG_link_resolved",0,23,"UNRESOLVED_ASSET_LINK","none confirmed repaired"),
  ("in_game_furniture_object_identity_certified",0,0,"UNKNOWN_TOTAL","requires actual game object registry or runtime evidence"),
  ("true_unique_game_furniture_completion",0,0,"UNMEASURABLE","no justified denominator; do not say 100%")
 ]
 prog=[]
 for k,n,tot,ev,desc in metrics:
  row=dict(metric_key=k,done=n,total=tot,percent=round(100*n/tot,2) if tot else None,
   evidence_category=ev,narrow_definition=desc)
  insert(c,"v26_progress_scope",row);prog.append(row)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
 for t,n in {**originals,
  "v26_new_direct_original_png_grid_visual":235,
  "v26_direct_original_sprite_pixels":583,
  "v26_all_820_source_direction_grid_visual_evidence":820,
  "v26_all_346_source_multitile_group_coverage":346,
  "v26_unreviewed_multitile_direction_candidates":0,
  "v26_progress_scope":len(metrics)}.items():
  assert cnt(c,t)==n,(t,cnt(c,t),n)
 assert c.execute("SELECT COUNT(*) FROM v26_all_820_source_direction_grid_visual_evidence WHERE direct_png_contact_grid_visually_reviewed<>1").fetchone()[0]==0
 assert c.execute("SELECT COUNT(*) FROM v26_new_direct_original_png_grid_visual WHERE runtime_game_object_identity_certified<>0 OR same_furniture_across_other_facings_certified<>0").fetchone()[0]==0
 c.close()
 write("V26_235_DIRECT_ORIGINAL_GRID_VISUAL_OBSERVATIONS.csv",visual_rows)
 write("V26_583_PER_PART_SOURCE_PNG_PIXEL_SHA256_PROOFS.csv",new_pixels)
 write("V26_ALL_820_DIRECT_SOURCE_GRID_VISUAL_LEDGER.csv",all_820)
 write("V26_ALL_346_MULTITILE_SOURCE_GROUP_VISUAL_COVERAGE.csv",all_346)
 write("V26_12_SCOPE_LIMITED_PROGRESS.csv",prog)
 (OUT/"V26_0_UNREVIEWED_MULTITILE_SOURCE_GRID_QUEUE.csv").write_text(
  "group_id,Facing,original_png_source_key,why_unreviewed\n",encoding="utf-8-sig")
 manifest=dict(version="v26",input_v25_full_sqlite_zip_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
  current_registered_Wiki_and_source_candidates=2231,
  preserved_TileDef_original_property_rows=195265,preserved_source_raw_slots=73644,
  preserved_source_candidate_tile_keys=8219,
  prior_source_directional_geometry_templates=3840,
  eligible_multitile_original_complete_rectangular_group_facing_candidates=820,
  prior_direct_original_grid_image_views=585,
  newly_directly_visually_reviewed_group_facing_grids=235,
  v26_new_original_source_sprite_crop_SHA256_rows=583,
  newly_viewed_original_png_atlases=stage["original_atlases_sha_verified"],
  all_original_contact_sheets_directly_inspected=24,
  all_multitile_group_facing_source_grid_images_directly_reviewed=820,
  multi_tile_directional_original_png_visual_coverage_pct=100.0,
  remaining_multitile_original_grid_direction_visual_queue=0,
  source_multitile_unique_groups_with_at_least_one_direct_image=346,
  all_source_multitile_groups_with_all_indexed_direction_images_seen=346,
  source_multitile_group_image_coverage_pct=100.0,
  source_groups_with_two_or_more_facing_original_grid_candidates=274,
  source_groups_with_two_facing_comparison_directly_viewed=274,
  source_two_facing_comparison_coverage_pct=100.0,
  new_v26_unique_source_groups_not_previously_viewed=stage["new_unique_source_groups_without_prior_any_facing"],
  v26_broad_shape_classification_counts=dict(sorted(categories.items())),
  v26_provisional_scope_counts=dict(sorted(provisional.items())),
  original_Wiki_reference_may_be_outdated_or_incomplete=True,
  original_group_registry_rows_not_same_as_unique_game_furniture_count=True,
  original_474_warnings_unresolved=True,
  original_23_png_unlinked_source_groups_unresolved=True,
  prior_Work_107_groups_574_tiles_reported_without_ID_cross_proof_not_added=True,
  original_PNG_cell_grid_not_actual_in_game_isometric_furniture_assembly=True,
  original_shape_similarity_not_verified_runtime_same_object=True,
  certified_runtime_furniture_object_identity=0,
  certified_completed_in_game_multi_tile_furniture_assemblies=0,
  verified_exact_cross_facing_game_object_equivalence=0,
  lua_loot_TMX_Minecraft_not_started=True,
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
  "# Project Zomboid B42 원본 가구 후보 시각 검수 v26 — 820/820 소스 다중타일 방향별 이미지 검수 완료\n\n"
  "**이번 버전은 원본 PNG와 SpriteGridPos에 근거한 시각 검수의 완료**이지, 게임에서의 고유 가구 목록/완성 오브젝트/방향별 동일성 인증 완료가 아닙니다.\n"
  "v25 전체 SQLite 원본 및 source TileDef 속성 195,265행, 슬롯 73,644행, 후보 타일 8,219개, Wiki 연결/미연결 자료, 474원본 경고/23PNG 미연결 근거를 그대로 보존했습니다.\n"
  "v25에서 직접 보지 않은 다중 타일 직사각형 group×Facing 후보 235건을 중복 없이 전부 원본 PNG atlas 55개에서 실제 crop하고, 583개 원본 PNG 셀의 SHA256 및 원본 x/y를 개별 검증했습니다.\n"
  "24개의 PNG 접촉 시트를 실제 모두 열어 확인했습니다. 남은 35개 고유 그룹(이전 어떤 Facing도 못 본 원본 그룹)도 포함해 346/346 source group의 모든 현재 적격 820개 기하학적 다중 타일 그리드를 직접 확인했습니다.\n"
  "v21 80 + v22 120 + v23 120 + v24 160 + v25 신규 105 + v26 신규 235 = **820/820=100%**; 신규/이전 중복 없이 source group×Facing 집합 연산으로 재검사했습니다.\n"
  "현재 source-only 대표 1개 PNG 직접 시각 검수는 **940/963=97.61%**, 원본 atlas 셀 연결 미해결은 23그룹입니다.\n"
  "820개 후보 안에는 실제 가구처럼 보이는 것 외에도 간판, 바위, 텐트, 포스터 등 설치물/장식물이 섞여 있습니다. 위키 이름이나 유사 스프라이트만으로 가구를 확정·병합·제거하지 않습니다.\n"
  "최종 가구 정체를 확인하려면 별도 게임 오브젝트/타일 SpriteGrid·방향별 인스턴스 및 미확정 경고 474건의 근거가 필요하며, 현재 이 단계의 인증 수치는 0입니다.\n"
  "Lua loot, TMX placement, Minecraft 구현은 보류합니다.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if f.is_file() and f!=PACK and not f.name.startswith("STAGED_") and not f.name.endswith("_BASE64.txt") and not f.name.startswith("_required_"):
    z.write(f,f.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V26_FULL_820_OF_820_MULTITILE_SOURCE_GRID_VISUAL_VIEWS_583_NEW_ORIGINAL_PNG_CELLS_346_SOURCE_GROUPS_FULL_SQLITE_ZIP_CRC_PASS",J(manifest),flush=True)
if __name__=="__main__":main()
