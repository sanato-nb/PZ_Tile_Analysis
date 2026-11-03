# 전체 가구 DB v3 분류

Wiki 원문 1268행과 원본 TileDef 195265 속성을 유지하며, 위키 바깥 963그룹을 출처 규칙으로 구분했다.

## 963그룹 분류

- DECORATION_REVIEW: 257

- UNNAMED_SPRITE_REVIEW: 191

- STORAGE_FUNCTION: 107

- NAMED_OBJECT_UNKNOWN: 105

- FURNITURE_OR_FIXTURE: 70

- APPLIANCE_OR_LIGHT: 60

- VEGETATION_VISUAL_REVIEW: 60

- BUILDING_PART_NOT_FURNITURE: 48

- ARCHITECTURE_OR_GROUND_NOT_FURNITURE: 44

- FURNITURE_NAME_REVIEW: 13

- STRUCTURE_NAME_REVIEW: 5

- EQUIPMENT_NAME_REVIEW: 3

## 이름이 같은 그룹을 공유하는 Wiki 항목

- SHARED_EXACT_TILE_IDS: 69

- DISJOINT_WIKI_IMAGE_IDS: 58

- MIXED_OVERLAP: 2

## 원본 타일 링크 근거 분류

- UNSAFE_SHARED_GROUP_EXPANSION: 6188

- SOURCE_ONLY: 4553

- UNVERIFIED_NAME_GROUP_EXPANSION: 1805

- DIRECT_WIKI_SPRITE_ID: 1649

원본 container 기능은 사실이며 타일셋/이름 기반 물체 종류는 분류 추론이다.

동일 CustomName+GroupName이어도 별개의 가구일 수 있어서 Wiki 별 실제 Sprite ID 집합을 비교했고 병합하지 않았다.

원본 속성/방향/다중타일은 기존 전체 DB를 계승. 아이템 생성 Lua, 맵 배치, 마크 Block/Entity 구현은 미결정.

이 단계에서 새로 눈으로 모든 스프라이트를 확인하지 않았으므로 서로 다른 완성형 가구 수를 확정하지 않는다.
