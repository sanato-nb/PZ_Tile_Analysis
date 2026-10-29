#!/usr/bin/env python3
"""v240: append-only physical unification of v196 5,409 + v238 4,633 source keys.
No status promotion; all original v196 tables are preserved by sqlite backup.
"""
import base64, csv, hashlib, json, os, sqlite3, tempfile, zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review/v240_unified_10042_2026-10-30"
DBOUT=ROOT/"analysis/current/v240"
OUT.mkdir(parents=True,exist_ok=True)
DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def readcsv(p):
    with open(ROOT/p,encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def writecsv(path, cols, rows):
    with open(path,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader();w.writerows(rows)
def key(name,local):return str(name)+"/"+str(int(local))
v196=json.loads((ROOT/"analysis/current/v196/MANIFEST.json").read_text("utf8"))
base64text="".join((ROOT/p).read_text("ascii").strip() for p in v196["parts"])
compressed=base64.b64decode(base64text,validate=True)
assert sha(compressed)==v196["compressed_sha256"],"v196 compressed hash mismatch"
originalbytes=zlib.decompress(compressed)
assert len(originalbytes)==v196["sqlite_bytes"] and sha(originalbytes)==v196["sqlite_sha256"],"v196 binary hash mismatch"
source=Path(tempfile.gettempdir())/"PZ_v240_source_v196_verified.sqlite"
source.write_bytes(originalbytes)
del originalbytes,base64text,compressed
parts=[f"review/v238_integrated_master_2026-10-29/MASTER_NEW_A_BC_{v}.csv" for v in
       ("0000_0879","0880_1679","1680_2479","2480_3279","3280_3839","3840_4319","4320_4632")]
modern=[r for p in parts for r in readcsv(p)]
assert len(modern)==4633
modernkeys={key(r["tile_set_name"],r["local_id"]) for r in modern}
assert len(modernkeys)==4633
assert {int(r["source_index"]) for r in modern}==set(range(4633))
held={key(r["tile_set_name"],r["local_id"]) for r in modern if r["integrated_status"]=="historical_held"}
assert len(held)==439
prioronly={key(r["tile_set_name"],r["local_id"]) for r in modern if r["integrated_status"]=="source_provisional_without_this_Afirst_note"}
missing={key(r["tile_set_name"],r["local_id"]) for r in modern if r["integrated_status"]=="source_missing_A_BC"}
assert len(prioronly)==8 and len(missing)==1 and len(modernkeys-held-prioronly-missing)==4185
manual=readcsv("review/v196_user_manual33/USER_UPLOADED_33_VERBATIM.csv")
assert len(manual)==33
manualmap={key(r["tile_set_name"],r["local_id"]):r for r in manual}
assert len(manualmap)==33
mexcluded={k for k,r in manualmap.items() if r["status"]=="미판정"}
assert len(mexcluded)==10
v113={key(r["tile_set_locator"],r["local_id"]) for r in readcsv("checkpoints/v113/user_review.csv") if r["user_action"]=="exclude_from_active_review"}
v116={key(r["tile_set_locator"],r["local_id"]) for r in readcsv("checkpoints/v116/user_exclude_six.csv") if r["user_action"]=="exclude_from_active_review"}
assert len(v113)==8 and len(v116)==6
assert v113.issubset(mexcluded)
assert len(v116 & (mexcluded|held))==0
excluded=held|mexcluded|v113|v116
assert len(excluded)==455,{"excluded":len(excluded)}
sourceDB=sqlite3.connect("file:"+str(source)+"?mode=ro",uri=True)
sourceDB.row_factory=sqlite3.Row
assert sourceDB.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
old_tables={r[0] for r in sourceDB.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
assert len(old_tables)==256, len(old_tables)
assert "tile_catalog" in old_tables
legacy=[dict(r) for r in sourceDB.execute("SELECT * FROM tile_catalog")]
assert len(legacy)==5409
legacykeys={key(r["tile_set_locator"],r["local_id"]) for r in legacy}
assert len(legacykeys)==5409 and not(legacykeys & modernkeys)
assert len(legacykeys|modernkeys)==10042
archived={key(r["tile_set_locator"],r["local_id"]) for r in readcsv("analysis/imports/merged_catalog_5409.csv")}
assert archived==legacykeys,"v196 legacy 5409 keys not equal historic source catalog"
assert set(manualmap).issubset(legacykeys|modernkeys)
assert (len(mexcluded&legacykeys),len(mexcluded&modernkeys))==(9,1)
assert v116.issubset(legacykeys)
# No rewrite of existing source tables; copy them into a new physical database.
target=Path(tempfile.gettempdir())/"PZ_v240_master_10042.sqlite"
if target.exists(): target.unlink()
with sqlite3.connect(target) as copy:
    sourceDB.backup(copy)
source_counts={name:sourceDB.execute('SELECT COUNT(*) FROM "'+name.replace('"','""')+'"').fetchone()[0] for name in old_tables}
sourceDB.close()
def exclusion(k):
    if k in mexcluded:return "USER_V196_MANUAL_UNDECIDED"
    if k in v116:return "USER_V116_PREVIOUS_EXCLUSION"
    if k in v113:return "USER_V113_PREVIOUS_EXCLUSION"
    if k in held:return "HISTORICAL_HELD_439"
    return ""
def cite(k):
    r=manualmap.get(k)
    return (r["status"],r["candidate"]) if r else ("","")
columns=["source_key","scope","tile_set_name","local_id","source_index","active_flag","active_exclusion_reason",
         "review_status","review_depth","image_observed_prior","object_identity_candidate",
         "A_visible_shape_note","A_original_source_png","A_rgba_sha256_prior",
         "B_original_TMX","B_level","B_layer_index","B_x","B_y","B_raw_gid","B_C_pixels_prior",
         "review_evidence_path","legacy_current_review_version","user_verdict_verbatim",
         "user_candidate_verbatim","prior_user_v113_excluded","prior_user_v116_excluded",
         "official_mapping_verified","tilezed_verified","certified","caution"]
outrows=[]
for x in legacy:
    k=key(x["tile_set_locator"],x["local_id"]);ms,mc=cite(k);ex=exclusion(k)
    outrows.append(dict(source_key=k,scope="legacy_5409",tile_set_name=x["tile_set_locator"],
        local_id=int(x["local_id"]),source_index="",active_flag=int(not ex),active_exclusion_reason=ex,
        review_status="legacy_v196_catalog_snapshot",review_depth="v196_physical_catalog_snapshot",
        image_observed_prior=x.get("observed_any",""),
        object_identity_candidate=x.get("current_candidate") or "",
        A_visible_shape_note="",A_original_source_png="",A_rgba_sha256_prior="",
        B_original_TMX="",B_level="",B_layer_index="",B_x="",B_y="",B_raw_gid="",B_C_pixels_prior="",
        review_evidence_path="analysis/current/v196/MANIFEST.json",
        legacy_current_review_version=x.get("current_review_version") or "",
        user_verdict_verbatim=ms,user_candidate_verbatim=mc,
        prior_user_v113_excluded=int(k in v113),prior_user_v116_excluded=int(k in v116),
        official_mapping_verified=0,tilezed_verified=0,certified=0,
        caution="Legacy v196 catalog + all 256 original tables preserved; no newly certified individual A/B/C identity"))
for x in modern:
    k=key(x["tile_set_name"],x["local_id"]);ms,mc=cite(k);ex=exclusion(k)
    outrows.append(dict(source_key=k,scope="new_4633",tile_set_name=x["tile_set_name"],
       local_id=int(x["local_id"]),source_index=int(x["source_index"]),active_flag=int(not ex),
       active_exclusion_reason=ex,review_status=x["integrated_status"],review_depth=x["review_quality_depth"],
       image_observed_prior="",object_identity_candidate=x["prior_identity_candidate"],
       A_visible_shape_note=x["A_visible_shape_note"],A_original_source_png=x["A_source_png"],
       A_rgba_sha256_prior=x["A_rgba_SHA256_prior"],
       B_original_TMX=x["B_original_TMX"],B_level=x["B_level"],B_layer_index=x["B_layer_index"],
       B_x=x["B_x"],B_y=x["B_y"],B_raw_gid=x["B_raw_gid"],
       B_C_pixels_prior=x["B_minus_C_pixels_prior"],
       review_evidence_path=x["held_source_file"] or x["QA_source_file"] or "review/v238_integrated_master_2026-10-29/",
       legacy_current_review_version="",user_verdict_verbatim=ms,user_candidate_verbatim=mc,
       prior_user_v113_excluded=int(k in v113),prior_user_v116_excluded=int(k in v116),
       official_mapping_verified=0,tilezed_verified=0,certified=0,
       caution="v185 other true TMX scene resolved missing-neighbour evidence; v238 old held remains excluded" if x["source_index"]=="3102"
       else ("No independent A-first pixel note" if k in prioronly else
             "Archive only, original A/B/C missing and user excluded" if k in missing else
             "Previous B/C approximate; A-first QA is provisional, not official mapping/identity certification")))
assert len(outrows)==10042 and len({x["source_key"] for x in outrows})==10042
assert sum(r["active_flag"] for r in outrows)==9587
assert sum(r["scope"]=="legacy_5409" for r in outrows)==5409
assert sum(r["scope"]=="new_4633" for r in outrows)==4633
assert sum(r["active_exclusion_reason"]=="HISTORICAL_HELD_439" for r in outrows)==439
assert sum(r["active_exclusion_reason"]=="USER_V196_MANUAL_UNDECIDED" for r in outrows)==10
assert sum(r["active_exclusion_reason"]=="USER_V116_PREVIOUS_EXCLUSION" for r in outrows)==6
outrows.sort(key=lambda r:(r["scope"]!="legacy_5409",r["tile_set_name"],r["local_id"]))
active=[r for r in outrows if r["active_flag"]]
inactive=[r for r in outrows if not r["active_flag"]]
writecsv(OUT/"MASTER_ALL_10042.csv",columns,outrows)
writecsv(OUT/"ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv",columns,active)
writecsv(OUT/"EXCLUDED_ARCHIVE_455.csv",columns,inactive)
con=sqlite3.connect(target)
con.execute("PRAGMA journal_mode=DELETE")
coltypes={"local_id":"INTEGER","source_index":"INTEGER","active_flag":"INTEGER","image_observed_prior":"INTEGER",
          "B_level":"INTEGER","B_layer_index":"INTEGER","B_x":"INTEGER","B_y":"INTEGER","B_raw_gid":"INTEGER",
          "B_C_pixels_prior":"INTEGER","prior_user_v113_excluded":"INTEGER","prior_user_v116_excluded":"INTEGER",
          "official_mapping_verified":"INTEGER","tilezed_verified":"INTEGER","certified":"INTEGER"}
sqlcols=[('"'+c+'" '+coltypes.get(c,"TEXT")+(" PRIMARY KEY" if c=="source_key" else "")) for c in columns]
con.execute("CREATE TABLE v240_tile_master_10042 ("+",".join(sqlcols)+")")
ints=set(coltypes)
con.executemany("INSERT INTO v240_tile_master_10042 VALUES ("+",".join("?" for _ in columns)+")",
   [[(int(r[c]) if r[c]!="" else None) if c in ints else r[c] for c in columns] for r in outrows])
con.execute("""CREATE TABLE v240_excluded_archive_455 AS SELECT * FROM v240_tile_master_10042 WHERE active_flag=0""")
con.execute("""CREATE VIEW v240_active_tile_master AS SELECT * FROM v240_tile_master_10042 WHERE active_flag=1""")
con.execute("CREATE UNIQUE INDEX v240_idx_excluded_key ON v240_excluded_archive_455(source_key)")
con.execute("CREATE INDEX v240_idx_scope_status ON v240_tile_master_10042(scope,review_status,active_flag)")
con.commit()
assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
assert con.execute("SELECT COUNT(*) FROM v240_tile_master_10042").fetchone()[0]==10042
assert con.execute("SELECT COUNT(*) FROM v240_active_tile_master").fetchone()[0]==9587
assert con.execute("SELECT COUNT(*) FROM v240_excluded_archive_455").fetchone()[0]==455
new_tables={r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
assert old_tables.issubset(new_tables) and len(new_tables)==258
assert all(con.execute('SELECT COUNT(*) FROM "'+name.replace('"','""')+'"').fetchone()[0]==n for name,n in source_counts.items())
assert con.execute("SELECT COUNT(*) FROM tile_catalog").fetchone()[0]==5409
con.close()
raw=target.read_bytes()
packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode("ascii")
packedparts=[]
for n,start in enumerate(range(0,len(encoded),3000000)):
    path=DBOUT/("v240.part%03d.b64"%n)
    path.write_text(encoded[start:start+3000000]+"\n",encoding="ascii")
    packedparts.append(str(path.relative_to(ROOT)))
manifest={
 "version":"v240_full_physical_master_append_only","date":"2026-10-30",
 "original_v196_sha256":v196["sqlite_sha256"],"original_v196_tables":256,
 "v240_sqlite_sha256":sha(raw),"v240_sqlite_bytes":len(raw),"v240_zlib_sha256":sha(packed),
 "v240_parts":packedparts,"v240_sqlite_tables":258,"integrity_check":"ok",
 "legacy_source_keys":5409,"new_source_keys":4633,"integrated_total_unique":10042,
 "excluded_held_439":439,"excluded_user_v196_10":10,"excluded_other_v116_6":6,
 "user_v113_8_overlap_v196_10":8,"excluded_total_unique":455,"active_total":9587,
 "new_source_status":{"A_first_QA_provisional":4185,"held":439,"prior_only_A_note_missing":8,"source_missing_A_BC":1},
 "historical_provisional_image_observations_v196":10007,
 "historical_image_observation_rate_percent":10007/10042*100,
 "official_mapping_verified":0,"tilezed_verified":0,"identity_certified":0,
 "manual_user33_all_preserved":True,"source_png_tmx_and_legacy_256_tables_untouched":True,
 "source_hash_checked":True,"legacy_table_row_counts_before_after_equal":True,
 "original_TMX_rerendered_this_round":False,"individual_A_new_visual_certifications":0,
 "v185_index3102_conflict":"older representative scene remains held; verified alternative scene v185 has zero missing neighbours and candidate, preserved as caution, excluded under held439 until state reconciliation",
 "active_flag_not_map_ready":True,
 "output_all":"review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv",
 "output_active":"review/v240_unified_10042_2026-10-30/ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv",
 "output_archived":"review/v240_unified_10042_2026-10-30/EXCLUDED_ARCHIVE_455.csv"
}
(OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(DBOUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(OUT/"README.md").write_text(
"# v240: 기존 5,409 + 신규 4,633 = 전체 10,042종 실제 물리 통합\n\n"
"원본 v196 물리 SQLite 256테이블 전체를 SHA-256/PRAGMA로 확인하고 백업 복제한 뒤, 새 마스터·활성·보류 아카이브를 추가했다. 기존 테이블 삭제/수정 없음.\n\n"
"| 항목 | 고유키 |\n|---|---:|\n| 전체 마스터 | 10,042 |\n| 기존 v196 | 5,409 |\n| 신규 v238 | 4,633 |\n| 과거 보류(활성 제외) | 439 |\n| v196 사용자 미판정(활성 제외) | 10 |\n| 이전 v116 사용자 제외(추가로 활성 제외) | 6 |\n| **활성 목록 합계** | **9,587** |\n| 제외 아카이브 합계 | 455 |\n\n"
"과거 v113 사용자 제외 8종은 v196 미판정 10종과 겹치므로 두 번 빼지 않았다. "
"**활성 = 지금 읽고 활용할 수 있는 잠정 레코드이며, 정체가 확정됐거나 마인크래프트 변환을 승인했다는 뜻이 아니다.** "
"신규 4,185 QA 중 개별 설명 누락 232, 추가 8종은 독립 A 메모 없음. "
"원본 A/B/C가 없는 사용자 미판정 1종은 그대로 제외.\n\n"
"파일: MASTER_ALL_10042.csv(누락 없이 모두), ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv(활성만), "
"EXCLUDED_ARCHIVE_455.csv(과거 제외 원문과 상태 보존). "
"물리 SQLite는 analysis/current/v240/MANIFEST.json의 zlib+base64 파트들을 이어 복원한다.\n\n"
"이 통합은 과거 실제 검수 결과를 소스키로 병합한 작업이고, 새 원본 이미지 판독·TMX 레이어별 B/C 렌더·공식 TileZed 인증은 실행하지 않았다. "
"최종 정체 인증 0. "
"3102는 v185에서 다른 진짜 TMX 위치로 이웃 PNG 누락을 해소했으나 v238의 원 대표 보류를 기록대로 유지하고 이번 활성 제외 적용.\n",
encoding="utf8")
print("PASS v240 10042 total / 9587 active / 455 inactive / 258 tables / PRAGMA ok; sha "+sha(raw)+"; chunks "+str(len(packedparts)),flush=True)
