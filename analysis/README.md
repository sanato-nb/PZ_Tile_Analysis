# 분석 데이터 — 이제 GitHub에서 직접 복구 가능

- **통합 카탈로그**: `imports/merged_catalog_5409.csv` — 전체 5,409종, v36·v46 관찰/후보/충돌 상태.
- **모든 추출 가능한 버전별 개별 관찰**: `imports/all_observation_records.csv`.
- **추론 후보 용어 충돌**: `imports/conflicting_candidates.csv` (256개 동일 타일에서 서로 다른 잠정 이름).
- **중복 제거 근거**: `imports/RECONCILIATION_RESULT.json` 및 `imports/README_RECONCILIATION.md`.
- **가벼운 병합 SQLite**: `python3 scripts/restore_merged_evidence.py /tmp/merged.sqlite`.
- **실제 원본 v36/v46 SQLite 모두**: `python3 scripts/restore_source_databases.py /tmp/pz_originals`. 아카이브는 `archive/v36`, `archive/v46`에 base64 + xz 분할되어 있으며 SHA-256까지 검증한다.

분할 텍스트 파일은 압축 바이너리를 GitHub의 텍스트 API로 저장하기 위한 형식이다. **개별 조각 자체는 SQLite가 아니고**, 스크립트로 모두 복원해야 한다. 원본 TMX 및 PNG 파일은 기존 폴더에서 보존한다.

검증 수치: v36 2,509종 + 별도 v37~v46 477종 - 중복 402종 = **2,584종**, 관찰 47.77%. 남은 미관찰 2,825종. 최종 정체 인증 0종.

v36의 보고 후보 2,291종 중 원본 시각 증거 키로 재현 가능한 후보는 2,156종이며, 두 계보의 후보 키 합집합 2,302종은 여전히 잠정 정체 후보이다.
