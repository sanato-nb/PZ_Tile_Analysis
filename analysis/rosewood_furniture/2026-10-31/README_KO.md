# 로즈우드 가구 및 설비 TMX 전체 추출 결과

원본 TMX 56개를 직접 읽어 Local ID별/배치 위치별로 정리했다.

중심 영역: TMX X30..33, Y43..48. 주변 완충 조사 영역: X28..34, Y42..49.
완충 영역은 로즈우드 행정 경계로 확정할 수 없으며 결과에서는 별도 집계한다.

## 검증 수치
- scanned_tmx: 56
- scanned_layers: 1156
- all_gid_placements: 7268100
- selected_sprite_part_placements: 94073
- unique_selected_tile_ids: 4248
- unique_direct_ids: 1929
- unique_special_review_ids: 2319
- core_selected_placements: 67841
- buffer_selected_placements: 26232
- roomdefs_object_refs: 4692
- original_named_tile_ids: 2870
- old_visual_candidate_ids: 3810

## 중심 지역의 상위 가구 타일(동일 가구의 여러 부품은 각각 기록)

| 원본 타일 | 스프라이트 배치수 | 원본 이름/후보 |
|---|---:|---|
| appliances_com_01/109 | 3988 | 가공 전선의 짧은 선분 모듈 |
| appliances_com_01/108 | 3988 | (unnamed) |
| appliances_com_01/96 | 1184 | (unnamed) |
| appliances_com_01/97 | 1183 | (unnamed) |
| lighting_indoor_01/4 | 824 | Switch |
| lighting_indoor_01/5 | 789 | Switch |
| trashcontainers_01/20 | 379 | Round Bin |
| lighting_indoor_01/3 | 259 | Switch |
| lighting_indoor_01/2 | 255 | Switch |
| appliances_com_01/115 | 220 | 가공 전선의 길이·방향별 선분 |
| fixtures_windows_curtains_01/55 | 218 | Curtain |
| appliances_com_01/114 | 218 | 가공 전선의 길이·방향별 선분 |
| furniture_seating_indoor_01/54 | 215 | Chair |
| lighting_outdoor_01/16 | 213 | 회색 전신주 또는 전력 기둥 |
| appliances_com_01/113 | 212 | 가공 전선의 길이·방향별 선분 |
| appliances_com_01/112 | 212 | 가공 전선의 길이·방향별 선분 |
| furniture_seating_indoor_01/52 | 210 | Chair |
| lighting_indoor_01/1 | 207 | Switch |
| fixtures_bathroom_01/1 | 200 | Toilet |
| fixtures_windows_curtains_01/53 | 197 | Curtain |
| fixtures_bathroom_01/0 | 197 | Toilet |
| trashcontainers_01/16 | 196 | Recycle Bin |
| furniture_seating_indoor_01/55 | 191 | Chair |
| furniture_seating_indoor_01/53 | 190 | Chair |
| appliances_com_01/120 | 189 | (unnamed) |
| furniture_seating_indoor_01/63 | 188 | Chair |
| appliances_com_01/122 | 185 | 전신주 주변의 가는 선 구성 조각 |
| appliances_com_01/121 | 182 | (unnamed) |
| lighting_indoor_01/0 | 181 | Switch |
| fixtures_windows_curtains_01/52 | 179 | Curtain |
| fixtures_windows_curtains_01/54 | 175 | Curtain |
| vegetation_indoor_01/9 | 170 | Dragon Tree |
| furniture_shelving_01/27 | 170 | Shelves |
| furniture_shelving_01/26 | 170 | Shelves |
| vegetation_indoor_01/21 | 168 | Chinese Evergreen |
| rooftop_furniture/22 | 166 | 둥근 환기구 덮개 |
| vegetation_indoor_01/19 | 160 | Cast Iron Plant |
| rooftop_furniture/1 | 153 | 외부에 놓인 금속 설비함 |
| furniture_storage_02/18 | 144 | Cartbox |
| trashcontainers_01/17 | 141 | Green Garbage Bin |
| furniture_shelving_01/25 | 140 | Shelves |
| furniture_shelving_01/24 | 140 | Shelves |
| furniture_shelving_01/40 | 135 | Shelves |
| furniture_shelving_01/41 | 117 | Shelves |
| furniture_seating_indoor_01/56 | 114 | Chair |
| furniture_storage_02/0 | 103 | Locker |
| fixtures_counters_01/37 | 102 | Counter |
| lighting_outdoor_01/1 | 99 | 흰 구형 등갓의 검은 옥외 가로등 |
| recreational_sports_01/63 | 96 | Bowling Lane Floor |
| furniture_tables_high_01/23 | 93 | Dark Round Table |
| furniture_seating_outdoor_01/23 | 93 | Bench |
| furniture_seating_outdoor_01/22 | 93 | Bench |
| appliances_com_01/167 | 92 | (unnamed) |
| furniture_tables_high_01/35 | 91 | Table |
| furniture_tables_high_01/34 | 91 | Table |
| appliances_com_01/95 | 91 | 목제 전신주 방향 부품 |
| appliances_com_01/94 | 91 | 목재 전신주 지주 |
| appliances_com_01/92 | 91 | 전신주 가로보·절연체 |
| vegetation_indoor_01/18 | 89 | Snake Plant |
| furniture_seating_indoor_02/5 | 89 | Chair |
| lighting_indoor_01/21 | 88 | Wall Lamp |
| furniture_storage_02/17 | 82 | Cartbox |
| vegetation_indoor_01/12 | 81 | Ficus |
| furniture_seating_indoor_01/61 | 81 | Chair |
| furniture_seating_indoor_02/4 | 78 | Chair |
| lighting_indoor_03/18 | 76 | Lamp |
| lighting_indoor_03/17 | 76 | Lamp |
| lighting_indoor_03/16 | 76 | Lamp |
| furniture_storage_02/1 | 75 | Locker |
| furniture_seating_indoor_01/59 | 75 | Chair |
| furniture_seating_indoor_02/6 | 74 | Chair |
| furniture_seating_indoor_01/57 | 74 | Chair |
| lighting_indoor_01/20 | 73 | Wall Lamp |
| furniture_storage_02/16 | 71 | Cartbox |
| fixtures_bathroom_01/3 | 71 | Toilet |

## 전체 파일
- ALL_FURNITURE_TILE_IDS.csv: 각 원본 타일 ID별 1행, 모드 블록 ID 대응용 빈 열 포함.
- FURNITURE_PLACEMENTS.csv.gz: 실제 가구 후보의 모든 좌표, 층, 레이어, 사각 RoomDefs 방, TBX 경로.
- CATEGORY_SUMMARY.csv: 가구 계열별 종류/배치 수.
- ROOM_FURNITURE_COUNTS.csv: 방 유형별 후보 타일 수.
- ALL_USED_TILES_SUMMARY.csv: 가구에 포함하지 않은 원본 GID도 검수 가능하도록 모두 집계.
- ROOMDEFS_TBX_REFERENCES.csv: 사용된 방 오브젝트의 참조 파일.
- ROSEWOOD_FURNITURE.sqlite: 가구 타일·방 원장.

## 판독 한계
- 완성된 가구 개수를 세지 않았으며, GID 배치 기록은 가구의 개별 스프라이트 부품이다.
- 산업·특수 건물 등은 실제 가구와 구조물이 혼재하여 SPECIAL_REVIEW로 따로 분리해야 한다.
- RoomDefs는 TBX 내부 방 마스크가 아닌 TMX 사각 영역에 근거하므로 방 이름은 근사치다.
- 가구 모드 대응 블록 ID와 마인크래프트 최종 블록 배치는 미확정이다.
