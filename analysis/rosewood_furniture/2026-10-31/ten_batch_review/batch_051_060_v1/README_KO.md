# 로즈우드 357종 — 6차 051~060번 완성 가구 수동 재검수

이번 10건은 PZ 1~4개 스프라이트가 만드는 완성 가구를 확인한 뒤 Minecraft Decocraft 1.20.1 Forge의 원본 .bbmodel + PNG 후보 25종을 Blockbench 5.2.2에서 렌더링하여 판정함.

조건부 대안 4개, 다른 모드/바닐라 후속 검토 6개. 동일 기능·형태 1:1 최종 인증 0. 기존 357 원자료, PZ PNG, SQLite/TMX는 변경하지 않음.

## 개별 판정

- **051 Dark Round Table / ** → decocraft:diner_table_round_black | CONDITIONAL_ROUND_TRIPOD_MATERIAL_MISMATCH. PZ는 진갈색 목제 원형 상판+중앙 기둥과 갈라진 다리다. 실제 Decocraft Diner Table Round Black(21 cubes)은 원형/중앙 기둥/삼발이 구조가 비슷하지만 검정 상판·회색 금속 지지대여서 목재 재질은 불일치. Bamboo Round Yellow는 노란 4다리 격자라 하부형태가 더 멀다. 기존 Macaw 모델은 정사각 두꺼운 석판처럼 렌더되어 반려.

- **052 Table / Large Simple** → 정확한 후보 미발견 | DEFER_LONG_TABLE_TWO_TILE_IRON_TRESTLES. PZ는 길이 2칸 밝은 나무 높은 테이블, 철제 검정 접이식 가대형 다리이다. 새 Cottage Coffee Table Long은 단색 어두운 갈색이고 높이가 낮고 얇은 나무다리라 형태/재질/높이가 전부 달라 정답으로 승인하지 않는다. 기존 Decocraft Table Setting Double은 아예 접시·컵 세트였으므로 완전 반려.

- **053 Low Table / Fancy** → decocraft:cottage_coffee_table | CONDITIONAL_LOW_DARK_WOOD_TABLE. PZ는 어두운 갈색 모서리 가공 상판과 바깥으로 휘는 네 다리가 있는 작은 낮은 탁자. 새 Cottage Coffee Table 실제 원본 33 cubes 모델은 목재 색감·낮은 상판·네 다리 형태가 유사해 기존 Macaw 회색 두꺼운 석판보다 낫다. 다만 원본은 더 작고 다리는 더 장식적이므로 정확한 일치가 아니다.

- **054 Box / Battered Cartboard** → 정확한 후보 미발견 | DEFER_DENTED_TAPED_CARDBOARD_BOX. PZ는 찌그러진 옅은 갈색 종이박스로, 테이프와 찢어지거나 구겨진 윗부분이 중요하다. 기존 Refurbished Mail Box는 불완전한 큰 목제 기둥 형태로 아예 종류가 틀리다. 실제 Decocraft 25개 후보 목록에는 닮은 종이상자가 없어서 우측에 없는 모델의 가상 렌더를 만들지 않는다. Forge 1.20.1 호환 Cardboard box 모드와 Shipping은 배포처 확인까지만 했다.

- **055 Bed / Large Oak** → decocraft:double_bed_oak_white | CONDITIONAL_FULL_WHITE_DOUBLE_BED_WITH_FOOTBOARD. PZ 원본은 큰 연한 참나무 침대 틀에 연속된 흰 침구, 등받이는 넓은 수평 나무판, 발치에는 낮은 나무 프레임. Decocraft Oak White는 36 cubes로 정상 렌더되며 원목 프레임·흰 침구는 가까우나 흰 회색 체크 패턴, 분리된 베개, 세로살 머리판·발치 난간이 원본과 명확히 다르다. 기존 매칭은 조건부였으나 외형을 재평가해 조건부 유지.

- **056 Oven / Modern** → decocraft:stove | STRONG_VISUAL_CONDITIONAL_FOUR_BURNER_OVEN. PZ는 4개의 검은 둥근 화구·은회색 오븐 본체·전면 제어 노브·검정 오븐창·높은 검정 뒷판을 가진다. Decocraft Stove 실제 98큐브 모델은 4구 상판·노브·은회색 전면/검정 창을 모두 갖춰 기존 Paladin Gray Stove의 단일 막대 누락 모델보다 훨씬 정확하다. 다만 화구는 사각 격자, 검정 뒷판 생략, 손잡이/도어 높이 차이. 게임에서 요리 기능은 별도로 확인해야 한다.

- **057 Bin / Wheelie** → 정확한 후보 미발견 | DEFER_GREEN_WHEELED_WASTE_BIN. PZ는 초록색 긴 본체, 상단 양쪽 덮개, 뒤쪽 손잡이와 밑바퀴 2개가 있는 이동식 쓰레기통. 기존 Refurbished recycle bin은 회색 일반 통으로 뚜껑/바퀴가 없고 부품도 불완전하다. 새 Decocraft Pedal Trash Can은 직육면체에 덮개는 있으나 회색이며 작은 바닥 페달뿐이어서 колес wheelie bin과 전혀 다름. Skart's Decorations 0.3 1.20.1 Forge에 Wheelie Bins 추가 이력이 있으나 모델 ID/초록 변형 실제 렌더 필요.

- **058 Chair / Grey Plastic** → 정확한 후보 미발견 | DEFER_GREY_MOLDED_PLASTIC_CHAIR. PZ는 한 몸체로 굽어진 회보라 플라스틱 좌석과 등받이, 가운데 손잡이 구멍, 검정 얇은 금속 다리. 새 Diner Chair Gray는 색상과 금속다리가 비슷하나 등받이가 납작한 사각판에 굵은 흰 줄무늬가 있고 구멍이 없다. School Chair Gray도 판형 등받이와 금속 직선다리라 동일한 성형 의자가 아니다. 기존 PFM Gray Arm Chair는 안락의자 블록 형태로 구조 불일치.

- **059 Bench / Park** → 정확한 후보 미발견 | DEFER_TWO_TILE_WOODEN_PARK_BENCH. PZ는 목제 2줄 등받이+긴 이중 나무판 좌석+얇은 갈색 철제 받침다리로 구성되는 길쭉한 공원 벤치다. 기존 Decocraft Gym Bench는 헬스장 운동 기구였고 새 Piano Bench Spruce는 등받이도 없고 폭도 1칸인 피아노 의자라 둘 다 불합격. Just Outdoor Stuffs는 1.20.1 Forge 지원과 2인 벤치 기능까지 공식 소개에서 확인됐지만 실제 모델과 PZ처럼 2칸인지 아직 확인하지 않았다.

- **060 Drawers / Fancy** → 정확한 후보 미발견 | DEFER_WHITE_WOODEN_THREE_DRAWER_DRESSER. PZ는 크림 흰색 목제 3단 서랍장이며 서랍마다 검정 동그란 손잡이 2개(총 6개). 새로운 Decocraft Filing Cabinet White는 실제 렌더에서 3단이긴 하나 흰 철제 문서 보관함으로 각 서랍마다 긴 금속 손잡이와 라벨 칸이 있다. Modular Desk Drawers White는 흰색 목제에 가깝지만 2단만 있어 둘 다 완성형으로는 맞지 않는다. 기존 Macaw BookShelf Drawer 렌더는 초록 판 한 장이라 무효.

## 외부 모드 검증 전까지 보류

054 찌그러진 종이상자: Cardboard Box 1.20.1 Forge(https://modrinth.com/mod/cardboard-box), Shipping(https://modrinth.com/mod/shipping). 공식 배포 확인됐으나 모델 로드/찌그러진 외형 검증 전.

057 초록색 바퀴 달린 쓰레기통: Skart's Decorations Wheelie Bins 1.20.1 Forge(https://www.curseforge.com/minecraft/mc-mods/skarts-decorations/files/5112417) 모델·녹색 변형 필요.

059 등받이 있는 목재 2인 공원 벤치: Just Outdoor Stuffs 1.20.1 Forge(https://modrinth.com/project/6hCfRrRD) 및 Blockables Chairs bench with back (https://modrinth.com/mod/movables-chairs/) 후보 형태 검증 전.

052 긴 2칸 금속다리 테이블, 058 손잡이 구멍 플라스틱 의자, 060 아이보리 3단 6개 손잡이 서랍장은 현 후보와 구조 차이가 커서 보류.

바닐라 대안은 장식적 배치 가능성만 제안하고 실제 블록 설치/충돌·2칸 크기 검증 전에는 매칭 완료 처리하지 않음.

## 진행

전체 36묶음 중 6묶음(001~060) 개별 검수 / 총 60/357. 나머지 30묶음 QUEUED. 다음 구간은 061~070.

## 파일

- INDEX.html 및 cards/: 왼쪽 PZ 완성 가구와 오른쪽 원본 Minecraft 모델 또는 검증된 대체품 미발견 상태를 분리한 10종 비교 카드

- BATCH_051_060_MANUAL_VISUAL_REVIEW.csv: 10건 개별 속성·기존 후보·새 후보·원본 모델 SHA-256·형태·크기·보류 이유

- BATCH_051_060_DEFERRED_OTHER_MODS.csv: 후속 검색 6종

- BATCHES_ALL_357_PROGRESS.csv: 누적 36묶음 진행 현황

- 새로운 25개 원본 Blockbench 모델 렌더는 ten_batch_review/06_051_060/extra_decocraft_render/에 별도 저장.
