#!/usr/bin/env python3
"""Checkpoint v190 with strictly zero visual-observation/certification promotions."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v190_twelve_held_visual_source_recheck/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v190/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v189/MANIFEST.json').read_text())
path=R/'PROJECT_STATE.json';state=json.loads(path.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v189'
assert state['latest_checkpoint']['expanded_unique_observed']==9898 and state['latest_checkpoint']['expanded_unique_unobserved']==144
assert state['latest_checkpoint']['active_review_queue_remaining']==0
assert d['parent']=='v189' and d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==252 and d['prior_tables_preserved']==251 and d['new_rows']==12 and d['new_observed_rows']==0
assert m['individual_original_A_RGBA_and_PNG_SHA_verified']==12 and m['actual_source_TMX_raw_GID_verified']==12
assert m['newly_provisionally_observed']==0 and m['held']==12
assert m['previous_v188_exclusions_preserved'] is True
assert m['official_mapping_verified']==m['tilezed_verified']==m['certified']==0
state['previous_checkpoint_v189']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update({
 'version':'v190','date':'2026-10-28',
 'kind':'targeted_12_unverified_appearance_only_source_audit_held',
 'physical_unified_sqlite_version':'v190',
 'expanded_unique_observed':9898,'expanded_unique_unobserved':144,
 'expanded_observation_percent':9898/10042*100,
 'active_review_queue_remaining':0,
 'v190_source_checked':12,'v190_new_provisional':0,'v190_still_held':12,
 'v190_original_A_RGBA_sha_verified':12,'v190_original_TMX_raw_gid_verified':12,
 'v190_reviewed_indices':m['reviewed_indices'],
 'evidence_repo_path':'review/v190_twelve_held_visual_source_recheck/RECHECK_12.csv',
 'evidence_manifest':'review/v190_twelve_held_visual_source_recheck/MANIFEST.json',
 'v190_sqlite_sha256':d['sqlite_sha256'],
 'mapping_verified':0,'tilezed_verified':0,'approved_final_certifications':0,
 'caution':'One-time 12-key source-image and TMX audit. The originals remain physically/visually insufficient for independent identity: 4-73 pixel B-C differences for 11, 298 clipped at edge. Active v188 exclusions unchanged; source-name-family hypotheses are not official IDs or observed new items.'
})
state['unified_database'].update({
 'version':'v190','status':'VERIFIED_SOURCE_AUDIT_HOLDS_PRESERVED',
 'repo_manifest':'analysis/current/v190/MANIFEST.json','parent_unified_version':'v189',
 'sqlite_sha256':d['sqlite_sha256'],'table_count':252,'prior_tables_preserved':251,
 'sqlite_size_bytes':d['sqlite_bytes'],'all_prior_tables_preserved':True,
 'expanded_observed_unique':9898,'expanded_unobserved_unique':144,
 'v190_held_source_audit_rows':12,'certified':0
})
state['latest_v190_evidence']={'source_checked':12,'still_held':12,'newly_observed':0,
 'original_A_RGBA_verified':12,'original_TMX_verified':12,'physical_DB_tables':252,
 'prior_DB_tables_preserved':251,'database_sha256':d['sqlite_sha256'],
 'checkpoint_observed':9898,'checkpoint_unobserved':144,'physical_unobserved_keys':142,
 'historical_count_gap':2,'official_mapping_verified':0,'final_certified':0}
state['next_actions']=[
 'v190: keep 12 correctly source-audited but still ambiguous tile keys excluded from routine re-review; only reopen if new original source scene, unobscured imagery or official TileZed metadata is supplied.',
 'v190: two unresolved historical checkpoint count cases are accounting only; do not assign them invented tile-set/local IDs.',
 *state.get('next_actions',[])
]
path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v190 이전 보류 12종 A 원본·실제 TMX 증거 재검수 (2026-10-28)\n\n'
 '- 원본 A 접촉시트에서 12종의 실제 형태를 다시 구별하되, 298은 지도끝 잘림, 다른 11종은 원래 B−C 변화가 4~73픽셀 등으로 충분한 사물 독립 형상을 보여주지 못함. 4024의 다른 실제 TMX 배치도 기존 v180에서 변화12픽셀로 근거 불충분.\n'
 '- 실제 PNG SHA256/선택 RGBA 픽셀 SHA256, TMX 파일 SHA/원본 firstgid·raw GID·층·레이어·좌표를 각각 12종 검증, v182·v183·v188·v180 기록과 고유키 대조. 개별 노트는 눈에 보이는 형태/부분계열과 무엇을 확정할 수 없는지를 분리 기록.\n'
 '- 새 관찰+0, 공식 Local ID/TileZed 정체 인증+0; v188 검수 제외 유지. 누적 이미지 잠정 관찰 **9,898/10,042(98.57%)**, 기록상 미관찰144 (실물142+역사적 누적 집계차이2).\n'
 f"- 물리 SQLite **252테이블**: 부모 v189 251테이블의 모든 행 값·수 보존, 신규 12행 증거 1테이블, SHA256 {d['sqlite_sha256']}, PRAGMA integrity_check=ok.\n"
 '- 원본 84 TMX/Tiles PNG, 사용자 이전 수동검수80/제외 항목, 기존 5409·D-held2/JUMBO-held20·과거 DB·증거 전부 보존.\n'
 '- 증거 review/v190_twelve_held_visual_source_recheck/ 와 analysis/current/v190/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;old=f.read_text(encoding='utf-8')
 assert 'v189' in old
 i=old.index('\n')
 f.write_text(old[:i+1]+'\n'+summary+old[i+1:].lstrip('\n'),encoding='utf-8')
print('PASS v190 12 inspected, all held, 252 preserved SQLite tables, observation unchanged 9898/10042')
