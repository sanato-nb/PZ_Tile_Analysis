#!/usr/bin/env python3
"""v109 full SQLite physical copy + 30 v110 directly viewed A/B/C/D records; mapping provisional."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v109/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
 assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
 assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==5358
 assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==4475
with (ROOT/'checkpoints/v110/observations.tsv').open(encoding='utf8',newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==30
assert sum(r['review_status']=='candidate' for r in rows)==25
assert sum(r['review_status']=='held' for r in rows)==5
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v110_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
 c.execute('pragma journal_mode=DELETE')
 for col in ('v110_observed','v110_candidate_auditable'):
  c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
 for col in ('v110_review_status','v110_identity_candidate','v110_observed_features'):
  c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
 cols=list(rows[0])
 ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
       'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
 c.execute('CREATE TABLE v110_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
 for r in rows:
  k=(r['tile_set_locator'],int(r['local_id']))
  assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
  assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
  cand=int(r['review_status']=='candidate')
  c.execute('INSERT INTO v110_visual_review VALUES('+','.join('?' for _ in cols)+')',
            [int(r[x]) if x in ints else r[x] for x in cols])
  c.execute("""UPDATE tile_catalog SET observed_any=1,v110_observed=1,
             provisional_candidate_any_auditable=?,v110_candidate_auditable=?,v110_review_status=?,
             v110_identity_candidate=?,v110_observed_features=?,current_candidate=?,current_review_version='v110'
             WHERE tile_set_locator=? AND local_id=?""",
             (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
 c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
  ('v110_new_observed',30,'Original A/B/C/D with actual D; provisional TileZed text grid'),
  ('v110_new_candidates',25,'provisional low, not certified'),
  ('v110_new_held',5,'ambiguous small vegetation or wall cracks'),
  ('v110_total_observed',5388,'v109 5358 + 30 non-overlapping'),
  ('v110_unobserved',21,'5409 - 5388'),
  ('v110_candidate_auditable',4500,'4475 + 25')])
 c.commit()
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
 checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
             observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
             candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
             remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
             v110review=c.execute('select count(*) from v110_visual_review').fetchone()[0],
             final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
 assert checks==dict(all=5409,observed=5388,candidate=4500,remaining=21,v110review=30,final=0),checks
 c.execute('VACUUM')
out=ROOT/'analysis/current/v110'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
 rel=f'analysis/current/v110/v110.part{i//3000000:03}.b64'
 (ROOT/rel).write_text(encoded[i:i+3000000]+chr(10),'ascii')
 parts.append(rel)
manifest=dict(version='v110',sqlite_file='tile_visual_v110_unified.sqlite',
 sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
 compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
 base_version='v109',base_sqlite_sha256=prior['sqlite_sha256'],
 new_records_repo_path='checkpoints/v110/observations.tsv',
 evidence_manifest='checkpoints/v110_tiledef_preview/EVIDENCE_MANIFEST.json',
 source_record_count=30,observed=5388,provisional_candidates=4500,remaining=21,
 certified=0,all_prior_tables_preserved=True,
 original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
 note='v109 미관찰 30종 A/B/C/D와 실제 D 30종(원거리 28, 근접 2). TileZed 타일정의 텍스트 격자 잠정 크롭, 공식 Local ID 미검증. 후보 25 보류 5 인증 0.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=0)+chr(10),'utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert (s['unified_database']['version'],s['unified_database']['observed_unique']) in {('v109',5358),('v110',5388)}
s['latest_checkpoint']=dict(version='v110',date='2026-10-26',baseline_reconciliation='v109',
 baseline_unique_observed=5358,new_unique_observed=30,new_provisional_candidates=25,new_held=5,
 overlap_with_prior=0,merged_unique_observed=5388,merged_observation_percent=round(5388/5409*100,4),
 remaining_unobserved=21,auditable_provisional_candidate_keys=4500,approved_final_certifications=0,
 delta_repo_path='checkpoints/v110/observations.tsv',evidence_repo_path='checkpoints/v110_tiledef_preview/',
 verification_script='checkpoints/v110/verify_delta.py',png_tmx_mapping_verified=0,
 tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v110',status='VERIFIED',
 repo_manifest='analysis/current/v110/MANIFEST.json',restore_script='scripts/restore_unified_v110.py',
 observed_unique=5388,observed_percent=round(5388/5409*100,4),remaining_unobserved=21,
 auditable_candidates=4500,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
 complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
 v110_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
 'v110 통합 DB 미관찰 21종에서 실제 다른 D와 원본 PNG 대응을 우선 확인한다.',
 'v110 30종은 TileZed 타일정의 텍스트 격자에 따른 잠정 Local ID 크롭이므로 공식 TileZed 렌더와 재대조한다.',
 'v110 미확보 원본 PNG 2종(e_cockspurhawthornJUMBO_1/1, jumbo_tree_01/0)은 별도 소스 검색이 필요하다.',
 'v110 보류 5종은 작은 식생·균열로 역할 불명확하므로 확대·공식 정합 검증을 우선한다.',
 '기존 모든 원본 DB·체크포인트·사용자 수동 검수 80종 및 재검수 계보를 보존한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=0)+chr(10),'utf8')
print('PASS BUILD v110',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
