#!/usr/bin/env python3
"""v184: second-pass manual review, strictly original A and actual TMX B/C.
Only 3 of 4 individually re-inspected previously held fragments are provisional.
Never promote masked layer X/Y or source-incomplete observations.
"""
from pathlib import Path
from functools import lru_cache
import bisect,base64,csv,hashlib,io,json,re,sqlite3,xml.etree.ElementTree as ET,zipfile,zlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v184_true_BC_reinspect4';DBOUT=R/'analysis/current/v184'
DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(8*1024*1024),b''):h.update(x)
 return h.hexdigest()
def csvrows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def raw_sqlite(m):
 packed=base64.b64decode(''.join((R/x).read_text('ascii').strip() for x in m['parts']),validate=True)
 assert sha(packed)==m['compressed_sha256']
 original=zlib.decompress(packed)
 assert sha(original)==m['sqlite_sha256'] and len(original)==m['sqlite_bytes']
 return original
notes=json.loads((OUT/'MANUAL_VISUAL_NOTES.json').read_text(encoding='utf-8'))
parent=json.loads((R/'analysis/current/v183/MANIFEST.json').read_text())
proofmeta=json.loads((R/'review/v182_occlusion202/MANIFEST.json').read_text())
history=json.loads((R/'review/v183_original_BC_visual65/MANIFEST.json').read_text())
assert parent['version']=='v183' and parent['table_count']==245 and parent['new_rows']==65
assert notes['version']=='v184' and notes['parent']=='v183'
assert set(map(int,notes['notes']))=={29,298,327,3901}
assert notes['provisional_eligible']==3 and notes['still_held']==1
assert notes['official_mapping_verified']==notes['tilezed_verified']==notes['identity_certified']==0
assert history['source_verified_promoted']==65 and history['held_total']==137
assert proofmeta['source_new_key_unobserved_before']==202 and proofmeta['original_B_C_positive']==87
src=R/'review/v182_occlusion202'
records={int(r['index']):r for r in csvrows(src/'SOURCE_OCCLUSION_202.csv')}
held={int(r['index']):r for r in csvrows(R/'review/v183_original_BC_visual65/HELD_137.csv')}
a={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')}
assert len(records)==202 and len(held)==137 and len(a)==4633
for idx in map(int,notes['notes']):
 assert idx in held and held[idx]['reason']=='true_B_C_positive_but_missing_neighbors_or_ambiguous'
 assert records[idx]['full_context_missing_neighbor_sprites']=='0'
 assert int(records[idx]['actual_B_C_pixels'])>=100
 assert records[idx]['original_source_A_pixels_verified']=='1'
zip_path=Path('/tmp/pz-v184-verified-original-202-scenes.zip')
with zip_path.open('wb') as f:
 for part in proofmeta['evidence_zip_parts']:
  with (src/part).open('rb') as p:
   for block in iter(lambda:p.read(8*1024*1024),b''):f.write(block)
assert zip_path.stat().st_size==proofmeta['evidence_zip_bytes']
assert filesha(zip_path)==proofmeta['image_evidence_zip_sha256']
@lru_cache(maxsize=4)
def mapdata(name):
 path=R/'B4220.3_MapExport_256/tmx'/name
 root=ET.parse(path).getroot()
 layers=list(root.iter('layer'))
 ts=sorted((int(x.get('firstgid')),x.get('name')) for x in root.findall('tileset') if x.get('name'))
 return root,layers,ts,filesha(path)
accepted=[];deferred=[]
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None and len(z.namelist())==201*6
 for idx in [29,298,327,3901]:
  meta=records[idx];key=(meta['tile_set_name'],int(meta['local_id']))
  note=notes['notes'][str(idx)]
  src_a=a[key];p=f'{idx:05d}/'
  with Image.open(io.BytesIO(z.read(p+'A_original.png'))) as im: A=im.convert('RGBA')
  with Image.open(io.BytesIO(z.read(p+'B_true_TMX.png'))) as im: B=im.convert('RGB')
  with Image.open(io.BytesIO(z.read(p+'C_true_TMX_target_removed.png'))) as im: C=im.convert('RGB')
  assert sha(A.tobytes())==src_a['selected_rgba_pixel_sha256'],('png_A',idx)
  assert B.size==C.size==(800,580)
  delta=sum(v!=0 for v in ImageChops.difference(B,C).convert('L').getdata())
  assert delta==int(meta['actual_B_C_pixels']) and delta>=100
  assert int(meta['layer_limited_B_C_pixels'])>=0
  assert note['official_mapping_verified']==note['tilezed_verified']==note['identity_certified']==0
  if note['manual_hold']:
   deferred.append(dict(index=idx,tile_set_name=key[0],local_id=key[1],actual_B_C_pixels=delta,
     reason='still_ambiguous_after_independent_manual_second_pass',observed=0,certified=0))
   continue
  root,layers,ts,tsha=mapdata(meta['original_tmx'])
  assert tsha==meta['tmX_sha256']
  il=int(meta['layer']);x=int(meta['x']);y=int(meta['y']);level=int(meta['level'])
  assert 0<=il<len(layers) and 0<=x<int(root.get('width')) and 0<=y<int(root.get('height'))
  layer=layers[il]
  prop=layer.find("properties/property[@name='level']")
  actual_level=int(layer.get('level','0')) if 'level' in layer.attrib else int((prop.get('value') or prop.text or '0') if prop is not None else '0')
  assert actual_level==level
  vals=[int(t) for t in re.findall(r'\d+',layer.find('data').text or '')]
  assert len(vals)==int(root.get('width'))*int(root.get('height'))
  gid=vals[y*int(root.get('width'))+x]
  assert gid==int(meta['tmX_raw_gid'])
  j=bisect.bisect_right([v[0] for v in ts],gid&0x0fffffff)-1
  assert j>=0 and (ts[j][1],(gid&0x0fffffff)-ts[j][0])==key
  accepted.append(dict(index=idx,tile_set_name=key[0],local_id=key[1],candidate=note['candidate'],
   features=note['features'],part=note['part'],material=note['material'],confidence=note['confidence'],
   orientation='unverified',connections='unverified',real_B_C_pixels=delta,
   original_A_RGBA_SHA256=sha(A.tobytes()),source_tmx=meta['original_tmx'],source_tmx_SHA256=tsha,
   layer=il,level=level,x=x,y=y,raw_gid=gid,evidence_basis=note['observation_basis'],
   review_status='provisional_candidate',certified=0,official_mapping_verified=0,tilezed_verified=0))
assert len(accepted)==3 and len(deferred)==1 and deferred[0]['index']==298
assert {x['index'] for x in accepted}=={29,327,3901}
with (OUT/'VISUAL_REVIEW_3.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(accepted[0]));w.writeheader();w.writerows(accepted)
with (OUT/'HELD_1.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(deferred[0]));w.writeheader();w.writerows(deferred)
tmp=Path('/tmp/pz-v184-original-bc.sqlite');tmp.write_bytes(raw_sqlite(parent))
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==245 and before['v183_visual_review']==65
for q in accepted:
 k=(q['tile_set_name'],q['local_id'])
 assert db.execute('SELECT COUNT(*) FROM v183_visual_review WHERE tile_set_name=? AND local_id=?',k).fetchone()[0]==0
 assert db.execute('SELECT COUNT(*) FROM v182_source_layer_occlusion_audit WHERE tile_set_name=? AND local_id=?',k).fetchone()[0]==1
 assert db.execute('SELECT COUNT(*) FROM v175_remaining_evidence_audit WHERE tile_set_name=? AND local_id=?',k).fetchone()[0]==1
cols=list(accepted[0])
ints={'index','local_id','real_B_C_pixels','layer','level','x','y','raw_gid','certified','official_mapping_verified','tilezed_verified'}
db.execute('CREATE TABLE v184_visual_review ('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+', PRIMARY KEY(tile_set_name,local_id), CHECK(certified=0 AND official_mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v184_visual_review ('+','.join('"'+x+'"' for x in cols)+') VALUES ('+','.join('?' for _ in cols)+')',[tuple(v[x] for x in cols) for v in accepted])
db.commit()
after={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==246 and set(after)-set(before)=={'v184_visual_review'}
assert all(after[n]==q for n,q in before.items()) and after['v184_visual_review']==3
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
raw=tmp.read_bytes();comp=zlib.compress(raw,8)
enc=base64.b64encode(comp).decode('ascii');parts=[]
for n in range(0,len(enc),3000000):
 part=DBOUT/f'v184.part{n//3000000:03}.b64';part.write_text(enc[n:n+3000000]);parts.append(part.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/x).read_text('ascii') for x in parts))))==sha(raw)
dbm=dict(version='v184',parent='v183',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(raw),compressed_sha256=sha(comp),sqlite_bytes=len(raw),parts=parts,
 table_count=246,prior_tables_preserved=245,new_rows=3,new_observed_rows=3,
 integrity_check='ok',certified=0,official_mapping_verified=0,tilezed_verified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
m=dict(version='v184',parent='v183',manual_source_original_B_C_reviewed=4,
 prior_ambiguous_count=4,promoted_provisional=3,still_held=1,
 upgraded_indices=[29,327,3901],held_indices=[298],
 source_true_TMX_B_C_reverified=4,source_neighbor_missing=0,
 prior_observed=9894,current_observed=9897,remaining_checkpoint=145,
 original_A_sha_count=4,original_TMX_sha_count=3,
 no_masked_diagnostic_only_promotion=True,
 official_mapping_verified=0,tilezed_verified=0,identity_certified=0,
 parent_tables_preserved=245,physical_tables=246,sqlite_sha256=sha(raw),
 observations_sha256=filesha(OUT/'VISUAL_REVIEW_3.csv'),held_csv_sha256=filesha(OUT/'HELD_1.csv'),
 evidence_original_zip_sha256=proofmeta['image_evidence_zip_sha256'])
(OUT/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v184 원본 실제 TMX A/B/C 모호한 부품 4종 재검수\n\n'
 'v183에서 실제 B-C가 100픽셀 이상이고 주변 원본 소스 누락이 없는 4종(29,298,327,3901)을 동일 원본 A와 원래 TMX B/C 장면에서 재검토. 29는 휴대 통신기 모양의 작은 장치, 327은 두 가로대의 난간 부품, 3901은 벽돌무늬 박공 사선 끝판으로 외형/부품계열만 provisional_candidate로 등록. 298은 역할 불명 작은 목재 조각으로 보류. 새 정체 최종 인증0.\n'
 '실제 원본 PNG A_RGBA SHA, 원본 TMX raw GID·좌표·레이어·층/해시, 실제 B-C 453/361/250/125픽셀 대조. 위층 숨김 X/Y 진단 영상은 근거로 사용하지 않음. 부모 v183 물리 245테이블의 전체 값/행 수 보존해 새 246번째 3행 테이블만 추가.\n'
 '누적 9897/10042(98.56%) 잠정 이미지 관찰, 기록상 미관찰145. 공식 PNG↔Local ID/TileZed 맵과 사물 최종 인증0. 84 원본 TMX/PNG·기존5409·사용자 검수80·제외14·D2/JUMBO20·과거 DB/증거 모두 보존.\n',encoding='utf-8')
print('PASS v184',json.dumps(m,ensure_ascii=False),flush=True)
