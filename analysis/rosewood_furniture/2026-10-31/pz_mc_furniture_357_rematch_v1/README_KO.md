# 로즈우드 357종 마인크래프트 가구 Blockbench 근거 기반 재대조

## 실제 새로 수행한 작업
이번에는 원본 마크 Decocraft 모드의 bbmodel 및 색상 텍스처를 실제 Blockbench 데스크톱에서 열어 스크린샷으로 비교했어.
오른쪽 Blockbench 이미지가 있는 건 확정된 가구가 아니라 실재하는 형상을 볼 수 있는 후보라는 뜻이야.
나머지 모드의 이미지는 기존 근사 모델로 **확실히 구분**했고, 검증됐다고 표시하지 않았어.

## 검증 상태
- total_pz_styles: 357
- native_unique_decocraft_models: 50
- native_blockbench_style_cards: 110
- previous_approximation_only_cards: 221
- no_visual_mc_model_cards: 26
- four_manually_reassessed: 4
- other_styles_not_manually_approved: 353
- visually_rejected: 1
- visually_conditional: 2
- visually_needs_better: 1
- original_mc_candidates_replaced_automatically: 0
- exact_pz_to_mc_3d_matches_certified: 0
- mc_in_game_screenshots: 0
- all_candidate_rows: 881

## 직접 육안 비교한 대표 4건
- Chair/Grey: NEEDS_BETTER_SHAPE — 회색 학교의자는 색상이 맞지만 PZ 의자 쿠션과 등받이 구조가 달라 동일 외형 대체품으로 확정 불가
- Television/Antique: REJECT_CURRENT_MATCH — 좀보이드는 나무 케이스·안테나·다리가 달린 TV인데 Decocraft는 검은 CRT형 TV여서 외형 불일치
- Bed/Large Oak: CONDITIONAL_MATCH — 둘 다 목제 침대지만 헤드보드/발판/침구와 크기가 달라 설치 모습 재검증 필요
- Grand Piano/Black: CONDITIONAL_MATCH — 검은 그랜드 피아노로 형태가 유사하지만 좀보이드는 상판 닫힘, Decocraft는 상판 열림

## 대체 후보 주의
후보 재정렬 점수는 이름·기능·색상 일치 단서일 뿐 외형 비교 점수가 아니야. 기존 모델을 자동 교체하지 않았어.
정확한 충돌박스, 멀티블록 배치 및 게임 내 기능은 실행 검증 전이야.

## 열기
ZIP 압축 해제 후 INDEX.html을 열어 357개 가구를 검색하고, 원본 속성·크기를 확인해.
