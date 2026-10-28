#!/usr/bin/env python3
"""Finalize 108 out of 163 manually observed tile parts, only after source evidence and SQLite checks."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'review/v179_alternative163_visual/MANIFEST.json').read_text())
d=json.loads((R/'analysis/current/v179/MANIFEST.json').read_text())
p=json.loads((R/'analysis/current/v178/MANIFEST.json').read_text())
fp=R/'PROJECT_STATE.json';state=json.loads(fp.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v178'
assert state['latest_checkpoint']['expanded_unique_observed']==9684
assert state['latest_checkpoint']['expanded_unique_unobserved']==358
assert state['unified_database']['version']=='v178'
assert state['unified_database']['sqlite_sha256']==p['sqlite_sha256']
assert d['version']=='v179' and d['parent']=='v178'
assert d['parent_sqlite_sha256']==p['sqlite_sha256']
assert d['table_count']==241 and d['prior_tables_preserved']==240
assert d['new_rows']==d['new_observed_rows']==108
assert m['visually_reviewed']==163 and m['positive_alt_B_C']==126
assert m['newly_provisional']==108 and m['held']==55
assert m['held_zero']==37 and m['held_weak_or_missing']==18
assert m['observed_parent']==9684 and m['observed_now']==9792
assert m['remaining_checkpoint']==250 and m['remaining_physical_unique']==248 and m['checkpoint_discrepancy']==2
assert m['official_mapping_verified']==m['tilezed_verified']==m['identity_certified']==0
state['previous_checkpoint_v178']=json.loads(json.dumps(state['latest_checkpoint']))
state['latest_checkpoint'].update(dict(
 version='v179',date='2026-10-28',
 kind='manual_bulk_163_original_A_B_C_108_source_backed_provisional_visual_review',
 physical_unified_sqlite_version='v179',prior_visual_checkpoint='v178',
 expanded_84_tmx_unique_total=10042,
 expanded_unique_observed=9792,expanded_unique_unobserved=250,expanded_observation_percent=9792/10042*100,
 new_image_observed=9792-5400,new_keys_unobserved=4633-(9792-5400),
 v179_alternate_scenes_manually_reviewed=163,v179_B_C_positive=126,v179_new_provisional=108,v179_excluded_unverified=55,
 v179_zero_held=37,v179_weak_held=18,v179_physical_unobserved_distinct=248,v179_historical_count_discrepancy=2,
 v179_reviewed_indices=m['accepted_indices'],v179_sqlite_sha256=d['sqlite_sha256'],
 evidence_repo_path='review/v179_alternative163_visual/VISUAL_REVIEW_108.csv',
 evidence_manifest='review/v179_alternative163_visual/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 caution='Reviewed every one of the 163 alternate A/B/C source-proven scenes by eye. 108 provisional part descriptions with identifiable silhouette and B-C >=200 positive source pixels, 55 held. v178 true raw PNG/TMX GID verification reused with parent DB cryptographic evidence chain; v179 independently checked 652 original PNG/CRC/A RGBA and B-C. Not official TileZed Local ID or final identities. Checkpoint missing 250 vs true physical missing 248, historical discrepancy two unresolved.'
))
state['unified_database'].update(dict(
 version='v179',status='VERIFIED_SOURCE_PROVEN_BULK_MANUAL_VISUAL_REVIEW',
 repo_manifest='analysis/current/v179/MANIFEST.json',parent_unified_version='v178',
 sqlite_sha256=d['sqlite_sha256'],table_count=241,prior_tables_preserved=240,
 sqlite_size_bytes=d['sqlite_bytes'],all_prior_tables_preserved=True,
 expanded_observed_unique=9792,expanded_unobserved_unique=250,
 new_4633_observed=9792-5400,new_4633_unobserved=4633-(9792-5400),
 v179_visual_review_rows=108,certified=0
))
state['latest_v179_evidence']=dict(
 version='v179',original_alternate_5x5_source_scenes_visually_reviewed=163,
 source_pixels_positive=126,new_provisional_image_records=108,
 held_zero_pixel=37,held_weak_or_missing=18,
 observed_total=9792,unobserved_remaining=250,
 physical_distinct_unobserved=248,historical_count_discrepancy=2,
 parent_tables_preserved=240,physical_sqlite_tables=241,
 sqlite_sha256=d['sqlite_sha256'],official_mapping_verified=0,tilezed_verified=0,final_identity_certified=0
)
state['next_actions']=[
 'v179: new A-selected alternate scene pool 211/211 is now source-rendered: 48 v176 plus 163 v178, and all 163 v178 visually reviewed. Further visual identity work needs other original TMX placements or original PNG families for still-held 248 distinct keys.',
 'v179: specifically investigate original 5409 nine remaining selected-original-A mapping absence; do not substitute guessed PNG or silently mark resolved.',
 'v179: reconcile two historical checkpoint accounting difference (250 reported missing vs 248 physically distinct keys).',
 *state.get('next_actions',[])
]
fp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v179 대형 타일 시각검수: 실제 다른 TMX A/B/C 163종 전체 직접 판독 (2026-10-28)\n\n'
 '- v178에서 원본 A 선택 이미지의 실제 다른 TMX B, 그 자리 하나의 GID만 삭제한 C 및 차이 **163종 × 4장 PNG = 652장, 접촉시트 28장**을 모두 눈으로 검토. 외형·실물 부분·설치 장면이 일치하고 B−C 변화가 충분한 **108종**을 provisional_candidate로 개별 기록, 37종 변화0/18종 지나치게 작은 변화·이웃 스프라이트 미확보·모호성으로 **55종 보류**.\n'
 '- 장작/건초 보관대·모래무더기·산업 덕트/환풍 그릴·건설 철골/바닥 합판·안전난간·실내 문틀·박공벽·욕실 타일·매장 진열장/흔들의자·지구본 등 외형만 근거가 있는 범주로 잠정 기록. 정식 재질·방향/연결·사물 공식 명칭은 미인증.\n'
 f"- 물리 SQLite **241테이블**, v178 부모의 모든 240개 기존 테이블/전체 행 내용 및 행 수 그대로 보존. 신규108행 1테이블, SHA256 {d['sqlite_sha256']}, PRAGMA integrity_check=ok. v178 원본 PNG/TMX raw GID·좌표·층·레이어 검증은 변경 불가능한 부모 증거로 재사용하고 v179 원본 B/C/차이 PNG ZIP CRC 및 픽셀 차이, 타일 ID/원본 SHA/부모 물리 DB 행 동등성을 재확인.\n"
 '- 이미지 잠정 관찰 **9,792/10,042 (97.51%)**, 기록상 미관찰 **250**, 물리 실제 고유키 미관찰 **248** 및 과거 집계 차이 **2건**. 정체 최종 인증과 공식 TileZed/Local ID 매핑 **0**.\n'
 '- 원본 84 TMX·Tiles PNG, 기존5409·수동80·제외14·held D2/JUMBO20 및 이전 모든 SQLite/증거 보존. 사용자 정의 D(같은 키 다른 공식 A를 원래 B 같은 층·레이어·좌표로 대입) 실험 아님.\n'
 '- 근거 review/v179_alternative163_visual/, 원본 652 이미지 ZIP 및 28시트 review/v178_alt_scene_bulk172/, DB analysis/current/v179/MANIFEST.json.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel;s=p.read_text(encoding='utf-8')
 assert 'v178' in s
 k=s.index('\n')
 p.write_text(s[:k+1]+'\n'+summary+s[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v179 108 more manual source-backed candidate parts, 9792/10042 and 241 tables',d['sqlite_sha256'],flush=True)
