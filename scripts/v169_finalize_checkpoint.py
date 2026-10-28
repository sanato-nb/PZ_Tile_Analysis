#!/usr/bin/env python3
"""v169 checkpoint after all source/SQLite independent verification has passed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v169_abc_4120_4159/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v169/MANIFEST.json').read_text())
parent_dbm=json.loads((R/'analysis/current/v168/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
# Re-validation of a checkpoint already materialized by the same workflow must be safe.
if state['latest_checkpoint']['version']=='v169':
 assert state['latest_checkpoint']['expanded_unique_observed']==9209+review['promoted_provisional']
 assert state['latest_checkpoint']['expanded_unique_unobserved']==10042-state['latest_checkpoint']['expanded_unique_observed']
 assert state['unified_database']['version']=='v169'
 assert state['unified_database']['sqlite_sha256']==dbm['sqlite_sha256']
 assert state['unified_database']['table_count']==231
 assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
 assert dbm['new_rows']==review['promoted_provisional']
 assert dbm['skipped_rows']==review['excluded_unverified']
 assert dbm['mapping_verified']==dbm['tilezed_verified']==dbm['certified']==0
 for rel in ['AGENTS.md','docs/HANDOFF.md']:
  assert '## v169 ' in (R/rel).read_text(encoding='utf-8')
 print('PASS v169 already materialized; verified idempotent checkpoint',dbm['sqlite_sha256'],flush=True)
 raise SystemExit(0)
assert state['latest_checkpoint']['version']=='v168'
assert state['latest_checkpoint']['expanded_unique_observed']==9209
assert state['unified_database']['version']=='v168'
assert review['manual_image_annotations']==40 and review['original_scope']==[4160,4199]
assert review['promoted_provisional']+review['excluded_unverified']==40
assert dbm['version']=='v169' and dbm['parent']=='v168'
assert dbm['prior_tables_preserved']==230 and dbm['table_count']==231
assert dbm['new_rows']==review['promoted_provisional']
assert dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==parent_dbm['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
parent=json.loads(json.dumps(state['latest_checkpoint']))
n=review['promoted_provisional']
obs=9209+n
remaining=10042-obs
state['previous_checkpoint_v168']=parent
state['latest_checkpoint'].update(dict(
 version='v169',date='2026-10-28',kind='manual_A_B_C_beige_plaster_cream_siding_red_wood_gable_visual_review',
 physical_unified_sqlite_version='v169',prior_visual_checkpoint='v168',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v169_abc_4120_4159/VISUAL_REVIEW.csv',
 evidence_manifest='review/v169_abc_4120_4159/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v169_new_provisional=n,v169_excluded_unverified=review['excluded_unverified'],
 v169_exception_indices=review['excluded_indices'],v169_index_range=[4160,4199],
 v169_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Beige smooth wall fragments, cream horizontal siding with dark roof-edge trim, and reddish-brown vertical plank gable wall fragments visually described from original A/B/C and source PNG atlases. Source atlas Local ID, physical material, orientation and joining unverified. Zero or tiny B-C, map edge, missing neighbors and duplicates never transparent or certified.'
))
state['unified_database'].update(dict(
 version='v169',status='VERIFIED',repo_manifest='analysis/current/v169/MANIFEST.json',
 parent_unified_version='v168',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=231,prior_tables_preserved=230,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,
 expanded_unobserved_unique=remaining,new_4633_observed=obs-5400,
 new_4633_unobserved=4633-(obs-5400),v169_visual_review_rows=n,certified=0
))
state['latest_v169_evidence']=dict(version='v169',source_indices=[4160,4199],
 manual_images_seen=40,source_verified_provisional=n,
 excluded_unverified=review['excluded_unverified'],
 excluded_indices=review['excluded_indices'],sqlite_sha256=dbm['sqlite_sha256'],
 prior_tables_and_rows_preserved=230,mapping_verified=0,tilezed_verified=0,
 certified=0,observed_total=obs,unobserved_remaining=remaining)
state['next_actions']=[
 f'v169: {remaining} image observations remain; source images and ABCD renders are not final identity certification.',
 'v169: official TileZed/Local ID and same-key alternative A mapping unverified; no final certifications.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 "## v169 원본 A/B/C 연베이지 평활 벽·크림 수평 사이딩·적갈색 세로 널판 박공 외벽 40종 검수 (2026-10-28)\n\n"
 f"- 원본 A052/B051-052/C051-052 및 차이 접촉시트 **40종** 직접 시각 관찰, 원본 walls_exterior_roofs_30_14/15/16/17 PNG 아틀라스 무늬 대조. PNG RGBA·TMX raw GID·좌표·층·레이어 및 ZIP SHA/CRC 검사 후 **{n}종** 신규 잠정 후보, **{review['excluded_unverified']}종** 미세/0·지도끝·이웃 누락·중복 보류. A/B/C 인덱스는 키로 결합.\n"
 f"- 누적 이미지 관찰 **{obs}/10,042 ({obs/10042*100:.2f}%)**, 미관찰 **{remaining}종**. 최종 정체 인증·공식 Local ID/TileZed 매핑 모두 0.\n"
 f"- 물리 SQLite **231개 테이블**: 부모 v168 230개 테이블 및 모든 기존 행 수·내용 보존, 신규 {n}행. SHA256 {dbm['sqlite_sha256']}, integrity_check=ok.\n"
 "- 연베이지 평활 벽면, 크림색 수평 사이딩과 검은 경사 마감선, 적갈색 세로 널판무늬 박공 외벽 조각을 잠정 기록. 실제 재질·방향·연결 미확정, B−C=0·미세 변화·지도끝·이웃 누락·중복은 투명 확정 금지.\n"
 "- 기존 5,409종, 수동80·제외14, D held2/JUMBO20, 원본 84 TMX·Tiles PNG·이전 SQLite 보존. D는 같은 키의 공식 다른 A를 원래 B 동일 위치·층·레이어에서 교체해야 하며 아직 미검증.\n"
 "- 증거 review/v169_abc_4160_4199/, DB analysis/current/v169/MANIFEST.json.\n\n---\n"
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v168' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v169 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
