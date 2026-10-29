# GitHub Actions — 현행 / 과거 재현용 구분

현재 기준은 **v240 물리 통합 10,042종**이며, 과거 `v49`~`v196`이나 v117~v239의 빌드 워크플로는 당시 검수·SQLite 증거 재현을 위해 보존합니다.

| 자동화 | 상태·용도 |
|---|---|
| `build-v240-physical-master.yml` | **v240 생성의 검증된 실행 이력**: v196 DB 256테이블 보존 + 신규 4,633 키 병합. 연결된 작업 브랜치 push에서만 실행 |
| `sync-handoff.yml` | **현행** `main`의 최신 `PROJECT_STATE.json`에서 문서 요약 재생성 |
| `validate-source-archives.yml`, `verify-analysis-archives.yml` | 역사적 소스 DB 무결성 검사 |
| `build-unified-v49.yml` ~ `build-unified-v111.yml` 등 | **과거 재현용**. 현재 파일을 새로 만들 때 쓰지 않음 |
| 그 외 vNN 스크립트/작업별 워크플로 | 해당 단계의 이미지/판독 실험 기록. 경로·트리거를 확인한 뒤 사용 |

GitHub API 확인 시 이 디렉터리는 **254개 항목**입니다. 다수의 워크플로는 과거 작업 브랜치만 트리거하도록 제한되어 있어, 전부가 현재 `main`에서 자동 실행되는 것은 아닙니다.

오래된 자동화와 브랜치 삭제는 이력·재현성·실패한 실험 원인에 영향을 줄 수 있어 보류했습니다. [브랜치/워크플로 정리 점검](../../docs/BRANCH_AND_WORKFLOW_AUDIT_2026-10-30.md).

원본 PNG/TMX, 사용자 판정, 과거 데이터 삭제 금지. 인수인계·새 커밋 제목은 가능하면 한글을 사용하되 실행 코드·파일명·GitHub Actions 키워드는 원형을 유지합니다.
