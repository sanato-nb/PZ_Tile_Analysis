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
OUT=ROOT/'checkpoints/v100_preview'
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

subprocess.run([sys.executable,str(ROOT/'scripts/restore_unified_v99.py'),'/tmp/pz_v99_preview.sqlite'],check=True)
with sqlite3.connect('/tmp/pz_v99_preview.sqlite') as conn:
    queue={(r[0],int(r[1])) for r in conn.execute('select tile_set_locator,local_id from analysis_queue')}
assert len(queue)==639,len(queue)
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
TARGET_COUNT=216
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
TARGETS=[tuple(x) for x in [["walls_decoration_01",23],["walls_decoration_06",85],["walls_detailing_01",67],["walls_detailing_02",40],["walls_exterior_house_01",39],["walls_exterior_house_02",31],["walls_exterior_roofs_01",117],["walls_exterior_roofs_02",51],["walls_exterior_roofs_03",19],["walls_exterior_roofs_08",73],["walls_exterior_roofs_09",84],["walls_exterior_roofs_30_03",9],["walls_exterior_roofs_30_04",60],["walls_exterior_roofs_30_06",27],["walls_exterior_roofs_30_11",9],["walls_exterior_roofs_30_15",75],["walls_exterior_roofs_30_16",25],["walls_interior_bathroom_01",29],["walls_interior_detailing_bathroom_01",153],["walls_interior_detailing_bathroom_03",105],["walls_interior_house_04",12],["boulders",15],["d_wallcracks_1",27],["fencing_damaged_01",171],["floors_rugs_01",29],["lighting_indoor_02",17],["lighting_outdoor_01",37],["overlay_graffiti_wall_01",58],["radio_tower",77],["recreational_01",27],["recreational_sports_01",79],["roofs_30_01",12],["roofs_30_02",49],["roofs_30_03",59],["roofs_30_07",58],["roofs_30_08",80],["roofs_30_10",28],["roofs_accents_01",46],["roofs_shallow_01",13],["rooftop_furniture",36],["signs_miscbrands_01",52],["signs_one-off_01",84],["signs_one-off_02",189],["signs_one-off_03",372],["signs_one-off_09",44],["street_decoration_01",31],["street_trafficlines_01",46],["trash_walls_01",4],["appliances_cooking_01",51],["appliances_refrigeration_01",18],["fixtures_bathroom_01",63],["fixtures_counters_01",67],["fixtures_windows_curtains_01",95],["furniture_bedding_01",36],["furniture_seating_indoor_03",97],["furniture_storage_01",21],["furniture_storage_02",44],["industry_01",33],["industry_02",67],["location_business_machinery_01",8],["location_community_church_small_01",25],["location_community_medical_01",12],["location_community_school_02",42],["location_restaurant_bar_01",12],["location_restaurant_seahorse_01",62],["location_shop_accessories_01",30],["location_shop_bargNclothes_01",52],["location_trailer_02",32],["walls_decoration_01",26],["walls_detailing_01",68],["walls_detailing_02",44],["walls_exterior_house_01",50],["walls_exterior_house_02",47],["walls_exterior_roofs_02",93],["walls_exterior_roofs_03",21],["walls_exterior_roofs_08",76],["walls_exterior_roofs_09",91],["walls_exterior_roofs_30_03",10],["walls_exterior_roofs_30_04",64],["walls_exterior_roofs_30_06",28],["walls_exterior_roofs_30_11",12],["walls_exterior_roofs_30_15",76],["walls_exterior_roofs_30_16",26],["walls_interior_bathroom_01",31],["walls_interior_house_04",15],["boulders",34],["d_wallcracks_1",36],["fencing_damaged_01",179],["floors_rugs_01",32],["lighting_indoor_02",23],["lighting_outdoor_01",48],["overlay_graffiti_wall_01",72],["radio_tower",78],["recreational_01",30],["recreational_sports_01",138],["roofs_30_01",16],["roofs_30_02",50],["roofs_30_03",61],["roofs_30_07",59],["roofs_30_08",81],["roofs_30_10",29],["roofs_accents_01",48],["roofs_shallow_01",14],["rooftop_furniture",39],["signs_miscbrands_01",53],["signs_one-off_02",190],["signs_one-off_09",45],["street_decoration_01",56],["street_trafficlines_01",47],["trash_walls_01",6],["appliances_cooking_01",53],["appliances_refrigeration_01",19],["fixtures_bathroom_01",67],["fixtures_counters_01",70],["furniture_bedding_01",37],["furniture_seating_indoor_03",99],["furniture_storage_01",30],["furniture_storage_02",45],["industry_01",35],["industry_02",68],["location_business_machinery_01",9],["location_community_church_small_01",29],["location_community_medical_01",28],["location_community_school_02",43],["location_restaurant_bar_01",13],["location_restaurant_seahorse_01",63],["location_shop_bargNclothes_01",53],["location_trailer_02",33],["walls_decoration_01",27],["walls_detailing_01",72],["walls_detailing_02",47],["walls_exterior_house_01",55],["walls_exterior_house_02",58],["walls_exterior_roofs_02",96],["walls_exterior_roofs_03",35],["walls_exterior_roofs_08",77],["walls_exterior_roofs_09",92],["walls_exterior_roofs_30_03",11],["walls_exterior_roofs_30_04",77],["walls_exterior_roofs_30_06",32],["walls_exterior_roofs_30_11",13],["walls_exterior_roofs_30_15",84],["walls_exterior_roofs_30_16",27],["walls_interior_bathroom_01",32],["walls_interior_house_04",20],["boulders",35],["d_wallcracks_1",41],["floors_rugs_01",33],["lighting_indoor_02",25],["overlay_graffiti_wall_01",73],["radio_tower",79],["recreational_01",31],["recreational_sports_01",145],["roofs_30_01",34],["roofs_30_02",59],["roofs_30_07",60],["roofs_30_08",82],["roofs_30_10",33],["roofs_accents_01",52],["roofs_shallow_01",15],["rooftop_furniture",42],["signs_miscbrands_01",54],["signs_one-off_02",191],["signs_one-off_09",46],["street_decoration_01",57],["street_trafficlines_01",49],["trash_walls_01",8],["appliances_cooking_01",55],["appliances_refrigeration_01",20],["fixtures_counters_01",71],["furniture_bedding_01",38],["furniture_seating_indoor_03",102],["furniture_storage_01",31],["industry_01",36],["industry_02",69],["location_business_machinery_01",10],["location_community_church_small_01",40],["location_community_medical_01",32],["location_community_school_02",44],["location_restaurant_bar_01",16],["location_trailer_02",34],["walls_decoration_01",51],["walls_detailing_01",73],["walls_detailing_02",48],["walls_exterior_house_01",59],["walls_exterior_house_02",74],["walls_exterior_roofs_02",97],["walls_exterior_roofs_03",36],["walls_exterior_roofs_09",105],["walls_exterior_roofs_30_03",20],["walls_exterior_roofs_30_04",84],["walls_exterior_roofs_30_06",43],["walls_exterior_roofs_30_11",36],["walls_exterior_roofs_30_16",28],["walls_interior_bathroom_01",33],["walls_interior_house_04",21],["boulders",40],["d_wallcracks_1",49],["floors_rugs_01",34],["lighting_indoor_02",31],["overlay_graffiti_wall_01",77],["radio_tower",92],["recreational_01",40],["recreational_sports_01",147],["roofs_30_01",44],["roofs_30_02",61],["roofs_30_07",61],["roofs_30_10",36],["roofs_accents_01",53],["roofs_shallow_01",22],["rooftop_furniture",44],["signs_miscbrands_01",55],["signs_one-off_02",196],["signs_one-off_09",47],["street_decoration_01",58],["appliances_cooking_01",63]]]
assert len(set(TARGETS))==len(TARGETS), 'duplicate target keys'

assert len(TARGETS)>=TARGET_COUNT,('not enough review targets',TARGETS)
print('v100 UNREVIEWED PREVIEW TARGETS',TARGETS,flush=True)
results=[]
for key in TARGETS:
    if key not in queue:
        results.append({'key':key,'status':'skipped_not_in_v99_queue'})
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
    'source':'GitHub original PNG and TMX','base':'v99','observed_count_added':0, 'excluded_early_v99_keys':0,
    'rendering':'approximate isometric, not TileZed; actual D only when other map or >=5 cells; absence explicitly shown',
    'original_tmx_suffix_note':'Repository files omit (2), but 5409/302177 scope counts match',
    'sha256':HASHES,'results':results},ensure_ascii=False,indent=2),encoding='utf8')

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
