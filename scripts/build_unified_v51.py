#!/usr/bin/env python3
"""Build a single SHA-reproducible v51 SQLite from untouched v50 and new 41 visual records."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
m50=json.loads((ROOT/"analysis/current/v50/MANIFEST.json").read_text("utf8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)==m50["sqlite_sha256"],"Source v50 SHA256 mismatch"
with sqlite3.connect(src) as c:
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0]==2643
 assert c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0]==2343
with (ROOT/"checkpoints/v51/observations.tsv").open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({(r["tile_set_locator"],int(r["local_id"])) for r in rows})==41
assert sum(r["review_status"]=="candidate" for r in rows)==35
assert sum(r["review_status"]=="held" for r in rows)==6
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
dst=Path(os.environ.get("RUNNER_TEMP","/tmp"))/"tile_visual_v51_unified.sqlite"
if dst.exists():dst.unlink()
with sqlite3.connect(src) as before,sqlite3.connect(dst) as c:before.backup(c)
with sqlite3.connect(dst) as c:
 c.execute("PRAGMA journal_mode=DELETE")
 for field in ("v51_observed","v51_candidate_auditable"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} INTEGER NOT NULL DEFAULT 0")
 for field in ("v51_review_status","v51_identity_candidate","v51_observed_features"):
  c.execute(f"ALTER TABLE tile_catalog ADD COLUMN {field} TEXT")
 cols=list(rows[0])
 numerics={"local_id","level","x","y","visible_pixel_delta","missing_png_neighbors","mapping_verified","tilezed_verified","final_certified"}
 schema=",".join('"'+x+'" '+("INTEGER" if x in numerics else "TEXT") for x in cols)
 c.execute("CREATE TABLE v51_visual_review("+schema+",PRIMARY KEY(tile_set_locator,local_id))")
 sql="INSERT INTO v51_visual_review VALUES("+",".join("?" for _ in cols)+")"
 for r in rows:
  key=(r["tile_set_locator"],int(r["local_id"]))
  prev=c.execute("SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?",key).fetchone()
  assert prev==(0,),f"Overlap/unknown key: {key}, {prev}"
  c.execute(sql,[int(r[x]) if x in numerics else r[x] for x in cols])
  candidate=int(r["review_status"]=="candidate")
  c.execute("""UPDATE tile_catalog SET observed_any=1,v51_observed=1,
       provisional_candidate_any_auditable=?,v51_candidate_auditable=?,v51_review_status=?,
       v51_identity_candidate=?,v51_observed_features=?,current_candidate=?,current_review_version='v51'
       WHERE tile_set_locator=? AND local_id=?""",
       (candidate,candidate,r["review_status"],r["identity_candidate"],r["observed_features"],r["identity_candidate"],*key))
 progress=[("v51_new_observed",41,"direct A/B/C/D reviewed"),
           ("v51_new_candidates",35,"provisional only"),("v51_new_held",6,"uncertain"),
           ("v51_total_observed",2684,"2643 + 41, no overlap"),
           ("v51_unobserved",2725,"5409-2684"),
           ("v51_candidate_auditable",2378,"2343+35")]
 c.executemany("INSERT INTO progress_snapshot VALUES (?,?,?)",progress)
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 checks={"all":c.execute("select count(*) from tile_catalog").fetchone()[0],
         "observed":c.execute("select count(*) from tile_catalog where observed_any=1").fetchone()[0],
         "candidate":c.execute("select count(*) from tile_catalog where provisional_candidate_any_auditable=1").fetchone()[0],
         "remaining":c.execute("select count(*) from analysis_queue").fetchone()[0],
         "v51review":c.execute("select count(*) from v51_visual_review").fetchone()[0],
         "final":c.execute("select count(*) from tile_catalog where identity_final_certified=1").fetchone()[0]}
 assert checks=={"all":5409,"observed":2684,"candidate":2378,"remaining":2725,"v51review":41,"final":0},checks
 c.execute("VACUUM")
out=ROOT/"analysis/current/v51";out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode("ascii")
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f"analysis/current/v51/v51.part{i//3000000:03}.b64"
 (ROOT/rel).write_text(encoded[i:i+3000000]+"\n","ascii")
 parts.append(rel)
manifest={"version":"v51","sqlite_file":"tile_visual_v51_unified.sqlite","sqlite_size_bytes":len(raw),
 "sqlite_sha256":hashlib.sha256(raw).hexdigest(),"compressed_sha256":hashlib.sha256(packed).hexdigest(),
 "compression":"zlib_base64","parts":parts,"base_version":"v50",
 "base_sqlite_sha256":m50["sqlite_sha256"],"new_records_repo_path":"checkpoints/v51/observations.tsv",
 "source_record_count":41,"observed":2684,"provisional_candidates":2378,
 "remaining":2725,"certified":0,"original_v36_v46_v47_v48_v50_tables_preserved":True,
 "original_sprite_evidence_images_in_github":False,
 "note":"v51 GitHub TSV column set integrated; extra local v51 audit fields are retained in the conversation checkpoint ZIP"}
(out/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
statepath=ROOT/"PROJECT_STATE.json";s=json.loads(statepath.read_text("utf8"))
assert s["unified_database"]["version"]=="v50" and s["unified_database"]["observed_unique"]==2643
s["latest_checkpoint"]={"version":"v51","date":"2026-10-25","baseline_reconciliation":"v50",
 "baseline_unique_observed":2643,"new_unique_observed":41,"new_provisional_candidates":35,
 "new_held":6,"overlap_with_prior":0,"merged_unique_observed":2684,
 "merged_observation_percent":49.6210,"remaining_unobserved":2725,
 "auditable_provisional_candidate_keys":2378,"approved_final_certifications":0,
 "delta_repo_path":"checkpoints/v51/observations.tsv",
 "verification_script":"checkpoints/v51/verify_delta.py",
 "png_tmx_mapping_verified":0,"tilezed_verified":0,
 "high_resolution_evidence_images_in_conversation_zip_not_github":True}
s["unified_database"]={"version":"v51","status":"VERIFIED",
 "repo_manifest":"analysis/current/v51/MANIFEST.json",
 "restore_script":"scripts/restore_unified_v51.py","observed_unique":2684,
 "observed_percent":49.6210,"remaining_unobserved":2725,
 "auditable_candidates":2378,"certified":0,"sqlite_sha256":manifest["sqlite_sha256"],
 "complete_v36_tables":True,"complete_v46_tables":True,
 "v47_v48_v50_tables_preserved":True,"v51_git_checkpoint_integrated":True,
 "v51_extra_local_metadata_in_external_checkpoint":True,"image_binaries_in_github":False}
s["next_actions"]=["Continue new A/B/C/D original-PNG visual review from the v51 analysis_queue of 2,766 never-observed keys.",
 "Review the v51 6 held keys using alternative source scenes and correct PNG atlas versions.",
 "Keep 256 historical candidate-wording conflicts and 135 v36 candidate-report discrepancies unresolved.",
 "Preserve every original SQLite and upgrade only new versioned unified databases.",
 "Collect/store high-resolution image evidence in a persistent accessible source; do not claim embedded images in GitHub until done."]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BUILT v51, verified",checks,"SHA256",manifest["sqlite_sha256"],"parts",len(parts))
