# 프로젝트 좀보이드 B42 타일 정체 분석 — 자동 인수인계

> GitHub 기준일: 2026-10-25. **이 문서는 PROJECT_STATE.json에서 자동 생성됩니다.**

## 최우선 목표

이름 추측이 아닌 **원본 PNG의 실제 이미지**를 TMX 주변 5×5 타일과 조립해 관찰하고, 분할된 사물의 부품 역할과 오염·벽·지붕·가구 구성 요소를 구별한다. A=원본, B=조립, C=선택 배치 제거, D=다른 위치. TileZed와의 정합 검증 없이 확정 금지.

## 기준 범위

- TMX 원본: 31_45(2).tmx, 31_46(2).tmx
- TMX 고유 사용 타일: **5,409종**, 전체 배치 302,177건.

## 실제 원본 SQLite로 중복 제거 완료 (v47)

| 범위 | 수량 |
|---|---:|
| v36 기존 이미지 관찰 | **2,509종** |
| v37~v46 별도 기록 | **477종** |
| 두 계보의 중복 키 | **402종** |
| v37~v46 중 진짜 신규 | **75종** |
| **통합 이미지 관찰** | **2,584종 / 5,409종 (47.77%)** |
| 미관찰 | **2,825종** |
| 최종 정체 인증 | **0종** |

두 실제 DB에서 (tile_set_locator, local_id) 합집합을 계산해 **2,584종**으로 검증 완료. 보고 수치 2,986을 그대로 합하지 않는다.

## 잠정 후보 수량 주의

- v36의 과거 문서 보고: 2,291종; v36 시각 증거 테이블에서 실제 키와 후보를 재검증한 수: **2,156종**. 차이 135종은 보고 및 증거 키 간 불일치로 남긴다.
- v46 직접 확인 후보: **402종**.
- 감사 가능한 잠정 후보 키 합집합: **2,302종**. **정체 확정 수가 아니다.**
- 두 기록이 다른 단어로 후보를 표시한 동일 키 **256종**: 두 가설 모두 보존, 이미지 재검토 전 자동 병합 불가.

## 원본 DB와 재현

- GitHub 복구 스크립트: `python3 scripts/restore_source_databases.py /tmp/pz_originals`
- 이 스크립트가 `analysis/archive/v36/`, `analysis/archive/v46/`의 분할 파일을 읽고 SHA-256 검증 뒤 두 원본 SQLite를 복원한다.
- 병합 경량 SQLite 복원: `python3 scripts/restore_merged_evidence.py /tmp/pz_merged.sqlite`
- 통합 표: `analysis/imports/merged_catalog_5409.csv`
- 상세 증거·후보 충돌: `analysis/imports/all_observation_records.csv`, `analysis/imports/conflicting_candidates.csv`
- SQL 원본·CSV·증거를 혼동하지 말 것. 경량 병합 DB는 모든 과거 보조 테이블을 복제한 원본 DB가 아니다.

## 최신 물리 통합 SQLite (v49)

- **v36 전체 원본 SQLite + v46 전체 데이터 테이블 + v47 병합 색인 + v48·v50 신규 관찰 기록**을 한 SQLite로 통합했습니다.
- 단일 테이블 `tile_catalog`: **2,614/5,409종 (48.33%)**, 미관찰 2,795종, 잠정 후보 2,325종, 최종 인증 0종.
- SHA-256 검증과 전체 복원 방법: `analysis/current/v49/MANIFEST.json`, `scripts/restore_unified_database.py`.
- 과거 DB는 별도 보존합니다. 신규 체크포인트는 GitHub에 저장된 TSV 필드까지 통합되며, 로컬 보조 SQLite에만 남은 추가 메타데이터와 고해상도 이미지 바이너리는 아직 GitHub 본문에 모두 포함되지 않았습니다.

## 최신 체크포인트 (v48)

- 새로 직접 관찰: **30종** (잠정 후보 23, 보류 7).
- 중복 제거 누적 관찰: **2,614/5,409종 (48.33%)**.
- 아직 미관찰: **2,795종**. 최종 인증 0종.
- 기록: `checkpoints/v48/observations.tsv` (v47 원본 DB와 별도로 보존).

## 다음 실제 작업

1. Run python3 checkpoints/v48/verify_delta.py; preserve both original v36/v46 SQLite archives and v47 merged index.
2. Review 7 held v48 cases using alternative TMX placements and PNG version checks.
3. Preserve 256 candidate wording conflicts and 135 historical v36 candidate-discrepancy cases.
4. Continue A/B/C/D visual review on 2,795 as-yet-unobserved unique tiles.
5. Require official mapping and TileZed checks before any final certification.

## 불변 원칙

- 이미지 직접 관찰, 추론 후보, PNG-TMX Local ID 검증, TileZed 렌더 검증, 최종 인증을 분리한다.
- 역사적 v31 AI 분류를 증거로 삼지 않는다.
- 기존 `Tiles/`와 `B4220.3_MapExport_256/`의 원본은 절대로 수정하지 않는다.
- 모든 작업 종료마다 PROJECT_STATE.json과 checkpoints/를 기록하고 GitHub Actions 검증 결과를 확인한다.
