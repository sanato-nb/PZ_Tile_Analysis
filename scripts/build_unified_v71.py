#!/usr/bin/env python3
"""v70 물리 DB 복사 + v71 실제 시각 판독 20종 결합. 원본/기존 테이블 불변 보존."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v70/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
    assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==3285
    assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==2817
with (ROOT/'checkpoints/v71/observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==20
assert sum(r['review_status']=='candidate' for r in rows)==18
assert sum(r['review_status']=='held' for r in rows)==2
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v71_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
    c.execute('pragma journal_mode=DELETE')
    for col in ('v71_observed','v71_candidate_auditable'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
    for col in ('v71_review_status','v71_identity_candidate','v71_observed_features'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
    cols=list(rows[0])
    ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
          'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
    c.execute('CREATE TABLE v71_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        k=(r['tile_set_locator'],int(r['local_id']))
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
        assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
        cand=int(r['review_status']=='candidate')
        c.execute('INSERT INTO v71_visual_review VALUES('+','.join('?' for _ in cols)+')',
                  [int(r[x]) if x in ints else r[x] for x in cols])
        c.execute("""UPDATE tile_catalog SET observed_any=1,v71_observed=1,
                  provisional_candidate_any_auditable=?,v71_candidate_auditable=?,v71_review_status=?,
                  v71_identity_candidate=?,v71_observed_features=?,current_candidate=?,current_review_version='v71'
                  WHERE tile_set_locator=? AND local_id=?""",
                  (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
    c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
        ('v71_new_observed',20,'A/B/C/D visually inspected and recorded'),
        ('v71_new_candidates',18,'provisional, not certified'),
        ('v71_new_held',2,'Occluded tiles held without identity'),
        ('v71_total_observed',3305,'v70 3285 + 20 non-overlapping'),
        ('v71_unobserved',2104,'5409 - 3305'),
        ('v71_candidate_auditable',2835,'2817 + 18')])
    c.commit()
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
    checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
                observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
                candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
                remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
                v71review=c.execute('select count(*) from v71_visual_review').fetchone()[0],
                final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=3305,candidate=2835,remaining=2104,v71review=20,final=0),checks
    c.execute('VACUUM')
out=ROOT/'analysis/current/v71'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes()
packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v71/v71.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n','ascii')
    parts.append(rel)
manifest=dict(version='v71',sqlite_file='tile_visual_v71_unified.sqlite',
    sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
    compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
    base_version='v70',base_sqlite_sha256=prior['sqlite_sha256'],
    new_records_repo_path='checkpoints/v71/observations.tsv',
    evidence_manifest='checkpoints/v71_preview/EVIDENCE_MANIFEST.json',
    source_record_count=20,observed=3305,provisional_candidates=2835,remaining=2104,
    certified=0,all_prior_tables_preserved=True,
    original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
    note='A/B/C/D 원본 증거의 20종 직접 시각 판독. 잠정 후보 18 보류 2. PNG height mismatch/TileZed 미검증.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert s['unified_database']['version']=='v70' and s['unified_database']['observed_unique']==3285
s['latest_checkpoint']=dict(version='v71',date='2026-10-26',baseline_reconciliation='v70',
    baseline_unique_observed=3285,new_unique_observed=20,new_provisional_candidates=18,new_held=2,
    overlap_with_prior=0,merged_unique_observed=3305,merged_observation_percent=round(3305/5409*100,4),
    remaining_unobserved=2104,auditable_provisional_candidate_keys=2835,approved_final_certifications=0,
    delta_repo_path='checkpoints/v71/observations.tsv',evidence_repo_path='checkpoints/v71_preview/',
    verification_script='checkpoints/v71/verify_delta.py',png_tmx_mapping_verified=0,
    tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v71',status='VERIFIED',
    repo_manifest='analysis/current/v71/MANIFEST.json',restore_script='scripts/restore_unified_v71.py',
    observed_unique=3305,observed_percent=round(3305/5409*100,4),remaining_unobserved=2104,
    auditable_candidates=2835,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
    complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
    v71_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
    'v71 통합 DB의 미관찰 2,124종을 PNG·TMX A/B/C/D 직접 관찰로 이어간다.',
    'v71 보류 2종은 가림 및 선택 배치 기여를 다른 위치에서 재검수한다.',
    'v70 이하 보류 기록과 PNG 물리 높이 불일치·TileZed 정합을 독립 검증한다.',
    '사용자 수동 검수 80종 및 재검수 자료는 별도 계보로 보존하고 자동 합산하지 않는다.',
    'v70 이하 원본 SQLite·체크포인트·원본 PNG·TMX·충돌 기록을 삭제하거나 덮어쓰지 않는다.',
    'v71 신규 20종 A/B/C/D+비교판 100장 JPEG를 checkpoints/v71_preview/에 보관한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS BUILD v71',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
