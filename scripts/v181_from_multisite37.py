#!/usr/bin/env python3
"""v181 manually checked 56 actual-source TMX A/B/C scenes; append only 37 recognizable
positive-delta provisional parts to v180 physical SQLite. Never certify TileZed IDs.
"""
from pathlib import Path
from functools import lru_cache
import base64,bisect,csv,hashlib,io,json,re,sqlite3,xml.etree.ElementTree as ET,zlib,zipfile
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];OUT=R/'review/v181_multisite_visual37'
DBOUT=R/'analysis/current/v181';DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for a in iter(lambda:f.read(8*1024*1024),b''):h.update(a)
 return h.hexdigest()
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def readraw(m):
 compressed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in m['parts']),validate=True)
 assert sha(compressed)==m['compressed_sha256']
 raw=zlib.decompress(compressed)
 assert sha(raw)==m['sqlite_sha256'] and len(raw)==m['sqlite_bytes']
 return raw
p=json.loads((R/'analysis/current/v180/MANIFEST.json').read_text())
prev=json.loads((R/'review/v180_remnant239_multisite/MANIFEST.json').read_text())
notes=json.loads((OUT/'MANUAL_VISUAL_NOTES.json').read_text())
assert p['version']=='v180' and p['table_count']==242 and p['new_observed_rows']==0
assert prev['new_TMX_context_candidates_rendered']==56
assert prev['source_candidates_with_positive_new_B_C']==47 and prev['source_candidates_with_new_B_C_zero']==9
assert notes['parent_version']=='v180' and notes['manual_sheets_read']==10 and notes['scene_candidates_seen']==56
assert len(notes['notes'])==47 and notes['accepted_provisional_candidates']==37
assert notes['held_positive_tiny_or_missing']==10 and notes['held_B_C_zero']==9
assert notes['mapping_verified']==notes['tilezed_verified']==notes['final_identity_certified']==0
source=R/'review/v180_remnant239_multisite'
assert filesha(source/'ALTERNATE_MULTISITE_IMAGES.zip')==prev['archive_sha256']
assert filesha(source/'ALTERNATE_SELECTED_SCENES.csv')==prev['selected_csv_sha256']
data=readcsv(source/'ALTERNATE_SELECTED_SCENES.csv')
assert len(data)==56 and len({(r['tile_set_name'],r['local_id']) for r in data})==56
manual={int(k):v for k,v in notes['notes'].items()}
assert set(manual)=={int(r['index']) for r in data if int(r['selected_B_C_changed_pixels'])>0}
observed=[];held=[]
@lru_cache(maxsize=12)
def readtmx(name):
 path=R/'B4220.3_MapExport_256/tmx'/name
 root=ET.parse(path).getroot();layers=list(root.iter('layer'))
 first=sorted((int(t.get('firstgid')),t.get('name')) for t in root.findall('tileset') if t.get('name'))
 return root,layers,first,filesha(path)
def srcpng(z,which):
 with Image.open(io.BytesIO(z.read(which))) as im:return im.convert('RGBA' if which.endswith('/A.png') else 'RGB')
with zipfile.ZipFile(source/'ALTERNATE_MULTISITE_IMAGES.zip') as archive:
 assert archive.testzip() is None and len(archive.namelist())==56*4
 for r in data:
  idx=int(r['index']);pref=f'{idx:05d}/'
  A=srcpng(archive,pref+'A.png');B=srcpng(archive,pref+'B.png')
  C=srcpng(archive,pref+'C.png');D=srcpng(archive,pref+'DIFF.png')
  assert sha(A.tobytes())==r['original_A_pixel_sha'],('original_A_sha',idx)
  assert B.size==C.size==D.size==(800,580)
  diff=ImageChops.difference(B,C).convert('RGB')
  assert diff.tobytes()==D.tobytes(),('raw_rgb_difference_mismatch',idx)
  changed=sum(x!=0 for x in diff.convert('L').getdata())
  assert changed==int(r['selected_B_C_changed_pixels']),('changed_pixel_count',idx,changed,r['selected_B_C_changed_pixels'])
  if idx not in manual:
   assert changed==0
   held.append(dict(index=idx,tile_set_name=r['tile_set_name'],local_id=int(r['local_id']),reason='B_C_zero_no_visual_appearance',changed_pixels=changed))
   continue
  note=manual[idx]
  assert note['mapping_verified']==note['tilezed_verified']==note['certified']==0
  if note['manual_hold']:
   assert changed<100 or int(r['neighbor_source_missing'])>0,('weak_or_missing_hold_rule',idx)
   reason='source_neighbor_missing' if int(r['neighbor_source_missing'])>0 else 'visual_weak_under100_pixels'
   held.append(dict(index=idx,tile_set_name=r['tile_set_name'],local_id=int(r['local_id']),reason=reason,changed_pixels=changed))
   continue
  assert changed>=100 and int(r['neighbor_source_missing'])==0 and int(r['renderer_outside_canvas'])==0
  assert note['confidence'] in ('low','medium','high')
  assert note['orientation']==note['connections']=='unverified'
  root,layers,first,real_sha=readtmx(r['alternate_tmx'])
  assert real_sha==r['alternate_TMX_sha256'],('original_tmx_sha',idx)
  layer=int(r['alternate_layer']);x=int(r['alternate_x']);y=int(r['alternate_y'])
  assert 0<=layer<len(layers) and 2<=x<int(root.get('width'))-2 and 2<=y<int(root.get('height'))-2
  ly=layers[layer];assert ly.find('data').get('encoding')=='csv'
  vals=[int(v) for v in re.findall(r'\d+',ly.find('data').text or '')]
  gid=vals[y*int(root.get('width'))+x]
  assert gid==int(r['alternate_raw_gid']),('actual_raw_gid',idx)
  firstgid=[g for g,_ in first];pos=bisect.bisect_right(firstgid,gid&0x0fffffff)-1
  assert pos>=0 and (first[pos][1],(gid&0x0fffffff)-first[pos][0])==(r['tile_set_name'],int(r['local_id']))
  observed.append(dict(index=idx,tile_set_name=r['tile_set_name'],local_id=int(r['local_id']),
   original_png=r['original_png'],source_A_pixel_sha=r['original_A_pixel_sha'],
   original_tmx=r['alternate_tmx'],raw_gid=gid,level=int(r['alternate_level']),
   layer=layer,x=x,y=y,source_TMX_SHA256=r['alternate_TMX_sha256'],
   B_C_changed_pixels=changed,candidate=note['candidate'],features=note['features'],
   part=note['part'],material=note['material'],confidence=note['confidence'],
   orientation='unverified',connections='unverified',source_basis=note['source_basis'],
   evidence_zip='review/v180_remnant239_multisite/ALTERNATE_MULTISITE_IMAGES.zip',
   review_status='provisional_candidate',mapping_verified=0,tilezed_verified=0,certified=0))
assert len(observed)==37 and len(held)==19
assert sum(q['reason']=='B_C_zero_no_visual_appearance' for q in held)==9
assert sum(q['reason']=='visual_weak_under100_pixels' for q in held)==9
assert sum(q['reason']=='source_neighbor_missing' for q in held)==1
dbpath=Path('/tmp/pz-v181-visual37.sqlite');dbpath.write_bytes(readraw(p))
db=sqlite3.connect(dbpath)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==242 and before['v180_additional_TMX_scene_evidence']==56
for q in observed:
 assert db.execute('SELECT COUNT(*) FROM v180_additional_TMX_scene_evidence WHERE tile_set_name=? AND local_id=?',(q['tile_set_name'],q['local_id'])).fetchone()[0]==1
 assert db.execute('SELECT observed,certified FROM v180_additional_TMX_scene_evidence WHERE tile_set_name=? AND local_id=?',(q['tile_set_name'],q['local_id'])).fetchone()==(0,0)
columns=list(observed[0]);ints={'index','local_id','raw_gid','level','layer','x','y','B_C_changed_pixels','mapping_verified','tilezed_verified','certified'}
db.execute('CREATE TABLE v181_visual_review ('+','.join('"'+k+'" '+('INTEGER' if k in ints else 'TEXT') for k in columns)+',PRIMARY KEY(tile_set_name,local_id),CHECK(mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
db.executemany('INSERT INTO v181_visual_review ('+','.join('"'+k+'"' for k in columns)+') VALUES ('+','.join('?' for _ in columns)+')',[tuple(q[k] for k in columns) for q in observed])
db.commit()
after={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==243 and set(after)-set(before)=={'v181_visual_review'}
assert all(after[t]==count for t,count in before.items()) and after['v181_visual_review']==37
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
dbraw=dbpath.read_bytes();compressed=zlib.compress(dbraw,8);txt=base64.b64encode(compressed).decode('ascii');parts=[]
for i in range(0,len(txt),3000000):
 part=DBOUT/f'v181.part{i//3000000:03}.b64';part.write_text(txt[i:i+3000000],encoding='ascii');parts.append(part.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(dbraw)
dbm=dict(version='v181',parent='v180',parent_sqlite_sha256=p['sqlite_sha256'],
 sqlite_sha256=sha(dbraw),compressed_sha256=sha(compressed),sqlite_bytes=len(dbraw),parts=parts,
 table_count=243,prior_tables_preserved=242,new_rows=37,new_observed_rows=37,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
with (OUT/'VISUAL_REVIEW_37.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(observed)
with (OUT/'EXCLUDED_19.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(held[0]));w.writeheader();w.writerows(held)
newobs=9792+37;assert newobs==9829 and 10042-newobs==213
m=dict(version='v181',original_alt_scenes_manually_reviewed=56,
 B_C_positive=47,B_C_zero=9,provisional_accepted=37,excluded=19,
 weak_delta_held=9,neighbor_missing_held=1,zero_delta_held=9,
 accepted_indices=[q['index'] for q in observed],
 source_original_png_B_C_evidence='review/v180_remnant239_multisite/ALTERNATE_MULTISITE_IMAGES.zip',
 source_evidence_zip_sha256=prev['archive_sha256'],
 reviewed_contact_sheets=10,observed_parent=9792,observed_now=newobs,
 checkpoint_missing_after=213,physical_missing_after=248-37,historical_discrepancy=2,
 parent_tables_preserved=242,new_db_tables=243,sqlite_sha256=sha(dbraw),
 visual_csv_sha256=filesha(OUT/'VISUAL_REVIEW_37.csv'),exceptions_sha256=filesha(OUT/'EXCLUDED_19.csv'),
 official_mapping_verified=0,tilezed_verified=0,final_certified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v181 실제 추가 TMX 위치의 A/B/C 56종 직접 시각검수 37종 신규 잠정 정체\n\n'
 'v180에서 원본 TMX의 새 배치로 다시 조립한 총 56종/접촉시트10장을 직접 시각 판독. B−C 변화 양수47 중, A 단독 외형 및 B 문맥이 일치하고 변화100픽셀 이상이며 이웃 PNG 누락이 없는 37종만 신규 provisional_candidate 등록. 변화 0인9/100픽셀 미만9/주변 PNG 한 건 누락1 등 19종은 계속 보류.\n'
 '원본 A RGBA SHA256, ZIP CRC, 차이 RGB 이미지 224장 재검증, B 원본 TMX SHA/GID/firstgid/localid/층/레이어/x/y 정합 검사. 물리 SQLite v180 부모242테이블의 이전 행/내용을 보존하고 신규 v181 37행 1테이블(총243).\n'
 '이번 기록에는 가전세탁기·냉장설비형 궤체·의료 진찰대·식당 테이블·식물·회색 노면·러그·안전난간·벽 패널·코너 등 외형과 부분 역할만 잠정 저장. 공식 타일 ID/TileZed 매핑·완성 물체 정체·정확한 재질·벽 결합 방향은 미인증.\n'
 '이미지 관찰 9829/10042 (97.88%), 기록상 미관찰 213. 물리 고유 키 미관찰211과 과거 집계차이2 별도 유지.\n',encoding='utf-8')
print('PASS v181',json.dumps(m,ensure_ascii=False),flush=True)
