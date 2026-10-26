#!/usr/bin/env python3
"""v110 diagnostic-only physical SQLite: 9 visually blank cases + 42 missing source crops.
No tile is promoted to observed, candidate, mapping-verified, or certified.
"""
from pathlib import Path
import base64,csv,hashlib,json,os,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prior=json.loads((ROOT/'analysis/current/v109/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prior['sqlite_sha256']
ev=json.loads((ROOT/'checkpoints/v110_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert ev['base']=='v109' and len(ev['results'])==9 and ev['blocked_count']==len(ev['blocked_unobserved'])==42
notes={}
for line in (ROOT/'checkpoints/v110/review_notes_000_008.psv').read_text('utf8').splitlines()[1:]:
    ix,description,status,reason=line.split('|')
    notes[int(ix)]=(description,status,reason)
assert len(notes)==9 and all(x[1]=='held' for x in notes.values())
with sqlite3.connect(src) as conn:
    assert conn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    previous_tables={r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    queue={(r[0],int(r[1])) for r in conn.execute('SELECT tile_set_locator,local_id FROM analysis_queue')}
    assert len(queue)==51
    assert conn.execute('SELECT COUNT(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5358
    assert conn.execute('SELECT COUNT(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0]==4475
rows=[]
for i,x in enumerate(ev['results']):
    k=(x['key'][0],int(x['key'][1]))
    assert x['visible_pixel_delta']==0 and x['status']=='evidence_only_unreviewed'
    description,status,reason=notes[i]
    rows.append(dict(tile_set_locator=k[0],local_id=k[1],review_status='held_no_visible_source',
      reason=reason,source_issue=x['atlas_status'],tmx_uses=x['uses'],
      visible_pixel_delta=0,other_placement_available=int(x['other_placement_available']),
      D_independent=int(x['D_independent_5_cells_or_other_map']),
      observed_features=description,evidence_prefix='checkpoints/v110_preview/'+k[0]+'__'+str(k[1]).zfill(3)))
for x in ev['blocked_unobserved']:
    rows.append(dict(tile_set_locator=x['key'][0],local_id=int(x['key'][1]),
      review_status='held_source_unavailable',reason=x['reason'],
      source_issue=x['atlas_status'],tmx_uses=x['uses'],visible_pixel_delta=-1,
      other_placement_available=0,D_independent=0,
      observed_features='원본 PNG 누락 또는 공식 Local ID가 현재 PNG 범위 밖이라 크롭·정체 검증 불가',
      evidence_prefix=''))
fields=list(rows[0]); keys={(r['tile_set_locator'],r['local_id']) for r in rows}
assert len(rows)==len(keys)==51 and keys==queue,('missing_or_duplicate',len(keys),len(queue),sorted(queue-keys))
p=ROOT/'checkpoints/v110'
p.mkdir(parents=True,exist_ok=True)
with (p/'unresolved_51.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v110_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as conn:
    conn.execute('PRAGMA journal_mode=DELETE')
    types={'local_id':'INTEGER','tmx_uses':'INTEGER','visible_pixel_delta':'INTEGER','other_placement_available':'INTEGER','D_independent':'INTEGER'}
    ddl=','.join('"'+f+'" '+types.get(f,'TEXT') for f in fields)
    conn.execute('CREATE TABLE v110_unresolved_queue_audit('+ddl+',PRIMARY KEY(tile_set_locator,local_id))')
    for r in rows:
        k=(r['tile_set_locator'],r['local_id'])
        assert conn.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()==(0,)
        conn.execute('INSERT INTO v110_unresolved_queue_audit VALUES('+','.join('?' for _ in fields)+')',[r[f] for f in fields])
    conn.executemany('INSERT INTO progress_snapshot VALUES (?,?,?)',[
      ('v110_attempted_but_blank',9,'A visually blank, B-C 0; still unobserved'),
      ('v110_source_unavailable',42,'PNG missing 5 or Local ID out of png 37; still unobserved'),
      ('v110_new_observed',0,'No change to tile_catalog observed flags'),
      ('v110_remaining_unobserved',51,'All pending official local ID/PNG mapping'),
      ('v110_audit_rows',51,'Separate unresolved evidence table only')])
    conn.commit()
    assert conn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert previous_tables.issubset({r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")})
    checks=dict(all=conn.execute('SELECT count(*) FROM tile_catalog').fetchone()[0],
      observed=conn.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0],
      candidate=conn.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0],
      remaining=conn.execute('SELECT count(*) FROM analysis_queue').fetchone()[0],
      v110audit=conn.execute('SELECT count(*) FROM v110_unresolved_queue_audit').fetchone()[0],
      certified=conn.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=5358,candidate=4475,remaining=51,v110audit=51,certified=0),checks
    conn.execute('VACUUM')
out=ROOT/'analysis/current/v110'
out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes(); packed=zlib.compress(raw,6);encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    rel=f'analysis/current/v110/v110.part{i//3000000:03}.b64'
    (ROOT/rel).write_text(encoded[i:i+3000000]+'\n',encoding='ascii')
    parts.append(rel)
manifest=dict(version='v110',mode='source_gap_diagnostic_no_progress',
  sqlite_file='tile_visual_v110_unified.sqlite',sqlite_size_bytes=len(raw),
  sqlite_sha256=hashlib.sha256(raw).hexdigest(),compressed_sha256=hashlib.sha256(packed).hexdigest(),
  compression='zlib_base64',parts=parts,base_version='v109',base_sqlite_sha256=prior['sqlite_sha256'],
  observed=5358,provisional_candidates=4475,remaining=51,certified=0,
  new_unique_observed=0,visually_checked_but_blank=9,blocked_missing_png=5,blocked_out_of_png=37,
  v110_unresolved_audit_rows=51,all_prior_tables_preserved=True,
  evidence_manifest='checkpoints/v110_preview/EVIDENCE_MANIFEST.json',
  audit_csv='checkpoints/v110/unresolved_51.csv',mapping_verified=0,tilezed_verified=0,
  note='9 original crops A blank / B-C delta zero, 37 local_id_out_of_png, 5 missing. No new identity candidates or observed flags. Need official mapping / TileZed.')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
statepath=ROOT/'PROJECT_STATE.json'
state=json.loads(statepath.read_text('utf8'))
assert state['unified_database']['version']=='v109' and state['unified_database']['observed_unique']==5358
state['latest_checkpoint']=dict(version='v110',date='2026-10-26',baseline_reconciliation='v109',
  baseline_unique_observed=5358,new_unique_observed=0,new_provisional_candidates=0,new_held=0,
  new_unresolved_source_audits=51,checked_blank_no_visible_effect=9,blocked_missing_png=5,
  blocked_local_id_out_of_png=37,overlap_with_prior=0,
  merged_unique_observed=5358,merged_observation_percent=round(5358/5409*100,4),
  remaining_unobserved=51,auditable_provisional_candidate_keys=4475,approved_final_certifications=0,
  delta_repo_path='checkpoints/v110/unresolved_51.csv',evidence_repo_path='checkpoints/v110_preview/',
  verification_script='scripts/verify_v110_audit.py',png_tmx_mapping_verified=0,tilezed_verified=0,
  high_resolution_evidence_images_in_github=True)
state['unified_database']=dict(version='v110',status='VERIFIED_DIAGNOSTIC',
  repo_manifest='analysis/current/v110/MANIFEST.json',restore_script='scripts/restore_unified_v110.py',
  observed_unique=5358,observed_percent=round(5358/5409*100,4),
  remaining_unobserved=51,auditable_candidates=4475,certified=0,
  sqlite_sha256=manifest['sqlite_sha256'],complete_v36_tables=True,
  complete_v46_tables=True,all_prior_tables_preserved=True,
  v110_git_checkpoint_integrated=True,image_binaries_in_github=True)
state['status_date']='2026-10-26'
state['next_actions']=[
 'v110 미관찰 51종은 투명 A·B-C 0인 9종과, Local ID 범위 밖 37종 및 PNG 누락 5종으로 분류했다. 정체와 관찰 수는 인증하지 않는다.',
 '공식 TileZed 타일셋 PNG/매핑에서 out-of-png 37종의 Local ID 대응 및 실제 원본 스프라이트를 먼저 재획득한다.',
 'PNG 누락 5종의 원본 파일명을 확인하고 유실된 대상을 사용자가 제공한 Tiles 소스와 대조한다.',
 '실제 대응이 확인될 때만 A/B/C/D를 다시 생성하고 observed/candidate를 올린다.',
 'v36~v109 전체 테이블·수동 검수 80종 계보를 보존한다.'
]
statepath.write_text(json.dumps(state,ensure_ascii=False,indent=0)+'\n',encoding='utf8')
print('PASS v110 diagnostic SQLite physically preserved, no new observed/candidates',checks,manifest['sqlite_sha256'])