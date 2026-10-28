#!/usr/bin/env python3
"""Record original source A/alternate TMX B/C evidence without visual identity promotion."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v176_alt_scene_48/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v176/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v175/MANIFEST.json').read_text())
path=R/'PROJECT_STATE.json'
state=json.loads(path.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v175'
assert state['latest_checkpoint']['expanded_unique_observed']==9661
assert state['latest_checkpoint']['expanded_unique_unobserved']==381
assert d['parent']=='v175' and d['table_count']==238 and d['prior_tables_preserved']==237
assert d['new_rows']==48 and d['new_observed_rows']==0
assert d['parent_sqlite_sha256']==p['sqlite_sha256']
assert m['true_alternate_TMX_scenes']==48 and m['observed_after']==9661
assert m['new_B_C_positive_count']+m['new_B_C_zero_count']==48
assert m['official_mapping_verified']==m['tilezed_verified']==m['identity_certified']==0
state['previous_checkpoint_v175']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v176',date='2026-10-28',
 kind='actual_alternate_84_TMX_5x5_B_C_evidence_only_no_identity_promotion',
 physical_unified_sqlite_version='v176',prior_visual_checkpoint='v175',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9661,
 expanded_unique_unobserved=381,expanded_observation_percent=9661/10042*100,
 v176_true_original_alternate_B_C_scenes=48,
 v176_new_B_C_positive=m['new_B_C_positive_count'],
 v176_new_B_C_zero=m['new_B_C_zero_count'],
 v176_newly_observed=0,
 evidence_repo_path='review/v176_alt_scene_48/ALT_SCENE_RESULTS_48.csv',
 evidence_manifest='review/v176_alt_scene_48/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v176_sqlite_sha256=d['sqlite_sha256'],
 caution='48 other ORIGINAL TMX placements assembled with identical original A candidate and single GID deletion. Pixel differences do NOT prove identity, material or official Local ID. Must visually inspect the newly rendered B/C evidence before any provisional identity promotion. Parent checkpoint 381 missing vs 379 strict physically missing remains unresolved.'
))
state['unified_database'].update(dict(version='v176',status='VERIFIED_ALTERNATE_SCENE_EVIDENCE_NOT_IDENTITIES',
 repo_manifest='analysis/current/v176/MANIFEST.json',parent_unified_version='v175',
 sqlite_sha256=d['sqlite_sha256'],table_count=238,prior_tables_preserved=237,
 sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9661,expanded_unobserved_unique=381,
 v176_alternative_scene_rows=48,certified=0))
state['latest_v176_evidence']=dict(
 version='v176',original_alternate_5x5_TMX_BC_scenes=48,
 new_positive_deltas=m['new_B_C_positive_count'],
 new_zero_deltas=m['new_B_C_zero_count'],
 no_neighbor_source_missing=m['no_missing_sprites_count'],
 visual_identification_promotions=0,source_keys_audited=379,
 checkpoint_discrepancy_cases=2,observed_total=9661,unobserved_remaining=381,
 physical_database_sha256=d['sqlite_sha256'],physical_tables=238,
 official_mapping_verified=0,tilezed_verified=0,certified=0)
state['next_actions']=[
 'v176: review ALT_BC_00..07.jpg and original A/B/C by eye; only promote physically source-checked and visually interpretable positive-delta scenes.',
 'v176: continue alternate render among v175 total 220 eligible 5x5 sites after these 48; do not confuse scene construction with identity certification.',
 'v176: reconcile checkpoint 381 vs 379 actual missing keys without artificially assigning two tile identities.',
 *state.get('next_actions',[])
]
path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v176 원본 동일 타일을 다른 실제 TMX 배치에서 A/B/C 재조립 48종 (2026-10-28)\n\n'
 f"- v175 전수 조사에서 나온 배치 후보 220종 중 우선 **48종**의 다른 실제 5×5 TMX 위치(원래 같은 키·raw GID)를 선택. 원본 A PNG를 그대로 둔 B, 그 자리 한 GID만 제거한 C와 B−C 이미지/ZIP 증거를 작성. 대체 장면에서 픽셀 변화 양수 **{m['new_B_C_positive_count']}종**, 변화0 **{m['new_B_C_zero_count']}종**.\n"
 '- PNG 원본 크롭 RGBA 해시, 실제 TMX 좌표/층·레이어 GID, C 정확히 한 타일 제거, 증거 ZIP CRC 검증. 렌더링은 잠정 TileZed 유사 투영이며 실제 사물 정체·방향·연결·공식 Local ID 매핑은 미인증. 후속 육안 검수가 필요하므로 새 관찰 완료 0종.\n'
 f"- 물리 SQLite **238테이블**: 부모 v175의 모든 237테이블/행 값과 행 수 보존, 이미지 대체장면 증거 48행 1테이블, SHA256 {d['sqlite_sha256']}, integrity_check=ok.\n"
 '- 누적 관찰 **9,661/10,042 (96.21%)** 유지. 상태 파일 미관찰381 vs 실제 고유키379와 과거 집계차이2 미해결. 최종 정체·TileZed 공식 인증 0.\n'
 '- 원본 84 TMX/Tiles PNG, 이전 모든 DB, 기존5409·수동80/제외14/D held2/JUMBO20 유지. 이번은 다른 배치의 같은 A를 보는 실험으로 공식 다른 A를 대입하는 사용자 정의 D가 아님.\n'
 '- 증거 review/v176_alt_scene_48/ 및 analysis/current/v176/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;s=f.read_text(encoding='utf-8')
 assert 'v175' in s
 k=s.index('\n')
 f.write_text(s[:k+1]+'\n'+summary+s[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v176 alternative rendered evidence, zero observation promotions',m['new_B_C_positive_count'],m['new_B_C_zero_count'],d['sqlite_sha256'])
