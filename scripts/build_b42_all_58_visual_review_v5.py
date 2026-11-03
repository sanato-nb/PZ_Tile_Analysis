#!/usr/bin/env python3
"""Commit the 58/58 directly inspected source-PNG review into B42 furniture SQLite.

11 previously inspected groups from v4 + 47 new direct visual reviews.
Preserve full PZ TileDef source, v1-v4 tables, Wiki 1268 source rows and
per-tile attributes. Do not invent Game Moveable object identity or
Minecraft implementation decisions.
"""
import csv,sqlite3,json,zipfile,shutil,hashlib
from pathlib import Path
from collections import Counter,defaultdict

ROOT=Path(__file__).resolve().parents[1]
P4=ROOT/"analysis/furniture_full_b42/2026-11-03/disjoint_visual_v4"
P5=ROOT/"analysis/furniture_full_b42/2026-11-03/full_visual_review_v5"
BASE=P4/"B42_DISJOINT_VISUAL_V4_BUNDLE.zip"
DB=P5/"B42_ALL_58_VISUALLY_REVIEWED_FURNITURE.sqlite"
ARCHIVE=P5/"B42_ALL_58_FURNITURE_VISUAL_REVIEW_V5.zip"
BASE_GROUPS=P4/"GROUPS_58_V4.csv"
BASE_FAMILIES=P4/"WIKI_NAME_FAMILIES_66.csv"
BASE_WIKI=P4/"WIKI_VARIANT_ROWS_357.csv"
BASE_IMAGE=P4/"ORIGINAL_PNG_CROP_EVIDENCE.csv"
OLD11=P4/"V4_MANUAL_VISUAL_OBSERVATIONS_11.csv"
NEW47=P5/"V5_NEW_47_DIRECT_VISUAL_OBSERVATIONS.csv"

OLD_CATEGORIES={
 "FLOOR_PATTERN_VARIATION":"FLOOR_DECOR",
 "FILL_STATE_AND_COLOR_VARIATION":"CRAFTING_DEVICE",
 "MULTIPLE_SHAPES_AND_CONTENT_STATES":"PLUMBING_OR_FARM_FIXTURE",
 "ARCHITECTURAL_DIRECTION_LIKELY":"ARCHITECTURAL_WINDOW",
 "COLOR_AND_VIEW_VARIATIONS":"STORAGE_CONTAINER",
 "MULTIPART_TWO_FACINGS_SOURCE_CONFIRMED":"PLUMBING_OR_FARM_FIXTURE",
 "CARD_BOX_TEXTURE_AND_VIEW_VARIATIONS":"STORAGE_CONTAINER",
 "TWO_DIFFERENT_VISUAL_TABLE_FORMS":"TABLE_FURNITURE",
 "POSSIBLE_SAME_BODY_DIFFERENT_FILL":"CRAFTING_FIXTURE",
 "SIMILAR_SHAPE_WITH_TEXTURE_DIFFERENCE":"STORAGE_CONTAINER",
}
# "MULTIPART_TWO_FACINGS_SOURCE_CONFIRMED" category depends on group name.
def csvread(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def csvout(p,items):
 assert items,str(p)
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(items[0]),extrasaction="ignore");w.writeheader();w.writerows(items)
def cnt(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def unique(x):return sorted({str(v) for v in x if v not in ("",None)})
def connect(x):return "|".join(unique(x))
def verdict(group,source):
 if source=="V4_PREVIOUS_11_REVIEW":
  cat=OLD_CATEGORIES.get(group["original_PNG_visual_relationship"],"VISUAL_OBJECT_REVIEW")
  if group["observed_wiki_family_names"]=="Wooden Bench":cat="SEATING_FURNITURE"
  return cat
 return group["functional_visual_scope"]
def main():
 assert NEW47.is_file() and BASE.is_file()
 assert not DB.exists(),"Refuse replacing previously built database"
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  target="PZ_B42_FURNITURE_DISJOINT_VISUAL_V4.sqlite"
  assert target in z.namelist()
  with z.open(target) as stream,DB.open("wb") as out:shutil.copyfileobj(stream,out)
 con=sqlite3.connect(DB);con.row_factory=sqlite3.Row
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert cnt(con,"v4_disjoint_group")==58
 assert cnt(con,"v4_name_family")==66
 assert cnt(con,"v4_name_family_member")==357
 assert cnt(con,"source_attributes")==195265
 assert cnt(con,"wiki_furniture")==1268
 assert cnt(con,"furniture_tile")==8219
 assert cnt(con,"registry_entry")==2231

 indexed=csvread(BASE_GROUPS)
 old=csvread(OLD11)
 new=csvread(NEW47)
 assert len(indexed)==58 and len(old)==11 and len(new)==47
 idx={x["source_group_id"]:x for x in indexed}
 assert len(idx)==58
 merged=[]
 for x in old:
  gid=x["source_group_id"]
  v=idx[gid]
  merged.append(dict(
   group_index=int(v["index"]),source_group_id=gid,original_tileset=v["tileset"],
   source_CustomName=v["original_CustomName"],source_GroupName=v["original_GroupName"],
   wiki_row_count=v["wiki_entries"],observed_wiki_family_names=v["family_names"],
   functional_visual_scope="",original_PNG_visual_relationship=x["visual_relationship_class"],
   observation_KO=x["observation_from_original_source_PNG"],
   map_generation_handling_KO=x["classification_guidance"],
   source_image=x["contact_sheet"],review_type="V4_PREVIOUS_11_REVIEW",
   physical_game_object_identity_certified="NO"))
 for x in new:
  y=dict(x)
  y["group_index"]=int(y["group_index"])
  y["review_type"]="V5_NEW_47_DIRECT_VISUAL_INSPECTION"
  merged.append(y)
 assert len(merged)==58 and len({x["source_group_id"] for x in merged})==58
 assert set(idx)=={x["source_group_id"] for x in merged}
 merged.sort(key=lambda x:x["group_index"])
 for x in merged:
  source="V4_PREVIOUS_11_REVIEW" if x["review_type"]=="V4_PREVIOUS_11_REVIEW" else "V5_NEW_47_DIRECT_VISUAL_INSPECTION"
  x["functional_visual_scope"]=verdict(x,source)
  x["identity_level"]="SOURCE_PNG_APPEARANCE_REVIEWED_NOT_GAME_OBJECT_CERTIFIED"
  assert x["physical_game_object_identity_certified"]=="NO"
  assert x["source_image"]==idx[x["source_group_id"]]["image_path"]
  assert str(x["wiki_row_count"])==idx[x["source_group_id"]]["wiki_entries"]
 total_wiki_entries=sum(int(x["wiki_row_count"]) for x in merged)
 assert total_wiki_entries==357

 con.executescript("""
 CREATE TABLE v5_manual_visual_group_review(
   source_group_id TEXT PRIMARY KEY,contact_sheet_index INTEGER,
   source_tileset TEXT,original_CustomName TEXT,original_GroupName TEXT,
   wiki_row_count INTEGER,source_family_names TEXT,
   functional_visual_scope TEXT NOT NULL,visual_relationship TEXT NOT NULL,
   observation TEXT NOT NULL,map_generation_handling TEXT NOT NULL,
   source_contact_sheet TEXT NOT NULL,review_origin TEXT NOT NULL,
   observed_original_png INTEGER NOT NULL DEFAULT 1,
   same_game_moveable_object_verified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v5_wiki_row_review(
   wiki_id TEXT PRIMARY KEY,source_group_id TEXT NOT NULL,family_id TEXT NOT NULL,
   source_wiki_name TEXT NOT NULL,source_original_sprite_ids_json TEXT NOT NULL,
   source_facing_values TEXT,source_grid_positions_json TEXT,
   source_container_types TEXT,source_container_capacity_values TEXT,
   visual_relationship TEXT NOT NULL,
   original_png_visual_review_completed INTEGER NOT NULL DEFAULT 1,
   verified_game_furniture_identity INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v5_family_review(
   family_id TEXT PRIMARY KEY,source_group_id TEXT NOT NULL,
   wiki_base_name TEXT,wiki_member_count INTEGER NOT NULL,
   source_facings TEXT,source_grid_evidence TEXT,
   functional_visual_scope TEXT NOT NULL,
   game_object_design_identity_verified INTEGER NOT NULL DEFAULT 0);
 CREATE INDEX v5_review_scope_index ON v5_manual_visual_group_review(functional_visual_scope);
 CREATE INDEX v5_review_wiki_group ON v5_wiki_row_review(source_group_id);
 """)
 classified=Counter()
 for g in merged:
  con.execute("INSERT INTO v5_manual_visual_group_review VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,1,0)",
   (g["source_group_id"],g["group_index"],g["original_tileset"],
    g["source_CustomName"],g["source_GroupName"],int(g["wiki_row_count"]),
    g["observed_wiki_family_names"],g["functional_visual_scope"],
    g["original_PNG_visual_relationship"],g["observation_KO"],
    g["map_generation_handling_KO"],g["source_image"],g["review_type"]))
  classified[g["functional_visual_scope"]]+=1
 gidreview={g["source_group_id"]:g for g in merged}
 family_raw=csvread(BASE_FAMILIES)
 row_raw=csvread(BASE_WIKI)
 evidence=csvread(BASE_IMAGE)
 assert len(family_raw)==66 and len(row_raw)==357 and len(evidence)==368
 evid=defaultdict(list)
 for e in evidence:evid[e["wiki_id"]].append(e)
 family_to_rows=defaultdict(list)
 for w in row_raw:family_to_rows[w["family_id"]].append(w)
 family_export=[]
 for f in family_raw:
  fid=f["family_id"];gid=f["group_id"]
  rs=family_to_rows[fid]
  source_evidence=[e for r in rs for e in evid[r["wiki_id"]]]
  faces=unique(e["Facing"] for e in source_evidence)
  groups=gidreview[gid]
  multi_parts=sum(len(evid[r["wiki_id"]])>1 for r in rs)
  gridpositions=[e["SpriteGridPos"] for e in source_evidence if e["SpriteGridPos"]]
  grid="SOURCE_GRID_POS_PRESENT" if gridpositions else "NO_SOURCE_GRID_POS"
  con.execute("INSERT INTO v5_family_review VALUES(?,?,?,?,?,?,?,0)",
   (fid,gid,f["family_name"],len(rs),connect(faces),grid,
    groups["functional_visual_scope"]))
  family_export.append(dict(family_id=fid,source_group_id=gid,normalized_name=f["family_name"],
   member_wiki_rows=len(rs),facing_values=connect(faces),
   multipart_wiki_items=multi_parts,source_grid_evidence=grid,
   visual_scope=groups["functional_visual_scope"],
   relationship=groups["original_PNG_visual_relationship"],
   game_object_identity_verified="NO"))
 wiki_export=[]
 for w in row_raw:
  gid=w["group_id"];gg=gidreview[gid]
  ee=evid[w["wiki_id"]]
  keys=[e["source_key"] for e in ee]
  faces=unique(e["Facing"] for e in ee)
  containers=unique(e["container"] for e in ee)
  cap=unique(e["ContainerCapacity"] for e in ee)
  grids={e["source_key"]:e["SpriteGridPos"] for e in ee}
  assert all(e["rendered_original_png"]=="YES" for e in ee)
  con.execute("INSERT INTO v5_wiki_row_review VALUES(?,?,?,?,?,?,?,?,?,?,1,0)",
   (w["wiki_id"],gid,w["family_id"],w["original_name"],
    json.dumps(keys,ensure_ascii=False),connect(faces),
    json.dumps(grids,ensure_ascii=False),
    connect(containers),connect(cap),gg["original_PNG_visual_relationship"]))
  wiki_export.append(dict(wiki_id=w["wiki_id"],family_id=w["family_id"],group_id=gid,
   original_name=w["original_name"],source_tile_ids=connect(keys),
   source_tile_count=len(keys),source_Facing=connect(faces),
   source_SpriteGridPos_by_tile=json.dumps(grids,ensure_ascii=False),
   source_container_types=connect(containers),source_ContainerCapacity=connect(cap),
   source_wiki_capacity=w["wiki_capacity_raw"],
   visual_scope=gg["functional_visual_scope"],
   image_relationship=gg["original_PNG_visual_relationship"],
   original_source_png_verified="YES",game_object_identity_verified="NO"))
 con.commit()
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for table,n in [("v5_manual_visual_group_review",58),("v5_wiki_row_review",357),
                 ("v5_family_review",66),("source_attributes",195265),
                 ("source_slots",73644),("wiki_furniture",1268),
                 ("v4_original_crop_evidence",368)]:
  assert cnt(con,table)==n,(table,cnt(con,table),n)
 assert cnt(con,"future_item_distribution")==0
 assert cnt(con,"future_map_placement")==0
 assert cnt(con,"future_minecraft_implementation")==0
 assert con.execute("SELECT COUNT(*) FROM v5_manual_visual_group_review WHERE same_game_moveable_object_verified!=0").fetchone()[0]==0
 assert con.execute("SELECT COUNT(*) FROM v5_wiki_row_review WHERE verified_game_furniture_identity!=0").fetchone()[0]==0
 csvout(P5/"V5_ALL_58_ACTUAL_SOURCE_PNG_GROUP_VISUAL_REVIEWS.csv",merged)
 csvout(P5/"V5_ALL_357_WIKI_ROWS_WITH_FACING_STORAGE.csv",wiki_export)
 csvout(P5/"V5_ALL_66_FAMILY_VISUAL_AND_DIRECTION_REVIEWS.csv",family_export)
 manifest=dict(
  source_v4_visual_groups=58,previously_direct_inspected_groups=11,
  newly_direct_inspected_groups=47,total_groups_with_direct_PNG_review=len(merged),
  full_wiki_rows_with_visual_group_review=357,
  original_wiki_list_rows_preserved=1268,original_TileDef_source_attributes_preserved=195265,
  original_source_slot_rows_preserved=73644,
  visual_name_family_count=66,original_source_png_crop_evidence_rows_preserved=368,
  source_functional_visual_classification_counts=dict(sorted(classified.items())),
  game_moveable_object_identities_newly_certified=0,
  actual_game_loot_rules_loaded=0,
  minecraft_implementation_selected=False,
  physical_model_geometry_certified_count=0,
  original_source_files_changed=False,
  database_integrity="ok"
 )
 (P5/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 report=[
  "# B42 원본 58개 그룹 실제 이미지 검수 완료 (v5)",
  "### 작업 범위",
  "기존 11그룹에 더하여 47그룹의 원본 PNG 접촉시트를 추가로 직접 확인하고 총 58그룹/357개 Wiki 행을 근거별로 정리했어.",
  "원본 TileDef 61,418 고유 키, source_slots 73,644행 및 속성 195,265행, 전체 PZwiki 1,268행을 SQLite에 보존했어.",
  "원본 PNG에서 추출한 셀 368개와 58장 접촉시트는 v4 경로에 그대로 남아 있으며, v5의 모든 검수 CSV는 v4 이미지 상대경로와 원본 ID를 연결해.",
  "### 가장 중요한 구분",
  "- **가구의 방향**: Wooden Bench (2부품×N/W), Large Metal Trough (3부품×N/W), Office Desk (2부품·Facing E/S)는 실제 원본 Facing/SpriteGridPos 참고.",
  "- **같은 Wiki 이름의 다른 3D 형태**: Rain Collector Barrel의 원형 통과 사각형 통, Road Cone의 낮은 주황 콘과 높은 줄무늬 표지봉, Ornamental Bush의 원뿔형과 구형을 분리.",
  "- **상태 변형**: Metal Drum 불꽃·내용물, Raised Plantbed의 식물 성장/빈 흙, Ficus/Dragon Tree/Chinese Evergreen/Snake Plant/Cast Iron Plant의 잎 시듦 상태.",
  "- **부품/패턴**: 러그 가장자리와 중앙 조각, Flowerbed 테두리 및 꽃 색상, Air conditioner의 별도 팬·환기 그릴.",
  "- **가구와 구분해야 하는 맵 요소**: Trash 51개는 쓰레기 잔해/오버레이, Windows는 건축 설비, 타일/카펫은 바닥 재질.",
  "- **위키 명명 주의**: Red Carpet은 원본 그림에 매우 다양한 색상·무늬가 포함되므로 위키 기본 이름만으로 모두 같은 텍스처라고 처리하면 안 돼.",
  "### 시각·기능 범주별 그룹 수"]
 for category,n in sorted(classified.items(),key=lambda x:(-x[1],x[0])):
  report.append("- "+category+": "+str(n))
 report.extend([
  "### 생성한 파일",
  "- B42_ALL_58_VISUALLY_REVIEWED_FURNITURE.sqlite — v4 전체 DB + 새 v5 직접 검수 그룹(58), Wiki 행(357), 명칭 계열(66) 관계형 테이블.",
  "- V5_ALL_58_ACTUAL_SOURCE_PNG_GROUP_VISUAL_REVIEWS.csv — 58그룹 원본 이미지 관찰 기록·취급 방식.",
  "- V5_ALL_357_WIKI_ROWS_WITH_FACING_STORAGE.csv — 357개 위키 행의 원본 타일 ID, Facing, SpriteGridPos, container, ContainerCapacity.",
  "- V5_ALL_66_FAMILY_VISUAL_AND_DIRECTION_REVIEWS.csv — 66계열의 방향 근거·부품 여부·시각 관계.",
  "- V5_NEW_47_DIRECT_VISUAL_OBSERVATIONS.csv — 이번에 새로 직접 검수한 47그룹의 관찰 기록 원본.",
  "- MANIFEST.json — 검증된 집계 및 보존·미구현 상태.",
  "### 검수 범위와 한계",
  "총 58개 그룹 **원본 PNG의 외형을 직접 봤음**. 이것은 게임의 Moveable 오브젝트 1:1 동일성, 실제 모델 3D 형상, 모든 아이템 분포를 검증한 것과 달라.",
  "특히 외형상 동일해 보여도 서로 다른 게임 내부 오브젝트일 수 있어. 따라서 위키 항목 병합과 마크 Block/Entity 선택은 계속 보류해.",
  "기존 v4 그림 58장 및 원본 PNG를 변경하지 않았어."
 ])
 (P5/"README_KO.md").write_text("\n\n".join(report)+"\n",encoding="utf8")
 con.close()
 with zipfile.ZipFile(ARCHIVE,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(P5.iterdir()):
   if f.is_file() and f!=ARCHIVE:z.write(f,f.name)
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None
  assert DB.name in z.namelist()
 print("PZ_FURNITURE_V5_REVIEW_COMPLETED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":
 main()
