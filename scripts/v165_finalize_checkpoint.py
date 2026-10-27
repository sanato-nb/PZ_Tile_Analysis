#!/usr/bin/env python3
"""v165 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v165_abc_4000_4039/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v165/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v164/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v165':
 assert state['latest_checkpoint']['expanded_unique_observed']==9088+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v165'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==227
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v165 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v165 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v164'
assert state['latest_checkpoint']['expanded_unique_observed']==9088
assert state['unified_database']['version']=='v164'
assert review['manual_image_annotations']==40 and review['original_scope']==[4000,4039]
assert review['promoted_provisional']+review['excluded_unverified']==40
assert dbm['version']=='v165' and dbm['parent']=='v164'
assert dbm['prior_tables_preserved']==226 and dbm['table_count']==227
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9088+n
remaining=10042-obs
state['previous_checkpoint_v164']=parent
state['latest_checkpoint'].update(dict(
 version='v165',date='2026-10-28',kind='manual_A_B_C_taupe_bluegray_yellow_siding_gable_visual_review',
 physical_unified_sqlite_version='v165',prior_visual_checkpoint='v164',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v165_abc_4000_4039/VISUAL_REVIEW.csv',
 evidence_manifest='review/v165_abc_4000_4039/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v165_new_provisional=n,v165_excluded_unverified=review['excluded_unverified'],
 v165_exception_indices=review['excluded_indices'],v165_index_range=[4000,4039],
 v165_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Gray brick-pattern, blue-gray/yellow-beige horizontal siding and ochre brick-pattern gable pieces visually described. Source atlas Local ID, material, orientation and joining unverified. Zero B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v165',status='VERIFIED',repo_manifest='analysis/current/v165/MANIFEST.json',
 parent_unified_version='v164',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=227,prior_tables_preserved=226,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v165_visual_review_rows=n,certified=0
))
state['latest_v165_evidence']=dict(version='v165',source_indices=[4000,4039],
 manual_images_seen=40,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=226,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v165: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v165: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v165 원본 A/B/C 회갈색·청회색·황베이지·황갈색 박공 외벽 40종 검수 (2026-10-28)\n\n"
 f"- 원본 A050/B050/C050/차이 이미지 **40종** 직접 시각 관찰(첫 키의 B/C는 049). PNG RGBA·TMX raw GID·좌표·층·레이어 및 ZIP SHA/CRC 검사 후 **{n}종** 신규 잠정 후보, **{review['excluded_unverified']}종** 미세 변화·B−C=0·지도끝·이웃 누락·중복 보류. A/B/C 행 인덱스 차이는 키로 결합.\n"
 f"- 누적 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 최종 정체 인증·공식 Local ID/TileZed 매핑 모두 0.\n"
 f"- 물리 SQLite **227개 테이블**: 부모 v164 226개 테이블 및 모든 기존 행 수 보존, 신규 {n}행. SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\n"
 "- 회갈색 벽돌무늬·청회색/황베이지색 수평 사이딩·황갈색 벽돌무늬의 경사 박공 외벽 조각을 잠정 기록. 실제 재질·방향·연결 미확정, B−C=0·지도끝·이웃 누락·중복은 투명 확정 금지.\n"
 "- 기존 5,409종, 수동80·제외14, D held2/JUMBO20, 원본 84 TMX·Tiles PNG·이전 SQLite 보존. D는 같은 키의 공식 다른 A를 원래 B 동일 위치·층·레이어에서 교체해야 하며 아직 미검증.\n"
 "- 증거 review/v165_abc_4000_4039/, DB analysis/current/v165/MANIFEST.json.\n\n---\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v159' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v165 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
