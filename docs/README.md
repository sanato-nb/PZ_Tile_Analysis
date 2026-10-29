# 프로젝트 문서 — v240 기준 안내

**현재 통합 데이터**는 [현재 상태](CURRENT_STATUS.md) → [저장소 지도](REPOSITORY_MAP.md) 순으로, **새 이미지 분석**은 [v242 경험 기반 분석 매뉴얼](SPRITE_VISUAL_ANALYSIS_PLAYBOOK.md) → [빠른 판정표](SPRITE_ANALYSIS_QUICK_REFERENCE.md) 순으로 읽으세요.

| 안내 | 용도 |
|---|---|
| [CURRENT_STATUS.md](CURRENT_STATUS.md) | **최신 v240** 전체10,042 / 활성9,587 / 보류·제외455 / SQLite258테이블 |
| [REPOSITORY_MAP.md](REPOSITORY_MAP.md) | 실제 필요한 마스터·원본 PNG/TMX·검수 증거·복원 코드 위치 |
| [NEXT_CHAT_PROMPT.md](NEXT_CHAT_PROMPT.md) | 새 ChatGPT 채팅/Work에서 바로 이어가기 |
| [HISTORY_INDEX.md](HISTORY_INDEX.md) | 오래된 검수/SQLite 계보, v238/v239/v240 출처 색인 |
| [BRANCH_AND_WORKFLOW_AUDIT_2026-10-30.md](BRANCH_AND_WORKFLOW_AUDIT_2026-10-30.md) | 브랜치229개·워크플로254개 이력 보호 및 후속 정리 기준 |
| [PROJECT_GOAL.md](PROJECT_GOAL.md) | 원본 A를 실제로 관찰해 타일의 사물·부품 정체를 알아내는 목표 |
| [ANALYSIS_RULES.md](ANALYSIS_RULES.md) | A/B/C/D 및 벽·상위층 가림 검증 원칙 |
| [SPRITE_VISUAL_ANALYSIS_PLAYBOOK.md](SPRITE_VISUAL_ANALYSIS_PLAYBOOK.md) | **v242 실제 오류 사례 기반 상세 분석 매뉴얼**: A 우선, 조각·모서리·기둥·방향·피/오염·가림 |
| [SPRITE_ANALYSIS_QUICK_REFERENCE.md](SPRITE_ANALYSIS_QUICK_REFERENCE.md) | 새 이미지 판독 시 바로 확인하는 표 |
| [SPRITE_REVIEW_RECORD_TEMPLATE.json](SPRITE_REVIEW_RECORD_TEMPLATE.json) | 타일 1개 단위 출처·A/B/C/D·불확실성 저장 템플릿 |
| [SPRITE_VISUAL_NEXT_CHAT_PROMPT.md](SPRITE_VISUAL_NEXT_CHAT_PROMPT.md) | 다음 채팅/모델에 동일 분석 규칙을 적용하는 시작 요청문 |
| [HANDOFF.md](HANDOFF.md) | 자동 요약+긴 역사 인수인계 |
| [history/ROOT_README_BEFORE_V241.md](history/ROOT_README_BEFORE_V241.md) | 예전 루트 README의 자세한 과거 연대기 원문 |

[NEW_CHAT_HANDOFF_V196_2026-10-29.md](NEW_CHAT_HANDOFF_V196_2026-10-29.md)와 예전 `V...` 이름의 문서는 각 **당시 기준의 역사적 체크포인트**입니다. '최신 v196', '최신 v57' 같은 과거 표현은 v240 최신 판단을 대체하지 않습니다.

기준 데이터는 [PROJECT_STATE.json](../PROJECT_STATE.json)의 `latest_checkpoint` = v240 및 [v240 매니페스트](../review/v240_unified_10042_2026-10-30/MANIFEST.json)입니다. 원본·과거 기록은 삭제하지 않습니다.
