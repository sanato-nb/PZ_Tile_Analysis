# 로즈우드 가구 독립 시각 검수 — 레인 C, 241–250

검수일: 2026-11-02 (Asia/Seoul). 기준: `work/rosewood-manual-batch10-091-100-20261101`. 기존 001–240 범위 및 A/B 레인 결과는 변경하지 않음.

## 결과

- **10종 시각 대조 기록 / 조건부 매칭 0 / 보류 10 / 인게임 1:1 인증 0**.
- 원본 PZ 완성형 미리보기 10장과 기존 Minecraft 소스 기반 비교 카드 10장을 실제로 열어 개별 시각 재판독함.
- **이번 실행에서 새 Blockbench 렌더는 하지 않음**. 오른쪽 이미지 중 `NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON`은 모델 일부만 표현할 수 있어 후보의 완전한 외형을 입증하지 못함. 소스 유형을 CSV에 구분함.
- 이전 자료의 243번 'CONDITIONAL_MATCH'는 **프레임 없는 직사각형 대 검정 아치 프레임**의 외형 차이 때문에 이번 수동 판정에서 **보류로 수정**. 원본 CSV는 보존함.
- 244번은 실제 Minecraft 모드 모델이 없어 비교 카드 오른쪽은 단순 안내 텍스트임.

## 개별 판정

- **241 Fancy Dark Table** — 보류. table geometry and wood color absent. 후속: Find actual dark square four-leg table.
- **242 Industrial / Bake-O-Matic** — 보류. different appliance, shape, material, footprint and height. 후속: Search industrial stainless commercial oven/bakery machine.
- **243 Mirror / Middle** — 보류. outline and frame strongly differ; downgrade prior conditional match. 후속: Search unframed rectangular wall mirror.
- **244 Radio / Premium Technologies Ham** — 보류. missing actual MC asset; no visual comparison possible. 후속: Search real ham radio or build verified custom model.
- **245 Sink / Beige** — 보류. partial import is not complete candidate evidence; no faithful sink shape. 후속: Re-render complete textured sink and inspect basin/faucet.
- **246 Table / Long Dark Oak** — 보류. material and 1x3 footprint mismatch; partial source render. 후속: Find 3-block wooden table with complete support frame.
- **247 Chair / Salon** — 보류. no chair seat, armrests or pedestal; partial model evidence. 후속: Search black swivel salon/barber chair.
- **248 Desk / Office 2** — 보류. missing 3x1 desk assembly, tabletop and cabinet; partial side segment. 후속: Render left/middle/right desk states as complete 3x1 unit.
- **249 Shelves / Fancy Wooden Shop** — 보류. open display geometry absent; major material/color mismatch. 후속: Find light wood open retail display shelves.
- **250 Chair / Victorian 5** — 보류. missing upholstery, arms, seat and wood trim; partial model evidence. 후속: Search brown Chesterfield/Victorian armchair.

## 증거 및 제약

- `cards/`: 기존 소스 모델 기반 PZ/MC 비교 JPG **10장** (원본 Git blob SHA-1과 SHA-256은 별도 CSV에 기록).
- `pz_previews/`: PZ 완성형 PNG **10장**. 비교 JPG 및 PNG는 기준 브랜치의 **동일 Git blob**을 재사용하므로 원본 바이트를 바꾸지 않음.
- `BATCH_241_250_MANUAL_VISUAL_REVIEW.csv`: 관찰한 외형, 모드 ID, 근거 수준, 판정.
- `BATCH_241_250_DEFERRED_OTHER_MODS.csv`: 10종 재검색 우선순위.
- `SOURCE_SHA256.csv`: 비교 이미지와 PZ 원본 이미지 20개 SHA-256 및 원본 Git blob SHA-1.
- `MANIFEST.json`, `ROSEWOOD_BATCH_241_250_REVIEW.zip`, `verify_batch.py`: 패키지/무결성 검증.

**판정 기준:** 모양·재질·색상·방향·부분 결합·PZ 멀티타일 점유를 시각적으로 비교. 이미지 크기와 모델 데이터만으로 Minecraft 월드 내 배치·충돌·기능을 인증하지 않음. 미확인 사항을 승인으로 승격하지 않음.

**원본 보존:** TMX/PNG/SQLite 및 이전 PR을 수정하거나 병합하지 않았고, 결과는 전용 브랜치/디렉터리에서만 추가함.
