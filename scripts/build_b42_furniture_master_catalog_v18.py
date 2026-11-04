#!/usr/bin/env python3
"""v18 source-first furniture master: 160 additional directly viewed ORIGINAL PZ sprite crops.
Preserves every v17 SQLite table and all original evidence; never certifies an in-game object from a crop.
"""
import csv, hashlib, json, shutil, sqlite3, zipfile
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/furniture_full_b42/2026-11-04/visual_review_v17/B42_FURNITURE_MASTER_INVENTORY_V17.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/visual_review_v18"
DB=OUT/"B42_FURNITURE_MASTER_INVENTORY_V18.sqlite"
PACKAGE=OUT/"B42_FURNITURE_MASTER_INVENTORY_V18.zip"

def qr(db, sql, p=()):
    return [dict(x) for x in db.execute(sql,p)]
def ct(db, table):
    return db.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
def dump(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)
def put(db, table, obj):
    names=list(obj)
    db.execute("INSERT INTO "+table+"("+",".join(names)+") VALUES("+",".join("?" for _ in names)+")",[obj[k] for k in names])
def export(filename, records):
    assert records,filename
    with (OUT/filename).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]))
        w.writeheader();w.writerows(records)
def csvread(path):
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def main():
    assert BASE.is_file() and OUT.is_dir() and not DB.exists()
    stage=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
    assert stage["original_png_pixel_crops_ok"]==160
    assert stage["overlap_with_v15_v16_v17"]==0
    assert stage["distinct_source_only_samples"]==640
    assert stage["stage_image_reviewed"]==0
    crops=csvread(OUT/"V18_160_NEW_ORIGINAL_PNG_CROP_SHA256.csv")
    observed=csvread(OUT/"V18_160_DIRECT_VISUAL_LABELS.csv")
    assert len(crops)==160 and len(observed)==160
    labels={}
    for r in observed:
        i=int(r["sample_index"])
        assert i not in labels and 481<=i<=640
        assert r["observation_scope"]=="DIRECT_VIEW_ONE_ORIGINAL_PNG_SPRITE_NOT_WHOLE_GAME_OBJECT"
        assert r["classification_confidence"] in ("LOW","MODERATE_BROAD_SHAPE","HIGH_ONLY_FOR_COARSE_SHAPE")
        labels[i]=r
    assert sorted(labels)==list(range(481,641))
    verified_sheets={}
    for i in range(1,5):
        p=OUT/("V18_NEW_SOURCE_CONTACT_%02d.png"%i)
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        assert actual==stage["contact_sheet_sha256"][str(i)],("sheet CRC/hash mismatch",i)
        verified_sheets[i]=actual

    basehash=hashlib.sha256(BASE.read_bytes()).hexdigest()
    with zipfile.ZipFile(BASE) as z:
        assert z.testzip() is None
        with z.open("B42_FURNITURE_MASTER_INVENTORY_V17.sqlite") as original, DB.open("wb") as dest:
            shutil.copyfileobj(original,dest)
    con=sqlite3.connect(DB);con.row_factory=sqlite3.Row
    assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    expect={
      "source_attributes":195265,"source_slots":73644,"registry_entry":2231,
      "wiki_furniture":1268,"furniture_tile":8219,"v12_template_proof":3840,
      "v13_warning_case":474,"v13_storage_link":1855,
      "v14_source_only_ledger":963,"v15_visual_part_observation":160,
      "v16_visual_part_observation":160,"v17_visual_part_observation":160,
      "v17_master_furniture_registry":2231,"v17_source_only_review_coverage":963,
      "v17_next_unreviewed_source_queue":483
    }
    for table,n in expect.items():assert ct(con,table)==n,(table,ct(con,table),n)
    prior_v15=qr(con,"SELECT entry_id,group_id,observed_broad_part_class AS broad_class FROM v15_visual_part_observation")
    prior_v16=qr(con,"SELECT entry_id,source_group_id AS group_id,broad_visual_shape_class AS broad_class FROM v16_visual_part_observation")
    prior_v17=qr(con,"SELECT entry_id,source_group_id AS group_id,broad_visual_shape_class AS broad_class FROM v17_visual_part_observation")
    prior=prior_v15+prior_v16+prior_v17
    prior_ids={r["entry_id"] for r in prior}
    prior_groups={r["group_id"] for r in prior}
    assert len(prior_ids)==480 and len(prior_groups)==480
    source={r["entry_id"]:r for r in qr(con,"SELECT * FROM v14_source_only_ledger")}
    assert len(source)==963

    con.executescript("""
    CREATE TABLE v18_visual_part_observation(
      sample_index INTEGER PRIMARY KEY, entry_id TEXT, source_group_id TEXT, source_key TEXT,
      original_name TEXT, original_png_path TEXT, original_png_sha256 TEXT,
      original_crop_pixel_sha256 TEXT, contact_sheet_number INTEGER,contact_sheet_sha256 TEXT,
      visible_broad_shape TEXT, broad_shape_confidence TEXT, evidence_scope TEXT,
      directly_viewed_original_one_sprite INTEGER NOT NULL DEFAULT 1,
      entire_furniture_assembled_and_verified INTEGER NOT NULL DEFAULT 0,
      same_game_object_across_facings_certified INTEGER NOT NULL DEFAULT 0,
      game_identity_certified INTEGER NOT NULL DEFAULT 0);
    CREATE UNIQUE INDEX v18_review_unique_group ON v18_visual_part_observation(source_group_id);
    CREATE TABLE v18_master_furniture_registry AS SELECT * FROM v17_master_furniture_registry;
    CREATE UNIQUE INDEX v18_master_entry ON v18_master_furniture_registry(entry_id);
    CREATE TABLE v18_source_only_review_coverage AS SELECT * FROM v17_source_only_review_coverage;
    CREATE UNIQUE INDEX v18_coverage_entry ON v18_source_only_review_coverage(entry_id);
    CREATE TABLE v18_pending_source_only_queue (
      entry_id TEXT PRIMARY KEY, group_id TEXT, original_name TEXT,
      original_sprite_tile_count INTEGER, original_png_cell_mapping_present INTEGER,
      source_key TEXT, original_png_path TEXT, original_facing_templates INTEGER,
      geometric_rectangle_candidate_templates INTEGER,
      raw_container_types_json TEXT, raw_capacity_values_json TEXT,
      review_status TEXT NOT NULL DEFAULT 'SINGLE_SOURCE_SPRITE_NOT_YET_VISUALLY_INSPECTED',
      game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE v18_progress_metric(
      metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,percent REAL,
      meaning TEXT, evidence_grade TEXT);
    """)
    reviewed=[]
    new_ids=set()
    new_groups=set()
    for row in crops:
        i=int(row["sample_index"])
        assert i in labels
        label=labels[i]
        eid=row["entry_id"]
        assert eid in source and eid not in prior_ids and eid not in new_ids
        group=row["group_id"]
        assert group==source[eid]["group_id"] and group not in prior_groups and group not in new_groups
        assert row["crop_status"]=="OK"
        assert row["prior_v15_v16_v17_review_overlap"]=="0"
        assert row["game_identity_certified"]=="0" and row["visually_inspected"]=="0"
        assert row["source_key"]==source[eid]["original_png_tile_key"]
        assert row["png_path"]==source[eid]["original_png_path"]
        assert len(row["crop_pixel_sha256"])==64 and len(row["png_sha256"])==64
        sheet=(i-481)//40+1
        rec=dict(sample_index=i,entry_id=eid,source_group_id=group,source_key=row["source_key"],
                 original_name=source[eid]["original_name"],original_png_path=row["png_path"],
                 original_png_sha256=row["png_sha256"],original_crop_pixel_sha256=row["crop_pixel_sha256"],
                 contact_sheet_number=sheet,contact_sheet_sha256=verified_sheets[sheet],
                 visible_broad_shape=label["observed_broad_class"],
                 broad_shape_confidence=label["classification_confidence"],
                 evidence_scope=label["observation_scope"])
        put(con,"v18_visual_part_observation",rec)
        con.execute("""UPDATE v18_master_furniture_registry
         SET direct_1cell_source_image_visual_review_rows=1, direct_1cell_visual_broad_class=?,
             review_scope_status='ONE_RAW_TILE_VISUAL_REVIEWED_NOT_WHOLE_FURNITURE'
         WHERE entry_id=? AND direct_1cell_source_image_visual_review_rows=0""",
         (label["observed_broad_class"],eid))
        assert con.execute("SELECT changes()").fetchone()[0]==1,("master",eid)
        con.execute("""UPDATE v18_source_only_review_coverage
         SET direct_one_cell_visual_reviewed=1,first_direct_visual_review_version='v18',
             broad_visible_shape=?
         WHERE entry_id=? AND direct_one_cell_visual_reviewed=0""",
         (label["observed_broad_class"],eid))
        assert con.execute("SELECT changes()").fetchone()[0]==1,("coverage",eid)
        new_ids.add(eid);new_groups.add(group);reviewed.append(rec)
    assert len(new_ids)==160 and len(new_groups)==160
    assert ct(con,"v18_master_furniture_registry")==2231
    assert ct(con,"v18_source_only_review_coverage")==963
    assert con.execute("SELECT SUM(direct_one_cell_visual_reviewed) FROM v18_source_only_review_coverage").fetchone()[0]==640
    assert con.execute("SELECT SUM(direct_1cell_source_image_visual_review_rows) FROM v18_master_furniture_registry").fetchone()[0]==640

    pending=[]
    for rec in qr(con,"SELECT entry_id FROM v18_source_only_review_coverage WHERE direct_one_cell_visual_reviewed=0 ORDER BY entry_id"):
        s=source[rec["entry_id"]]
        item=dict(entry_id=rec["entry_id"],group_id=s["group_id"],original_name=s["original_name"],
            original_sprite_tile_count=s["original_tile_count"],
            original_png_cell_mapping_present=s["image_mapping_present"],
            source_key=s["original_png_tile_key"],original_png_path=s["original_png_path"],
            original_facing_templates=s["direction_templates"],
            geometric_rectangle_candidate_templates=s["geometrically_rectangular_candidates"],
            raw_container_types_json=s["container_types_raw_json"],
            raw_capacity_values_json=s["capacity_raw_json"])
        put(con,"v18_pending_source_only_queue",item);pending.append(item)
    assert len(pending)==323
    image_mapped_remaining=sum(int(r["original_png_cell_mapping_present"]) for r in pending)
    all_class=Counter(r["broad_class"] for r in prior)
    all_class.update(r["visible_broad_shape"] for r in reviewed)
    new_class=Counter(r["visible_broad_shape"] for r in reviewed)
    assert sum(all_class.values())==640 and sum(new_class.values())==160

    metrics=[
     ("registered_current_candidate_rows",2231,2231,"Current source+Wiki candidate rows; NOT unique furniture found in full game","REGISTRY_ONLY"),
     ("registered_wiki_reference_rows",1268,1268,"Wiki may be stale/incomplete","REFERENCE_ONLY"),
     ("wiki_source_image_ID_matched_rows",1257,1268,"Exact Wiki image ID crosswalk, not official object identity","SOURCE_ID_LINK"),
     ("registered_source_only_candidate_groups",963,963,"No exact Wiki image ID crosswalk; NOT proof page missing","SOURCE_GROUP"),
     ("direct_one_original_sprite_image_reviewed",640,963,"One original PNG sprite each from distinct TileDef source-only groups","DIRECT_SINGLE_SPRITE"),
     ("remaining_source_only_groups_unreviewed",0,323,"323 source groups not yet single-image reviewed","PENDING"),
     ("original_tile_ID_provenance",8219,8219,"TileDef tile keys preserved","SOURCE_RAW"),
     ("source_directional_geometry",3840,3840,"Candidate group×Facing geometry, not object verification","GEOMETRIC"),
     ("original_storage_evidence_links",1855,1855,"TileDef storage links, not Lua loot contents","SOURCE_RAW"),
     ("original_warning_cases_resolved",0,474,"All original 474 warnings remain unverified","UNRESOLVED"),
     ("actual_game_object_identity_certified",0,0,"Ground-truth count unknown; no percent","UNVERIFIED")
    ]
    metric_rows=[]
    for key,n,den,meaning,grade in metrics:
        item=dict(metric_key=key,numerator=n,denominator=den,percent=round(100*n/den,2) if den else None,
                  meaning=meaning,evidence_grade=grade)
        put(con,"v18_progress_metric",item);metric_rows.append(item)
    con.commit()
    assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    assert not con.execute("PRAGMA foreign_key_check").fetchall()
    for table,n in {**expect,"v18_visual_part_observation":160,
       "v18_master_furniture_registry":2231,"v18_source_only_review_coverage":963,
       "v18_pending_source_only_queue":323,"v18_progress_metric":len(metrics)}.items():
        assert ct(con,table)==n,(table,ct(con,table),n)
    assert con.execute("""SELECT COUNT(*) FROM v18_visual_part_observation WHERE
     entire_furniture_assembled_and_verified!=0 OR same_game_object_across_facings_certified!=0
     OR game_identity_certified!=0""").fetchone()[0]==0
    master=qr(con,"SELECT * FROM v18_master_furniture_registry ORDER BY entry_id")
    coverage=qr(con,"SELECT * FROM v18_source_only_review_coverage ORDER BY entry_id")
    con.close()

    export("V18_160_DIRECT_ORIGINAL_SPRITE_VISUAL_OBSERVATIONS.csv",reviewed)
    export("V18_2231_MASTER_CANDIDATE_CATALOG.csv",master)
    export("V18_963_PER_GROUP_VISUAL_REVIEW_STATUS.csv",coverage)
    export("V18_323_UNREVIEWED_SOURCE_CANDIDATE_QUEUE.csv",pending)
    export("V18_640_COMBINED_BROAD_VISUAL_PART_COUNTS.csv",[
      dict(broad_visual_part_class=k,visually_reviewed_one_sprite_groups=n,
           assembled_furniture_game_objects_certified=0) for k,n in sorted(all_class.items())])
    export("V18_11_SCOPED_PROGRESS.csv",metric_rows)

    manifest=dict(version="v18",base_v17_zip_sha256=basehash,
      raw_TileDef_property_rows=195265,original_source_slots=73644,
      currently_registered_candidate_rows=2231,wiki_reference_rows=1268,
      wiki_image_source_id_linked_rows=1257,wiki_unlinked_reference_rows=11,
      source_only_candidate_groups=963,original_furniture_candidate_tile_keys=8219,
      directional_geometry_templates=3840,original_storage_evidence_links=1855,
      v15_viewed_one_sprite_groups=160,v16_viewed_one_sprite_groups=160,
      v17_viewed_one_sprite_groups=160,v18_new_direct_one_sprite_groups=160,
      unique_direct_one_sprite_reviewed_source_only_groups=640,
      direct_one_sprite_review_coverage_percent=round(640/963*100,2),
      source_only_groups_pending_visual_review=323,
      pending_groups_with_original_png_cell=image_mapped_remaining,
      pending_groups_without_original_png_cell=323-image_mapped_remaining,
      broad_class_counts_new=dict(sorted(new_class.items())),
      broad_class_counts_total=dict(sorted(all_class.items())),
      prior_Work_107_groups_574_tiles_report_only_no_individual_group_IDs=True,
      prior_Work_reported_groups=107,prior_Work_reported_tiles=574,
      prior_129_duplicate_group_visual_review_reference=129,
      maximum_unique_if_all_Work_groups_disjoint=747,
      work_disjoint_upper_percent=round(747/963*100,2),
      game_object_identity_certified=0,
      assembled_entire_furniture_verified=0,
      four_facing_same_object_certified=0,
      old_original_warnings_unresolved=474,
      wiki_is_fallible_reference=True,
      lua_loot_TMX_minecraft_not_started=True,
      sqlite_integrity="ok",zip_crc="ok")
    (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    (OUT/"README_KO.md").write_text(
      "# B42 가구 DB v18 — 원본 PNG 실검수 640 / 963, 전체 수집 후보 2,231행\n\n"
      "원본 TileDef/PNG를 우선하며 위키는 누락되거나 오래됐을 수 있는 참고 자료입니다.\n"
      "v15~v17 480개의 서로 다른 원본 전용 그룹에 더해 v18 신규 160개 그룹의 원본 단일 PNG를 직접 보고 광의 형태를 기록했습니다.\n"
      "직접 확인한 원본 그룹 640/963(66.46%), 남은 323개입니다. 이미지가 없는 후보와 여러 방향/부품은 별개 검증이 필요합니다.\n"
      "후보 목록 2,231행을 모두 등록한 것은 **현재 수집한 후보 행 등록률 100%**이지 게임 가구 목록 100% 확정이 아닙니다.\n"
      "한 스프라이트의 시각적 외형을 본 것은 가구 완전체 조립, 4방향 동일 오브젝트, 실제 게임 오브젝트 ID 인증을 의미하지 않습니다.\n"
      "Work의 107그룹/574타일 열람 보고는 개별 그룹 ID가 없어 검증된 640개와 중복 제거·합산하지 않았습니다.\n"
      "이전 중복 그룹 이미지 검수 참조 129개, 원본 경고 474개, 기존 원본 속성 195,265건을 유지합니다.\n"
      "Lua loot/TMX 배치/마인크래프트 가구 구현은 계속 보류합니다.\n",encoding="utf8")
    with zipfile.ZipFile(PACKAGE,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
        for f in sorted(OUT.iterdir()):
            if (f.is_file() and f!=PACKAGE and not f.name.startswith("STAGED_") and
                not f.name.startswith("_v18_required") and not f.name.endswith("_BASE64.txt")):
                z.write(f,f.name)
    with zipfile.ZipFile(PACKAGE) as z:
        assert z.testzip() is None and DB.name in z.namelist()
    print("V18_2231_CATALOG_640_DISJOINT_DIRECT_SPRITE_REVIEW_SQLITE_ZIP_VERIFIED",dump(manifest),flush=True)

if __name__=="__main__":
    main()
