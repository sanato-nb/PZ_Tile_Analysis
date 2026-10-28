#!/usr/bin/env python3
"""v171 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v171_interior_4360_4519/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v171/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v170/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v171':
 assert state['latest_checkpoint']['expanded_unique_observed']==9363+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v171'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==233
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v171 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v171 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v170'
assert state['latest_checkpoint']['expanded_unique_observed']==9363
assert state['unified_database']['version']=='v170'
assert review['manual_image_annotations']==160 and review['original_scope']==[4360,4519]
assert review['promoted_provisional']+review['excluded_unverified']==160
assert dbm['version']=='v171' and dbm['parent']=='v170'
assert dbm['prior_tables_preserved']==232 and dbm['table_count']==233
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9363+n
remaining=10042-obs
state['previous_checkpoint_v170']=parent
state['latest_checkpoint'].update(dict(
 version='v171',date='2026-10-28',kind='manual_A_B_C_large_bathroom_mosaic_interior_house_walls_visual_review',
 physical_unified_sqlite_version='v171',prior_visual_checkpoint='v170',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v171_interior_4360_4519/VISUAL_REVIEW.csv',
 evidence_manifest='review/v171_interior_4360_4519/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v171_new_provisional=n,v171_excluded_unverified=review['excluded_unverified'],
 v171_exception_indices=review['excluded_indices'],v171_index_range=[4360,4519],
 v171_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Bathroom mosaic borders, cream-gray tile walls and brightly colored interior wall and door/window fragments visually described from original A/B/C 054/055/056 image sheets. Source atlas Local ID, physical material, orientation and joining unverified. Zero or tiny B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v171',status='VERIFIED',repo_manifest='analysis/current/v171/MANIFEST.json',
 parent_unified_version='v170',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=233,prior_tables_preserved=232,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v171_visual_review_rows=n,certified=0
))
state['latest_v171_evidence']=dict(version='v171',source_indices=[4360,4519],
 manual_images_seen=160,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=232,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v171: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v171: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v171 원본 A/B/C 욕실타일·다색 장식띠·내벽/실내문 160종 검수 (2026-10-28)\\n\\n"
 f"- 원본 A054~056, TMX 주변 B054~056 및 한 타일 제거 C와 B−C 차이 시트 **160종** 실제 시각 관찰. 원본 PNG RGBA/실제 TMX raw GID·좌표·층·레이어/ZIP SHA·CRC 검사 후 **{n}종** 신규 provisional_candidate, **{review['excluded_unverified']}종** 시각불충분/변화0/지도끝/중복 보류.\\n"
 f"- 누적 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 정체 인증·공식 Local ID/TileZed 매핑 0.\\n"
 f"- 물리 SQLite **233개 테이블**: 부모 v170의 모든 232개 테이블 및 행 값·수 그대로 유지, 신규 {n}행, SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\\n"
 "- 흰색/회색 욕실 타일과 장식 모자이크, 연분홍·청색·녹색 실내 문/출입 프레임과 개구 있는 벽 조각의 가시 부분 형태를 잠정 기록. B−C=0·극소 부속·이웃 누락/기존 관찰은 투명·정체 인증으로 승격하지 않음.\\n"
 "- 기존5409·수동80·제외14·held D2/JUMBO20·원본84 TMX/Tiles PNG 및 과거 모든 자료 보존. 사용자 정의 D는 같은 키의 다른 공식 A를 원래 B 동일 위치·층·레이어에 넣는 대체 테스트, 이번 회차 정식 인증 없음.\\n"
 "- 증거 review/v171_interior_4360_4519/, DB analysis/current/v171/MANIFEST.json.\\n\\n---\\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v170' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v171 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
