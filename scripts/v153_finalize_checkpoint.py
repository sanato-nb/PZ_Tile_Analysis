#!/usr/bin/env python3
"""v153 final checkpoint: only after image, ZIP, SQLite checks have passed."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
r=json.loads((R/'review/v153_roads_farm_2960_3119/MANIFEST.json').read_text())
m=json.loads((R/'analysis/current/v153/MANIFEST.json').read_text())
sp=R/'PROJECT_STATE.json'
s=json.loads(sp.read_text(encoding='utf-8'))
assert s['latest_checkpoint']['version']=='v152'
assert s['latest_checkpoint']['expanded_unique_observed']==8132
assert r['promoted_provisional']+r['excluded_unverified']==160
assert m['new_rows']==r['promoted_provisional']
assert m['parent']=='v152' and m['table_count']==215
assert m['prior_tables_preserved']==214
assert r['mapping_verified']==r['tilezed_verified']==r['certified']==0
n=r['promoted_provisional']
obs=8132+n
remaining=10042-obs
s['previous_checkpoint_v149']=json.loads(json.dumps(s['latest_checkpoint']))
s['latest_checkpoint'].update(dict(
 version='v153',date='2026-10-27',kind='direct_manual_original_A_B_C_160_visual_review',
 physical_unified_sqlite_version='v153',prior_visual_checkpoint='v152',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v153_roads_farm_2960_3119/VISUAL_REVIEW.csv',
 evidence_manifest='review/v153_roads_farm_2960_3119/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v153_new_provisional=n,v153_excluded_unverified=r['excluded_unverified'],
 v153_index_range=[2480,2639],v153_sqlite_sha256=m['sqlite_sha256'],
 caution='160 source A/B/C sprites manually examined, only verified keys provisional. No authoritative TileZed Local-ID mapping or certified identity. B-C zero, truncated scenes or neighbor holes are not transparency. Held entries are immutable.'))
s['unified_database'].update(dict(
 version='v153',status='VERIFIED',repo_manifest='analysis/current/v153/MANIFEST.json',
 parent_unified_version='v152',sqlite_sha256=m['sqlite_sha256'],
 table_count=212,prior_tables_preserved=214,sqlite_size_bytes=m['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,expanded_unobserved_unique=remaining,
 new_4633_observed=obs-5400,new_4633_unobserved=4633-(obs-5400),
 v153_visual_review_rows=n,certified=0))
s['latest_v153_evidence']=dict(version='v153',source_indices=[2960,3119],
 manual_images_seen=160,source_verified_provisional=n,
 excluded_unverified=r['excluded_unverified'],excluded_indices=r['excluded_indices'],
 sqlite_sha256=m['sqlite_sha256'],prior_tables_and_rows_preserved=211,
 mapping_verified=0,tilezed_verified=0,certified=0,
 observed_total=obs,unobserved_remaining=remaining)
s['next_actions']=[
 'v153: '+str(remaining)+' unique TMX keys still lack individually observed A/B/C images; never treat rendered ABCD as certified identity.',
 'B-C zero/map-edge/incomplete neighbor are not transparent; official TileZed and A-to-local-ID mapping remain unverified.',
 *s.get('next_actions',[])
]
sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
section=(
 '## v153 녹색·검정·갈색·적갈색 지붕판 A/B/C 이미지 직접 검수 (2026-10-27)\n\n'
 '- 기존 A/B/C 접촉시트 037/038 총 160종을 개별 시각 판독. PNG RGBA·원래 TMX GID/층/레이어/좌표, C 제거 및 B−C SHA 검증 통과 **'
 +str(n)+'종**만 provisional_candidate 신규 관찰, **'+str(r['excluded_unverified'])
 +'종**은 B-C=0·이웃 누락·지도끝 등으로 완료에서 제외, 투명 인증하지 않음.\n'
 '- 전체 84 TMX 10,042종에서 **'+str(obs)+'종 관찰 기록 ('
 +format(obs/10042*100,'.2f')+'%)**, 미관찰 **'+str(remaining)+'종**. '
 '공식 Local ID/TileZed/사물 정체 인증 모두 0. D 인접격자/과거 두 번째 위치는 공식 매핑 아님.\n'
 '- 물리 SQLite analysis/current/v153/MANIFEST.json, SHA '+m['sqlite_sha256']
 +', **215개 테이블**(부모 v149 211테이블·이전 모든 행 수 보존 + 신규 '+str(n)
 +'행 1테이블). PRAGMA integrity_check=ok. review/v153_roads_farm_2960_3119에 증거 CSV·ZIP·시각 검수판·예외표 보존.\n'
 '- 기존 사용자 수동80·제외14·기존 5409·held D2/JUMBO20, 원본 PNG/TMX 및 과거 DB 불변. '
 'ABCD 그림의 생성 완료와 최종 정체 확인은 다름.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 assert 'v152' in t
 sep=t.index('\n')
 p.write_text(t[:sep+1]+'\n'+section+t[sep+1:].lstrip('\n'),encoding='utf-8')
print('PASS v153 checkpoint',obs,'observed',remaining,'remaining',m['sqlite_sha256'],flush=True)
