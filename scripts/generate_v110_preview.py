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
OUT=ROOT/'checkpoints/v110_preview'
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

subprocess.run([sys.executable,str(ROOT/'scripts/restore_unified_v109.py'),'/tmp/pz_v109_preview.sqlite'],check=True)
with sqlite3.connect('/tmp/pz_v109_preview.sqlite') as conn:
    queue={(r[0],int(r[1])) for r in conn.execute('select tile_set_locator,local_id from analysis_queue')}
assert len(queue)==51,len(queue)
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

# 남은 미관찰 전체를 대상으로, 복수 사용 위치가 없어도 원본 A/B/C 검증 가능.
# 멀리 떨어진(거리 >=5 또는 타 TMX) 다른 사용 위치가 없으면 D 독립 현장 없음으로 명확히 표시한다.
TARGET_COUNT=9
eligible=sorted(OCC, key=lambda k:(k[0],k[1]))
buckets=defaultdict(list)
for key in eligible:
    uses=OCC[key]
    m=MAP_DATA[uses[0]['tmx']]
    t=next(t for t in m['tilesets'] if t['name']==key[0])
    sprite,status=crop(t,key[1])
    if sprite is None or not sprite.getbbox(): continue
    buckets[key[0]].append(key)
families=sorted(buckets, key=lambda name:(0 if name.startswith(('fixtures_','furniture_','appliances_','walls_','industry_','location_','vegetation_','carpentry_','crafted_')) else 1,name))
selected=[]
for round_idx in range(100):
    if len(selected)>=TARGET_COUNT: break
    for family in families:
        keys=buckets[family]
        if round_idx>=len(keys):continue
        key=keys[round_idx]
        selected.append(key)
        if len(selected)>=TARGET_COUNT:break
# 이미지 전체가 투명한 타일도 미관찰 키인 이상 보류 증거로 검수한다.
# 원본 PNG가 투명해도 크롭 가능한 키는 별도로 보류 대상으로 포함한다.
if len(selected)<TARGET_COUNT:
    for key in eligible:
        if key in selected:continue
        m=MAP_DATA[OCC[key][0]['tmx']]
        t=next(t for t in m['tilesets'] if t['name']==key[0])
        sprite,status=crop(t,key[1])
        if sprite is None:continue
        selected.append(key)
        if len(selected)>=TARGET_COUNT:break
TARGETS=selected[:TARGET_COUNT]
assert len(set(TARGETS))==len(TARGETS), 'duplicate target keys'

assert len(TARGETS)>=TARGET_COUNT,('not enough review targets',TARGETS)
# 51종 중 크롭 불가능한 대상을 근거와 함께 미관찰로 보존한다.
blocked=[]
for key in sorted(queue):
    if key in TARGETS:continue
    uses=OCC.get(key,[])
    if not uses:
        reason='no_tmx_placement'
        atlas_state='not_checked'
    else:
        m=MAP_DATA[uses[0]['tmx']]
        t=next(t for t in m['tilesets'] if t['name']==key[0])
        sprite,atlas_state=crop(t,key[1])
        reason=atlas_state if sprite is None else 'not_selected_or_transparent'
    blocked.append({'key':list(key),'reason':reason,'atlas_status':atlas_state,'uses':len(uses),'needs_official_local_id':True})
assert len(blocked)==len(queue)-len(TARGETS)==42,(len(blocked),len(TARGETS))
print('v110 UNREVIEWED PREVIEW TARGETS',TARGETS,flush=True)
print('v110 BLOCKED UNSEEN',len(blocked),flush=True)
results=[]
for key in TARGETS:
    if key not in queue:
        results.append({'key':key,'status':'skipped_not_in_v109_queue'})
        continue
    uses=OCC[key]
    if len(uses)<1:
        results.append({'key':key,'status':'skipped_no_usage','uses':len(uses)})
        continue
    a=uses[0]
    b=next((p for p in uses[1:] if p['tmx']!=a['tmx'] or abs(p['x']-a['x'])+abs(p['y']-a['y'])>=5),uses[1] if len(uses)>1 else None)
    d_available=b is not None
    if not d_available:b={'tmx':'','level':-1,'layer':'NO_SECOND_USE','layer_index':-1,'x':-1,'y':-1,'gid':0}
    m=MAP_DATA[a['tmx']]
    target=next(t for t in m['tilesets'] if t['name']==key[0])
    original,atlas_status=crop(target,key[1])
    if original is None:
        results.append({'key':key,'status':'skipped_png_unavailable','reason':atlas_status})
        continue
    B,mb,db_count,_=render(a,False)
    C,mc,dc_count,removed=render(a,True)
    if d_available: D,md,dd_count,_=render(b,False)
    else:
        D=Image.new('RGBA',(900,680),(239,242,244,255))
        ImageDraw.Draw(D).text((100,200),'D INDEPENDENT SITE UNAVAILABLE (>=5 GRID CELLS)',font=FONT,fill=(120,20,20,255))
        md=0;dd_count=0
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
        im.convert('RGB').save(OUT/f'{basename}_{kind}.jpg',quality=76,optimize=True)
    contact=Image.new('RGB',(1800,1360),'white')
    for idx,im in enumerate([A,B,C,D]):
        contact.paste(im.convert('RGB'),((idx%2)*900,(idx//2)*680))
    contact.save(OUT/f'{basename}_ABCD.jpg',quality=79,optimize=True)
    results.append({'key':key,'status':'evidence_only_unreviewed','atlas_status':atlas_status,
        'A':f'{basename}_A.jpg','B':f'{basename}_B.jpg','C':f'{basename}_C.jpg',
        'D':f'{basename}_D.jpg','board':f'{basename}_ABCD.jpg',
        'primary_placement':a,'other_placement':b,'other_placement_available':d_available,'D_independent_5_cells_or_other_map':d_available and (b['tmx']!=a['tmx'] or abs(b['x']-a['x'])+abs(b['y']-a['y'])>=5),'uses':len(uses),
        'visible_pixel_delta':delta_pixels,'missing_png_neighbors_B':mb,
        'missing_png_neighbors_C':mc,'missing_png_neighbors_D':md,
        'rendered_placements_B':db_count,'rendered_placements_C':dc_count,
        'rendered_placements_D':dd_count,
        'mapping_verified':False,'tilezed_verified':False,'final_certified':False})
(OUT/'EVIDENCE_MANIFEST.json').write_text(json.dumps({
    'source':'GitHub original PNG and TMX','base':'v109','observed_count_added':0, 'excluded_early_v109_keys':0,
    'rendering':'approximate isometric, not TileZed; actual D only when other map or >=5 cells; absence explicitly shown',
    'original_tmx_suffix_note':'Repository files omit (2), but 5409/302177 scope counts match',
    'sha256':HASHES,'results':results,'blocked_unobserved':blocked,'blocked_count':len(blocked)},ensure_ascii=False,indent=2),encoding='utf8')

# 사람/모델이 실제 A/B/C/D를 한 눈에 검토하기 위한 합본 미리보기 (6개 타일/장).
# 이 판은 시각 판독을 대신하지 않으며 개별 A/B/C/D 원본은 모두 별도 저장한다.
SHEET_DIR=OUT/'review_sheets'
SHEET_DIR.mkdir(parents=True,exist_ok=True)
sheets=[]
valid=[r for r in results if r['status']=='evidence_only_unreviewed']
for start_idx in range(0,len(valid),6):
    sheet=Image.new('RGB',(2080,1200),(231,235,238))
    draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(valid[start_idx:start_idx+6]):
        x0=(i%2)*1040; y0=(i//2)*400
        draw.rectangle((x0+8,y0+8,x0+1032,y0+392), fill=(250,250,250),outline=(100,120,130),width=2)
        title=f"{start_idx+i:03d} {r['key'][0]}/{r['key'][1]}  DELTA={r['visible_pixel_delta']}  MISSING={r['missing_png_neighbors_B']}"
        draw.text((x0+20,y0+20),title,font=FONT,fill=(20,35,45))
        for k,dx in [('A',0),('B',250),('C',500),('D',750)]:
            with Image.open(OUT/r[k]) as im:
                # A crop (전체 바탕을 제거한 실제 원본 픽셀 영역) / B,C,D는 전체 맥락을 축소
                if k=='A':
                    rgb=im.convert('RGB')
                    bbox=ImageChops.difference(rgb,Image.new('RGB',rgb.size,(239,242,244))).getbbox()
                    im=rgb.crop(bbox or (0,0,rgb.width,rgb.height))
                else: im=im.convert('RGB')
                im.thumbnail((245,318),Image.Resampling.LANCZOS)
                px=x0+20+dx+(245-im.width)//2;py=y0+62+(318-im.height)//2
                sheet.paste(im,(px,py))
                draw.text((x0+120+dx,y0+371),k,font=FONT,fill=(20,30,50))
    name=f"sheet_{start_idx//6:03}.jpg"
    file=SHEET_DIR/name
    sheet.save(file,quality=75,optimize=True)
    sheets.append(str(file.relative_to(ROOT)))
manifest_path=OUT/'EVIDENCE_MANIFEST.json'
updated=json.loads(manifest_path.read_text('utf8'))
updated['review_sheets']=sheets
updated['review_sheets_sha256']={p:sha(ROOT/p) for p in sheets}
manifest_path.write_text(json.dumps(updated,ensure_ascii=False,indent=2),encoding='utf8')
print('REVIEW_SHEETS',len(sheets),flush=True)

print(json.dumps({'generated':sum(x['status']=='evidence_only_unreviewed' for x in results),
    'results':results},ensure_ascii=False))
