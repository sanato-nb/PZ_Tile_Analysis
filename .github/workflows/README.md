# GitHub Actions 자동화

이 폴더에는 데이터베이스 복원, 무결성 검사, 인수인계 갱신을 자동 수행하는 GitHub Actions 설정이 있습니다.

| 자동화 파일 | 역할 |
|---|---|
| `sync-handoff.yml` | `PROJECT_STATE.json`을 확인하고 최신 `docs/HANDOFF.md`를 자동 갱신 |
| `build-unified-v52.yml` | **현재 v52 통합 SQLite 생성·복원·SHA-256 검증** |
| `build-unified-v49.yml` ~ `build-unified-v51.yml` | 이전 통합 DB 버전의 재현용 자동화 |
| `validate-source-archives.yml` | 과거 원본 SQLite 복원·검사 |
| `verify-analysis-archives.yml` | 원본 및 병합 아카이브의 검증 |

**앞으로 새로 생성하는 커밋의 제목과 자동화 이름은 한글로 작성합니다.** 다만 Python 명령어·파일명·GitHub Actions 문법처럼 실행에 필요한 영문은 그대로 유지합니다.

과거 영어 커밋 메시지는 무리하게 변경하지 않습니다. 기존 커밋을 고치려면 Git 기록을 재작성해야 하므로 프로젝트의 추적 가능성이 깨질 수 있습니다.
