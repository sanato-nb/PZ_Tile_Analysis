# 로즈우드 B 레인 36차 — 351~357 개별 시각 검수

PZ 원본 완성형 조립 미리보기 7종과 기존 Minecraft 원본 소스 기반 비교 JPG 7개를 실제로 열어 각각 관찰했다.
이번 실행에서 Blockbench를 새로 구동한 것은 아니며, 기존 원본 소스 기반 렌더를 재사용했다.
원본 PZ 미리보기는 임시 조립 상태일 수 있어 구조적 불일치 판정의 제한을 함께 기록한다.

- 개별 검수 7종 / 조건부 0종 / 보류 7종 / 1:1 인증 0종.
- 351·357번 Minecraft JSON 결과는 부분 렌더이므로 완성 모델의 외형 증거로 승인하지 않는다.
- 351번은 PZ 1×2 치과 진료 의자이며 일반 가죽 의자의 부분 렌더와는 비교 승인할 수 없다.
- 352~356번은 서로 다른 색상·재질의 코너 카운터인데 동일한 검정·은색 줄무늬 모델이 후보로 지정돼 있다.
- Minecraft Forge 1.20.1 설치·충돌·방향·기능 검증은 수행되지 않았다.

## 검증 자료

- cards/: 기존 이미지로부터 새로 제작한 개별 좌우 비교 JPG 10장.
- BATCH_351_357_MANUAL_VISUAL_REVIEW.csv: 7개 외형·재질·색상·구조·점유·한계 판정.
- BATCH_351_357_DEFERRED_OTHER_MODS.csv: 다른 모드 또는 바닐라 재검색 대상 7종.
- SOURCE_SHA256.csv: PZ PNG, 기존 MC 비교 JPG, 새 JPG의 SHA-256 및 기존 Git blob SHA-1.
- MANIFEST.json / BATCH36_STANDALONE_PROGRESS.json / INDEX.html / ZIP / ZIP_SHA256.txt.
- 원본 TMX, PNG, SQLite, 357종 전체 표, 다른 레인의 브랜치는 수정하지 않았다.
- 별도 Draft PR이며 임의 병합하지 않는다.

## 개별 관찰

- 351 Chair / Dentist Patient ↔ pfm:arm_chair_leather: PZ는 1×2 진료용 리클라이닝 체어와 발받침·금속 프레임이 일체화되어 있다. 기존 MC pfm:arm_chair_leather의 Blockbench 결과는 회색 평판처럼 보이는 부분 JSON 렌더라 팔걸이·발받침·기울기·1×2 형상을 검증할 수 없다. 용도도 일반 가죽 안락의자여서 승인 불가.
- 352 Counter / Crafter Corner ↔ decocraft:diner_counter_corner_black: PZ는 거친 갈색 목재 판재로 만든 L자 수제 코너이고, MC는 검정 본체와 은회색 가로띠가 두드러지는 식당 카운터다. 코너 실루엣만 비슷하며 색상·재질·판재 방향이 다르다.
- 353 Counter / Oak Corner Bar ↔ decocraft:diner_counter_corner_black: PZ는 밝은 오크 상판과 진한 목재 세로 패널을 조합한 코너 바인데 MC는 검정 상판과 회색 수평 줄무늬가 있는 식당 카운터다. 상판 색·세로 나뭇결·L자 길이와 방향이 불일치한다.
- 354 Counter / Pizzawhirled Corner ↔ decocraft:diner_counter_corner_black: PZ는 붉은 상판과 빨강·흰색 체크 타일 벽면이 특징인데 MC는 검정 본체와 회색 가로 띠다. 색상·체커보드 패턴·매장 정체성이 모두 다르다.
- 355 Counter / Seahorse Coffee Corner ↔ decocraft:diner_counter_corner_black: PZ는 밝은 황토색 상판과 어두운 갈색의 무늬 없는 목재 몸체로 구성되지만 MC는 검정 상판과 은회색 가로 줄무늬다. 상판 색상·하부 재질·띠 유무가 다르다.
- 356 Counter / Spiffos Corner ↔ decocraft:diner_counter_corner_black: PZ는 주황 상판·갈색 몸체·초록색 장식 띠가 핵심인데 MC는 검정 상판과 은회색 줄무늬다. 주황/초록 배색과 전면 패널 구조가 모두 불일치한다.
- 357 Table / Quality ↔ mcwfurnitures:acacia_glass_table: PZ는 짙은 갈색 원목 상판과 네 개의 굵은 다리가 있는 소형 목재 테이블이다. MC acacia_glass_table의 비교 이미지는 밝은 주황색 평판만 보이는 불완전한 부분 JSON 렌더이며 유리/다리 구조가 확인되지 않는다. 재질·색상·형상이 일치하지 않는다.
