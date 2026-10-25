# v67 신규 10종 독립 시각 판독·무결성 감사 (2026-10-26)

## 범위와 실제 수행
- 최신 v66 통합 SQLite를 복원한 `analysis_queue` 미관찰 2,244종에서 중복 없는 10종을 선정했다. 두 TMX와 실제 PNG를 GitHub Actions의 원본 파일로 로딩하여 A(원본), B(동일 층 5×5), C(선택 배치 한 개 제거), D(다른 실제 사용 위치) 및 2×2 비교판을 만들었다.
- 10종의 A/B/C/D **비교판 10개를 직접 열어 시각 판독**했다. 이미지의 형태 설명과 잠정 정체·부품 역할·보류를 구별해 `observations.tsv`와 `observations.csv`에 기록했다.
- 기존 v31 AI 분류나 타일셋명 자체를 정체의 근거로 사용하지 않았다. A/B/C/D 근사 아이소메트릭은 TileZed 인증이 아니다.

## 관찰 결과
| 고유 키 | 이미지 관찰에서 확인한 핵심 형태 | 잠정 후보 / 보류 |
|---|---|---|
| fixtures_counters_01/26 | 갈색 상판과 양문, B/C에서 주방 벽면 상부장 한 조각 사라짐 | 갈색 양문형 벽걸이 수납장 |
| fixtures_counters_01/30 | 회색 금속 상판·양문·손잡이, 다른 위치 L자 상부장 | 회색 금속 상부장 |
| furniture_seating_indoor_03/19 | 황록색 쿠션 좌면·등받이·팔걸이, B/C에서 소파 일부 분리 | 황록색 소파 좌석 모듈 |
| furniture_seating_indoor_03/24 | 청회색 푹신한 1인용 좌석, D의 소파 옆에 배치 | 청회색 안락의자 |
| appliances_cooking_01/27 | 흰색 직사각형 소형 기기 측면·환기구, 앞면 식별 불가 | **보류**: 기종 미확정 |
| appliances_cooking_01/29 | 회색 소형 기기의 검은 앞창과 오른쪽 조작부 | 회색 탁상형 전자레인지 |
| location_community_church_small_01/68 | 갈색 아치 패널 문짝, 손잡이 오른쪽, B/C 출입구 일부 제거 | 양개문 왼쪽 문짝 |
| location_community_church_small_01/69 | 갈색 아치 패널 문짝, 손잡이 왼쪽, B/C 출입구 일부 제거 | 양개문 오른쪽 문짝 |
| industry_02/75 | 곡면 금속 외벽·원호형 상판, B/C에서 원통 설비 일부 제거 | 산업용 원통 탱크 측면 조각 |
| industry_02/140 | 낮은 회색 분절 블록과 둥근 끝, B/C에서 ㄱ자 경계석 일부 제거 | 콘크리트 경계석 연결 조각 |

**집계:** 10종 관찰, 잠정 후보 9종, 보류 1종, 중복 0종. 모두 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`으로 보존.

## 독립 데이터·파일 검사
- `checkpoints/v67/verify_delta.py` GitHub Actions 통과: 10개 키·위치·레이어·raw GID·다른 위치·원본 PNG/TMX SHA-256·원본 PNG 로딩·A/B/C/D/비교판 **JPEG 50장 로딩**·B-C 비동일 장면 확인.
- `scripts/restore_unified_v66.py`에서 이전 SHA-256·SQLite `integrity_check` 통과, `scripts/build_unified_v67.py`에서 이전 모든 테이블 보존과 신규 10개 키 중복 검사 통과.
- `scripts/restore_unified_v67.py` 압축 7조각 SHA-256 및 SQLite 무결성 왕복 통과. v67 SQLite 84,377,600바이트, SHA-256 `b9513caa3073acc604a3ae475edec3e18d0b9a6f24e106072fd8dd686d0a656c`.
- `scripts/build_v67_review_html.py`에서 JPEG 50장 데이터 URI 내장, HTML 4,825,316바이트, ZIP **54항목** CRC PASS. ZIP 5,816,513바이트, SHA-256 `c1afad88f1d8fa410d4d9894682f4559607f9fb07e1fb708442786902e1c094c`.
- `PROJECT_STATE.json` 기준 누적 **3,175/5,409종 (58.6985%)**, 미관찰 **2,234종**, 감사 가능한 잠정 후보 **2,737종**, 최종 인증 **0종**.

## 미해결 위험
- 신규 10종 모두 PNG 선언 높이 불일치(`height_mismatch`)가 기록됐다. 원본 스프라이트의 공식 Local ID 대응과 TileZed 렌더 정합을 인증하지 않았다.
- B/C는 동일 층 5×5 근사 조립이며 실제 게임의 가림·벽 처리·다층 표시와 차이가 있을 수 있다. 특히 기종·부품 기능과 문의 정확한 개폐 방향은 잠정이다.
- 기존 v36~v66 체크포인트와 원본 PNG/TMX, 사용자 수동 검수 80종을 변경하거나 자동 합산하지 않았다.
