# 버전별 핵심 자료 색인

이 문서는 과거 데이터를 삭제·이동하지 않고 **최신 통합본과 출처를 역추적하기 위한 색인**입니다. 오래된 README에 있는 '최신' 표현은 당시 시점의 기록입니다.

| 단계 | 주요 출처 | 의미 |
|---|---|---|
| v36~v47 | [analysis/imports/](../analysis/imports/) / [초기 SQLite 아카이브](../analysis/archive/) | 과거 5,409종 범위의 원본 관찰 계보 |
| v49~v113 | [checkpoints/](../checkpoints/) / [analysis/current/](../analysis/current/) | 원본 데이터 계승·개별 관찰·임시후보 |
| v115~v120 | [v117 A 소스 10,042](../review/v117_A_candidates_10042/) / [v119 A 신규 4,633](../review/v119_selected_A_new4633/) / [v120 B 맥락](../review/v120_B_context_new4632/) | 실제 원본 A 이미지/실제 B 장면 원천 증거 |
| v121~v132 | [v121 C 비교](../review/v121_C_diff_new4632/) / [review/](../review/) | 원래 TMX에서 목표 1타일 제거 증거, D 실험의 한계 |
| v133~v196 | [AGENTS.md](../AGENTS.md) / [v196 수동33](../review/v196_user_manual33/) | 과거 A/B/C 개별 QA, 사용자 잠정23·미판정10 |
| v197~v230 | [review/](../review/) | 기존 검수의 A 우선 2차 감사, 누락·가림·부품 혼동 위험 |
| v231~v237 | [review/](../review/) | 초기 0~159와 역사적 보류 키별 A/B/C 감사 |
| **v238** | [신규 4,633종 통합 마스터](../review/v238_integrated_master_2026-10-29/) | A/B/C·이전 후보·보류 상태 원장 |
| **v239** | [439 보류 재교차검증](../review/v239_held439_independent_source_crosscheck_2026-10-30/) | 439 키 출처 확인, v185의 3102 충돌 근거 |
| **v240** | [10,042종 전체 통합 CSV](../review/v240_unified_10042_2026-10-30/) / [물리 SQLite](../analysis/current/v240/) | **최신 통합 데이터: 전체 10,042, 활성 9,587, 비활성 455** |

## 역사 문서 보존

- [과거 루트 README 전체 원문](history/ROOT_README_BEFORE_V241.md): 초창기 v59~v80 상세 연대기 포함.
- [v196 채팅 인수인계](NEW_CHAT_HANDOFF_V196_2026-10-29.md): **v196 시점의 정확한 역사적 자료**, 현재 v240 요약과 구별.
- [PR #91~162 기록](PR_91-162_2026-10-29.md): 과거 버전별 병합 증거.
- [docs/HANDOFF.md](HANDOFF.md): 기존 긴 연대기/생성된 자동 요약은 보존, 새 현재 상태는 [CURRENT_STATUS.md](CURRENT_STATUS.md) 우선.

**원칙:** 역사적 데이터·원본 파일을 절대 일괄 삭제하지 않으며, Git 이력이나 버전별 SHA-256을 변경하는 폴더 이동도 별도 영향 분석 전에는 하지 않습니다.
