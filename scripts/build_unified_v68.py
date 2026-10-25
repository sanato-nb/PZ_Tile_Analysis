#!/usr/bin/env python3
"""v67 물리 DB 복사 + v68 실제 시각 판독 10종 결합. 원본/기존 테이블 불변 보존."""
from pathlib import Path
import csv,sqlite3,hashlib,zlib,base64,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v67/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
with sqlite3.connect(src) as c:
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    tables_prior={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
    assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==3175
    assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==2737
with (ROOT/'checkpoints/v68/observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==80
assert sum(r['review_status']=='candidate' for r in rows)==56
assert sum(r['review_status']=='held' for r in rows)==24
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v68_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
    c.execute('pragma journal_mode=DELETE')
    for col in ('v68_observed','v68_candidate_auditable'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' INTEGER NOT NULL DEFAULT 0')
    for col in ('v68_review_status','v68_identity_candidate','v68_observed_features'):
        c.execute('ALTER TABLE tile_catalog ADD COLUMN '+col+' TEXT')
    cols=list(rows[0])
    ints={'local_id','level','x','y','other_level','other_x','other_y','visible_pixel_delta',
          'missing_png_neighbors','png_height_mismatch','mapping_verified','tilezed_verified','final_certified'}
    c.execute('CREATE TABLE v68_visual_review('+','.join('"'+x+'" '+('INTEGER' if x in ints else 'TEXT') for x in cols)+',PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        k=(r['tile_set_locator'],int(r['local_id']))
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,),('duplicate/unknown',k)
        assert r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0'
        cand=int(r['review_status']=='candidate')
        c.execute('INSERT INTO v68_visual_review VALUES('+','.join('?' for _ in cols)+')',
                  [int(r[x]) if x in ints else r[x] for x in cols])
        c.execute("""UPDATE tile_catalog SET observed_any=1,v68_observed=1,
                  provisional_candidate_any_auditable=?,v68_candidate_auditable=?,v68_review_status=?,
                  v68_identity_candidate=?,v68_observed_features=?,current_candidate=?,current_review_version='v68'
                  WHERE tile_set_locator=? AND local_id=?""",
                  (cand,cand,r['review_status'],r['identity_candidate'],r['observed_features'],r['identity_candidate'],*k))
    c.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
        ('v68_new_observed',80,'A/B/C/D visually inspected and recorded'),
        ('v68_new_candidates',56,'provisional, not certified'),
        ('v68_new_held',24,'Occluded tiles held without identity'),
        ('v68_total_observed',3255,'v67 3175 + 80 non-overlapping'),
        ('v68_unobserved',2154,'5409 - 3255'),
        ('v68_candidate_auditable',2793,'2737 + 56')])
    c.commit()
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert tables_prior.issubset({r[0] for r in c.execute("select name from sqlite_master where type='table'")})
    checks=dict(all=c.execute('select count(*) from tile_catalog').fetchone()[0],
                observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
                candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
                remaining=c.execute('select count(*) from analysis_queue').fetchone()[0],
                v68review=c.execute('select count(*) from v68_visual_review').fetchone()[0],
                final=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=3255,candidate=2793,remaining=2154,v68review=80,final=0),checks
    c.execute('VACUUM')
out=ROOT/'analysis/current/v68'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes()
packed=zlib.compress(raw,6)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v68/v68.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n','ascii')
    parts.append(rel)
manifest=dict(version='v68',sqlite_file='tile_visual_v68_unified.sqlite',
    sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
    compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',parts=parts,
    base_version='v67',base_sqlite_sha256=prior['sqlite_sha256'],
    new_records_repo_path='checkpoints/v68/observations.tsv',
    evidence_manifest='checkpoints/v68_preview/EVIDENCE_MANIFEST.json',
    source_record_count=80,observed=3255,provisional_candidates=2793,remaining=2154,
    certified=0,all_prior_tables_preserved=True,
    original_sprite_evidence_images_in_github=True,mapping_verified=0,tilezed_verified=0,
    note='A/B/C/D 원본 증거의 80종 직접 시각 판독. 잠정 후보 56 보류 24. PNG height mismatch/TileZed 미검증.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json'
s=json.loads(statepath.read_text('utf8'))
assert s['unified_database']['version']=='v67' and s['unified_database']['observed_unique']==3175
s['latest_checkpoint']=dict(version='v68',date='2026-10-26',baseline_reconciliation='v67',
    baseline_unique_observed=3175,new_unique_observed=80,new_provisional_candidates=56,new_held=24,
    overlap_with_prior=0,merged_unique_observed=3255,merged_observation_percent=round(3255/5409*100,4),
    remaining_unobserved=2154,auditable_provisional_candidate_keys=2793,approved_final_certifications=0,
    delta_repo_path='checkpoints/v68/observations.tsv',evidence_repo_path='checkpoints/v68_preview/',
    verification_script='checkpoints/v68/verify_delta.py',png_tmx_mapping_verified=0,
    tilezed_verified=0,high_resolution_evidence_images_in_github=True)
s['unified_database']=dict(version='v68',status='VERIFIED',
    repo_manifest='analysis/current/v68/MANIFEST.json',restore_script='scripts/restore_unified_v68.py',
    observed_unique=3255,observed_percent=round(3255/5409*100,4),remaining_unobserved=2154,
    auditable_candidates=2793,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
    complete_v36_tables=True,complete_v46_tables=True,all_prior_tables_preserved=True,
    v68_git_checkpoint_integrated=True,image_binaries_in_github=True)
s['status_date']='2026-10-26'
s['next_actions']=[
    'v68 통합 DB의 미관찰 2,234종을 PNG·TMX A/B/C/D 직접 관찰로 이어간다.',
    'v68 보류 24종의 가림 및 미확인 부품 방향을 추가 재검수한다.',
    'v67 이하 보류 타일의 층·레이어 가림 및 PNG 높이 불일치를 별도로 재검수한다.',
    'PNG 선언 높이 불일치와 Local ID 매핑을 TileZed에서 검증한다.',
    '사용자 수동 검수 80종 및 재검수 기록은 별도 계보로 보존하고 자동 합산하지 않는다.',
    'v67 이하 모든 통합 SQLite·체크포인트·원본 PNG·TMX·충돌 기록을 변경하지 않는다.',
    'v68 신규 80종 A/B/C/D+비교판 400장 JPEG를 checkpoints/v68_preview/에 보관한다.'
]
statepath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS BUILD v68',checks,'sha',manifest['sqlite_sha256'],'parts',len(parts))
