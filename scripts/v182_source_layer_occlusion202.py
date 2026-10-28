#!/usr/bin/env python3
"""v182: audit 239 actually missing new A keys at all 84 original TMX maps.
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
OUT=R/'review/v182_occlusion202'
DBOUT=R/'analysis/current/v182'
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
def scene(m,loc,replacement=None,delete=False,through_layer=None):
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
        if layer['level']!=level or (through_layer is not None and layer['index']>through_layer):continue
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
def scene(m,loc,replacement=None,delete=False,through_layer=None):
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
        if layer['level']!=level or (through_layer is not None and layer['index']>through_layer):continue
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





# v175 source ledger minus exactly three proven appended visual batches.
ledger=csvrows(R/'review/v175_remaining381_evidence_audit/REMAINING_381_EVIDENCE_AUDIT.csv')
assert len(ledger)==379
prev=[]
for file,num in [('review/v177_alternate_visual23/VISUAL_REVIEW_23.csv',23),('review/v179_alternative163_visual/VISUAL_REVIEW_108.csv',108),('review/v181_multisite_visual37/VISUAL_REVIEW_37.csv',37)]:
 q=csvrows(R/file);assert len(q)==num,(file,len(q))
 prev+=q
seen={(r['tile_set_name'],int(r['local_id'])) for r in prev}
assert len(seen)==168
records=[r for r in ledger if r['origin']=='new_A_4633' and (r['tile_set_name'],int(r['local_id'])) not in seen]
records.sort(key=lambda r:(r['original_scene_tmx'],int(r['index'])))
assert len(records)==202,('unobserved 202 source keys',len(records))
assert len({(r['tile_set_name'],int(r['local_id'])) for r in records})==202
parent=json.loads((R/'analysis/current/v181/MANIFEST.json').read_text())
compressed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(compressed)==parent['compressed_sha256']
raw=zlib.decompress(compressed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
dbpath=Path('/tmp/pz-v182-unseen202.sqlite');dbpath.write_bytes(raw)
db=sqlite3.connect(dbpath)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={x[0]:db.execute('SELECT COUNT(*) FROM "'+x[0]+'"').fetchone()[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==243 and before['v181_visual_review']==37
for rec in records:
 assert db.execute('SELECT count(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',(rec['tile_set_name'],int(rec['local_id']))).fetchone()==1
scenezip=zipfile.ZipFile(OUT/'OCCLUSION_ACTUAL_BC_AND_LAYER_DIAGNOSTIC.zip','w',zipfile.ZIP_DEFLATED,compresslevel=5)
results=[]
# TMX map data cache avoids repeated parse of very large maps.
mapread=lru_cache(maxsize=3)(mapread)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for i,rec in enumerate(records):
 key=(rec['tile_set_name'],int(rec['local_id']));idx=int(rec['index'])
 record=dict(index=idx,tile_set_name=key[0],local_id=key[1],original_tmx=rec['original_scene_tmx'],
 layer=rec['original_scene_layer'],level=rec['original_scene_level'],x=rec['original_scene_x'],
 y=rec['original_scene_y'],source_A_status=rec['selected_A_status'],original_B_C_pixels=rec['B_C_changed_pixels'],
 actual_B_C_pixels='',layer_limited_B_C_pixels='',original_source_A_pixels_verified=0,
 tmX_raw_gid='',tmX_sha256='',full_context_missing_neighbor_sprites='',isolated_context_missing_neighbor_sprites='',
 original_B_C_zero=rec['B_C_changed_pixels']=='0',
 source_full_map_5x5_clipped=rec['B_map_edge'],
 alternate_scene_candidates_known=rec['eligible_for_visual_followup'],manual_visual_completed=0,
 observed_new=0,certified=0,official_mapping_verified=0,tilezed_verified=0,classification='')
 if not rec['source_png'] or not a.get(key,{}).get('selected_crop_xyxy'):
  record['classification']='original_A_missing_held'
  results.append(record)
  continue
 A=sprite(key)
 if A is None:
  record['classification']='original_A_missing_or_transparent_held'
  results.append(record)
  continue
 assert sha(A.tobytes())==a[key]['selected_rgba_pixel_sha256']
 assert filesha(R/a[key]['source_image_path'])==a[key]['source_png_sha256']
 record['original_source_A_pixels_verified']=1
 if not rec['original_scene_tmx'] or rec['original_scene_layer']=='' or rec['original_scene_x']=='':
  record['classification']='original_representative_TMX_missing_held'
  results.append(record)
  continue
 m=mapread(rec['original_scene_tmx'])
 layer=int(rec['original_scene_layer']);x=int(rec['original_scene_x']);y=int(rec['original_scene_y']);lvl=int(rec['original_scene_level'])
 assert 0<=layer<len(m['layers']) and 0<=x<m['w'] and 0<=y<m['h']
 rawgid=m['layers'][layer]['values'][y*m['w']+x]
 assert resolve(m,rawgid)==key,('real_gid_key_mismatch',idx,key)
 assert m['layers'][layer]['level']==lvl
 record['tmX_raw_gid']=rawgid
 record['tmX_sha256']=filesha(ROOT/rec['original_scene_tmx'])
 loc=dict(source_x=x,source_y=y,source_level=lvl,source_layer_index=layer,source_raw_gid=rawgid,
   tile_set_name=key[0],local_id=key[1])
 # TRUE reconstructed source TMX scene B and one raw-GID removed C.
 B,missB=scene(m,loc)
 C,missC=scene(m,loc,delete=True)
 assert missB==missC
 # DIAGNOSTIC ONLY: same original TMX scene but hide layers higher than target.
 # X/Y is NOT the original map B/C, and NEVER constitutes an official D alternate-A.
 X,missX=scene(m,loc,through_layer=layer)
 Y,missY=scene(m,loc,delete=True,through_layer=layer)
 assert missX==missY
 delta=difference(B,C);exposed=difference(X,Y)
 record['actual_B_C_pixels']=delta
 record['layer_limited_B_C_pixels']=exposed
 record['full_context_missing_neighbor_sprites']=missB.get('missing_source',0)
 record['isolated_context_missing_neighbor_sprites']=missX.get('missing_source',0)
 record['classification']='visible_actual_B_C_requires_direct_visual_inspection' if delta>=100 and not missB.get('missing_source',0) else (
   'diagnostic_only_target_masking_candidates_not_source_scene' if exposed>=100 and delta<100 else (
   'small_or_occluded_or_neighbor_source_missing_held'))
 imgs=[('A_original.png',A),('B_true_TMX.png',B),('C_true_TMX_target_removed.png',C),
       ('X_target_level_visible_diagnostic.png',X),('Y_target_level_removed_diagnostic.png',Y),
       ('X_minus_Y_DIAGNOSTIC.png',ImageChops.difference(X,Y).convert('RGB'))]
 for label,img in imgs:
  scenezip.writestr(f'{idx:05d}/{label}',png_bytes(img))
 results.append(record)
 if (i+1)%15==0:print('v182 SOURCE',i+1,'/202','current',idx,'original changed',delta,'diagnostic changed',exposed,flush=True)
scenezip.close()
with zipfile.ZipFile(OUT/'OCCLUSION_ACTUAL_BC_AND_LAYER_DIAGNOSTIC.zip') as z:
 assert z.testzip() is None
 assert len(z.namelist())==6*sum(int(r['original_source_A_pixels_verified']) and r['tmX_raw_gid']!='' for r in results)
# Prepare 6 per sheet with original A, actual B, exposed diagnostic X, X-Y; each sheet
# is only an annotation aid, not an official scene nor identity confirmation.
with zipfile.ZipFile(OUT/'OCCLUSION_ACTUAL_BC_AND_LAYER_DIAGNOSTIC.zip') as z:
 rendered=[r for r in results if r['tmX_raw_gid']!='']
 for batch in range((len(rendered)+5)//6):
  board=Image.new('RGB',(1750,1530),(230,237,246));drawer=ImageDraw.Draw(board)
  for j,rec in enumerate(rendered[batch*6:(batch+1)*6]):
   y=j*255;idx=int(rec['index']);k=(rec['tile_set_name'],int(rec['local_id']))
   drawer.rectangle((3,y+2,1745,y+253),fill=(255,255,255),outline=(175,184,202))
   drawer.text((12,y+7),f"{idx} | {k[0]}/{k[1]} | original B-C {rec['actual_B_C_pixels']} | layer-masked X-Y {rec['layer_limited_B_C_pixels']}",
    font=font,fill=(28,47,74))
   for n,(label,imgpath) in enumerate([
     ('SOURCE A',f'{idx:05d}/A_original.png'),('TRUE B (TMX)',f'{idx:05d}/B_true_TMX.png'),
     ('LAYER-MASKED X (NOT MAP)',f'{idx:05d}/X_target_level_visible_diagnostic.png'),
     ('X-Y (DIAGNOSTIC)',f'{idx:05d}/X_minus_Y_DIAGNOSTIC.png')
    ]):
    p=io.BytesIO(z.read(imgpath))
    with Image.open(p) as im:q=im.convert('RGBA')
    q.thumbnail((410,190))
    x=n*435
    drawer.text((x+8,y+29),label,font=font,fill=(86,95,111))
    pos=(x+(430-q.width)//2,y+52+(193-q.height)//2)
    board.paste(q,pos,q)
  board.save(SHEETS/f'SOURCE_LAYER_DIAGNOSTIC_{batch:02d}.jpg',quality=83,optimize=True)
assert len(results)==202
fields=list(results[0])
with (OUT/'SOURCE_OCCLUSION_202.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(results)
# Existing physical DB remains unchanged except a segregated evidence-audit table.
types={k:'INTEGER' if k in ('index','local_id','tmX_raw_gid','original_source_A_pixels_verified','manual_visual_completed',
 'observed_new','certified','official_mapping_verified','tilezed_verified') else 'TEXT' for k in fields}
db.execute('CREATE TABLE v182_source_layer_occlusion_audit ('+','.join('"'+k+'" '+types[k] for k in fields)+', PRIMARY KEY(tile_set_name,local_id),CHECK(observed_new=0 AND certified=0 AND official_mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v182_source_layer_occlusion_audit ('+','.join('"'+k+'"' for k in fields)+') VALUES ('+','.join('?' for k in fields)+')',
 [tuple(r[k] for k in fields) for r in results])
db.commit()
after={x[0]:db.execute('SELECT COUNT(*) FROM "'+x[0]+'"').fetchone()[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==244 and set(after)-set(before)=={'v182_source_layer_occlusion_audit'}
assert all(after[k]==v for k,v in before.items())
assert after['v182_source_layer_occlusion_audit']==202
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=dbpath.read_bytes();newpack=zlib.compress(newraw,8)
encoded=base64.b64encode(newpack).decode('ascii');parts=[]
for i in range(0,len(encoded),3000000):
 p=DBOUT/f'v182.part{i//3000000:03}.b64';p.write_text(encoded[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/k).read_text('ascii').strip() for k in parts))))==sha(newraw)
dbm=dict(version='v182',parent='v181',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(newpack),sqlite_bytes=len(newraw),parts=parts,
 table_count=244,prior_tables_preserved=243,new_rows=202,new_observed_rows=0,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
summary=dict(version='v182',source_new_key_unobserved_before=202,source_new_key_unobserved_after=202,
 parent_checkpoint_observed=9829,parent_checkpoint_missing=213,
 original_9_unobserved_held=9,historical_checkpoint_count_discrepancy=2,
 true_original_png_verified=sum(r['original_source_A_pixels_verified'] for r in results),
 true_original_TMXS_rendered=sum(r['tmX_raw_gid']!='' for r in results),
 original_B_C_positive=sum(isinstance(r['actual_B_C_pixels'],int) and r['actual_B_C_pixels']>0 for r in results),
 diagnostic_mask_positive=sum(isinstance(r['layer_limited_B_C_pixels'],int) and r['layer_limited_B_C_pixels']>0 for r in results),
 diagnostic_visible_but_original_zero=sum(isinstance(r['actual_B_C_pixels'],int) and r['actual_B_C_pixels']==0
   and isinstance(r['layer_limited_B_C_pixels'],int) and r['layer_limited_B_C_pixels']>0 for r in results),
 missing_source_A=sum(r['classification']=='original_A_missing_held' for r in results),
 original_B_C_not_yet_manually_certified=202,
 physical_sqlite_tables=244,prior_tables_preserved=243,new_observed=0,
 final_certified=0,official_mapping_verified=0,tilezed_verified=0,
 evidence_csv_sha256=filesha(OUT/'SOURCE_OCCLUSION_202.csv'),
 image_evidence_zip_sha256=filesha(OUT/'OCCLUSION_ACTUAL_BC_AND_LAYER_DIAGNOSTIC.zip'),
 contact_sheets=[x.name for x in sorted(SHEETS.glob('*.jpg'))],db_sha256=sha(newraw))
(OUT/'MANIFEST.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v182 실제 미관찰 새 A 키 202종 원본 장면/가림 레이어 전수진단\n\n'
 'v175의 새 키 370 중 실제 원본 A/B/C 장면을 육안 검토하여 잠정승격된 v177 23, v179 108, v181 37(합 168)을 제외한 202개 고유키를 추적합니다. 이 단계에서 원본 A PNG 크롭 픽셀 해시와 실제 최초 TMX raw GID/좌표/층/레이어를 검증하고, 실제 장면 B/한 GID 제거 C를 다시 렌더합니다.\n'
 '추가 X/Y는 위쪽 TMX 레이어를 의도적으로 감춘 *진단용 합성*이며 원본 B/C나 사용자 정의 D 이미지가 아닙니다. 원본 B-C가 0이어도 X-Y가 양수면 위 레이어가 가리는 가능성을 찾아 다음 육안 시각 판독 우선순위로 삼습니다. 그 숫자만으로 물체 정체/방향·실제 재질·TileZed 공식 ID를 인증하거나 관찰 완료 처리하면 안 됩니다.\n'
 '202개 고유키의 실제 원본/진단 비교 CSV, 6이미지/정상타일 ZIP, 6타일당 한 장 비교 접촉시트, SQLite v181 부모243테이블 행 값/수 보존 후 신규 감사202행을 v182 244번째 테이블에 추가합니다. 기록상 관찰 9829/10042(97.88%)와 미관찰213(실제 고유 211+기존 역사적 집계차이2), 원본 미관찰 old9 그대로입니다.\n'
 '사용자 수동80·제외14·D held2/JUMBO20 및 84 TMX, 원본 Tiles PNG, 과거 모든 SQLite/CSV/ZIP 보존합니다.\n',encoding='utf-8')
print('PASS v182 202 original source diagnostics',json.dumps(summary,ensure_ascii=False),flush=True)
