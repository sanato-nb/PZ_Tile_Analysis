# 로즈우드 가구 22차 221~230번 개별 시각 검수

PZ B42 원본 완성형 미리보기 10장과 이전 Minecraft 원본 Blockbench 비교판 10장을 실제로 육안 검수했다. 별도 GitHub Actions는 Decocraft 3.0.4-1.20.1 Forge 원본 BBMODEL/텍스처를 검증한 뒤 Blockbench 5.2.2로 새로 렌더해 추가 대조한다.

이전 A 레인 131~140, 161~170 및 191~200번은 별도 Draft PR로 보존했으며, 이번 221~230번만 독립 검수했다. 다른 레인과 원본 파일은 건드리지 않았다.

원본 Decocraft JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05 | https://modrinth.com/mod/decocraft/version/K6V6djNF

검수 10종: 조건부 1종, 보류 9종. 네이티브 Blockbench 캡처 10/10개 모델. 비교 JPG 10장. 인게임 1:1 확정 0종.

일부 원본 스프라이트의 SpriteGridPos 조립과 마크 모델의 동적 블록 상태는 잠정이다. 1×1/2×1/1×2 점유·방향·충돌·상호작용·색상/재질은 인게임 미검증. 부분 모델 캡처는 완성형으로 승인하지 않는다.

## 개별 근거

### 221 Chair / Purple Rattan
판정: **DEFER_WICKER_ARMCHAIR_VS_PURPLE_STRIPED_DECK_CHAIR**. 후보: 보류

PZ 형태: 짙은 갈색 라탄으로 감싼 낮은 사각 1인 의자. 두꺼운 둥근 팔걸이와 분홍색 쿠션/등받이, 네 개의 짧은 다리.

수동 비교: PZ는 낮고 둥근 갈색 라탄 팔걸이·분홍 쿠션의 실내 암체어다. 기존 pfm:oak_chair_classic_purple Blockbench 캡처는 기둥 2개와 청록 가로대만 있는 불완전 모델이었다. 새로 Decocraft beach_chair_purple 원본 BBMODEL 18 cubes를 공식 Blockbench 5.2.2에서 렌더하니 보라·흰색 줄무늬 천이 늘어진 긴 야외 접이식 덱체어, 가느다란 밝은 목재 경사 프레임으로 확인됐다. 등나무 양팔걸이·두꺼운 분홍 쿠션·낮은 사각 몸체가 없어 보류.

추가 검증: 라탄 감김 1인 소파 원본 모델, 분홍 쿠션/팔걸이 및 1×1 점유·앉기 동작 검증.

PZ SHA-256: `ba566ec63036842f18b6ac2553471172eb8b37a2f3c097be5b4f403f58269523`
MC 모델 SHA-256: `ef7759d3dd1b64eadd7507536995553eaac771f210224316e807169f7c24e17e`
비교 이미지 SHA-256: `89f565d14b5d68ec0a8be3efffd3817260b19b9c066317a47604fdf108a1b780`


### 222 Chair / Red Comfy
판정: **DEFER_RED_PADDED_ARMCHAIR_VS_RED_STRIPED_DECK_CHAIR**. 후보: 보류

PZ 형태: 빨강~주황색 패브릭 통쿠션 1인 암체어. 두꺼운 좌판과 양팔걸이, 분리된 낮은 등받이 쿠션, 짧은 검정 발.

수동 비교: PZ는 두꺼운 적색 통쿠션과 양팔걸이, 낮은 네 발이 있는 실내 암체어다. 기존 pfm:oak_chair_classic_red는 불완전 기둥 2개/가로대만 보였다. 새 Decocraft beach_chair_red 원본 BBMODEL 18 cubes를 Blockbench 5.2.2에서 렌더하니 빨강·흰색 줄무늬 천과 가는 나무 경사 프레임을 가진 접이식 야외 덱체어였다. 패딩·양팔걸이·사각 실내 암체어 구조가 모두 다르다.

추가 검증: 적색 두꺼운 양팔걸이 소파형 의자, 전체 모델 텍스처 및 앉기 기능 검증.

PZ SHA-256: `85cd3d0b0a0c2e5f50936dcd534098f7d5c459a7d13ab33b1e65d72ef518b414`
MC 모델 SHA-256: `ef7759d3dd1b64eadd7507536995553eaac771f210224316e807169f7c24e17e`
비교 이미지 SHA-256: `6b4b182342d887beca9eba84f09b519f11575178ed9310531d003813defdd534`


### 223 Couch / Purple Rattan
판정: **DEFER_PINK_RATTAN_TWO_SEATER_VS_SOLID_PURPLE_CORNER**. 후보: 보류

PZ 형태: 2×1 라탄 갈색 프레임의 2인 소파. 양끝 둥근 등나무 팔걸이, 분홍색 좌석 쿠션 두 개와 긴 등받이 쿠션.

수동 비교: PZ는 2×1 갈색 라탄 양팔걸이와 연분홍 좌석 2개/등받이를 가진 완성형 소파다. 기존 Macaw purple_couch 실제 Blockbench는 보라색 한쪽 조각으로 라탄·분홍 쿠션이 없다. 새 Decocraft couch_corner_purple BBMODEL 7 cubes를 Blockbench 5.2.2로 렌더하니 선명한 보라색의 두꺼운 코너/한 좌석 모듈일 뿐 라탄 골조와 연분홍 패브릭이 없고 2×1 완제품 결합도 미검증. 보류.

추가 검증: 갈색 등나무 2인 소파 + 분홍색 패브릭 2좌석, 2×1 조립·회전·충돌 검증.

PZ SHA-256: `a1b9a157a693fb6384806ffe806f6be19cdcef88809e56a750508533098c9c34`
MC 모델 SHA-256: `2d353c50b87de0fae4a25a97177f53e1c7f851e2044ffdbd35125802bdf71656`
비교 이미지 SHA-256: `d66c8b754129e7b158139a165e9bcb6aec85115a87eb59d90f8d1f4caecbf6ee`


### 224 Couch / Yellow Modern
판정: **DEFER_YELLOW_MODERN_TWO_SEATER_VS_GREEN_FLORAL_BAMBOO_SINGLE**. 후보: 보류

PZ 형태: 1×2의 노란색 직사각형 현대식 2인 소파. 낮고 곧은 등받이, 평평한 두 자리 좌판, 두꺼운 양팔걸이, 낮은 검정 다리.

수동 비교: PZ는 단색 황토 노란 1×2 현대식 직선 2인 소파다. 기존 Macaw yellow_couch 렌더는 단일 좌석/팔걸이 조각으로 2인 결합 미검증. 새 Decocraft bamboo_couch_left_yellow 원본 BBMODEL 34 cubes를 Blockbench 5.2.2로 렌더하니 녹색 대나무 개방형 프레임에 흰색·분홍 꽃무늬 쿠션과 분홍 등받이가 있는 단일 좌석 모듈이었다. PZ의 단색 노랑 두꺼운 프레임·낮은 직선 등받이와 색·재질·폭·형태가 다르다.

추가 검증: 노란 2인 소파의 좌·우 모델 결합, 1×2 점유와 방향, 낮은 발과 좌석 사용 검증.

PZ SHA-256: `13a36bb0b32c8b71bb00b51dbfb615bd94466f6963ed1c8e29a651bcb79bd78a`
MC 모델 SHA-256: `5d1cd8cdb2beb233ba77374f71b48e1d8c73d2af27ac2bad8bfec70b2022cc63`
비교 이미지 SHA-256: `36dbe51963d68ff5c81e8891b67ad1537366e5212ac6cf2d074bf102161fca89`


### 225 Counter / Green Corner
판정: **DEFER_SOLID_OLIVE_L_CORNER_VS_GREEN_STRIPED_DINER**. 후보: 보류

PZ 형태: 1×1 무광 올리브색 단색 목재 L자 코너 카운터. 평평한 넓은 상판과 안쪽 직각 홈, 수직 측면 패널.

수동 비교: PZ는 무광 올리브 단색 목재의 안쪽 직각 홈이 있는 L자 코너 카운터다. Decocraft diner_counter_corner_green 실제 BBMODEL 11 cubes를 Blockbench 5.2.2에서 재검증한 결과 채도 높은 녹색/흰색·은색의 수평 줄무늬와 검은 하부, 각진 다이너형 전면이었다. PZ의 단색 무장식 올리브 패널과 재질·색·코너 형상·인접 연결 구조가 다르다.

추가 검증: 올리브색 목재 코너 상판과 좌우 인접 카운터 연결, 1×1 회전·충돌 검증.

PZ SHA-256: `4e969e07f1d0004687fd99d09778560a7cd0e842e78180a2dd65dd0aae07d66d`
MC 모델 SHA-256: `25ef3b784df0de583daad5bbf2d506ceeeadb62db760d80521b8cff7860de13a`
비교 이미지 SHA-256: `b8684737a72cadea429a808b8758d586b7374e56e3957c0414fcc2b843ff9b91`


### 226 Counter / Hardwood Floating
판정: **DEFER_DARK_FLOATING_TWO_DOOR_VS_LIGHT_OAK_FOUR_DRAWER**. 후보: 보류

PZ 형태: 짙은 갈색 원목의 벽걸이형 사각 수납장. 두 개의 세로 패널문과 작은 원형 손잡이, 평평한 상판, 바닥 받침 다리 없음.

수동 비교: PZ는 짙은 갈색 벽걸이 2문 수납장, 전면 세로 판문 2개와 작은 손잡이, 다리 없는 상자형이다. 기존 mcwfurnitures:acacia_counter는 주황 상판/회색 돌 몸체의 높은 카운터로 오매칭이다. 새 Decocraft bottom_cabinet_2_oak 원본 BBMODEL 11 cubes를 Blockbench 5.2.2로 렌더하니 흰 상판·밝은 참나무 몸체에 검은 손잡이가 달린 가로 서랍 4개가 있는 바닥형 서랍장이었다. 문 개수·방향·높이·벽부착·재질이 모두 다르다.

추가 검증: 벽면 부착 2문 진갈색 원목 수납장, 문 열림·부착면·회전·충돌 검증.

PZ SHA-256: `ec4fda86bdbb04263be7a5f65b6f6cbd5187a2ede6af2a26a3063e2d67165992`
MC 모델 SHA-256: `630ffe7f31d8c5b84a5f112221f8e13d97084f820c76d7312c89a8daccc1e3f0`
비교 이미지 SHA-256: `120ad151c7a5b33d594e0a3aa23d49ec21e20c293c23a90eb8fa384a22dc2f29`


### 227 Shelves / White Wall
판정: **DEFER_THIN_WHITE_WALL_SHELF_VS_FULL_DISH_RACK**. 후보: 보류

PZ 형태: 1×1 길이의 매우 얇은 흰색/연회색 벽부착형 단일 선반판. 문·그릇·지지 다리 없음.

수동 비교: PZ는 벽에 부착하는 얇고 긴 흰색/연회색 단일 선반판이다. Decocraft dish_rack_white 원본 BBMODEL 686 cubes를 Blockbench 5.2.2에서 렌더하니 갈색 나무 등판, 접시/컵과 걸린 수건·유리잔이 포함된 완성형 식기 거치대였다. PZ의 무장식 단일 판재와 두께·색상·부속품·벽면 배치가 다르므로 보류.

추가 검증: 얇은 흰색 플로팅 선반 모델, 벽 고정·회전·아이템 놓기 기능 확인.

PZ SHA-256: `823454d734c2baf9d876814decfe656a22ffd279ba969d7d5ab3a3f97354ec7d`
MC 모델 SHA-256: `4914f18647bc78e9d91d4bb906d94773fd28bcb49d65e8f9f30509cd4fa8ef9f`
비교 이미지 SHA-256: `239bac31ede62a29f494f525975cfe93618b3dc61a90489d13e76a935fca1aba`


### 228 Table / Black Low Modern
판정: **DEFER_SOLID_LOW_BLACK_BLOCK_VS_TALL_METAL_PEDESTAL**. 후보: 보류

PZ 형태: 검정색의 낮고 두꺼운 직육면체 커피 테이블/단단한 받침. 다리와 장식 없는 상판·측면, 바닥과 거의 붙은 높이.

수동 비교: PZ는 다리 없는 낮은 검정 직육면체의 통짜 커피 테이블/받침이다. Decocraft diner_table_black 원본 BBMODEL 12 cubes를 Blockbench 5.2.2에서 재렌더하니 검정 얇은 상판에 밝은 금속 테두리, 긴 중앙 금속 기둥과 넓은 바닥판이 있는 높은 식탁이었다. 높이·기둥·금속 비율·외곽 실루엣이 명백히 다르다.

추가 검증: 낮은 검정 1×1 일체형 커피 테이블, 실제 블록 높이와 상판/충돌 검증.

PZ SHA-256: `03455accae1a07a34425a7106280e53b2d9a00cdcd2ed999453e36f106663fb7`
MC 모델 SHA-256: `9be049c262802b52e979df0933aa4b93fee3a6d3bdad79d4060c747a80ce75ce`
비교 이미지 SHA-256: `d90f21bd93155488d677699a351542e2465af2e57e04cacd4438c01aba363efd`


### 229 Beds / Twin
판정: **CONDITIONAL_BUNK_STRUCTURE_LADDER_SIMILAR_BUT_FRAME_COLOR_AND_BEDDING_DIFFER**. 후보: decocraft:bunk_bed_birch_black

PZ 형태: 2개 PZ 스프라이트로 조립된 붉은 목재 2층 침대. 흰색 상하 매트리스, 빨간 사다리와 긴 수평 난간, 네 기둥.

수동 비교: PZ 2×1 조립은 빨간 목재 2층 침대, 흰색 상하 매트리스, 빨간 측면 사다리/난간이다. Decocraft bunk_bed_birch_black 원본 BBMODEL 66 cubes를 Blockbench 5.2.2에서 재렌더해 두 층, 4개 기둥, 측면 사다리와 난간이라는 기본 구조가 유사함을 확인했다. 그러나 밝은 자작나무 프레임과 검정/회색 침구, 촘촘한 세로 난간·사다리 위치는 PZ의 붉은 단순 수평 난간·흰 매트리스와 다르다. 구조적 대안으로만 조건부 보관하고 1:1 승인·설치 인증은 하지 않는다.

추가 검증: 빨간 나무 프레임 텍스처 대안, 2×1 조립/침대 사용·충돌·층별 상호작용 확인.

PZ SHA-256: `afc688754c67f6de8824643295872c3d02d5d62dc09dd0fab0bdcb7dc6086ee5`
MC 모델 SHA-256: `26924a701635c145444a22a18d27ac74b37d8363ecb41a0bb5ad8f301743c886`
비교 이미지 SHA-256: `680e0d6b0aeaef51306cf4bc36fbe198d6dbaaefc561264745e7a5b043c0943f`


### 230 Chair / Darkblue Modern
판정: **DEFER_NAVY_PADDED_CHAIR_VS_BLUE_METAL_SCHOOL_CHAIR**. 후보: 보류

PZ 형태: 짙은 남색 천으로 감싼 높은 둥근 등받이와 두툼한 좌판, 팔걸이 없는 검은 가느다란 4다리 식탁 의자.

수동 비교: PZ는 짙은 남색 천 쿠션의 둥근 높은 등받이와 두툼한 좌판, 가느다란 검정 4다리 의자다. 기존 Macaw acacia_modern_chair Blockbench 캡처는 수직 기둥 하나만 보여 불완전했다. 새 Decocraft school_chair_blue 원본 BBMODEL 37 cubes를 Blockbench 5.2.2로 렌더하니 밝은 파란 평판 좌석과 분리된 직사각 등받이, 은색 금속 4다리의 교실 의자였다. 패딩·둥근 등받이·남색 천·검정 다리와 모두 다르다.

추가 검증: 짙은 남색 패브릭 좌판·등받이와 검정 4다리, 1×1 배치 및 앉기 검증.

PZ SHA-256: `b7ecf327a4954da1437f2f06dcf46936ee0be8bb294a4a47d8eb13d2311cbae8`
MC 모델 SHA-256: `10b356207b2641cf3b2ffeb46973e647c94631c85ddad80d392240464139e2d1`
비교 이미지 SHA-256: `0588c871a91c79b422a3f346e453af36b2d47da499ff455a3f2f54a6fbf81a71`


## 산출물

- cards/ : PZ 원본 완성형과 실제 소스 모델(또는 명시적 미검증 화면) 비교 JPG 10장

- BATCH_221_230_MANUAL_VISUAL_REVIEW.csv : 상세 수동 판정, 기존 자동 매칭의 오차, 모델 출처와 SHA

- BATCH_221_230_DEFERRED_OTHER_MODS.csv : 다른 모드·바닐라·신규 모델 후속 검토 목록

- BATCH_221_230_SHA256_PROVENANCE.csv : 원본 PZ/BBMODEL/텍스처/Blockbench 캡처/카드 해시

- MANIFEST.json / BATCH22_STANDALONE_PROGRESS.json : 독립 검수 범위·상태

- INDEX.html : 10개 비교판 탐색

- ROSEWOOD_BATCH_221_230_MANUAL_REVIEW.zip : 카드·CSV·README·인덱스 일괄 보관

원본 게임 TMX/PNG/SQLite와 기존 357종 누적 검수 CSV, 다른 레인 결과를 수정하지 않는다.
