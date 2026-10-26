#!/usr/bin/env python3
"""v108 물리 DB 복사 + v109 신규 48종 직접 판독. 독립 D 1개는 투명 원본·B-C 0으로 보류, 기존 계보 불변."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v108/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
    assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==5310
    assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==4435
with (ROOT/'checkpoints/v109/observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==48
assert sum(r['review_status']=='candidate' for r in rows)==40
assert sum(r['review_status']=='held' for r in rows)==8
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v109_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
    c.execute('pragma journal_mode=DELETE')
    for col in ('v109_observed','v109_candidate_auditable'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
    for col in ('v109_review_status','v109_identity_candidate','v109_observed_features'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
    cols=list(rows[0])
    ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
          'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
    c.execute('CREATE TABLE v109_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        k=(r['tile_set_locator'],int(r['local_id']))
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
        assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
        cand=int(r['review_status']=='candidate')
        c.execute('INSERT INTO v109_visual_review VALUES('+','.join('?' for _ in cols)+')',
                  [int(r[x]) if x in ints else r[x] for x in cols])
        c.execute("""UPDATE tile_catalog SET observed_any=1,v109_observed=1,
                  provisional_candidate_any_auditable=?,v109_candidate_auditable=?,v109_review_status=?,
                  v109_identity_candidate=?,v109_observed_features=?,current_candidate=?,current_review_version='v109'
                  WHERE tile_set_locator=? AND local_id=?""",
                  (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
    c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
        ('v109_new_observed',48,'A/B/C/D visually inspected and recorded'),
        ('v109_new_candidates',38,'provisional, not certified'),
        ('v109_new_held',10,'Occluded tiles held without identity'),
        ('v109_total_observed',5358,'v108 5310 + 48 non-overlapping'),
        ('v109_unobserved',51,'5409 - 5358'),
        ('v109_candidate_auditable',4475,'4435 + 38')])
    c.commit()
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
    checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
                observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
                candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
                remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
                v109review=c.execute('select count(*) from v109_visual_review').fetchone()[0],
                final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=5358,candidate=4475,remaining=51,v109review=48,final=0),checks
    c.execute('VACUUM')
out=ROOT/'analysis/current/v109'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes()
packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v109/v109.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n','ascii')
    parts.append(rel)
manifest=dict(version='v109',sqlite_file='tile_visual_v109_unified.sqlite',
    sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
    compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
    base_version='v108',base_sqlite_sha256=prior['sqlite_sha256'],
    new_records_repo_path='checkpoints/v109/observations.tsv',
    evidence_manifest='checkpoints/v109_preview/EVIDENCE_MANIFEST.json',
    source_record_count=48,observed=5358,provisional_candidates=4475,remaining=51,
    certified=0,all_prior_tables_preserved=True,
    original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
    note='v108 미관찰 48종 A/B/C와 1종 실제 원거리 D를 확인했으나 투명 원본으로 정체 보류. 나머지 D 미확보 47종. 후보 40 보류 8; 공식 Local ID/TileZed 미검증, PNG 높이 불일치.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert (s['unified_database']['version'],s['unified_database']['observed_unique']) in {('v108',5310),('v109',5358)}
s['latest_checkpoint']=dict(version='v109',date='2026-10-26',baseline_reconciliation='v108',
    baseline_unique_observed=5310,new_unique_observed=48,new_provisional_candidates=40,new_held=8,
    overlap_with_prior=0,merged_unique_observed=5358,merged_observation_percent=round(5358/5409*100,4),
    remaining_unobserved=51,auditable_provisional_candidate_keys=4475,approved_final_certifications=0,
    delta_repo_path='checkpoints/v109/observations.tsv',evidence_repo_path='checkpoints/v109_preview/',
    verification_script='checkpoints/v109/verify_delta.py',png_tmx_mapping_verified=0,
    tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v109',status='VERIFIED',
    repo_manifest='analysis/current/v109/MANIFEST.json',restore_script='scripts/restore_unified_v109.py',
    observed_unique=5358,observed_percent=round(5358/5409*100,4),remaining_unobserved=51,
    auditable_candidates=4475,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
    complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
    v109_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
    'v109 통합 DB 미관찰 51종에서 신규 고유 키를 선정하고 A/B/C/D 실제 증거를 확인한다.',
    'v109 D는 1종에서 5칸 이상 다른 실제 배치 확인. 그러나 A 투명·B-C 변화 0으로 정체 미식별이므로 TileZed 및 공식 Local ID 검증을 우선한다.',
    'v109 보류 8종은 제거 영향이 작거나 부품 역할이 불명확하므로 독립 배치와 TileZed 검증을 우선한다.',
    'PNG 물리 높이 불일치와 공식 Local ID·TileZed 정합을 검증한다.',
    '기존 모든 원본 DB·체크포인트·사용자 수동 검수 80종 및 재검수 계보를 보존한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
print('PASS BUILD v109',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
