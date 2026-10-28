#!/usr/bin/env python3
"""Record original source A/alternate TMX B/C evidence without visual identity promotion."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v178_alt_scene_bulk172/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v178/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v177/MANIFEST.json').read_text())
path=R/'PROJECT_STATE.json'
state=json.loads(path.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v177'
assert state['latest_checkpoint']['expanded_unique_observed']==9684
assert state['latest_checkpoint']['expanded_unique_unobserved']==358
assert d['parent']=='v177' and d['table_count']==240 and d['prior_tables_preserved']==239
assert d['new_rows']==172 and d['new_observed_rows']==0
assert d['parent_sqlite_sha256']==p['sqlite_sha256']
assert m['true_alternate_TMX_scenes']==172 and m['observed_after']==9684
assert m['new_B_C_positive_count']+m['new_B_C_zero_count']==172
assert m['official_mapping_verified']==m['tilezed_verified']==m['identity_certified']==0
state['previous_checkpoint_v175']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v178',date='2026-10-28',
 kind='actual_alternate_84_TMX_5x5_B_C_evidence_only_no_identity_promotion',
 physical_unified_sqlite_version='v178',prior_visual_checkpoint='v177',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9661,
 expanded_unique_unobserved=381,expanded_observation_percent=9661/10042*100,
 v178_true_original_alternate_B_C_scenes=172,
 v178_new_B_C_positive=m['new_B_C_positive_count'],
 v178_new_B_C_zero=m['new_B_C_zero_count'],
 v178_newly_observed=0,
 evidence_repo_path='review/v178_alt_scene_bulk172/ALT_SCENE_RESULTS_172.csv',
 evidence_manifest='review/v178_alt_scene_bulk172/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v178_sqlite_sha256=d['sqlite_sha256'],
 caution='172 other ORIGINAL TMX placements assembled with identical original A candidate and single GID deletion. Pixel differences do NOT prove identity, material or official Local ID. Must visually inspect the newly rendered B/C evidence before any provisional identity promotion. Parent checkpoint 381 missing vs 379 strict physically missing remains unresolved.'
))
state['unified_database'].update(dict(version='v178',status='VERIFIED_ALTERNATE_SCENE_EVIDENCE_NOT_IDENTITIES',
 repo_manifest='analysis/current/v178/MANIFEST.json',parent_unified_version='v177',
 sqlite_sha256=d['sqlite_sha256'],table_count=240,prior_tables_preserved=239,
 sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9661,expanded_unobserved_unique=381,
 v178_alternative_scene_rows=172,certified=0))
state['latest_v178_evidence']=dict(
 version='v178',original_alternate_5x5_TMX_BC_scenes=172,
 new_positive_deltas=m['new_B_C_positive_count'],
 new_zero_deltas=m['new_B_C_zero_count'],
 no_neighbor_source_missing=m['no_missing_sprites_count'],
 visual_identification_promotions=0,source_keys_audited=379,
 checkpoint_discrepancy_cases=2,observed_total=9661,unobserved_remaining=381,
 physical_database_sha256=d['sqlite_sha256'],physical_tables=240,
 official_mapping_verified=0,tilezed_verified=0,certified=0)
state['next_actions']=[
 'v178: review ALT_BC_00..07.jpg and original A/B/C by eye; only promote physically source-checked and visually interpretable positive-delta scenes.',
 'v178: first 48 (v176) plus remaining 172 (v178) complete 220 alternative scenes; visually examine 29 contact sheets and verify candidate identities before observed promotion.',
 'v178: reconcile checkpoint 381 vs 379 actual missing keys without artificially assigning two tile identities.',
 *state.get('next_actions',[])
]
path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v178 대형 배치: 다른 실제 TMX 위치 A/B/C 잔여 172종 전부 재조립 (2026-10-28)\n\n'
 '- v175 원본84 TMX 전수 조사에서 실제 다른 5×5 위치가 확인된 220종 중 v176에서 만든 48종을 제외한 **172종 전체**를 기존과 같은 A PNG에 대해 새로운 원본 B·단일 GID 제거 C·B−C 비교로 재구성. 6종/장 비교 시트와 A/B/C/차이 688 PNG ZIP 생성.\n'
 f"- 새 장면에서 B−C 픽셀 변화 있음 **{m['new_B_C_positive_count']}종**, 없음 **{m['new_B_C_zero_count']}종**. 정체/물체 부품은 실제 접촉시트 사람이 읽고 구분할 때만 다음 v179에서 새 잠정 관찰 승격. 자동으로 '관찰 완료' 처리하지 않음.\n"
 f"- 물리 SQLite **240테이블**, 부모 v177의 239개 테이블 모든 행 내용/수 보존, 신규 증거 172행 1테이블. SHA256 {d['sqlite_sha256']}, integrity_check=ok.\n"
 '- 최신 누적 이미지 잠정 관찰률 **9,684/10,042종(96.43%)** 및 기록상 미관찰 **358종** 유지, 실제 원본 고유 미관찰 356과 과거 집계 차이 2 미해결. 공식 TileZed/Local ID 정체 최종 인증 0.\n'
 '- 원본 84 TMX/PNG, 기존 5409·수동80·제외14·D held2/JUMBO20 및 역사 DB/근거 보존. 이것은 같은 원본 A의 다른 진짜 TMX B 자리를 보는 것이지 D의 다른 공식 A를 원래 B 같은 좌표에 넣는 작업이 아님.\n'
 '- 증거 review/v178_alt_scene_bulk172/, 물리 SQLite analysis/current/v178/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;s=f.read_text(encoding='utf-8')
 assert 'v177' in s
 k=s.index('\n')
 f.write_text(s[:k+1]+'\n'+summary+s[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v178 alternative rendered evidence, zero observation promotions',m['new_B_C_positive_count'],m['new_B_C_zero_count'],d['sqlite_sha256'])
