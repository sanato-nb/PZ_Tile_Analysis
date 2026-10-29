# 프로젝트 좀보이드 B42 → Minecraft 맵 변환을 위한 타일 분석

**현재 기준: v240 통합 데이터베이스 (2026-10-30)** · 원본 PNG/TMX로 개별 타일의 사물·부품·연결·방향을 분석하고, 나중에 Minecraft 월드로 재현하기 위한 프로젝트입니다.

> **빠른 시작:** [현재 상태](docs/CURRENT_STATUS.md) · [저장소 사용 안내](docs/REPOSITORY_MAP.md) · [새 채팅/작업 이어가기](docs/NEXT_CHAT_PROMPT.md) · [검수 원칙](docs/ANALYSIS_RULES.md)

## 최신 기준 데이터

<!-- AUTO_README_START -->
> **최신 통합: v240 (2026-10-30)** — 10,042종 통합이며 정체 인증 10,042종이 아닙니다.

| 항목 | 현재 기준 |
|---|---:|
| 전체 고유 타일 | **10,042종** (기존 5,409 + 신규 4,633) |
| 이미지 잠정 관찰 기록 | **10,007/10,042 (99.65%)** |
| 통합 활성 목록 | **9,587종** (잠정, 정체 미인증) |
| 별도 보류/제외 아카이브 | **455종** (보류439 + 사용자 미판정10 + 과거 추가6) |
| 물리 SQLite | **258테이블** (기존256 보존) |
| PNG↔Local ID / TileZed / 최종 정체 인증 | **0 / 0 / 0종** |

- [전체 10,042종](review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv) · [활성 9,587종](review/v240_unified_10042_2026-10-30/ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv) · [보류/제외 455종](review/v240_unified_10042_2026-10-30/EXCLUDED_ARCHIVE_455.csv)
- [물리 SQLite 매니페스트](analysis/current/v240/MANIFEST.json) · [복원 명령](scripts/restore_v240_master.py). 보류는 삭제하지 않았고 원본 PNG/TMX·사용자 원문·과거 검수 이력 모두 보존합니다.
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
