#!/usr/bin/env python3
"""v191 handoff of completed original-A-only manual image examination.
The physical v190 SQLite and historically excluded v188 entries stay intact.
No observed/provisional/final-identity promotions until independent TMX B/C audit.
"""
from pathlib import Path
import json,csv,hashlib,collections
R=Path(__file__).resolve().parents[1]
D=R/'review/v191_reopen142_A_first'
data=json.loads((D/'MANUAL_A_IMAGE_OBSERVATIONS_142.json').read_text(encoding='utf-8'))
m=json.loads((D/'MANIFEST.json').read_text(encoding='utf-8'))
rows=data['manual_image_notes']
assert len(rows)==142 and [r['order'] for r in rows]==list(range(142))
assert len({(r['tile_set_name'],r['local_id']) for r in rows})==142
assert data['visually_inspected_original_A']==132 and data['original_A_unavailable']==10
assert sum(x['original_A_sha256_verified'] for x in rows)==132
assert sum(x['visual_reviewer_looked_at_A'] for x in rows)==132
assert sum(x['appearance_observation'] is not None for x in rows)==132
assert sum(x['appearance_observation'] is None for x in rows)==10
assert collections.Counter(x['appearance_confidence'] for x in rows)=={
 'high':60,'medium':49,'low':23,'none':10}
assert all(not r['observed_new'] and not r['provisional_candidate_new'] and
 not r['mapping_verified'] and not r['tilezed_verified'] and not r['certified'] for r in rows)
assert m['input_v188_excluded_keys']==142 and m['original_A_rgba_sha_verified']==132
assert all((D/'sheets'/('A_ORIGINAL_%02d.jpg'%i)).stat().st_size>150000 for i in range(9))
m.update(A_sheets_direct_visual_review_finished=9,manual_A_appearance_descriptions=132,
 original_A_unknown_or_unverified=10,
 A_confidence_count={'high':60,'medium':49,'low':23,'none':10},
 manual_notes_file='review/v191_reopen142_A_first/MANUAL_A_IMAGE_OBSERVATIONS_142.json',
 manual_notes_sha256=hashlib.sha256((D/'MANUAL_A_IMAGE_OBSERVATIONS_142.json').read_bytes()).hexdigest(),
 user_reopened_active_review=True,B_C_followup_still_required=142,
 new_provisional_or_observed_after_A_only=0)
(D/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=R/'PROJECT_STATE.json'
state=json.loads(p.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v190'
assert state['latest_checkpoint']['expanded_unique_observed']==9898
assert state['latest_checkpoint']['expanded_unique_unobserved']==144
assert state['unified_database']['version']=='v190'
assert state['unified_database']['table_count']==252
state['latest_v191_explicit_142_reopen']={
 'reopened_by_user':True,'stage':'A_original_pixel_verified_and_all_visible_individual_images_visually_reviewed',
 'all_targeted_keys':142,'actual_A_image_verified_and_viewed':132,
 'A_image_missing_or_no_exact_crop':10,'A_visual_notes':142,
 'A_confidence_high':60,'A_confidence_medium':49,'A_confidence_low':23,
 'official_mapping_verified':0,'tilezed_verified':0,'identity_final_certified':0,
 'new_image_observed':0,
 'awaiting_BC_contextual_crosscheck_count':142,
 'source_evidence':'review/v191_reopen142_A_first/MANUAL_A_IMAGE_OBSERVATIONS_142.json',
 'source_manifest':'review/v191_reopen142_A_first/MANIFEST.json',
 'note':'v188 exclusion was from active review ONLY. User expressly reopened 142 keys; new source-A appearance descriptions are NOT provisional observed or official certified tile identities. 10 without exact original A remain source-blocked. Physical v190 SQLite and checkpoint 9898/10042 unchanged.'
}
state['next_actions']=[
 'v191 user reopening supersedes earlier active queue exclusion; re-examine 142 original image descriptions and original TMX B/C one GID removal evidence, do not ignore clear direct A appearance when B-C=0.',
 'v191 cross-check 132 original A source-visible shapes with real placement/part family. Upgrade only upon independently supported source key, TMX scene and candidate identity evidence; keep final official mapping 0 until proven.',
 'v191 resolve exact original A source/crop for 9 older original catalog keys plus 1 new missing original source; never substitute a guess.',
 *state.get('next_actions',[])
]
p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=(
 '## v191 — 사용자가 제외 142종 재개: 원본 A 이미지 우선 육안 판독 (2026-10-28)\n\n'
 '- v188에서 활성 검수 제외했던 142종을 사용자의 새 명시 지시로 다시 검수 대상으로 열었음. 이전 v188 제외 기록, 과거 사용자 제외8/keep_provisional1 등 역사적 정보는 불변.\n'
 '- 원본 새 아틀라스 133종, 과거 5409 범위 9종. 실제 원본 PNG 파일 SHA256 및 A 스프라이트 RGBA 픽셀 SHA256로 **132종의 이미지 무결성 확인**, '
 '해당 원본 A와 알파 비투명 범위 확대를 9장 시트로 모두 실제 눈으로 판독하고 **132종 개별 외형 메모** 작성. '
 '명확60/계열 추정49/모호23. 나머지10종(옛9 + 새 원본A 불가1)은 정확한 A 크롭 출처 부재로 별도 보류.\n'
 '- 이번 단계는 **B-C 픽셀 차이 0을 투명/미상으로 확정하지 않음**. A 자체에서 선명한 기계/가구/모자이크벽 등은 그 형태를 기록했으나, '
 '원래 TMX B/C 와 실물 부품 기능 교차 검증 전 신규 provisional_candidate/observed 승격은 0, 공식 PNG Local ID/TileZed/최종 정체 인증도 0.\n'
 '- 누적 원래 체크포인트 **9,898/10,042(98.57%)**, 기록상 미관찰 144종(원본 실제 미관찰142 + 역사적 2건 집계차이), '
 '물리 SQLite v190 **252테이블 전부 변경 없이 보존**. 이번 작업은 원본 이미지 판독 근거만 추가한 별도 v191 증거 버전.\n'
 '- 다음 작업: 132개의 A 외형 메모와 원래 TMX 실제 위치 B/C·동계열 스프라이트 연결을 대조해 확실한 것만 잠정 승격. 정확한 A 없는10종은 출처 별도 조사.\n'
 '- 증거 review/v191_reopen142_A_first/ (A_ORIGINAL_00~08.jpg, REOPEN_142_A_SOURCE_AUDIT.csv, MANUAL_A_IMAGE_OBSERVATIONS_142.json).\n\n---\n'
)
for rel in ['AGENTS.md','docs/HANDOFF.md']:
 f=R/rel
 s=f.read_text(encoding='utf-8')
 assert 'v190' in s
 k=s.index('\n')
 f.write_text(s[:k+1]+'\n'+summary+s[k+1:].lstrip('\n'),encoding='utf-8')
print('PASS v191 142 reopened 132 actual original A inspected, 10 source unavailable, no observed or DB changes',flush=True)
