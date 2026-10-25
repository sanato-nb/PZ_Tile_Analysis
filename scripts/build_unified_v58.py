#!/usr/bin/env python3
"""기존 v57 SQLite를 보존하며 실제 A/B/C/D 검수 6종을 추가한 v58 통합 DB 생성."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
m=json.loads((ROOT/'analysis/current/v57/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==m['sqlite_sha256']
with sqlite3.connect(src) as c:
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==2994
 assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==2596
 old_tables={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
with (ROOT/'checkpoints/v58/observations.tsv').open(encoding='utf8',newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==len({(r['tile_set_locator'],int(r['local_id'])) for r in rows})==6
assert sum(r['review_status']=='candidate' for r in rows)==5
assert sum(r['review_status']=='held' for r in rows)==1
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v58_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as before,sqlite3.connect(dst) as c:before.backup(c)
with sqlite3.connect(dst) as c:
 c.execute('PRAGMA journal_mode=DELETE')
 for field in ('v58_observed','v58_candidate_auditable'):
  c.execute(f'ALTER TABLE tile_catalog ADD COLUMN {field} INTEGER NOT NULL DEFAULT 0')
 for field in ('v58_review_status','v58_identity_candidate','v58_observed_features'):
  c.execute(f'ALTER TABLE tile_catalog ADD COLUMN {field} TEXT')
 cols=list(rows[0])
 numerics={'local_id','level','x','y','other_level','other_x','other_y',
           'visible_pixel_delta','missing_png_neighbors','png_height_mismatch',
           'mapping_verified','tilezed_verified','final_certified'}
 schema=','.join('"'+x+'" '+('INTEGER' if x in numerics else 'TEXT') for x in cols)
 c.execute('CREATE TABLE v58_visual_review('+schema+',PRIMARY KEY(tile_set_locator,local_id))')
 sql='INSERT INTO v58_visual_review VALUES('+','.join('?' for _ in cols)+')'
 for r in rows:
  key=(r['tile_set_locator'],int(r['local_id']))
  prev=c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',key).fetchone()
  assert prev==(0,),f'Overlap/unknown key: {key}, {prev}'
  c.execute(sql,[int(r[x]) if x in numerics else r[x] for x in cols])
  candidate=int(r['review_status']=='candidate')
  c.execute("""UPDATE tile_catalog SET observed_any=1,v58_observed=1,
       provisional_candidate_any_auditable=?,v58_candidate_auditable=?,v58_review_status=?,
       v58_identity_candidate=?,v58_observed_features=?,current_candidate=?,current_review_version='v58'
       WHERE tile_set_locator=? AND local_id=?""",
       (candidate,candidate,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*key))
 progress=[('v58_new_observed',6,'direct A/B/C/D reviewed'),
           ('v58_new_candidates',5,'provisional only'),
           ('v58_new_held',1,'part role and occlusion unresolved'),
           ('v58_total_observed',3000,'2994 + 6, no overlap'),
           ('v58_unobserved',2409,'5409-3000'),
           ('v58_candidate_auditable',2601,'2596+5')]
 c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',progress)
 c.commit()
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 new_tables={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
 assert old_tables.issubset(new_tables),old_tables-new_tables
 checks={'all':c.execute('select count(*) from tile_catalog').fetchone()[0],
         'observed':c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
         'candidate':c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
         'remaining':c.execute('select count(*) from analysis_queue').fetchone()[0],
         'v58review':c.execute('select count(*) from v58_visual_review').fetchone()[0],
         'final':c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0]}
 assert checks=={'all':5409,'observed':3000,'candidate':2601,'remaining':2409,'v58review':6,'final':0},checks
 c.execute('VACUUM')
out=ROOT/'analysis/current/v58'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f'analysis/current/v58/v58.part{i//3000000:03}.b64'
 (ROOT/rel).write_text(encoded[i:i+3000000]+'\n','ascii')
 parts.append(rel)
manifest={'version':'v58','sqlite_file':'tile_visual_v58_unified.sqlite',
 'sqlite_size_bytes':len(raw),'sqlite_sha256':hashlib.sha256(raw).hexdigest(),
 'compressed_sha256':hashlib.sha256(packed).hexdigest(),'compression':'zlib_base64',
 'parts':parts,'base_version':'v57','base_sqlite_sha256':m['sqlite_sha256'],
 'new_records_repo_path':'checkpoints/v58/observations.tsv',
 'evidence_manifest':'checkpoints/v58_preview/EVIDENCE_MANIFEST.json',
 'source_record_count':6,'observed':3000,'provisional_candidates':2601,
 'remaining':2409,'certified':0,'all_prior_tables_preserved':True,
 'original_sprite_evidence_images_in_github':True,
 'mapping_verified':0,'tilezed_verified':0,
 'note':'6개 신규 타일의 원본 PNG A와 근사 TMX B/C/D JPEG가 저장소의 v58_preview에 보존됨. PNG height mismatch, 매핑·TileZed 인증 0.'}
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json';s=json.loads(statepath.read_text('utf8'))
assert s['unified_database']['version']=='v57' and s['unified_database']['observed_unique']==2994
s['latest_checkpoint']={'version':'v58','date':'2026-10-25','baseline_reconciliation':'v57',
 'baseline_unique_observed':2994,'new_unique_observed':6,'new_provisional_candidates':5,
 'new_held':1,'overlap_with_prior':0,'merged_unique_observed':3000,
 'merged_observation_percent':round(3000/5409*100,4),'remaining_unobserved':2409,
 'auditable_provisional_candidate_keys':2601,'approved_final_certifications':0,
 'delta_repo_path':'checkpoints/v58/observations.tsv',
 'evidence_repo_path':'checkpoints/v58_preview/',
 'verification_script':'checkpoints/v58/verify_delta.py',
 'png_tmx_mapping_verified':0,'tilezed_verified':0,
 'high_resolution_evidence_images_in_github':True}
s['unified_database']={'version':'v58','status':'VERIFIED',
 'repo_manifest':'analysis/current/v58/MANIFEST.json',
 'restore_script':'scripts/restore_unified_v58.py','observed_unique':3000,
 'observed_percent':round(3000/5409*100,4),'remaining_unobserved':2409,
 'auditable_candidates':2601,'certified':0,'sqlite_sha256':manifest['sqlite_sha256'],
 'complete_v36_tables':True,'complete_v46_tables':True,
 'all_prior_tables_preserved':True,'v58_git_checkpoint_integrated':True,
 'image_binaries_in_github':True}
s['next_actions']=[
 'v58 통합 DB의 미관찰 2,409종을 원본 PNG·TMX A/B/C/D로 직접 검수한다.',
 'v58 보류 1종(appliances_com_01/82)은 안테나의 타일 분할·지붕 가림·Local ID를 재검증한다.',
 'appliances_com_01 원본 PNG 높이 7,680px와 TMX 명시 높이 2,688px의 차이를 검증하고 TileZed 정합 확인 전 인증 0을 유지한다.',
 '사용자 수동 검수 80종과 재검수 원본은 별도 계보로 보존하고 자동 합산하지 않는다.',
 'v57 이하 모든 원본 SQLite·체크포인트 및 기존 PNG·TMX를 삭제하거나 덮어쓰지 않는다.',
 'v58 A/B/C/D JPEG 6종 및 원본 출처 SHA-256은 checkpoints/v58_preview/에 저장했다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('BUILT v58',checks,'SHA256',manifest['sqlite_sha256'],'parts',len(parts))
