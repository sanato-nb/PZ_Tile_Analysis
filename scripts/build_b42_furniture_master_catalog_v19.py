#!/usr/bin/env python3
"""B42 v19: direct visual source evidence for groups 641-800, no in-game identity claims.
Preserves full v18 SQLite; adds v19 master, review, queue, 23 source-image blockers.
"""
import csv,hashlib,json,sqlite3,zipfile,shutil
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/furniture_full_b42/2026-11-04/visual_review_v18/B42_FURNITURE_MASTER_INVENTORY_V18.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/visual_review_v19"
DB=OUT/"B42_FURNITURE_MASTER_INVENTORY_V19.sqlite"
PACK=OUT/"B42_FURNITURE_MASTER_INVENTORY_V19.zip"
def query(c,sql,args=()): return [dict(x) for x in c.execute(sql,args)]
def count(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def js(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def insert(c,t,row):
 names=list(row)
 c.execute("INSERT INTO "+t+" ("+",".join(names)+") VALUES ("+",".join("?" for _ in names)+")",list(row.values()))
def readcsv(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def output(name,items):
 assert items,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)

def main():
 assert BASE.is_file() and OUT.is_dir() and not DB.exists()
 stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 assert stage["original_png_pixel_crops_ok"]==160 and stage["distinct_source_only_samples"]==800
 assert stage["overlap_with_v15_v16_v17_v18"]==0
 crops=readcsv(OUT/"V19_160_NEW_ORIGINAL_PNG_CROP_SHA256.csv")
 labels=readcsv(OUT/"V19_160_DIRECT_VISUAL_LABELS.csv")
 assert len(crops)==160 and len(labels)==160
 bylabel={int(x["sample_index"]):x for x in labels}
 assert set(bylabel)==set(range(641,801))
 sheets={}
 for i in range(1,5):
  p=OUT/("V19_NEW_SOURCE_CONTACT_%02d.png"%i)
  sheets[i]=hashlib.sha256(p.read_bytes()).hexdigest()
  assert sheets[i]==stage["contact_sheet_sha256"][str(i)],i
 base_sha=hashlib.sha256(BASE.read_bytes()).hexdigest()
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_MASTER_INVENTORY_V18.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 original={"source_attributes":195265,"source_slots":73644,"registry_entry":2231,
 "wiki_furniture":1268,"furniture_tile":8219,"v12_template_proof":3840,
 "v13_warning_case":474,"v13_storage_link":1855,"v14_source_only_ledger":963,
 "v15_visual_part_observation":160,"v16_visual_part_observation":160,
 "v17_visual_part_observation":160,"v18_visual_part_observation":160,
 "v18_master_furniture_registry":2231,"v18_source_only_review_coverage":963,
 "v18_pending_source_only_queue":323}
 for t,n in original.items():assert count(c,t)==n,(t,count(c,t),n)
 sources={x["entry_id"]:x for x in query(c,"SELECT * FROM v14_source_only_ledger")}
 prior_queries=[
 "SELECT entry_id,group_id,observed_broad_part_class AS shape FROM v15_visual_part_observation",
 "SELECT entry_id,source_group_id AS group_id,broad_visual_shape_class AS shape FROM v16_visual_part_observation",
 "SELECT entry_id,source_group_id AS group_id,broad_visual_shape_class AS shape FROM v17_visual_part_observation",
 "SELECT entry_id,source_group_id AS group_id,visible_broad_shape AS shape FROM v18_visual_part_observation"]
 prior=[r for q in prior_queries for r in query(c,q)]
 previous_ids={r["entry_id"] for r in prior};previous_groups={r["group_id"] for r in prior}
 assert len(previous_ids)==640 and len(previous_groups)==640
 c.executescript("""
 CREATE TABLE v19_visual_part_observation(
  sample_index INTEGER PRIMARY KEY,entry_id TEXT NOT NULL,source_group_id TEXT,
  source_key TEXT,original_name TEXT,original_png_path TEXT,
  source_png_sha256 TEXT,source_crop_pixel_sha256 TEXT,
  contact_sheet_number INTEGER,contact_sheet_sha256 TEXT,
  broad_visible_shape TEXT,confidence_scope TEXT,visual_evidence_scope TEXT,
  directly_observed_original_single_sprite INTEGER NOT NULL DEFAULT 1,
  entire_furniture_assembly_certified INTEGER NOT NULL DEFAULT 0,
  same_game_object_across_facings_certified INTEGER NOT NULL DEFAULT 0,
  official_game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE UNIQUE INDEX v19_observation_unique_source_group ON v19_visual_part_observation(source_group_id);
 CREATE TABLE v19_master_furniture_registry AS SELECT * FROM v18_master_furniture_registry;
 CREATE UNIQUE INDEX v19_master_entry ON v19_master_furniture_registry(entry_id);
 CREATE TABLE v19_source_only_review_coverage AS SELECT * FROM v18_source_only_review_coverage;
 CREATE UNIQUE INDEX v19_source_entry ON v19_source_only_review_coverage(entry_id);
 CREATE TABLE v19_unreviewed_source_queue(
  entry_id TEXT PRIMARY KEY,source_group_id TEXT,original_name TEXT,
  source_sprite_tile_count INTEGER,original_png_cell_mapping_present INTEGER,
  original_png_path TEXT,selected_source_key TEXT,
  directional_template_candidates INTEGER,
  geometric_complete_rectangle_candidates INTEGER,
  original_raw_container_types_json TEXT,original_raw_capacity_values_json TEXT,
  source_visual_review_status TEXT NOT NULL DEFAULT 'NOT_REVIEWED',
  exact_game_object_identity_verified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v19_23_missing_png_group_diagnostics(
  entry_id TEXT PRIMARY KEY,source_group_id TEXT,original_name TEXT,
  source_tile_count INTEGER,source_keys_json TEXT,source_files_json TEXT,
  tiledef_tilesets_json TEXT,local_ids_json TEXT,
  candidate_image_cell_rows INTEGER,candidate_original_png_paths_json TEXT,
  mapping_diagnostic TEXT,manual_image_identity_reviewed INTEGER DEFAULT 0,
  exact_game_object_identity_verified INTEGER DEFAULT 0);
 CREATE TABLE v19_progress_metric(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,percent REAL,
  evidence_scope TEXT,description TEXT);
 """)
 observed=[];newids=set();newgroups=set()
 for row in crops:
  idx=int(row["sample_index"]);eid=row["entry_id"];gid=row["group_id"]
  assert idx in bylabel and idx not in newids
  assert eid in sources and eid not in previous_ids and eid not in newids
  assert gid==sources[eid]["group_id"] and gid not in previous_groups and gid not in newgroups
  assert row["crop_status"]=="OK" and row["prior_v15_v16_v17_v18_review_overlap"]=="0"
  assert row["visually_inspected"]=="0" and row["game_identity_certified"]=="0"
  assert row["source_key"]==sources[eid]["original_png_tile_key"]
  assert row["png_path"]==sources[eid]["original_png_path"]
  assert len(row["png_sha256"])==64 and len(row["crop_pixel_sha256"])==64
  lab=bylabel[idx]
  assert lab["observation_scope"]=="DIRECT_VIEW_ONE_ORIGINAL_PNG_SPRITE_NOT_WHOLE_GAME_OBJECT"
  sheet=(idx-641)//40+1
  rec=dict(sample_index=idx,entry_id=eid,source_group_id=gid,source_key=row["source_key"],
   original_name=sources[eid]["original_name"],original_png_path=row["png_path"],
   source_png_sha256=row["png_sha256"],source_crop_pixel_sha256=row["crop_pixel_sha256"],
   contact_sheet_number=sheet,contact_sheet_sha256=sheets[sheet],
   broad_visible_shape=lab["observed_broad_class"],confidence_scope=lab["classification_confidence"],
   visual_evidence_scope=lab["observation_scope"])
  insert(c,"v19_visual_part_observation",rec);observed.append(rec)
  c.execute("""UPDATE v19_master_furniture_registry SET direct_1cell_source_image_visual_review_rows=1,
   direct_1cell_visual_broad_class=?,review_scope_status='ONE_RAW_TILE_VISUAL_REVIEWED_NOT_WHOLE_FURNITURE'
   WHERE entry_id=? AND direct_1cell_source_image_visual_review_rows=0""",(lab["observed_broad_class"],eid))
  assert c.execute("SELECT changes()").fetchone()[0]==1,("master",eid)
  c.execute("""UPDATE v19_source_only_review_coverage SET direct_one_cell_visual_reviewed=1,
   first_direct_visual_review_version='v19',broad_visible_shape=?
   WHERE entry_id=? AND direct_one_cell_visual_reviewed=0""",(lab["observed_broad_class"],eid))
  assert c.execute("SELECT changes()").fetchone()[0]==1,("coverage",eid)
  newids.add(eid);newgroups.add(gid)
 assert len(observed)==160 and len(newids)==160 and len(newgroups)==160
 assert c.execute("SELECT SUM(direct_one_cell_visual_reviewed) FROM v19_source_only_review_coverage").fetchone()[0]==800
 assert c.execute("SELECT SUM(direct_1cell_source_image_visual_review_rows) FROM v19_master_furniture_registry").fetchone()[0]==800

 pending=[]
 for r in query(c,"SELECT entry_id FROM v19_source_only_review_coverage WHERE direct_one_cell_visual_reviewed=0 ORDER BY entry_id"):
  s=sources[r["entry_id"]]
  o=dict(entry_id=r["entry_id"],source_group_id=s["group_id"],original_name=s["original_name"],
   source_sprite_tile_count=s["original_tile_count"],
   original_png_cell_mapping_present=s["image_mapping_present"],
   original_png_path=s["original_png_path"],selected_source_key=s["original_png_tile_key"],
   directional_template_candidates=s["direction_templates"],
   geometric_complete_rectangle_candidates=s["geometrically_rectangular_candidates"],
   original_raw_container_types_json=s["container_types_raw_json"],
   original_raw_capacity_values_json=s["capacity_raw_json"])
  insert(c,"v19_unreviewed_source_queue",o);pending.append(o)
 assert len(pending)==163
 missing=[x for x in pending if not x["original_png_cell_mapping_present"]]
 mapped=[x for x in pending if x["original_png_cell_mapping_present"]]
 assert len(missing)==23 and len(mapped)==140,(len(missing),len(mapped))

 # Trace the 23 mapping blockers at original per-tile level. Never synthesize missing pixels.
 tile_by_source={x["source_key"]:x for x in query(c,"SELECT source_key,tileset,local_id FROM furniture_tile")}
 image_cells=defaultdict(list)
 for r in query(c,"SELECT tileset,local_id,png_path FROM image_cells WHERE tileset IS NOT NULL AND local_id IS NOT NULL"):
  image_cells[(r["tileset"].casefold(),r["local_id"])].append(r["png_path"])
 blockers=[]
 for item in missing:
  src=sources[item["entry_id"]]
  keys=json.loads(src["original_tile_ids_json"])
  tiles=[tile_by_source[k] for k in keys]
  matched=sorted({p for t in tiles for p in image_cells.get((t["tileset"].casefold(),t["local_id"]),[]) if p})
  ncell=sum(len(image_cells.get((t["tileset"].casefold(),t["local_id"]),[])) for t in tiles)
  diag=("NO_MATCHING_ORIGINAL_PNG_CELL_IN_INDEXED_ATLASES" if ncell==0 else
        "IMAGE_CELL_EXISTS_BUT_NO_VALID_SELECTED_SOURCE_PNG_MAPPING_VERIFY_SCHEMA")
  r=dict(entry_id=item["entry_id"],source_group_id=item["source_group_id"],
   original_name=item["original_name"],source_tile_count=len(keys),
   source_keys_json=js(keys),source_files_json=src["original_source_files_json"],
   tiledef_tilesets_json=js(sorted({t["tileset"] for t in tiles})),
   local_ids_json=js(sorted({t["local_id"] for t in tiles})),
   candidate_image_cell_rows=ncell,candidate_original_png_paths_json=js(matched),
   mapping_diagnostic=diag)
  insert(c,"v19_23_missing_png_group_diagnostics",r);blockers.append(r)
 assert len(blockers)==23

 counted=Counter(r["shape"] for r in prior)
 counted.update(r["broad_visible_shape"] for r in observed)
 newcount=Counter(r["broad_visible_shape"] for r in observed)
 assert sum(counted.values())==800 and sum(newcount.values())==160
 metrics=[
  ("collected_candidate_registry_rows",2231,2231,"registered known source+Wiki candidates, not complete game furniture","REGISTRY"),
  ("wiki_reference_rows",1268,1268,"Wiki may be stale or incomplete","REFERENCE"),
  ("wiki_image_source_id_connected",1257,1268,"direct Wiki image IDs not official game object identity","IMAGE_ID_LINK"),
  ("source_only_candidates_grouped",963,963,"exact Wiki image ID unlinked does not prove Wiki page missing","SOURCE_GROUP"),
  ("source_only_one_original_sprite_directly_inspected",800,963,"one representative original sprite of each distinct group, not whole assembly","VISUAL_SHAPE"),
  ("source_only_original_png_remaining_mapped",0,140,"140 image-mapped groups not yet visually inspected","PENDING"),
  ("source_only_original_png_mapping_blockers",0,23,"23 groups lack valid original atlas cell mapping; detailed reasons recorded","PENDING"),
  ("source_tiles_with_provenance",8219,8219,"original TileDef source keys preserved","RAW_SOURCE"),
  ("source_group_direction_geometry_checked",3840,3840,"candidate geometry not runtime furniture certification","GEOMETRY"),
  ("source_storage_evidence_links",1855,1855,"raw source values not loot item content","RAW_SOURCE"),
  ("old_warnings_resolved",0,474,"source warnings not yet resolved","UNRESOLVED"),
  ("exact_game_object_identity_certified",0,0,"ground truth game-furniture count unknown","UNKNOWN")
 ]
 progress=[]
 for key,num,den,desc,grade in metrics:
  o=dict(metric_key=key,numerator=num,denominator=den,
         percent=round(100*num/den,2) if den else None,
         evidence_scope=grade,description=desc)
  insert(c,"v19_progress_metric",o);progress.append(o)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for table,n in {**original,"v19_visual_part_observation":160,
 "v19_master_furniture_registry":2231,"v19_source_only_review_coverage":963,
 "v19_unreviewed_source_queue":163,
 "v19_23_missing_png_group_diagnostics":23,
 "v19_progress_metric":len(metrics)}.items():
  assert count(c,table)==n,(table,count(c,table),n)
 assert c.execute("""SELECT COUNT(*) FROM v19_visual_part_observation
  WHERE entire_furniture_assembly_certified!=0 OR same_game_object_across_facings_certified!=0
  OR official_game_object_identity_certified!=0""").fetchone()[0]==0
 master=query(c,"SELECT * FROM v19_master_furniture_registry ORDER BY entry_id")
 coverage=query(c,"SELECT * FROM v19_source_only_review_coverage ORDER BY entry_id")
 c.close()
 output("V19_160_NEW_DIRECT_VISUAL_OBSERVATIONS.csv",observed)
 output("V19_2231_FULL_MASTER_CANDIDATE_CATALOG.csv",master)
 output("V19_963_SOURCE_ONLY_REVIEW_COVERAGE.csv",coverage)
 output("V19_163_REMAINING_SOURCE_GROUP_QUEUE.csv",pending)
 output("V19_23_MISSING_PNG_ORIGINAL_TILE_DIAGNOSTICS.csv",blockers)
 output("V19_800_COMBINED_VISUAL_SHAPE_CLASS_COUNTS.csv",[
  dict(broad_visual_shape=k,one_original_sprite_group_count=n,whole_object_identity_verified=0)
  for k,n in sorted(counted.items())])
 output("V19_12_SCOPED_PROGRESS.csv",progress)
 manifest=dict(version="v19",base_v18_zip_sha256=base_sha,
  currently_collected_candidate_registry_rows=2231,wiki_reference_rows=1268,
  wiki_image_to_source_id_linked=1257,wiki_unlinked_rows=11,
  source_only_candidate_groups=963,raw_tiledef_property_rows=195265,
  original_source_slots=73644,furniture_candidate_tile_keys=8219,
  source_directional_geometry_candidates=3840,raw_source_storage_evidence_links=1855,
  original_png_direct_single_sprite_review_groups=800,
  each_visual_review_version_160=["v15","v16","v17","v18","v19"],
  verified_disjoint_original_single_sprite_review_pct=round(100*800/963,2),
  new_directly_viewed_source_sprite_groups=160,
  source_only_groups_without_one_sprite_visual_review=163,
  remaining_original_png_mapped_groups=140,remaining_png_mapping_blockers=23,
  missing_png_diagnostic_summary=dict(sorted(Counter(x["mapping_diagnostic"] for x in blockers).items())),
  new_160_visual_class_counts=dict(sorted(newcount.items())),
  all_800_visual_class_counts=dict(sorted(counted.items())),
  prior_Work_107_groups_574_tiles_group_ids_not_confirmed=True,
  prior_duplicate_129_groups_image_review_reference=129,
  wiki_is_potentially_stale_or_incomplete=True,
  source_only_group_is_not_proof_wiki_absence=True,
  original_source_warnings_unresolved=474,
  certified_whole_assembled_furniture=0,certified_4way_same_game_object=0,
  certified_game_object_identities=0,loa_lua_TMX_minecraft_not_implemented=True,
  original_SQLite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 가구 데이터베이스 v19 — 원본 중심의 단일 이미지 검수 800/963\n\n"
 "기존 v18 SQLite 전체와 v15~v18의 640개 원본 타일 시각 관찰 이력을 보존합니다.\n"
 "추가 원본 PNG 접촉 시트 4장, 서로 다른 160그룹의 대표 스프라이트 1장씩 직접 살펴보고 광의 시각 유형을 개별 저장했습니다.\n"
 "원본 전용 963 후보 중 대표 타일 단독 시각 검수 800(83.07%), 미검수 163입니다.\n"
 "미검수 163개 중 원본 PNG 셀 연결 가능 140개, 연결 미확인 23개를 원본 source key/tileset/local ID 단위로 별도 진단했습니다.\n"
 "이 통계는 '대표 스프라이트 한 장의 외형 관찰'이며 전체 가구 조립, 4방향 일치 또는 게임 내부 정체 인증이 아닙니다.\n"
 "현재 확보된 목록 2231행 등록률 100%는 위키/원본 소스 후보 목록에 한정되며 고유 가구 수 확정이 아닙니다.\n"
 "Wiki는 최신·완전하지 않을 수 있는 참고 소스이고 TileDef·PNG가 우선입니다.\n"
 "Work의 기존 107그룹/574타일 이미지 열람 보고는 개별 ID가 확보되지 않아 중복 제거 후 추가 합산하지 않았습니다.\n"
 "기존 중복 그룹 129건 이미지 검수 참조와 474개 미해결 원본 경고를 보존합니다.\n"
 "Lua loot/TMX 배치/마인크래프트 구현은 계속 보류합니다.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for file in sorted(OUT.iterdir()):
   if (file.is_file() and file!=PACK and not file.name.startswith("STAGED_")
       and not file.name.startswith("_v19_required") and not file.name.endswith("_BASE64.txt")):
    z.write(file,file.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V19_FULL_2231_MASTER_800_DISJOINT_SOURCE_VISUAL_REVIEWS_AND_23_PNG_DIAGNOSTICS_VERIFIED",
       js(manifest),flush=True)
if __name__=="__main__":main()
