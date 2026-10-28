#!/usr/bin/env python3
"""v182: append raw source/occlusion evidence without claiming any new identity."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
audit=json.loads((R/'review/v182_occlusion202/MANIFEST.json').read_text())
parent=json.loads((R/'analysis/current/v181/MANIFEST.json').read_text())
db=json.loads((R/'analysis/current/v182/MANIFEST.json').read_text())
p=R/'PROJECT_STATE.json';state=json.loads(p.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v181'
assert state['latest_checkpoint']['expanded_unique_observed']==9829
assert state['latest_checkpoint']['expanded_unique_unobserved']==213
assert state['unified_database']['version']=='v181'
assert state['unified_database']['sqlite_sha256']==parent['sqlite_sha256']
assert db['version']=='v182' and db['parent']=='v181'
assert db['parent_sqlite_sha256']==parent['sqlite_sha256']
assert db['table_count']==244 and db['prior_tables_preserved']==243
assert db['new_rows']==202 and db['new_observed_rows']==0
assert audit['source_new_key_unobserved_before']==audit['source_new_key_unobserved_after']==202
assert audit['parent_checkpoint_observed']==9829 and audit['parent_checkpoint_missing']==213
assert audit['original_9_unobserved_held']==9 and audit['historical_checkpoint_count_discrepancy']==2
assert audit['final_certified']==audit['official_mapping_verified']==audit['tilezed_verified']==0
state['previous_checkpoint_v181']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v182',date='2026-10-28',
 kind='source_key_202_original_TMX_BC_vs_layer_masking_diagnostic_evidence',
 physical_unified_sqlite_version='v182',
 prior_visual_checkpoint='v181',
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=9829,
 expanded_unique_unobserved=213,
 expanded_observation_percent=9829/10042*100,
 v182_original_new_keys_audited=202,
 v182_original_A_pixels_verified=audit['true_original_png_verified'],
 v182_true_original_TMX_B_C_rendered=audit['true_original_TMXS_rendered'],
 v182_original_B_C_positive=audit['original_B_C_positive'],
 v182_layer_mask_positive=audit['diagnostic_mask_positive'],
 v182_only_exposed_after_layer_mask=audit['diagnostic_visible_but_original_zero'],
 v182_additional_observed=0,
 v182_original_9_unobserved_held=9,
 v182_unreconciled_historical_count_discrepancy=2,
 v182_sqlite_sha256=db['sqlite_sha256'],
 evidence_repo_path='review/v182_occlusion202/SOURCE_OCCLUSION_202.csv',
 evidence_manifest='review/v182_occlusion202/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='202 physical new-key remaining candidates have original A/real B-C/explicit diagnostic X-Y. X-Y masks upper TMX layers and is NOT the actual map scene nor a valid D official alternate-A proof. Pixels alone do not certify an object. Parent checkpoint 9829/10042 and 213 missing unchanged; historical two-count discrepancy unresolved.'
))
state['unified_database'].update(dict(
 version='v182',status='VERIFIED_SOURCE_OCCLUSION_FORENSIC_EVIDENCE_NOT_IDENTITIES',
 repo_manifest='analysis/current/v182/MANIFEST.json',parent_unified_version='v181',
 sqlite_sha256=db['sqlite_sha256'],table_count=244,
 prior_tables_preserved=243,sqlite_size_bytes=db['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=9829,
 expanded_unobserved_unique=213,v182_occlusion_evidence_rows=202,
 certified=0))
state['latest_v182_evidence']=dict(version='v182',
 remaining_new_key_original_scenes_rechecked=202,
 true_A_verified=audit['true_original_png_verified'],
 true_TMX_BC_rendered=audit['true_original_TMXS_rendered'],
 original_scene_positive=audit['original_B_C_positive'],
 diagnostic_layer_mask_positive=audit['diagnostic_mask_positive'],
 hidden_only_unmasked=audit['diagnostic_visible_but_original_zero'],
 known_old_nine_held=9,history_discrepancy=2,
 newly_observed=0,observed_total=9829,unobserved_remaining=213,
 db_sha256=db['sqlite_sha256'],db_tables=244,
 final_identity_certified=0,official_mapping_verified=0,tilezed_verified=0)
state['next_actions']=[
 'v182: inspect the 202 original-versus-layer-masked A/B/C diagnostic contact sheets; do not confuse diagnostic X/Y with actual map B/C or official D.',
 'v182: prioritize source-confirmed real B-C>0 part shapes; use X-Y only to explain occlusion and to select further source evidence.',
 'v182: preserve old nine user-held/JUMBO and historical 2-key status difference; no fabricated official Local ID↔PNG mapping.',
 *state.get('next_actions',[])
]
p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v182 남은 새 타일 202종 원본 A/B/C 및 위 레이어 가림 진단 (2026-10-28)\n\n'
 '- 원본 84 TMX 전체의 기존 v175 보류 새키370에서 v177 잠정23·v179 108·v181 37을 뺀 **202종**을 실제 원본 A PNG/ TMX B/단일 GID 제거 C로 되돌려 전수 검토용으로 재구성. 추가 X/Y는 **위쪽 레이어를 의도적으로 가린 별도의 진단 합성**이며 원래 게임 장면이나 사용자 정의 다른 A의 D 실험이 아님.\n'
 f"- 원본 PNG A 해시 검증 **{audit['true_original_png_verified']}종**, 원본 B/C 재조립 **{audit['true_original_TMXS_rendered']}종**, 실제 B-C 변화 양수 **{audit['original_B_C_positive']}종**, 층 레이어 일부를 감춘 X-Y 변화 양수 **{audit['diagnostic_mask_positive']}종**, B-C 0이지만 X-Y에서만 드러난 **{audit['diagnostic_visible_but_original_zero']}종**. 이들은 아직 정체 관찰 완료나 공식 인증에 포함하지 않음.\n"
 f"- 물리 SQLite **244테이블**: 부모 v181 243개 모든 행 내용/수 보존, 증거 테이블 신규 202행. SHA256 {db['sqlite_sha256']}; integrity_check=ok.\n"
 '- 잠정 이미지 관찰 9829/10042(97.88%), 미관찰 213 유지(새키202, 기존9, 집계차이2), 최종 사물 정체·TileZed 공식 Local ID 인증 0. 가림 해제용 X/Y는 공식 A/B/C과 분리 기록.\n'
 '- 원본 TMX84/타일 PNG, 기존5409·수동80·제외14·held D2/JUMBO20, 과거 모든 파일 및 DB 불변.\n'
 '- 증거 review/v182_occlusion202/ 및 analysis/current/v182/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;text=f.read_text(encoding='utf-8')
 assert 'v181' in text
 i=text.index('\n')
 f.write_text(text[:i+1]+'\n'+summary+text[i+1:].lstrip('\n'),encoding='utf-8')
print('PASS v182 source/occlusion evidence no identity inflation',db['sqlite_sha256'])
