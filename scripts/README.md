# 분석·복원 스크립트 — 최신 v240

현재 기준은 **물리 통합 10,042종, 활성 9,587종, 비활성 455종**입니다.

## 현재 사용할 명령

```bash
# 최신 전체 10,042종 물리 SQLite 복원 (표준 라이브러리만 사용)
python3 scripts/restore_v240_master.py PZ_Tile_Analysis_v240_MASTER_10042.sqlite

# PROJECT_STATE.json이 지정한 최신 버전을 자동 선택해 복원
python3 scripts/restore_latest_unified.py PZ_Tile_Analysis_latest.sqlite

# 오래된 상태 및 기본 계보 스키마도 함께 검증
python3 scripts/validate_project.py

# docs/HANDOFF.md 및 루트 README.md 자동 요약 새로 쓰기
python3 scripts/generate_handoff.py
```

복원 스크립트는 기존 파일을 덮어쓰지 않습니다. `restore_v240_master.py`는 8개의 v240 압축 부분을 연결하여 SHA-256, `PRAGMA integrity_check=ok`, 전체10,042/활성9,587/보류455 및 부모 5,409행을 검증합니다.

## 버전별 스크립트 분류

| 스크립트 | 목적 |
|---|---|
| `build_v240_physical_10042.py` | v196 원본 DB 전체를 물리 복제한 뒤 v238 신규4,633과 소스키 병합 (v240 재현) |
| `restore_v240_master.py` | **현재 권장 복원기** |
| `restore_latest_unified.py` | `PROJECT_STATE.json` 최신 버전 선택; v240일 때 위 복원기로 연결 |
| `validate_project.py` | 상태 파일의 스키마·역사적 검증 내용 확인 |
| `generate_handoff.py` | 최신 현재 상태와 긴 역사 인수인계의 자동 요약만 변경 |
| `build_unified_v49.py` ~ `build_unified_v111.py` 및 `restore_unified_v...` | **과거 실험 복원용, 현재 운영 경로 아님** |
| v117~v239 개별 타일 이미지·TMX 분석 코드 | 당시 단계별 증거 재현용, 해당 원본/좌표 규칙 확인 필수 |

스크립트 421개를 버전명만 보고 삭제하면 시각 검수 근거를 잃을 수 있어 **기존 파일명과 위치를 보존**했습니다. 새 업무는 v240 마스터와 새 버전의 체크포인트를 중심으로 수행합니다.
