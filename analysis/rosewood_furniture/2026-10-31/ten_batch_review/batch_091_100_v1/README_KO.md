# 로즈우드 357종 — 10차 091~100번 실제 가구 매칭 개별 시각 검수

PZ B42 원본 완성 가구 10종의 형상/모델 구성/원본 속성 및 크기 vs Minecraft Java 1.20.1 Forge Decocraft 원본 BBMODEL 31개를 Blockbench 5.2.2로 실제 열어 비교. 31개 시도 중 30개 정상 원본·텍스처 해시 및 실제 3D 렌더 인증, diner_counter_yellow 1개는 실패해 판단 증거 제외.

조건부 후보 5건(091,093,096,098,100), 부적합/미검증 5건(092,094,095,097,099). 1:1 인증 0, 마크 인게임 설치·충돌·기능 인증 0. PZ 원본 PNG/357 자동 결과/TMX/SQLite 변경 없음.

## 개별 이미지 판정

- **091 Television / Antique** → decocraft:tv_old | STRONG_VISUAL_CONDITIONAL_ANTIQUE_WOODEN_TELEVISION. PZ 원본은 1960년대 나무 프레임, 다리 네 개, 윗면 V자 토끼귀 안테나, 전면 왼쪽 화면과 오른쪽 세로 조절부가 있는 골동품 TV다. Decocraft TV Old 원본 30큐브 모델을 실제 Blockbench로 열었더니 나무 프레임/다리/V 안테나/측면 전면 조절 노브가 모두 나타나 기존 Decocraft CRT TV(검정 플라스틱 상자)보다 훨씬 정확하다. 다만 원본 화면은 어둡고 버튼은 세로로 더 작고, MC 모델의 나무톤이 조금 더 진하고 안테나 막대 굵기/각도 차이가 있어 최종 1:1은 아니다.

- **092 Counter / Generic Shop** → 정확한 후보 미발견 | DEFER_GENERIC_SHOP_PLAIN_LIGHT_WOODEN_COUNTER. PZ는 상판과 몸체 모두 밝은 황갈색이며 앞면에 서랍·문·손잡이가 없는 매끈한 상점용 1칸 카운터다. 기존 Macaw Acacia Counter는 상판만 주황빛, 몸체는 어두운 회색/검정이라 다름. 새 Decocraft Bottom Cabinet 1 Birch/Oak는 목재 몸체는 더 가깝지만 흰 상판과 서랍 1개+손잡이 달린 아래 문이 노출되어 원본 단순한 앞판과 불일치. Diner Counter Yellow는 배포 모델 존재는 확인했지만 이 실행에서 렌더 검증 실패하여 비교 증거로 사용하지 않음.

- **093 Bed / Fancy** → decocraft:single_bed_black_white | CONDITIONAL_SINGLE_BLACK_WOOD_WHITE_BED_CHECKER_MISMATCH. PZ는 두 개 타일의 검정 금속/목재 세로살 침대 프레임(머리판·발판)과 무늬 없는 크림빛 흰 침구로 구성된다. 기존 Decocraft Birch Black은 밝은 원목 프레임+검정 체크 침구로 색이 거꾸로였다. 새 Single Bed Black White 실제 29큐브 모델은 검정 세로살 머리판·발판, 흰 침구, 좁은 1인 침대 구조가 명확하게 일치하는 방향이다. 하지만 MC 침구가 흰 회색 체크무늬이고 커다란 흰 베개와 접힌 담요가 돌출돼, PZ의 매끈한 단색 매트리스와 차이. 1×2 타일 점유 역시 게임에서 미검증.

- **094 Light Round Table / ** → 정확한 후보 미발견 | DEFER_LIGHT_WOOD_ROUND_TRIPOD_TABLE. PZ는 밝은 나무 원형 상판 아래 갈색 중심 기둥 1개와 작게 뻗은 세 발이 있는 테이블. 기존 Macaw Acacia Coffee Table는 회색 사각 두꺼운 상판만 렌더돼 구조가 틀렸다. 새 Decocraft Bamboo Round Yellow는 밝은 노란 원형 상판이지만 높이가 낮고 옆면 십자 격자와 4개의 바깥 다리가 둘러싸기 때문에 기존 삼발이 목재 원형 식탁이 아니다. Diner Round Yellow도 금속 기둥+노란 플라스틱 상판이라 목재색과 다름.

- **095 Round Table / ** → 정확한 후보 미발견 | DEFER_ORANGE_WOOD_ROUND_TRIPOD_TABLE. PZ Round Table은 094와 구조가 거의 같지만 상판이 더 오렌지빛 갈색이며 다리도 같은 갈색 나무다. 기존 Macaw 회색 판은 유사성이 없다. 새 Decocraft Diner Table Round Yellow는 원형 상판·세발 받침이라는 기본 실루엣은 유사하지만 판은 노란 플라스틱이고 다리·기둥은 은회색 금속이라 원본 목재 재질과 오렌지톤이 맞지 않는다. 정확히 같은 가구로 승인하면 안 된다.

- **096 Drawers / Mirror And** → decocraft:vanity_left_birch | CONDITIONAL_MIRRORED_BIRCH_VANITY_DRAWER_COUNT_MISMATCH. PZ 원본은 나무 서랍장(3단, 서랍당 검정 원형 손잡이 2개) 위에 곡선 상단의 세로 거울이 붙은 한 덩어리 화장대다. 기존 Macaw Bookshelf Drawer는 녹색 벽 판만 나온 부품 누락이고 거울이 없다. 새 Decocraft Vanity Left Birch의 실제 20큐브 원본 모델은 연목색 프레임, 큰 거울, 서랍 본체가 모두 일체형이어서 물건 유형을 올바르게 맞췄다. 다만 2단 서랍에 은색 긴 손잡이 하나씩이라 PZ의 3단/검정 손잡이 6개와 불일치, 거울 상단도 다각형이다. 더 닮은 모델을 찾기 전까지 조건부.

- **097 Low Table / White** → 정확한 후보 미발견 | DEFER_LOW_SMALL_WHITE_RECTANGULAR_TABLE. PZ는 흰색/아이보리 낮은 사각 테이블로 윗판과 짧고 단순한 네 다리만 있다. 이전 Decocraft Bedside Table Open 1 White는 실제 파일에서 갈색 2단 서랍장이 펼쳐진 모습이라 전혀 다른 가구. 새 Decocraft Wooden Table White는 아이보리색 상판/네 다리는 있지만 **높이가 식탁급이고 굵은 장식 다리**가 있어 원본 낮은 테이블과 다르다. Cottage Coffee Table은 낮지만 짙은 갈색, Bamboo Square Yellow는 노랑 라탄 격자라 불일치.

- **098 Toaster / Small Chrome** → decocraft:toaster_silver | STRONG_VISUAL_CONDITIONAL_SILVER_COMPACT_TWO_SLOT_TOASTER. PZ는 손바닥만한 은회색 크롬 빵 토스터이며 윗면에 평행한 2개의 투입 슬롯, 둥근 모서리, 어두운 받침/측면 손잡이가 있다. 기존 Refurbished Dark Toaster의 불완전 검정 상자 렌더보다, 새 Decocraft Toaster Silver의 진짜 14큐브 원본은 은색 몸체·위 2개 슬롯·받침·모서리 깎임이 일치해서 외형이 상당히 근접한다. 그래도 PZ는 전면 좌하단 둥근 패널이 있고 MC는 각진 윗모서리라 완전 1:1은 아니며 설치 위치·음식 굽기 기능 확인 전.

- **099 Chair / Pile o' Crepe** → 정확한 후보 미발견 | DEFER_ORANGE_WOOD_CHAIR_SINGLE_HORIZONTAL_BACKREST. PZ 식당 의자는 선명한 주황 갈색 나무 좌석/다리 네 개와 등받이에 하나의 가로 나무대가 걸친 구조다. 기존 PFM Leather Armchair 렌더는 회색 한 판뿐이었고 팔걸이부터 물건 종류가 잘못되었다. Decocraft Chair 1 Cherry는 나무 4다리 형태는 맞지만 전체가 옅은 분홍빛이고 등받이에 여러 세로살이 있어 핵심적인 주황 나무색/가로대 1개와 다르다. School Chair Orange는 색상은 비슷하지만 주황 플라스틱+회색 금속 다리여서 재질이 다르고 Diner Chair Orange는 흰 줄무늬 플라스틱이라 불가.

- **100 Table / Picknic** → decocraft:picnic_table | STRONG_VISUAL_CONDITIONAL_CONNECTED_PICNIC_TABLE_BENCHES. PZ 원본은 2×2 네 개 타일을 합쳐야 하는 나무 피크닉 테이블로 양쪽에 긴 좌석 두 개가 붙고 비스듬한 프레임 다리로 지지된다. 이전 Macaw Glass Table 렌더는 얇은 나무 평판 한 장이라 완전히 틀린 가구였다. 이번 Decocraft Picnic Table **실제 22큐브 BBMODEL을 전체 렌더**했더니 나무 상판+양쪽 2개 벤치+A형 경사 받침대가 함께 나타나 **완성형 전체 구조가 매우 유사**하다. 다만 PZ는 녹색 도색 금속/목재 다리인 데 반해 MC는 전부 밝은 목재이고 상판 판자 수·다리 색이 다르며, 2×2 칸을 차지하는지는 마크 게임에서 아직 검증하지 않았다. Benched 모드에도 2×2 실용 피크닉 벤치가 공식적으로 있으므로 추가 대안으로 남김.

## 새로운 후보 및 추가 검증 조건

100 Picnic Table: Decocraft 'picnic_table' 실제 22큐브 원본 Blockbench 모델에서는 완성된 상판과 양쪽 벤치+A형 프레임 확인. https://modrinth.com/mod/benched 공식 자료에도 Forge 1.20.1 호환 2×2 Bench가 있다고 명시됨. 현재 Benched 개별 자바 소스 모델은 이 패키지에서 아직 렌더링하지 않았고, Decocraft 모델의 2×2 실제 설치도 확인 전이다.

091 Antique Television: Decocraft 'tv_old' 실제 30큐브 원목 TV+V 안테나+조절 노브+4다리. 이전 'crt_tv'는 플라스틱 검정 모니터라 정확하지 않다.

093 Fancy Bed: Decocraft 'single_bed_black_white'는 1인용 검정 슬랫 프레임과 흰 침구가 맞지만 MC 체크 이불과 돌출 베개는 PZ와 다르다.

096 Mirror and Drawers: Decocraft 'vanity_left_birch' 원본 모델은 거울+2단 서랍 일체형, PZ는 거울+3단 각 2개 손잡이여서 조건부; 단순 거울이나 서랍장만 설치하는 대안은 최종 승인하지 않는다.

098 Chrome Toaster: Decocraft 'toaster_silver' 진짜 14큐브 모형에서 은색 둥근 корпус과 두 슬롯 확인; 카운터 위 설치 및 사용 기능 미검증.

092 Generic Shop Counter: 기존 Macaw Counter는 큰 어두운 원통처럼 보이고 Decocraft 'bottom_cabinet_1_birch'는 흰 상판·서랍/문이 있어서 빈 판넬과 같은 계열 상판을 가진 PZ와 불일치. 실패한 diner_counter_yellow는 정상 렌더 수에 포함하지 않음.

094/095 나무 원형 삼발이: Decocraft 카페 금속 다리/뱀부 라탄 장식과 재질·지지 구조 차이가 커서 보류.

097 흰색 낮은 테이블: 기존 Decocraft 협탁은 서랍장, 새 White Wooden Table은 식탁 높이와 장식 다리로 높이 차이.

099 오렌지 목재 4다리 의자: 새 Cherry Chair는 분홍색 여러 세로살, Orange School Chair는 플라스틱/금속이라 원본의 단순 가로대+오렌지 원목 구조 부적합.

## 진행 현황 및 파일

총 36묶음 중 10개(001~100) 총 100/357개 원본 가구 스타일 개별 검수 완료. 26묶음 QUEUED. 다음 101~110.

- INDEX.html 및 cards/: PZ 완성 가구 이미지·원본 Blockbench 모델 좌우 비교 10개

- BATCH_091_100_MANUAL_VISUAL_REVIEW.csv: 원본 타일/기존 후보/신규 렌더 후보/소스 해시/형태·크기·작동 판정

- BATCH_091_100_DEFERRED_OTHER_MODS.csv: 5건 후속 다른 모드/바닐라 검색 목록

- BATCHES_ALL_357_PROGRESS.csv: 누적 36묶음 작업 현황

- ten_batch_review/10_091_100/extra_decocraft_render/: 전체 시도 31개 중 source-backed native Blockbench 30개 검증, 실패 1개.

- 게임 실제 설치 및 인게임 화면 캡처가 아니라 원본 BBMODEL을 Blockbench로 열어 렌더링한 자료. 모드 JAR 원본 파일 자체는 재배포하지 않는다.
