# Rosewood 가구 명칭별·마크 대응 우선순위 추가 정리

원본 TMX 56개와 원본 .tiles 속성으로 추출한 4,248종을 실제 가구/설비와 구조물로 혼동하지 않도록 재분류했다.

## 우선순위별 수량

| 분류 | Local ID 종류 | 중심 배치 스프라이트 | 외곽 배치 스프라이트 |
|---|---:|---:|---:|
| SPECIAL_MANUAL_REVIEW | 2319 | 24705 | 13572 |
| FURNITURE_BLOCK_PRIORITY | 1172 | 18975 | 6237 |
| UTILITY_NOT_FURNITURE | 52 | 12605 | 3313 |
| INTERIOR_DECOR | 497 | 4712 | 530 |
| SWITCH_WALL_CONTROL | 8 | 2590 | 972 |
| INDOOR_LIGHT_FIXTURE | 112 | 1775 | 683 |
| OUTDOOR_LIGHT_INFRASTRUCTURE | 39 | 1380 | 514 |
| ROOF_EQUIPMENT | 48 | 1003 | 411 |
| SPORTS_FLOOR_SURFACE | 1 | 96 | 0 |

원본 CustomName/GroupName은 정확한 완제품 수를 나타내지 않는다. 동일 가구가 여러 스프라이트 조각으로 나뉘거나 원본 이름이 빠진 경우가 있다.

- MINECRAFT_MATCH_PRIORITY.csv: 4,248종 각각에 대응 우선순위와 사유를 기록. 원본 마크 모드 ID 열은 비워둠.
- FURNITURE_BY_ORIGINAL_NAME.csv: 원본 CustomName, GroupName별 묶음과 해당 Local ID 샘플, 배치 건수. 원본 이름 미기재 타일은 묶음으로 분리됨.
- CATEGORY_AND_PRIORITY_SUMMARY.csv: 우선순위+기존 분류별 집계.

주의: SPECIAL_MANUAL_REVIEW는 산업·특수 건물 등 추가 조사할 대상이며, UTILITY_NOT_FURNITURE도 원본 시각·TBX 검수 전에는 자동으로 삭제하지 않는다. 원본 데이터 변경 없음.
