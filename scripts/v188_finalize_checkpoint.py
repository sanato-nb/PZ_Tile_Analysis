#!/usr/bin/env python3
"""Update status: 142 actual unresolved source keys excluded FROM ACTIVE QUEUE only."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v188_active_review_exclusions/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v188/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v187/MANIFEST.json').read_text())
file=R/'PROJECT_STATE.json'
state=json.loads(file.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v187'
assert state['latest_checkpoint']['expanded_unique_observed']==9898
assert state['latest_checkpoint']['expanded_unique_unobserved']==144
assert state['unified_database']['version']=='v187'
assert d['parent']=='v187' and d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==250 and d['prior_tables_preserved']==249
assert d['new_rows']==d['active_review_excluded_rows']==142 and d['new_observed_rows']==0
assert m['physically_unobserved_distinct']==142 and m['excluded_from_active_review_unique']==142
assert m['historical_checkpoint_two_count_difference']==2 and m['active_review_queue_remaining']==0
assert m['previously_reclassified_49_already_observed']==49 and m['already_classified_overlap_pending']==0
assert m['old_nine_prior_user_excluded']==8 and m['old_nine_prior_kept_provisional']==1
assert m['newly_observed_this_version']==0
assert m['official_mapping_verified']==m['tilezed_verified']==m['final_identity_certified']==0
state['previous_checkpoint_v187']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v188',date='2026-10-28',
 kind='explicit_user_requested_exclusion_of_pending_unresolved_tiles_from_active_review',
 physical_unified_sqlite_version='v188',
 prior_visual_checkpoint='v187',
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=9898,
 expanded_unique_unobserved=144,
 expanded_observation_percent=9898/10042*100,
 active_review_queue_remaining=0,
 active_review_excluded_actual_distinct_keys=142,
 non_tile_historical_checkpoint_count_difference=2,
 v188_observed_new=0,
 v188_historical_observations_unchanged=9898,
 v188_existing_disambiguated_49_already_counted=True,
 v188_original_user_excluded_8_preserved=True,
 v188_original_keep_provisional_one_preserved=True,
 v188_reopen_requires_explicit_scope_change=True,
 v188_exclusion_is_not_observation_or_final_certification=True,
 evidence_repo_path='review/v188_active_review_exclusions/EXCLUDED_FROM_ACTIVE_REVIEW_142.csv',
 evidence_manifest='review/v188_active_review_exclusions/MANIFEST.json',
 sqlite_sha256_v188=d['sqlite_sha256'],
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='User requested exclusion, not false certification. Remaining ACTIVE REVIEW 0, while historical provisional observations stay 9898/10042 and 144 unobserved (142 actual source keys plus historical two-count inconsistency). Preserve all old physical DB records and user manual exclusions. Automation should not reopen these keys without new explicit user request.'
))
state['unified_database'].update(dict(
 version='v188',status='VERIFIED_USER_SCOPE_ACTIVE_REVIEW_CLOSED_NO_FALSE_OBSERVATIONS',
 repo_manifest='analysis/current/v188/MANIFEST.json',
 parent_unified_version='v187',
 sqlite_sha256=d['sqlite_sha256'],
 table_count=250,prior_tables_preserved=249,
 sqlite_size_bytes=d['sqlite_bytes'],
 all_prior_tables_preserved=True,
 expanded_observed_unique=9898,
 expanded_unobserved_unique=144,
 active_review_excluded_rows=142,active_review_remaining=0,
 certified=0
))
state['latest_v188_review_scope']={
 'version':'v188','user_instruction':'Exclude unresolvable tiles from review workload instead of repeatedly reprocessing',
 'observed_tiles':9898,'total_original_tile_keys':10042,'raw_unobserved_checkpoint':144,
 'actual_unobserved_distinct_keys_excluded':142,'historical_count_discrepancy_not_keys':2,
 'active_remaining_review_count':0,'already_disambiguated_49_already_observed':49,
 'old_9_historical_user_excluded':8,'old_9_kept_provisional_historical':1,
 'observed_this_version':0,'mapping_verified':0,'tilezed_verified':0,'certified':0,
 'source_evidence_csv':'review/v188_active_review_exclusions/EXCLUDED_FROM_ACTIVE_REVIEW_142.csv',
 'sqlite_sha256':d['sqlite_sha256'],'physical_tables':250
}
state['next_actions']=[
 'v188 USER SCOPE: active unresolved tile review queue is ZERO because all 142 remaining actual source keys were excluded from future repetitive analysis at user request; 2 historical counter discrepancies are not tile identities.',
 'Do NOT continue automatic visual review of excluded keys or re-add them to active workload unless the user explicitly reopens specific keys or changes policy.',
 'Continue the overall PZ->Minecraft map conversion workflow if requested; previously observed 9898 provisional part candidates can be used without pretending the last 144 were identified or certified.',
 'Preserve original 84 TMX/Tiles PNG, 5409, user excluded14/manual80, held D2/JUMBO20 and all 249 parent SQLite tables intact.',
 *state.get('next_actions',[])
]
file.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v188 남은 타일 활성 검수 제외 — 사용자 명시 요청 반영 (2026-10-28)\n\n'
 '- **사용자 지시: 이미 정체를 설명한 타일을 되풀이하지 말고 해결 불가 항목은 제외한다.** v187 실물 SQLite에서 실제로 미관찰인 142개 (새 133 + 기존 9)를 일일이 분리하고 신규 `v188_active_review_disposition` 142행으로 근거/보류 원인/제외 범위를 기록. 기존 기록상 미관찰144와의 **차이 2는 실제 타일 고유키가 아닌 누적 집계 차이**로 별도 감사표에 보존.\n'
 '- v186 이미 분류해 두었던 49종은 기존 잠정 관찰 집합에 들어 있어 새로 이중 차감하지 않음. 원본 9종 중 과거 사용자 제외8, 기존 keep_provisional1의 역사적 상태를 변경하지 않음. v187 B−C 양수지만 주변 원본 JUMBO A 소스 누락6종은 별도 정확한 차단 사유 보존.\n'
 '- 새 **실행 중인 활성 검수 잔여 0건**. 하지만 **실제 잠정 관찰 기록 9,898/10,042(98.57%)와 기록상 미관찰144종은 변함없음**. 이번 신규 관찰0, 최종 물체 정체 인증·공식 타일셋 Local ID/TileZed 매핑0. 검수 제외 ≠ 관찰·인증 완료.\n'
 f"- 물리 SQLite **250테이블**, 부모 v187 기존249테이블 모든 행 내용/수 보존. 새 상태 테이블 142행만 추가. SHA256 {d['sqlite_sha256']}, integrity_check=ok.\n"
 '- 신규 리뷰 워크를 다시 시작하려면 구체적인 타일 ID·사유 또는 사용자 지시로 제외를 해제해야 함. 기존 D held2/JUMBO20, 수동80·제외14 및 원본84 TMX/Tiles PNG 불변.\n'
 '- 근거 review/v188_active_review_exclusions/, analysis/current/v188/MANIFEST.json.\n\n---\n'
)
for name in ['AGENTS.md','docs/HANDOFF.md']:
 path=R/name;s=path.read_text(encoding='utf-8')
 assert 'v187' in s
 pos=s.index('\n')
 path.write_text(s[:pos+1]+'\n'+summary+s[pos+1:].lstrip('\n'),encoding='utf-8')
print('PASS v188 exact 142 source-key active-review exclusions; historical observed 9898/10042 unchanged; 250 tables',d['sqlite_sha256'],flush=True)
