# Project Zomboid B42 전체 가구 원장 (최초 DB)

목표: 모든 원본 가구 스프라이트/방향/부품/속성을 보존해 후속 Minecraft 맵 변환에 사용.

가구를 Block/Entity로 만들지는 아직 결정하지 않았다.

## 원본이 보존된 범위

- 원본 TileDef의 61418개 고유 타일 키, 원본 source_slots 73644행, 원본 source_attributes 195265행과 PNG 격자 47796행을 SQLite에 그대로 보존.

- 위키 1268행 원문 JSON, 이미지 링크, 위키 항목에서 지목된 원본 타일 ID, 가구별 명칭/크기/수납 정보.

- 속성 또는 위키 원본 ID로 연결된 가구 후보 타일: 8219개.

- 잠정 가구 그룹: 1863개. 이는 실제 고유 가구 디자인 수가 아님.

## 원본 정보와 추정값 구분

- furniture_tile: 각 타일의 모든 원본 속성값과 그 값이 기록된 source_file 정보.

- furniture_group: 같은 타일셋의 CustomName+GroupName 기준 잠정 그룹. 무명 타일은 ID별로 보존.

- furniture_direction_parts: Facing 방향과 SpriteGridPos 부품 좌표. 타일 중복/방향 누락은 REVIEW 상태.

- furniture_container_source: container, ContainerCapacity, ContainerPosition. 원본 그대로 보존.

- furniture_function_property: 수납/가전/물/기타 기능 관련 원본 속성값.

- wiki_furniture/wiki_image_tile/wiki_group_candidate: PZwiki 원문 1268행과 원본 타일 ID 후보 관계.

- rosewood_357_3d_bridge: 기존 로즈우드 357 검수와 Viewpoint 3D 참조를 연결. 공식 객체 ID 보증은 아님.

- future_map_placement, future_item_distribution, future_minecraft_implementation: 의도적으로 비움. 데이터 근거 확보 뒤 작성.

## 중요

61,418개 원본 타일 모두가 가구인 것은 아니다. 타일 속성이 부실하거나 위키에 없는 가구도 남아 있을 수 있다. 전체 원본 61,418개는 보존하되 가구 후보 자동 선별은 실물 가구 판정이 아니다.

같은 CustomName+GroupName이라도 구조가 다를 수 있고, 다른 이름이 같은 디자인일 수도 있다. 방향·부품을 임의로 합쳐 확정하지 않는다.

Item distribution을 구현하려면 별도 원본 Lua 분포와 맵 방 유형을 연결해야 한다. 아직 수납 내용물 생성 규칙을 추정하지 않았다.

## 출력물

- B42_FURNITURE_ALL_SOURCE.sqlite: 원본 전체 자료 + 가구/방향/속성/위키 관계형 DB.

- FURNITURE_GROUPS.csv: 잠정 가구 그룹과 연결된 모든 타일 ID.

- FURNITURE_TILES_AND_ATTRIBUTES.csv: 원본 타일/방향/그룹/수납 속성.

- FURNITURE_DIRECTIONS_AND_PARTS.csv: 방향·구성 부품 기록.

- FURNITURE_FUNCTION_PROPERTIES.csv: 기능 관련 속성.

- ALL_PZWIKI_1268_LINKED.csv: 전체 위키 가구 행 매핑.

- MANIFEST.json: 실제 작업 범위와 검증 수치.

- PZ_B42_FULL_FURNITURE_DB.zip: SQLite DB 포함 통합 압축본.
