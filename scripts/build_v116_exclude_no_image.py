#!/usr/bin/env python3
"""v116 user exclusion: hide six PNG-unavailable v115 held keys in future active review.
Preserve complete v115 SQLite, full historical held queue, all evidence and source catalog.
"""
from pathlib import Path
import csv,json,hashlib,sqlite3,base64,zlib,os,sys
R=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
prev=json.loads((R/'analysis/current/v115/MANIFEST.json').read_text('utf-8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==prev['sqlite_sha256']
with (R/'checkpoints/v116/user_exclude_six.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==6
assert len({(r['tile_set_locator'],int(r['local_id'])) for r in rows})==6
assert [int(r['review_index']) for r in rows]==[123,124,125,705,712,713]
assert all(r['user_action']=='exclude_from_active_review' for r in rows)
assert all(r['reason']=='source_png_or_localid_mapping_unavailable' for r in rows)
sjson=json.loads((R/'checkpoints/v116/user_exclude_summary.json').read_text('utf8'))
assert sjson['user_excluded_from_active_ai_review']==6 and sjson['remaining_active_held_no_image']==0
with sqlite3.connect(src) as c:
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    earlier={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert c.execute('SELECT count(*) FROM v115_ai_held_queue').fetchone()[0]==6
    assert c.execute('SELECT count(*) FROM v115_ai_candidate_queue').fetchone()[0]==882
    assert c.execute('SELECT count(*) FROM v113_active_review_queue').fetchone()[0]==1
    heldkeys={(r[0],int(r[1])) for r in c.execute("SELECT tile_set_locator,local_id FROM v115_ai_held_queue")}
    assert heldkeys=={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
dest=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v116_unified.sqlite'
if dest.exists():dest.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dest) as b:a.backup(b)
with sqlite3.connect(dest) as c:
    c.execute('PRAGMA journal_mode=DELETE')
    c.execute("""CREATE TABLE v116_user_excluded_missing_image(
      tile_set_locator TEXT NOT NULL,
      local_id INTEGER NOT NULL,
      review_index INTEGER NOT NULL UNIQUE,
      user_action TEXT NOT NULL,
      reason TEXT NOT NULL,
      source_visual_sheet TEXT NOT NULL,
      official_transparent_certified INTEGER NOT NULL DEFAULT 0 CHECK(official_transparent_certified=0),
      restore_allowed INTEGER NOT NULL DEFAULT 1,
      PRIMARY KEY (tile_set_locator,local_id))""")
    c.execute('ALTER TABLE tile_catalog ADD COLUMN v116_exclude_missing_image INTEGER NOT NULL DEFAULT 0')
    for r in rows:
        key=(r['tile_set_locator'],int(r['local_id']))
        prevRow=c.execute("SELECT review_index,review_status,source_status FROM v115_ai_visual_review WHERE tile_set_locator=? AND local_id=?",key).fetchone()
        assert prevRow is not None and prevRow[0]==int(r['review_index']) and prevRow[1]=='held'
        assert 'png_or_mapping_problem' in prevRow[2],(key,prevRow)
        assert c.execute('SELECT observed_any FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',key).fetchone()==(1,)
        c.execute('INSERT INTO v116_user_excluded_missing_image VALUES (?,?,?,?,?,?,?,?)',
            (*key,int(r['review_index']),r['user_action'],r['reason'],r['source_visual_sheet'],
             int(r['official_transparent_certified']),int(r['restore_allowed'])))
        c.execute('UPDATE tile_catalog SET v116_exclude_missing_image=1 WHERE tile_set_locator=? AND local_id=?',key)
    c.execute("""CREATE VIEW v116_active_v115_review_queue AS
      SELECT r.* FROM v115_ai_visual_review r
      LEFT JOIN v116_user_excluded_missing_image e ON
      e.tile_set_locator=r.tile_set_locator AND e.local_id=r.local_id
      WHERE e.tile_set_locator IS NULL""")
    c.execute("""CREATE VIEW v116_active_v115_held_queue AS
      SELECT * FROM v116_active_v115_review_queue WHERE review_status='held'""")
    # All prior v115 tables including v115_ai_held_queue still exist unchanged.
    assert earlier.issubset({r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")})
    checks={
      'catalog':c.execute('SELECT count(*) FROM tile_catalog').fetchone()[0],
      'image_observed':c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0],
      'prior_auditable_candidates':c.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0],
      'v115_historical_held':c.execute('SELECT count(*) FROM v115_ai_held_queue').fetchone()[0],
      'v115_original_candidates':c.execute('SELECT count(*) FROM v115_ai_candidate_queue').fetchone()[0],
      'user_excluded_six':c.execute('SELECT count(*) FROM v116_user_excluded_missing_image').fetchone()[0],
      'catalog_excluded_six':c.execute('SELECT count(*) FROM tile_catalog WHERE v116_exclude_missing_image=1').fetchone()[0],
      'remaining_held_active':c.execute('SELECT count(*) FROM v116_active_v115_held_queue').fetchone()[0],
      'remaining_active_v115':c.execute('SELECT count(*) FROM v116_active_v115_review_queue').fetchone()[0],
      'v113_historical_missing':c.execute('SELECT count(*) FROM analysis_queue').fetchone()[0],
      'v113_user_excluded':c.execute("SELECT count(*) FROM v113_user_review WHERE user_action='exclude_from_active_review'").fetchone()[0],
      'v113_active_missing':c.execute('SELECT count(*) FROM v113_active_review_queue').fetchone()[0],
      'final_certified':c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0],
    }
    assert checks==dict(catalog=5409,image_observed=5400,prior_auditable_candidates=4512,
         v115_historical_held=6,v115_original_candidates=882,user_excluded_six=6,
         catalog_excluded_six=6,remaining_held_active=0,remaining_active_v115=882,
         v113_historical_missing=9,v113_user_excluded=8,v113_active_missing=1,final_certified=0),checks
    c.commit()
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    c.execute('VACUUM')
out=R/'analysis/current/v116';out.mkdir(parents=True,exist_ok=True)
raw=dest.read_bytes()
compressed=zlib.compress(raw,6)
encoded=base64.b64encode(compressed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    p=out/f'v116.part{i//3000000:03}.b64'
    p.write_text(encoded[i:i+3000000]+'\n',encoding='ascii')
    parts.append(p.relative_to(R).as_posix())
manifest=dict(version='v116',kind='user_excluded_six_no_valid_A_images',
  sqlite_file='tile_visual_v116_unified.sqlite',
  sqlite_size_bytes=len(raw),sqlite_sha256=hashlib.sha256(raw).hexdigest(),
  compressed_sha256=hashlib.sha256(compressed).hexdigest(),compression='zlib_base64',
  parts=parts,base_version='v115',base_sqlite_sha256=prev['sqlite_sha256'],
  original_image_observed=5400,prior_auditable_candidates=4512,
  prior_v115_ai_candidates=882,historical_v115_held=6,
  v116_excluded_no_image=6,active_v115_held=0,active_v115_total=882,
  v113_excluded_unobserved=8,v113_active_unobserved=1,
  mapping_verified=0,tilezed_verified=0,final_certified=0,
  all_prior_tables_preserved=True,
  next_review_view='v116_active_v115_review_queue',
  next_held_view='v116_active_v115_held_queue',
  caution='No picture excludes from active review, not from physical tile catalog or historical source logs; does not prove transparency')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf8')
sp=R/'PROJECT_STATE.json'
s=json.loads(sp.read_text('utf8'))
assert s['latest_checkpoint']['version']=='v115'
s['previous_checkpoint_v115']=s['latest_checkpoint']
s['latest_checkpoint']=dict(
  version='v116',date='2026-10-26',kind='user_exclusion_missing_images',
  baseline_reconciliation='v115',
  new_image_observed=0,merged_unique_observed=5400,
  previous_ai_visual_candidate_keys=882,previous_ai_held_keys=6,
  new_candidate_keys=0,user_excluded_from_v115_held=6,
  active_v115_held=0,active_v115_review_keys=882,
  v113_user_excluded_unobserved=8,v113_active_unobserved=1,
  official_mapping_verified=0,official_tilezed_verified=0,approved_final_certifications=0,
  evidence_repo_path='checkpoints/v116/user_exclude_six.csv',
  caution='user exclusion from active no-image review only, not transparency or object certification')
s['unified_database']=dict(
  version='v116',status='VERIFIED',repo_manifest='analysis/current/v116/MANIFEST.json',
  restore_script='scripts/restore_unified_v116.py',observed_unique=5400,
  auditable_candidates=4512,v115_ai_visual_candidates=882,
  historical_v115_held=6,excluded_no_image=6,active_v115_held=0,
  active_v115_review=882,original_unobserved=9,
  v113_excluded=8,active_unobserved=1,certified=0,
  sqlite_sha256=manifest['sqlite_sha256'],all_prior_tables_preserved=True,
  image_binaries_in_github=True)
s['latest_user_exclusion_no_images']=dict(
  version='v116',excluded_keys=6,source='v115_ai_visual_review',
  only_active_review_excluded=True,historical_held_rows_preserved=6,
  unresolved_without_image_active=0,source_png_or_mapping_problem=True,
  transparency_certified=0,final_certified=0)
s['next_actions']=[
  'v116 user explicitly excludes all six image-unavailable v115 held keys: consult v116_active_v115_held_queue (0) not the historical v115_ai_held_queue (6).',
  'Preserve v115 source images/hold records and tile_catalog full 5409; do not label six as transparent or certified.',
  'Existing v115 visual family candidates 882 remain provisional; use v116_active_v115_review_queue (882) for any targeted verification.',
  'v113 original unobserved nine remain; user had separately excluded eight; f_bushes_1/66 remains active under v113_active_review_queue.',
  'Continue eventual 10,042-key target with 4,633 newly seen only after image/Local-ID candidate alignment is checked.'
]
s['status_date']='2026-10-26'
sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v116 all 6 missing-image keys excluded from ACTIVE review only',checks,'SHA',manifest['sqlite_sha256'],flush=True)
