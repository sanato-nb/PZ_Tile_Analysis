#!/usr/bin/env python3
"""v254 reconstruct the uploaded user CSV byte-for-byte from v253 template + 18 verbatim edits.
Explicit user choices and implicit acceptance are separate, never official certifications.
"""
from pathlib import Path
import csv, json, io, hashlib
R=Path(__file__).resolve().parents[1]
D=R/"review/v254_user_manual68_2026-10-30"
BASE=R/"review/v253_user_manual68_reviewkit_2026-10-30/USER_REVIEW_68_BLANK_TEMPLATE.csv"
changes=json.loads((D/"USER_NONEMPTY_FIELDS_VERBATIM.json").read_text("utf-8"))
edits=changes["user_verbatim_nonempty_fields_by_key"]
def sha256(x):return hashlib.sha256(x).hexdigest()
def blob_sha1(x):return hashlib.sha1(("blob %d\0"%len(x)).encode()+x).hexdigest()
raw_base=BASE.read_bytes()
assert blob_sha1(raw_base)==changes["baseline_git_blob_sha1"],"v253 parent template changed"
with BASE.open("r",encoding="utf-8",newline="") as f:
 reader=csv.DictReader(f);cols=reader.fieldnames;rows=list(reader)
assert len(rows)==68 and len({r["source_key"] for r in rows})==68
assert all(r["user_decision"]=="" for r in rows)
assert set(edits).issubset({r["source_key"] for r in rows}) and len(edits)==18
for row in rows:
 for k,v in edits.get(row["source_key"],{}).items():
  assert k in cols and k.startswith("user_") and isinstance(v,str) and len(v)>0
  row[k]=v
content=io.StringIO(newline="")
writer=csv.DictWriter(content,fieldnames=cols,quoting=csv.QUOTE_ALL,lineterminator="\r\n")
writer.writeheader();writer.writerows(rows)
raw_upload=("\ufeff"+content.getvalue()).encode("utf-8")
assert sha256(raw_upload)==changes["sha256_raw_user_upload"],"original user upload SHA mismatch; no bytes written"
raw_dest=D/"USER_UPLOADED_68_VERBATIM.csv"
raw_dest.write_bytes(raw_upload)

counts={"identified_explicit":0,"part_only_explicit":0,"implicit_agree":0,"implicit_with_free_text":0,
"entirely_blank_user_fields":0,"unknown3_selected":0,"user_edited_rows":0}
out=[]
for row in rows:
 key=row["source_key"];dec=row["user_decision"]
 filled={k:v for k,v in row.items() if k.startswith("user_") and v!=""}
 if filled:counts["user_edited_rows"]+=1
 if dec=="identified":counts["identified_explicit"]+=1
 elif dec=="part_only":counts["part_only_explicit"]+=1
 else:
  assert dec==""
  counts["implicit_agree"]+=1
  if filled:counts["implicit_with_free_text"]+=1
  else:counts["entirely_blank_user_fields"]+=1
 if row["review_group"].startswith("정체불명") and dec:
  counts["unknown3_selected"]+=1
 prior=row["v252_revised_candidate_KO"] or row["v251_original_candidate_KO"]
 freeform=row["user_object_name_KO"] or row["user_orientation_KO"]
 # For checked rows, do not turn freeform "orientation" into an official object label.
 # Keep previous candidate as fallback and the entire user prose unchanged in separate fields.
 out.append(dict(
  source_index=row["source_index"],source_key=key,review_group=row["review_group"],
  status=("user_explicit_"+dec if dec else "user_implicit_accept_prior_provisional"),
  user_provisional_priority=1,baseline_candidate_when_agree_KO=prior,
  user_object_name_verbatim=row["user_object_name_KO"],
  user_part_role_verbatim=row["user_part_role_KO"],
  user_orientation_verbatim=row["user_orientation_KO"],
  user_material_verbatim=row["user_material_KO"],
  user_confidence_verbatim=row["user_confidence"],
  user_reason_verbatim=row["user_reason_evidence_KO"],
  user_notes_verbatim=row["user_notes_KO"],
  user_preferred_visual_description_KO=(freeform if freeform else prior),
  user_notes_only_no_choice=int(not dec and bool(filled)),
  evidence_A_SHA256=row["original_A_RGBA_SHA256"],
  evidence_A_sheet=row["original_A_sheet_path"],
  evidence_actual_BC_image=row["true_TMX_B_C_evidence_path"],
  official_local_id_mapping_verified=0,TileZed_verified=0,final_identity_certified=0,
  v240_active_status_changed=0
 ))
assert counts==dict(identified_explicit=4,part_only_explicit=12,implicit_agree=52,
 implicit_with_free_text=2,entirely_blank_user_fields=50,unknown3_selected=3,user_edited_rows=18),counts
with (D/"ALL68_USER_PRIORITY_PROVISIONAL_OVERLAY.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]),quoting=csv.QUOTE_ALL,lineterminator="\r\n")
 w.writeheader();w.writerows(out)
manifest=dict(version="v254",date="2026-10-30",user_upload_exact_sha256=sha256(raw_upload),
 original_uploaded_name=changes["source_upload_filename"],exact_user_upload_bytes=len(raw_upload),
 unique_keys=68,from_v253_review_kit=68,review_medium=65,previously_unknown=3,
 counts=counts,not_selected_means_user_agrees_with_previous_provisional_candidate=True,
 previous_candidate_priority_when_blank="v252 revised candidate if supplied; otherwise v251",
 explicit_user_wording_has_priority_but_is_not_formal_tile_id_certification=True,
 new_final_game_identity_certification=0,new_TileZed_certification=0,
 prior_v251_v252_v253_unmodified=True,master_v240_unchanged=True,
 original_PNG_TMX_SQLite_unchanged=True,
 outputs=["USER_UPLOADED_68_VERBATIM.csv","ALL68_USER_PRIORITY_PROVISIONAL_OVERLAY.csv"])
(D/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"source_sha_verified":manifest["user_upload_exact_sha256"],"counts":counts,"status":"passed"},ensure_ascii=False))
