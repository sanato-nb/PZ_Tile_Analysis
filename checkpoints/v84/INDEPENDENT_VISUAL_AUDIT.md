# v84 독립 시각 판독 감사 기록 (2026-10-26)

v83 통합 SQLite 미관찰 대기열에서 중복 없는 12종을 선정했다. GitHub 원본 PNG·TMX로 생성된 A 원본, B 동일 층 5×5 조립, C 단일 배치 제거, D 다른 실제 위치의 비교판 12개를 **직접 열어 시각 판독**했다. 이는 이미지 기반 관찰이며 공식 Local ID 또는 TileZed 검증이 아니다.

| 고유 키 | 상태 | 잠정 정체/보류 | B-C 변화(픽셀) | 신뢰도 |
|---|---|---|---:|---|
| fixtures_stairs_01/33 | candidate | 갈색 목재 실내 계단의 4단 분할 조각 | 8797 | high |
| fixtures_stairs_01/34 | candidate | 갈색 목재 실내 계단의 3단 분할 조각 | 4978 | high |
| furniture_storage_01/57 | candidate | 연갈색 1도어·2서랍 키 큰 수납장 조각 | 3337 | medium |
| furniture_storage_01/58 | candidate | 베이지색 1도어·2서랍 높은 수납장 조각 | 3843 | medium |
| blends_street_01/70 | candidate | 짙은 회색 입자 질감의 도로 포장 기본 타일 | 3989 | high |
| blends_street_01/71 | candidate | 회색 아스팔트 포장 기본 바닥 타일 | 4096 | high |
| blends_street_01/72 | held | 정체 보류 | 328 | low |
| blends_street_01/73 | held | 정체 보류 | 322 | low |
| blends_street_01/74 | held | 정체 보류 | 310 | low |
| blends_street_01/75 | held | 정체 보류 | 219 | low |
| blends_street_01/82 | candidate | 짙은 회색 지붕 표면의 하향 삼각형 질감 조각 | 1263 | medium |
| blends_street_01/83 | candidate | 회색 지붕 표면의 측방향 삼각형 질감 조각 | 2057 | medium |

**신규 관찰 12종, 잠정 후보 8종, 보류 4종.** 모든 타일에서 B-C 차이는 0보다 크지만 72~75는 미세한 선형 오버레이의 배치 기여·정확한 재질 연결을 시각적으로 구분하기 어려워 보류했다. 모든 타일의 PNG 물리 높이 불일치가 남아 있으며 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`이다.

원본과 계보는 변경하지 않는다: v36·v46 원본 SQLite, v47~v83 통합 계보, 이전 체크포인트, 사용자 수동 검수 80종 및 재검수 자료.

증거: `checkpoints/v84_preview/EVIDENCE_MANIFEST.json`, `checkpoints/v84_preview/`의 A/B/C/D+비교판 JPEG 60장, `checkpoints/v84/observations.tsv`.
