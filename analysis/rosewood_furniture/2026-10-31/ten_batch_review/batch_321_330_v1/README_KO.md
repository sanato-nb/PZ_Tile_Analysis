# 로즈우드 B 레인 33차 — 321~330 개별 시각 검수

PZ 원본 완성형 조립 미리보기 10종과 기존 Minecraft 원본 소스 기반 비교 JPG 10개를 실제로 열어 각각 관찰했다.
이번 실행에서 Blockbench를 새로 구동한 것은 아니며, 기존 원본 소스 기반 렌더를 재사용했다.
원본 PZ 미리보기는 임시 조립 상태일 수 있어 구조적 불일치 판정의 제한을 함께 기록한다.

- 개별 검수 10종 / 조건부 0종 / 보류 10종 / 1:1 인증 0종.
- 323번의 Minecraft JSON 스크린샷은 부분 렌더이므로 완성 모델의 외형 증거로 승인하지 않는다.
- 322에는 검증된 MC 모델이 없으며 우측은 안내 카드이므로 실제 모델 비교가 아니다.
- 325·326·327은 서로 다른 색상의 L자 코너 카운터인데 동일한 검정·은색 줄무늬 카운터가 후보로 지정돼 있다.
- Minecraft Forge 1.20.1 설치·충돌·방향·기능 검증은 수행되지 않았다.

## 검증 자료

- cards/: 기존 이미지로부터 새로 제작한 개별 좌우 비교 JPG 10장.
- BATCH_321_330_MANUAL_VISUAL_REVIEW.csv: 10개 외형·재질·색상·구조·점유·한계 판정.
- BATCH_321_330_DEFERRED_OTHER_MODS.csv: 다른 모드 또는 바닐라 재검색 대상 10종.
- SOURCE_SHA256.csv: PZ PNG, 기존 MC 비교 JPG, 새 JPG의 SHA-256 및 기존 Git blob SHA-1.
- MANIFEST.json / BATCH33_STANDALONE_PROGRESS.json / INDEX.html / ZIP / ZIP_SHA256.txt.
- 원본 TMX, PNG, SQLite, 357종 전체 표, 다른 레인의 브랜치는 수정하지 않았다.
- 별도 Draft PR이며 임의 병합하지 않는다.

## 개별 관찰

- 321 Table / Long White ↔ decocraft:kitchen_table_white: PZ는 3×1 길이의 연한 목재 상판과 긴 가로 지지대가 있는 테이블이다. MC kitchen_table_white는 정사각형 1블록 갈색 상판·밝은 다리로 렌더되어 길이·색·지지대·멀티타일 점유가 불일치한다.
- 322 Walkie Talkie / Toys-R-Mine ↔ : PZ는 작은 검정 무전기지만 검증된 Minecraft 모드 원본 모델이 없다. 우측은 안내 카드로 실제 3D 렌더가 아니다. 통신 기능도 검증되지 않았다.
- 323 Cabinet / Wide Medical ↔ mcwfurnitures:acacia_double_kitchen_cabinet: PZ는 금속 의료 수납장에 경사진 상단과 밝은 패널·하단 양문이 있지만 MC 후보는 어두운 아카시아 통나무 질감과 붉은 문처럼 보이는 부분 JSON 렌더다. 재질·색·형상이 다르고 완성 모델 증거도 부족하다.
- 324 Counter / Crafted ↔ mcwfurnitures:acacia_counter: PZ는 짙은 갈색 판재를 수직으로 조립한 카운터인데 MC acacia_counter는 주황 상판과 회흑색 나무껍질 질감의 단순 상자다. 판재 배열·재질·색상이 다르다.
- 325 Counter / Dark Bar Corner ↔ decocraft:diner_counter_corner_black: 둘 다 코너형이지만 PZ는 짙은 갈색 목재이고 MC는 검정 몸체에 굵은 은회색 가로 줄무늬가 반복되는 식당 카운터다. 상판·전면 질감이 다르다.
- 326 Counter / Motel Corner ↔ decocraft:diner_counter_corner_black: PZ는 밝은 아이보리색 모텔 코너 카운터인데 MC 후보는 검정 몸체와 은회색 띠의 식당 카운터다. 코너 실루엣 외 색상·패널·재질이 다르다.
- 327 Counter / Zippee Corner ↔ decocraft:diner_counter_corner_black: PZ는 빨간 상판과 흰색 하부의 Zippee 코너인데 MC 후보는 검정·은색 줄무늬 카운터다. 상판·하부 색상과 패널 질감이 다르다.
- 328 Counter / Zippee Display ↔ mcwfurnitures:acacia_counter: PZ는 빨간 상판 아래 열린 진열 선반이 있지만 MC acacia_counter는 주황 상판과 어두운 나무껍질 질감의 불투명 상자다. 열린 진열공간·색상·재질이 다르다.
- 329 Shelves / Clothing Shop ↔ handcrafted:acacia_shelf: PZ는 검정 의류 걸이 봉과 갈색 받침이 분리된 벽걸이 구조인데 MC acacia_shelf는 두꺼운 갈색 목재 덩어리 형태의 선반이다. 금속 봉·벽 고정 구조·빈 공간이 다르다.
- 330 Shelves / Crafted Wooden ↔ handcrafted:dark_oak_shelf: PZ는 전면이 크게 열린 3단 원목 선반인데 MC dark_oak_shelf JSON 렌더는 어두운 목재의 닫힌 상자처럼 보여 개방된 3단 구조가 확인되지 않는다. 승인할 수 없다.
