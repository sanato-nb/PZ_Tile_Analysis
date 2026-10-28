#!/usr/bin/env python3
"""Make a portable offline manual reviewer for the 33 physically unresolved v192
tile keys: 23 with exact original A and actual original TMX B/C from verified
v182 evidence, and 10 without exact source A. Never infer final identities.
No changes to PROJECT_STATE, original SQLite or previous classifications.
"""
from pathlib import Path
from collections import Counter
from io import BytesIO
import base64,csv,hashlib,html,json,zipfile
from PIL import Image,ImageChops,ImageEnhance
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v193_manual33_offline_review'
OUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for c in iter(lambda:f.read(8*1024*1024),b''):h.update(c)
 return h.hexdigest()
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rows=csvrows(R/'review/v192_image_first_TMX_BC_142/CROSSCHECK_142.csv')
pending=[r for r in rows if r['new_provisional_observation']=='0']
assert len(rows)==142 and len(pending)==33
assert len({(r['tile_set_name'],r['local_id']) for r in pending})==33
assert sum(r['A_appearance_confidence']=='low' for r in pending)==23
assert sum(r['A_appearance_confidence']=='none' for r in pending)==10
notes=json.loads((R/'review/v191_reopen142_A_first/MANUAL_A_IMAGE_OBSERVATIONS_142.json').read_text())
note_by_key={(x['tile_set_name'],str(x['local_id'])):x for x in notes['manual_image_notes']}
assert len(note_by_key)==142
occ=csvrows(R/'review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')
occ_index={(r['tile_set_name'],r['local_id']):r for r in occ}
old9=json.loads((R/'review/v175_remaining381_evidence_audit/OLD_NINE_UNOBSERVED.json').read_text())
old_index={(x['tile_set_name'],str(x['local_id'])):x['source_catalog_record'] for x in old9}
assert len(old_index)==9
m182=json.loads((R/'review/v182_occlusion202/MANIFEST.json').read_text())
m192=json.loads((R/'review/v192_image_first_TMX_BC_142/MANIFEST.json').read_text())
assert m192['image_observed_now']==10007 and m192['physical_unique_unobserved_remaining']==33
assert m182['source_new_key_unobserved_before']==202
zip_path=OUT/'수동검수_33종_오프라인_패키지.zip'
target_html=OUT/'PZ_남은33종_수동검수.html'
target_csv=OUT/'수동검수_33종_입력양식.csv'
target_json=OUT/'수동검수_33종_입력양식.json'
review=[]
# B/C images are *actual original full-layer true TMX* from v182, not
# artificially masked diagnostic X/Y, and may be visually fully occluded.
with zipfile.ZipFile(BytesIO(b''.join((R/'review/v182_occlusion202'/p).read_bytes()
 for p in m182['evidence_zip_parts']))) as archive:
 assert archive.testzip() is None and len(archive.namelist())==6*201
 for rec in pending:
  key=(rec['tile_set_name'],rec['local_id'])
  is_a=rec['A_appearance_confidence']=='low'
  n=note_by_key[key]
  blob=dict(id=key[0]+'::'+key[1],name=key[0],local_id=int(key[1]),
   source_index=int(rec['index']) if rec['index'] else None,
   source_type='원본 A 검증됨' if is_a else '정확한 A 출처 없음',
   old_catalog=rec['origin']=='original_5409',
   A_description=rec['A_direct_visible_description'] or '',
   source_png=rec['original_A_PNG'] or '',
   original_A_sha256=rec['original_A_RGBA_sha256'] or '',
   original_tmx=rec['actual_TMX'] or '',
   original_layer=rec['source_layer'] or '',
   original_level=rec['source_level'] or '',
   x=rec['source_x'] or '',y=rec['source_y'] or '',
   raw_gid=rec['raw_gid'] or '',
   changed_pixels=int(rec['true_original_B_C_changed_pixels']) if rec['true_original_B_C_changed_pixels'] else None,
   original_missing_neighbors=int(rec['original_missing_neighbor_sprites']) if rec['original_missing_neighbor_sprites'] else None,
   prior_reason=rec['previous_exclusion_reason'],images={},source_note='',
   previous_user_candidate='',previous_user_action='',previous_occurrences=None)
  if not is_a:
   if key in old_index:
    x=old_index[key]
    blob['previous_user_candidate']=x.get('v113_user_candidate','')
    blob['previous_user_action']=x.get('v113_user_review_action','')
    blob['previous_occurrences']=x.get('occurrence_count')
    blob['source_note']='옛 타일 DB 기록만 있음. 공식 PNG와 Local ID 크롭을 검증하지 못했으므로 이미지를 추정하여 표시하지 않음.'
   else:
    assert rec['tile_set_name']=='overlay_graffiti_wall_02' and rec['local_id']=='2'
    blob['source_note']='새 타일 중 원본 A 이미지 자체가 누락된 1종. 공식 원본 PNG/크롭을 확보해야 검수 가능.'
  else:
   idx=int(rec['index'])
   assert key in occ_index and int(occ_index[key]['index'])==idx
   assert rec['A_image_status']=='verified_exact_selected_original_A_RGBA_and_visible'
   base=str(idx).zfill(5)+'/'
   def read_png(fname,mode):
    with Image.open(BytesIO(archive.read(base+fname))) as im:return im.convert(mode)
   A=read_png('A_original.png','RGBA')
   B=read_png('B_true_TMX.png','RGB')
   C=read_png('C_true_TMX_target_removed.png','RGB')
   assert A.size[0]>0 and A.size[1]>0
   assert sha(A.tobytes())==rec['original_A_RGBA_sha256'],('original_A_pixel_mismatch',idx)
   assert B.size==C.size==(800,580),('actual_context_size',idx)
   diff=ImageChops.difference(B,C)
   change=diff.getbbox() is not None
   assert change==(blob['changed_pixels']>0),('B_C_zero_not_matching',idx)
   def data_uri(im,format='PNG',**opts):
    z=BytesIO();im.save(z,format=format,**opts)
    return 'data:image/'+('jpeg' if format=='JPEG' else 'png')+';base64,'+base64.b64encode(z.getvalue()).decode('ascii')
   blob['images']['A']=data_uri(A)
   zoom=A.crop(A.getchannel('A').getbbox())
   zoom.thumbnail((340,400),Image.Resampling.NEAREST)
   blob['images']['A_zoom']=data_uri(zoom)
   for k,im in [('B',B),('C',C)]:
    thumbnail=im.copy();thumbnail.thumbnail((680,500),Image.Resampling.LANCZOS)
    blob['images'][k]=data_uri(thumbnail,format='JPEG',quality=87,optimize=True)
   if change:
    overlay=Image.new('RGB',B.size,(14,20,27))
    mask=ImageChops.difference(B,C).convert('L').point(lambda x:255 if x else 0)
    red=Image.new('RGB',B.size,(255,89,82))
    overlay.paste(red,(0,0),mask)
    overlay.thumbnail((680,500),Image.Resampling.LANCZOS)
    blob['images']['diff']=data_uri(overlay)
   else:blob['images']['diff']=None
   blob['source_note']='A=실제 출처 검증 PNG. B=TMX 원래 배치. C=B에서 대상 raw GID 1개 제거. B/C는 v182 실제 원본 장면의 축소 미리보기. 레이어를 가린 X/Y 진단 이미지는 사용하지 않았음.'
  review.append(blob)
assert len(review)==33 and sum(bool(x['images'].get('A')) for x in review)==23
assert sum(x['old_catalog'] for x in review)==9
assert sum(x['changed_pixels']==0 for x in review if x['changed_pixels'] is not None)==16
print('sourced 33; available original actual B/C',sum(bool(x['images']) for x in review),flush=True)
# Do not write image data in the CSV template; UI offline HTML has fully embedded
# thumbnails. Exported user's own manual decisions are separate from verified data.
cols=['tile_set_name','local_id','source_A_status','A_appearance_reference','original_TMX','layer','level','x','y','B_C_changed_pixels','status','manual_identity_candidate','part_role','material','orientation_or_connections','confidence','reason_and_evidence','requested_new_source','final_certified']
with target_csv.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for r in review:w.writerow(dict(tile_set_name=r['name'],local_id=r['local_id'],
  source_A_status=r['source_type'],A_appearance_reference=r['A_description'],
  original_TMX=r['original_tmx'],layer=r['original_layer'],level=r['original_level'],
  x=r['x'],y=r['y'],B_C_changed_pixels=r['changed_pixels'] if r['changed_pixels'] is not None else '',
  status='미판정',manual_identity_candidate='',part_role='',material='',
  orientation_or_connections='',confidence='미정',reason_and_evidence='',
  requested_new_source='',final_certified=0))
template={'schema':'PZ_manual33_review_v193','source':'v192 original pending 33 actual tile keys',
 'official_certification':0,'manual_decisions':{
  r['id']:dict(status='미판정',candidate='',part='',material='',orientation='',confidence='미정',evidence='',source_request='',user_image='') for r in review}}
target_json.write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Actual self-contained HTML, works with no network. All source images are
# embedded; it is intended to be downloaded and opened in a browser, not rendered
# inside GitHub's text preview.
data=json.dumps(review,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
page=r'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>프로젝트 좀보이드 · 남은 33종 수동 검수</title>
<style>
:root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#dce7f4;background:#101a2b}
*{box-sizing:border-box}body{margin:0}.shell{max-width:1500px;margin:auto;padding:22px}
h1{font-size:29px;margin:0 0 8px}.sub{color:#a7bcd3;line-height:1.6}.note{background:#24334b;border:1px solid #47617a;border-radius:12px;padding:14px;margin:12px 0}
.stats,.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:15px 0}
.stats .stat{background:#1c2c43;border-radius:12px;padding:12px 18px;min-width:155px}.num{font-size:24px;font-weight:800}
button,select,input,textarea{background:#15233a;color:#e9f4ff;border:1px solid #516883;border-radius:9px;padding:10px;font:inherit}
button{cursor:pointer}button:hover{background:#254164}button.primary{background:#316da5;border-color:#4d91c8}
button:disabled{opacity:.45;cursor:not-allowed}.input{flex:1;min-width:190px}.status{font-weight:700;color:#b4f5d0}
.main{display:grid;grid-template-columns:290px minmax(0,1fr);gap:16px}
.sidebar{background:#162339;padding:12px;border-radius:13px;max-height:78vh;overflow:auto;position:sticky;top:8px}
.item{padding:11px;border:1px solid #3d536c;border-radius:8px;margin:5px 0;cursor:pointer;font-size:12px;overflow-wrap:anywhere}
.item.active{background:#365474;border-color:#71b3e8}.item small{display:block;color:#a0b8d3;margin-top:5px}
.detail{min-width:0;background:#17283e;border-radius:14px;padding:18px}
.meta{color:#b4c7dd;font-size:13px;line-height:1.8;overflow-wrap:anywhere}
.tag{border:1px solid #5f7997;border-radius:6px;padding:3px 7px;font-size:12px;display:inline-block;margin:3px}
.evidence{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0}
.figure{background:#e5eaf0;border-radius:10px;min-height:160px;display:flex;flex-direction:column;overflow:hidden}
.figure .label{background:#293f5e;color:#e4effc;padding:8px;font-weight:bold;font-size:13px}
.figure img{display:block;max-width:100%;width:100%;height:245px;object-fit:contain;padding:12px;image-rendering:auto}
.figure.alpha{background:repeating-conic-gradient(#cdd9e7 0 25%,#eff3f8 0 50%) 50%/20px 20px}
.figure .empty{color:#344256;padding:35px 15px;text-align:center;line-height:1.7;font-size:13px}
fieldset{border:1px solid #4f6986;border-radius:10px;margin:12px 0;padding:12px}
legend{color:#9cc6eb;padding:0 8px;font-weight:700}
.fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.field{display:flex;flex-direction:column;gap:6px}.field label{font-size:13px;color:#bed1e7}
.field input,.field select,.field textarea{width:100%}.wide{grid-column:1/-1}
nav{display:flex;justify-content:space-between;gap:8px;margin-top:14px}
.warn{color:#ffcb9b}.small{font-size:12px;color:#adc2dc}hr{border:0;border-top:1px solid #39516c;margin:14px 0}
@media(max-width:900px){.main{grid-template-columns:1fr}.sidebar{max-height:170px;position:static;display:flex;overflow-x:auto;gap:8px}.item{min-width:165px}.evidence{grid-template-columns:1fr}.fields{grid-template-columns:1fr}}
</style></head>
<body><div class="shell">
<h1>프로젝트 좀보이드 B42 · 남은 33종 수동 검수</h1>
<p class="sub">v192 원본 근거 기준 · 23종 원본 A 이미지 + 실제 TMX B/C · 10종 원본 A 미확인 · 2건의 과거 집계 불일치는 실제 타일 ID가 없어 제외</p>
<div class="note"><b>검수 원칙</b> — A 원본 이미지 자체를 우선 판단하세요. 원본 B−C=0은 다른 레이어에 가려져 있다는 뜻일 수 있으며, 투명·무의미하다는 증거가 아닙니다. 이 화면의 결과는 <b>사용자 수동 판정</b>으로, 공식 TileZed/Local ID 인증이나 GitHub DB에 자동 반영되지 않습니다. 완료 후 JSON 또는 CSV를 내려받아 이 대화에 올려주세요.</div>
<div class="stats"><div class="stat"><div class="small">전체 대상</div><div class="num">33종</div></div><div class="stat"><div class="small">사용자 검토 완료</div><div class="num" id="countDone">0 / 33</div></div><div class="stat"><div class="small">잠정 후보 선택</div><div class="num" id="countProvisional">0</div></div><div class="stat"><div class="small">보류 / 자료 필요</div><div class="num" id="countHeld">0</div></div></div>
<div class="controls">
<input id="search" class="input" placeholder="타일셋·ID·외형 설명 검색">
<select id="filter"><option value="all">전체 33종</option><option value="undone">미판정</option><option value="source">원본 A 미확보 10종</option><option value="available">원본 A 확인된 23종</option><option value="done">판정 입력됨</option><option value="hold">보류 및 추가 자료 필요</option></select>
<button class="primary" id="exportJson">판정 JSON 저장</button>
<button id="exportCsv">판정 CSV 저장</button>
<button id="importBtn">기존 JSON 불러오기</button><input type="file" accept=".json,application/json" id="importFile" style="display:none">
<button id="clearAll">내 입력 초기화</button>
</div>
<div class="main"><aside class="sidebar" id="sidebar"></aside><main class="detail" id="detail"></main></div>
<p class="small">원본 A 이미지/실제 B/C 미리보기 포함. 원본 증거: v191·v182·v192. 데이터는 이 컴퓨터의 브라우저 로컬 저장소에 저장되며, 직접 JSON/CSV 내보내기를 해야 안전하게 옮길 수 있습니다. 서버로 전송하지 않습니다.</p>
</div>
<script id="source-data" type="application/json">__PAYLOAD__</script>
<script>
(function(){
"use strict";
const tiles=JSON.parse(document.getElementById("source-data").textContent);
const statuses=["미판정","잠정 후보","보류","추가 자료 필요"];
const levels=["미정","낮음","보통","높음"];
const storageKey="PZ_v193_manual33_draft_20261028";
const defaultDecision=()=>({status:"미판정",candidate:"",part:"",material:"",orientation:"",confidence:"미정",evidence:"",source_request:"",user_image:""});
let decisions={};
try{decisions=JSON.parse(localStorage.getItem(storageKey)||"{}")||{}}catch(e){decisions={}}
tiles.forEach(t=>{if(!decisions[t.id])decisions[t.id]=defaultDecision()});
let selected=0;
function escape(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function save(){try{localStorage.setItem(storageKey,JSON.stringify(decisions))}catch(e){alert("브라우저 저장 공간이 부족합니다. JSON을 내려받아 보관하세요.")}stats()}
function stats(){
let d=tiles.filter(t=>decisions[t.id].status!=="미판정").length,p=tiles.filter(t=>decisions[t.id].status==="잠정 후보").length;
document.getElementById("countDone").textContent=d+" / 33";
document.getElementById("countProvisional").textContent=p;
document.getElementById("countHeld").textContent=tiles.filter(t=>["보류","추가 자료 필요"].includes(decisions[t.id].status)).length}
function visible(t){let q=document.getElementById("search").value.toLowerCase(),f=document.getElementById("filter").value,d=decisions[t.id];if(q&&!(t.name+"/"+t.local_id+" "+t.A_description).toLowerCase().includes(q))return false;
return f==="all"||f==="undone"&&d.status==="미판정"||f==="done"&&d.status!=="미판정"||f==="hold"&&["보류","추가 자료 필요"].includes(d.status)||f==="source"&&!t.images.A||f==="available"&&!!t.images.A}
function sidebar(){
let el=document.getElementById("sidebar");el.innerHTML="";
tiles.forEach((t,i)=>{if(!visible(t))return;
const div=document.createElement("div");div.className="item"+(selected===i?" active":"");
div.innerHTML="<b>"+escape(t.name)+" / "+t.local_id+"</b><small>"+(t.images.A?"A 확인됨":"A 미확인")+" · "+escape(decisions[t.id].status)+"</small>";
div.onclick=()=>{selected=i;render()};el.appendChild(div)})}
function imageFrame(name,src,transparent=false,emptyText="증거 이미지 없음"){
return '<div class="figure '+(transparent?'alpha':'')+'"><div class="label">'+escape(name)+'</div>'+(src?'<img loading="lazy" src="'+src+'" alt="'+escape(name)+'">':'<div class="empty">'+escape(emptyText)+'</div>')+'</div>'}
function field(label,key,kind="text"){
let d=decisions[tiles[selected].id];
if(kind==="textarea")return '<div class="field wide"><label>'+escape(label)+'</label><textarea rows="3" data-key="'+key+'">'+escape(d[key])+'</textarea></div>';
if(kind==="status")return '<div class="field"><label>'+escape(label)+'</label><select data-key="'+key+'">'+statuses.map(x=>'<option '+(x===d[key]?"selected":"")+'>'+x+'</option>').join("")+'</select></div>';
if(kind==="confidence")return '<div class="field"><label>'+escape(label)+'</label><select data-key="'+key+'">'+levels.map(x=>'<option '+(x===d[key]?"selected":"")+'>'+x+'</option>').join("")+'</select></div>';
return '<div class="field"><label>'+escape(label)+'</label><input data-key="'+key+'" value="'+escape(d[key])+'"></div>'}
function render(){
sidebar();let t=tiles[selected],d=decisions[t.id];const imgs=t.images;
let h='<h2>검수 '+(selected+1)+'/33 · '+escape(t.name)+' <span class="tag">ID '+t.local_id+'</span></h2>';
h+='<p class="meta">원본 A 상태: <b>'+escape(t.source_type)+'</b> | 이전 보류: '+escape(t.prior_reason)+'<br>v191 A 외형 참고: '+escape(t.A_description||"원본 A가 검증되지 않아 판정 불가")+'</p>';
h+='<p class="meta">원본 TMX: '+escape(t.original_tmx||"없음")+' · 층 '+escape(t.original_level||"—")+' · 레이어 '+escape(t.original_layer||"—")+' · 좌표 ('+escape(t.x||"—")+','+escape(t.y||"—")+') · raw GID '+escape(t.raw_gid||"—")+'<br>실제 B−C 변화: <b>'+escape(t.changed_pixels===null?"측정 불가":t.changed_pixels+'픽셀')+'</b> | 원본 주변 누락: '+escape(t.original_missing_neighbors===null?"정보 없음":t.original_missing_neighbors)+'</p>';
h+='<p class="small">'+escape(t.source_note)+'</p>';
if(t.changed_pixels===0)h+='<p class="note warn">원본 B−C=0: 대상 타일이 가려졌을 수 있습니다. A 자체와 같은 타일셋의 다른 조각을 근거로만 판단하세요.</p>';
if(t.old_catalog)h+='<p class="note warn">옛 타일 ID: 정확한 원본 A 크롭·공식 매핑 없음. 과거 사용자 메모: '+escape(t.previous_user_candidate||"없음")+' | 이전 처리: '+escape(t.previous_user_action||"없음")+'</p>';
h+='<div class="evidence">';
h+=imageFrame("A · 원본 픽셀 (출처 검증)",imgs.A,true,"검증된 원본 A 이미지 없음");
h+=imageFrame("A · 비투명 영역 확대 (동일 픽셀)",imgs.A_zoom,true,"정확한 A 크롭 확보 필요");
h+=imageFrame("B · 실제 TMX 원래 장면 (축소)",imgs.B,false,"실제 TMX 장면 미확보");
h+=imageFrame("C · 대상 GID 하나 제거 (축소)",imgs.C,false,"C 원본 증거 미확보");
h+=imageFrame("B−C · 변화 영역 강조",imgs.diff,false,t.changed_pixels===0?"실제 B−C 변화 0픽셀":"증거 없음");
h+=imageFrame("직접 추가한 검수 이미지",d.user_image,true,"새 A 사진이 있다면 아래에서 첨부 가능");
h+='</div><fieldset><legend>내 수동 검수 입력 (자동 저장)</legend><div class="fields">';
h+=field("판정 상태","status","status")+field("내 확신도","confidence","confidence")+field("사물 / 부품 정체 후보","candidate")+field("부품 역할","part")+field("재질","material")+field("방향·연결 관계","orientation");
h+=field("원본 A 또는 B/C를 보고 판단한 근거","evidence","textarea");
h+=field("추가로 필요한 PNG·TMX 자료","source_request","textarea");
h+='</div><p class="small">직접 추가할 A 이미지(선택): <input type="file" id="customImage" accept="image/*"> 공식 매핑 검증을 대체하지 않습니다.</p></fieldset>';
h+='<nav><button id="prev" '+(selected===0?"disabled":"")+'>← 이전 타일</button><button class="primary" id="next" '+(selected===tiles.length-1?"disabled":"")+'>다음 타일 →</button></nav>';
const detail=document.getElementById("detail");detail.innerHTML=h;
detail.querySelectorAll("[data-key]").forEach(el=>{el.onchange=()=>{decisions[t.id][el.dataset.key]=el.value;save();sidebar()};el.oninput=()=>{decisions[t.id][el.dataset.key]=el.value;save()}});
document.getElementById("prev").onclick=()=>{selected=Math.max(0,selected-1);render()};
document.getElementById("next").onclick=()=>{selected=Math.min(tiles.length-1,selected+1);render()};
document.getElementById("customImage").onchange=ev=>{const f=ev.target.files?.[0];if(!f)return;if(f.size>2500000){alert("2.5MB 이하 사진만 추가하세요.");return}
const fr=new FileReader();fr.onload=()=>{decisions[t.id].user_image=String(fr.result);save();render()};fr.readAsDataURL(f)};
stats()}
function download(name,content,mime){const blob=new Blob([content],{type:mime}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000)}
document.getElementById("exportJson").onclick=()=>download("PZ_33종_수동판정.json",JSON.stringify({schema:"PZ_manual33_review_v193",source:"v192",exported_at:new Date().toISOString(),official_mapping_verified:0,certified:0,manual_decisions:decisions},null,2),"application/json;charset=utf-8");
document.getElementById("exportCsv").onclick=()=>{let head=["tile_set_name","local_id","status","candidate","part","material","orientation","confidence","evidence","source_request","official_mapping_verified","certified"];let a=[head];tiles.forEach(t=>{let d=decisions[t.id];a.push([t.name,t.local_id,d.status,d.candidate,d.part,d.material,d.orientation,d.confidence,d.evidence,d.source_request,0,0])});const esc=x=>'"'+String(x??"").replace(/"/g,'""')+'"';download("PZ_33종_수동판정.csv","\uFEFF"+a.map(r=>r.map(esc).join(",")).join("\r\n"),"text/csv;charset=utf-8")};
document.getElementById("importBtn").onclick=()=>document.getElementById("importFile").click();
document.getElementById("importFile").onchange=ev=>{let f=ev.target.files[0];if(!f)return;const fr=new FileReader();fr.onload=()=>{try{const a=JSON.parse(String(fr.result));if(a.schema!=="PZ_manual33_review_v193"||!a.manual_decisions)throw Error("다른 양식입니다");tiles.forEach(t=>{if(a.manual_decisions[t.id])decisions[t.id]=Object.assign(defaultDecision(),a.manual_decisions[t.id])});save();render();alert("판정 데이터를 불러왔습니다.")}catch(e){alert("불러오기 실패: "+e.message)}};fr.readAsText(f)};
document.getElementById("clearAll").onclick=()=>{if(confirm("33종의 작성한 모든 판정 내용을 초기화할까요?")){decisions={};tiles.forEach(t=>decisions[t.id]=defaultDecision());save();render()}};
document.getElementById("search").oninput=sidebar;
document.getElementById("filter").onchange=sidebar;
render();
})();
</script></body></html>'''
page=page.replace('__PAYLOAD__',data)
target_html.write_text(page,encoding='utf-8')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in [target_html,target_csv,target_json]:z.write(f,arcname=f.name)
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None and len(z.namelist())==3
manifest=dict(version='v193',scope='offline standalone browser user-manual review 33 actual remaining tile keys',
 source_checkpoint='v192',actual_key_count=33,verified_A_and_real_B_C=23,no_exact_A_or_scene=10,
 unresolved_count_gap_not_keys=2,prior_reviewed_observed=10007,prior_remaining_checkpoint=35,
 number_already_certified=0,number_auto_promoted=0,
 html_file=target_html.name,html_bytes=target_html.stat().st_size,html_sha256=filehash(target_html),
 csv_template_file=target_csv.name,json_template_file=target_json.name,zip_file=zip_path.name,
 zip_sha256=filehash(zip_path),zip_bytes=zip_path.stat().st_size,
 image_count=sum(len([k for k,v in t['images'].items() if v]) for t in review),
 B_C_zero_count=sum(x['changed_pixels']==0 for x in review),
 B_C_positive_count=sum(x['changed_pixels']>0 for x in review if x['changed_pixels'] is not None),
 source_zip_sha256=m182['image_evidence_zip_sha256'],
 review_records_sha256=sha(json.dumps([t['id'] for t in review],ensure_ascii=False).encode()))
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'README.md').write_text(
 '# 남은 실제 타일 33종 수동 검수 패키지\n\n'
 '1. \`수동검수_33종_오프라인_패키지.zip\`을 다운로드해 압축을 푸세요.\n'
 '2. \`PZ_남은33종_수동검수.html\`을 Chrome/Edge로 열면 인터넷 없이 원본 A 23개와 실제 TMX B·C 장면을 함께 검수할 수 있습니다.\n'
 '3. 나머지 10개는 정확한 원본 A가 검증되지 않았기 때문에 임의 이미지를 넣지 않았고, 원본을 직접 첨부할 수 있는 칸을 제공합니다.\n'
 '4. 사용자 판정(잠정 후보/보류/자료필요), 이름, 역할, 재질, 방향, 근거를 입력한 뒤 **JSON 저장**으로 결과를 보관하여 채팅에 업로드하세요. 선택으로 CSV 저장 가능.\n'
 '5. 판정 데이터는 이 컴퓨터의 브라우저 로컬 저장소에 임시 보관됩니다. 다른 기기에서 이어할 때는 JSON 불러오기를 사용하세요.\n'
 '6. HTML에 직접 포함된 B/C는 실제 원본 TMX 장면의 축소 미리보기입니다. 레이어 마스킹 진단 X/Y와 다릅니다. B−C=0이라도 원본 A 판독은 유효한 보조 근거입니다.\n'
 '7. 33종 검수 양식은 사용자 참여용이며, 원본 SQLite·PROJECT_STATE·기존 제외 이력·최종 인증/공식 매핑을 바꾸지 않습니다. 과거 2개 집계불일치는 특정 타일 ID가 아니므로 사용자 검수 33종에 섞지 않았습니다.\n',encoding='utf-8')
print('PASS v193 MANUAL REVIEW KIT',json.dumps(manifest,ensure_ascii=False),flush=True)
