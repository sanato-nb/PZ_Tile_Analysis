# 로즈우드 357종 — 14차 131~140번 원본 가구 개별 시각 검수

131~140 원본 PZ 가구 10종을 독립 검토. Decocraft JAR 원본 BBMODEL/텍스처 33개 렌더 시도 중 33개 Blockbench 5.2.2 소스 이미지 성공. 실제 Minecraft 1.20.1 Forge 게임 설치/충돌/상호작용 테스트 및 1:1 최종 인증은 0건.

조건부 2건, 보류 8건. 11차·12차·13차의 진행 CSV를 덮어쓰지 않기 위해 독립 JSON만 생성.

외부 모드 공식 호환성 자료 10건은 별도 CSV에 보존하며, 해당 모델의 3D 렌더·외형 검증이 완료된 것으로 간주하지 않음.

## 10종 검수 근거

검증된 모드 원본: Decocraft 3.0.4-1.20.1 Forge 1.20.1, JAR SHA-512: f32020fc64170a55afb26fa0ab8a58c6d5d957c97d9e387aa09d107a27737e90f6caafa46bf71b78c01d7b4c283042a88fcf5b8ba3465d0005f4dd6fa0580d05, https://modrinth.com/mod/decocraft/version/K6V6djNF

### 131 Freezer / Chest
판정: DEFER_CHEST_FREEZER_TOP_LID_NOT_VERTICAL_FRIDGE / 제안: 보류

PZ 원본은 높이가 낮고 위로 열리는 크림색 상자형 냉동고이며 상단 금속 걸쇠와 아래쪽 측면 통풍구가 보인다. 기존 Refurbished Dark Freezer 자동 렌더는 검은 앞면과 목재색 측면의 부품 한 개만 나타나 완성형을 확인할 수 없었다. 이번 Decocraft Fridge Small Cream/Silver 모델은 실제 293큐브 완성형이지만 높이 큰 전면 2도어 냉장고라 구조가 완전히 다르다. 비슷한 색이라는 이유로 채택하지 않는다.

후속 검증: MrCrayfish Refurbished/Paladin Freezer 실제 JAR 전체 모델과 PZ처럼 낮은 1×1 상부 힌지형 냉동고를 확인. 입체 크기·상부 열림·기능·설치 방향 검증.

PZ 이미지 SHA-256: `2c4d861a4f6979dc945ecf7ae58d70e2070fa2d19061495a7f58cb349754e70e`
MC 원본 모델 SHA-256: `c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48|c508cf92ce6adedc83b969869ffb0cdf6fe8d006bed6a18a878b5c7e3e1d3a48`

### 132 Fridge / Build-in Trailer
판정: DEFER_BUILTIN_TRAILER_WOOD_ENCASED_FRIDGE / 제안: 보류

PZ 원본은 트레일러 가구와 일체인 작은 은색 냉장고 문 한 장, 양옆 황갈색 목재 프레임, 윗쪽 넓은 나무 상판이다. 기존 Refurbished Dark Fridge 렌더는 분홍색 높은 냉장고의 일부 그래픽으로 원본과 다르다. 이번 Decocraft Small Cream/Silver Open 냉장고는 상하 2도어의 세로형 프리즘이고 내부에 음식이 보이는 열린 상태라 PZ의 낮은 1도어 목재 내장형 가구가 아니다.

후속 검증: Forge 1.20.1 RV trailer built-in fridge/undercounter integrated cabinet 모델 검수. 나무틀과 은색 한 문이 1×1에 동시에 설치되는지, 마크 상판 높이 충돌 확인.

PZ 이미지 SHA-256: `4ebbe997021f29124a3a4fa51d2d983da1b172f16357e24fc70f7ff3c16ac974`
MC 원본 모델 SHA-256: `dfee96207b329ab14fb77976d75f9e0d5f5ca417f23667c5d4c1bb9b78df13b4|bf9b95782244bbae172f2b6a51c8f74bd69c20a463255e888206c9dac14c46d9`

### 133 Chair / Black Fancy
판정: DEFER_BLACK_FANCY_ROUND_BACK_LEATHER_ARMCHAIR_WOOD_LEGS / 제안: 보류

PZ는 짙은 갈색/검정 천 또는 가죽의 부드러운 높은 곡선 등받이, 둥근 쿠션 팔걸이, 밑으로 노출된 가느다란 갈색 목제 다리 네 개를 갖춘 고전식 안락의자다. 기존 Paladin Black Arm Chair는 검정 직각 의자처럼 보여 원본의 다리·곡선 쿠션이 없다. 새 Decocraft Armchair Black/Dark Gray/Leather Brown 원본 모델을 모두 확인해도 각진 등받이·직선 팔걸이·바닥까지 막힌 함체 구조라 핵심 형태가 달라 보류한다.

후속 검증: 1.20.1 Forge wingback/oval high-back club armchair with curved arms and exposed wooden four legs; Skniro's Furniture / [Let's Do] Furniture actual model sources inspect.

PZ 이미지 SHA-256: `fe29584a50d2c6bcc94aca60be4fdc82535124264babfe1f2f4345cfb0818fdf`
MC 원본 모델 SHA-256: `fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28`

### 134 Oven / Green
판정: DEFER_MINT_GREEN_VINTAGE_ENAMEL_OVEN / 제안: 보류

PZ 원본은 녹회색/민트색 에나멜 오븐으로 같은 초록색 굽은 뒷판, 둥근 화구 4개와 전면 조작 노브, 둥근 오븐창이 연결된다. 새 Decocraft Stove는 98큐브 온전한 금속 오븐과 화구는 있으나 완전히 은색/회색이며 위의 화구가 사각형 가스 레인지형이고 초록색 뒷판이 전혀 없다. Decocraft Toilet Mint는 녹색만 비슷하고 변기이므로 가구 종류가 다르다. 실제 같은 녹색 오븐 모델을 찾기 전까지 보류한다.

후속 검증: Forge 1.20.1 green enamel retro oven four round burners and curved backsplash source model search. Beyond The Furnace/JAR variant 검증 및 1×1 조리 기능/충돌 확인.

PZ 이미지 SHA-256: `888f085403e7eec955685cde2151a659929694d36c8fcf4974b15aac81b6fbb1`
MC 원본 모델 SHA-256: `eb82d15603ad7fc4638e06250e5e82a2facfefb760c45af9347c9c7e3c29d30a|e3fdf537b8b1b804ea9ae902026e5804421a5a2b77eab4247299f45cf2e3312f`

### 135 Bed / Simple
판정: DEFER_MINIMAL_SINGLE_BED_NO_HEADBOARD / 제안: 보류

PZ 원본은 나무 4다리와 낮은 평평한 베이스에 무늬 없는 크림색 직사각 매트리스 하나만 얹힌 간단 침대이고, 높은 머리판·발치 울타리가 없다. 이전 Decocraft Bunk Bed Birch Black 렌더는 2층 침대라 명백한 오매칭. 새 Single Bed Oak/Spruce White 실제 BBMODEL은 단층이지만 침대 머리와 발끝에 높은 세로살 목재 울타리와 체크무늬 매트리스/분리 베개가 있어 소박한 원본과 크게 달라; 후보 승인 불가.

후속 검증: Minecraft vanilla white bed or Forge 1.20.1 simple plain unpatterned mattress single cot no headboard/footboard wooden frame 1×2, in-game placement/height verify.

PZ 이미지 SHA-256: `7cc5f7615ba18a54fa39b1cdcbf599d5c7d7812ee2d864c4bb3562709764b5ac`
MC 원본 모델 SHA-256: `21d09a95a29c27508b47e64a8f87542c2fd850b4081aa6c713fd81b14f2ebab7|21d09a95a29c27508b47e64a8f87542c2fd850b4081aa6c713fd81b14f2ebab7`

### 136 Bench / Birchwood
판정: DEFER_BIRCHWOOD_TWO_TILE_BACKLESS_3_STEEL_LEGS_BENCH / 제안: 보류

원본은 2타일 길이의 회갈색 노후 목재 판자 3줄과 바닥에 고정되는 회색 철제 T자 지지대 3개를 가진 등받이 없는 공원 벤치다. 기존 Handcrafted Birch Bench는 빨간 등받이 쿠션이 붙은 1인 의자 부품으로 나와 오매칭. 새 Decocraft Piano Bench Spruce/White는 단일 1칸, 목재 다리 4개, 철제 받침 없는 피아노 의자이고 Picnic Table은 탁자까지 있는 구조여서 정확한 가구가 아니다.

후속 검증: Furnitury 1.20.1 Forge dynamically connecting backless benches original source model 확인. 연결형 2×1 길이, 회색 나무 상판, 중간 지지대·철제 다리 셋이 실제 생성되는지 테스트.

PZ 이미지 SHA-256: `528491024c3d71dc91af672546142c9696aa3d7394a74644a9787185f84f916e`
MC 원본 모델 SHA-256: `d09559af32104d7d54228db9f7adddf4129b826ef7a29253ab3cfa1356d5367a|d09559af32104d7d54228db9f7adddf4129b826ef7a29253ab3cfa1356d5367a|73fffd9416f276aaf0c7f1b97ddabf87b69995a50d22782554cf8597cc1e4332`

### 137 Chair / White Lazy
판정: CONDITIONAL_CREAM_PADDED_LOUNGE_ARMCHAIR / 제안: decocraft:armchair_cream

원본은 누런 크림색 천이 있는 통통한 1인 안락의자, 좌우 두꺼운 팔걸이와 두툼한 좌석 쿠션, 바닥까지 내려오는 스커트형 몸체다. Decocraft Armchair Cream 실제 원본 모델은 크림색, 넓은 팔걸이와 낮은 박스형 본체의 구성이 비슷해 기존 Paladin Oak Chair Classic White (의자 다리 두 개와 분홍 막대만 보이던 불완전 렌더)보다 훨씬 낫다. 다만 마크는 등받이가 높은 각진 평판이고 팔걸이도 직선이며 원본의 부드럽고 둥근 쿠션과 층진 스커트가 없다. 조건부 후보만.

후속 검증: 가구 크기 1×1, 실제 착석 기능 확인. 더 둥근 부드러운 의자 모델과 쿠션 높이·바닥 테두리 비교.

PZ 이미지 SHA-256: `c7b13a1e339e1e6fe8f5ed738d0819f1171da808ab5e697a2c922dac4efc37c3`
MC 원본 모델 SHA-256: `fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|fc06c22b5bdce28a1e6814159462fe258811c7be50308775c1f892377e484c28|34b37379ca11b74db0546d02ca155f7b8047ded9c95debb49e08a1a55380674c`

### 138 Toilet / Low
판정: DEFER_LOW_TOILET_OPEN_BOWL_EXPOSED_FLUSH_POLE / 제안: 보류

PZ Low Toilet는 일반 도기 양변기처럼 큰 물통이 없고, 열린 낮은 둥근 변기 볼 뒤쪽으로 긴 금속 수직 봉과 십자 손잡이·배수 장치가 드러나는 구식 화장실 설비다. 기존 Paladin Basic Toilet은 커다란 사각 물통이 있고, 이번 Decocraft Toilet White/Aqua도 물통과 위로 세워진 뚜껑이 있는 보통 양변기다. 낮은 볼+노출 금속 봉의 모양이 빠져 있어 부적합으로 보류.

후속 검증: Forge 1.20.1 low tankless old-style toilet with exposed chrome metal flush rod and no cistern. Position/height of vertical pole relative to wall and tankless function verify.

PZ 이미지 SHA-256: `adb51e89167eb28777d2d1cfddb9ee56863e1367cb4aadebe51806e2841dd6a1`
MC 원본 모델 SHA-256: `e3fdf537b8b1b804ea9ae902026e5804421a5a2b77eab4247299f45cf2e3312f|e3fdf537b8b1b804ea9ae902026e5804421a5a2b77eab4247299f45cf2e3312f`

### 139 Counter / Floating Trailer
판정: CONDITIONAL_WALL_HUNG_WOOD_TWO_DOOR_TRAILER_CABINET / 제안: decocraft:top_cabinet_3_oak

PZ는 트레일러 내부 벽에 설치된 황갈색 2도어 수납장이고 위에 같은 나무색 상판이 있다. 새 Decocraft Top Cabinet 3 Oak 실모델은 목재 색감, 두 개의 틀 있는 전면 문과 가벼운 낮은 높이, 윗면 나무판이 가까워 기존 Macaw Acacia Counter의 붉은 상판+검은 단색 직육면체 오매칭보다 좋다. 다만 PZ는 각 문에 아래쪽 작은 원형 손잡이가 있고 MC에는 중앙에 긴 은회색 손잡이 하나처럼 보이며 방향/벽 부착·1칸 설치는 검증되지 않았다. 조건부만.

후속 검증: Decocraft Top Cabinet 3 Oak 1×1 wall mount support, door opens, wall clearance and handle direction check; further match wooden double door with separate small knobs.

PZ 이미지 SHA-256: `b8f6f6323a6acb91977e463edb5d7b0cf71dd2d423fbf192f8dacae3f73b5a81`
MC 원본 모델 SHA-256: `11aea885ce49dcc119ed89ec976019aadae5fc8227f1714efb25dbaf99cb1df3|7f877b0cbcab9da65406016859bc5974e3167d33afdec027d232d435ce291611|512f252cb22f035ad901daef97a208680f8e57b67f47b250318dd05151e87c1b`

### 140 Couch / Blue Comfy
판정: DEFER_BLUE_COMFY_TWO_TILE_ROLLED_ARM_BOLSTER_COUCH / 제안: 보류

PZ는 탁한 남청색 패브릭 두 칸 소파로 양끝에 둥근 말린 팔걸이가 있고 등받이 위쪽도 긴 원통형 쿠션이 연결되는 형태다. 기존 Macaw Blue Couch는 밝은 파란색 직각 1좌석만 렌더되어 완성형 2칸 근거가 없다. 새 Decocraft Couch Left/Right Ocean Blue와 Light Blue를 실제 BBMODEL로 각각 렌더해 2모듈 구성은 확인했지만 모두 박스형 평평한 등받이, 직선 팔걸이이고 원본 둥근 롤쿠션·어두운 색감이 다르다. 게임에서 실제 접속도 확인되지 않았으므로 보류.

후속 검증: [Let's Do] Furniture Forge 1.20.1 gray-blue two-seat couch and 2×1 rolled-arm soft sofa models inspect; in-game left+right connection and armrest/cushion source shading verify.

PZ 이미지 SHA-256: `6185bc7772f720f85e5a2bc8fa65b9845559cf296d02964543084770156d9bb2`
MC 원본 모델 SHA-256: `0e36aa9871bc061aa4e7683e7ec69cbb080226280259d47c14f684f23d7b31cc|9681b0789bf07ad97494ac57e0e48e955dd0bb8076db55fb7ab6a5006f3d2fa5|0e36aa9871bc061aa4e7683e7ec69cbb080226280259d47c14f684f23d7b31cc|9681b0789bf07ad97494ac57e0e48e955dd0bb8076db55fb7ab6a5006f3d2fa5`

## 출처·검증 범위

- PZ: 기존 B42 원본 Tiles PNG 및 TMX/.tiles 기반 조립 미리보기 (시각 조립은 잠정이며 인게임 모델이 아님)

- Minecraft: 검증된 Decocraft Forge 1.20.1 JAR에서 BBMODEL과 선택 텍스처를 읽어 원본 해시를 기록하고 Blockbench 5.2.2 데스크톱 화면 캡처

- 원본 모드 JAR, 텍스처 및 BBMODEL 자체는 재배포하지 않음. 비교 이미지·해시·출처만 보관.

- 실제 마인크래프트 설치 시 방향, 크기, 멀티블록, 충돌/상호작용은 별도 테스트 전까지 승인하지 않음.

## 파일

- cards/ : 131~140 원본 PZ 대 Minecraft 원본 모델 비교 10장

- BATCH_131_140_MANUAL_VISUAL_REVIEW.csv : 상세 10종 및 SHA-256

- BATCH_131_140_DEFERRED_OTHER_MODS.csv : 보류 후속 목록

- BATCH_131_140_OTHER_MOD_RESEARCH.csv : 공식 Forge 1.20.1 호환성 링크 (모델 미검증)

- BATCH14_STANDALONE_PROGRESS.json : 병렬 작업 충돌 방지 독립 진행 상태

- INDEX.html : 비교 이미지 열람기

- MANIFEST.json : 범위 및 검증 수치

- ROSEWOOD_BATCH_131_140_MANUAL_REVIEW.zip : 전체 결과
