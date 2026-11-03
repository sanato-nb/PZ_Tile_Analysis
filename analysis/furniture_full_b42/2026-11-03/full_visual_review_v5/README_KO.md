# B42 원본 58개 그룹 실제 이미지 검수 완료 (v5)

### 작업 범위

기존 11그룹에 더하여 47그룹의 원본 PNG 접촉시트를 추가로 직접 확인하고 총 58그룹/357개 Wiki 행을 근거별로 정리했어.

원본 TileDef 61,418 고유 키, source_slots 73,644행 및 속성 195,265행, 전체 PZwiki 1,268행을 SQLite에 보존했어.

원본 PNG에서 추출한 셀 368개와 58장 접촉시트는 v4 경로에 그대로 남아 있으며, v5의 모든 검수 CSV는 v4 이미지 상대경로와 원본 ID를 연결해.

### 가장 중요한 구분

- **가구의 방향**: Wooden Bench (2부품×N/W), Large Metal Trough (3부품×N/W), Office Desk (2부품·Facing E/S)는 실제 원본 Facing/SpriteGridPos 참고.

- **같은 Wiki 이름의 다른 3D 형태**: Rain Collector Barrel의 원형 통과 사각형 통, Road Cone의 낮은 주황 콘과 높은 줄무늬 표지봉, Ornamental Bush의 원뿔형과 구형을 분리.

- **상태 변형**: Metal Drum 불꽃·내용물, Raised Plantbed의 식물 성장/빈 흙, Ficus/Dragon Tree/Chinese Evergreen/Snake Plant/Cast Iron Plant의 잎 시듦 상태.

- **부품/패턴**: 러그 가장자리와 중앙 조각, Flowerbed 테두리 및 꽃 색상, Air conditioner의 별도 팬·환기 그릴.

- **가구와 구분해야 하는 맵 요소**: Trash 51개는 쓰레기 잔해/오버레이, Windows는 건축 설비, 타일/카펫은 바닥 재질.

- **위키 명명 주의**: Red Carpet은 원본 그림에 매우 다양한 색상·무늬가 포함되므로 위키 기본 이름만으로 모두 같은 텍스처라고 처리하면 안 돼.

### 시각·기능 범주별 그룹 수

- FLOOR_DECOR: 17

- ARCHITECTURAL_WINDOW: 6

- POTTED_PLANT: 5

- FLOOR_SURFACE: 4

- CRAFTING_DEVICE: 3

- GARDEN_DECOR: 3

- STORAGE_CONTAINER: 3

- FARM_PROP: 2

- OUTDOOR_PROP: 2

- PLUMBING_OR_FARM_FIXTURE: 2

- APPLIANCE_COMPONENT: 1

- CRAFTING_FIXTURE: 1

- DEBRIS_OVERLAY: 1

- DECORATIVE_PROP: 1

- DISPLAY_MANNEQUIN: 1

- DISPLAY_PROP: 1

- OFFICE_FURNITURE: 1

- OUTDOOR_VEGETATION: 1

- PLANTER_FIXTURE: 1

- SEATING_FURNITURE: 1

- TABLE_FURNITURE: 1

### 생성한 파일

- B42_ALL_58_VISUALLY_REVIEWED_FURNITURE.sqlite — v4 전체 DB + 새 v5 직접 검수 그룹(58), Wiki 행(357), 명칭 계열(66) 관계형 테이블.

- V5_ALL_58_ACTUAL_SOURCE_PNG_GROUP_VISUAL_REVIEWS.csv — 58그룹 원본 이미지 관찰 기록·취급 방식.

- V5_ALL_357_WIKI_ROWS_WITH_FACING_STORAGE.csv — 357개 위키 행의 원본 타일 ID, Facing, SpriteGridPos, container, ContainerCapacity.

- V5_ALL_66_FAMILY_VISUAL_AND_DIRECTION_REVIEWS.csv — 66계열의 방향 근거·부품 여부·시각 관계.

- V5_NEW_47_DIRECT_VISUAL_OBSERVATIONS.csv — 이번에 새로 직접 검수한 47그룹의 관찰 기록 원본.

- MANIFEST.json — 검증된 집계 및 보존·미구현 상태.

### 검수 범위와 한계

총 58개 그룹 **원본 PNG의 외형을 직접 봤음**. 이것은 게임의 Moveable 오브젝트 1:1 동일성, 실제 모델 3D 형상, 모든 아이템 분포를 검증한 것과 달라.

특히 외형상 동일해 보여도 서로 다른 게임 내부 오브젝트일 수 있어. 따라서 위키 항목 병합과 마크 Block/Entity 선택은 계속 보류해.

기존 v4 그림 58장 및 원본 PNG를 변경하지 않았어.
