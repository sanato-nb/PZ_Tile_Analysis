# B42 가구 원장 v9 — 원본 정의 우선 근거 검수

원본 정의로 확인할 수 있는 가구 종류·타일 ID·Facing·SpriteGridPos·수납 속성을 먼저 분리한 DB야. 기존 v2 원본 2,231행 및 195,265 속성을 보존했고, v8 이미지 검수 129그룹은 출처/범위만 계승했어.

## 미연결 위키 항목 11건

- PZW-0808 Painting: COLLECTION_HEADING_NOT_SINGLE_SPRITE; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-0876 Decorations: COLLECTION_HEADING_NOT_SINGLE_SPRITE; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-0938 Ominous Sign (variant 2): VARIANT_IMAGE_MISSING; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-0944 Signs: COLLECTION_HEADING_NOT_SINGLE_SPRITE; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-0950 Spiffos Logo Large Sign: SPECIFIC_ITEM_IMAGE_MISSING; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-0951 Spiffos Sign: SPECIFIC_ITEM_IMAGE_MISSING; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-1060 Flowerbed (variant 12): VARIANT_IMAGE_MISSING; 원본 이름 후보 1그룹, 정확 ID 추가 없음

- PZW-1072 Flowerbed (variant 24): VARIANT_IMAGE_MISSING; 원본 이름 후보 1그룹, 정확 ID 추가 없음

- PZW-1231 Green Canopy: SPECIFIC_ITEM_IMAGE_MISSING; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-1237 The Glorious Spiffo: SPECIFIC_ITEM_IMAGE_MISSING; 원본 이름 후보 0그룹, 정확 ID 추가 없음

- PZW-1258 Deer Hide: SPECIFIC_ITEM_IMAGE_MISSING; 원본 이름 후보 0그룹, 정확 ID 추가 없음

## 판단 기준

Painting, Decorations, Signs는 컬렉션/범주형 항목일 수 있으므로 하나의 독립 가구로 단정하지 않아.

Ominous Sign variant 2와 Flowerbed variant 12/24는 다른 형제 변형의 ID가 있어도 해당 변형의 ID로 복사하지 않아.

원본 CustomName/GroupName을 이용한 후보 연결은 타일 ID 검증이 아니며 후보 테이블에서만 조회 가능.

원본 container, ContainerCapacity, ContainerPosition은 각각 원본 값으로 저장. Wiki 수납 용량은 별도의 원문 필드로 남겨 서로 섞지 않아. 한 가구를 구성하는 여러 원본 타일의 용량을 자동 합산하지 않아.

게임 Lua Loot Distribution 및 RoomDefs와의 결합은 원본 Lua가 확보될 때만 수행하고, Block/Entity 선택은 계속 보류해.

## 파일

B42_FURNITURE_DEFINITION_FIRST_V9.sqlite 와 ZIP: 원본 전체 DB에 5개의 v9 근거 테이블을 추가.

V9_2231_SOURCE_EVIDENCE.csv: 모든 가구 목록 레코드별 직접 ID/이름 확장/기능 속성/방향 근거.

V9_1855_STORAGE_EVIDENCE.csv: 모든 수납 타일 연결의 원본 기능 값 및 증거 등급.

V9_11_UNLINKED_WIKI_AUDIT.csv: 링크 없는 11개 항목의 원인·대응 현황.

V9_11_NAME_CANDIDATES_UNVERIFIED.csv: 확인 전의 출처 이름·형제 변형 후보.

MANIFEST.json: 전체 SQLite·ZIP 검증에 사용된 집계.

이 단계에서는 개별 타일 그림을 불필요하게 추가 검수하지 않았어. 정체/방향/부품의 실제 게임 객체 동일성은 공식 근거가 확인되어야 확정할 수 있어.
