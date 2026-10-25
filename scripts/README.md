# 데이터베이스 생성·복원·검증 프로그램

프로젝트의 분석 결과를 복원하고 새 버전으로 통합하는 Python 프로그램입니다.

## 지금 사용하는 명령

```bash
# 최신 v53 통합 SQLite 복원
python3 scripts/restore_unified_v53.py

# 프로젝트 상태 검증
python3 scripts/validate_project.py

# 신규 v53 체크포인트의 고유 키·후보·보류 검사
python3 checkpoints/v52/verify_delta.py

# 프로젝트 인수인계서 갱신
python3 scripts/generate_handoff.py
```

## 프로그램별 역할

| 프로그램 | 설명 |
|---|---|
| `restore_unified_v53.py` | **최신 v53 단일 SQLite 복원 및 SHA-256 검증** |
| `build_unified_v53.py` | 이전 v52와 v53 신규 관찰을 물리적으로 통합 |
| `restore_unified_v50.py`, `restore_unified_v51.py`, `restore_unified_v52.py` | 이전 통합 DB 버전 복원 |
| `restore_unified_database.py` | 최초 물리 통합 v49 복원 |
| `restore_source_databases.py` | 과거 v36·v46 원본 SQLite 복원 |
| `restore_merged_evidence.py` | v47 병합 색인 DB 복원 |
| `validate_reconciliation.py` | 옛 데이터의 교집합·중복·감사 근거 검증 |
| `validate_project.py` | 프로젝트 상태 파일의 형식 및 수치 점검 |
| `generate_handoff.py` | 최신 상태를 사람용 인수인계 문서로 출력 |

버전 이름이 포함된 프로그램은 **과거 작업 재현용으로 보존**합니다. 다음 신규 분석에서는 이전 코드를 덮어쓰지 않고 새 버전으로 추가합니다.
