#!/usr/bin/env python3
"""Build 888-source review browser. Extract from verified v113 SQLite, only documented PNG/TMX sources.
This does NOT change original catalog or claim official Local ID mapping.
"""
from pathlib import Path
from collections import defaultdict, Counter
from functools import lru_cache
from xml.etree import ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageChops
import base64,bisect,csv,hashlib,io,json,os,re,sqlite3,sys,zipfile

ROOT=Path(__file__).resolve().parents[1]
TMXROOT=ROOT/'B4220.3_MapExport_256/tmx'
OUT=ROOT/'review/888_no_identity_candidate'
OUT.mkdir(parents=True,exist_ok=True)
DB=Path(sys.argv[1]).resolve()
MAPS=['31_45.tmx','31_46.tmx']
assert hashlib.sha256(DB.read_bytes()).hexdigest()==json.loads((ROOT/'analysis/current/v113/MANIFEST.json').read_text())['sqlite_sha256']

with sqlite3.connect(DB) as conn:
    conn.row_factory=sqlite3.Row
    cols=[r['name'] for r in conn.execute('PRAGMA table_info(tile_catalog)')]
    sql="""SELECT * FROM tile_catalog WHERE observed_any=1 AND provisional_candidate_any_auditable=0
        ORDER BY tile_set_locator,local_id"""
    rows=[dict(r) for r in conn.execute(sql)]
    assert len(rows)==888, len(rows)
    assert len({(r['tile_set_locator'],r['local_id']) for r in rows})==888
    assert conn.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert conn.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0]==4512
    assert conn.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
    assert sum(r['v113_user_review_action']=='exclude_from_active_review' for r in rows)==0
TARGET={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
print('QUEUE 888 from verified physical SQLite',flush=True)
# The .tiles text is a provisional hypothesis; never claim official mapping from it.
definitions={}
for block in re.findall(r'tileset\s*\{(.*?)\}',(ROOT/'Tiles/tiledefinitions.tiles.txt').read_text('utf8'),re.S):
    fm=re.search(r'file\s*=\s*(\S+)',block)
    size=re.search(r'size\s*=\s*(\d+)\s*,\s*(\d+)',block)
    if fm and size:definitions[fm.group(1)]=(int(size.group(1)),int(size.group(2)))

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
SOURCES={p:sha(TMXROOT/p) for p in MAPS}
maps={}
usages=defaultdict(list)
for name in MAPS:
    root=ET.parse(TMXROOT/name).getroot()
    tiles=[]
    for x in root.findall('tileset'):
        im=x.find('image')
        if im is None:continue
        tiles.append(dict(first=int(x.get('firstgid')),name=x.get('name'),
            tw=int(x.get('tilewidth')),th=int(x.get('tileheight')),
            iw=int(im.get('width')),ih=int(im.get('height'))))
    tiles.sort(key=lambda t:t['first'])
    firsts=[t['first'] for t in tiles]
    layers=[]
    for ix,layer in enumerate(root.findall('layer')):
        x=layer.find('data')
        if x is None or x.get('encoding')!='csv':continue
        vals=[int(v) for v in re.findall(r'\d+',x.text or '')]
        assert len(vals)==int(layer.get('width','256'))*int(layer.get('height','256'))
        ly=dict(index=ix,name=layer.get('name'),level=int(layer.get('level','0')),vals=vals)
        layers.append(ly)
    maps[name]=dict(tiles=tiles,firsts=firsts,layers=layers)
    # Traverse each layer once, including all floors: track only the 888 keys.
    for ly in layers:
        for i,raw in enumerate(ly['vals']):
            if not raw:continue
            gid=raw&0x0fffffff
            idx=bisect.bisect_right(firsts,gid)-1
            if idx<0:continue
            t=tiles[idx];key=(t['name'],gid-t['first'])
            if key in TARGET and len(usages[key])<80:
                usages[key].append(dict(tmx=name,level=ly['level'],layer=ly['name'],
                    layer_index=ly['index'],x=i%256,y=i//256,gid=raw))
    print('INDEX',name,'layers',len(layers),'matched',len(usages),flush=True)
assert len(usages)==888, 'Target keys missing from original two TMX: '+str(list(TARGET-usages.keys())[:20])

@lru_cache(maxsize=12)
def get_atlas(name):
    ps=[
       ROOT/'Tiles/2x'/(name+'.png'),
       ROOT/'Tiles/2x/jumbo'/(name+'.png'),
       ROOT/'Tiles/2x/jumbo_xl'/(name+'.png'),
       ROOT/'Tiles/2x/jumbo_xxl'/(name+'.png'),
       ROOT/'Tiles/2x/stumps'/(name+'.png'),
       ROOT/'Tiles'/(name+'.png')
    ]
    p=next((p for p in ps if p.is_file()),None)
    if p is None:return None,None
    with Image.open(p) as source:
        im=source.convert('RGBA')
    return im,str(p.relative_to(ROOT))
@lru_cache(maxsize=2600)
def sprite(name,id,mode,first_map):
    m=maps[first_map]
    t=next((t for t in m['tiles'] if t['name']==name),None)
    if t is None:return None,'no_tileset',None
    im,path=get_atlas(name)
    if im is None:return None,'png_missing',None
    src_scale=im.width/t['iw'] if t['iw'] else 0
    # Declared map atlas is sometimes 8-col while original TileZed is 16-col.
    if mode=='tiledef':
        grid=definitions.get(name)
        if not grid:return None,'tiledef_no_grid',path
        if im.width!=grid[0]*t['tw']*2 or im.height!=grid[1]*t['th']*2:
            return None,'tiledef_grid_size_mismatch',path
        cols=grid[0];sw=t['tw']*2;sh=t['th']*2;why='tiledef_provisional'
    else:
        if src_scale not in (1,2,4):return None,'tmx_width_scale_unexpected',path
        cols=int(t['iw']/t['tw']);sw=int(t['tw']*src_scale);sh=int(t['th']*src_scale)
        why='tmx_declaration_provisional'
    x=(id%cols)*sw;y=(id//cols)*sh
    if x<0 or x+sw>im.width or y+sh>im.height:return None,'local_id_out_of_png',path
    return im.crop((x,y,x+sw,y+sh)),why,path
def resolve(mapname,raw):
    gid=raw&0x0fffffff
    if not gid:return None
    m=maps[mapname]
    i=bisect.bisect_right(m['firsts'],gid)-1
    if i<0:return None
    t=m['tiles'][i]
    return t['name'],gid-t['first']
def choose(name,lid,mapname):
    t,stat,src=sprite(name,lid,'tiledef',mapname)
    if t is not None and t.getbbox():return t,'tiledef_provisional',src
    x,s,xsrc=sprite(name,lid,'tmx',mapname)
    if x is not None and x.getbbox():return x,'tmx_declaration_provisional',xsrc
    if t is not None:return t,'tiledef_empty',src
    if x is not None:return x,'tmx_empty',xsrc
    return None,stat+' / '+s,src or xsrc

def render(place,remove=False):
    m=maps[place['tmx']]
    xx,yy=place['x'],place['y']
    out=Image.new('RGBA',(700,520),(243,246,247,255))
    missing=0;drawn=0;was_removed=False
    for ly in m['layers']:
        if ly['level']!=place['level']:continue
        for y in range(max(0,yy-2),min(256,yy+3)):
            for x in range(max(0,xx-2),min(256,xx+3)):
                raw=ly['vals'][y*256+x]
                if not raw:continue
                if remove and ly['index']==place['layer_index'] and x==xx and y==yy and raw==place['gid']:
                    was_removed=True
                    continue
                key=resolve(place['tmx'],raw)
                if key is None:continue
                im,_,_=choose(*key,place['tmx'])
                if im is None:missing+=1;continue
                px=350+(x-xx-y+yy)*60-im.width//2
                py=260+(x-xx+y-yy)*30+30-im.height
                out.alpha_composite(im,(px,py))
                drawn+=1
    return out,missing,drawn,was_removed

FONT=ImageFont.load_default()
def image_panel(board,img,column,label,color=(17,33,45)):
    x0=column*240
    draw=ImageDraw.Draw(board)
    draw.rectangle((x0,0,x0+239,269),fill=(242,246,249),outline=(154,169,183),width=1)
    draw.rectangle((x0+2,2,x0+237,25),fill=color)
    draw.text((x0+10,7),label,font=FONT,fill='white')
    if img is None:
        draw.text((x0+16,116),'SOURCE UNAVAILABLE',font=FONT,fill=(121,55,40))
        return
    img=img.convert('RGB')
    img.thumbnail((236,234),Image.Resampling.LANCZOS)
    board.paste(img,(x0+(240-img.width)//2,27+(238-img.height)//2))
def a_board_sprite(im):
    if im is None:return None
    bg=Image.new('RGBA',(225,235),(243,246,249,255))
    if not im.getbbox():return bg
    thumb=im.copy();thumb.thumbnail((214,224),Image.Resampling.NEAREST)
    bg.alpha_composite(thumb,((225-thumb.width)//2,(235-thumb.height)//2))
    return bg
def data_img(board):
    buf=io.BytesIO()
    board.save(buf,'WEBP',quality=53,method=4)
    return 'data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode('ascii')

prior_cols=sorted([k for k in cols if ('observed_features' in k or 'review_notes' in k)],reverse=True)
items=[];status_counts=Counter()
for i,row in enumerate(rows):
    n,lid=row['tile_set_locator'],int(row['local_id'])
    sites=usages[n,lid];p=sites[0]
    m=maps[p['tmx']]
    other=next((a for a in sites[1:] if a['tmx']!=p['tmx'] or abs(a['x']-p['x'])+abs(a['y']-p['y'])>=5),None)
    if other is None:
        other=next((a for a in sites[1:] if (a['tmx'],a['level'],a['x'],a['y'])!=(p['tmx'],p['level'],p['x'],p['y'])),None)
    a1,why1,src1=sprite(n,lid,'tmx',p['tmx'])
    a2,why2,src2=sprite(n,lid,'tiledef',p['tmx'])
    B,missingB,drawnB,_=render(p,False)
    C,missingC,drawnC,removed=render(p,True)
    assert removed
    delta=ImageChops.difference(B,C)
    diffpixels=sum(1 for px in delta.getdata() if any(px))
    if other:
        D,missingD,drawnD,_=render(other)
    else:D=None;missingD=None
    board=Image.new('RGB',(1200,270),(243,246,249))
    image_panel(board,a_board_sprite(a1),0,'A1 / TMX GRID')
    image_panel(board,a_board_sprite(a2),1,'A2 / TILEDEF GRID')
    image_panel(board,B,2,'B / ORIGINAL SCENE')
    image_panel(board,C,3,'C / TARGET REMOVED')
    image_panel(board,D,4,'D / ANOTHER USE' if other else 'D / NO SECOND SITE')
    key=n+'|'+str(lid)
    prev=next((str(row[k]) for k in prior_cols if row.get(k) and str(row[k]).strip()),'')
    status='ok' if (a1 is not None or a2 is not None) else 'png_or_mapping_problem'
    if diffpixels==0:status='zero_BC_'+status
    status_counts[status]+=1
    item=dict(key=key,tileset=n,local_id=lid,maps_using=len(sites),source_status=status,
        source_note=f'A1:{why1}, A2:{why2}; png={src1 or src2 or "missing"}; B neighbors missing {missingB}; C neighbors missing {missingC}; D others {len(sites)-1}; mapping NOT officially verified.',
        tmx=p['tmx'],level=p['level'],layer=p['layer'],x=p['x'],y=p['y'],raw_gid=p['gid'],
        delta=diffpixels,previous_features=prev[:340],image=data_img(board))
    items.append(item)
    if (i+1)%48==0:print('RENDER',i+1,'/',len(rows),'image_bytes',sum(len(x['image']) for x in items),flush=True)
assert len(items)==888 and len({x['key'] for x in items})==888
# Indexed HTML is self-contained: image pixels are embedded, no remote server or file selection needed.
template=(ROOT/'scripts/reviewer_888_bulk_template.html').read_text(encoding='utf8')
assert template.count('__PZ_888_ROWS_JSON__')==1
html=template.replace('__PZ_888_ROWS_JSON__',
    json.dumps(items,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
assert 'data:image/webp;base64,' in html and len(items)==888
htmlPath=OUT/'PZ_888종_일괄수동검수.html'
htmlPath.write_text(html,encoding='utf8')
csvPath=OUT/'PZ_888종_검수대기열.csv'
with csvPath.open('w',encoding='utf-8-sig',newline='') as f:
    fields=['tile_set_locator','local_id','source_tmx','level','layer','x','y','raw_gid','B_C_pixel_delta',
        'A_source_status','previous_observed_features']
    w=csv.writer(f);w.writerow(fields)
    for x in items:w.writerow([x['tileset'],x['local_id'],x['tmx'],x['level'],x['layer'],x['x'],x['y'],
        x['raw_gid'],x['delta'],x['source_status'],x['previous_features']])
manifest=dict(version='v114',kind='manual_recheck_observed_without_auditable_candidate',
    historical_observed=5400,historical_auditable_candidates=4512,review_target_count=888,
    images_embedded=888,source_uses=MAPS,visual_evidence_not_certified=True,
    official_png_tmx_mapping_verified=0,final_identity_certifications_added=0,
    status_counts=dict(status_counts),tmx_sha256=SOURCES,
    source_sqlite_sha256=hashlib.sha256(DB.read_bytes()).hexdigest(),
    review_html=htmlPath.relative_to(ROOT).as_posix(),
    review_html_sha256=sha(htmlPath),review_html_bytes=htmlPath.stat().st_size,
    manual_queue_sha256=sha(csvPath),manual_queue_bytes=csvPath.stat().st_size,
    note='Bulk seen is a user interface operation only and does not certify identity. Both A atlas crops and scene images are provisional and require Local ID verification.')
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf8')
zipPath=OUT/'PZ_888종_수동검수_HTML_CSV.zip'
readme=OUT/'사용법_먼저읽기.txt'
readme.write_text('PZ B42 888종 수동 검수 (v114)\\n1. ZIP을 풀고 PZ_888종_일괄수동검수.html을 Chrome/Edge에서 엽니다.\\n2. 현재 페이지/검색결과 모두 선택 -> 선택한 항목 확인 완료 또는 보류.\\n3. 정체가 드러나면 각 카드의 정체·속성·근거를 적거나 같은 종류만 일괄 정체명 적용.\\n4. 검수결과 CSV 저장 버튼으로 결과를 백업하고 채팅에 올리세요.\\n주의: 확인 완료는 의미 확정이나 공식 Local ID 인증이 아닙니다. 이미지의 A1/A2는 출처 미인증 후보입니다.\\n','utf8')
with zipfile.ZipFile(zipPath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in [htmlPath,csvPath,readme,OUT/'MANIFEST.json']:
        z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(zipPath) as z:
    assert z.testzip() is None and len(z.namelist())==4
manifest['review_zip_sha256']=sha(zipPath)
manifest['review_zip_bytes']=zipPath.stat().st_size
manifest['review_zip_crc']='PASS'
# Repack once to ensure manifest inside ZIP includes ZIP content reference? Use manifest outside, stable embedded archive manifest earlier.
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf8')
assert htmlPath.stat().st_size<98_000_000,('GitHub 100MB file limit',htmlPath.stat().st_size)
print('PASS',json.dumps({k:manifest[k] for k in ('review_target_count','images_embedded','status_counts','review_html_bytes','review_zip_bytes','review_zip_crc')},ensure_ascii=False),flush=True)
