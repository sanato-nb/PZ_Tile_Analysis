#!/usr/bin/env python3
"""v117 A-candidate atlas for exactly 10,042 DISTINCT B42 TMX used tile keys.
A1 = TMX declared tileset grid; A2 = TileZed tiledefinitions grid.
The *chosen image* is a provisional proposal, never a certified Local ID correspondence.
No claims of AI inspecting 10,042 cropped pictures are made at this mechanical stage.
"""
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
import csv,json,re,hashlib,io,sys,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
TILES=ROOT/'Tiles'
OUT=ROOT/'review/v117_A_candidates_10042'
SHEETS=OUT/'sheets'
OUT.mkdir(parents=True,exist_ok=True);SHEETS.mkdir(parents=True,exist_ok=True)
RANGE=ROOT/'audits/map_range_26_43_to_37_49'
RANGE_REPORT=json.loads((RANGE/'SUMMARY.json').read_text('utf8'))
assert RANGE_REPORT['files_present']==84
assert RANGE_REPORT['distinct_tile_keys_tile_layers']==10042
SOURCE=(RANGE/'DISTINCT_TILE_KEYS.csv')
with SOURCE.open(newline='',encoding='utf-8-sig') as f:target=list(csv.DictReader(f))
assert len(target)==10042
keys={(r['tile_set_name'],int(r['local_id'])) for r in target}
assert len(keys)==10042
assert len({x[0] for x in keys})==322
with (ROOT/'analysis/imports/merged_catalog_5409.csv').open(encoding='utf-8-sig',newline='') as f:
    old=list(csv.DictReader(f))
oldkeys={(r['tile_set_locator'],int(r['local_id'])) for r in old}
assert len(oldkeys)==5409 and oldkeys.issubset(keys)
EXCLUSIONS=set()
for filename in ('checkpoints/v113/user_review.csv','checkpoints/v116/user_exclude_six.csv'):
    with (ROOT/filename).open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            if r['user_action']=='exclude_from_active_review':
                EXCLUSIONS.add((r['tile_set_locator'],int(r['local_id'])))
assert len(EXCLUSIONS)==14 and EXCLUSIONS.issubset(keys)
# One TMX export references 413 atlas definitions; the 322 used tilesets should all
# be listed. Verify keys and image source declarations instead of silently inferring.
tmxroot=ET.parse(ROOT/'B4220.3_MapExport_256/tmx/26_43.tmx').getroot()
decl={}
for t in tmxroot.findall('tileset'):
    im=t.find('image')
    if im is None:continue
    n=t.get('name')
    if n:
        decl[n]=dict(firstgid=int(t.get('firstgid')),
            tilewidth=int(t.get('tilewidth')),tileheight=int(t.get('tileheight')),
            img_width=int(im.get('width','0')),img_height=int(im.get('height','0')),
            img_source=im.get('source',''),columns=int(t.get('columns','0')))
missing_decl=sorted(set(n for n,_ in keys)-set(decl))
assert not missing_decl, 'Used tilesets missing from 26_43 exported definitions: '+str(missing_decl[:20])
# TileZed grid is separate and optional. Size is count of logical atlas columns/rows.
textdef=(TILES/'tiledefinitions.tiles.txt').read_text('utf8')
tiledefs={}
for block in re.findall(r'tileset\s*\{(.*?)\}',textdef,re.S):
    n=re.search(r'file\s*=\s*(\S+)',block)
    size=re.search(r'size\s*=\s*(\d+)\s*,\s*(\d+)',block)
    if n and size:tiledefs[n.group(1)]=(int(size.group(1)),int(size.group(2)))
# Atlas filenames can live in subdirectories: preserve all exact basename matches.
allpng=sorted(p for p in TILES.rglob('*.png') if p.is_file())
pngByStem=defaultdict(list)
for p in allpng:pngByStem[p.stem].append(p)
def path_priority(p):
    s=p.relative_to(ROOT).as_posix()
    return (0 if p.parent==TILES/'2x' else 1 if p.parent==TILES else 2,s)
for items in pngByStem.values():items.sort(key=path_priority)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
@lru_cache(maxsize=2)
def getPNG(src):
    # Avoid full 322-atlas unbounded RGBA cache; tileset keys are sorted.
    with Image.open(src) as im: return im.convert('RGBA')
def source_choice(name):
    variants=pngByStem.get(name,[])
    return (variants[0] if variants else None,
            [p.relative_to(ROOT).as_posix() for p in variants])
def dims_candidate(atlas,cols,rows,lid):
    if cols<=0 or rows<=0 or lid<0 or lid>=cols*rows:
        return None, 'id_out_of_grid',None
    if atlas.width%cols or atlas.height%rows:
        return None, 'pixel_grid_not_integer',None
    sw=atlas.width//cols;sh=atlas.height//rows
    if sw<=0 or sh<=0:return None,'invalid_cell_dims',None
    left=(lid%cols)*sw;top=(lid//cols)*sh
    crop=atlas.crop((left,top,left+sw,top+sh))
    return crop,'ok',dict(cols=cols,rows=rows,cell_width=sw,cell_height=sh,
                          crop_bbox=[left,top,left+sw,top+sh])
def candidate_tmx(atlas,t,lid):
    tw,th=t['tilewidth'],t['tileheight']
    iw,ih=t['img_width'],t['img_height']
    if min(tw,th,iw,ih)<=0:return None,'tmx_dimensions_missing',None
    if iw%tw or ih%th:return None,'tmx_atlas_dims_not_divisible',None
    cols,rows=iw//tw,ih//th
    scx=atlas.width/iw;scy=atlas.height/ih
    if abs(scx-scy)>0.001 or not 0.25<=scx<=8:
        return None,'tmx_png_size_or_scale_conflict',None
    if abs(scx-round(scx))>0.001 and abs(1/scx-round(1/scx))>0.001:
        return None,'tmx_png_nonstandard_scale',None
    return dims_candidate(atlas,cols,rows,lid)
def candidate_tiledef(atlas,name,t,lid):
    grid=tiledefs.get(name)
    if not grid:return None,'tiledef_missing',None
    cols,rows=grid
    scx=atlas.width/(cols*t['tilewidth'])
    scy=atlas.height/(rows*t['tileheight'])
    if abs(scx-scy)>.001 or not 0.25<=scx<=8:
        return None,'tiledef_png_size_or_scale_conflict',None
    if abs(scx-round(scx))>.001 and abs(1/scx-round(1/scx))>.001:
        return None,'tiledef_png_nonstandard_scale',None
    return dims_candidate(atlas,cols,rows,lid)
def visible(im):
    if im is None:return 0,None
    box=im.getchannel('A').getbbox()
    # Count visible pixels using histogram; efficiency independent of resolution.
    h=im.getchannel('A').histogram()
    return sum(h[1:]),list(box) if box else None
def hashpix(im):
    return hashlib.sha256(im.tobytes()).hexdigest() if im is not None else ''
# Modern fonts supplied by system; labels are primarily ASCII to avoid fonts dropping JUMBO etc.
fontpath=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
font=ImageFont.truetype(str(fontpath),13) if fontpath.exists() else ImageFont.load_default()
tiny=ImageFont.truetype(str(fontpath),10) if fontpath.exists() else ImageFont.load_default()
def thumb(im,maxw=128,maxh=94):
    bg=Image.new('RGB',(maxw,maxh),(243,245,249))
    draw=ImageDraw.Draw(bg)
    for x in range(0,maxw,12):
        for y in range(0,maxh,12):
            if (x//12+y//12)%2==0:draw.rectangle((x,y,x+11,y+11),fill=(227,230,234))
    if im is None:
        draw.text((14,maxh//2-7),'NO SOURCE',font=tiny,fill=(132,38,38))
        return bg
    # Thumbnail only, do not flatten the original atlas source.
    src=im.copy();src.thumbnail((maxw-6,maxh-6),Image.Resampling.LANCZOS)
    bg.paste(src,((maxw-src.width)//2,(maxh-src.height)//2),src)
    return bg

# Keep original selection evidence and source candidates; prefer exact agree, otherwise
# single nonzero only as a reviewable proposal, with "needs_ai_comparison" flags.
COLUMNS=['tile_set_name','local_id','maps_using_tile_key','prior_in_5409','user_excluded',
 'source_png_path','other_exact_name_pngs','source_png_sha256','atlas_w','atlas_h',
 'tmx_source_declared','tmx_firstgid','tmx_grid','tiledef_grid',
 'A1_status','A1_bbox','A1_alpha_pixels','A1_pixel_sha256',
 'A2_status','A2_bbox','A2_alpha_pixels','A2_pixel_sha256',
 'A1_A2_identical','preferred_A','preferred_reason','candidate_decision',
 'ai_visual_selected','official_mapping_verified','tilezed_verified',
 'source_hypothesis_sheet','sheet_cell','source_warning']
outputs=[]
stats=Counter();details=defaultdict(Counter)
for idx, rec in enumerate(target):
    name=rec['tile_set_name'];lid=int(rec['local_id']);k=(name,lid)
    if idx and idx%1000==0:print('PROGRESS A',idx,'of 10042',dict(stats),flush=True)
    t=decl[name];source,variants=source_choice(name)
    atlas=getPNG(str(source)) if source else None
    if atlas is None:
        A1=A2=None;s1=s2='exact_png_missing';info1=info2=None
    else:
        A1,s1,info1=candidate_tmx(atlas,t,lid)
        A2,s2,info2=candidate_tiledef(atlas,name,t,lid)
    a1,b1=visible(A1);a2,b2=visible(A2)
    h1=hashpix(A1) if A1 is not None else ''
    h2=hashpix(A2) if A2 is not None else ''
    identical=bool(A1 is not None and A2 is not None and h1==h2 and A1.size==A2.size)
    if identical and a1:
        choose='A1=A2';reason='both_grid_crops_same_nontransparent';decision='proposed_consistent'
    elif a1>0 and a2==0:
        choose='A1';reason='A1_nontransparent_A2_missing_or_transparent';decision='proposed_one_visible_needs_ai'
    elif a2>0 and a1==0:
        choose='A2';reason='A2_nontransparent_A1_missing_or_transparent';decision='proposed_one_visible_needs_ai'
    elif a1 and a2:
        choose='UNDECIDED';reason='two_different_visible_A_candidates';decision='needs_ai_comparison'
    elif A1 is not None or A2 is not None:
        choose='UNDECIDED';reason='candidate_crops_empty_cannot_certify_transparent';decision='no_visible_candidate'
    else:
        choose='UNDECIDED';reason='no_source_or_usable_geometry';decision='no_usable_source'
    stats[decision]+=1
    if k in EXCLUSIONS:stats['user_excluded_total']+=1
    if k in oldkeys:stats['prior_5409']+=1
    elif k not in oldkeys:stats['new_4633']+=1
    if not source:stats['no_exact_png']+=1
    if variants and len(variants)>1:stats['multiple_exact_path_variants']+=1
    if identical:stats['identical_A1_A2']+=1
    details[name][decision]+=1
    sheetNo=idx//80
    outputs.append(dict(tile_set_name=name,local_id=lid,
        maps_using_tile_key=int(rec['maps_using_tile_key']),
        prior_in_5409=int(k in oldkeys),user_excluded=int(k in EXCLUSIONS),
        source_png_path=source.relative_to(ROOT).as_posix() if source else '',
        other_exact_name_pngs=';'.join(variants[1:]),
        source_png_sha256='', # Filled from per-atlas evidence manifest
        atlas_w=atlas.width if atlas else 0,atlas_h=atlas.height if atlas else 0,
        tmx_source_declared=t['img_source'],tmx_firstgid=t['firstgid'],
        tmx_grid=f"{t['img_width']//t['tilewidth']}x{t['img_height']//t['tileheight']}",
        tiledef_grid='x'.join(map(str,tiledefs[name])) if name in tiledefs else '',
        A1_status=s1,A1_bbox=','.join(map(str,info1['crop_bbox'])) if info1 else '',
        A1_alpha_pixels=a1,A1_pixel_sha256=h1,A2_status=s2,
        A2_bbox=','.join(map(str,info2['crop_bbox'])) if info2 else '',
        A2_alpha_pixels=a2,A2_pixel_sha256=h2,A1_A2_identical=int(identical),
        preferred_A=choose,preferred_reason=reason,candidate_decision=decision,
        ai_visual_selected=0,official_mapping_verified=0,tilezed_verified=0,
        source_hypothesis_sheet=f'review/v117_A_candidates_10042/sheets/A_{sheetNo:03d}.jpg',
        sheet_cell=idx%80,
        source_warning='Multiple exact basename PNG paths: verify archive variant' if len(variants)>1 else
          'Not a transparency or Local ID certification; user excluded from active analysis' if k in EXCLUSIONS else
          'A candidate is mechanically proposed, not AI-selected or TileZed-certified'
    ))
    if idx%80==0:
        sheet=Image.new('RGB',(1920,1650),(236,241,246))
        drawer=ImageDraw.Draw(sheet)
    n=idx%80;cx=n%8;cy=n//8
    ox=cx*240;oy=cy*165
    drawer.rectangle((ox+2,oy+2,ox+237,oy+163),fill='white',outline=(139,156,169),width=1)
    drawer.text((ox+7,oy+8),f'{idx:05d} {name[:26]}',font=tiny,fill=(30,43,59))
    drawer.text((ox+7,oy+26),f'Local ID {lid} / {choose[:13]}',font=tiny,
        fill=(20,115,87) if decision=='proposed_consistent' else (142,80,38))
    sheet.paste(thumb(A1),(ox+4,oy+45))
    sheet.paste(thumb(A2),(ox+134,oy+45))
    drawer.text((ox+8,oy+141),f'A1:{s1[:9]} {a1:,}',font=tiny,fill=(65,76,91))
    drawer.text((ox+135,oy+141),f'A2:{s2[:9]} {a2:,}',font=tiny,fill=(65,76,91))
    if n==79 or idx==len(target)-1:
        sheet.save(SHEETS/f'A_{sheetNo:03d}.jpg',quality=85,optimize=True)
        sheet.close()
# Avoid having 10K repeated SHA hash computations on same PNG read.
pngHashes={}
for p in {r['source_png_path'] for r in outputs if r['source_png_path']}:
    pngHashes[p]=sha(ROOT/p)
for r in outputs:r['source_png_sha256']=pngHashes.get(r['source_png_path'],'')
assert len(outputs)==10042
assert stats['prior_5409']==5409 and stats['new_4633']==4633
assert stats['user_excluded_total']==14
assert sum(stats[k] for k in ('proposed_consistent','proposed_one_visible_needs_ai',
                  'needs_ai_comparison','no_visible_candidate','no_usable_source'))==10042
assert len(list(SHEETS.glob('A_*.jpg')))==126
csvpath=OUT/'A_CANDIDATE_MASTER_10042.csv'
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=COLUMNS)
    writer.writeheader();writer.writerows(outputs)
# A status and priority lists for AI work are independent of model guesses.
for decision in ('proposed_consistent','proposed_one_visible_needs_ai','needs_ai_comparison',
                 'no_visible_candidate','no_usable_source'):
    with (OUT/f'{decision}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader()
        w.writerows(r for r in outputs if r['candidate_decision']==decision)
# Lightweight offline index, no external requests when viewing locally.
entry=[[r['tile_set_name'],r['local_id'],r['preferred_A'],r['candidate_decision'],
       r['source_hypothesis_sheet'].split('/')[-1],r['sheet_cell'],
       r['prior_in_5409'],r['user_excluded']] for r in outputs]
page=r"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>B42 A 후보 10,042종</title><style>
body{font:14px system-ui,sans-serif;background:#f1f5f9;margin:0;color:#243347}
header{background:#1d3449;color:white;padding:22px}h1{margin:0;font-size:23px}
main{max-width:1540px;margin:15px auto;padding:0 10px}
section{background:white;border-radius:9px;padding:12px;margin:10px 0}
input,select{font:inherit;padding:8px;border:1px solid #becdd8;border-radius:5px}
button{font:inherit;padding:8px;cursor:pointer;border-radius:5px;border:1px solid #acbfca;background:#e7f1f4}
table{border-collapse:collapse;width:100%;font-size:12px}td,th{padding:7px;border-bottom:1px solid #edf0f3;text-align:left}
td:first-child{overflow-wrap:anywhere}#viewer{width:100%;max-height:76vh;object-fit:contain;border:1px solid #bac9d3}
small{color:#64778a}code{background:#f0f3f5;padding:3px}a{color:#0b6b8f}
</style></head><body>
<header><h1>프로젝트 좀보이드 A 후보 10,042종</h1>
A1=TMX 선언 격자, A2=TileZed 타일 정의 격자 · 기계적 후보 생성 · 공식 대응 인증 아님</header>
<main><section>
<label>찾기 <input id="search" placeholder="타일셋 이름 / Local ID"/></label>
<label>상태 <select id="status"><option value="">전체</option><option value="proposed_consistent">A1=A2 일치</option>
<option value="proposed_one_visible_needs_ai">하나만 가시</option>
<option value="needs_ai_comparison">서로 다른 2개</option>
<option value="no_visible_candidate">후보 이미지 비가시</option><option value="no_usable_source">원본·격자 오류</option></select></label>
<label><input type="checkbox" id="newOnly">신규 4,633종만</label>
<label><input type="checkbox" id="excludedOff" checked>사용자 제외 14종 숨김</label>
<p id="counter"></p>
</section><section><div><b id="sheetLabel">A_000.jpg</b> <button id="prev">이전 접촉시트</button> <button id="next">다음 접촉시트</button>
<a id="open" target="_blank" rel="noopener">원본 접촉시트 열기</a></div>
<img id="viewer" alt="A1 A2 비교 접촉시트" src="sheets/A_000.jpg">
<small>한 장에 80종(8열×10행). 각 칸의 두 이미지 A1/A2를 비교. Local ID 오류·투명 여부는 최종 판정이 아닙니다.</small>
</section><section><table><thead><tr><th>타일셋</th><th>Local ID</th><th>선호 A</th><th>상태</th><th>기존</th><th>이미지</th></tr></thead><tbody id="results"></tbody></table>
<button id="more">50개 더 보기</button></section>
</main><script>
const D=__ROWS__;
let shown=[],limit=50,sheet=0;
const $=id=>document.getElementById(id);
function setSheet(n){sheet=Math.max(0,Math.min(125,n));const name='A_'+String(sheet).padStart(3,'0')+'.jpg';$('sheetLabel').textContent=name;$('viewer').src='sheets/'+name;$('open').href='sheets/'+name}
function draw(){let q=$('search').value.toLowerCase().trim(),f=$('status').value,newOnly=$('newOnly').checked,hide=$('excludedOff').checked;
shown=D.filter(r=>(!q||r[0].toLowerCase().includes(q)||String(r[1]).includes(q))&&(!f||r[3]===f)&&(!newOnly||!r[6])&&(!hide||!r[7]));
$('counter').textContent='해당 타일 '+shown.length.toLocaleString('ko-KR')+'종 / 전체 10,042종. 여러 후보는 AI 추가 대조 필요.';
let html='';for(const r of shown.slice(0,limit)){html+='<tr><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+r[2]+'</td><td>'+r[3]+'</td><td>'+(r[6]?'기존':'신규')+'</td><td><button class="jump" data-sheet="'+Number(r[4].slice(2,5))+'">시트 '+r[4]+' ('+r[5]+'번)</button></td></tr>'}
$('results').innerHTML=html;$('more').disabled=limit>=shown.length;
for(const b of document.querySelectorAll('.jump'))b.onclick=()=>{setSheet(Number(b.dataset.sheet));$('viewer').scrollIntoView({behavior:'smooth'})};
}
for(const id of ['search','status','newOnly','excludedOff'])$(id).oninput=()=>{limit=50;draw()};
$('more').onclick=()=>{limit+=50;draw()};
$('prev').onclick=()=>setSheet(sheet-1);$('next').onclick=()=>setSheet(sheet+1);
setSheet(0);draw();
</script></body></html>"""
html=page.replace('__ROWS__',json.dumps(entry,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
(OUT/'A_CANDIDATE_REVIEW_INDEX.html').write_text(html,encoding='utf-8')
manifest=dict(version='v117',scope='26_43_to_37_49',source_tiles=10042,
 existing_5409=stats['prior_5409'],new_4633=stats['new_4633'],user_excluded_14=stats['user_excluded_total'],
 source_tmx=RANGE_REPORT['per_map'],source_distinct_key_sha256=RANGE_REPORT['distinct_tile_keys_sha256'],
 source_png_file_count=len(allpng),source_exact_png_count=len(pngHashes),
 tiledefinitions_sha256=sha(TILES/'tiledefinitions.tiles.txt'),
 candidate_stats={k:stats[k] for k in ('proposed_consistent','proposed_one_visible_needs_ai',
             'needs_ai_comparison','no_visible_candidate','no_usable_source')},
 diagnostics={k:v for k,v in stats.items() if k not in ('proposed_consistent','proposed_one_visible_needs_ai',
             'needs_ai_comparison','no_visible_candidate','no_usable_source')},
 sheet_count=126,master_csv=csvpath.relative_to(ROOT).as_posix(),
 master_csv_sha256=sha(csvpath),offline_index='review/v117_A_candidates_10042/A_CANDIDATE_REVIEW_INDEX.html',
 offline_index_sha256=sha(OUT/'A_CANDIDATE_REVIEW_INDEX.html'),
 source_png_sha256=pngHashes,
 source_name_status_per_tileset={k:dict(v) for k,v in details.items()},
 mapping_verified=0,tilezed_verified=0,final_identity_certified=0,
 AI_selected_by_visual_review=0,
 disclaimer='A1/A2 are programmatically selected atlas-grid hypotheses, even if agreeing; do not call official or AI-selected without visual and TileZed verification. Transparent is never inferred from zero-alpha crop.')
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('SUCCESS v117',json.dumps(manifest['candidate_stats']), 'PNG FILES',len(allpng),
      'EXACT SOURCE NAMES',len(pngHashes),'contact sheets',manifest['sheet_count'],flush=True)
