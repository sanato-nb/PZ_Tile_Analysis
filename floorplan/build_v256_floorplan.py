#!/usr/bin/env python3
"""Build v256 offline floorplan with complete v255 10042-key unified source."""
from pathlib import Path
import base64,csv,gzip,hashlib,json
R=Path(__file__).resolve().parents[1]
SOURCE=R/"review/v255_latest_integrated_10042_2026-10-30/MASTER_ALL_10042_LATEST_PREFERRED.csv"
BASE=R/"floorplan/current/v255_floorplan_latest_user_priority.html"
OUT=R/"floorplan/current/v256_floorplan_unified_10042.html"
MAN=R/"floorplan/current/MANIFEST_V256.json"
def hash_(b):return hashlib.sha256(b).hexdigest()
def rep(s,old,new):
 assert s.count(old)==1,("non-unique patch",old[:60],s.count(old))
 return s.replace(old,new,1)
source_man=json.loads((R/"review/v255_latest_integrated_10042_2026-10-30/MANIFEST.json").read_text("utf8"))
assert hash_(SOURCE.read_bytes())==source_man["new_master_sha256"]
with SOURCE.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
assert len(rows)==10042 and len({r["source_key"] for r in rows})==10042
assert sum(r["active_flag"]=="1" for r in rows)==9587
held=[r for r in rows if r["active_exclusion_reason"]=="HISTORICAL_HELD_439"]
assert len(held)==439 and sum(bool(r["latest_user_choice"]) for r in held)==68
assert sum(r["latest_user_choice"]=="user_implicit_accept_prior_provisional" for r in held)==52
assert sum(r["latest_user_choice"]=="user_explicit_identified" for r in held)==4
assert sum(r["latest_user_choice"]=="user_explicit_part_only" for r in held)==12
assert sum(r["active_flag"]=="0" for r in rows)==455
fields=["source_key","active_flag","active_exclusion_reason","review_status","object_identity_candidate",
"user_candidate_verbatim","A_visible_shape_note","latest_visual_candidate_KO","latest_visual_shape_KO",
"latest_visual_source","latest_user_choice","latest_user_object_name_verbatim",
"latest_user_part_role_verbatim","latest_user_orientation_verbatim","latest_user_notes_verbatim",
"latest_evidence_BC_path"]
packed=json.dumps([[r.get(k,"") for k in fields] for r in rows],ensure_ascii=False,separators=(",",":")).encode()
encoded=base64.b64encode(gzip.compress(packed,9,mtime=0)).decode()
JS=r'''
// Integrated v256 full source. Legacy v22 raw GID/geometry is retained separately.
const V256_COLUMNS=__COLS__;
const V256_B64="__B64__";
let v256Definitions=new Map();
function v256Label(r){return r.latest_visual_candidate_KO||r.user_candidate_verbatim||r.object_identity_candidate||"";}
function v256Preferred(t,sheet,id){
 const rec=v256Definitions.get(canonical(sheet)+"/"+id);
 if(!rec)return t;
 const base=t||{image:"",category:"",geometry:"",kind:"",kindSource:"",
 individual:0,deferred:1,sourceName:"",sourceGroup:"",flags:{},material:"",
 materialStatus:"unverified",facing:"",edge:"",directionStatus:"unverified"};
 base._sheet=sheet;base._localId=id;base._v256=rec;
 const label=v256Label(rec);
 if(label){base.kind=label;base.sourceName=label;base.kindSource=rec.latest_visual_source||"v255 unified provisional";}
 if(rec.active_flag==="0"){base.deferred=1;base.individual=0;}
 return base;
}
function v256ItemKey(item){return canonical(item.mapping.sheet)+"/"+item.mapping.id;}
function v256Search(){
 const q=$("v256Query").value.trim().toLowerCase(),area=$("v256Hits");
 area.replaceChildren();if(!q){$("v256Hint").textContent="타일 키나 사물명을 입력하세요.";return;}
 const hits=[];
 for(const [key,r] of v256Definitions){if(key.toLowerCase().includes(q)||v256Label(r).toLowerCase().includes(q)){
 hits.push([key,r]);if(hits.length===30)break;}}
 $("v256Hint").textContent=hits.length===30?"30개까지만 표시, 검색어를 구체화하세요.":hits.length+"개 검색됨";
 for(const [key,r] of hits){const b=document.createElement("button");b.className="v256hit";
 b.textContent=(r.active_flag==="0"?"[보류] ":"")+key+" · "+(v256Label(r)||"정체 미확정");
 b.onclick=()=>v256Jump(key);area.append(b);}
}
function v256Jump(key){
 if(!model){$("v256Hint").textContent="TMX를 먼저 불러오세요.";return;}
 for(const [z,f] of model.floors)for(const cell of f.draw)for(const a of cell.items){
 if(v256ItemKey(a)!==key)continue;
 if(currentFloor!==z)selectFloor(z);
 const p=screen(cell.x+.5,cell.y+.5);
 panX+=dims.w/2-p.x;panY+=dims.h/2-p.y;
 inspect(cell.x,cell.y);
 $("v256Hint").textContent="Level "+z+" · "+key+" @ ("+cell.x+","+cell.y+")";
 return;
 }$("v256Hint").textContent="현재 TMX에 "+key+" 배치 없음";
}
function v256MapStats(){
 let active=0,held=0,excluded=0,outside=0,all=0;const keys=new Set();
 for(const f of model.floors.values())for(const c of f.draw)for(const a of c.items){
 all++;const k=v256ItemKey(a);keys.add(k);const r=v256Definitions.get(k);
 if(!r)outside++;else if(r.active_flag==="1")active++;
 else if(r.active_exclusion_reason==="HISTORICAL_HELD_439")held++;
 else excluded++;
 }
 $("v256Stats").textContent="현재 맵 실제 배치 "+all.toLocaleString("ko-KR")+" · 활성 "+active+
 " · 보류 "+held+" · 과거 제외 "+excluded+" · 통합 키 없음 "+outside+" · 고유 키 "+keys.size;
 v256Search();
}
function v256CsvCell(x){let s=String(x??"");if(/^\s*[=+\-@]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';}
function v256Export(){
 const f=getView();if(!f){$("v256Hint").textContent="TMX를 먼저 불러오세요.";return;}
 const h=["file","level","x","y","layer","gid","source_key","active","exclusion_reason",
 "latest_name","A_shape","user_choice","evidence_source"];
 const lines=[h.map(v256CsvCell).join(",")];
 for(const c of f.draw)for(const a of c.items){
 const r=v256Definitions.get(v256ItemKey(a));
 lines.push([model.filename,currentFloor,c.x,c.y,a.layer.name,a.mapping.clean,
 v256ItemKey(a),r?.active_flag??"not in master",r?.active_exclusion_reason||"",
 r?v256Label(r):"",r?.latest_visual_shape_KO||r?.A_visible_shape_note||"",
 r?.latest_user_choice||"",r?.latest_visual_source||""].map(v256CsvCell).join(","));
 }
 downloadBlob(new Blob(["\ufeff"+lines.join("\r\n")+"\r\n"],{type:"text/csv;charset=utf-8"}),
 model.filename.replace(/\.tmx$/i,"")+"_Level_"+currentFloor+"_v256.csv");
}
function v256Inspect(items){
 const blocks=$("details").querySelectorAll(".tile");
 for(let i=0;i<items.length;i++){
 const r=items[i].mapping.tile?._v256;if(!r||!blocks[i])continue;
 const arr=["v256 최신 통합 사물(잠정): "+(v256Label(r)||"없음"),
 "적용: "+(r.active_flag==="1"?"활성 잠정":"비활성 · 구조물 생성 안 함"),
 "원본 A: "+(r.latest_visual_shape_KO||r.A_visible_shape_note||"개별 설명 부족"),
 "출처: "+(r.latest_visual_source||"v240/v22"),
 "사용자 판정: "+(r.latest_user_choice||"없음"),
 "사용자 사물명: "+(r.latest_user_object_name_verbatim||"없음"),
 "사용자 부품: "+(r.latest_user_part_role_verbatim||"없음"),
 "사용자 방향/설명: "+(r.latest_user_orientation_verbatim||"없음"),
 "사용자 추가 메모: "+(r.latest_user_notes_verbatim||"없음"),
 "TMX B/C 증거: "+(r.latest_evidence_BC_path||"기존 데이터 확인"),
 "공식 Local ID/TileZed/정체 인증 0"];
 const div=document.createElement("div");div.className="v256audit";div.textContent=arr.join("\n");
 blocks[i].append(div);
 }
}
function v256MarkHeld(visible,show,v){
 if(!options.heldPreview||v<4)return;
 ctx.save();ctx.strokeStyle="#b95a85";ctx.lineWidth=Math.max(1,Math.min(2,v*.07));
 ctx.setLineDash([Math.max(2,v*.18),Math.max(2,v*.14)]);
 for(const c of visible){
 if(!c.items.some(a=>show(a)&&a.mapping.tile?._v256?.active_flag==="0"))continue;
 const p=screen(c.x,c.y);ctx.strokeRect(p.x+1,p.y+1,Math.max(1,v-2),Math.max(1,v-2));
 }ctx.restore();
}
'''
s=BASE.read_text("utf8")
prior=json.loads((R/"floorplan/current/MANIFEST_V255.json").read_text("utf8"))
assert hash_(s.encode())==prior["output_sha256"]
s=rep(s,"const V255_COLUMNS=",JS.replace("__COLS__",json.dumps(fields,ensure_ascii=False)).replace("__B64__",encoded)+"\nconst V255_COLUMNS=")
anchor="function getTile(sheet,id){const c=catalog?.tilesets[sheet]?.[String(id)];const t=c?Object.fromEntries(FIELDS.map((n,i)=>[n,c[i]])):null;return v243Preferred(t,v243Lookup(sheet,id),sheet,id);}"
s=rep(s,anchor,anchor.replace("return v243Preferred(t,v243Lookup(sheet,id),sheet,id);",
"return v256Preferred(v243Preferred(t,v243Lookup(sheet,id),sheet,id),sheet,id);"))
s=rep(s,"function isPillar(t){return !!(t&&t._sheet&&(",
"function isPillar(t){return !!(t&&t._v256?.active_flag!==\"0\"&&t._sheet&&(")
s=rep(s,"const ROLE=(t)=>{if(t?._v243?.role)return t._v243.role;",
"const ROLE=(t)=>{if(t?._v256?.active_flag===\"0\")return 'held';if(t?._v243?.role)return t._v243.role;")
anchor="status('v240 통합 타일 우선 적용 · 비활성 455종은 기존 기록만 보조 · TMX 파일 선택');"
insert="""const bytes256=await decompress(bytesFromBase64(V256_B64),'gzip');
    const rows256=JSON.parse(new TextDecoder().decode(bytes256));
    if(rows256.length!==10042)throw new Error('v256 master row count');
    v256Definitions=new Map(rows256.map(row=>[row[0],Object.fromEntries(V256_COLUMNS.map((k,i)=>[k,row[i]]))]));
    if(v256Definitions.size!==10042)throw new Error('duplicate v256 source key');
    let active256=0,held256=0,excluded256=0,user256=0;
    for(const [key,r] of v256Definitions){
      if(!v243Definitions.has(key))throw new Error('v256 source mismatch '+key);
      if(String(v243Definitions.get(key).active_flag)!==r.active_flag)throw new Error('active changed '+key);
      if(r.active_flag==='1')active256++;
      else if(r.active_exclusion_reason==='HISTORICAL_HELD_439')held256++;
      else excluded256++;
      if(r.latest_user_choice)user256++;
    }
    if(active256!==9587||held256!==439||excluded256!==16||user256!==68)
      throw new Error('v256 reconciliation failed');
    $('catalogState').textContent='v256 · 최신 통합 10,042 · 사용자 68 우선 · 공식 인증 0';
    $('v256Stats').textContent='전체 10,042종 / 활성 9,587 / 보류 439 / 과거 제외 16';
    status('v256 통합 정체 로드 완료 · 원본 TMX를 선택하세요');"""
s=rep(s,anchor,anchor+"\n    "+insert)
s=rep(s,"const options={floor:true,wall:true,door:true,window:true,objects:true,vegetation:true,roof:false,rooms:true,uncertain:false,grid:false,labels:true};",
"const options={floor:true,wall:true,door:true,window:true,objects:true,vegetation:true,roof:false,rooms:true,uncertain:false,grid:false,labels:true,heldPreview:true};")
s=rep(s,'<div class="section"><h3>층 선택</h3>','''<div class="section"><h3>v256 최신 통합 타일 검색</h3>
<input id="v256Query" placeholder="타일 키 또는 사물명 검색" style="width:100%;padding:9px;border:1px solid #bbccd7;border-radius:7px"/>
<div id="v256Hits" style="max-height:170px;overflow:auto;display:grid;gap:4px;margin-top:7px"></div>
<p class="note" id="v256Hint">타일 키나 사물명을 입력하세요.</p>
<button class="smallbtn" id="v256Export">현재 층 CSV 내보내기</button>
<div id="v256Stats" class="note" style="margin-top:9px;background:#e6f2ee;padding:8px;border-radius:7px">v256 데이터 준비 중</div>
</div><div class="section"><h3>층 선택</h3>''')
s=rep(s,'<label>가구 기호<input data-opt="labels" type="checkbox" checked/></label>',
'<label>가구 기호<input data-opt="labels" type="checkbox" checked/></label><label>보류 타일 위치(점선)<input data-opt="heldPreview" type="checkbox" checked/></label>')
s=rep(s,'<span><i class="square" style="background:#a8b4be"></i>도로</span>',
'<span><i class="square" style="background:#a8b4be"></i>도로</span><span><i class="square" style="background:#b95a85"></i>보류 위치</span>')
s=rep(s,"if(selected){const q=screen(selected.x,selected.y);","v256MarkHeld(visible,show,v);\nif(selected){const q=screen(selected.x,selected.y);")
s=rep(s,"v243Inspect(items);schedule()}","v243Inspect(items);v256Inspect(items);schedule()}")
s=rep(s,"selectFloor([...model.floors.keys()].sort((a,b)=>a-b)[0]);status(",
"selectFloor([...model.floors.keys()].sort((a,b)=>a-b)[0]);v256MapStats();status(")
s=rep(s,"$('fit').onclick=fit;","$('v256Query').addEventListener('input',v256Search);$('v256Export').onclick=v256Export;\n$('fit').onclick=fit;")
s=rep(s,">v243</span>",">v256</span>")
s=rep(s,"</style></head><body>",'''.v256hit{padding:5px;border:1px solid #b7d6d1;border-radius:5px;text-align:left;font-size:11px;color:#2b5965;background:#f0f7f4;overflow-wrap:anywhere}
.v256audit{border-left:3px solid #368e7a;background:#ecf5f1;padding:7px;margin-top:6px;white-space:pre-wrap;line-height:1.65}
</style></head><body>''')
s=rep(s,"<title>좀보이드 → 마인크래프트 | v255 통합 평면도 엔진 — 최신 사용자 정의 우선</title>",
"<title>좀보이드 → 마인크래프트 | v256 최신 통합 10,042종 평면도</title>")
OUT.write_text(s,"utf8")
assert "v256Inspect(items);schedule()" in s and "v256MarkHeld(visible,show,v)" in s
obj=dict(version="v256",date="2026-10-30",
 source_master=str(SOURCE.relative_to(R)),source_master_sha256=hash_(SOURCE.read_bytes()),
 input_v255_sha256=prior["output_sha256"],output_html=str(OUT.relative_to(R)),
 output_sha256=hash_(OUT.read_bytes()),source_keys=10042,active=9587,held=439,other_excluded=16,
 user_explicit=16,user_implicit=52,official_identity_certified=0,
 map_capabilities=["TMX/TSX","floor and layer controls","pan/zoom/PNG/ZIP",
 "all 10042 integrated names","source key/name search + jump to real TMX",
 "coordinate inspection","held diagnostic overlay","per-floor CSV export"],
 geometry_policy="Only 9587 active keys contribute geometry; inactive455 are outlined and inspected",
 original_data_unchanged=True)
MAN.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n","utf8")
print(json.dumps({"success":True,"keys":len(rows),"html_bytes":OUT.stat().st_size,"SHA256":obj["output_sha256"]}))
