#!/usr/bin/env python3
"""v172 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v172_interior_4520_4632/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v172/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v171/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v172':
 assert state['latest_checkpoint']['expanded_unique_observed']==9469+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v172'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==234
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v172 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v172 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v171'
assert state['latest_checkpoint']['expanded_unique_observed']==9469
assert state['unified_database']['version']=='v171'
assert review['manual_image_annotations']==113 and review['original_scope']==[4520,4632]
assert review['promoted_provisional']+review['excluded_unverified']==113
assert dbm['version']=='v172' and dbm['parent']=='v171'
assert dbm['prior_tables_preserved']==233 and dbm['table_count']==234
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9469+n
remaining=10042-obs
state['previous_checkpoint_v171']=parent
state['latest_checkpoint'].update(dict(
 version='v172',date='2026-10-28',kind='manual_A_B_C_last_source_113_interior_and_log_walls_visual_review',
 physical_unified_sqlite_version='v172',prior_visual_checkpoint='v171',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v172_interior_4520_4632/VISUAL_REVIEW.csv',
 evidence_manifest='review/v172_interior_4520_4632/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v172_new_provisional=n,v172_excluded_unverified=review['excluded_unverified'],
 v172_exception_indices=review['excluded_indices'],v172_index_range=[4520,4632],
 v172_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Various interior house wall segmented door openings, cream/gray frame fragments and wooden log-wall entrance panels visually described from original A/B/C 056/057 image sheets. Source atlas Local ID, physical material, orientation and joining unverified. Zero or tiny B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v172',status='VERIFIED',repo_manifest='analysis/current/v172/MANIFEST.json',
 parent_unified_version='v171',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=234,prior_tables_preserved=233,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v172_visual_review_rows=n,certified=0
))
state['latest_v172_evidence']=dict(version='v172',source_indices=[4520,4632],
 manual_images_seen=113,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=233,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v172: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v172: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v172 원본 A/B/C 첫패스 마지막 113종: 실내벽 개구·통나무 벽 (2026-10-28)\\n\\n"
 f"- 직접 시각 열람한 A056/057, 원래 TMX B056/057, 같은 위치 대상 GID 단일 제거 C·차이 시트 **113종**. 원본 PNG RGBA/TMX raw GID·위치·층·레이어/B-C/ZIP SHA·CRC 검사 후 **{n}종** 신규 provisional_candidate, **{review['excluded_unverified']}종** 사전 시각보류·픽셀변화0·경계·기검수 중복·B/C 원본 근거 누락으로 보류.\\n"
 f"- 누적 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 정체 최종 인증·공식 Local ID/TileZed 매핑 0.\\n"
 f"- 물리 SQLite **234테이블**, 부모 v171 233테이블 전부 과거 행 값·수 그대로 보존. 신규 {n}행, SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\\n"
 "- 밝은 실내 문·높이별 지그재그 벽 개구, 도장 목재/벽지, 마지막 통나무 창/문 외벽 후보를 잠정 관찰. 아주 작은 단부는 인증 보류; B−C=0은 투명이 아니며 원본 B/C 한 키 누락을 허위 원본으로 치환하지 않음.\\n"
 "- 기존5409·수동80·제외14·held D2/JUMBO20·원본 84 TMX/PNG와 역사적 모든 DB/CSV 보존. D는 동일 키의 다른 공식 A를 원래 B의 동일 위치·층·레이어에서 비교하는 것이고 이번 회차 최종 인증 없음.\\n"
 "- 근거 review/v172_interior_4520_4632/, DB analysis/current/v172/MANIFEST.json.\\n\\n---\\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v171' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v172 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
