#!/usr/bin/env python3
"""v173 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v173_reinspection_held89/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v173/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v172/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v173':
 assert state['latest_checkpoint']['expanded_unique_observed']==9564+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v173'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==235
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v173 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v173 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v172'
assert state['latest_checkpoint']['expanded_unique_observed']==9564
assert state['unified_database']['version']=='v172'
assert review['manual_image_annotations']==89 and review['original_scope']==[4160,4632]
assert review['promoted_provisional']+review['excluded_unverified']==89
assert dbm['version']=='v173' and dbm['parent']=='v172'
assert dbm['prior_tables_preserved']==234 and dbm['table_count']==235
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9564+n
remaining=10042-obs
state['previous_checkpoint_v172']=parent
state['latest_checkpoint'].update(dict(
 version='v173',date='2026-10-28',kind='manual_A_B_C_followup_held89_family_part_reinspection',
 physical_unified_sqlite_version='v173',prior_visual_checkpoint='v172',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v173_reinspection_held89/VISUAL_REVIEW.csv',
 evidence_manifest='review/v173_reinspection_held89/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v173_new_provisional=n,v173_excluded_unverified=review['excluded_unverified'],
 v173_exception_indices=review['excluded_indices'],v173_index_range=[4160,4632],v173_reviewed_indices=review['reviewed_indices'],
 v173_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Review 89 earlier manually held roof gable, siding, garage frame and bathroom tile fragments. 48 conditionally eligible on recognizable same-family parts, 41 retained held. All accepted descriptions low-confidence provisional only, not official. Source atlas Local ID, physical material, orientation and joining unverified. Zero or tiny B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v173',status='VERIFIED',repo_manifest='analysis/current/v173/MANIFEST.json',
 parent_unified_version='v172',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=235,prior_tables_preserved=234,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v173_visual_review_rows=n,certified=0
))
state['latest_v173_evidence']=dict(version='v173',source_indices=[4160,4632],
 manual_images_seen=89,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=234,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v173: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v173: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v173 A/B/C 과거 시각근거 부족 보류 89종 재검수 — 낮은 신뢰도 잠정 기록 (2026-10-28)\\n\\n"
 f"- 기존 v169~v172 수동 시각근거 부족만을 근거로 보류했던 89종의 원본 A052~057/B 원래 TMX 장면/C 단일 GID 제거 및 B−C를 다시 검토. PNG RGBA/원본 TMX GID·좌표·층·레이어/ZIP SHA·CRC/이전 관찰 중복 검사 후 **{n}종** 낮은 확신의 신규 provisional_candidate, **{review['excluded_unverified']}종** 계속 보류. 정확한 역할은 같은 계열 부품 추론이며 최종정체 인증이 아님.\\n"
 f"- 누적 이미지 잠정 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 여전히 미관찰 **{remaining}종**. 공식 Local ID/TileZed 매핑·사물 최종 인증 0.\\n"
 f"- 물리 SQLite **235개 테이블**: 부모 v172의 모든 234개 테이블/각 행의 전 값·행 수 보존, 신규 {n}행, SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\\n"
 "- 지붕/박공벽·사이딩·차고 문틀·욕실 모자이크 경계 부품을 주변 원본 A/B/C 확인하며 재검수. B−C=0·기존 중복·원본 이웃/지도끝 부족 등은 절대 인증/투명으로 승격하지 않음. 모든 신규 기록도 confidence=low 및 방향·연결 미확정.\\n"
 "- 원본 84 TMX/PNG, 기존 5409·수동80·제외14·D held2/JUMBO20 및 과거 모든 SQLite/CSV/ZIP 보존. 사용자 D 공식 대체A 정식 인증 0.\\n"
 "- 증거 review/v173_reinspection_held89/, 물리 DB analysis/current/v173/MANIFEST.json.\\n\\n---\\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v172' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v173 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
