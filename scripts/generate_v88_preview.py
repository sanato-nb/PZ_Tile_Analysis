#!/usr/bin/env python3
"""GitHub 원본 PNG+TMX로 신규 미관찰 타일의 A/B/C/D 비교판을 생성한다.
이 스크립트는 관찰 판정을 수행하지 않으며, 이미지 검토 전에는 공식 수치를 변경하지 않는다.
"""
import csv, hashlib, json, sqlite3, subprocess, sys
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'checkpoints/v88_preview'
OUT.mkdir(parents=True,exist_ok=True)
TARGETS=[]
MAPS=['31_45.tmx','31_46.tmx']
TMX_DIR=ROOT/'B4220.3_MapExport_256/tmx'
TILE_DIR=ROOT/'Tiles/2x'
MAP_DATA={}
OCC=defaultdict(list)
ATLASES={}
HASHES={}
FONT=ImageFont.load_default()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read_map(name):
    path=TMX_DIR/name
    root=ET.parse(path).getroot()
    ts=[]
    for t in root.findall('tileset'):
        im=t.find('image')
        if im is None: continue
        ts.append({'first':int(t.attrib['firstgid']),'name':t.attrib['name'],
                   'tw':int(t.attrib['tilewidth']),'th':int(t.attrib['tileheight']),
                   'iw':int(im.attrib['width']),'ih':int(im.attrib['height'])})
    ts.sort(key=lambda t:t['first'])
    layers=[]
    for li,layer in enumerate(root.findall('layer')):
        data=layer.find('data')
        if data is None or data.attrib.get('encoding')!='csv': continue
        vals=[int(v.strip()) for v in data.text.split(',') if v.strip()]
        if len(vals)!=256*256: raise ValueError((name,li,len(vals)))
        lvl=int(layer.attrib.get('level',0))
        layers.append({'name':layer.attrib['name'],'level':lvl,'index':li,'vals':vals})
    return {'path':path,'tilesets':ts,'layers':layers}

for name in MAPS:
    MAP_DATA[name]=read_map(name)
    HASHES[name]=sha(TMX_DIR/name)

def resolve(m,gid):
    gid &= 0x1fffffff
    if not gid:return None
    lo,hi=0,len(m['tilesets'])-1
    while lo<hi:
        mid=(lo+hi+1)//2
        if m['tilesets'][mid]['first']<=gid:lo=mid
        else:hi=mid-1
    t=m['tilesets'][lo]
    if gid<t['first']:return None
    return t,gid-t['first']

subprocess.run([sys.executable,str(ROOT/'scripts/restore_unified_v87.py'),'/tmp/pz_v87_preview.sqlite'],check=True)
with sqlite3.connect('/tmp/pz_v87_preview.sqlite') as conn:
    queue={(r[0],int(r[1])) for r in conn.execute('select tile_set_locator,local_id from analysis_queue')}
assert len(queue)==1748,len(queue)
target_set=queue
for name,m in MAP_DATA.items():
    for layer in m['layers']:
        for pos,raw in enumerate(layer['vals']):
            r=resolve(m,raw)
            if r and (r[0]['name'],r[1]) in target_set:
                OCC[(r[0]['name'],r[1])].append({'tmx':name,'level':layer['level'],
                    'layer':layer['name'],'layer_index':layer['index'],
                    'x':pos%256,'y':pos//256,'gid':raw})

def atlas(t):
    name=t['name']
    if name in ATLASES:return ATLASES[name]
    p=TILE_DIR/(name+'.png')
    if not p.exists():p=ROOT/'Tiles'/(name+'.png')
    if not p.exists():
        ATLASES[name]=(None,None,None,'missing')
        return ATLASES[name]
    im=Image.open(p).convert('RGBA')
    sx=im.width/t['iw']
    sy=im.height/t['ih']
    if sx not in (1,2,4):
        status='width_scale_unexpected'
    elif sy!=sx:
        status='height_mismatch'
    else:status='dimensions_consistent'
    ATLASES[name]=(im,p,sx,status)
    HASHES[str(p.relative_to(ROOT))]=sha(p)
    return ATLASES[name]

def crop(t,lid):
    im,p,scale,status=atlas(t)
    if im is None:return None,status
    sw=round(t['tw']*scale);sh=round(t['th']*scale)
    cols=round(t['iw']/t['tw'])
    x=(lid%cols)*sw;y=(lid//cols)*sh
    if x+sw>im.width or y+sh>im.height:return None,'local_id_out_of_png'
    return im.crop((x,y,x+sw,y+sh)),status

def render(placement,remove=False):
    m=MAP_DATA[placement['tmx']]
    x0,y0=placement['x'],placement['y']
    board=Image.new('RGBA',(900,680),(239,242,244,255))
    missing=0;drawn=0;target_seen=False
    for layer in m['layers']:
        if layer['level']!=placement['level']:continue
        for y in range(max(0,y0-2),min(256,y0+3)):
            for x in range(max(0,x0-2),min(256,x0+3)):
                raw=layer['vals'][y*256+x]
                if not raw:continue
                if remove and layer['index']==placement['layer_index'] and x==x0 and y==y0 and raw==placement['gid']:
                    target_seen=True
                    continue
                r=resolve(m,raw)
                if r is None:continue
                sprite,status=crop(*r)
                if sprite is None:missing+=1;continue
                dx=x-x0;dy=y-y0
                xx=450+(dx-dy)*64-sprite.width//2
                yy=360+(dx+dy)*32+32-sprite.height
                board.alpha_composite(sprite,(xx,yy))
                drawn+=1
    return board,missing,drawn,target_seen

def label(img,label_text):
    d=ImageDraw.Draw(img)
    d.rectangle((0,0,img.width,30),fill=(20,30,40,235))
    d.text((10,8),label_text,font=FONT,fill=(255,255,255,255))

# 다양한 종류의 미관찰 타일을 실제 사용 위치·PNG 존재 여부로만 선별한다.
# 여기서는 이미지 판독/정체 분류를 수행하지 않는다.
tiers=[('fixtures_',6),('furniture_',6),('carpentry_',6),('d_',6),('blends_',6),('boulders',6),('appliances_',6),('location_',6),('industry_',6),('vegetation_',6)]
eligible=sorted((key for key, uses in OCC.items() if len(uses)>=2),key=lambda k:(k[0],k[1]))
selected=[]
for prefix, quota in tiers:
    added=0
    for key in eligible:
        if not key[0].startswith(prefix) or key in selected:continue
        uses=OCC[key]
        other=next((p for p in uses[1:] if p['tmx']!=uses[0]['tmx'] or abs(p['x']-uses[0]['x'])+abs(p['y']-uses[0]['y'])>=5),None)
        if other is None:continue
        m=MAP_DATA[uses[0]['tmx']]
        t=next(t for t in m['tilesets'] if t['name']==key[0])
        sprite,status=crop(t,key[1])
        if sprite is None or not sprite.getbbox():continue
        selected.append(key);added+=1
        if added>=quota:break
# 나머지 범주에서도 충분한 다른 배치가 있는 미관찰 타일을 보충한다.
for key in eligible:
    if len(selected)>=50: break
    if key in selected: continue
    uses=OCC[key]
    other=next((p for p in uses[1:] if p['tmx']!=uses[0]['tmx'] or abs(p['x']-uses[0]['x'])+abs(p['y']-uses[0]['y'])>=5),None)
    if other is None: continue
    m=MAP_DATA[uses[0]['tmx']]
    t=next(t for t in m['tilesets'] if t['name']==key[0])
    sprite,status=crop(t,key[1])
    if sprite is None or not sprite.getbbox(): continue
    selected.append(key)
TARGETS=selected[:50]
assert len(set(TARGETS))==len(TARGETS), 'duplicate target keys'

assert len(TARGETS)>=25,('not enough review targets',TARGETS)
print('v88 UNREVIEWED PREVIEW TARGETS',TARGETS,flush=True)
results=[]
for key in TARGETS:
    if key not in queue:
        results.append({'key':key,'status':'skipped_not_in_v87_queue'})
        continue
    uses=OCC[key]
    if len(uses)<2:
        results.append({'key':key,'status':'skipped_no_D_placement','uses':len(uses)})
        continue
    a=uses[0]
    b=next((p for p in uses[1:] if p['tmx']!=a['tmx'] or abs(p['x']-a['x'])+abs(p['y']-a['y'])>=5),uses[1])
    m=MAP_DATA[a['tmx']]
    target=next(t for t in m['tilesets'] if t['name']==key[0])
    original,atlas_status=crop(target,key[1])
    if original is None:
        results.append({'key':key,'status':'skipped_png_unavailable','reason':atlas_status})
        continue
    B,mb,db_count,_=render(a,False)
    C,mc,dc_count,removed=render(a,True)
    D,md,dd_count,_=render(b,False)
    if not removed:raise ValueError('selected placement not removed '+str(key))
    delta=ImageChops.difference(B,C)
    delta_pixels=sum(1 for px in delta.getdata() if px[:3]!=(0,0,0) or px[3]!=0)
    basename=f'{key[0]}__{key[1]:03d}'
    A=Image.new('RGBA',(900,680),(239,242,244,255))
    scale=min(4,600//max(original.width,original.height))
    scale=max(1,scale)
    enlarged=original.resize((original.width*scale,original.height*scale),Image.Resampling.NEAREST)
    A.alpha_composite(enlarged,((900-enlarged.width)//2,(680-enlarged.height)//2))
    for kind,im in [('A',A),('B',B),('C',C),('D',D)]:
        label(im,f'{kind} {basename} | {a["tmx"]} level {a["level"]} x{a["x"]} y{a["y"]}')
        im.convert('RGB').save(OUT/f'{basename}_{kind}.jpg',quality=88,optimize=True)
    contact=Image.new('RGB',(1800,1360),'white')
    for idx,im in enumerate([A,B,C,D]):
        contact.paste(im.convert('RGB'),((idx%2)*900,(idx//2)*680))
    contact.save(OUT/f'{basename}_ABCD.jpg',quality=90,optimize=True)
    results.append({'key':key,'status':'evidence_only_unreviewed','atlas_status':atlas_status,
        'A':f'{basename}_A.jpg','B':f'{basename}_B.jpg','C':f'{basename}_C.jpg',
        'D':f'{basename}_D.jpg','board':f'{basename}_ABCD.jpg',
        'primary_placement':a,'other_placement':b,'uses':len(uses),
        'visible_pixel_delta':delta_pixels,'missing_png_neighbors_B':mb,
        'missing_png_neighbors_C':mc,'missing_png_neighbors_D':md,
        'rendered_placements_B':db_count,'rendered_placements_C':dc_count,
        'rendered_placements_D':dd_count,
        'mapping_verified':False,'tilezed_verified':False,'final_certified':False})
(OUT/'EVIDENCE_MANIFEST.json').write_text(json.dumps({
    'source':'GitHub original PNG and TMX','base':'v87','observed_count_added':0,
    'rendering':'approximate isometric, not TileZed',
    'original_tmx_suffix_note':'Repository files omit (2), but 5409/302177 scope counts match',
    'sha256':HASHES,'results':results},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'generated':sum(x['status']=='evidence_only_unreviewed' for x in results),
    'results':results},ensure_ascii=False))
