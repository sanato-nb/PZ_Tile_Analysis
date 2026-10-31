#!/usr/bin/env python3
"""Commit v156 checkpoint only after source PNG/TMX, ZIP, and SQLite integrity checks."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
review=json.loads((R/'review/v156_walls_3440_3599/MANIFEST.json').read_text())
dbm=json.loads((R/'analysis/current/v156/MANIFEST.json').read_text())
state_path=R/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v155'
assert state['latest_checkpoint']['expanded_unique_observed']==8585
assert review['manual_image_annotations']==160
assert review['original_scope']==[3440,3599]
assert review['promoted_provisional']+review['excluded_unverified']==160
assert dbm['version']=='v156' and dbm['parent']=='v155'
assert dbm['table_count']==218 and dbm['prior_tables_preserved']==217
assert dbm['new_rows']==review['promoted_provisional'] and dbm['skipped_rows']==review['excluded_unverified']
assert dbm['parent_sqlite_sha256']==state['unified_database']['sqlite_sha256']
assert review['mapping_verified']==review['tilezed_verified']==review['certified']==0
n=review['promoted_provisional']
obs=8585+n
remaining=10042-obs
state['previous_checkpoint_v155']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v156',date='2026-10-28',
 kind='manual_A_B_C_house_wall_trim_frame_visual_review',
 physical_unified_sqlite_version='v156',prior_visual_checkpoint='v155',
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=obs,expanded_unique_unobserved=remaining,
 expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v156_walls_3440_3599/VISUAL_REVIEW.csv',
 evidence_manifest='review/v156_walls_3440_3599/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v156_new_provisional=n,v156_excluded_unverified=review['excluded_unverified'],
 v156_exception_indices=review['excluded_indices'],
 v156_index_range=[3440,3599],v156_sqlite_sha256=dbm['sqlite_sha256'],
 caution='Wall picture prints, decorative trim, siding walls, house window and door frames visually reviewed. Printed subjects/texts too small to certify. B-C zero, map boundary, missing neighbors, and previously observed duplicates are not newly observed or transparent. Authoritative atlas Local-ID/TileZed mapping and identity certifications remain zero.'
))
state['unified_database'].update(dict(
 version='v156',status='VERIFIED',repo_manifest='analysis/current/v156/MANIFEST.json',
 parent_unified_version='v155',sqlite_sha256=dbm['sqlite_sha256'],
 table_count=218,prior_tables_preserved=217,sqlite_size_bytes=dbm['sqlite_bytes'],
 all_prior_tables_preserved=True,
 expanded_observed_unique=obs,expanded_unobserved_unique=remaining,
 new_4633_observed=obs-5400,new_4633_unobserved=4633-(obs-5400),
 v156_visual_review_rows=n,certified=0
))
state['latest_v156_evidence']={
 'version':'v156','source_indices':[3440,3599],
 'manual_images_seen':160,'source_verified_provisional':n,
 'excluded_unverified':review['excluded_unverified'],
 'excluded_indices':review['excluded_indices'],
 'sqlite_sha256':dbm['sqlite_sha256'],
 'prior_tables_and_rows_preserved':217,
 'mapping_verified':0,'tilezed_verified':0,'certified':0,
 'observed_total':obs,'unobserved_remaining':remaining
}
state['next_actions']=[
 f'v156: {remaining} image-observation records still missing; do not call source A/B/C/D render completion final identity verification.',
 'v156: official TileZed/Local ID mapping and final identity certification still zero. Poster text and image subjects illegible are held as provisional.',
 *state.get('next_actions',[])
]
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v156 실물 A/B/C 벽 그림·몰딩·기둥·주택 외벽 창틀 검수 (2026-10-28)\n\n'
 f'- 원본 접촉시트 043/044 총 160종을 직접 시각 검토. 원본 PNG RGBA/실제 TMX GID·층·레이어·좌표/C 제거/ZIP CRC·SHA 검증 후 **{n}종**만 신규 provisional_candidate, '
 f'**{review["excluded_unverified"]}종**은 기존 관찰 중복·B−C 0·지도끝 등의 사유로 신규 관찰에서 제외. 투명 인증 불가.\n'
 f'- 전체 **{obs}/10,042종 ({obs/10042*100:.2f}%)** 이미지 관찰 기록, 미관찰 **{remaining}종**. 그림/글자 세부 판독 불가 항목은 특정 인물·문구로 추측하지 않음.\n'
 f'- **218개 물리 SQLite 테이블** (부모 v155 217개/모든 기존 행 수 그대로 보존, 신규 {n}행 1테이블), SHA256 {dbm["sqlite_sha256"]}, PRAGMA integrity_check=ok. '
 '증거 review/v156_walls_3440_3599의 CSV/ZIP/시각 검수판/예외표에 저장.\n'
 '- 원본 PNG/TMX, 기존 5,409, 수동80·제외14, held D2/JUMBO20 및 이전 DB 불변. 공식 Local ID/TileZed/정체 최종 인증 0; 사용자 정의 D 동일키 다른 A 공식 매핑 미검증.\n'
 '- 참고: 과거 v154 PROJECT_STATE의 일부 중복 메타데이터(범위와 table_count)가 실제 MANIFEST와 불일치했음. 이 버전의 활성 필드는 원본 v156 MANIFEST에 맞춰 정정하되 과거 증거/DB는 덮어쓰지 않음.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel
 original=p.read_text(encoding='utf-8')
 assert 'v155' in original
 newline=original.index('\n')
 p.write_text(original[:newline+1]+'\n'+summary+original[newline+1:].lstrip('\n'),encoding='utf-8')
print('PASS v156 checkpoint',obs,'observed',remaining,'remaining',dbm['sqlite_sha256'],flush=True)
