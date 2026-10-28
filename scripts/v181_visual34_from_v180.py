#!/usr/bin/env python3
"""v181: append source-backed manually observed 34 provisional tile parts after
direct viewing of v180's 56 actual alternate TMX A/B/C scenes.
Avoid re-downloading 84 TMX, reuse original source-verified parent, compare
every original A RGBA pixel, B/C difference and physical SQLite evidence.
"""
from pathlib import Path
import base64,csv,hashlib,io,json,sqlite3,zlib,zipfile
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v181_multisite56_visual'
DBOUT=R/'analysis/current/v181'
DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for a in iter(lambda:f.read(8*1024*1024),b''):h.update(a)
 return h.hexdigest()
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def readparent(man):
 z=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in man['parts']),validate=True)
 assert sha(z)==man['compressed_sha256']
 raw=zlib.decompress(z)
 assert sha(raw)==man['sqlite_sha256'] and len(raw)==man['sqlite_bytes']
 return raw
def zipimg(z,name,mode):
 with Image.open(io.BytesIO(z.read(name))) as im:return im.convert(mode)
parent=json.loads((R/'analysis/current/v180/MANIFEST.json').read_text())
ev=R/'review/v180_remnant239_multisite'
evidence=json.loads((ev/'MANIFEST.json').read_text())
notes=json.loads((OUT/'MANUAL_VISUAL_NOTES.json').read_text())
assert parent['version']=='v180' and parent['table_count']==242 and parent['new_observed_rows']==0
assert evidence['new_TMX_context_candidates_rendered']==56
assert evidence['source_candidates_with_positive_new_B_C']==47
assert evidence['source_candidates_with_new_B_C_zero']==9
assert evidence['new_observed']==0
assert evidence['official_mapping_verified']==evidence['tilezed_verified']==evidence['final_identity_certified']==0
assert notes['version']=='v181' and notes['parent']=='v180'
assert notes['original_multisite_scenes_visually_reviewed']==56
assert notes['positive_pixel_scenes']==47
assert notes['manually_eligible_provisional_after_integrity']==34
assert notes['held_after_manual_review']==22
assert notes['held_zero']==9 and notes['held_small_or_missing']==13
assert len(notes['notes'])==34 and len(notes['held_indices'])==22
assert not (set(map(int,notes['notes']))&set(map(int,notes['held_indices'])))
assert notes['certified']==notes['tilezed_verified']==notes['official_mapping_verified']==0
sources=csvrows(ev/'ALTERNATE_SELECTED_SCENES.csv')
assert len(sources)==56 and len({(r['tile_set_name'],int(r['local_id'])) for r in sources})==56
assert filesha(ev/'ALTERNATE_SELECTED_SCENES.csv')==evidence['selected_csv_sha256']
proof=ev/'ALTERNATE_MULTISITE_IMAGES.zip'
assert filesha(proof)==evidence['archive_sha256']
manual={int(k):v for k,v in notes['notes'].items()}
held=set(map(int,notes['held_indices']))
assert set(manual)|held=={int(r['index']) for r in sources}
for i in held:assert i not in manual
tmp=Path('/tmp/pz_v181_multisite_visual.sqlite');tmp.write_bytes(readparent(parent))
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==242 and before['v180_additional_TMX_scene_evidence']==56
accepted=[];excluded=[]
with zipfile.ZipFile(proof) as z:
 assert z.testzip() is None and len(z.namelist())==56*4
 for r in sources:
  ix=int(r['index']);key=(r['tile_set_name'],int(r['local_id']))
  base=f'{ix:05}/'
  a=zipimg(z,base+'A.png','RGBA')
  b=zipimg(z,base+'B.png','RGB')
  c=zipimg(z,base+'C.png','RGB')
  d=zipimg(z,base+'DIFF.png','RGB')
  assert sha(a.tobytes())==r['original_A_pixel_sha'],('A_pixel',ix)
  assert b.size==c.size==d.size==(800,580)
  rawdiff=ImageChops.difference(b,c)
  assert rawdiff.getbbox()==d.getbbox(),('delta_bbox',ix)
  pixels=sum(p>0 for p in rawdiff.convert('L').getdata())
  assert pixels==int(r['selected_B_C_changed_pixels']),('delta_value',ix,pixels)
  assert r['observed']==r['certified']==r['official_mapping_verified']==r['tilezed_verified']=='0'
  prior=db.execute('SELECT original_png,original_A_pixel_sha,alternate_tmx,alternate_layer,alternate_level,alternate_x,alternate_y,alternate_raw_gid,alternate_TMX_sha256,selected_B_C_changed_pixels,neighbor_source_missing,renderer_outside_canvas,observed FROM v180_additional_TMX_scene_evidence WHERE tile_set_name=? AND local_id=?',key).fetchone()
  expected=(r['original_png'],r['original_A_pixel_sha'],r['alternate_tmx'],int(r['alternate_layer']),int(r['alternate_level']),int(r['alternate_x']),int(r['alternate_y']),int(r['alternate_raw_gid']),r['alternate_TMX_sha256'],pixels,int(r['neighbor_source_missing']),int(r['renderer_outside_canvas']),0)
  assert prior==expected,('v180_physical_scene_evidence_changed',ix)
  assert db.execute('SELECT COUNT(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',key).fetchone()[0]==1
  if ix in held:
   reason='new_B_C_zero' if pixels==0 else 'neighbor_source_missing' if int(r['neighbor_source_missing']) else 'too_small_or_ambiguous_visual_delta'
   excluded.append(dict(index=ix,tile_set_name=key[0],local_id=key[1],reason=reason,changed_pixels=pixels))
   continue
  n=manual[ix]
  assert not n['manual_hold'] and pixels>=200
  assert int(r['neighbor_source_missing'])==int(r['renderer_outside_canvas'])==0
  assert n['confidence'] in ('low','medium','high') and len(n['features'])>=15
  assert n['orientation']==n['connections']=='unverified'
  assert n['official_mapping_verified']==n['identity_certified']==0
  accepted.append(dict(index=ix,tile_set_name=key[0],local_id=key[1],TMX=r['alternate_tmx'],
   layer=int(r['alternate_layer']),level=int(r['alternate_level']),x=int(r['alternate_x']),
   y=int(r['alternate_y']),raw_gid=int(r['alternate_raw_gid']),original_A_pixel_sha=r['original_A_pixel_sha'],
   B_C_changed_pixels=pixels,candidate=n['candidate'],features=n['features'],part=n['part'],
   material=n['material'],confidence=n['confidence'],orientation='unverified',connections='unverified',
   source_basis='v180 parent source and real TMX SHA256/GID/level/layer/site; v181 direct visual inspection of 10 A/B/C/DIFF sheets and 224 proof ZIP A pixels and B-C differences',
   original_proof_zip='review/v180_remnant239_multisite/ALTERNATE_MULTISITE_IMAGES.zip',
   review_status='provisional_candidate',mapping_verified=0,tilezed_verified=0,certified=0))
assert len(accepted)==34 and len(excluded)==22,(len(accepted),len(excluded))
assert sum(r['reason']=='new_B_C_zero' for r in excluded)==9
assert sum(r['reason']!='new_B_C_zero' for r in excluded)==13
assert len({(r['tile_set_name'],r['local_id']) for r in accepted})==34
cols=list(accepted[0])
integers={'index','local_id','layer','level','x','y','raw_gid','B_C_changed_pixels','mapping_verified','tilezed_verified','certified'}
db.execute('CREATE TABLE v181_visual_review ('+','.join('"'+k+'" '+('INTEGER' if k in integers else 'TEXT') for k in cols)+',PRIMARY KEY(tile_set_name,local_id),CHECK(mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
db.executemany('INSERT INTO v181_visual_review ('+','.join('"'+k+'"' for k in cols)+') VALUES ('+','.join('?' for _ in cols)+')',[tuple(r[k] for k in cols) for r in accepted])
db.commit()
after={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==243 and set(after)-set(before)=={'v181_visual_review'}
assert all(after[n]==v for n,v in before.items()) and after['v181_visual_review']==34
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
raw=tmp.read_bytes();z=zlib.compress(raw,8)
encoded=base64.b64encode(z).decode('ascii');parts=[]
for k in range(0,len(encoded),3000000):
 p=DBOUT/f'v181.part{k//3000000:03}.b64';p.write_text(encoded[k:k+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(raw)
dbm=dict(version='v181',parent='v180',parent_sqlite_sha256=parent['sqlite_sha256'],sqlite_sha256=sha(raw),
 compressed_sha256=sha(z),sqlite_bytes=len(raw),parts=parts,table_count=243,prior_tables_preserved=242,
 new_rows=34,new_observed_rows=34,integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
with (OUT/'VISUAL_REVIEW_34.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(accepted)
with (OUT/'EXCLUDED_22.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(excluded[0]));w.writeheader();w.writerows(excluded)
observed=9792+34
assert observed==9826 and 10042-observed==216
manifest=dict(version='v181',visually_reviewed=56,positive_B_C_scenes=47,
 newly_provisional=34,held=22,held_zero=9,held_weak_or_missing=13,
 accepted_indices=sorted(x['index'] for x in accepted),source_original_sheets=10,
 observed_parent=9792,observed_now=observed,remaining_checkpoint=216,
 remaining_physical_unique=248-34,checkpoint_discrepancy=2,
 parent_tables_preserved=242,physical_db_tables=243,sqlite_sha256=sha(raw),
 review_csv_sha256=filesha(OUT/'VISUAL_REVIEW_34.csv'),
 excluded_csv_sha256=filesha(OUT/'EXCLUDED_22.csv'),
 original_evidence_zip_sha256=evidence['archive_sha256'],
 official_mapping_verified=0,tilezed_verified=0,identity_certified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v181 추가 실제 TMX 56종 시각 검수: 신규 잠정34·보류22\n\n'
 'v180 실물 원본 A/B/C/DIFF 10장 접촉시트를 사람이 직접 읽고 부품의 외형·맵 주변 맥락을 확인했다. '
 '동일 원본 타일 제거 픽셀 변화 >=200, 원본 이웃 누락0, 캔버스경계0이며 외형과 기능 부분이 구별되는 34종만 낮음/보통/높음 신뢰도 잠정 기록. '
 '차이0인9종, 작은/모호한 변화 또는 이웃 미비13종은 보류.\n'
 'v180 증거 224개 PNG ZIP CRC, 원본 A 크롭 RGBA SHA, 같은 GID 실제 TMX/층/레이어/좌표의 부모 DB 데이터, B/C 차이픽셀을 다시 검증.\n'
 '물리 SQLite 부모 v180 242개 테이블 전 행·행수 그대로 유지하고 v181 243번째 테이블에 신규34행 추가. '
 '누적 이미지 관찰 9826/10042 (97.85%), 체크포인트 미관찰216, 실제 고유키 미관찰214와 역사적 집계차이2 유지. '
 '공식 타일 ID/TileZed 인증·완성 사물 정체 인증은 0.\n',encoding='utf-8')
print('PASS v181',json.dumps(manifest,ensure_ascii=False),flush=True)
