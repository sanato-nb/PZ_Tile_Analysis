# 프로젝트 좀보이드 B42 타일 정체 분석

프로젝트 좀보이드(Project Zomboid) B42의 **원본 타일 이미지를 직접 관찰**하고, TMX의 원래 위치·층·레이어와 주변 타일을 비교하여 개별 타일이 어떤 사물 또는 사물의 어느 부분인지 기록하는 프로젝트입니다. 최종 목표는 Minecraft 월드 재현을 위한 검증 가능한 구조·재질 정보를 축적하는 것입니다.

## 1. 현재 작업 상태

<!-- AUTO_README_START -->
> **최신 검증 체크포인트: v163 (2026-10-28)** — 원본 이미지 관찰과 잠정 정체 후보 기록이며, 최종 정체 인증과 다릅니다.

| 최신 진행 항목 | 확인된 수치 |
|---|---:|
| 84개 TMX의 고유 타일 | **10,042종** |
| 이미지 관찰 기록 | **9,061종 (90.23%)** |
| 미관찰 타일 | **981종** |
| 이번 v163 신규 잠정 기록 | **36종** (160종 검토 중 4종 제외) |
| 물리 SQLite | **225테이블** |
| 공식 PNG↔Local ID / TileZed / 최종 정체 인증 | **0 / 0 / 0종** |

- [최신 시각 관찰 CSV](review/v163_abc_3920_3959/VISUAL_REVIEW.csv) · [이미지 증거 및 검수 결과](review/v163_abc_3920_3959/) · [최신 SQLite 매니페스트](analysis/current/v163/MANIFEST.json)
- SQLite SHA-256: `94cd995522958a09c905fdb6dfae971e2082d80ec9379010a992be7d8690bb4d`. **기존 결과·사용자 수동 80종·제외 14종·원본 PNG/TMX는 보존**하며, 보류 항목을 완료에 합산하지 않습니다.
<!-- AUTO_README_END -->

**모수 구분:** 확장 범위는 **84개 TMX에서 발견한 고유 10,042종**입니다. 기존 5,409종(관찰 기록 5,400·미관찰 9)은 결과와 원본 이미지를 재사용하며, 새 4,633종 가운데 관찰 기록 1,809·미관찰 2,824종입니다. 예전 README의 5,409종 기준 통계는 **과거 v80 당시 기록**이며 현재 진행률이 아닙니다.

**주의:** `observed`는 이미지를 실제로 본 기록, `provisional_candidate`는 정체의 잠정 추론, `held`는 보류입니다. `mapping_verified`, `tilezed_verified`, `certified`는 각각 별개이며 **현재 공식 인증은 모두 0**입니다.

## 2. 분석 절차와 증거

1. **A — 원본 이미지:** 해당 타일의 실제 PNG 픽셀과 출처·크롭 범위를 확인합니다.
2. **B — 원래 TMX 맥락:** 원래 지도의 동일 위치·층·레이어와 주변 5×5 배치를 관찰합니다.
3. **C — 원래 위치에서 제거:** B에서 해당 타일 한 배치만 제거해 픽셀 차이와 가려짐을 비교합니다.
4. **D — 같은 키의 다른 A 대입 실험:** **동일 `(tile_set_name, local_id)`에 대응하는 다른 A 이미지**를 찾아, 원래 B의 정확히 같은 TMX 위치·층·레이어에 치환하여 비교합니다. 과거의 '두 번째 TMX 사용 위치'나 **다른 Local ID일 수 있는 인접 PNG 격자**는 현재 D 완료·공식 매핑의 증거가 아닙니다.
5. **시각 판독:** 형태·부분 역할·방향·연결·재질을 실제 이미지 근거와 함께 기록하고, 모르면 보류합니다. 파일명만 보고 정체를 확정하지 않습니다.
6. **증거 및 DB 검증:** 타일별 증거·신뢰도·상태를 분리해 저장하고, 기존 SQLite·원본 데이터 무변경 여부, ZIP CRC·SHA-256·SQLite 무결성을 검사합니다.

A/B/C/D 이미지를 생성했다는 것만으로 사물 정체가 검증된 것은 아닙니다. 특히 **B−C 변화 0이나 B 가림은 투명 타일 확정의 근거가 아닙니다.** 원래 보류 D 2종과 JUMBO 20종은 사용자 지시대로 보존합니다.

## 3. 최신 결과 찾기

| 경로 | 내용 |
|---|---|
| [`PROJECT_STATE.json`](PROJECT_STATE.json) | 최신 버전과 전체 진행률의 기준 데이터 |
| [`AGENTS.md`](AGENTS.md) | 작업 중 지켜야 할 사용자 결정·인수인계 규칙 |
| [`docs/HANDOFF.md`](docs/HANDOFF.md) | 최신 작업과 과거 버전 기록 |
| [`docs/ANALYSIS_RULES.md`](docs/ANALYSIS_RULES.md) | 시각 판독·상태 분리·인증 기준 |
| [`analysis/current/`](analysis/current/) | 버전별 SQLite 복원용 압축 조각과 매니페스트 |
| [`review/`](review/) | 버전별 타일 관찰 CSV·A/B/C 증거 이미지·예외 내역 |
| [`B4220.3_MapExport_256/`](B4220.3_MapExport_256/) | 원본 TMX 지도 (변경 금지) |
| [`Tiles/`](Tiles/) | 원본 타일셋 PNG (변경 금지) |
| [`checkpoints/`](checkpoints/) | 예전 버전의 관찰 기록·증거 |

## 4. 최신 통합 SQLite 복원

저장소를 내려받은 환경에서 다음 명령으로 **`PROJECT_STATE.json`이 지정하는 최신 물리 SQLite**를 복원할 수 있습니다.

```bash
python3 scripts/restore_latest_unified.py ./pz_tiles_latest.sqlite
```

복원 도구는 해당 버전의 `MANIFEST.json`과 모든 압축 조각의 SHA-256을 검증하고 `PRAGMA integrity_check` 및 물리 테이블 수를 확인합니다. 기존 출력 파일이 있으면 **덮어쓰지 않고 중지**합니다.

**과거 복원 명령** `scripts/restore_unified_v80.py`, `scripts/restore_unified_v132.py`는 해당 시점의 역사적 DB 복원에만 사용해야 합니다.

---

## 이전 버전 보존 기록 (v59~v80)

아래의 수치·'최신' 표현은 **각 버전 작성 시점의 역사 기록**입니다. 현재 통계는 위 최신 상태 표와 `PROJECT_STATE.json`을 우선합니다.

## 5. GitHub 커밋 메시지 작성 규칙

**새로 작성하는 커밋 메시지는 한글**을 기본으로 합니다. 파일명, 버전명, Python 명령어, 실행에 필요한 기술 용어는 원래 형태를 유지합니다.

예시:

- `분석: 신규 타일 50종 이미지 검수 결과 저장`
- `데이터: v54 통합 SQLite 생성 및 무결성 검증`
- `문서: 최신 분석 진행률과 인수인계 갱신`
- `자동화: 데이터베이스 복원 검사 개선`

이전에 생성된 영어 커밋을 억지로 수정하지는 않습니다. Git 커밋의 메시지를 과거까지 바꾸려면 이력 재작성이 필요하므로, **기존 이력은 보존하고 이후 기록부터 한글을 적용합니다.**

---

**과거 증거 보존:** v58 신규 6종의 A/B/C/D 및 비교판 총 30개 JPEG는 [v58 원본 증거](checkpoints/v58_preview/)에 업로드되어 있습니다. 과거 버전의 일부 고해상도 증거는 별도 채팅 체크포인트 ZIP에 남아 있으며 GitHub에 전부 올라온 것은 아닙니다. PNG 높이 불일치 및 TileZed 정합성은 미검증입니다.

## 6. v59 신규 판독과 증거 다운로드

- **신규 직접 관찰 12종**: 후보 11종, 보류 1종, 현재 관찰 3,012/5,409종(55.69%).
- [v59 관찰 결과 CSV](checkpoints/v59/observations.csv) · [TSV](checkpoints/v59/observations.tsv) · [이미지 내장 검수 HTML](checkpoints/v59/v59_이미지내장_검수.html)
- [A/B/C/D 증거 ZIP](checkpoints/v59/v59_증거_12종_A_B_C_D.zip) · [ZIP CRC 보고서](checkpoints/v59/ZIP_CRC_REPORT.json) · [60장 이미지 원본](checkpoints/v59_preview/)
- [v59 SQLite 복원 MANIFEST](analysis/current/v59/MANIFEST.json) · [v59 통합 복원 프로그램](scripts/restore_unified_v59.py)
- 최종 인증 0종. 공식 PNG–TMX Local ID와 TileZed 정합 검증 전에는 잠정 후보를 확정으로 바꾸지 않습니다.


## 7. v60 신규 판독과 증거 다운로드

- **신규 직접 관찰 12종**: 잠정 후보 9종, 보류 3종. 누적 관찰 **3,024/5,409종(55.91%)**, 미관찰 2,385종, 잠정 후보 누적 2,621종.
- [v60 관찰 결과 CSV](checkpoints/v60/observations.csv) · [TSV](checkpoints/v60/observations.tsv) · [이미지 내장 검수 HTML](checkpoints/v60/v60_이미지내장_검수.html)
- [A/B/C/D 증거 ZIP](checkpoints/v60/v60_증거_12종_A_B_C_D.zip) · [ZIP CRC 보고서](checkpoints/v60/ZIP_CRC_REPORT.json) · [60장 원본 비교 이미지](checkpoints/v60_preview/)
- [v60 SQLite 복원 MANIFEST](analysis/current/v60/MANIFEST.json) · [v60 통합 복원 프로그램](scripts/restore_unified_v60.py)
- B-C 변화가 0인 3종은 **보류**로 유지합니다. 공식 PNG–TMX Local ID 정합과 TileZed 검증이 완료되지 않아 최종 인증은 **0종**입니다.


## 8. v61 이전 체크포인트

- v61에서 신규 12종(후보 8·보류 4)을 직접 판독하여 누적 3,036/5,409종(56.13%)을 기록했습니다.
- [v61 관찰 기록](checkpoints/v61/observations.tsv) · [v61 증거](checkpoints/v61_preview/) · [v61 통합 DB](analysis/current/v61/MANIFEST.json)

## 9. v62 과거 판독·증거·SQLite

- **신규 이미지 직접 관찰 12종**: 잠정 후보 10종, 보류 2종. 누적 **3,048/5,409종(56.35%)**, 미관찰 **2,361종**, 감사 가능한 잠정 후보 **2,639종**.
- 보류 2종은 `appliances_com_01/133`(전신주 수직선 역할 불명), `location_business_machinery_01/29`(갈색 벽판의 기능 불명)입니다.
- [v62 CSV](checkpoints/v62/observations.csv) · [TSV](checkpoints/v62/observations.tsv) · [이미지 내장 검수 HTML](checkpoints/v62/v62_이미지내장_검수.html)
- [A/B/C/D 증거 ZIP](checkpoints/v62/v62_증거_12종_A_B_C_D.zip) · [60장 JPEG](checkpoints/v62_preview/) · [ZIP CRC 검사](checkpoints/v62/ZIP_CRC_REPORT.json)
- [v62 SQLite MANIFEST](analysis/current/v62/MANIFEST.json) · [v62 복원 스크립트](scripts/restore_unified_v62.py)
- PNG–TMX Local ID 공식 매핑 및 TileZed 정합 미검증이므로 **최종 인증은 0종**입니다. 사용자 수동 검수 80종은 별도 계보를 유지합니다.


## 10. v71 과거 판독·증거·SQLite

- v71에서 신규 **20종**(후보 18·보류 2)을 관찰해 누적 **3,305종(61.10%)**, 미관찰 **2,104종**, 잠정 후보 **2,835종**을 기록했습니다.
- [v71 검수 기록](checkpoints/v71/observations.tsv) · [이미지 증거](checkpoints/v71_preview/) · [SQLite 명세](analysis/current/v71/MANIFEST.json).

## 11. v74 당시 직접 판독·증거·SQLite

- v73의 미관찰 2,064종에서 중복 없는 신규 **12종**을 선택해 A/B/C/D 비교판 12개를 실제 열어 판독했습니다. 잠정 후보 **11종**, 보류 **1종**(잔디 경계 `blends_natural_01/19`, B-C 0픽셀).
- 누적 이미지 관찰 **3,357/5,409종(62.06%)**, 미관찰 **2,052종**, 감사 가능한 잠정 후보 **2,882종**, 최종 인증 **0종**입니다.
- [v74 CSV](checkpoints/v74/observations.csv) · [TSV](checkpoints/v74/observations.tsv) · [A/B/C/D JPEG 60장](checkpoints/v74_preview/) · [이미지 내장 검수 HTML](checkpoints/v74/v74_이미지내장_검수.html) · [증거 ZIP](checkpoints/v74/v74_증거_12종_A_B_C_D.zip) · [ZIP CRC](checkpoints/v74/ZIP_CRC_REPORT.json).
- [v74 통합 SQLite MANIFEST](analysis/current/v74/MANIFEST.json) · [v74 복원 스크립트](scripts/restore_unified_v74.py). PNG–TMX Local ID 공식 대응 및 TileZed 검증은 미완료입니다.

## v80 신규 직접 판독 (2026-10-26)

- 신규 미관찰 20종을 A/B/C/D 및 비교판 100장으로 직접 검수: **후보 19종·보류 1종**. 누적 **3,461/5,409종(63.99%)**, 미관찰 1,948종, 최종 인증 0종.
- [v80 관찰 CSV](checkpoints/v80/observations.csv) · [TSV](checkpoints/v80/observations.tsv) · [독립 시각 검수 기록](checkpoints/v80/INDEPENDENT_VISUAL_AUDIT.md) · [이미지 내장 HTML](checkpoints/v80/v80_이미지내장_검수.html)
- [A/B/C/D 증거 100장](checkpoints/v80_preview/) · [증거 ZIP](checkpoints/v80/v80_증거_20종_A_B_C_D.zip) · [CRC 보고서](checkpoints/v80/ZIP_CRC_REPORT.json) · [통합 SQLite MANIFEST](analysis/current/v80/MANIFEST.json)
- 모든 신규 PNG에서 높이 불일치가 확인되어 공식 Local ID 매핑 및 TileZed 검증 전까지 최종 인증하지 않습니다.
