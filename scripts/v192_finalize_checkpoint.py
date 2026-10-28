#!/usr/bin/env python3
"""v192 source-verified A-first provisional observations and 33 holds; keep historical
v188 excluded rows and v190 parent tables exactly unchanged, re-open active queue.
"""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v192_image_first_TMX_BC_142/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v192/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v190/MANIFEST.json').read_text())
q=R/'PROJECT_STATE.json';state=json.loads(q.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v190'
assert state['latest_checkpoint']['expanded_unique_observed']==9898
assert state['latest_checkpoint']['expanded_unique_unobserved']==144
assert state['latest_v191_explicit_142_reopen']['actual_A_image_verified_and_viewed']==132
assert state['unified_database']['version']=='v190' and state['unified_database']['table_count']==252
assert d['version']=='v192' and d['parent']=='v190' and d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==253 and d['prior_tables_preserved']==252 and d['new_rows']==142
assert d['new_observed_rows']==109 and d['integrity_check']=='ok'
assert m['total']==142 and m['A_RGBA_sha_verified']==m['TMX_raw_GID_and_exact_key_verified']==132
assert m['A_visible_high']==60 and m['A_visible_medium']==49
assert m['new_A_first_provisional_observations']==109 and m['new_B_C_zero_occluded_in_accepted']==99
assert m['A_ambiguous_low_held']==23 and m['exact_A_unavailable_held']==10
assert m['image_observed_now']==10007 and m['remaining_checkpoint']==35
assert m['physical_unique_unobserved_remaining']==33 and m['historical_two_count_gap']==2
assert m['official_mapping_verified']==m['tilezed_verified']==m['certified']==0
state['previous_checkpoint_v190']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v192',date='2026-10-28',kind='image_first_original_A_shape_verified_with_real_TMX_GID_BC_109_provisional',
 physical_unified_sqlite_version='v192',prior_visual_checkpoint='v190',source_image_review_checkpoint='v191',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=10007,expanded_unique_unobserved=35,
 expanded_observation_percent=10007/10042*100,
 original_5409_observed_preserved=5400,original_5409_unobserved_preserved=9,
 new_image_observed=4607,new_keys_unobserved=26,
 v192_reopened_checked=142,v192_A_RGBA_and_original_TMX_verified=132,
 v192_new_A_first_source_provisional=109,v192_actual_B_C_positive_in_promoted=10,
 v192_actual_B_C_zero_occluded_in_promoted=99,
 v192_original_coverage_missing_neighbors_in_promoted=6,
 v192_low_confidence_A_held=23,v192_exact_A_unavailable=10,
 v192_remaining_physical_unique=33,v192_historical_checkpoint_gap=2,
 active_review_queue_remaining=33,active_review_excluded_actual_distinct_keys=0,
 v188_previous_exclusion_history_preserved=True,
 v192_original_A_source_primary=True,
 v192_source_evidence='review/v192_image_first_TMX_BC_142/CROSSCHECK_142.csv',
 v192_evidence_manifest='review/v192_image_first_TMX_BC_142/MANIFEST.json',
 v192_sqlite_sha256=d['sqlite_sha256'],
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='109 new PROVISIONAL source-A visual observations with exact source PNG crop pixel hash AND original TMX source key GID provenance, NOT final identity certified. 99 real B-C=0 because original full map occludes the A sprite; these 99 are A image-only provisional interpretations and MUST NOT be claimed as visually exposed in B. 6 source neighbor gaps remain. 23 low A and 10 exact-A unavailable held. Physical missing 33+unresolved historical count difference 2=checkpoint35.'
))
state['unified_database'].update(dict(
 version='v192',status='SOURCE_IMAGE_FIRST_PROVISIONAL_NOT_OFFICIAL_ID',
 repo_manifest='analysis/current/v192/MANIFEST.json',
 parent_unified_version='v190',sqlite_sha256=d['sqlite_sha256'],
 table_count=253,prior_tables_preserved=252,all_prior_tables_preserved=True,
 sqlite_size_bytes=d['sqlite_bytes'],expanded_observed_unique=10007,expanded_unobserved_unique=35,
 new_4633_observed=4607,new_4633_unobserved=26,v192_reopened_review_rows=142,v192_new_provisional_observed=109,
 active_review_remaining=33,certified=0
))
state['latest_v192_crosscheck']={
 'version':'v192','reopened_total':142,'original_A_RGBA_verified':132,'original_TMX_raw_GID_verified':132,
 'high_A_image_appearance':60,'medium_A_image_appearance':49,
 'new_A_based_provisional':109,'A_based_true_B_C_positive':10,'A_based_true_B_C_zero':99,
 'held_low_A_ambiguous':23,'held_exact_A_missing':10,
 'observed_total':10007,'unobserved_checkpoint':35,'physical_unique_missing':33,
 'historical_two_count_gap':2,'db_sha256':d['sqlite_sha256'],
 'physical_db_tables':253,'parent_tables_preserved':252,
 'official_mapping_verified':0,'tilezed_verified':0,'identity_certified':0
}
state['next_actions']=[
 'v192: re-examine the remaining 23 low-confidence A fragments, requiring neighboring sprite group and exact TMX placement; never call B-C zero transparent.',
 'v192: find exact original A atlas and crop for historical 9 + missing new overlay_graffiti_wall_02/2, never infer an official Local ID from a filename.',
 'v192: distinguish 99 A-visible but actual B-C-occluded provisional candidates from 10 actual B-C positive; none are official TileZed or final identity certified.',
 'v192: reconcile two bookkeeping count differences; remaining 33 genuine distinct keys are all back in active review queue.',
 *state.get('next_actions',[])
]
q.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v192 — 재개 142종 원본 A 자체 + 진짜 TMX B/C 교차검증 (2026-10-28)\n\n'
 '- **v191 원본 A 직접 시각판독132종** 중 high60·medium49를 그대로 원본 PNG A 픽셀검증 및 실제 TMX raw GID/tileset firstgid/layer/level/x/y 일치 확인 후 **신규 109종 A 기반 잠정 이미지 관찰**로 등록. '
 '이는 확정 사물명이나 TileZed 공식 Local ID가 아님. 23종 원본 A 단편·10종 정확한 A 미확보는 보류.\n'
 '- 실제 84 TMX 원본 B/C 재검수 근거: v182 진짜 TMX 장면/해당 raw GID 제거 증거 ZIP 전체 SHA256·CRC, 진단 마스킹과 원래 장면 혼동 금지. '
 '**109종 중 원래 B-C 변화양수 10, 변화0·가림 99**. 99종은 실제 B에서 보인 것이 아니라 **원본 A 그 자체만 형태를 읽은 잠정 관찰**이므로 일체 최종 인증/공식 매핑 아님. 주변 원본 PNG 누락 가능성 6종도 분리 기록.\n'
 '- 물리 SQLite v190의 **252개 기존 테이블 모든 행·값과 행수 보존**, v192에 142개 출처/임시후보/보류 근거행 1테이블 추가하여 **253테이블**. 신규 잠정 관찰109. '
 f'SQLite SHA256 {d["sqlite_sha256"]}, integrity_check=ok.\n'
 '- 기록상 누적 이미지 잠정 관찰 **10,007/10,042 (99.65%)**, 기록상 미관찰35종=실제 키33종+과거 집계 차이2. '
 '해결된 109종을 과거 v188 활성 제외에서 다시 연 상태로 기록했고, 아직 33종이 활성 검수 범위. '
 '공식 PNG↔LocalID/TileZed/최종 정체 인증은 모두0.\n'
 '- 원본 PNG/TMX, 5409/수동80/과거 제외14·D/JUMBO held 및 기존 이력 보존. 사용자 D는 같은 키 다른 공식 A를 기존 B 같은 위치에 대입하는 방식으로 미수행. '
 '근거 review/v192_image_first_TMX_BC_142/ 와 review/v191_reopen142_A_first/, review/v182_occlusion202/.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;s=f.read_text(encoding='utf-8')
 assert 'v191' in s
 j=s.index('\n');f.write_text(s[:j+1]+'\n'+summary+s[j+1:].lstrip('\n'),encoding='utf-8')
print('PASS v192 A-first 109 new source-backed provisional, 99 actual B-C zero and occluded, 33 genuine remaining plus historical gap2',d['sqlite_sha256'])
