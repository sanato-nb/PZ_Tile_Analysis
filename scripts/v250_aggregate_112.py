import csv,json
from pathlib import Path
P=Path("review/v250_held112_Afirst_individual_2026-10-30")
def r(p):return list(csv.DictReader(p.open(encoding="utf-8-sig",newline="")))
base=r(P/"EXACT_PENDING_112_KEY_CROSSWALK.csv")
hashes={x["source_key"]:x for x in r(P/"A_ORIGINAL_112_SHA_VERIFIED.csv")}
notes={}
for p in list(P.glob("A_FIRST_INDIVIDUAL_112_PAGE_*.csv"))+list(P.glob("A_FIRST_PAGE_*.csv")):
 for x in r(p):
  i=int(x["source_index"]);assert i not in notes
  notes[i]=(x.get("A_visible") or x.get("A_just_seen_pixel_morphology_KO") or x.get("A_observed_KO"),x.get("candidate") or x.get("provisional_object_part_name_KO") or x.get("provisional_part_KO"))
assert len(base)==len(hashes)==len(notes)==112
out=[]
for x in base:
 i=int(x["source_index"]);a,b=notes[i];h=hashes[x["source_key"]]
 assert a and b
 out.append(dict(key=x["source_key"],index=i,A_pixel_observed=a,provisional_part=b,A_SHA=h["A_RGBA_sha256"],TMX=x["actual_TMX_alternate"],B_C=x["original_B_C_change_pixels"],source_BC=x["exact_source_qualified_BC_panel"],certified=0))
with (P/"ALL112_DETAILED.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
(P/"MANIFEST.json").write_text(json.dumps(dict(v="v250",seen=112,sha=112,auth=0)))
print(len(out))
