# v71 원본 타일 A/B/C/D 직접 시각 감사

검수일: 2026-10-26. 기준: v70 통합 SQLite의 미관찰 대기열 2,124종. 기존 관찰과 중복 없는 20종을 원본 PNG·TMX에서 생성한 A/B/C/D와 2×2 비교판으로 직접 확인했다. A는 개별 PNG, B는 같은 층 5×5 조립, C는 같은 레이어의 선택 배치 한 건만 제거, D는 다른 실제 사용 위치다. 근사 렌더링은 TileZed 공식 렌더가 아니다.

| 고유 키 | 판정 | B−C 변화 픽셀 | 잠정 후보 (최종 인증 아님) | 비교판 |
|---|---|---:|---|---|
| `fixtures_counters_01/78` | candidate | 2128 | 아이보리색 수납 카운터 모서리 | [A/B/C/D](../v71_preview/fixtures_counters_01__078_ABCD.jpg) |
| `fixtures_counters_01/79` | candidate | 3635 | 아이보리색 직선형 카운터 조각 | [A/B/C/D](../v71_preview/fixtures_counters_01__079_ABCD.jpg) |
| `fixtures_counters_01/147` | candidate | 6228 | 갈색 벽걸이 주방 상부 수납장 | [A/B/C/D](../v71_preview/fixtures_counters_01__147_ABCD.jpg) |
| `furniture_seating_outdoor_01/6` | candidate | 5368 | 연갈색 야외 벤치 한쪽 끝 | [A/B/C/D](../v71_preview/furniture_seating_outdoor_01__006_ABCD.jpg) |
| `furniture_seating_outdoor_01/7` | candidate | 4289 | 연갈색 야외 벤치 반대쪽 끝 | [A/B/C/D](../v71_preview/furniture_seating_outdoor_01__007_ABCD.jpg) |
| `furniture_seating_outdoor_01/8` | candidate | 7256 | 목재 좌판과 검은 철제 팔걸이의 공원 벤치 | [A/B/C/D](../v71_preview/furniture_seating_outdoor_01__008_ABCD.jpg) |
| `location_trailer_02/18` | candidate | 5487 | 갈색 양문형 싱크대 하부장 | [A/B/C/D](../v71_preview/location_trailer_02__018_ABCD.jpg) |
| `location_trailer_02/59` | held | 917 | 정체 보류 | [A/B/C/D](../v71_preview/location_trailer_02__059_ABCD.jpg) |
| `location_trailer_02/60` | held | 1630 | 정체 보류 | [A/B/C/D](../v71_preview/location_trailer_02__060_ABCD.jpg) |
| `industry_02/268` | candidate | 5100 | 녹색 탁상형 기둥 드릴프레스 | [A/B/C/D](../v71_preview/industry_02__268_ABCD.jpg) |
| `blends_grassoverlays_01/8` | candidate | 4101 | 낮고 넓은 야생 풀 군락 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__008_ABCD.jpg) |
| `blends_grassoverlays_01/12` | candidate | 3642 | 긴 잎이 모인 야생 풀 군락 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__012_ABCD.jpg) |
| `blends_grassoverlays_01/18` | candidate | 2494 | 작은 야생 풀 포기 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__018_ABCD.jpg) |
| `blends_grassoverlays_01/19` | candidate | 2496 | 성긴 녹색 풀 포기 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__019_ABCD.jpg) |
| `blends_grassoverlays_01/20` | candidate | 1908 | 성긴 야생 풀잎 묶음 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__020_ABCD.jpg) |
| `blends_grassoverlays_01/21` | candidate | 2337 | 둥근 야생 풀 포기 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__021_ABCD.jpg) |
| `blends_grassoverlays_01/24` | candidate | 6240 | 누런빛 긴 마른 풀 포기 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__024_ABCD.jpg) |
| `blends_grassoverlays_01/25` | candidate | 4835 | 누런빛 키 큰 풀 포기 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__025_ABCD.jpg) |
| `blends_grassoverlays_01/26` | candidate | 4554 | 올리브색 키 큰 풀 군락 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__026_ABCD.jpg) |
| `blends_grassoverlays_01/27` | candidate | 4796 | 누런빛 긴 풀 덤불 | [A/B/C/D](../v71_preview/blends_grassoverlays_01__027_ABCD.jpg) |

## 증거·무결성 결과

- 신규 고유 키 **20종**, 중복 **0종**; 이미지 기반 잠정 후보 **18종**, 정체 보류 **2종**. 누적 **3,305/5,409종(61.1019%)**, 미관찰 **2,104종**, 누적 감사 가능한 잠정 후보 **2,835종**, 최종 인증 **0종**.
- `location_trailer_02/59`, `/60`은 A에 검은 지붕·경계 음영이 보이지만 B/C/D만으로 역할이 특정되지 않아 보류했다. 모든 20종의 B−C 픽셀 변화는 0보다 크지만, 변화만으로 정체를 인증하지 않는다.
- 실제 원본 PNG/TMX SHA-256 검증, TMX 좌표·층·레이어·raw GID 대조, A/B/C/D JPEG **100장** 로딩 및 B−C 검증, 증거 ZIP **104개 항목 CRC PASS**.
- 증거 ZIP SHA-256: `6d44f6917fe549a6726fe1fcf09d00e42d4a2c0afe8ea96a0804fb06537bb91d`.
- 통합 SQLite **84,598,784바이트**, SHA-256 `8a65bffd76b5e2ed397e8822f1b289301f3df09dd49c7009c15bacfde93ef505`; 압축 조각 SHA-256 왕복·SQLite `integrity_check`·이전 테이블 보존·고유 키 중복 검사 통과.
- PNG 물리 높이와 TMX 선언 높이 불일치가 계속 관찰됐다. 공식 Local ID 대응과 TileZed 정합 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.
- v36·v46 원본 DB, v47~v70 모든 이전 체크포인트, 사용자 별도 수동 검수 80종 및 재검수 계보는 변경하지 않았다.
