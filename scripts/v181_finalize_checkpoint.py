#!/usr/bin/env python3
"""Finalize v181 after original A/B/C/TMX/GID and SQLite exact-parent checks."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v181_multisite_visual37/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v181/MANIFEST.json').read_text())
parent=json.loads((R/'analysis/current/v180/MANIFEST.json').read_text())
path=R/'PROJECT_STATE.json';state=json.loads(path.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v180'
assert state['latest_checkpoint']['expanded_unique_observed']==9792
assert state['latest_checkpoint']['expanded_unique_unobserved']==250
assert state['unified_database']['sqlite_sha256']==parent['sqlite_sha256']
assert m['original_alt_scenes_manually_reviewed']==56 and m['B_C_positive']==47
assert m['provisional_accepted']==37 and m['excluded']==19
assert m['weak_delta_held']==9 and m['neighbor_missing_held']==1 and m['zero_delta_held']==9
assert m['observed_now']==9829 and m['checkpoint_missing_after']==213 and m['physical_missing_after']==211
assert m['historical_discrepancy']==2 and m['reviewed_contact_sheets']==10
assert m['official_mapping_verified']==m['tilezed_verified']==m['final_certified']==0
assert d['version']=='v181' and d['parent']=='v180'
assert d['parent_sqlite_sha256']==parent['sqlite_sha256']
assert d['new_rows']==d['new_observed_rows']==37
assert d['table_count']==243 and d['prior_tables_preserved']==242
state['previous_checkpoint_v180']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v181',date='2026-10-28',
 kind='manual_A_B_C_56_actual_multisite_tiles_37_source_checked_provisional_part_observations',
 physical_unified_sqlite_version='v181',prior_visual_checkpoint='v180',
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=9829,expanded_unique_unobserved=213,
 expanded_observation_percent=9829/10042*100,
 new_image_observed=9829-5400,new_keys_unobserved=4633-(9829-5400),
 v181_original_alt_scenes_directly_viewed=56,v181_B_C_positive=47,
 v181_new_provisional=37,v181_excluded_held=19,
 v181_weak_positive_held=9,v181_zero_held=9,v181_neighbor_missing_held=1,
 v181_physical_missing_keys=211,v181_historical_count_discrepancy=2,
 v181_accepted_indices=m['accepted_indices'],
 evidence_repo_path='review/v181_multisite_visual37/VISUAL_REVIEW_37.csv',
 evidence_manifest='review/v181_multisite_visual37/MANIFEST.json',
 v181_sqlite_sha256=d['sqlite_sha256'],
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='56 truly different original TMX locations rendered in v180 were visually examined. Only 37 distinguishable original A/B/C source-backed parts with >=100 changed pixels and no neighbor PNG missing are provisional. 19 remain held, including 9 no-delta, 9 too small and 1 neighbor PNG missing. Official Local ID/TileZed mapping and object identity certification 0; historical 2-count discrepancy unresolved.'
))
state['unified_database'].update(dict(
 version='v181',status='VERIFIED_A_B_C_TMX_SOURCE_MANUAL_VISUAL_PROVISIONAL',
 repo_manifest='analysis/current/v181/MANIFEST.json',parent_unified_version='v180',
 sqlite_sha256=d['sqlite_sha256'],table_count=243,
 prior_tables_preserved=242,sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9829,expanded_unobserved_unique=213,
 new_4633_observed=9829-5400,new_4633_unobserved=4633-(9829-5400),
 v181_visual_review_rows=37,certified=0
))
state['latest_v181_evidence']=dict(
 version='v181',source_backed_alt_scenes_manually_inspected=56,
 B_C_positive=47,new_source_provisional=37,held_zero=9,held_weak=9,held_missing_neighbors=1,
 observed_total=9829,remaining_in_checkpoint=213,
 physical_unobserved_keys=211,historical_count_discrepancy=2,
 prior_tables_preserved=242,physical_database_table_count=243,
 sqlite_sha256=d['sqlite_sha256'],mapping_verified=0,tilezed_verified=0,certified=0
)
state['next_actions']=[
 'v181: study remaining 213 checkpoint missing (211 physical unique + historical two-count discrepancy) with priority on alternate original-map spots, missing neighbor PNGs and original source A mapping; exclude user-held 8 original map tiles and D/JUMBO exclusions.',
 'v181: for any new provisional identity require actual same original PNG A and TMX raw GID/level/layer/coordinates, B/C positive changed pixels and human-readable part; never certify official TileZed without mapping.',
 'v181: reconcile 2 historical aggregate discrepancies without inventing observed source keys.',
 *state.get('next_actions',[])
]
path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v181 실제 추가 TMX A/B/C 56종 육안검수, 신규 잠정 부품 37종 (2026-10-28)\n\n'
 '- v180에서 원본 A PNG, 실제 다른 TMX B, 해당 GID 하나만 제거 C·차이 이미지를 재조립한 **56종·10장 접촉시트**를 눈으로 직접 확인. 변화 양수47종 중 외형/배치가 함께 구별되고 변화100픽셀 이상·이웃 원본 PNG 누락이 없는 **37종**에 부품/사물 잠정후보 설명·신뢰도를 개별 기록. 변화0 9/너무 작은 차이9/이웃 원본 누락1 **19종** 보류.\n'
 '- 세탁기, 가전 금속 장치, 산업 철제 기계박스, 의료 진찰 침대, 식당 테이블, 밭작물·꽃줄기, 검정 바닥 매트·러그, 벽돌/목재 패널, 안전난간 등을 원본 A/B/C·주변 장면으로 판독. 정확한 재질·방향·조립 연결/공식 사물명은 미인증.\n'
 f"- 물리 SQLite **243개 테이블**, v180 부모 242개 기존 테이블 모든 행 수·전체 행 내용 보존, 새37행 추가. SHA256 {d['sqlite_sha256']}; PRAGMA integrity_check=ok, 원본 A RGBA·TMX raw GID/좌표·층·레이어·CRC/차이 이미지 재검증.\n"
 '- 누적 이미지 잠정 관찰 **9,829/10,042 (97.88%)**, 기록상 미관찰 **213종**. 실제 물리 고유 미관찰211종과 역사적 집계 차이2 보존. 최종 물체 정체/TileZed 및 공식 Local ID/PNG 매핑 인증0.\n'
 '- 기존 원본84 TMX/Tiles PNG, 이전5409·수동80·제외14·held D2/JUMBO20 및 모든 과거 DB/CSV/ZIP 보존. 사용자 정의 D는 같은 키 다른 공식 A를 원본 B 동일 좌표·층·레이어에 넣어 비교하는 테스트로, 이번 작업과 구분함.\n'
 '- 근거 review/v181_multisite_visual37/, 원본 이미지 review/v180_remnant239_multisite/, DB analysis/current/v181/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;t=f.read_text(encoding='utf-8');assert 'v180' in t
 k=t.index('\n');f.write_text(t[:k+1]+'\n'+summary+t[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v181 37 visually evidence-confirmed provisional keys, physical SQLite 243, 9829/10042')
