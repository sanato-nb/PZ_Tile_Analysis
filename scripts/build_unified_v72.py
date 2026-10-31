#!/usr/bin/env python3
"""v71 물리 DB 복사 + v72 실제 시각 판독 20종 결합. 원본/기존 테이블 불변 보존."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v71/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
    assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==3305
    assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==2835
with (ROOT/'checkpoints/v72/observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==20
assert sum(r['review_status']=='candidate' for r in rows)==20
assert sum(r['review_status']=='held' for r in rows)==0
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v72_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
    c.execute('pragma journal_mode=DELETE')
    for col in ('v72_observed','v72_candidate_auditable'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
    for col in ('v72_review_status','v72_identity_candidate','v72_observed_features'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
    cols=list(rows[0])
    ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
          'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
    c.execute('CREATE TABLE v72_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        k=(r['tile_set_locator'],int(r['local_id']))
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
        assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
        cand=int(r['review_status']=='candidate')
        c.execute('INSERT INTO v72_visual_review VALUES('+','.join('?' for _ in cols)+')',
                  [int(r[x]) if x in ints else r[x] for x in cols])
        c.execute("""UPDATE tile_catalog SET observed_any=1,v72_observed=1,
                  provisional_candidate_any_auditable=?,v72_candidate_auditable=?,v72_review_status=?,
                  v72_identity_candidate=?,v72_observed_features=?,current_candidate=?,current_review_version='v72'
                  WHERE tile_set_locator=? AND local_id=?""",
                  (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
    c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
        ('v72_new_observed',20,'A/B/C/D visually inspected and recorded'),
        ('v72_new_candidates',20,'provisional, not certified'),
        ('v72_new_held',0,'Occluded tiles held without identity'),
        ('v72_total_observed',3325,'v71 3305 + 20 non-overlapping'),
        ('v72_unobserved',2084,'5409 - 3325'),
        ('v72_candidate_auditable',2855,'2835 + 20')])
    c.commit()
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
    checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
                observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
                candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
                remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
                v72review=c.execute('select count(*) from v72_visual_review').fetchone()[0],
                final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=3325,candidate=2855,remaining=2084,v72review=20,final=0),checks
    c.execute('VACUUM')
out=ROOT/'analysis/current/v72'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes()
packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v72/v72.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n','ascii')
    parts.append(rel)
manifest=dict(version='v72',sqlite_file='tile_visual_v72_unified.sqlite',
    sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
    compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
    base_version='v71',base_sqlite_sha256=prior['sqlite_sha256'],
    new_records_repo_path='checkpoints/v72/observations.tsv',
    evidence_manifest='checkpoints/v72_preview/EVIDENCE_MANIFEST.json',
    source_record_count=20,observed=3325,provisional_candidates=2855,remaining=2084,
    certified=0,all_prior_tables_preserved=True,
    original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
    note='A/B/C/D 원본 증거 20종 직접 시각 판독. 잠정 후보 20, 보류 0. PNG height mismatch/TileZed 미검증.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert s['unified_database']['version']=='v71' and s['unified_database']['observed_unique']==3305
s['latest_checkpoint']=dict(version='v72',date='2026-10-26',baseline_reconciliation='v71',
    baseline_unique_observed=3305,new_unique_observed=20,new_provisional_candidates=20,new_held=0,
    overlap_with_prior=0,merged_unique_observed=3325,merged_observation_percent=round(3325/5409*100,4),
    remaining_unobserved=2084,auditable_provisional_candidate_keys=2855,approved_final_certifications=0,
    delta_repo_path='checkpoints/v72/observations.tsv',evidence_repo_path='checkpoints/v72_preview/',
    verification_script='checkpoints/v72/verify_delta.py',png_tmx_mapping_verified=0,
    tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v72',status='VERIFIED',
    repo_manifest='analysis/current/v72/MANIFEST.json',restore_script='scripts/restore_unified_v72.py',
    observed_unique=3325,observed_percent=round(3325/5409*100,4),remaining_unobserved=2084,
    auditable_candidates=2855,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
    complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
    v72_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
    'v72 통합 DB의 미관찰 2,084종에서 신규 고유 키를 선정해 PNG·TMX A/B/C/D 직접 검수한다.',
    'v71 이하의 보류 타일은 가림·다중 부품 역할을 다른 위치에서 재검수한다.',
    'PNG 물리 높이 불일치 및 TileZed 공식 Local ID 정합을 독립 검증한다.',
    '사용자 수동 검수 80종 및 재검수 자료는 별도 계보로 보존하며 자동 합산하지 않는다.',
    'v71 이하 원본 SQLite·체크포인트·원본 PNG·TMX를 삭제하거나 덮어쓰지 않는다.',
    'v72 신규 20종 A/B/C/D+비교판 100 JPEG를 checkpoints/v72_preview/에 보존한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
print('PASS BUILD v72',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
