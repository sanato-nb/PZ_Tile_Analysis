#!/usr/bin/env python3
"""v103 물리 DB 복사 + v104 신규 48종 직접 판독. 독립 D는 0이며 기존 계보 불변."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v103/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
    assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==5070
    assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==4255
with (ROOT/'checkpoints/v104/observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==48
assert sum(r['review_status']=='candidate' for r in rows)==35
assert sum(r['review_status']=='held' for r in rows)==13
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v104_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
    c.execute('pragma journal_mode=DELETE')
    for col in ('v104_observed','v104_candidate_auditable'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
    for col in ('v104_review_status','v104_identity_candidate','v104_observed_features'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
    cols=list(rows[0])
    ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
          'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
    c.execute('CREATE TABLE v104_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        k=(r['tile_set_locator'],int(r['local_id']))
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
        assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
        cand=int(r['review_status']=='candidate')
        c.execute('INSERT INTO v104_visual_review VALUES('+','.join('?' for _ in cols)+')',
                  [int(r[x]) if x in ints else r[x] for x in cols])
        c.execute("""UPDATE tile_catalog SET observed_any=1,v104_observed=1,
                  provisional_candidate_any_auditable=?,v104_candidate_auditable=?,v104_review_status=?,
                  v104_identity_candidate=?,v104_observed_features=?,current_candidate=?,current_review_version='v104'
                  WHERE tile_set_locator=? AND local_id=?""",
                  (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
    c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
        ('v104_new_observed',48,'A/B/C/D visually inspected and recorded'),
        ('v104_new_candidates',35,'provisional, not certified'),
        ('v104_new_held',13,'Occluded tiles held without identity'),
        ('v104_total_observed',5118,'v103 5070 + 48 non-overlapping'),
        ('v104_unobserved',291,'5409 - 5118'),
        ('v104_candidate_auditable',4290,'4255 + 35')])
    c.commit()
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
    checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
                observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
                candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
                remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
                v104review=c.execute('select count(*) from v104_visual_review').fetchone()[0],
                final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=5118,candidate=4290,remaining=291,v104review=48,final=0),checks
    c.execute('VACUUM')
out=ROOT/'analysis/current/v104'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes()
packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v104/v104.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n','ascii')
    parts.append(rel)
manifest=dict(version='v104',sqlite_file='tile_visual_v104_unified.sqlite',
    sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
    compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
    base_version='v103',base_sqlite_sha256=prior['sqlite_sha256'],
    new_records_repo_path='checkpoints/v104/observations.tsv',
    evidence_manifest='checkpoints/v104_preview/EVIDENCE_MANIFEST.json',
    source_record_count=48,observed=5118,provisional_candidates=4290,remaining=291,
    certified=0,all_prior_tables_preserved=True,
    original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
    note='v103 미관찰 48종 A/B/C와 3종 실제 근접 D 직접 판독. 나머지 D 미확보 45종. 후보 35 보류 13; 공식 Local ID/TileZed 미검증, PNG 높이 불일치.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert (s['unified_database']['version'],s['unified_database']['observed_unique']) in {('v103',5070),('v104',5118)}
s['latest_checkpoint']=dict(version='v104',date='2026-10-26',baseline_reconciliation='v103',
    baseline_unique_observed=5070,new_unique_observed=48,new_provisional_candidates=35,new_held=13,
    overlap_with_prior=0,merged_unique_observed=5118,merged_observation_percent=round(5118/5409*100,4),
    remaining_unobserved=291,auditable_provisional_candidate_keys=4290,approved_final_certifications=0,
    delta_repo_path='checkpoints/v104/observations.tsv',evidence_repo_path='checkpoints/v104_preview/',
    verification_script='checkpoints/v104/verify_delta.py',png_tmx_mapping_verified=0,
    tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v104',status='VERIFIED',
    repo_manifest='analysis/current/v104/MANIFEST.json',restore_script='scripts/restore_unified_v104.py',
    observed_unique=5118,observed_percent=round(5118/5409*100,4),remaining_unobserved=291,
    auditable_candidates=4290,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
    complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
    v104_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
    'v104 통합 DB 미관찰 291종에서 신규 고유 키를 선정하고 A/B/C/D 실제 증거를 확인한다.',
    'v104 가까운 D 3종은 독립 현장 미검증이며 45종은 2번째 현장이 없어 TileZed 확인을 우선한다.',
    'v104 보류 13종은 제거 변화가 미미하거나 부품 역할이 모호하므로 다른 배치·TileZed로 재검수한다.',
    'PNG 물리 높이 불일치와 공식 Local ID·TileZed 정합을 검증한다.',
    '기존 모든 원본 DB·체크포인트·사용자 수동 검수 80종 및 재검수 계보를 보존한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
print('PASS BUILD v104',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
