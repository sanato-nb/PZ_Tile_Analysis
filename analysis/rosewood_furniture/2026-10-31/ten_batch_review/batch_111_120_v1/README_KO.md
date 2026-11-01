# 로즈우드 357종 — 12차 111~120번 원본 가구 개별 시각 검수

111~120 원본 PZ 가구 10종을 독립 검토. Decocraft JAR 원본 BBMODEL/텍스처 33개 렌더 시도 중 33개 Blockbench 5.2.2 소스 이미지 성공. 실제 Minecraft 1.20.1 Forge 게임 설치/충돌/상호작용 테스트 및 1:1 최종 인증은 0건.

조건부 2건, 보류 8건. 11차 101~110 및 13차 121~130의 진행 CSV를 덮어쓰지 않기 위해 독립 JSON만 생성.

외부 모드 공식 호환성 자료 8건은 별도 CSV에 보존하며, 해당 모델의 3D 렌더·외형 검증이 완료된 것으로 간주하지 않음.

## 10종 검수 근거

### 111 Bed / Large Fancy
판정: CONDITIONAL_BLACK_SLATTED_DOUBLE_BED_WHITE_CHECKER_BEDDING_MISMATCH / 제안: decocraft:double_bed_black_white

원본 PZ는 검정 세로살 머리판·발판과 흰색 단색 매트리스가 핵심이다. 기존 Birch Black은 밝은 원목 프레임에 검정 체크 침구라 색 배합이 반대다. Decocraft Double Bed Black White는 검정 프레임과 흰 침구라는 방향은 맞지만 회백색 체크무늬와 커다란 흰 베개/접힌 이불이 두드러져 원본의 평평한 단색 침구와 다르다. 2×2 설치·수면 기능은 인증하지 않는다.

후속 검증: MultiBeds 1.20.1 Forge의 검정 세로살 프레임/단색 크림 침구 조합 및 실제 2×2 점유·방향·충돌 테스트.

PZ 이미지 SHA-256: `8ceee67480df9a47e0311af14b963726ccad23bf81d0ae8c63cab65f8894c9bc`
MC 원본 모델 SHA-256: `386e358e9cf72ead5f9e5f916b9b3f4dc9387b68aec75cba29f3a5ba8c058b13|386e358e9cf72ead5f9e5f916b9b3f4dc9387b68aec75cba29f3a5ba8c058b13`

### 112 Fridge / Mini
판정: DEFER_PLAIN_MATTE_BLACK_MINI_FRIDGE_FORM / 제안: 보류

PZ 원본은 손잡이와 도어 분할선이 거의 보이지 않는 검정 무광 직육면체 미니 냉장고다. 기존 Refurbished Dark Fridge는 부분 모델 가져오기에서 분홍 측면/검정 전면으로 잘못 보였다. 이번 Decocraft Fridge Small Black 원본 293큐브를 Blockbench 5.2.2로 직접 렌더하니 위아래 2개 문, 은색 손잡이 2개, 상단 통풍구가 있는 높고 큰 가정용 냉장고였다. PZ의 짧고 단순한 검정 미니 냉장고와 문 수·높이·외관이 달라 보류한다.

후속 검증: 작은 검정 단문 미니냉장고, 높이/도어 손잡이/실제 1×1 설치 및 냉장고 저장 기능 검증.

PZ 이미지 SHA-256: `eaadf81a849ce553d6d1aee76a10e50f12dcd7fc1d857cfa85f0dd7f6c0aecb5`
MC 원본 모델 SHA-256: `c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48|c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48`

### 113 Bin / Washing
판정: DEFER_YELLOW_CANVAS_LAUNDRY_BIN_SQUARE_METAL_FRAME / 제안: 보류

PZ 원본은 노란 천 자루를 회색 금속 사각 프레임에 걸어 둔 세탁물 수거함이다. 이번 Decocraft Laundry Basket Rattan의 실제 20큐브 렌더는 갈색 등나무 뚜껑이 달린 사각 바구니로 천과 금속 프레임이 없다. Rolling Bin Yellow의 실제 41큐브 렌더는 검정 뚜껑·바퀴 달린 노란 플라스틱 쓰레기통이다. 둘 다 원본의 구조/소재가 달라 보류한다.

후속 검증: 1.20.1 Forge에서 노란 천과 노출 금속 사각 프레임이 결합된 laundry cart / canvas hamper 탐색, 실제 블록 렌더링.

PZ 이미지 SHA-256: `dd49e3aff7ebfdda2299fa7a02db5872353236ea517f6fb428ec5972c6bc44e5`
MC 원본 모델 SHA-256: `80c24c903f08088a5292b3353834f914d089f151cdbc889d26f1511a830ee998|991e8fad6bc5ae8dca6f5198a28d1d85a4a4346cec43507086791d3b3dfb0eb0`

### 114 Box / Cartboard
판정: DEFER_TAPED_SMALL_CARDBOARD_CARTON_EXTERNAL_MOD_SOURCE_PENDING / 제안: 보류

원본은 위쪽을 갈색 테이프로 봉한 작은 종이 골판지 택배 상자다. 기존 Refurbished Acacia Mail Box는 길고 높은 우편함이라 전혀 맞지 않는다. 기존 5개 모드의 실제 등록 블록에서는 같은 카드보드 상자를 찾지 못했다. 공식 Forge 1.20.1을 지원하는 CardboardBox 및 Cardboard Boxes 모드를 추가 발견했지만 해당 JAR의 3D 모델을 아직 렌더링하지 않아 후보 확정은 보류한다.

후속 검증: CardboardBox 1.0.2/ Cardboard Boxes 1.0.0 Forge JAR에서 실제 블록 ID, 텍스처, 봉합 테이프, 높이, 보관 기능을 추출·렌더링해 비교.

PZ 이미지 SHA-256: `742866cf98fed4f5951fceff4beaac18af835aa7845085c23cbc9fe151b967f7`
MC 원본 모델 SHA-256: `해당 없음`

### 115 Drawers / Dark Fancy
판정: CONDITIONAL_BLACK_TWO_DRAWER_MODULAR_DESK_DRAWERS_ORNATE_LEGS_MISMATCH / 제안: decocraft:modular_desk_drawers_black

PZ 원본은 검정 무광 단순 2단 서랍장으로 위아래 서랍에 짧은 은색 가로 손잡이가 하나씩 달린다. 기존 Macaw Acacia Bookshelf Drawer는 선반의 초록 판만 표시되어 반려한다. 이번 Decocraft Modular Desk Drawers Black의 실제 50큐브 Blockbench 모델은 검정 목재, 서랍 2개, 은색 손잡이 2개가 확인되어 구조·색상에서 가장 가깝다. 하지만 다리 네 개가 길고 장식이 많으며 상판이 두껍고 원본보다 높은 듯해 조건부다. Bedside Table Black은 ID와 달리 렌더에서 갈색 목재로 보여 선택 텍스처/원본 모델 표현을 추가 검증해야 한다.

후속 검증: Decocraft modular_desk_drawers_black의 실제 1×1 설치·서랍 기능·장식 다리 높이·색상 확인; bedside_table_black의 variant source texture discrepancy 재검증.

PZ 이미지 SHA-256: `3a4fcf0f039f14e35ebec66613f461bcad7bf198420efc6004db8000d25cebf9`
MC 원본 모델 SHA-256: `14a5ddcaebae394d1e9f0b4543e5144b70d35ae298521a77b6c45fc0df6622b1|56bfc79f85fbddccfb6c7a9535c1113174b338cd4c851025139a5ebe3a5b6613|56bfc79f85fbddccfb6c7a9535c1113174b338cd4c851025139a5ebe3a5b6613`

### 116 Table / Large Dark Oak
판정: DEFER_TWO_TILE_REDDISH_DARK_OAK_PLAIN_RECTANGULAR_TABLE / 제안: 보류

PZ 원본은 적갈색 단순 2×1 긴 사각 테이블로 얇은 평평한 상판과 직선 다리 네 개를 가진다. 기존 Macaw Dark Oak Glass Table은 유리 상판 한 장만 표시돼 반려한다. 이번 Decocraft Wooden Table Ebony 25큐브는 정사각형에 가까운 매우 짙은 갈색 상판과 두꺼운 장식 다리, Kitchen Table Ebony 29큐브는 검정 상판과 두꺼운 장식 다리, Wooden Table Cherry는 분홍색 상판과 장식 다리로 각각 원본의 긴 직사각형·적갈색·곧은 다리 구조와 다르다. 멀티타일 2×1 설치 여부도 미검증이므로 보류한다.

후속 검증: 실제 2×1 배치되는 직선 네 다리 적갈색 원목 테이블 모델 및 Minecraft 방향/연결 여부 검증.

PZ 이미지 SHA-256: `25b5d90971151b45d707adfb79247aa42f19e1fadc42e2033e1e7abe0b13524a`
MC 원본 모델 SHA-256: `014cf39af640f4120c32def0d1fbb27511bc7f14dfef1be3c82fabfbe6a06deb|f156fc905a8529b6e536456ba7b7e362b8d55316b90f98c652e040698b999242|f156fc905a8529b6e536456ba7b7e362b8d55316b90f98c652e040698b999242`

### 117 Fridge / Industrial
판정: DEFER_BLACK_GLASS_FRONT_INDUSTRIAL_DISPLAY_FRIDGE / 제안: 보류

PZ 원본은 검은 산업용 냉장 진열장으로 전면의 큰 투명 유리문과 내부 가로 선반, 세로 손잡이가 핵심이다. Decocraft Fridge Large 실제 372큐브 모델은 은색 4문 불투명 가정용 냉장고이고, 문을 활짝 연 Fridge Large Open Full에서만 내부 선반이 보인다. Vending Machine Soda 200큐브 모델은 음료 진열창과 선반이 있지만 우드색 전면·동전/버튼 패널을 가진 자동판매기로 냉장고와 다르다. 검정 유리문 진열장과 일치하지 않아 보류한다.

후속 검증: 검은 상업용 유리문 냉장 쇼케이스의 1.20.1 Forge 실제 원본 모델/텍스처를 찾아 검증.

PZ 이미지 SHA-256: `afd9961430bc3667ea3350ae11752c8fdaabc01c497f3931e961d421004a5f3d`
MC 원본 모델 SHA-256: `af84a9d6b4b4aadd7977d2c3b5abfecf6300949733f61129271dd08bb765f3c5|ee9c045710bb04a1d828889276117ad97ef52bf63f168a7e2edcdcd93ae097f8`

### 118 Fridge / White Industrial
판정: DEFER_WHITE_GLASS_FRONT_INDUSTRIAL_DISPLAY_FRIDGE / 제안: 보류

PZ 원본은 117번과 같은 산업용 유리문 냉장 진열장이지만 흰색/연회색 외장, 청록빛 투명 문과 내부 선반, 검정 받침대를 가진다. 기존 Paladin White Fridge는 불투명 문과 통풍 그릴이 있어 부적합. 이번 Decocraft Fridge Large 372큐브는 은색 불투명 4문이고 Fridge Small Silver 293큐브는 은색 2문 가정용 모델이며 Open Top Silver는 문을 열어 놓은 변형일 뿐 닫힌 투명 유리문이 아니다. 모두 보류한다.

후속 검증: 1.20.1 Forge 흰색 상업용 유리 진열 냉장고 모델, 내부 선반, 세로 손잡이, 1×1 설치 검증.

PZ 이미지 SHA-256: `2a29b987964414a73155374a7bbd2bd26a6eae0820945862670f128abfe91249`
MC 원본 모델 SHA-256: `af84a9d6b4b4aadd7977d2c3b5abfecf6300949733f61129271dd08bb765f3c5|bf9b95782244bbae172f2b6a51c8f74bd69c20a463255e888206c9dac14c46d9`

### 119 Television / Premium Technologies
판정: DEFER_PREMIUM_GRAY_CRT_TELEVISION_REAR_VIEW_UNCONFIRMED / 제안: 보류

PZ 원본은 Facing W의 뒷면/측면이 보이는 회색 쐐기형 CRT TV로 후면 가로 통풍구와 주황 표시등이 관찰된다. 기존 Refurbished Television은 정육면체 전면 검정 패널로 윤곽이 다르다. 이번 Decocraft CRT TV 실제 12큐브 모델은 검정 정육면체에 가까운 화면 상자로 회색 사다리꼴 후면과 다르며, TV Small/Wall Small은 평면형 모니터라 두께와 형태가 더욱 다르다. 같은 방향에서 후면을 비교한 인게임 회전 검증도 없으므로 보류한다.

후속 검증: 원본 PZ Facing W 후면을 MC 모델 뒷면으로 회전한 360도 비교, 1×1 배치와 TV 기능 검증.

PZ 이미지 SHA-256: `1bf174ef52bcbc99ef9203eb973fbf4c61a48863e1b6eb5bc28a3bb1de5a520e`
MC 원본 모델 SHA-256: `03cd2ace89442159bc59e10968c028282982e5d4daec3cedb83a2b191406ea5e|70019d659851fd0b1bb4f5f4772804e484a09579cbbbdc57521b8efc3a7ae0ec|f4f66a1acb2f309c1963aef56686c2b3063b40c7568168813b3a00cfdf9a0d3b`

### 120 Counter / Modern Corner
판정: DEFER_L_SHAPED_CREAM_TOP_DARK_WOOD_CORNER_COUNTER / 제안: 보류

PZ 원본은 베이지색 L자 상판의 안쪽 모서리가 파여 있고 아래는 진한 황갈색 목재 판넬로 이어지는 1칸 코너 카운터다. 기존 Decocraft Diner Corner Black은 검정·은색 띠와 대각 챔퍼로 부적합. 이번 Decocraft Bottom Cabinet Corner Inner Oak 9큐브는 흰 정사각형 상판과 밝은 갈색 큐브 몸체, Inner Ebony는 검정 상판과 거의 검정 몸체로 나타났다. Outer 1 Oak 23큐브는 부분 삼각형 상판 조각일 뿐 1×1 오목 L자 전체가 아니다. 어느 것도 원본의 베이지 L자 홈과 진한 목재색을 동시에 갖추지 않아 보류한다.

후속 검증: 실제 1×1 L자 오목 코너 상판 + 진한 목재 몸체 모델, 좌우 회전·연결 및 상판 높이 검증.

PZ 이미지 SHA-256: `dfb7c87e94fda3507c7dd6a9abc39b733b221902db43aa1f0c56f6f24e269749`
MC 원본 모델 SHA-256: `eda45de8c4240cd56db24908765c4450b028b519d3eea585542ed0477e364630|e579e5c28586460fa64a53e91cb07c64a3eee5bf4c1b36192bbc71bab607646d|eda45de8c4240cd56db24908765c4450b028b519d3eea585542ed0477e364630`

## 출처·검증 범위

- PZ: 기존 B42 원본 Tiles PNG 및 TMX/.tiles 기반 조립 미리보기 (시각 조립은 잠정이며 인게임 모델이 아님)

- Minecraft: 검증된 Decocraft Forge 1.20.1 JAR에서 BBMODEL과 선택 텍스처를 읽어 원본 해시를 기록하고 Blockbench 5.2.2 데스크톱 화면 캡처

- 원본 모드 JAR, 텍스처 및 BBMODEL 자체는 재배포하지 않음. 비교 이미지·해시·출처만 보관.

- 실제 마인크래프트 설치 시 방향, 크기, 멀티블록, 충돌/상호작용은 별도 테스트 전까지 승인하지 않음.

## 파일

- cards/ : 111~120 원본 PZ 대 Minecraft 원본 모델 비교 10장

- BATCH_111_120_MANUAL_VISUAL_REVIEW.csv : 상세 10종 및 SHA-256

- BATCH_111_120_DEFERRED_OTHER_MODS.csv : 보류 후속 목록

- BATCH_111_120_OTHER_MOD_RESEARCH.csv : 공식 Forge 1.20.1 호환성 링크 (모델 미검증)

- BATCH12_STANDALONE_PROGRESS.json : 병렬 작업 충돌 방지 독립 진행 상태

- INDEX.html : 비교 이미지 열람기

- MANIFEST.json : 범위 및 검증 수치

- ROSEWOOD_BATCH_111_120_MANUAL_REVIEW.zip : 전체 결과
