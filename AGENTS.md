# 좀보이드 B42 타일 정체 분석 — 중앙 AI 작업 지침 (v97)

## 목표 및 최신 검증 기준
- B42 TMX 두 개(저장소 파일 `B4220.3_MapExport_256/tmx/31_45.tmx`, `31_46.tmx`)에서 사용한 고유 **5,409종**, 기준 배치 **302,177건**을 원본 PNG와 실제 배치로 이해한다. 최초 이름 `31_45(2).tmx` / `31_46(2).tmx`과 저장소 이름의 동일성은 공식 인증 전까지 별개로 취급한다.
- 모든 작업은 `PROJECT_STATE.json`의 `unified_database` 및 `latest_checkpoint`를 우선한다. `reconciliation`의 2,584(v47)는 과거 교집합 대조 기준이다.
- 2026-10-26 최신 **v97: 4,566/5,409종(84.4149%); 미관찰 843종; 감사 가능한 잠정 후보 3,841종; 최종 인증 0종**.
- 최신 물리 통합 SQLite: `analysis/current/v97/`. 복원: `python3 scripts/restore_unified_v97.py /tmp/pz_latest.sqlite`. 압축 7조각의 SHA-256·SQLite 무결성·누적 수량 검증을 거친다.
- `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 먼저 읽는다.

## 실제 이미지 시각 분석 규칙
1. 최신 DB `analysis_queue`에서 미관찰 키 `(tile_set_locator,local_id)`를 선택하고, 이전 관찰과 겹치는 키는 신규로 계상하지 않는다.
2. A 원본 PNG 타일 크롭, B TMX 동일 층 주변 5×5 근사 아이소메트릭, C 동일 레이어 대상 배치 **하나만** 제거, D 다른 실제 TMX 사용 위치를 생성하고 **직접 이미지를 관찰**한다.
3. `observed_features`, `identity_candidate`, `part_role`, `confidence`, `review_status`를 분리한다. 타일셋명 또는 과거 v31 AI 분류만으로 정체를 판단하지 않는다.
4. TMX 좌표·층·레이어·raw GID·원본 PNG/TMX SHA-256·B-C 픽셀 변화·주변 누락·`height_mismatch`를 증거에 남긴다. 불충분한 정체는 `held`로 처리한다.
5. 이미지 관찰 `observed`, 잠정 `candidate`, 공식 Local ID 매핑 검증 `mapping_verified`, TileZed 정합, 최종 `certified`를 혼동하지 않는다. 공식 PNG–TMX 매핑 및 TileZed 미검증 상태에서 인증 0.
6. 이전에 폐기된 TMX→2D 평면도 엔진을 재사용하지 않는다.

## 보존·계보
- v36 원본 전체 SQLite, v46 원본 `v46__` 테이블, v47 병합 `v47__` 및 v48~v87의 누적 테이블을 유지한다.
- v36 과거 보고 후보 2,291종과 감사 가능한 2,156종의 차이 135종, v36/v46 후보 단어 충돌 256종을 자동 재분류하지 않는다.
- 사용자 수동 검수 80종과 재검수 의견은 별도 계보이며 누적 관찰에 자동 합산하지 않는다.
- `analysis/archive/`, `analysis/current/v49/`~`v66/`, `checkpoints/v36/`~`v66/`, `Tiles/`, `B4220.3_MapExport_256/`는 삭제·덮어쓰기 금지.

## v97 신규 120종 A/B/C/D 시각 판독 (2026-10-26)
- v96 통합 SQLite의 미관찰 대기열 **963종**에서 기존 관찰과 겹치지 않는 **120종**(118개 타일셋)을 선정했다. 원본 PNG A, TMX 실제 같은 층 주변 5×5 B, 동일 레이어 대상 한 배치 제거 C, 다른 실제 위치가 있으면 D 아니면 미확보 D 안내판을 생성했다. 개별 증거와 판독 보드 **600 JPEG**, 6개 타일씩 합친 **20개 접촉시트 모두 직접 열어 시각 판독**, `checkpoints/v97/review_notes_*.psv` 8개와 `observations.tsv`로 기록.
- 실제 다른 사용 위치 D **15종 모두 근접 비독립**, 다른 위치 없는 **105종**은 D 안내 화면. 독립된 원거리 D는 **0종**. A 외형과 B/C 제거 비교가 충분하지 않으면 보류했다.
- 신규 이미지 관찰 **120종**, 잠정 후보 **104종**(신뢰도 전부 low), 보류 **16종**, 중복 **0종**. 누적 **4,566/5,409종(84.4149%)**, 미관찰 **843종**, 감사 가능한 잠정 후보 **3,841종**, 최종 인증 **0종**.
- `analysis/current/v97/MANIFEST.json`에서 물리 SQLite **87,322,624바이트** SHA-256 `1e9976cf3df2c89f79a07e138628c3d2e0f526b6e675e01d393c2c8aa53fde64`와 7개 복구 조각의 SHA를 보존. v96 원본 확인 후 복제해 이전 v36~v96 전체 DB 테이블 및 사용자 수동 검수 80종의 별도 계보를 유지. DB integrity_check, 중복, SQL 총수, 원본 PNG/TMX SHA, TMX 좌표와 GID, JPEG 로딩, DB 압축 복원 모두 통과.
- `checkpoints/v97/`에 관찰 CSV/TSV, 300장씩 이미지 내장 HTML 2개 및 증거 ZIP 2개(각 314항목, **ZIP CRC PASS**) 보존. `checkpoints/v97_preview/` 원본 JPEG 600장·접촉시트 20장·증거 매니페스트 보존.
- 공식 PNG–TMX Local ID 정합 및 TileZed 미검증이므로 신규 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0` 유지. 다음은 v97 통합 SQLite 대기열 **843종**에서 재개.

## v96 신규 120종 A/B/C 직접 시각 분석 (2026-10-26)
- v95 물리 통합 SQLite의 미관찰 1,083종에서 고유 **120종** 선정. 서로 다른 120개 타일셋에 대해 원본 PNG A·TMX 같은 층 주변 5×5 B·선택 레이어 하나 제거 C·D 실제 근접 사용 좌표 또는 미확보 안내·ABCD 합본 **총 600 JPEG** 생성. 6종씩 묶인 20개 접촉 시각검수판을 전부 직접 열어 관찰하고 개별 시각 관찰 notes 9개 파일에 기록.
- **TMX 실제 근접 D 14종**(거리 5칸 미만·독립 현장 아님), **별도 배치 없는 타일 106종**(D 안내판). 독립 원거리 D 검증은 0종이며 공식 Local ID·TileZed 미검증이다.
- 신규 고유 이미지 관찰 **120종**, 잠정 후보 **99종(전부 confidence low)**, 보류 **21종**, 중복 0. 누적 이미지 관찰 **4,446/5,409종(82.1963%)**, 미관찰 **963종**, 잠정 후보 **3,737종**, 최종 인증 0종.
- `checkpoints/v96/observations.tsv`·CSV, `review_notes_*.psv`, `checkpoints/v96_preview/`의 600 JPEG·20개 접촉판, 300장씩 내장 HTML 2개 및 증거 ZIP 2개(각 314개 항목, CRC PASS)를 보관. 원본 PNG/TMX SHA·사용 좌표/GID·B-C 픽셀 차·D 사실 상태 검사 통과.
- `analysis/current/v96/MANIFEST.json` 물리 SQLite **87,076,864바이트**, SHA-256 `3c37fc2aec482f47c2852c1237a5daff1cc8434e0b301c658f988e5bc3ff6f9b`. v95 원본 DB SHA 인증 뒤 v36~v95 모든 테이블 보존·중복 검사·SQLite integrity_check·7개 압축 조각 SHA 왕복 검증 성공.
- v36~v95 원본·사용자 수동 검수 80종 별도 계보는 수정/삭제하지 않음. 새로운 인증 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.
- 후속 분석은 v96 통합 DB `analysis_queue`의 미관찰 **963종**을 이용할 것.

## v95 신규 실제 A/B/C/D 시각 판독 (2026-10-26)
- 최신 v94 물리 통합 SQLite SHA-256 `4bad407adf9803256d9f39cf691824fe5c2c98a39b9c9a20367c81e9dd5cf679` 복원 후 `analysis_queue`의 미관찰 1,095종에서 고유 12종 선정. 원본 PNG A, 동일 층 5×5 TMX 조립 B, 선택 배치 하나 제거 C, **다른 실제 TMX 좌표 D** 및 비교판 **60 JPEG** 생성·직접 이미지 판독.
- D 12종 모두 동일 TMX의 **맨해튼 거리 1~3칸** 다른 위치. 독립된 원거리 현장이 아니므로 신뢰도 최대 low, 최종 인증 0. D는 안내판이 아니라 실제 다른 배치지만 독립성 부족을 명시한다.
- 신규 잠정 후보 **7종**, 정체 보류 **5종**(B-C 0·0·0·28·221픽셀). 모든 후보는 원본 외형·B/C 제거·D 근접 맥락을 대조한 잠정 판정. 신규 중복 0.
- 누적 관찰 **4,326/5,409종(79.9778%)**, 미관찰 **1,083종**, 감사 가능한 잠정 후보 **3,638종**, 최종 인증 **0종**.
- 증거: `checkpoints/v95/observations.tsv`·CSV·`INDEPENDENT_VISUAL_AUDIT.md`, `checkpoints/v95_preview/`의 60 JPEG·2 접촉판, 이미지 내장 HTML·증거 ZIP CRC 검사. `analysis/current/v95/MANIFEST.json`에 물리 SQLite SHA-256 `8f485d2993ef262a4f4243f4af72ad5a5c50f6f2a530c6f0d1cbbc0938e04081`과 7개 분할 복원 명세 보존.
- v36~v94 원본 DB·체크포인트 및 사용자 수동 검수 80종·재검수 계보 변경 없음. PNG 물리 높이 불일치, 공식 Local ID 및 TileZed 정합 미검증이므로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.
- 후속: v95 미관찰 1,083종에서 A/B/C/D 실사용 검증 가능한 신규 키를 찾고, v94에서 독립 D 미확보된 120종과 v95 근접 D 12종은 별도 독립 위치를 재검증한다.

## v94 신규 A/B/C 판독 및 독립 D 미확보 (2026-10-26)
- v93 통합 DB의 **미관찰 1,215종**을 원본 TMX에서 재확인. 총 **1,016종은 TMX 배치 단 1건, 199종은 복수 배치**가 있었다. 기존 선택기는 복수 배치 + 거리가 충분히 떨어진 D를 강제해 0종 선택했던 문제를 수정했다. 원본 PNG 크롭 가능성을 검사해 120종 신규 선정했다.
- 신규 타일 **120종(각각 서로 다른 타일셋)**의 원본 PNG A, 동일 층 5×5 TMX B, 선택된 레이어 위치 한 곳만 제거한 C, D 정보판 및 ABCD 비교판 **600 JPEG**를 생성했다. **6종씩 묶은 20개 접촉 검수판 모두 직접 열어 이미지 판독**, `checkpoints/v94/review_notes_*.psv`에 각 타일 형태·후보·보류·신뢰도 기록.
- 이번 120종 중 정확히 **103종은 TMX에서 단일 배치**, **17종은 복수 배치지만 독립적 거리(맨해튼 5칸 이상 또는 다른 TMX)로 떨어진 별도 현장이 없음**. 이 경우 D 이미지는 *다른 배치 증거가 아니라 명시적인 미확보 안내*다. 차선책으로 다른 타일을 가져오거나 위치를 조작하지 않았다.
- 신규 잠정 후보 **98종**(전부 confidence 최대 low), 보류 **22종**. D 확보가 없어 공식 Local ID·TileZed 정합 미검증 상태에서 최종 인증 0종.
- 누적 이미지 관찰 **4,314/5,409종(79.7560%)**, 남은 미관찰 **1,095종**, 잠정 후보 **3,631종**, 신규 중복 **0**.
- `analysis/current/v94/MANIFEST.json`에 v93 SHA 검증 후 DB 복제·새 테이블 추가, 7개 조각 분할·압축 왕복 SHA-256, `PRAGMA integrity_check` 및 기존 v36~v93 테이블 보존 기록. 원본 PNG·TMX SHA, 동일 원본 위치·GID, B–C 차이, JPEG 로딩, ZIP CRC 검사.
- `checkpoints/v94/observations.tsv` / CSV, 이미지 300장씩 내장 HTML 2개, JPEG 증거 ZIP 2개, 20개 합본 검수판 보존. 원본 `Tiles/` 및 `B4220.3_MapExport_256/`, 사용자 수동 검수 80종 계보 불변.
- 후속: v94 통합 DB의 **미관찰 1,095종**으로 이동. PNG 아틀라스 높이 불일치·Local ID 범위 문제를 해결하기 전에는 공식 인증을 금지한다.

## v92 신규 12종 실제 A/B/C/D 판독 통합 (2026-10-26)
- v91 통합 SQLite 미관찰 **1,232종**에서 신규 고유 키 12종을 선정했다. GitHub 원본 PNG·TMX로 A 원본, B 동일 층 5×5, C 단일 배치 제거, D 다른 실제 사용 위치 및 비교판 **60 JPEG**를 생성하고, 접촉판 2개와 개별 ABCD 12개를 직접 열어 판독했다.
- **잠정 후보 9종·보류 3종**. 벽 패널·실내 직각 코너·창/문 개구부·벽돌 외벽 코너·난간 상단 가로 장식 등을 잠정 기록. 보류 `walls_detailing_01/22`(정확한 역할 불명), `street_curbs_01/62`(B-C 154px·주변 누락 1), `walls_detailing_01/55`(B-C 89px). 타일셋 이름만으로 정체를 확정하지 않았다.
- 누적 **4,189/5,409종(77.4450%)**, 미관찰 **1,220종**, 감사 가능한 잠정 후보 **3,530종**, 최종 인증 **0종**. 신규 키 중복 0.
- `checkpoints/v92/observations.tsv`, CSV, `INDEPENDENT_VISUAL_AUDIT.md`, `checkpoints/v92_preview/`의 60 JPEG, 이미지 내장 HTML 60장, ZIP **67항목 CRC PASS**를 보존한다.
- `analysis/current/v92/MANIFEST.json`: 물리 SQLite **86,433,792바이트**, SHA-256 `1ba2d19fc7765c6d2e4f59035cfd3780f12a320730eb46be1cbfd884c54f591e`. v91 복원 SHA 확인, 이전 테이블 보존, SQLite `integrity_check`, 원본 PNG/TMX SHA, B-C, 이미지 로딩, 압축 7조각 SHA 왕복 검증 성공.
- PNG 물리 높이 불일치, 공식 PNG–TMX Local ID 및 TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v91 원본과 사용자 수동 검수 80종 계보를 변경하지 않는다.
- 다음 작업: v92 미관찰 대기열 **1,220종**에서 신규 고유 키를 선정하고, 기존 보류 타일은 다른 위치로 재검수한다.

## v93 신규 5종 A/B/C/D 직접 판독 (2026-10-26)
- v92 최신 통합 DB 미관찰 1,220종 중 **다른 실제 TMX 사용 위치 D가 확인되는 고유 키 5종**을 선택해 A 원본 PNG, B 동일 층 주변 5×5, C 대상 배치 하나 제거, D 다른 사용 위치를 생성하고 비교판 5개를 직접 열어 판독했다.
- `walls_detailing_01` Local ID **66·82·89** 잠정 후보, **90·91** 보류. 신규 후보 3종·보류 2종·중복 0종. PNG 높이 불일치, TileZed·공식 Local ID 미검증으로 최종 인증 0종.
- 누적 관찰 **4,194/5,409종(77.5374%)**, 미관찰 **1,215종**, 감사 가능한 후보 **3,533종**.
- `checkpoints/v93/observations.tsv`·CSV·독립 시각 검수 기록·`checkpoints/v93_preview/`의 A/B/C/D+비교판 **25 JPEG**, 이미지 내장 HTML(25장), 증거 ZIP(31항목 CRC PASS)을 보존한다.
- `analysis/current/v93/MANIFEST.json` 물리 SQLite **86,454,272바이트**, SHA-256 `b83266fd8fc626a56410458409a3259c2696467cda4cc7efff671113bd6a06af`. GitHub Actions에서 원본 v92 SHA, PNG/TMX 원본 해시, 이미지 로딩, B-C 변화, 중복 키, SQLite 무결성, 압축 7조각 왕복 및 ZIP CRC 검증 통과.
- v36~v92 원본·체크포인트 및 사용자 수동 검수 80종 계보는 변경하지 않는다. 다음은 v93 대기열 1,215종 중 새로운 실사용 증거가 충분한 키를 선정한다.

## v91 132종 시각 판독 통합 (2026-10-26)
- v90 미관찰 1,364종에서 기존 별도 독립 판독 12종(과거 미계상)을 보존하고, 겹치지 않게 새로 선정한 **120종**을 추가 A 원본 PNG, B TMX 동일 층 5×5 근사 조립, C 해당 단일 배치 제거, D 다른 실사용 위치로 재구성했다.
- 신규 120종은 20개의 6종 묶음 접촉 검수판을 모두 직접 열어 관찰하고 `checkpoints/v91/review_notes_extra_*.psv`에 개별 형태·역할·잠정 정체·보류 원인을 기록했다. 기존 12종은 `checkpoints/v91/observations.tsv` 및 `v91_preview/` 기록을 불변 보존한다.
- `checkpoints/v91/observations_combined.tsv`에 합본 **132종(신규 잠정 후보 102·보류 30)** 반영. 앞선 v90 타일과 중복 0, 기존 12와 신규 120 사이 중복 0.
- 누적 **4,177/5,409종(77.2231%)**, 미관찰 **1,232종**, 감사 가능한 후보 **3,521종**, 최종 인증 **0**.
- `analysis/current/v91/MANIFEST.json`의 물리 DB **86,405,120바이트**, SHA-256 `ae36baf4e632ccecd7f80249813a12fc3da90a967699bed3e8ede67fd1170ecf`. v90 원본 복원 SHA 확인 → SQLite 복사·기존 테이블 보존 → v91 132종 추가 → SQLite 무결성 → 압축 7조각 왕복 SHA 대조 모두 통과.
- 총 660 JPEG, 22개 접촉 검수판, CSV, 이미지 330개씩 내장 HTML **2개**, 각 346항목 증거 ZIP **2개 CRC PASS**. 원본 PNG/TMX SHA-256, GID·좌표, 독립 132 키 및 B-C 픽셀 변화 검사 통과.
- 원본 PNG 높이·공식 Local ID/TileZed 검증 미완료 상태: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. 과거 v36~v90 데이터 및 사용자 수동 검수 80종 원래 계보 유지.
- 다음 작업: 최신 v91 분석 대기열 **1,232종**에서 고유 미관찰 선택 및 보류 재검토.

## v90 신규 실제 타일 판독 (2026-10-26)
- v89 통합 SQLite 미관찰 1,604종에서 중복 없는 **240종** 선정. 총 26개 타일셋에 분산해 원본 PNG·TMX로 A 원본, B 동일 층 5×5 근사 조립, C 같은 레이어 타일 하나 제거, D 다른 실사용 좌표 및 ABCD 비교판 **1,200개 JPEG**를 생성했다.
- 6종씩 조합한 40개 실제 접촉 검수판(`checkpoints/v90_preview/review_sheets/sheet_000.jpg`~`sheet_039.jpg`)을 **모두 직접 열어 관찰**하고, 240종 각각의 원본 외형·정체 후보·부품 역할·보류·TMX 좌표·GID·PNG/TMX 해시 기록을 `checkpoints/v90/review_notes_*.psv` 및 `observations.tsv`로 보존했다.
- 신규 **잠정 정체 후보 191종, 보류 49종**. B-C 가시변화가 500픽셀 미만이거나 사물/배치가 애매한 타일은 보류. 사용한 B/C/D는 TileZed 공식 렌더가 아닌 근사 판이므로 최종 인증 금지.
- 누적 관찰 **4,045/5,409종(74.7828%)**, 남은 미관찰 **1,364종**, 감사 가능한 잠정 후보 **3,419종**, 인증 **0종**, 신규 중복 **0종**.
- SQLite `analysis/current/v90/MANIFEST.json` 86,147,072바이트 SHA-256 `59ca4987eb72a8b771c4d3122edb4f0253c267889ba0ff0343f26283f87ffc9f`. 이전 v89 DB SHA 대조 후 복사, v36~v89 기존 전체 테이블·수동 검수 80종 계보 불변 보존, PRAGMA integrity_check OK, 7압축조각 왕복 SHA 검증.
- `checkpoints/v90/` CSV 및 이미지 내장 HTML **2개(총 1,200 JPEG 내장)**, 증거 ZIP **2개(각 624항목, CRC PASS)**, 40개 합본 JPEG 및 원본 개별 JPEG 모두 GitHub에 보관한다. SHA·PNG 검증·이미지 로딩·중복과 현장 매핑 이력 검증 성공.
- 모든 신규 타일은 공식 Local ID와 TileZed 검증 미완료: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.
- 다음 작업: v90 분석 대기열 1,364종과 이전 보류 타일들을 다른 실사용 좌표와 고해상도 정합을 활용해 분석한다.

## v89 신규 타일 직접 이미지 판독 (2026-10-26)
- v88 통합 SQLite `analysis_queue` 미관찰 1,724종에서 중복 없이 120종을 선택했다. 40개 타일셋의 실제 사용 위치를 확인했고, 원본 PNG A·TMX 같은 층 5×5 조립 B·해당 레이어 대상 1건 제거 C·다른 실제 위치 D 및 비교판 총 600 JPEG를 만들었다.
- 6종씩 조립된 `checkpoints/v89_preview/review_sheets/sheet_000.jpg`~`sheet_019.jpg` 20장을 실제 열어 A/B/C/D 시각 검토했다. 개별 120종의 원본 A/B/C/D·비교판 600장을 원형 보존한다. 텍스트 이름만으로 정체를 확정하지 않았다.
- 신규 판독 잠정 후보 98종, 보류 22종(B-C 변화 없거나 작거나 가림 등). 외벽·개구부·타일·문틀·지붕 마감·실내외 조명·정지 표지·이동식 녹색 쓰레기통·오염 등 개별 후보에 관찰 특징, 부품 역할, 신뢰도·보류 이유 분리 기록.
- 누적 이미지 관찰 **3,805/5,409종(70.3457%)**, 미관찰 **1,604종**, 감사 가능한 잠정 후보 **3,228종**, 최종 인증 **0종**, 신규 중복 **0종**.
- `checkpoints/v89/observations.tsv` 및 CSV, `checkpoints/v89_preview/` 600 JPEG·20 합본, 이미지 600개 내장 HTML, ZIP **604항목·CRC PASS**. 원본 PNG/TMX SHA-256 검증, A/B/C/D JPEG 로딩 및 B-C 근거 검사 통과.
- `analysis/current/v89/MANIFEST.json` 기준 물리 SQLite **85,663,744바이트**, SHA-256 `350fa5ad3b3569de7152db0cf8359114045fbad7b196c9f0ef8a24e38a14cc3d`, 7개 압축 조각 왕복 SHA-256·SQLite 무결성·이전 테이블 불변·중복 검증 통과.
- 기존 v36~v88 DB/검수 이력·사용자 수동 검수 80종 및 원본 PNG/TMX는 삭제하거나 덮어쓰지 않았다. 신규 타일 모두 PNG 높이 불일치 및 TileZed 공식 정합 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.
- 다음 작업: v89 `analysis_queue`의 미관찰 1,604종에서 계속.

## v88 신규 실제 이미지 판독 (2026-10-26)
- v87 통합 SQLite 미관찰 **1,748종**에서 중복 없는 신규 **24종**을 선택했다. A=원본 PNG, B=TMX 동일 층 5×5 조립, C=대상 단일 배치 제거, D=다른 실제 TMX 위치, ABCD 비교판 **120 JPEG**를 만들고 모든 **24개 비교판을 직접 열어 판독**했다.
- 신규 잠정 후보 **12종**, 보류 **12종**. 원본에서 짙은 갈색 낮은 탁자, 연보라색 매트, 검정/회색 테두리 러그, 황토색 원형 무늬 러그 조각을 시각 확인했고, B-C 픽셀 차이 0~38 또는 주변 가림의 경우 보류했다.
- 누적 **3,685/5,409종(68.1272%)**, 미관찰 **1,724종**, 감사 가능한 후보 **3,130종**, 최종 인증 **0종**, 중복 키 0.
- `checkpoints/v88/observations.tsv` 및 CSV, `checkpoints/v88_preview/` A/B/C/D+비교판 120 JPEG, 이미지 내장 HTML, 증거 ZIP **124항목 CRC PASS**.
- `analysis/current/v88/MANIFEST.json` 기준 SQLite **85,422,080바이트**, SHA-256 `22c162c96bfa3a7c0883a80b02b0e159b421e7ffde2437cb5dffdf08f8b4ae24`; v87 압축 복원 및 SHA 원본 대조, 신규 키 중복·PNG/TMX 해시·B-C 변화·기존 테이블 불변 보존·DB 무결성·압축 왕복 검증 통과.
- 공식 PNG–TMX Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v87 기록과 사용자 수동 검수 80종 보존.
- 다음 작업: v88 미관찰 **1,724종**을 검수. 보류 타일은 다른 사용 위치 또는 높이 정합을 개선하여 재검수.

## v87 신규 실제 이미지 판독 (2026-10-26)
- v86 최신 통합 SQLite `analysis_queue` 미관찰 1,760종에서 중복 없는 신규 **12종**을 선정했다. 원본 PNG A, 같은 층 TMX 5×5 B, 대상 단일 배치 제거 C, 다른 실제 위치 D, 비교판 **60 JPEG**를 GitHub 원본으로 생성하고 **12개 비교판을 직접 열어 시각 판독**했다.
- 신규 **잠정 후보 7종, 보류 5종**. 갈색 낮은 목제 탁자 조각 1종, 청회색 녹회색 테두리 실내 깔개 조각 3종, 자주회색 테두리 실내 깔개 조각 3종을 잠정 후보로 기록했다. 보류: `floors_rugs_01/7`(4px), `/8`(350px, 가림), `/9`(0px), `/12`(2px), `/50`(0px).
- 누적 **3,661/5,409종(67.6835%)**, 미관찰 **1,748종**, 감사 가능한 누적 잠정 후보 **3,118종**, 최종 인증 **0종**, 신규 중복 0.
- `checkpoints/v87/observations.tsv`·CSV·`INDEPENDENT_VISUAL_AUDIT.md`, `checkpoints/v87_preview/`의 A/B/C/D 및 비교판 60 JPEG, 이미지 내장 HTML 60장, ZIP 64항목 CRC PASS를 보존한다.
- `analysis/current/v87/MANIFEST.json`: 물리 SQLite **85,372,928바이트**, SHA-256 `82a525e299a3330e17e16eebc9eb7267cea7d27a46315a3b9f12ef0c6e8f1c38`. GitHub Actions에서 원본 PNG/TMX SHA, 이미지 로딩, B-C, 압축 7조각 왕복, SQLite `integrity_check`, 이전 테이블 보존, 중복 검증 통과.
- 신규 12종 모두 PNG 물리 높이 불일치, 공식 PNG–TMX Local ID 및 TileZed 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v86 원본 DB·체크포인트·원본 PNG/TMX와 사용자 수동 검수 80종은 변경하지 않는다.
- 다음 작업: v87 `analysis_queue` 미관찰 **1,748종**을 기준으로 신규 검수한다.

## v86 신규 실제 이미지 판독 (2026-10-26)
- v85 최신 통합 SQLite의 `analysis_queue` 미관찰 1,772종에서 고유 12종을 선정했다. 원본 PNG A, 같은 층 TMX 5×5 B, 단일 배치 제거 C, 다른 사용 위치 D 및 비교판 60 JPEG를 실제 생성하고 **12개 비교판을 직접 열어 판독**했다.
- 신규 잠정 후보 7종, 보류 5종(`floors_interior_tilesandwood_01/44` 4px, `/47` 2px, `/49` 0px, `floors_rugs_01/1` 0px, `/3` 0px). 갈색 낮은 목재 탁자, 주방 체크·격자 바닥, 청록색 테두리 러그의 분할 부품을 잠정 후보로 기록했다.
- 누적 **3,649/5,409종(67.4616%)**, 미관찰 **1,760종**, 감사 가능한 잠정 후보 **3,111종**, 최종 인증 **0종**. 기존 관찰 중복 0.
- `checkpoints/v86/observations.tsv`·CSV·`INDEPENDENT_VISUAL_AUDIT.md`, `checkpoints/v86_preview/` A/B/C/D+비교판 60 JPEG, 이미지 내장 HTML 60장, ZIP 64항목 CRC PASS.
- `analysis/current/v86/MANIFEST.json`: SQLite SHA-256 `2e78637cf37a68e3ac7295d425b04ac32fbdef23cadd52a99f13d76fa4180c91`; v85 원본 SHA·압축 왕복·SQLite 무결성·원본 PNG/TMX SHA·JPEG 로딩·중복 검사 통과.
- PNG 물리 높이 불일치 및 공식 Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v85 모든 원본 DB·체크포인트·사용자 수동 검수 80종은 변경하지 않는다.
- 다음 작업: v86 `analysis_queue` 미관찰 1,760종에서 중복 없는 신규 키를 선별한다.

## v85 신규 실제 이미지 판독 (2026-10-26)
- 최신 v84 `analysis_queue` 미관찰 1,820종에서 중복 없는 48종을 선택해 원본 PNG A, TMX 같은 층 5×5 B, 단일 배치 제거 C, 다른 실제 위치 D 및 비교판 총 240 JPEG를 직접 열어 판독했다.
- 잠정 후보 33종, 보류 15종. 누적 관찰 3,637/5,409(67.2398%), 미관찰 1,772종, 감사 가능한 누적 후보 3,104종, 최종 인증 0종.
- `checkpoints/v85/observations.tsv`·CSV·`INDEPENDENT_VISUAL_AUDIT.md`에 관찰 특징/잠정 정체/부품 역할/신뢰도/보류 사유와 원본 PNG·TMX 해시 및 위치를 분리 보존한다.
- `checkpoints/v85_preview/`에 A/B/C/D 비교판 240 JPEG, `checkpoints/v85/v85_이미지내장_검수.html`에 이미지 240개 데이터 URI 내장, `v85_증거_48종_A_B_C_D.zip` 244항목 CRC PASS.
- `analysis/current/v85/MANIFEST.json` 기준 SQLite SHA-256 `1428e58501c73eb2aae65897d69b2eeb0dfd57ebb67b90817acd5cbda4849998`. 원본 v36~v84 DB·체크포인트·사용자 검수 80종은 보존한다.
- 공식 PNG–TMX Local ID 및 TileZed 검증은 0으로 유지하며, B-C 변화가 없거나 극소인 타일은 보류한다.

## v68 신규 실제 이미지 판독 (2026-10-26)
- v67 통합 SQLite의 미관찰 대기열 2,234종에서 중복 없는 **신규 80종**을 선정하고 실제 원본 PNG와 TMX의 A/B/C/D 이미지 + 비교판 **400장**을 직접 판독했다.
- 잠정 후보 **56종**, 보류 **24종**, 누적 이미지 관찰 **3,255/5,409(60.1775%)**, 미관찰 **2,154종**, 감사 가능한 누적 후보 **2,793종**, 최종 인증 **0종**.
- `checkpoints/v68/observations.tsv`, CSV: 좌표·레이어·raw GID·원본 PNG/TMX SHA-256·원본 관찰·정체 가설·다중 타일 부품 역할·신뢰도·B-C 변화·가림 보류를 각각 기록. B-C 변화 0인 12종 모두 보류.
- `checkpoints/v68_preview/`에 A/B/C/D 및 비교판 400 JPEG 실물 증거 보존, `checkpoints/v68/v68_이미지내장_검수.html`에 이미지 400장 데이터 URI 내장, 증거 ZIP **404개 항목 CRC PASS**.
- 잠정 후보에는 산업 주방 카운터와 냉장고·토스터·커피머신, 가구점 소파·의자, 의료 작업대·실내 벽, 산업용 사각 환기 덕트·전기 계량함·전선 연결부 등이 있다.
- `analysis/current/v68/MANIFEST.json`: 물리 SQLite **84,484,096바이트**, SHA-256 **478304acfde12f53a0c03fc5bdb9264a6da9bb3b3e4c796244d06f15b8543fd8**. SQLite integrity_check·이전 테이블 보존·신규 키 중복·증거 SHA·JPEG 로딩 검증.
- 공식 Local ID 높이 대응과 TileZed 정합 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`; 과거 v36~v67 및 사용자 직접 검수 80종은 변경 없음.

## v69 신규 직접 이미지 판독 (2026-10-26)
- v68 통합 SQLite 미관찰 대기열 **2,154종**에서 고유 키 중복 없는 **15종**을 선별했다. 원본 PNG·TMX에서 A(원본), B(같은 층 5×5), C(단일 배치 제거), D(다른 위치), 비교판을 생성한 뒤 **15종의 비교판을 직접 열어 시각 검수**했다.
- 이번 신규 잠정 후보 **11종**, 보류 **4종**. 누적 관찰 **3,270/5,409(60.4548%)**, 미관찰 **2,139종**, 누적 감사 가능한 후보 **2,804종**, 최종 인증 **0종**.
- 잠정 후보에는 짙은 갈색 수납 하부장, 녹색 주방 카운터 코너·양문 수납장, 검은 퀼팅 안락의자, 크림색 2단 냉장고의 방향별 타일, 갈색 분기·병렬 배관, 벽 부착 전기 접속함과 케이블 분기부가 포함된다.
- 보류 4종: `furniture_seating_indoor_03/61`(B-C 0), `/103`(16), `appliances_refrigeration_01/27`(1511이나 정체 불명), `location_services_beauty_01/10`(4). A에서 보이는 모양과 실제 배치의 기여를 구분해 기록한다.
- 증거: `checkpoints/v69_preview/`의 A/B/C/D+비교판 **75 JPEG**, `checkpoints/v69/observations.tsv`, CSV, 이미지 내장 HTML, 증거 ZIP 79항목 CRC PASS. 각 키에 TMX 좌표·층·레이어·raw GID·원본 해시·B-C 변화 기록.
- 물리 SQLite `analysis/current/v69/MANIFEST.json`: **84,516,864바이트**, SHA-256 `bffc80c2358767efed77e486d7c796d229db5c231dab2d4b362c78ccd1eac053`. SHA 왕복·SQLite integrity_check·누적 수량·기존 테이블 보존·신규 키 중복·PNG/TMX SHA·JPEG 검증 완료.
- 공식 PNG–TMX Local ID 높이 정합과 TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v68 이하 및 수동 검수 80종은 별도 보존.

## v70 신규 직접 이미지 판독 (2026-10-26)
- v69 `analysis_queue`의 미관찰 **2,139종**에서 신규 키 **15종**을 선택하고, GitHub 원본 PNG·TMX로 A/B/C/D 및 비교판 **75장**을 생성해 실제 비교판 15개를 직접 시각 검수했다.
- 잠정 후보 **13종**, 보류 **2종**(`furniture_seating_indoor_03/134`, `/135`; 두 항목 모두 B-C 픽셀 변화 0). 신규 키 중복 0종.
- 주요 잠정 후보: 아이보리색 판매대 코너·카운터 연결부, 목재 야외 벤치, 냉장기기 후면·빨간 2도어 냉장고·상부 개폐형 냉동고, 갈색 목재 벽 코너·창 개구부·문틀, 외벽 전기 접속함 방향별 조각, 수직 빗물 배수관.
- 누적 **3,285/5,409종(60.7321%)**, 미관찰 **2,124종**, 감사 가능한 누적 잠정 후보 **2,817종**, 최종 인증 **0종**.
- `checkpoints/v70/observations.tsv`, CSV, `checkpoints/v70_preview/` 원본 증거 JPEG 75장, 이미지 내장 HTML(75장), ZIP(79항목 CRC PASS)을 보존한다.
- `analysis/current/v70/MANIFEST.json`: SQLite **84,553,728바이트**, SHA-256 `3fe194e8097ef41658a9eed7970b8f0c567c4bf1b8e9a115c988ab2be72a7087`. SHA 왕복·SQLite 무결성·이전 테이블 보존·신규 키 중복·원본 SHA·PNG/JPEG 로딩·장면 B-C·ZIP CRC 검증 통과.
- 모든 신규 키의 PNG 높이 불일치와 공식 Local ID·TileZed 미검증 상태를 유지한다. `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`; 이전 v69 이하 및 사용자 직접 검수 80종을 변경하지 않는다.

## v71 신규 직접 이미지 판독 (2026-10-26)
- v70 통합 SQLite 미관찰 2,124종에서 중복 없는 신규 키 20종을 선별했다. 원본 PNG·TMX의 A/B/C/D 및 비교판 **100 JPEG**를 GitHub Actions로 생성하고 비교판 20개를 직접 열어 육안 판독했다.
- 신규 잠정 후보 **18종**, 보류 **2종**(`location_trailer_02/59`, `/60`: 지붕 표면의 음영·경계 부품으로 보이나 정확한 기능 불명). 모든 B-C 비교에서 픽셀 변화가 있었다.
- 주요 잠정 후보: 밝은 아이보리 카운터 조각 2종, 갈색 주방 상부장, 목재 야외 벤치 3종, 양문형 싱크대 하부장, 녹색 기둥형 드릴프레스, 풀잎 오버레이 10종. 이름만으로 판단하지 않고 A의 외형과 B/C 변화 및 D 배치를 대조했다.
- 누적 관찰 **3,305/5,409종(61.1019%)**, 미관찰 **2,104종**, 누적 잠정 후보 **2,835종**, 최종 인증 **0종**.
- `checkpoints/v71/observations.tsv` 및 CSV, `checkpoints/v71_preview/`의 JPEG 100장, HTML 내장 검수기, 증거 ZIP 104항목 CRC PASS를 보존한다.
- `analysis/current/v71/MANIFEST.json`: SQLite **84,598,784바이트**, SHA-256 `8a65bffd76b5e2ed397e8822f1b289301f3df09dd49c7009c15bacfde93ef505`. 원본 SHA, JPEG 로딩, SQLite 무결성, 기존 테이블 보존, 중복 키 0을 검증했다.
- PNG 물리 높이와 TMX 선언 높이 불일치, 공식 Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. 과거 체크포인트와 사용자 수동 검수 80종은 변경하지 않는다.

## v72 신규 직접 이미지 판독 (2026-10-26)
- v71 통합 SQLite 미관찰 **2,104종** 중 중복 없는 신규 **20종**을 선별했다. GitHub 원본 PNG/TMX를 이용한 A(원본)·B(동일 층 5×5)·C(선택 배치 하나 제거)·D(다른 실제 사용 위치)와 비교판 **100 JPEG**를 생성하고 비교판 20개를 직접 열어 관찰했다.
- 신규 잠정 후보 **20종**, 보류 **0종**. 대상: 아이보리색 상부장 2종, 갈색 주방 상부장 코너 1종, 목재·철제 야외 벤치 분할 조각 3종, 황록·녹갈색 풀잎 오버레이 14종. 타일셋명만으로 정체를 판정하지 않고 각 A의 외형과 B-C 제거 효과 및 D 사용 장면을 비교했다.
- 누적 관찰 **3,325/5,409종(61.4716%)**, 미관찰 **2,084종**, 감사 가능한 잠정 후보 **2,855종**, 최종 인증 **0종**. 신규 중복 키 0.
- 증거: `checkpoints/v72/observations.tsv`·CSV, `checkpoints/v72_preview/`의 A/B/C/D+비교판 100 JPEG, 이미지 내장 HTML, ZIP **104항목 CRC PASS**.
- `analysis/current/v72/MANIFEST.json`: SQLite **84,643,840바이트**, SHA-256 `17f2ca1c42af9f93f6fc4c6cbbe938118cccc1c9b95039f0351aa38278fa500b`. 원본 PNG/TMX SHA-256, JPEG 로딩, B-C 변화, 이전 테이블 보존, 중복 키 0, SQLite 무결성 및 압축 복원 왕복 검증.
- PNG 물리 높이와 TMX 선언 높이 불일치, 공식 Local ID·TileZed 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v71 원본·체크포인트 및 사용자 수동 검수 80종 보존.

## v73 신규 직접 이미지 판독 (2026-10-26)
- v72 통합 SQLite의 미관찰 **2,084종**에서 중복 없는 신규 20종을 선정했다. GitHub 원본 PNG/TMX로 A/B/C/D 및 비교판 **100 JPEG**를 생성하고 **20개 비교판을 실제 열어 육안 관찰**했다.
- **잠정 후보 16종, 보류 4종**. 갈색 4패널 여닫이문 2종, 검은 격자·키패드 출입문 1종, 목재·철제 벤치 방향별 조각 3종, 황갈색 야생 풀 오버레이 10종이 잠정 후보.
- 보류 `blends_grassoverlays_01/57`: B-C 변화 423픽셀·가림. `/59`, `/61`, `/67`: B-C 변화 0픽셀. A 외형과 가시 기여를 구분해 후보 단정을 피했다.
- 누적 이미지 관찰 **3,345/5,409종(61.8414%)**, 미관찰 **2,064종**, 감사 가능한 잠정 후보 **2,871종**, 최종 인증 **0종**.
- `checkpoints/v73/observations.tsv`·CSV, `checkpoints/v73_preview/` A/B/C/D 비교판 100 JPEG, `checkpoints/v73/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML·ZIP CRC 보고서를 보존한다.
- `analysis/current/v73/MANIFEST.json`: 물리 SQLite 84,688,896바이트, SHA-256 `002e8198db76667cb6c73103831e751933d024b50aa98490beab3e4d5acca104`; 압축 7조각 복원·SQLite 무결성·기존 테이블 보존을 검증했다. 기존 원본 DB, 이전 체크포인트, 수동 검수 80종은 변경하지 않는다.
- PNG 물리 높이 불일치와 TileZed 공식 정합 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.

## v74 신규 직접 이미지 판독 (2026-10-26)
- v73 통합 SQLite 미관찰 2,064종에서 중복 없는 신규 12종을 선정해 원본 PNG/TMX A/B/C/D 및 비교판 60 JPEG를 생성하고 12개 비교판을 직접 시각 판독했다.
- 잠정 후보 11종, 보류 1종(`blends_natural_01/19`, B-C 0픽셀). 반투명 유리문 2종, 야외 벤치 조각·줄무늬 데크체어 2종, 풀잎 오버레이 2종, 모래 바닥 3종, 잔디 경계 2종을 잠정 후보로 기록했다.
- 누적 이미지 관찰 3,357/5,409종(62.0632%), 미관찰 2,052종, 누적 잠정 후보 2,882종, 인증 0종.
- `checkpoints/v74/observations.tsv`, `checkpoints/v74_preview/`, `analysis/current/v74/MANIFEST.json`에 증거·통합 SQLite를 보존한다. PNG 높이 불일치와 TileZed 공식 검증은 미완료.

## v75 신규 직접 이미지 판독 (2026-10-26)
- v74 통합 SQLite의 미관찰 2,052종에서 신규 고유 키 **20종**을 선정하고 원본 PNG A, TMX 같은 층 5×5 B, 대상 배치 하나 제거 C, 다른 실제 사용 위치 D 및 비교판 **100 JPEG**를 생성해 **20개 비교판을 실제 열어 시각 관찰**했다.
- 신규 잠정 후보 **18종**, 보류 **2종**(`blends_natural_01/27`, `/29`; B-C 변화 0픽셀). 검은 프레임 유리문·회색 평판문 3종, 청백 줄무늬 낮은 접이식 야외 의자 1종, 아이보리색 키 큰 수납장 방향별 조각 2종, 잔디 바닥·삼각 경계·가는 풀잎 오버레이 14종을 분리 판독했다.
- 누적 **3,377/5,409종(62.4330%)**, 미관찰 **2,032종**, 감사 가능한 누적 후보 **2,900종**, 최종 인증 **0종**. 신규 키 중복 0.
- `checkpoints/v75/observations.tsv`·CSV, `checkpoints/v75_preview/`의 A/B/C/D 비교판 100 JPEG, `checkpoints/v75/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 100장 및 증거 ZIP **104항목 CRC PASS**.
- `analysis/current/v75/MANIFEST.json`: SQLite **84,774,912바이트**, SHA-256 `f71baf0507e7287230cd36f8411f2d98f46f1d83450a23d5dad3c0f10564dd9a`. 압축 7조각 복원, SQLite 무결성, 이전 테이블 보존, 원본 PNG/TMX SHA, 이미지 로딩, B-C 근거 검증을 GitHub Actions에서 통과했다.
- 모든 신규 키의 PNG 물리 높이 불일치와 공식 Local ID·TileZed 미검증을 기록하고 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`을 유지한다. 사용자 수동 검수 80종과 과거 원본 자산은 별도 보존한다.

## v76 신규 직접 이미지 판독 (2026-10-26)
- v75 통합 SQLite 미관찰 **2,032종**에서 중복 없는 **20종**을 선정했다. 원본 PNG/TMX A(원본)·B(같은 층 5×5 조립)·C(단일 배치 제거)·D(다른 실제 사용 위치)와 비교판 **100 JPEG**를 생성하고 **20개 비교판을 직접 열어 이미지 판독**했다.
- 신규 잠정 후보 **19종**, 보류 **1종**(`furniture_storage_01/14`, B-C 차이 단 **1픽셀**). 흰 타원 세면대 방향별 3종, 아이보리 수납장 분할 2종, 잔디 바닥 4종, 가는 풀잎 경계 7종, 삼각 잔디 경계 3종을 관찰 특징과 후보로 구분했다.
- 누적 이미지 관찰 **3,397/5,409종(62.8027%)**, 미관찰 **2,012종**, 감사 가능한 누적 잠정 후보 **2,919종**, 최종 인증 **0종**. 신규 중복 키 0.
- 증거: `checkpoints/v76/observations.tsv`·CSV, `checkpoints/v76_preview/` A/B/C/D+비교판 100 JPEG, `checkpoints/v76/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML, 증거 ZIP **104항목 CRC PASS**.
- `analysis/current/v76/MANIFEST.json`: 물리 SQLite **84,815,872바이트**, SHA-256 `4eeca114b57f2ed286b1215cc89a76cb83aa9c0bc9f2c6b22f4e1efc8a46f4ab`. GitHub Actions에서 v75 복원 SHA, 원본 PNG/TMX SHA, 이미지 100장 로딩, 새 키 중복, SQLite 무결성·이전 테이블 보존·압축 복원 검증을 통과했다.
- PNG 물리 높이 불일치 및 TileZed 공식 정합 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v75 원본·체크포인트 및 사용자 수동 검수 80종은 변경하지 않는다.

## v77 신규 직접 이미지 판독 (2026-10-26)
- v76 최신 통합 SQLite `analysis_queue` 미관찰 **2,012종**에서 중복 없는 신규 **20종**을 선정했다. GitHub 원본 PNG/TMX의 A(원본), B(동일 층 주변 5×5), C(단일 배치 제거), D(다른 실제 사용 위치) 및 비교판 **100 JPEG**를 생성하고 **20개 비교판을 실제 이미지로 직접 열어 판독**했다.
- 신규 **잠정 후보 16종**, **보류 4종**. 흰색 벽걸이 세면대, 사각 스테인리스 싱크볼, 갈색 키 큰 옷장 분할 조각, 황갈색 잔디 바닥과 사선 풀잎·흙 경계가 주요 잠정 후보. 보류는 `fixtures_sinks_01/10`(B-C 0), `blends_natural_01/60`(0), `/74`(18), `/75`(51)로 가림·변화 미미. `furniture_storage_01/22`는 B-C 239로 신뢰도 낮음.
- 누적 **3,417/5,409종(63.1725%)**, 미관찰 **1,992종**, 감사 가능한 누적 잠정 후보 **2,935종**, 최종 인증 **0종**. 신규 키 중복 0.
- 증거: `checkpoints/v77/observations.tsv`·CSV, `checkpoints/v77_preview/` A/B/C/D+비교판 100 JPEG, `checkpoints/v77/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 100장 및 증거 ZIP **104항목 CRC PASS**.
- `analysis/current/v77/MANIFEST.json`: 물리 SQLite **84,860,928바이트**, SHA-256 `c534cdf47b801e09e6530af123b8855a08652397c79d0dc60d855ec678d352a7`. GitHub Actions에서 v76 복원 SHA, 원본 PNG/TMX SHA, JPEG 로딩, 신규 키 중복, SQLite 무결성·이전 테이블 보존·압축 복원·ZIP CRC를 검증했다.
- PNG 물리 높이 불일치 및 TileZed 공식 정합 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v76 원본·체크포인트 및 사용자 수동 검수 80종은 변경하지 않는다.

## v78 신규 직접 이미지 판독 (2026-10-26)
- v77 통합 SQLite의 미관찰 **1,992종**에서 중복 없는 신규 **12종**을 선정했다. GitHub 원본 PNG/TMX로 A(원본), B(동일 층 5×5 조립), C(선택 배치 하나 제거), D(다른 사용 위치) 및 비교판 **60 JPEG**를 생성하고 **12개 비교판을 직접 열어 육안 검수**했다.
- 신규 잠정 후보 **7종**, 정체 보류 **5종**. 주요 후보는 금속 싱크볼·분사 수전·격자 선반이 결합된 업소용 싱크대, 갈색·검은색 키 큰 보관장, 방향별 황갈색 마른 풀 삼각 경계 4종이다. 보류는 `fixtures_sinks_01/30`(B-C 0), `blends_natural_01/80`(0), `/85`(0), `/86`(0), `/87`(4)로 가림과 미미한 배치 기여 때문이다.
- 누적 **3,429/5,409종(63.3943%)**, 미관찰 **1,980종**, 감사 가능한 잠정 후보 **2,942종**, 최종 인증 **0종**. 신규 고유 키 중복 0.
- 증거: `checkpoints/v78/observations.tsv`·CSV, `checkpoints/v78_preview/`의 A/B/C/D 및 비교판 60 JPEG, `checkpoints/v78/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 60장 및 ZIP **64항목 CRC PASS**.
- `analysis/current/v78/MANIFEST.json`: 물리 SQLite **84,893,696바이트**, SHA-256 `160f7fb87fe854645d97bf2035d185743f70d4eb95a8d70c6c8f61b253eafe0b`. GitHub Actions에서 v77 복원 SHA, 원본 PNG/TMX SHA, JPEG 로딩, 신규 키 중복, SQLite 무결성·이전 테이블 보존·압축 복원·ZIP CRC를 검증했다.
- PNG 물리 높이 불일치 및 TileZed 공식 정합 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v77 원본·체크포인트 및 사용자 수동 검수 80종은 변경하지 않았다.

## v79 신규 직접 이미지 판독 (2026-10-26)
- v78 통합 SQLite `analysis_queue` 미관찰 1,980종 중 중복 없는 신규 고유 키 **12종**을 선택하고 GitHub 원본 PNG·TMX로 A/B/C/D+비교판 **60 JPEG**를 생성했다. 12개 비교판을 **실제 열어 시각 판독**했다.
- 신규 **잠정 후보 8종**, **정체 보류 4종**. 업소용 싱크대와 분사 수전, 검정 키 큰 장의 문판·측면, 검정 2단 서랍장, 물가 청회색 경계 오버레이 2종, 도로 아스팔트 삼각 경계 3종이 잠정 후보. 보류: `fixtures_sinks_01/35`(B-C 0), `blends_natural_01/88`(492), `/91`(491), `blends_street_01/0`(0).
- 누적 **3,441/5,409종(63.6162%)**, 미관찰 **1,968종**, 감사 가능한 누적 잠정 후보 **2,950종**, 최종 인증 **0종**. 신규 중복 키 0.
- 증거: `checkpoints/v79/observations.tsv`·CSV, `checkpoints/v79_preview/`의 JPEG 60장, `checkpoints/v79/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 60장 및 ZIP **64항목 CRC PASS**.
- `analysis/current/v79/MANIFEST.json`: SQLite **84,922,368바이트(매니페스트 기준)**, SHA-256 `52324ec4bdf5377b85594115e24e0156b0459858cbf3fcf1efb9dd7d4abc2e80`. GitHub Actions에서 v78 복원 SHA, 원본 PNG/TMX SHA, 이미지 로딩, 중복 키, SQLite 무결성·이전 테이블 보존·압축 복원·ZIP CRC를 검증했다.
- PNG 물리 높이 불일치 및 공식 Local ID·TileZed 정합 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v78 원본·체크포인트 및 사용자 수동 검수 80종은 변경하지 않는다.

## v80 신규 직접 이미지 판독 (2026-10-26)
- v79 통합 SQLite 미관찰 **1,968종** 중 중복 없는 신규 **20종**을 선정하고 GitHub 원본 PNG/TMX의 A(원본), B(동일 층 5×5), C(단일 배치 제거), D(다른 실제 위치)와 비교판 **100 JPEG**를 생성했다. 비교판 20개를 직접 열어 판독했다.
- 신규 잠정 후보 **19종**, 보류 **1종**(`furniture_storage_01/40`, B-C 변화 0). 검은 개방형 금속 계단 3종, 침실용 검정 낮은 장 2종, 도로 보수 아스팔트·균열 경계·모래/자갈 경계 14종을 외형과 배치 기여로 구분했다.
- 누적 **3,461/5,409종(63.9859%)**, 미관찰 **1,948종**, 감사 가능한 누적 잠정 후보 **2,969종**, 최종 인증 **0종**. 신규 고유 키 중복 0.
- 증거: `checkpoints/v80/observations.tsv`·CSV, `checkpoints/v80_preview/` A/B/C/D+비교판 100 JPEG, `checkpoints/v80/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 100장 및 증거 ZIP **104항목 CRC PASS**.
- `analysis/current/v80/MANIFEST.json`: SQLite **84,971,520바이트**, SHA-256 `255a92f0851dbc769fbc7da6863925fb99eaa4d541b5643b93b124ac5b4caa97`. GitHub Actions에서 v79 복원 SHA, 원본 PNG/TMX SHA, JPEG 로딩, 중복 키, SQLite 무결성·이전 테이블 보존·압축 복원·ZIP CRC 검증을 통과했다.
- PNG 물리 높이 불일치와 공식 Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v79 원본·체크포인트와 사용자 수동 검수 80종은 별도 보존한다.

## v81 신규 직접 이미지 판독 (2026-10-26)
- v80 통합 SQLite 미관찰 **1,948종** 중 고유 키 중복 없는 신규 **12종**을 선별했다. 원본 PNG A, 동일 층 5×5 TMX 합성 B, 단일 배치 제거 C, 다른 실제 사용 위치 D 및 비교판 **60 JPEG**를 GitHub Actions로 생성하고 비교판 12개를 실제 열어 육안 판독했다.
- 신규 **잠정 후보 10종**, **보류 2종**. 갈색 개방형 금속 계단 분할 2종, 아치형 거울이 붙은 밝은 목재 3단 화장대 2종, 회색 아스팔트 포장 바닥·삼각 블렌드·가는 경계선 6종이 잠정 후보. 보류 `blends_street_01/32`, `/39`는 B-C 변화 0픽셀로 단일 배치 기여를 확인하지 못했다.
- 누적 **3,473/5,409종(64.2078%)**, 미관찰 **1,936종**, 감사 가능한 누적 잠정 후보 **2,979종**, 최종 인증 **0종**, 신규 키 중복 **0종**.
- 증거: `checkpoints/v81/observations.tsv`·CSV, `checkpoints/v81_preview/`의 A/B/C/D 및 비교판 60 JPEG, `checkpoints/v81/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 60장 및 ZIP **64항목 CRC PASS**.
- `analysis/current/v81/MANIFEST.json`: SQLite **85,008,384바이트**, SHA-256 `0f04632938f637916e84706e5e933cbeccb541ee88dfb334e6dd813b3d14294b`. GitHub Actions에서 v80 SHA 복원, 원본 PNG/TMX SHA, JPEG 로딩, 중복 키, SQLite 무결성·이전 테이블 보존·압축 복원·ZIP CRC를 검증했다.
- PNG 높이 불일치 및 공식 Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v80 원본·체크포인트 및 사용자 수동 검수 80종은 보존한다.

## v82 신규 직접 이미지 판독 (2026-10-26)
- v81 최신 통합 SQLite의 미관찰 **1,936종**에서 중복 없는 신규 고유 키 **12종**을 선별했다. GitHub 원본 PNG/TMX로 A(원본), B(동일 층 5×5), C(선택 배치 하나 제거), D(다른 실제 위치), 비교판 **60 JPEG**를 생성하고 **12개 비교판을 직접 열어 육안 판독**했다.
- 신규 잠정 후보 **8종**, 보류 **4종**. 금속 계단 분할 2종, 밝은 목재 3단 서랍장, 도로 포장 패치의 가는 경계 2종, 자갈 바닥의 삼각 경계 3종이 잠정 후보다. 보류는 `furniture_storage_01/45`(B-C 0), `blends_street_01/41`(340), `/52`(0), `/56`(166): 가림·배치 기여 미확인·미세한 변화.
- 누적 **3,485/5,409종(64.4297%)**, 미관찰 **1,924종**, 감사 가능한 누적 후보 **2,987종**, 최종 인증 **0종**, 신규 고유 키 중복 0.
- 증거: `checkpoints/v82/observations.tsv`·CSV, `checkpoints/v82_preview/` A/B/C/D 및 비교판 60 JPEG, `checkpoints/v82/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 60장, ZIP **64항목 CRC PASS**.
- `analysis/current/v82/MANIFEST.json`: SQLite **85,037,056바이트**, SHA-256 `2171804042807905938c00a8817fb9a50e5f6911eeb52802374c94cb0274e0d1`. GitHub Actions에서 v81 원본 SHA 복원, PNG/TMX SHA, JPEG 로딩, 신규 키 중복, SQLite 무결성·기존 테이블 보존·압축 복원·ZIP CRC 검증 통과.
- PNG 물리 높이 불일치, 공식 Local ID·TileZed 정합 미검증으로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v81 원본·체크포인트와 사용자 수동 검수 80종은 별도 보존한다.

## 다음 작업
- v92 `analysis_queue`의 **미관찰 1,220종**에서 중복 없는 신규 키를 선정해 A/B/C/D 직접 시각 검수를 계속한다.
- v92 이하 보류 타일의 가림·분할 부품 역할을 다른 위치에서 재검수한다.
- PNG–TMX Local ID 물리 높이 불일치와 TileZed 공식 정합을 독립 검증한다.
- 기존 원본·체크포인트·사용자 수동 검수 80종을 보존하고 SHA·SQLite 무결성·CRC·중복을 확인한다.
- GitHub 커밋은 한국어를 기본으로 하고 공개 저장소에 토큰·개인정보·비공개 대화 원문을 올리지 않는다.

## v83 신규 직접 이미지 판독 (2026-10-26)
- v82 통합 SQLite의 `analysis_queue` 미관찰 1,924종 중 기존 키와 중복 없는 신규 **12종**을 선정했다. 원본 PNG A, 동일 층 5×5 TMX B, 단일 배치 제거 C, 다른 실제 사용 위치 D 및 비교판 **60 JPEG**를 생성하고 12개 비교판을 직접 열어 판독했다.
- 신규 잠정 후보 **10종**, 보류 **2종**(`furniture_storage_01/50`, `blends_street_01/59`; B-C 변화 0). 검정색 금속 계단 분할 2종, 연갈색 수납장 1종, 포장 경계선 2종, 회색 아스팔트 삼각 경계 4종, 아스팔트 바닥 1종을 잠정 기록했다.
- 누적 이미지 관찰 **3,497/5,409종(64.6515%)**, 미관찰 **1,912종**, 감사 가능한 누적 후보 **2,997종**, 최종 인증 **0종**. 신규 중복 키 0.
- `checkpoints/v83/observations.tsv`·CSV, `checkpoints/v83_preview/` 원본 A/B/C/D+비교판 60 JPEG, `checkpoints/v83/INDEPENDENT_VISUAL_AUDIT.md`, 이미지 내장 HTML 60장, ZIP 64항목 CRC PASS를 보존한다.
- `analysis/current/v83/MANIFEST.json`: SQLite **85,069,824바이트**, SHA-256 `4101d1a1df655df0161fbd4da75890f508a8b68bd80cc003f34413a2409b6369`. 압축 7조각 복원·SHA-256·SQLite integrity_check·이전 테이블 보존·원본 PNG/TMX 해시·PNG/JPEG 로딩·B-C 장면·ZIP CRC 검증.
- PNG 물리 높이와 TMX 선언 높이 불일치 및 공식 Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v82 체크포인트와 원본 자산, 사용자 수동 검수 80종은 변경하지 않는다.

## v84 신규 직접 이미지 판독 (2026-10-26)
- GitHub v83 통합 SQLite의 미관찰 1,912종에서 중복 없는 **92종**을 선정해 A: 원본 PNG, B: TMX 같은 층 5×5, C: 한 배치 제거, D: 다른 실제 TMX 위치, ABCD 비교판 **460 JPEG**를 직접 열어 판독했다.
- 신규 잠정 후보 **74종**, 보류 **18종**, 누적 **3,589 / 5,409종(66.3524%)**, 미관찰 **1,820종**, 누적 후보 **3,071종**, 최종 인증 **0종**, 기존 관찰 키 중복 0.
- 사물·부품 역할 관찰: 3단 목재 계단, 반원형 목제 창틀의 좌우, 커튼 상단 레일, 양문 철망 수납장·옷장·상자, 도로 포장 블렌딩과 노면 균열, 바닥 돌·바위, 차양 기둥·목재 가로보·삼각 보강대, 정원 관목 등을 분리 기록했다.
- **보류 18종**은 PNG 원본에서 모양이 보이더라도 TMX 배치 가림·B-C 미세 변화·분할 타일 연결 불충분 때문에 공식 정체 후보를 기입하지 않았다.
- 증거: `checkpoints/v84/observations.tsv` 및 CSV, `checkpoints/v84_preview/`의 A/B/C/D와 비교판 460 JPEG, `checkpoints/v84/v84_이미지내장_검수.html`에 460장 데이터 URI, `v84_증거_92종_A_B_C_D.zip`에 **464파일 CRC PASS**.
- `analysis/current/v84/MANIFEST.json`: 물리 SQLite **85,229,568바이트**, SHA-256 `db8975cbaea588d17b4f5f36375fea3366c3bdb0f0b8389596d89ad200548708`와 압축 7조각. v83 원본 SHA 복원, v84 압축 왕복, PRAGMA integrity_check, 테이블 보존·원본 PNG/TMX SHA·장면 근거·키 중복·PNG/JPEG 로딩 검사 통과.
- 공식 PNG–TMX Local ID 높이와 TileZed 매핑 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. v36~v83 모든 원본·관찰 계보 및 사용자 수동 검수 80종 불변.
- **다음 작업**: v84 통합 DB 미관찰 **1,820종**에서 이어서 신규 키를 검수하고, 별도로 기존 보류 타일·공식 Local ID 정합을 검증한다.
