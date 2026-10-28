#!/usr/bin/env python3
"""Materialize source-evidence checkpoint without marking unresolved tiles observed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
out=R/'review/v175_remaining381_evidence_audit'
m=json.loads((out/'MANIFEST.json').read_text(encoding='utf-8'))
d=json.loads((R/'analysis/current/v175/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v174/MANIFEST.json').read_text())
q=R/'PROJECT_STATE.json';state=json.loads(q.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v174'
assert state['latest_checkpoint']['expanded_unique_observed']==9661
assert state['latest_checkpoint']['expanded_unique_unobserved']==381
assert state['unified_database']['version']=='v174'
assert d['version']=='v175' and d['parent']=='v174'
assert d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==237 and d['prior_tables_preserved']==236
assert d['new_rows']==379 and d['new_observed_rows']==0
assert m['total_remaining_in_checkpoint']==381 and m['source_keys_audited']==379 and m['new_source_missing']==370 and m['old_source_missing']==9 and m['bookkeeping_discrepancy']==2
assert m['observed_after']==9661 and m['remaining_after']==381
assert m['identity_certifications']==m['official_mapping_verified']==m['tilezed_verified']==0
state['previous_checkpoint_v174']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v175',date='2026-10-28',kind='forensic_source_audit_of_all_381_remaining_without_visual_promotion',
 physical_unified_sqlite_version='v175',prior_visual_checkpoint='v174',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=9661,expanded_unique_unobserved=381,
 expanded_observation_percent=9661/10042*100,new_image_observed=4261,new_keys_unobserved=372,
 v175_source_audited_keys=379,v175_bookkeeping_discrepancy=2,v175_new_observed=0,v175_old_missing=9,v175_new_missing=370,
 v175_real_tmx_uses=m['real_tmx_occurrences_total'],
 v175_alternate_scene_candidates=m['alternate_inbounds_candidates'],
 evidence_repo_path='review/v175_remaining381_evidence_audit/REMAINING_381_EVIDENCE_AUDIT.csv',
 evidence_manifest='review/v175_remaining381_evidence_audit/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,v175_sqlite_sha256=d['sqlite_sha256'],
 caution='379 distinct source keys audited, with 2 historical provisional-candidate keys discrepant from the checkpoint count; unresolved accounting, not fabricated source keys. This audit adds ZERO visually observed/identity-certified keys. B-C=0, map-edge, neighbor missing, or original atlas failures cannot be called transparent, observed or certified. Follow-up visual rendering in alternate scene required.'
))
state['unified_database'].update(dict(version='v175',status='VERIFIED_SOURCE_AUDIT_NOT_IDENTITY',
 repo_manifest='analysis/current/v175/MANIFEST.json',parent_unified_version='v174',
 sqlite_sha256=d['sqlite_sha256'],table_count=237,prior_tables_preserved=236,
 sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9661,expanded_unobserved_unique=381,
 new_4633_observed=4261,new_4633_unobserved=372,v175_forensic_audit_rows=379,certified=0
))
state['latest_v175_evidence']={
 'version':'v175','remaining_unique_keys_audited':379,'unreconciled_checkpoint_gap':2,'original_84_tmx_occurrences':m['real_tmx_occurrences_total'],
 'inbounds_alternate_scene_candidate_keys':m['alternate_inbounds_candidates'],
 'original_png_pixel_verified':m['original_png_pixel_verified'],
 'original_primary_tmx_verified':m['original_B_TMX_placement_verified'],
 'original_missing_5409':9,'new_missing_4633_source_keys':370,'newly_observed':0,
 'reason_distribution':m['reason_distribution'],'observed_total':9661,'unobserved_remaining':381,
 'db_sha256':d['sqlite_sha256'],'sqlite_tables':237,
 'mapping_verified':0,'tilezed_verified':0,'certified':0
}
state['next_actions']=[
 'v175: render alternate-source A/B/C for 379 source-confirmed pending tile keys; reconcile two historical checkpoint discrepancy cases before final coverage claim.',
 'v175: review older 9 catalog keys separately; require actual source PNG and TMX placement evidence. Do not invent source or count them as observed.',
 'v175: source ledger has 379 distinct unresolved tile keys (370 new, 9 old), but v174 checkpoint says 381. Reconcile 2 historical undercounted provisional source records before claiming full coverage.',
 *state.get('next_actions',[])
]
q.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v175 전체 미관찰 381종 원본 TMX/PNG 근거 전수 조사 (2026-10-28)\n\n'
 '- 부모 v174 관찰률 **9,661/10,042종(96.21%)** 유지. **상태 파일의 미관찰 381종**과 달리 **원본 SQLite에서 중복 제거한 미관찰 실제 키 379종(새 370, 기존 9)**을 전수 집계하고, 차이 2는 역사적 집계 불일치로 별도 명시하고 CSV·시각검토용 A 이미지 시트와 증거 요약 생성.\n'
 f"- 84개 TMX에서 실제 raw GID/firstgid 배치 {m['real_tmx_occurrences_total']}건 확인, 유효 5×5 내 다른 위치가 있는 후보 {m['alternate_inbounds_candidates']}종 탐색. 실제 대체 위치 원본 PNG/TMX 그림 재조립과 육안 확인은 후속 작업; 발견만으로 관찰이나 사물 정체 인증 금지.\n"
 f"- 새 물리 SQLite **237테이블**: v174 부모의 기존 236개 테이블/전체 행 내용 및 수 보존, 새 forensic audit 379행 1테이블. SHA256 {d['sqlite_sha256']}; PRAGMA integrity_check=ok.\n"
 '- 신뢰할 수 있는 증거가 없는 B−C 0·TMX 지도 끝·주변 레이어 누락·너무 작은 부품은 무조건 관찰 미완료/투명 미인증. 이번 버전 실제 신규 관찰 0, 공식 Local ID/TileZed/최종 정체 인증 0.\n'
 '- 기존 5409·사용자 수동80/제외14/D held2/JUMBO20 및 84개 원본 TMX·Tiles PNG·과거 SQLite 보존. 사용자 정의 D는 같은 키 다른 공식 A를 정확히 원본 B 같은 위치·층·레이어에 대입해야 함.\n'
 '- 증거 review/v175_remaining381_evidence_audit/ 및 analysis/current/v175/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 file=R/rel;s=file.read_text(encoding='utf-8')
 assert 'v174' in s
 k=s.index('\n')
 file.write_text(s[:k+1]+'\n'+summary+s[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v175 379 actual pending source keys and 2 unresolved checkpoint-count differences, unchanged observed 9661/10042,',d['sqlite_sha256'])
