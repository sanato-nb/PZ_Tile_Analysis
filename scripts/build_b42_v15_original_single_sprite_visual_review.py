#!/usr/bin/env python3
"""v15: persisted coarse visual observations from four directly inspected ORIGINAL sprite contact sheets.
Visual part class != same game object != source-group assembly != furniture ontology certification.
"""
import csv,hashlib,json,shutil,sqlite3,zipfile
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis/furniture_full_b42/2026-11-04/source_first_v14/B42_FURNITURE_SOURCE_FIRST_V14.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/visual_review_v15"
DB=OUT/"B42_FURNITURE_COARSE_VISUAL_REVIEW_V15.sqlite"
CATS={"SHELTER_PART":[1,2,3,4,9,11,20,119,135],"FURNITURE_TABLE_OR_COUNTER_PART":[5,7,34,35,38,39,41,51,55,90,91,92,94,95,97,98,99,105,106,142],"FURNITURE_STORAGE_OR_SHELVING_PART":[6,19,93,96,100,103,109],"MATERIAL_OR_LOOSE_ITEM":[8,17,138,139,140,141],"STRUCTURE_OR_ARCHITECTURAL_PART":[10,137,149,150,151,152,153,157,158,159],"VISUALLY_INDETERMINATE":[12,58],"RUG_OR_GROUND_DECOR":[13,23,24,26,65,68,72],"EQUIPMENT_OR_APPLIANCE":[14,15,18,46,101,102,104,116,117,120,121,124,128,129,132,136],"LIGHTING_OR_STRING_LIGHT":[16,36,40,43,48,49,57,111,113,115,118,122,125,127,130,131,134],"SIGN_POSTER_WALL_GRAPHIC":[21,22,25,27,28,29,30,31,32,33,37,44,45,47,50,53,54,66,67,69,73,74,75,76,77,80,81,82,83,84,85,86,87,88,89,107,126,133,143,144,145,146,147,148,154,155,156],"FURNITURE_BED_OR_CRIB_PART":[42,59,60],"DECORATIVE_SCULPTURE_OR_BUNTING":[52,61,62,63,64],"FURNITURE_SEATING_PART":[56,123],"NATURAL_BOULDER_OR_VEGETATION":[70,71,78,79,160],"CURTAIN_OR_CLOTH_PANEL":[108,110,112,114]}
def rows(c,q):return [dict(x) for x in c.execute(q)]
def emit(name,items):
 assert items
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
def insert(c,table,item):
 c.execute("INSERT INTO "+table+"("+",".join(item)+") VALUES("+",".join("?" for _ in item)+")",list(item.values()))
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 assert SOURCE.exists()
 assert not DB.exists(),"Do not overwrite v15 SQLite"
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_SOURCE_FIRST_V14.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
  sha={}
  for i in range(1,5):
   key="V14_SOURCE_ONLY_ORIGINAL_CONTACT_%02d.png"%i
   data=z.read(key)
   sha[i]=hashlib.sha256(data).hexdigest()
   (OUT/key).write_bytes(data)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,n in [("source_attributes",195265),("furniture_tile",8219),
             ("v13_warning_case",474),("v14_source_only_ledger",963),
             ("v14_original_png_crop",160)]:
  assert c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]==n
 labels={}
 for label,ids in CATS.items():
  for idx in ids:
   assert 1<=idx<=160 and idx not in labels,(label,idx)
   labels[idx]=label
 assert sorted(labels)==list(range(1,161))
 c.executescript("""
 CREATE TABLE v15_visual_part_observation(
  sample_index INTEGER PRIMARY KEY,entry_id TEXT,group_id TEXT,source_key TEXT,
  original_png_path TEXT,source_crop_pixel_sha256 TEXT,source_png_sha256 TEXT,
  contact_sheet_no INTEGER,contact_sheet_sha256 TEXT,
  observed_broad_part_class TEXT,classification_confidence TEXT,
  visual_review_scope TEXT NOT NULL,source_image_directly_viewed INTEGER NOT NULL,
  automatic_game_identity_match INTEGER NOT NULL DEFAULT 0,
  same_furniture_across_directions_verified INTEGER NOT NULL DEFAULT 0,
  whole_furniture_assembly_verified INTEGER NOT NULL DEFAULT 0,
  original_tile_class_is_exact INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v15_source_group_review_coverage(
  entry_id TEXT PRIMARY KEY,group_id TEXT,original_name TEXT,
  original_tile_count INTEGER,observed_single_source_crop INTEGER,
  observed_broad_part_class TEXT,
  full_group_visually_reviewed INTEGER NOT NULL DEFAULT 0,
  game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE INDEX v15_part_group ON v15_visual_part_observation(group_id);
 """)
 sample=rows(c,"SELECT * FROM v14_original_png_crop ORDER BY crop_queue_number")
 entry={r["entry_id"]:r for r in rows(c,"SELECT * FROM v14_source_only_ledger")}
 audit=[];counts=Counter();viewed=set()
 confidence_med={"SHELTER_PART","FURNITURE_TABLE_OR_COUNTER_PART","FURNITURE_STORAGE_OR_SHELVING_PART",
  "EQUIPMENT_OR_APPLIANCE","STRUCTURE_OR_ARCHITECTURAL_PART","FURNITURE_SEATING_PART",
  "FURNITURE_BED_OR_CRIB_PART","MATERIAL_OR_LOOSE_ITEM"}
 for x in sample:
  idx=x["crop_queue_number"];label=labels[idx]
  assert x["crop_status"]=="ORIGINAL_PIXEL_CROP_OK" and len(x["crop_pixel_sha256"])==64
  assert len(x["png_sha256"])==64
  s=(idx-1)//40+1
  conf="LOW" if label=="VISUALLY_INDETERMINATE" else ("MODERATE" if label in confidence_med else "HIGH_FOR_BROAD_VISUAL_SHAPE_ONLY")
  r=dict(sample_index=idx,entry_id=x["entry_id"],group_id=entry[x["entry_id"]]["group_id"],
   source_key=x["source_key"],original_png_path=x["png_path"],
   source_crop_pixel_sha256=x["crop_pixel_sha256"],source_png_sha256=x["png_sha256"],
   contact_sheet_no=s,contact_sheet_sha256=sha[s],
   observed_broad_part_class=label,classification_confidence=conf,
   visual_review_scope="DIRECT_VIEW_OF_ONE_ORIGINAL_PNG_SPRITE_CELL_NOT_ASSEMBLED_OBJECT",
   source_image_directly_viewed=1)
  insert(c,"v15_visual_part_observation",r);audit.append(r)
  counts[label]+=1;viewed.add(x["entry_id"])
 coverage=[]
 for x in entry.values():
  idx=next((i for i in sample if i["entry_id"]==x["entry_id"]),None)
  r=dict(entry_id=x["entry_id"],group_id=x["group_id"],original_name=x["original_name"],
   original_tile_count=x["original_tile_count"],observed_single_source_crop=int(bool(idx)),
   observed_broad_part_class=labels[idx["crop_queue_number"]] if idx else "")
  insert(c,"v15_source_group_review_coverage",r);coverage.append(r)
 assert len(viewed)==160 and len(coverage)==963
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("SELECT COUNT(*) FROM v15_visual_part_observation").fetchone()[0]==160
 assert c.execute("SELECT COUNT(*) FROM v15_source_group_review_coverage").fetchone()[0]==963
 assert c.execute("SELECT COUNT(*) FROM v15_visual_part_observation WHERE automatic_game_identity_match!=0 OR same_furniture_across_directions_verified!=0 OR whole_furniture_assembly_verified!=0 OR original_tile_class_is_exact!=0").fetchone()[0]==0
 assert c.execute("SELECT COUNT(*) FROM v15_source_group_review_coverage WHERE full_group_visually_reviewed!=0 OR game_object_identity_certified!=0").fetchone()[0]==0
 c.close()
 emit("V15_160_DIRECTLY_INSPECTED_ORIGINAL_TILE_BROAD_VISUAL_CLASSES.csv",audit)
 emit("V15_963_SOURCE_GROUP_SINGLE_CROP_VISUAL_COVERAGE.csv",coverage)
 emit("V15_15_BROAD_VISUAL_CATEGORIES.csv",[
  dict(broad_visual_class=k,source_sprite_samples=v,game_object_identities_certified=0,
   interpretation="appearance of 1 source tile only, not full physical furniture") for k,v in sorted(counts.items())])
 manifest=dict(version="v15",base_v14_full_sqlite_preserved=True,
  raw_tiledef_attributes=195265,source_furniture_candidate_tile_keys=8219,
  source_only_registry_candidates=963,original_png_tiles_directly_viewed=160,
  original_png_contact_sheets_directly_viewed=4,representative_one_cell_visual_coverage_percent=round(160/963*100,2),
  unreviewed_source_only_groups=803,broad_visual_category_counts=dict(sorted(counts.items())),
  reviewed_full_group_assemblies=0,identities_certified=0,
  original_warnings_unresolved=474,wiki_not_authoritative=True,
  lua_tmx_minecraft_not_started=True,
  original_contact_sheet_sha256={str(k):v for k,v in sha.items()},
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 source-only v15 — 원본 타일 160개의 실제 이미지 형태 관찰\n\n"
 "v14 접촉시트 4장을 직접 열어 보고 총 160개의 단일 스프라이트 셀에 대한 넓은 시각적 유형을 기록했습니다.\n"
 "원본 PNG 픽셀 SHA256 및 접촉시트 SHA256에 행별로 연결하여 160개 개별 시각 검수 레코드를 보존했습니다.\n"
 "가구 외에 간판/포스터/자연물/건축 자재/설치물도 섞여 있으므로 '963개 미연결 = 963종 가구'로 보지 않습니다.\n"
 "시각 유형은 텍스트/원본 이미지의 단일 타일에 근거한 **잠정 광의 분류**이며 정확한 게임 이름, 동일 가구의 다른 방향, 조립/런타임 정체를 뜻하지 않습니다.\n"
 "160/963은 한 셀의 시각적 확인 범위일 뿐, 개별 가구 전체의 확인율이 아닙니다.\n"
 "기존 Work에서 보고한 107그룹/574타일은 행별 증거가 없어서 이전과 같이 신규 160 검수 결과로 합산하지 않았습니다.\n"
 "위키는 오래되거나 누락될 수 있는 보조자료, 원본 TileDef/PNG 우선. 기존 474경고 전부 미해결.\n",encoding="utf8")
 package=OUT/"B42_FURNITURE_COARSE_VISUAL_REVIEW_V15.zip"
 with zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(OUT.iterdir()):
   if f.is_file() and f!=package and not f.name.startswith("STAGED_"):
    z.write(f,f.name)
 with zipfile.ZipFile(package) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V15_160_SOURCE_CROPS_DIRECTLY_VISUALLY_INSPECTED_SAVED",json.dumps(manifest,ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
