# v91 신규 미관찰 타일 12종 — 직접 A/B/C/D 시각 검수

검수일: 2026-10-26. **이 기록은 아직 중앙 DB에 통합하지 않은 독립 검수 대기분**이다.

## 선정과 중복 방지

- `PROJECT_STATE.json`의 v89 물리 통합 SQLite `analysis_queue` 미관찰 **1,604종**에서 선정.
- 병행 작업 `work/v90-visual-review-20261026`의 v90 증거 대기열 **240종**을 `excluded_v90_240.json`으로 고정해 제외.
- 선정된 12개 `(tile_set_locator,local_id)` 고유 키의 자체 중복 **0**, v90 240종과의 교집합 **0**.
- 원본 PNG A, 동일 층 TMX 5×5 B, 선택 배치 하나 제거 C, 다른 실제 사용 위치 D 및 합본 12개, 총 **60 JPEG**를 GitHub Actions에서 생성. [실행 기록](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40261982563).
- **12개 개별 A/B/C/D 합본을 실제 열어 관찰**하고 TSV·CSV에 외형/정체 후보/부품 역할/보류 사유를 분리했다.

## 독립 시각 판독

| 키 | 직접 관찰 및 잠정 판정 | B-C 픽셀 변화 | 상태 |
|---|---|---:|---|
| walls_decoration_01/13 | 회청색 벽 부착 반사 패널, 미용 작업대 위 거울 가능성 | 4,933 | 후보 |
| walls_detailing_01/4 | 매우 가는 연회색 수직 몰딩; 정확한 구조 역할 불명 | 1,165 | 보류 |
| walls_exterior_house_01/49 | 회갈색 수평 사이딩 외벽 | 11,009 | 후보 |
| walls_exterior_house_02/10 | 황회색 석재 외벽의 출입구 개구부 | 988 | 후보 |
| walls_interior_house_04/14 | 연분홍 실내 벽의 문 개구부 | 435 | 후보 |
| lighting_indoor_02/49 | 벽에 가로로 붙는 긴 회색 선형 조명 | 1,323 | 후보 |
| lighting_outdoor_01/40 | 회색 원형 벽 부착물, 조명인지 덮개인지 불명 | 565 | 보류 |
| overlay_grime_wall_01/29 | 흐릿한 회색 세로형 벽 오염 자국 | 1,309 | 후보 |
| roofs_accents_01/29 | 검은 경사 지붕 모서리 마감 | 2,166 | 후보 |
| roofs_accents_30_01/20 | 검은 윗선과 흰 하부의 수평 처마 마감 | 1,645 | 후보 |
| street_curbs_01/4 | 연회색 낮은 연석/포장 경계 | 480 | 후보(낮은 신뢰도) |
| trash_01/6 | 구겨진 종이·파란 포장재·갈색 쓰레기 조각 | 578 | 후보 |

**이번 독립 판독: 신규 직접 관찰 12종, 잠정 후보 10종, 보류 2종.** 모든 타일은 `png_height_mismatch=1`, `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.

## 통합 보류와 보존

v90의 240종이 중앙 `main` 통합 SQLite로 검증·병합되기 전에는 v91 누적 관찰 수를 중앙 통계에 더하지 않는다. 이 체크포인트의 TSV·CSV·A/B/C/D는 **실제 판독 근거이지만 아직 최종 통합 SQLite가 아니다**. v90 병합 후 최신 `analysis_queue`와 12개 키의 중복을 다시 확인한 뒤 통합한다. 기존 v36~v89 원본 DB·체크포인트·수동 검수 80종과 재검수 계보는 변경하지 않았다.

검증 스크립트: `checkpoints/v91/verify_delta.py`. 증거: `checkpoints/v91_preview/EVIDENCE_MANIFEST.json`, `review_sheets/`, 개별 A/B/C/D/ABCD 60 JPEG.
