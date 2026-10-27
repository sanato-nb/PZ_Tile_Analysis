#!/usr/bin/env python3
"""v122: append 160 visually reviewed A/B/C/D new-key records to historical v121 SQLite without altering prior tables."""
from pathlib import Path
import csv, json, hashlib, base64, zlib, sqlite3, zipfile
R=Path(__file__).resolve().parents[1]
O=R/'review/v122_AI_ABCD_160'
D=R/'analysis/current/v122'
O.mkdir(exist_ok=True,parents=True)
D.mkdir(exist_ok=True,parents=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def readcsv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
revfile=O/'AI_VISUAL_REVIEW_160.csv'
reviews=readcsv(revfile)
original=readcsv(R/'review/v121_ABCD_first160/ABCD_160.csv')
assert len(reviews)==len(original)==160
for i,(r,p) in enumerate(zip(reviews,original)):
    assert int(r['index'])==i and (r['tile_set_name'],r['local_id'])==(p['tile_set_name'],p['local_id'])
    assert r['tmx_file']==p['tmx_file'] and r['source_raw_gid']==p['raw_gid']
    assert r['b_c_changed_pixels']==p['b_c_changed_pixels']
    assert r['visual_observed']=='1'
    assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
    assert r['review_status'] in ('held','provisional_candidate')
assert len(set((r['tile_set_name'],r['local_id']) for r in reviews))==160
assert sum(r['review_status']=='provisional_candidate' for r in reviews)==144
assert sum(r['review_status']=='held' for r in reviews)==16
assert sum(int(r['b_c_changed_pixels'])==0 for r in reviews)==9
for r in reviews:
    if int(r['b_c_changed_pixels'])==0:assert r['review_status']=='held'
m=json.loads((R/'analysis/current/v121/MANIFEST.json').read_text('utf8'))
encoded=''.join((R/s).read_text('ascii').strip() for s in m['parts'])
compressed=base64.b64decode(encoded,validate=True)
assert sha(compressed)==m['compressed_sha256']
raw=zlib.decompress(compressed)
assert len(raw)==m['sqlite_bytes'] and sha(raw)==m['sqlite_sha256']
db=Path('/tmp/pz_v122.sqlite');db.write_bytes(raw)
with sqlite3.connect(db) as c:
    before={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(before)==183 and 'v121_abcd_evidence' in before
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert c.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0]==4512
    assert c.execute('SELECT count(*) FROM v115_ai_candidate_queue').fetchone()[0]==882
    assert c.execute('SELECT count(*) FROM v116_user_excluded_missing_image').fetchone()[0]==6
    assert c.execute('SELECT count(*) FROM v121_abcd_evidence').fetchone()[0]==160
    c.execute("""CREATE TABLE v122_ai_visual_review_160(
      tile_set_name TEXT NOT NULL,local_id INTEGER NOT NULL, original_index INTEGER NOT NULL,
      observed_features TEXT, identity_candidate TEXT,part_role TEXT,confidence TEXT,
      review_status TEXT, visual_observed INTEGER,evidence_sheet TEXT,source_tmx TEXT,
      source_level INTEGER,source_x INTEGER,source_y INTEGER,source_raw_gid INTEGER,
      b_c_changed_pixels INTEGER,d_status TEXT,note TEXT,mapping_verified INTEGER DEFAULT 0,
      tilezed_verified INTEGER DEFAULT 0,final_certified INTEGER DEFAULT 0,
      PRIMARY KEY(tile_set_name,local_id))""")
    placeholders=','.join('?' for _ in range(21))
    c.executemany('INSERT INTO v122_ai_visual_review_160 VALUES ('+placeholders+')',[
      (r['tile_set_name'],int(r['local_id']),int(r['index']),r['observed_features'],
       r['identity_candidate'],r['part_role'],r['confidence'],r['review_status'],1,
       r['source_sheet'],r['tmx_file'],int(r['source_level']),int(r['source_x']),
       int(r['source_y']),int(r['source_raw_gid']),int(r['b_c_changed_pixels']),
       r['d_status'],r['note'],0,0,0) for r in reviews])
    assert c.execute('SELECT count(*) FROM v122_ai_visual_review_160').fetchone()[0]==160
    assert c.execute("SELECT count(*) FROM v122_ai_visual_review_160 WHERE review_status='provisional_candidate'").fetchone()[0]==144
    assert c.execute("SELECT count(*) FROM v122_ai_visual_review_160 WHERE review_status='held'").fetchone()[0]==16
    assert c.execute('SELECT sum(mapping_verified),sum(tilezed_verified),sum(final_certified) FROM v122_ai_visual_review_160').fetchone()==(0,0,0)
    after={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert after-before=={'v122_ai_visual_review_160'} and before<=after
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    c.commit()
newraw=db.read_bytes()
z=zlib.compress(newraw,level=8)
encoded=base64.b64encode(z).decode('ascii')
parts=[]
for start in range(0,len(encoded),3000000):
    path=D/f'v122.part{start//3000000:03}.b64'
    path.write_text(encoded[start:start+3000000],'ascii')
    parts.append(path.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbmeta={'version':'v122','parent':'v121','parent_sqlite_sha256':m['sqlite_sha256'],
 'sqlite_size_bytes':len(newraw),'sqlite_sha256':sha(newraw),
 'compressed_sha256':sha(z),'parts':parts,'prior_tables_preserved':183,
 'review_table':'v122_ai_visual_review_160','new_visually_observed':160,
 'candidate':144,'held':16,'final_certified':0,'integrity_check':'ok'}
(D/'MANIFEST.json').write_text(json.dumps(dbmeta,ensure_ascii=False,indent=2)+'\n','utf8')
report='''# v122 직접 시각 검수 — 신규 160종
검토한 원본 이미지: v121 4장 접촉시트, 각 A 원본, B TMX 5×5, C 한 개 GID 제거, D 실제 두 번째 위치(있을 경우).
신규 160종을 모델이 직접 관찰했고 잠정 계열/부품 후보 144종, 보류 16종을 별도 필드로 기록했다.
D 106종, D 없음 54종, B−C 변화 0인 9종은 보류한다. 계열 후보는 공식 식별이 아니다.
기존 5,409종(관찰 5,400종)은 수정하지 않았다. 신규 4,633종 중 직접 관찰 160종/미관찰 4,473종.
확장 10,042종 중 누적 이미지 관찰 5,560종(55.37%), 미관찰 4,482종(기존 9+신규 4,473).
기존 4,512종 감사 후보, v115 별도 882종 후보, 과거 수동 검수 80종도 불변.
공식 PNG−TMX 매핑, TileZed, 최종 정체 인증 모두 0종.
시각 관찰 근거와 정체 후보는 AI_VISUAL_REVIEW_160.csv에 분리 기록. 
'''
(O/'REPORT.md').write_text(report,'utf8')
assets=[revfile,O/'REPORT.md',R/'review/v121_ABCD_first160/ABCD_160.csv',
 R/'review/v121_ABCD_first160/ABCD_160_embedded.html']+sorted((R/'review/v121_ABCD_first160').glob('ABCD_sheet_*.jpg'))
assert len(assets)==8
archive=O/'V122_AI_ABCD160_EVIDENCE.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as zz:
    for p in assets:zz.write(p,p.name)
with zipfile.ZipFile(archive) as zz:
    assert zz.testzip() is None and len(zz.namelist())==8 and len(set(zz.namelist()))==8
manifest={'version':'v122','source':'v121_ABCD_first160','visually_observed_new':160,
  'provisional_candidate':144,'held':16,'D_second_location':106,
  'D_unavailable':54,'B_C_zero_held':9,'prior_observed_5409':5400,
  'expanded_unique':10042,'expanded_observed':5560,'expanded_unobserved':4482,
  'new_4633_unobserved':4473,'final_certified':0,'mapping_verified':0,'tilezed_verified':0,
  'review_csv_sha256':sha(revfile.read_bytes()),'zip_sha256':sha(archive.read_bytes()),
  'zip_crc':'PASS','sqlite_sha256':sha(newraw),'sqlite_integrity':'ok',
  'images_embedded_HTML':'review/v121_ABCD_first160/ABCD_160_embedded.html'}
(O/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v122',json.dumps(manifest,ensure_ascii=False),flush=True)
