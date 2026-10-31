#!/usr/bin/env python3
"""v149 final checkpoint: only after image, ZIP, SQLite checks have passed."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
r=json.loads((R/'review/v149_abc_2320_2479/MANIFEST.json').read_text())
m=json.loads((R/'analysis/current/v149/MANIFEST.json').read_text())
sp=R/'PROJECT_STATE.json'
s=json.loads(sp.read_text(encoding='utf-8'))
assert s['latest_checkpoint']['version']=='v148'
assert s['latest_checkpoint']['expanded_unique_observed']==7507
assert r['promoted_provisional']+r['excluded_unverified']==160
assert m['new_rows']==r['promoted_provisional']
assert m['parent']=='v148' and m['table_count']==211
assert m['prior_tables_preserved']==210
assert r['mapping_verified']==r['tilezed_verified']==r['certified']==0
n=r['promoted_provisional']
obs=7507+n
remaining=10042-obs
s['previous_checkpoint_v148']=json.loads(json.dumps(s['latest_checkpoint']))
s['latest_checkpoint'].update(dict(
 version='v149',date='2026-10-27',kind='direct_manual_original_A_B_C_160_visual_review',
 physical_unified_sqlite_version='v149',prior_visual_checkpoint='v148',
 expanded_84_tmx_unique_total=10042,expanded_unique_observed=obs,
 expanded_unique_unobserved=remaining,expanded_observation_percent=obs/10042*100,
 new_image_observed=obs-5400,new_keys_unobserved=4633-(obs-5400),
 evidence_repo_path='review/v149_abc_2320_2479/VISUAL_REVIEW.csv',
 evidence_manifest='review/v149_abc_2320_2479/MANIFEST.json',
 mapping_verified=0,tilezed_verified=0,approved_final_certifications=0,
 v149_new_provisional=n,v149_excluded_unverified=r['excluded_unverified'],
 v149_index_range=[2320,2479],v149_sqlite_sha256=m['sqlite_sha256'],
 caution='160 source A/B/C sprites manually examined, only verified keys provisional. No authoritative TileZed Local-ID mapping or certified identity. B-C zero, truncated scenes or neighbor holes are not transparency. Held entries are immutable.'))
s['unified_database'].update(dict(
 version='v149',status='VERIFIED',repo_manifest='analysis/current/v149/MANIFEST.json',
 parent_unified_version='v148',sqlite_sha256=m['sqlite_sha256'],
 table_count=211,prior_tables_preserved=210,sqlite_size_bytes=m['sqlite_bytes'],
 all_prior_tables_preserved=True,expanded_observed_unique=obs,expanded_unobserved_unique=remaining,
 new_4633_observed=obs-5400,new_4633_unobserved=4633-(obs-5400),
 v149_visual_review_rows=n,certified=0))
s['latest_v149_evidence']=dict(version='v149',source_indices=[2320,2479],
 manual_images_seen=160,source_verified_provisional=n,
 excluded_unverified=r['excluded_unverified'],excluded_indices=r['excluded_indices'],
 sqlite_sha256=m['sqlite_sha256'],prior_tables_and_rows_preserved=210,
 mapping_verified=0,tilezed_verified=0,certified=0,
 observed_total=obs,unobserved_remaining=remaining)
s['next_actions']=[
 'v149: '+str(remaining)+' unique TMX keys still lack individually observed A/B/C images; never treat rendered ABCD as certified identity.',
 'B-C zero/map-edge/incomplete neighbor are not transparent; official TileZed and A-to-local-ID mapping remain unverified.',
 *s.get('next_actions',[])
]
sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
section=(
 '## v149 검정·갈색·녹색 지붕 기와 및 골판 A/B/C 실제 시각 검수 (2026-10-27)\n\n'
 '- 기존 A/B/C 접촉시트 029/030 총 160종을 직접 관찰. 원본 PNG·A RGBA·TMX raw GID/층/레이어/좌표와 C 제거 및 B-C SHA를 검증 통과한 **'
 +str(n)+'종**만 provisional_candidate. **'+str(r['excluded_unverified'])
 +'종**은 B−C 무변화·이웃 누락·지도끝 등으로 관찰 완료에서 제외하고 투명 인증하지 않음.\n'
 '- 전체 84 TMX 10,042종 중 **'+str(obs)+'종 관찰 기록 ('
 +format(obs/10042*100,'.2f')+'%)**, 미관찰 **'+str(remaining)+'종**. '
 '공식 Local ID↔PNG/TileZed·사물 최종 인증 각 0. 준비된 ABCD 이미지 생성과 정체 인증은 별개.\n'
 '- 물리 SQLite analysis/current/v149/MANIFEST.json, SHA '+m['sqlite_sha256']
 +', **211개 테이블** (v148 기존 210개 테이블과 전 행 수 보존, 신규 '+str(n)
 +'행 1테이블). PRAGMA integrity_check=ok. review/v149_abc_2320_2479의 CSV·증거 ZIP·개별 이미지·예외표 보존.\n'
 '- 기존 5,409·사용자 수동80·제외14·보류 D2/JUMBO20, 원본 PNG/TMX와 과거 DB 무변경. '
 '사용자 D 정의는 같은 키 다른 A를 원래 B 위치/층/레이어에 대입하는 것; 인접 격자/두 번째 TMX 위치는 미인증.\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 assert 'v148' in t
 sep=t.index('\n')
 p.write_text(t[:sep+1]+'\n'+section+t[sep+1:].lstrip('\n'),encoding='utf-8')
print('PASS v149 checkpoint',obs,'observed',remaining,'remaining',m['sqlite_sha256'],flush=True)
