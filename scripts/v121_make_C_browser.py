#!/usr/bin/env python3
"""Create offline browser for B / C / B-C panels; JSON data embedded locally."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'review/v121_C_diff_new4632'
with (OUT/'C_B_DIFFERENCE_4632.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==4632
data=[[r['tile_set_name'],int(r['local_id']),r['tmx_file'],int(r['source_level']),
       int(r['source_x']),int(r['source_y']),int(r['B_minus_C_changed_pixels']),
       int(r['source_neighbor_skipped_B']),int(r['C_sheet_slot']),
       int(r['C_contact_sheet'].split('_')[-1].split('.')[0]),
       r['source_layer'],r['B_minus_C_bbox']]
      for r in rows]
html="""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>B / C / B-C 비교 · 신규 4632종</title><style>
body{margin:0;background:#f1f4f8;font:14px system-ui,sans-serif;color:#283a4c}
header{background:#193348;color:#fff;padding:22px}h1{margin:0 0 6px;font-size:23px}
main{margin:auto;max-width:1550px;padding:12px}.panel{background:white;border-radius:9px;padding:13px;margin:12px 0}
.row{display:flex;gap:9px;align-items:center;flex-wrap:wrap}
button,input,select{padding:8px;border-radius:6px;border:1px solid #b8c9d6;font:inherit;background:white}
button{cursor:pointer}#sheet{max-width:100%;max-height:76vh;object-fit:contain;border:1px solid #cad8e1}
#focus{width:450px;height:205px;max-width:100%;background-repeat:no-repeat;border:1px solid #a8bac8}
table{border-collapse:collapse;width:100%;font-size:12px}td,th{text-align:left;padding:8px;border-bottom:1px solid #e5eaf0}
.warning{background:#fff3dc;border-left:3px solid #c77d2b;padding:10px}
</style></head><body>
<header><h1>C단계 · 신규 4,632종 B/C/B−C 비교</h1>실제 TMX의 층·레이어·좌표 하나만 제거, 변경 픽셀은 손실 압축 이전에 계산</header>
<main><section class="panel"><div class="row">
<input id="search" placeholder="타일셋 이름 / Local ID / TMX" size="36">
<select id="filter"><option value="">전체</option><option value="zero">B−C 변화 0</option>
<option value="positive">B−C 변화 있음</option><option value="missing">주변 이미지 누락</option></select>
<b id="count"></b></div></section>
<section class="panel"><div class="row"><button id="previous">이전 시트</button>
<b id="sheetname"></b><button id="next">다음 시트</button><a id="full" target="_blank" rel="noopener">접촉시트 원본 보기</a></div>
<img id="sheet" src="sheets/C_B_DIFF_000.jpg" alt="B-before C-after red B-minus-C"/>
<h3>선택 타일 확대 카드 (B, C, 빨간 차이)</h3>
<div id="focus"></div><p id="selected"></p>
<p class="warning">차이가 0인 것은 투명 인증이 아닙니다. 주변 물체에 가렸거나 임시 PNG/Local ID 매핑이 틀렸을 수 있습니다.</p>
</section><section class="panel"><table><thead><tr><th>타일셋</th><th>ID</th><th>TMX</th>
<th>층·좌표</th><th>변화 픽셀</th><th>주변 누락</th><th>비교</th></tr></thead><tbody id="rows"></tbody></table>
<button id="more">50개 더 보기</button></section></main>
<script>
const D=__ROWS__;let filtered=D,count=50,at=0;
const get=id=>document.getElementById(id);
function sheetName(i){return 'C_B_DIFF_'+String(i).padStart(3,'0')+'.jpg'}
function sheet(i){at=Math.max(0,Math.min(57,i));let p='sheets/'+sheetName(at);
get('sheetname').textContent=sheetName(at)+' / 58';get('sheet').src=p;get('full').href=p}
function focus(r){
 sheet(r[9]);const cx=r[8]%8,cy=Math.floor(r[8]/8);
 get('focus').style.backgroundImage='url(sheets/'+sheetName(r[9])+')';
 get('focus').style.backgroundSize='3600px 2050px';
 get('focus').style.backgroundPosition=(-450*cx)+'px '+(-205*cy)+'px';
 get('selected').textContent=r[0]+' / '+r[1]+' | '+r[2]+' L'+r[3]+' ('+r[4]+','+r[5]+
 ') | B-C 픽셀 '+r[6]+' | 레이어 '+r[10]+' | bbox '+(r[11]||'없음');
}
function display(){
 const q=get('search').value.toLowerCase().trim(),f=get('filter').value;
 filtered=D.filter(r=>(!q||r[0].toLowerCase().includes(q)||String(r[1]).includes(q)||r[2].toLowerCase().includes(q))
 &&(!f||f==='zero'&&r[6]===0||f==='positive'&&r[6]>0||f==='missing'&&r[7]>0));
 get('count').textContent=filtered.length.toLocaleString('ko-KR')+' / 4,632종';
 const body=get('rows');body.replaceChildren();
 for(const r of filtered.slice(0,count)){
   const tr=document.createElement('tr');
   for(const v of [r[0],r[1],r[2],'L'+r[3]+' ('+r[4]+','+r[5]+')',r[6],r[7]]){
     const td=document.createElement('td');td.textContent=String(v);tr.append(td)}
   const td=document.createElement('td'),btn=document.createElement('button');
   btn.textContent='선택';btn.onclick=()=>{focus(r);get('focus').scrollIntoView({behavior:'smooth',block:'nearest'})};
   td.append(btn);tr.append(td);body.append(tr)}
 get('more').disabled=count>=filtered.length;
}
get('search').oninput=get('filter').onchange=()=>{count=50;display()};
get('more').onclick=()=>{count+=50;display()};
get('previous').onclick=()=>sheet(at-1);get('next').onclick=()=>sheet(at+1);
sheet(0);focus(D[0]);display();
</script></body></html>"""
page=html.replace('__ROWS__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
out=OUT/'C_B_DIFF_BROWSER_4632.html'
out.write_text(page,encoding='utf8')
print('PASS C B DELTA offline browser',out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest())
