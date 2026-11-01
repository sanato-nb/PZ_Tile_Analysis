# 로즈우드 357종 — 11차 101~110번 원본 가구 개별 시각 검수

101~110 원본 PZ 가구 10종을 독립 검토. Decocraft JAR 원본 BBMODEL/텍스처 26개 렌더 시도 중 26개 Blockbench 5.2.2 소스 이미지 성공. 실제 Minecraft 1.20.1 Forge 게임 설치/충돌/상호작용 테스트 및 1:1 최종 인증은 0건.

조건부 5건, 보류 5건. 12차 111~120 및 13차 121~130의 진행 CSV를 덮어쓰지 않기 위해 독립 JSON만 생성.

## 10종 검수 근거

### 101 Wardrobe / Fancy Oak
판정: DEFER_TWO_TILE_DARK_OAK_DOUBLE_WARDROBE_WITH_TWO_LOWER_DRAWERS / 제안: 보류

PZ 원본은 짙은 적갈색 양문 옷장과 아래 서랍 2단(각 금빛 원형 손잡이 2개)을 합친 1×2 가구다. 원본 Decocraft BBMODEL 렌더를 실제 확인하니 Closet 5 Ebony(8큐브)는 정면이 열린 등나무 바구니/선반 형태이며 옷장 문 자체가 없다. Closet 6 Oak(11큐브)는 좁은 단문 밝은 목재 옷장으로 하부 서랍이 전혀 없다. 기존 Macaw Dark Oak Double Wardrobe는 상단 상태 일부만 보였으므로 모두 반려한다.

후속 검증: 2×1 full wardrobe with two doors AND two bottom drawers in 1.20.1 Forge; verify original blockstate full multi-part, collision, direction.

PZ 이미지 SHA-256: `0a92f9f28be94ea705f9c7f685c6b7401af68b2525d4739ac16a331777b20be2`
MC 원본 모델 SHA-256: `5fe2b3e8746cafa6b5afa0e72bd8db7df20efb089b7ac45cf2739f82b275f0f5|59589a58ed55c7a95c34d397424be9d970a34235a4056666fdb31a15e7cd8cf2`

### 102 Cabinet / Grey File
판정: CONDITIONAL_THREE_DRAWER_FILE_CABINET_WHITE_VS_GRAY_METAL / 제안: decocraft:filing_cabinet_white

원본은 짙은 회색 철제 세로형 3단 파일 캐비닛이다. 기존 Refurbished 회색 주방 수납장은 전면 서랍이 없는 불완전한 상자여서 반려. Decocraft White Filing Cabinet의 실제 원본 렌더에서는 3개의 서랍, 라벨 틀, 가로 손잡이가 모두 보여 구조가 상당히 가깝지만 표면은 밝은 백색에 가까워 원본의 중간 회색 금속과 차이가 크다. 검정 변형도 회색이 아니므로 조건부다.

후속 검증: 회색 3단 파일 캐비닛 색상 variant 및 실제 1×1 배치/저장 기능 검증.

PZ 이미지 SHA-256: `964b15a6ca3beeb4f47bc080271656ad830a18d399629950624cfa332ac3b312`
MC 원본 모델 SHA-256: `d01d8ea34d3cc1173560526264e6582e483c46f75b1248f41df9d1b097895533|d01d8ea34d3cc1173560526264e6582e483c46f75b1248f41df9d1b097895533`

### 103 Counter / Shop Display
판정: DEFER_PALE_WOOD_OPEN_TOP_SHOP_DISPLAY_COUNTER / 제안: 보류

PZ 원본은 밝은 베이지 목재의 1칸 진열대로 윗면에 두꺼운 사각 목재 테두리와 안쪽으로 파인 연회색 진열 공간이 있고 앞·옆면에는 서랍이나 문이 없다. 실제 렌더한 Decocraft Display Counter Bottom Oak(6큐브)는 베이지 목재 몸체는 비슷하지만 상판이 회색 금속/석재의 완전히 평평한 뚜껑으로 덮여 있으며 테두리 안쪽 오목한 공간이 없다. White 변형은 몸체까지 백색이다. 기존 Macaw Acacia Counter의 붉은 상판/검은 몸체도 부적합하므로 보류.

후속 검증: Forge 1.20.1 single-block wood grocery bin with inset display tray and no glass showcase; confirm model geometry/texture and in-game surface.

PZ 이미지 SHA-256: `0ca8a9140ec6e434e6eb452e73905ce87a9f7d0d6bc7a02aeff8a975b64a348b`
MC 원본 모델 SHA-256: `1bb5bba0b5b6768f76bbe2fcd51a0010ecd38d70c0f244682ebd88c92edfe2fa|1bb5bba0b5b6768f76bbe2fcd51a0010ecd38d70c0f244682ebd88c92edfe2fa`

### 104 Couch / Brown Lazy
판정: CONDITIONAL_BROWN_LEATHER_TWO_SEAT_SOFA_TWO_MODULE_ASSEMBLY / 제안: decocraft:couch_left_leather_brown

PZ 원본은 짙은 붉은 갈색 가죽의 2인용 소파로 양끝 둥근 팔걸이, 두 좌석 쿠션, 분할된 부드러운 등받이가 있다. 실제 Decocraft Couch Left Leather Brown(6큐브)과 Right Leather Brown(6큐브)은 갈색 가죽 질감과 좌우 각 1개 팔걸이를 가진 별개 모듈이므로 두 개를 붙이면 기본 소파 유형이 맞는다. 그러나 모델은 PZ보다 밝은 주황 갈색, 팔걸이와 등받이가 각진 평판이며 2×1 완성 연결/중간 경계는 게임에서 확인하지 않았다. 기존 Macaw Brown Couch는 한쪽 모듈만 렌더돼 완성형을 재현하지 못했다.

후속 검증: Place left and right leather brown couch modules together in Forge 1.20.1 and capture 2×1 finished view; inspect seams/armrest placement/collision.

PZ 이미지 SHA-256: `d3fe5aed3b66d9e1e619aabacfe8c18bccbfabf0a11a0afc77af382683377e26`
MC 원본 모델 SHA-256: `0e36aa9871bc061aa4e7683e7ec69cbb080226280259d47c14f684f23d7b31cc|9681b0789bf07ad97494ac57e0e48e955dd0bb8076db55fb7ab6a5006f3d2fa5`

### 105 Table / Large Plastic
판정: DEFER_TWO_TILE_WHITE_PLASTIC_FOLDING_BANQUET_TABLE / 제안: 보류

PZ 원본은 2×1 흰색 플라스틱 접이식 긴 테이블로 중앙 상판 접합선과 어두운 금속 U자형 다리 2쌍/가로 보강대가 보인다. 기존 Decocraft table_setting_double은 접시와 컵만 렌더돼 테이블이 아니다. 새 Wooden Table White(25큐브)는 흰 목재의 굵고 장식된 다리 4개를 가진 일반 식탁이며, Diner Table Light Gray(12큐브)는 회색 판 아래 중앙 금속 기둥 1개가 있는 카페 테이블이다. 모두 원본의 접이식 다리 구조와 2칸 긴 상판을 재현하지 못해 보류한다.

후속 검증: Search source-backed 1.20.1 Forge 2×1 folding plastic banquet table with tubular metal legs; test actual placement and multi-block.

PZ 이미지 SHA-256: `6f50efe462316dfa297691c017be2123ff37ddfe1b1ed8e6b7f02de8bf938366`
MC 원본 모델 SHA-256: `f156fc905a8529b6e536456ba7b7e362b8d55316b90f98c652e040698b999242|9be049c262802b52e979df0933aa4b93fee3a6d3bdad79d4060c747a80ce75ce`

### 106 Public Garbage Bin / 
판정: DEFER_CYLINDRICAL_PUBLIC_LITTER_BIN_SLATTED_DOME / 제안: 보류

PZ 원본은 검은 철제 원통형 공공 쓰레기통으로 세로 철살 몸통과 방사형으로 벌어진 상단 테두리, 중앙의 열린 원형 투입구가 특징이다. Decocraft Trash Can(59큐브)은 녹슨 은회색 아연도금 원통에 손잡이 달린 닫힌 평평한 뚜껑이 있다. Trash Can Open(60큐브)은 뚜껑이 옆으로 젖혀지고 검은 쓰레기봉투가 드러나며, 어느 쪽도 PZ의 방사형 원형 투입구가 아니다. 기존 Paladin Mesh Trashcan은 사각형 그물망과 초록색 윗면으로 완전히 달라 반려한다.

후속 검증: Check 1.20.1 Forge Trashcans Forever!/Simple Trashcan original model for dark cylindrical slatted outdoor bin; source render before approval.

PZ 이미지 SHA-256: `803c8473a74f0a5501de44d46ed5f9e87568b42f943e61d7d77b237e7eae555b`
MC 원본 모델 SHA-256: `35f3e7c84f53ca7e0efce023c87c2924c7d11f00c58ca589d3af8025007ab845|ffea402b1a3ee021be6975fdc7d777c6dd0678d73268c7dd529fe10f0bf9052e`

### 107 Chair / Brown Lazy
판정: CONDITIONAL_BROWN_LEATHER_UPHOLSTERED_ARMCHAIR / 제안: decocraft:armchair_leather_brown

PZ 원본은 104번과 같은 짙은 붉은 갈색 가죽의 1인용 안락의자로 둥근 높은 등받이와 두꺼운 양쪽 팔걸이, 넓은 좌석 쿠션이 있다. Decocraft Armchair Leather Brown의 원본 9큐브 모델을 실제 렌더했으며 두 팔걸이, 좌석, 등받이, 아래 가죽 받침이 모두 완전하게 나타나 의자 유형이 맞는다. 하지만 마크 모델은 더 밝은 주황 갈색이고 각진 직선 등받이/팔걸이로 원본의 둥근 쿠션형 실루엣과 다르다. Cottage Armchair는 꽃무늬 천이라 재질·색 모두 불일치한다.

후속 검증: Verify Decocraft leather armchair front and back, sitting behavior, 1×1 placement, color matching PZ 104 sofa.

PZ 이미지 SHA-256: `9beb18cc92fbddb10ea61ec5b9093b8a2aaa18f5efb22a15c693c9c73e0e0c18`
MC 원본 모델 SHA-256: `fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|34b37379ca11b74db0546d02ca155f7b8047ded9c95debb49e08a1a55380674c`

### 108 Microwave / White
판정: CONDITIONAL_LIGHT_COLORED_COUNTERTOP_MICROWAVE / 제안: decocraft:microwave

PZ 원본은 크림색/백색 소형 전자레인지로 왼쪽 어두운 전면 창, 오른쪽 세로 조작부가 있다. 새 Decocraft Microwave(14큐브) 원본 BBMODEL을 Blockbench로 확인하니 본체·검정 유리문·오른쪽 버튼 격자·아래 다이얼까지 완전하게 나타난다. 이전 Refurbished Dark Microwave의 녹색 기둥 하나짜리 부분 렌더보다 확실히 낫다. 다만 새 모델 몸체는 회색 금속이고 전면 버튼·다이얼이 PZ와 달라 색상/세부 외형은 조건부로 남긴다.

후속 검증: Check source Decocraft microwave body color and controls; alternatively source-render refurbished_furniture:light_microwave, test on-counter placement and heating.

PZ 이미지 SHA-256: `cacc3626102318b1ba2c6175a41140c968939b1b483705127fc89b677e178a9e`
MC 원본 모델 SHA-256: `a207a21d0647df819cbe66721f3a754d2d79b927d66e462ab8d735585075f198`

### 109 Piano / Western
판정: CONDITIONAL_TWO_TILE_WESTERN_UPRIGHT_PIANO / 제안: decocraft:piano_upright_spruce

PZ 원본은 2×1 적갈색 서부풍 업라이트 피아노로 검은색/흰색 건반과 아래 금빛 페달 3개, 둥근 옆판이 있다. 실제 Decocraft Piano Upright Spruce(56큐브)는 가로로 긴 업라이트 목재 본체, 검은/흰 건반, 3개 금빛 페달이 전부 갖춰져 외형이 상당히 유사하다. 하지만 PZ보다 밝은 갈색이며 큰 흰 악보판, 직선적 사각 프레임과 하단 다리가 달라 조건부다. 별도 렌더한 Piano Spruce(245큐브)는 뚜껑을 연 그랜드 피아노이므로 구조상 대체할 수 없다.

후속 검증: Minecraft piano upright spruce exact 2×1 placement, musical interaction and key/pedal positions; compare piano_spruce alternative.

PZ 이미지 SHA-256: `da2438d1783e65a26f5628584cab51c13d8fdc9ef05055a525cfeee8c6dfb6be`
MC 원본 모델 SHA-256: `3ee7245d484bdbcc2676bec440836fc24475031441cf77f5735953f3560426d2|4a979f163839957ef56de1a37b2fb0ff09801370121a8a4a6ad14b01ede3aeca`

### 110 Shelves / Hardwood Wall
판정: DEFER_TWO_DARK_WOOD_FLOATING_WALL_SHELVES / 제안: 보류

원본은 진갈색 목재 판자 2개가 벽에 간격을 두고 수평으로 붙은 단순 벽 선반이다. 기존 Handcrafted Acacia Shelf 렌더는 양옆 벽과 뒷판이 있는 두꺼운 책장형 상자여서 구조가 다르다. 현재 확인된 원본 모델 목록에서 같은 높이의 독립된 판자 2개를 한 블록 안에 배치하는 완성형 가구를 찾지 못했다. 마크 다크오크 덫문 2개를 벽에 펼쳐 만드는 방법은 바닐라 재현안일 뿐 실제 한 칸 배치는 미검증이다.

후속 검증: Aesthetic Shelving/Furnish/Wall Shelf Forge 1.20.1 source model for two floating planks; verify 1×1 wall mount and double-shelf height.

PZ 이미지 SHA-256: `2297cf7fc940096718c22cb1b346f4312080e9ba65557f0712e5c8b149f3052f`
MC 원본 모델 SHA-256: `해당 없음`

## 출처·검증 범위

- PZ: 기존 B42 원본 Tiles PNG 및 TMX/.tiles 기반 조립 미리보기 (시각 조립은 잠정이며 인게임 모델이 아님)

- Minecraft: 검증된 Decocraft Forge 1.20.1 JAR에서 BBMODEL과 선택 텍스처를 읽어 원본 해시를 기록하고 Blockbench 5.2.2 데스크톱 화면 캡처

- 원본 모드 JAR, 텍스처 및 BBMODEL 자체는 재배포하지 않음. 비교 이미지·해시·출처만 보관.

- 실제 마인크래프트 설치 시 방향, 크기, 멀티블록, 충돌/상호작용은 별도 테스트 전까지 승인하지 않음.

## 파일

- cards/ : 101~110 원본 PZ 대 Minecraft 원본 모델 비교 10장

- BATCH_101_110_MANUAL_VISUAL_REVIEW.csv : 상세 10종 및 SHA-256

- BATCH_101_110_DEFERRED_OTHER_MODS.csv : 보류 후속 목록

- BATCH11_STANDALONE_PROGRESS.json : 병렬 작업 충돌 방지 독립 진행 상태

- INDEX.html : 비교 이미지 열람기

- MANIFEST.json : 범위 및 검증 수치

- ROSEWOOD_BATCH_101_110_MANUAL_REVIEW.zip : 전체 결과
