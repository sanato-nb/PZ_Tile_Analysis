#!/usr/bin/env python3
"""Commit only original-source verified v181 observations; no final identities."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v181_multisite56_visual/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v181/MANIFEST.json').read_text())
parent=json.loads((R/'analysis/current/v180/MANIFEST.json').read_text())
p=R/'PROJECT_STATE.json';state=json.loads(p.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v180'
assert state['latest_checkpoint']['expanded_unique_observed']==9792
assert state['latest_checkpoint']['expanded_unique_unobserved']==250
assert state['unified_database']['version']=='v180'
assert state['unified_database']['sqlite_sha256']==parent['sqlite_sha256']
assert d['version']=='v181' and d['parent']=='v180' and d['parent_sqlite_sha256']==parent['sqlite_sha256']
assert d['table_count']==243 and d['prior_tables_preserved']==242
assert d['new_rows']==d['new_observed_rows']==34
assert m['visually_reviewed']==56 and m['positive_B_C_scenes']==47
assert m['newly_provisional']==34 and m['held']==22
assert m['held_zero']==9 and m['held_weak_or_missing']==13
assert m['observed_parent']==9792 and m['observed_now']==9826
assert m['remaining_checkpoint']==216 and m['remaining_physical_unique']==214 and m['checkpoint_discrepancy']==2
assert m['official_mapping_verified']==m['tilezed_verified']==m['identity_certified']==0
state['previous_checkpoint_v180']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v181',date='2026-10-28',
 kind='manual_visual_source_backed_56_additional_multisite_scenes_and_34_provisional_parts',
 physical_unified_sqlite_version='v181',prior_visual_checkpoint='v180',
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=9826,expanded_unique_unobserved=216,expanded_observation_percent=9826/10042*100,
 new_image_observed=9826-5400,new_keys_unobserved=4633-(9826-5400),
 v181_alternate_scenes_visually_reviewed=56,v181_B_C_positive=47,v181_new_provisional=34,
 v181_excluded_unverified=22,v181_zero_held=9,v181_weak_held=13,
 v181_physical_unobserved_distinct=214,v181_historical_count_discrepancy=2,
 v181_reviewed_indices=m['accepted_indices'],v181_sqlite_sha256=d['sqlite_sha256'],
 evidence_repo_path='review/v181_multisite56_visual/VISUAL_REVIEW_34.csv',
 evidence_manifest='review/v181_multisite56_visual/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='v180 56 source-proven actual TMX B/C 10 contact sheets manually inspected. Only 34 candidates with source B-C>=200 and missing neighbors=0 were provisionally observed. 9 zero + 13 tiny/ambiguous/missing held. Parent table immutability verified. Official mapping and final object identity zero. Checkpoint missing216 vs physical actual missing214; historical discrepancy2 persists.'
))
state['unified_database'].update(dict(
 version='v181',status='VERIFIED_ORIGINAL_TMX_MULTISITE_MANUAL_VISUAL_PROVISIONAL',
 repo_manifest='analysis/current/v181/MANIFEST.json',parent_unified_version='v180',
 sqlite_sha256=d['sqlite_sha256'],table_count=243,prior_tables_preserved=242,
 sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9826,expanded_unobserved_unique=216,
 new_4633_observed=9826-5400,new_4633_unobserved=4633-(9826-5400),
 v181_visual_review_rows=34,certified=0
))
state['latest_v181_evidence']=dict(
 version='v181',additional_original_TMX_scenes_visually_reviewed=56,
 source_pixel_positive=47,new_provisional_image_records=34,
 held_zero_pixel=9,held_weak_or_missing=13,
 observed_total=9826,unobserved_remaining=216,physical_distinct_unobserved=214,
 historical_count_discrepancy=2,parent_tables_preserved=242,physical_sqlite_tables=243,
 sqlite_sha256=d['sqlite_sha256'],official_mapping_verified=0,tilezed_verified=0,final_identity_certified=0)
state['next_actions']=[
 'v181: explore nonselected new TMX locations/actual world map evidence for 214 still unobserved source keys, prioritizing source-supported original A and B-C>0. Do not falsely count the old-nine held source identifiers or historical two-count discrepancy as finished.',
 'v181: 56 newly found TMX scenes all manually reviewed; 34 provisional and 22 held, including 9 truly B-C zero. Preserve full source PNG/TMX and prior DB untouched.',
 'v181: reconcile historical two-case aggregate checkpoint 216 vs physical unique missing 214 before declaring complete.',
 *state.get('next_actions',[])
]
p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v181 추가 원본 TMX의 A/B/C 56종 시각 판독 및 34종 잠정 기록 (2026-10-28)\n\n'
 '- v180 84개 원본 TMX 중 추가 위치 56종의 원본 A/B/C/차이 시트 10장을 직접 검수: 픽셀 변화 47종, 변화0 9종. 실제 외형과 장면을 보고 34종을 잠정 기록, 근거 부족/지나치게 작은 차이 13종 및 변화0 9종은 보류.\n'
 '- 각 신규 기록은 원본 PNG A RGBA SHA256, 56개 원본 A/B/C/DIFF 총224장 ZIP CRC, 원본 TMX raw GID/층/레이어/좌표를 v180 부모 DB에서 대조하고 B/C 실제 픽셀 변화 재계산. 신뢰도와 부품 역할 기록만 수행, 공식 ID·정체 최종 인증 0.\n'
 f"- 물리 SQLite **243테이블**, 부모 v180의 기존 242테이블 모든 행 내용·수를 보존, 신규34행. SHA256 {d['sqlite_sha256']}, integrity_check=ok.\n"
 '- 누적 이미지 잠정 관찰 **9,826/10,042 (97.85%)**, 기록상 미관찰 **216종**, 실제 원본 고유키 기준 **214종**, 과거 집계차이 2건은 여전히 미해결.\n'
 '- 원본 84 TMX/Tiles PNG, 기존5409·수동80/제외14·D held2/JUMBO20·과거 SQLite/증거 전부 보존. 사용자 정의 D는 같은 키 다른 공식 A를 기존 B 동일 좌표/층/레이어에 대입하는 것이며 이번 회차 미실행.\n'
 '- 증거 review/v181_multisite56_visual/, 부모 review/v180_remnant239_multisite/, DB analysis/current/v181/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;txt=f.read_text(encoding='utf-8')
 assert 'v180' in txt
 k=txt.index('\n')
 f.write_text(txt[:k+1]+'\n'+summary+txt[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v181: 34 source-backed provisional additions, 9826/10042 and 243 SQLite tables',d['sqlite_sha256'])
