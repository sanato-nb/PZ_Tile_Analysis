# 로즈우드 가구 20차 191~200번 개별 시각 검수

PZ B42 원본 완성형 미리보기 10장과 이전 Minecraft 원본 Blockbench 비교판 10장을 실제로 육안 검수했다. 별도 GitHub Actions는 Decocraft 3.0.4-1.20.1 Forge 원본 BBMODEL/텍스처를 검증한 뒤 Blockbench 5.2.2로 새로 렌더해 추가 대조한다.

이전 131~140번은 PR #254에서 이미 검수되어 재작업하지 않았다. 141~150번은 레인 B, 151~160번은 레인 C에 속하므로 건드리지 않았다.

원본 Decocraft JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05 | https://modrinth.com/mod/decocraft/version/K6V6djNF

검수 10종: 조건부 1종, 보류 9종. 네이티브 Blockbench 캡처 4/4개 모델. 비교 JPG 10장. 인게임 1:1 확정 0종.

일부 원본 스프라이트의 SpriteGridPos 조립과 마크 모델의 동적 블록 상태는 잠정이다. 1×1/2×1/1×2 점유·방향·충돌·상호작용·색상/재질은 인게임 미검증. 부분 모델 캡처는 완성형으로 승인하지 않는다.

## 개별 근거

### 191 Desk / Medical
판정: **DEFER_THREE_TILE_MEDICAL_DESK_VS_PARTIAL_WOOD_PANEL**. 후보: 보류

PZ 형태: 원본 3타일 1×3 길이의 진회색·검정 평평한 상판, 좌측 판형 다리, 우측 밝은 갈색 이중문 수납장과 열린 중앙 다리 공간.

수동 비교: 실제 PZ 완성형과 기존 mcwfurnitures:acacia_covered_desk Blockbench 화면을 비교하면 오른쪽에는 책상 전체가 아닌 세로 목재판 한 장만 보인다. 검정 긴 상판·우측 2문 수납장·1×3 조립 근거가 모두 빠져 원본 후보는 부적합.

추가 검증: 1.20.1 Forge 3블록 길이 검정 상판 + 밝은 목재 캐비닛 일체형 책상 또는 다중 블록 조합 모델의 실제 렌더·충돌·회전 검사.

PZ SHA-256: `dc419a7204744253539b4f544bf4b4b5ba0f5aa8b603aab762cfc75844b45b86`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `e002b67721b75f10a8f1e50a4e6897e342cfbefecd8724771680983ea78fbaea`


### 192 Counter / Steel Floating
판정: **DEFER_WALL_MOUNTED_STEEL_CABINET_VS_WOOD_COUNTER**. 후보: 보류

PZ 형태: 1×1 벽걸이 은회색 스테인리스 직사각 상부 수납장. 전면 작은 금속문 2개와 하단 손잡이, 회색 평판 상단, 바닥 지지대 없음.

수동 비교: PZ는 금속 벽걸이 이중문 캐비닛인데 기존 mcwfurnitures:acacia_counter 렌더는 갈색 상판과 어두운 목재의 바닥형 카운터. 재질·문·벽면 부착 방식·높이 모두 불일치.

추가 검증: 벽걸이 금속 양문형 상부 수납장 모델 원본 및 wall-attachment/회전/1×1 설치 확인.

PZ SHA-256: `777e84e501852aaf8c91a8bf2d5dfcb5fc1fbcf1adc30563e564d9f57d874a4f`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `4d61a48bb43aa737f206ba2728f27470e6cfe4872e877b34c41b4758a6328f4c`


### 193 Jukebox / Oldies
판정: **CONDITIONAL_VINTAGE_JUKEBOX_TYPE_BUT_SILHOUETTE_AND_PALETTE_DIFFER**. 후보: decocraft:jukebox

PZ 형태: 1×1 아치형 어두운 회색 캐비닛, 전면 초록 패널과 적·황 테두리, 좁은 선택 패널과 검정 하부 스피커.

수동 비교: PZ 완성형과 Decocraft jukebox의 원본 BBMODEL을 Blockbench 5.2.2로 재렌더한 화면(50 cubes)을 직접 대조했다. 둘 다 빈티지 주크박스이고 아치형 상단·전면 장식·하단 캐비닛이 있지만, Minecraft는 민트·노랑·빨강 네온과 나무 측면, PZ는 회색 둥근 돔과 초록색 하단/검정 전면이다. 크기·음악 재생·1:1 외형은 미검증이므로 조건부만.

추가 검증: 새 원본 BBMODEL 재렌더 및 실제 블록 높이·음악 재생·색감 조정 가능 여부 검증.

PZ SHA-256: `16c66a7207d662388c6794d645e727dbe202175af3d448a74dfcee04ed8be4a3`
MC 모델 SHA-256: `23a7fd4be9ff8a00e9026f0ab869687a8d0a9e6f95789b990931ea63a498041d`
비교 이미지 SHA-256: `41e9e2953395f51110152350e478fd9793b837a7f5bdad8bdafca8fea584c7bb`


### 194 Chair / Modern White
판정: **DEFER_UPHOLSTERED_BOX_ARMCHAIR_VS_PARTIAL_WOODEN_CHAIR**. 후보: 보류

PZ 형태: 1×1 크림색 쿠션 팔걸이 의자. 넓고 두꺼운 좌우 팔걸이, 부드러운 등받이, 짙은 목재 짧은 네 다리.

수동 비교: PZ는 폭이 넓은 천 쿠션형 암체어인데 기존 pfm:oak_chair_classic_white 네이티브 캡처에는 두 나무 기둥과 분홍 가로막대만 보이며 쿠션·좌판·등받이·팔걸이 전체가 빠져 있다. 부분 모델은 대체 근거로 부적합.

추가 검증: Forge 1.20.1 cream upholstered box armchair의 완전한 모델 및 네 다리·팔걸이·쿠션 확인.

PZ SHA-256: `de5ff3ac8525e26b8574088061549a0e0e1eacfe989053fc226ee656970a8c51`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `a1afabdfbd0bd33e12cefab94c75e95ca80f247f5a7a71ec9715d34b35f0b340`


### 195 Counter / Motel
판정: **DEFER_DOUBLE_DOOR_MOTEL_CABINET_VS_FOUR_DRAWER_CABINET**. 후보: 보류

PZ 형태: 1×1 크림·아이보리색 낮은 수납 카운터. 평평한 밝은 베이지 상판, 전면 이중 여닫이문과 작은 둥근 황동색 손잡이 두 개.

수동 비교: 기존 mcwfurnitures:acacia_counter는 붉은 상판과 어두운 목재로 PZ 크림색 이중문 캐비닛과 다르다. 추가로 Decocraft bottom_cabinet_2_white의 실제 원본 BBMODEL 11 cubes를 Blockbench로 새로 렌더한 결과, 흰색 몸통과 밝은 상판은 비슷하나 전면에 수평 손잡이 달린 서랍 4개가 있고 PZ의 세로 여닫이문 2개·황동색 둥근 손잡이 2개가 없다. 따라서 추가 후보도 반려.

추가 검증: 문 2개와 작은 황동 손잡이 2개를 갖춘 1×1 크림색 base cabinet 실제 모델/텍스처 확인. 4서랍형으로 대체하지 말 것.

PZ SHA-256: `cfb4c0dca62e2adeb40ad4da121c6cc510a74badbb62e6bf2ec5718db944cdf5`
MC 모델 SHA-256: `630ffe7f31d8c5b84a5f112221f8e13d97084f820c76d7312c89a8daccc1e3f0`
비교 이미지 SHA-256: `5b27edba5ecea9d15ec7980d82577ae50018be610f9ee3432de07f816f6f6cef`


### 196 Shelves / Trapzoid Shop
판정: **DEFER_DOUBLE_OPEN_TRAPEZOID_BINS_VS_CLOSED_ACACIA_SHELF**. 후보: 보류

PZ 형태: 1×1 밝은 목재로 만든 2단 오픈형 판매 진열대. 위아래 사다리꼴 상자형 진열 바구니 2개, 기둥 지지대, 전면이 열린 구조.

수동 비교: PZ 원본은 두 개의 위로 열린 목재 진열 바구니인데 기존 handcrafted:acacia_shelf 네이티브 화면은 갈색 직육면체 측면에 검은 사각 개구부 두 개가 있는 캐비닛 형태. 진열 상자 깊이·측판·전면 구조가 불일치.

추가 검증: stacked wooden produce bins / two-tier trapezoid retail display 실제 원본 모델 검증.

PZ SHA-256: `893f5298793ea59228652b0a26c44fddd7cf2107541254cb908530dfde3d8451`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `28f65ab203df7720f37a841d72d169e937dc8b1d814e43bcfa8bff5244171369`


### 197 Contraption / Fitness
판정: **DEFER_WEIGHT_BENCH_WITH_BAR_SUPPORTS_NO_VERIFIED_COMPLETE_MATCH**. 후보: 보류

PZ 형태: 2타일 1×2 헬스용 벤치프레스 기구. 긴 검정 쿠션 평판, 은회색 지지 프레임, 뒤쪽 좌우 높은 수직 바벨 거치 기둥 2개.

수동 비교: PZ는 검정 쿠션 벤치에 높은 은회색 바벨 거치 기둥 2개가 달린 1×2 벤치프레스 기구다. Decocraft gym_bench 실제 원본 BBMODEL 7 cubes를 Blockbench 5.2.2로 새로 렌더했지만 화면에는 검은 좌판과 한쪽 지지대 일부만 보이고 바벨 거치대 2개가 확인되지 않는다. 원본 모델 전체가 캡처되었는지도 불확실하여 승인하지 않는다.

추가 검증: 1.20.1 Forge bench press with barbell stands 모델 또는 마인크래프트 스타일 신규 모델을 검증.

PZ SHA-256: `7300d29b842ce92b9bb26c1db15e4f651e0e5034f51a374b61197a9fda48a516`
MC 모델 SHA-256: `80de203fee5ce870e3934b0061a6fa0aff397748fc501a2131e2d913173ae632`
비교 이미지 SHA-256: `dc6593958682cc96f342b675cbb61e1f37f7427c1b3da8c0e268884f1d4755c8`


### 198 Stand / Pool Cue
판정: **DEFER_FLAT_WALL_CUE_PANEL_VS_FREESTANDING_BILLIARDS_RACK**. 후보: 보류

PZ 형태: 1×1 좁고 평평한 벽 부착형 진갈색 나무판, 금색 장식이 있는 윗틀과 아랫틀. 스프라이트에는 큐대·공이 보이지 않는다.

수동 비교: PZ 원본은 금색 장식이 있는 얇은 갈색 벽걸이 판자형 큐 스탠드지만 Decocraft pool_rack 실제 원본 BBMODEL 59 cubes의 재렌더는 바닥형 넓은 나무 랙과 여러 큐대·삼각대·컬러 볼 진열을 보여준다. 종류는 연관되어도 폭·깊이·벽 부착 여부·물체 수가 달라 기존 조건부 판정을 보류로 하향한다.

추가 검증: wall mounted pool cue holder flat wooden plaque model의 원본/설치 방향 확인, 필요 시 장식 판자 바닐라 조합.

PZ SHA-256: `21aa18f49e9778db810ade33b33272fb767afb4dc0b0a2e2addad6aee597a49e`
MC 모델 SHA-256: `3fcfbaa24ed79e07a2e524ace8112684cdd99c31b8ecabfe66de0a53e3229db5`
비교 이미지 SHA-256: `1564d232df1922a7b2511db2bd801216a6872e46acf05df0c33e55d88d4f9709`


### 199 Shelves / Large Rental
판정: **DEFER_LARGE_RENTAL_PANEL_VS_SMALL_ACACIA_SHELF**. 후보: 보류

PZ 형태: 2타일 1×2 길이의 연한 베이지색 높은 평판형 선반/가림판. 양끝 수직 측판과 긴 상단 선반이 보이며 전면은 넓고 닫힌 판면. 조립 상태는 잠정.

수동 비교: PZ 조립 미리보기에는 길고 높은 밝은 베이지색 판 구조가 보이는데 handcrafted:acacia_shelf 원본 렌더는 작은 짙은 적갈색 1블록 선반 캐비닛으로 색상·비율·길이·전면 구조가 다르다. PZ 뒷면이 보이는지 추가 시점 확인 필요.

추가 검증: 2타일 대여점 선반 완성형 전후면 시점 재조립 및 실제 2블록 목재 전시 선반 모델 비교.

PZ SHA-256: `0445a38eecb42c6ddc6ed5c54b82911fd2c21df0fddd4f4415dc94c1b4903666`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `d7e3ae501716989dfd27e737737a80813dd1225c04f22a7684adfc5e5ebfa0e6`


### 200 Bench / Sports
판정: **DEFER_WOODEN_SPORTS_BENCH_VS_BLACK_GYM_BENCH**. 후보: 보류

PZ 형태: 2타일 2×1 길이의 등받이 없는 목재 스포츠 벤치. 길고 밝은 갈색 나무 판자 좌판, 아래에 은회색 금속 다리 3개와 넓은 발판.

수동 비교: PZ는 2×1 길이의 밝은 목재 좌판과 은회색 금속 다리 3개가 있는 스포츠 벤치다. Decocraft gym_bench 실제 원본 BBMODEL 7 cubes 재렌더는 검은 운동기구 좌판과 한쪽 다리 일부만 보여 목재 재질·세 지지대·2블록 길이와 맞지 않는다. 197 헬스기구와 200 목재 벤치를 같은 Minecraft gym_bench로 자동 매칭한 오류를 확인했다.

추가 검증: 2블록 길이 3개의 회색 금속 다리 + 목재 평판 좌석을 가진 sports locker room bench 원본 모델 찾기.

PZ SHA-256: `beb0d916788a8f26073cd6df82012b6bc02a576ba323f318166e4ddd413bdff3`
MC 모델 SHA-256: `80de203fee5ce870e3934b0061a6fa0aff397748fc501a2131e2d913173ae632`
비교 이미지 SHA-256: `67db2fde4194abcc67002b57bbca7f018026d362a1168158321b04171f48efcd`


## 산출물

- cards/ : PZ 원본 완성형과 실제 소스 모델(또는 명시적 미검증 화면) 비교 JPG 10장

- BATCH_191_200_MANUAL_VISUAL_REVIEW.csv : 상세 수동 판정, 기존 자동 매칭의 오차, 모델 출처와 SHA

- BATCH_191_200_DEFERRED_OTHER_MODS.csv : 다른 모드·바닐라·신규 모델 후속 검토 목록

- BATCH_191_200_SHA256_PROVENANCE.csv : 원본 PZ/BBMODEL/텍스처/Blockbench 캡처/카드 해시

- MANIFEST.json / BATCH20_STANDALONE_PROGRESS.json : 독립 검수 범위·상태

- INDEX.html : 10개 비교판 탐색

- ROSEWOOD_BATCH_191_200_MANUAL_REVIEW.zip : 카드·CSV·README·인덱스 일괄 보관

원본 게임 TMX/PNG/SQLite와 기존 357종 누적 검수 CSV, 다른 레인 결과를 수정하지 않는다.
