#!/usr/bin/env python3
"""v170 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v170_large_4200_4359/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v170/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v169/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v170':
 assert state['latest_checkpoint']['expanded_unique_observed']==9235+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v170'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==232
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v170 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v170 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v169'
assert state['latest_checkpoint']['expanded_unique_observed']==9235
assert state['unified_database']['version']=='v169'
assert review['manual_image_annotations']==160 and review['original_scope']==[4200,4359]
assert review['promoted_provisional']+review['excluded_unverified']==160
assert dbm['version']=='v170' and dbm['parent']=='v169'
assert dbm['prior_tables_preserved']==231 and dbm['table_count']==232
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9235+n
remaining=10042-obs
state['previous_checkpoint_v169']=parent
state['latest_checkpoint'].update(dict(
 version='v170',date='2026-10-28',kind='manual_A_B_C_large_roof_garage_bathroom_visual_review',
 physical_unified_sqlite_version='v170',prior_visual_checkpoint='v169',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v170_large_4200_4359/VISUAL_REVIEW.csv',
 evidence_manifest='review/v170_large_4200_4359/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v170_new_provisional=n,v170_excluded_unverified=review['excluded_unverified'],
 v170_exception_indices=review['excluded_indices'],v170_index_range=[4200,4359],
 v170_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Dark roof gable, cream vertical siding, wooden exterior frame, metal garage shutter and tiled bathroom partition components visually described from original A/B/C contact sheets and source PNG. Source atlas Local ID, physical material, orientation and joining unverified. Zero or tiny B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v170',status='VERIFIED',repo_manifest='analysis/current/v170/MANIFEST.json',
 parent_unified_version='v169',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=232,prior_tables_preserved=231,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v170_visual_review_rows=n,certified=0
))
state['latest_v170_evidence']=dict(version='v170',source_indices=[4200,4359],
 manual_images_seen=160,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=231,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v170: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v170: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v170 원본 A/B/C 대형 검수 160종 — 박공 지붕·외벽·차고문·욕실 칸막이 (2026-10-28)\\n\\n"
 f"- 직접 열람한 A052~054, B052~054, C/차이052~054의 타일 **160종**. PNG RGBA·실제 TMX GID/층/레이어/좌표 및 B/C/DIFF ZIP SHA/CRC를 검증한 **{n}종** 신규 잠정 후보, **{review['excluded_unverified']}종** 보류/중복. 직접 보기에 작은 부분은 사전 수동 보류. 인덱스가 아닌 고유키로 대응.\\n"
 f"- 누적 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 최종 정체 인증·공식 Local ID/TileZed 매핑 0.\\n"
 f"- 물리 SQLite **232개 테이블**: 부모 v169의 기존 231개 테이블과 모든 행 값·수 보존. 신규 {n}행, SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\\n"
 "- 지붕 판과 박공·차고 셔터·욕실 칸막이 등 부분 형태 잠정 기록. 실제 재질·방향·연결/완성 사물 공식 대응 미검증. B−C=0/지도 끝/이웃 누락/기존 관찰 중복은 투명 또는 인증으로 취급하지 않음.\\n"
 "- 기존5409, 수동80·제외14, D 보류2/JUMBO20, 원본84 TMX·Tiles PNG/과거 모든 DB 불변. D의 올바른 의미는 같은 키의 공식 다른 A를 원래 B의 동일 자리·층·레이어에 넣어 비교하는 것이며 이번 회차 미실행.\\n"
 "- 근거 review/v170_large_4200_4359/, DB analysis/current/v170/MANIFEST.json.\\n\\n---\\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v169' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v170 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
