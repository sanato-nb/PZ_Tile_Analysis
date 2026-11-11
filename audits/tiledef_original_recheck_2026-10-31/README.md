# v258 제안 — 원본 TILEDEF 7종 기반 전체 10,042종 재검수

검수일: **2026-10-31**. 이 폴더는 **비파괴 비교 결과**이며 v258 SQLite를 생성했거나 원본 정체를 인증한 것이 아니다. 최신 v255 CSV 원장에 원본 7종을 연결했고, 원본 속성·기존 잠정 사물명·사용자 선택과 보류 상태를 독립 열로 보존했다.

## 핵심 결과

- 기준: `review/v255_latest_integrated_10042_2026-10-30/MASTER_ALL_10042_LATEST_PREFERRED.csv` (총 10,042행).
- 원본: `tiledef/tiledef.zip` 내 7개 `.tiles`, SHA-256 = `ffba6f55e178ef0c4622906bfdd670c6a7cae779cf6dbe4e7d4b0dce45c18171`. 다섯 텍스트 추출본은 원본 바이너리의 파일별 타일셋/슬롯/속성 건수와 대조; 나머지 두 파일은 바이너리 직접 파싱.
- 전체 원본: 파일별 슬롯 합 73,644개, 고유 슬롯 61,418개, 속성 기록 합 195,265건. 출처별 중복은 같은 실제 타일 키를 공유하므로 합계는 고유 타일 수가 아님.
- 원본 키 정확 일치: **10,039/10,042**. 나머지 3개는 기존 정체를 취소하거나 투명으로 취급하지 않음.
- 일치 슬롯 중 속성 있음 9,938, 속성 없음 101.
- 원본 이름 힌트: `CustomName` 3,597, `GroupName` 2,701, 둘 중 하나 3,606.
- `Facing` 3,079, `SpriteGridPos` 1,204, `Material/MaterialType` 4,195, 구조 속성 4,510.
- 사용자 선택 68종 원본 키 일치(이름 힌트 23); 보류 439종 원본 키 일치(이름 힌트 114); **어느 것도 임의 변경하지 않음**.
- 원본 출처 간 속성값 충돌 **8건 / 4종**. 전부 냉장고 `appliances_refrigeration_01`의 20/21/38/39번 `ContainerOpenSound`/`ContainerCloseSound`; 새 이름·정체 충돌이라고 볼 수 없음.

## 원본 연결 실패 3종
- `camping_03 (ayrton orio's conflicted copy 2025-09-10)/19`
- `jumbo_tree_01/0`
- `overlay_graffiti_wall_02/2`

## 원본을 반영한 실제 재검토 후보
- `appliances_com_01/1`: 기존 '사무용 탁상 전자기기 또는 전화기' 후보에 비해 원본 `CustomName=Radio`, `GroupName=Premium Technologies Ham`이 더 구체적인 근거. **무전기/라디오 계열을 우선 후보로 제안**. 정확한 모델·방향·한 스프라이트의 부분 역할은 미확정.
- `appliances_com_01/74`: 원본 `CustomName=Computer`, `GroupName=Desktop`. 기존 '베이지 받침 전기설비 상자 후보'는 컴퓨터 관련 부품일 수 있으므로 **주변 스프라이트 및 A 이미지 재검토 권장**, 확정 수정 아님.
- `appliances_cooking_01/0`: `CustomName=Oven`, `GroupName=Green`이 기존 민트색 오븐 레인지 후보와 계열상 부합하므로 **유지 권장**(개별 파츠 인증 아님).
- `appliances_com_01/20`: `CustomName=Dish`, `GroupName=Satellite`가 기존 위성 접시 안테나 후보와 계열상 부합, **유지 권장**.

## 의미 및 검수 범위의 한계

1. `CustomName`은 종종 여러 Local ID에 동일하게 반복되므로, 개별 픽셀이 독립 물체인지 상단/측면 부품인지는 원본 PNG A와 실제 TMX B/C로 별도 검증해야 함.
2. `SpriteGridPos`는 멀티타일의 위치 힌트일 뿐 자동 완성 가구 인증이 아님. `Facing`도 개별 타일의 완전한 월드 방향 검증을 대체하지 않음.
3. 기존 v257의 10,003/10,042는 **다른 두 소스(메인+레거시) 범위**의 일치율. 여기의 10,039는 원본 7종으로 다시 대조한 결과이며 36종 추가 일치는 기존 원본 매칭 범위 확대이지 사물 정체 신규 확정이 아님.
4. `NO_ORIGINAL_PROPERTIES` 101종은 '이미지 없음'이 아니라 이 7개 정의에서 속성 없음. `SOURCE_SLOT_MISSING` 3종은 커스텀/과거 사본·별칭 등 출처 검토 필요.
5. 이 검수는 **7개 원본 정의 및 기존 v255의 텍스트 데이터 교차검수**. 새로 10,042개 원본 PNG를 모두 시각 재열람한 것이 아니며, 공식 정체/TileZed/PNG↔Local ID 인증 추가는 **0종**.

## 산출물

- `SOURCE_SUMMARY.json` — 파일별 검증 수치, 누락 3종, 통계 및 한계.
- `MASTER_ORIGINAL_AUDIT_PART*.csv` — 전체 10,042종의 기존 이름과 원본 `CustomName`, `GroupName`, `Facing`, `SpriteGridPos`, `Material`, `MaterialType`/구조속성, 사용자/보류 상태. `source_key`는 원문 그대로.
- `PRIORITY_FINDINGS.csv` — 출처 미연결, 충돌, 명칭 재검토 후보.

**이 폴더는 감사 증거이며 기존 파일을 수정하지 않는다. 정식 물리 DB 재빌드는 v258 별도 작업으로 수행해야 한다.**
