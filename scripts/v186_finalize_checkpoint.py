#!/usr/bin/env python3
"""Finalize v186 only after source hashes + SQLite exact parent rows validated."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v186_object_disambiguation_49/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v186/MANIFEST.json').read_text())
parent=json.loads((R/'analysis/current/v185/MANIFEST.json').read_text())
p=R/'PROJECT_STATE.json'
state=json.loads(p.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v185'
assert state['latest_checkpoint']['expanded_unique_observed']==9898
assert state['latest_checkpoint']['expanded_unique_unobserved']==144
assert state['unified_database']['version']=='v185'
assert d['version']=='v186' and d['parent']=='v185'
assert d['parent_sqlite_sha256']==parent['sqlite_sha256']
assert d['new_rows']==49 and d['new_observed_rows']==0
assert d['table_count']==248 and d['prior_tables_preserved']==247
assert m['reclassification_rows']==49 and m['new_image_observations']==0
assert m['source_A_rgba_crops_verified']==49
assert m['observed_before']==m['observed_after']==9898
assert m['checkpoint_remaining']==144
assert m['mapping_verified']==m['tilezed_verified']==m['certified']==0
state['previous_checkpoint_v185']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v186',date='2026-10-28',
 kind='manual_identity_disambiguation_49_existing_observations_no_new_count',
 physical_unified_sqlite_version='v186',prior_visual_checkpoint='v185',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9898,
 expanded_unique_unobserved=144,expanded_observation_percent=9898/10042*100,
 v186_manually_reinspected=49,v186_source_A_RGBA_verified=49,
 v186_existing_records_reclassified=49,v186_newly_observed=0,
 v186_original_B_C_zero_held_preserved=[70],
 v186_sqlite_sha256=d['sqlite_sha256'],
 evidence_repo_path='review/v186_object_disambiguation_49/RECLASSIFIED_49.csv',
 evidence_manifest='review/v186_object_disambiguation_49/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='User-requested category correction: differentiate heat/grill and possible external LPG cylinder from cushioned sofa/armchair and powered machines. Red/orange cylinder is visually suggested LPG but contents/connection not official. Historical index 70 B-C zero remains held. 49 existing candidate reinterpretations do not increase observed count and do not certify official Local ID or TileZed.'
))
state['unified_database'].update(dict(
 version='v186',status='VERIFIED_MANUAL_49_CATEGORY_CORRECTION_OVERLAY_NOT_NEW_IDENTITIES',
 repo_manifest='analysis/current/v186/MANIFEST.json',
 parent_unified_version='v185',sqlite_sha256=d['sqlite_sha256'],table_count=248,
 prior_tables_preserved=247,sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9898,expanded_unobserved_unique=144,
 v186_corrections=49,v186_new_observed=0,certified=0))
state['latest_v186_evidence']={
 'version':'v186','original_A_png_and_crop_hashes_verified':49,
 'existing_keys_manually_reclassified':49,
 'categories':m['category_counts'],
 'held_original_B_C_zero_index70':True,
 'new_observed':0,'observed':9898,'checkpoint_remaining':144,
 'sqlite_parent_tables_preserved':247,'sqlite_current_tables':248,
 'sqlite_sha256':d['sqlite_sha256'],'mapping_verified':0,
 'tilezed_verified':0,'certified':0
}
state['next_actions']=[
 'v186: consult corrected category overlay review/v186_object_disambiguation_49/RECLASSIFIED_49.csv before reusing v122/v140/v141 broad early AI labels for BBQ, upholstered seating or powered machines.',
 'v186: visually inspect fuel cylinder/BBQ coupling against original source A and true B/C; never call propane contents officially verified without independent confirmation.',
 'v186: keep index 70 B-C zero as held; do not mark these 49 old records new or claim mapping/TileZed certification.',
 *state.get('next_actions',[])
]
p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v186 소파·프로판통형 바비큐·공작기계 혼동 정정 49종 (2026-10-28)\n\n'
 '- 사용자 지적에 따라 기존 큰 범주 판정을 신뢰하지 않고 원본 A000/012/013/014, 진짜 TMX B, 같은 raw GID 1개 제거 C/차이 이미지를 직접 다시 확인하여 **49종**의 외형·부품 근거·다른 범주가 아닌 이유를 개별 재기록.\n'
 '- 조리 설비13종(그중 바비큐 그릴 후보7), 좌석/안락의자/소파 모듈21종, 산업 기계·작업대·보관통·실린더15종. BBQ의 독립 연료용기 후보, 쿠션·등받이·팔걸이, 기계의 모터·가공헤드, 작동부 없는 작업대 등을 구별함. \n'
 '- **원본 A PNG 바이트 SHA256 및 크롭 RGBA 픽셀 SHA256 49종 일치**, 기존 B/C 대응·타일 고유키 49종 대조, 접촉시트12장 검증. 인덱스70은 원래 B-C=0이라 held 유지. 모든 재분류는 외형 기준 잠정이고 프로판 연료 자체는 정식 인증되지 않음.\n'
 f"- 물리 SQLite **248테이블**, 부모 v185 기존247테이블 모든 행값·수 그대로 보존, 새 정정 오버레이 49행 1테이블. SHA256 {d['sqlite_sha256']}, integrity_check=ok. 원본 타일셋 PNG/84 TMX/기존5409·사용자 수동80·제외14·D-held2/JUMBO20 보존.\n"
 '- 이번 49종은 **이미 존재하는 기록의 정정**이라 신규 관찰 +0. 누적 관찰 **9898/10042 (98.57%)**, 기록상 미관찰 **144종** 유지. 공식 PNG↔Local ID/TileZed 및 최종 사물 인증 0.\n'
 '- 증거 review/v186_object_disambiguation_49/, 물리 DB analysis/current/v186/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel;txt=f.read_text(encoding='utf-8')
 assert 'v185' in txt
 k=txt.index('\n')
 f.write_text(txt[:k+1]+'\n'+summary+txt[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v186 quality correction, no false new observed 9898/10042,',d['sqlite_sha256'],flush=True)
