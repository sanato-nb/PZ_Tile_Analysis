# 로즈우드 가구 24차: B 레인 231~240번 독립 수동 시각 검수

PZ B42 완성형 원본 10개와 기존 비교판을 직접 육안 대조했다. 이번 후보는 Decocraft 3.0.4-1.20.1 공식 배포 JAR의 원본 BBMODEL 및 텍스처를 SHA512/SHA256 검증한 뒤 Blockbench 5.2.2에서 재렌더했다.

본 결과는 10개 고유 가구에 대한 외형 판정이다. 모드 실제 게임 설치, 1:1 동일성, 충돌/상호작용/방향, PZ 멀티타일 재조립 정확성은 인증하지 않았다.

기존 001~230번 및 A/C 레인의 독립 Draft PR은 병합하거나 덮어쓰지 않았다. 원본 TMX/PNG/SQLite 및 글로벌 357행 매칭표는 변경하지 않았다.

검수 10종: 조건부 0, 보류 10. 네이티브 Blockbench 원본 로드 10/10, 전체 형상 캡처 10/10 (238번 넓은 카메라 재촬영), 비교 JPG 10장, 인게임 1:1 인증 0종.

Decocraft 원본 JAR SHA512: \`f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05\` / https://modrinth.com/mod/decocraft/version/K6V6djNF

## 개별 검수

### 231 Couch / Red Comfy

판정: **DEFER_RED_TWO_SEATER_VS_SINGLE_CORNER_MODULE**. 검토 후보: decocraft:couch_corner_red.

PZ 형태: 2×1 오렌지·붉은색 패브릭 2인 소파. 두꺼운 양팔걸이, 낮은 직선 등받이, 4개 어두운 다리.

육안 비교 및 오매칭 원인: PZ는 오렌지색 두 좌석과 양끝 두꺼운 팔걸이·낮은 검정 다리의 2×1 완성 소파다. 기존 Macaw red_couch는 한쪽 소파 조각으로 완성 2인 결합 미확인. 이번 Decocraft couch_corner_red 원본 BBMODEL(7 cubes)을 공식 Blockbench 5.2.2로 렌더하니 짙은 빨강 단색 한 좌석 코너 모듈과 한쪽 팔걸이/높은 등받이가 나타났다. PZ의 밝은 오렌지 패브릭·두 좌석·양끝 팔걸이·검정 발과 색/조립이 달라 보류.

추가 확인: 2좌석 전체 결합, 붉은 패브릭 톤, 양쪽 팔걸이, 2×1 설치·회전·앉기 기능.

원본 PZ SHA256: \`92bf2fa0d8955e20a0490125f87e111a1f12f43d11102ee10c8fbb0154bf302e\`

원본 MC 모델 SHA256: \`2d353c50b87de0fae4a25a97177f53e1c7f851e2044ffdbd35125802bdf71656\`

비교 카드 SHA256: \`74a9c23af56dc2907fe49379c6f8435bd86945eb0b80874507ae82486a6dd31b\`


### 232 Counter / Oak Floating

판정: **DEFER_FLOATING_WALL_CABINET_VS_FLOOR_VANITY**. 검토 후보: decocraft:bathroom_counter_left_oak.

PZ 형태: 1×1 중간 갈색 목재 벽걸이 2문 캐비닛. 평평한 상판, 앞면 세로 패널문 2개와 작은 손잡이, 다리 없음.

육안 비교 및 오매칭 원인: PZ는 벽에 매다는 중간 갈색 원목 2문 캐비닛(작은 손잡이 두 개)이다. 기존 Macaw dark_oak_counter는 문 없는 검정 갈색 통나무 블록. 새 Decocraft bathroom_counter_left_oak 원본 BBMODEL(13 cubes)은 흰색 두꺼운 상판, 밝은 참나무 측판, 열린 측면 수납칸과 흰 병/수건이 있는 바닥형 욕실 카운터로 확인됐다. 문·벽부착·색상·높이가 모두 다르다.

추가 확인: 벽걸이 2문 캐비닛, 문 열림·바닥과의 간격·벽 부착 및 1×1 점유.

원본 PZ SHA256: \`dc3fbe4c8d8e1afc7a1d2bbe5587f090477f4e8705ffe197d344b41b9e663de4\`

원본 MC 모델 SHA256: \`eaa9c1d69c46b653df6f07f5c3e83b6076a15690539ad76707502deab6e9a7bc\`

비교 카드 SHA256: \`01da01dac652bb6c80f36214661931ae1ed95bb9f6b420d9c1131aa65eeec9b1\`


### 233 Lamp / Fancy Green

판정: **DEFER_THREE_ARM_HANGING_GREEN_LAMP_VS_SINGLE_POLE**. 검토 후보: decocraft:lamp_cable_base_black_green.

PZ 형태: 2×1 금색 중앙 줄기에서 3개 곡선 팔이 뻗은 천장형 샹들리에. 녹색 갓 3개와 아래 금색 프린지.

육안 비교 및 오매칭 원인: PZ는 금색 줄기에서 3개 곡선 가지와 녹색 갓·금색 장식이 내려오는 2×1 샹들리에다. 기존 decocraft:lamp_cable_base_black_green을 실제 Blockbench 5.2.2(6 cubes)로 재렌더하니 검정 긴 단일 수직 봉과 녹색 납작한 상단 캡만 있다. 3등 가지, 전등갓, 천장형 구조가 없어 보류.

추가 확인: 3개 전등갓·금색 곡선 팔·천장 매달림·2×1 설치·조명 ON/OFF.

원본 PZ SHA256: \`30f0b87ddbd86fe627b936a8141efef076526257373484279e87b429f18df0f0\`

원본 MC 모델 SHA256: \`26b59a37fd0c3c9e9924be16661447f6df21d07fd9037d0bbfd7dc8829e1888b\`

비교 카드 SHA256: \`ecdc098fac0c90d401dd44fe7d4696b3290aec3eec2882763d1611a6f11a74ce\`


### 234 Sink / Fancy Hanging

판정: **DEFER_STAINLESS_WALL_FOUNTAIN_VS_FLOOR_SINK_CABINET**. 검토 후보: decocraft:sink_cabinet_white.

PZ 형태: 1×1 벽부착형 은색 음수대/세면대. 뒤에 직사각 금속 벽판, 앞으로 돌출한 둥근 스테인리스 물받이와 수도꼭지.

육안 비교 및 오매칭 원인: PZ는 회색 스테인리스 벽판에 앞으로 돌출된 둥근 음수대와 금속 수도꼭지가 달린 1×1 벽걸이형 설비다. 기존 pfm:basic_sink Blockbench는 황색 평판 하나만 나오는 불완전 모델. 새 Decocraft sink_cabinet_white 원본 BBMODEL(10 cubes)은 흰색 바닥 수납장 상자와 문·경첩이며, 둥근 금속 물받이/수도꼭지/벽판이 없어 보류.

추가 확인: 벽부착 원형 스테인리스 물받이·수도꼭지·배관 기능·높이/방향.

원본 PZ SHA256: \`ba9025ef137911c67b0a7fcaf738fa86f8289717c5ae611d6966fdb763beb5f0\`

원본 MC 모델 SHA256: \`e492edc5161e4fb8a6a36ae3ebe0e527940b47249a2a67a2c8795402f2c9eb33\`

비교 카드 SHA256: \`230f339f8dfb5e4a7fe4a46d904596046974c0fb00366839b3616b4ad8880a2b\`


### 235 Table / Long Oak

판정: **DEFER_THREE_TILE_WOOD_METAL_TABLE_VS_SHORT_KITCHEN_TABLE**. 검토 후보: decocraft:kitchen_table_oak.

PZ 형태: 3×1 긴 직사각 중간 갈색 원목 상판과 얇은 검정 금속 4다리, 아래 삼각형 보강 지지대.

육안 비교 및 오매칭 원인: PZ는 3×1 갈색 원목 상판, 얇은 검정 금속 4다리, 양끝 대각 보강대를 가진 긴 테이블이다. 기존 Macaw dark_oak_glass_table 캡처는 유리 평판 일부만 보이는 불완전 모델. 새 Decocraft kitchen_table_oak 원본 BBMODEL(29 cubes)은 두꺼운 흰 상판과 밝은 참나무 장식 기둥 4개를 가진 정사각/짧은 식탁이다. 상판 재질·3칸 길이·검정 금속 다리·보강대가 달라 보류.

추가 확인: 3×1 길이, 목재 상판, 검정 금속 다리/보강대, 연결·충돌·회전.

원본 PZ SHA256: \`fa20ea287710b67ca976d443122da48da5f7b9fe16a749fc7f987ffc6019375b\`

원본 MC 모델 SHA256: \`014cf39af640f4120c32def0d1fbb27511bc7f14dfef1be3c82fabfbe6a06deb\`

비교 카드 SHA256: \`850edfe5013fdd90c13b2f755bf7f4c8ec69adcd90665dac36be6f6643e91524\`


### 236 Counter / Pie Store

판정: **DEFER_WHITE_PANELED_PIE_COUNTER_VS_KITCHEN_CABINET**. 검토 후보: decocraft:bottom_cabinet_1_white.

PZ 형태: 1×1 작은 파이 가게 카운터. 밝은 흰색 세로 판재 몸체, 연한 갈색 원목 상판과 갈색 모서리 프레임.

육안 비교 및 오매칭 원인: PZ는 연갈색 목재 상판과 흰색 세로 패널 몸체, 갈색 모서리 프레임을 가진 파이 가게용 1×1 카운터다. 기존 Macaw acacia_counter는 회색 석재 몸체/주황 상판. 새 Decocraft bottom_cabinet_1_white 원본 BBMODEL(13 cubes)은 흰 가로 프레임의 상단 서랍과 아래 수납문, 검정 손잡이 및 밝은 나무 상판을 가진 주방 하부장이다. 흰 몸체/목재 상판이라는 일부 유사성은 있지만 PZ의 무손잡이 세로 판재 카운터와 전면 구성이 다르므로 확정·조건부 승인하지 않는다.

추가 확인: 흰색 세로 패널 1×1 카운터, 밝은 목재 상판, 앞/옆 마감, 수납 기능.

원본 PZ SHA256: \`c6e8970ac815da2360bdbe2fa53dd460a1453888d723b4326d24286347b133a9\`

원본 MC 모델 SHA256: \`512f252cb22f035ad901daef97a208680f8e57b67f47b250318dd05151e87c1b\`

비교 카드 SHA256: \`d4b706bf87f3276b6b0494c67a0cbc793d08fe1448f8ee5047bb3020bbbd86f5\`


### 237 Bed / Hospital

판정: **DEFER_GREEN_METAL_HOSPITAL_BED_VS_WOOD_DOUBLE_BED**. 검토 후보: decocraft:double_bed_oak_white.

PZ 형태: 1×2 단층 병원 침대. 얇은 흰 매트리스, 어두운 녹색 금속 프레임과 낮은 앞뒤 튜브 난간, 바닥에서 뜬 4다리.

육안 비교 및 오매칭 원인: PZ는 1×2 얇은 흰 매트리스, 짙은 녹색 금속 프레임, 머리·발끝에 얇은 튜브 난간을 가진 단층 병원 침대다. 기존 Decocraft 2층 나무 침대는 오매칭. 새 double_bed_oak_white 원본 BBMODEL(36 cubes)은 두 명이 눕는 넓은 밝은 참나무 프레임, 체크무늬 침구, 나무 헤드보드와 발판이 있는 일반 더블침대다. 병상 금속 난간·단인용 폭·녹색 프레임이 없어 보류.

추가 확인: 1×2 단층 금속 병원 침대, 양끝 난간, 녹색 프레임, 눕기/충돌.

원본 PZ SHA256: \`e718505d13b1946485d43c9984b2933442a71412914173e071bff35f13c540b8\`

원본 MC 모델 SHA256: \`386e358e9cf72ead5f9e5f916b9b3f4dc9387b68aec75cba29f3a5ba8c058b13\`

비교 카드 SHA256: \`ef2be2db9e751f882bc128697a7b0a087ded3480704e58b04fcce820b63a369a\`


### 238 Bench / Long Wooden

판정: **DEFER_LONG_BROWN_BACKLESS_BENCH_VS_PADDED_GYM_BENCH**. 검토 후보: decocraft:gym_bench.

PZ 형태: 1×2 등받이·팔걸이 없는 긴 갈색 나무 벤치. 여러 개의 좁은 세로 목재 좌판과 양끝 사선 다리.

육안 비교 및 오매칭 원인: PZ는 1×2 갈색 목재 판재 좌판과 양끝 사선 다리만 있는 등받이 없는 긴 벤치다. 기존 Handcrafted dark_oak_bench는 빨강 쿠션·등받이 있는 한쪽 좌석 모듈. 이번 Decocraft gym_bench 원본 BBMODEL(7 cubes)은 처음 Blockbench 캡처가 잘려 전체 형상을 판정할 수 없었지만, 넓은 카메라로 공식 Blockbench 5.2.2를 재실행하여 검정 패딩 상판과 검정 금속 사선 지지대가 있는 짧은 운동용 벤치임을 확인했다. PZ의 갈색 나무 긴 좌판·2칸 길이·목재 사선 다리와 재질/비율이 달라 보류.

추가 확인: 2칸 연속 나무 좌판, 등받이 없는 구조, 사선 다리, 앉기 기능.

원본 PZ SHA256: \`0a6a7088eb0b39ded9866859fc4afa5cd05f3cb197f2dfe1bdb5bd39933be5c3\`

원본 MC 모델 SHA256: \`80de203fee5ce870e3934b0061a6fa0aff397748fc501a2131e2d913173ae632\`

비교 카드 SHA256: \`820580757cbac56ca787f5b506ec3b84031f7b29bae28d04365f84c8f62f339a\`


### 239 Chair / Rocking

판정: **DEFER_RATTAN_ROCKING_CHAIR_VS_FOLDING_DECK_CHAIR**. 검토 후보: decocraft:beach_chair_gray.

PZ 형태: 1×1 짙은 갈색 곡선 목재 프레임의 라탄 흔들의자. 높은 타원형 라탄 등받이, 좌판 격자, 말린 팔걸이와 바닥 곡선 러너.

육안 비교 및 오매칭 원인: PZ는 곡선 갈색 나무 러너, 말린 팔걸이, 높은 타원형 라탄 등받이와 라탄 좌판을 가진 1×1 흔들의자다. 기존 pfm:arm_chair_leather는 회색 판만 보이는 불완전 모델. 새 Decocraft beach_chair_gray 원본 BBMODEL(18 cubes)을 렌더하니 검정·흰색 줄무늬 천과 가는 밝은 나무 경사 프레임의 접이식 해변 의자다. 흔들목·라탄·곡선 팔걸이가 없어 보류.

추가 확인: 라탄 직조, 타원형 높은 등받이, 곡선 흔들목·팔걸이, 흔들기/앉기 기능.

원본 PZ SHA256: \`b24eb7ae2907aa788a9d1768e92498537667c96a65a1cfdb382e722ee2789865\`

원본 MC 모델 SHA256: \`ef7759d3dd1b64eadd7507536995553eaac771f210224316e807169f7c24e17e\`

비교 카드 SHA256: \`593299ff18629c17df14b5704e2672ded92528a90730316ecfbdbe8d6b414fa0\`


### 240 Couch / Victorian C5

판정: **DEFER_TUFTED_BROWN_VICTORIAN_CHAISE_VS_PLAIN_CORNER**. 검토 후보: decocraft:couch_corner_leather_brown.

PZ 형태: 1×2 빅토리아풍 갈색 가죽 긴 셰즈/소파. 등받이와 한쪽 팔걸이의 두툼한 단추형 퀼팅, 한쪽 열린 좌석과 짧은 나무 다리.

육안 비교 및 오매칭 원인: PZ는 1×2 갈색 가죽 빅토리아풍 비대칭 셰즈로, 높은 한쪽 등받이/팔걸이에 둥근 단추형 퀼팅이 가득하다. 기존 Macaw black_couch는 검정 한 좌석 소파 조각이다. 새 Decocraft couch_corner_leather_brown 원본 BBMODEL(7 cubes)은 갈색 단색 평면 코너 모듈 1석으로 확인됐다. 단추형 퀼팅·긴 비대칭 몸체·1×2 전체 조립이 없어 보류.

추가 확인: 갈색 단추형 퀼팅 가죽, 한쪽 높은 팔걸이, 1×2 셰즈 전체 연결·회전·앉기.

원본 PZ SHA256: \`a98d235e2ff9b7d5e90d1a7b48a68198491f75ee8e4b190fad0118cc8a3d2ca9\`

원본 MC 모델 SHA256: \`2d353c50b87de0fae4a25a97177f53e1c7f851e2044ffdbd35125802bdf71656\`

비교 카드 SHA256: \`a18c5a2e9f680470869eeb79885886cb2935fc0bdb23d75b32167da210a40d08\`


## 산출물

cards/ : 231~240 PZ 대 실제 원본 Minecraft 모델(미확인 시 구형 참고 이미지로 명시) JPG 10장

BATCH_231_240_MANUAL_VISUAL_REVIEW.csv : 검수 판정·형태·이전 오매칭·후속 확인

BATCH_231_240_DEFERRED_OTHER_MODS.csv : 다른 모드 또는 바닐라 재검색 목록

BATCH_231_240_SHA256_PROVENANCE.csv : 원본·텍스처·렌더·카드 SHA256

NATIVE_BLOCKBENCH_PROOF.json / MANIFEST.json / BATCH24_STANDALONE_PROGRESS.json : 원본 렌더 증빙 및 범위

INDEX.html / ROSEWOOD_BATCH_231_240_MANUAL_REVIEW.zip : 갤러리와 묶음 산출물
