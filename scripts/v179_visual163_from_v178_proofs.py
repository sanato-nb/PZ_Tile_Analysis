#!/usr/bin/env python3
"""v179 manually seen source-backed tile parts, using v178 proof instead of re-downloading 84 TMX.
v178 cryptographically verified exact raw TMX GID/local_id/PNG crop at the true
alternate placement. This run REUSES that physical DB chain and independent 652-image
A/B/C ZIP and rechecks A RGBA and B-C pixel evidence for each of 163 visual reviews.
Never claims official TileZed mapping or final object certification.
"""
from pathlib import Path
from collections import Counter
import base64,csv,hashlib,io,json,sqlite3,zlib,zipfile
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v179_alternative163_visual'
DBOUT=R/'analysis/current/v179';DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def csvrows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def readparent(man):
 enc=''.join((R/p).read_text('ascii').strip() for p in man['parts'])
 zipped=base64.b64decode(enc,validate=True)
 assert sha(zipped)==man['compressed_sha256']
 raw=zlib.decompress(zipped)
 assert sha(raw)==man['sqlite_sha256'] and len(raw)==man['sqlite_bytes']
 return raw
def imagefromzip(z,path,mode):
 with Image.open(io.BytesIO(z.read(path))) as a:return a.convert(mode)
parent=json.loads((R/'analysis/current/v178/MANIFEST.json').read_text())
evidence=json.loads((R/'review/v178_alt_scene_bulk172/MANIFEST.json').read_text())
notes=json.loads((OUT/'MANUAL_VISUAL_NOTES.json').read_text())
assert parent['version']=='v178' and parent['table_count']==240 and parent['prior_tables_preserved']==239
assert evidence['true_alternate_TMX_scenes']==163 and evidence['new_B_C_positive_count']==126
assert evidence['identity_certified']==evidence['official_mapping_verified']==evidence['tilezed_verified']==0
assert notes['version']=='v179' and notes['parent']=='v178'
assert notes['original_alternative_scenes_visually_reviewed']==163
assert notes['positive_difference_scenes']==126
assert len(notes['notes'])==163
assert notes['manually_eligible_provisional_after_integrity']==108
assert notes['held_after_manual_review']==55
assert notes['official_mapping_verified']==notes['tilezed_verified']==notes['certified']==0
ev=R/'review/v178_alt_scene_bulk172'
assert filesha(ev/'ALT_BC_163_ORIGINAL_TMXS.zip')==evidence['evidence_zip_sha']
assert filesha(ev/'ALT_SCENE_RESULTS_163.csv')==evidence['evidence_csv_sha']
sources=csvrows(ev/'ALT_SCENE_RESULTS_163.csv')
assert len(sources)==163 and len({(r['tile_set_name'],int(r['local_id'])) for r in sources})==163
manual={int(i):v for i,v in notes['notes'].items()}
assert set(manual)=={int(r['index']) for r in sources}
raw=readparent(parent)
tmp=Path('/tmp/pz_v179_bulk_manual.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==240 and before['v178_alternate_scene_evidence']==163 and before['v177_visual_review']==23
accepted=[];excluded=[]
with zipfile.ZipFile(ev/'ALT_BC_163_ORIGINAL_TMXS.zip') as z:
 assert z.testzip() is None and len(z.namelist())==163*4
 for r in sources:
  idx=int(r['index']);key=(r['tile_set_name'],int(r['local_id']));n=manual[idx]
  prefix=f'{idx:05}/'
  a=imagefromzip(z,prefix+'A_original.png','RGBA')
  b=imagefromzip(z,prefix+'B_alt_actual_TMX.png','RGB')
  c=imagefromzip(z,prefix+'C_one_GID_removed.png','RGB')
  d=imagefromzip(z,prefix+'B_minus_C_raw.png','RGB')
  assert a.size[0]>0 and b.size==c.size==d.size==(800,580)
  assert sha(a.tobytes())==r['original_A_pixel_sha']
  difference=ImageChops.difference(b,c)
  assert difference.getbbox()==d.getbbox(),('difference',idx)
  changed=sum(p>0 for p in difference.convert('L').getdata())
  assert changed==int(r['alternate_changed_pixels'])==int(n['source_alternate_changed_pixels']),('delta',idx)
  assert r['actual_raw_gid_matches_key']==r['exactly_one_target_GID_removed']=='1'
  assert r['observed']==r['mapping_verified']==r['tilezed_verified']==r['certified']=='0'
  assert n['identity_certified']==n['official_mapping_verified']==n['tilezed_verified']==0
  assert n['orientation']==n['connections']=='unverified'
  row=db.execute('SELECT source_png,alternate_tmx,alternate_layer,alternate_level,alternate_x,alternate_y,alternate_raw_gid,alternate_changed_pixels,neighbors_missing,outside_canvas,original_A_pixel_sha,alternate_TMX_sha256,observed FROM v178_alternate_scene_evidence WHERE tile_set_name=? AND local_id=?',key).fetchone()
  assert row is not None
  comparison=(r['source_png'],r['alternate_tmx'],int(r['alternate_layer']),int(r['alternate_level']),int(r['alternate_x']),int(r['alternate_y']),int(r['alternate_raw_gid']),changed,int(r['neighbors_missing']),int(r['outside_canvas']),r['original_A_pixel_sha'],r['alternate_TMX_sha256'],0)
  assert row==comparison,('v178_source_DB_evidence_disagrees',idx)
  assert db.execute('SELECT COUNT(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',key).fetchone()[0]==1
  hold=bool(n['manual_hold'])
  if hold:
   reason='new_B_C_zero' if changed==0 else 'source_neighbors_missing' if int(r['neighbors_missing']) else 'visual_ambiguous_or_too_few_pixels'
   excluded.append(dict(index=idx,tile_set_name=key[0],local_id=key[1],reason=reason,changed_pixels=changed,original_a_pixel_sha=sha(a.tobytes())))
   continue
  assert changed>=200 and int(r['neighbors_missing'])==0 and int(r['outside_canvas'])==0
  assert n['confidence'] in ('low','medium','high') and len(n['features'])>=15
  accepted.append(dict(index=idx,tile_set_name=key[0],local_id=key[1],TMX=r['alternate_tmx'],
   layer=int(r['alternate_layer']),level=int(r['alternate_level']),x=int(r['alternate_x']),y=int(r['alternate_y']),raw_gid=int(r['alternate_raw_gid']),
   original_A_pixel_sha=r['original_A_pixel_sha'],B_C_changed_pixels=changed,
   candidate=n['candidate'],features=n['features'],part=n['part'],material=n['material'],
   confidence=n['confidence'],orientation='unverified',connections='unverified',
   source_basis='v178 original PNG/TMX SHA256, original raw GID and true alternate site separately independently verified; v179 human 28-sheet visual + 652 PNG ZIP A/B/C pixel recheck',
   original_proof_zip='review/v178_alt_scene_bulk172/ALT_BC_163_ORIGINAL_TMXS.zip',
   review_status='provisional_candidate',mapping_verified=0,tilezed_verified=0,certified=0))
assert len(accepted)==108 and len(excluded)==55,(len(accepted),len(excluded))
assert len({(r['tile_set_name'],r['local_id']) for r in accepted})==108
assert sum(x['reason']=='new_B_C_zero' for x in excluded)==37
assert sum(x['reason']!='new_B_C_zero' for x in excluded)==18
fields=list(accepted[0])
itypes={'index','local_id','layer','level','x','y','raw_gid','B_C_changed_pixels','mapping_verified','tilezed_verified','certified'}
db.execute('CREATE TABLE v179_visual_review ('+','.join('"'+k+'" '+('INTEGER' if k in itypes else 'TEXT') for k in fields)+', PRIMARY KEY(tile_set_name,local_id), CHECK(mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
db.executemany('INSERT INTO v179_visual_review ('+','.join('"'+k+'"' for k in fields)+') VALUES ('+','.join('?' for _ in fields)+')',[tuple(r[k] for k in fields) for r in accepted])
db.commit()
after={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==241 and set(after)-set(before)=={'v179_visual_review'}
assert all(after[name]==count for name,count in before.items()) and after['v179_visual_review']==108
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
outputraw=tmp.read_bytes();compressed=zlib.compress(outputraw,8)
encoded=base64.b64encode(compressed).decode('ascii');parts=[]
for j in range(0,len(encoded),3000000):
 p=DBOUT/f'v179.part{j//3000000:03}.b64'
 p.write_text(encoded[j:j+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(outputraw)
dbm=dict(version='v179',parent='v178',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(outputraw),compressed_sha256=sha(compressed),sqlite_bytes=len(outputraw),parts=parts,
 table_count=241,prior_tables_preserved=240,new_rows=108,new_observed_rows=108,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
with (OUT/'VISUAL_REVIEW_108.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(accepted)
with (OUT/'EXCLUDED_55.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(excluded[0]));w.writeheader();w.writerows(excluded)
total=9684+108
assert total==9792 and 10042-total==250
manifest=dict(version='v179',visually_reviewed=163,positive_alt_B_C=126,
 newly_provisional=108,held=55,held_zero=37,held_weak_or_missing=18,
 accepted_indices=sorted(x['index'] for x in accepted),source_original_sheets=28,
 observed_parent=9684,observed_now=total,remaining_checkpoint=250,
 remaining_physical_unique=356-108,checkpoint_discrepancy=2,
 database_table_count=241,parent_tables_preserved=240,sqlite_sha256=sha(outputraw),
 review_csv_sha256=filesha(OUT/'VISUAL_REVIEW_108.csv'),
 excluded_csv_sha256=filesha(OUT/'EXCLUDED_55.csv'),
 original_evidence_zip_sha256=evidence['evidence_zip_sha'],
 official_mapping_verified=0,tilezed_verified=0,identity_certified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v179 대형 A/B/C 접촉시트 28장 163종 직접 판독: 신규 잠정 108종, 보류55종\n\n'
 'v178에서 출처·원본 TIFF가 아닌 타일셋 PNG, TMX raw GID·층·레이어·좌표와 C 단일 GID 제거를 먼저 원본 검증한 뒤, 이번 단계는 그 증거를 재사용하여 실제 A/B/C/차이 28장의 육안 관찰과 652개 ZIP PNG RGB 변화를 재검증했다.\n'
 '건설 자재·철골·난간·장작더미·모래더미·가구/전화기/지구본·산업 덕트·욕실 벽·아치형 문틀 등 163종의 원본 이미지 및 실제 사용 배치를 검토했고 108종은 독립 외형·부분역할 근거가 충분하여 provisional_candidate. 차이 0인37종, 원본 이웃 부족 또는 변화 작거나 형태 모호한18종은 보류.\n'
 '새 물리 SQLite 241테이블: 부모 v178 240개 모든 기존 행값/행수 그대로 보존, 신규108행 한 테이블만 추가. 이미지 잠정관찰 9792/10042 (97.51%), 상태 미관찰250, 물리적으로 실제 미관찰248 + 역사적 집계 차이2. 공식 A/LocalID/TileZed 및 사물 정체 최종 인증0.\n'
 '수동80·제외14·held D2/JUMBO20·원본 TMX 84·PNG/이전 역사적 DB·ZIP 모두 그대로. 이번은 같은 공식 A를 다른 실제 TMX 위치 B에 넣은 증거로서 사용자 정의 D(다른 A를 같은 B 위치에 넣기)와 구별.\n',encoding='utf-8')
print('PASS v179 human reviewed 163, source-supported 108 provisional',json.dumps(manifest,ensure_ascii=False),flush=True)
