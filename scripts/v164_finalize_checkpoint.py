#!/usr/bin/env python3
"""v164 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v164_abc_3960_3999/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v164/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v163/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v164':
 assert state['latest_checkpoint']['expanded_unique_observed']==9061+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v164'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==226
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v164 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v164 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v163'
assert state['latest_checkpoint']['expanded_unique_observed']==9061
assert state['unified_database']['version']=='v163'
assert review['manual_image_annotations']==40 and review['original_scope']==[3960,3999]
assert review['promoted_provisional']+review['excluded_unverified']==40
assert dbm['version']=='v164' and dbm['parent']=='v163'
assert dbm['prior_tables_preserved']==225 and dbm['table_count']==226
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9061+n
remaining=10042-obs
state['previous_checkpoint_v163']=parent
state['latest_checkpoint'].update(dict(
 version='v164',date='2026-10-28',kind='manual_A_B_C_brick_brown_gray_siding_gable_visual_review',
 physical_unified_sqlite_version='v164',prior_visual_checkpoint='v163',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v164_abc_3960_3999/VISUAL_REVIEW.csv',
 evidence_manifest='review/v164_abc_3960_3999/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v164_new_provisional=n,v164_excluded_unverified=review['excluded_unverified'],
 v164_exception_indices=review['excluded_indices'],v164_index_range=[3960,3999],
 v164_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Brown-red brick-pattern and gray/beige horizontal siding gable pieces visually described. Source atlas Local ID, material, orientation and joining unverified. Zero B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v164',status='VERIFIED',repo_manifest='analysis/current/v164/MANIFEST.json',
 parent_unified_version='v163',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=226,prior_tables_preserved=225,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v164_visual_review_rows=n,certified=0
))
state['latest_v164_evidence']=dict(version='v164',source_indices=[3960,3999],
 manual_images_seen=40,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=225,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v164: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v164: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v164 원본 A/B/C 벽돌무늬·회갈색·베이지색 박공 외벽 40종 검수 (2026-10-28)\\n\\n"
 f"- 원본 A049/B049/C049/차이 이미지 **40종** 직접 시각 관찰. PNG RGBA·TMX 원시 GID·좌표·층·레이어 및 ZIP SHA/CRC 검사 후 **{n}종** 신규 잠정 후보, **{review['excluded_unverified']}종** 판독 부족·B−C=0·지도끝·이웃 누락·중복 보류.\\n"
 f"- 누적 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 최종 정체 인증·공식 Local ID/TileZed 매핑 모두 0.\\n"
 f"- 물리 SQLite **226개 테이블**: 부모 v163 225테이블 및 모든 기존 행 수 보존, 신규 {n}행. SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\\n"
 "- 적갈색 벽돌무늬 박공벽, 회갈색·베이지색 수평 사이딩 경사 외벽 조각을 타일별로 잠정 기록. 정확한 연결·방향·재질 미확정, 미세 변화·가림·지도끝·중복은 투명 확정 금지.\\n"
 "- 기존 5,409종, 수동80·제외14, D held2/JUMBO20, 원본 84 TMX·Tiles PNG·이전 SQLite 보존. D는 같은 키의 공식 다른 A를 원래 B 동일 위치·층·레이어에서 교체해야 하며 아직 미검증.\\n"
 "- 증거 review/v164_abc_3960_3999/, DB analysis/current/v164/MANIFEST.json.\\n\\n---\\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v159' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v164 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
