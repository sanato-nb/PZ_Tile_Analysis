#!/usr/bin/env python3
"""B42 furniture DB v20: finish 140/140 indexed source PNG representative crops.
Keep all v19 source evidence, separately trace 23 unresolved missing PNG atlas mappings.
A one-cell visual category is NOT an official object identity, facing assembly or wiki truth.
"""
import csv,hashlib,json,sqlite3,zipfile,shutil
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]
OLD=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v19/B42_FURNITURE_MASTER_INVENTORY_V19.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v20"
DB=OUT/"B42_FURNITURE_MASTER_INVENTORY_V20.sqlite"
PACK=OUT/"B42_FURNITURE_MASTER_INVENTORY_V20.zip"
def qr(c,q,p=()):return [dict(x) for x in c.execute(q,p)]
def count(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def j(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def add(c,t,d):
 keys=list(d);c.execute("INSERT INTO "+t+"("+",".join(keys)+") VALUES("+",".join("?" for _ in keys)+")",list(d.values()))
def readcsv(name):
 with (OUT/name).open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(name,rows):
 assert rows,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 assert OLD.is_file() and OUT.is_dir() and not DB.exists()
 stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["original_png_pixel_crops_ok"]==140 and stage["distinct_source_only_samples"]==940
 assert stage["overlap_with_v15_v16_v17_v18_v19"]==0
 crops=readcsv("V20_160_NEW_ORIGINAL_PNG_CROP_SHA256.csv")
 assert len(crops)==140, "The staging file retains its historic 160 label but contains exactly 140 new crops"
 labels=readcsv("V20_140_DIRECT_VISUAL_LABELS.csv")
 assert len(crops)==140 and len(labels)==140
 bylabel={int(x["sample_index"]):x for x in labels}
 assert len(bylabel)==140 and set(bylabel)==set(range(801,941))
 for rec in labels:
  assert rec["observation_scope"]=="DIRECT_VIEW_ONE_ORIGINAL_PNG_SPRITE_NOT_WHOLE_GAME_OBJECT"
  assert rec["classification_confidence"] in ("HIGH_ONLY_FOR_COARSE_SHAPE","MODERATE_BROAD_SHAPE")
 sha={}
 for idx in range(1,5):
  p=OUT/("V20_NEW_SOURCE_CONTACT_%02d.png"%idx)
  sha[idx]=hashlib.sha256(p.read_bytes()).hexdigest()
  assert sha[idx]==stage["contact_sheet_sha256"][str(idx)],idx
 atlas=json.loads((OUT/"V20_372_ORIGINAL_PNG_ASSET_FILENAME_INVENTORY.json").read_text(encoding="utf8"))
 assert atlas["total_files"]==372 and len(atlas["filename_inventory"])==372
 original_assets={x["name"] for x in atlas["filename_inventory"] if x["type"]=="file"}
 assert "lighting_indoor_01.png" in original_assets and "crafted_03.png" not in original_assets

 with zipfile.ZipFile(OLD) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_MASTER_INVENTORY_V19.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 originals={
 "source_attributes":195265,"source_slots":73644,"registry_entry":2231,"wiki_furniture":1268,
 "furniture_tile":8219,"v12_template_proof":3840,"v13_warning_case":474,
 "v13_storage_link":1855,"v14_source_only_ledger":963,
 "v15_visual_part_observation":160,"v16_visual_part_observation":160,
 "v17_visual_part_observation":160,"v18_visual_part_observation":160,
 "v19_visual_part_observation":160,"v19_master_furniture_registry":2231,
 "v19_source_only_review_coverage":963,"v19_unreviewed_source_queue":163,
 "v19_23_missing_png_group_diagnostics":23}
 for t,n in originals.items():assert count(c,t)==n,(t,count(c,t),n)
 prior=[]
 for tab,groupcol,cat in [
  ("v15_visual_part_observation","group_id","observed_broad_part_class"),
  ("v16_visual_part_observation","source_group_id","broad_visual_shape_class"),
  ("v17_visual_part_observation","source_group_id","broad_visual_shape_class"),
  ("v18_visual_part_observation","source_group_id","visible_broad_shape"),
  ("v19_visual_part_observation","source_group_id","broad_visible_shape")]:
  prior+=qr(c,f"SELECT entry_id,{groupcol} AS group_id,{cat} AS broad_class FROM {tab}")
 seen_entry={r["entry_id"] for r in prior}
 seen_group={r["group_id"] for r in prior}
 assert len(seen_entry)==800 and len(seen_group)==800
 src={r["entry_id"]:r for r in qr(c,"SELECT * FROM v14_source_only_ledger")}
 assert len(src)==963

 c.executescript("""
 CREATE TABLE v20_visual_part_observation(
  sample_index INTEGER PRIMARY KEY,entry_id TEXT NOT NULL,source_group_id TEXT NOT NULL,
  source_key TEXT NOT NULL,original_name TEXT,original_png_path TEXT,
  original_png_sha256 TEXT,original_crop_pixel_sha256 TEXT,
  contact_sheet_no INTEGER,contact_sheet_sha256 TEXT,
  broad_visible_shape TEXT,classification_confidence TEXT,observation_scope TEXT,
  original_one_sprite_directly_viewed INTEGER NOT NULL DEFAULT 1,
  full_furniture_assembly_verified INTEGER NOT NULL DEFAULT 0,
  same_game_object_across_facings_certified INTEGER NOT NULL DEFAULT 0,
  exact_game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE UNIQUE INDEX v20_visual_group ON v20_visual_part_observation(source_group_id);
 CREATE TABLE v20_master_furniture_registry AS SELECT * FROM v19_master_furniture_registry;
 CREATE UNIQUE INDEX v20_master_entry ON v20_master_furniture_registry(entry_id);
 CREATE TABLE v20_source_only_review_coverage AS SELECT * FROM v19_source_only_review_coverage;
 CREATE UNIQUE INDEX v20_review_entry ON v20_source_only_review_coverage(entry_id);
 CREATE TABLE v20_unreviewed_source_queue(
  entry_id TEXT PRIMARY KEY,source_group_id TEXT,original_name TEXT,
  source_tile_count INTEGER,source_keys_json TEXT,source_tileset_png_mapping_status TEXT,
  exact_game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v20_23_original_atlas_filename_audit(
  entry_id TEXT PRIMARY KEY,source_group_id TEXT,original_name TEXT,
  original_tilesets_json TEXT,expected_png_filenames_json TEXT,
  exact_expected_png_assets_in_current_repo_json TEXT,
  missing_expected_png_assets_json TEXT,possible_neighbor_or_state_alias_assets_json TEXT,
  source_image_cell_matches_in_prior_db INTEGER,
  reason TEXT,original_png_mapping_certified INTEGER NOT NULL DEFAULT 0,
  visible_furniture_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v20_scoped_progress(
  metric_key TEXT PRIMARY KEY,done INTEGER,total INTEGER,percent REAL,
  evidence_kind TEXT,meaning TEXT);
 """)
 observed=[];new_entry=set();new_group=set()
 for crop in crops:
  idx=int(crop["sample_index"]);entry=crop["entry_id"];gid=crop["group_id"]
  assert 801<=idx<=940 and idx in bylabel
  assert entry in src and entry not in seen_entry and entry not in new_entry
  assert gid==src[entry]["group_id"] and gid not in seen_group and gid not in new_group
  assert crop["crop_status"]=="OK"
  assert crop["prior_v15_v16_v17_v18_v19_review_overlap"]=="0"
  assert crop["visually_inspected"]=="0" and crop["game_identity_certified"]=="0"
  assert crop["source_key"]==src[entry]["original_png_tile_key"]
  assert crop["png_path"]==src[entry]["original_png_path"]
  assert len(crop["png_sha256"])==64 and len(crop["crop_pixel_sha256"])==64
  sheet=(idx-801)//40+1
  label=bylabel[idx]
  record=dict(sample_index=idx,entry_id=entry,source_group_id=gid,source_key=crop["source_key"],
   original_name=src[entry]["original_name"],original_png_path=crop["png_path"],
   original_png_sha256=crop["png_sha256"],original_crop_pixel_sha256=crop["crop_pixel_sha256"],
   contact_sheet_no=sheet,contact_sheet_sha256=sha[sheet],
   broad_visible_shape=label["observed_broad_class"],
   classification_confidence=label["classification_confidence"],
   observation_scope=label["observation_scope"])
  add(c,"v20_visual_part_observation",record);observed.append(record)
  c.execute("""UPDATE v20_master_furniture_registry SET
   direct_1cell_source_image_visual_review_rows=1,
   direct_1cell_visual_broad_class=?,
   review_scope_status='ONE_RAW_TILE_VISUAL_REVIEWED_NOT_WHOLE_FURNITURE'
   WHERE entry_id=? AND direct_1cell_source_image_visual_review_rows=0""",
   (label["observed_broad_class"],entry))
  assert c.execute("SELECT changes()").fetchone()[0]==1,("master",entry)
  c.execute("""UPDATE v20_source_only_review_coverage SET
   direct_one_cell_visual_reviewed=1,
   first_direct_visual_review_version='v20',
   broad_visible_shape=?
   WHERE entry_id=? AND direct_one_cell_visual_reviewed=0""",
   (label["observed_broad_class"],entry))
  assert c.execute("SELECT changes()").fetchone()[0]==1,("review",entry)
  new_entry.add(entry);new_group.add(gid)
 assert len(new_entry)==140 and len(new_group)==140
 assert c.execute("SELECT SUM(direct_one_cell_visual_reviewed) FROM v20_source_only_review_coverage").fetchone()[0]==940
 assert c.execute("SELECT SUM(direct_1cell_source_image_visual_review_rows) FROM v20_master_furniture_registry").fetchone()[0]==940
 remaining=[]
 for r in qr(c,"SELECT entry_id FROM v20_source_only_review_coverage WHERE direct_one_cell_visual_reviewed=0 ORDER BY entry_id"):
  orig=src[r["entry_id"]]
  item=dict(entry_id=r["entry_id"],source_group_id=orig["group_id"],original_name=orig["original_name"],
    source_tile_count=orig["original_tile_count"],source_keys_json=orig["original_tile_ids_json"],
    source_tileset_png_mapping_status="NO_ORIGINAL_IMAGE_CELL_MATCH_IN_CURRENT_INDEX")
  add(c,"v20_unreviewed_source_queue",item);remaining.append(item)
 assert len(remaining)==23
 assert sum(int(src[r["entry_id"]]["image_mapping_present"]) for r in remaining)==0
 existing23={r["entry_id"]:r for r in qr(c,"SELECT * FROM v19_23_missing_png_group_diagnostics")}
 assert set(existing23)=={r["entry_id"] for r in remaining}
 audits=[];reasons=Counter()
 for r in remaining:
  old=existing23[r["entry_id"]]
  tilesets=json.loads(old["tiledef_tilesets_json"])
  requested=[x+".png" for x in tilesets]
  exists=sorted(x for x in requested if x in original_assets)
  missing=sorted(x for x in requested if x not in original_assets)
  alias=set()
  for t in tilesets:
   if t.endswith("_on") and t[:-3]+".png" in original_assets:
    alias.add(t[:-3]+".png")
   if t.endswith("_off") and t[:-4]+".png" in original_assets:
    alias.add(t[:-4]+".png")
  # Similar filenames are navigation hints, not evidence of the SAME sprite/object.
  for t in tilesets:
   toks=t.split("_")
   if len(toks)>=2:
    prefix="_".join(toks[:2])+"_"
    candidates=sorted(x for x in original_assets if x.startswith(prefix))[:8]
    alias.update(candidates)
  alias.difference_update(exists)
  if exists and int(old["candidate_image_cell_rows"])==0:
   reason="EXACT_REPO_PNG_PRESENT_BUT_NOT_INDEXED_AS_TILE_CELL"
  elif not exists:
   reason="EXPECTED_TILESET_PNG_FILENAME_NOT_PRESENT_IN_CURRENT_REPO_ASSETS"
  else:
   reason="SOURCE_IMAGE_MAPPING_UNRESOLVED"
  item=dict(entry_id=r["entry_id"],source_group_id=r["source_group_id"],
   original_name=r["original_name"],original_tilesets_json=old["tiledef_tilesets_json"],
   expected_png_filenames_json=j(requested),
   exact_expected_png_assets_in_current_repo_json=j(exists),
   missing_expected_png_assets_json=j(missing),
   possible_neighbor_or_state_alias_assets_json=j(sorted(alias)),
   source_image_cell_matches_in_prior_db=int(old["candidate_image_cell_rows"]),
   reason=reason)
  add(c,"v20_23_original_atlas_filename_audit",item);audits.append(item);reasons[reason]+=1
 assert len(audits)==23

 broad=Counter(r["broad_class"] for r in prior)
 broad.update(r["broad_visible_shape"] for r in observed)
 fresh=Counter(r["broad_visible_shape"] for r in observed)
 assert sum(broad.values())==940 and sum(fresh.values())==140
 scopes=[
  ("source_candidate_registry_rows",2231,2231,"REGISTRY","Registered current Wiki+TileDef candidates, not true game census"),
  ("wiki_reference_rows",1268,1268,"REFERENCE","May be stale/missing entries"),
  ("wiki_to_source_sprite_id_linked",1257,1268,"DIRECT_IMAGE_ID","Does not certify actual game object identity"),
  ("source_only_candidate_group_rows",963,963,"SOURCE_GROUP","No Wiki image ID match; may be non-furniture"),
  ("source_only_mapped_original_png_one_cell_seen",940,940,"PIXEL_DIRECT","All currently mapped source-only groups, only ONE representative tile each"),
  ("source_only_any_original_one_cell_seen",940,963,"VISUAL_SCOPE","23 source-only groups missing original image-cell mappings"),
  ("missing_png_mapping_resolved",0,23,"OPEN_GAP","23 original tile atlas mappings not certified"),
  ("source_tile_id_preserved",8219,8219,"SOURCE_RAW","TileDef original candidate tile keys and properties"),
  ("directional_group_templates_analyzed",3840,3840,"GEOMETRY","Not actual full furniture assembly"),
  ("original_storage_rows_joined",1855,1855,"SOURCE_RAW","Container properties, not Lua contents"),
  ("old_warnings_certified_resolved",0,474,"OPEN_WARNING","Still unresolved source warnings"),
  ("verified_full_object_identity",0,0,"UNKNOWN_DENOMINATOR","No certified in-game game object identity")
 ]
 prog=[]
 for k,n,total,grade,desc in scopes:
  item=dict(metric_key=k,done=n,total=total,percent=round(100*n/total,2) if total else None,
   evidence_kind=grade,meaning=desc)
  add(c,"v20_scoped_progress",item);prog.append(item)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for tab,n in {**originals,"v20_visual_part_observation":140,"v20_master_furniture_registry":2231,
  "v20_source_only_review_coverage":963,"v20_unreviewed_source_queue":23,
  "v20_23_original_atlas_filename_audit":23,"v20_scoped_progress":len(scopes)}.items():
  assert count(c,tab)==n,(tab,count(c,tab),n)
 assert c.execute("""SELECT COUNT(*) FROM v20_visual_part_observation WHERE
  full_furniture_assembly_verified!=0 OR same_game_object_across_facings_certified!=0
  OR exact_game_object_identity_certified!=0""").fetchone()[0]==0
 master=qr(c,"SELECT * FROM v20_master_furniture_registry ORDER BY entry_id")
 coverage=qr(c,"SELECT * FROM v20_source_only_review_coverage ORDER BY entry_id")
 c.close()
 shutil.copy2(OUT/"V20_160_NEW_ORIGINAL_PNG_CROP_SHA256.csv", OUT/"V20_140_NEW_ORIGINAL_PNG_CROP_SHA256.csv")
 writecsv("V20_140_DIRECT_ORIGINAL_SPRITE_VISUAL_OBSERVATIONS.csv",observed)
 writecsv("V20_2231_FULL_SOURCE_FIRST_MASTER.csv",master)
 writecsv("V20_963_SOURCE_GROUP_VISUAL_COVERAGE.csv",coverage)
 writecsv("V20_23_UNREVIEWED_MISSING_PNG_GROUPS.csv",remaining)
 writecsv("V20_23_PNG_SOURCE_ASSET_EXISTENCE_AUDIT.csv",audits)
 writecsv("V20_940_VISUAL_BROAD_CLASS_COUNTS.csv",[
  dict(broad_visual_shape=k,one_sprite_groups=v,game_identity_certified=0)
  for k,v in sorted(broad.items())])
 writecsv("V20_12_SCOPE_LIMITED_PROGRESS.csv",prog)
 manifest=dict(version="v20",original_v19_zip_sha256=hashlib.sha256(OLD.read_bytes()).hexdigest(),
  registered_source_and_wiki_candidate_rows=2231,wiki_reference_rows=1268,
  wiki_image_source_id_links=1257,wiki_image_id_unlinked_rows=11,
  source_only_candidate_groups=963,
  original_source_attributes=195265,original_source_slots=73644,
  furniture_candidate_source_tile_IDs=8219,directional_geometry_candidates=3840,
  original_source_storage_evidence_rows=1855,
  v15_v16_v17_v18_v19_one_original_sprite_reviewed=800,
  new_v20_one_original_sprite_directly_viewed=140,
  deduplicated_one_original_sprite_viewed_groups=940,
  known_original_png_mapped_group_visual_coverage="940/940",
  single_sprite_visual_coverage_percent_of_963=round(100*940/963,2),
  source_only_without_original_png_mapping=23,
  source_png_missing_asset_reason_counts=dict(sorted(reasons.items())),
  v20_broad_visible_class_counts=dict(sorted(fresh.items())),
  all_940_one_sprite_broad_classes=dict(sorted(broad.items())),
  prior_129_duplicate_group_visual_review_references=129,
  Work_prior_107_groups_574_sprites_reported_but_group_IDs_not_verified=True,
  wiki_may_be_outdated_incomplete=True,
  source_only_not_all_verified_furniture=True,
  warning_cases_unresolved=474,
  whole_assembled_furniture_certified=0,same_object_facing_certified=0,
  in_game_object_identity_certified=0,
  actual_lua_tmx_minecraft_not_started=True,
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 가구 목록 v20 — 연결 가능한 원본 PNG 대표 스프라이트 940/940 검수\n\n"
 "위키는 오래되거나 누락될 수 있는 참고이고 TileDef/원본 PNG가 우선입니다.\n"
 "v15~v19에 직접 본 서로 다른 800그룹에 더해 마지막 원본 PNG 매핑 140그룹의 단일 셀 스프라이트를 직접 확인하고 임시 외형을 기록했습니다.\n"
 "DB에 저장된 원본 전용 후보의 단일 대표 이미지 검수는 940/963=97.61%입니다. 현재 원본 PNG 셀 매핑이 존재하는 범위는 940/940=100%입니다.\n"
 "나머지 23개는 PNG 매핑 오류나 누락 가능성으로 개별 원본 TileDef ID/atlas 파일명까지 추적했고 임의 이미지 대체하지 않았습니다.\n"
 "2,231은 현재 수집한 Wiki 참조 1,268 + 소스 후보 963을 합한 등록 행 수이지 고유 게임 가구 수가 아닙니다.\n"
 "시각 외형 검수는 완성 가구 조립/방향별 객체 동일성 및 인게임 게임 오브젝트 인증이 아닙니다.\n"
 "이전 Work 보고 107그룹/574타일은 그룹 ID 중복 여부가 확인되지 않아 새로운 940에 더하지 않았습니다.\n"
 "과거 129개 중복 그룹 이미지 검수 참조, 474개 원본 경고, 모든 원본 테이블을 그대로 유지합니다.\n"
 "Lua loot/TMX/마크 구현은 계속 보류합니다.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in sorted(OUT.iterdir()):
   if (p.is_file() and p!=PACK and not p.name.startswith("STAGED_") and
       not p.name.startswith("_v20_required") and not p.name.endswith("_BASE64.txt")):
    z.write(p,p.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V20_ALL_940_MAPPED_PNG_SOURCE_GROUPS_DIRECTLY_VIEWED_AND_23_ASSET_GAPS_AUDITED",
       j(manifest),flush=True)
if __name__=="__main__":main()
