#!/usr/bin/env python3
"""v255: preserve v240 10,042 source records and append the 439 latest provisional interpretations.
Priority: explicit user v254 > implicit user approval of v252/v251 > v252 > v251
for one-use 188; v250 > v249 > v248 for alternate-site 251.
Do not activate the 439 archived keys or claim official game identity authentication.
"""
from pathlib import Path
import base64,csv,hashlib,io,json,sqlite3,tempfile,zlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review/v255_latest_integrated_10042_2026-10-30"
DBOUT=ROOT/"analysis/current/v255"
OUT.mkdir(parents=True,exist_ok=True);DBOUT.mkdir(parents=True,exist_ok=True)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path):
 with (ROOT/path).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(path,rows,cols=None):
 if cols is None:cols=list(rows[0])
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
def keyed(rows,name):
 m={x["source_key"]:x for x in rows}
 assert len(rows)==len(m),(name,len(rows),len(m))
 return m
def pick(*args):
 for x in args:
  if x:return x
 return ""
base=read("review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv")
first=keyed(read("review/v248_held251_full_alternate_BC_2026-10-30/ALL_251_A_FIRST_OBJECT_PART_HYPOTHESES.csv"),"251")
occlusion=keyed(read("review/v249_held251_occlusion38_diagnostics_2026-10-30/A_FIRST_38_INDIVIDUAL_MORPHOLOGY_AND_PARTS.csv"),"38")
detail112={r["key"]:r for r in read("review/v250_held112_Afirst_individual_2026-10-30/ALL112_DETAILED.csv")}
single=keyed(read("review/v251_held188_single_location_Afirst_2026-10-30/ALL188_COMPLETE_A_ORIGINAL_BC_AND_OCCLUDER_AUDIT.csv"),"188")
correct65=keyed(read("review/v252_manual_medium65_A_B_2026-10-30/ALL65_A_FIRST_MANUAL_REVIEW_AND_CORRECTIONS.csv"),"65")
user68=keyed(read("review/v254_user_manual68_2026-10-30/ALL68_USER_PRIORITY_PROVISIONAL_OVERLAY.csv"),"68")
assert len(base)==10042 and len(first)==251 and len(occlusion)==38
assert len(detail112)==112 and len(single)==188 and len(correct65)==65 and len(user68)==68
assert set(occlusion).issubset(first) and set(detail112).issubset(first)
assert not (set(first)&set(single))
assert len(set(first)|set(single))==439
assert set(correct65).issubset(single) and set(user68).issubset(single)
assert sum(x["status"]=="user_explicit_identified" for x in user68.values())==4
assert sum(x["status"]=="user_explicit_part_only" for x in user68.values())==12
assert sum(x["status"]=="user_implicit_accept_prior_provisional" for x in user68.values())==52
basecols=list(base[0])
extra=["latest_visual_shape_KO","latest_visual_candidate_KO","latest_visual_source",
"latest_evidence_A_SHA256","latest_evidence_BC_path","latest_evidence_original_BC_change_pixels",
"latest_user_choice","latest_user_object_name_verbatim","latest_user_part_role_verbatim",
"latest_user_orientation_verbatim","latest_user_material_verbatim","latest_user_notes_verbatim",
"latest_user_reason_verbatim","latest_user_provisional_priority",
"latest_explicit_user_label_KO","latest_held_provisional_only","latest_final_certification"]
assert set(extra).isdisjoint(basecols)
overlays={}
for k,r in first.items():
 overlays[k]=dict(source_key=k,latest_visual_shape_KO=r["A_historical_visible_pixels_KO"],
  latest_visual_candidate_KO=r["A_visual_hypothesis_KO"],latest_visual_source="v248_A_first",
  latest_evidence_A_SHA256="",latest_evidence_BC_path=r["actual_A_B_C_evidence_image"],
  latest_evidence_original_BC_change_pixels=r["real_original_B_C_pixels"])
for k,r in occlusion.items():
 x=overlays[k]
 x.update(latest_visual_shape_KO=r["A_direct_morphology_individually_screened_this_turn_KO"],
 latest_visual_candidate_KO=r["A_only_provisional_object_name_KO"],
 latest_visual_source="v249_occlusion38_A_first",
 latest_evidence_A_SHA256=r["source_original_A_RGBA_SHA256"])
for k,r in detail112.items():
 x=overlays[k];x.update(latest_visual_shape_KO=r["A_pixel_observed"],
 latest_visual_candidate_KO=r["provisional_part"],latest_visual_source="v250_individual112_A_first",
 latest_evidence_A_SHA256=r["A_SHA"],latest_evidence_BC_path=r["source_BC"])
for k,r in single.items():
 overlays[k]=dict(source_key=k,latest_visual_shape_KO=r["original_A_pixel_morphology_KO"],
  latest_visual_candidate_KO=r["provisional_single_sprite_object_or_part_KO"],
  latest_visual_source="v251_single188_A_first",
  latest_evidence_A_SHA256=r["original_A_RGBA_SHA256"],
  latest_evidence_BC_path=r["single_use_original_B_C_panel"],
  latest_evidence_original_BC_change_pixels=r["true_original_B_C_delta_pixels"])
for k,r in correct65.items():
 x=overlays[k];x.update(latest_visual_shape_KO=r["v252_A_observed_independently_KO"],
 latest_visual_candidate_KO=r["v252_refined_provisional_identity_KO"],
 latest_visual_source="v252_manual65_A_first")
for k,r in user68.items():
 x=overlays[k];st=r["status"];prior=x["latest_visual_candidate_KO"]
 if st=="user_implicit_accept_prior_provisional":
  assert r["baseline_candidate_when_agree_KO"]==prior,(k,prior,r["baseline_candidate_when_agree_KO"])
  label=prior
  x["latest_visual_source"]="v254_user_implicit_agrees_"+x["latest_visual_source"]
 else:
  label=pick(r["user_object_name_verbatim"],r["user_part_role_verbatim"],r["user_orientation_verbatim"],prior)
  x["latest_visual_source"]="v254_user_explicit_priority_over_"+x["latest_visual_source"]
 x["latest_visual_candidate_KO"]=label
 x.update(latest_user_choice=st,latest_user_object_name_verbatim=r["user_object_name_verbatim"],
 latest_user_part_role_verbatim=r["user_part_role_verbatim"],
 latest_user_orientation_verbatim=r["user_orientation_verbatim"],
 latest_user_material_verbatim=r["user_material_verbatim"],
 latest_user_notes_verbatim=r["user_notes_verbatim"],
 latest_user_reason_verbatim=r["user_reason_verbatim"],
 latest_user_provisional_priority="1",
 latest_explicit_user_label_KO=(label if st!="user_implicit_accept_prior_provisional" else ""))
 assert r["evidence_A_SHA256"]==overlays[k]["latest_evidence_A_SHA256"],(k,"A SHA differs")
assert len(overlays)==439
full=[];held=[];active=0;excluded={}
for row in base:
 k=row["source_key"];original_active=int(row["active_flag"]);active+=original_active
 if not original_active:excluded[row["active_exclusion_reason"]]=excluded.get(row["active_exclusion_reason"],0)+1
 overlay=overlays.get(k)
 assert (overlay is not None)==(row["active_exclusion_reason"]=="HISTORICAL_HELD_439"),(k,row["active_exclusion_reason"])
 out=dict(row)
 out.update({name:"" for name in extra})
 if overlay:
  assert not original_active
  out.update(overlay)
  out.update(latest_held_provisional_only="1",latest_final_certification="0")
  held.append(out)
 full.append(out)
assert len(full)==10042 and len(held)==439 and active==9587
assert excluded=={"HISTORICAL_HELD_439":439,"USER_V196_MANUAL_UNDECIDED":10,"USER_V116_PREVIOUS_EXCLUSION":6},excluded
assert len({r["source_key"] for r in full})==10042
write(OUT/"MASTER_ALL_10042_LATEST_PREFERRED.csv",full,basecols+extra)
write(OUT/"HELD439_LATEST_VISUAL_USER_PRIORITY.csv",held,basecols+extra)
write(OUT/"USER68_EFFECTIVE_ROWS.csv",[r for r in held if r["latest_user_choice"]],basecols+extra)
basefile=ROOT/"review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv"
oldmanifest=json.loads((ROOT/"analysis/current/v240/MANIFEST.json").read_text("utf-8"))
encoded="".join((ROOT/x).read_text("ascii").strip() for x in oldmanifest["v240_parts"])
packed=base64.b64decode(encoded,validate=True)
assert sha(packed)==oldmanifest["v240_zlib_sha256"]
raw=zlib.decompress(packed)
assert len(raw)==oldmanifest["v240_sqlite_bytes"] and sha(raw)==oldmanifest["v240_sqlite_sha256"]
with tempfile.TemporaryDirectory(prefix="pz_v255_") as folder:
 old=Path(folder)/"base.sqlite";old.write_bytes(raw)
 src=sqlite3.connect("file:"+str(old)+"?mode=ro",uri=True)
 assert src.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 before={n:src.execute('SELECT COUNT(*) FROM "'+n.replace('"','""')+'"').fetchone()[0]
         for (n,) in src.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
 assert len(before)==258
 new=Path(folder)/"latest.sqlite"
 with sqlite3.connect(new) as db:
  src.backup(db)
  db.execute("""CREATE TABLE v255_latest_held439 (
source_key TEXT PRIMARY KEY, latest_visual_candidate_KO TEXT, latest_visual_shape_KO TEXT,
latest_visual_source TEXT, evidence_A_SHA256 TEXT, evidence_BC TEXT, user_choice TEXT,
user_orientation_verbatim TEXT, user_notes_verbatim TEXT, official_certified INTEGER NOT NULL DEFAULT 0
CHECK(official_certified=0))""")
  db.executemany("INSERT INTO v255_latest_held439 VALUES (?,?,?,?,?,?,?,?,?,0)",
   [(r["source_key"],r["latest_visual_candidate_KO"],r["latest_visual_shape_KO"],
     r["latest_visual_source"],r["latest_evidence_A_SHA256"],r["latest_evidence_BC_path"],
     r["latest_user_choice"],r["latest_user_orientation_verbatim"],r["latest_user_notes_verbatim"])
    for r in held])
  db.execute("""CREATE TABLE v255_user68_manual_verdict (
source_key TEXT PRIMARY KEY, verdict_status TEXT NOT NULL, user_verbatim_fields_json TEXT NOT NULL)""")
  userrows=[(k,r["status"],json.dumps({s:r[s] for s in r if s.endswith("_verbatim") or s in
   ("user_notes_verbatim","user_reason_verbatim")},ensure_ascii=False))
   for k,r in user68.items()]
  db.executemany("INSERT INTO v255_user68_manual_verdict VALUES (?,?,?)",userrows)
  db.execute("""CREATE VIEW v255_latest_preferred_10042 AS
SELECT base.*, latest.latest_visual_candidate_KO,latest.latest_visual_shape_KO,
latest.latest_visual_source,latest.user_choice, latest.official_certified
FROM v240_tile_master_10042 base
LEFT JOIN v255_latest_held439 latest ON latest.source_key=base.source_key""")
  db.commit()
  assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
  assert db.execute("SELECT count(*) FROM v255_latest_held439").fetchone()[0]==439
  assert db.execute("SELECT count(*) FROM v255_user68_manual_verdict").fetchone()[0]==68
  assert db.execute("SELECT count(*) FROM v255_latest_preferred_10042").fetchone()[0]==10042
  assert db.execute("SELECT count(*) FROM v240_active_tile_master").fetchone()[0]==9587
  after={n:db.execute('SELECT COUNT(*) FROM "'+n.replace('"','""')+'"').fetchone()[0] for n in before}
  assert before==after
  assert len({n for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")})==260
 src.close()
 newraw=new.read_bytes()
 z=zlib.compress(newraw,6);encoded255=base64.b64encode(z).decode("ascii")
 parts=[]
 for i,start in enumerate(range(0,len(encoded255),3000000)):
  p=DBOUT/("v255.part%03d.b64"%i)
  p.write_text(encoded255[start:start+3000000]+"\n",encoding="ascii")
  parts.append(str(p.relative_to(ROOT)))
dbmanifest=dict(version="v255_append_only_source_v240",parent_version="v240",
parent_sqlite_sha256=oldmanifest["v240_sqlite_sha256"],
parent_table_count=258,parent_table_row_counts_equal=True,
new_sqlite_sha256=sha(newraw),new_sqlite_bytes=len(newraw),zlib_sha256=sha(z),
parts=parts,table_count=260,view_count_added=1,integrity_check="ok",
original_84_TMX_and_Tiles_PNG_unchanged=True,active=9587,inactive=455,
official_certifications=0)
(DBOUT/"MANIFEST.json").write_text(json.dumps(dbmanifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
manifest=dict(version="v255",date="2026-10-30",
base_master_path=str(basefile.relative_to(ROOT)),base_master_sha256=sha(basefile.read_bytes()),
total_keys=10042,active_unchanged=9587,excluded_unchanged=455,
held_439_enriched=439,alternative_TMXS_251=251,single_position_188=188,
detail_overrides={"v249":38,"v250":112,"v252":65,"v254":68},
manual_counts={"explicit_identified":4,"explicit_part_only":12,"implicit_agree":52},
old_v240_master_preserved=True,raw_original_data_preserved=True,
official_mapping_verified=0,tilezed_verified=0,final_certified=0,
new_preferred_master="review/v255_latest_integrated_10042_2026-10-30/MASTER_ALL_10042_LATEST_PREFERRED.csv",
new_master_sha256=sha((OUT/"MASTER_ALL_10042_LATEST_PREFERRED.csv").read_bytes()),
new_db_sha256=dbmanifest["new_sqlite_sha256"])
(OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"result":"PASS","keys":10042,"enriched":439,"user":68,"active":active,
"sqlite_tables":260,"new_sqlite_sha256":dbmanifest["new_sqlite_sha256"],"parts":len(parts)},ensure_ascii=False),flush=True)
