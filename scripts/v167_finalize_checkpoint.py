#!/usr/bin/env python3
"""v167 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v167_abc_4080_4119/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v167/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v166/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v167':
 assert state['latest_checkpoint']['expanded_unique_observed']==9147+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v167'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==229
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v167 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v167 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v166'
assert state['latest_checkpoint']['expanded_unique_observed']==9147
assert state['unified_database']['version']=='v166'
assert review['manual_image_annotations']==40 and review['original_scope']==[4080,4119]
assert review['promoted_provisional']+review['excluded_unverified']==40
assert dbm['version']=='v167' and dbm['parent']=='v166'
assert dbm['prior_tables_preserved']==228 and dbm['table_count']==229
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9147+n
remaining=10042-obs
state['previous_checkpoint_v166']=parent
state['latest_checkpoint'].update(dict(
 version='v167',date='2026-10-28',kind='manual_A_B_C_rose_olive_siding_and_ochre_brick_gable_visual_review',
 physical_unified_sqlite_version='v167',prior_visual_checkpoint='v166',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v167_abc_4080_4119/VISUAL_REVIEW.csv',
 evidence_manifest='review/v167_abc_4080_4119/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v167_new_provisional=n,v167_excluded_unverified=review['excluded_unverified'],
 v167_exception_indices=review['excluded_indices'],v167_index_range=[4080,4119],
 v167_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Dusty-rose and olive-green horizontal siding and ochre brick-pattern gable wall fragments visually described from original A/B/C and full source PNG atlases. Source atlas Local ID, physical material, orientation and joining unverified. Zero or tiny B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v167',status='VERIFIED',repo_manifest='analysis/current/v167/MANIFEST.json',
 parent_unified_version='v166',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=229,prior_tables_preserved=228,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v167_visual_review_rows=n,certified=0
))
state['latest_v167_evidence']=dict(version='v167',source_indices=[4080,4119],
 manual_images_seen=40,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=228,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v167: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v167: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v167 원본 A/B/C 황갈색·적갈색 벽돌무늬와 분홍회색 사이딩 박공벽 40종 검수 (2026-10-28)\n\n"
 f"- 원본 A050/B050/C050/차이 이미지 **40종** 직접 시각 관찰하고 원본 30_07·30_08·30_09 PNG 전체 아틀라스에서 실제 줄눈/가로널 무늬 확인. PNG RGBA·TMX raw GID·좌표·층·레이어 및 ZIP SHA/CRC 검사 후 **{n}종** 신규 잠정 후보, **{review['excluded_unverified']}종** B−C 미세/0·지도끝·이웃 누락·중복 보류. A/B/C 인덱스 차이는 타일 키로 결합.\n"
 f"- 누적 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 최종 정체 인증·공식 Local ID/TileZed 매핑 모두 0.\n"
 f"- 물리 SQLite **229개 테이블**: 부모 v166 228개 테이블 및 모든 기존 행 수 보존, 신규 {n}행. SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\n"
 "- 황갈색·밝은 베이지 벽돌무늬, 적갈색 벽돌무늬, 분홍회색 수평 사이딩의 경사 박공 외벽 단편을 잠정 기록. 실제 재질·방향·연결 미확정, B−C=0·미세 변화·지도끝·이웃 누락·중복은 투명 확정 금지.\n"
 "- 기존 5,409종, 수동80·제외14, D held2/JUMBO20, 원본 84 TMX·Tiles PNG·이전 SQLite 보존. D는 같은 키의 공식 다른 A를 원래 B 동일 위치·층·레이어에서 교체해야 하며 아직 미검증.\n"
 "- 증거 review/v167_abc_4080_4119/, DB analysis/current/v167/MANIFEST.json.\n\n---\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v166' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v167 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
