# GitHub 저장소 이용 안내 — 최신 파일 우선

이 저장소는 오랜 이미지 검수 실험이 누적되어 `review/`, `scripts/`, `.github/workflows/`, `analysis/current/`에 **재현용 과거 버전**이 많습니다. **과거 파일을 지우거나 한 폴더에 몰아넣으면 상대 경로 및 SHA 증명이 깨질 수 있으므로 위치를 그대로 보존**했습니다. 이 문서는 찾기 쉬운 입구입니다.

## 1. 실제 업무에 사용할 파일

| 목적 | 현재 바로 사용할 위치 |
|---|---|
| 타일 10,042종 전체 | [v240 전체 CSV](../review/v240_unified_10042_2026-10-30/MASTER_ALL_10042.csv) |
| 비활성 제외 후 9,587종 | [v240 활성 CSV](../review/v240_unified_10042_2026-10-30/ACTIVE_9587_EXCLUDING_HELD_AND_MANUAL.csv) |
| 439 보류 + 16 사용자 제외 | [v240 별도 보관 CSV](../review/v240_unified_10042_2026-10-30/EXCLUDED_ARCHIVE_455.csv) |
| 최신 SQLite 복원 데이터 | [v240 SQLite 매니페스트](../analysis/current/v240/MANIFEST.json) |
| 통합 DB 복원 | [restore_v240_master.py](../scripts/restore_v240_master.py) |
| 프로젝트 최신 요약 | [CURRENT_STATUS.md](CURRENT_STATUS.md), [PROJECT_STATE.json](../PROJECT_STATE.json) |
| 분석 작업 규칙 | [ANALYSIS_RULES.md](ANALYSIS_RULES.md) |
| 새 채팅·후속 작업 | [NEXT_CHAT_PROMPT.md](NEXT_CHAT_PROMPT.md) |

## 2. 경로별 역할

| 폴더/파일 | 실제 역할 | 변경 방침 |
|---|---|---|
| `Tiles/` | 원본 B42 타일셋 PNG | **삭제·이름변경·픽셀 수정 금지** |
| `B4220.3_MapExport_256/` | 원본 TMX 지도 | **변경 금지** |
| `analysis/current/v240/` | 최신 물리 통합 SQLite 복원용 압축 파트 | 검증 완료한 산출물, 원본 보존 |
| `analysis/current/v196/` | 기존 5,409종과 과거 256테이블 최종 부모 | **역사적 보존** |
| `review/v240_unified_10042_2026-10-30/` | 전체/활성/제외 3종 단일 CSV | 최신 읽기용 마스터 |
| `review/v238_integrated_master_2026-10-29/` | 신규 4,633종 A/B/C·QA 출처 | 원본 대조 증거 |
| `review/v239_held439_independent_source_crosscheck_2026-10-30/` | 439종 출처 QA, 3102 예외 | 현재 보류 판단의 보조 자료 |
| `review/v197`~`v237` 및 그 이전 | 항목별 실물 시각 검수·보류 이력 | 보존, 필요 시 근거 추적 |
| `checkpoints/` | 초창기 이미지 관찰 및 복원 체크포인트 | 이력 보존 |
| `scripts/` | 현재 복원 및 역사적 빌드·검증 코드 | 최신/과거를 README에서 구분 |
| `.github/workflows/` | 과거 버전 재현과 현행 자동검사 | **이력 보호, 무분별한 대량 삭제 금지** |
| `docs/`, `AGENTS.md` | 현재 안내 및 장기간 누적된 검수 규칙 | 최신 상태와 역사 기록 구분 |

## 3. SQLite 복원

```bash
python3 scripts/restore_v240_master.py PZ_Tile_Analysis_v240_MASTER_10042.sqlite
```

완성된 DB에는 `v240_tile_master_10042` (전체 10,042), `v240_active_tile_master` (9,587 활성 VIEW), `v240_excluded_archive_455` (455 비활성 TABLE)이 있습니다. 기존 v196의 256개 테이블은 보존되어 있습니다.

## 4. 버전 명칭의 의미

`v240`은 **최신 통합 형식/검수 결과 합본**을 가리키며, 정체가 공식적으로 인증됐다는 뜻이 아닙니다. `v238`은 신규 4,633종 마스터, `v239`는 기존 보류439 정합성 점검, `v196`은 과거 256테이블 부모 물리DB입니다. **숫자가 높은 버전을 모든 종류의 타일별 최종 판정 증거로 오해하지 않습니다.**

상세 연대기: [HISTORY_INDEX.md](HISTORY_INDEX.md).
