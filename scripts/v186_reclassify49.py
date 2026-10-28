#!/usr/bin/env python3
"""v186 source-backed disambiguation overlay, not a new observed/official-ID promotion.
Confirm all 49 existing original A PNG RGBA crops, original B/C same-key evidence,
and preserve every byte of all 247 parent SQLite table row values.
"""
from pathlib import Path
from collections import Counter
import hashlib,base64,csv,json,re,zlib,sqlite3
from PIL import Image
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v186_object_disambiguation_49'
DBOUT=R/'analysis/current/v186'
DBOUT.mkdir(parents=True,exist_ok=True)
def sha(x):return hashlib.sha256(x).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def rgba_box(txt):
 xy=tuple(int(x) for x in re.findall(r'\d+',txt))
 assert len(xy)==4 and 0<=xy[0]<xy[2] and 0<=xy[1]<xy[3],(txt,xy)
 return xy
def readparent(manifest):
 compressed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in manifest['parts']),validate=True)
 assert sha(compressed)==manifest['compressed_sha256']
 raw=zlib.decompress(compressed)
 assert sha(raw)==manifest['sqlite_sha256'] and len(raw)==manifest['sqlite_bytes']
 return raw
parent=json.loads((R/'analysis/current/v185/MANIFEST.json').read_text())
state=json.loads((R/'PROJECT_STATE.json').read_text())
review=json.loads((OUT/'MANUAL_REINSPECTION.json').read_text(encoding='utf-8'))
assert parent['version']=='v185' and parent['table_count']==247
assert state['latest_checkpoint']['version']=='v185'
assert state['latest_checkpoint']['expanded_unique_observed']==9898
assert state['latest_checkpoint']['expanded_unique_unobserved']==144
assert review['version']=='v186' and review['parent']=='v185'
assert review['manually_reinspected']==review['correction_count']==49
assert review['new_observed']==review['official_mapping_verified']==review['tilezed_verified']==review['final_certified']==0
notes=review['entries']
assert len(notes)==49 and len({int(x['index']) for x in notes})==49
assert len({(x['tile_set_name'],int(x['local_id'])) for x in notes})==49
assert sorted({int(x['index']) for x in notes})==sorted([*range(63,76),*range(974,995),1064,1065,1066,1067,1068,1069,1070,1078,1117,1118,1119,1120,1121,1122,1125])
A=readcsv(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
B=readcsv(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')
C=readcsv(R/'review/v121_C_diff_new4632/C_B_DIFFERENCE_4632.csv')
assert len(A)==4633 and len(B)==len(C)==4632
Bmap={(x['tile_set_name'],int(x['local_id'])):x for x in B}
Cmap={(x['tile_set_name'],int(x['local_id'])):x for x in C}
assert len(Bmap)==len(Cmap)==4632
sheet_sha={}
for path in review['source_contact_sheets']:
 p=R/path
 assert p.is_file(),path
 with Image.open(p) as im:
  im.verify()
 sheet_sha[path]=filesha(p)
assert len(sheet_sha)==12
source_cache={}
rows=[]
for n in notes:
 idx=int(n['index']);rec=A[idx]
 key=n['tile_set_name'],int(n['local_id'])
 assert (rec['tile_set_name'],int(rec['local_id']))==key,('index-key mismatch',idx,key)
 assert key in Bmap and key in Cmap,('original B/C evidence absent',idx,key)
 source=rec['source_image_path']
 assert source.startswith('Tiles/') and '..' not in source,source
 if source not in source_cache:
  p=R/source
  assert filesha(p)==rec['source_png_sha256'],('original PNG modified',source)
  with Image.open(p) as img:source_cache[source]=img.convert('RGBA').copy()
 crop=source_cache[source].crop(rgba_box(rec['selected_crop_xyxy']))
 a_hash=sha(crop.tobytes())
 assert a_hash==rec['selected_rgba_pixel_sha256'],('A RGBA mismatch',idx,key)
 assert int(n['official_mapping_verified'])==int(n['tilezed_verified'])==int(n['final_identity_certified'])==0
 assert n['orientation']==n['connections']=='unverified'
 assert n['confidence'] in ('low','medium','high')
 q=Bmap[key];v=Cmap[key]
 pix=int(v['B_minus_C_changed_pixels'])
 if idx==70:
  assert pix==0,('historical held changed',idx,pix)
  assert n['review_status']=='held_original_B_minus_C_zero'
 else:
  assert n['review_status']=='correction_overlay_no_new_observed'
 rows.append(dict(index=idx,tile_set_name=key[0],local_id=key[1],
  category=n['category'],revised_identity=n['revised_identity'],
  visible_features=n['visible_features'],distinguishing_rule=n['distinguishing_rule'],
  fuel_cylinder_status=n['fuel_cylinder_status'],
  confidence=n['confidence'],historical_B_C_pixels=pix,
  source_png=source,source_png_sha256=rec['source_png_sha256'],
  source_RGBA_crop_SHA256=a_hash,original_TMX=q['tmx_file'],
  original_level=int(q['source_level']),original_layer=int(q['source_layer_index']),
  original_x=int(q['source_x']),original_y=int(q['source_y']),
  original_raw_gid=int(q['source_raw_gid']),
  original_B_contact=n['source_B_contact'],
  original_C_diff_contact=n['source_C_diff_contact'],
  original_A_contact=n['source_A_contact'],
  status=n['review_status'],new_observed=0,
  mapping_verified=0,tilezed_verified=0,certified=0))
assert len(rows)==49 and len(source_cache)==6,('source atlases',list(source_cache))
with (OUT/'RECLASSIFIED_49.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (OUT/'SOURCE_SHEET_SHA256.json').open('w',encoding='utf-8') as f:
 json.dump(sheet_sha,f,ensure_ascii=False,indent=2)
# Add a review/errata overlay ONLY, while preserving all existing historical records.
praw=readparent(parent)
tmp=Path('/tmp/pz-v186-disambiguation.sqlite');tmp.write_bytes(praw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={r[0]:db.execute('SELECT COUNT(*) FROM "'+r[0]+'"').fetchone()[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==247 and before['v185_visual_review']==1
keys=list(rows[0]);textfields=[x for x in keys if x not in ('index','local_id','historical_B_C_pixels','original_level','original_layer','original_x','original_y','original_raw_gid','new_observed','mapping_verified','tilezed_verified','certified')]
types={k:('TEXT' if k in textfields else 'INTEGER') for k in keys}
db.execute('CREATE TABLE v186_object_reclassification ('+','.join('"'+k+'" '+types[k] for k in keys)+',PRIMARY KEY(tile_set_name,local_id),CHECK(new_observed=0 AND mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
db.executemany('INSERT INTO v186_object_reclassification ('+','.join('"'+k+'"' for k in keys)+') VALUES ('+','.join('?' for _ in keys)+')',[tuple(r[k] for k in keys) for r in rows])
db.commit()
after={r[0]:db.execute('SELECT COUNT(*) FROM "'+r[0]+'"').fetchone()[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==248 and set(after)-set(before)=={'v186_object_reclassification'}
assert all(after[k]==v for k,v in before.items()) and after['v186_object_reclassification']==49
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
raw=tmp.read_bytes();compressed=zlib.compress(raw,8)
enc=base64.b64encode(compressed).decode('ascii');parts=[]
for i in range(0,len(enc),3000000):
 p=DBOUT/f'v186.part{i//3000000:03}.b64'
 p.write_text(enc[i:i+3000000],encoding='ascii')
 parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/x).read_text('ascii') for x in parts))))==sha(raw)
dbm=dict(version='v186',parent='v185',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(raw),compressed_sha256=sha(compressed),sqlite_bytes=len(raw),
 parts=parts,table_count=248,prior_tables_preserved=247,
 new_rows=49,new_observed_rows=0,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
m=dict(version='v186',parent='v185',manually_reviewed_existing_objects=49,
 source_png_atlases_verified=6,source_A_rgba_crops_verified=49,
 original_B_C_evidence_keys_verified=49,source_contact_sheet_sha_verified=12,
 reclassification_rows=49,previous_B_C_zero_held_preserved=[70],
 new_image_observations=0,observed_before=9898,observed_after=9898,
 checkpoint_remaining=144,physical_parent_tables_preserved=247,
 database_tables=248,sqlite_sha256=sha(raw),
 correction_csv_sha256=filesha(OUT/'RECLASSIFIED_49.csv'),
 source_sheets_sha256=sheet_sha, category_counts=dict(Counter(n['category'] for n in notes)),
 mapping_verified=0,tilezed_verified=0,certified=0)
(OUT/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v186 기존 오류 분류 정정: 바비큐/프로판통 유사부품, 소파/의자, 산업 동력기계와 작업대 49종\n\n'
 '원본 A000/012/013/014, 원래 TMX B 000/012/013/014와 한 raw GID 제거 C 차이 000/012/013/014를 직접 재검수했다. 모든 49개의 원본 A PNG 파일 SHA256·실제 크롭 RGBA SHA256와 기존 B/C 키·근거를 재검증한 정정 오버레이다.\n'
 '바비큐 그릴의 수평 조리통·다리·별도 붉은/주황 실린더 유사 부품, 좌석의 두꺼운 좌면·등받이·팔걸이, 공작기계 모터·구동축·작업 헤드, 작업대 상판·받침, 독립 소화기형 실린더를 명확히 구분한다. 실제 프로판 내용물/연결 여부는 공식 자료 없이 확정하지 않는다.\n'
 '기존 조리기기와 가스 그릴도 혼동하지 않고, 목재 식탁 의자·쿠션 스툴·소파 모듈을 모두 완성된 소파로 분류하지 않는다. 기계 작업대·금속 보관통과 진짜 동력 공작기계도 구분한다.\n'
 '정정은 기존 보존 DB를 덮어쓰지 않고 v186 248번째 테이블의 별도 판정 오버레이 49행에 추가한다. 기존 v185 247테이블 전체 행값·행수, 사용자 검수80·제외14·D2/JUMBO20 및 원본 84 TMX/Tiles PNG 불변.\n'
 '이번 재검수는 신규 타일 관찰 카운트에 추가하지 않는다. 기존 관찰 9,898/10,042(98.57%), 기록상 미관찰 144, 정체 최종/공식 Local ID/TileZed 인증 0. 원래 B-C가 0인 70번은 계속 held.\n',encoding='utf-8')
print('PASS v186 original PNG/TMX B-C audit 49 reclassified, zero newly observed, SQLite 248 tables',sha(raw),flush=True)
