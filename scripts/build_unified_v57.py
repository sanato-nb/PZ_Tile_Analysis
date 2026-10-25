#!/usr/bin/env python3
"""Build a single SHA-reproducible v57 SQLite from untouched v56 and new 48 visual records."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
m52=json.loads((ROOT/"analysis/current/v56/MANIFEST.json").read_text("utf8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)==m52["sqlite_sha256"],"Source v56 SHA256 mismatch"
with sqlite3.connect(src) as c:
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0]==2946
 assert c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0]==2559
with (ROOT/"checkpoints/v57/observations.tsv").open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({(r["tile_set_locator"],int(r["local_id"])) for r in rows})==48
assert sum(r["review_status"]=="candidate" for r in rows)==37
assert sum(r["review_status"]=="held" for r in rows)==11
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
dst=Path(os.environ.get("RUNNER_TEMP","/tmp"))/"tile_visual_v57_unified.sqlite"
if dst.exists():dst.unlink()
with sqlite3.connect(src) as before,sqlite3.connect(dst) as c:before.backup(c)
with sqlite3.connect(dst) as c:
 c.execute("PRAGMA journal_mode=DELETE")
 for field in ("v57_observed","v57_candidate_auditable"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} INTEGER NOT NULL DEFAULT 0")
 for field in ("v57_review_status","v57_identity_candidate","v57_observed_features"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} TEXT")
 cols=list(rows[0])
 numerics={"local_id","level","x","y","visible_pixel_delta","missing_png_neighbors","mapping_verified","tilezed_verified","final_certified"}
 schema=",".join('"'+x+'" '+("INTEGER" if x in numerics else "TEXT") for x in cols)
 c.execute("CREATE TABLE v57_visual_review("+schema+",PRIMARY KEY(tile_set_locator,local_id))")
 sql="INSERT INTO v57_visual_review VALUES("+",".join("?" for _ in cols)+")"
 for r in rows:
  key=(r["tile_set_locator"],int(r["local_id"]))
  prev=c.execute("SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?",key).fetchone()
  assert prev==(0,),f"Overlap/unknown key: {key}, {prev}"
  c.execute(sql,[int(r[x]) if x in numerics else r[x] for x in cols])
  candidate=int(r["review_status"]=="candidate")
  c.execute("""UPDATE tile_catalog SET observed_any=1,v57_observed=1,
       provisional_candidate_any_auditable=?,v57_candidate_auditable=?,v57_review_status=?,
       v57_identity_candidate=?,v57_observed_features=?,current_candidate=?,current_review_version='v57'
       WHERE tile_set_locator=? AND local_id=?""",
       (candidate,candidate,r["review_status"],r["identity_candidate"],r["observed_features"],r["identity_candidate"],*key))
 progress=[("v57_new_observed",48,"direct A/B/C/D reviewed"),
           ("v57_new_candidates",37,"provisional only"),("v57_new_held",11,"uncertain"),
           ("v57_total_observed",2994,"2946 + 48, no overlap"),
           ("v57_unobserved",2415,"5409-2994"),
           ("v57_candidate_auditable",2596,"2559+37")]
 c.executemany("INSERT INTO progress_snapshot VALUES (?,?,?)",progress)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 checks={"all":c.execute("select count(*) from tile_catalog").fetchone()[0],
         "observed":c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0],
         "candidate":c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0],
         "remaining":c.execute("select count(*) from analysis_queue").fetchone()[0],
         "v57review":c.execute("select count(*) from v57_visual_review").fetchone()[0],
         "final":c.execute("select count(*) from tile_catalog where identity_final_certified=1").fetchone()[0]}
 assert checks=={"all":5409,"observed":2994,"candidate":2596,"remaining":2415,"v57review":48,"final":0},checks
 c.execute("VACUUM")
out=ROOT/"analysis/current/v57";out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode("ascii")
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f"analysis/current/v57/v57.part{i//3000000:03}.b64"
 (ROOT/rel).write_text(encoded[i:i+3000000]+"\n","ascii")
 parts.append(rel)
manifest={"version":"v57","sqlite_file":"tile_visual_v57_unified.sqlite","sqlite_size_bytes":len(raw),
 "sqlite_sha256":hashlib.sha256(raw).hexdigest(),"compressed_sha256":hashlib.sha256(packed).hexdigest(),
 "compression":"zlib_base64","parts":parts,"base_version":"v56",
 "base_sqlite_sha256":m52["sqlite_sha256"],"new_records_repo_path":"checkpoints/v57/observations.tsv",
 "source_record_count":48,"observed":2994,"provisional_candidates":2596,
 "remaining":2415,"certified":0,"original_v36_v46_v47_v48_v52_v56_tables_preserved":True,
 "original_sprite_evidence_images_in_github":False,
 "note":"v57 GitHub TSV column set integrated; extra local v57 audit fields are retained in the conversation checkpoint ZIP"}
(out/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
statepath=ROOT/"PROJECT_STATE.json";s=json.loads(statepath.read_text("utf8"))
assert s["unified_database"]["version"]=="v56" and s["unified_database"]["observed_unique"]==2946
s["latest_checkpoint"]={"version":"v57","date":"2026-10-25","baseline_reconciliation":"v56",
 "baseline_unique_observed":2946,"new_unique_observed":48,"new_provisional_candidates":37,
 "new_held":11,"overlap_with_prior":0,"merged_unique_observed":2994,
 "merged_observation_percent":55.3522,"remaining_unobserved":2415,
 "auditable_provisional_candidate_keys":2596,"approved_final_certifications":0,
 "delta_repo_path":"checkpoints/v57/observations.tsv",
 "verification_script":"checkpoints/v57/verify_delta.py",
 "png_tmx_mapping_verified":0,"tilezed_verified":0,
 "high_resolution_evidence_images_in_conversation_zip_not_github":True}
s["unified_database"]={"version":"v57","status":"VERIFIED",
 "repo_manifest":"analysis/current/v57/MANIFEST.json",
 "restore_script":"scripts/restore_unified_v57.py","observed_unique":2994,
 "observed_percent":55.3522,"remaining_unobserved":2415,
 "auditable_candidates":2596,"certified":0,"sqlite_sha256":manifest["sqlite_sha256"],
 "complete_v36_tables":True,"complete_v46_tables":True,
 "v47_v48_v56_tables_preserved":True,"v57_git_checkpoint_integrated":True,
 "v57_extra_local_metadata_in_external_checkpoint":True,"image_binaries_in_github":False}
s["next_actions"]=[
 "v57 통합 DB의 미관찰 2,415종을 대상으로 원본 PNG 및 TMX A/B/C/D 비교판 직접 검수를 계속한다.",
 "v57의 11종 보류 항목은 다른 배치와 세탁실 설비·TV·탁자 원본 대응을 추가 확인한다.",
 "사용자 수동 검수 80종과 재검수 원본은 공식 관찰 수에 합산하지 않고 보존한다.",
 "v56 이하 SQLite·v36·v46 원본과 각 체크포인트를 삭제하거나 덮어쓰지 않는다.",
 "v57 이미지 원본 증거 48개는 이번 채팅의 ZIP에 있으며 GitHub에 이미지 바이너리가 전부 들어 있다고 주장하지 않는다."
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BUILT v57, verified",checks,"SHA256",manifest["sqlite_sha256"],"parts",len(parts))
