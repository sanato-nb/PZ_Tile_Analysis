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

## 최신 물리 통합 SQLite (v60)

- **v36·v46 원본 테이블 + v47 병합 색인 + v48부터 v60까지의 모든 신규 체크포인트**를 한 SQLite에서 조회할 수 있습니다.
- 단일 테이블 `tile_catalog`: **3,024/5,409종 (55.91%)**, 미관찰 2,385종, 잠정 후보 2,621종, 최종 인증 0종.
- SHA-256 검증과 전체 복원 방법: `analysis/current/v60/MANIFEST.json`, `scripts/restore_unified_v60.py`.
- 과거 DB는 별도 보존합니다. 최신 체크포인트 이미지의 GitHub 보관 여부: **보관됨**. 이전 버전의 로컬 보조 이미지·메타데이터는 각 버전 안내를 따릅니다.

## 최신 체크포인트 (v60)

- 새로 직접 관찰: **12종** (잠정 후보 9, 보류 3).
- 중복 제거 누적 관찰: **3,024/5,409종 (55.91%)**.
- 아직 미관찰: **2,385종**. 최종 인증 0종.
- 기록: `checkpoints/v60/observations.tsv` (이전 통합 DB와 별도로 보존).

## 다음 실제 작업

1. v60 통합 DB의 미관찰 2,385종을 PNG·TMX A/B/C/D 직접 관찰로 이어간다.
2. v60 보류 fixtures_bathroom_01/10·14 및 furniture_bedding_01/11의 B-C 변화 0 원인을 재검수한다.
3. v59 보류 appliances_com_01/3 및 v58 보류 appliances_com_01/82의 스프라이트 가림을 검토한다.
4. PNG 선언 높이 불일치와 Local ID 매핑을 TileZed에서 검증한다.
5. 사용자 수동 검수 80종 및 재검수 기록은 별도 계보로 보존하고 자동 합산하지 않는다.
6. v59 이하 모든 통합 SQLite·체크포인트·원본 PNG·TMX·충돌 기록을 변경하지 않는다.
7. v60 신규 12종 A/B/C/D+비교판 60장 JPEG를 checkpoints/v60_preview/에 보관한다.

## 불변 원칙

- 이미지 직접 관찰, 추론 후보, PNG-TMX Local ID 검증, TileZed 렌더 검증, 최종 인증을 분리한다.
- 역사적 v31 AI 분류를 증거로 삼지 않는다.
- 기존 `Tiles/`와 `B4220.3_MapExport_256/`의 원본은 절대로 수정하지 않는다.
- 모든 작업 종료마다 PROJECT_STATE.json과 checkpoints/를 기록하고 GitHub Actions 검증 결과를 확인한다.
