# Project Zomboid B42 가구 목록 정리 v6 — 남은 위키 중복 연결 71그룹

## 원본의 의미를 해치지 않는 정리

위키 원문 1268행 중 같은 정확한 타일 ID 집합을 공유하는 146행을 검토했어.

기존 71개의 TileDef 이름 그룹은 69그룹이 각각 원본 이미지 타일 조합 하나를 중복 가리키고, 2그룹은 서로 다른 이미지 조합 두 개를 각각 중복 가리켜. 총 73개 원본 스프라이트 조합이야.

게임 가구 오브젝트 73종 또는 마인크래프트 모델 73종으로 확정한 것이 아냐.

## 기능 및 수납 속성

같은 카운터가 위키 Tables/All과 Storage/Counters에 각각 표기되면서 Storage쪽에만 50 등 용량이 있는 사례를 보존했어. 두 행이 정확히 같은 TileSet/LocalID를 참조할 경우 이미지 연결을 하나만 두되 위키 분류·크기·수납용량을 원문 행마다 별도 컬럼으로 연결해.

수납이 빈칸이라는 것은 0으로 추정하지 않고 원문 공란 그대로 남겨. 실제 원본 TileDef container, ContainerCapacity도 구분 저장했어.

같은 이미지 타일을 다른 명칭이 가리키는 사례는 오류 가능성이 있으므로 V6_CONFLICTS_SAME_SPRITE_DIFFERENT_NAMES.csv에 남겨 자동 통합을 금지했어.

## 이미지

Tiles/2x 원본 PNG 19개 타일셋에서 원본 DB image_cells의 실제 localID/격자좌표를 이용해 71개 비교 카드를 만들어. 원본 픽셀 크롭 성공 수는 MANIFEST.json에 기록되어 있어.

## 파일

- B42_SHARED_WIKI_OVERLAP_V6.sqlite, B42_SHARED_WIKI_OVERLAP_V6.zip: v5 전체 원본 + v6 분류 SQL 테이블

- V6_71_SHARED_SOURCE_GROUPS.csv: 71그룹과 원본 ID 조합 관계

- V6_73_EXACT_SOURCE_APPEARANCES.csv: 73개의 정확한 스프라이트 ID 집합과 모든 관련 수납/기능/원본 속성

- V6_146_WIKI_CROSS_CATEGORY_FACETS.csv: 위키 146행의 원문 카테고리 및 용량

- V6_ALL_SOURCE_TILE_AND_FUNCTION_EVIDENCE.csv: TileDef 원본 속성/PNG 크롭 SHA

- V6_CONFLICTS_SAME_SPRITE_DIFFERENT_NAMES.csv: 원문 명칭이 다르거나 속성 충돌 시 별도 기록

- ORIGINAL_PNG_CONTACT_SHEETS_71/: 71개 그룹의 원본 PNG 비교 이미지

## 이후 작업

원본 스프라이트의 실제 Moveable object identity는 게임 Lua 및 TMX 그룹과 함께 검증해야 해. 별도 원본 그룹 963개 전수 시각 검수, loot 분포 Lua 연결도 남아 있어.

Minecraft Block/Entity/3D 구현은 아직 결정하지 않았어.
