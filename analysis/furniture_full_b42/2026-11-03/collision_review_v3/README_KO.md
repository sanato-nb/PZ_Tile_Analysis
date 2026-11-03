# 전체 가구 정체 검수 v3 — 같은 TileDef 그룹을 공유하는 Wiki 항목 129그룹

이 결과는 기존 B42 전체 가구 원장 v2의 원본 DB를 보존하면서 위키의 중복 행과 실제 다른 원본 타일 번호를 구분하는 작업이다.

## 직접 확인한 타일 ID 중복 유형

- SAME_IMAGE_IDS_SAME_NAME: 63그룹

- DISJOINT_IMAGE_IDS: 58그룹

- SAME_IMAGE_IDS_DIFFERENT_NAMES: 6그룹

- OVERLAPPING_IMAGE_IDS: 2그룹

같은 이름+같은 타일 ID인 경우 위키의 동일 항목 반복 기재로 볼 근거가 충분하지만 원문 Wiki 행은 삭제하지 않고 canonical row로 참조만 한다. 게임 내 단일 3D/가구임을 인증하지는 않는다.

같은 TileDef 그룹인데 직접 이미지 ID가 다르면 다른 방향인지, 상태 변형인지, 실물 디자인이 다른지는 별도 분류가 필요하다. 특히 GroupName과 CustomName만 같다는 이유로 자동 병합하지 않는다.

## 원본 이미지 증거

원본 Tiles/ PNG + v259의 image_cells, image_atlases에 기록된 ID, 그리드 좌표, 픽셀 크기를 이용해 실제 스프라이트 크롭 이미지 758장을 생성했다.

웹 접근 없이도 HTML과 함께 ZIP으로 열어 129그룹을 방향·부품·원본 픽셀로 비교할 수 있다. PZwiki 외부 문서 링크는 인터넷이 있어야 한다.

## 자료 파일

- PZ_B42_FURNITURE_COLLISION_AUDIT_V3.zip: 원본 v2 SQLite 내용 + 검토 증거 + 실제 원본 스프라이트 크롭이 들어 있는 통합 자료.

- ORIGINAL_SPRITE_COMPARE_129.html: 129그룹의 원본 이미지 비교.

- 129_GROUP_COLLISIONS_CLASSIFIED.csv: 그룹별 충돌 유형, 모든 원본 소스 타일, 원본 수납속성.

- WIKI_ROWS_WITH_EXACT_TILE_ID_EVIDENCE.csv: Wiki 항목별 확인된 타일 번호/방향/그리드 및 문서 URL.

- EXACT_DUPLICATE_WIKI_LISTINGS.csv: 위키 중복 등재 관계.

- DISTINCT_OR_OVERLAPPING_TILE_ID_GROUPS.csv: 다른 실제 가구 여부를 추가 확인할 문제 그룹.

- ORIGINAL_TILE_CROP_AND_PROPERTIES.csv: 타일 ID별 원본 스프라이트, Facing, SpriteGridPos, container, 용량.

## 하지 않은 작업

게임 내 IsoObject 및 IsoSpriteGrid 생성/회전 검증, 완제품 3D 시각 동일성 인증, 963개의 위키 미등재 소스 그룹 전수 시각검토, Lua 방별 아이템 생성, Minecraft 구현은 이번 단계에서 완료하지 않았다.

원본 TileDef/PZwiki/TMX/이전 DB의 가구 분류와 수납 아이템 생성 규칙은 변경하지 않았다.


## 원본 방향 속성까지 나눈 58개 불일치 그룹

정확한 원본 타일 ID가 서로 겹치지 않는 58그룹에 대해 방향 정보까지 다시 확인한 결과, **41그룹은 Facing 미기록**, **7그룹은 동일 Facing에 여러 원본 이미지가 연결되어 디자인/상태 차이 검토 필요**, **7그룹은 위키 항목 간 Facing이 서로 분리되어 회전 변형 가능성이 있음**, **3그룹은 Facing이 부분적으로 겹쳐 구조 확인 필요**로 분류되었어. 방향이 겹치지 않는 7그룹도 게임 내 동일 가구라고 확정된 것은 아니야.

### 원본 스프라이트 직접 확인 사례: Wooden Bench

- 위키 PZW-0183: 원본 furniture_seating_indoor_03/66 + /67, Facing N, SpriteGridPos (0,0) + (1,0).
- 위키 PZW-0184: 원본 furniture_seating_indoor_03/65 + /64, Facing W, SpriteGridPos (0,0) + (0,1).
- 두 위키 행은 Wooden Bench 및 Wooden Bench (variant 2)로 분류되어 있지만 같은 원본 CustomName/GroupName 계열이야. 원본 스프라이트 4장을 실제로 관찰했을 때, 나무 벤치의 방향에 따라 두 부품의 투영 방향·배치가 달라지는 모습과 일치했어.
- 따라서 **각 방향당 2개 타일로 구성된 하나의 벤치 디자인의 방향 변형이라는 시각적 근거가 강함**. 단, 이 단계에서는 게임 런타임의 IsoSpriteGrid/getFaces 연결이나 실제 객체 ID를 검증하지 않았으므로 모델/게임 동등성을 확정값으로 표기하지 않아.

파일 ORIGINAL_SPRITE_COMPARE_129.html에서 PZW-0183/0184와 원본 WEBP 4장을 직접 비교할 수 있어.
