# v81 독립 이미지 직접 검수 기록 (2026-10-26)

## 범위와 방법

v80 통합 SQLite의 미관찰 고유 키 1,948종에서 중복 없는 12종을 선정했다. 원본 PNG 타일 A, 동일 층 5×5 TMX 합성 장면 B, 선택 배치 한 건만 제거한 C, 다른 실제 사용 위치 D를 GitHub Actions에서 생성했다. 검수자는 12개 A/B/C/D 비교판을 실제 열어 관찰했고, 생성만 된 증거와 시각 판독을 구분했다. 총 60 JPEG(각 5장)가 있다.

## 직접 관찰과 잠정 판정

| 고유 키 | B-C 변화 | 판정 | 잠정 정체 / 보류 이유 | 신뢰도 |
|---|---:|---|---|---|
| `fixtures_stairs_01/3` | 9770 | 잠정 | 갈색 개방형 금속 계단의 4단 연결 부품 | high |
| `fixtures_stairs_01/4` | 10233 | 잠정 | 수직 지지대가 달린 갈색 금속 계단의 3단 조각 | high |
| `furniture_storage_01/42` | 11681 | 잠정 | 아치형 거울이 달린 밝은 목재 화장대·3단 서랍장 | high |
| `furniture_storage_01/43` | 10746 | 잠정 | 아치형 거울이 달린 3단 목재 화장대의 반대 방향 | high |
| `blends_street_01/32` | 0 | 보류 | 가림 또는 합성 상 중복으로 단일 배치 기여 0픽셀 | low |
| `blends_street_01/33` | 1120 | 잠정 | 회색 아스팔트 포장면의 삼각형 혼합 경계 | medium |
| `blends_street_01/34` | 2033 | 잠정 | 회색 아스팔트·자갈 포장 경계의 반대 방향 삼각형 | medium |
| `blends_street_01/35` | 1224 | 잠정 | 회색 아스팔트 포장 경계의 측면 삼각 조각 | medium |
| `blends_street_01/37` | 4098 | 잠정 | 회색 아스팔트 포장 바닥 전체 타일 | high |
| `blends_street_01/38` | 4096 | 잠정 | 회색 아스팔트 포장 바닥 전체 타일의 변형 | high |
| `blends_street_01/39` | 0 | 보류 | 가림 또는 합성 상 중복으로 단일 배치 기여 0픽셀 | low |
| `blends_street_01/40` | 339 | 잠정 | 회색 아스팔트 패치의 가는 불규칙 경계선 | low |

## 품질 경계

신규 관찰 12종, 잠정 후보 10종, 보류 2종(`blends_street_01/32`, `blends_street_01/39`: B-C 변화 0), 신규 중복 0종. v81 빌드가 통과할 경우 누적 관찰 3,473/5,409종(64.2078%), 미관찰 1,936종, 감사 가능한 잠정 후보 2,979종이다. 이 숫자는 SQLite 빌드 전에는 예정값으로만 취급한다.

모든 신규 타일에 PNG 물리 높이와 TMX 선언 높이 불일치가 있으며, 공식 PNG–TMX Local ID 매핑 및 TileZed 정합은 검증되지 않았다. 따라서 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`을 유지한다. B/C는 TileZed가 아닌 근사 아이소메트릭 합성으로, 가림과 층·레이어 중첩의 한계가 있다. v36~v80 원본·SQLite·체크포인트·사용자 수동 검수 80종은 변경하지 않는다.

증거 원문: `checkpoints/v81/observations.tsv`, `checkpoints/v81_preview/EVIDENCE_MANIFEST.json`, `checkpoints/v81_preview/*_ABCD.jpg`.
