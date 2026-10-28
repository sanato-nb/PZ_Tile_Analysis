#!/usr/bin/env python3
"""v188 explicit user-directed ACTIVE REVIEW exclusions; not observations.

Recompute actual missing tile keys using the unmodified physical SQLite.
Preserve the user's historic 8 exclusions and f_bushes provisional preference
as audit evidence. Exclude all still-unresolved keys only from the *active
work queue*, not from the historical unobserved count or official certification.
"""
from pathlib import Path
from collections import Counter
import base64,csv,hashlib,json,sqlite3,zlib
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v188_active_review_exclusions'
DBOUT=R/'analysis/current/v188'
OUT.mkdir(parents=True,exist_ok=True);DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def read_csv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def idx_by_key(path):
 return {(r['tile_set_name'],int(r['local_id'])):r for r in read_csv(R/path)}
p=json.loads((R/'analysis/current/v187/MANIFEST.json').read_text())
assert p['version']=='v187' and p['table_count']==249
data=base64.b64decode(''.join((R/x).read_text('ascii').strip() for x in p['parts']),validate=True)
assert sha(data)==p['compressed_sha256']
raw=zlib.decompress(data)
assert sha(raw)==p['sqlite_sha256'] and len(raw)==p['sqlite_bytes']
path=Path('/tmp/pz-v188-disposition.sqlite')
path.write_bytes(raw)
db=sqlite3.connect(path)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==249 and before['v187_missing_neighbor_audit']==6
# Historical source-confirmed provisional observations, deduplicated by actual key.
observed=set()
for name in ['v132_visual3_jumbo20','v133_visual_review_32']+['v%d_visual_review'%i for i in range(134,175)]+['v177_visual_review','v179_visual_review','v181_visual_review','v183_visual_review','v184_visual_review','v185_visual_review']:
 observed.update((x[0],int(x[1])) for x in db.execute('SELECT tile_set_name,local_id FROM "'+name+'"'))
for name in ['v122_ai_visual_review_160','v125_ai_visual_spotcheck_20']:
 observed.update((x[0],int(x[1])) for x in db.execute('SELECT tile_set_name,local_id FROM "'+name+'" WHERE review_status=?',('provisional_candidate',)))
assert len(observed)==4500,('source_distinct_prior_provisionals',len(observed))
A=read_csv(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
assert len(A)==4633
new={}
for index,r in enumerate(A):
 k=(r['tile_set_name'],int(r['local_id']))
 assert k not in new
 new[k]=(index,r)
pending={k:('new_4633',idx,r) for k,(idx,r) in new.items() if k not in observed}
assert len(pending)==133,('new_pending',len(pending))
old=json.loads((R/'review/v175_remaining381_evidence_audit/OLD_NINE_UNOBSERVED.json').read_text())
assert len(old)==9
history_excluded=0;history_keep=0
for row in old:
 k=(row['tile_set_name'],int(row['local_id']))
 assert k not in pending and k not in observed and k not in new
 d=row['source_catalog_record']
 assert int(d['observed_any'])==0
 action=d['v113_user_review_action']
 assert action in ('exclude_from_active_review','keep_provisional')
 history_excluded+=action=='exclude_from_active_review'
 history_keep+=action=='keep_provisional'
 pending[k]=('original_5409',None,d)
assert len(pending)==142 and history_excluded==8 and history_keep==1
src_175=idx_by_key('review/v175_remaining381_evidence_audit/REMAINING_381_EVIDENCE_AUDIT.csv')
src_180=idx_by_key('review/v180_remnant239_multisite/UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv')
src_182=idx_by_key('review/v182_occlusion202/SOURCE_OCCLUSION_202.csv')
src_183=idx_by_key('review/v183_original_BC_visual65/HELD_137.csv')
src_187=idx_by_key('review/v187_missing_neighbor6/SOURCE_BLOCKED_6.csv')
classified_49=idx_by_key('review/v186_object_disambiguation_49/RECLASSIFIED_49.csv')
assert len(classified_49)==49 and not (set(classified_49)&set(pending)),('already classified counted as still pending',set(classified_49)&set(pending))
rows=[]
for key in sorted(pending):
 origin,index,record=pending[key]
 s175=src_175.get(key,{})
 s180=src_180.get(key,{})
 s182=src_182.get(key,{})
 s183=src_183.get(key,{})
 s187=src_187.get(key,{})
 old_action=record.get('v113_user_review_action','') if origin=='original_5409' else ''
 if origin=='original_5409':
  category='historical_user_excluded' if old_action=='exclude_from_active_review' else 'historical_keep_provisional_not_source_observed'
  evidence=f'Historical v113 action: {old_action}; old tile_catalog observed_any=0. Preserve original record exactly.'
 elif s187:
  category='original_neighborhood_source_missing'
  evidence='v187 original B-C changed, but one or more adjacent original sprite pixels unavailable; do not certify object.'
 elif s183.get('reason')=='original_A_missing_source_and_B_C_evidence' or record.get('selection_status')=='held_missing_source':
  category='original_A_unavailable'
  evidence='Original selected A is missing; a different unofficial A is not permitted as a substitute.'
 elif s183.get('reason'):
  category='previously_reviewed_visual_or_occlusion_held'
  evidence='v183 hold: '+s183['reason']+'; no additional independent original human-readable evidence recorded.'
 elif s182.get('classification'):
  category='actual_scene_source_evidence_insufficient'
  evidence='v182: '+s182['classification']+'; original B-C pixels='+s182.get('actual_B_C_pixels','')
 elif s180.get('status'):
  category='no_reliable_new_source_scene'
  evidence='v180: '+s180['status']+'; '+s180.get('prior_hold_reason','')
 elif s175.get('reason'):
  category='original_scene_unresolved'
  evidence='v175: '+s175['reason']
 else:
  category='previous_source_evidence_unresolved'
  evidence='Physical source key found in original A records but no independent final visual proof.'
 # Explicit user instruction EXCLUDES from active queue, NOT historical observation or final identity.
 rows.append(dict(tile_set_name=key[0],local_id=key[1],origin=origin,
  source_A_index='' if index is None else index,
  previous_user_action=old_action,
  previous_source_reason=s183.get('reason') or s175.get('reason') or s180.get('prior_hold_reason') or '',
  source_blocker_category=category,
  evidence_note=evidence,
  disposition='excluded_from_active_review_per_latest_user_instruction',
  disposition_scope='only_future_repeat_review_work_queue_not_historical_source_or_certification',
  previous_source_key_observed=0,
  new_observed=0,official_mapping_verified=0,tilezed_verified=0,final_identity_certified=0))
assert len(rows)==142 and len({(r['tile_set_name'],r['local_id']) for r in rows})==142
assert all((r['tile_set_name'],r['local_id']) not in observed for r in rows)
assert sum(x['origin']=='original_5409' for x in rows)==9
assert sum(x['origin']=='new_4633' for x in rows)==133
assert sum(x['source_blocker_category']=='original_neighborhood_source_missing' for x in rows)==6
fields=list(rows[0])
csvpath=OUT/'EXCLUDED_FROM_ACTIVE_REVIEW_142.csv'
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
categories=dict(Counter(x['source_blocker_category'] for x in rows))
assert sum(categories.values())==142
ledger=dict(version='v188',parent='v187',policy='user_directed_exclusion_from_active_review_only',
 original_unique_TMX_keys=10042,checkpoint_observed=9898,checkpoint_unobserved=144,
 physical_ever_provisionally_observed_new=4500,
 physically_unobserved_new=133,physically_unobserved_old=9,physically_unobserved_distinct=142,
 historical_checkpoint_two_count_difference=2,
 old_nine_prior_user_excluded=8,old_nine_prior_kept_provisional=1,
 previously_reclassified_49_already_observed=49,already_classified_overlap_pending=0,
 newly_observed_this_version=0,reviewed_for_scope_disposition=142,
 excluded_from_active_review_unique=142,
 accounting_only_unresolved_nonkey_count=2,
 active_review_queue_remaining=0,
 exclude_means_final_certification=False,
 official_mapping_verified=0,tilezed_verified=0,final_identity_certified=0,
 source_blocker_distribution=categories,
 source_evidence_reference_paths=[
  'review/v175_remaining381_evidence_audit/OLD_NINE_UNOBSERVED.json',
  'review/v180_remnant239_multisite/UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv',
  'review/v182_occlusion202/SOURCE_OCCLUSION_202.csv',
  'review/v183_original_BC_visual65/HELD_137.csv',
  'review/v186_object_disambiguation_49/RECLASSIFIED_49.csv',
  'review/v187_missing_neighbor6/SOURCE_BLOCKED_6.csv'])
(OUT/'COUNT_RECONCILIATION.json').write_text(json.dumps({
 'checkpoint_unobserved':144,'distinct_source_unobserved_keys':142,
 'historical_count_gap_without_distinct_tile_key':2,
 'active_review_exclusions':142,'active_review_queue_after_user_exclusion':0,
 'not_implied':['144 new identities observed','official Local ID mapping verified','final identities certified','historical 9898 modified'],
 'explicit_user_instruction':'Exclude remaining insufficiently resolved entries from work queue, preserve evidence and source statuses.'
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ints={'local_id','source_A_index','previous_source_key_observed','new_observed','official_mapping_verified','tilezed_verified','final_identity_certified'}
db.execute('CREATE TABLE v188_active_review_disposition ('+
 ','.join('"'+k+'" '+('INTEGER' if k in ints else 'TEXT') for k in fields)+
 ',PRIMARY KEY(tile_set_name,local_id),CHECK(new_observed=0 AND official_mapping_verified=0 AND tilezed_verified=0 AND final_identity_certified=0))')
db.executemany('INSERT INTO v188_active_review_disposition ('+','.join('"'+k+'"' for k in fields)+') VALUES ('+
 ','.join('?' for _ in fields)+')',[tuple(row[k] for k in fields) for row in rows])
db.commit()
after={name:db.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==250 and set(after)-set(before)=={'v188_active_review_disposition'}
assert all(after[k]==v for k,v in before.items()) and after['v188_active_review_disposition']==142
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=path.read_bytes();compressed=zlib.compress(newraw,8)
encoded=base64.b64encode(compressed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
 f=DBOUT/f'v188.part{i//3000000:03}.b64';f.write_text(encoded[i:i+3000000],encoding='ascii');parts.append(f.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/q).read_text('ascii') for q in parts))))==sha(newraw)
dbm=dict(version='v188',parent='v187',parent_sqlite_sha256=p['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(compressed),sqlite_bytes=len(newraw),
 parts=parts,table_count=250,prior_tables_preserved=249,new_rows=142,
 new_observed_rows=0,active_review_excluded_rows=142,active_review_remaining=0,
 integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
ledger.update(csv_sha256=sha(csvpath.read_bytes()),sqlite_sha256=sha(newraw),
 physical_database_tables=250,all_prior_tables_preserved=249)
(OUT/'MANIFEST.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v188 사용자 요청: 남은 타일을 기존 검수 건수에서 제외 (원본·정체 인증 불변)\n\n'
 '남은 144종이라는 상태 숫자는 물리 SQLite에서 확인된 서로 다른 미관찰 실제 키 142개와 2건의 역사적 체크포인트 집계 차이로 이루어져 있습니다. 원본 자료와 과거 기록을 보존한 상태로 142개를 "활성 반복 검수 대상에서 제외" 처리하고 역사적 집계 차이 2건은 가짜 타일을 만들지 않고 별도 기록했습니다.\n'
 '과거 9개 미관찰 중 8개는 애초 v113부터 활성 검수 제외였고, f_bushes_1/66 하나는 과거 keep_provisional로 지정됐습니다. 해당 역사적 상태 자체는 변경하지 않고 이번 사용자의 최신 지시 범위에 따라 작업 큐에서만 제외했습니다.\n'
 'v186에서 물체 정체를 재분류한 49종은 이미 관찰 기록에 들어 있어 이중으로 미처리 건수에서 빼지 않습니다. v187 B-C 양수 6종은 누락된 jumbo_tree_01/0 주변 원본 이미지가 여전히 없다는 차단 사유로 분류하되 기존 A/B/C와 DB 증거를 보존했습니다.\n'
 '따라서 활성 검수 잔여 **0건**이고 실물 이미지 잠정 관찰 기록 9,898/10,042(98.57%), 역사적 미관찰144, 공식 PNG↔Local ID·TileZed·최종 정체 인증0은 변경되지 않았습니다. 제외는 관찰/인증이 아닙니다. 필요한 경우 개별 키의 제외를 해제해 다시 검수할 수 있습니다.\n'
 '모든 원본 84 TMX, PNG 타일셋, 사용자 수동 검수80·제외14·held D2/JUMBO20·과거 자료 전부 유지하고 v187의 249개 물리 SQLite 테이블을 전체 행 값/행 수 그대로 보존, v188 작업 상태 테이블 142행만 추가(총250테이블).\n',
 encoding='utf-8')
print('PASS v188 user-scoped exclusion',json.dumps(ledger,ensure_ascii=False),flush=True)
