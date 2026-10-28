#!/usr/bin/env python3
"""v180: audit 239 actually missing new A keys at all 84 original TMX maps.
Seek additional distinct same-GID scenes, render up to 64 keys with up to 3
untried scenes each; pick strongest actual B-C delta, never mark identity.
"""
from pathlib import Path
from collections import defaultdict,Counter
from functools import lru_cache
import bisect,csv,hashlib,base64,zlib,json,sqlite3,re,io,zipfile
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageEnhance
R=Path(__file__).resolve().parents[1]
ROOT=R/'B4220.3_MapExport_256/tmx'
OUT=R/'review/v185_crop3102_source'
DBOUT=R/'analysis/current/v185'
SHEETS=OUT/'sheets'
for d in [OUT,DBOUT,SHEETS]:d.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for z in iter(lambda:f.read(8*1024*1024),b''):h.update(z)
 return h.hexdigest()
def csvrows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bbox(v):
 if not v:return None
 a=tuple(map(int,v.strip('[]').split(',')))
 assert len(a)==4
 return a
W,H=800,580
a={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')}
cand={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv')}
assert len(a)==4633 and len(cand)==10042
def layerlevel(ly):
    if 'level' in ly.attrib:
        return int(ly.get('level','0'))
    prop=ly.find("properties/property[@name='level']")
    return int((prop.get('value') or prop.text or '0') if prop is not None else '0')

def mapread(name):
    tree=ET.parse(ROOT/name).getroot()
    ts=sorted((int(x.get('firstgid')),x.get('name')) for x in tree.findall('tileset') if x.get('name'))
    first=[v[0] for v in ts]
    w,h=int(tree.get('width','256')),int(tree.get('height','256'))
    layers=[]
    for ix,ly in enumerate(tree.iter('layer')):
        dat=ly.find('data')
        assert dat is not None and dat.get('encoding')=='csv'
        vals=[int(v) for v in re.findall(r'\d+',dat.text or '')]
        assert len(vals)==w*h
        layers.append(dict(index=ix,level=layerlevel(ly),values=vals))
    return dict(ts=ts,first=first,layers=layers,w=w,h=h)
def resolve(m,raw):
    gid=raw&0x0fffffff
    if not gid:return None
    pos=bisect.bisect_right(m['first'],gid)-1
    if pos<0:return None
    return (m['ts'][pos][1],gid-m['ts'][pos][0])
@lru_cache(maxsize=5)
def atlas(path):
    if not path:return None
    with Image.open(R/path) as im:return im.convert('RGBA')
@lru_cache(maxsize=1600)
def sprite(k):
    rec=a.get(k)
    if rec:
        path=rec['source_image_path'];box=bbox(rec['selected_crop_xyxy'])
        expected=rec['selected_rgba_pixel_sha256']
    else:
        rec=cand.get(k)
        if not rec:return None
        path=rec.get('source_png_path','')
        key=rec.get('new_preferred_A','')
        if key=='A3':box=bbox(rec.get('A3_crop_bbox',''));expected=rec.get('A3_pixel_sha256','')
        elif key in ('A1','A1=A2'):box=bbox(rec.get('A1_bbox',''));expected=rec.get('A1_pixel_sha256','')
        elif key=='A2':box=bbox(rec.get('A2_bbox',''));expected=rec.get('A2_pixel_sha256','')
        else:return None
    if not path or not box or not expected:return None
    src=atlas(path)
    if src is None or box[0]<0 or box[1]<0 or box[2]>src.width or box[3]>src.height:return None
    img=src.crop(box)
    assert sha(img.tobytes())==expected,(k,'old A pixel drift')
    return img if img.getbbox() else None
def flips(img,raw):
    if raw&0x20000000:img=img.transpose(Image.Transpose.TRANSPOSE)
    if raw&0x80000000:img=img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if raw&0x40000000:img=img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return img
W,H=800,580
def scene(m,loc,replacement=None,delete=False):
    x0,y0=int(loc['source_x']),int(loc['source_y'])
    level=int(loc['source_level'])
    layerid=int(loc['source_layer_index'])
    rawtarget=int(loc['source_raw_gid'])
    index=y0*m['w']+x0
    raw=m['layers'][layerid]['values'][index]
    assert raw==rawtarget and resolve(m,raw)==(loc['tile_set_name'],int(loc['local_id']))
    canvas=Image.new('RGBA',(W,H),(237,242,247,255))
    replacement_drawn=0;misses=Counter()
    for layer in m['layers']:
        if layer['level']!=level:continue
        commands=[]
        for dy in range(-2,3):
            y=y0+dy
            if not 0<=y<m['h']:continue
            for dx in range(-2,3):
                x=x0+dx
                if not 0<=x<m['w']:continue
                p=y*m['w']+x;gid=layer['values'][p]
                if gid:commands.append((dx+dy,dy,dx,p,gid))
        commands.sort()
        for _,dy,dx,p,gid in commands:
            istarget=layer['index']==layerid and p==index and gid==rawtarget
            if istarget and delete:
                replacement_drawn+=1
                continue
            if istarget and replacement is not None:
                image=replacement
                replacement_drawn+=1
            else:
                image=sprite(resolve(m,gid))
            if image is None:misses['missing_source']+=1;continue
            image=flips(image,gid)
            px=int(W/2+(dx-dy)*58-image.width/2)
            py=int(H/2+(dx+dy)*29+34-image.height)
            if px<0 or py<0 or px+image.width>W or py+image.height>H:
                clip=(max(0,-px),max(0,-py),min(image.width,W-px),min(image.height,H-py))
                if clip[2]<=clip[0] or clip[3]<=clip[1]:
                    misses['outside_canvas']+=1
                    continue
                image=image.crop(clip);px=max(0,px);py=max(0,py)
            canvas.alpha_composite(image,(px,py))
    if replacement is not None or delete:assert replacement_drawn==1,(loc,replacement_drawn)
    return canvas.convert('RGB'),dict(misses)
def difference(a,b):
    img=ImageChops.difference(a,b).convert('L')
    return sum(px!=0 for px in img.getdata())


def pixels_nontransparent(im):
    return sum(im.getchannel('A').histogram()[1:])
def png_bytes(img):
    f=io.BytesIO();img.save(f,format='PNG');return f.getvalue()



def layerlevel(ly):
    if 'level' in ly.attrib:
        return int(ly.get('level','0'))
    prop=ly.find("properties/property[@name='level']")
    return int((prop.get('value') or prop.text or '0') if prop is not None else '0')

def mapread(name):
    tree=ET.parse(ROOT/name).getroot()
    ts=sorted((int(x.get('firstgid')),x.get('name')) for x in tree.findall('tileset') if x.get('name'))
    first=[v[0] for v in ts]
    w,h=int(tree.get('width','256')),int(tree.get('height','256'))
    layers=[]
    for ix,ly in enumerate(tree.iter('layer')):
        dat=ly.find('data')
        assert dat is not None and dat.get('encoding')=='csv'
        vals=[int(v) for v in re.findall(r'\d+',dat.text or '')]
        assert len(vals)==w*h
        layers.append(dict(index=ix,level=layerlevel(ly),values=vals))
    return dict(ts=ts,first=first,layers=layers,w=w,h=h)
def resolve(m,raw):
    gid=raw&0x0fffffff
    if not gid:return None
    pos=bisect.bisect_right(m['first'],gid)-1
    if pos<0:return None
    return (m['ts'][pos][1],gid-m['ts'][pos][0])
@lru_cache(maxsize=5)
def atlas(path):
    if not path:return None
    with Image.open(R/path) as im:return im.convert('RGBA')
@lru_cache(maxsize=1600)
def sprite(k):
    rec=a.get(k)
    if rec:
        path=rec['source_image_path'];box=bbox(rec['selected_crop_xyxy'])
        expected=rec['selected_rgba_pixel_sha256']
    else:
        rec=cand.get(k)
        if not rec:return None
        path=rec.get('source_png_path','')
        key=rec.get('new_preferred_A','')
        if key=='A3':box=bbox(rec.get('A3_crop_bbox',''));expected=rec.get('A3_pixel_sha256','')
        elif key in ('A1','A1=A2'):box=bbox(rec.get('A1_bbox',''));expected=rec.get('A1_pixel_sha256','')
        elif key=='A2':box=bbox(rec.get('A2_bbox',''));expected=rec.get('A2_pixel_sha256','')
        else:return None
    if not path or not box or not expected:return None
    src=atlas(path)
    if src is None or box[0]<0 or box[1]<0 or box[2]>src.width or box[3]>src.height:return None
    img=src.crop(box)
    assert sha(img.tobytes())==expected,(k,'old A pixel drift')
    return img if img.getbbox() else None
def flips(img,raw):
    if raw&0x20000000:img=img.transpose(Image.Transpose.TRANSPOSE)
    if raw&0x80000000:img=img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if raw&0x40000000:img=img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return img
W,H=800,580
def scene(m,loc,replacement=None,delete=False):
    x0,y0=int(loc['source_x']),int(loc['source_y'])
    level=int(loc['source_level'])
    layerid=int(loc['source_layer_index'])
    rawtarget=int(loc['source_raw_gid'])
    index=y0*m['w']+x0
    raw=m['layers'][layerid]['values'][index]
    assert raw==rawtarget and resolve(m,raw)==(loc['tile_set_name'],int(loc['local_id']))
    canvas=Image.new('RGBA',(W,H),(237,242,247,255))
    replacement_drawn=0;misses=Counter()
    for layer in m['layers']:
        if layer['level']!=level:continue
        commands=[]
        for dy in range(-2,3):
            y=y0+dy
            if not 0<=y<m['h']:continue
            for dx in range(-2,3):
                x=x0+dx
                if not 0<=x<m['w']:continue
                p=y*m['w']+x;gid=layer['values'][p]
                if gid:commands.append((dx+dy,dy,dx,p,gid))
        commands.sort()
        for _,dy,dx,p,gid in commands:
            istarget=layer['index']==layerid and p==index and gid==rawtarget
            if istarget and delete:
                replacement_drawn+=1
                continue
            if istarget and replacement is not None:
                image=replacement
                replacement_drawn+=1
            else:
                image=sprite(resolve(m,gid))
            if image is None:misses['missing_source']+=1;continue
            image=flips(image,gid)
            px=int(W/2+(dx-dy)*58-image.width/2)
            py=int(H/2+(dx+dy)*29+34-image.height)
            if px<0 or py<0 or px+image.width>W or py+image.height>H:
                clip=(max(0,-px),max(0,-py),min(image.width,W-px),min(image.height,H-py))
                if clip[2]<=clip[0] or clip[3]<=clip[1]:
                    misses['outside_canvas']+=1
                    continue
                image=image.crop(clip);px=max(0,px);py=max(0,py)
            canvas.alpha_composite(image,(px,py))
    if replacement is not None or delete:assert replacement_drawn==1,(loc,replacement_drawn)
    return canvas.convert('RGB'),dict(misses)
def difference(a,b):
    img=ImageChops.difference(a,b).convert('L')
    return sum(px!=0 for px in img.getdata())


def pixels_nontransparent(im):
    return sum(im.getchannel('A').histogram()[1:])
def png_bytes(img):
    f=io.BytesIO();img.save(f,format='PNG');return f.getvalue()





# v180 census itself already verified the three distinct original 3102 GID occurrences.
# The highest-change alternate scene had one missing neighbor; select the independently
# documented third original location with zero missing source sprites, and re-render.
key=('vegetation_farming_01b',21)
old=csvrows(R/'review/v180_remnant239_multisite/ALTERNATE_SELECTED_SCENES.csv')
prior=[q for q in old if (q['tile_set_name'],int(q['local_id']))==key]
assert len(prior)==1 and int(prior[0]['index'])==3102
locs=json.loads(prior[0]['all_tried_site_evidence'])
assert len(locs)==3,('original_alt_3_sites',locs)
choice=locs[2]
assert choice['tmx']=='35_48.tmx' and choice['layer_index']==2 and choice['level']==0
assert (choice['x'],choice['y'],choice['raw_gid'])==(93,141,23718)
assert choice['delta_pixels']>=100 and choice['missing_source']==0 and choice['outside_canvas']==0
assert filesha(ROOT/choice['tmx'])==choice['real_TMX_sha256']
loc=dict(source_x=choice['x'],source_y=choice['y'],source_level=choice['level'],
 source_layer_index=choice['layer_index'],source_raw_gid=choice['raw_gid'],
 tile_set_name=key[0],local_id=key[1])
m=mapread(choice['tmx'])
assert resolve(m,choice['raw_gid'])==key
orig=a[key]
assert orig['selection_status']=='selected_provisional'
assert filesha(R/orig['source_image_path'])==orig['source_png_sha256']
A=sprite(key)
assert A is not None and sha(A.tobytes())==orig['selected_rgba_pixel_sha256']
B,missB=scene(m,loc)
C,missC=scene(m,loc,delete=True)
assert missB==missC=={},('neighbor_sources_missing',missB,missC)
pixels=difference(B,C)
assert pixels==choice['delta_pixels'] and pixels>=100,('verified_original_B-C',pixels,choice)
D=ImageChops.difference(B,C).convert('RGB')
evidence_zip=OUT/'3102_ALT_TRUE_SOURCE_ABC.zip'
with zipfile.ZipFile(evidence_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for name,img in [('A_original',A),('B_original_TMX',B),('C_exact_one_GID_removed',C),('B_minus_C_raw',D)]:
  z.writestr(name+'.png',png_bytes(img))
with zipfile.ZipFile(evidence_zip) as z:
 assert z.testzip() is None and len(z.namelist())==4
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
sheet=Image.new('RGB',(1800,670),(241,245,249));drawer=ImageDraw.Draw(sheet)
for i,(name,img) in enumerate([('A ORIGINAL',A),('B TRUE TMX',B),('C ONE GID REMOVED',C),('RGB B-C DIFF',D)]):
 q=img.copy();q.thumbnail((438,520))
 x=i*450+(450-q.width)//2;y=75+(520-q.height)//2
 if q.mode=='RGBA':sheet.paste(q,(x,y),q)
 else:sheet.paste(q,(x,y))
 drawer.text((i*450+15,20),name,fill=(32,47,68),font=font)
sheet.save(OUT/'3102_ALT_TRUE_ABC.jpg',quality=90,optimize=True)
obs={
 'index':3102,'tile_set_name':key[0],'local_id':key[1],
 'source_tmx':choice['tmx'],'source_layer':choice['layer_index'],'source_level':choice['level'],
 'source_x':choice['x'],'source_y':choice['y'],'source_raw_gid':choice['raw_gid'],
 'source_png':orig['source_image_path'],
 'source_png_sha256':orig['source_png_sha256'],
 'source_RGBA_pixel_sha256':orig['selected_rgba_pixel_sha256'],
 'source_TMX_sha256':choice['real_TMX_sha256'],
 'actual_original_B_C_pixels':pixels,'missing_neighbor_source':0,
 'candidate':'밭에서 여러 줄기와 잎을 위로 세운 녹색 작물 묶음',
 'features':'흙 이랑 세 줄에서 가는 수직 줄기와 작은 녹색 잎들이 자라는 형태. 실제 농경지 줄 식재 배치와 일치',
 'part':'밭작물 성장 단계의 여러 줄기/잎 군락',
 'material':'식물/흙',
 'confidence':'medium','orientation':'unverified','connections':'unverified',
 'review_status':'provisional_candidate',
 'evidence_basis':'Source A 3102 original crop and original TMX 35_48.tmx at layer2 floor0 x93 y141, exactly original raw GID23718 removed for C, nonzero 7650 changed pixels, all 5x5 neighbors with actual PNG and no canvas clipping; prior representative B was missing a neighbor.',
 'mapping_verified':0,'tilezed_verified':0,'certified':0}
parent=json.loads((R/'analysis/current/v184/MANIFEST.json').read_text())
enc=''.join((R/p).read_text('ascii').strip() for p in parent['parts'])
packed=base64.b64decode(enc,validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz-v185-crop3102.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==246 and before['v184_visual_review']==3
assert db.execute('SELECT COUNT(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',key).fetchone()[0]==1
assert db.execute('SELECT COUNT(*) FROM v183_visual_review WHERE tile_set_name=? AND local_id=?',key).fetchone()[0]==0
assert db.execute('SELECT COUNT(*) FROM v184_visual_review WHERE tile_set_name=? AND local_id=?',key).fetchone()[0]==0
cols=list(obs)
ints={'index','local_id','source_layer','source_level','source_x','source_y','source_raw_gid','actual_original_B_C_pixels','missing_neighbor_source','mapping_verified','tilezed_verified','certified'}
db.execute('CREATE TABLE v185_visual_review ('+','.join('"'+k+'" '+('INTEGER' if k in ints else 'TEXT') for k in cols)+',PRIMARY KEY(tile_set_name,local_id),CHECK(certified=0 AND tilezed_verified=0 AND mapping_verified=0))')
db.execute('INSERT INTO v185_visual_review ('+','.join('"'+k+'"' for k in cols)+') VALUES ('+','.join('?' for _ in cols)+')',tuple(obs[k] for k in cols))
db.commit()
after={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==247 and set(after)-set(before)=={'v185_visual_review'}
assert all(after[n]==v for n,v in before.items()) and after['v185_visual_review']==1
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();compressed=zlib.compress(newraw,8)
coded=base64.b64encode(compressed).decode('ascii');parts=[]
for i in range(0,len(coded),3000000):
 p=DBOUT/f'v185.part{i//3000000:03}.b64'
 p.write_text(coded[i:i+3000000],encoding='ascii')
 parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v185',parent='v184',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(compressed),sqlite_bytes=len(newraw),
 parts=parts,table_count=247,prior_tables_preserved=246,new_rows=1,new_observed_rows=1,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
with (OUT/'VISUAL_REVIEW_1.csv').open('w',newline='',encoding='utf-8-sig') as h:
 w=csv.DictWriter(h,fieldnames=cols);w.writeheader();w.writerow(obs)
manifest=dict(version='v185',parent='v184',manual_original_source_alt_BC_reexamined=1,
 promoted_provisional=1,index=3102,actual_B_C_pixels=pixels,
 actual_missing_neighbor_sources=0,physical_database_tables=247,
 parent_tables_preserved=246,observed_parent=9897,observed_now=9898,
 remaining_checkpoint=144,remaining_distinct=142,unresolved_two_count_discrepancy=2,
 original_A_RGBA_verified=1,original_TMX_GID_verified=1,
 visual_csv_sha256=filesha(OUT/'VISUAL_REVIEW_1.csv'),
 images_zip_sha256=filesha(evidence_zip),sqlite_sha256=sha(newraw),
 final_identity_certified=0,official_mapping_verified=0,tilezed_verified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v185 기존 주변 PNG 누락 보류 3102를 실제 다른 TMX 장면에서 재검수\n\n'
 'v183은 3102 (vegetation_farming_01b/21)가 실제 원래 B-C=7356픽셀이지만 주변 PNG 1개 누락 때문에 보류했다. v180 원본 84 TMX 다중배치 증거에서는 35_48.tmx 층0 레이어2에 타일 3개 실제 반복이 있으며, 세번째 좌표 93,141은 같은 raw GID23718이지만 주변 PNG 누락0, 정확히 그 GID 제거 C에 대한 변화 7650픽셀과 캔버스 이상0이 확인되어 있음을 발견했다. 본 작업에서 원본 A 픽셀/TMX SHA/GID를 직접 재확인하고 B/C/차이 재렌더와 ZIP을 생성, 시각적으로 관찰되는 가는 줄기와 녹색 잎의 밭작물 군락을 잠정 후보로 기록한다. 작물 종류·성장단계 정확명/공식 TileZed LocalID는 인증하지 않는다.\n'
 '부모 v184 246개 테이블 전 행값/행수 보존한 채 신규 v185 관찰 1행 테이블 하나 추가(247테이블). 원본 PNG/TMX와 기존5409/사용자 수동80·제외14·held D2/JUMBO20 불변.\n',encoding='utf-8')
print('PASS v185 direct original TMX crop source',json.dumps(manifest,ensure_ascii=False),flush=True)
