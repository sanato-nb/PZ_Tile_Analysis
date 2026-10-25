#!/usr/bin/env python3
"""Build a single SHA-reproducible v53 SQLite from untouched v52 and new 50 visual records."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
m52=json.loads((ROOT/"analysis/current/v52/MANIFEST.json").read_text("utf8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)==m52["sqlite_sha256"],"Source v52 SHA256 mismatch"
with sqlite3.connect(src) as c:
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0]==2750
 assert c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0]==2419
with (ROOT/"checkpoints/v53/observations.tsv").open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({(r["tile_set_locator"],int(r["local_id"])) for r in rows})==50
assert sum(r["review_status"]=="candidate" for r in rows)==39
assert sum(r["review_status"]=="held" for r in rows)==11
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
dst=Path(os.environ.get("RUNNER_TEMP","/tmp"))/"tile_visual_v53_unified.sqlite"
if dst.exists():dst.unlink()
with sqlite3.connect(src) as before,sqlite3.connect(dst) as c:before.backup(c)
with sqlite3.connect(dst) as c:
 c.execute("PRAGMA journal_mode=DELETE")
 for field in ("v53_observed","v53_candidate_auditable"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} INTEGER NOT NULL DEFAULT 0")
 for field in ("v53_review_status","v53_identity_candidate","v53_observed_features"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} TEXT")
 cols=list(rows[0])
 numerics={"local_id","level","x","y","visible_pixel_delta","missing_png_neighbors","mapping_verified","tilezed_verified","final_certified"}
 schema=",".join('"'+x+'" '+("INTEGER" if x in numerics else "TEXT") for x in cols)
 c.execute("CREATE TABLE v53_visual_review("+schema+",PRIMARY KEY(tile_set_locator,local_id))")
 sql="INSERT INTO v53_visual_review VALUES("+",".join("?" for _ in cols)+")"
 for r in rows:
  key=(r["tile_set_locator"],int(r["local_id"]))
  prev=c.execute("SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?",key).fetchone()
  assert prev==(0,),f"Overlap/unknown key: {key}, {prev}"
  c.execute(sql,[int(r[x]) if x in numerics else r[x] for x in cols])
  candidate=int(r["review_status"]=="candidate")
  c.execute("""UPDATE tile_catalog SET observed_any=1,v53_observed=1,
       provisional_candidate_any_auditable=?,v53_candidate_auditable=?,v53_review_status=?,
       v53_identity_candidate=?,v53_observed_features=?,current_candidate=?,current_review_version='v53'
       WHERE tile_set_locator=? AND local_id=?""",
       (candidate,candidate,r["review_status"],r["identity_candidate"],r["observed_features"],r["identity_candidate"],*key))
 progress=[("v53_new_observed",50,"direct A/B/C/D reviewed"),
           ("v53_new_candidates",39,"provisional only"),("v53_new_held",11,"uncertain"),
           ("v53_total_observed",2800,"2750 + 50, no overlap"),
           ("v53_unobserved",2609,"5409-2800"),
           ("v53_candidate_auditable",2458,"2419+39")]
 c.executemany("INSERT INTO progress_snapshot VALUES (?,?,?)",progress)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 checks={"all":c.execute("select count(*) from tile_catalog").fetchone()[0],
         "observed":c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0],
         "candidate":c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0],
         "remaining":c.execute("select count(*) from analysis_queue").fetchone()[0],
         "v53review":c.execute("select count(*) from v53_visual_review").fetchone()[0],
         "final":c.execute("select count(*) from tile_catalog where identity_final_certified=1").fetchone()[0]}
 assert checks=={"all":5409,"observed":2800,"candidate":2458,"remaining":2609,"v53review":50,"final":0},checks
 c.execute("VACUUM")
out=ROOT/"analysis/current/v53";out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode("ascii")
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f"analysis/current/v53/v53.part{i//3000000:03}.b64"
 (ROOT/rel).write_text(encoded[i:i+3000000]+"\n","ascii")
 parts.append(rel)
manifest={"version":"v53","sqlite_file":"tile_visual_v53_unified.sqlite","sqlite_size_bytes":len(raw),
 "sqlite_sha256":hashlib.sha256(raw).hexdigest(),"compressed_sha256":hashlib.sha256(packed).hexdigest(),
 "compression":"zlib_base64","parts":parts,"base_version":"v52",
 "base_sqlite_sha256":m52["sqlite_sha256"],"new_records_repo_path":"checkpoints/v53/observations.tsv",
 "source_record_count":50,"observed":2800,"provisional_candidates":2458,
 "remaining":2609,"certified":0,"original_v36_v46_v47_v48_v52_tables_preserved":True,
 "original_sprite_evidence_images_in_github":False,
 "note":"v53 GitHub TSV column set integrated; extra local v53 audit fields are retained in the conversation checkpoint ZIP"}
(out/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
statepath=ROOT/"PROJECT_STATE.json";s=json.loads(statepath.read_text("utf8"))
assert s["unified_database"]["version"]=="v52" and s["unified_database"]["observed_unique"]==2750
s["latest_checkpoint"]={"version":"v53","date":"2026-10-11","baseline_reconciliation":"v52",
 "baseline_unique_observed":2750,"new_unique_observed":50,"new_provisional_candidates":39,
 "new_held":11,"overlap_with_prior":0,"merged_unique_observed":2800,
 "merged_observation_percent":51.7656,"remaining_unobserved":2609,
 "auditable_provisional_candidate_keys":2458,"approved_final_certifications":0,
 "delta_repo_path":"checkpoints/v53/observations.tsv",
 "verification_script":"checkpoints/v53/verify_delta.py",
 "png_tmx_mapping_verified":0,"tilezed_verified":0,
 "high_resolution_evidence_images_in_conversation_zip_not_github":True}
s["unified_database"]={"version":"v53","status":"VERIFIED",
 "repo_manifest":"analysis/current/v53/MANIFEST.json",
 "restore_script":"scripts/restore_unified_v53.py","observed_unique":2800,
 "observed_percent":51.7656,"remaining_unobserved":2609,
 "auditable_candidates":2458,"certified":0,"sqlite_sha256":manifest["sqlite_sha256"],
 "complete_v36_tables":True,"complete_v46_tables":True,
 "v47_v48_v52_tables_preserved":True,"v53_git_checkpoint_integrated":True,
 "v53_extra_local_metadata_in_external_checkpoint":True,"image_binaries_in_github":False}
s["next_actions"]=[
 "v53 최신 통합 SQLite의 미관찰 2,609종을 대상으로 원본 PNG와 TMX A/B/C/D 직접 관찰을 계속한다.",
 "v53에서 보류한 11종의 다른 사용 위치 및 PNG 버전 대응을 추가 검토한다.",
 "v36·v46 기존 후보 충돌 256종과 v36 후보 보고-감사 차이 135종을 계속 별도 보존한다.",
 "원본 DB 및 v52 이전 DB를 삭제·덮어쓰지 않고 새 버전 SQLite만 추가한다.",
 "고해상도 v53 증거판 50개는 채팅 ZIP에 있으며 GitHub에 이미지가 업로드됐다고 주장하지 않는다."
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BUILT v53, verified",checks,"SHA256",manifest["sqlite_sha256"],"parts",len(parts))
