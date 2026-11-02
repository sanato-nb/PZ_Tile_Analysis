# 로즈우드 가구 357종 최종 QA 인덱스

2026-11-02. 36개 독립 Draft PR에서 001~357번의 상세 검수 CSV와 MANIFEST를 조회하여 범위·중복·판정·CI 상태를 감사했다.

**357개 고유 번호 / 누락 0 / 중복 0 / 조건부 68 / 보류 289 / 게임 내 1:1 인증 0.**

자세한 결과는 [FINAL_QA_REPORT_KO.md](FINAL_QA_REPORT_KO.md), 번호별 기록은 [MASTER_INDEX_001_357.csv](MASTER_INDEX_001_357.csv), 보류 목록은 [DEFERRED_BACKLOG_289.csv](DEFERRED_BACKLOG_289.csv), 조건부 재검수는 [CONDITIONAL_RECHECK_068.csv](CONDITIONAL_RECHECK_068.csv) 참조.

바이너리 JPG/ZIP의 SHA-256·CRC는 이번 감사에서 독립 재계산하지 않았으며, 4개 PR의 CI 성공 기록도 미확인이다. 모든 원본 PR은 미병합 Draft로 유지했다.

검증: `python scripts/verify_rosewood_final_qa_357.py` (저장소 루트에서 실행).
