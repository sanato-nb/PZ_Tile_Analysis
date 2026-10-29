# 체크포인트 — 과거 분석 이력 보존

**현재 통합 결과는 `checkpoints/`가 아니라 [v240 통합 마스터](../review/v240_unified_10042_2026-10-30/)에 있습니다.**

이 폴더의 `v48/`, `v49/` ... `v113/` 등은 초창기 원본 타일의 신규 관찰, 잠정 후보/보류, TMX 증거·검증 코드·ZIP을 버전별로 기록한 **역사적 체크포인트**입니다.

- **v240 전체 10,042종**: [MASTER_ALL_10042.csv](../review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv)
- **v240 활성 9,587종**: [ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv](../review/v240_unified_10042_2026-10-30/ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv)
- **v240 비활성 455종**: [EXCLUDED_ARCHIVE_455.csv](../review/v240_unified_10042_2026-10-30/EXCLUDED_ARCHIVE_455.csv)
- **v240 물리DB**: [analysis/current/v240/](../analysis/current/v240/)
- **버전별 원본 증거 색인**: [docs/HISTORY_INDEX.md](../docs/HISTORY_INDEX.md)

기존 `observations.tsv`/`verify_delta.py`와 증거 이미지는 과거 신규 관찰 당시 판정과 중복 검사를 재현하기 위한 자료입니다. 옛 README의 'v57 최신' 표현은 역사적 시점이므로 더 이상 현재 진행률로 사용하지 않습니다.

**기존 체크포인트를 덮어쓰거나 삭제하지 마세요.** 새 보고서는 버전별로 추가하고, 이미지 관찰/잠정 정체/보류/공식 인증을 구별합니다.
