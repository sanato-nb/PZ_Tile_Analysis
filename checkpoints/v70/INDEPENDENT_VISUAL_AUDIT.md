# v70 원본 타일 A/B/C/D 독립 시각 검수 기록

검수일: 2026-10-26. 기준: v69 통합 SQLite의 `analysis_queue` 미관찰 키 2,139종. 원본 PNG와 TMX의 같은 층 5×5 근사 장면을 사용했다. A는 원본 개별 타일, B는 원래 배치, C는 그 배치 한 건만 제거, D는 다른 실제 TMX 위치다. 비교판 15장을 각각 직접 열어 시각 확인했다. PNG/TMX의 공식 Local ID 대응과 TileZed 검증은 수행되지 않았으므로 아래 정체는 모두 잠정 후보이며 인증 0종이다.

| 고유 키 | 상태 | B−C 변화(픽셀) | 관찰로부터의 잠정 후보 | 비교판 |
|---|---|---:|---|---|
| `fixtures_counters_01/72` | candidate | 11528 | 아이보리색 접수·판매대 코너 카운터 | [A/B/C/D](../v70_preview/fixtures_counters_01__072_ABCD.jpg) |
| `fixtures_counters_01/74` | candidate | 3030 | 아이보리색 직선 카운터 단부 | [A/B/C/D](../v70_preview/fixtures_counters_01__074_ABCD.jpg) |
| `fixtures_counters_01/76` | candidate | 6584 | 크림색 ㄱ자 카운터 안쪽 코너 | [A/B/C/D](../v70_preview/fixtures_counters_01__076_ABCD.jpg) |
| `furniture_seating_indoor_03/134` | held | 0 | 정체 보류 | [A/B/C/D](../v70_preview/furniture_seating_indoor_03__134_ABCD.jpg) |
| `furniture_seating_indoor_03/135` | held | 0 | 정체 보류 | [A/B/C/D](../v70_preview/furniture_seating_indoor_03__135_ABCD.jpg) |
| `furniture_seating_outdoor_01/5` | candidate | 5207 | 목재 야외 벤치의 한쪽 구간 | [A/B/C/D](../v70_preview/furniture_seating_outdoor_01__005_ABCD.jpg) |
| `appliances_refrigeration_01/30` | candidate | 13047 | 세로형 냉각 가전의 후면 방열부 | [A/B/C/D](../v70_preview/appliances_refrigeration_01__030_ABCD.jpg) |
| `appliances_refrigeration_01/33` | candidate | 14814 | 빨간색 상냉동 2도어 냉장고 | [A/B/C/D](../v70_preview/appliances_refrigeration_01__033_ABCD.jpg) |
| `appliances_refrigeration_01/49` | candidate | 7089 | 크림색 상부 개폐형 냉동고 | [A/B/C/D](../v70_preview/appliances_refrigeration_01__049_ABCD.jpg) |
| `location_shop_bargNclothes_01/26` | candidate | 14774 | 갈색 세로 판재 코너 벽체 | [A/B/C/D](../v70_preview/location_shop_bargNclothes_01__026_ABCD.jpg) |
| `location_shop_bargNclothes_01/33` | candidate | 7702 | 갈색 목재 창 개구부 벽 패널 | [A/B/C/D](../v70_preview/location_shop_bargNclothes_01__033_ABCD.jpg) |
| `location_shop_bargNclothes_01/34` | candidate | 2046 | 갈색 목재 출입문 개구부 벽 패널 | [A/B/C/D](../v70_preview/location_shop_bargNclothes_01__034_ABCD.jpg) |
| `industry_02/220` | candidate | 803 | 외벽 전기 접속함과 오른쪽 배선 | [A/B/C/D](../v70_preview/industry_02__220_ABCD.jpg) |
| `industry_02/221` | candidate | 833 | 외벽 전기 접속함과 왼쪽 배선 | [A/B/C/D](../v70_preview/industry_02__221_ABCD.jpg) |
| `industry_02/238` | candidate | 2230 | 외벽 수직 빗물 배수관 | [A/B/C/D](../v70_preview/industry_02__238_ABCD.jpg) |

## 검증 결과 및 한계

- 신규 키 15종, 기존 관찰 중복 0종, 잠정 후보 13종, 보류 2종. 보류 `furniture_seating_indoor_03/134` 및 `/135`는 원본에 퀼팅 소파 조각이 보이지만 B−C 실제 변화가 0이므로 정체를 확정하지 않았다.
- JPEG 75장(A/B/C/D/비교판 각 15장) PNG 원본 로딩, TMX 좌표·층·레이어·raw GID·SHA-256 대조 및 B−C 제거 배치 검증을 통과했다.
- 증거 ZIP 79개 항목 CRC PASS; SHA-256 `db6e63a29e9aa4e7bf566c7bd67d30902a4e914f8fb14c46dc6ab3f40fa35a02`.
- v70 SQLite 84,553,728바이트, SHA-256 `3fe194e8097ef41658a9eed7970b8f0c567c4bf1b8e9a115c988ab2be72a7087`; 압축 7조각 왕복 복원과 `PRAGMA integrity_check` 통과, v69 이하 기존 테이블 보존.
- 모든 신규 PNG에서 TMX 선언 높이와 물리 PNG 높이 불일치(`height_mismatch`)가 기록됐다. 따라서 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`이다. 근사 렌더링은 TileZed 공식 결과와 동일하다고 주장하지 않는다.
- 과거 v36~v69 원본 SQLite·체크포인트 및 사용자 수동 검수 80종은 보존하고 별도 계보로 취급한다.
