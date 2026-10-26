#!/usr/bin/env python3
"""v118: scope A candidate work to ONLY 4,633 new TMX keys; preserve 5,409 historical keys.
Creates a standalone searchable offline gallery of 58 A1/A2/A3 contact sheets,
strictly excluding every old catalog key and all 14 prior manual exclusions.
This is scope preparation, not an AI-certified sprite mapping.
"""
from pathlib import Path
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import csv,hashlib,html,json,math,zipfile
ROOT=Path(__file__).resolve().parents[1]
ORIG=ROOT/'review/v117_A_candidates_10042'
OUT=ROOT/'review/v118_A_new_only_4633'
SHEETS=OUT/'sheets'
OUT.mkdir(parents=True,exist_ok=True)
SHEETS.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_csv(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def askey(r,a='tile_set_name'):return(r[a],int(r['local_id']))
source=ORIG/'A_CANDIDATE_COMBINED_10042.csv'
original=read_csv(source)
prior=read_csv(ROOT/'analysis/imports/merged_catalog_5409.csv')
allkeys=[askey(r) for r in original]
oldkeys={askey(r,'tile_set_locator') for r in prior}
assert len(original)==10042 and len(set(allkeys))==10042
assert len(oldkeys)==5409 and oldkeys.issubset(allkeys)
existing=[r for r in original if askey(r) in oldkeys]
new=[r for r in original if askey(r) not in oldkeys]
assert len(existing)==5409 and len(new)==4633
assert sum(int(r['prior_in_5409']) for r in existing)==5409
assert sum(int(r['prior_in_5409']) for r in new)==0
assert all(int(r['user_excluded'])==0 for r in new)
assert sum(int(r['user_excluded']) for r in existing)==14
assert all(askey(r) not in oldkeys for r in new)

# Include only A1/A2/A3 candidate state; preserve old source paths and provisional caveats.
fields=list(original[0])
fields.extend(['active_a_scope','a_stage_status','review_priority','new_sheet','new_sheet_cell'])
decision_priority={
    'proposed_consistent':('ready_for_ai_verification',3),
    'proposed_one_visible_needs_ai':('needs_ai_visual_selection',1),
    'proposed_jumbo_whole_sprite_grid_needs_ai':('needs_ai_jumbo_mapping',0),
    'needs_ai_comparison':('needs_ai_visual_comparison',0),
    'no_visible_candidate':('source_held',0),
    'no_usable_source':('source_held',0)
}
counts=Counter();groups=Counter()
for i,r in enumerate(new):
    status=r['new_candidate_decision']
    if status not in decision_priority:raise AssertionError(f'Unrecognized status {status}')
    step,prio=decision_priority[status]
    r.update(active_a_scope='new_only',a_stage_status=step,review_priority=prio,
             new_sheet=f'sheets/new_A_{i//80:03}.jpg',new_sheet_cell=i%80)
    counts[status]+=1
    groups[r['tile_set_name']]+=1
assert sum(counts.values())==4633
assert len({(r['tile_set_name'],r['local_id']) for r in new})==4633
csvpath=OUT/'A_CANDIDATE_NEW_ONLY_4633.csv'
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(new)

# Produce compact A evidence contact sheets without re-rendering or modifying source A candidates.
# Each 240x165 cell is cropped verbatim from v117's 126 source 80-tile sheets.
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(fontpath,12)
small=ImageFont.truetype(fontpath,10)
A3INDEX={askey(r):i for i,r in enumerate(read_csv(ORIG/'jumbo_a3/A3_CANDIDATES.csv'))}
assert len(A3INDEX)==36
with Image.open(ORIG/'jumbo_a3/A3_JUMBO_review_sheet.jpg') as a3:
    a3gallery=a3.convert('RGB')
sheet_cache={}
def load_sheet(path):
    if path not in sheet_cache:
        with Image.open(ROOT/path) as im:sheet_cache[path]=im.convert('RGB')
    return sheet_cache[path]
def get_A3(key):
    i=A3INDEX[key]
    x=i%6*300;y=i//6*300
    # A3's original user-facing 300x300 card with whole-tree provisional source.
    crop=a3gallery.crop((x,y,x+300,y+300))
    tile=Image.new('RGB',(240,165),(250,245,233))
    dr=ImageDraw.Draw(tile)
    dr.text((7,5),'A3: provisional JUMBO',font=small,fill=(118,62,17))
    crop=crop.crop((35,56,265,225))
    crop.thumbnail((234,134),Image.Resampling.LANCZOS)
    tile.paste(crop,((240-crop.width)//2,26+(134-crop.height)//2))
    dr.text((7,148),'Local ID mapping UNVERIFIED',font=small,fill=(121,70,21))
    return tile
num_sheets=math.ceil(len(new)/80)
assert num_sheets==58
rendered=0;render_a3=0
for sn in range(num_sheets):
    board=Image.new('RGB',(1920,1650),(233,240,247))
    for pos,r in enumerate(new[sn*80:(sn+1)*80]):
        ox=(pos%8)*240;oy=(pos//8)*165
        key=askey(r)
        if r['new_preferred_A']=='A3':
            tile=get_A3(key);render_a3+=1
        else:
            path=r['source_hypothesis_sheet']
            src=load_sheet(path)
            loc=int(r['sheet_cell'])
            x=(loc%8)*240;y=(loc//8)*165
            tile=src.crop((x,y,x+240,y+165))
        board.paste(tile,(ox,oy))
        rendered+=1
    board.save(SHEETS/f'new_A_{sn:03}.jpg',quality=86,optimize=True)
    if (sn+1)%10==0:print('SHEETS',sn+1,'/',num_sheets,flush=True)
    # Minimize peak RSS: only 1-2 old sheets relevant to each new 80 tiles.
    sheet_cache.clear()
assert rendered==4633
assert render_a3==counts['proposed_jumbo_whole_sprite_grid_needs_ai']

# Portable HTML index with only NEW 4,633; no old cards even under search.
indices=[[r['tile_set_name'],int(r['local_id']),r['new_preferred_A'],
          r['new_candidate_decision'],int(r['review_priority']),
          int(r['new_sheet'].split('_')[-1].split('.')[0]),
          int(r['new_sheet_cell'])] for r in new]
page=r"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PZ B42 신규 A 후보 4633종</title><style>
body{font:14px system-ui,'Malgun Gothic',sans-serif;margin:0;background:#f3f6f9;color:#25364b}
header{padding:24px;background:#153047;color:white}h1{margin:0 0 7px;font-size:22px}
main{max-width:1600px;padding:14px;margin:auto}.panel{background:white;margin:10px 0;padding:14px;border-radius:9px}
.row{display:flex;gap:9px;align-items:center;flex-wrap:wrap}
input,select,button{padding:8px;font:inherit;border:1px solid #bbcad7;border-radius:5px}
button{background:#eef4f7;cursor:pointer}#viewer{width:100%;max-height:75vh;object-fit:contain;border:1px solid #c1d1db}
table{border-collapse:collapse;width:100%;font-size:12px}td,th{padding:8px;border-bottom:1px solid #edf1f5;text-align:left}
a{color:#076e8b}.note{color:#586d81}#pager{margin-bottom:10px}
</style></head><body>
<header><h1>신규 타일 A 후보 · 4,633종 전용 검토판</h1>
기존 5,409종 제외 · A1(TMX) / A2(TileZed) / A3(JUMBO 잠정) · 공식 Local ID 인증 아님</header>
<main><section class="panel">
<strong>신규 4,633종만 표시합니다.</strong>
<p class="note">기존 검수 5,409종과 사용자 제외 14종은 이 검토판에 나타나지 않습니다. 대표 A가 기계적으로 제안됐어도 AI 및 공식 매핑 검증은 별도로 필요합니다.</p>
<div class="row"><input id="query" placeholder="타일셋 이름 / Local ID 검색" size="40">
<select id="status"><option value="">전체 후보</option><option value="proposed_consistent">A1=A2 동일</option>
<option value="proposed_one_visible_needs_ai">단일 가시 A</option><option value="proposed_jumbo_whole_sprite_grid_needs_ai">A3 JUMBO</option>
<option value="no_visible_candidate">가시 후보 없음</option><option value="no_usable_source">PNG/격자 문제</option></select>
<span id="count"></span></div></section>
<section class="panel"><div id="pager" class="row">
<button id="prev">이전 이미지 시트</button><b id="label"></b><button id="next">다음 이미지 시트</button>
<a id="open" target="_blank" rel="noopener">원본 이미지 열기</a>
</div><img id="viewer" src="sheets/new_A_000.jpg" alt="신규 A 후보 비교 이미지">
<p class="note">이미지 한 장에 최대 80종. A3는 임시 JUMBO 전체 나무 스프라이트 구간이므로 Local ID 검증 전에 확정하지 마세요.</p>
</section><section class="panel"><table><thead><tr><th>타일셋</th><th>Local ID</th><th>제안 A</th><th>상태</th><th>위치</th></tr></thead>
<tbody id="rows"></tbody></table><button id="more">50개 더 보기</button></section>
</main><script>
const D=__ROWS__;let filtered=D,shown=50,current=0;
const g=id=>document.getElementById(id);
function showSheet(n){current=Math.min(57,Math.max(0,n));let path='sheets/new_A_'+String(current).padStart(3,'0')+'.jpg';
g('label').textContent=path+' / 58개';g('viewer').src=path;g('open').href=path;}
function update(){
 const q=g('query').value.trim().toLowerCase(),s=g('status').value;
 filtered=D.filter(x=>(!q||x[0].toLowerCase().includes(q)||String(x[1]).includes(q))&&(!s||x[3]===s));
 g('count').textContent=filtered.length.toLocaleString('ko-KR')+' / 4,633종';
 let tbody=g('rows');tbody.replaceChildren();
 for(const x of filtered.slice(0,shown)){
 const tr=document.createElement('tr');
 for(const t of [x[0],x[1],x[2],x[3]]){const td=document.createElement('td');td.textContent=t;tr.append(td);}
 const td=document.createElement('td');const btn=document.createElement('button');
 btn.textContent='A_'+String(x[5]).padStart(3,'0')+' · #'+x[6];btn.onclick=()=>{showSheet(x[5]);g('viewer').scrollIntoView({behavior:'smooth'})};
 td.append(btn);tr.append(td);tbody.append(tr);
 }
 g('more').disabled=shown>=filtered.length;
}
g('query').oninput=g('status').onchange=()=>{shown=50;update()};
g('more').onclick=()=>{shown+=50;update()};
g('prev').onclick=()=>showSheet(current-1);g('next').onclick=()=>showSheet(current+1);
showSheet(0);update();
</script></body></html>"""
index=OUT/'NEW_ONLY_A_4633_VIEWER.html'
index.write_text(page.replace('__ROWS__',json.dumps(indices,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')),encoding='utf8')

unresolved=new and [r for r in new if r['new_candidate_decision'] in ('no_visible_candidate','no_usable_source')]
with (OUT/'UNRESOLVED_NEW_ONLY.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(unresolved)
summary=dict(
version='v118',kind='A_stage_new_only_scope',scope='26_43_through_37_49',
total_range_tile_keys=10042,reused_old_unchanged=5409,new_only_active=4633,
excluded_prior_manual_keys_in_active=0,prior_manual_exclusions_kept=14,
new_only_status_counts=dict(counts),
new_only_visible_A=4633-len(unresolved),
new_only_unresolved=len(unresolved),
new_only_sheet_count=58,
new_only_sprite_cards_rendered=rendered,
new_only_A3_cards_rendered=render_a3,
new_only_tileset_count=len(groups),
full_source_ledger='review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv',
source_sha256=sha(source),
master_new_only_csv=str(csvpath.relative_to(ROOT)),
master_new_only_sha256=sha(csvpath),
review_viewer=str(index.relative_to(ROOT)),
review_viewer_sha256=sha(index),
review_sheets=str(SHEETS.relative_to(ROOT)),
frozen_previous_analysis_version='v116',
existing_keys_must_not_be_rerun=True,
AI_per_key_A_selection_verified=0,official_mapping_verified=0,
final_identity_certified=0,
note='Scope exclusion means 5409 old keys do not appear in active NEW A worklist; historical v116 SQLite and v117 full ledger preserved, no transparency or identity certification.'
)
manifest=OUT/'SUMMARY.json';manifest.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
readme=OUT/'README_사용법.txt'
readme.write_text('B42 신규 A 후보 검토용 - 기존 5,409종 제외, 신규 4,633종 전용.\n'
'NEW_ONLY_A_4633_VIEWER.html을 실행해 새 타일만 검색합니다.\n'
'이미지는 sheets/new_A_000.jpg부터 57까지 총 58장입니다.\n'
'A_CANDIDATE_NEW_ONLY_4633.csv는 각 후보 A1/A2/A3 출처·Local ID·검토 우선순위입니다.\n'
'후보 추출과 AI의 시각 대응 검증은 구분합니다. 공식 매핑 인증 0종입니다.\n'
'이 4633종은 이번 A단계 새 분석 대상으로 정리한 것이며, 기존 5409종 자료는 보존되어 있습니다.\n',encoding='utf8')
archive=OUT/'PZ_신규4633종_A후보_검토자료.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in [index,csvpath,OUT/'UNRESOLVED_NEW_ONLY.csv',readme,manifest,*sorted(SHEETS.glob('new_A_*.jpg'))]:
        z.write(f,arcname=f.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==63
summary['zip_sha256']=sha(archive)
summary['zip_crc']='PASS'
summary['zip_entries']=63
summary['zip_size_bytes']=archive.stat().st_size
manifest.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
# Self-referential ZIP manifest contains original summary without own SHA; external SUMMARY is final.
print('PASS v118 NEW-ONLY',json.dumps({
 'total':len(original),'old':len(existing),'new':len(new),
 'states':dict(counts),'unresolved':len(unresolved),
 'sheets':num_sheets,'archive_bytes':archive.stat().st_size,'zip_crc':'PASS',
 'a3_tiles':render_a3},ensure_ascii=False),flush=True)
