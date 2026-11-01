# 잘못된 로즈우드 가구 매칭 감사 및 의자 2종 수정

## 실제 수행
- 12개의 Decocraft 실물 .bbmodel+원본 텍스처를 실제 Blockbench 5.2.2에서 열고 완성 모델의 원본 PZ 모습과 비교. 12/12 렌더 성공.
- Green Dinner: 기존 pfm:green_arm_chair는 안락의자라 부적합. 조건부 1순위 decocraft:chair_1_spruce, 녹색 시트 대안 decocraft:diner_chair_green. 목재와 방석을 동시에 일치시키는 후보는 아직 미확정.
- Wooden: 기존 pfm:oak_chair_classic_black은 실제로 일부 모델 부품만 불러온 오류. 조건부 decocraft:chair_1_spruce. 나무 의자로 조립되지만 등받이가 완전히 같지는 않음.

## 357종 전체 위험 게이트
- 기존 매칭은 실재 모델을 이미지로 만들었다고 해서 외형이 맞는 것은 아님. 이번 파일은 모든 레코드의 이전 증거, 미완성 렌더링, 잘못된 의자 형태, 수동 검수 결여를 명시함.
- 불완전한 원본 렌더링은 승인 불가. 잘못된 팔걸이·접이식·흔들의자 구별도 별도 문제로 처리.
- 357개의 원본 매칭/아틀라스/TMX/타일 속성을 변경하지 않음. 새 대체 후보는 최종 확정 아닌 조건부 제안.

## 파일
- ALL_357_MATCH_SAFETY_AUDIT.csv : 전체 승인 게이트
- ALL_CHAIR_BENCH_STOOL_COUCH_REVIEW.csv : 앉는 가구 집중 검수 목록
- TWO_WRONG_CHAIRS_REPLACEMENT_PROPOSALS.csv : 잘못된 두 후보 수정안
- examples : 좀보이드 왼쪽 / 실제 Blockbench 오른쪽 비교 사진
- 전체 새 후보 사진은 이전 폴더 chair_candidate_native_blockbench_v1 의 12개 비교 JPG.
