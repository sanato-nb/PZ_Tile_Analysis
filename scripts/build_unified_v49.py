#!/usr/bin/env python3
"""Physically consolidate complete v36, v46, v47 source tables plus v48 GitHub checkpoint.
Originals remain untouched. This is a new versioned SQLite artifact.
"""
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"analysis/current/v49"
SOURCE_HASH={"v36":"db64cc6285664f715f7b0168f99d625ee4e909e2cefef07b8f15abe817ea0c39",
             "v46":"73ca1bd292dbfbd22ac63ce5f06671d1475244e0b0f96a1b7a57c08e74031aa7"}
def digest(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(4*1024*1024),b""):h.update(b)
 return h.hexdigest()
def q(s):return '"'+s.replace('"','""')+'"'
def main():
 sources=Path(sys.argv[1]);merged=Path(sys.argv[2])
 a=sources/"tile_visual_v36.sqlite"; b=sources/"tile_visual_v46.sqlite"
 for label,p in [("v36",a),("v46",b)]:
  assert digest(p)==SOURCE_HASH[label],label+" SHA256 mismatch"
 for p in (a,b,merged):
  with sqlite3.connect(p) as db:assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 with sqlite3.connect(a) as c:
  A={(s,int(i)) for s,i in c.execute("select tile_set_locator,local_id from v36_full_scope where v36_visual_review_any=1")}
 with sqlite3.connect(b) as c:
  B=set()
  for v in (37,38,39,41,42,43,44,45,46):
   B|={(s,int(i)) for s,i in c.execute(f"select tile_set,local_id from v{v}_evidence")}
 assert (len(A),len(B),len(A&B),len(A|B))==(2509,477,402,2584)
 with (ROOT/"analysis/imports/merged_catalog_5409.csv").open(encoding="utf-8-sig",newline="") as f:
  base=list(csv.DictReader(f))
 with (ROOT/"checkpoints/v48/observations.tsv").open(encoding="utf-8-sig",newline="") as f:
  delta=list(csv.DictReader(f,delimiter="\t"))
 new={(r["tile_set_locator"],int(r["local_id"])):r for r in delta}
 assert len(new)==len(delta)==30 and not(set(new)&(A|B))
 assert sum(r["review_status"]=="candidate" for r in delta)==23
 assert sum(r["review_status"]=="held" for r in delta)==7
 assert all(r["mapping_verified"]=="0" and r["tilezed_verified"]=="0" and r["certified"]=="0" for r in delta)
 assert len(base)==5409 and sum(r["observed_any"]=="1" for r in base)==2584
 assert sum(r["provisional_candidate_any_auditable"]=="1" for r in base)==2302
 assert {(r["tile_set_locator"],int(r["local_id"])) for r in base if r["observed_any"]=="1"}==A|B
 OUT.mkdir(parents=True,exist_ok=True)
 target=Path(os.environ.get("RUNNER_TEMP","/tmp"))/"tile_visual_v49_unified.sqlite"
 if target.exists():target.unlink()
 # Start with a physical copy of the WHOLE original v36 DB, retaining its full schema.
 with sqlite3.connect(a) as original,sqlite3.connect(target) as db:
  original.backup(db)
 with sqlite3.connect(target) as c:
  c.execute("PRAGMA journal_mode=DELETE")
  for tag,p in [("src46",b),("src47",merged)]:
   c.execute(f"ATTACH DATABASE ? AS {tag}",("file:"+str(p.resolve())+"?mode=ro",))
  c.execute("BEGIN")
  copied=[]
  for tag,prefix in [("src46","v46__"),("src47","v47__")]:
   names=[x[0] for x in c.execute(f"select name from {tag}.sqlite_master where type='table' and name not like 'sqlite_%' order by name")]
   for name in names:
    dst=prefix+name
    c.execute(f"create table {q(dst)} as select * from {tag}.{q(name)}")
    count=c.execute(f"select count(*) from {q(dst)}").fetchone()[0]
    src_count=c.execute(f"select count(*) from {tag}.{q(name)}").fetchone()[0]
    assert count==src_count
    copied.append((tag,name,dst,count))
  c.execute("create table unified_source_tables(source_version text,source_table text,unified_table text,row_count int)")
  c.executemany("insert into unified_source_tables values(?,?,?,?)",copied)
  c.execute("create table v47_catalog ("+",".join(q(x)+" TEXT" for x in base[0])+")")
  cols=list(base[0]);c.executemany("insert into v47_catalog values("+",".join("?" for _ in cols)+")",[[r[x] for x in cols] for r in base])
  v48cols=list(delta[0])
  ints={"local_id","level","x","y","missing_png_neighbors","removal_visible_pixel_count","mapping_verified","tilezed_verified","certified"}
  c.execute("create table v48__review_checkpoint("+",".join(q(x)+(" INTEGER" if x in ints else " TEXT") for x in v48cols)+",PRIMARY KEY(tile_set_locator,local_id))")
  c.executemany("insert into v48__review_checkpoint values("+",".join("?" for _ in v48cols)+")",[[int(r[x]) if x in ints else r[x] for x in v48cols] for r in delta])
  c.execute("""create table tile_catalog(
   tile_set_locator TEXT NOT NULL, local_id INTEGER NOT NULL, occurrence_count INTEGER NOT NULL,
   v36_observed INTEGER NOT NULL, v46_observed INTEGER NOT NULL, v48_observed INTEGER NOT NULL,
   observed_any INTEGER NOT NULL, provisional_candidate_any_auditable INTEGER NOT NULL,
   v36_candidate_auditable INTEGER NOT NULL,v46_candidate_auditable INTEGER NOT NULL,
   v48_candidate_auditable INTEGER NOT NULL,
   v36_latest_candidate TEXT,v46_latest_candidate TEXT,v48_identity_candidate TEXT,
   v48_observed_features TEXT,v48_review_status TEXT,
   current_candidate TEXT,current_review_version TEXT,
   different_candidate_wording INTEGER NOT NULL,identity_final_certified INTEGER NOT NULL DEFAULT 0,
   png_tmx_mapping_verified INTEGER NOT NULL DEFAULT 0,tilezed_verified INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY(tile_set_locator,local_id))""")
  values=[]
  for r in base:
   key=(r["tile_set_locator"],int(r["local_id"]))
   d=new.get(key);recent=1 if d else 0
   observed=int(r["observed_any"])|recent
   cand=int(r["provisional_candidate_any_auditable"]) | (1 if d and d["review_status"]=="candidate" else 0)
   current=(d["identity_candidate"] if d else (r["v46_latest_candidate"] or r["v36_latest_candidate"]))
   version=("v48" if d else (r["v46_latest_review_version"] if r["v46_observed"]=="1" else r["v36_latest_review_version"]))
   values.append((key[0],key[1],int(r["occurrence_count"]),int(r["v36_observed"]),int(r["v46_observed"]),
     recent,observed,cand,int(r["v36_candidate_auditable"]),int(r["v46_candidate_auditable"]),
     int(bool(d and d["review_status"]=="candidate")),r["v36_latest_candidate"],r["v46_latest_candidate"],
     d["identity_candidate"] if d else None,d["observed_features"] if d else None,
     d["review_status"] if d else None,current,version,int(r["different_candidate_wording"]),0,0,0))
  c.executemany("insert into tile_catalog values("+",".join("?" for _ in values[0])+")",values)
  c.execute("create index idx_tile_observation on tile_catalog(observed_any,provisional_candidate_any_auditable)")
  c.execute("create view analysis_queue as select tile_set_locator,local_id,occurrence_count from tile_catalog where observed_any=0 order by occurrence_count desc,tile_set_locator,local_id")
  c.execute("create view candidate_conflicts as select tile_set_locator,local_id,v36_latest_candidate,v46_latest_candidate from tile_catalog where different_candidate_wording=1")
  c.execute("create table progress_snapshot (metric text primary key,value integer,source text)")
  pr=[("all_tiles",5409,"TMX"),("v36_observed",2509,"original v36"),("v46_observed",477,"original v46"),
      ("prior_overlap",402,"set intersection"),("v47_observed_unique",2584,"set union"),
      ("v48_new_observed",30,"new zero-overlap keys"),("v48_candidate",23,"new provisional"),
      ("v48_held",7,"new observed but identity held"),("v49_observed_unique",2614,"total"),
      ("remaining_unobserved",2795,"5409-2614"),("candidate_auditable_unique",2325,"2302+23"),
      ("candidate_wording_conflicts",256,"unresolved"),("v36_historical_candidate_discrepancy",135,"unresolved"),
      ("final_certified",0,"mapping & TileZed unverified")]
  c.executemany("insert into progress_snapshot values(?,?,?)",pr)
  c.commit()
  for tag in ("src46","src47"):c.execute("detach database "+tag)
  assert c.execute("pragma integrity_check").fetchone()[0]=="ok"
  def n(sql):return c.execute(sql).fetchone()[0]
  assert n("select count(*) from v36_full_scope")==5409
  assert n("select count(*) from tile_catalog")==5409
  assert n("select count(*) from tile_catalog where observed_any=1")==2614
  assert n("select count(*) from tile_catalog where provisional_candidate_any_auditable=1")==2325
  assert n("select count(*) from analysis_queue")==2795
  assert n("select count(*) from v48__review_checkpoint")==30
  assert n("select count(*) from tile_catalog where v48_observed=1 and v36_observed=0 and v46_observed=0")==30
  assert n("select count(*) from tile_catalog where identity_final_certified=1")==0
  assert n("select count(*) from candidate_conflicts")==256
  c.execute("vacuum")
 raw=target.read_bytes(); compressed=zlib.compress(raw,6)
 encoded=base64.b64encode(compressed).decode("ascii")
 parts=[]
 for i in range(0,len(encoded),3000000):
  rel=f"analysis/current/v49/v49.part{i//3000000:03}.b64"
  (ROOT/rel).write_text(encoded[i:i+3000000]+"\n","ascii")
  parts.append(rel)
 manifest={"version":"v49","sqlite_file":"tile_visual_v49_unified.sqlite",
   "sqlite_sha256":hashlib.sha256(raw).hexdigest(),"sqlite_size_bytes":len(raw),
   "compressed_sha256":hashlib.sha256(compressed).hexdigest(),"compression":"zlib_base64",
   "parts":parts,"v36_original_sha256":digest(a),"v46_original_sha256":digest(b),
   "v47_merged_sha256":digest(merged),"v48_source":"checkpoints/v48/observations.tsv",
   "v48_note":"GitHub TSV fields physically integrated; additional metadata in local v48 original SQLite remains in conversation ZIP",
   "scoped_tiles":5409,"observed":2614,"candidates":2325,"remaining":2795,"final_certifications":0,
   "v36_original_complete":True,"v46_tables_copied":len([x for x in copied if x[0]=="src46"]),
   "v47_tables_copied":len([x for x in copied if x[0]=="src47"]),
   "image_binaries_in_github":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n","utf8")
 state_path=ROOT/"PROJECT_STATE.json"
 s=json.loads(state_path.read_text("utf8"))
 assert s["reconciliation"]["merged_unique_observed"]==2584
 assert s["latest_checkpoint"]["merged_unique_observed"]==2614
 s["unified_database"]={"version":"v49","status":"VERIFIED","repo_manifest":"analysis/current/v49/MANIFEST.json",
    "restore_script":"scripts/restore_unified_database.py",
    "observed_unique":2614,"observed_percent":48.3269,"remaining_unobserved":2795,
    "auditable_candidates":2325,"certified":0,
    "sqlite_sha256":manifest["sqlite_sha256"],"complete_v36_tables":True,
    "complete_v46_tables":True,"v48_git_checkpoint_integrated":True,
    "v48_local_extra_metadata_in_external_checkpoint":True,"image_binaries_in_github":False}
 state_path.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n","utf8")
 print(json.dumps({"PASS":True,"observed":2614,"sqlite_bytes":len(raw),"tables_copied":len(copied),"parts":len(parts),"sha256":manifest["sqlite_sha256"]}),flush=True)
if __name__=="__main__":main()
