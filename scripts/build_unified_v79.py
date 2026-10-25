#!/usr/bin/env python3
"""v78 물리 DB 복사 + v79 실제 시각 판독 12종 결합. 원본/기존 테이블 불변 보존."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v78/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
    assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==3429
    assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==2942
with (ROOT/'checkpoints/v79/observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==12
assert sum(r['review_status']=='candidate' for r in rows)==8
assert sum(r['review_status']=='held' for r in rows)==4
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v79_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
    c.execute('pragma journal_mode=DELETE')
    for col in ('v79_observed','v79_candidate_auditable'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
    for col in ('v79_review_status','v79_identity_candidate','v79_observed_features'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
    cols=list(rows[0])
    ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
          'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
    c.execute('CREATE TABLE v79_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        k=(r['tile_set_locator'],int(r['local_id']))
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
        assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
        cand=int(r['review_status']=='candidate')
        c.execute('INSERT INTO v79_visual_review VALUES('+','.join('?' for _ in cols)+')',
                  [int(r[x]) if x in ints else r[x] for x in cols])
        c.execute("""UPDATE tile_catalog SET observed_any=1,v79_observed=1,
                  provisional_candidate_any_auditable=?,v79_candidate_auditable=?,v79_review_status=?,
                  v79_identity_candidate=?,v79_observed_features=?,current_candidate=?,current_review_version='v79'
                  WHERE tile_set_locator=? AND local_id=?""",
                  (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
    c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
        ('v79_new_observed',12,'A/B/C/D visually inspected and recorded'),
        ('v79_new_candidates',8,'provisional, not certified'),
        ('v79_new_held',4,'Occluded tiles held without identity'),
        ('v79_total_observed',3441,'v78 3429 + 12 non-overlapping'),
        ('v79_unobserved',1968,'5409 - 3441'),
        ('v79_candidate_auditable',2950,'2942 + 8')])
    c.commit()
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
    checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
                observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
                candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
                remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
                v79review=c.execute('select count(*) from v79_visual_review').fetchone()[0],
                final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=3441,candidate=2950,remaining=1968,v79review=12,final=0),checks
    c.execute('VACUUM')
out=ROOT/'analysis/current/v79'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes()
packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v79/v79.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n','ascii')
    parts.append(rel)
manifest=dict(version='v79',sqlite_file='tile_visual_v79_unified.sqlite',
    sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
    compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
    base_version='v78',base_sqlite_sha256=prior['sqlite_sha256'],
    new_records_repo_path='checkpoints/v79/observations.tsv',
    evidence_manifest='checkpoints/v79_preview/EVIDENCE_MANIFEST.json',
    source_record_count=12,observed=3441,provisional_candidates=2950,remaining=1968,
    certified=0,all_prior_tables_preserved=True,
    original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
    note='A/B/C/D 원본 증거 12종 직접 시각 판독. 잠정 후보 8, 보류 4. PNG height mismatch/TileZed 미검증.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert (s['unified_database']['version'],s['unified_database']['observed_unique']) in {('v78',3429),('v79',3441)}
s['latest_checkpoint']=dict(version='v79',date='2026-10-26',baseline_reconciliation='v78',
    baseline_unique_observed=3429,new_unique_observed=12,new_provisional_candidates=8,new_held=4,
    overlap_with_prior=0,merged_unique_observed=3441,merged_observation_percent=round(3441/5409*100,4),
    remaining_unobserved=1968,auditable_provisional_candidate_keys=2950,approved_final_certifications=0,
    delta_repo_path='checkpoints/v79/observations.tsv',evidence_repo_path='checkpoints/v79_preview/',
    verification_script='checkpoints/v79/verify_delta.py',png_tmx_mapping_verified=0,
    tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v79',status='VERIFIED',
    repo_manifest='analysis/current/v79/MANIFEST.json',restore_script='scripts/restore_unified_v79.py',
    observed_unique=3441,observed_percent=round(3441/5409*100,4),remaining_unobserved=1968,
    auditable_candidates=2950,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
    complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
    v79_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
    'v79 통합 DB의 미관찰 1,980종에서 신규 고유 키를 선정해 PNG·TMX A/B/C/D 직접 검수한다.',
    'v78 이하의 보류 타일은 가림·다중 부품 역할을 다른 위치에서 재검수한다.',
    'PNG 물리 높이 불일치 및 TileZed 공식 Local ID 정합을 독립 검증한다.',
    '사용자 수동 검수 80종 및 재검수 자료는 별도 계보로 보존하며 자동 합산하지 않는다.',
    'v78 이하 원본 SQLite·체크포인트·원본 PNG·TMX를 삭제하거나 덮어쓰지 않는다.',
    'v79 신규 12종 A/B/C/D+비교판 60 JPEG를 checkpoints/v79_preview/에 보존한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
print('PASS BUILD v79',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
