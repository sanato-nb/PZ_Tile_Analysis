#!/usr/bin/env python3
"""v183: original TMX B/C real-visibility manual identity hypotheses.
Do NOT promote masked-only X-Y diagnostics as genuine B/C evidence.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import base64,bisect,csv,hashlib,io,json,re,sqlite3,xml.etree.ElementTree as ET,zlib,zipfile
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v183_original_BC_visual65'
DBOUT=R/'analysis/current/v183'
DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for piece in iter(lambda:f.read(8*1024*1024),b''):h.update(piece)
 return h.hexdigest()
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sqlite_raw(man):
 c=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in man['parts']),validate=True)
 assert sha(c)==man['compressed_sha256']
 data=zlib.decompress(c)
 assert sha(data)==man['sqlite_sha256'] and len(data)==man['sqlite_bytes']
 return data
parent=json.loads((R/'analysis/current/v182/MANIFEST.json').read_text())
proofmeta=json.loads((R/'review/v182_occlusion202/MANIFEST.json').read_text())
notes=json.loads((OUT/'MANUAL_VISUAL_NOTES.json').read_text())
assert parent['version']=='v182' and parent['table_count']==244
assert proofmeta['version']=='v182' and proofmeta['original_B_C_positive']==87
assert proofmeta['true_original_TMXS_rendered']==201
assert notes['parent']=='v182' and len(notes['notes'])==76
assert notes['eligible_source_verified_after_review']==65
assert notes['held_positive_ge100']==11 and notes['held_positive_under100']==11
assert notes['held_B_C_zero']==114 and notes['missing_original_A']==1
assert notes['final_identity_certified']==notes['official_mapping_verified']==notes['tilezed_verified']==0
src=R/'review/v182_occlusion202'
csvfile=src/'SOURCE_OCCLUSION_202.csv'
assert filesha(csvfile)==proofmeta['evidence_csv_sha256']
record=readcsv(csvfile)
assert len(record)==202 and len({(r['tile_set_name'],r['local_id']) for r in record})==202
manual={int(k):v for k,v in notes['notes'].items()}
positive_ge100={int(r['index']) for r in record if r['actual_B_C_pixels'] and int(r['actual_B_C_pixels'])>=100}
assert set(manual)==positive_ge100 and len(positive_ge100)==76
selected={idx for idx,n in manual.items() if not n['manual_hold']}
assert len(selected)==65
source_a={(r['tile_set_name'],int(r['local_id'])):r for r in readcsv(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')}
assert len(source_a)==4633
# Reassemble exact GitHub-stored binary parts, verify complete archive hash+CRC.
parts=proofmeta['evidence_zip_parts']
assert len(parts)==3
zip_path=Path('/tmp/pz-v183-v182-original-source.zip')
with zip_path.open('wb') as f:
 for part in parts:
  p=src/part
  assert p.stat().st_size<=70000000
  with p.open('rb') as g:
   for block in iter(lambda:g.read(4*1024*1024),b''):f.write(block)
assert zip_path.stat().st_size==proofmeta['evidence_zip_bytes']
assert filesha(zip_path)==proofmeta['image_evidence_zip_sha256']
@lru_cache(maxsize=5)
def tmx(name):
 p=R/'B4220.3_MapExport_256/tmx'/name
 root=ET.parse(p).getroot();layers=list(root.iter('layer'))
 first=sorted((int(t.get('firstgid')),t.get('name')) for t in root.findall('tileset') if t.get('name'))
 return root,layers,first,filesha(p)
accepted=[];excluded=[]
def excluded_row(r,why):
 return dict(index=int(r['index']),tile_set_name=r['tile_set_name'],local_id=int(r['local_id']),
   real_B_C_pixels=int(r['actual_B_C_pixels'] or 0),masked_only_X_Y_pixels=int(r['layer_limited_B_C_pixels'] or 0),
   reason=why,observed=0,certified=0)
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None and len(z.namelist())==201*6,('proof_count',len(z.namelist()))
 for row in record:
  idx=int(row['index']);key=(row['tile_set_name'],int(row['local_id']))
  actual=int(row['actual_B_C_pixels'] or 0)
  masked=int(row['layer_limited_B_C_pixels'] or 0)
  if row['original_source_A_pixels_verified']!='1':
   assert idx not in manual and row['tmX_raw_gid']=='' and actual==0
   excluded.append(excluded_row(row,'original_A_missing_source_and_B_C_evidence'))
   continue
  pref=f'{idx:05d}/'
  with Image.open(io.BytesIO(z.read(pref+'A_original.png'))) as im:A=im.convert('RGBA')
  a=source_a[key]
  assert sha(A.tobytes())==a['selected_rgba_pixel_sha256'],('original_A_pixel_sha',idx)
  with Image.open(io.BytesIO(z.read(pref+'B_true_TMX.png'))) as im:B=im.convert('RGB')
  with Image.open(io.BytesIO(z.read(pref+'C_true_TMX_target_removed.png'))) as im:C=im.convert('RGB')
  assert B.size==C.size==(800,580)
  actual_calc=sum(x!=0 for x in ImageChops.difference(B,C).convert('L').getdata())
  assert actual_calc==actual,('real_B_C_delta',idx,actual_calc,actual)
  if idx not in manual:
   assert actual<100,('unreviewed_true_scene_positive_ge100',idx,actual)
   why='true_B_C_zero_not_visible' if actual==0 else 'true_B_C_too_few_pixels_under100'
   # Masked X-Y may be positive, NEVER substitute for real B-C.
   excluded.append(excluded_row(row,why))
   continue
  note=manual[idx]
  assert actual>=100
  if note['manual_hold']:
   excluded.append(excluded_row(row,'true_B_C_positive_but_missing_neighbors_or_ambiguous'))
   continue
  assert not note['held_reason']
  assert row['full_context_missing_neighbor_sprites']=='0'
  assert note['confidence'] in ('low','medium','high')
  assert note['orientation']==note['connections']=='unverified'
  assert note['official_mapping_verified']==note['tilezed_verified']==note['certified']==0
  root,layers,first,source_tmx_sha=tmx(row['original_tmx'])
  assert source_tmx_sha==row['tmX_sha256'],('source_tmx_hash',idx)
  layer=int(row['layer']);x=int(row['x']);y=int(row['y']);lvl=int(row['level'])
  assert 0<=layer<len(layers) and 0<=x<int(root.get('width')) and 0<=y<int(root.get('height'))
  ly=layers[layer]
  props=ly.find("properties/property[@name='level']")
  actual_lvl=int(ly.get('level','0')) if 'level' in ly.attrib else int((props.get('value') or props.text or '0') if props is not None else '0')
  assert lvl==actual_lvl
  vals=[int(v) for v in re.findall(r'\d+',ly.find('data').text or '')]
  assert len(vals)==int(root.get('width'))*int(root.get('height'))
  gid=vals[y*int(root.get('width'))+x]
  assert gid==int(row['tmX_raw_gid']),('source_raw_gid',idx)
  gids=[a[0] for a in first];bi=bisect.bisect_right(gids,gid&0x0fffffff)-1
  assert bi>=0 and (first[bi][1],(gid&0x0fffffff)-first[bi][0])==key,('official_source_key',idx)
  accepted.append(dict(index=idx,tile_set_name=key[0],local_id=key[1],
   candidate=note['candidate'],features=note['features'],part=note['part'],material=note['material'],
   confidence=note['confidence'],orientation='unverified',connections='unverified',
   real_B_C_pixels=actual,diagnostic_masked_X_Y_pixels=masked,
   original_A_RGBA_SHA256=sha(A.tobytes()),
   source_tmx=row['original_tmx'],source_tmx_SHA256=source_tmx_sha,
   layer=layer,level=lvl,x=x,y=y,raw_gid=gid,
   evidence_basis=note['observation_basis'],review_status='provisional_candidate',
   certified=0,official_mapping_verified=0,tilezed_verified=0))
  if len(accepted)%20==0:print('v183 REAL SOURCE APPROVED',len(accepted),flush=True)
assert len(accepted)==65 and len(excluded)==137
assert len({(r['tile_set_name'],r['local_id']) for r in accepted})==65
assert sum(x['reason']=='true_B_C_zero_not_visible' for x in excluded)==114
assert sum(x['reason']=='true_B_C_too_few_pixels_under100' for x in excluded)==11
assert sum(x['reason']=='true_B_C_positive_but_missing_neighbors_or_ambiguous' for x in excluded)==11
assert sum(x['reason']=='original_A_missing_source_and_B_C_evidence' for x in excluded)==1
with (OUT/'VISUAL_REVIEW_65.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(accepted[0]));w.writeheader();w.writerows(accepted)
with (OUT/'HELD_137.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(excluded[0]));w.writeheader();w.writerows(excluded)
raw=sqlite_raw(parent);dbpath=Path('/tmp/pz-v183.sqlite');dbpath.write_bytes(raw)
db=sqlite3.connect(dbpath)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==244 and before['v182_source_layer_occlusion_audit']==202
for a in accepted:
 assert db.execute('SELECT COUNT(*) FROM v182_source_layer_occlusion_audit WHERE tile_set_name=? AND local_id=?',(a['tile_set_name'],a['local_id'])).fetchone()[0]==1
 assert db.execute('SELECT COUNT(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',(a['tile_set_name'],a['local_id'])).fetchone()[0]==1
keys=list(accepted[0])
types={k:('INTEGER' if k in ('index','local_id','real_B_C_pixels','diagnostic_masked_X_Y_pixels','layer','level','x','y','raw_gid','certified','official_mapping_verified','tilezed_verified') else 'TEXT') for k in keys}
db.execute('CREATE TABLE v183_visual_review ('+','.join('"'+k+'" '+types[k] for k in keys)+', PRIMARY KEY(tile_set_name,local_id), CHECK(certified=0 AND official_mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v183_visual_review ('+','.join('"'+k+'"' for k in keys)+') VALUES ('+','.join('?' for k in keys)+')',[tuple(v[k] for k in keys) for v in accepted])
db.commit()
after={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==245 and set(after)-set(before)=={'v183_visual_review'}
assert all(after[k]==v for k,v in before.items()) and after['v183_visual_review']==65
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=dbpath.read_bytes();packed=zlib.compress(newraw,8)
encoded=base64.b64encode(packed).decode('ascii');parts=[]
for k in range(0,len(encoded),3000000):
 p=DBOUT/f'v183.part{k//3000000:03}.b64'
 p.write_text(encoded[k:k+3000000],encoding='ascii')
 parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v183',parent='v182',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(packed),sqlite_bytes=len(newraw),parts=parts,
 table_count=245,prior_tables_preserved=244,new_rows=65,new_observed_rows=65,
 integrity_check='ok',certified=0,official_mapping_verified=0,tilezed_verified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
count=9829+65
assert count==9894 and 10042-count==148
summary=dict(version='v183',parent='v182',source_original_TMX_A_B_C_directly_reviewed=202,
 real_B_C_positive=87,positive_ge100=76,source_verified_promoted=65,
 held_total=137,positive_ge100_held=11,weak_under100_held=11,B_C_zero_held=114,
 source_A_missing_held=1,diagnostic_mask_only_promoted=0,
 prior_observed=9829,current_observed=count,remaining_checkpoint=148,
 current_percent=round(100*count/10042,4),official_mapping_verified=0,tilezed_verified=0,
 identity_certified=0,prior_tables_preserved=244,physical_tables=245,sqlite_sha256=sha(newraw),
 accepted_csv_sha256=filesha(OUT/'VISUAL_REVIEW_65.csv'),
 held_csv_sha256=filesha(OUT/'HELD_137.csv'),
 evidence_zip_sha256=proofmeta['image_evidence_zip_sha256'],
 evidence_source='review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')
(OUT/'MANIFEST.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'README.md').write_text(
 '# v183 실제 원본 B-C 대조 후 65종 잠정 관찰 — 진단 X/Y는 관찰 인증 근거 아님\n\n'
 'v182의 A 원본 이미지와 TMX B/C 장면 202종 접촉시트 34장을 직접 검토. 실제 원본 B-C 변화 87종 중 변화100픽셀이상 76종을 개별 기술. 주변 원본 타일 PNG 누락 7종, 의미 불명 미세한 부품 4종은 보류하고, 나머지 65종만 잠정 사물/부품에 대한 시각 관찰을 기록.\n'
 '진단 X-Y는 상위 레이어를 인위적으로 제거한 시각화이므로 원본 지도 B-C를 대신하지 않으며, 원래 변화0인 114종과 작은 변화11종/소스A누락1종은 전부 미관찰 유지. v182 원본 이미지 ZIP 분할 SHA256 및 CRC, PNG A_RGBA 픽셀 SHA, 원본 TMX raw GID·층·레이어·좌표·TMX 원본 해시와 부모 SQLite 244테이블 전체 내용/수를 재검증한다.\n'
 '기존 9,829/10,042(97.88%)에서 신규65종만 추가하여 9,894/10,042(98.53%), 기록상 미관찰 148종. 새로운 물리 DB 245테이블, 이전244 모두 보존. 공식 A PNG↔TileZed Local ID 및 최종 사물 정체 인증0. 예전 2건 역사적 관찰 집계차이 별도 유지.\n',encoding='utf-8')
print('PASS v183 actual original TMX 65 source-backed visual provisional keys',json.dumps(summary,ensure_ascii=False),flush=True)
