#!/usr/bin/env python3
"""Build a single SHA-reproducible v54 SQLite from untouched v53 and new 50 visual records."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
m52=json.loads((ROOT/"analysis/current/v53/MANIFEST.json").read_text("utf8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)==m52["sqlite_sha256"],"Source v53 SHA256 mismatch"
with sqlite3.connect(src) as c:
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0]==2800
 assert c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0]==2458
with (ROOT/"checkpoints/v54/observations.tsv").open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({(r["tile_set_locator"],int(r["local_id"])) for r in rows})==50
assert sum(r["review_status"]=="candidate" for r in rows)==33
assert sum(r["review_status"]=="held" for r in rows)==17
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
dst=Path(os.environ.get("RUNNER_TEMP","/tmp"))/"tile_visual_v54_unified.sqlite"
if dst.exists():dst.unlink()
with sqlite3.connect(src) as before,sqlite3.connect(dst) as c:before.backup(c)
with sqlite3.connect(dst) as c:
 c.execute("PRAGMA journal_mode=DELETE")
 for field in ("v54_observed","v54_candidate_auditable"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} INTEGER NOT NULL DEFAULT 0")
 for field in ("v54_review_status","v54_identity_candidate","v54_observed_features"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} TEXT")
 cols=list(rows[0])
 numerics={"local_id","level","x","y","visible_pixel_delta","missing_png_neighbors","mapping_verified","tilezed_verified","final_certified"}
 schema=",".join('"'+x+'" '+("INTEGER" if x in numerics else "TEXT") for x in cols)
 c.execute("CREATE TABLE v54_visual_review("+schema+",PRIMARY KEY(tile_set_locator,local_id))")
 sql="INSERT INTO v54_visual_review VALUES("+",".join("?" for _ in cols)+")"
 for r in rows:
  key=(r["tile_set_locator"],int(r["local_id"]))
  prev=c.execute("SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?",key).fetchone()
  assert prev==(0,),f"Overlap/unknown key: {key}, {prev}"
  c.execute(sql,[int(r[x]) if x in numerics else r[x] for x in cols])
  candidate=int(r["review_status"]=="candidate")
  c.execute("""UPDATE tile_catalog SET observed_any=1,v54_observed=1,
       provisional_candidate_any_auditable=?,v54_candidate_auditable=?,v54_review_status=?,
       v54_identity_candidate=?,v54_observed_features=?,current_candidate=?,current_review_version='v54'
       WHERE tile_set_locator=? AND local_id=?""",
       (candidate,candidate,r["review_status"],r["identity_candidate"],r["observed_features"],r["identity_candidate"],*key))
 progress=[("v54_new_observed",50,"direct A/B/C/D reviewed"),
           ("v54_new_candidates",33,"provisional only"),("v54_new_held",17,"uncertain"),
           ("v54_total_observed",2850,"2800 + 50, no overlap"),
           ("v54_unobserved",2559,"5409-2850"),
           ("v54_candidate_auditable",2491,"2458+33")]
 c.executemany("INSERT INTO progress_snapshot VALUES (?,?,?)",progress)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 checks={"all":c.execute("select count(*) from tile_catalog").fetchone()[0],
         "observed":c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0],
         "candidate":c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0],
         "remaining":c.execute("select count(*) from analysis_queue").fetchone()[0],
         "v54review":c.execute("select count(*) from v54_visual_review").fetchone()[0],
         "final":c.execute("select count(*) from tile_catalog where identity_final_certified=1").fetchone()[0]}
 assert checks=={"all":5409,"observed":2850,"candidate":2491,"remaining":2559,"v54review":50,"final":0},checks
 c.execute("VACUUM")
out=ROOT/"analysis/current/v54";out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode("ascii")
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f"analysis/current/v54/v54.part{i//3000000:03}.b64"
 (ROOT/rel).write_text(encoded[i:i+3000000]+"\n","ascii")
 parts.append(rel)
manifest={"version":"v54","sqlite_file":"tile_visual_v54_unified.sqlite","sqlite_size_bytes":len(raw),
 "sqlite_sha256":hashlib.sha256(raw).hexdigest(),"compressed_sha256":hashlib.sha256(packed).hexdigest(),
 "compression":"zlib_base64","parts":parts,"base_version":"v53",
 "base_sqlite_sha256":m52["sqlite_sha256"],"new_records_repo_path":"checkpoints/v54/observations.tsv",
 "source_record_count":50,"observed":2850,"provisional_candidates":2491,
 "remaining":2559,"certified":0,"original_v36_v46_v47_v48_v52_v53_tables_preserved":True,
 "original_sprite_evidence_images_in_github":False,
 "note":"v54 GitHub TSV column set integrated; extra local v54 audit fields are retained in the conversation checkpoint ZIP"}
(out/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
statepath=ROOT/"PROJECT_STATE.json";s=json.loads(statepath.read_text("utf8"))
assert s["unified_database"]["version"]=="v53" and s["unified_database"]["observed_unique"]==2800
s["latest_checkpoint"]={"version":"v54","date":"2026-10-25","baseline_reconciliation":"v53",
 "baseline_unique_observed":2800,"new_unique_observed":50,"new_provisional_candidates":33,
 "new_held":17,"overlap_with_prior":0,"merged_unique_observed":2850,
 "merged_observation_percent":52.6900,"remaining_unobserved":2559,
 "auditable_provisional_candidate_keys":2491,"approved_final_certifications":0,
 "delta_repo_path":"checkpoints/v54/observations.tsv",
 "verification_script":"checkpoints/v54/verify_delta.py",
 "png_tmx_mapping_verified":0,"tilezed_verified":0,
 "high_resolution_evidence_images_in_conversation_zip_not_github":True}
s["unified_database"]={"version":"v54","status":"VERIFIED",
 "repo_manifest":"analysis/current/v54/MANIFEST.json",
 "restore_script":"scripts/restore_unified_v54.py","observed_unique":2850,
 "observed_percent":52.6900,"remaining_unobserved":2559,
 "auditable_candidates":2491,"certified":0,"sqlite_sha256":manifest["sqlite_sha256"],
 "complete_v36_tables":True,"complete_v46_tables":True,
 "v47_v48_v53_tables_preserved":True,"v54_git_checkpoint_integrated":True,
 "v54_extra_local_metadata_in_external_checkpoint":True,"image_binaries_in_github":False}
s["next_actions"]=[
 "v54 최신 통합 SQLite의 미관찰 2,559종을 대상으로 원본 PNG와 TMX의 A/B/C/D 직접 관찰을 계속한다.",
 "v54에서 보류한 17종에 대해 다른 사용 위치 및 타일셋 PNG 버전을 재검토한다.",
 "v36·v46 기존 후보 표현 충돌 256종과 v36 후보 보고-감사 차이 135종을 유지한다.",
 "이전 원본 데이터와 v53 이하 SQLite를 삭제·덮어쓰지 않고 신규 버전을 별도 생성한다.",
 "v54 고해상도 증거판 50개는 별도 채팅 ZIP에 보존돼 있으며 GitHub 이미지 업로드로 표시하지 않는다."
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BUILT v54, verified",checks,"SHA256",manifest["sqlite_sha256"],"parts",len(parts))
