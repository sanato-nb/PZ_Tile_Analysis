#!/usr/bin/env python3
"""v113 user feedback filter. Full-copy v111; never promote/excise historical catalog records."""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
parent=json.loads((ROOT/'analysis/current/v111/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==parent['sqlite_sha256']
summary=json.loads((ROOT/'checkpoints/v113/user_review_summary.json').read_text('utf8'))
with (ROOT/'checkpoints/v113/user_review.csv').open('r',encoding='utf-8-sig',newline='') as f:
    feedback=list(csv.DictReader(f))
assert len(feedback)==9 and len({(r['tile_set_locator'],int(r['local_id'])) for r in feedback})==9
assert [int(r['review_number']) for r in feedback]==list(range(1,10))
assert sum(r['user_action']=='exclude_from_active_review' for r in feedback)==8
assert sum(r['user_action']=='keep_provisional' for r in feedback)==1
assert next(x for x in feedback if x['user_action']=='keep_provisional')['tile_set_locator']=='f_bushes_1'
assert next(x for x in feedback if x['user_action']=='keep_provisional')['local_id']=='66'
assert all(r['user_confidence']=='low' for r in feedback if r['user_action']=='keep_provisional')
assert all(r['user_confidence']=='not_applicable' for r in feedback if r['user_action']=='exclude_from_active_review')
assert (summary['already_observed'],summary['historical_unobserved'],summary['user_excluded_from_active_review'],summary['active_unobserved_to_review'])==(5400,9,8,1)
with sqlite3.connect(src) as c:
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    prior_tables={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    prior_views={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='view'")}
    q={(r[0],int(r[1])) for r in c.execute('SELECT tile_set_locator,local_id FROM analysis_queue')}
    assert len(q)==9 and q=={(r['tile_set_locator'],int(r['local_id'])) for r in feedback}
    assert c.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0]==4512
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v113_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
    c.execute('PRAGMA journal_mode=DELETE')
    c.execute("""CREATE TABLE v113_user_review(
        review_number INTEGER UNIQUE NOT NULL,
        tile_set_locator TEXT NOT NULL,
        local_id INTEGER NOT NULL,
        user_action TEXT NOT NULL CHECK(user_action IN ('exclude_from_active_review','keep_provisional')),
        user_candidate TEXT NOT NULL,
        user_confidence TEXT NOT NULL,
        source_evidence_status TEXT NOT NULL,
        manual_review_note TEXT NOT NULL,
        PRIMARY KEY(tile_set_locator,local_id))""")
    c.execute('ALTER TABLE tile_catalog ADD COLUMN v113_user_review_action TEXT')
    c.execute('ALTER TABLE tile_catalog ADD COLUMN v113_user_candidate TEXT')
    cols=list(feedback[0].keys())
    assert len(cols)==8
    for r in feedback:
        key=(r['tile_set_locator'],int(r['local_id']))
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',key).fetchone()==(0,)
        c.execute('INSERT INTO v113_user_review VALUES (?,?,?,?,?,?,?,?)',
            (int(r['review_number']),r['tile_set_locator'],int(r['local_id']),
             r['user_action'],r['user_candidate'],r['user_confidence'],
             r['source_evidence_status'],r['manual_review_note']))
        c.execute('UPDATE tile_catalog SET v113_user_review_action=?,v113_user_candidate=? WHERE tile_set_locator=? AND local_id=?',
            (r['user_action'],r['user_candidate'] or None,*key))
    c.execute("""CREATE VIEW v113_active_review_queue AS
        SELECT q.tile_set_locator,q.local_id FROM analysis_queue q
        LEFT JOIN v113_user_review r ON
            r.tile_set_locator=q.tile_set_locator AND r.local_id=q.local_id
        WHERE r.user_action IS NULL OR r.user_action!='exclude_from_active_review'""")
    c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
        ('v113_user_review_entries',9,'User manual visual verdicts; historical table remains untouched'),
        ('v113_user_excluded_active',8,'Review exclusion only; not transparent-certified, observed or deleted'),
        ('v113_user_provisional_active',1,'f_bushes_1/66: grass or flower plant, low confidence, B-C delta zero'),
        ('v113_new_observed',0,'No original image observation promoted'),
        ('v113_historical_unobserved',9,'Original analysis_queue remains 9'),
        ('v113_active_review_remaining',1,'Use v113_active_review_queue for future review selection')])
    c.commit()
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert prior_tables.issubset({r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")})
    assert prior_views.issubset({r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='view'")})
    checks=dict(total=c.execute('SELECT count(*) FROM tile_catalog').fetchone()[0],
        observed=c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0],
        candidate=c.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0],
        historical_unobserved=c.execute('SELECT count(*) FROM analysis_queue').fetchone()[0],
        active_review=c.execute('SELECT count(*) FROM v113_active_review_queue').fetchone()[0],
        manual_excluded=c.execute("SELECT count(*) FROM v113_user_review WHERE user_action='exclude_from_active_review'").fetchone()[0],
        manual_provisional=c.execute("SELECT count(*) FROM v113_user_review WHERE user_action='keep_provisional'").fetchone()[0],
        final=c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0])
    assert checks==dict(total=5409,observed=5400,candidate=4512,historical_unobserved=9,
        active_review=1,manual_excluded=8,manual_provisional=1,final=0),checks
    remaining=c.execute('SELECT tile_set_locator,local_id FROM v113_active_review_queue').fetchall()
    assert remaining==[('f_bushes_1',66)],remaining
    c.execute('VACUUM')
out=ROOT/'analysis/current/v113';out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes();packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v113/v113.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n',encoding='ascii')
    parts.append(rel)
manifest=dict(version='v113',mode='user_review_filter_no_observed_change',
    sqlite_file='tile_visual_v113_unified.sqlite',sqlite_size_bytes=len(raw),
    sqlite_sha256=hashlib.sha256(raw).hexdigest(),compressed_sha256=hashlib.sha256(packed).hexdigest(),
    compression='zlib_base64',parts=parts,base_version='v111',base_sqlite_sha256=parent['sqlite_sha256'],
    observed=5400,provisional_candidates_auditable=4512,historical_remaining=9,
    active_review_remaining=1,user_excluded=8,user_provisional=1,certified=0,
    review_csv='checkpoints/v113/user_review.csv',review_view='v113_active_review_queue',
    user_review_table='v113_user_review',all_prior_tables_preserved=True,
    mapping_verified=0,tilezed_verified=0,
    note='Eight user-excluded from active review without deletion or observed promotion; grass/flower low-confidence manual candidate 1; official mapping unverified.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json';s=json.loads(statepath.read_text('utf8'))
assert s['latest_checkpoint']['version']=='v111'
assert s['unified_database']['version']=='v111' and s['unified_database']['observed_unique']==5400
s['latest_checkpoint']=dict(
    version='v113',date='2026-10-26',kind='manual_review_filter',baseline_reconciliation='v111',
    baseline_unique_observed=5400,new_unique_observed=0,new_provisional_candidates=0,new_held=0,
    new_user_manual_candidates=1,new_user_review_excluded=8,new_user_review_count=9,
    merged_unique_observed=5400,merged_observation_percent=round(5400/5409*100,4),
    remaining_unobserved=9,active_unobserved=1,user_excluded_from_active_review=8,
    auditable_provisional_candidate_keys=4512,approved_final_certifications=0,
    delta_repo_path='checkpoints/v113/user_review.csv',
    evidence_repo_path='checkpoints/v111_singleuse_preview/',
    verification_script='scripts/restore_unified_v113.py',
    png_tmx_mapping_verified=0,tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v113',status='VERIFIED',
    repo_manifest='analysis/current/v113/MANIFEST.json',
    restore_script='scripts/restore_unified_v113.py',observed_unique=5400,
    observed_percent=round(5400/5409*100,4),remaining_unobserved=9,
    active_unobserved=1,user_excluded=8,auditable_candidates=4512,
    user_provisional_candidates=1,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
    complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
    v113_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['latest_user_review']=dict(version='v113',source='user_manual_review',
    reviewed_count=9,exclude_from_active_review=8,keep_provisional=1,
    active_review_key=['f_bushes_1',66],user_identity_candidate='풀 또는 꽃 계열 식물',
    confidence='low',historical_unobserved_preserved=9,final_certified=0)
s['next_actions']=[
    'v113부터 신규 검수 대상은 analysis_queue 대신 v113_active_review_queue를 사용한다. 사용자가 8종을 활성 검수에서 제외했으며 과거 타일 키와 출처는 보존한다.',
    '남은 활성 f_bushes_1/66은 사용자 잠정 후보 풀 또는 꽃 계열 식물. 원본 A 알파 4,837픽셀이나 B-C 변화 0이므로 공식 Local ID·TileZed 정합 전 정체 확정 금지.',
    '제외 8종 중 사무실 3종은 잠정 크롭 투명, JUMBO 3종은 매핑 불확실한 빈 크롭, PNG 미확보 2종은 실제 투명 여부 미검증.',
    'v36~v111 과거 DB 테이블·사용자 수동 검수 80종·PNG/TMX 원본은 삭제 또는 수정하지 않는다.'
]
s['status_date']='2026-10-26'
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v113 physical SQLite + review scope',checks,manifest['sqlite_sha256'])