# 분석 데이터베이스 — 최신 v240과 과거 복원 파일

**현재 기준: [v240 물리 SQLite](current/v240/)**

| 항목 | v240 |
|---|---:|
| 전체 고유 타일 | **10,042종** |
| 기존(부모 v196) | 5,409종, 부모 256테이블 |
| 신규(v238) | 4,633종 |
| 활성 목록 | 9,587종 |
| 별도 보관 | 455종 (보류439 + 사용자미판정10 + 추가6) |
| 새 SQLite | **258테이블**, `PRAGMA integrity_check=ok` |
| 공식 정체/TileZed/PNG-ID 인증 | 0 |

전체 읽기용 CSV는 [review/v240_unified_10042_2026-10-30/](../review/v240_unified_10042_2026-10-30/)를 사용하세요.

```bash
python3 scripts/restore_v240_master.py PZ_Tile_Analysis_v240_MASTER_10042.sqlite
```

주요 SQLite 조회 대상: `v240_tile_master_10042`(전체), `v240_active_tile_master`(활성 VIEW), `v240_excluded_archive_455`(아카이브). 복원 코드는 SHA-256 및 SQLite 무결성을 확인하며 기존 파일을 덮어쓰지 않습니다.

## 옛 경로를 지우면 안 되는 이유

- `archive/v36/`, `archive/v46/`: 구형 SQLite 원본 계보.
- `imports/`: 과거 5,409 키의 병합·충돌 색인.
- `current/v49/`부터 `current/v196/`: 각 버전의 당시 SQLite 복원 파일·증거·암호학적 해시. **현재 최신 상태라는 뜻이 아님**.
- `current/v196/`: 실제 v240이 복제한 256테이블 부모 SQLite. **원본 불변**.
- `current/v240/`: 새 최신 258테이블 DB의 zlib+base64 8개 조각·MANIFEST.

**과거 v57 등 README의 '최신' 표시와 통계는 역사 기록**입니다. 현재 원본 이미지 잠정 관찰10,007/10,042(99.65%) 역시 공식 정체 인증과 구별합니다.
