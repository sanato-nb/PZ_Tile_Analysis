#!/usr/bin/env python3
"""v184 state update only after original A B C and immutable 246-table SQLite verification."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
meta=json.loads((R/'review/v184_true_BC_reinspect4/MANIFEST.json').read_text())
new=json.loads((R/'analysis/current/v184/MANIFEST.json').read_text())
parent=json.loads((R/'analysis/current/v183/MANIFEST.json').read_text())
p=R/'PROJECT_STATE.json';state=json.loads(p.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v183'
assert state['latest_checkpoint']['expanded_unique_observed']==9894
assert state['latest_checkpoint']['expanded_unique_unobserved']==148
assert state['unified_database']['version']=='v183'
assert state['unified_database']['sqlite_sha256']==parent['sqlite_sha256']
assert meta['manual_source_original_B_C_reviewed']==4
assert meta['promoted_provisional']==3 and meta['still_held']==1
assert set(meta['upgraded_indices'])=={29,327,3901} and meta['held_indices']==[298]
assert meta['prior_observed']==9894 and meta['current_observed']==9897
assert meta['remaining_checkpoint']==145 and new['parent']=='v183'
assert new['parent_sqlite_sha256']==parent['sqlite_sha256']
assert new['table_count']==246 and new['prior_tables_preserved']==245 and new['new_rows']==3
assert new['certified']==meta['identity_certified']==0
state['previous_checkpoint_v183']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(version='v184',date='2026-10-28',
 kind='reinspection_of_four_true_BC_source_positive_ambiguous_parts',
 physical_unified_sqlite_version='v184',prior_visual_checkpoint='v183',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9897,
 expanded_unique_unobserved=145,expanded_observation_percent=9897/10042*100,
 original_5409_observed_preserved=5400,original_5409_unobserved_preserved=9,
 new_image_observed=4497,new_keys_unobserved=136,
 v184_direct_original_scene_reviewed=4,v184_provisional_new=3,v184_ambiguous_held=1,
 v184_physical_missing_distinct=143,v184_historical_count_discrepancy=2,
 v184_sqlite_sha256=new['sqlite_sha256'],
 evidence_repo_path='review/v184_true_BC_reinspect4/VISUAL_REVIEW_3.csv',
 evidence_manifest='review/v184_true_BC_reinspect4/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='Three cautious provisional part-family readings derive only from original A and actual TMX B-C >100 pixels and complete original neighboring PNGs. No layer-masked X/Y promotion. Source A uncertain small item 298 remains held. Original identity and official TileZed mapping still zero; historical 2-count mismatch unresolved.'
))
state['unified_database'].update(dict(version='v184',
 status='VERIFIED_TRUE_ORIGINAL_BC_MANUAL_REINSPECTION_APPEND_ONLY',
 repo_manifest='analysis/current/v184/MANIFEST.json',parent_unified_version='v183',
 sqlite_sha256=new['sqlite_sha256'],table_count=246,prior_tables_preserved=245,
 sqlite_size_bytes=new['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9897,expanded_unobserved_unique=145,
 new_4633_observed=4497,new_4633_unobserved=136,
 v184_visual_review_rows=3,certified=0))
state['latest_v184_evidence']=dict(version='v184',manually_reinspected_ambiguous=4,
 new_source_backed_provisional=3,continued_ambiguous_hold=1,
 original_true_BC_positive_checked=4,missing_neighbor_source=0,
 current_observed=9897,remaining_checkpoint=145,
 physical_missing_distinct=143,historical_discrepancy=2,
 physical_SQLite_tables=246,prior_tables_preserved=245,
 sha256=new['sqlite_sha256'],final_certified=0,official_mapping_verified=0,tilezed_verified=0)
state['next_actions']=[
 'v184: among previous 137 held in v183, the four complete-source ambiguous positives are re-reviewed and indices 29/327/3901 provisionally added, 298 still held. Focus next on 7 high-delta entries with missing neighbor PNG and 114 true B-C-zero entries, do not use diagnostic X/Y as real map.',
 'v184: recover source PNG neighborhood or find exact actual alternative TMX placement for 7 held with missing neighbor evidence; never invent sprite pixels.',
 'v184: historical physical missing 143 vs checkpoint missing 145 has 2 unassigned count discrepancies; do not assert full certification.',
 *state.get('next_actions',[])
]
p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v184 실제 원본 B-C 양수·주변 소스 완비였던 미세 부품 4종 재검수 (2026-10-28)\n\n'
 '- v183에서 원본 TMX B-C 픽셀 변화가 100 이상이고 **주변 원본 PNG 누락이 없는** 모호한 4종을 원본 A 및 진짜 TMX B/C에서 다시 눈으로 검수. 휴대 무전기 모양 작은 기기(29), 2가로대 난간 부품(327), 벽돌무늬 박공 사선 끝판(3901)은 부분외형만 잠정 기록, 의미불명 작은 목재 조각(298)은 계속 보류.\n'
 '- 원본 A RGBA 해시와 실제 TMX raw GID·firstgid/LocalID·좌표·층·레이어·원본 TMX SHA 및 진짜 B-C PNG 픽셀을 재대조. 상층 숨김 진단 X/Y는 인증 근거로 사용하지 않음.\n'
 '- 누적 이미지 잠정 관찰 **9,897/10,042(98.56%)**, 기록상 미관찰145종(물리 실제 미관찰 고유키 143종 + 역사적 수치차이2). 공식 타일셋 PNG↔TileZed LocalID/사물 최종 정체 인증0.\n'
 f"- 물리 SQLite **246테이블**: 부모 v183 245개 전체 테이블·모든 과거 행 수/내용 보존, 신규 3행 1테이블. SHA256 {new['sqlite_sha256']}, integrity_check=ok.\n"
 '- 원본 84 TMX/Tiles PNG, 기존5409·사용자 수동80/제외14/held D2/JUMBO20 및 역사 DB/근거 보존. D는 같은 키의 다른 공식 A를 기존 B 동일 위치·층·레이어에 대입하는 실험이고 이번에는 하지 않음.\n'
 '- 증거 review/v184_true_BC_reinspect4/, 원본 A/B/C ZIP review/v182_occlusion202/, 물리 DB analysis/current/v184/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;s=f.read_text(encoding='utf-8')
 assert 'v183' in s
 k=s.index('\n')
 f.write_text(s[:k+1]+'\n'+summary+s[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v184 source-backed +3 candidates 9897/10042, parent 245 tables unchanged',new['sqlite_sha256'],flush=True)
