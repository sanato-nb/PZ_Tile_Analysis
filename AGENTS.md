# 좀보이드 B42 타일 정체 분석 — 중앙 AI 작업 지침 (v65)

## 목표 및 작업 기준
- B42 TMX 두 개(저장소 실제 파일 `B4220.3_MapExport_256/tmx/31_45.tmx`, `31_46.tmx`)에서 사용한 고유 5,409종(기준 배치 302,177건)을 원본 PNG와 실제 배치로 이해한다. 최초 원본 이름 `31_45(2).tmx` / `31_46(2).tmx`과 저장소 파일명 차이는 기록되었으며, 원본 동일성 인증으로 혼동하지 않는다.
- 모든 신규 작업의 **최신 소스는 `PROJECT_STATE.json`의 `unified_database`와 `latest_checkpoint`**다. `reconciliation`의 2,584(v47)는 옛 교집합 대조 기준이다.
- 2026-10-26 현재 최신 **v65: 3,120/5,409종(57.6816%); 미관찰 2,289종; 감사 가능한 잠정 후보 2,693종; 최종 인증 0종**.
- 최신 물리 통합 SQLite는 `analysis/current/v65/`, 복원기는 `python3 scripts/restore_unified_v65.py /tmp/pz_latest.sqlite`. 압축 7개 조각의 SHA-256·SQLite 무결성·누적 수량을 검증한다.
- `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 우선 읽는다.

## 실제 이미지 시각 분석 규칙
1. 반드시 최신 DB의 `analysis_queue`에서 **미관찰** 키 `(tile_set_locator, local_id)`를 선택한다. 동일 키는 재검수는 가능하나 신규 종수로 중복 계상하지 않는다.
2. **A** 원본 PNG 타일 크롭, **B** 동일 층 주변 5×5 근사 아이소메트릭, **C** 동일 레이어의 해당 타일 한 배치만 제거, **D** 다른 실제 TMX 배치 장면을 모두 생성하고 직접 확인한다.
3. 이미지에서 직접 보이는 `observed_features`, 추정 `identity_candidate`, 여러 타일 사물의 `part_role`, `confidence`를 분리한다. 타일셋 이름이나 v31 AI 분류만으로 판정하지 않는다.
4. 출처·좌표·레이어·GID, 원본 TMX와 PNG SHA, 제거 전후 픽셀 변화, 주변 누락과 `height_mismatch`를 보존한다. 픽셀 근거가 부족하면 `held` 처리한다.
5. 이미지 관찰 `observed`, 잠정 후보 `candidate`, 공식 Local ID 매핑 검증 `mapping_verified`, TileZed 정합, 최종 `certified`를 구별한다. TileZed·공식 매핑 검증 전 최종 인증 0.
6. 기존 폐기된 TMX 2D 평면도 엔진은 이 분석에 사용하지 않는다.

## 계보·보존
- v36 원본 전체 SQLite, v46 원본 테이블 `v46__`, v47 병합 `v47__`와 이후 v48~v65 작업 버전이 최신 DB에 검색 가능하게 보존된다.
- v36 과거 보고 후보 2,291종과 감사 가능한 2,156종의 차이 135종, v36/v46 후보 단어 충돌 256종은 자동 재분류하지 않는다.
- 사용자 수동 검수 80종과 재검수 의견은 최신 누적에 자동 병합되지 않은 별도 계보이며 함부로 수정하거나 합산하지 않는다.
- 과거 `analysis/archive/`, `analysis/current/v49/` ~ `v59/`, `Tiles/`, `B4220.3_MapExport_256/`, `checkpoints/` 원본은 삭제·덮어쓰기 금지.

## 최신 작업 (v65 대량 검수)
- 최신 v64 물리 SQLite를 SHA-256·무결성 검증 복원하고 `analysis_queue`의 미관찰 2,337종에서 **48개 중복 없는 신규 키**를 선정했다.
- `checkpoints/v65_preview/`: 원본 PNG A, TMX 같은 층 5×5 B, 대상 한 배치만 제거한 C, 다른 TMX 실배치 D 및 2×2 비교판 **240개 JPEG**를 원본 TMX 좌표·레이어·GID·PNG/TMX SHA-256·B-C 픽셀 변화와 함께 저장했다.
- `checkpoints/v65/observations.tsv` 및 `observations.csv`: **48종 직접 이미지 판독; 잠정 후보 37종, 보류 11종**, 중복 0종. 형태 관찰과 기능 추론을 분리 기록했다.
- 잠정 후보 예: 흰 욕조 조각과 수전, 갈색 안내 카운터 모서리, 검은 난간형 침대, 베이지 쿠션 안락의자, 전신주 원통 설비, 녹색·흰색 4구 오븐 레인지, 탁상전화, 석재 아치형 문틀, 파이프 묶음, 사각 통풍 덕트, 꽃다발·플랜터·관상식물.
- 보류 11종: `fixtures_bathroom_01/47·52·56·59`, `furniture_bedding_01/67·72·73·75`, `appliances_cooking_01/3`, `location_business_machinery_01/52`, `location_business_office_generic_02/18`. 이미지상 외형이 보이더라도 B-C 기여가 없거나 미소하고 정확한 배치·조립 역할이 불명확하다.
- `checkpoints/v65/v65_이미지내장_검수.html`: 증거 JPEG **240장 내장**, `v65_증거_48종_A_B_C_D.zip`: **244항목 ZIP CRC PASS**, 이미지 240/240 로딩 PASS.
- `analysis/current/v65/MANIFEST.json`: 이전 모든 SQLite 테이블 보존; 물리 SQLite **84,279,296바이트**, SHA-256 **3f5847935af80b89fb62630820a47ce6b1e9424af00051fee0307a9668181789**. `scripts/build_unified_v65.py`, `scripts/restore_unified_v65.py`, `checkpoints/v65/verify_delta.py`로 고유키·DB 무결성·재복원 확인.
- 공식 PNG–TMX Local ID 높이 불일치와 TileZed 검증은 미완료로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. 기존 v36~v64 계보 및 사용자 직접 검수 80종을 보존.

## 다음 작업과 GitHub 규칙
- 다음 버전은 v65 통합 DB의 **2,289종 미관찰 대기열**에서 시작한다. 사용자 수동 검수 80종은 별도 유지한다.
- 새 작업 종료마다 실제 A/B/C/D 판독 → 근거 CSV/SQLite/이미지 내장 HTML/증거 ZIP → 중복·SQLite·PNG·ZIP CRC 검증 → 새 버전 체크포인트 → `PROJECT_STATE.json` → `docs/HANDOFF.md`를 갱신한다.
- GitHub 커밋 제목은 한국어를 기본으로 쓰고 원본 자산과 기존 버전을 변경하지 않는다.
- **공개 저장소**에 토큰·개인정보·비공개 대화 원문을 올리지 않는다.
