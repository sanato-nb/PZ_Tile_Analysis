# 로즈우드 가구 17차 161~170번 개별 시각 검수

이번 검수는 PZ B42 완성형 미리보기와 이전 실제 Minecraft 원본 모델 Blockbench 비교판을 먼저 수동 관찰하고, 별도 GitHub Actions에서 Decocraft 3.0.4-1.20.1 Forge의 실제 BBMODEL/텍스처를 검증 후 Blockbench 5.2.2로 새로 렌더한 화면을 추가 대조한다.

이전 131~140번은 PR #254에서 이미 검수되어 재작업하지 않았다. 141~150번은 레인 B, 151~160번은 레인 C에 속하므로 건드리지 않았다.

원본 Decocraft JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05 | https://modrinth.com/mod/decocraft/version/K6V6djNF

검수 10종: 조건부 2종, 보류 8종. 네이티브 Blockbench 캡처 9/9개 모델. 비교 JPG 10장. 인게임 1:1 확정 0종.

일부 원본 스프라이트의 SpriteGridPos 조립과 마크 모델의 동적 블록 상태는 잠정이다. 1×1/2×1/1×2 점유·방향·충돌·상호작용·색상/재질은 인게임 미검증. 부분 모델 캡처는 완성형으로 승인하지 않는다.

## 개별 근거

### 161 Hamster Wheel / Human
판정: **CONDITIONAL_TREADMILL_STRUCTURE_COLOR_MISMATCH**. 후보: decocraft:treadmill

PZ 형태: PZ 이름은 Human Hamster Wheel이지만 실제 완성 스프라이트는 회색 전동 러닝머신. 1×2 길이의 검은 벨트, 은회색 바닥 프레임, 상단 콘솔과 양측 손잡이, 뒤로 기울어진 두 기둥.

수동 비교: PZ 완성형과 Decocraft Treadmill 원본 BBMODEL 모두 러닝 벨트·전면 콘솔·좌우 손잡이·지지대가 있는 같은 가구 유형이다. 다만 PZ는 은회색 프레임/검정 벨트, Minecraft는 거의 전체가 검정이고 콘솔과 벨트 비례가 다르다. 기존 Casino Wheel 자동 후보는 가구 종류 자체가 달라 반려한다. 구조가 가까운 조건부 대안만.

추가 검증: Minecraft Forge 1.20.1에서 실제 1×2 점유·방향·충돌·작동 가능 여부 확인, PZ 회색 프레임과 콘솔 비율에 가까운 다른 러닝머신 검토.

PZ SHA-256: `4135ffc3ec498dd4125357fded34d5d789ebe768dbc29196bcf04636c241d14c`
MC 모델 SHA-256: `655b1bab9b4c990bf5dd3cb261053ca0981b7d809d233009f84a096f1b609599`
비교 이미지 SHA-256: `5b24991ebd6ace2807108b2e5722bf2703be47b7a29cd16703f22db23862b34b`


### 162 Locker / Blue Wall
판정: **DEFER_TWO_DOOR_VS_ONE_DOOR_BLUE_LOCKER**. 후보: 보류

PZ 형태: PZ 파란색 두 개의 좁은 금속 사물함 문이 하나의 1×1 완성형으로 조립되어 있다. 각 문 상하 통풍구와 가운데 작은 검정 매립 손잡이, 좁은 전체 깊이.

수동 비교: Decocraft Locker Blue 실제 원본은 색과 금속 캐비닛 높이, 통풍구는 비슷하지만 큰 문 하나, 긴 외부 손잡이 하나, 상단 이름표가 있다. PZ의 두 개 문과 각 매립 손잡이 구조가 빠져 있다. 동일한 1×1 블록에 두 문을 표현할 수 있는지 확인 전까지 보류.

추가 검증: Forge 1.20.1 실제 원본 3D 모델 중 two-door blue school locker, paired doors/2 narrow compartments with vents를 탐색하고 1×1 설치 확인.

PZ SHA-256: `9c96ac42c06aee5128c6b4658c2ee2910e47403e56ea5e27605a0ae1646e6db6`
MC 모델 SHA-256: `8ddf3e9c5a059754877afbb4f01624583f4557d70da5d11b471f29cf0c8a79b7`
비교 이미지 SHA-256: `15305507f18d6d3611f54a2c321b042307d5f2d05669e04e7cafd5dfe977f6bb`


### 163 Bench / Sturdy
판정: **DEFER_WOOD_UPHOLSTERED_LONG_BENCH_VS_GYM_BENCH**. 후보: 보류

PZ 형태: PZ 1×2 긴 낮은 목재 직육면체 벤치에 어두운 갈색 쿠션 좌판, 한쪽 긴 면을 따라 올라온 밝은 목재 판자형 등받이/측판이 있다.

수동 비교: PZ는 긴 밝은 목재 외장·갈색 쿠션·한쪽 긴 측판이 있는 1×2 벤치다. 실제 Decocraft Gym Bench BBMODEL(7큐브) Blockbench 화면은 검정색 금속 운동기구의 왼쪽 일부만 나타나며, 긴 나무 외장과 등받이/쿠션이 없다. 화면 밖 잘림 또는 원본 모델의 파트 누락 가능성까지 있어 완성형 대체로 인증할 수 없다.

추가 검증: 1.20.1 Forge 원본 모델에서 2블록 길이의 light wood box upholstered bench with brown cushion and wood back panel 검색. 조립·좌석 높이 확인.

PZ SHA-256: `74b3dda73173b8254f33048808066447c31de7cb23df0a92e4f478356fec3491`
MC 모델 SHA-256: `80de203fee5ce870e3934b0061a6fa0aff397748fc501a2131e2d913173ae632`
비교 이미지 SHA-256: `153be5113a9d28a1a2b22662c62041323886b976bba5b6a21b04d65abe85a4e2`


### 164 Bench / Foot
판정: **DEFER_LOW_METAL_FOOT_BENCH_VS_GYM_BENCH_PART**. 후보: 보류

PZ 형태: PZ 1×1 낮은 직사각 회색 평판 상판, 양쪽에 얇은 검정 금속 U자형 프레임 다리. 등받이와 쿠션 없음.

수동 비교: PZ는 회색 평판 상판과 두 개의 가느다란 검정 금속 U자 프레임으로 된 1×1 낮은 발받침이다. Decocraft Gym Bench 원본 7큐브 렌더는 검은 체육기구의 한쪽만 나타나 회색 상판·U자 지지대 두 개와 맞지 않는다. 163번 목재 벤치와 동일 MC ID를 부여한 자동 매칭은 형태를 구분하지 못한 오류다.

추가 검증: Forge 1.20.1 낮은 1×1 metal frame foot bench / rectangular footstool 원본 3D 렌더 비교. 프레임 두께·높이 확인.

PZ SHA-256: `31e0ae9d521db3d24329a71f2b1f9ccd6133deb1194a68d90dcbf70ff8dd8778`
MC 모델 SHA-256: `80de203fee5ce870e3934b0061a6fa0aff397748fc501a2131e2d913173ae632`
비교 이미지 SHA-256: `0356b96180af35eb6112eed397f74e43e10debd300330017f9328622ae15542e`


### 165 Desk / Lightwood
판정: **DEFER_LIGHTWOOD_TWO_PANEL_DESK_VS_INCOMPLETE_DARK_SLAB**. 후보: 보류

PZ 형태: PZ 2×1 밝은 베이지 목재 사무용 책상. 길고 평평한 상판, 양 끝 넓은 세로 목재 판자 다리 두 개, 하단 중앙은 열린 공간. 서랍이 보이지 않는다.

수동 비교: PZ는 2×1 밝은 목재의 긴 책상으로, 서랍 없는 평판 상판과 양 끝 두 개의 넓은 판자 다리가 보인다. 기존 Macaw Acacia Covered Desk 자동 캡처는 검은 수직 판자 하나만 보여 불완전하다. 새로 원본 Decocraft Modular Desk Drawers Oak BBMODEL(50큐브)을 Blockbench로 렌더했더니 작은 1×1 목재 서랍장(전면 은색 손잡이 두 개)이며 긴 상판·양끝 판자 다리·열린 하부 공간이 전혀 없다. 따라서 새 후보도 반려한다.

추가 검증: 원본 BBMODEL 전체 책상 형태와 2×1 설치 크기 확인, 서랍 없는 light oak slab-legged office desk 또는 2블록 조합 찾기.

PZ SHA-256: `1db397815eebe494ca74e773d52e821c5f76dd54756614185a4a0ba3f1d3a5b4`
MC 모델 SHA-256: `14a5ddcaebae394d1e9f0b4543e5144b70d35ae298521a77b6c45fc0df6622b1`
비교 이미지 SHA-256: `3e663eae7310c6979cc59c536ee4d17a44beb8e66a0c08d31ca983eeb75e6b3a`


### 166 Sink / Large Industrial
판정: **DEFER_INDUSTRIAL_SPRAYER_SINK_VS_INCOMPLETE_BASIC_SINK**. 후보: 보류

PZ 형태: PZ 1×1 스테인리스 산업용 깊은 사각 싱크볼, 네 개의 얇은 금속 다리와 아래 격자 선반, 높게 구부러진 스프링형 분무 호스와 수전.

수동 비교: PZ는 스테인리스 산업용 독립 싱크대(깊은 금속 볼, 4개의 금속 다리, 아래 철제 선반, 높게 굽은 스프링 분무 호스)다. 기존 Paladin Basic Sink 부분 렌더는 노란 수평판만 나타났다. 새로 Decocraft Kitchen Sink Silver 원본 BBMODEL(23큐브)을 실제 렌더한 결과 흰색 도기 사각 싱크와 짧은 고정형 수전만 있으며 금속 4다리·하부 선반·산업용 호스가 없다. 색·재질·구조가 달라 반려한다.

추가 검증: Forge 1.20.1 commercial stainless steel prep sink with tall flexible sprayer and open lower wire shelf 실물 모델 찾기, 물 사용 기능·설치 검증.

PZ SHA-256: `b3db975a38a01ce064e7ecf4800865e2708d846b68f6921daf4fb467b556f34a`
MC 모델 SHA-256: `e4ccda4a967c34a64b9803ef4d86dbf4573c9f87f12d85eb151b2fc80df103b8`
비교 이미지 SHA-256: `9fdf3bfc7b43b34cacbb8ff69c868ee74c921e3c37372aad017db363404e8256`


### 167 Stool / Piano
판정: **CONDITIONAL_WOOD_PIANO_BENCH_WITH_FOOTPRINT_RISK**. 후보: decocraft:piano_bench_spruce

PZ 형태: PZ 2×1 낮고 긴 적갈색 피아노 스툴, 등받이 없는 직사각 평평한 목재 좌판, 4개의 가늘고 긴 적갈색 다리.

수동 비교: 기존 Macaw Acacia Stool Chair 캡처는 얇은 상판만 보여 다리 4개와 완성형 벤치 구조가 누락됐다. Decocraft Piano Bench Spruce의 실제 원본 Blockbench 화면은 등받이 없는 짙은 갈색 평판 좌판과 네 개 목재 다리를 완전하게 보여 PZ와 외형 종류가 유사하다. 그러나 PZ는 2×1이며 Minecraft 모델의 실제 설치 길이/좌판 비율과 색감은 다를 수 있어 조건부만.

추가 검증: Decocraft 피아노 벤치 실제 2×1 점유 또는 여러 개 배치 시 이음새 검증, PZ 적갈색 색감·좌판 높이·좌우 폭 확인.

PZ SHA-256: `42be814cc8f375ac201bb8d5d5530b4f8200aea29eb763fbcdb9340a983f9db3`
MC 모델 SHA-256: `d09559af32104d7d54228db9f7adddf4129b826ef7a29253ab3cfa1356d5367a`
비교 이미지 SHA-256: `141bf7c0544bebbfe9dc6b5bf258e9ffb05f5c4e3092b3ac129ff58f53d79606`


### 168 Bed / Blue
판정: **DEFER_BLUE_PLAIN_MATTRESS_VS_CHECKED_BED_WITH_FOOTBOARD**. 후보: 보류

PZ 형태: PZ 2×1 침대는 짙은 갈색 평판 헤드보드 하나, 가는 목재 다리 4개, 베개·무늬 없이 매끈한 푸른 회색 매트리스.

수동 비교: Decocraft Single Bed Birch Blue 실제 BBMODEL은 같은 단층 침대이고 파란 이불이 있지만 높은 세로살 머리판과 발치 울타리, 흰 베개와 체크무늬 짙은 남색 이불을 포함한다. PZ의 단순한 민무늬 회청색 매트리스와 평판 머리판/발치 무울타리 구조가 달라 색상 유사만으로 승인하지 않는다.

추가 검증: Minecraft 바닐라 파란 침대 또는 Forge 1.20.1 flat wooden headboard bed with plain blue-gray mattress, no footboard, 2×1 배치 확인.

PZ SHA-256: `c96349f38c0667856d20d2b6597defb13a6b9d674c4ff0112c544a66d25967de`
MC 모델 SHA-256: `21d09a95a29c27508b47e64a8f87542c2fd850b4081aa6c713fd81b14f2ebab7`
비교 이미지 SHA-256: `9d26a74498cd5c1abf7a3a8bc87a046deeabd492258e0233a158fe84ecb571ed`


### 169 Fridge / Green
판정: **DEFER_GREEN_RETRO_FRIDGE_VS_PARTIAL_PINK_DARK_FRIDGE**. 후보: 보류

PZ 형태: PZ 1×1 연한 민트/세이지 초록색 빈티지 독립 냉장고. 위 작은 냉동칸과 아래 큰 냉장칸, 각 왼쪽 경첩과 가는 검은 문 손잡이.

수동 비교: 기존 Refurbished Dark Fridge Blockbench 캡처는 분홍색 측면과 검은 전면의 일부 그래픽으로만 보이며 PZ의 초록색 두 문 냉장고 완성형을 보여주지 못한다. Decocraft Small Cream은 두 칸 구조만 비슷하고 색이 크림색이며 PZ의 레트로 곡면과 경첩/손잡이 위치가 달라 보류.

추가 검증: Forge 1.20.1 sage green retro two-door fridge 실제 원본 텍스처/BBMODEL 검증. 상하문 분리·기능·1×1 높이 확인.

PZ SHA-256: `099c5a8da66d279cf460366c9e0cf912b877a8d7b44be47bed48e2627a28ea72`
MC 모델 SHA-256: `c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48`
비교 이미지 SHA-256: `7ccc50c0b90ea6e59648c67f5c1ca2ab75f677256a412f15009abb294e2dc1b6`


### 170 Industrial 2000 / Fryers Club
판정: **DEFER_NO_SOURCE_INDUSTRIAL_DEEP_FRYER**. 후보: 보류

PZ 형태: PZ 1×1 산업용 스테인리스 이중 튀김기. 위에 나란한 사각 튀김조 2개, 전면 검정 컨트롤 패널과 작은 조작 다이얼, 높은 금속 뒤판과 네 개 금속 다리.

수동 비교: 기존 7개 모드 JAR의 자동 매칭 결과에는 검증된 실제 Minecraft 모델이 없다. 이름 Industrial 2000을 일반 오븐으로 대체하면 깊은 튀김조·배수/온도조절 패널·산업용 다리 구조가 사라지므로 후보를 임의 생성하거나 승인하지 않는다.

추가 검증: Forge 1.20.1 restaurant commercial double deep fryer / kitchen equipment mod에서 원본 모델 및 텍스처와 실제 블록 ID 확보, 없으면 Minecraft 스타일 Blockbench 신규 모델 제작 검토.

PZ SHA-256: `4086b218273fe211c1756a880c11a047157fda581b11e16958b27bf43a85ec4e`
MC 모델 SHA-256: `미검증`
비교 이미지 SHA-256: `41cdd836866c65bc6be03fd7aa0e99c7f506db559dc582df200f2f8af561976b`


## 산출물

- cards/ : PZ 원본 완성형과 실제 소스 모델(또는 명시적 미검증 화면) 비교 JPG 10장

- BATCH_161_170_MANUAL_VISUAL_REVIEW.csv : 상세 수동 판정, 기존 자동 매칭의 오차, 모델 출처와 SHA

- BATCH_161_170_DEFERRED_OTHER_MODS.csv : 다른 모드·바닐라·신규 모델 후속 검토 목록

- BATCH_161_170_SHA256_PROVENANCE.csv : 원본 PZ/BBMODEL/텍스처/Blockbench 캡처/카드 해시

- MANIFEST.json / BATCH17_STANDALONE_PROGRESS.json : 독립 검수 범위·상태

- INDEX.html : 10개 비교판 탐색

- ROSEWOOD_BATCH_161_170_MANUAL_REVIEW.zip : 카드·CSV·README·인덱스 일괄 보관

원본 게임 TMX/PNG/SQLite와 기존 357종 누적 검수 CSV, 다른 레인 결과를 수정하지 않는다.
