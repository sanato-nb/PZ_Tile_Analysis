#!/usr/bin/env python3
"""Extend tested v243 HTML with 439 v255 image-first visual results for inspector.
Inactive held keys stay physically INACTIVE: no wall/geometry role promotion.
The latest user v254 wording takes precedence as a *provisional label* only.
"""
from pathlib import Path
import base64,csv,gzip,hashlib,json
R=Path(__file__).resolve().parents[1]
MASTER=R/"review/v255_latest_integrated_10042_2026-10-30/HELD439_LATEST_VISUAL_USER_PRIORITY.csv"
BASE=R/"floorplan/current/v243_floorplan_v240_priority.html"
OUT=R/"floorplan/current/v255_floorplan_latest_user_priority.html"
MAN=R/"floorplan/current/MANIFEST_V255.json"
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,needle,repl):
 n=s.count(needle)
 if n!=1:raise AssertionError(f"anchor {needle[:55]!r} appears {n} times")
 return s.replace(needle,repl,1)
with MASTER.open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f))
assert len(rows)==439 and len({x["source_key"] for x in rows})==439
assert all(x["active_flag"]=="0" and x["active_exclusion_reason"]=="HISTORICAL_HELD_439" for x in rows)
assert sum(bool(x["latest_user_choice"]) for x in rows)==68
assert sum(x["latest_user_choice"]=="user_implicit_accept_prior_provisional" for x in rows)==52
assert sum(x["latest_user_choice"]=="user_explicit_identified" for x in rows)==4
assert sum(x["latest_user_choice"]=="user_explicit_part_only" for x in rows)==12
cols=["source_key","latest_visual_candidate_KO","latest_visual_shape_KO","latest_visual_source",
"latest_user_choice","latest_user_object_name_verbatim","latest_user_part_role_verbatim",
"latest_user_orientation_verbatim","latest_user_notes_verbatim","latest_evidence_BC_path",
"latest_evidence_A_SHA256","latest_held_provisional_only"]
packed=[[r[k] for k in cols] for r in rows]
payload=json.dumps(packed,ensure_ascii=False,separators=(",",":")).encode("utf-8")
encoded=base64.b64encode(gzip.compress(payload,compresslevel=9,mtime=0)).decode()
legacy=BASE.read_text("utf-8")
prior=json.loads((R/"floorplan/current/MANIFEST.json").read_text("utf-8"))
assert sha(legacy.encode())==prior["output_sha256"],"v243 HTML changed; unsafe patch"
source="""// v255 newer held tile meanings: viewable in inspector, never activated by the renderer.
const V255_COLUMNS=REPLACE_COLUMNS;
const V255_DATA_B64="REPLACE_B64";
let v255Definitions=new Map();
""".replace("REPLACE_COLUMNS",json.dumps(cols,ensure_ascii=False)).replace("REPLACE_B64",encoded)
legacy=rep(legacy,"const V243_DATA_B64=",source+"\nconst V243_DATA_B64=")
anchor="v243Definitions=new Map(records240.map(cols=>[cols[0],Object.fromEntries(V243_COLUMNS.map((k,i)=>[k,cols[i]]))]));"
code="""const raw255=await decompress(bytesFromBase64(V255_DATA_B64),'gzip');
    const records255=JSON.parse(new TextDecoder().decode(raw255));
    if(records255.length!==439)throw new Error('v255 latest 439 missing');
    v255Definitions=new Map(records255.map(cols=>[cols[0],Object.fromEntries(V255_COLUMNS.map((k,i)=>[k,cols[i]]))]));
    if(v255Definitions.size!==439)throw new Error('v255 held key duplicate');
    for(const k of v255Definitions.keys()){
      const legacy=v243Definitions.get(k);
      if(!legacy||legacy.active_flag!==0||legacy.active_exclusion_reason!=='HISTORICAL_HELD_439')
        throw new Error('v255 held scope violates source v240: '+k);
    }
    $('catalogState').textContent='v255 최신 시각 후보 439종 (사용자68 우선) · 활성 9,587 / 보류 455 · 공식 인증 0';
    """
legacy=rep(legacy,anchor,anchor+"\n    "+code)
# Inspector lookup metadata without altering original mapping or real role
anchor2="  if(active){\n    const current=source.user_candidate_verbatim||source.object_identity_candidate;"
insertion="""  const newLatest=v255Definitions.get(sheet+'/'+id);
  if(newLatest)out._v255=newLatest;
"""
legacy=rep(legacy,anchor2,insertion+anchor2)
anchor3="    const r=items[i].mapping.tile?._v243;"
legacy=rep(legacy,anchor3,anchor3+"\n    const latest=items[i].mapping.tile?._v255;")
anchor4='      "정체/TileZed/공식 Local ID 인증: 0",'
insert='''      ...(latest?[
        "v255 최신 타일 정체 (잠정): "+(latest.latest_visual_candidate_KO||"불명"),
        "v255 원본 A 형태: "+(latest.latest_visual_shape_KO||"설명 없음"),
        "v255 분석 출처: "+latest.latest_visual_source,
        "사용자 판정 우선: "+(latest.latest_user_choice||"사용자 추가 판정 없음"),
        "사용자 입력 원문 (물체명): "+(latest.latest_user_object_name_verbatim||"없음"),
        "사용자 입력 원문 (부품/방향): "+
          (latest.latest_user_part_role_verbatim||latest.latest_user_orientation_verbatim||"없음"),
        "사용자 추가 메모: "+(latest.latest_user_notes_verbatim||"없음"),
        "B/C 증거: "+(latest.latest_evidence_BC_path||"없음"),
        "중요: 기존 v240에서 보류된 타일. 시각 이름만 보존하며 활성·구조 변환 금지"
       ]:[]),'''
legacy=rep(legacy,anchor4,anchor4+"\n"+insert)
legacy=legacy.replace("v243 통합 평면도 엔진 — v240 우선","v255 통합 평면도 엔진 — 최신 사용자 정의 우선",1)
assert "const V255_DATA_B64=" in legacy and "v255Definitions.size!==439" in legacy
assert "v243Inspect(items);schedule()}" in legacy
OUT.write_text(legacy,encoding="utf-8")
manifest=dict(version="v255_floorplan_user_latest_439_inactive_inspection",
date="2026-10-30",source_v243_html_sha256=prior["output_sha256"],
source_latest_held439_csv_sha256=sha(MASTER.read_bytes()),
output_html=str(OUT.relative_to(R)),output_sha256=sha(legacy.encode()),
total_master_keys=10042,held_latest_visual_candidates=439,latest_user_choices=68,
explicit_identified=4,explicit_part_only=12,implicit_agreement=52,
active_preserved=9587,inactive_preserved=455,
geometry_policy="v243 active geometry unchanged; held tiles receive evidence metadata only",
official_certification=0,legacy_v243_html_untouched=True)
MAN.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(dict(result="PASS",size=len(legacy),latest439=len(rows),user68=68,output=manifest["output_html"])))
