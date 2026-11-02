# 로즈우드 가구 15차 141~150번 개별 시각 검수

이번 검수는 PZ B42 완성형 미리보기와 이전 실제 Minecraft 원본 모델 Blockbench 비교판을 먼저 수동 관찰하고, 별도 GitHub Actions에서 Decocraft 3.0.4-1.20.1 Forge의 실제 BBMODEL/텍스처를 검증 후 Blockbench 5.2.2로 새로 렌더한 화면을 추가 대조한다.

이전 131~140번은 PR #254에서 이미 검수되어 재작업하지 않았다. 이번 141~150번만 레인 B로 검수하며 레인 A의 161~170번과 레인 C의 151~160번을 건드리지 않았다.

원본 Decocraft JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05 | https://modrinth.com/mod/decocraft/version/K6V6djNF

검수 10종: 조건부 1종, 보류 9종. 네이티브 Blockbench 캡처 12/12개 모델. 비교 JPG 10장. 인게임 1:1 확정 0종.

일부 원본 스프라이트의 SpriteGridPos 조립과 마크 모델의 동적 블록 상태는 잠정이다. 1×1/2×1/1×2 점유·방향·충돌·상호작용·색상/재질은 인게임 미검증. 부분 모델 캡처는 완성형으로 승인하지 않는다.

## 개별 근거

### 141 Couch / White Lazy
판정: **DEFER_CREAM_TWO_SEAT_COUCH_VS_SINGLE_BLOCK_SEGMENT**. 후보: 보류

PZ 형태: PZ 크림색/옅은 베이지 2×1 두 좌석 소파. 등받이와 좌석에 두 개의 쿠션 분할선, 둥근 목재 팔걸이 두 개, 아래쪽 나무 패널 프레임이 연결됨.

수동 비교: 기존 Macaw White Couch는 흰 직각형 단일 소파 조각만 렌더되어 2좌석 완성형이 아니며 색·목재 하단 프레임이 없다. Decocraft Couch Left/Right Light Blue 실모델은 연결 가능한 좌우 모듈 형태지만 파란색 단색 직각 쿠션과 직선 팔걸이라 크림색+목재 팔걸이 원본과 다르다. 좌우 게임 내 접속도 미검증.

추가 검증: 1.20.1 Forge 크림색 두 좌석 목재 프레임 소파 실제 모델/연결 상태, 2×1 배치, 양쪽 팔걸이·좌석 쿠션·회전 검증.

PZ SHA-256: `6ae5e7f5c24471d8184119e9a562a8719fa1160b3d9e1cb5b8dec00239498b3d`
MC 모델 SHA-256: `0e36aa9871bc061aa4e7683e7ec69cbb080226280259d47c14f684f23d7b31cc`
비교 이미지 SHA-256: `173c32a51dad9de79687ebbd2f91f5ec00dee92f805adc507fa19f40c7671d9a`


### 142 Counter / Green
판정: **DEFER_GREEN_TWO_DOOR_COUNTER_VS_STRIPED_CORNER**. 후보: 보류

PZ 형태: PZ 어두운 올리브/회녹색 1×1 수납형 카운터. 회녹색 평평한 상판, 전면 두 개의 여닫이 문과 세로 손잡이 두 개, 장식 띠 없음.

수동 비교: 기존 Decocraft Diner Counter Corner Green은 초록+흰색 수평 줄무늬가 있는 각진 모서리 바/기둥으로 전면 문 두 개와 손잡이가 없어 오매칭. Decocraft Bottom Cabinet 1 Oak는 수납장 종류는 가깝지만 원목색, 문/서랍 구성과 상판색이 달라 정확한 대체가 아니다.

추가 검증: 녹회색 두 문이 분리되고 손잡이 두 개가 있는 1×1 Forge 주방 하부장 모델 검증. 카운터 높이·문 열림·상판 점유 확인.

PZ SHA-256: `9327207bbb2c0b11c81a2132d6db697f366a69c2e2f9296171efa9f118dd9145`
MC 모델 SHA-256: `512f252cb22f035ad901daef97a208680f8e57b67f47b250318dd05151e87c1b`
비교 이미지 SHA-256: `1e5a14f565024a2e41eeadd00c9e61feffbaf235d4c5f4a68a2c4e36e7b8dea3`


### 143 Dumpster / Blue
판정: **CONDITIONAL_BLUE_TWO_TILE_DUMPSTER_LID_CLOSE**. 후보: decocraft:dumpster

PZ 형태: PZ 2×1 넓은 보라빛 파란 철제 대형 쓰레기 수거함. 상단 검정색 여러 줄 접이식/분할 뚜껑, 옆면 굵은 손잡이, 낮고 긴 직사각 상자.

수동 비교: 기존 Decocraft Rolling Bin Blue는 높고 좁은 1인용 바퀴 달린 수거통이어서 2×1 대형 덤프스터와 종류가 다름. 원본 Decocraft Dumpster BBMODEL의 기존 네이티브 Blockbench 렌더에서 검정 다중 리브 뚜껑, 파란 금속 직사각 몸체, 측면 손잡이와 오염 흔적이 확인되어 훨씬 가깝다. 다만 PZ는 더 보랏빛이며 뚜껑 패널 수/경사, 2×1 설치 범위는 차이가 있고 실제 게임에서 미검증이므로 조건부만.

추가 검증: Decocraft Dumpster 실제 2×1 점유·회전·뚜껑 개폐·충돌/수납 검증. PZ의 보라 파랑 색과 뚜껑 분할 수 비교.

PZ SHA-256: `7acbbe9bc3ba6d831397b32aa855e7fba4311ef2c8522b4a8db582f1de38272b`
MC 모델 SHA-256: `e1dc85140857c1f433397ce55dd8e4cdc71cb085baa112c73fcc36ceaf5f6790`
비교 이미지 SHA-256: `c299073d428c593f0cb490f959b036d12a3474521fdcfd3e7c3739f23631ddad`


### 144 Fridge / Plain
판정: **DEFER_VENTED_PLAIN_FRIDGE_VS_WRONG_FRIDGE**. 후보: 보류

PZ 형태: PZ 키 큰 아이보리색 직사각 냉장 설비. 전면 대부분이 검정/회색 가로 통풍 격자이며 아래 작은 제어/압축기 칸이 보이고 일반 가정용 냉장고 문 손잡이가 없음.

수동 비교: 기존 Refurbished Dark Fridge 부분 렌더는 분홍색 측면과 검정 앞면만 보여 원본의 크림색 전면 통풍 격자/아래 제어칸이 없다. Decocraft Small Cream도 일반 상하 두 문 냉장고로 원본 통풍 전면 구조와 다르다.

추가 검증: Forge 1.20.1 상업용 통풍 전면 냉장고/냉장 장비 원본 모델 탐색. 실제 PZ 용도와 1×1 높이, 전원·냉장 기능 확인.

PZ SHA-256: `61215ade683a5a19408f9bc6453d6e7ecbd4163c96fa7900efedf67fbe560772`
MC 모델 SHA-256: `c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48`
비교 이미지 SHA-256: `a5e5e3c3fc70b5bb5ffc04771226e41ed8782863975105f358fc2b719c2d71d5`


### 145 Counter / Low Motel
판정: **DEFER_FLOATING_IVORY_MOTEL_COUNTER_VS_FULL_CABINET**. 후보: 보류

PZ 형태: PZ 1×1 얇고 낮은 아이보리색 사각 상판과 밑면 턱만 있는 벽 부착형 선반/낮은 카운터. 아래에 문·서랍·바닥 지지대가 보이지 않음.

수동 비교: 기존 Macaw Acacia Counter는 주황색 상판과 검은 전체 높이의 블록형 받침이 있어 원본의 벽 부착형 얇은 판과 다르다. Decocraft Bathroom Counter Left White도 수납형 전체 가구로 원본의 빈 하부 공간을 재현하지 못한다.

추가 검증: 바닐라 자작나무/석영 덫문·반블록의 벽 설치 또는 실제 Forge 벽 부착 아이보리 선반 모델을 검토하되 설치 높이·충돌·모서리 일치 검증.

PZ SHA-256: `ca6be44e88406ad96ddf1576dff8681d8121b91d1e25f742fa5c622dac4e9443`
MC 모델 SHA-256: `eaa9c1d69c46b653df6f07f5c3e83b6076a15690539ad76707502deab6e9a7bc`
비교 이미지 SHA-256: `a0e46bad9f22687f51b6e59c091c0c6580720bb86eb63560d112c6ca88995448`


### 146 Chair / Blue Comfy
판정: **DEFER_BLUE_ROUNDED_UPHOLSTERED_ARMCHAIR_VS_BLOCKY_OR_FLORAL**. 후보: 보류

PZ 형태: PZ 1×1 탁한 회청색 푹신한 안락의자. 둥근 등받이, 굵고 둥근 팔걸이 두 개, 깊은 별도 좌석 쿠션, 검은 바닥 받침.

수동 비교: 기존 Paladin Blue Arm Chair는 밝은 청색 직각 등받이·한 좌석 블록으로 원본의 둥근 팔걸이/두툼한 쿠션/짙은 색을 재현하지 못한다. Decocraft Cottage Armchair는 곡선형 쿠션과 팔걸이는 가깝지만 꽃무늬 분홍·크림 패턴이라 원본의 단색 회청색과 큰 차이.

추가 검증: 1.20.1 Forge 단색 청회색 패브릭 둥근 팔걸이 1인 소파 원본 모델 검증. 좌석 높이·등받이 곡률·발판·착석 기능 확인.

PZ SHA-256: `e671710f5df01ba34994962442f484f05a176dcc1a9be6310b98ab034f65fc5f`
MC 모델 SHA-256: `34b37379ca11b74db0546d02ca155f7b8047ded9c95debb49e08a1a55380674c`
비교 이미지 SHA-256: `495cd7a5743856e3bf0367eacedcd5be586c723bf3f3230370b07849f111244b`


### 147 Couch / Green Comfy
판정: **DEFER_OLIVE_ROLLED_ARM_COUCH_VS_BLUE_BOX_SEGMENT**. 후보: 보류

PZ 형태: PZ 2×1 올리브/카키색 2인 소파. 등받이 윗면과 양쪽 팔걸이가 둥글게 말린 원통형, 하단 짙은 적갈색 받침이 연속됨.

수동 비교: 기존 Macaw Green Couch는 밝은 초록색 직각 1좌석만 보여 2인 완성형과 다르다. Decocraft Couch Left/Right Ocean Blue는 좌우 모듈 구조는 있지만 푸른 색감, 평평한 각진 팔걸이와 등받이로 PZ의 올리브색 롤쿠션·하단 목재 베이스가 없다.

추가 검증: 카키색 rolled-arm 2-seater sofa 실제 Forge 원본 모델과 좌우 연결, 2×1 설치 및 쿠션·목재 베이스 검증.

PZ SHA-256: `00018526572ae4ed5145d4911b6377209bc93a494c90886b5d84d043f91620d7`
MC 모델 SHA-256: `0e36aa9871bc061aa4e7683e7ec69cbb080226280259d47c14f684f23d7b31cc`
비교 이미지 SHA-256: `672a00d39a15ac61789ebec473738f515ca74e251a8ff49ea99278fa1f8cbb6a`


### 148 Low Table / Long
판정: **DEFER_LONG_LOW_BROWN_WOOD_TABLE_VS_GRAY_SLAB**. 후보: 보류

PZ 형태: PZ 2×1 적갈색 긴 낮은 커피테이블. 나뭇결이 있는 두꺼운 직사각 상판, 네 모서리의 짧은 갈색 나무 다리, 하부가 열려 있음.

수동 비교: 기존 Macaw Acacia Coffee Table의 렌더는 회색 낮은 평판만 보여 갈색 나뭇결·다리·2×1 길이가 모두 다름. Decocraft Piano Bench Spruce는 갈색 평판+다리 구조는 있지만 좌판용 좁은 벤치이며 원본 테이블 상판의 폭·길이와 다를 수 있어 검증된 대체가 아님.

추가 검증: 2×1 낮은 원목 직사각 커피테이블 모드 원본/바닐라 조합 검증. 4다리·상판 색·높이·충돌 및 연결 설치 확인.

PZ SHA-256: `fc70983e5ec97e138025635d37b57d86d9049d4dadeeaaa714efcc49dac8309d`
MC 모델 SHA-256: `d09559af32104d7d54228db9f7adddf4129b826ef7a29253ab3cfa1356d5367a`
비교 이미지 SHA-256: `4aca671a4b824d55df6ffb5f7de2ee884c6fd7060b4ee8dfd46d3194d7c616e0`


### 149 Shelves / Lightwood Wall
판정: **DEFER_SINGLE_WALL_WOOD_SHELF_VS_FULL_CABINET**. 후보: 보류

PZ 형태: PZ 1×1 가는 갈색/황토색 원목 판자 하나가 벽에 수평으로 돌출된 벽 선반. 서랍·수직 옆판·뒷판이 보이지 않음.

수동 비교: 기존 Handcrafted Acacia Shelf 네이티브 렌더는 전면에 큰 구멍 두 개가 있는 전체 높이 나무 캐비닛 형태로 원본의 얇은 한 장 선반과 다름. Decocraft Top Cabinet 3 Oak도 두 문이 있는 상부 수납장이라 단순 판자 한 장을 대신하지 못한다.

추가 검증: 바닐라 가문비나무 덫문 또는 Forge 단일 판자 벽 선반 원본 블록모델의 얇기·부착 방향·실제 설치와 충돌을 검증.

PZ SHA-256: `413b1c2d9f8ea115587e37378f2cc198acd7256b323d59f0ee74302204fcc0c7`
MC 모델 SHA-256: `11aea885ce49dcc119ed89ec976019aadae5fc8227f1714efb25dbaf99cb1df3`
비교 이미지 SHA-256: `c049b153aed266af8c0571bcb53dddf9c8c00a946e6c79a1649f24b50ca6d8b1`


### 150 Wardrobe / Fancy White
판정: **DEFER_WHITE_FANCY_WARDROBE_TWO_DOORS_TWO_DRAWERS**. 후보: 보류

PZ 형태: PZ 1×2 조립형 흰색/아이보리 고전식 높은 옷장. 위쪽 큰 두 개의 여닫이 문과 작은 둥근 손잡이, 아래 두 개의 가로 서랍 각각 손잡이 두 개, 상단 장식 몰딩.

수동 비교: 기존 Macaw Acacia Double Wardrobe는 짙은 회색 목재 몸체와 주황 문 두 개가 있는 직각 옷장으로 흰색 몰딩/하단 두 서랍이 없다. Decocraft Bottom Cabinet 2 White는 흰색 수납장 계열이지만 낮은 주방 하부장이라 높은 옷장과 두 서랍 구성에 부적합.

추가 검증: Forge 1.20.1 흰색 2도어 상단+2단 하단 서랍의 장식 옷장 원본 모델 탐색. 1×2 조립·높이·문 개폐·수납 검증.

PZ SHA-256: `d3b4bf03121d8640b35dab30764888eaf9569014d35460a5ac0ea0331d5a327f`
MC 모델 SHA-256: `630ffe7f31d8c5b84a5f112221f8e13d97084f820c76d7312c89a8daccc1e3f0`
비교 이미지 SHA-256: `89ac7d5f2dfdf23b20430e9169765ed0e478534b4def08d696d68af647fe5fd8`


## 산출물

- cards/ : PZ 원본 완성형과 실제 소스 모델(또는 명시적 미검증 화면) 비교 JPG 10장

- BATCH_141_150_MANUAL_VISUAL_REVIEW.csv : 상세 수동 판정, 기존 자동 매칭의 오차, 모델 출처와 SHA

- BATCH_141_150_DEFERRED_OTHER_MODS.csv : 다른 모드·바닐라·신규 모델 후속 검토 목록

- BATCH_141_150_SHA256_PROVENANCE.csv : 원본 PZ/BBMODEL/텍스처/Blockbench 캡처/카드 해시

- MANIFEST.json / BATCH15_STANDALONE_PROGRESS.json : 독립 검수 범위·상태

- INDEX.html : 10개 비교판 탐색

- ROSEWOOD_BATCH_141_150_MANUAL_REVIEW.zip : 카드·CSV·README·인덱스 일괄 보관

원본 게임 TMX/PNG/SQLite와 기존 357종 누적 검수 CSV, 다른 레인 결과를 수정하지 않는다.
