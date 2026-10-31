# 로즈우드 다칸 가구 조립 기반 개수 검수

전수 타일 배치 94,073건을 가구 수라고 부르지 않는다. 건물 내 가구 우선분류 타일 25,212건을 대상으로 원본 SpriteGridPos 조립을 검토했다.

## CORE
- 가구 후보 타일 배치: 18975
- 원본 격자와 실제 좌표가 맞아 조립된 다칸 가구 후보: 1745
- 그 가구에 사용된 부품 타일: 3612
- 이름이 있는 단일 스프라이트 배치 후보(독립 가구 인증 아님): 12142
- 정체/조립 미확정 나머지 부품: 3221

## BUFFER
- 가구 후보 타일 배치: 6237
- 원본 격자와 실제 좌표가 맞아 조립된 다칸 가구 후보: 587
- 그 가구에 사용된 부품 타일: 1184
- 이름이 있는 단일 스프라이트 배치 후보(독립 가구 인증 아님): 4140
- 정체/조립 미확정 나머지 부품: 913

원본 레이어·층과 격자 위치가 일치하는 완전 조립 패턴만 묶었다. 조립 실패 부품을 개별 가구라고 세지 않았다.
이것은 높은 신뢰도의 조립 후보 집계이며, TBX 내부 마스크·완성 가구 경계·수납·실제 PNG 형상과의 최종 검수는 별개다.
파일: ASSEMBLED_MULTI_FURNITURE_INSTANCES.csv (조립 후보 1행당 1개); ALL_PRIORITY_FURNITURE_PART_STATUSES.csv; CATEGORY_ASSEMBLY_COUNTS.csv; ASSEMBLY_GEOMETRY_DIAGNOSTICS.csv; SOURCE_TEMPLATE_EXCLUSIONS.csv; MANIFEST.json.
