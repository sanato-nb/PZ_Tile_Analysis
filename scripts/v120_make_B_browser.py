#!/usr/bin/env python3
"""Produce standalone offline B scene viewer by embedding the verified 4632 CSV rows.
No browsing network or client CSV fetch; require source B ZIP evidence separately.
"""
from pathlib import Path
import csv,json,hashlib
R=Path(__file__).resolve().parents[1]
P=R/'review/v120_B_context_new4632'
with (P/'B_CONTEXT_4632.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==4632
assert len({(r['tile_set_name'],r['local_id']) for r in rows})==4632
summary=json.loads((P/'MANIFEST.json').read_text('utf8'))
assert summary['B_5x5_rendered']==4632
data=[[r['tile_set_name'],int(r['local_id']),r['tmx_file'],int(r['source_level']),
       int(r['source_x']),int(r['source_y']),int(r['neighbor_tiles_rendered']),
       int(r['neighbor_tiles_skipped']),int(r['scene_truncated_at_map_edge']),
       r['B_contact_sheet'].split('/')[-1],int(r['B_contact_sheet_cell']),
       r['B_zip_shard'].split('/')[-1],r['B_zip_entry']]
      for r in rows]
html=r"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PZ B 신규 4632종 - 실제 TMX 주변 장면</title>
<style>
:root{font-family:system-ui,'Malgun Gothic',sans-serif;color:#26394d;background:#f2f5f9}
*{box-sizing:border-box}body{margin:0}header{background:#182f42;color:white;padding:22px 3vw}
header h1{margin:0 0 8px;font-size:23px}header p{margin:0;color:#c8d8e4}
main{max-width:1660px;margin:10px auto;padding:0 12px}section{background:white;padding:15px;margin:12px 0;border-radius:9px}
button,select,input{font:inherit;padding:9px;border-radius:6px;border:1px solid #b5c8d6;background:white}
button{cursor:pointer}button:disabled{opacity:.45;cursor:default}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.big{font-size:19px;font-weight:800}.muted{color:#556b7e}.layout{display:grid;grid-template-columns:1fr 500px;gap:16px}
#sheet{width:100%;max-height:75vh;object-fit:contain;border:1px solid #cad4dc}
#zoom{width:480px;height:370px;background-repeat:no-repeat;border:2px solid #869cae}
table{border-collapse:collapse;width:100%;font-size:12px}th,td{padding:7px;border-bottom:1px solid #e7edf1;text-align:left}
tr.pick{background:#e7f2fa}th{position:sticky;top:0;background:white}
.wrap{max-height:480px;overflow:auto}.note{background:#fff7df;border-radius:6px;padding:11px}
@media(max-width:1050px){.layout{grid-template-columns:1fr}#zoom{max-width:100%}}
</style></head><body>
<header><h1>신규 4,632종 B · 실제 TMX 5×5 주변 장면</h1>
<p>기존 5,409종 신규 분석에서 제외 · 84개 TMX 원본 기반 · 정체/공식 Local ID 미인증</p></header>
<main><section><div class="row">
<b id="count" class="big"></b><input id="query" size="38" placeholder="타일셋 / Local ID / TMX 31_44 검색">
<select id="filter"><option value="all">전체 장면</option>
<option value="missing">주변 이미지 일부 누락</option>
<option value="edge">지도 가장자리 잘림</option>
<option value="clean">주변 누락 없음</option></select></div>
<p class="muted">이미지는 실제 TMX 배치를 기반으로 한 아이소메트릭 근사 조립입니다. 한 장에 최대 80종. 누락·가림은 투명 타일의 증거가 아닙니다.</p>
</section><section class="layout"><div>
<div class="row"><button id="prev">이전 시트</button><b id="label"></b>
<button id="next">다음 시트</button><a id="open" target="_blank" rel="noopener">접촉시트 원본 열기</a></div>
<img id="sheet" src="sheets/B_5x5_000.jpg" alt="신규 타일 B 주변 장면"/>
</div><div><b>선택 장면 확대 (2배)</b><div id="zoom"></div>
<p id="focus" class="muted"></p>
<div class="note">B는 원본에서 해당 타일을 제거하지 않은 주변 장면입니다. 대상이 벽이나 높은 가구에 가려져 보이지 않을 수 있으며, 제거 비교는 C단계에서 수행합니다. 각 타일의 정확한 원본 좌표와 ZIP 파일명은 아래 표와 CSV에 남아 있습니다.</div>
</div></section>
<section><div class="wrap"><table><thead><tr><th>타일셋</th><th>Local ID</th><th>TMX</th><th>층·좌표</th><th>그린 타일</th><th>누락</th><th>선택</th></tr></thead><tbody id="rows"></tbody></table></div>
<div class="row"><button id="more">50개 더 보기</button></div></section></main>
<script>
const DATA=__ROWS__;
const $=id=>document.getElementById(id);
let filtered=DATA,limit=50,page=0,focused=null;
function sheetFile(p){return 'B_5x5_'+String(p).padStart(3,'0')+'.jpg'}
function changeSheet(p){
page=Math.max(0,Math.min(57,p));const f=sheetFile(page);
$('sheet').src='sheets/'+f;$('label').textContent=f+' / 58장';
$('open').href='sheets/'+f;
}
function focus(row){
focused=row;const index=DATA.indexOf(row);const sheet=Math.floor(index/80);
changeSheet(sheet);
const pos=row[10],col=pos%8,rr=Math.floor(pos/8);
$('zoom').style.backgroundImage='url("sheets/'+sheetFile(sheet)+'")';
$('zoom').style.backgroundSize='3840px 3700px';
$('zoom').style.backgroundPosition=(-col*480)+'px '+(-rr*370)+'px';
$('focus').textContent=row[0]+' / Local ID '+row[1]+' | '+row[2]+' L'+row[3]+' ('+row[4]+','+row[5]+') | 주변 누락 '+row[7]+' | 이미지 '+row[11]+'/'+row[12];
}
function render(){
const query=$('query').value.trim().toLowerCase(),type=$('filter').value;
filtered=DATA.filter(r=>(!query||r[0].toLowerCase().includes(query)||String(r[1]).includes(query)||r[2].toLowerCase().includes(query))
 &&(type==='all'||type==='missing'&&r[7]>0||type==='edge'&&r[8]>0||type==='clean'&&r[7]===0&&r[8]===0));
$('count').textContent=filtered.length.toLocaleString('ko-KR')+' / 4,632종';
$('rows').replaceChildren();
for(const r of filtered.slice(0,limit)){
const tr=document.createElement('tr');if(focused===r)tr.className='pick';
for(const value of [r[0],r[1],r[2],'L'+r[3]+' ('+r[4]+','+r[5]+')',r[6],r[7]]){
const td=document.createElement('td');td.textContent=String(value);tr.append(td);}
const td=document.createElement('td'),btn=document.createElement('button');btn.textContent='B 보기';
btn.onclick=()=>{focus(r);render();$('zoom').scrollIntoView({behavior:'smooth',block:'nearest'})};
td.append(btn);tr.append(td);$('rows').append(tr);
}
$('more').disabled=limit>=filtered.length;
}
$('query').oninput=$('filter').onchange=()=>{limit=50;render()};
$('more').onclick=()=>{limit+=50;render()};
$('prev').onclick=()=>changeSheet(page-1);$('next').onclick=()=>changeSheet(page+1);
changeSheet(0);focus(DATA[0]);render();
</script></body></html>"""
out=P/'B_CONTEXT_4632_BROWSER.html'
out.write_text(html.replace('__ROWS__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')),encoding='utf8')
assert len(data)==4632
print('PASS offline browser B 4632',out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest())
