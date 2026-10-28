#!/usr/bin/env python3
"""v189 explicitly requested, narrow re-verification of seven held-but-classified originals.
No false observed promotions or implicit reactivation of v188 exclusion.
Only chair indices 986,987 possess additional *untried* actual TMX scenes.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import bisect,csv,hashlib,base64,zlib,json,sqlite3,re,io,zipfile
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageEnhance
R=Path(__file__).resolve().parents[1]
ROOT=R/'B4220.3_MapExport_256/tmx'
OUT=R/'review/v189_seven_prior_classified_source_recheck'
DBOUT=R/'analysis/current/v189'
SHEETS=OUT/'sheets'
for p in (OUT,DBOUT,SHEETS):p.mkdir(parents=True,exist_ok=True)
def sha(data):return hashlib.sha256(data).hexdigest()
def filesha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bbox(t):
 if not t:return None
 b=tuple(map(int,t.strip('[]').split(',')))
 assert len(b)==4 and b[0]<b[2] and b[1]<b[3]
 return b
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


EXPECTED={
70:('appliances_cooking_01',39),
974:('furniture_seating_indoor_01',6),
975:('furniture_seating_indoor_01',7),
977:('furniture_seating_indoor_01',32),
986:('furniture_seating_indoor_03',22),
987:('furniture_seating_indoor_03',23),
1119:('industry_02',270)
}
claim={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v188_active_review_exclusions/EXCLUDED_FROM_ACTIVE_REVIEW_142.csv')}
history={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v186_object_disambiguation_49/RECLASSIFIED_49.csv')}
original={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v175_remaining381_evidence_audit/REMAINING_381_EVIDENCE_AUDIT.csv')}
multi={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v180_remnant239_multisite/UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv')}
occlusion={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')}
parent=json.loads((R/'analysis/current/v188/MANIFEST.json').read_text())
assert parent['version']=='v188' and parent['table_count']==250
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz-v189-7-source-audit.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
prior={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(prior)==250 and prior['v188_active_review_disposition']==142
out=[]
selected=[]
for idx,k in EXPECTED.items():
 assert k in claim and k in history and k in original and k in multi and k in occlusion and k in a
 old=claim[k];history_note=history[k];org=original[k];locations=multi[k];masked=occlusion[k]
 assert old['source_blocker_category']=='previously_visually_classified_but_not_observation_promoted'
 assert old['disposition']=='excluded_from_active_review_per_latest_user_instruction'
 assert int(old['previous_source_key_observed'])==int(old['new_observed'])==int(old['final_identity_certified'])==0
 assert int(org['index'])==idx and int(org['B_C_changed_pixels'])==0
 assert int(history_note['historical_B_C_pixels'])==int(masked['actual_B_C_pixels'])==0
 assert org['source_png']==history_note['source_png']==a[k]['source_image_path']
 assert a[k]['source_png_sha256']==history_note['source_png_sha256']
 assert filesha(R/a[k]['source_image_path'])==a[k]['source_png_sha256']
 A=sprite(k);assert A is not None
 assert sha(A.tobytes())==a[k]['selected_rgba_pixel_sha256']==history_note['source_RGBA_crop_SHA256']
 count=int(locations['fresh_untried_inbounds_candidate_count_capped_3'])
 others=json.loads(locations['candidate_locations'])
 assert count==len(others) and count==(1 if idx in (986,987) else 0)
 assert int(locations['actual_original_TMX_uses'])==(3 if idx in (986,987) else 1)
 record=dict(index=idx,tile_set_name=k[0],local_id=k[1],
  earlier_visual_classification=history_note['revised_identity'],
  historical_confidence=history_note['confidence'],original_A_RGBA_sha256=sha(A.tobytes()),
  original_TMX=org['original_scene_tmx'],original_B_C_pixels=0,
  original_layer_diagnostic_pixels=int(masked['layer_limited_B_C_pixels']),
  original_TMX_occurrences=int(locations['actual_original_TMX_uses']),
  new_untried_actual_positions=count,
  new_actual_TMX='',new_x='',new_y='',new_layer='',new_level='',new_gid='',new_B_C_pixels='',
  new_scene_missing_neighbors='',new_source_status='original_A_verified_existing_BC_zero',
  historical_v188_review_exclusion_preserved=1,
  newly_observed=0,final_identity_certified=0,tilezed_verified=0,mapping_verified=0)
 if count:
  loc=others[0]
  assert loc['tmx']=='32_46.tmx' and int(loc['x'])==(235 if idx==986 else 236)
  assert int(loc['raw_gid'])==(7727 if idx==986 else 7728)
  assert filesha(ROOT/loc['tmx'])==loc['real_TMX_sha256']
  m=mapread(loc['tmx'])
  assert resolve(m,int(loc['raw_gid']))==k
  z=dict(source_x=loc['x'],source_y=loc['y'],source_level=loc['level'],source_layer_index=loc['layer_index'],
    source_raw_gid=loc['raw_gid'],tile_set_name=k[0],local_id=k[1])
  B,missB=scene(m,z);C,missC=scene(m,z,delete=True)
  assert missB==missC
  delta=difference(B,C)
  D=ImageChops.difference(B,C).convert('RGB')
  selected.append((idx,k,loc,A,B,C,D,delta,missB))
  record.update(new_actual_TMX=loc['tmx'],new_x=loc['x'],new_y=loc['y'],
    new_layer=loc['layer_index'],new_level=loc['level'],new_gid=loc['raw_gid'],
    new_B_C_pixels=delta,new_scene_missing_neighbors=missB.get('missing_source',0),
    new_source_status='new_actual_TMX_position_pixel_evidence_needs_manual_identity_review')
 out.append(record)
assert len(out)==7 and len(selected)==2
# Also preserve the five negative cases; no fabricated untried TMX scene.
proof=OUT/'REAL_ALTERNATE_BC_TWO.zip'
with zipfile.ZipFile(proof,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for idx,k,loc,A,B,C,D,delta,miss in selected:
  for name,img in [('A_source',A),('B_actual',B),('C_target_removed',C),('B_minus_C',D)]:
   z.writestr(f'{idx:04d}/{name}.png',png_bytes(img))
with zipfile.ZipFile(proof) as z:
 assert z.testzip() is None and len(z.namelist())==8
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
font2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
board=Image.new('RGB',(1660,800),(236,243,248));draw=ImageDraw.Draw(board)
for i,(idx,k,loc,A,B,C,D,delta,miss) in enumerate(selected):
 y=i*395
 draw.rectangle((5,y+3,1653,y+390),fill='white',outline=(169,186,200))
 draw.text((16,y+12),f'IDX {idx}, {k[0]}/{k[1]}  NEW actual {loc["tmx"]} x={loc["x"]} y={loc["y"]} rawGID={loc["raw_gid"]}  B-C delta={delta}  missing={miss.get("missing_source",0)}',font=font,fill=(30,48,67))
 for t,(name,img) in enumerate([('A ORIGINAL',A),('B same original TMX',B),('C one GID deleted',C),('B-C RAW DIFFERENCE',D)]):
  x=t*412
  draw.text((x+18,y+52),name,font=font2,fill=(58,70,90))
  c=img.copy();c.thumbnail((395,300))
  p=(x+(410-c.width)//2,y+75+(300-c.height)//2)
  if c.mode=='RGBA':board.paste(c,p,c)
  else:board.paste(c,p)
board.save(SHEETS/'TWO_REAL_ALT_CHAIR_PARTS.jpg',quality=90,optimize=True)
with (OUT/'SEVEN_RECHECK.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
cols=list(out[0]);types={c:('INTEGER' if c in ['index','local_id','original_B_C_pixels','original_layer_diagnostic_pixels','original_TMX_occurrences','new_untried_actual_positions','historical_v188_review_exclusion_preserved','newly_observed','final_identity_certified','tilezed_verified','mapping_verified'] else 'TEXT') for c in cols}
db.execute('CREATE TABLE v189_held_source_reverification ('+','.join('"'+c+'" '+types[c] for c in cols)+', PRIMARY KEY(tile_set_name,local_id), CHECK(historical_v188_review_exclusion_preserved=1 AND newly_observed=0 AND final_identity_certified=0 AND tilezed_verified=0 AND mapping_verified=0))')
db.executemany('INSERT INTO v189_held_source_reverification ('+','.join('"'+c+'"' for c in cols)+') VALUES ('+','.join('?' for c in cols)+')',[tuple(r[c] for c in cols) for r in out])
db.commit()
after={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==251 and set(after)-set(prior)=={'v189_held_source_reverification'}
assert all(after[n]==v for n,v in prior.items()) and after['v189_held_source_reverification']==7
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();comp=zlib.compress(newraw,8)
enc=base64.b64encode(comp).decode('ascii');parts=[]
for i in range(0,len(enc),3000000):
 p=DBOUT/f'v189.part{i//3000000:03}.b64';p.write_text(enc[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/x).read_text('ascii') for x in parts))))==sha(newraw)
dbm=dict(version='v189',parent='v188',parent_sqlite_sha256=parent['sqlite_sha256'],sqlite_sha256=sha(newraw),
 compressed_sha256=sha(comp),sqlite_bytes=len(newraw),parts=parts,table_count=251,prior_tables_preserved=250,
 new_rows=7,new_observed_rows=0,integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,indent=2)+'\n')
report=dict(version='v189',user_explicit_new_recheck_request=True,
 previous_active_review_exclusions_preserved=True,
 seven_prior_A_exterior_part_classifications_reexamined=7,
 alternate_real_TMX_scene_candidates=2,
 no_new_actual_location_available=5,
 alternate_changed_pixels_by_index={str(x['index']):x['new_B_C_pixels'] for x in out if x['new_untried_actual_positions']==1},
 original_A_RGBA_and_original_PNG_SHA_verified=7,
 no_unverified_ID_promotions=7,newly_observed=0,
 checkpoint_observed=9898,checkpoint_unobserved=144,
 physical_held_unique=142,unreconciled_historical_count_gap=2,
 official_mapping_verified=0,tilezed_verified=0,certified=0,
 parent_tables_preserved=250,sqlite_tables=251,sqlite_sha256=sha(newraw),
 comparison_zip_sha=filesha(proof),
 comparison_csv_sha=filesha(OUT/'SEVEN_RECHECK.csv'))
(OUT/'MANIFEST.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v189 미검증 타일 재검수: A에서 형태 설명은 있으나 실제 B-C=0이었던 7종\n\n'
 '이전 사용자 지시로 v188 활성검수에서 제외했던 142종을 대량 자동 복구하지 않는다. 이번 명시 재검수 요청에 따라 이미 외형 후보 기록이 있는 7종만 엄밀히 원본 A PNG 해시/크롭 RGBA 해시, 기존 실제 TMX 위치와 B−C=0, 84개 전수조사의 새로운 실제 장면 후보를 재대조했다.\n'
 '7종 중 안락의자 쿠션 부분 986/987만 새로운 실제 TMX 배치(32_46.tmx)에서 각 한 번 추가 비교할 수 있어 B/C/DIFF를 재조립했다. 나머지 70/974/975/977/1119의 실제 TMX 단일 사용 기록은 다시 확인했지만 다른 위치가 없으므로 관찰률을 올리지 않는다.\n'
 '변화량이나 분리된 원본 A 외형만으로 TileZed 공식 Local ID 매핑/정확한 물체·재질·조립 인증을 만들 수 없다. 새 인간 시각 판독과 추가 증거 전까지 신규 관찰0, 최종 인증0, v188 제외기록 보존.\n'
 '새 SQLite v189 251개 테이블 = 기존250개 전체 행/값 보존 + 추가 소스 재검수 7행. 원본 TMX, Tiles PNG, 과거 DB, 사용자 수동80/제외14/D held2/JUMBO20 불변.\n',encoding='utf-8')
print('PASS v189 7 verified A sources, 2 other true TMX scenes, no false promotions',json.dumps(report,ensure_ascii=False),flush=True)
