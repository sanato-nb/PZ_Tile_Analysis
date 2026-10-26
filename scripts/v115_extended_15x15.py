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


# v115 extended-context experiment: 15x15 cells, full same-floor layers.
from PIL import ImageEnhance
EX=ROOT/'review/v115_extended_context'
EX.mkdir(parents=True,exist_ok=True)
targets=[
  ('appliances_com_01',3), ('appliances_com_01',82),
  ('appliances_com_01',96),('appliances_com_01',120),
  ('appliances_com_01',124),('appliances_com_01',133),
  ('electricity_pylon',42),('electricity_pylon',45)
]
def render15(place,remove=False):
    m=maps[place['tmx']]
    xx,yy=place['x'],place['y'];r=7
    canvas=Image.new('RGBA',(2000,1480),(243,246,247,255))
    missing=drawn=0;removed=False
    for ly in m['layers']:
        if ly['level']!=place['level']:continue
        for y in range(max(0,yy-r),min(256,yy+r+1)):
            for x in range(max(0,xx-r),min(256,xx+r+1)):
                raw=ly['vals'][y*256+x]
                if not raw:continue
                if remove and ly['index']==place['layer_index'] and x==xx and y==yy and raw==place['gid']:
                    removed=True;continue
                key=resolve(place['tmx'],raw)
                if key is None:continue
                im,_,_=choose(*key,place['tmx'])
                if im is None:missing+=1;continue
                px=1000+(x-xx-y+yy)*60-im.width//2
                py=760+(x-xx+y-yy)*30+30-im.height
                canvas.alpha_composite(im,(px,py))
                drawn+=1
    draw=ImageDraw.Draw(canvas)
    draw.rectangle((0,0,1200,37),fill=(16,30,42,255))
    draw.text((12,12),f'15x15 {place["tmx"]}, level {place["level"]}, x={xx} y={yy},  {"REMOVE CENTER" if remove else "ORIGINAL"}',
              fill=(255,255,255,255))
    return canvas.convert('RGB'),missing,drawn,removed

evidence=[]
for i,(ts,lid) in enumerate(targets):
    sites=usages[ts,lid]
    assert sites
    p=sites[0]
    B,mb,db,_=render15(p,False);C,mc,dc,removed=render15(p,True)
    assert removed
    delta=ImageChops.difference(B,C)
    dif=delta.getbbox()
    if dif is not None:
        # Mark affected region in the DIFF image; do not invent scale.
        enhanced=ImageEnhance.Contrast(delta).enhance(2.5)
    else:
        enhanced=delta
    base=f'{i:02d}_{ts}__{lid:03d}'
    pb=EX/(base+'_B15.jpg');pc=EX/(base+'_C15.jpg');pd=EX/(base+'_DIFF15.jpg')
    B.save(pb,quality=81,optimize=True);C.save(pc,quality=81,optimize=True)
    enhanced.save(pd,quality=84,optimize=True)
    combined=Image.new('RGB',(2000,1480),(247,249,250))
    # Half-size originals, retaining 15x15 detail and differences.
    combined.paste(B.resize((1000,740),Image.Resampling.LANCZOS),(0,0))
    combined.paste(C.resize((1000,740),Image.Resampling.LANCZOS),(1000,0))
    combined.paste(enhanced.resize((1000,740),Image.Resampling.NEAREST),(0,740))
    A,astat,src=choose(ts,lid,p['tmx'])
    pane=Image.new('RGB',(1000,740),(237,242,245))
    if A:
        v=a_board_sprite(A)
        v=v.resize((675,705),Image.Resampling.NEAREST)
        pane.paste(v,(140,25))
    dd=ImageDraw.Draw(pane)
    dd.text((15,5),f'A candidate {ts}/{lid}; source {src}',fill=(20,30,45))
    combined.paste(pane,(1000,740))
    comb=EX/(base+'_15x15_compared.jpg');combined.save(comb,quality=83,optimize=True)
    info=dict(key=[ts,lid],primary_placement=p,source=src,source_provisional_status=astat,
      context_radius=7,window='15x15',missing_B=mb,missing_C=mc,
      rendered_B=db,rendered_C=dc,removed=removed,
      delta_bbox=dif,has_visible_difference=dif is not None,
      images=[str(z.relative_to(ROOT)) for z in (pb,pc,pd,comb)])
    evidence.append(info)
    print('EXTENDED',ts,lid,'difference',dif,'B drawn',db,flush=True)
(EX/'MANIFEST.json').write_text(json.dumps(dict(type='v115 extended visual evidence',
  context='15x15 compared with previous 5x5',mapping_verified=False,tilezed_verified=False,
  items=evidence),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS extended contexts',len(evidence),flush=True)
