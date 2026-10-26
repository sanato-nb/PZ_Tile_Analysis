#!/usr/bin/env python3
"""v110 full SQLite physical copy + 30 v111 directly viewed A/B/C/D records; mapping provisional."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v110/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
 assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
 assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==5388
 assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==4500
with (ROOT/'checkpoints/v111/observations.tsv').open(encoding='utf8',newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==12
assert sum(r['review_status']=='candidate' for r in rows)==12
assert sum(r['review_status']=='held' for r in rows)==0
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v111_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
 c.execute('pragma journal_mode=DELETE')
 for col in ('v111_observed','v111_candidate_auditable'):
  c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
 for col in ('v111_review_status','v111_identity_candidate','v111_observed_features'):
  c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
 cols=list(rows[0])
 ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
       'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
 c.execute('CREATE TABLE v111_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
 for r in rows:
  k=(r['tile_set_locator'],int(r['local_id']))
  assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
  assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
  cand=int(r['review_status']=='candidate')
  c.execute('INSERT INTO v111_visual_review VALUES('+','.join('?' for _ in cols)+')',
            [int(r[x]) if x in ints else r[x] for x in cols])
  c.execute("""UPDATE tile_catalog SET observed_any=1,v111_observed=1,
             provisional_candidate_any_auditable=?,v111_candidate_auditable=?,v111_review_status=?,
             v111_identity_candidate=?,v111_observed_features=?,current_candidate=?,current_review_version='v111'
             WHERE tile_set_locator=? AND local_id=?""",
             (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
 with (ROOT/'checkpoints/v111/unresolved_9.csv').open(encoding='utf-8-sig',newline='') as f:
  held_rows=list(csv.DictReader(f))
 assert len(held_rows)==9
 c.execute('CREATE TABLE v111_unresolved_queue_audit(tile_set_locator TEXT,local_id INTEGER, status TEXT,reason TEXT, observed_features TEXT,PRIMARY KEY(tile_set_locator,local_id))')
 for h in held_rows:
  key=(h['tile_set_locator'],int(h['local_id']))
  assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',key).fetchone()==(0,)
  c.execute('INSERT INTO v111_unresolved_queue_audit VALUES (?,?,?,?,?)',(key[0],key[1],h['status'],h['reason'],h['observed_features']))
 c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
  ('v111_new_observed',12,'Single-use actual A/B/C visual differences; D unavailable and provisional TileZed text grid'),
  ('v111_new_candidates',12,'provisional low, not certified'),
  ('v111_new_held',0,'4 blank and 5 missing remain unobserved in separate v111_unresolved_queue_audit'),
  ('v111_total_observed',5400,'v110 5388 + 12 non-overlapping'),
  ('v111_unobserved',9,'5409 - 5400'),
  ('v111_candidate_auditable',4512,'4500 + 12')])
 c.commit()
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
 checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
             observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
             candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
             remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
             v111review=c.execute('select count(*) from v111_visual_review').fetchone()[0],
             final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
 assert checks==dict(all=5409,observed=5400,candidate=4512,remaining=9,v111review=12,final=0),checks
 c.execute('VACUUM')
out=ROOT/'analysis/current/v111'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f'analysis/current/v111/v111.part{i//3000000:03}.b64'
 (ROOT/rel).write_text(encoded[i:i+3000000]+chr(10),'ascii')
 parts.append(rel)
manifest=dict(version='v111',sqlite_file='tile_visual_v111_unified.sqlite',
 sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
 compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
 base_version='v110',base_sqlite_sha256=prior['sqlite_sha256'],
 new_records_repo_path='checkpoints/v111/observations.tsv',
 unresolved_repo_path='checkpoints/v111/unresolved_9.csv',
 evidence_manifest='checkpoints/v111_singleuse_preview/EVIDENCE_MANIFEST.json',
 source_record_count=12,observed=5400,provisional_candidates=4512,remaining=9,unresolved_source_and_no_delta=9,
 certified=0,all_prior_tables_preserved=True,
 original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
 note='v110 미관찰 21종 중 단일 사용 PNG A와 TMX B/C 차이가 있는 12종 잠정 후보, B-C 0인 4종과 PNG 누락 5종은 미관찰로 유지. D 미확보, 공식 TileZed 검증 0.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=0)+chr(10),'utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert (s['unified_database']['version'],s['unified_database']['observed_unique']) in {('v110',5388),('v111',5400)}
s['latest_checkpoint']=dict(version='v111',date='2026-10-26',baseline_reconciliation='v110',
 baseline_unique_observed=5388,new_unique_observed=12,new_provisional_candidates=12,new_held=0,
 overlap_with_prior=0,merged_unique_observed=5400,merged_observation_percent=round(5400/5409*100,4),
 remaining_unobserved=9,auditable_provisional_candidate_keys=4512,approved_final_certifications=0,
 delta_repo_path='checkpoints/v111/observations.tsv',evidence_repo_path='checkpoints/v111_singleuse_preview/',
 verification_script='checkpoints/v111/verify_delta.py',png_tmx_mapping_verified=0,
 tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v111',status='VERIFIED',
 repo_manifest='analysis/current/v111/MANIFEST.json',restore_script='scripts/restore_unified_v111.py',
 observed_unique=5400,observed_percent=round(5400/5409*100,4),remaining_unobserved=9,
 auditable_candidates=4512,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
 complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
 v111_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
 'v111에서 남은 9종: 원본 PNG 누락 5종과 B-C 제거 차이 0인 사무실·관목 4종을 우선 확인한다.',
 '단일 배치인 12종의 PNG A 및 B-C 차이를 시각 검수했지만 D 미확보·TileZed 텍스트 격자 잠정 매핑이므로 공식 인증 0.',
 'missing PNG 5종의 원본 아틀라스를 확보하고 공식 TileZed Local ID 그리드 대응을 검증한다.',
 'v36~v110 물리 SQLite 전체 테이블과 사용자 수동 검수 80종을 보존한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=0)+chr(10),'utf8')
print('PASS BUILD v111',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
