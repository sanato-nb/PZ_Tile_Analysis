# v75 독립 시각 검수 기록 (2026-10-26)

v74의 미관찰 고유 키에서 20종을 선정하여 GitHub Actions가 원본 PNG와 TMX를 읽어 생성한 A(개별 타일), B(동일 층 5×5), C(대상 배치 하나 제거), D(다른 실제 사용 위치) 비교판 **20개를 실제 이미지로 열어 관찰**했다. 관찰의 자연어 근거와 좌표·GID·해시는 `observations.tsv`에 있다. PNG–TMX 공식 Local ID 및 TileZed 정합은 확인하지 않았으므로 최종 인증 0이다.

| 고유 키 | 검수 | 잠정 정체(또는 보류) | B-C 픽셀 변화 | 신뢰도 |
|---|---|---|---:|---|
| `fixtures_doors_02/45` | candidate | 검은 프레임의 2단 유리 출입문 | 7812 | high |
| `fixtures_doors_02/48` | candidate | 회색 불투명 평판 여닫이문 | 5095 | medium |
| `fixtures_doors_02/52` | candidate | 회색 불투명 평판 여닫이문(반대 방향) | 5520 | medium |
| `furniture_seating_outdoor_01/27` | candidate | 청백 줄무늬 낮은 접이식 야외 의자 | 3021 | high |
| `furniture_storage_01/0` | candidate | 아이보리색 1도어 2서랍 키 큰 수납장 | 5908 | high |
| `furniture_storage_01/1` | candidate | 아이보리색 1도어 2서랍 수납장(다른 방향) | 6498 | medium |
| `blends_natural_01/20` | candidate | 녹색 삼각형 잔디 경계 오버레이 | 2249 | medium |
| `blends_natural_01/24` | candidate | 얇은 녹색 풀잎 경계 오버레이 | 506 | low |
| `blends_natural_01/25` | candidate | 가느다란 녹색 잔디 경계 띠 | 554 | low |
| `blends_natural_01/26` | candidate | 가느다란 잔디 가장자리 오버레이 | 216 | low |
| `blends_natural_01/27` | held | 정체 보류 | 0 | low |
| `blends_natural_01/28` | candidate | 올리브색 가는 풀잎 경계 오버레이 | 385 | low |
| `blends_natural_01/29` | held | 정체 보류 | 0 | low |
| `blends_natural_01/30` | candidate | 짧은 녹색 풀잎 경계 오버레이 | 226 | low |
| `blends_natural_01/31` | candidate | 올리브색 짧은 풀잎 경계 띠 | 496 | low |
| `blends_natural_01/33` | candidate | 짙은 녹색 삼각형 잔디 경계 조각 | 1154 | medium |
| `blends_natural_01/34` | candidate | 황록색 삼각형 잔디 모서리 조각 | 1112 | medium |
| `blends_natural_01/35` | candidate | 녹갈색 삼각형 잔디 경계 조각 | 1264 | medium |
| `blends_natural_01/36` | candidate | 황록색 삼각형 잔디 경계 조각 | 126 | low |
| `blends_natural_01/37` | candidate | 올리브색 잔디 바닥 타일 | 2281 | high |

**이번 신규:** 20종 직접 관찰, 잠정 후보 18종, 보류 2종(`blends_natural_01/27`, `/29`; B-C 변화 0). 신규 중복 키 0종. **누적 예정:** 3,377/5,409종(62.4330%), 미관찰 2,032종, 감사 가능한 후보 2,900종, 최종 인증 0종. 이 수치는 v75 통합 SQLite 생성·복원·무결성 검증이 성공한 경우에만 정식 반영한다.

모든 20종에서 PNG 물리 높이 불일치(`height_mismatch`)가 기록됐다. 일부 풀잎 경계 타일은 B-C 변화가 수백 픽셀 이하이며 가림·중첩 가능성이 있어 신뢰도를 low로 제한했다. 증거판 렌더는 TileZed 공식 렌더가 아닌 근사 아이소메트릭이다. 사용자 수동 검수 80종과 v36 이후 원본 SQLite·체크포인트·PNG·TMX는 별도 계보로 보존한다.
