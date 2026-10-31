#!/usr/bin/env python3
"""v187: audit six source-incomplete original TMX target scenes.
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
OUT=R/'review/v187_missing_neighbor6'
DBOUT=R/'analysis/current/v187'
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







# Six genuine B-C-positive unresolved keys: no other inbounds TMX site in 84 original maps.
targets=[197,198,685,4408,4409,3104]
src={int(r['index']):r for r in csvrows(R/'review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')}
held={int(r['index']):r for r in csvrows(R/'review/v183_original_BC_visual65/HELD_137.csv')}
census={int(r['index']):r for r in csvrows(R/'review/v180_remnant239_multisite/UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv')}
assert len(set(targets))==6
parent=json.loads((R/'analysis/current/v186/MANIFEST.json').read_text())
assert parent['version']=='v186' and parent['table_count']==248
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz-v187-missing-neighbor.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==248 and before['v186_object_reclassification']==49
for idx in targets:
 assert idx in src and idx in held and idx in census
 assert held[idx]['reason']=='true_B_C_positive_but_missing_neighbors_or_ambiguous'
 assert int(src[idx]['actual_B_C_pixels'])>=100
 assert int(src[idx]['full_context_missing_neighbor_sprites'])>=1
 assert census[idx]['status']=='no_other_new_inbounds_site_in_84_TMX'
 assert int(census[idx]['fresh_untried_inbounds_candidate_count_capped_3'])==0

def neighbor_diagnostics(m,loc):
 x0,y0=int(loc['source_x']),int(loc['source_y'])
 level=int(loc['source_level']);missing=[]
 for ly in m['layers']:
  if ly['level']!=level:continue
  for dy in range(-2,3):
   y=y0+dy
   if not 0<=y<m['h']:continue
   for dx in range(-2,3):
    x=x0+dx
    if not 0<=x<m['w']:continue
    v=ly['values'][y*m['w']+x]
    if not v:continue
    k=resolve(m,v)
    if sprite(k) is not None:continue
    dat=cand.get(k,{})
    selected=a.get(k,{})
    missing.append(dict(tile_set_name=k[0],local_id=k[1],
      layer_index=ly['index'],relative_dx=dx,relative_dy=dy,
      raw_gid=v,source_kind='new_A' if k in a else 'legacy_A',
      new_A_selected_status=selected.get('selection_status',''),
      new_A_source_image_path=selected.get('source_image_path',''),
      legacy_preferred_A=dat.get('new_preferred_A',''),
      legacy_source_png_path=dat.get('source_png_path',''),
      legacy_A1_bbox=dat.get('A1_bbox',''),
      legacy_A2_bbox=dat.get('A2_bbox',''),
      legacy_A3_crop_bbox=dat.get('A3_crop_bbox',''),
      reason='original_sprite_missing_or_no_trusted_pixel_crop'))
 return missing

rows=[];allmiss=[];sheets=[]
evidence_zip=OUT/'SOURCE_INCOMPLETE_SIX_ACTUAL_ABC.zip'
with zipfile.ZipFile(evidence_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for n,idx in enumerate(targets):
  t=src[idx];key=(t['tile_set_name'],int(t['local_id']))
  assert t['original_tmx'] in ('28_45.tmx','32_47.tmx','35_48.tmx')
  loc=dict(source_x=int(t['x']),source_y=int(t['y']),source_level=int(t['level']),
   source_layer_index=int(t['layer']),source_raw_gid=int(t['tmX_raw_gid']),
   tile_set_name=key[0],local_id=key[1])
  m=mapread(t['original_tmx'])
  assert resolve(m,loc['source_raw_gid'])==key
  assert filesha(ROOT/t['original_tmx'])==t['tmX_sha256']
  rec=a[key];assert rec['selection_status']=='selected_provisional'
  assert filesha(R/rec['source_image_path'])==rec['source_png_sha256']
  A=sprite(key)
  assert A is not None and sha(A.tobytes())==rec['selected_rgba_pixel_sha256']
  B,missB=scene(m,loc)
  C,missC=scene(m,loc,delete=True)
  assert missB==missC
  measured=difference(B,C)
  assert measured==int(t['actual_B_C_pixels']),('original_BC_pixel',idx,measured,t['actual_B_C_pixels'])
  diag=neighbor_diagnostics(m,loc)
  assert len(diag)==int(t['full_context_missing_neighbor_sprites'])==missB['missing_source'],('missing_neighbor_counts',idx,len(diag),missB)
  for d in diag:allmiss.append(dict(target_index=idx,target_tileset=key[0],target_local_id=key[1],**d))
  D=ImageChops.difference(B,C).convert('RGB')
  for lab,img in [('A_original',A),('B_original_TMX',B),('C_one_GID_removed',C),('BC_pixel_difference',D)]:
   z.writestr(f'{idx:05d}/{lab}.png',png_bytes(img))
  rows.append(dict(index=idx,tile_set_name=key[0],local_id=key[1],original_tmx=t['original_tmx'],
   layer_index=loc['source_layer_index'],level=loc['source_level'],x=loc['source_x'],y=loc['source_y'],
   source_raw_gid=loc['source_raw_gid'],original_A_RGBA_sha=sha(A.tobytes()),
   source_png_SHA=rec['source_png_sha256'],source_tmx_SHA=t['tmX_sha256'],
   B_C_pixels=measured,missing_neighbor_occurrences=len(diag),
   missing_neighbor_unique_keys=len({(e['tile_set_name'],e['local_id']) for e in diag}),
   other_original_inbounds_site=0,
   resolution='held_unresolved_missing_neighbor_original_A',
   identity_observed=0,mapping_verified=0,tilezed_verified=0,final_certified=0))
  board=Image.new('RGB',(1710,650),(237,243,249));draw=ImageDraw.Draw(board)
  draw.text((8,6),f'idx {idx} {key[0]}/{key[1]} Original B-C pixels {measured}; missing neighbor sprites {len(diag)}',fill=(24,40,60))
  for j,(label,img) in enumerate([('A SOURCE',A),('B ACTUAL TMX',B),('C ONE GID REMOVED',C),('TRUE B-C DIFF',D)]):
   xp=j*425;draw.text((xp+8,28),label,fill=(25,50,72))
   c=img.copy();c.thumbnail((415,565))
   pos=(xp+(425-c.width)//2,55+(550-c.height)//2)
   if c.mode=='RGBA':board.paste(c,pos,c)
   else:board.paste(c,pos)
  pic=OUT/f'SOURCE_INCOMPLETE_{idx}.jpg';board.save(pic,quality=88,optimize=True)
  sheets.append(pic.name)
  print('AUDITED',idx,'B-C',measured,'missing',[(d['tile_set_name'],d['local_id']) for d in diag],flush=True)
with zipfile.ZipFile(evidence_zip) as z:
 assert z.testzip() is None and len(z.namelist())==24
assert len(rows)==6 and len(allmiss)>=6

def writecsv(path,dat):
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(dat[0]));w.writeheader();w.writerows(dat)
writecsv(OUT/'SOURCE_BLOCKED_6.csv',rows)
writecsv(OUT/'MISSING_NEIGHBOR_KEYS.csv',allmiss)
unique_missing=sorted(set((x['tile_set_name'],x['local_id']) for x in allmiss))
summary=dict(version='v187',parent='v186',source_incomplete_true_BC_positive_cases=6,
 original_TMX_sources=sorted(set(x['original_tmx'] for x in rows)),original_B_C_positive=sum(x['B_C_pixels']>0 for x in rows),
 missing_neighbor_occurrences=len(allmiss),missing_neighbor_unique_keys=len(unique_missing),
 missing_neighbor_ids=[dict(tile_set_name=x[0],local_id=x[1]) for x in unique_missing],
 alternate_84_TMX_5x5_locations=0,source_reconstruction_zip_sha256=filesha(evidence_zip),
 missing_key_csv_sha256=filesha(OUT/'MISSING_NEIGHBOR_KEYS.csv'),audit_csv_sha256=filesha(OUT/'SOURCE_BLOCKED_6.csv'),
 evidence_contact_sheets=sheets,original_A_and_TMX_source_verified=6,
 new_observed=0,original_checkpoint_observed=9898,original_checkpoint_unobserved=144,
 final_identity_certified=0,official_mapping_verified=0,tilezed_verified=0)

cols=list(rows[0]);ints={'index','local_id','layer_index','level','x','y','source_raw_gid','B_C_pixels',
 'missing_neighbor_occurrences','missing_neighbor_unique_keys','other_original_inbounds_site','identity_observed','mapping_verified','tilezed_verified','final_certified'}
db.execute('CREATE TABLE v187_missing_neighbor_audit ('+','.join('"'+k+'" '+('INTEGER' if k in ints else 'TEXT') for k in cols)+',PRIMARY KEY(tile_set_name,local_id),CHECK(identity_observed=0 AND final_certified=0))')
db.executemany('INSERT INTO v187_missing_neighbor_audit ('+','.join('"'+k+'"' for k in cols)+') VALUES ('+','.join('?' for k in cols)+')',[tuple(q[k] for k in cols) for q in rows])
db.commit()
after={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==249 and set(after)-set(before)=={'v187_missing_neighbor_audit'}
assert all(after[k]==v for k,v in before.items()) and after['v187_missing_neighbor_audit']==6
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();comp=zlib.compress(newraw,8)
encoded=base64.b64encode(comp).decode('ascii');parts=[]
for i in range(0,len(encoded),3000000):
 p=DBOUT/f'v187.part{i//3000000:03}.b64';p.write_text(encoded[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v187',parent='v186',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(comp),sqlite_bytes=len(newraw),
 parts=parts,table_count=249,prior_tables_preserved=248,new_rows=6,new_observed_rows=0,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
summary.update(physical_SQLite_table_count=249,parent_tables_preserved=248,sqlite_sha256=sha(newraw))
(OUT/'MANIFEST.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v187 원본 B-C 양수이지만 이웃 PNG 누락으로 보류된 6종 근거 조사\n\n'
 '197,198(캠핑),685(카운터),4408/4409(욕실 벽),3104(밭작물)의 기존 원본 TMX 실제 층/좌표/GID/A RGBA 픽셀/원본 PNG·TMX SHA/B-C 차이값을 재검증하고 이웃 누락의 원인이 되는 타일 키를 열거함. 원본 84 TMX 전수조사에서도 이 6개는 다른 5×5 대체 위치가 없어 그대로 held.\n'
 '6개의 A/B/C/DIFF 원본 PNG 24장 ZIP과 6개의 가로 비교 JPG, 이웃 누락 상세 CSV를 제공한다. 누락된 타일의 원본 A가 없으면 임의 스프라이트나 상상 그림으로 배경을 채우지 않는다. 실제 눈으로 대상 정체를 인증하는 것도 이번에는 보류. 따라서 누적 9898/10042(98.57%)와 미관찰 144 유지.\n'
 '물리 SQLite 부모 v186 248테이블의 모든 행 값/수를 그대로 보존하고 증거감사6행 249번째 테이블만 추가. TileZed↔Local ID/공식 이미지 대응·최종 사물 정체 인증 0.\n',encoding='utf-8')
print('PASS v187 actual source missing neighbor audit',json.dumps(summary,ensure_ascii=False),flush=True)
