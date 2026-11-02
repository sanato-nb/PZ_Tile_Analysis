# 로즈우드 가구 개별 시각 재검수 16차 — 151~160

이 배치는 기존 PZ B42 완성형 가구 미리보기와 실제 모드 소스에서 과거 렌더링한 Minecraft 비교 JPG **10장 전부를 직접 열람하여 재판독**한 기록이다. 10개 비교 JPG는 기존 저장소 이미지 blob을 **변경 없이 재사용**했으며 이번 실행에서 Blockbench를 새로 실행하거나 JAR를 다시 추출한 것은 아니다. 원본 JPG에 일부 한글 글리프가 깨져 있으므로 아래 설명을 기준으로 판독한다. 외형 비교는 시각적 잠정 판단이며 게임 설치·충돌·상호작용·방향·1:1 인증은 모두 0건이다.

**판정:** 시각 조건부 1건(160, 실제 설치 크기 충돌로 승인 불가), 보류 9건(151~159), 인게임 승인 0건. 이전 자동 이름 매칭 결과를 확정 판정으로 승격하지 않았다.

## 개별 관찰

### 151 Radio / ValuTech — DEFER
- **PZ 원본 관찰:** Portable silver/black rectangular radio with vertical aerial and circular dial/speaker
- **기존 MC 후보:** `NONE` (과거 모델 근거: NO_REAL_MOD_ASSET)
- **실물 비교:** No actual MC radio source/model found in existing inspected candidate list; do not invent a radio model
- **후속 조치:** Find source-verified tabletop portable radio with antenna and working radio analogue
- **PZ 구성:** 1 parts, 1x1 provisional; 원본 Tile ID: `appliances_radio_01/0`
- **증거:** [비교 이미지](cards/151_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `796cd99d8012087e30db68dff23271a3aebd41b93e5df5e4bbd10897df2f17bb`

### 152 Shower / Deluxe — DEFER
- **PZ 원본 관찰:** White square raised shower base, round drain, detached chrome head and wall controls
- **기존 MC 후보:** `pfm:basic_shower_handle` (과거 모델 근거: PARTIAL_JSON)
- **실물 비교:** MC render shows only a small rectangular red/grey handle, not tray, plumbing or shower head
- **후속 조치:** Search complete shower enclosure/base/head; verify 1x1 plumbing and wall attachment
- **PZ 구성:** 1 parts, 1x1 provisional; 원본 Tile ID: `fixtures_bathroom_01/32`
- **증거:** [비교 이미지](cards/152_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `cb88aebda35240c70abbb370ba65b8395e210e426034e472adedc770776665cb`

### 153 Shelves / Beige Rack Shop — DEFER
- **PZ 원본 관찰:** Long beige 4-tile shop rack, 3 open shelf levels, upright end frames and thin rods
- **기존 MC 후보:** `handcrafted:acacia_shelf` (과거 모델 근거: FULL_JSON)
- **실물 비교:** MC single orange/brown blocky shelf has solid sides and no continuous 4x1 open rack geometry
- **후속 조치:** Find real 4x1 retail gondola/rack or verified repeatable multipart modular model
- **PZ 구성:** 4 parts, 4x1; 원본 Tile ID: `location_shop_generic_01/8|9|10|11`
- **증거:** [비교 이미지](cards/153_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `6187b604b9c1ed8509c325d433d6cb2d083157fc76b4fd87bc5fadb5570b5a97`

### 154 Barbecue / Charcoal — DEFER
- **PZ 원본 관찰:** Red rounded dome lid on black kettle bowl, three slim angled legs
- **기존 MC 후보:** `refurbished_furniture:black_grill` (과거 모델 근거: PARTIAL_JSON)
- **실물 비교:** MC partial render is separated tall grey post and black cuboid; no red dome, kettle bowl or tripod
- **후속 조치:** Check Decocraft grill_black full BBMODEL or another verified red kettle charcoal grill
- **PZ 구성:** 1 parts, 1x1 provisional; 원본 Tile ID: `appliances_cooking_01/35`
- **증거:** [비교 이미지](cards/154_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `b7c62fb1dd1c553882af8d587495574ff65d2a3ef3b504d62abce06531565e75`

### 155 Counter / White Floating — DEFER
- **PZ 원본 관찰:** Solid cream wall-mounted closed cabinet with two front doors and small vertical handles
- **기존 MC 후보:** `decocraft:bathroom_counter_left_white` (과거 모델 근거: SOURCE_BBMODEL)
- **실물 비교:** MC model is an open white bathroom counter with wood top and visible shelves/bottles; not a closed hanging cabinet
- **후속 조치:** Search closed ivory wall-mounted double-door cabinet, no counter top
- **PZ 구성:** 1 parts, 1x1 provisional; 원본 Tile ID: `fixtures_counters_01/159`
- **증거:** [비교 이미지](cards/155_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `0198a2c0620bc6bb70d153e5608178f4c5d00e50d5a50d48a266cae039557701`

### 156 Shelves / Corner A — DEFER
- **PZ 원본 관찰:** Brown left end section of three open horizontal shelves with left back/support panel
- **기존 MC 후보:** `handcrafted:acacia_shelf` (과거 모델 근거: FULL_JSON)
- **실물 비교:** MC orange closed boxy cubby is not three open protruding shelves; left/right geometry unverified
- **후속 조치:** Find 3-tier brown open modular shelving left-end source model
- **PZ 구성:** 1 parts, 1x1 provisional; 원본 Tile ID: `furniture_shelving_01/16`
- **증거:** [비교 이미지](cards/156_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `61a4fa7cb6a8e406fbe01521b5110f3989b25e0d10dbacf8c050ebd68d96c6d5`

### 157 Shelves / Corner B — DEFER
- **PZ 원본 관찰:** Brown right end section with right-side support and three open projecting shelf boards
- **기존 MC 후보:** `handcrafted:acacia_shelf` (과거 모델 근거: FULL_JSON)
- **실물 비교:** Same MC candidate reused for opposite PZ end; cannot encode both handed variants as shown
- **후속 조치:** Find 3-tier brown open modular shelving right-end source model
- **PZ 구성:** 1 parts, 1x1 provisional; 원본 Tile ID: `furniture_shelving_01/18`
- **증거:** [비교 이미지](cards/157_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `6527c21f93b6687fe5903070b8338486c2f367d8aea0c16976abc435caad8554`

### 158 Shelves / Middle — DEFER
- **PZ 원본 관찰:** Three brown horizontal open floating shelf boards without side panel
- **기존 MC 후보:** `handcrafted:acacia_shelf` (과거 모델 근거: FULL_JSON)
- **실물 비교:** MC full orange solid cabinet/shelf body with thick top and sides, not open center piece
- **후속 조치:** Find source-verified 3-tier open shelf center segment and test joins to 156/157
- **PZ 구성:** 1 parts, 1x1 provisional; 원본 Tile ID: `furniture_shelving_01/17`
- **증거:** [비교 이미지](cards/158_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `1c114e6015e1ae5141b856863bb7458de4d1bdf71418be84a6efc19c6dbda353`

### 159 Table / Large Dark Wooden — DEFER
- **PZ 원본 관찰:** Long dark walnut wood tabletop with four straight legs, 2x1 footprint
- **기존 MC 후보:** `mcwfurnitures:dark_oak_glass_table` (과거 모델 근거: PARTIAL_JSON)
- **실물 비교:** MC proof renders a pale flat glass-textured plane, no dark wooden top or legs; partial model
- **후속 조치:** Find source-rendered 2x1 dark oak four-leg table, verify multiblock and collision
- **PZ 구성:** 2 parts, 2x1; 원본 Tile ID: `furniture_tables_high_01/40|41`
- **증거:** [비교 이미지](cards/159_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `df999c754941304c9cf892c7d613443994abb833b24166fd7a2a1c33ffc13e2b`

### 160 Table / Pool — CONDITIONAL_VISUAL_ONLY
- **PZ 원본 관찰:** Green felt pool table, brown rails, six pockets and four legs, empty top
- **기존 MC 후보:** `decocraft:pool_table` (과거 모델 근거: SOURCE_BBMODEL)
- **실물 비교:** MC has recognisable matching felt/wood/legs/pockets but visible coloured racked balls and cue ball; prior MC model bounds ~3x2 blocks versus PZ 2x1
- **후속 조치:** Verify actual Minecraft 3x2 footprint, placement, rotation and game function; seek 2x1/empty variant
- **PZ 구성:** 2 parts, 2x1; 원본 Tile ID: `recreational_01/2|3`
- **증거:** [비교 이미지](cards/160_PZ_vs_MC.jpg) · 원본 비교 JPG SHA-256 `9e9a109651ef37adf4fc67464a76535c3b94b4796b0f60c49e33205565ace3d8`

## 출처와 한계

- PZ: 저장소 `analysis/rosewood_furniture/2026-10-31/all_357_complete_native_comparisons_v1/cards`의 완성형 PZ 이미지. 원본 TMX/PNG를 이번 실행에서 직접 재조립하지 않았으므로 이전 조립 결과의 정확성을 재인증하지 않는다.
- MC: 같은 카드 오른쪽에 보이는 기존 Blockbench 소스 렌더. `PARTIAL_JSON`은 실제 모델 전체 형상 증거가 아니므로 부적합 후보를 승인하지 않는다. 특히 153/156/157/158에 같은 `handcrafted:acacia_shelf`가 재사용된 것은 독립 매칭 증거가 아니다.
- 160의 Decocraft Pool Table은 형태는 유사하지만 기존 소스 모델의 약 3×2 블록 경계와 PZ 2×1 점유가 달라 **실제 맵에 1:1 치환하면 공간 충돌 가능성이 크다.** 게임 배치 검증 전에는 사용 금지.
- 기존 카드 10개를 원본 Git blob SHA 그대로 참조하며 새로 렌더했다고 주장하지 않는다. JPG별 SHA-256은 `SOURCE_SHA256.csv`에 기록.
- Forge 1.20.1 실제 인게임 배치/모드 호환성/기능 인증 0. 사용한 모드 버전·JAR의 현재 재검증도 0.
- 다른 예약 작업 A(131~140 등), B(141~150 등) 범위와 겹치지 않는다. 기존 PR #251~#257 및 모든 원본 TMX/PNG/SQLite/기존 CSV는 수정하지 않았다.

## 산출물

- `cards/151_PZ_vs_MC.jpg` ~ `cards/160_PZ_vs_MC.jpg`: **기존 비교 이미지의 정확한 재사용 사본** 10장
- `BATCH_151_160_MANUAL_VISUAL_REVIEW.csv`: 독립 시각 판정 10행
- `BATCH_151_160_DEFERRED_OTHER_MODS.csv`: 후속 검색 보류 9행
- `SOURCE_SHA256.csv`: 10개 JPG 실제 바이트 SHA-256 + Git blob SHA
- `MANIFEST.json`: 검수 범위·수량·인증 수준
- `INDEX.html`: 카드 열람기
- `ROSEWOOD_BATCH_151_160_REVIEW.zip`: 동일 결과 ZIP (추가 커밋에서 생성)
