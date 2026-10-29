# 다음 채팅에서 프로젝트 이어가기 — v240 최신 기준

> **이미지/스프라이트 새 분석을 수행할 때**는 [v242 분석 매뉴얼](SPRITE_VISUAL_ANALYSIS_PLAYBOOK.md), [1분 빠른 판정표](SPRITE_ANALYSIS_QUICK_REFERENCE.md), [레코드 템플릿](SPRITE_REVIEW_RECORD_TEMPLATE.json)을 먼저 확인하세요. [이미지 분석 시작 전문](SPRITE_VISUAL_NEXT_CHAT_PROMPT.md)을 복사해 사용할 수도 있습니다.

이 저장소는 **좀보이드 B42 원본 타일 10,042종의 잠정 정체·부품 분석**과 Minecraft 월드 변환 준비 작업을 담습니다.

## 시작 시 우선 확인할 파일

1. [현재 상태](CURRENT_STATUS.md), [파일/폴더 안내](REPOSITORY_MAP.md).
2. [PROJECT_STATE.json](../PROJECT_STATE.json) (최신 `v240`; 과거 버전 스냅샷은 별도 필드에 보존).
3. [v240 전체10,042종 CSV](../review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv), [활성9,587 CSV](../review/v240_unified_10042_2026-10-30/ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv), [비활성455 CSV](../review/v240_unified_10042_2026-10-30/EXCLUDED_ARCHIVE_455.csv).
4. [v240 물리DB](../analysis/current/v240/MANIFEST.json), [복원 스크립트](../scripts/restore_v240_master.py).
5. [ANALYSIS_RULES.md](ANALYSIS_RULES.md), [AGENTS.md](../AGENTS.md), [v238 신규키 증거](../review/v238_integrated_master_2026-10-29/), [v239 보류439 감사](../review/v239_held439_independent_source_crosscheck_2026-10-30/).

## 채팅에 전달할 핵심 지시

**"GitHub `sanato-nb/PZ_Tile_Analysis`의 `main`을 먼저 가져와 최신 상태를 확인해. v240 기준 전체10,042종, 활성9,587종, 비활성455종(보류439·사용자미판정10·이전사용자제외6). 기존 439종과 수동 제외는 내가 새 방법을 지시하기 전까지 활성화하지 마. 원본 PNG/TMX 및 과거 256개 부모 SQLite 테이블, 수동검수 원문을 삭제·덮어쓰지 마. A 실제 픽셀을 먼저 보고 B 실제 TMX 장면·C 단독 제거 및 가림을 별도로 판단하며, 공식 같은 키 대체 A가 없는 D는 검증 완료로 주장하지 마. 활성 목록도 확정 블록 매핑이 아니며 공식 정체/TileZed 인증은 0이야. 새 작업은 출처·무결성을 검증해 버전별 파일과 매니페스트로 남겨."**

이전 [v196 새 채팅 프롬프트](NEW_CHAT_START_PROMPT_V196_2026-10-29.txt)는 **역사적 참고 자료**이며 현재 v240 명세를 대체하지 않습니다.
