#!/usr/bin/env python3
"""Publish v189 targeted source verification, retain v188 active queue excluded."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v189_seven_prior_classified_source_recheck/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v189/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v188/MANIFEST.json').read_text())
statefile=R/'PROJECT_STATE.json'
state=json.loads(statefile.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v188'
assert state['latest_checkpoint']['expanded_unique_observed']==9898
assert state['latest_checkpoint']['expanded_unique_unobserved']==144
assert state['latest_checkpoint']['active_review_queue_remaining']==0
assert d['parent']=='v188' and d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['prior_tables_preserved']==250 and d['table_count']==251
assert d['new_rows']==7 and d['new_observed_rows']==0
assert m['seven_prior_A_exterior_part_classifications_reexamined']==7
assert m['alternate_real_TMX_scene_candidates']==2
assert m['no_new_actual_location_available']==5
assert m['newly_observed']==0
assert m['previous_active_review_exclusions_preserved'] is True
assert m['official_mapping_verified']==m['tilezed_verified']==m['certified']==0
state['previous_checkpoint_v188']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update({
 'version':'v189','date':'2026-10-28',
 'kind':'user_explicit_new_targeted_source_reverification_of_7_previous_active_exclusions',
 'physical_unified_sqlite_version':'v189',
 'expanded_unique_observed':9898,'expanded_unique_unobserved':144,
 'expanded_observation_percent':9898/10042*100,
 'active_review_queue_remaining':0,
 'v189_explicit_one_time_recheck':7,
 'v189_new_actual_alternate_TMX_B_C_scenes':2,
 'v189_no_new_valid_site':5,
 'v189_new_provisional_observed':0,
 'v189_changed_pixels_by_index':m['alternate_changed_pixels_by_index'],
 'evidence_repo_path':'review/v189_seven_prior_classified_source_recheck/SEVEN_RECHECK.csv',
 'evidence_manifest':'review/v189_seven_prior_classified_source_recheck/MANIFEST.json',
 'v189_sqlite_sha256':d['sqlite_sha256'],
 'mapping_verified':0,'tilezed_verified':0,'approved_final_certifications':0,
 'caution':'v188 active review exclusion retained. Explicit one-time request only rechecked seven already categorized but original B-C zero candidates; real other TMX locations only for 986/987. No observed or officially mapped certification is inferred from A appearance, nonzero diagnostic difference or an unsupported alternate site.'
})
state['unified_database'].update({
 'version':'v189','status':'VERIFIED_7_HELD_ACTUAL_SOURCE_A_BC_AUDIT_NO_PROMOTION',
 'repo_manifest':'analysis/current/v189/MANIFEST.json',
 'parent_unified_version':'v188','sqlite_sha256':d['sqlite_sha256'],
 'table_count':251,'prior_tables_preserved':250,
 'sqlite_size_bytes':d['sqlite_bytes'],'all_prior_tables_preserved':True,
 'expanded_observed_unique':9898,'expanded_unobserved_unique':144,
 'v189_targeted_source_reverification_rows':7,'certified':0
})
state['latest_v189_evidence']={
 'version':'v189','source_A_RGBA_PNG_SHA_verified':7,'original_B_C_zero_before':7,
 'true_new_original_TMX_placements_rendered':2,
 'alt_diff_pixels':m['alternate_changed_pixels_by_index'],
 'other_five_have_no_untried_actual_84_TMX_site':True,
 'previous_user_exclusion_queue_retained':True,
 'new_observed':0,'total_observed':9898,'remaining_in_checkpoint':144,
 'physical_remaining_unique_keys':142,'bookkeeping_count_gap':2,
 'physical_tables':251,'parent_tables_preserved':250,
 'sqlite_sha256':d['sqlite_sha256'],'official_mapping_verified':0,'certified':0
}
state['next_actions']=[
 'v189: visual inspection of new actual source A/B/C comparison for 986/987; do not promote just because delta is nonzero or A looks like sofa.',
 'v189: five other examined one-occurrence tiles have no alternate source TMX site; require NEW independent evidence, not repeated guesses.',
 'v189: keep v188 user-directed active review exclusions, except explicitly scoped new user request, until new instruction.',
 *state.get('next_actions',[])
]
statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
handoff=(
 '## v189 이전 검수 제외 중 원본 A 실물 분류가 있던 7종의 근거 재검증 (2026-10-28)\n\n'
 '- 최신 사용자 명시 재검수 요청에 따라 v188의 활성 검수 제외를 대량 해제하지 않고, 이미 외형 분류가 기록되었으나 원본 실제 B−C=0이던 **7종**만 대상으로 원본 PNG SHA256·크롭 RGBA 해시·실제 TMX 최초 원본 84맵 발생건수 및 v186 분류를 재대조.\n'
 f"- 986/987 안락의자 부품은 원본 32_46.tmx의 아직 안 쓰던 실제 x235/236,y126 레이어9 층0, raw GID7727/7728에서 A/B/C/DIFF **각 4장 PNG와 접촉시트**를 생성하고 실제 차이 {m['alternate_changed_pixels_by_index']}. 다른 70/974/975/977/1119은 TMX 사용 단 1회로 새 원본 배치가 없어 보류 유지.\n"
 '- 이번 재검수는 새 원본 관찰 판정이나 공식 매핑을 강제하지 않으므로 신규 잠정 관찰 0, **9,898/10,042(98.57%)**, 기록상 미관찰144 및 실물 미관찰142+과거 집계차이2 그대로.\n'
 f"- 물리 SQLite **251테이블**, 기존 v188 부모250개 테이블 모든 행값·행수 보존하고 새 소스재검수 7행 한 테이블 추가. SHA256 {d['sqlite_sha256']}, PRAGMA integrity_check=ok.\n"
 '- 사용자 이전 제외8·수동80·JUMBO held20·D held2 및 원본 TMX84/PNG/기존5409, 과거 모든 파일 보존. v188 활성 검수 제외는 한 회차 사용자 명시 요청 이외 변경되지 않음.\n'
 '- 근거 review/v189_seven_prior_classified_source_recheck/, analysis/current/v189/MANIFEST.json.\n\n---\n'
)
for path in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/path
 old=f.read_text(encoding='utf-8')
 assert 'v188' in old
 split=old.index('\n')
 f.write_text(old[:split+1]+'\n'+handoff+old[split+1:].lstrip('\n'),encoding='utf-8')
print('PASS v189 physical source/SQLite verified',m['alternate_changed_pixels_by_index'],d['sqlite_sha256'],flush=True)
