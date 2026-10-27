#!/usr/bin/env python3
"""v146 final checkpoint: only after image, ZIP, SQLite checks have passed."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
r=json.loads((R/'review/v146_abc_1680_1839/MANIFEST.json').read_text())
m=json.loads((R/'analysis/current/v146/MANIFEST.json').read_text())
sp=R/'PROJECT_STATE.json'
s=json.loads(sp.read_text(encoding='utf-8'))
assert s['latest_checkpoint']['version']=='v145'
assert s['latest_checkpoint']['expanded_unique_observed']==7054
assert r['promoted_provisional']+r['excluded_unverified']==160
assert m['new_rows']==r['promoted_provisional']
assert m['parent']=='v145' and m['table_count']==208
assert m['prior_tables_preserved']==207
assert r['mapping_verified']==r['tilezed_verified']==r['certified']==0
n=r['promoted_provisional']
obs=7054+n
remaining=10042-obs
s['previous_checkpoint_v145']=json.loads(json.dumps(s['latest_checkpoint']))
s['latest_checkpoint'].update(dict(
 version='v146',date='2026-10-27',kind='direct_manual_original_A_B_C_160_visual_review',
 physical_unified_sqlite_version='v146',prior_visual_checkpoint='v145',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v146_abc_1680_1839/VISUAL_REVIEW.csv',
 evidence_manifest='review/v146_abc_1680_1839/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v146_new_provisional=n,v146_excluded_unverified=r['excluded_unverified'],
 v146_index_range=[1840,1999],v146_sqlite_sha256=m['sqlite_sha256'],
 caution='160 source A/B/C sprites manually examined, only verified keys provisional. No authoritative TileZed Local-ID mapping or certified identity. B-C zero, truncated scenes or neighbor holes are not transparency. Held entries are immutable.'))
s['unified_database'].update(dict(
 version='v146',status='VERIFIED',repo_manifest='analysis/current/v146/MANIFEST.json',
 parent_unified_version='v145',sqlite_sha256=m['sqlite_sha256'],
 table_count=208,prior_tables_preserved=207,sqlite_size_bytes=m['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,expanded_unobserved_unique=remaining,
 new_4633_observed=obs-5400,new_4633_unobserved=4633-(obs-5400),
 v146_visual_review_rows=n,certified=0))
s['latest_v146_evidence']=dict(version='v146',source_indices=[1840,1999],
 manual_images_seen=160,source_verified_provisional=n,
 excluded_unverified=r['excluded_unverified'],excluded_indices=r['excluded_indices'],
 sqlite_sha256=m['sqlite_sha256'],prior_tables_and_rows_preserved=207,
 mapping_verified=0,tilezed_verified=0,certified=0,
 observed_total=obs,unobserved_remaining=remaining)
s['next_actions']=[
 'v146: '+str(remaining)+' unique TMX keys still lack individually observed A/B/C images; never treat rendered ABCD as certified identity.',
 'B-C zero/map-edge/incomplete neighbor are not transparent; official TileZed and A-to-local-ID mapping remain unverified.',
 *s.get('next_actions',[])
]
sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
section=(
 '## v146 식당·주유소·소매 상점 A/B/C 실제 이미지 관찰 (2026-10-27)\n\n'
 '- 원본 A/B/C 접촉시트 1840~1999 총 160개 직접 검토; PNG 픽셀·원래 TMX GID/좌표/층/레이어, C 제거 및 B-C SHA 검증 통과 **'
 +str(n)+'종**만 provisional_candidate, **'+str(r['excluded_unverified'])
 +'종**은 B-C=0·이웃 누락·지도 경계 등으로 신규 완료 계산 제외.\n'
 '- 전체 84 TMX 고유 10,042종에서 **'+str(obs)+'종 관찰 기록 ('
 +format(obs/10042*100,'.2f')+'%)**, 미관찰 **'+str(remaining)+'종**. '
 '공식 Local ID↔PNG/TileZed·정체 최종 인증 각 0. 준비된 ABCD 증거는 정체 완료가 아님.\n'
 '- 물리 SQLite analysis/current/v146/MANIFEST.json, SHA '+m['sqlite_sha256']
 +', **208개 테이블**(v145 이전 207테이블과 전체 기존 행 수 보존, 신규 '+str(n)
 +'행 1테이블). PRAGMA integrity_check=ok. 증거 review/v146_abc_1680_1839 에 CSV·PNG ZIP·접촉시트·예외표 저장.\n'
 '- 기존 수동80·사용자 제외14·기존5409, 사용자 held D2/JUMBO20, 원본 PNG/TMX 및 과거 DB 불변. '
 'D 다른 A 동일 TMX 위치/층/레이어 공식 매핑 미검증, 인접격자 및 두 번째 TMX 위치는 인증 근거 아님.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 assert 'v145' in t
 sep=t.index('\n')
 p.write_text(t[:sep+1]+'\n'+section+t[sep+1:].lstrip('\n'),encoding='utf-8')
print('PASS v146 checkpoint',obs,'observed',remaining,'remaining',m['sqlite_sha256'],flush=True)
