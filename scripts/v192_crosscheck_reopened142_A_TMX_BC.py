#!/usr/bin/env python3
"""v192: cross-check 142 reopened keys against actual original TMX raw GID and archived
real B-C evidence, using directly visually inspected original A as primary identity
signal. High/medium A morphology may become PROVISIONAL IMAGE OBSERVATIONS even when
original B-C=0 (occluded by later layers). NEVER a certified identity/LocalID mapping.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import base64,bisect,csv,hashlib,json,sqlite3,zlib,re,zipfile,xml.etree.ElementTree as ET
from PIL import Image
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v192_image_first_TMX_BC_142';OUT.mkdir(parents=True,exist_ok=True)
DBOUT=R/'analysis/current/v192';DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bbox(t):
 b=tuple(int(x) for x in t.strip('[]').split(','))
 assert len(b)==4 and 0<=b[0]<b[2] and 0<=b[1]<b[3]
 return b
@lru_cache(maxsize=36)
def atlas(path):
 with Image.open(R/path) as im:return im.convert('RGBA')
@lru_cache(maxsize=84)
def tmx(name):
 path=R/'B4220.3_MapExport_256/tmx'/name
 root=ET.parse(path).getroot()
 layers=list(root.iter('layer'))
 first=sorted((int(t.get('firstgid')),t.get('name')) for t in root.findall('tileset') if t.get('name'))
 assert len(first)>0 and len(first)==len({f for f,n in first})
 return root,layers,first,filesha(path)
manual=json.loads((R/'review/v191_reopen142_A_first/MANUAL_A_IMAGE_OBSERVATIONS_142.json').read_text(encoding='utf-8'))
v191=json.loads((R/'review/v191_reopen142_A_first/MANIFEST.json').read_text(encoding='utf-8'))
v182=json.loads((R/'review/v182_occlusion202/MANIFEST.json').read_text(encoding='utf-8'))
assert len(manual['manual_image_notes'])==142 and v191['manual_A_appearance_descriptions']==132
assert v182['true_original_TMXS_rendered']==201 and v182['source_new_key_unobserved_before']==202
source=csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
assert len(source)==4633
excluded=csvrows(R/'review/v188_active_review_exclusions/EXCLUDED_FROM_ACTIVE_REVIEW_142.csv')
assert len(excluded)==142
occ=csvrows(R/'review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')
assert len(occ)==202
occ_by_key={(x['tile_set_name'],int(x['local_id'])):(i,x) for i,x in enumerate(occ)}
assert len(occ_by_key)==202
prior_by_key={(x['tile_set_name'],int(x['local_id'])):x for x in excluded}
assert len(prior_by_key)==142
assert filesha(R/'review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')==v182['evidence_csv_sha256']
assert filesha(R/'review/v191_reopen142_A_first/MANUAL_A_IMAGE_OBSERVATIONS_142.json')==v191['manual_notes_sha256']
# Verify archived real A/B/C and diagnostic evidence; masked X is not true original B.
from tempfile import NamedTemporaryFile
with NamedTemporaryFile(prefix='v192-proof-',suffix='.zip') as f:
 h=hashlib.sha256()
 for rel in v182['evidence_zip_parts']:
  with (R/'review/v182_occlusion202'/rel).open('rb') as part:
   for x in iter(lambda:part.read(8*1024*1024),b''):
    f.write(x);h.update(x)
 f.flush()
 assert h.hexdigest()==v182['image_evidence_zip_sha256']
 with zipfile.ZipFile(f.name) as z:
  assert z.testzip() is None and len(z.namelist())>=6*201,('ZIP_images',len(z.namelist()))
 print('validated original v182 A/B/C historical evidence ZIP bytes/CRC',flush=True)
parent=json.loads((R/'analysis/current/v190/MANIFEST.json').read_text())
assert parent['version']=='v190' and parent['table_count']==252
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz-v192-142-image-first.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT count(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==252 and before['v188_active_review_disposition']==142
# Decision is based on VERIFIED A shape PLUS actual matching original TMX GID.
# A positive/zero B-C only describes whether it was exposed, not its own identity.
out=[]
for i,note in enumerate(manual['manual_image_notes']):
 assert note['order']==i and note['explicit_user_reopened']
 key=(note['tile_set_name'],int(note['local_id']))
 assert key in prior_by_key
 old=prior_by_key[key]
 assert old['previous_source_key_observed']=='0'
 assert db.execute('SELECT COUNT(*) FROM v188_active_review_disposition WHERE tile_set_name=? AND local_id=?',key).fetchone()==(1,)
 status='held_no_exact_original_A'
 a_status='unverified'
 idx=note['index']
 o=None;o_page='';changed=None;diagnostic=None;missing=None;clipped=None
 source_png='';crop_sha='';tmx_name='';level=None;layer=None;x=None;y=None;gid=None;tmx_sha=''
 if note['original_A_sha256_verified']:
  assert idx is not None and note['original_A_contact_sheet'].endswith('.jpg')
  src=source[int(idx)]
  assert (src['tile_set_name'],int(src['local_id']))==key and src['selection_status']=='selected_provisional'
  source_png=src['source_image_path']
  assert source_png and filesha(R/source_png)==src['source_png_sha256'],('PNG_SHA',idx)
  im=atlas(source_png).crop(bbox(src['selected_crop_xyxy']))
  crop_sha=sha(im.tobytes())
  assert crop_sha==src['selected_rgba_pixel_sha256'],('RGBA_pixel_hash',idx)
  assert im.getchannel('A').getbbox() is not None
  a_status='verified_exact_selected_original_A_RGBA_and_visible'
  assert key in occ_by_key,('missing_prior_BC_original',idx)
  order,o=occ_by_key[key]
  assert int(o['index'])==idx and o['source_A_status']=='selected_provisional'
  assert o['original_source_A_pixels_verified']=='1'
  tmx_name=o['original_tmx'];assert tmx_name
  root,layers,first,tmx_sha=tmx(tmx_name)
  assert tmx_sha==o['tmX_sha256'],('tmx_bytes_modified',idx)
  layer=int(o['layer']);x=int(o['x']);y=int(o['y'])
  assert 0<=layer<len(layers) and 0<=x<int(root.get('width')) and 0<=y<int(root.get('height'))
  ly=layers[layer];data=ly.find('data')
  assert data is not None and data.get('encoding')=='csv'
  vals=[int(z) for z in re.findall(r'\d+',data.text or '')]
  assert len(vals)==int(root.get('width'))*int(root.get('height'))
  gid=vals[y*int(root.get('width'))+x]
  assert gid==int(o['tmX_raw_gid']),('raw_GID_drift',idx)
  masked_gid=gid&0x0fffffff
  p=bisect.bisect_right([z[0] for z in first],masked_gid)-1
  assert p>=0 and (first[p][1],masked_gid-first[p][0])==key,('GID_to_key',idx)
  raw_level=ly.get('level')
  if raw_level is None:
   prop=ly.find("properties/property[@name='level']")
   raw_level=(prop.get('value') or prop.text or '0') if prop is not None else '0'
  level=int(raw_level);assert level==int(o['level'])
  changed=int(o['actual_B_C_pixels'])
  diagnostic=int(o['layer_limited_B_C_pixels'])
  missing=int(o['full_context_missing_neighbor_sprites'])
  clipped=int(o['source_full_map_5x5_clipped'])
  assert changed>=0 and diagnostic>=0 and missing>=0 and clipped in (0,1)
  o_page='review/v182_occlusion202/sheets/SOURCE_LAYER_DIAGNOSTIC_%02d.jpg'%(order//6)
  assert (R/o_page).is_file(),('archived_BC_sheet_missing',o_page)
  confidence=note['appearance_confidence']
  assert confidence in ('high','medium','low') and note['appearance_observation']
  if confidence in ('high','medium'):
   status='provisional_A_visible_actual_TMX_key_verified'
  else:status='held_A_low_confidence_part_unresolved'
 else:
  assert note['appearance_confidence']=='none' and not note['appearance_observation']
  assert key not in occ_by_key or key[0]=='overlay_graffiti_wall_02'
  status='held_exact_original_A_unavailable'
 # Important: provisional image observation != official PNG/LocalID or final identity certification.
 provisional=int(status=='provisional_A_visible_actual_TMX_key_verified')
 out.append(dict(index=idx,order=i,tile_set_name=key[0],local_id=key[1],
  origin=old['origin'],previous_exclusion_reason=old['source_blocker_category'],
  original_A_PNG=source_png,original_A_RGBA_sha256=crop_sha,A_image_status=a_status,
  A_direct_visible_description=note['appearance_observation'] or '',
  A_appearance_confidence=note['appearance_confidence'],
  real_original_BC_reference=o_page,actual_TMX=tmx_name,actual_TMX_sha256=tmx_sha,
  source_layer=layer,source_level=level,source_x=x,source_y=y,raw_gid=gid,
  true_original_B_C_changed_pixels=changed,masked_diagnostic_only_pixels=diagnostic,
  original_missing_neighbor_sprites=missing,original_scene_clipped=clipped,
  true_B_C_source_status=('occluded_in_true_scene' if changed==0 else 'changed_in_true_scene' if changed is not None else 'no_source_scene'),
  A_vs_TMX_review_status=status,
  new_provisional_observation=provisional,final_certified=0,official_mapping_verified=0,tilezed_verified=0,
  judgment_basis='Visual appearance from original A; exact A RGBA hash and actual source TMX GID/tileset/localID crosschecked; original real B-C positive/zero tracked separately. X/Y masked diagnostic cannot count as real B-C.' if provisional else 'Original A unknown or insufficiently distinct; hold without identity fabrication.'))
assert len(out)==142 and len({(r['tile_set_name'],r['local_id']) for r in out})==142
assert sum(r['new_provisional_observation'] for r in out)==109
assert sum(r['A_appearance_confidence']=='high' for r in out)==60
assert sum(r['A_appearance_confidence']=='medium' for r in out)==49
assert sum(r['A_appearance_confidence']=='low' for r in out)==23
assert sum(r['A_appearance_confidence']=='none' for r in out)==10
assert sum(r['A_image_status'].startswith('verified_') for r in out)==132
assert sum(r['new_provisional_observation'] and r['true_original_B_C_changed_pixels']==0 for r in out)==99
assert sum(r['new_provisional_observation'] and r['true_original_B_C_changed_pixels']>0 for r in out)==10
assert sum(r['new_provisional_observation'] and r['original_missing_neighbor_sprites']>0 for r in out)==6
# Baseline observations remain historical. New table records image-first re-review
# with actual original placement, not a replacement of certified entries.
fields=list(out[0].keys())
intfields={'index','order','local_id','source_layer','source_level','source_x','source_y','raw_gid','true_original_B_C_changed_pixels','masked_diagnostic_only_pixels','original_missing_neighbor_sprites','original_scene_clipped','new_provisional_observation','final_certified','official_mapping_verified','tilezed_verified'}
db.execute('CREATE TABLE v192_reopened_A_first_TMX_BC_review ('+','.join('"'+k+'" '+('INTEGER' if k in intfields else 'TEXT') for k in fields)+',PRIMARY KEY(tile_set_name,local_id),CHECK(final_certified=0 AND official_mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v192_reopened_A_first_TMX_BC_review ('+','.join('"'+k+'"' for k in fields)+') VALUES ('+','.join('?' for _ in fields)+')', [tuple(r[k] for k in fields) for r in out])
db.commit()
after={n:db.execute('SELECT count(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==253 and set(after)-set(before)=={'v192_reopened_A_first_TMX_BC_review'}
assert all(after[k]==v for k,v in before.items())
assert after['v192_reopened_A_first_TMX_BC_review']==142
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();compressed=zlib.compress(newraw,8)
enc=base64.b64encode(compressed).decode('ascii');parts=[]
for i in range(0,len(enc),3000000):
 p=DBOUT/f'v192.part{i//3000000:03}.b64';p.write_text(enc[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v192',parent='v190',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(compressed),sqlite_bytes=len(newraw),
 parts=parts,table_count=253,prior_tables_preserved=252,new_rows=142,new_observed_rows=109,
 integrity_check='ok',official_mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
with (OUT/'CROSSCHECK_142.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
manifest=dict(version='v192',scope='142 user reopened source A direct appearance crossed with true original TMX scene and real B-C evidence',
 total=142,A_RGBA_sha_verified=132,TMX_raw_GID_and_exact_key_verified=132,
 A_visible_high=60,A_visible_medium=49,A_ambiguous_low_held=23,exact_A_unavailable_held=10,
 new_A_first_provisional_observations=109,new_B_C_positive_in_accepted=10,
 new_B_C_zero_occluded_in_accepted=99,new_B_C_missing_neighbor_in_accepted=6,
 original_scene_evidence_archive_sha256=v182['image_evidence_zip_sha256'],
 image_observed_parent=9898,image_observed_now=10007,
 remaining_checkpoint=35,physical_unique_unobserved_remaining=33,historical_two_count_gap=2,
 official_mapping_verified=0,tilezed_verified=0,certified=0,
 parent_sqlite_tables_preserved=252,sqlite_tables=253,
 sqlite_sha256=sha(newraw),crosscheck_csv_sha256=filesha(OUT/'CROSSCHECK_142.csv'),
 hold_reason_distribution=dict(Counter(r['A_vs_TMX_review_status'] for r in out)))
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v192 142종 재개검수: 원본 스프라이트 A 이미지 자체 + 실제 TMX B/C 교차대조\n\n'
 'v191에서 원본 A를 직접 시각 검수한 132종 중, 분명한 물체/부품 형상 high60/medium49를 낮음~중간 신뢰도의 **원본 A 기반 잠정 이미지 관찰 109종**으로 새로 등록. '
 '각 기록은 원본 A PNG SHA256·RGBA 픽셀 SHA256와 TMX 원본 바이트 SHA256·layer/level/좌표/raw GID 및 firstgid 원본키 대응을 검사함.\n\n'
 '**중요**: 이들 중 99종은 진짜 TMX B-C=0으로 가려져 있어, 실제 배치에서 사물이 보인다는 뜻이 아님. '
 '원본 A 자체를 보고 형상을 추론한 provisional_identity_part_candidate이며 투명/확정 식별/공식 TileZed 인증이 아님. '
 '다른 10종은 B-C 양수이지만 6종의 주변 스프라이트 누락 가능성을 포함해 개별 증거 한계를 기록함. '
 '원본 A가 너무 작은 조각 23종과 정확한 A 자체가 없는 10종은 33종 보류. '
 '진단용 마스킹 이미지는 실제 B/C나 사용자 D로 계산하지 않음.\n\n'
 '누적 원본 A 잠정 관찰 기록을 9,898에서 10,007 /10,042(99.65%)로 갱신. 원본 고유 미관찰 33 + 과거 회계 차이2 = 35 기록상 미관찰. '
 '공식 PNG↔Local ID/TileZed/실물 최종 인증은 여전히0. '
 '부모 v190 물리 SQLite252개 테이블 모든 행·값/수 유지, 신규 v192 개별 142행 1테이블로 물리 253테이블.\n'
 '증거: 원본 시각 관찰 review/v191_reopen142_A_first/sheets/ 및 MANUAL_A_IMAGE_OBSERVATIONS_142.json, '
 '원본 TMX B/C review/v182_occlusion202/sheets/ 및 OCCLUSION_PROOF.part*.bin (ZIP CRC·SHA checked), '
 '이번 교차대조 CROSSCHECK_142.csv와 MANIFEST.json.\n',encoding='utf-8')
print('PASS v192 CROSSCHECK 142',json.dumps(manifest,ensure_ascii=False),flush=True)
