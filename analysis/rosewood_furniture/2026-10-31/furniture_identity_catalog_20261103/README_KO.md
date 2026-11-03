# 로즈우드 원본 가구 정체 목록 (2026-11-03)

## 357종이라는 숫자의 정확한 의미

357개는 방향을 한 차례 합친 CustomName + GroupName 조합이야. 79개 CustomName은 넓은 종류이지 실제 디자인 수가 아니고, 357개도 최종 서로 다른 완성형 가구 3D 디자인 수가 아니야.

원본 타일 ID 1,347개를 정의 파일·방향·SpriteGridPos·기능 속성·Viewpoint 참고 모델에 연결했고, 타일셋 출처를 보존한 스타일은 363개야.

## 동일 이름·스타일이 두 타일셋에서 나타나는 6개 (기존 집계의 5개 외 Bed / Hospital 추가)

- Wardrobe / Oak : furniture_storage_01 [E|S] / furniture_storage_02 [N|W] => LIKELY_SAME_DESIGN_COMPLEMENTARY_DIRECTIONS

- Counter / Wooden Corner : fixtures_counters_01 [E|N|S|W] / location_trailer_02 [E|N|S|W] => HIGH_SAME_FACING_DIFFERENT_3D_ASSET

- Table / Large Dark Oak : furniture_tables_high_01 [E|S] / location_restaurant_bar_smutz [S] => OVERLAPPING_FACING_MISSING_3D_EVIDENCE

- Bench / Sturdy : furniture_seating_indoor_02 [E|S] / furniture_seating_indoor_03 [N|W] => LIKELY_SAME_DESIGN_COMPLEMENTARY_DIRECTIONS

- Chair / Modern White : furniture_seating_indoor_01 [E|S] / furniture_seating_indoor_03 [N|W] => LIKELY_SAME_DESIGN_COMPLEMENTARY_DIRECTIONS

- Bed / Hospital : furniture_bedding_01 [E|S] / location_community_medical_01 [E|S] => OVERLAPPING_FACING_MISSING_3D_EVIDENCE

Counter / Wooden Corner은 같은 방향 네 가지가 두 타일셋에 존재하지만 서로 다른 Viewpoint OBJ 연결명을 갖고 있어 **잘못 합쳐졌을 가능성을 반드시 확인**해야 해. Bed / Hospital도 원본 타일셋 두 곳에 같은 방향이 겹치지만 한쪽에는 Viewpoint 연결이 없어서 별도 검토가 필요해. Chair / Modern White 등은 같은 3D 모델이 두 방향 그룹에 나뉘어 있으므로 방향별 자산 분리일 가능성이 높아.

## 가구 정체 계층

79 family -> 357 style labels -> 363 source tileset variants -> facing N/E/S/W(or missing) -> SpriteGridPos parts.

게임 맵의 가구 배치 인스턴스는 별도 층위로 유지하고, 제작용 Blockbench 모델 수는 수동 확인 전까지 확정하지 않아.

Viewpoint 모델은 공개 3D모드의 참고 바인딩이지 공식 PZ 가구 identity ID가 아냐. 원본 B42.20.3과 Viewpoint 모델 기준의 버전 차이가 있으므로 그대로 동등하다고 할 수 없어.

## 원본 자료와 검수 파일

- CATALOG_357_STYLES.csv : 원본 스타일 357개와 방향·부품·속성·3D 연결, 위험 표시.

- FAMILIES_79.csv : 큰 가구 범주 79개(스타일을 자동 통합하지 않음).

- SOURCE_TILESET_VARIANTS_363.csv : 같은 이름도 출처 타일셋이 다르면 분리 보존.

- ORIENTATION_GRID_TEMPLATES.csv : 타일셋별 방향·부품과 SpriteGridPos.

- SOURCE_SPRITES_1347.csv : 개별 타일마다 원본 정의 전체 속성 + 3D 모드 바인딩.

- SAME_NAME_MULTIPLE_TILESETS_6.csv : 중복 통합의 근거 및 예외 5개.

- UNNAMED_CORE_ASSETS_NOT_IN_357.csv : 이름 없어 357종 목록에 아예 빠진 원본 후보.

- FURNITURE_IDENTITY.json : 향후 Forge 가구 모드 데이터베이스용 JSON 구조.

- reference_previews/ : 기존 완성형 원본 타일 이미지 357개 그대로 복사.

- INDEX.html : 79개 이름/스타일 검색·필터 가능한 오프라인 가구 도감.

## 다음 검수

1. 동일 이름 다중 타일셋 5종 중 Counter Wooden Corner과 Table Large Dark Oak부터 시각 검증.

2. 같은 이름 다른 GroupName들이 실제 같은 형상이고 색상만 다른지 3D·PNG 대조.

3. 여러 타일 가구, 일부 방향만 존재하는 가구의 조립을 점검.

4. 이름 없는 물체는 최종 목록에 별도 추가 검증. 현재 357에 포함되지 않음.

5. 확정된 디자인별로 Minecraft용 1개 모델 + facing/blockstate + 필요한 색상·재질 변형 설계.

## 하지 않은 일

357종을 모두 동일 디자인이라고 단정하지 않았고 3D모드 OBJ를 재배포하지 않았어. TMX, TileDef, PNG, 이전 매칭 결과의 어떤 원본도 변경하지 않았어.
