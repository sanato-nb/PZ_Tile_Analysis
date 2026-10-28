#!/usr/bin/env python3
"""Finalize v180 exploratory evidence without confusing rendered scenes with observations."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v180_remnant239_multisite/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v180/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v179/MANIFEST.json').read_text())
q=R/'PROJECT_STATE.json';state=json.loads(q.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v179'
assert state['latest_checkpoint']['expanded_unique_observed']==9792 and state['latest_checkpoint']['expanded_unique_unobserved']==250
assert state['unified_database']['sqlite_sha256']==p['sqlite_sha256']
assert m['actual_distinct_new_A_missing_keys']==239 and m['historical_missing_old_keys']==9
assert m['checkpoint_missing']==250 and m['physical_missing_total']==248 and m['unreconciled_difference']==2
assert 0<m['new_TMX_context_candidates_rendered']<=64
assert m['source_candidates_with_positive_new_B_C']+m['source_candidates_with_new_B_C_zero']==m['new_TMX_context_candidates_rendered']
assert m['new_observed']==m['official_mapping_verified']==m['tilezed_verified']==m['final_identity_certified']==0
assert d['version']=='v180' and d['parent']=='v179' and d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==242 and d['prior_tables_preserved']==241 and d['new_observed_rows']==0
state['previous_checkpoint_v179']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v180',date='2026-10-28',kind='all_239_remaining_new_key_multiple_additional_actual_TMX_scene_census_and_selective_render',
 physical_unified_sqlite_version='v180',prior_visual_checkpoint='v179',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9792,expanded_unique_unobserved=250,
 expanded_observation_percent=9792/10042*100,
 v180_remaining_new_unique_keys_censused=239,
 v180_alternative_fresh_site_candidates=m['original_source_keys_with_fresh_untried_inbounds_sites'],
 v180_no_fresh_site=m['original_source_keys_without_untried_5x5_sites'],
 v180_source_scenes_rendered=m['new_TMX_context_candidates_rendered'],
 v180_new_B_C_positive=m['source_candidates_with_positive_new_B_C'],
 v180_new_B_C_zero=m['source_candidates_with_new_B_C_zero'],
 v180_newly_provisional_observed=0,
 v180_hist_missing_old=9,v180_historical_count_discrepancy=2,
 evidence_repo_path='review/v180_remnant239_multisite/UNOBSERVED_239_ADDITIONAL_SITE_CENSUS.csv',
 evidence_manifest='review/v180_remnant239_multisite/MANIFEST.json',
 v180_sqlite_sha256=d['sqlite_sha256'],mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='Actual source GID, new independent 5x5 original TMX and B-C subtraction only. No visual identity or transparency certification from scene reconstruction; manual visual review required before provisional observation. Two historical count discrepancies remain unresolved.'
))
state['unified_database'].update(dict(
 version='v180',status='VERIFIED_MULTISITE_ORIGINAL_TMX_EVIDENCE_NOT_OBSERVED',
 repo_manifest='analysis/current/v180/MANIFEST.json',
 parent_unified_version='v179',sqlite_sha256=d['sqlite_sha256'],
 table_count=242,prior_tables_preserved=241,sqlite_size_bytes=d['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=9792,expanded_unobserved_unique=250,
 v180_multisite_evidence_rows=m['new_TMX_context_candidates_rendered'],certified=0
))
state['latest_v180_evidence']=dict(
 version='v180',censused_original_new_keys=239,
 additional_untried_key_sites=m['original_source_keys_with_fresh_untried_inbounds_sites'],
 no_additional_available_sites=m['original_source_keys_without_untried_5x5_sites'],
 newly_rendered_original_B_C_scenes=m['new_TMX_context_candidates_rendered'],
 positive_new_delta=m['source_candidates_with_positive_new_B_C'],
 zero_new_delta=m['source_candidates_with_new_B_C_zero'],
 new_provisional_observations=0,observed_total=9792,remaining_checkpoint=250,
 physical_missing_keys=248,unreconciled_difference=2,
 original_old_missing_keys=9,db_tables=242,db_sha256=d['sqlite_sha256'],
 official_mapping_verified=0,tilezed_verified=0,certified=0
)
state['next_actions']=[
 'v180: directly visually inspect new A/B/C contact sheets and select only source-verified, recognizable delta-positive candidates for v181 provisional review.',
 'v180: unresolved new-key tiles without any additional 5x5 source location cannot be completed by reusing the same TMX position; find official source or alternative evidence.',
 'v180: old 9 and unresolved two-count checkpoint mismatch remain under strict hold, never assume TileZed/official mapping.',
 *state.get('next_actions',[])
]
q.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v180 미관찰 새 원본키 239종의 실제 TMX 다중 위치 전수검사 및 2차 A/B/C 배치 생성 (2026-10-28)\n\n'
 f"- 부모 v179에 없는 새 A 원본 키 **239종**을 84개 원본 TMX에서 raw GID 기준 재검색. 기존 원래 대표 장소와 v176/v178 재조립 위치를 제외했을 때 추가 실내 5×5 배치가 가능한 타일 **{m['original_source_keys_with_fresh_untried_inbounds_sites']}종**, 없는 타일 **{m['original_source_keys_without_untried_5x5_sites']}종**.\n"
 f"- 새 대체장면 **{m['new_TMX_context_candidates_rendered']}종**을 최대 세 곳에서 재구성하고 B−C 변화가 가장 잘 드러난 실제 TMX 위치 선택. 차이 양수 **{m['source_candidates_with_positive_new_B_C']}종**, 변화0 **{m['source_candidates_with_new_B_C_zero']}종**. 원본 PNG A/B/C/DIFF 및 접촉시트·원본 위치 CSV 보존.\n"
 f"- 물리 SQLite **242테이블**: 기존 v179 **241개 테이블/모든 행 값·행 수** 그대로 보존, 신규 TMX 증거 {m['new_TMX_context_candidates_rendered']}행 1테이블. SHA256 {d['sqlite_sha256']}; integrity_check=ok.\n"
 '- 신뢰할 수 있는 물체 부분 외형의 직접 판독 전이므로 관찰률 **9,792/10,042 (97.51%)**, 기록상 미관찰 **250종** 그대로. 실제 고유 미관찰 248종 및 과거 집계 차이2, 기존5409 중 원본A 미선정9종 보류 유지. 공식 Local ID/TileZed 매핑과 사물 최종 인증 0.\n'
 '- 사용자 수동80·제외14·D held2/JUMBO20 및 원본84 TMX/Tiles PNG·과거 SQLite/CSV/ZIP 모두 불변. 이 작업은 같은 A의 다른 TMX 좌표 테스트로서 같은 원본 B에 다른 공식 A를 대입하는 사용자 정의 D 실험이 아님.\n'
 '- 증거 review/v180_remnant239_multisite/ 및 analysis/current/v180/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;t=f.read_text(encoding='utf-8');assert 'v179' in t
 k=t.index('\n');f.write_text(t[:k+1]+'\n'+summary+t[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v180 original TMX multisite evidence, zero observed promotion, tables 242:',m['new_TMX_context_candidates_rendered'])
