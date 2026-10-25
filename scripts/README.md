# 데이터베이스 생성·복원·검증 프로그램

프로젝트의 분석 결과를 복원하고 새 버전으로 통합하는 Python 프로그램입니다.

## 지금 사용하는 명령

```bash
# 최신 v59 통합 SQLite 복원
python3 scripts/restore_unified_v59.py

# 프로젝트 상태 검증
python3 scripts/validate_project.py

# 신규 v57 체크포인트의 고유 키·후보·보류 검사
python3 checkpoints/v59/verify_delta.py

# 프로젝트 인수인계서 갱신
python3 scripts/generate_handoff.py
```

## 프로그램별 역할

| 프로그램 | 설명 |
|---|---|
| `restore_unified_v59.py` | **최신 v59 단일 SQLite 복원 및 SHA-256 검증** |
| `build_unified_v59.py` | v58 통합 DB에 v59 신규 12종을 물리적으로 추가 |
| `restore_unified_v50.py`, `restore_unified_v51.py`, `restore_unified_v52.py`, `restore_unified_v53.py`, `restore_unified_v54.py`, `restore_unified_v55.py`, `restore_unified_v56.py` | 과거 통합 DB 버전 복원 |
| `restore_unified_database.py` | 최초 물리 통합 v49 복원 |
| `restore_source_databases.py` | 과거 v36·v46 원본 SQLite 복원 |
| `restore_merged_evidence.py` | v47 병합 색인 DB 복원 |
| `validate_reconciliation.py` | 옛 데이터의 교집합·중복·감사 근거 검증 |
| `validate_project.py` | 프로젝트 상태 파일의 형식 및 수치 점검 |
| `generate_handoff.py` | 최신 상태를 사람용 인수인계 문서로 출력 |

버전 이름이 포함된 프로그램은 **과거 작업 재현용으로 보존**합니다. 다음 신규 분석에서는 이전 코드를 덮어쓰지 않고 새 버전으로 추가합니다.

## v59 이번 작업

- `generate_v59_preview.py`: 최신 v58 미관찰 큐에서 원본 A/B/C/D JPEG 60장을 생성.
- `build_unified_v59.py`: v58 SQLite의 모든 기존 테이블을 보존하며 검수된 12종을 삽입.
- `restore_unified_v59.py`: 압축 7파트 SHA-256, SQLite 무결성, 타일 5,409/관찰 3,012/후보 2,612/미관찰 2,397/인증 0 검증.
- `build_v59_review_html.py`: 이미지 60장 내장 HTML과 JPEG 로딩·ZIP CRC를 검증.
