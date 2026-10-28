#!/usr/bin/env python3
"""v177: manually observed 23 actual alternative TMX B/C tile instances.
Require unchanged v176 evidence, PNG pixel identity, exact TMX GID, and independently
observed positive B-C before any new provisional observation. ZERO final IDs.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import base64,bisect,csv,hashlib,io,json,re,sqlite3,zlib,zipfile
from PIL import Image,ImageChops
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v177_alternate_visual23'
DBOUT=R/'analysis/current/v177'
DBOUT.mkdir(parents=True,exist_ok=True)
def sha(x):return hashlib.sha256(x).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def readparent(man):
 enc=''.join((R/p).read_text('ascii').strip() for p in man['parts'])
 z=base64.b64decode(enc,validate=True)
 assert sha(z)==man['compressed_sha256']
 raw=zlib.decompress(z)
 assert sha(raw)==man['sqlite_sha256'] and len(raw)==man['sqlite_bytes']
 return raw
parent=json.loads((R/'analysis/current/v176/MANIFEST.json').read_text())
prior=json.loads((R/'review/v176_alt_scene_48/MANIFEST.json').read_text())
notes=json.loads((OUT/'MANUAL_VISUAL_NOTES.json').read_text())
assert parent['version']=='v176' and parent['table_count']==238 and parent['new_observed_rows']==0
assert prior['true_alternate_TMX_scenes']==48 and prior['new_B_C_positive_count']==27
assert notes['version']=='v177' and len(notes['notes'])==27 and notes['eligible_after_manual_review']==23
assert notes['actually_inspected']==48 and notes['positive_pixel_scenes']==27
assert notes['official_mapping_verified']==notes['tilezed_verified']==notes['identity_certified']==0
v176=R/'review/v176_alt_scene_48'
assert filesha(v176/'ALT_BC_48_ORIGINAL_TMXS.zip')==prior['evidence_zip_sha']
assert filesha(v176/'ALT_SCENE_RESULTS_48.csv')==prior['evidence_csv_sha']
entries=readcsv(v176/'ALT_SCENE_RESULTS_48.csv')
assert len(entries)==48 and len({(r['tile_set_name'],int(r['local_id'])) for r in entries})==48
r_by_index={int(r['index']):r for r in entries}
assert len(r_by_index)==48
manual={int(k):v for k,v in notes['notes'].items()}
assert set(manual)=={int(r['index']) for r in entries if int(r['alternate_changed_pixels'])>0}
accepted=[];excluded=[]
@lru_cache(maxsize=32)
def tmxtree(name):
 p=R/'B4220.3_MapExport_256/tmx'/name
 root=ET.parse(p).getroot()
 layers=list(root.iter('layer'))
 first=sorted((int(t.get('firstgid')),t.get('name')) for t in root.findall('tileset'))
 return root,layers,first,filesha(p)
def png_from_zip(z,path):
 with Image.open(io.BytesIO(z.read(path))) as im:return im.copy()
with zipfile.ZipFile(v176/'ALT_BC_48_ORIGINAL_TMXS.zip') as z:
 assert z.testzip() is None and len(z.namelist())==192
 for r in entries:
  idx=int(r['index'])
  path=f'{idx:05}/'
  A=png_from_zip(z,path+'A_original.png').convert('RGBA')
  B=png_from_zip(z,path+'B_alt_actual_TMX.png').convert('RGB')
  C=png_from_zip(z,path+'C_one_GID_removed.png').convert('RGB')
  D=png_from_zip(z,path+'B_minus_C_raw.png').convert('RGB')
  assert sha(A.tobytes())==r['original_A_pixel_sha'],('A_pixel',idx)
  assert B.size==C.size==D.size==(800,580)
  assert ImageChops.difference(B,C).getbbox()==D.getbbox(),('difference_extent',idx)
  changed=sum(x!=0 for x in ImageChops.difference(B,C).convert('L').getdata())
  assert changed==int(r['alternate_changed_pixels']),('pixel_mismatch',idx,changed,r['alternate_changed_pixels'])
  assert r['actual_raw_gid_matches_key']==r['exactly_one_target_GID_removed']=='1'
  assert r['neighbors_missing']==r['outside_canvas']=='0'
  assert r['mapping_verified']==r['tilezed_verified']==r['certified']==r['observed']=='0'
  if idx not in manual:
   assert changed==0,('positive_delta_not_manually_reviewed',idx)
   excluded.append(dict(index=idx,tile_set_name=r['tile_set_name'],local_id=int(r['local_id']),reason='alternate_B_C_zero_still_unobserved',changed_pixels=0))
   continue
  note=manual[idx];held=bool(note['manual_hold'])
  assert (changed>=100) == (not held),('positive_tiny_rule',idx,changed,held)
  if held:
   excluded.append(dict(index=idx,tile_set_name=r['tile_set_name'],local_id=int(r['local_id']),reason='alternate_B_C_tiny_manual_visual_held',changed_pixels=changed))
   continue
  assert note['confidence'] in ('low','medium','high')
  assert note['identity_certified']==note['tilezed_verified']==0
  assert note['orientation']==note['connections']=='unverified'
  root,layers,first,actual_tmxdigest=tmxtree(r['alternate_tmx'])
  assert actual_tmxdigest==r['alternate_TMX_sha256'],('TMX_SHA',idx)
  ix=int(r['alternate_layer'])
  x=int(r['alternate_x']);y=int(r['alternate_y'])
  assert 0<=ix<len(layers)
  assert 2<=x<int(root.get('width'))-2 and 2<=y<int(root.get('height'))-2
  ly=layers[ix];assert ly.find('data').get('encoding')=='csv'
  raw=[int(v) for v in re.findall(r'\d+',ly.find('data').text or '')]
  gid=raw[y*int(root.get('width'))+x]
  assert gid==int(r['alternate_raw_gid']),('TMX_GID',idx)
  firstgids=[q[0] for q in first]
  k=bisect.bisect_right(firstgids,gid&0x0fffffff)-1
  assert k>=0 and (first[k][1],(gid&0x0fffffff)-first[k][0])==(r['tile_set_name'],int(r['local_id']))
  accepted.append(dict(index=idx,tile_set_name=r['tile_set_name'],local_id=int(r['local_id']),
    original_source_png=r['source_png'],TMX=r['alternate_tmx'],layer=ix,level=int(r['alternate_level']),
    x=x,y=y,raw_gid=gid,original_A_pixel_sha=r['original_A_pixel_sha'],B_C_changed_pixels=changed,
    candidate=note['candidate'],features=note['features'],part=note['part'],material=note['material'],
    confidence=note['confidence'],orientation='unverified',connections='unverified',
    evidence_basis=note['evidence_basis'],
    original_evidence_zip='review/v176_alt_scene_48/ALT_BC_48_ORIGINAL_TMXS.zip',
    review_status='provisional_candidate',mapping_verified=0,tilezed_verified=0,certified=0))
assert len(accepted)==23 and len(excluded)==25
assert len({(x['tile_set_name'],x['local_id']) for x in accepted})==23
assert sum(x['reason']=='alternate_B_C_zero_still_unobserved' for x in excluded)==21
assert sum(x['reason']=='alternate_B_C_tiny_manual_visual_held' for x in excluded)==4
parent_raw=readparent(parent)
tmp=Path('/tmp/pz-v177-alternate-visual.sqlite');tmp.write_bytes(parent_raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT count(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==238 and before['v176_alternate_scene_evidence']==48
for row in accepted:
 assert db.execute('SELECT COUNT(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',(row['tile_set_name'],row['local_id'])).fetchone()[0]==1
 assert db.execute('SELECT observed FROM v176_alternate_scene_evidence WHERE tile_set_name=? AND local_id=?',(row['tile_set_name'],row['local_id'])).fetchone()==(0,)
keys=list(accepted[0])
types={k:('INTEGER' if k in ['index','local_id','layer','level','x','y','raw_gid','B_C_changed_pixels','mapping_verified','tilezed_verified','certified'] else 'TEXT') for k in keys}
db.execute('CREATE TABLE v177_visual_review ('+','.join('"'+k+'" '+types[k] for k in keys)+', PRIMARY KEY(tile_set_name,local_id), CHECK(certified=0 AND mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v177_visual_review ('+','.join('"'+k+'"' for k in keys)+') VALUES ('+','.join('?' for k in keys)+')',[tuple(x[k] for k in keys) for x in accepted])
db.commit()
after={n:db.execute('SELECT count(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==239 and set(after)-set(before)=={'v177_visual_review'}
assert all(after[n]==v for n,v in before.items()) and after['v177_visual_review']==23
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();comp=zlib.compress(newraw,8)
enc=base64.b64encode(comp).decode('ascii');parts=[]
for i in range(0,len(enc),3000000):
 p=DBOUT/f'v177.part{i//3000000:03}.b64';p.write_text(enc[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v177',parent='v176',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(comp),sqlite_bytes=len(newraw),parts=parts,
 table_count=239,prior_tables_preserved=238,new_rows=23,new_observed_rows=23,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,indent=2)+'\n')
with (OUT/'VISUAL_REVIEW_23.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(accepted)
with (OUT/'EXCLUDED_25.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(excluded[0]));w.writeheader();w.writerows(excluded)
obs=9661+23
assert obs==9684 and 10042-obs==358
m=dict(version='v177',visually_seen_alternate_scenes=48,alternative_delta_positive=27,
 provisional_promoted_after_manual_visual_review=23,
 tiny_positive_held=4,zero_pixel_held=21,excluded_total=25,
 visual_review_indices=[r['index'] for r in accepted],
 observed_parent=9661,observed_now=obs,remaining_in_checkpoint=358,
 source_distinct_unobserved_after=379-23,checkpoint_discrepancy=2,
 prior_tables_preserved=238,physical_db_tables=239,sqlite_sha256=sha(newraw),
 visual_review_csv_sha256=filesha(OUT/'VISUAL_REVIEW_23.csv'),
 excluded_csv_sha256=filesha(OUT/'EXCLUDED_25.csv'),
 evidence_zip= 'review/v176_alt_scene_48/ALT_BC_48_ORIGINAL_TMXS.zip',
 evidence_zip_sha256=prior['evidence_zip_sha'],
 official_mapping_verified=0,tilezed_verified=0,identity_certified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v177 48종 다른 실제 TMX 위치 A/B/C 수동 재검수, 신규 잠정 23종\n\n'
 '실제 v176 원본 A/B/C/DIFF 8장 접촉시트를 사람 눈으로 직접 확인. 변화0인 21종과 1~10픽셀처럼 육안 판별 어려운 변화4종을 보류. 건초더미·작은 식재·금속 산업작업대·경사진 상점 차양·목제 식당 의자·박공지붕 삼각사이딩·실내/상업 벽체·바닥 포장 등 변화100픽셀이상이며 형태와 실제 배치가 상호 일치하는 **23종**만 신규 낮음/보통/높음 신뢰도 잠정 사물 부분으로 등록.\n'
 '승격 전 v176 증거 ZIP CRC/PNG A RGBA SHA256 및 B-C 픽셀차, 실제 TMX SHA/원래 raw GID·좌표·레이어·firstgid-tileset/local_id, v175 원본 미관찰 키와 SQLite 물리 부모 238개 테이블을 다시 검증함.\n'
 '이미지 관찰 9,684/10,042(96.43%)로 23 증가, 상태 미관찰 358, 부모 v176 238테이블+새 v177 23행 1테이블=239테이블, 모든 과거 행 값·수 보존. 실물 정체/정확한 재질/방향·공식 PNG ↔ TileZed Local ID 인증 모두 0.\n'
 '역사적 체크포인트 관찰 집계와 물리 서로 다른 2건의 불일치 유지: 원본의 실제 미관찰 고유키는 379−23=356. 상태 표시 미관찰 358과 혼동하지 않는다.\n',encoding='utf-8')
print('PASS v177',json.dumps(m,ensure_ascii=False),flush=True)
