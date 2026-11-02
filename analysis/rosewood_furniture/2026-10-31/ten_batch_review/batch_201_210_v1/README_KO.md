# 로즈우드 가구 20차 201~210번 개별 시각 검수

PZ B42 원본 완성형 미리보기 10장과 이전 Minecraft 원본 Blockbench 비교판 10장을 실제로 육안 검수했다. 별도 GitHub Actions는 Decocraft 3.0.4-1.20.1 Forge 원본 BBMODEL/텍스처를 검증한 뒤 Blockbench 5.2.2로 새로 렌더해 추가 대조한다.

이전 B 레인 141~150 및 171~180번은 별도 Draft PR로 보존했으며, 이번 201~210번만 독립 검수했다. 다른 레인과 원본 파일은 건드리지 않았다.

원본 Decocraft JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05 | https://modrinth.com/mod/decocraft/version/K6V6djNF

검수 10종: 조건부 1종, 보류 9종. 네이티브 Blockbench 캡처 8/8개 모델. 비교 JPG 10장. 인게임 1:1 확정 0종.

일부 원본 스프라이트의 SpriteGridPos 조립과 마크 모델의 동적 블록 상태는 잠정이다. 1×1/2×1/1×2 점유·방향·충돌·상호작용·색상/재질은 인게임 미검증. 부분 모델 캡처는 완성형으로 승인하지 않는다.

## 개별 근거

### 201 Fireplace / 
판정: **DEFER_NO_SOURCE_AUTHENTIC_FIREPLACE_MODEL**. 후보: 보류

PZ 형태: 벽면에 매립된 어두운 회색 직사각형 화실, 검은 내부 개구부, 낮은 회색 하부 받침판. 1×1 단일 타일로 보이나 벽면 결합 및 돌출 폭은 미측정.

수동 비교: PZ 원본 완성형을 직접 확인했으며 기존 357종 비교판에는 실제 Minecraft 모델이 없고 'MOD FURNITURE NOT VERIFIED'로 표시된다. 원본 자산을 확인하지 않은 상태에서 벽난로 모델을 임의 지정하지 않는다.

추가 검증: Forge 1.20.1용 매립형 검정 벽난로의 실제 모델/텍스처 및 벽 결합, 화재 기능, 충돌 검증.

PZ SHA-256: `11fdbb86805f70991edc49e1ca146c0e00c474799a5695375702730262582ce4`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `18d8223d7c2481f910b8082e64f2960436044300205a2bb7b8a4b3537c7c96c9`


### 202 Oven / Large Modern
판정: **DEFER_STAINLESS_DOUBLE_OVEN_VS_BRICK_PIZZA_OVEN**. 후보: 보류

PZ 형태: 2×1 회색 스테인리스 대형 오븐, 전면 상하 2개의 검은 유리문과 왼쪽 세로 조작 패널, 매끈한 금속 상판 및 낮은 다리.

수동 비교: PZ 원본은 은색 스테인리스 2단 전기 오븐과 전면 검정 유리문 2개·좌측 조작 패널이다. 공식 Blockbench 5.2.2에서 실제 Decocraft pizza_oven BBMODEL 31 cubes를 다시 렌더해 확인했으나 붉은 벽돌 화덕, 높은 벽돌 굴뚝, 둥근 입구와 불꽃, 삽이 있는 완전히 다른 장치다. 2×1 점유와 전기 오븐 기능도 일치하지 않아 보류.

추가 검증: 두 개의 독립 오븐문과 금속 상판을 가진 2블록 폭 산업용 전기 오븐 모델 및 조리 상호작용.

PZ SHA-256: `6eef0cefd8f283c0b774a7bd5a294e5a1fbc6a336d2e41f87f1968a14064968c`
MC 모델 SHA-256: `9ab500f2281f0c8c6a96ef3da9d65f60faab6b6c5a1c764d82cc0f64d7a10bcb`
비교 이미지 SHA-256: `aecc2a90b8d222beeec2fe0ba7caf52fcd682c8aca5e8ced42cb8b6bf3bc8503`


### 203 Table / Large Dark
판정: **DEFER_DARK_RECTANGULAR_TABLE_VS_TABLE_SETTING**. 후보: 보류

PZ 형태: 2×1의 넓은 짙은 회갈색 직사각형 평판 상판과 네 모서리의 얇은 검정 사각 다리, 별도 식기 없음.

수동 비교: 기존 decocraft:table_setting_double 렌더는 접시·컵·수저만 있는 식기 장식이다. 새로 실제 Blockbench에서 diner_table_black(12 cubes)을 열어 보니 어두운 직사각 상판은 유사하지만 은색 테두리와 중앙 단일 금속 받침/넓은 발판이며 PZ의 짙은 목재 상판·네 모서리 가는 다리와 다르다. wooden_table_oak(25 cubes)도 네 다리 구조는 있으나 밝은 참나무 정사각 상판과 굵고 장식적인 다리로 PZ의 2×1 짙은 긴 테이블과 다르다.

추가 검증: 어두운 2블록 길이 4다리 식탁 원본, 양 끝 연결부·회전 및 바닥 충돌 검증.

PZ SHA-256: `53928ba8a32f9a1d356ca1519eeab6559428c77fda32e83bf5374d6b2e9cab02`
MC 모델 SHA-256: `9be049c262802b52e979df0933aa4b93fee3a6d3bdad79d4060c747a80ce75ce`
비교 이미지 SHA-256: `5d2dc2f31c89631b3fdd77681d40ce7789e44d97528270f19999cbb8b6b831c7`


### 204 Chair / Makeshift
판정: **DEFER_ROUGH_PLANK_CHAIR_VS_LEATHER_ARMCHAIR_PARTIAL**. 후보: 보류

PZ 형태: 거친 갈색 목재 널빤지로 만든 낮은 임시 의자, 판자 좌판, 짧은 수직 등받이, 겹친 판재 받침대, 팔걸이 없음.

수동 비교: 기존 pfm:arm_chair_leather 네이티브 캡처는 회색 판 한 장만 보이는 부분 모델이다. 새 Decocraft school_chair_gray 원본 BBMODEL 37 cubes를 Blockbench로 렌더한 결과 얇은 회색 금속 네 다리, 평평한 금속 좌판과 분리된 회색 등받이의 교실 의자다. PZ의 두꺼운 거친 목재 널빤지 좌판, 판재 바닥 받침 및 짧은 판자 등받이와 형태·재질·높이가 불일치.

추가 검증: 원목 널빤지/팔레트로 제작된 낮은 등받이 의자, 1×1 바닥 점유 및 앉기 동작.

PZ SHA-256: `d18cd84fec5da7615c57cf4eed2a908d709168104067ee426d345ecc9fe17593`
MC 모델 SHA-256: `10b356207b2641cf3b2ffeb46973e647c94631c85ddad80d392240464139e2d1`
비교 이미지 SHA-256: `bed3e6222a2818e3930c53d037f8b47e0e3eb542d1ab017b63430864e803987f`


### 205 Shelves / Zippee Wall
판정: **DEFER_TWO_FLOATING_WHITE_RED_SHELVES_VS_ACACIA_CABINET**. 후보: 보류

PZ 형태: 벽에 분리 설치된 얇고 긴 흰색/은색 선반판 2개, 각각 붉은 전면 테두리, 지지 기둥과 수납 상자는 보이지 않음.

수동 비교: 기존 handcrafted:acacia_shelf의 실제 Blockbench 렌더는 두 개의 검은 개구부가 있는 두꺼운 적갈색 박스형 캐비닛이다. PZ의 개방형 얇은 2단 흰색 벽 선반과 재질·색상·깊이·부착 구조가 다르다.

추가 검증: 벽부착형 얇은 흰색 선반 두 개와 붉은 전면 립을 가진 실제 모델, 수평 길이 및 벽면 배치 확인.

PZ SHA-256: `ac85a0252529b07956ae7137f0b69dbbf84e987774aaf5aa5e80f695db12d4a5`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `12cc9be3c15902aff62faf28beef7c515359352ec880df2557554c40734bd78e`


### 206 Table / Lightwood Trailer
판정: **DEFER_BEIGE_ROUNDED_TRAILER_TABLE_VS_PARTIAL_GLASS_TABLE**. 후보: 보류

PZ 형태: 1×2의 연한 베이지색 길고 모서리가 둥근 직사각형 상판, 중앙 아래로 내려오는 두 개의 가느다란 회색 금속 지지 다리.

수동 비교: 기존 mcwfurnitures:acacia_glass_table 네이티브 캡처는 얇은 나무판 한 장만 보이는 부분 렌더다. 새 Decocraft kitchen_table_oak BBMODEL 29 cubes는 흰색 상판과 밝은 참나무의 굵은 4다리 식탁으로 확인했다. PZ는 베이지색 모서리 둥근 1×2 길이 상판과 중앙 금속 기둥 2개이므로 상판 색·모서리·다리 수·재질·길이 모두 불일치.

추가 검증: 연베이지 라운드 1×2 상판 + 중앙 금속 2다리 테이블의 실제 2블록 결합 모델.

PZ SHA-256: `e9314089eea00fce56f9dfaeb6dcf824abbbd1e900c54c6cfad5578489788c8f`
MC 모델 SHA-256: `014cf39af640f4120c32def0d1fbb27511bc7f14dfef1be3c82fabfbe6a06deb`
비교 이미지 SHA-256: `4c676990d630e926abf242d41e1e59ff525921a19eee5d1d50c3cfee6e3a3e8d`


### 207 Barbecue / Jorge Foreguy
판정: **CONDITIONAL_PROPANE_GRILL_SIMILAR_BODY_SIDE_SHELVES_BUT_WHEELS_LID_DIFFER**. 후보: decocraft:grill_black

PZ 형태: 검정 직립 가스 바비큐, 밝은 은색 둥근 뚜껑, 양옆 짙은 갈색 목재 보조 선반, 오른쪽 작은 바퀴, 검정 프레임과 하단 공간.

수동 비교: 기존 refurbished_furniture:black_grill 캡처는 부분 소스만 보여 완성형 근거가 없다. 새로 Decocraft grill_black 원본 BBMODEL 70 cubes를 Blockbench 5.2.2로 열어 확인하니 검정 가스그릴 몸체, 양쪽 갈색 목재 보조 선반, 회색 프레임, 하부 선반이 PZ와 구조적으로 유사하다. 그러나 Minecraft는 뚜껑이 열린 검정색이며 내부 음식과 가스통이 보이고, PZ는 은회색 닫힌 둥근 뚜껑과 측면 바퀴가 있으며 Decocraft 화면에는 바퀴가 보이지 않는다. 따라서 1:1 승인 없이 조건부 후보만 유지한다.

추가 검증: Minecraft 1.20.1 Forge 실제 설치에서 grill_black의 뚜껑 닫힌 상태/회전/바퀴 여부/1×1 배치/충돌·요리 기능 확인. PZ 은색 뚜껑·바퀴가 없으면 다른 모드 후보 또는 커스텀 모델 필요.

PZ SHA-256: `cdd0e84ddd7fc01714ba3488b6b52debbab5cbba7834e04ae5f5d18b694fe68d`
MC 모델 SHA-256: `403c49a6c6fadaf3de8a0159b39e6e791cefc8a0e6523ced695365348154e215`
비교 이미지 SHA-256: `f65cd2e9b55de644f56868c4ed9cab7a721359b8656e0236037059cae4b7b98a`


### 208 Chair / Modern Red
판정: **DEFER_RED_PADDED_DINING_CHAIR_VS_PARTIAL_OAK_FRAME**. 후보: 보류

PZ 형태: 붉은 쿠션이 있는 둥근 상단 등받이와 붉은 두꺼운 좌판, 가늘고 어두운 네 다리, 팔걸이 없는 1×1 식탁 의자.

수동 비교: 기존 pfm:oak_chair_classic_red의 Blockbench 캡처는 갈색 수직 막대 2개와 연녹색 가로막대 1개뿐이며 빨간 쿠션·좌판·등받이가 없다. 부분 소스 로딩으로 보이므로 외형 일치 판정에 사용할 수 없다.

추가 검증: Forge 1.20.1 빨간 천 쿠션 4다리 식탁 의자의 전체 소스 모델·텍스처 및 앉기 기능 검증.

PZ SHA-256: `f371bec9a3c3c7db44cf695e4f20fe24c3e3a779f7c3c4983144bb5bdb9c5b50`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `8afe2544e8d297aa193f9cac16233a4ca59addc22d77cfa3fa3b6184aeb4e4dd`


### 209 Chair / Yellow Modern
판정: **DEFER_YELLOW_UPHOLSTERED_ARMCHAIR_VS_PARTIAL_FROGGY_PANEL**. 후보: 보류

PZ 형태: 넓은 겨자색 1인 패브릭 소파/암체어, 두꺼운 양쪽 팔걸이와 둥근 쿠션 등받이, 노란 좌판, 매우 낮은 검은 네 다리.

수동 비교: 기존 pfm:froggy_chair_yellow 네이티브 캡처는 노란 평판 한 장뿐이다. 새 Decocraft bamboo_chair_yellow BBMODEL 30 cubes의 실제 렌더는 노란빛 대나무/라탄 짜임 좌판, X자 등받이, 높은 나무 네 다리, 팔걸이 없는 개방형 의자다. PZ의 두꺼운 겨자색 패브릭 팔걸이·쿠션 등받이·낮은 다리 1인 소파와 전혀 다르다.

추가 검증: 겨자색 통쿠션 양팔걸이 소파형 1인 의자, 1×1 크기·앉기 기능·낮은 다리 검증.

PZ SHA-256: `5a762daa58a1faeb8902b186259a59d299bfb006f2afb8fc7ac7f1998200dac6`
MC 모델 SHA-256: `1f80d17a5abc4ef1a5d175f0532819bfd89054e414b4f1c921f0f643443dcb1b`
비교 이미지 SHA-256: `3a349a5ab420c2e524eb025652f5edf15f5cb3aa8cf18ca8fcf2c40fa7e8dfa0`


### 210 Counter / Dark Corner
판정: **DEFER_DARK_WOOD_L_COUNTER_VS_STRIPED_DINER_CORNER**. 후보: 보류

PZ 형태: 1×1 짙은 갈색 목재 L자형 코너 카운터, 평평한 상판 안쪽에 직각 홈/모서리, 전면은 문 없는 어두운 목재 패널.

수동 비교: 실제 Decocraft diner_counter_corner_black BBMODEL 11 cubes를 공식 Blockbench 5.2.2로 재렌더한 결과, 검정색 본체에 흰색/은색 가로 줄무늬가 반복되고 전면 모서리가 둥글게 꺾이는 다이너 카운터다. PZ는 어두운 갈색 나뭇결, 장식 없는 평평한 상판과 직각 안쪽 홈이 있는 L자 목재 코너다. 색·재질·모서리 및 인접 카운터 연결이 달라 보류.

추가 검증: 짙은 목재 L자 코너 1×1 카운터 실제 모델, 양측 직선 카운터 연결과 코너 회전/충돌 검증.

PZ SHA-256: `44f4fd5b2d57275aadc241738e96db7f45694044911ad10fdc5c8b1e3f87b051`
MC 모델 SHA-256: `25ef3b784df0de583daad5bbf2d506ceeeadb62db760d80521b8cff7860de13a`
비교 이미지 SHA-256: `814f740683fe078fb31b80369459d9d7b79f8a130f9e5ac3237a355d3bdec61f`


## 산출물

- cards/ : PZ 원본 완성형과 실제 소스 모델(또는 명시적 미검증 화면) 비교 JPG 10장

- BATCH_201_210_MANUAL_VISUAL_REVIEW.csv : 상세 수동 판정, 기존 자동 매칭의 오차, 모델 출처와 SHA

- BATCH_201_210_DEFERRED_OTHER_MODS.csv : 다른 모드·바닐라·신규 모델 후속 검토 목록

- BATCH_201_210_SHA256_PROVENANCE.csv : 원본 PZ/BBMODEL/텍스처/Blockbench 캡처/카드 해시

- MANIFEST.json / BATCH21_STANDALONE_PROGRESS.json : 독립 검수 범위·상태

- INDEX.html : 10개 비교판 탐색

- ROSEWOOD_BATCH_201_210_MANUAL_REVIEW.zip : 카드·CSV·README·인덱스 일괄 보관

원본 게임 TMX/PNG/SQLite와 기존 357종 누적 검수 CSV, 다른 레인 결과를 수정하지 않는다.
