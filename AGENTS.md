# 좀보이드 B42 타일 정체 분석 — 중앙 AI 작업 지침 (v68)

## 목표 및 최신 검증 기준
- B42 TMX 두 개(저장소 파일 `B4220.3_MapExport_256/tmx/31_45.tmx`, `31_46.tmx`)에서 사용한 고유 **5,409종**, 기준 배치 **302,177건**을 원본 PNG와 실제 배치로 이해한다. 최초 이름 `31_45(2).tmx` / `31_46(2).tmx`과 저장소 이름의 동일성은 공식 인증 전까지 별개로 취급한다.
- 모든 작업은 `PROJECT_STATE.json`의 `unified_database` 및 `latest_checkpoint`를 우선한다. `reconciliation`의 2,584(v47)는 과거 교집합 대조 기준이다.
- 2026-10-26 최신 **v68: 3,255/5,409종(60.1775%); 미관찰 2,154종; 감사 가능한 잠정 후보 2,793종; 최종 인증 0종**.
- 최신 물리 통합 SQLite: `analysis/current/v68/`. 복원: `python3 scripts/restore_unified_v68.py /tmp/pz_latest.sqlite`. 압축 7조각의 SHA-256·SQLite 무결성·누적 수량 검증을 거친다.
- `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 먼저 읽는다.

## 실제 이미지 시각 분석 규칙
1. 최신 DB `analysis_queue`에서 미관찰 키 `(tile_set_locator,local_id)`를 선택하고, 이전 관찰과 겹치는 키는 신규로 계상하지 않는다.
2. A 원본 PNG 타일 크롭, B TMX 동일 층 주변 5×5 근사 아이소메트릭, C 동일 레이어 대상 배치 **하나만** 제거, D 다른 실제 TMX 사용 위치를 생성하고 **직접 이미지를 관찰**한다.
3. `observed_features`, `identity_candidate`, `part_role`, `confidence`, `review_status`를 분리한다. 타일셋명 또는 과거 v31 AI 분류만으로 정체를 판단하지 않는다.
4. TMX 좌표·층·레이어·raw GID·원본 PNG/TMX SHA-256·B-C 픽셀 변화·주변 누락·`height_mismatch`를 증거에 남긴다. 불충분한 정체는 `held`로 처리한다.
5. 이미지 관찰 `observed`, 잠정 `candidate`, 공식 Local ID 매핑 검증 `mapping_verified`, TileZed 정합, 최종 `certified`를 혼동하지 않는다. 공식 PNG–TMX 매핑 및 TileZed 미검증 상태에서 인증 0.
6. 이전에 폐기된 TMX→2D 평면도 엔진을 재사용하지 않는다.

## 보존·계보
- v36 원본 전체 SQLite, v46 원본 `v46__` 테이블, v47 병합 `v47__` 및 v48~v68의 누적 테이블을 유지한다.
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

## 다음 작업
- v68 `analysis_queue`의 **미관찰 2,154종**에서 계속 선정하고 동일한 A/B/C/D 직접 관찰 및 검증을 수행한다.
- v68 보류 24종의 부품 역할을 추가 근거로 재검수하고, v67 이하 보류도 별도 검토한다.
- PNG–TMX Local ID 높이 불일치와 TileZed 정합을 독립 검증한다.
- 신규 버전 종료마다 CSV·SQLite·원본 증거·이미지 내장 HTML·ZIP, SHA-256·무결성·CRC 검사 후 `PROJECT_STATE.json`과 `docs/HANDOFF.md`를 갱신한다.
- GitHub 커밋은 한국어를 기본으로 하고, 공개 저장소에 토큰·개인정보·비공개 대화 원문을 올리지 않는다.
