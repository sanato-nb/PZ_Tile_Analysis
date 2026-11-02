# 로즈우드 가구 18차 171~180번 개별 시각 검수

이번 검수는 PZ B42 완성형 미리보기와 이전 실제 Minecraft 원본 모델 Blockbench 비교판을 먼저 수동 관찰하고, 별도 GitHub Actions에서 Decocraft 3.0.4-1.20.1 Forge의 실제 BBMODEL/텍스처를 검증 후 Blockbench 5.2.2로 새로 렌더한 화면을 추가 대조한다.

이전 B 레인 141~150번은 PR #257에서 이미 검수되어 재작업하지 않았다. 이번 171~180번만 독립 검수하며 A/C 레인의 161~170, 181~200번 결과를 건드리지 않았다.

원본 Decocraft JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05 | https://modrinth.com/mod/decocraft/version/K6V6djNF

검수 10종: 조건부 0종, 보류 10종. 네이티브 Blockbench 캡처 10/10개 모델. 비교 JPG 10장. 인게임 1:1 확정 0종.

일부 원본 스프라이트의 SpriteGridPos 조립과 마크 모델의 동적 블록 상태는 잠정이다. 1×1/2×1/1×2 점유·방향·충돌·상호작용·색상/재질은 인게임 미검증. 부분 모델 캡처는 완성형으로 승인하지 않는다.

## 개별 근거

### 171 Oven / Red
판정: **DEFER_RED_ELECTRIC_RANGE_VS_BRICK_PIZZA_OVEN**. 후보: 보류

PZ 형태: PZ 붉은 금속 전기레인지. 검은 상단 버너 2개, 뒤쪽 다이얼/스위치 줄, 전면 작은 유리 오븐창과 아래 수납/도어, 회색 테두리, 1×1.

수동 비교: 기존 decocraft:pizza_oven 네이티브 렌더는 벽돌 화덕+굴뚝+장작형 불구멍이며 PZ 붉은 전기레인지의 금속 본체, 버너, 다이얼, 오븐문이 모두 없다. 화덕을 전기레인지로 승인할 수 없다.

추가 검증: Forge 1.20.1 붉은 금속 전기/가스레인지 원본 모델을 찾아 2구 버너·다이얼·오븐창·전원/요리 기능과 회전 상태 검증.

PZ SHA-256: `5d08a38978beb1e3a8ebb5309852aacf74812fa5aa28514dcc15d01b57808cd4`
MC 모델 SHA-256: `9ab500f2281f0c8c6a96ef3da9d65f60faab6b6c5a1c764d82cc0f64d7a10bcb`
비교 이미지 SHA-256: `6f2da37510bd2da24a6001c2922cbb6c8e0a5d5ddaae7d6c6cd85cbed916a672`


### 172 Wardrobe / White
판정: **DEFER_BEIGE_DOUBLE_WARDROBE_VS_LOW_CABINET**. 후보: 보류

PZ 형태: PZ 1×2 높은 연베이지/아이보리 2문 옷장. 평평한 상단과 두 세로 문, 가운데 낮은 검정 손잡이 2개, 아래 먼지·오염된 목재 질감.

수동 비교: 기존 Macaw Acacia Double Wardrobe는 회색 외장/주황 문으로 원본과 색이 정반대. 새 후보 Decocraft White Bottom Cabinet은 밝은 색은 유사해도 높이가 낮은 주방장으로 높은 옷장과 문/손잡이 배치가 다르다.

추가 검증: 아이보리색 2문 높은 옷장 실제 Forge 1.20.1 원본 모델, 1×2 배치·수납·문 열림 검증.

PZ SHA-256: `747453d18325d466d254a902228368f31c671acff5b5bf6880ccd3cff2d11dcc`
MC 모델 SHA-256: `630ffe7f31d8c5b84a5f112221f8e13d97084f820c76d7312c89a8daccc1e3f0`
비교 이미지 SHA-256: `500a4d4bdf9b1068c965db73808f2d440b669289787f1964586126c1b60718aa`


### 173 Chair / Spiffos Dinner
판정: **DEFER_SPIFFOS_RED_PEDESTAL_STOOL_VS_DINER_CHAIR**. 후보: 보류

PZ 형태: PZ Spiffo's 다이너용 원형 붉은 좌석과 높은 구부러진 황금색 관형 등받이, 중앙 한 개 금속 기둥과 원형 바닥판의 스툴.

수동 비교: 기존 pfm:arm_chair_leather 네이티브 비교는 회색 직육면체 일부만 보이는 불완전 모델이라 좌석 형태를 확인할 수 없다. Decocraft Diner Chair Blue는 다리/등받이/좌판 재질·색·중앙 받침 구조가 다른 일반 의자 후보여서 1:1 아님.

추가 검증: 붉은 원형 회전 스툴, 한 기둥 원형 받침, 둥근 금속 등받이를 갖춘 실제 원본 모델 검색. 착석 방향/높이 확인.

PZ SHA-256: `f1103c29529716a3769248a56dbf6a17cbfa354442fb72b437f7b28b3f5cc925`
MC 모델 SHA-256: `1640d476be17089159fef35e9f63fead1afc6694b21cdab115e668a4229e15dd`
비교 이미지 SHA-256: `fdc3c5573e571ef90ae6375b43507abfae99f2e635a150a477ab5d2475655a64`


### 174 Clothing Dryer / White
판정: **DEFER_WHITE_TOP_PANEL_DRYER_VS_FRONT_LOADING**. 후보: 보류

PZ 형태: PZ 흰색 정육면체 빨래 건조기. 뒤로 솟은 검은 조작 패널과 오른쪽 다이얼, 상판은 막혀 있고 전면 큰 평면 직사각형 문과 수직 손잡이.

수동 비교: Decocraft Dryer 원본 모델은 정면 큰 둥근 유리 도어, 앞면 상단 디지털 표시창·노브가 있는 드럼형 세탁/건조기. PZ의 상단 뒤 조작패널과 네모 문이 없어 디자인 불일치.

추가 검증: 뒤쪽 상단 제어 패널+직사각 문을 가진 흰색 상업용 건조기 모델과 건조기 기능 검증.

PZ SHA-256: `3fb5e917c13ac3f3e734b6afb9969ef3f8445be8ca4d9221b65cf4fc5c98e9fd`
MC 모델 SHA-256: `62230d9355b3b06134ef99ba8a37ea1e8062c7923124ac7e4dc9d136ee704423`
비교 이미지 SHA-256: `c09baeedd0b17758ff51a7577698558c20b09abeb8d9f21f487f5be7854afa9e`


### 175 Oven / Industrial
판정: **DEFER_STAINLESS_INDUSTRIAL_RANGE_NO_MATCH**. 후보: 보류

PZ 형태: PZ 1×1 산업용 스테인리스 오븐/레인지. 높은 은회색 좌측 보호판, 검정 상단 조리 그릴, 전면 스테인리스 문/손잡이와 직사각 몸체.

수동 비교: 기존 Decocraft Pizza Oven은 벽돌 화덕과 굴뚝이 있는 전혀 다른 종류. 추가 스테인리스 주방 설비 후보 Kitchen Sink Silver도 싱크대이므로 조리 그릴·오븐문·높은 측면 판을 재현하지 못한다. 후보 불승인.

추가 검증: Forge 1.20.1 상업용 스테인리스 조리레인지/오븐, 측면 가드, 검정 그릴, 전면 도어 실제 모델 탐색.

PZ SHA-256: `c5954095f6694be7995935b36c61b61f9e499c9ece3e8f4882d1890505adb7de`
MC 모델 SHA-256: `e4ccda4a967c34a64b9803ef4d86dbf4573c9f87f12d85eb151b2fc80df103b8`
비교 이미지 SHA-256: `84a66e77bc0e0bb274483ed286481ae10b9c4eff74c60027ef43bd109ba7860e`


### 176 Counter / Generic Shop Corner
판정: **DEFER_PALE_WOOD_CORNER_VS_BLACK_STRIPED_BAR**. 후보: 보류

PZ 형태: PZ 1×1 연한 황토/베이지 원목 L자형 매장 카운터 코너. 평평한 두꺼운 목재 상판이 두 방향으로 이어지고 하부는 문 없는 같은색 나무 판넬.

수동 비교: Decocraft Diner Counter Corner Black은 L형 상판과 코너 체적은 비슷하지만 검정·흰색 가로 줄무늬 금속/플라스틱 바 형태로 나무 질감·색상과 일치하지 않는다.

추가 검증: 연한 원목 무늬 L자 코너 카운터의 실제 1×1 Forge 모델/텍스처 또는 바닐라 나무 조합과 연결 방향 검증.

PZ SHA-256: `d4a04b95a2897ffd0b4e0dc4c002ed7c781bbd9ab61285c578863d941c4992bb`
MC 모델 SHA-256: `25ef3b784df0de583daad5bbf2d506ceeeadb62db760d80521b8cff7860de13a`
비교 이미지 SHA-256: `62e0daaf9e1a2304250a5bce2954530302fa9c50a3b433c74553a6786eec504b`


### 177 Counter / Dark
판정: **DEFER_DARK_TWO_DOOR_COUNTER_VS_OAK_CABINET**. 후보: 보류

PZ 형태: PZ 1×1 짙은 갈색/거의 검정 목재 수납 카운터. 진한 평판 상판, 앞면 두 개의 문과 작은 금속 손잡이, 바닥 받침.

수동 비교: 기존 Macaw Acacia Counter는 주황 상판+회색 석재 측면으로 원본과 재질 불일치. Decocraft Bottom Cabinet 2 Oak는 수납장 계열이지만 밝은 참나무 색과 문·서랍 배치가 달라 어두운 2도어 카운터 대체로 승인 불가.

추가 검증: 짙은 월넛/에보니 2문 하부 수납장, 같은색 상판과 세로 손잡이 2개를 가진 실제 모델 검증.

PZ SHA-256: `abdd69e368b38338c4388cfc9bf71581993e42d5d7856be314ead63f9dda4277`
MC 모델 SHA-256: `630ffe7f31d8c5b84a5f112221f8e13d97084f820c76d7312c89a8daccc1e3f0`
비교 이미지 SHA-256: `baf1cc84bdd10ee7a984546a3e772644b137de9d38aa62ffe8cc3864f77d36cb`


### 178 Chair / Red Theatre
판정: **DEFER_RED_THEATRE_DOUBLE_SEAT_VS_ARMCHAIR**. 후보: 보류

PZ 형태: PZ 극장식 붉은 2인 연속 좌석. 진홍색 쿠션형 등받이 2개, 검정 뒷판, 붉은 팔걸이, 얇은 검정 철제 다리·받침.

수동 비교: 기존 Paladin Oak Chair Classic Red는 갈색 막대 프레임 일부만 렌더되어 의자 전체를 입증하지 못한다. Decocraft Cottage Armchair는 꽃무늬 패브릭 1인용 의자여서 붉은 연속 2좌석·검정 금속 다리와 형태가 다르다.

추가 검증: 극장 좌석 연결형 2인 또는 두 모듈의 실제 Forge 모델, 좌석 연결·팔걸이·고정 설치와 충돌/착석 검증.

PZ SHA-256: `d8fcb589f1e2964de8e32bf2f12b67e8eaa7ae11ecbb7af2ef3d4371c123420d`
MC 모델 SHA-256: `34b37379ca11b74db0546d02ca155f7b8047ded9c95debb49e08a1a55380674c`
비교 이미지 SHA-256: `ec794da53db06140823c494783b9822f7be1313130b4b658e9b99eff447aac56`


### 179 Drawers / Pale
판정: **DEFER_PALE_THREE_DRAWER_CHEST_VS_DESK_DRAWERS**. 후보: 보류

PZ 형태: PZ 밝은 크림/황토색 1×1 3단 서랍장. 전면 3개 수평 서랍, 별도 손잡이 없는 얇은 가로 틈, 단순한 직사각 본체.

수동 비교: 기존 Macaw Acacia Bookshelf Drawer 네이티브 화면은 초록 판 하나만 나오는 불완전 모델. Decocraft Modular Desk Drawers Oak는 서랍 기능은 유사할 수 있지만 원본의 세 단, 무손잡이 가로 홈, 연한 색과 정확히 일치하는지 확인되지 않아 보류.

추가 검증: 3단 밝은 나무 서랍장 원본 모델의 실제 완성형 렌더와 서랍 개폐·1×1 높이 검증.

PZ SHA-256: `5fcc6859b098e726a73531ad9fa0a62f46f766cf0f277a5dd03c75b27176cea2`
MC 모델 SHA-256: `14a5ddcaebae394d1e9f0b4543e5144b70d35ae298521a77b6c45fc0df6622b1`
비교 이미지 SHA-256: `b6f4426f8100f18fd9cefeb57b2e357b719ec676a130b0f78f7abcb954282a5d`


### 180 Counter / Birchwood Floating
판정: **DEFER_BIRCH_FLOATING_TWO_DOOR_WALL_CABINET**. 후보: 보류

PZ 형태: PZ 벽 부착형 연갈색/황토색 낮은 2문 캐비닛. 길쭉한 상판, 전면 두 문과 은색 세로 손잡이, 바닥 지지대 없이 벽에 매달린 형태.

수동 비교: 기존 Macaw Birch Counter는 흰 회색 석재 본체+나무 상판의 바닥 설치 블록이어서 원본과 다름. Decocraft Top Cabinet 3 Oak는 벽 부착형 주방 수납장 종류지만 문 분할, 손잡이 수, 길이와 상판 색상 일치가 검증되지 않아 확정 불가.

추가 검증: 1×1 벽 부착 높이, 두 문과 손잡이, 방향별 연결·벽 지지 조건과 실제 인게임 수납 확인.

PZ SHA-256: `e9b9e3f36cb55c4d4b374cba13d70c50ce733e4a963a6f5072714f4a941a78e0`
MC 모델 SHA-256: `11aea885ce49dcc119ed89ec976019aadae5fc8227f1714efb25dbaf99cb1df3`
비교 이미지 SHA-256: `373aa8b33342d36fde724dee8aec134d9d21e9bc9bf83d50a0561cecfb264eee`


## 산출물

- cards/ : PZ 원본 완성형과 실제 소스 모델(또는 명시적 미검증 화면) 비교 JPG 10장

- BATCH_171_180_MANUAL_VISUAL_REVIEW.csv : 상세 수동 판정, 기존 자동 매칭의 오차, 모델 출처와 SHA

- BATCH_171_180_DEFERRED_OTHER_MODS.csv : 다른 모드·바닐라·신규 모델 후속 검토 목록

- BATCH_171_180_SHA256_PROVENANCE.csv : 원본 PZ/BBMODEL/텍스처/Blockbench 캡처/카드 해시

- MANIFEST.json / BATCH18_STANDALONE_PROGRESS.json : 독립 검수 범위·상태

- INDEX.html : 10개 비교판 탐색

- ROSEWOOD_BATCH_171_180_MANUAL_REVIEW.zip : 카드·CSV·README·인덱스 일괄 보관

원본 게임 TMX/PNG/SQLite와 기존 357종 누적 검수 CSV, 다른 레인 결과를 수정하지 않는다.
