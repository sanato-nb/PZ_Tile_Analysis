#!/usr/bin/env python3
"""Commit v158 checkpoint only after source PNG/TMX, ZIP, and SQLite integrity checks."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v158_roofgables_3680_3759/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v158/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version'] in ('v157','v158')
if state['latest_checkpoint']['version']=='v158':
    assert state['latest_checkpoint']['expanded_unique_observed']==8811+review['promoted_provisional']
    assert state['previous_checkpoint_v157']['version']=='v157'
    assert state['previous_checkpoint_v157']['expanded_unique_observed']==8811
    parent_checkpoint=state['previous_checkpoint_v157']
else:
    assert state['latest_checkpoint']['expanded_unique_observed']==8811
    parent_checkpoint=state['latest_checkpoint']
assert review['manual_image_annotations']==80
assert review['original_scope']==[3680,3759]
assert review['promoted_provisional']+review['excluded_unverified']==80
assert dbm['version']=='v158' and dbm['parent']=='v157'
assert dbm['table_count']==220 and dbm['prior_tables_preserved']==219
assert dbm['new_rows']==review['promoted_provisional'] and dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==json.loads((R/'analysis/current/v157/MANIFEST.json').read_text())['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
n=review['promoted_provisional']
obs=8811+n
remaining=10042-obs
state['previous_checkpoint_v157']=json.loads(json.dumps(parent_checkpoint))
state['latest_checkpoint'].update(dict(
 version='v158',date='2026-10-28',
 kind='manual_A_B_C_gable_roof_sidewall_visual_review',
 physical_unified_sqlite_version='v158',prior_visual_checkpoint='v157',
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=obs,expanded_unique_unobserved=remaining,
 expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v158_roofgables_3680_3759/VISUAL_REVIEW.csv',
 evidence_manifest='review/v158_roofgables_3680_3759/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v158_new_provisional=n,v158_excluded_unverified=review['excluded_unverified'],
 v158_exception_indices=review['excluded_indices'],
 v158_index_range=[3680,3759],v158_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Roof gable wall siding, slanted end-wall panels, small triangular connector pieces and roof-side wall fragments visually reviewed; exact official connections and orientations remain unverified. B-C zero, map boundary, missing neighbors, and previously observed duplicates are not newly observed or transparent. Authoritative atlas Local-ID/TileZed mapping and identity certifications remain zero.'
))
state['unified_database'].update(dict(
 version='v158',status='VERIFIED',repo_manifest='analysis/current/v158/MANIFEST.json',
 parent_unified_version='v157',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=220,prior_tables_preserved=219,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,
 expanded_observed_unique=obs,expanded_unobserved_unique=remaining,
 new_4633_observed=obs-5400,new_4633_unobserved=4633-(obs-5400),
 v158_visual_review_rows=n,certified=0
))
state['latest_v158_evidence']={
 'version':'v158','source_indices':[3680,3759],
 'manual_images_seen':80,'source_verified_provisional':n,
 'excluded_unverified':review['excluded_unverified'],
 'excluded_indices':review['excluded_indices'],
 'sqlite_sha256':dbm['sqlite_sha256'],
 'prior_tables_and_rows_preserved':219,
 'mapping_verified':0,'tilezed_verified':0,'certified':0,
 'observed_total':obs,'unobserved_remaining':remaining
}
state['next_actions']=[
 f'v158: {remaining} image-observation records still missing; do not call source A/B/C/D render completion final identity verification.',
 'v158: official TileZed/Local ID mapping and final identity certification still zero. Gable-wall piece connection and orientation are provisional, not certified.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v158 실물 A/B/C 지붕 박공벽·경사 외벽판·연결 쐐기 검수 (2026-10-28)\n\n'
 f'- 원본 접촉시트 046 총 80종을 직접 시각 검토. 원본 PNG RGBA/실제 TMX GID·층·레이어·좌표/C 제거/ZIP CRC·SHA 검증 후 **{n}종**만 신규 provisional_candidate, '
 f'**{review["excluded_unverified"]}종**은 기존 관찰 중복·B−C 0·지도끝 등의 사유로 신규 관찰에서 제외. 투명 인증 불가.\n'
 f'- 전체 **{obs}/10,042종 ({obs/10042*100:.2f}%)** 이미지 관찰 기록, 미관찰 **{remaining}종**. 박공벽 연결·방향·정확한 부품 규격은 공식 검증 전까지 보류.\n'
 f'- **220개 물리 SQLite 테이블** (부모 v157 219개/모든 기존 행 수 그대로 보존, 신규 {n}행 1테이블), SHA256 {dbm["sqlite_sha256"]}, PRAGMA integrity_check=ok. '
 '증거 review/v158_roofgables_3680_3759의 CSV/ZIP/시각 검수판/예외표에 저장.\n'
 '- 원본 PNG/TMX, 기존 5,409, 수동80·제외14, held D2/JUMBO20 및 이전 DB 불변. 공식 Local ID/TileZed/정체 최종 인증 0; 사용자 정의 D 동일키 다른 A 공식 매핑 미검증.\n'
 '- v158은 v157 물리 DB에서만 파생하고 기존 자료를 변경하지 않음.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v157' in original
 newline=original.index('\n')
 tail=original[newline+1:].lstrip('\n')
 if tail.startswith('## v158 '):
  boundary=tail.find('\n---\n## v157 ')
  assert boundary>=0, 'Cannot locate prior v157 handoff boundary'
  tail=tail[boundary+len('\n---\n'):]
 p.write_text(original[:newline+1]+'\n'+summary+tail,encoding='utf-8')
print('PASS v158 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
