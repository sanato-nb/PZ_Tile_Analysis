#!/usr/bin/env python3
"""v174 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v174_reinspection_held58/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v174/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v173/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v174':
 assert state['latest_checkpoint']['expanded_unique_observed']==9612+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v174'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==236
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v174 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v174 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v173'
assert state['latest_checkpoint']['expanded_unique_observed']==9612
assert state['unified_database']['version']=='v173'
assert review['manual_image_annotations']==58 and review['original_scope']==[3680,4159]
assert review['promoted_provisional']+review['excluded_unverified']==58
assert dbm['version']=='v174' and dbm['parent']=='v173'
assert dbm['prior_tables_preserved']==235 and dbm['table_count']==236
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9612+n
remaining=10042-obs
state['previous_checkpoint_v173']=parent
state['latest_checkpoint'].update(dict(
 version='v174',date='2026-10-28',kind='manual_A_B_C_followup_held58_masonry_siding_gable_reinspection',
 physical_unified_sqlite_version='v174',prior_visual_checkpoint='v173',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v174_reinspection_held58/VISUAL_REVIEW.csv',
 evidence_manifest='review/v174_reinspection_held58/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v174_new_provisional=n,v174_excluded_unverified=review['excluded_unverified'],
 v174_exception_indices=review['excluded_indices'],v174_index_range=[3680,4159],v174_reviewed_indices=review['reviewed_indices'],
 v174_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Review 58 earlier manually held roof gable/masonry/siding fragments. 49 low-confidence possible same-family parts and 9 retained held; all accepted descriptions provisional, neither official nor final identity. Source atlas Local ID, physical material, orientation and joining unverified. Zero or tiny B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v174',status='VERIFIED',repo_manifest='analysis/current/v174/MANIFEST.json',
 parent_unified_version='v173',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=236,prior_tables_preserved=235,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v174_visual_review_rows=n,certified=0
))
state['latest_v174_evidence']=dict(version='v174',source_indices=[3680,4159],
 manual_images_seen=58,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=235,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v174: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v174: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v174 A/B/C 기존 시각근거 부족 박공·사이딩 보류 58종 재검수 (2026-10-28)\\n\\n"
 f"- 기존 v158/v160~v168에서 오직 수동 시각근거 부족으로 보류된 **58종**을 원본 A/B/C046~051의 인접 벽판과 재대조. PNG RGBA, 실제 TMX GID·좌표·층·레이어, C 한 타일 제거/B-C/ZIP SHA·CRC/기존 DB 중복 검사 후 **{n}종** 낮은 신뢰도의 신규 provisional_candidate, **{review['excluded_unverified']}종** 지속 보류.\\n"
 f"- 누적 잠정 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 공식 Local ID↔원본 PNG·TileZed 대응·사물 최종 인증 0.\\n"
 f"- 물리 SQLite **236테이블**, 부모 v173의 기존 **235테이블** 모든 행 값 및 행 수 보존, 신규 {n}행, SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\\n"
 "- 미세한 박공 경계·세로 사이딩·벽돌/석재무늬 벽판 후보. 신규는 confidence=low, 방향·연결과 물성·정체 최종 인증 미정. 다른 사유 B-C=0/맵끝/이웃 부족/기존 중복 타일은 대상에서 제외.\\n"
 "- 원본 TMX 84개·Tiles PNG·기존5409·수동80/제외14/held D2/JUMBO20/과거 모든 DB CSV ZIP 보존. 같은 ID의 다른 A를 기존 B 동일 좌표·층·레이어에 넣는 공식 사용자 정의 D 정식 인증 미실행.\\n"
 "- 증거 review/v174_reinspection_held58/, DB analysis/current/v174/MANIFEST.json.\\n\\n---\\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v173' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v174 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
