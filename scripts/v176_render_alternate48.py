#!/usr/bin/env python3
"""v176 renderer: actual alternate TMX GID occurrence A/B/C comparison of
up to 48 formerly zero/edge B-C unresolved keys. Evidence only; no identity
claim, atlas Local ID certification, or visual-observed inflation.
Isometric TileZed presentation remains a provisional reconstructed renderer.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import bisect,csv,hashlib,base64,zlib,json,sqlite3,re,io,zipfile
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageEnhance
R=Path(__file__).resolve().parents[1]
ROOT=R/'B4220.3_MapExport_256/tmx'
OUT=R/'review/v176_alt_scene_48'
DBOUT=R/'analysis/current/v176'
SHEETS=OUT/'sheets'
for path in [OUT,DBOUT,SHEETS]:path.mkdir(parents=True,exist_ok=True)
def sha(x):return hashlib.sha256(x).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bbox(text):
 if not text:return None
 q=tuple(map(int,text.strip('[]').split(',')))
 assert len(q)==4 and 0<=q[0]<q[2] and 0<=q[1]<q[3]
 return q
a={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')}
cand={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv')}
assert len(a)==4633 and len(cand)==10042
W,H=800,580

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


audit=csvrows(R/'review/v175_remaining381_evidence_audit/REMAINING_381_EVIDENCE_AUDIT.csv')
assert len(audit)==379
pool=[r for r in audit if r['origin']=='new_A_4633' and r['eligible_for_visual_followup']=='1' and r['alternate_scene_candidate']]
pool.sort(key=lambda r:(
 0 if r['reason']=='B_C_zero_original_scene' else 1 if r['reason']=='original_scene_at_TMX_edge' else 2,
 -int(r['interior_occurrences_84']),-int(r['actual_occurrences_84']),int(r['index'])))
selected=pool[:48]
assert len(selected)==48 and len(set((x['tile_set_name'],x['local_id']) for x in selected))==48
parent=json.loads((R/'analysis/current/v175/MANIFEST.json').read_text())
pack=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(pack)==parent['compressed_sha256']
raw=zlib.decompress(pack)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz-v176-alternate-scenes.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==237 and before['v175_remaining_evidence_audit']==379
assert all(db.execute('SELECT COUNT(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',(r['tile_set_name'],int(r['local_id']))).fetchone()[0]==1 for r in selected)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
font2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
proofs=zipfile.ZipFile(OUT/'ALT_BC_48_ORIGINAL_TMXS.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5)
results=[]
maps={}
for i,row in enumerate(selected):
 k=(row['tile_set_name'],int(row['local_id']))
 original=a[k]
 assert original['selection_status']=='selected_provisional'
 loc=json.loads(row['alternate_scene_candidate'])
 assert loc['inbounds_5x5'] and (loc['tmx'],loc['x'],loc['y'])!=(row['original_scene_tmx'],int(row['original_scene_x']),int(row['original_scene_y']))
 if loc['tmx'] not in maps:
  maps[loc['tmx']]=mapread(loc['tmx'])
 m=maps[loc['tmx']]
 z=dict(source_x=loc['x'],source_y=loc['y'],source_level=loc['level'],
  source_layer_index=loc['layer_index'],source_raw_gid=loc['raw_gid'],
  tile_set_name=k[0],local_id=k[1])
 assert resolve(m,int(loc['raw_gid']))==k
 assert filesha(R/original['source_image_path'])==original['source_png_sha256']
 A=sprite(k)
 assert A is not None and sha(A.tobytes())==original['selected_rgba_pixel_sha256']
 B,missB=scene(m,z)
 C,missC=scene(m,z,delete=True)
 assert B.size==C.size==(800,580) and missB==missC
 changed=difference(B,C)
 D=ImageChops.difference(B,C).convert('RGB')
 # Enhance the difference only for human-readable proof; raw RGB values preserved in ZIP.
 enhanced=ImageEnhance.Contrast(D).enhance(2.8)
 im=[('A_original',A),('B_alt_actual_TMX',B),('C_one_GID_removed',C),('B_minus_C_raw',D)]
 for lab,img in im:proofs.writestr(f'{int(row["index"]):05}/{lab}.png',png_bytes(img))
 results.append(dict(index=int(row['index']),tile_set_name=k[0],local_id=k[1],source_png=original['source_image_path'],
  original_scene_reason=row['reason'],original_scene_changed_pixels=row['B_C_changed_pixels'],
  alternate_tmx=loc['tmx'],alternate_layer=int(loc['layer_index']),alternate_level=int(loc['level']),
  alternate_x=int(loc['x']),alternate_y=int(loc['y']),alternate_raw_gid=int(loc['raw_gid']),
  alternate_changed_pixels=changed,neighbors_missing=int(missB.get('missing_source',0)),
  outside_canvas=int(missB.get('outside_canvas',0)),
  actual_raw_gid_matches_key=1,exactly_one_target_GID_removed=1,
  original_A_pixel_sha=sha(A.tobytes()),alternate_TMX_sha256=filesha(ROOT/loc['tmx']),
  evidence_status='source_verified_new_scene_needs_manual_visual_identity_assessment',
  observed=0,mapping_verified=0,tilezed_verified=0,certified=0,
  note='New scene uses SAME original A and actual occurrence GID of the SAME key; C removes exactly this GID; no alternate PNG/D or TileZed official mapping asserted.'))
 if i%6==0:
  board=Image.new('RGB',(1750,1530),(232,239,247));draw=ImageDraw.Draw(board)
 rowno=i%6;y=rowno*255
 draw.rectangle((4,y+2,1744,y+253),fill=(255,255,255),outline=(176,192,204))
 draw.text((12,y+8),f'{row["index"]} {k[0]}/{k[1]} | old B-C {row["B_C_changed_pixels"]} | alternate delta {changed} | scene {loc["tmx"]}:{loc["x"]},{loc["y"]}',fill=(26,47,71),font=font)
 for j,(label,img) in enumerate([('SOURCE A',A),('ALT B actual TMX',B),('ALT C target removed',C),('B-C x contrast',enhanced)]):
  x=j*435
  draw.text((x+7,y+30),label,fill=(45,58,77),font=font2)
  q=img.copy();q.thumbnail((420,196))
  pos=(x+(430-q.width)//2,y+53+(196-q.height)//2)
  if q.mode=='RGBA':board.paste(q,pos,q)
  else:board.paste(q,pos)
 if i%6==5:board.save(SHEETS/f'ALT_BC_{i//6:02}.jpg',quality=88,optimize=True)
 print('ALT',i+1,'/48',k,'former pix',row['B_C_changed_pixels'],'new pix',changed,'missing sprites',missB.get('missing_source',0),flush=True)
proofs.close()
assert len(results)==48 and len({(r['tile_set_name'],r['local_id']) for r in results})==48
with zipfile.ZipFile(OUT/'ALT_BC_48_ORIGINAL_TMXS.zip') as proof:
 assert proof.testzip() is None and len(proof.namelist())==48*4
with (OUT/'ALT_SCENE_RESULTS_48.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
fields=[('index','INTEGER'),('tile_set_name','TEXT'),('local_id','INTEGER'),('source_png','TEXT'),
 ('original_scene_reason','TEXT'),('original_scene_changed_pixels','TEXT'),('alternate_tmx','TEXT'),
 ('alternate_layer','INTEGER'),('alternate_level','INTEGER'),('alternate_x','INTEGER'),('alternate_y','INTEGER'),
 ('alternate_raw_gid','INTEGER'),('alternate_changed_pixels','INTEGER'),('neighbors_missing','INTEGER'),
 ('outside_canvas','INTEGER'),('actual_raw_gid_matches_key','INTEGER'),('exactly_one_target_GID_removed','INTEGER'),
 ('original_A_pixel_sha','TEXT'),('alternate_TMX_sha256','TEXT'),('evidence_status','TEXT'),
 ('observed','INTEGER'),('mapping_verified','INTEGER'),('tilezed_verified','INTEGER'),('certified','INTEGER'),('note','TEXT')]
db.execute('CREATE TABLE v176_alternate_scene_evidence ('+','.join('"'+n+'" '+typ for n,typ in fields)+',PRIMARY KEY(tile_set_name,local_id),CHECK(observed=0 AND mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
columns=[n for n,_ in fields]
db.executemany('INSERT INTO v176_alternate_scene_evidence ('+','.join('"'+n+'"' for n in columns)+') VALUES ('+','.join('?' for _ in columns)+')',[tuple(row[n] for n in columns) for row in results])
db.commit()
after={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==238 and set(after)-set(before)=={'v176_alternate_scene_evidence'}
assert all(after[n]==v for n,v in before.items()) and after['v176_alternate_scene_evidence']==48
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();compressed=zlib.compress(newraw,8)
encoded=base64.b64encode(compressed).decode('ascii');parts=[]
for i in range(0,len(encoded),3000000):
 p=DBOUT/f'v176.part{i//3000000:03}.b64';p.write_text(encoded[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v176',parent='v175',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(compressed),sqlite_bytes=len(newraw),parts=parts,
 table_count=238,prior_tables_preserved=237,new_rows=48,new_observed_rows=0,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,indent=2)+'\n')
manifest=dict(version='v176',scope='48 high priority formerly zero or edge keys with alternative original TMX 5x5 occurrence',
 true_alternate_TMX_scenes=48,
 original_B_C_zero_count=sum(r['original_scene_reason']=='B_C_zero_original_scene' for r in results),
 new_B_C_positive_count=sum(int(r['alternate_changed_pixels'])>0 for r in results),
 new_B_C_zero_count=sum(int(r['alternate_changed_pixels'])==0 for r in results),
 no_missing_sprites_count=sum(int(r['neighbors_missing'])==0 for r in results),
 no_outside_canvas_count=sum(int(r['outside_canvas'])==0 for r in results),
 observed_before=9661,observed_after=9661,remaining_in_checkpoint=381,
 source_keys_pending=379,source_key_count_discrepancy=2,
 official_mapping_verified=0,tilezed_verified=0,identity_certified=0,
 parent_db_tables_preserved=237,physical_tables=238,sqlite_sha256=sha(newraw),
 evidence_zip_sha=filesha(OUT/'ALT_BC_48_ORIGINAL_TMXS.zip'),
 evidence_csv_sha=filesha(OUT/'ALT_SCENE_RESULTS_48.csv'),
 contact_sheets=[p.name for p in sorted(SHEETS.glob('*.jpg'))])
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v176 이전 B-C가 0이었던 타일 등의 다른 실제 TMX 위치 A/B/C 재조립 48종\n\n'
 'v175가 84 TMX에서 발견한 같은 (tile_set_name,local_id)의 다른 실제 inbounds 5x5 좌표 중 48개를 선택했습니다. 선택된 소스 PNG A를 절대 다른 것으로 바꾸지 않고, 새 TMX B 장면과 그 장면에서 원래 GID 한 개만 제거한 C, RGB 차이를 직접 렌더했습니다.\n'
 '원본과 같은 타일 키/GID/층/레이어/좌표, 원본 A 픽셀 해시, 타일셋 PNG, 실제 TMX SHA, 정확히 한 GID 제거, 48건 이미지 ZIP CRC/PNG 및 부모 v175 237개 SQLite 테이블 보존 검사.\n'
 '이 것은 공식 TileZed 투영이나 공식 Local ID/이미지 대응 인증이 아니라 기존 방식을 따라 구성한 잠정 원본 타일 장면입니다. B-C 픽셀이 양수라도 실제 사물 정체/재질/방향·연결 등은 사람의 재검수가 필요합니다. 그러므로 신규 observed=0, certified=0입니다.\n',encoding='utf-8')
print('PASS v176 ALTERNATE SCENES',json.dumps(manifest,ensure_ascii=False),flush=True)
