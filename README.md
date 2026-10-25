# 프로젝트 좀보이드 B42 타일 정체 분석

프로젝트 좀보이드(Project Zomboid) B42의 **원본 타일 이미지를 직접 관찰하고**, TMX 지도에서 사용되는 위치와 주변 타일을 비교해 개별 타일이 나타내는 사물·부품을 분석하는 프로젝트입니다.

> **중앙 저장소 운영 원칙:** 원본 지도와 PNG는 보존하고, 분석 결과와 데이터베이스는 버전별로 관리합니다. 최신 진행률은 `PROJECT_STATE.json`에서 확인합니다.

## 1. 전체 폴더 구조

```text
📁 PZ_Tile_Analysis/
│
├── 📂 B4220.3_MapExport_256/   좀보이드 원본 지도·격자 자료
├── 📂 Tiles/                    원본 타일셋 PNG 및 관련 자료
│
├── 📂 analysis/                 분석 결과와 SQLite 데이터베이스
│   ├── archive/                 v36·v46 과거 원본 DB 보관
│   ├── imports/                 중복 제거·충돌 검토·버전별 관찰 기록
│   └── current/                 최신 통합 DB와 이전 버전
│       ├── v49/
│       ├── v50/
│       ├── v51/
│       ├── v52/
│       ├── v53/
│       ├── v54/
│       ├── v55/
│       ├── v56/
│       ├── v57/
│       ├── v58/                 이전 통합 DB 복원 자료
│       ├── v59/ ~ v61/         이전 버전별 통합 DB
│       └── v62/                 ★ 최신 통합 DB
│
├── 📂 checkpoints/              분석 배치별 진행 기록
│   ├── v48/
│   ├── v50/
│   ├── v51/
│   ├── v52/
│   ├── v53/
│   ├── v54/
│   ├── v55/
│   ├── v56/
│   ├── v57/
│   ├── v58/ ~ v61/              이전 버전별 관찰 기록
│   ├── v62/                     ★ 신규 12종 검수 및 증거 ZIP
│   └── v62_preview/             A/B/C/D JPEG 60장
│
├── 📂 scripts/                  DB 생성·복원·검증 Python 프로그램
├── 📂 .github/workflows/        GitHub Actions 자동 검증 및 인수인계
├── 📂 docs/                     목표·규칙·인수인계 관리 문서
│
├── 📄 AGENTS.md                 AI 작업 지침
├── 📄 PROJECT_STATE.json        ★ 최신 진행 현황의 기준 정보
├── 📄 README.md                 저장소 안내문 (현재 문서)
└── 📄 .gitignore                Git 추적에서 제외할 파일 규칙
```

| 분류 | 폴더 | 설명 |
|---|---|---|
| 🟠 **원본 데이터** | [원본 지도](B4220.3_MapExport_256/) | 지도·격자·TMX 관련 자료를 보존하는 장소 |
| 🟠 **원본 데이터** | [타일 이미지](Tiles/) | 타일셋 PNG 픽셀과 관련 원본을 확인하는 장소 |
| 🔵 **분석 결과** | [통합 분석 DB](analysis/) | 원본 DB, 관찰·후보·충돌 정보, SQLite 복원 자료 |
| 🔵 **작업 기록** | [체크포인트](checkpoints/) | 버전별 신규 관찰, 보류, 중복 검사 결과 |
| 🟢 **실행 코드** | [분석 프로그램](scripts/) | 데이터베이스 복원·통합·검증 코드 |
| 🟢 **자동화** | [GitHub Actions](.github/workflows/) | 무결성 검사, 데이터 복구 및 인수인계 갱신 |
| 🟣 **관리 문서** | [프로젝트 문서](docs/) | 분석 원칙, 목표, 인수인계, 과거 검수 내용 |

## 2. 최신 작업 진행도

<details>
<summary>2026년 10월 26일 · v62 검증 완료 기준</summary>

| 항목 | 수량 |
|---|---:|
| 전체 TMX 고유 타일 | **5,409종** |
| 이미지 직접 관찰 | **3,048종 (56.35%)** |
| 아직 관찰하지 않은 타일 | **2,361종** |
| 감사 가능한 잠정 정체 후보 | **2,639종** |
| 최종 정체 인증 | **0종** |

</details>

**위 표는 v62 최신 검증 기록**입니다. 이후 분석이 진행되면 [`PROJECT_STATE.json`](PROJECT_STATE.json)의 `unified_database` 및 `latest_checkpoint`를 우선합니다.

이미지로 관찰한 타일이나 잠정 정체 후보는 검증된 최종 정체와 다릅니다. PNG–TMX Local ID 대응과 TileZed 렌더 정합성은 아직 검증 대상입니다.

## 3. 타일 분석 방법

1. **A — 원본 타일:** 타일셋 PNG의 해당 타일 픽셀을 직접 확인합니다.
2. **B — 주변 조립:** TMX 같은 층의 주변 5×5 타일과 합성해 설치 맥락을 확인합니다.
3. **C — 해당 배치 제거:** 특정 타일 한 배치만 제외해 어떤 부분이 사라지는지 비교합니다.
4. **D — 다른 사용 위치:** 동일 타일이 실제 지도의 다른 장소에 나타나는 모습을 확인합니다.
5. **정체 후보 기록:** 눈에 보이는 특징과 사물·부품 역할의 추론을 분리하고, 확실하지 않으면 보류합니다.
6. **검증 및 저장:** 기존 키와 중복을 확인하고, SQLite·관찰표·체크포인트·프로젝트 상태를 갱신합니다.

## 4. 최신 데이터베이스 복원

GitHub 저장소를 로컬에 받은 뒤 다음 명령으로 **v62 전체 통합 SQLite**를 복원할 수 있습니다.

```bash
python3 scripts/restore_unified_v62.py
```

복원 후 분석 대상 전체는 `tile_catalog`, 미관찰 대상은 `analysis_queue`에서 조회합니다. 구버전과 원본 DB는 그대로 보존합니다.

자세한 작업 기록: [인수인계서](docs/HANDOFF.md) · [판독 원칙](docs/ANALYSIS_RULES.md) · [최신 체크포인트](checkpoints/v62/)

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

## 9. v62 최신 판독·증거·SQLite

- **신규 이미지 직접 관찰 12종**: 잠정 후보 10종, 보류 2종. 누적 **3,048/5,409종(56.35%)**, 미관찰 **2,361종**, 감사 가능한 잠정 후보 **2,639종**.
- 보류 2종은 `appliances_com_01/133`(전신주 수직선 역할 불명), `location_business_machinery_01/29`(갈색 벽판의 기능 불명)입니다.
- [v62 CSV](checkpoints/v62/observations.csv) · [TSV](checkpoints/v62/observations.tsv) · [이미지 내장 검수 HTML](checkpoints/v62/v62_이미지내장_검수.html)
- [A/B/C/D 증거 ZIP](checkpoints/v62/v62_증거_12종_A_B_C_D.zip) · [60장 JPEG](checkpoints/v62_preview/) · [ZIP CRC 검사](checkpoints/v62/ZIP_CRC_REPORT.json)
- [v62 SQLite MANIFEST](analysis/current/v62/MANIFEST.json) · [v62 복원 스크립트](scripts/restore_unified_v62.py)
- PNG–TMX Local ID 공식 매핑 및 TileZed 정합 미검증이므로 **최종 인증은 0종**입니다. 사용자 수동 검수 80종은 별도 계보를 유지합니다.
