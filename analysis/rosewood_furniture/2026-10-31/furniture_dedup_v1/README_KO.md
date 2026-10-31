# 로즈우드 가구 중복 제외 집계 (2026-10-31)

중복에는 **동일 가구를 여러 타일로 나눴을 때의 부품 중복**과 **여러 레이어에 반복된 똑같은 완성 후보 기록**이 있다.
첫 번째는 앞선 v1에서 이미 SpriteGridPos 기준 결합했고, 이번 분석은 두 번째 중복을 찾는다.

## 위치별 객체 중복 제외
| 지역 | 범위 | 기존 가구 후보 수 | 동일 위치·원본부품 정확 중복 제외 | 중복 제외 가구 후보 수 | 고유 이름 있는 모델 키 |
|---|---|---:|---:|---:|---:|
| CORE | CORE_FURNITURE | 15957 | 8 | 15949 | 271 |
| CORE | NAMED_SPECIAL_FURNITURE | 1311 | 0 | 1311 | 91 |
| BUFFER | CORE_FURNITURE | 5321 | 0 | 5321 | 189 |
| BUFFER | NAMED_SPECIAL_FURNITURE | 292 | 0 | 292 | 38 |

## 중복 제외 규칙

- 동일 가구 모델이 서로 다른 집·좌표에 놓인 경우는 **각각 독립 가구**로 보존.
- 동일 x/y/z이면서 같은 원본 타일셋·Local ID 부품 집합·이름/그룹·방향·크기·범주인 경우에만 확정 중복으로 하나만 보존.
- 다중 부품 2~4칸 가구는 기존 조립 상태를 그대로 유지하고, 구성 타일을 다시 별도의 가구로 계산하지 않음.
- 같은 위치라도 다른 타일 ID나 가구 방향이 붙으면 무조건 삭제하지 않고 SAME_LOCATION_MODEL_CONFLICTS_FOR_REVIEW.csv로 따로 보존.
- 고유 종류는 이름+스타일(GroupName)+원본 타일셋으로 분류하며 E/S/W/N 방향만 다른 경우 모델 종류 수를 중복 계산하지 않음.
- 원본 이름 없는 항목은 고유 물체 이름/모델을 확정하지 않고 별도 불확실 자산 키로 관리.

## 원본과의 구분
이 결과는 원본 격자와 위치 기반 자동 잠정 집계다. 별개 가구를 잘못 병합할 위험을 피하기 위해 의심 중복은 제거하지 않았다.
배치된 가구의 개수와 서로 다른 가구 종류 수를 서로 혼용하지 말아야 한다.

## 결과 파일
- OBJECT_INSTANCES_DEDUPLICATED.csv — 중복 제거된 가구/비품 개별 위치 원장
- DISTINCT_NAMED_MODELS.csv — 방향 변형을 합친 원본 이름+그룹별 모델/종류
- DEDUP_COUNTS_BY_SCOPE_ZONE.csv — 구역/범위별 정량적 결과
- SAME_LOCATION_MODEL_CONFLICTS_FOR_REVIEW.csv — 같은 좌표라도 근거 부족해 삭제하지 않은 충돌
- REMOVED_EXACT_DUPLICATE_OBJECTS.csv — 실제 제거된 레코드와 원본 ID 대응
- UNNAMED_ASSET_KEYS_NOT_VALIDATED_MODELS.csv — 이름없는 타일로 인한 종류 미확정
- ROSEWOOD_DEDUP_OBJECTS.sqlite / ROSEWOOD_DEDUP_FURNITURE.zip — 조회용 데이터베이스와 전체 결과.
