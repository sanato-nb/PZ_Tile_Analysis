# B42 가구 분류 v4

위키 1,268항목에서 같은 원본 TileDef 그룹에 속하지만 위키 이미지 ID 집합이 서로 겹치지 않는 58개 그룹을 분석했어.

이 58개 그룹에는 357개의 서로 다른 위키 기록이 있어. 그중 50개 원본 그룹에서 기본 명칭을 공유하는 변형 행을 확인했고, 서로 다른 명칭이 혼합된 8개 그룹은 가구 이름 계열을 분리했어.

원본 타일 PNG 및 image_cells / image_atlases의 위치 메타데이터로 만든 접촉시트 58장, 원본 이미지 크롭 SHA-256, 위키 행/원본 스프라이트/속성을 추적 가능하게 저장했어.

같은 이름 계열 안에 여러 실제 디자인이 있을 수 있고, 서로 다른 로컬 ID가 같은 가구의 방향/부품일 수도 있어. 따라서 하나의 완성 3D 모델로 자동 병합하거나 개별 확정하지 않았어.

원본 source_attributes 195,265행, 기존 full TileDef, 위키 1,268행 및 v3 테이블은 모두 보존했어.

마크 Block/Entity 구현, 실맵 가구 인스턴스, 루팅 Lua 분포 규칙은 여전히 미결정/미수집 상태.

주요 산출물: SQLite, GROUPS_58_V4.csv, WIKI_NAME_FAMILIES_66.csv, WIKI_VARIANT_ROWS_357.csv, ORIGINAL_PNG_CROP_EVIDENCE.csv, ALL_58_VISUAL_GALLERY.md, CONTACT_SHEETS_58 폴더, 통합 ZIP.
