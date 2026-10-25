# 좀보이드 B42 타일 정체 분석 — 중앙 AI 작업 지침 (v50)

## 프로젝트 목표
좀보이드 B42 TMX 두 개(31_45(2).tmx, 31_46(2).tmx)의 **실제 사용 고유 타일 5,409종**이 원본 PNG 이미지에서 어떤 사물·부품을 나타내는지 직접 관찰하고, TMX 장면과 비교해 잠정적으로 판정한다. 이름·옛 AI 분류로 정체를 자동 생성하지 않는다.

## 시작 시 항상 확인할 것
1. `PROJECT_STATE.json`에서 **`unified_database`와 `latest_checkpoint`를 우선 조회**한다. `reconciliation`의 2,584종(v47)은 보존된 옛 교집합 검증 기준이며 최신 총수로 사용하지 않는다.
2. `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 읽는다.
3. 최신 원본 기준: **v50 물리 통합 SQLite**. `python3 scripts/restore_unified_v50.py /tmp/pz_latest.sqlite` 실행 시 GitHub의 `analysis/current/v50/` 내 압축 조각 7개를 SHA-256 검증 후 복원한다.
4. v36·v46 전체 원본 DB, v47 병합, v48 신규 기록 및 v50 신규 관찰을 모두 하나의 SQLite에서 검색할 수 있다. 과거 `analysis/archive/`, `analysis/current/v49/`, 원본 `Tiles/` 및 `B4220.3_MapExport_256/`는 보존한다.
5. 2026-10-25 v50 작업 기준은 **관찰 2,643/5,409종(48.86%), 미관찰 2,766종, 감사 가능한 잠정 후보 2,343종, 최종 인증 0종**. 새 작업 후엔 이 수치를 하드코딩하지 말고 상태 파일을 먼저 조회한다.

## 실제 이미지 분석 규칙
- 고유 키 `(tile_set_locator,local_id)`로 중복을 계산한다. 신규 작업 대상은 최신 DB의 `analysis_queue`에서 선택하고, 이미 관찰한 키는 다시 신규로 세지 않는다.
- 반드시 **A 원본 PNG 크롭 · B TMX 동일 층 5×5 주변 합성 · C 해당 placement 하나만 제거 · D 다른 실제 사용 위치**를 준비하고 이미지에서 직접 보이는 외형을 기록한다.
- `observed_features`와 `identity_candidate`를 분리하며, 사물 전체와 여러 타일로 나뉜 부품의 역할을 구별한다.
- 원본 픽셀이 없거나 주변이 가려지고 PNG 버전·Local ID가 불일치할 가능성이 높으면 **held**로 보존한다.
- **관찰≠정체 후보≠PNG–TMX Local ID 공식 대응≠TileZed 검증≠최종 인증**. 원본 매핑·TileZed 검증 전에는 최종 인증 0을 유지한다.
- 현재 그림 합성은 TileZed 공식 렌더러가 아니라 근사 아이소메트릭이다. 과거 폐기한 2D 평면도 엔진은 분석 근거로 재사용하지 않는다.

## v50 물리 통합 DB 구조 및 주의
- `tile_catalog`(5,409종) / `analysis_queue`(미관찰 2,766종) / `v50_visual_review`(신규 29종).
- v36 원본 테이블은 원래 이름을 유지하고 v46 테이블은 `v46__`, v47은 `v47__` 접두어로 보존.
- v50: 신규 29종(잠정 후보 18, 보류 11), 기존 v49와 교집합 0. `checkpoints/v50/observations.tsv`와 `analysis/current/v50/MANIFEST.json` 참조.
- GitHub에 저장된 TSV의 관찰 필드는 통합되었으나, 이번 채팅의 고해상도 증거판 및 로컬 SQLite에만 있는 추가 메타데이터·픽셀 이미지는 **별도 체크포인트 ZIP**에 있다. GitHub에 이미지까지 올렸다고 주장하지 않는다.
- v36 과거 보고 잠정 후보 2,291종과 감사 가능한 2,156종 사이 차이 135종, v36/v46 후보 표현 충돌 256종은 미해결 그대로 보존한다.

## 종료 절차
새로운 A/B/C/D 육안 판독 및 기록 CSV/SQLite와 이미지 근거 생성 → 기존 DB 중복·충돌 검사 → 새 버전 통합 SQLite 및 체크포인트 GitHub 보관 → `PROJECT_STATE.json` 갱신 → GitHub Actions 복원/무결성 검증 및 `docs/HANDOFF.md` 갱신 → **정확한 관찰·잠정 후보·보류·미관찰·인증 수량**을 사용자에게 보고한다.

공개 GitHub 저장소에 비공개 대화 원문, 토큰 또는 민감한 개인정보를 올리지 않는다.
