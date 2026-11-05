#!/usr/bin/env python3
"""B42 v22 source-first: 60 directly observed paired facing comparisons, 120 new group×Facing.
Preserve all v21 raw, Wiki, image-review, warning and original coordinate source tables.
A visually related appearance is NOT an authenticated in-game furniture object.
"""
import csv,hashlib,json,shutil,sqlite3,zipfile
from pathlib import Path
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/furniture_full_b42/2026-11-04/multipart_grid_v21/B42_FURNITURE_MULTIPART_GRID_V21.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v22"
DB=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V22.sqlite"
PACK=OUT/"B42_FURNITURE_CROSS_FACING_REVIEW_V22.zip"
def qr(c,q,args=()):return [dict(v) for v in c.execute(q,args)]
def count(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def J(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def read(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(name,recs):
 assert recs,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(recs[0]));w.writeheader();w.writerows(recs)
def ins(c,t,row):
 names=list(row)
 c.execute("INSERT INTO "+t+"("+",".join(names)+") VALUES("+",".join("?" for _ in names)+")",list(row.values()))
def main():
 assert SRC.is_file() and OUT.is_dir() and not DB.exists()
 stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["new_distinct_pair_groups"]==60 and stage["new_direction_candidates"]==120
 assert stage["new_direction_overlaps_with_v21"]==0 and stage["new_group_overlaps_with_v21"]==0
 assert stage["original_multitile_rectangles"]==820
 assert stage["all_new_source_tile_crops_verified"]==258
 assert stage["actual_pair_contact_page_count"]==6
 pairs=read("V22_60_PAIR_SELECTION_SOURCE_ONLY.csv")
 faces=read("V22_120_FACING_GRID_CANDIDATES.csv")
 partqueue=read("V22_SELECTED_ORIGINAL_PART_POSITIONS.csv")
 pixel=read("V22_DIRECT_ORIGINAL_SOURCE_PIXEL_SHA256.csv")
 observed=read("V22_60_DIRECT_PAIRED_VISUAL_CLASSIFICATIONS.csv")
 assert len(pairs)==len(observed)==60 and len(faces)==120
 assert len(partqueue)==len(pixel)==258
 expected_png=stage["original_pair_contact_sha256"]
 assert len(expected_png)==6
 for name,digest in expected_png.items():
  assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest,(name,"source contact PNG changed")
 p_by_index={int(x["pair_no"]):x for x in pairs}
 obs_by_index={int(x["pair_no"]):x for x in observed}
 assert set(p_by_index)==set(obs_by_index)==set(range(1,61))
 for lab in observed:
  assert lab["observation_scope"]=="DIRECT_VIEW_OF_TWO_ORIGINAL_PNG_SOURCE_DIRECTION_GRIDS"
  assert lab["confirmed_exact_game_object_identity"]=="0"
  assert lab["visual_similarity_scope"]=="CANDIDATE_RELATED_DESIGN_NOT_GAME_OBJECT_PROOF"
 assert len({x["group_id"] for x in pairs})==60
 assert all(x["prior_v21_visual_group_overlap"]=="0" for x in pairs)

 with zipfile.ZipFile(SRC) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_MULTIPART_GRID_V21.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 original_tables={"source_attributes":195265,"source_slots":73644,
   "furniture_tile":8219,"registry_entry":2231,"wiki_furniture":1268,
   "v12_template_proof":3840,"v13_warning_case":474,
   "v14_source_only_ledger":963,"v20_master_furniture_registry":2231,
   "v21_all_source_rectangle_template":843,
   "v21_source_tile_positioned_png":2221,
   "v21_direct_multisprite_grid_visual_observation":80,
   "v21_reviewed_multisprite_pixel_sha":335}
 for t,n in original_tables.items():assert count(c,t)==n,(t,count(c,t),n)
 prev=qr(c,"SELECT group_id,Facing FROM v21_direct_multisprite_grid_visual_observation")
 prev_keys={(v["group_id"],v["Facing"]) for v in prev}
 assert len(prev_keys)==80
 oldgroup={x["group_id"] for x in prev}
 allc=qr(c,"SELECT group_id,Facing,raw_sprite_part_count,grid_w,grid_h,source_only_group FROM v21_all_source_rectangle_template")
 all_multi={(x["group_id"],x["Facing"]):x for x in allc if x["raw_sprite_part_count"]>=2}
 assert len(all_multi)==820
 part_ref={(x["group_id"],x["Facing"],x["source_key"]):x for x in qr(c,
  "SELECT group_id,Facing,source_key,raw_sprite_grid_pos,relative_x,relative_y,original_png_path,atlas_col,atlas_row,original_cell_w,original_cell_h FROM v21_source_tile_positioned_png")}
 oldraw={(x["group_id"],x["Facing"],x["source_key"]):x for x in qr(c,
  "SELECT group_id,Facing,source_key,original_grid,relative_x_when_available,relative_y_when_available FROM v12_tile_proof")}
 original_src={x["source_key"]:x for x in qr(c,"SELECT source_key,group_id,SpriteGridPos FROM furniture_tile")}
 c.executescript("""
 CREATE TABLE v22_direct_two_facing_visual_comparison(
  pair_no INTEGER PRIMARY KEY,group_id TEXT UNIQUE,source_name_original TEXT,
  source_only_group INTEGER,Facing_A TEXT,Facing_B TEXT,
  raw_grid_A TEXT,raw_grid_B TEXT,
  original_parts_A INTEGER,original_parts_B INTEGER,
  observed_broad_subject TEXT,observed_face_relation TEXT,
  visual_observation_scope TEXT,visual_similarity_scope TEXT,
  shape_rotation_candidate INTEGER,
  direct_original_png_pair_inspected INTEGER DEFAULT 1,
  provisional_similar_visual_family INTEGER DEFAULT 1,
  actual_same_game_object_certified INTEGER DEFAULT 0,
  runtime_object_ID_certified INTEGER DEFAULT 0);
 CREATE TABLE v22_new_facing_original_grid(
  pair_no INTEGER,group_id TEXT,Facing TEXT,face_slot TEXT,
  raw_grid_width INTEGER,raw_grid_height INTEGER,
  raw_sprite_parts INTEGER,source_keys_json TEXT,
  original_source_grid_verified INTEGER DEFAULT 1,
  same_object_between_facings_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v22_original_sprite_pixel_sha(
  pair_no INTEGER,face_slot TEXT,group_id TEXT,Facing TEXT,source_key TEXT,
  original_tile_grid TEXT,raw_relative_x INTEGER,raw_relative_y INTEGER,
  original_png_path TEXT,original_png_sha256 TEXT,
  exact_cropped_source_pixel_sha256 TEXT,
  original_atlas_column INTEGER,original_atlas_row INTEGER,
  original_sprite_cell_w INTEGER,original_sprite_cell_h INTEGER,
  screenshot_crop_source_verified INTEGER DEFAULT 1,
  actual_game_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v22_remaining_multitile_direction_queue(
  group_id TEXT,Facing TEXT,raw_parts INTEGER,grid_w INTEGER,grid_h INTEGER,
  source_only_group INTEGER,original_png_parts_mapped INTEGER,
  single_object_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v22_progress_scope(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,
  percent REAL,evidence_level TEXT,scope_limit TEXT);
 """)
 outpairs=[];outfacings=[];outpixels=[];newf=set()
 for i in range(1,61):
  pp=p_by_index[i];lab=obs_by_index[i];g=pp["group_id"]
  assert g not in oldgroup
  a,b=pp["Facing_A"],pp["Facing_B"]
  assert a!=b and (g,a) in all_multi and (g,b) in all_multi
  assert (g,a) not in prev_keys and (g,b) not in prev_keys
  aw,ah=map(int,pp["original_grid_A"].split("x"))
  bw,bh=map(int,pp["original_grid_B"].split("x"))
  ga,gb=all_multi[(g,a)],all_multi[(g,b)]
  assert (aw,ah)==(ga["grid_w"],ga["grid_h"])
  assert (bw,bh)==(gb["grid_w"],gb["grid_h"])
  assert int(pp["source_part_count_A"])==ga["raw_sprite_part_count"]
  assert int(pp["source_part_count_B"])==gb["raw_sprite_part_count"]
  rotated=int(aw==bh and ah==bw and (aw,ah)!=(bw,bh))
  record=dict(pair_no=i,group_id=g,source_name_original=pp["original_name"],
   source_only_group=int(pp["source_only_group"]),Facing_A=a,Facing_B=b,
   raw_grid_A=pp["original_grid_A"],raw_grid_B=pp["original_grid_B"],
   original_parts_A=int(pp["source_part_count_A"]),
   original_parts_B=int(pp["source_part_count_B"]),
   observed_broad_subject=lab["observed_broad_visual_subject"],
   observed_face_relation=lab["observed_two_facing_relation"],
   visual_observation_scope=lab["observation_scope"],
   visual_similarity_scope=lab["visual_similarity_scope"],shape_rotation_candidate=rotated)
  ins(c,"v22_direct_two_facing_visual_comparison",record);outpairs.append(record)
 assert len(outpairs)==60

 sourcekeys=defaultdict(set)
 for r in partqueue:
  group=r["group_id"];face=r["Facing"];key=r["source_key"]
  label=(group,face,key)
  assert label in part_ref and label in oldraw
  sourcekeys[(group,face)].add(key)
  p=part_ref[label];o=oldraw[label];t=original_src[key]
  assert r["raw_sprite_grid_pos"]==p["raw_sprite_grid_pos"]==o["original_grid"]==t["SpriteGridPos"]
  assert int(r["relative_x"])==p["relative_x"]==o["relative_x_when_available"]
  assert int(r["relative_y"])==p["relative_y"]==o["relative_y_when_available"]
  assert r["original_png_path"]==p["original_png_path"]
  assert int(r["atlas_col"])==p["atlas_col"] and int(r["atlas_row"])==p["atlas_row"]
  assert int(r["original_cell_w"])==p["original_cell_w"] and int(r["original_cell_h"])==p["original_cell_h"]
  assert t["group_id"]==group
  assert (group,face) in all_multi
 for r in faces:
  g=r["group_id"];f=r["Facing"];i=int(r["pair_no"])
  assert i in p_by_index and p_by_index[i]["group_id"]==g
  assert (g,f) not in prev_keys and (g,f) not in newf
  src=all_multi[(g,f)]
  assert len(sourcekeys[(g,f)])==src["raw_sprite_part_count"]==int(r["original_parts"])
  assert (int(r["width"]),int(r["height"]))==(src["grid_w"],src["grid_h"])
  assert set(json.loads(r["original_keys_json"]))==sourcekeys[(g,f)]
  record=dict(pair_no=i,group_id=g,Facing=f,face_slot=r["face_slot"],
   raw_grid_width=int(r["width"]),raw_grid_height=int(r["height"]),
   raw_sprite_parts=int(r["original_parts"]),source_keys_json=r["original_keys_json"])
  ins(c,"v22_new_facing_original_grid",record);outfacings.append(record);newf.add((g,f))
 assert len(newf)==120 and not newf.intersection(prev_keys)
 assert len(sourcekeys)==120
 pixelkeys=set()
 for r in pixel:
  g=r["group_id"];f=r["Facing"];key=r["source_key"];x=(g,f,key)
  assert (g,f) in newf and key in sourcekeys[(g,f)]
  assert x not in pixelkeys
  assert r["actual_original_pixels_cropped"]=="1"
  assert len(r["original_png_sha256"])==64 and len(r["png_cell_pixel_sha256"])==64
  record=dict(pair_no=int(r["pair_no"]),face_slot=r["face_slot"],group_id=g,Facing=f,
   source_key=key,original_tile_grid=r["raw_grid"],
   raw_relative_x=int(r["relative_x"]),raw_relative_y=int(r["relative_y"]),
   original_png_path=r["png_path"],original_png_sha256=r["original_png_sha256"],
   exact_cropped_source_pixel_sha256=r["png_cell_pixel_sha256"],
   original_atlas_column=int(r["atlas_col"]),original_atlas_row=int(r["atlas_row"]),
   original_sprite_cell_w=int(r["cell_w"]),original_sprite_cell_h=int(r["cell_h"]))
  assert record["original_tile_grid"]==part_ref[x]["raw_sprite_grid_pos"]
  assert record["original_png_path"]==part_ref[x]["original_png_path"]
  ins(c,"v22_original_sprite_pixel_sha",record);outpixels.append(record);pixelkeys.add(x)
 assert len(pixelkeys)==258==sum(len(x) for x in sourcekeys.values())
 remaining=[]
 for (g,f),r in sorted(all_multi.items()):
  if (g,f) in prev_keys or (g,f) in newf:continue
  pp=dict(group_id=g,Facing=f,raw_parts=r["raw_sprite_part_count"],
   grid_w=r["grid_w"],grid_h=r["grid_h"],
   source_only_group=r["source_only_group"],
   original_png_parts_mapped=r["raw_sprite_part_count"])
  ins(c,"v22_remaining_multitile_direction_queue",pp);remaining.append(pp)
 assert len(remaining)==620
 all_multiface=defaultdict(int)
 for g,f in all_multi:all_multiface[g]+=1
 eligible_groups=sum(n>=2 for n in all_multiface.values())
 visual_subject=Counter(r["observed_broad_subject"] for r in outpairs)
 assert sum(visual_subject.values())==60
 scopes=[
  ("known_source_and_wiki_candidate_rows",2231,2231,"REGISTERED_NOT_UNIQUE_FURNITURE","Wiki may be incomplete"),
  ("single_sprite_source_only_direct_visual_review",940,963,"ONE_ORIGINAL_SPRITE","23 source groups have missing PNG mapping"),
  ("source_directional_geometry_candidates",3840,3840,"SOURCE_GEOMETRY","Not full object identification"),
  ("real_multitile_rectangle_source_candidates",820,820,"SOURCE_ONLY_RECTANGLES","820 group×Facing not unique game objects"),
  ("previous_v21_multipart_single_facing_visual",80,820,"DIRECT_SOURCE_GRID","80 prior distinct group×Facing image grids"),
  ("new_v22_cross_facing_grid_visual",120,820,"DIRECT_PAIRED_SOURCE_GRIDS","Two facings from each of 60 unique groups"),
  ("cumulative_distinct_multitile_direction_grid_visual",200,820,"DIRECT_SOURCE_GRID","80 v21 +120 v22; no overlap"),
  ("new_two_facing_group_comparisons",60,eligible_groups,"VISUAL_COMPARISON_ONLY","Visual relatives, no game object identity"),
  ("new_original_sprite_pixels_sha_checked",258,258,"ORIGINAL_PIXEL_HASH","Per source tile in newly reviewed 120 grid candidates"),
  ("original_warning_cases_resolved",0,474,"UNRESOLVED","No warning certified resolved"),
  ("source_only_png_mapping_blockers_resolved",0,23,"UNRESOLVED","23 original TileDef PNG atlas mappings missing"),
  ("actual_same_game_object_verified",0,0,"UNKNOWN_TOTAL","Runtime identity currently uncertified")
 ]
 progress=[]
 for key,n,den,kind,scope in scopes:
  rr=dict(metric_key=key,numerator=n,denominator=den,
   percent=round(n/den*100,2) if den else None,evidence_level=kind,scope_limit=scope)
  ins(c,"v22_progress_scope",rr);progress.append(rr)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for t,n in {**original_tables,"v22_direct_two_facing_visual_comparison":60,
  "v22_new_facing_original_grid":120,"v22_original_sprite_pixel_sha":258,
  "v22_remaining_multitile_direction_queue":620,"v22_progress_scope":12}.items():
  assert count(c,t)==n,(t,count(c,t),n)
 assert c.execute("""SELECT COUNT(*) FROM v22_direct_two_facing_visual_comparison
  WHERE actual_same_game_object_certified!=0 OR runtime_object_ID_certified!=0""").fetchone()[0]==0
 c.close()
 write("V22_60_NEW_DIRECT_CROSS_FACING_VISUAL_REVIEWS.csv",outpairs)
 write("V22_120_NEW_SOURCE_FACING_CANDIDATE_PROOFS.csv",outfacings)
 write("V22_258_ORIGINAL_TILE_PNG_PIXEL_SHA256.csv",outpixels)
 write("V22_620_STILL_UNREVIEWED_MULTITILE_FACING_QUEUE.csv",remaining)
 write("V22_12_SCOPED_PROGRESS.csv",progress)
 manifest=dict(version="v22",source_v21_zip_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),
  preserved_raw_property_rows=195265,preserved_raw_slots=73644,
  preserved_candidate_registry_rows=2231,preserved_source_candidate_tile_keys=8219,
  original_direction_geometry_candidates=3840,
  geometric_complete_rectangles_including_single=843,
  single_tile_rectangles=23,real_multitile_geometry_candidates=820,
  previous_single_direction_grid_direct_reviews=80,
  new_distinct_source_groups_two_facing_direct_image_reviews=60,
  new_unique_group_facing_direct_image_reviews=120,
  new_real_source_sprite_crops_SHA256=258,
  new_visual_pair_original_atlases=stage["distinct_original_png_sha_sources"],
  new_pair_source_only_groups=stage["selected_source_only_groups"],
  new_pair_wiki_linked_groups=stage["selected_wiki_linked_groups"],
  new_pair_visual_class_counts=dict(sorted(visual_subject.items())),
  new_pairs_with_rotated_rectangle_dimensions=sum(r["shape_rotation_candidate"] for r in outpairs),
  cumulative_direct_multitile_group_direction_views=200,
  cumulative_multitile_direction_visual_coverage_pct=round(200/820*100,2),
  still_unreviewed_multitile_direction_candidates=620,
  unique_multitile_group_count=len(all_multiface),
  groups_with_at_least_two_multitile_facings=eligible_groups,
  new_paired_group_comparison_pct=round(60/eligible_groups*100,2),
  all_60_pair_contacts_original_image_hashes_checked=True,
  source_only_one_sprite_visual_reviews_preserved=940,
  original_474_warnings_still_unresolved=True,
  original_23_png_mapping_blockers_unresolved=True,
  prior_Work_107_groups_574_tiles_unverified_per_group_id_not_added=True,
  wiki_can_be_incomplete_outdated=True,
  similar_visual_family_not_actual_same_game_object=True,
  certified_same_game_object_across_facing=0,
  certified_exact_runtime_game_object_ID=0,
  certified_whole_game_furniture_assemblies=0,
  lua_tmx_minecraft_not_started=True,
  integrity_check="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 원본 가구 방향 비교 v22 — 60그룹, 두 방향씩 실제 원본 타일 그리드 직접 검수\n\n"
 "v21 전체 SQLite를 복제해 원본 TileDef·위키 참조·대표 이미지 검수 940그룹·부품 그리드 80건·기존 경고 474건·PNG 미연결 23건을 보존.\n"
 "v21 시각 검수 그룹과 전혀 겹치지 않는 원본 그룹 60개에서 2개 Facing씩 골라 원본 PNG **258개 셀**의 실제 픽셀/PNG SHA를 기록했습니다.\n"
 "6개 접촉 시트에서 60그룹/120방향을 각각 두 방향 좌표 그리드로 **직접 나란히 관찰**, 동일 넓은 디자인 계열과 방향별 표현 차이를 기록했습니다.\n"
 "E와 S처럼 방향별 원본 SpriteGridPos 폭/높이가 교환되는 사례를 원본 값으로 따로 계산했으며, 위키 이름이나 좌표만으로 같은 가구라는 결론을 내리지 않았습니다.\n"
 "기존 v21 그리드 이미지 검수 80건 + 신규 방향별 이미지 검수 120건 = **200 / 820 = 24.39%**. 이후 620개 방향별 기하 후보가 남습니다.\n"
 "새 60개는 위키 연결이 있는 원본 그룹이지만, **위키는 최신성·완전성이 검증되지 않은 참고 자료**입니다.\n"
 "원본 타일 PNG 배치 그림은 게임 자체의 정밀 아이소메트릭 장면 합성이나 런타임 오브젝트 동일성 검증이 아닙니다. 공식 인증 0.\n"
 "기존 474 경고 미해결, 23개 PNG 매핑 미해결, Lua/TMX/Minecraft 구현 보류.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if (f.is_file() and f!=PACK and not f.name.startswith("STAGED_") and
       not f.name.startswith("_required_") and not f.name.endswith("_BASE64.txt")):
    z.write(f,f.name)
 with zipfile.ZipFile(PACK) as z:assert z.testzip() is None and DB.name in z.namelist()
 print("V22_60_TWO_DIRECTION_VISUAL_PAIRS_120_NEW_GRIDS_258_REAL_ORIGINAL_PIXEL_SHA_AND_620_QUEUE_VERIFIED",
       J(manifest),flush=True)
if __name__=="__main__":main()
