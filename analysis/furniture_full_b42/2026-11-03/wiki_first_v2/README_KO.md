# B42 전체 가구 원장 v2 — PZwiki 기반 + 원본 TileDef 전체 연결

## 정확한 기록 단위

이 DB는 게임에서 실제로 구분하는 2,231개 고유 가구라고 주장하지 않아. PZwiki 가구 목록의 원문 행 1,268개와, 위키 어떤 행에도 연결되지 않은 B42 원본 TileDef 그룹 963개를 합한 **검증 가능한 목록 항목 2,231개**야.

위키 1,268행 중 1,257행에 대해 이미지 파일명의 원본 타일 ID를 연결했고, 11행은 위키 표에는 존재하지만 이미지 ID가 없어 미연결로 보존. 전체 원본 가구 후보의 1,852개 그룹 중 889개 그룹을 위키와 연결했고 963개는 원본 단독 후보로 남아 있어.

원본 타일의 모든 속성은 동일 SQLite 안의 source_attributes(195,265행)와 furniture_tile.raw_properties_with_source_json에 보존돼. 61,418개 원본 키 전체는 source_slots에서 찾을 수 있어.

## 사실과 추론의 구별

- WIKI 목록에 실린 이름/분류/자료: 위키 원문 출처로 확인됨. Wiki에 있다는 사실을 게임 내 동일한 객체 인증과 혼동하면 안 됨.

- EXACT_WIKI_IMAGE_SPRITE_KEY: 위키 이미지 파일명에 나오는 특정 TileSet/LocalID가 원본 TileDef에 존재함. 원본 타일 ID 문자열 근거는 직접 확인.

- SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED: 같은 타일셋 CustomName+GroupName인 방향/부품 타일을 추가로 연결한 상태. 동일 물체인지, 별도 변형인지 추가 검토.

- B42_SOURCE_ONLY: 위키 이미지가 연결되지 않은 원본 TileDef의 타일 그룹. 바닥재, 간판, 장식물 등의 비가구가 포함될 수 있으므로 개별 시각 분류 필요.

- WIKI_ONLY_NO_ID_FROM_IMAGE: 위키 원문은 있으나 대응 원본 타일 ID가 없음. 11건을 임의의 타일에 연결하지 않았음.

## 가구 속성 및 아이템 생성

registry_entry_tile로 가구 항목에서 모든 관련 타일의 Facing/SpriteGridPos/원본 출처 파일을 찾을 수 있어. 전체 속성은 furniture_tile 및 source_attributes에서 쿼리 가능.

registry_entry_container에는 타일별 container/ContainerCapacity/ContainerPosition을 기록해. 같은 2칸짜리 책장에 여러 타일이 각각 컨테이너를 갖는 경우 이를 함부로 합치지 않아.

실제 아이템 생성은 방 종류 및 컨테이너 종류의 Lua 규칙이 필요하므로 registry_item_rule_source와 기존 future_item_distribution는 비워둠. 창고에 책이 들어간다고 허위 기록하지 않아.

Minecraft 구현 방식(Block 또는 Entity)은 결정하지 않고 향후 연결 테이블도 비워둠.

## 주요 산출물

- PZ_B42_FURNITURE_REGISTRY_WIKI_FIRST.sqlite: 전체 원본 v259 TileDef/PNG 소스와 v1 관계, Wiki 우선 새 테이블 및 검토 큐를 포함.

- WIKI_FIRST_ALL_CATALOG_ENTRIES.csv: PZwiki 목록+추가 B42 원본 가구 항목, 각각 정확히 한 행.

- WIKI_CONFIRMED_LISTINGS.csv: 위키에 등재된 1,268항목(그중 11항목 원본 타일 ID 미연결).

- WIKI_SOURCE_ONLY_UNLISTED_GROUPS.csv: 위키에 연결되지 않은 963개 B42 원본 그룹(전부 가구로 확정 아님).

- FURNITURE_ENTRY_ALL_LINKED_TILE_IDS.csv: 모든 항목별 원본 타일 ID, 타일별 수납 속성, 정확한 ID와 그룹 확장 연결의 차이.

- FURNITURE_ENTRY_STORAGE_ATTRIBUTES.csv: 가구의 타일별 수납 유형과 용량, 아이템 분포는 미수집.

- FURNITURE_ENTRY_DIRECTION_PARTS.csv: 해당 항목의 출처별 방향·부품 구성 후보.

- FURNITURE_IDENTITY_REVIEW_QUEUE.csv: 같은 그룹을 두 위키 행이 공유할 때 등의 위험과 검토 사유.

## 향후 검증

위키와 소스 타일 ID의 정확한 연결을 유지하면서, 실제 게임 가구로 간주할 정확한 경계와 방향/부품/색상 변형을 검수해야 해. 사용자 목표는 게임에서 정의된 모든 가구/설치물에 대한 DB 완성이며, 이 작업의 원본 가구 후보 선별은 아직 완전성을 인증하지 않아.

원본 정의·위키·이전 DB·이미지·GitHub 브랜치를 덮어쓰지 않고 별도 분석 산출물로 보존.
