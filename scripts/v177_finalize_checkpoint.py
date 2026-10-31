#!/usr/bin/env python3
"""Finalize parent-preserved v177 low/medium/high image observations only."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v177_alternate_visual23/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v177/MANIFEST.json').read_text())
parent=json.loads((R/'analysis/current/v176/MANIFEST.json').read_text())
p=R/'PROJECT_STATE.json'
state=json.loads(p.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v176'
assert state['latest_checkpoint']['expanded_unique_observed']==9661
assert state['latest_checkpoint']['expanded_unique_unobserved']==381
assert state['unified_database']['version']=='v176'
assert state['unified_database']['sqlite_sha256']==parent['sqlite_sha256']
assert d['version']=='v177' and d['parent']=='v176'
assert d['parent_sqlite_sha256']==parent['sqlite_sha256']
assert d['table_count']==239 and d['prior_tables_preserved']==238
assert d['new_rows']==d['new_observed_rows']==23
assert m['visually_seen_alternate_scenes']==48
assert m['alternative_delta_positive']==27
assert m['provisional_promoted_after_manual_visual_review']==23
assert m['tiny_positive_held']==4 and m['zero_pixel_held']==21
assert m['observed_parent']==9661 and m['observed_now']==9684
assert m['remaining_in_checkpoint']==358 and m['source_distinct_unobserved_after']==356
assert m['checkpoint_discrepancy']==2
assert m['official_mapping_verified']==m['tilezed_verified']==m['identity_certified']==0
state['previous_checkpoint_v176']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v177',date='2026-10-28',kind='manual_alternative_actual_TMX_A_B_C_visual23_provisional',
 physical_unified_sqlite_version='v177',prior_visual_checkpoint='v176',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9684,expanded_unique_unobserved=358,
 expanded_observation_percent=9684/10042*100,
 new_image_observed=9684-5400,new_keys_unobserved=4633-(9684-5400),
 v177_alternative_scenes_visually_reviewed=48,v177_source_change_detected=27,
 v177_new_provisional=23,v177_excluded_unverified=25,
 v177_excluded_tiny_positive=4,v177_excluded_B_C_zero=21,
 v177_physical_missing_distinct_keys=356,v177_historical_count_discrepancy=2,
 v177_reviewed_indices=m['visual_review_indices'],
 v177_sqlite_sha256=d['sqlite_sha256'],
 evidence_repo_path='review/v177_alternate_visual23/VISUAL_REVIEW_23.csv',
 evidence_manifest='review/v177_alternate_visual23/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='48 actual alternate TMX B/C contact-sheet scenes were inspected by eye. Only 23 evidence-positive (>100 pixels) and recognizable original A shapes promoted to provisional candidate. Twenty-one B-C zero and four ambiguous tiny deltas held. Official original A ↔ TileZed/Local ID mapping and final object identity still zero. Aggregate checkpoint 358 missing differs from physical distinct missing keys 356 by unresolved historical two-count discrepancy.'
))
state['unified_database'].update(dict(
 version='v177',status='VERIFIED_SOURCE_BACKED_LOW_CONFIDENCE_VISUAL_REVIEW',
 repo_manifest='analysis/current/v177/MANIFEST.json',
 parent_unified_version='v176',sqlite_sha256=d['sqlite_sha256'],table_count=239,
 prior_tables_preserved=238,sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9684,expanded_unobserved_unique=358,
 new_4633_observed=9684-5400,new_4633_unobserved=4633-(9684-5400),
 v177_visual_review_rows=23,certified=0
))
state['latest_v177_evidence']={
 'version':'v177','different_actual_TMX_positions_reviewed':48,'positive_delta_scenes':27,
 'new_provisional_image_observations':23,'tiny_deltas_held':4,'zero_deltas_held':21,
 'physical_distinct_missing_keys_after':356,'checkpoint_missing_after':358,
 'unreconciled_historical_count_discrepancy':2,
 'observed_total':9684,'unobserved_remaining':358,
 'sqlite_tables':239,'parent_tables_preserved':238,
 'sqlite_sha256':d['sqlite_sha256'],
 'official_mapping_verified':0,'tilezed_verified':0,'final_identity_certified':0
}
state['next_actions']=[
 'v177: render and physically compare more actual alternate TMX locations for the remaining 172 candidates from the 220 v175 census; the original 48 candidates were checked in v176.',
 'v177: require same-key original PNG crop, actual raw TMX GID and B/C pixel difference plus manual appearance/context observation before any new provisional or final certification.',
 'v177: reconcile historical two-case aggregate checkpoint 358 vs physical 356 actual missing keys, do not assign invented tile IDs.',
 *state.get('next_actions',[])
]
p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v177 실제 다른 TMX B/C 장면의 원본 타일 48종 수동 외형 판독 (2026-10-28)\n\n'
 '- v176의 원본 A 및 실제 다른 TMX B/C/차이 **48종, 8장 접촉시트**를 직접 육안 분석. 그중 원본 GID 하나 제거에 따라 변화 27종, 진짜 부품 형상/주변 맥락이 같이 드러나고 차이 >=100 픽셀인 **23종**에 잠정 정체 후보·외형·부분역할·재질·신뢰도 기록. 너무 작은 변화 4종 및 변화0 21종은 미관찰 유지.\n'
 '- 건초더미 3077, 작은 잎덤불 422, 산업 작업대 1067, 접이식 적백 차양막 3266, 식당 의자 1774/1776, 삼각 박공 사이딩 3730, 기타 벽·창 부품 등 **원본 A와 실제 타일 제거 차이 및 주변 장면 모두 대조**.\n'
 '- **9,684/10,042종 (96.43%)** 이미지 잠정 관찰, 상태 미관찰 **358종**. 원본 고유 키만 세면 미관찰 356종으로 역사적 집계 차이 2는 별도 조사. 사물 최종 인증과 공식 A PNG/TileZed Local ID 매핑은 모두 0.\n'
 f"- 물리 SQLite **239테이블**(v176 238개 과거 테이블 모든 행값·행수 유지, 신규 관찰 23행), SHA256 {d['sqlite_sha256']}; PRAGMA integrity_check=ok. 원본 B/C 192장 ZIP 해시·CRC 및 A RGBA/TMX GID/좌표·층·레이어 재검증.\n"
 '- 기존 원본 84 TMX/Tiles PNG, 기존 5409·수동80·제외14·D held2/JUMBO20, 과거 DB/CSV/ZIP 모두 보존. 사용자 정의 D는 같은 키의 다른 공식 A를 기존 B 같은 위치·층·레이어에 교체하는 것이며 이번 작업에서 미실행.\n'
 '- 근거 review/v177_alternate_visual23/, 원본 증거 review/v176_alt_scene_48/, DB analysis/current/v177/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel
 txt=f.read_text(encoding='utf-8')
 assert 'v176' in txt
 k=txt.index('\n')
 f.write_text(txt[:k+1]+'\n'+summary+txt[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v177 23 additional visually reviewed provisional tile keys: 9684/10042',d['sqlite_sha256'],flush=True)
