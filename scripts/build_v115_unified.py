#!/usr/bin/env python3
"""Append v115 visually inspected but explicitly UNVERIFIED AI candidate table to complete v113 SQLite."""
from pathlib import Path
import csv,json,hashlib,sqlite3,base64,zlib,os,sys
R=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve()
base=json.loads((R/'analysis/current/v113/MANIFEST.json').read_text('utf8'))
assert hashlib.sha256(src.read_bytes()).hexdigest()==base['sqlite_sha256']
f=R/'review/v115_ai_identity/AI_VISUAL_REVIEW_888.csv'
with f.open('r',newline='',encoding='utf-8-sig') as fp:reviews=list(csv.DictReader(fp))
assert len(reviews)==888
assert [(int(x['review_index'])) for x in reviews]==list(range(888))
assert len({(r['tile_set_locator'],int(r['local_id'])) for r in reviews})==888
assert sum(x['review_status']=='candidate' for x in reviews)==882
assert sum(x['review_status']=='held' for x in reviews)==6
assert sum(x['confidence']=='medium' for x in reviews)==12
assert sum(x['confidence']=='low' for x in reviews)==870
assert all(x['mapping_verified']==x['tilezed_verified']==x['final_certified']=='0' for x in reviews)
assert len({x['evidence_sheet'] for x in reviews})==74
j=json.loads((R/'review/v115_ai_identity/SUMMARY.json').read_text('utf8'))
assert j['candidate']==882 and j['held']==6 and j['reviewed_images']==888
with sqlite3.connect(src) as c:
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 tables={x[0] for x in c.execute("select name from sqlite_master where type='table'")}
 views={x[0] for x in c.execute("select name from sqlite_master where type='view'")}
 assert c.execute('select count(*) from tile_catalog').fetchone()[0]==5409
 assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==5400
 assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==4512
 assert c.execute('select count(*) from analysis_queue').fetchone()[0]==9
 assert c.execute("select count(*) from v113_user_review where user_action='exclude_from_active_review'").fetchone()[0]==8
 assert c.execute('select count(*) from v113_active_review_queue').fetchone()[0]==1
 assert c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0]==0
dst=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'tile_visual_v115_unified.sqlite'
if dst.exists():dst.unlink()
with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:a.backup(b)
with sqlite3.connect(dst) as c:
 c.execute('pragma journal_mode=DELETE')
 cols=list(reviews[0])
 ints={'review_index','local_id','slot','visible_delta_5x5','mapping_verified',
   'tilezed_verified','final_certified'}
 c.execute('CREATE TABLE v115_ai_visual_review ('+','.join('"'+n+'" '+('INTEGER' if n in ints else 'TEXT') for n in cols)+', PRIMARY KEY(tile_set_locator,local_id))')
 for n in ('v115_ai_identity_candidate','v115_ai_part_role','v115_ai_review_status','v115_ai_confidence'):
  c.execute('ALTER TABLE tile_catalog ADD COLUMN '+n+' TEXT')
 params=','.join('?' for x in cols)
 sql='INSERT INTO v115_ai_visual_review VALUES ('+params+')'
 for r in reviews:
  k=(r['tile_set_locator'],int(r['local_id']))
  db=c.execute('SELECT observed_any,provisional_candidate_any_auditable FROM tile_catalog WHERE tile_set_locator=? AND local_id=?',k).fetchone()
  assert db==(1,0),(k,db)
  vals=[int(r[x]) if x in ints else r[x] for x in cols]
  c.execute(sql,vals)
  c.execute("""UPDATE tile_catalog SET v115_ai_identity_candidate=?,v115_ai_part_role=?,
    v115_ai_review_status=?,v115_ai_confidence=? WHERE tile_set_locator=? AND local_id=?""",
    (r['identity_candidate'] or None,r['part_role'] or None,
      r['review_status'],r['confidence'],*k))
 c.execute("""CREATE VIEW v115_ai_candidate_queue AS SELECT tile_set_locator,local_id,identity_candidate,
    part_role,confidence,evidence_sheet,slot FROM v115_ai_visual_review WHERE review_status='candidate'""")
 c.execute("""CREATE VIEW v115_ai_held_queue AS SELECT tile_set_locator,local_id,source_status,
    evidence_sheet,slot FROM v115_ai_visual_review WHERE review_status='held'""")
 c.commit()
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 assert tables.issubset({x[0] for x in c.execute("select name from sqlite_master where type='table'")})
 assert views.issubset({x[0] for x in c.execute("select name from sqlite_master where type='view'")})
 assert c.execute('select count(*) from v115_ai_candidate_queue').fetchone()[0]==882
 assert c.execute('select count(*) from v115_ai_held_queue').fetchone()[0]==6
 assert c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0]==5400
 assert c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0]==4512
 assert c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0]==0
 c.execute('VACUUM')
out=R/'analysis/current/v115';out.mkdir(parents=True,exist_ok=True)
raw=dst.read_bytes(); packed=zlib.compress(raw,6)
b64=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(b64),3000000):
 p=out/f'v115.part{i//3000000:03}.b64'
 p.write_text(b64[i:i+3000000]+'\n',encoding='ascii')
 parts.append(p.relative_to(R).as_posix())
manifest=dict(version='v115',mode='user_requested_model_visual_recheck',
 sqlite_file='tile_visual_v115_unified.sqlite',sqlite_sha256=hashlib.sha256(raw).hexdigest(),
 sqlite_size_bytes=len(raw),compressed_sha256=hashlib.sha256(packed).hexdigest(),compression='zlib_base64',
 parts=parts,base='v113',base_sha256=base['sqlite_sha256'],
 original_observed=5400,previous_auditable_candidates=4512,
 v115_new_ai_visual_candidates=882,v115_held=6,model_viewed_sheets=74,
 mapping_verified=0,tilezed_verified=0,certified=0,
 previous_v113_untouched=True,original_analysis_queue=9,user_excluded_from_active=8,
 source_csv='review/v115_ai_identity/AI_VISUAL_REVIEW_888.csv',
 note='v115 882 model visual FAMILY/PART provisional inferences separately recorded; not 882 individually certified complete identities')
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf8')
state=R/'PROJECT_STATE.json'
s=json.loads(state.read_text('utf8'))
assert s['latest_checkpoint']['version']=='v113'
s['previous_checkpoint_v113']=s['latest_checkpoint']
s['latest_checkpoint']=dict(version='v115',date='2026-10-26',kind='ai_visual_recheck',
 baseline_reconciliation='v113',baseline_unique_observed=5400,new_unique_observed=0,
 new_ai_provisional_candidates=882,new_held=6,model_viewed_sheets=74,
 new_mapping_verified=0,new_tilezed_verified=0,new_final_certified=0,
 merged_unique_observed=5400,remaining_unobserved=9,active_unobserved=1,
 user_excluded_from_active_review=8,auditable_provisional_candidate_keys=4512,
 approved_final_certifications=0,review_evidence='review/v115_ai_identity/AI_VISUAL_REVIEW_888.csv',
 source_visual_sheets='review/v115_model_visual/',extended_context='review/v115_extended_context/',
 notes='882 low-or-medium-confidence AI visual FAMILY/PART guesses are not added to prior audited 4512 without individual mapping verification.')
s['unified_database']=dict(version='v115',status='VERIFIED',
 repo_manifest='analysis/current/v115/MANIFEST.json',
 restore_script='scripts/restore_unified_v115.py',observed_unique=5400,
 remaining_unobserved=9,active_unobserved=1,user_excluded=8,
 auditable_candidates=4512,new_ai_candidate_provisional=882,
 new_ai_held=6,certified=0,sqlite_sha256=manifest['sqlite_sha256'],
 all_prior_tables_preserved=True,image_binaries_in_github=True)
s['latest_ai_visual_recheck']=dict(version='v115',target_count=888,candidate=882,held=6,
 sheets_viewed=74,extended_15x15=8,exact_identity_verified=0,
 mapping_verified=0,final_certified=0,
 warning='Direct model inspection of source contact sheets; mostly family/part candidates (870 low), not 882 fully certified individual identities.')
s['next_actions']=[
 'v115 AI has reviewed 888 prior-image-observed no-candidate keys; 882 got low/medium VISUAL family/part candidate and 6 source holds. Do not call 882 final identities.',
 'Inspect v115_AI_VISUAL_REVIEW_888.csv and sheet refs for source-grounded per-tile candidate; v115 is an independent inference table; prior observed 5400 and prior auditable candidates 4512 unchanged.',
 'PNG/Local ID official mapping and TileZed certification still 0. Validate with TileZed before Minecraft block assignments.',
 'For electrical wires, request 15x15 and larger scenes when 5x5 fails. A1/A2 mapping is provisional.',
 'Preserve 8 user-excluded historical-unobserved and original 9 queue, v113 review statuses, prior 80 user records, all raw PNG/TMX and past SQLite history.'
]
state.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v115 full SQLite 5400 observed, 4512 prior candidate, 882 new visual family candidates, 6 held, certification 0. SHA',manifest['sqlite_sha256'],len(parts),flush=True)
