#!/usr/bin/env python3
"""Advance verified forensic evidence checkpoint without false observed promotions."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v187_missing_neighbor6/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v187/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v186/MANIFEST.json').read_text())
f=R/'PROJECT_STATE.json';state=json.loads(f.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v186'
assert state['latest_checkpoint']['expanded_unique_observed']==9898
assert state['latest_checkpoint']['expanded_unique_unobserved']==144
assert state['unified_database']['version']=='v186'
assert d['version']=='v187' and d['parent']=='v186' and d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==249 and d['prior_tables_preserved']==248
assert d['new_rows']==6 and d['new_observed_rows']==0 and d['integrity_check']=='ok'
assert m['source_incomplete_true_BC_positive_cases']==m['original_B_C_positive']==6
assert m['original_A_and_TMX_source_verified']==6 and m['new_observed']==0
assert m['final_identity_certified']==m['official_mapping_verified']==m['tilezed_verified']==0
state['previous_checkpoint_v186']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v187',date='2026-10-28',
 kind='source_blocker_audit_exact_missing_neighbor_original_key_6_no_promotion',
 physical_unified_sqlite_version='v187',prior_visual_checkpoint='v186',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9898,
 expanded_unique_unobserved=144,expanded_observation_percent=9898/10042*100,
 v187_source_blocked_positive_scenes=6,v187_missing_neighbor_unique_keys=m['missing_neighbor_unique_keys'],
 v187_missing_neighbor_occurrences=m['missing_neighbor_occurrences'],
 v187_new_observed=0,v187_evidence_sheets=6,
 v187_sqlite_sha256=d['sqlite_sha256'],
 evidence_repo_path='review/v187_missing_neighbor6/SOURCE_BLOCKED_6.csv',
 evidence_manifest='review/v187_missing_neighbor6/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='Original source A and actual TMX B-C are confirmed positive for all six tiles but neighbor source A PNG evidence is absent. Actual missing neighbor tile keys audited; no fake sprite, no altered official image, no new observed. Total 9898/10042 unchanged; 144 checkpoint unseen includes 2 historical reconciliation cases.'
))
state['unified_database'].update(dict(
 version='v187',status='VERIFIED_MISSING_SOURCE_EVIDENCE_NOT_NEW_IDENTITIES',
 repo_manifest='analysis/current/v187/MANIFEST.json',parent_unified_version='v186',
 sqlite_sha256=d['sqlite_sha256'],table_count=249,prior_tables_preserved=248,
 sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9898,expanded_unobserved_unique=144,
 new_4633_observed=4498,new_4633_unobserved=135,
 v187_source_missing_audit_rows=6,certified=0
))
state['latest_v187_evidence']=dict(
 version='v187',source_blocked_targets=6,targets=[197,198,685,4408,4409,3104],
 original_B_C_positive_verified=6,
 missing_neighbor_occurrences=m['missing_neighbor_occurrences'],
 missing_neighbor_unique_keys=m['missing_neighbor_unique_keys'],
 missing_neighbor_ids=m['missing_neighbor_ids'],
 original_84_TMX_alt_5x5_sites=0,newly_observed=0,
 observed_total=9898,unobserved_remaining=144,
 db_tables=249,parent_tables_preserved=248,
 db_sha256=d['sqlite_sha256'],mapping_verified=0,tilezed_verified=0,certified=0)
state['next_actions']=[
 'v187: resolve exact source A PNG and crop mapping for the missing neighbor tile keys identified in review/v187_missing_neighbor6/MISSING_NEIGHBOR_KEYS.csv; only then rerender full original six B/C contexts.',
 'v187: do not treat six positive B-C pixel-delta source-blocked tiles as observed or material-certified without complete original neighborhood evidence and human visual confirmation.',
 'v187: remaining checkpoint 144 includes 135 new, 9 historical, two-item unresolved accounting discrepancy; do not inflate progress.',
 *state.get('next_actions',[])
]
f.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v187 기존 B−C 양수·주변 원본 PNG 누락 6종의 정확한 방해 원본 키 감사 (2026-10-28)\n\n'
 '- 원본 camping_04 197/198, fixtures_counters_01 685, 욕실 벽 4408/4409, 밭작물 3104 등 총 **6종**을 원본 PNG A 및 실제 원본 TMX raw GID·좌표·층·레이어·SHA로 재조립. 각각 원본 RGB B−C가 100픽셀 이상 바뀌지만 진짜 주변 PNG 누락으로 보류된 사유를 직접 열거하고 CSV/비교 이미지 6장/원본 24 PNG 증거 ZIP으로 보관.\n'
 f"- 누락 원본 이웃 **{m['missing_neighbor_occurrences']}회**, 고유 누락 키 **{m['missing_neighbor_unique_keys']}종**을 정확한 타일셋/Local ID로 분리. 원본 84 TMX 조사에서 이 6개는 추가 다른 5×5 대체 장소 없음. 누락된 이웃을 임의 타일 이미지로 대체하지 않음.\n"
 f"- SQLite **249테이블**, v186의 248개 부모 테이블 모든 행·값 보존하고 별도 소스 방해 감사 6행만 추가. SHA256 {d['sqlite_sha256']}, PRAGMA integrity_check=ok.\n"
 '- 신규 잠정 관찰 0, 누적 이미지 잠정 관찰 **9,898/10,042(98.57%)**, 미관찰 144종 유지. 공식 Local ID/TileZed 대응 및 최종 사물 정체 인증0. 역사적 집계 차이2 미해결.\n'
 '- 원본 84 TMX/Tiles PNG, 기존 5409·수동80·제외14·held D2/JUMBO20 및 역사적 SQLite/CSV/증거 불변. 사용자 정의 D 같은 키 다른 공식 A 실험 미수행.\n'
 '- 근거 review/v187_missing_neighbor6/ 및 analysis/current/v187/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel;txt=p.read_text(encoding='utf-8')
 assert 'v186' in txt
 ix=txt.index('\n')
 p.write_text(txt[:ix+1]+'\n'+summary+txt[ix+1:].lstrip('\n'),encoding='utf-8')
print('PASS v187 source missing neighbor verified; preserve observed 9898/10042',d['sqlite_sha256'])
