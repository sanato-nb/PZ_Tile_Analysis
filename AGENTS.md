# 좀보이드 B42 타일 정체 분석 — 중앙 AI 작업 지침 (v71)

## 목표 및 최신 검증 기준
- B42 TMX 두 개(저장소 파일 `B4220.3_MapExport_256/tmx/31_45.tmx`, `31_46.tmx`)에서 사용한 고유 **5,409종**, 기준 배치 **302,177건**을 원본 PNG와 실제 배치로 이해한다. 최초 이름 `31_45(2).tmx` / `31_46(2).tmx`과 저장소 이름의 동일성은 공식 인증 전까지 별개로 취급한다.
- 모든 작업은 `PROJECT_STATE.json`의 `unified_database` 및 `latest_checkpoint`를 우선한다. `reconciliation`의 2,584(v47)는 과거 교집합 대조 기준이다.
- 2026-10-26 최신 **v71: 3,305/5,409종(61.1019%); 미관찰 2,104종; 감사 가능한 잠정 후보 2,835종; 최종 인증 0종**.
- 최신 물리 통합 SQLite: `analysis/current/v71/`. 복원: `python3 scripts/restore_unified_v71.py /tmp/pz_latest.sqlite`. 압축 7조각의 SHA-256·SQLite 무결성·누적 수량 검증을 거친다.
- `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 먼저 읽는다.

## 실제 이미지 시각 분석 규칙
1. 최신 DB `analysis_queue`에서 미관찰 키 `(tile_set_locator,local_id)`를 선택하고, 이전 관찰과 겹치는 키는 신규로 계상하지 않는다.
2. A 원본 PNG 타일 크롭, B TMX 동일 층 주변 5×5 근사 아이소메트릭, C 동일 레이어 대상 배치 **하나만** 제거, D 다른 실제 TMX 사용 위치를 생성하고 **직접 이미지를 관찰**한다.
3. `observed_features`, `identity_candidate`, `part_role`, `confidence`, `review_status`를 분리한다. 타일셋명 또는 과거 v31 AI 분류만으로 정체를 판단하지 않는다.
4. TMX 좌표·층·레이어·raw GID·원본 PNG/TMX SHA-256·B-C 픽셀 변화·주변 누락·`height_mismatch`를 증거에 남긴다. 불충분한 정체는 `held`로 처리한다.
5. 이미지 관찰 `observed`, 잠정 `candidate`, 공식 Local ID 매핑 검증 `mapping_verified`, TileZed 정합, 최종 `certified`를 혼동하지 않는다. 공식 PNG–TMX 매핑 및 TileZed 미검증 상태에서 인증 0.
6. 이전에 폐기된 TMX→2D 평면도 엔진을 재사용하지 않는다.

## 보존·계보
- v36 원본 전체 SQLite, v46 원본 `v46__` 테이블, v47 병합 `v47__` 및 v48~v71의 누적 테이블을 유지한다.
- v36 과거 보고 후보 2,291종과 감사 가능한 2,156종의 차이 135종, v36/v46 후보 단어 충돌 256종을 자동 재분류하지 않는다.
- 사용자 수동 검수 80종과 재검수 의견은 별도 계보이며 누적 관찰에 자동 합산하지 않는다.
- `analysis/archive/`, `analysis/current/v49/`~`v66/`, `checkpoints/v36/`~`v66/`, `Tiles/`, `B4220.3_MapExport_256/`는 삭제·덮어쓰기 금지.

## v68 신규 실제 이미지 판독 (2026-10-26)
- v67 통합 SQLite의 미관찰 대기열 2,234종에서 중복 없는 **신규 80종**을 선정하고 실제 원본 PNG와 TMX의 A/B/C/D 이미지 + 비교판 **400장**을 직접 판독했다.
- 잠정 후보 **56종**, 보류 **24종**, 누적 이미지 관찰 **3,255/5,409(60.1775%)**, 미관찰 **2,154종**, 감사 가능한 누적 후보 **2,793종**, 최종 인증 **0종**.
- `checkpoints/v68/observations.tsv`, CSV: 좌표·레이어·raw GID·원본 PNG/TMX SHA-256·원본 관찰·정체 가설·다중 타일 부품 역할·신뢰도·B-C 변화·가림 보류를 각각 기록. B-C 변화 0인 12종 모두 보류.
- `checkpoints/v68_preview/`에 A/B/C/D 및 비교판 400 JPEG 실물 증거 보존, `checkpoints/v68/v68_이미지내장_검수.html`에 이미지 400장 데이터 URI 내장, 증거 ZIP **404개 항목 CRC PASS**.
- 잠정 후보에는 산업 주방 카운터와 냉장고·토스터·커피머신, 가구점 소파·의자, 의료 작업대·실내 벽, 산업용 사각 환기 덕트·전기 계량함·전선 연결부 등이 있다.
- `analysis/current/v68/MANIFEST.json`: 물리 SQLite **84,484,096바이트**, SHA-256 **478304acfde12f53a0c03fc5bdb9264a6da9bb3b3e4c796244d06f15b8543fd8**. SQLite integrity_check·이전 테이블 보존·신규 키 중복·증거 SHA·JPEG 로딩 검증.
- 공식 Local ID 높이 대응과 TileZed 정합 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`; 과거 v36~v67 및 사용자 직접 검수 80종은 변경 없음.

## v69 신규 직접 이미지 판독 (2026-10-26)
- v68 통합 SQLite 미관찰 대기열 **2,154종**에서 고유 키 중복 없는 **15종**을 선별했다. 원본 PNG·TMX에서 A(원본), B(같은 층 5×5), C(단일 배치 제거), D(다른 위치), 비교판을 생성한 뒤 **15종의 비교판을 직접 열어 시각 검수**했다.
- 이번 신규 잠정 후보 **11종**, 보류 **4종**. 누적 관찰 **3,270/5,409(60.4548%)**, 미관찰 **2,139종**, 누적 감사 가능한 후보 **2,804종**, 최종 인증 **0종**.
- 잠정 후보에는 짙은 갈색 수납 하부장, 녹색 주방 카운터 코너·양문 수납장, 검은 퀼팅 안락의자, 크림색 2단 냉장고의 방향별 타일, 갈색 분기·병렬 배관, 벽 부착 전기 접속함과 케이블 분기부가 포함된다.
- 보류 4종: `furniture_seating_indoor_03/61`(B-C 0), `/103`(16), `appliances_refrigeration_01/27`(1511이나 정체 불명), `location_services_beauty_01/10`(4). A에서 보이는 모양과 실제 배치의 기여를 구분해 기록한다.
- 증거: `checkpoints/v69_preview/`의 A/B/C/D+비교판 **75 JPEG**, `checkpoints/v69/observations.tsv`, CSV, 이미지 내장 HTML, 증거 ZIP 79항목 CRC PASS. 각 키에 TMX 좌표·층·레이어·raw GID·원본 해시·B-C 변화 기록.
- 물리 SQLite `analysis/current/v69/MANIFEST.json`: **84,516,864바이트**, SHA-256 `bffc80c2358767efed77e486d7c796d229db5c231dab2d4b362c78ccd1eac053`. SHA 왕복·SQLite integrity_check·누적 수량·기존 테이블 보존·신규 키 중복·PNG/TMX SHA·JPEG 검증 완료.
- 공식 PNG–TMX Local ID 높이 정합과 TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v68 이하 및 수동 검수 80종은 별도 보존.

## v70 신규 직접 이미지 판독 (2026-10-26)
- v69 `analysis_queue`의 미관찰 **2,139종**에서 신규 키 **15종**을 선택하고, GitHub 원본 PNG·TMX로 A/B/C/D 및 비교판 **75장**을 생성해 실제 비교판 15개를 직접 시각 검수했다.
- 잠정 후보 **13종**, 보류 **2종**(`furniture_seating_indoor_03/134`, `/135`; 두 항목 모두 B-C 픽셀 변화 0). 신규 키 중복 0종.
- 주요 잠정 후보: 아이보리색 판매대 코너·카운터 연결부, 목재 야외 벤치, 냉장기기 후면·빨간 2도어 냉장고·상부 개폐형 냉동고, 갈색 목재 벽 코너·창 개구부·문틀, 외벽 전기 접속함 방향별 조각, 수직 빗물 배수관.
- 누적 **3,285/5,409종(60.7321%)**, 미관찰 **2,124종**, 감사 가능한 누적 잠정 후보 **2,817종**, 최종 인증 **0종**.
- `checkpoints/v70/observations.tsv`, CSV, `checkpoints/v70_preview/` 원본 증거 JPEG 75장, 이미지 내장 HTML(75장), ZIP(79항목 CRC PASS)을 보존한다.
- `analysis/current/v70/MANIFEST.json`: SQLite **84,553,728바이트**, SHA-256 `3fe194e8097ef41658a9eed7970b8f0c567c4bf1b8e9a115c988ab2be72a7087`. SHA 왕복·SQLite 무결성·이전 테이블 보존·신규 키 중복·원본 SHA·PNG/JPEG 로딩·장면 B-C·ZIP CRC 검증 통과.
- 모든 신규 키의 PNG 높이 불일치와 공식 Local ID·TileZed 미검증 상태를 유지한다. `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`; 이전 v69 이하 및 사용자 직접 검수 80종을 변경하지 않는다.

## v71 신규 직접 이미지 판독 (2026-10-26)
- v70 통합 SQLite 미관찰 2,124종에서 중복 없는 신규 키 20종을 선별했다. 원본 PNG·TMX의 A/B/C/D 및 비교판 **100 JPEG**를 GitHub Actions로 생성하고 비교판 20개를 직접 열어 육안 판독했다.
- 신규 잠정 후보 **18종**, 보류 **2종**(`location_trailer_02/59`, `/60`: 지붕 표면의 음영·경계 부품으로 보이나 정확한 기능 불명). 모든 B-C 비교에서 픽셀 변화가 있었다.
- 주요 잠정 후보: 밝은 아이보리 카운터 조각 2종, 갈색 주방 상부장, 목재 야외 벤치 3종, 양문형 싱크대 하부장, 녹색 기둥형 드릴프레스, 풀잎 오버레이 10종. 이름만으로 판단하지 않고 A의 외형과 B/C 변화 및 D 배치를 대조했다.
- 누적 관찰 **3,305/5,409종(61.1019%)**, 미관찰 **2,104종**, 누적 잠정 후보 **2,835종**, 최종 인증 **0종**.
- `checkpoints/v71/observations.tsv` 및 CSV, `checkpoints/v71_preview/`의 JPEG 100장, HTML 내장 검수기, 증거 ZIP 104항목 CRC PASS를 보존한다.
- `analysis/current/v71/MANIFEST.json`: SQLite **84,598,784바이트**, SHA-256 `8a65bffd76b5e2ed397e8822f1b289301f3df09dd49c7009c15bacfde93ef505`. 원본 SHA, JPEG 로딩, SQLite 무결성, 기존 테이블 보존, 중복 키 0을 검증했다.
- PNG 물리 높이와 TMX 선언 높이 불일치, 공식 Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. 과거 체크포인트와 사용자 수동 검수 80종은 변경하지 않는다.

## 다음 작업
- v71 `analysis_queue`의 **미관찰 2,104종**에서 고유 키를 선정하고 A/B/C/D 직접 관찰을 계속한다.
- v71 보류 2종과 이전 버전 보류 항목의 가림·분할 부품 역할을 재검수한다.
- PNG–TMX Local ID 물리 높이 불일치와 TileZed 공식 정합을 독립 검증한다.
- 신규 버전마다 기존 원본·체크포인트·사용자 수동 검수 80종을 보존하고, SHA·SQLite 무결성·CRC·중복을 확인한 뒤 PROJECT_STATE.json 및 docs/HANDOFF.md를 갱신한다.
- GitHub 커밋은 한국어를 기본으로 하고 공개 저장소에 토큰·개인정보·비공개 대화 원문을 올리지 않는다.
