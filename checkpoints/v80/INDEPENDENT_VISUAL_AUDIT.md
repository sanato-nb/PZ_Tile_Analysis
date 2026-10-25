# v80 독립 이미지 직접 검수 기록 (2026-10-26)

## 범위와 증거

v79 통합 SQLite `analysis_queue` 미관찰 1,968종 중 중복 없는 20종을 선정했다. GitHub Actions에서 원본 PNG와 두 TMX를 사용하여 A 원본 타일, B 동일 층 5×5 근사 아이소메트릭, C 같은 레이어 선택 배치 1건 제거, D 다른 실제 사용 위치, A/B/C/D 비교판을 총 100장 생성했다. 검수자는 `checkpoints/v80_preview/*_ABCD.jpg` 비교판 **20개를 직접 열어** A/B/C/D의 외형과 제거 효과를 관찰했다. 이미지 생성은 관찰 판정과 분리했고, 검수 이후에만 아래 후보와 보류를 기록했다.

## 타일별 육안 판독

| 고유 키 | B-C 변화 픽셀 | 잠정 판정 | 신뢰도 |
|---|---:|---|---|
| `fixtures_stairs_01/0` | 9639 | 검은색 개방형 금속 계단의 4단 분할 조각 | high |
| `fixtures_stairs_01/1` | 10058 | 검은색 개방형 금속 계단의 중간 분할 조각 | high |
| `fixtures_stairs_01/2` | 6372 | 검은색 개방형 금속 계단의 방향별 분할 조각 | high |
| `furniture_storage_01/34` | 7041 | 검정색 침대 옆 낮은 수납장 또는 협탁 | medium |
| `furniture_storage_01/35` | 7160 | 검정색 낮은 침실 수납장 또는 협탁 | medium |
| `furniture_storage_01/40` | 0 | **보류** — 가림으로 배치 기여 불명 | low |
| `blends_street_01/4` | 2065 | 회색 아스팔트 보수면의 삼각형 경계 조각 | medium |
| `blends_street_01/5` | 4096 | 밝은 회색 아스팔트 보수 바닥 | high |
| `blends_street_01/8` | 312 | 아스팔트 보수면의 가는 균열 경계선 | low |
| `blends_street_01/9` | 343 | 아스팔트 보수면의 반대 방향 균열선 | low |
| `blends_street_01/10` | 425 | 회색 아스팔트 보수면의 가는 균열 연결선 | low |
| `blends_street_01/11` | 431 | 회색 아스팔트 보수면의 가는 균열 연결선 | low |
| `blends_street_01/17` | 1194 | 베이지색 모래·자갈 지면의 삼각형 경계 | medium |
| `blends_street_01/18` | 2510 | 베이지색 모래·자갈과 회색 포장면의 삼각 경계 | medium |
| `blends_street_01/19` | 2320 | 베이지색 자갈 지면의 방향별 삼각 경계 | medium |
| `blends_street_01/20` | 2074 | 베이지색 모래·자갈 지면의 삼각형 경계 | medium |
| `blends_street_01/24` | 367 | 모래·자갈과 포장면 사이의 얇은 경계 띠 | low |
| `blends_street_01/25` | 390 | 모래·자갈 포장 경계의 얇은 연결선 | low |
| `blends_street_01/26` | 410 | 모래·자갈과 포장면 사이의 가는 경계선 | low |
| `blends_street_01/27` | 417 | 모래·자갈과 포장면 사이의 가는 경계선 | low |

## 주요 교차 관찰

- `fixtures_stairs_01/0~2`: 검은 개방형 금속 계단의 방향별 분할 조각. B에서 벽을 따라 연속되고 C에서 선택 조각만 빠지는 것을 확인했다.
- `furniture_storage_01/34~35`: 침대 옆의 낮은 검정 수납장. A의 상판·전면·측판, B/C의 배치 기여를 확인했지만 세부 용도는 잠정이다.
- `furniture_storage_01/40`: A에는 갈색 가구 형태가 있으나 B-C 변화가 0픽셀이며 D에서 동일성 판단이 불가능해 **보류**했다.
- `blends_street_01/4~11`: 회색 아스팔트 보수면·경계·가느다란 균열 선분. 얇은 선분은 픽셀 변화가 작아 신뢰도를 낮게 기록했다.
- `blends_street_01/17~27`: 회색 포장면과 베이지색 모래·자갈 경계의 삼각 조각 및 가는 경계선. A 형태와 B/C 변화를 구분했다.

## 품질 및 보존

- 신규 고유 키 20종, 잠정 후보 19종, 보류 1종, 중복 0종. 누적 예상 관찰 3,461/5,409종(63.9859%), 미관찰 1,948종, 감사 가능한 후보 2,969종.
- 모든 증거 매니페스트 항목은 원본 TMX 좌표·층·레이어·raw GID, 다른 위치, 원본 PNG/TMX SHA-256, B-C 변화, 누락 타일 수를 포함한다.
- **20종 모두 `height_mismatch`**: PNG의 실제 높이와 TMX 타일셋 선언 높이 불일치. 공식 PNG–TMX Local ID 대응 및 TileZed 검증 전에는 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`으로 유지한다.
- v36/v46 원본 DB, v47~v79 누적 테이블·체크포인트 및 사용자 수동 검수 80종·재검수 계보를 수정하거나 합산하지 않는다.
- 이 문서의 통합 수량은 v80 SQLite 빌드가 무결성 검사를 통과하기 전까지는 **예정 수치**이며, 실제 통합 검증은 `analysis/current/v80/MANIFEST.json`과 GitHub Actions 결과를 따른다.

검수 자료: `checkpoints/v80/observations.tsv`, `checkpoints/v80_preview/EVIDENCE_MANIFEST.json`, `checkpoints/v80_preview/*_ABCD.jpg`.
