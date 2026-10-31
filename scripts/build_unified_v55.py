#!/usr/bin/env python3
"""Build a single SHA-reproducible v55 SQLite from untouched v54 and new 48 visual records."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
m52=json.loads((ROOT/"analysis/current/v54/MANIFEST.json").read_text("utf8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)==m52["sqlite_sha256"],"Source v54 SHA256 mismatch"
with sqlite3.connect(src) as c:
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0]==2850
 assert c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0]==2491
with (ROOT/"checkpoints/v55/observations.tsv").open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({(r["tile_set_locator"],int(r["local_id"])) for r in rows})==48
assert sum(r["review_status"]=="candidate" for r in rows)==35
assert sum(r["review_status"]=="held" for r in rows)==13
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
dst=Path(os.environ.get("RUNNER_TEMP","/tmp"))/"tile_visual_v55_unified.sqlite"
if dst.exists():dst.unlink()
with sqlite3.connect(src) as before,sqlite3.connect(dst) as c:before.backup(c)
with sqlite3.connect(dst) as c:
 c.execute("PRAGMA journal_mode=DELETE")
 for field in ("v55_observed","v55_candidate_auditable"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} INTEGER NOT NULL DEFAULT 0")
 for field in ("v55_review_status","v55_identity_candidate","v55_observed_features"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} TEXT")
 cols=list(rows[0])
 numerics={"local_id","level","x","y","visible_pixel_delta","missing_png_neighbors","mapping_verified","tilezed_verified","final_certified"}
 schema=",".join('"'+x+'" '+("INTEGER" if x in numerics else "TEXT") for x in cols)
 c.execute("CREATE TABLE v55_visual_review("+schema+",PRIMARY KEY(tile_set_locator,local_id))")
 sql="INSERT INTO v55_visual_review VALUES("+",".join("?" for _ in cols)+")"
 for r in rows:
  key=(r["tile_set_locator"],int(r["local_id"]))
  prev=c.execute("SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?",key).fetchone()
  assert prev==(0,),f"Overlap/unknown key: {key}, {prev}"
  c.execute(sql,[int(r[x]) if x in numerics else r[x] for x in cols])
  candidate=int(r["review_status"]=="candidate")
  c.execute("""UPDATE tile_catalog SET observed_any=1,v55_observed=1,
       provisional_candidate_any_auditable=?,v55_candidate_auditable=?,v55_review_status=?,
       v55_identity_candidate=?,v55_observed_features=?,current_candidate=?,current_review_version='v55'
       WHERE tile_set_locator=? AND local_id=?""",
       (candidate,candidate,r["review_status"],r["identity_candidate"],r["observed_features"],r["identity_candidate"],*key))
 progress=[("v55_new_observed",48,"direct A/B/C/D reviewed"),
           ("v55_new_candidates",35,"provisional only"),("v55_new_held",13,"uncertain"),
           ("v55_total_observed",2898,"2850 + 48, no overlap"),
           ("v55_unobserved",2511,"5409-2898"),
           ("v55_candidate_auditable",2526,"2491+35")]
 c.executemany("INSERT INTO progress_snapshot VALUES (?,?,?)",progress)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 checks={"all":c.execute("select count(*) from tile_catalog").fetchone()[0],
         "observed":c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0],
         "candidate":c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0],
         "remaining":c.execute("select count(*) from analysis_queue").fetchone()[0],
         "v55review":c.execute("select count(*) from v55_visual_review").fetchone()[0],
         "final":c.execute("select count(*) from tile_catalog where identity_final_certified=1").fetchone()[0]}
 assert checks=={"all":5409,"observed":2898,"candidate":2526,"remaining":2511,"v55review":48,"final":0},checks
 c.execute("VACUUM")
out=ROOT/"analysis/current/v55";out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode("ascii")
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f"analysis/current/v55/v55.part{i//3000000:03}.b64"
 (ROOT/rel).write_text(encoded[i:i+3000000]+"\n","ascii")
 parts.append(rel)
manifest={"version":"v55","sqlite_file":"tile_visual_v55_unified.sqlite","sqlite_size_bytes":len(raw),
 "sqlite_sha256":hashlib.sha256(raw).hexdigest(),"compressed_sha256":hashlib.sha256(packed).hexdigest(),
 "compression":"zlib_base64","parts":parts,"base_version":"v54",
 "base_sqlite_sha256":m52["sqlite_sha256"],"new_records_repo_path":"checkpoints/v55/observations.tsv",
 "source_record_count":48,"observed":2898,"provisional_candidates":2526,
 "remaining":2511,"certified":0,"original_v36_v46_v47_v48_v52_v54_tables_preserved":True,
 "original_sprite_evidence_images_in_github":False,
 "note":"v55 GitHub TSV column set integrated; extra local v55 audit fields are retained in the conversation checkpoint ZIP"}
(out/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
statepath=ROOT/"PROJECT_STATE.json";s=json.loads(statepath.read_text("utf8"))
assert s["unified_database"]["version"]=="v54" and s["unified_database"]["observed_unique"]==2850
s["latest_checkpoint"]={"version":"v55","date":"2026-10-25","baseline_reconciliation":"v54",
 "baseline_unique_observed":2850,"new_unique_observed":48,"new_provisional_candidates":35,
 "new_held":13,"overlap_with_prior":0,"merged_unique_observed":2898,
 "merged_observation_percent":53.5774,"remaining_unobserved":2511,
 "auditable_provisional_candidate_keys":2526,"approved_final_certifications":0,
 "delta_repo_path":"checkpoints/v55/observations.tsv",
 "verification_script":"checkpoints/v55/verify_delta.py",
 "png_tmx_mapping_verified":0,"tilezed_verified":0,
 "high_resolution_evidence_images_in_conversation_zip_not_github":True}
s["unified_database"]={"version":"v55","status":"VERIFIED",
 "repo_manifest":"analysis/current/v55/MANIFEST.json",
 "restore_script":"scripts/restore_unified_v55.py","observed_unique":2898,
 "observed_percent":53.5774,"remaining_unobserved":2511,
 "auditable_candidates":2526,"certified":0,"sqlite_sha256":manifest["sqlite_sha256"],
 "complete_v36_tables":True,"complete_v46_tables":True,
 "v47_v48_v54_tables_preserved":True,"v55_git_checkpoint_integrated":True,
 "v55_extra_local_metadata_in_external_checkpoint":True,"image_binaries_in_github":False}
s["next_actions"]=[
 "v55 기준 미관찰 2,511종을 대상으로 원본 PNG 및 TMX의 A/B/C/D 시각 검수를 계속한다.",
 "사용자가 제출한 수동 검수 80종은 이번 신규 48종과 중복 없이 보존 중이다. 수동80 재검수 4종의 표현 수정 의견을 반영할지 확인하기 전까지 별도 계보로 유지한다.",
 "v55에서 판독 보류한 13종의 다른 장면·PNG 아틀라스 대응을 추가 확인한다.",
 "원본 v36·v46과 v54 이하 SQLite를 보존하고 새 통합 버전만 생성한다.",
 "v55 고해상도 증거판 48종은 이 채팅의 보존용 ZIP에 있으며 GitHub TSV에는 이미지를 내장하지 않았다."
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BUILT v55, verified",checks,"SHA256",manifest["sqlite_sha256"],"parts",len(parts))
