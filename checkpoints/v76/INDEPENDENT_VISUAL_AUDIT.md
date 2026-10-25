# v76 독립 이미지 검수 기록 (2026-10-26)

## 실제 검수 범위
- 기준: v75 통합 SQLite의 미관찰 2,032종에서 중복 없는 20종을 선정했다.
- GitHub Actions가 원본 PNG 및 `31_45.tmx`, `31_46.tmx`에서 A(원본), B(동일 층 5×5 근사 조립), C(한 배치만 제거), D(다른 실제 사용 위치), 4분할 비교판을 생성했다.
- 검수자는 `checkpoints/v76_preview/`에 있는 **20개 비교판을 실제 이미지로 모두 열어** 원본 A와 B/C 차이, D 사용 맥락을 비교했다.
- 검수 결과: 신규 이미지 관찰 **20종**, 이미지 기반 잠정 후보 **19종**, 정체 보류 **1종**. PNG–TMX Local ID 및 TileZed 공식 정합은 **0종**, 최종 인증 **0종**.

## 타일별 외형 판독
| 타일 | 이미지에서 보인 것 | 상태 |
|---|---|---|
| fixtures_sinks_01/1 | 흰 타원 세면대, 금속 수전과 양측 손잡이 | 잠정 후보 |
| fixtures_sinks_01/2 | 다른 방향의 흰 타원 세면대와 수전 | 잠정 후보 |
| fixtures_sinks_01/3 | 작은 흰 세면대와 수전. B에서는 벽에 가려 제거 효과 186픽셀 | 잠정 후보(낮음) |
| furniture_storage_01/2 | 아이보리색 장의 문 한쪽·서랍 2개, 분할 면 | 잠정 후보 |
| furniture_storage_01/3 | 아이보리색 장의 반대 문·서랍 2개·측면 | 잠정 후보 |
| furniture_storage_01/14 | 짙은 갈색 낮은 장 형태. B-C 차이 **1픽셀**, D도 가림 | **보류** |
| blends_natural_01/38,39 | 올리브·황록색 마름모 잔디 바닥 질감 | 잠정 후보 2종 |
| blends_natural_01/40,41,43,44,45,46,47 | 짧은 풀잎이 위/아래로 달린 방향별 가는 사선 경계 띠 | 잠정 후보 7종(낮음) |
| blends_natural_01/48 | 누런 올리브색 잔디 마름모 바닥 | 잠정 후보 |
| blends_natural_01/50,51,52 | 아래·왼쪽·오른쪽 방향의 삼각 잔디 경계 채움 | 잠정 후보 3종 |
| blends_natural_01/53 | 짙은 황록색 마름모 잔디 바닥 | 잠정 후보 |

## 검수 및 보존 주의
- `observations.tsv`에 원본 외형 설명, 잠정 후보, 부품 역할, 신뢰도, 보류, TMX 좌표·층·레이어·raw GID, 원본 PNG/TMX SHA-256, B-C 픽셀 변화, 누락 주변 타일, 증거 경로를 구분해 기록했다.
- 각 타일의 다른 위치 D는 같은 Local ID의 다른 실제 TMX 배치다. TileZed 렌더러가 아닌 근사 아이소메트릭이다.
- 모든 PNG에서 `height_mismatch`를 유지하며, `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`으로 처리했다.
- 이전 v36·v46 원본 DB와 v47~v75 체크포인트, 사용자 별도 수동 검수 80종과 재검수 계보를 수정하거나 신규 관찰에 중복 합산하지 않는다.
- 이 문서는 검수자의 이미지 판독 기록이며, SQLite·SHA·ZIP CRC의 실제 통과 여부는 GitHub Actions 실행 결과와 `analysis/current/v76/MANIFEST.json`, `checkpoints/v76/ZIP_CRC_REPORT.json`으로 별도 확인한다.
