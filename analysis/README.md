# 분석 데이터 보관 규칙

이 폴더에는 앞으로 고유 타일 정의 DB, 각 배치의 이미지 증거와 매핑 오류 내역을 보관한다.

권장 구조:
- `database/` — 실제 누적 SQLite 또는 LFS 포인터/릴리스 링크.
- `observations/` — 타일별 직접 관찰 CSV/JSONL.
- `evidence/` — PNG 원본 조각과 조립 장면 증거.
- `mapping_issues.csv` — 누락·투명·버전 차이 등. **아직 생성되지 않음**.

**중요:** 이 README만 있는 상태는 실제 DB나 증거 업로드 완료가 아니다. `PROJECT_STATE.json`의 `artifact_repo_path`가 null이면 해당 파일은 GitHub에 없는 상태다.

대용량 SQLite/ZIP은 Git 저장소에 매 버전 올리지 말고, Git LFS/릴리스/외부 원본 저장소 중 하나를 선택하고 SHA-256/버전 경로를 함께 기록한다. GitHub의 일반 파일 업로드 제한과 저장소 증가를 고려한다.
