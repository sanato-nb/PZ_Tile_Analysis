# 프로젝트 좀보이드 B42 → Minecraft 맵 변환을 위한 타일 분석

> **최신 상태 v255 (2026-10-30):** [최신 타일 통합 정의 10,042종 및 보류439·사용자68](review/v255_latest_integrated_10042_2026-10-30/README.md) · [최신 평면도 HTML](floorplan/current/v255_floorplan_latest_user_priority.html) · [실물 SQLite 260테이블/복원](analysis/current/v255/MANIFEST.json). 원본 9587 활성 / 455 비활성 보존, 사용자 동의/잠정 관찰과 공식 TileZed 인증을 구분(최종인증0).

**현재 기준: v240 통합 데이터베이스 (2026-10-30)** · 원본 PNG/TMX로 개별 타일의 사물·부품·연결·방향을 분석하고, 나중에 Minecraft 월드로 재현하기 위한 프로젝트입니다.

> **빠른 시작:** [현재 상태](docs/CURRENT_STATUS.md) · [저장소 안내](docs/REPOSITORY_MAP.md) · **[v242 이미지/스프라이트 분석 매뉴얼](docs/SPRITE_VISUAL_ANALYSIS_PLAYBOOK.md)** · [빠른 판정표](docs/SPRITE_ANALYSIS_QUICK_REFERENCE.md) · [새 채팅/작업 이어가기](docs/NEXT_CHAT_PROMPT.md)

## 최신 기준 데이터

<!-- AUTO_README_START -->
> **최신 통합: v255 (2026-10-30)** — 타일 정체 후보를 최신 자료로 통합했으며 공식 정체 인증과는 다릅니다.

| 항목 | 최신 기준 |
|---|---:|
| 전체 TMX 고유 타일 | **10,042종** (기존 5,409 + 신규 4,633) |
| 이미지 잠정 관찰 기록 | **10,007/10,042 (99.65%)**, 역사적 기록 유지 |
| 활성 잠정 목록 / 비활성 보존 | **9,587종 / 455종** |
| 최근 A 우선 시각 재판독 통합 | **439종** (실제 다른 위치 251 + 단일 위치 188) |
| 사용자 수동 판정 우선 | **68종** (명시 16, 미선택=기존 잠정에 동의 52) |
| 물리 SQLite | **260테이블**, 부모 v240 258테이블 보존 |
| 공식 PNG↔Local ID / TileZed / 정체 최종 인증 | **0 / 0 / 0종** |

- [v255 전체 10,042종 잠정 마스터](review/v255_latest_integrated_10042_2026-10-30/MASTER_ALL_10042_LATEST_PREFERRED.csv) · [보류439 최신 후보](review/v255_latest_integrated_10042_2026-10-30/HELD439_LATEST_VISUAL_USER_PRIORITY.csv) · [사용자68 우선 판정](review/v255_latest_integrated_10042_2026-10-30/USER68_EFFECTIVE_ROWS.csv)
- [물리 SQLite 매니페스트](analysis/current/v255/MANIFEST.json) · [복원 스크립트](scripts/restore_v255_master.py) · [v255 최신 평면도](floorplan/current/v255_floorplan_latest_user_priority.html).
- B−C=0은 후속 레이어의 가림일 수 있습니다. 보류439와 사용자 제외16은 활성으로 승격하지 않았습니다. 사용자 의견과 AI 잠정 이름은 공식 게임 ID·Minecraft 블록 인증이 아닙니다.
- SQLite SHA256: \`25df5bcd9ef1f332bc1178ae711ec09f43e070bbf8cc3c33b4e822a0a1766791\`. 기존 84 TMX, 원본 PNG, 과거 SQLite, 수동 기록, v240/v243 아티팩트 모두 보존합니다.
<!-- AUTO_README_END -->

**활성 9,587종은 마인크래프트 변환이 확정된 블록 목록이 아닙니다.** 기존 관찰·잠정 형태 분석을 활용하는 범위이며 재질·부분 역할·방향·공식 Local ID 매핑은 아직 검증이 필요합니다. 보류 439종은 추가 수동 검수나 다른 실험을 위해 별도 보관 중입니다. `99.65%`는 **이미지 잠정 관찰 기록률**이지 정체 정확도가 아닙니다.

## 파일은 여기에서 시작하세요

| 필요한 것 | 최신 링크 | 주의 |
|---|---|---|
| **전체 10,042종 단일 CSV** | [MASTER_ALL_10042.csv](review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv) | 타일 키 중복 없이 기존+신규 통합 |
| **활성 9,587종** | [ACTIVE_9587.csv](review/v240_unified_10042_2026-10-30/ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv) | 검수·후속 변환의 잠정 대상 |
| **비활성 455종** | [EXCLUDED_ARCHIVE_455.csv](review/v240_unified_10042_2026-10-30/EXCLUDED_ARCHIVE_455.csv) | 보류439·사용자 제외16, 삭제 아님 |
| **통합 SQLite** | [analysis/current/v240/](analysis/current/v240/) | 8개 .b64 압축 조각 + 매니페스트 |
| **복원 스크립트** | [restore_v240_master.py](scripts/restore_v240_master.py) | SHA-256 및 SQLite 무결성 검사 |
| **신규 4,633종 근거** | [v238 통합 검수](review/v238_integrated_master_2026-10-29/) | A/B/C·기존 판정·출처·보류 |
| **보류439 추가 대조** | [v239](review/v239_held439_independent_source_crosscheck_2026-10-30/) | 재검수 이력/미해결 상태 분리 |

## 2D 평면도 시스템 — v243

**[v243 평면도 HTML 실행본](floorplan/current/v243_floorplan_v240_priority.html)** · [사용법](floorplan/README.md)

기존 v22.1 평면도(기둥 보정 포함)에 **v240 통합 타일 10,042종의 잠정 정의를 우선 적용**했습니다. 활성 9,587종은 새 후보와 A 형태 설명을 먼저 표시하고, 기존 v22.1의 60,174개 정의는 정보가 없는 부분에서 보조로 사용합니다. 사용자 제외 16종과 보류 439종은 활성화하지 않고 과거 데이터/비활성 기록을 유지합니다. 실제 TMX를 불러와 층별 평면도·벽/기둥·가구·좌표 검사·PNG 저장을 수행합니다.

**평면도 표시 기준과 공식 정체 인증은 다릅니다.** 새 후보는 잠정이며, Minecraft 물리 블록 변환 규칙까지 확정한 버전은 아닙니다.

## 전체 SQLite 복원

저장소를 내려받은 뒤 프로젝트 루트에서 아래 명령을 실행합니다. Python 3 표준 라이브러리만 필요합니다.

```bash
python3 scripts/restore_v240_master.py PZ_Tile_Analysis_v240_MASTER_10042.sqlite
```

일반 최신 버전 복원기도 v240을 사용하도록 연결했습니다.

```bash
python3 scripts/restore_latest_unified.py PZ_Tile_Analysis_latest.sqlite
```

복원된 DB에는 `v240_tile_master_10042`(전체), `v240_active_tile_master`(활성 뷰), `v240_excluded_archive_455`(보류/제외) 등이 있고, 기존 v196의 256개 테이블도 변경 없이 포함되어 있습니다. 기존 출력 파일은 덮어쓰지 않도록 검사합니다.

## 분석·검수 원칙

**A:** 원본 PNG 스프라이트를 먼저 본다 → **B:** 진짜 TMX의 원래 좌표·층·레이어에서 5×5 주변 배치를 본다 → **C:** 그 위치의 목표 배치 한 개를 제거해 B−C의 실제 변화를 확인한다 → **D:** *같은 타일 키에 대응하는 검증된 다른 공식 A*가 존재할 때만 동일 B 위치에서 치환 실험한다.

**B−C=0은 투명 또는 물체가 없다는 증거가 아닙니다.** 벽·상위 레이어·인접 물체로 가려졌을 수 있습니다. 단일 타일의 부품 형태와 B의 완성된 집·가구·철탑을 혼동하지 말고, 불분명하면 보류를 유지합니다. 정확한 정의는 [검수 규칙](docs/ANALYSIS_RULES.md)에 있습니다.

## 보관 및 이력

- [Tiles/](Tiles/): 원본 타일셋 PNG — **변경 금지**
- [B4220.3_MapExport_256/](B4220.3_MapExport_256/): 원본 TMX — **변경 금지**
- [review/](review/), [analysis/current/](analysis/current/), [checkpoints/](checkpoints/): 버전별 **과거 증거**. 숫자가 크다는 이유만으로 원본 판정을 덮어쓰지 않습니다.
- [docs/HISTORY_INDEX.md](docs/HISTORY_INDEX.md): 버전별 핵심 증거 및 원본/과거 문서 색인.
- [docs/history/ROOT_README_BEFORE_V241.md](docs/history/ROOT_README_BEFORE_V241.md): 이전 루트 README의 상세 연대기 원문 보존.
- [AGENTS.md](AGENTS.md): AI 작업 규칙의 역사적 세부 내용. 최신 상태 판단은 **v240 매니페스트와 [PROJECT_STATE.json](PROJECT_STATE.json)** 우선.

이번 저장소 정리는 **문서·최신 포인터·복원 도구를 정돈하는 비파괴 작업**입니다. 이전 검수 파일, Git 브랜치, GitHub Actions 이력은 임의 삭제하지 않습니다.
