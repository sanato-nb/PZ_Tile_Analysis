#!/usr/bin/env python3
"""Physically merge v240 preferred tile semantics into the preserved v22.1 floorplan HTML.
The previous 60,174-definition catalog remains embedded for fallback geometry. No certifications.
"""
from pathlib import Path
import base64,csv,gzip,hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"floorplan/legacy/v22_1_recovered_source.html"
DATA=ROOT/"review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv"
OUT=ROOT/"floorplan/current/v243_floorplan_v240_priority.html"
MAN=ROOT/"floorplan/current/MANIFEST.json"
FIELDS=("source_key","active_flag","active_exclusion_reason","review_status",
        "A_visible_shape_note","object_identity_candidate","user_candidate_verbatim",
        "user_verdict_verbatim","A_original_source_png","A_rgba_sha256_prior",
        "B_C_pixels_prior","review_evidence_path","role_from_A")
def hash256(b): return hashlib.sha256(b).hexdigest()
def role(a, active):
    # Only direct A-shape notes, never a previous B-scene candidate or tileset filename.
    if not active or not a or not a.startswith(("A는","원본 A","A 이미지")): return ""
    if re.search(r"단정 불가|확정 불가|불분명|원인 미확인|역할 미확정",a):return ""
    if re.search(r"혈흔|오염흔|낙서|데칼|얼룩|그림자|먼지 자국",a):return "overlay"
    if re.search(r"기둥|수직 지주",a) and not re.search(r"기둥처럼|기둥과|기둥 주변|벽판|벽면|난간",a):return "pillar"
    if re.search(r"바닥 (?:타일|표면|마감)|노면 (?:무늬|표면)",a):return "floor"
    if re.search(r"지붕 (?:기와|판|표면)",a):return "roof"
    return ""
def load():
    with DATA.open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f))
    if len(rows)!=10042:raise ValueError("Incorrect v240 total")
    seen=set();active=0;reasons={};packed=[]
    for r in rows:
        k=r["source_key"]
        if k!=r["tile_set_name"]+"/"+str(int(r["local_id"])) or k in seen:raise ValueError("Bad key "+k)
        seen.add(k);a=int(r["active_flag"]);active+=a
        if not a: reasons[r["active_exclusion_reason"]]=reasons.get(r["active_exclusion_reason"],0)+1
        d={name:r.get(name,"") for name in FIELDS}
        d["active_flag"]=a
        d["role_from_A"]=role(d["A_visible_shape_note"],a)
        packed.append([d[x] for x in FIELDS])
    if active!=9587 or reasons!={"HISTORICAL_HELD_439":439,"USER_V196_MANUAL_UNDECIDED":10,"USER_V116_PREVIOUS_EXCLUSION":6}:raise ValueError("Bad exclusion counts "+str(reasons))
    packed.sort(key=lambda r:r[0]);return packed,reasons

EXT=r'''
// v243 preferred image-based tile semantics. Legacy v22.1 is a fallback, not deleted.
const V243_COLUMNS=["source_key","active_flag","active_exclusion_reason","review_status",
"A_visible_shape_note","object_identity_candidate","user_candidate_verbatim",
"user_verdict_verbatim","A_original_source_png","A_rgba_sha256_prior",
"B_C_pixels_prior","review_evidence_path","role_from_A"];
const V243_DATA_B64="REPLACE_V240_DATA";
let v243Definitions=new Map();
function v243Lookup(sheet,id){return v243Definitions.get(canonical(sheet)+"/"+id);}
function v243Preferred(t,source,sheet,id){
  if(!source)return t;
  const active=source.active_flag===1;
  const base=t||{image:source.A_original_source_png||"v240_reference",category:"",
    geometry:"",kind:"",kindSource:"",individual:0,deferred:1,sourceName:"",
    sourceGroup:"",flags:{},material:"",materialStatus:"unverified",
    facing:"",edge:"",directionStatus:"unverified"};
  const out={...base,flags:{...(base.flags||{})},_sheet:sheet,_localId:id,
    _v243:{...source,active:active,role:active?source.role_from_A:""}};
  if(active){
    const current=source.user_candidate_verbatim||source.object_identity_candidate;
    if(current){out.kind=current;out.sourceName=current;out.kindSource="v240 priority (provisional)";}
    // Only directly supported A shapes override renderer roles. Otherwise preserve wall edge flags.
    if(source.role_from_A==="pillar"){out.geometry="pillar";out.category="pillar";}
    if(source.role_from_A==="overlay"){out.geometry="floor_overlay";out.category="overlay";}
    if(source.role_from_A==="floor"){out.geometry="floor_surface";out.category="floor";}
    if(source.role_from_A==="roof"){out.geometry="roof_candidate";out.category="roof";}
    out.individual=0;out.deferred=1;
  }
  return out;
}
function v243Inspect(items){
  const blocks=$("details").querySelectorAll(".tile");
  for(let i=0;i<items.length;i++){
    const r=items[i].mapping.tile?._v243;
    if(!r||!blocks[i])continue;
    const textLines=[
      "v240: "+(r.active?"우선 적용(잠정)":"활성 제외 · 기존 기록 보존"),
      "A 외형: "+(r.A_visible_shape_note||"개별 A 독립 메모 없음 (v22 구조 정보 보조)"),
      "사용자 잠정 후보: "+(r.user_candidate_verbatim||"없음"),
      "현재 잠정 후보: "+(r.object_identity_candidate||"없음"),
      "검수 상태: "+r.review_status,
      "출처: "+(r.A_original_source_png||r.review_evidence_path||"없음"),
      "정체/TileZed/공식 Local ID 인증: 0",
      r.active?"":"비활성 이유: "+r.active_exclusion_reason
    ];
    const el=document.createElement("div");
    el.className="meta";el.style.cssText="border-top:1px solid #c9d6df;margin-top:7px;padding-top:8px;white-space:pre-wrap";
    el.textContent=textLines.filter(Boolean).join("\n");
    blocks[i].appendChild(el);
  }
}
'''
def replace_exact(s,old,new,label):
    if s.count(old)!=1:raise ValueError(label+" anchor count "+str(s.count(old)))
    return s.replace(old,new,1)
def patch(s,b64):
    ext=EXT.replace("REPLACE_V240_DATA",b64)
    s=replace_exact(s,"const FIELDS=['image'",ext+"\nconst FIELDS=['image'","fields")
    anchor="status('v22 의미 사전 준비 완료 · TMX 파일을 선택하세요.');"
    injected="""const raw240=await decompress(bytesFromBase64(V243_DATA_B64),'gzip');
    const records240=JSON.parse(new TextDecoder().decode(raw240));
    if(records240.length!==10042)throw new Error('v240 source count not 10042');
    v243Definitions=new Map(records240.map(cols=>[cols[0],Object.fromEntries(V243_COLUMNS.map((k,i)=>[k,cols[i]]))]));
    if(v243Definitions.size!==10042)throw new Error('v240 key duplicate');
    $('catalogState').textContent='v240 우선 10,042 / 활성 9,587 · v22.1 기존 정의 보조';
    status('v240 통합 타일 우선 적용 · 비활성 455종은 기존 기록만 보조 · TMX 파일 선택');"""
    s=replace_exact(s,anchor,injected,"loadCatalog")
    s=replace_exact(s,
      "function getTile(sheet,id){const c=catalog?.tilesets[sheet]?.[String(id)];if(!c)return null;const t={};FIELDS.forEach((n,i)=>t[n]=c[i]);t._sheet=sheet;t._localId=id;return t;}",
      "function getTile(sheet,id){const c=catalog?.tilesets[sheet]?.[String(id)];const t=c?Object.fromEntries(FIELDS.map((n,i)=>[n,c[i]])):null;return v243Preferred(t,v243Lookup(sheet,id),sheet,id);}",
      "getTile")
    s=replace_exact(s,
      "function isPillar(t){return !!(t&&t._sheet&&CONFIRMED_POSTS[t._sheet]?.has(t._localId));}",
      "function isPillar(t){return !!(t&&t._sheet&&(t._v243?.role==='pillar'||CONFIRMED_POSTS[t._sheet]?.has(t._localId)));}",
      "pillar")
    s=replace_exact(s,
      "const ROLE=(t)=>{if(!t||!t.image)return 'none';",
      "const ROLE=(t)=>{if(t?._v243?.role)return t._v243.role;if(!t||!t.image)return 'none';",
      "ROLE")
    s=replace_exact(s,
      "const role=ROLE(t),verified=!!t.individual,kind=isPillar(t)?'기둥 (시각 검증 보정)':t.deferred?'미확정 / 최종 검수 보류':t.kind||t.sourceName||t.category||'미분류'",
      "const role=ROLE(t),verified=!!t.individual&&!t._v243,kind=t._v243?.active?(t._v243.user_candidate_verbatim||t._v243.object_identity_candidate||t.kind||'A 형태 후보'):isPillar(t)?'기둥 (시각 검증 보정)':t.deferred?'미확정 / 최종 검수 보류':t.kind||t.sourceName||t.category||'미분류'",
      "inspector label")
    # Keep the old inspector and append explicit latest source, including active exclusions.
    lines=s.splitlines(keepends=True)
    indices=[i for i,l in enumerate(lines) if l.startswith("function inspect(x,y){")]
    if len(indices)!=1 or ";schedule()}" not in lines[indices[0]]:raise ValueError("inspector source changed")
    i=indices[0];lines[i]=lines[i].replace(";schedule()}",";v243Inspect(items);schedule()}",1)
    s="".join(lines)
    s=s.replace("v22 통합 평면도 엔진","v243 통합 평면도 엔진 — v240 우선",1)
    s=s.replace(">v22</span>",">v243</span>",1)
    s=s.replace("v22 누적 타일 정의 60,174개","v240 우선 10,042종 / 활성 9,587종 · v22 보조 60,174개",1)
    if "v243Inspect(items);schedule()}" not in s:raise ValueError("Missing inspector injection")
    return s
def main():
    rows,reasons=load()
    packed=json.dumps(rows,ensure_ascii=False,separators=(",",":")).encode()
    encoded=base64.b64encode(gzip.compress(packed,compresslevel=9,mtime=0)).decode("ascii")
    legacy=OLD.read_text("utf8")
    html=patch(legacy,encoded)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(html,"utf8")
    obj={
      "version":"v243_floorplan_v240_preferred",
      "source_engine":"floorplan/legacy/v22_1_recovered_source.html",
      "original_engine_sha256":hash256(legacy.encode()),
      "source_master":"review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv",
      "source_master_sha256":hash256(DATA.read_bytes()),
      "output_html":str(OUT.relative_to(ROOT)),"output_sha256":hash256(html.encode()),
      "total":len(rows),"active":9587,"inactive":455,"inactive_reasons":reasons,
      "legacy_definitions_preserved":60174,
      "semantic_priority":"v240 manual candidate > v240 provisional candidate > v22",
      "geometry_priority":"explicit v240 A-only shape > v22 wall edge flags",
      "official_mapping_verified":0,"tilezed_verified":0,"identity_certified":0,
      "notes":"A shape role inferred by conservative heuristic, not official mapping; all v240 data has provisional status",
    }
    MAN.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n","utf8")
    print("PASS v243 10042 unique rows, 9587 active, 455 excluded; HTML sha:",obj["output_sha256"],"size:",len(html))
if __name__=="__main__":main()
