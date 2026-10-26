# 프로젝트 좀보이드 B42 타일 정체 분석 — 자동 인수인계

> GitHub 기준일: 2026-10-26. **이 문서는 PROJECT_STATE.json에서 자동 생성됩니다.**

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

## 최신 물리 통합 SQLite (v113)

- **v36·v46 원본 테이블 + v47 병합 색인 + v48부터 v113까지의 모든 신규 체크포인트**를 한 SQLite에서 조회할 수 있습니다.
- 단일 테이블 `tile_catalog`: **5,400/5,409종 (99.83%)**, 미관찰 9종, 잠정 후보 4,512종, 최종 인증 0종.
- SHA-256 검증과 전체 복원 방법: `analysis/current/v113/MANIFEST.json`, `scripts/restore_unified_v113.py`.
- 과거 DB는 별도 보존합니다. 최신 체크포인트 이미지의 GitHub 보관 여부: **보관됨**. 이전 버전의 로컬 보조 이미지·메타데이터는 각 버전 안내를 따릅니다.

## 최신 체크포인트 (v113)

- 새로 직접 관찰: **0종** (잠정 후보 0, 보류 0).
- 중복 제거 누적 관찰: **5,400/5,409종 (99.83%)**.
- 아직 미관찰: **9종**. 최종 인증 0종.
- 기록: `checkpoints/v113/user_review.csv` (이전 통합 DB와 별도로 보존).

## 다음 실제 작업

1. v113부터 신규 검수 대상은 analysis_queue 대신 v113_active_review_queue를 사용한다. 사용자가 8종을 활성 검수에서 제외했으며 과거 타일 키와 출처는 보존한다.
2. 남은 활성 f_bushes_1/66은 사용자 잠정 후보 풀 또는 꽃 계열 식물. 원본 A 알파 4,837픽셀이나 B-C 변화 0이므로 공식 Local ID·TileZed 정합 전 정체 확정 금지.
3. 제외 8종 중 사무실 3종은 잠정 크롭 투명, JUMBO 3종은 매핑 불확실한 빈 크롭, PNG 미확보 2종은 실제 투명 여부 미검증.
4. v36~v111 과거 DB 테이블·사용자 수동 검수 80종·PNG/TMX 원본은 삭제 또는 수정하지 않는다.

## 최신 v115 AI 실제 판독 결과 (2026-10-26)

- 기존 5,400종 이미지 관찰 중 정체 후보 미기록 888종을 A1/A2/B/C/D 74장으로 모델이 직접 재검토.
- 새 시각 후보 **882종(870 low/12 medium)**, 원본 문제로 보류 **6종**. 모두 시각적 계열·부품 *잠정 후보*이며 정체 완결 인증 아님. 기존 감사 가능 후보 **4,512종**은 변경 없음.
- 15×15 확대 **8종**의 전신주·가공 전선·통신 설비 B/C 비교. `appliances_com_01/3`은 전화·무전 통신기 형태 후보이며 가려진 대상. `appliances_com_01/96` 등은 전선 선분으로 잠정 식별.
- 실제 파일: `review/v115_ai_identity/AI_VISUAL_REVIEW_888.csv`, `review/v115_model_visual/`, `review/v115_extended_context/`, `docs/V115_AI_VISUAL_REVIEW_888.md`.
- 최신 통합 SQLite: `analysis/current/v115/MANIFEST.json` SHA-256 `4f0f0679c85d18a2ac87d440a0c41f9708348b0004e1efe231410e7f99ffae20`. 복원: `python3 scripts/restore_unified_v115.py /tmp/pz_latest.sqlite`. v115 별도 테이블에 888종 기록. 기존 관찰 5,400/5,409, 과거 후보 4,512, 미관찰 9, 사용자 제외 8, 최종 인증 0 보존.
- **주의:** 882개 전부 세부 정체를 최종 확정한 상태가 아니고 Local ID 공식 매핑·TileZed 검증은 0종. 특정 마크 블록에 자동 배정 금지.

## 최신 v116: 이미지 근거 미확보 6종 활성 제외 (2026-10-26)

- 사용자 요청에 따라 v115의 소스 이미지/격자 문제 보류 6종을 **추가 분석·재검수 대상에서 제외**했다. 기존 보류 이력 및 검수판은 그대로 보존한다.
- 이전 `v115_ai_held_queue`는 기록상 **6종**, 최신 `v116_active_v115_held_queue`는 **0종**이다. 이미지가 확인된 AI 잠정 후보 882종은 변경 없음.
- 이번 6종은 v113 이전 미관찰 사용자 제외 8종과 **서로 다른 작업 대기열의 제외**다. 과거 관찰 5,400종과 기존 감사 후보 4,512종, 최종 인증 0종도 불변.
- 최신 통합 DB 복원: `python3 scripts/restore_unified_v116.py /tmp/pz_latest.sqlite`. `analysis/current/v116/MANIFEST.json`, `checkpoints/v116/user_exclude_six.csv`, `docs/V116_USER_EXCLUDED_NO_IMAGES.md` 참조.
- **주의:** PNG 이미지가 없거나 Local ID가 불명확하다는 이유로 타일의 투명성·부재를 확정한 것은 아니다.

## 불변 원칙

- 이미지 직접 관찰, 추론 후보, PNG-TMX Local ID 검증, TileZed 렌더 검증, 최종 인증을 분리한다.
- 역사적 v31 AI 분류를 증거로 삼지 않는다.
- 기존 `Tiles/`와 `B4220.3_MapExport_256/`의 원본은 절대로 수정하지 않는다.
- 모든 작업 종료마다 PROJECT_STATE.json과 checkpoints/를 기록하고 GitHub Actions 검증 결과를 확인한다.
