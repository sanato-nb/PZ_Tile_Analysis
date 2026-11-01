# 로즈우드 357종 — 13차 121~130번 원본 가구 개별 시각 검수

121~130 원본 PZ 가구 10종을 독립 검토. Decocraft JAR 원본 BBMODEL/텍스처 31개 렌더 시도 중 30개 Blockbench 5.2.2 소스 이미지 성공. 실제 Minecraft 1.20.1 Forge 게임 설치/충돌/상호작용 테스트 및 1:1 최종 인증은 0건.

조건부 2건, 보류 8건. 11차 101~110 및 12차 111~120의 진행 CSV를 덮어쓰지 않기 위해 독립 JSON만 생성.

외부 모드 공식 호환성 자료 10건은 별도 CSV에 보존하며, 해당 모델의 3D 렌더·외형 검증이 완료된 것으로 간주하지 않음.

## 10종 검수 근거

검증된 모드 원본: Decocraft 3.0.4-1.20.1 Forge 1.20.1, JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05, https://modrinth.com/mod/decocraft/version/K6V6djNF

### 121 Fridge / Steel
판정: DEFER_STEEL_SINGLE_DOOR_FRIDGE_VS_DOUBLE_DOOR_DECOCRAFT / 제안: 보류

원본은 은회색 단일 전면판과 왼쪽 검정 세로 경계가 두드러지는 좁은 냉장고다. 실제 Decocraft Fridge Small Silver 원본 293큐브는 위·아래 두 문이 가로선으로 분리되고 전면에 은색 가로 손잡이 두 개와 상부 통풍구가 있어 외형이 다르다. Fridge Large 372큐브는 좌우 양문·디스펜서까지 있는 넓은 최신형이라 더 멀다. 이전 Paladin Iron Fridge는 이 묶음에서 실제 완성 모델 검증을 하지 않았으므로 승인하지 않는다.

후속 검증: Paladin iron/gray fridge의 실제 전체 원본 모델과 단일 전면문 여부 비교. Forge 1.20.1 실제 1×1 설치, 냉장 기능, 높이 확인.

PZ 이미지 SHA-256: `722405d86810381a3b5a8f21ca447b62886c613247293de6f43e202f2af639db`
MC 원본 모델 SHA-256: `c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48|af84a9d6b4b4aadd7977d2c3b5abfecf6300949733f61129271dd08bb765f3c5`

### 122 Counter / Bar
판정: DEFER_DARK_WOOD_BAR_COUNTER_SOLID_PANELS / 제안: 보류

원본은 상판·몸체·하단 몰딩이 모두 짙은 나무이며 서랍·손잡이·흰 조리대가 없다. 실제 Decocraft Bottom Cabinet 1 Spruce/Oak 13큐브를 열어 보니 두 모델 모두 흰색 두꺼운 상판, 앞쪽 상부 서랍 및 손잡이, 하부 문이 나타나 원본 바 카운터와 다르다. Diner Counter Yellow는 원본 파일이 있지만 이번 실행에서 Blockbench 모델 큐브 3개로 완성 렌더 판정을 받지 못해 비교 증거로 쓰지 않는다.

후속 검증: 무광 짙은 원목 일체형 1칸 바 카운터의 1.20.1 Forge 모델을 찾고 실제 상판 높이, 연속 연결, 저장 기능 확인.

PZ 이미지 SHA-256: `cd1deb408380faf03bcb6e17a65a75bff928822f4a0c3d209949804ac4fcb7d0`
MC 원본 모델 SHA-256: `512f252cb22f035ad901daef97a208680f8e57b67f47b250318dd05151e87c1b|512f252cb22f035ad901daef97a208680f8e57b67f47b250318dd05151e87c1b`

### 123 Chair / Fancy White
판정: DEFER_FANCY_CREAM_WINGBACK_ARMCHAIR_WITH_EXPOSED_WOOD_LEGS / 제안: 보류

원본의 핵심은 위로 둥글게 올라간 전통형 등받이, 부드러운 곡면 팔걸이, 얇게 드러난 어두운 나무 다리 네 개다. 실제 Decocraft Armchair Cream 9큐브는 크림색이 가깝지만 직선 평판 등받이와 네모 팔걸이·바닥까지 막힌 몸체로 구조가 크게 다르다. Cottage Armchair 23큐브는 꽃무늬와 아래 천 스커트가 있어 원본 단색 우아한 의자와 더 다르다. 색만 맞았다는 이유로 승인하지 않는다.

후속 검증: 고전형 rounded wingback/rolled armchair와 4개 노출 목재 다리가 있는 실제 Forge 1.20.1 모델을 조사하고 앉기 기능 확인.

PZ 이미지 SHA-256: `62fee5b5ede31d53acd98a5d6ed69535045a244bf5b9f62ed79c0a36b28678e4`
MC 원본 모델 SHA-256: `fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|34b37379ca11b74db0546d02ca155f7b8047ded9c95debb49e08a1a55380674c`

### 124 Fridge / White
판정: CONDITIONAL_WARM_WHITE_TWO_DOOR_FRIDGE_HANDLES_AND_VENTS_MISMATCH / 제안: decocraft:fridge_small_cream

원본은 위쪽 작은 냉동실과 아래쪽 큰 냉장실로 구분된 따뜻한 아이보리 2도어 냉장고다. Decocraft Fridge Small Cream 실제 293큐브 모델은 크림색 세로 직육면체, 위아래 2도어 분할이라는 중요한 실루엣이 일치한다. 다만 마크 모델에는 앞쪽 수평 은색 손잡이 두 개, 상단 4개 통풍구, 각진 윗모서리가 뚜렷하며 PZ는 옆면 세로 손잡이와 더 매끈한 면이다. 실물 외형은 조건부이며 게임 설치/냉장 기능은 확인하지 않았다.

후속 검증: 원본 PZ 1×1과 마크 실제 점유·높이·방향 및 2문 열림/보관 기능 검증, 손잡이 위치가 더 비슷한 대안 검색.

PZ 이미지 SHA-256: `82b1fbbe2e3618434089363400e77ad410af0d398f0e58625e28ff595117f2e3`
MC 원본 모델 SHA-256: `c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48|c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48`

### 125 Chair / Beach
판정: CONDITIONAL_STRONG_BLUE_WHITE_STRIPED_FOLDING_WOOD_BEACH_CHAIR / 제안: decocraft:beach_chair_light_blue

원본은 나무 접이식 프레임과 하늘색·흰색 줄무늬 천이 연결된 낮은 비치 체어다. 실제 Decocraft Beach Chair Light Blue 원본 18큐브를 Blockbench로 렌더하니 흰색/하늘색 세로 줄무늬 천, 비스듬한 목재 등받이, 앞쪽으로 내려오는 좌석, 뒤 지지대가 모두 존재해 이전 Paladin Arm Chair Leather의 회색 세로판보다 훨씬 정확하다. Blue 변형은 줄무늬가 진한 남색이어서 PZ 밝은 파랑보다 멀다. PZ 프레임 각도·다리의 교차 위치·천 굴곡은 일부 다르고 실제 1×2 설치 여부는 미검증이다.

후속 검증: Forge 1.20.1 Decocraft 게임에 배치하여 1×2 점유·회전·앉기/접기·충돌·텍스처 실제 렌더를 확인. Beachparty Sun Lounger와 실물 비교.

PZ 이미지 SHA-256: `736da8c48405e99055683d1fcae46ad3a82c33f9cb7ac55d8a1bbc0b74f3d111`
MC 원본 모델 SHA-256: `ef7759d3dd1b64eadd7507536995553eaac771f210224316e807169f7c24e17e|ef7759d3dd1b64eadd7507536995553eaac771f210224316e807169f7c24e17e`

### 126 Chair / Green Comfy
판정: DEFER_OLIVE_PADDED_LOW_COMFY_ARMCHAIR_VS_ANGULAR_GREEN / 제안: 보류

PZ는 노란 기가 도는 올리브 천, 낮고 둥근 등받이, 쿠션 굴곡, 아래쪽 짙은 적갈색 받침이 특징이다. Decocraft Armchair Green 실제 9큐브 모델은 진한 녹색 직선 평판 등받이·각진 팔걸이·바닥까지 같은 녹색 몸체이며 둥근 쿠션과 목재 받침이 없다. Lime은 훨씬 선명한 연두라 색상도 다르다. 가구 분류만 같고 핵심 실루엣·재질이 달라 보류한다.

후속 검증: 낮고 둥근 올리브 클럽체어, 별도 쿠션과 적갈색 베이스가 있는 1×1 모드 가구를 렌더 검증.

PZ 이미지 SHA-256: `7b60fa6a839b10d0ae84a6fc786673410868b03e7f929711bc45386f950cb118`
MC 원본 모델 SHA-256: `fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28`

### 127 Counter / Oak Corner
판정: DEFER_ONE_TILE_ALL_OAK_L_NOTCHED_CORNER_COUNTER / 제안: 보류

원본은 상판에 안쪽으로 파인 직각 ㄱ자 홈이 보이는 한 칸짜리 전체 원목 코너 카운터다. Decocraft Corner Inner Oak 실제 9큐브는 흰 상판을 가진 정사각형 캐비닛으로 홈이 없고, Corner Outer 2 Oak 실제 21큐브는 흰 상판+서랍·손잡이가 붙은 사다리꼴 모서리 부품이다. 둘을 임의로 합쳐 원본 1×1 ㄱ자 가구라고 간주할 근거가 없으므로 보류한다.

후속 검증: ㄱ자 안쪽 홈이 실제 1×1에서 형성되는 일체형 oak corner counter 모드 모델, 연속 배치/방향 및 충돌 검증.

PZ 이미지 SHA-256: `7b3a04d2ec329808b540b612b6b706491b97abb5a723432734353d319ce27d25`
MC 원본 모델 SHA-256: `1fc152370e5bac2b89b8c9b1a0963a78716a0bae804081185758da5a23f54e39|eda45de8c4240cd56db24908765c4450b028b519d3eea585542ed0477e364630`

### 128 Counter / White Corner
판정: DEFER_ONE_TILE_MONOCHROME_IVORY_L_NOTCHED_CORNER_COUNTER / 제안: 보류

원본은 ㄱ자로 안쪽이 파인 상판과 몸체 전체가 아이보리색인 단순한 코너 카운터다. 실제 Decocraft Corner Outer 1 White 23큐브는 상판이 갈색 나무이고 몸체는 얇은 패널 조각이라 한 덩어리 가구가 아니다. Corner Inner White 9큐브도 나무색 정사각 상판에 흰 몸체인 평범한 정육면체로 ㄱ자 홈이 없다. 기존 후보의 색·형상·부품 완결성이 모두 달라 보류한다.

후속 검증: Forge 1.20.1 올아이보리 ㄱ자 코너 카운터를 실제 1×1 모델로 확인하거나 바닐라 석영 계단 조합의 점유·높이 차이를 검증.

PZ 이미지 SHA-256: `090a9fc61ffb104e35dbc55a646d4d0cc2f9332a4bfe48cdf65dbf82acf6e135`
MC 원본 모델 SHA-256: `e579e5c28586460fa64a53e91cb07c64a3eee5bf4c1b36192bbc71bab607646d|eda45de8c4240cd56db24908765c4450b028b519d3eea585542ed0477e364630`

### 129 Chair / Light Blue
판정: DEFER_PALE_GRAY_BLUE_ROUNDED_CLUB_CHAIR_VS_SATURATED_BLOCKY_ARMCHAIR / 제안: 보류

PZ 이름은 Light Blue지만 실제 완성형 미리보기는 회색에 가까운 아주 옅은 청록빛 천과 둥근 등받이·쿠션을 가진 낮은 안락의자다. 실제 Decocraft Armchair Light Blue 9큐브는 채도 높은 밝은 파랑, Ocean Blue는 더 짙은 청록이며 둘 다 각진 높은 평판 등받이와 직각 팔걸이, 아래 받침이 없는 일체형이다. 이전 Paladin Blue Arm Chair 역시 검푸른 단순 L형 판으로 맞지 않았다. 색과 실루엣 차이가 커 보류한다.

후속 검증: 밝고 채도 낮은 회청색 둥근 쿠션 안락의자 모델을 Forge 1.20.1에서 확인하고 1×1 설치/앉기 검증.

PZ 이미지 SHA-256: `0d4d481ca7f2e4d2565ccbb09ff080ad11cca9cb3229a2b0443d875c361eaba9`
MC 원본 모델 SHA-256: `fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28`

### 130 Couch / Light Blue
판정: DEFER_TWO_TILE_PALE_BLUE_SOFA_MODULAR_SHAPE_AND_COLOR_MISMATCH / 제안: 보류

원본은 회청색 2인 소파가 2×1로 이어지고 둥근 등받이와 좌석 쿠션이 중앙에서 구분된다. Decocraft Couch Left/Right Light Blue 원본을 각각 Blockbench로 열어 보니 좌·우 팔걸이가 있는 모듈은 실제로 존재하지만 마크의 선명한 파랑이 PZ의 회색에 가까운 색보다 진하고, 등받이는 직선 평판이며 원본의 쿠션 굴곡·하단 받침이 없다. 두 소스 모델을 한 게임에서 연결해 확인한 것도 아니므로 완성형 2인 소파로 승인하지 않는다.

후속 검증: Decocraft 2개 모듈 실제 2×1 연결/팔걸이/방향·앉기 기능 검증. 더 낮은 채도의 회청색 둥근 쿠션 소파 대체 모델 검색.

PZ 이미지 SHA-256: `7e4cb16b4f593469577efc8906f156b58b72b0cd475cf5f726a45370b28c4d3d`
MC 원본 모델 SHA-256: `0e36aa9871bc061aa4e7683e7ec69cbb080226280259d47c14f684f23d7b31cc|9681b0789bf07ad97494ac57e0e48e955dd0bb8076db55fb7ab6a5006f3d2fa5`

## 출처·검증 범위

- PZ: 기존 B42 원본 Tiles PNG 및 TMX/.tiles 기반 조립 미리보기 (시각 조립은 잠정이며 인게임 모델이 아님)

- Minecraft: 검증된 Decocraft Forge 1.20.1 JAR에서 BBMODEL과 선택 텍스처를 읽어 원본 해시를 기록하고 Blockbench 5.2.2 데스크톱 화면 캡처

- 원본 모드 JAR, 텍스처 및 BBMODEL 자체는 재배포하지 않음. 비교 이미지·해시·출처만 보관.

- 실제 마인크래프트 설치 시 방향, 크기, 멀티블록, 충돌/상호작용은 별도 테스트 전까지 승인하지 않음.

## 파일

- cards/ : 121~130 원본 PZ 대 Minecraft 원본 모델 비교 10장

- BATCH_121_130_MANUAL_VISUAL_REVIEW.csv : 상세 10종 및 SHA-256

- BATCH_121_130_DEFERRED_OTHER_MODS.csv : 보류 후속 목록

- BATCH_121_130_OTHER_MOD_RESEARCH.csv : 공식 Forge 1.20.1 호환성 링크 (모델 미검증)

- BATCH13_STANDALONE_PROGRESS.json : 병렬 작업 충돌 방지 독립 진행 상태

- INDEX.html : 비교 이미지 열람기

- MANIFEST.json : 범위 및 검증 수치

- ROSEWOOD_BATCH_121_130_MANUAL_REVIEW.zip : 전체 결과
