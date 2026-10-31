# 로즈우드 357개 완성 가구 → 실제 모드 JAR에 존재하는 블록 모델 후보

Minecraft Java 1.20.1 Forge 모드 7개의 실제 JAR에 존재하는 blockstates/*.json 경로를 기반으로 원본 357종을 비교.

## 집계 결과
- FUNCTION_OR_NAME_CANDIDATE: 205종
- NAME_AND_STYLE_CANDIDATE: 108종
- NO_REAL_ASSET_CANDIDATE: 19종
- MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY: 17종
- NO_SUITABLE_SHAPE_OR_MATERIAL_IN_INSPECTED_MODS: 4종
- BROAD_SUBSTITUTE_CANDIDATE: 4종

## 실제 블록 자산 ID로 대응한 대표 가구
| 원본 완성 가구 | 부품 수 | 실제 MC 블록 상태 자산 ID | 근거 수준 |
|---|---:|---|---|
| Bed / Large Oak | 4 | decocraft:double_bed_oak_white | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Couch / Blue Rattan | 2 | mcwfurnitures:blue_couch | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Shelves / Large Metal | 2 | 없음 | NO_SUITABLE_SHAPE_OR_MATERIAL_IN_INSPECTED_MODS |
| Chair / Grey | 1 | pfm:gray_arm_chair | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Fridge / White | 1 | pfm:white_fridge | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Oven / Modern | 1 | pfm:gray_stove | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Toilet / Fancy | 1 | pfm:basic_toilet | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Bath / Large Deluxe | 2 | refurbished_furniture:acacia_bath | FUNCTION_OR_NAME_CANDIDATE |
| Wardrobe / Oak | 2 | mcwfurnitures:oak_double_wardrobe | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Computer / Desktop | 1 | refurbished_furniture:computer | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Television / Antique | 1 | decocraft:crt_tv | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Microwave / Chrome | 1 | pfm:iron_microwave | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Counter / Steel | 1 | 없음 | NO_SUITABLE_SHAPE_OR_MATERIAL_IN_INSPECTED_MODS |
| Table / Large Oak | 2 | mcwfurnitures:oak_table | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Machine / PAWS Pinball | 2 | 없음 | NO_SUITABLE_SHAPE_OR_MATERIAL_IN_INSPECTED_MODS |
| Jukebox / Oldies | 1 | decocraft:jukebox | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Piano / Western | 2 | decocraft:piano_upright_spruce | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |
| Grand Piano / Black | 6 | decocraft:piano_black | MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY |

## 중요한 제한
- 실제 모드 JAR의 블록상태 모델을 직접 읽어 확인했지만, 해당 ID가 게임에 등록되어 사용되는지는 미검증이다.
- 원본 PNG의 다칸 가구는 전체를 하나로 보고 평가한다. Minecraft 가구 1블록으로 자동 대체할 경우 크기와 외형이 달라질 수 있다.
- 모델의 색상·질감·3D 윤곽 일치 여부는 아직 별도 렌더 검증 전이다. 위 표는 존재하는 Minecraft 블록 자산 기반 후보이며 '정확하게 같다'는 확정이 아니다.
- 모드가 동적으로 생성하는 가구는 blockstates/ JSON 파일을 사용하지 않을 수도 있어 누락될 수 있다.
- JAR과 텍스처 파일 자체는 재배포하지 않고 자산 경로와 원본 버전 해시만 남겼다.

## 파일
- ROSEWOOD_357_PZ_TO_REAL_MINECRAFT_BLOCKSTATE_MATCH.csv: 357종 완성 가구 PNG·PZ3D·실존 MC 블록 상태 ID 매핑
- ALL_RANKED_MATCHED_MC_BLOCKSTATE_IDS.csv: 각 가구에 대해 최대 3개 실제 모드 후보
- STATUS_BY_MOD.csv: 1순위 모드별 잠정 검색 근거 집계
- ../minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json: 모드 실제 버전/다운로드 해시 증거

**확정된 마인크래프트 3D 외형 1:1 대응:** 현재 0종. 나머지는 실제 모델 검수 후보다.
