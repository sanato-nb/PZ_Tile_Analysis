#!/usr/bin/env python3
"""Checkpoint v183 only if physical 245-table original-A/B/C review passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
new=json.loads((R/'review/v183_original_BC_visual65/MANIFEST.json').read_text())
db=json.loads((R/'analysis/current/v183/MANIFEST.json').read_text())
parent=json.loads((R/'analysis/current/v182/MANIFEST.json').read_text())
path=R/'PROJECT_STATE.json'
st=json.loads(path.read_text(encoding='utf-8'))
assert st['latest_checkpoint']['version']=='v182'
assert st['latest_checkpoint']['expanded_unique_observed']==9829
assert st['latest_checkpoint']['expanded_unique_unobserved']==213
assert st['unified_database']['version']=='v182'
assert st['unified_database']['sqlite_sha256']==parent['sqlite_sha256']
assert new['parent']=='v182' and db['parent']=='v182'
assert new['source_original_TMX_A_B_C_directly_reviewed']==202
assert new['source_verified_promoted']==65 and new['held_total']==137
assert new['positive_ge100_held']==11 and new['weak_under100_held']==11
assert new['B_C_zero_held']==114 and new['source_A_missing_held']==1
assert new['diagnostic_mask_only_promoted']==0
assert new['prior_observed']==9829 and new['current_observed']==9894 and new['remaining_checkpoint']==148
assert db['parent_sqlite_sha256']==parent['sqlite_sha256']
assert db['table_count']==245 and db['prior_tables_preserved']==244
assert db['new_rows']==db['new_observed_rows']==65
assert new['official_mapping_verified']==new['tilezed_verified']==new['identity_certified']==0
st['previous_checkpoint_v182']=json.loads(json.dumps(st['latest_checkpoint']))
st['latest_checkpoint'].update(dict(version='v183',date='2026-10-28',
 kind='manual_original_84_TMX_A_B_C_visual65_excluding_occlusion_diagnostic',
 physical_unified_sqlite_version='v183',prior_visual_checkpoint='v182',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9894,
 expanded_unique_unobserved=148,expanded_observation_percent=9894/10042*100,
 original_5409_observed_preserved=5400,original_5409_unobserved_preserved=9,
 new_image_observed=4494,new_keys_unobserved=139,
 v183_direct_original_scene_reviewed=202,v183_original_B_C_positive=87,
 v183_provisional_new=65,v183_unverified_held=137,
 v183_masked_diagnostic_only_promoted=0,
 v183_physical_missing_distinct=146,v183_historical_count_discrepancy=2,
 v183_sqlite_sha256=db['sqlite_sha256'],
 evidence_repo_path='review/v183_original_BC_visual65/VISUAL_REVIEW_65.csv',
 evidence_manifest='review/v183_original_BC_visual65/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='Manual visual observations only from original A and real unmodified TMX B-C evidence. X/Y upper-layer-masked diagnostic must never substitute for actual B-C source scene. 65 provisional, 137 held; final identity zero and official PNG/TileZed Local ID mapping zero. Historical 2-count discrepancy remains.'
))
st['unified_database'].update(dict(version='v183',status='VERIFIED_REAL_ORIGINAL_TMXS_MANUAL_VISUAL65_APPEND_ONLY',
 repo_manifest='analysis/current/v183/MANIFEST.json',parent_unified_version='v182',
 sqlite_sha256=db['sqlite_sha256'],table_count=245,prior_tables_preserved=244,
 sqlite_size_bytes=db['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9894,expanded_unobserved_unique=148,
 new_4633_observed=4494,new_4633_unobserved=139,
 v183_visual_review_rows=65,certified=0))
st['latest_v183_evidence']=dict(
 version='v183',actual_original_TMX_A_B_C_scenes_manually_seen=202,
 true_B_C_positive=87,true_B_C_ge100=76,
 new_source_backed_provisional=65,still_held=137,
 B_C_zero_held=114,tiny_positive_held=11,high_delta_but_missing_or_ambiguous_held=11,
 no_source_held=1,diagnostic_mask_only_promoted=0,
 previous_observed=9829,current_observed=9894,remaining_checkpoint=148,
 physical_missing_distinct=146,historical_discrepancy=2,
 physical_SQLite_tables=245,prior_tables_preserved=244,
 sha256=db['sqlite_sha256'],final_certified=0,official_mapping_verified=0,tilezed_verified=0
)
st['next_actions']=[
 'v183: focus on 137 real B-C invisible/weak/missing-neighbor source tiles from v182; X/Y diagnostic alone does not justify observed identity.',
 'v183: separate actual neighbor PNG missing from true occluded-by-higher-TMX-layer zero-delta tiles and render another verified original TMX occurrence where possible.',
 'v183: reconcile historic 2-count difference between 148 checkpoint missing and 146 actual source distinct unobserved, with no fabricated identities.',
 *st.get('next_actions',[])
]
path.write_text(json.dumps(st,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v183 실제 원본 TMX A/B/C 202종 수동 검수 — 65종 잠정 신규 기록 (2026-10-28)\n\n'
 '- v182 원본 PNG A, 실제 TMX의 기존 B 장면, 같은 GID 1개를 제거한 원래 C, 상위층 숨긴 진단 X/Y 비교 이미지 **202종·34장 시트** 직접 시각 판독. 실제 B-C 양수 87종 중 100픽셀 이상 76종 개별 설명; 원본 주변 PNG 누락7종 및 불분명한 부품4종 제외, **65종 신규 provisional_candidate** 기록.\n'
 '- 실제 원본 B-C가 0인 114종, 100픽셀 미만11종, A 원본이 없는 1종은 관찰 미완료. **진단 X/Y만 양수인 것은 어떤 타일도 관찰 완료로 승격하지 않음**.\n'
 f"- 누적 이미지 잠정 관찰 **9,894/10,042 (98.53%)**, 기록상 미관찰 **148종**. 공식 A↔TileZed/Local ID 매핑 및 최종 사물 정체 인증 0.\n"
 f"- 원본 v182 분할 PNG ZIP 3개 결합의 SHA/CRC, A_RGBA 픽셀 SHA, 원본 TMX 파일 SHA/raw GID·층·레이어·좌표 및 RGB B-C 픽셀을 다시 검증. 부모 물리 SQLite **244테이블 전부의 행수·행내용 보존**하고 새 관찰65행 한 테이블 추가하여 **245테이블**, SHA256 {db['sqlite_sha256']}, integrity_check=ok.\n"
 '- 시각적으로 파이프 오르간, 산업기계·전기장치, 문틀·아치, 지붕/박공판, 벽난로, 금속 펜스, 식물/농작물, 가구와 공사 소품 등 실제 부품 형태를 관찰했지만 정확한 재질·방향·연결·공식 타일 매핑은 인증하지 않음.\n'
 '- 역사적 집계 차이2 보류. 84 TMX/Tiles 원본 PNG, 기존5409·사용자 수동80·제외14·held D2/JUMBO20, 과거 SQLite/CSV/증거 전부 보존. D는 같은 키의 다른 공식 A를 기존 B 동일 위치·층·레이어에 넣는 정식 사용자 정의 대체 A 비교이며 이번에 미실행.\n'
 '- 증거 review/v183_original_BC_visual65/ 및 review/v182_occlusion202/, 물리 DB analysis/current/v183/MANIFEST.json.\n\n---\n'
)
for rel in ('AGENTS.md','docs/HANDOFF.md'):
 f=R/rel
 data=f.read_text(encoding='utf-8')
 assert 'v182' in data
 k=data.index('\n')
 f.write_text(data[:k+1]+'\n'+summary+data[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v183 original A + true TMX B-C visual source review 65, observed=9894/10042',db['sqlite_sha256'])
