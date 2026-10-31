#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v185_crop3102_source/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v185/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v184/MANIFEST.json').read_text())
q=R/'PROJECT_STATE.json';st=json.loads(q.read_text(encoding='utf-8'))
assert st['latest_checkpoint']['version']=='v184'
assert st['latest_checkpoint']['expanded_unique_observed']==9897
assert st['latest_checkpoint']['expanded_unique_unobserved']==145
assert st['unified_database']['version']=='v184' and st['unified_database']['sqlite_sha256']==p['sqlite_sha256']
assert m['promoted_provisional']==1 and m['index']==3102 and m['actual_B_C_pixels']==7650
assert m['actual_missing_neighbor_sources']==0
assert m['observed_parent']==9897 and m['observed_now']==9898 and m['remaining_checkpoint']==144
assert d['version']=='v185' and d['parent']=='v184' and d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==247 and d['prior_tables_preserved']==246 and d['new_rows']==1 and d['new_observed_rows']==1
assert m['final_identity_certified']==m['official_mapping_verified']==m['tilezed_verified']==0
st['previous_checkpoint_v184']=json.loads(json.dumps(st['latest_checkpoint']))
st['latest_checkpoint'].update(dict(
 version='v185',date='2026-10-28',kind='original_TMXS_third_occurrence_recovered_missing_neighbor_source_for_crop3102',
 physical_unified_sqlite_version='v185',prior_visual_checkpoint='v184',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9898,
 expanded_unique_unobserved=144,expanded_observation_percent=9898/10042*100,
 original_5409_observed_preserved=5400,original_5409_unobserved_preserved=9,
 new_image_observed=4498,new_keys_unobserved=135,
 v185_source_verified_crop3102=1,v185_original_A_RGBA_hash_verified=1,
 v185_real_TMX_raw_gid_verified=23718,v185_new_actual_B_C_pixels=7650,
 v185_neighbors_missing=0,v185_new_provisional=1,v185_new_certified=0,
 v185_physical_distinct_missing=142,v185_accounting_discrepancy_unresolved=2,
 v185_sqlite_sha256=d['sqlite_sha256'],
 evidence_repo_path='review/v185_crop3102_source/VISUAL_REVIEW_1.csv',
 evidence_manifest='review/v185_crop3102_source/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='One true source crop part only. The first scene had 1 missing sprite, but third genuine TMX same-key occurrence had 0 missing and B-C changed 7650. Crop species, official tile identity and direction not certified. Checkpoint 144 vs 142 distinct physical missing and history discrepancy 2 remains.'
))
st['unified_database'].update(dict(
 version='v185',status='VERIFIED_ALTERNATIVE_ORIGINAL_GID_A_B_C_PROVISIONAL',
 repo_manifest='analysis/current/v185/MANIFEST.json',parent_unified_version='v184',
 sqlite_sha256=d['sqlite_sha256'],table_count=247,prior_tables_preserved=246,
 sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9898,expanded_unobserved_unique=144,
 new_4633_observed=4498,new_4633_unobserved=135,
 v185_visual_review_rows=1,certified=0
))
st['latest_v185_evidence']=dict(
 version='v185',index=3102,tile_set_name='vegetation_farming_01b',local_id=21,
 actual_TMX='35_48.tmx',location={'layer_index':2,'level':0,'x':93,'y':141,'raw_gid':23718},
 new_nonzero_B_C_pixels=7650,missing_neighbor_sources=0,new_provisional=1,
 observed_total=9898,remaining_checkpoint=144,physical_missing_distinct=142,
 db_tables=247,db_sha256=d['sqlite_sha256'],official_mapping_verified=0,certified=0
)
st['next_actions']=[
 'v185: For 135 remaining newer keys, seek same-key other true TMX placements with complete neighbor sprites; keep missing original source and B-C=0 unobserved.',
 'v185: The first 3102 site lacked neighboring PNG; the alternate 35_48.tmx source x93 y141 has full neighbor sprites. Reproduce this process for other held positive candidates; do not promote when sources remain missing.',
 'v185: Reconcile checkpoint 144 missing versus 142 actual distinct unobserved; historical two-key accounting discrepancy not resolved.',
 *st.get('next_actions',[])
]
q.write_text(json.dumps(st,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v185 실제 다른 TMX 위치로 주변 소스 누락 해소, 밭작물 3102 1종 검수 (2026-10-28)\n\n'
 '- 원래 B-C 7356픽셀이었지만 주변 이미지 1개 누락으로 보류했던 vegetation_farming_01b/21(인덱스3102)을 원본 35_48.tmx의 다른 세번째 동일 raw GID 배치(레이어2, 층0, x93/y141, gid23718)에서 재조립. 새 위치 주변 PNG 누락0, 원본 GID 한 개 제거 B-C 7650픽셀. 실제 A 원본 RGBA/PNG SHA와 TMX SHA 검증.\n'
 '- 가느다란 줄기와 작은 녹색 잎이 흙이랑을 따라 묶인 농작물 일부라는 잠정 외형·부품 역할 기록 1종. 정확한 작물 종·모델·방향·공식 TileZed LocalID/원본 PNG 대응 및 최종 정체 인증은 0.\n'
 '- 이미지 잠정 관찰 **9,898/10,042 (98.57%)**, 기록상 미관찰 **144종**, 실물 고유 미관찰 142종 + 과거 집계차이2 유지.\n'
 f"- 물리 SQLite **247개 테이블**: v184 246테이블 모든 과거 행 내용·수 보존, 신규1행 1테이블, SHA256 {d['sqlite_sha256']}, integrity_check=ok.\n"
 '- 원본84 TMX/Tiles PNG·기존5409·수동80/제외14/held D2/JUMBO20와 모든 역사적 근거 불변. 사용자 정의 D의 다른 공식 A 대체 실험은 수행하지 않음.\n'
 '- 증거 review/v185_crop3102_source/, 물리 DB analysis/current/v185/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel
 src=f.read_text(encoding='utf-8')
 assert 'v184' in src
 n=src.index('\n')
 f.write_text(src[:n+1]+'\n'+summary+src[n+1:].lstrip('\n'),encoding='utf-8')
print('PASS v185 9898/10042 source verified, 247 tables',d['sqlite_sha256'],flush=True)
