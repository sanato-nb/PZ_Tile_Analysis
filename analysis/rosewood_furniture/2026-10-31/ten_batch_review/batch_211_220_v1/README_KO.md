# 로즈우드 가구 211~220 수동 시각 검수 — 레인 C

**2026-11-02 / 기준 브랜치** `work/rosewood-manual-batch10-091-100-20261101`

원본 PZ 완성형 이미지와 기존 원본 Minecraft 모드 기반 좌우 비교 JPG 10장을 **각각 실제로 관찰**하여 211~220번만 재판정했다. **시각 조건부 1종(#214), 보류 9종, 인게임 1:1 인증 0종**. 기존 자동 판정은 승인 근거로 사용하지 않는다.

**이번 실행 신규 Blockbench 렌더는 0건**이다. 비교 JPG 10개는 원본을 바이트 그대로 재사용했고, 원본 PNG 10개도 함께 복사했다. 카드 이미지에 인쇄된 과거 판정(특히 #213의 CONDITIONAL_MATCH)은 최신 결론이 아니며, 최신 수동 판정은 CSV에 있다.

## 10개 개별 관찰

- **#211 Dish / Satellite** — `decocraft:dish_rack_birch`, PZ 1×1 (임시), **DEFER_WRONG_OBJECT**: PZ는 흰 접시형 위성 안테나와 수신 암·벽면 브래킷, MC는 목제 접시 건조대와 그릇이다. Dish라는 영어 동음이의어만 일치하며 용도·형상·벽 부착 모두 다름.
- **#212 Freezer / Popsicle** — `refurbished_furniture:dark_freezer`, PZ 1×2, **DEFER_CHEST_FREEZER_MISMATCH**: PZ는 1×2 수평형 연회색 ICE 냉동고·상단 유리 미닫이 뚜껑 2장, MC는 검정 전면문과 갈색 측판의 세로형 1블록 냉동고 부분 렌더다.
- **#213 Fridge / Large** — `decocraft:fridge_large`, PZ 2×1, **DEFER_INDUSTRIAL_VS_DOMESTIC_FRIDGE**: PZ는 2×1 검정 산업용 평판 냉장고·하단 통풍 그릴, MC는 은색 4문 가정용 냉장고·손잡이·정수기. 기존 조건부 판정을 외형 불일치로 보류로 변경한다.
- **#214 Microphone / Standing** — `decocraft:microphone_stand_black`, PZ 1×1 (임시), **CONDITIONAL_VISUAL_ONLY**: 둘 다 검정색 수직 스탠드 위에 기울어진 마이크가 있다. PZ의 세 갈래 삼각 받침·가느다란 마이크 목과 MC의 팔각 원형 받침·굵은 헤드가 다르므로 외형 조건부만 인정한다.
- **#215 Table / Long** — `mcwfurnitures:acacia_glass_table`, PZ 1×1 (임시), **DEFER_MISSING_LEGS_AND_COLOR**: PZ는 진갈색 목재 직사각 상판·4개의 가는 다리, MC는 밝은 아카시아색 납작한 부분 렌더만 표시돼 다리·높이·길이가 누락됐다.
- **#216 Table / Long Dark** — `mcwfurnitures:acacia_glass_table`, PZ 1×1 (임시), **DEFER_MISSING_LEGS_AND_DARK_FINISH**: PZ는 흑갈색 긴 목제 상판·4다리, MC는 215번과 동일한 밝은 아카시아색 납작한 부분 렌더라 다리·어두운 색·두께가 누락됐다.
- **#217 Counter / Glass Display** — `mcwfurnitures:acacia_counter`, PZ 1×1 (임시), **DEFER_GLASS_DISPLAY_ABSENT**: PZ는 검정 받침 위 투명 유리 3면·유리 상판·금속 프레임의 진열 카운터, MC는 불투명 나무 몸통과 주황 상판의 일반 카운터다.
- **#218 Shelves / Comics Shop** — `handcrafted:acacia_shelf`, PZ 1×1 (임시), **DEFER_COMICS_SHELF_MISMATCH**: PZ는 회색 금속 3단 개방 선반과 초록·노랑 만화가게 광고 패널, MC는 적갈색 목제 2칸 박스 선반이다.
- **#219 Shelves / Long** — `handcrafted:acacia_shelf`, PZ 1×4, **DEFER_FOOTPRINT_1X4_VS_1X1**: PZ는 4조각을 이은 1×4 긴 밝은 목재 3단 선반, MC는 1×1 적갈색 2칸 박스 선반으로 길이·층수·개방도·색·멀티타일 조립이 다르다.
- **#220 Barbecue / Full Jorge Foreguy** — `refurbished_furniture:black_grill`, PZ 1×1 (임시), **DEFER_PARTIAL_GRILL_RENDER**: PZ는 은색 곡면 뚜껑·검정 본체·전면 노브·좌우 선반·바퀴의 가스 바비큐, MC 부분 JSON 렌더는 회색 막대와 검정 블록만 보여 완성 모델 증거가 아니다.

## 다음 검증 우선순위

- #211 위성 안테나 ↔ 식기 건조대의 **동음이의어 오매칭** 해소.
- #212 수평 1×2 ICE 냉동고, #213 검정 산업용 2×1 냉장고, #219 1×4 목제 선반의 **멀티타일 크기·조립** 검증.
- #214 검정 마이크 스탠드는 형태만 조건부. 삼각 받침 차이와 인게임 충돌·설치 미확인.
- #215·216·220은 **부분 모델 렌더를 완성품으로 착각하지 않도록** 실제 원본 JAR 모델 재로딩이 필요.
- #217·218은 유리 진열장·광고판이 빠진 다른 종류의 가구이므로 다른 모드/바닐라 조합 탐색.

## 파일 구성 및 한계

- `cards/`: 원본 좌우 비교 JPG 10개 (기존 소스 렌더 재사용)
- `pz_previews/`: PZ 완성형 PNG 10개
- `BATCH_211_220_MANUAL_VISUAL_REVIEW.csv`: 최신 개별 수동 판정·사유·후속 조건
- `BATCH_211_220_DEFERRED_OTHER_MODS.csv`: 보류 9종
- `SOURCE_SHA256.csv`: **20개 이미지의 실제 바이트로 계산한 SHA-256**, Git blob SHA-1, 원본 경로
- `MANIFEST.json`, `verify_batch.py`, `ROSEWOOD_BATCH_211_220_REVIEW.zip`: 범위/검증 도구/비교 JPG 10개+문서 ZIP

ZIP에는 10개 비교 JPG와 문서 6개를 담고, 10개 PZ PNG는 브랜치에 별도로 보관한다. ZIP 생성 시 CRC32를 계산하고, verify_batch.py로 검증 가능하다.

**미검증**: 이번 실행에 Minecraft Forge 1.20.1 또는 Blockbench 5.2.2를 실행하지 않았고 원본 JAR을 새로 열지 않았다. 설치·회전·충돌·상호작용·실제 1:1 배치 인증 없음. 이 PR은 Draft로만 유지하며 기존 TMX·PNG·SQLite·다른 PR은 수정하지 않는다.
