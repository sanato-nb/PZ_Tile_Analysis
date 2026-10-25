#!/usr/bin/env python3
"""Build a single SHA-reproducible v56 SQLite from untouched v55 and new 48 visual records."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
m52=json.loads((ROOT/"analysis/current/v55/MANIFEST.json").read_text("utf8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)==m52["sqlite_sha256"],"Source v55 SHA256 mismatch"
with sqlite3.connect(src) as c:
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0]==2898
 assert c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0]==2526
with (ROOT/"checkpoints/v56/observations.tsv").open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({(r["tile_set_locator"],int(r["local_id"])) for r in rows})==48
assert sum(r["review_status"]=="candidate" for r in rows)==33
assert sum(r["review_status"]=="held" for r in rows)==15
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
dst=Path(os.environ.get("RUNNER_TEMP","/tmp"))/"tile_visual_v56_unified.sqlite"
if dst.exists():dst.unlink()
with sqlite3.connect(src) as before,sqlite3.connect(dst) as c:before.backup(c)
with sqlite3.connect(dst) as c:
 c.execute("PRAGMA journal_mode=DELETE")
 for field in ("v56_observed","v56_candidate_auditable"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} INTEGER NOT NULL DEFAULT 0")
 for field in ("v56_review_status","v56_identity_candidate","v56_observed_features"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} TEXT")
 cols=list(rows[0])
 numerics={"local_id","level","x","y","visible_pixel_delta","missing_png_neighbors","mapping_verified","tilezed_verified","final_certified"}
 schema=",".join('"'+x+'" '+("INTEGER" if x in numerics else "TEXT") for x in cols)
 c.execute("CREATE TABLE v56_visual_review("+schema+",PRIMARY KEY(tile_set_locator,local_id))")
 sql="INSERT INTO v56_visual_review VALUES("+",".join("?" for _ in cols)+")"
 for r in rows:
  key=(r["tile_set_locator"],int(r["local_id"]))
  prev=c.execute("SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?",key).fetchone()
  assert prev==(0,),f"Overlap/unknown key: {key}, {prev}"
  c.execute(sql,[int(r[x]) if x in numerics else r[x] for x in cols])
  candidate=int(r["review_status"]=="candidate")
  c.execute("""UPDATE tile_catalog SET observed_any=1,v56_observed=1,
       provisional_candidate_any_auditable=?,v56_candidate_auditable=?,v56_review_status=?,
       v56_identity_candidate=?,v56_observed_features=?,current_candidate=?,current_review_version='v56'
       WHERE tile_set_locator=? AND local_id=?""",
       (candidate,candidate,r["review_status"],r["identity_candidate"],r["observed_features"],r["identity_candidate"],*key))
 progress=[("v56_new_observed",48,"direct A/B/C/D reviewed"),
           ("v56_new_candidates",33,"provisional only"),("v56_new_held",15,"uncertain"),
           ("v56_total_observed",2946,"2898 + 48, no overlap"),
           ("v56_unobserved",2463,"5409-2946"),
           ("v56_candidate_auditable",2559,"2526+33")]
 c.executemany("INSERT INTO progress_snapshot VALUES (?,?,?)",progress)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 checks={"all":c.execute("select count(*) from tile_catalog").fetchone()[0],
         "observed":c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0],
         "candidate":c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0],
         "remaining":c.execute("select count(*) from analysis_queue").fetchone()[0],
         "v56review":c.execute("select count(*) from v56_visual_review").fetchone()[0],
         "final":c.execute("select count(*) from tile_catalog where identity_final_certified=1").fetchone()[0]}
 assert checks=={"all":5409,"observed":2946,"candidate":2559,"remaining":2463,"v56review":48,"final":0},checks
 c.execute("VACUUM")
out=ROOT/"analysis/current/v56";out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode("ascii")
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f"analysis/current/v56/v56.part{i//3000000:03}.b64"
 (ROOT/rel).write_text(encoded[i:i+3000000]+"\n","ascii")
 parts.append(rel)
manifest={"version":"v56","sqlite_file":"tile_visual_v56_unified.sqlite","sqlite_size_bytes":len(raw),
 "sqlite_sha256":hashlib.sha256(raw).hexdigest(),"compressed_sha256":hashlib.sha256(packed).hexdigest(),
 "compression":"zlib_base64","parts":parts,"base_version":"v55",
 "base_sqlite_sha256":m52["sqlite_sha256"],"new_records_repo_path":"checkpoints/v56/observations.tsv",
 "source_record_count":48,"observed":2946,"provisional_candidates":2559,
 "remaining":2463,"certified":0,"original_v36_v46_v47_v48_v52_v55_tables_preserved":True,
 "original_sprite_evidence_images_in_github":False,
 "note":"v56 GitHub TSV column set integrated; extra local v56 audit fields are retained in the conversation checkpoint ZIP"}
(out/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
statepath=ROOT/"PROJECT_STATE.json";s=json.loads(statepath.read_text("utf8"))
assert s["unified_database"]["version"]=="v55" and s["unified_database"]["observed_unique"]==2898
s["latest_checkpoint"]={"version":"v56","date":"2026-10-25","baseline_reconciliation":"v55",
 "baseline_unique_observed":2898,"new_unique_observed":48,"new_provisional_candidates":33,
 "new_held":15,"overlap_with_prior":0,"merged_unique_observed":2946,
 "merged_observation_percent":54.4648,"remaining_unobserved":2463,
 "auditable_provisional_candidate_keys":2559,"approved_final_certifications":0,
 "delta_repo_path":"checkpoints/v56/observations.tsv",
 "verification_script":"checkpoints/v56/verify_delta.py",
 "png_tmx_mapping_verified":0,"tilezed_verified":0,
 "high_resolution_evidence_images_in_conversation_zip_not_github":True}
s["unified_database"]={"version":"v56","status":"VERIFIED",
 "repo_manifest":"analysis/current/v56/MANIFEST.json",
 "restore_script":"scripts/restore_unified_v56.py","observed_unique":2946,
 "observed_percent":54.4648,"remaining_unobserved":2463,
 "auditable_candidates":2559,"certified":0,"sqlite_sha256":manifest["sqlite_sha256"],
 "complete_v36_tables":True,"complete_v46_tables":True,
 "v47_v48_v55_tables_preserved":True,"v56_git_checkpoint_integrated":True,
 "v56_extra_local_metadata_in_external_checkpoint":True,"image_binaries_in_github":False}
s["next_actions"]=[
 "v56 통합 DB의 미관찰 2,463종을 대상으로 실제 PNG와 TMX A/B/C/D 시각 판독을 이어간다.",
 "v56에서 보류한 15종은 다른 위치의 원본 PNG 및 가려짐을 재검토한다.",
 "사용자의 수동 검수 80종은 별도 계보로 보존하여 이 누적에 합산하지 않았다. 수동 자료의 4종 수정 제안은 원본 기록을 덮어쓰지 않고 별도로 관리한다.",
 "기존 v55 이하 통합 DB, v36·v46 원본을 보존하고 새 SQLite만 추가한다.",
 "v56의 고해상도 이미지 증거 48개는 채팅 ZIP에 저장했으며 GitHub에 이미지 자체를 올렸다고 주장하지 않는다."
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BUILT v56, verified",checks,"SHA256",manifest["sqlite_sha256"],"parts",len(parts))
