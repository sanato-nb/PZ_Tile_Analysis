#!/usr/bin/env python3
"""v190: targeted reinspection of 12 physically unresolved original source keys.
This source audit never upgrades them to observed or officially certifies IDs.
"""
from pathlib import Path
from functools import lru_cache
import base64,bisect,csv,hashlib,json,re,sqlite3,xml.etree.ElementTree as ET,zlib
from PIL import Image
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v190_twelve_held_visual_source_recheck'
DBOUT=R/'analysis/current/v190';DBOUT.mkdir(parents=True,exist_ok=True)
def sha(x):return hashlib.sha256(x).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(8*1024*1024),b''):h.update(x)
 return h.hexdigest()
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def keys(p):return {(r['tile_set_name'],int(r['local_id'])):r for r in rows(p)}
def bbox(t):
 x=tuple(map(int,t.strip('[]').split(',')))
 assert len(x)==4 and x[2]>x[0] and x[3]>x[1]
 return x
notes=json.loads((OUT/'MANUAL_ASSESSMENT_12.json').read_text(encoding='utf-8'))
assert notes['version']=='v190' and len(notes['indices'])==12 and len(notes['notes'])==12
assert notes['reclassified_as_provisional']==notes['identity_certified']==notes['official_mapping_verified']==notes['tilezed_verified']==0
a=keys(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
A_SEQUENCE={(r['tile_set_name'],int(r['local_id'])):i for i,r in enumerate(rows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv'))}
assert len(A_SEQUENCE)==4633
occ=keys(R/'review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')
excl=keys(R/'review/v188_active_review_exclusions/EXCLUDED_FROM_ACTIVE_REVIEW_142.csv')
held=keys(R/'review/v183_original_BC_visual65/HELD_137.csv')
more=keys(R/'review/v180_remnant239_multisite/UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv')
parent=json.loads((R/'analysis/current/v189/MANIFEST.json').read_text())
assert parent['version']=='v189' and parent['table_count']==251
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert len(raw)==parent['sqlite_bytes'] and sha(raw)==parent['sqlite_sha256']
tmp=Path('/tmp/pz_v190_verified12.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={n:db.execute('SELECT count(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==251 and before['v189_held_source_reverification']==7,('parent_tables',len(before))
out=[]
@lru_cache(maxsize=40)
def png(p):
 with Image.open(R/p) as im:return im.convert('RGBA')
@lru_cache(maxsize=12)
def tmx(name):
 p=R/'B4220.3_MapExport_256/tmx'/name
 root=ET.parse(p).getroot()
 w,h=int(root.get('width')),int(root.get('height'))
 first=sorted((int(e.get('firstgid')),e.get('name')) for e in root.findall('tileset') if e.get('name'))
 layers=list(root.iter('layer'))
 return root,w,h,first,layers,filesha(p)
for index in notes['indices']:
 note=notes['notes'][str(index)]
 assert note['index']==index and note['new_observed']==note['certified']==0
 matches=[(key,r) for key,r in a.items() if A_SEQUENCE[key]==index]
 assert len(matches)==1,('index_lookup',index,len(matches))
 key,src=matches[0]
 assert key in occ and key in held and key in excl and key in more
 oc=occ[key];pr=held[key];prior=excl[key];mult=more[key]
 assert int(pr['index'])==int(oc['index'])==int(mult['index'])==index
 assert prior['disposition']=='excluded_from_active_review_per_latest_user_instruction'
 assert prior['previous_source_key_observed']==prior['new_observed']==prior['final_identity_certified']=='0'
 assert int(oc['actual_B_C_pixels'])==int(pr['real_B_C_pixels'])==note['expected_real_B_C_pixels']
 assert int(oc['full_context_missing_neighbor_sprites'])==0
 assert int(oc['source_full_map_5x5_clipped'])==(1 if index==298 else 0)
 assert int(mult['fresh_untried_inbounds_candidate_count_capped_3'])==(1 if index==4024 else 0)
 assert src['selection_status']=='selected_provisional'
 path=src['source_image_path']
 assert path.startswith('Tiles/') and filesha(R/path)==src['source_png_sha256']
 im=png(path)
 box=bbox(src['selected_crop_xyxy'])
 assert 0<=box[0]<box[2]<=im.width and 0<=box[1]<box[3]<=im.height
 crop=im.crop(box)
 assert sha(crop.tobytes())==src['selected_rgba_pixel_sha256'],('A_RGBA_pixel_drift',index,key)
 root,w,h,first,layers,tmx_sha=tmx(oc['original_tmx'])
 assert tmx_sha==oc['tmX_sha256']
 layer=layers[int(oc['layer'])]
 data=layer.find('data');assert data is not None and data.get('encoding')=='csv'
 vals=[int(x) for x in re.findall(r'\d+',data.text or '')]
 assert len(vals)==w*h
 x,y=int(oc['x']),int(oc['y'])
 raw_gid=vals[y*w+x]
 assert raw_gid==int(oc['tmX_raw_gid'])
 z=raw_gid&0x0fffffff
 pos=bisect.bisect_right([x[0] for x in first],z)-1
 assert pos>=0 and (first[pos][1],z-first[pos][0])==key
 lvl=layer.get('level')
 if lvl is None:
  p=layer.find("properties/property[@name='level']")
  lvl=(p.get('value') or p.text or '0') if p is not None else '0'
 assert int(lvl)==int(oc['level'])
 out.append(dict(source_index=index,tile_set_name=key[0],local_id=key[1],
  source_png=path,source_png_sha256=src['source_png_sha256'],
  source_RGBA_pixel_sha256=sha(crop.tobytes()),
  original_tmx=oc['original_tmx'],original_tmx_sha256=tmx_sha,level=int(lvl),
  layer=int(oc['layer']),x=x,y=y,raw_gid=raw_gid,
  original_B_C_pixels=int(oc['actual_B_C_pixels']),
  prior_layer_mask_diagnostic_pixels=int(oc['layer_limited_B_C_pixels']),
  clipped_at_edge=int(oc['source_full_map_5x5_clipped']),
  missing_neighbor_sprites=int(oc['full_context_missing_neighbor_sprites']),
  new_alt_candidate_known=int(mult['fresh_untried_inbounds_candidate_count_capped_3']),
  visible_A_description=note['visible_features'],candidate_family=note['part_family'],
  hold_reason=note['hold_reason'],confidence='low',
  original_v188_exclusion_preserved=1,observed=0,
  official_mapping_verified=0,tilezed_verified=0,certified=0))
 assert db.execute('SELECT count(*) FROM v188_active_review_disposition WHERE tile_set_name=? AND local_id=?',key).fetchone()==(1,)
 assert db.execute('SELECT count(*) FROM v189_held_source_reverification WHERE tile_set_name=? AND local_id=?',key).fetchone()==(0,)
assert len(out)==12 and len({(r['tile_set_name'],r['local_id']) for r in out})==12
fieldnames=list(out[0])
with (OUT/'RECHECK_12.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fieldnames);w.writeheader();w.writerows(out)
intnames={'source_index','local_id','level','layer','x','y','raw_gid','original_B_C_pixels','prior_layer_mask_diagnostic_pixels','clipped_at_edge','missing_neighbor_sprites','new_alt_candidate_known','original_v188_exclusion_preserved','observed','official_mapping_verified','tilezed_verified','certified'}
db.execute('CREATE TABLE v190_held_twelve_source_audit ('+','.join('"'+k+'" '+('INTEGER' if k in intnames else 'TEXT') for k in fieldnames)+',PRIMARY KEY(tile_set_name,local_id),CHECK(observed=0 AND certified=0 AND official_mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v190_held_twelve_source_audit ('+','.join('"'+k+'"' for k in fieldnames)+') VALUES ('+','.join('?' for _ in fieldnames)+')',[tuple(x[k] for k in fieldnames) for x in out])
db.commit()
after={n:db.execute('SELECT count(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==252 and set(after)-set(before)=={'v190_held_twelve_source_audit'}
assert all(after[n]==v for n,v in before.items()) and after['v190_held_twelve_source_audit']==12
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes()
comp=zlib.compress(newraw,8)
enc=base64.b64encode(comp).decode('ascii');parts=[]
for i in range(0,len(enc),3000000):
 p=DBOUT/f'v190.part{i//3000000:03}.b64';p.write_text(enc[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
d=dict(version='v190',parent='v189',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(comp),sqlite_bytes=len(newraw),parts=parts,
 table_count=252,prior_tables_preserved=251,new_rows=12,new_observed_rows=0,
 integrity_check='ok',official_mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=dict(version='v190',scope='one-time explicit source review of 12 previously held',
 individual_original_A_RGBA_and_PNG_SHA_verified=12,actual_source_TMX_raw_GID_verified=12,
 original_C_pixel_delta_records_cross_checked=12,
 edge_clipped=1,small_unchanged_reviewed=11,
 alternate_scene_exists_but_already_tested=1,previous_v188_exclusions_preserved=True,
 manually_described_shape_only=12,newly_provisionally_observed=0,held=12,
 checkpoint_observed=9898,checkpoint_unobserved=144,physical_held_unique=142,historical_count_gap=2,
 parent_tables_preserved=251,physical_db_tables=252,sqlite_sha256=sha(newraw),
 reviewed_indices=notes['indices'],review_csv_sha256=filesha(OUT/'RECHECK_12.csv'),
 official_mapping_verified=0,tilezed_verified=0,certified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'README.md').write_text(
 '# v190 미검증 타일 12종의 원본 A 및 실제 TMX 재검수\n\n'
 '직접 열람한 원본 A 접촉시트의 소형 조각 12종을 이전 v182 실제 TMX B-C·v183 held·v188 검수제외 및 v180 추가 장면 기록과 대조했습니다. 타일별로 보이는 모양, 후보 계열, 한계 및 원본 PNG/TMX SHA/GID/층/좌표·RGBA 픽셀 증거를 기록했으며, 기존 모호함을 감추지 않습니다. 한 원본 장면은 지도 끝이 잘렸고 다른 11종은 차이가 작으며, 4024 추가 장소도 이미 12픽셀이라 검증으로 충분하지 않습니다.\n'
 '신규 잠정 관찰+0, 기존 관찰9898/10042 (98.57%) 유지, 미관찰 기록144 (실제142+역사적 2). v188의 제외 기록을 보존하고 이번 항목을 임의로 관찰/투명/정체 인증으로 승격하지 않았습니다.\n'
 '물리 SQLite v189 251개 모든 테이블/행값 보존, 새 감사12행 1개 테이블로 v190 252개. 원본 84 TMX/Tiles PNG 및 기존 사용자 제외·수동80·held D2/JUMBO20 유지.\n',encoding='utf-8')
print('PASS v190 source-backed 12 held reviews, no false observations',json.dumps(m,ensure_ascii=False),flush=True)
