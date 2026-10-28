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
OUT=R/'review/v180_remnant239_multisite'
DBOUT=R/'analysis/current/v180'
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



ledger=csvrows(R/'review/v175_remaining381_evidence_audit/REMAINING_381_EVIDENCE_AUDIT.csv')
assert len(ledger)==379
accepted17=csvrows(R/'review/v177_alternate_visual23/VISUAL_REVIEW_23.csv')
accepted19=csvrows(R/'review/v179_alternative163_visual/VISUAL_REVIEW_108.csv')
observed={(r['tile_set_name'],int(r['local_id'])) for r in accepted17+accepted19}
assert len(observed)==131 and len(accepted17)==23 and len(accepted19)==108
remaining=[r for r in ledger if r['origin']=='new_A_4633' and (r['tile_set_name'],int(r['local_id'])) not in observed]
assert len(remaining)==239
target={(r['tile_set_name'],int(r['local_id'])):r for r in remaining}
assert len(target)==239
hist={}
for path in ['review/v176_alt_scene_48/ALT_SCENE_RESULTS_48.csv','review/v178_alt_scene_bulk172/ALT_SCENE_RESULTS_163.csv']:
 for r in csvrows(R/path):
  k=(r['tile_set_name'],int(r['local_id']))
  hist.setdefault(k,set()).add((r['alternate_tmx'],int(r['alternate_layer']),int(r['alternate_x']),int(r['alternate_y'])))
assert len(hist)==211
# 84 original TMX files, no hallucinated filenames, positions or tile identities.
aud=json.loads((R/'audits/map_range_26_43_to_37_49/SUMMARY.json').read_text())
assert aud['files_present']==84
best=defaultdict(list)
all_count=Counter()
for num,meta in enumerate(aud['per_map'],1):
 name=meta['tmx'];p=ROOT/name
 assert p.stat().st_size==meta['filesize_bytes'] and filesha(p)==meta['sha256'],('map_integrity',name)
 m=mapread(name)
 gid_map={}
 for k in target:
  for first,tsname in m['ts']:
   if tsname==k[0]:
    g=first+k[1]
    if resolve(m,g)==k:gid_map[g]=k
 if not gid_map:continue
 # Determine coverage by other same-level layers to favor the less occluded scene.
 levels={lvl:[i for i,ly in enumerate(m['layers']) if ly['level']==lvl] for lvl in set(q['level'] for q in m['layers'])}
 for layer in m['layers']:
  v=layer['values']
  for n,raw in enumerate(v):
   key=gid_map.get(raw&0x0fffffff)
   if key is None:continue
   all_count[key]+=1
   x,y=n%m['w'],n//m['w']
   if x<2 or y<2 or x>=m['w']-2 or y>=m['h']-2:continue
   curr=(name,layer['index'],x,y)
   original=target[key]
   primary=(original['original_scene_tmx'],int(original['original_scene_layer']) if original['original_scene_layer'] else -1,int(original['original_scene_x']) if original['original_scene_x'] else -1,int(original['original_scene_y']) if original['original_scene_y'] else -1)
   if curr==primary or curr in hist.get(key,set()):continue
   same=[j for j in levels[layer['level']] if j>layer['index'] and m['layers'][j]['values'][n]]
   upper=len(same)
   coverage=min(x,y,m['w']-1-x,m['h']-1-y)
   rank=(upper,-coverage,abs(x-m['w']//2)+abs(y-m['h']//2),name,layer['index'],y,x)
   loc=dict(tmx=name,layer_index=layer['index'],level=layer['level'],
     x=x,y=y,raw_gid=raw,real_TMX_sha256=meta['sha256'],upper_same_level_layers=upper)
   q=best[key]
   if any(z[1]['tmx']==name and z[1]['layer_index']==layer['index'] and z[1]['x']==x and z[1]['y']==y for z in q):continue
   q.append((rank,loc));q.sort(key=lambda z:z[0])
   if len(q)>3:q.pop()
 if num%12==0:print('TMX',num,'/84, selected keys with additional unseen interior sites',len(best),flush=True)
rows=[]
for k,r in target.items():
 options=best.get(k,[])
 rows.append(dict(index=int(r['index']),tile_set_name=k[0],local_id=k[1],
  prior_hold_reason=r['reason'],actual_original_TMX_uses=all_count[k],
  fresh_untried_inbounds_candidate_count_capped_3=len(options),
  candidate_locations=json.dumps([loc for _,loc in options],ensure_ascii=False),
  status='additional_original_TMX_site_found_needs_visual' if options else 'no_other_new_inbounds_site_in_84_TMX',
  observed=0,certified=0))
assert len(rows)==239 and len({(x['tile_set_name'],x['local_id']) for x in rows})==239
with (OUT/'UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Some original A records were never selected (e.g. held graffiti overlay);
# never replace those with guessed source sprites or count them as rendered.
eligible=[r for r in rows if r['fresh_untried_inbounds_candidate_count_capped_3']>0
 and a[(r['tile_set_name'],r['local_id'])]['selection_status']=='selected_provisional'
 and a[(r['tile_set_name'],r['local_id'])]['source_image_path']]
eligible.sort(key=lambda r:(
  0 if r['prior_hold_reason']=='B_C_zero_original_scene' else 1,
  -int(r['actual_original_TMX_uses']),-int(r['fresh_untried_inbounds_candidate_count_capped_3']),r['index']))
selected=eligible[:64]
print('CENSUS complete',len(eligible),'eligible unique keys; render',len(selected),flush=True)
parent=json.loads((R/'analysis/current/v179/MANIFEST.json').read_text())
compressed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(compressed)==parent['compressed_sha256']
raw=zlib.decompress(compressed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz-v180-multisite.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==241 and before['v179_visual_review']==108
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
rendered=[]
with zipfile.ZipFile(OUT/'ALTERNATE_MULTISITE_IMAGES.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as archive:
 for pos,row in enumerate(selected):
  k=(row['tile_set_name'],row['local_id'])
  orig=a[k]
  assert orig['source_image_path'] and orig['selection_status']=='selected_provisional'
  assert filesha(R/orig['source_image_path'])==orig['source_png_sha256']
  A=sprite(k)
  assert A is not None and sha(A.tobytes())==orig['selected_rgba_pixel_sha256']
  bestscene=None;seen_options=[]
  for loc in json.loads(row['candidate_locations']):
   m=mapread(loc['tmx'])
   z=dict(source_x=loc['x'],source_y=loc['y'],source_level=loc['level'],
      source_layer_index=loc['layer_index'],source_raw_gid=loc['raw_gid'],
      tile_set_name=k[0],local_id=k[1])
   assert resolve(m,int(loc['raw_gid']))==k and filesha(ROOT/loc['tmx'])==loc['real_TMX_sha256']
   B,missing=scene(m,z)
   C,missing2=scene(m,z,delete=True)
   assert missing==missing2
   pixels=difference(B,C)
   r2=(pixels,-int(missing.get('missing_source',0)),-int(missing.get('outside_canvas',0)))
   seen_options.append(dict(**loc,delta_pixels=pixels,missing_source=missing.get('missing_source',0),outside_canvas=missing.get('outside_canvas',0)))
   if bestscene is None or r2>bestscene[0]:bestscene=(r2,loc,B,C,missing)
  _,loc,B,C,missing=bestscene
  D=ImageChops.difference(B,C).convert('RGB')
  changed=difference(B,C)
  # Preserve exact raw RGB difference, not artificial contrast.
  for label,im in [('A',A),('B',B),('C',C),('DIFF',D)]:
   archive.writestr(f'{row["index"]:05d}/{label}.png',png_bytes(im))
  rendered.append(dict(index=row['index'],tile_set_name=k[0],local_id=k[1],
   original_png=orig['source_image_path'],original_A_pixel_sha=sha(A.tobytes()),
   prior_hold_reason=row['prior_hold_reason'],alternate_tmx=loc['tmx'],
   alternate_layer=loc['layer_index'],alternate_level=loc['level'],
   alternate_x=loc['x'],alternate_y=loc['y'],alternate_raw_gid=loc['raw_gid'],
   alternate_TMX_sha256=loc['real_TMX_sha256'],
   actual_original_TMX_uses=row['actual_original_TMX_uses'],
   additional_locations_tried=len(seen_options),all_tried_site_evidence=json.dumps(seen_options,ensure_ascii=False),
   selected_B_C_changed_pixels=changed,neighbor_source_missing=missing.get('missing_source',0),
   renderer_outside_canvas=missing.get('outside_canvas',0),
   observed=0,certified=0,official_mapping_verified=0,tilezed_verified=0))
  if pos%6==0:
   board=Image.new('RGB',(1700,1470),(235,241,246));draw=ImageDraw.Draw(board)
  y=(pos%6)*245
  draw.rectangle((2,y+2,1698,y+243),fill=(255,255,255),outline=(177,195,210))
  draw.text((10,y+8),f'{row["index"]} {k[0]} / {k[1]} | new changed={changed} | {loc["tmx"]} ({loc["x"]},{loc["y"]})',font=font,fill=(25,55,75))
  images=[('Original A',A),('Actual TMX B',B),('One GID removed C',C),('B-C contrast',ImageEnhance.Contrast(D).enhance(2.8))]
  for col,(label,im) in enumerate(images):
   x=col*425
   draw.text((x+6,y+29),label,font=small,fill=(60,80,90))
   thumb=im.copy();thumb.thumbnail((412,186))
   xy=(x+(425-thumb.width)//2,y+50+(186-thumb.height)//2)
   board.paste(thumb,xy,thumb if thumb.mode=='RGBA' else None)
  if pos%6==5 or pos==len(selected)-1:
   board.save(SHEETS/f'ALT_239_{pos//6:02d}.jpg',quality=85,optimize=True)
  if (pos+1)%8==0:print('RENDER',pos+1,'/',len(selected),flush=True)
assert len(rendered)<=64 and len(rendered)>0
with zipfile.ZipFile(OUT/'ALTERNATE_MULTISITE_IMAGES.zip') as zz:
 assert zz.testzip() is None and len(zz.namelist())==4*len(rendered)
with (OUT/'ALTERNATE_SELECTED_SCENES.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rendered[0]));w.writeheader();w.writerows(rendered)
cols=list(rendered[0])
integers={'index','local_id','alternate_layer','alternate_level','alternate_x','alternate_y','alternate_raw_gid','actual_original_TMX_uses','additional_locations_tried','selected_B_C_changed_pixels','neighbor_source_missing','renderer_outside_canvas','observed','certified','official_mapping_verified','tilezed_verified'}
db.execute('CREATE TABLE v180_additional_TMX_scene_evidence ('+','.join('"'+col+'" '+('INTEGER' if col in integers else 'TEXT') for col in cols)+',PRIMARY KEY(tile_set_name,local_id),CHECK(observed=0 AND certified=0 AND official_mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v180_additional_TMX_scene_evidence ('+','.join('"'+k+'"' for k in cols)+') VALUES ('+','.join('?' for _ in cols)+')',[tuple(r[k] for k in cols) for r in rendered])
db.commit()
after={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==242 and set(after)-set(before)=={'v180_additional_TMX_scene_evidence'}
assert all(after[n]==v for n,v in before.items())
assert after['v180_additional_TMX_scene_evidence']==len(rendered)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();pack=zlib.compress(newraw,8);text64=base64.b64encode(pack).decode('ascii');parts=[]
for i in range(0,len(text64),3000000):
 p=DBOUT/f'v180.part{i//3000000:03}.b64';p.write_text(text64[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v180',parent='v179',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(pack),sqlite_bytes=len(newraw),parts=parts,
 table_count=242,prior_tables_preserved=241,new_rows=len(rendered),new_observed_rows=0,integrity_check='ok',
 mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
summary=dict(version='v180',source_map_count=84,actual_distinct_new_A_missing_keys=239,
 historical_missing_old_keys=9,checkpoint_missing=250,physical_missing_total=248,unreconciled_difference=2,
 original_source_keys_with_fresh_untried_inbounds_sites=sum(r['fresh_untried_inbounds_candidate_count_capped_3']>0 for r in rows),
 original_source_keys_without_untried_5x5_sites=sum(r['fresh_untried_inbounds_candidate_count_capped_3']==0 for r in rows),
 source_candidates_with_missing_original_A=sum(r['fresh_untried_inbounds_candidate_count_capped_3']>0 and (a[(r['tile_set_name'],r['local_id'])]['selection_status']!='selected_provisional' or not a[(r['tile_set_name'],r['local_id'])]['source_image_path']) for r in rows),
 new_TMX_context_candidates_rendered=len(rendered),
 source_candidates_with_positive_new_B_C=sum(x['selected_B_C_changed_pixels']>0 for x in rendered),
 source_candidates_with_new_B_C_zero=sum(x['selected_B_C_changed_pixels']==0 for x in rendered),
 best_source_has_all_neighbor_images=sum(x['neighbor_source_missing']==0 for x in rendered),
 preserved_parent_tables=241,new_table_count=242,
 new_observed=0,official_mapping_verified=0,tilezed_verified=0,final_identity_certified=0,
 sqlite_sha256=sha(newraw),
 CSV_239_sha256=filesha(OUT/'UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv'),
 selected_csv_sha256=filesha(OUT/'ALTERNATE_SELECTED_SCENES.csv'),
 archive_sha256=filesha(OUT/'ALTERNATE_MULTISITE_IMAGES.zip'),
 selected_indices=[x['index'] for x in rendered],
 contact_sheets=[x.name for x in sorted(SHEETS.glob('*.jpg'))])
(OUT/'MANIFEST.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v180 실제 미관찰 239개 신규 A 키의 원본 84 TMX 다른 배치 전수검사 및 추가 B/C 재조립\n\n'
 'v179에서 실제 미관찰인 새 키 239개는 원본 v175 ledger 370개에서 v177 23개 및 v179 108개 잠정 승격된 고유키를 빼 정확히 산출함. 기존 원본5409 중 미관찰9개는 원본 A 증거별로 따로 보류하고 역사 집계 차이2는 임의 타일에 배분하지 않음.\n'
 '원본 84개 TMX의 firstgid 및 실제 raw GID·층·레이어·좌표를 전수 훑어, 최초 B위치와 v176/v178에서 재조립한 기존 대체 장소를 제외한 새로운 5x5 좌표만 선별하고 우선 최대 64개 키마다 최대 3개 다른 위치를 실제 B/C로 재조립해 차이 픽셀이 가장 뚜렷한 곳을 원본 A/B/C/DIFF ZIP 및 접촉 시트로 기록.\n'
 'A 원본 PNG SHA256와 RGBA, TMX SHA256/raw GID 일치, 원본 C 단일 제거/ZIP CRC·부모 241 SQLite 테이블 내용/행수 유지 및 PRAGMA integrity_check 확인. 렌더링이나 B-C 변화량 자체로 사물/부품 정체를 인증하거나 관찰 완료 처리하지 않음.\n'
 '이 단계는 추후 이미지 육안 검수용 증거 추가이며 9792/10042(97.51%) 관찰률을 변경하지 않는다. 공식 Local ID/TileZed/최종 사물 정체 인증 0. 원본 84 TMX/PNG, 수동80·제외14, D2/JUMBO20 및 과거 모든 DB/증거 보존.\n',encoding='utf-8')
print('PASS v180',json.dumps(summary,ensure_ascii=False),flush=True)
