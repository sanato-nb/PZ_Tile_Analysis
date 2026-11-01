# 로즈우드 가구 357종 Blockbench 기반 재매칭 v3

실제 Blockbench 5.2.2에서 기존 고유 Decocraft 모델 50개를 로딩해 110개 PZ 스타일 이미지에 붙임.

그중 50개 대표 완성 가구를 이미지로 대조해 28개 부적합, 12개 조건부, 5개 색상 불확실, 5개 형태 대체 필요로 판정.

나머지 307개 스타일은 육안 확정이 아니며 실제 마크 게임의 설치 크기/충돌/상호작용은 미검증.

## 신규 대체 후보 8개 (각각 원본 .bbmodel과 variant source 해시 존재)

초기 모드 매치 결과를 덮어쓰지 않고 추천 변경 후보로만 별도 기록.

- Counter / White: decocraft:bathroom_counter_left_white → decocraft:bottom_cabinet_1_white — 흰색 하부 수납장으로 기존 세면대 카운터보다 닫힌 외형에 가까움; 상판 나무색 차이

- Bed / Fancy: decocraft:bunk_bed_birch_black → decocraft:single_bed_birch_black — 단층 침대 형태로 이전 2층 침대보다 적합; PZ 검정 프레임과 MC 밝은 목재 프레임 차이

- Counter / White Corner: decocraft:diner_counter_corner_cyan → decocraft:bottom_cabinet_corner_outer_1_white — 흰색 모서리 하부장으로 기존 청록 식당 카운터보다 색상/종류가 적합; 방향 및 코너 완성배치 확인 필요

- Oven / Green: decocraft:pizza_oven → decocraft:stove — 가정용 가스레인지/오븐으로 기존 벽돌 피자 화덕보다 구조가 적합; 원본 초록색 대비 후보 회색

- Hamster Wheel / Human: decocraft:casino_wheel → decocraft:treadmill — 원본은 사람용 러닝머신이므로 기존 카지노 룰렛 후보보다 훨씬 정확한 종류

- Bed / Blue: decocraft:bunk_bed_birch_blue → decocraft:single_bed_birch_blue — 단층 파란 침대 형태로 이전 2층 침대보다 적합; 침대 머리/발판 및 색감 다름

- Stand / Pool Cue: decocraft:coat_stand_birch → decocraft:pool_rack — 당구 큐대 보관대이므로 기존 옷걸이보다 기능과 형태가 적합; 선반 및 크기 차이

- Bed / Oak: decocraft:bunk_bed_oak_black → decocraft:crib_oak — 참나무 아기침대로 기존 2층 침대보다 분명히 적합; 마크 모델 상단 장난감 모빌 차이

## 파일

- INDEX.html: 왼쪽 PZ 원본 / 오른쪽 실제 Blockbench (또는 미확인 구분) 가구 검색

- REVISED_357_PZ_MC_MATCHES.csv: 전체 357종 개선 추천 및 형상 검수 상태

- EIGHT_BLOCKBENCH_VERIFIED_IMPROVED_CANDIDATES.csv: 새 8개 검수 비교와 모델 원본 해시

- cards 및 better 폴더: 각각 기존 349개 비교와 새 Blockbench 대체 비교 8개

- ZIP을 풀고 INDEX.html 열기. Blockbench 렌더는 마인크래프트 게임 스크린샷이 아니야.

원본 좀보이드 TMX/PNG/SQLite와 기존 357개 매칭 파일은 변경하지 않음.
