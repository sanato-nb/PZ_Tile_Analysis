# 좀보이드 B42 타일 정체 분석 — 중앙 AI 작업 지침 (v66)

## 목표 및 작업 기준
- B42 TMX 두 개(저장소 실제 파일 `B4220.3_MapExport_256/tmx/31_45.tmx`, `31_46.tmx`)에서 사용한 고유 5,409종(기준 배치 302,177건)을 원본 PNG와 실제 배치로 이해한다. 최초 원본 이름 `31_45(2).tmx` / `31_46(2).tmx`과 저장소 파일명 차이는 기록되었으며, 원본 동일성 인증으로 혼동하지 않는다.
- 모든 신규 작업의 **최신 소스는 `PROJECT_STATE.json`의 `unified_database`와 `latest_checkpoint`**다. `reconciliation`의 2,584(v47)는 옛 교집합 대조 기준이다.
- 2026-10-26 현재 최신 **v66: 3,165/5,409종(58.5136%); 미관찰 2,244종; 감사 가능한 잠정 후보 2,728종; 최종 인증 0종**.
- 최신 물리 통합 SQLite는 `analysis/current/v66/`, 복원기는 `python3 scripts/restore_unified_v66.py /tmp/pz_latest.sqlite`. 압축 7개 조각의 SHA-256·SQLite 무결성·누적 수량을 검증한다.
- `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 우선 읽는다.

## 실제 이미지 시각 분석 규칙
1. 반드시 최신 DB의 `analysis_queue`에서 **미관찰** 키 `(tile_set_locator, local_id)`를 선택한다. 동일 키는 재검수는 가능하나 신규 종수로 중복 계상하지 않는다.
2. **A** 원본 PNG 타일 크롭, **B** 동일 층 주변 5×5 근사 아이소메트릭, **C** 동일 레이어의 해당 타일 한 배치만 제거, **D** 다른 실제 TMX 배치 장면을 모두 생성하고 직접 확인한다.
3. 이미지에서 직접 보이는 `observed_features`, 추정 `identity_candidate`, 여러 타일 사물의 `part_role`, `confidence`를 분리한다. 타일셋 이름이나 v31 AI 분류만으로 판정하지 않는다.
4. 출처·좌표·레이어·GID, 원본 TMX와 PNG SHA, 제거 전후 픽셀 변화, 주변 누락과 `height_mismatch`를 보존한다. 픽셀 근거가 부족하면 `held` 처리한다.
5. 이미지 관찰 `observed`, 잠정 후보 `candidate`, 공식 Local ID 매핑 검증 `mapping_verified`, TileZed 정합, 최종 `certified`를 구별한다. TileZed·공식 매핑 검증 전 최종 인증 0.
6. 기존 폐기된 TMX 2D 평면도 엔진은 이 분석에 사용하지 않는다.

## 계보·보존
- v36 원본 전체 SQLite, v46 원본 테이블 `v46__`, v47 병합 `v47__`와 이후 v48~v66 작업 버전이 최신 DB에 검색 가능하게 보존된다.
- v36 과거 보고 후보 2,291종과 감사 가능한 2,156종의 차이 135종, v36/v46 후보 단어 충돌 256종은 자동 재분류하지 않는다.
- 사용자 수동 검수 80종과 재검수 의견은 최신 누적에 자동 병합되지 않은 별도 계보이며 함부로 수정하거나 합산하지 않는다.
- 과거 `analysis/archive/`, `analysis/current/v49/` ~ `v59/`, `Tiles/`, `B4220.3_MapExport_256/`, `checkpoints/` 원본은 삭제·덮어쓰기 금지.

## 최신 작업 (v66 신규 이미지 판독)
- v65 통합 SQLite를 SHA-256 검증 복원하고 `analysis_queue`의 **미관찰 2,289종** 중 중복 없는 45종을 선정했다. 기준 대기열의 실제 자격을 충족하는 만큼만 선정하여 강제로 48종을 채우지 않았다.
- `checkpoints/v66_preview/`: 원본 PNG A / TMX 동일 층 5×5 B / 대상 한 배치 제거 C / 다른 좌표 장면 D / 2×2 비교판을 직접 생성·확인한 **225개 JPEG**. 좌표·레이어·GID·원본 PNG/TMX SHA-256·B-C 변화 보존.
- `checkpoints/v66/observations.tsv` 및 `observations.csv`: **45종 직접 이미지 관찰**, 잠정 후보 **35종**, 보류 **10종**. 정체 이름과 눈으로 확인한 형태, 다중 타일 결합 역할을 분리 기록하고 중복 0종 보장.
- 관찰 후보 예: 밝은 상판의 목재 카운터, 베이지 연결식 소파, 빨간색 4구 오븐 레인지, 흰 전자레인지 정·후면, 대리석 느낌의 아치 출입구, 청회색·진갈색 양여닫이문, 교회 십자가 첨탑·지붕 탑, 붉은 산업용 파이프와 연결 엘보, 산업탱크·배기관, 마른 화분.
- **보류 10종:** `fixtures_counters_01/10·11`, `furniture_seating_indoor_03/7·14·15`, `appliances_cooking_01/11`, `industry_02/21·72`, `vegetation_indoor_01/20·27`; B-C 변화 0 또는 장면 가림으로 개별 배치 역할 확인 불가.
- `checkpoints/v66/v66_이미지내장_검수.html`: JPEG 225장 내장, `v66_증거_45종_A_B_C_D.zip` 229항목 ZIP CRC **PASS** 및 이미지 전수 로딩 PASS.
- `analysis/current/v66/MANIFEST.json`: 이전 모든 SQLite 테이블 보존, SQLite **84,340,736바이트**, SHA-256 **fa71fd4002c3c9f94b22ab3625a008e8743818d044fdc91628a6310bbc2cd877**. `scripts/build_unified_v66.py`, `scripts/restore_unified_v66.py`, `checkpoints/v66/verify_delta.py` 검사 통과.
- 공식 PNG–TMX Local ID 매핑 높이 불일치·TileZed 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. 이전 v36~v65와 사용자 직접 검수 80종은 별도 보존.

## 다음 작업과 GitHub 규칙
- 다음 버전은 v66 통합 DB의 **2,244종 미관찰 대기열**에서 시작한다. 사용자 수동 검수 80종은 별도 유지한다.
- 새 작업 종료마다 실제 A/B/C/D 판독 → 근거 CSV/SQLite/이미지 내장 HTML/증거 ZIP → 중복·SQLite·PNG·ZIP CRC 검증 → 새 버전 체크포인트 → `PROJECT_STATE.json` → `docs/HANDOFF.md`를 갱신한다.
- GitHub 커밋 제목은 한국어를 기본으로 쓰고 원본 자산과 기존 버전을 변경하지 않는다.
- **공개 저장소**에 토큰·개인정보·비공개 대화 원문을 올리지 않는다.
