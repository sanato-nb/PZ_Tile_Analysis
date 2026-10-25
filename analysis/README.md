# 분석 결과와 통합 데이터베이스

이 폴더에는 **원본 분석 데이터, 이전 버전, 최신 통합 SQLite, 중복·충돌 감사 자료**를 보관합니다.

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `archive/v36/` | 기존 v36 원본 SQLite의 복원용 보관 파일 |
| `archive/v46/` | 기존 v46 원본 SQLite의 복원용 보관 파일 |
| `imports/` | v36·v46 병합 카탈로그, 출처별 관찰 기록, 후보 표현 충돌 및 검증 결과 |
| `current/v49/` | 첫 물리 통합 SQLite 복원 자료 |
| `current/v50/` | v50 누적 데이터베이스 복원 자료 |
| `current/v51/` | v51 누적 데이터베이스 복원 자료 |
| `current/v52/` | v52 과거 통합 SQLite 복원 자료 |
| `current/v53/` | 이전 v53 통합 SQLite 복원 자료 |
| `current/v54/` | **현재 최신 통합 SQLite 복원 자료** |

## 최신 통합 DB (2026년 10월 25일, v54)

| 항목 | 수량 |
|---|---:|
| 전체 분석 대상 | 5,409종 |
| 중복 제거한 이미지 관찰 | **2,850종 (52.69%)** |
| 미관찰 타일 | **2,559종** |
| 감사 가능한 잠정 정체 후보 | **2,491종** |
| 최종 정체 인증 | **0종** |

> 위 수치는 v54 생성 시점의 기록입니다. 새 버전이 생기면 루트 `PROJECT_STATE.json`의 `unified_database`가 우선입니다.

GitHub에 저장된 압축 조각을 모아 전체 SQLite를 복원합니다.

```bash
python3 scripts/restore_unified_v54.py
```

복원 후 `tile_catalog`에서 5,409종을 조회하고, `analysis_queue`에서 미관찰 타일을 선택할 수 있습니다.

## 기존 기록과 감사 자료

- `imports/merged_catalog_5409.csv` — v47 당시 전체 고유 키의 병합 색인
- `imports/all_observation_records.csv` — 복원된 원본 계보의 버전별 관찰 기록
- `imports/conflicting_candidates.csv` — 서로 다른 후보 표현이 있는 타일
- `imports/RECONCILIATION_RESULT.json` — v36·v46 중복 계산의 근거

v47 당시 2,584종은 **과거 병합 기준**이지 최신 관찰 수가 아닙니다. 이전 DB와 원본 자료는 삭제하거나 덮어쓰지 않습니다. **고해상도 A/B/C/D 이미지 전체는 아직 GitHub 통합 DB에 내장되지 않았으며**, 별도 분석 증거 ZIP에 보존됩니다.
