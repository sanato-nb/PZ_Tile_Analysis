# 프로젝트 좀보이드 B42 타일 정체 분석 — 인수인계 (v131 최신)

## v145 군용시설·식당 A/B/C 실제 이미지 관찰 (2026-10-27)

- 원본 A/B/C 접촉시트 1680~1839 총 160개 직접 검토; PNG 픽셀·원래 TMX GID/좌표/층/레이어, C 제거 및 B-C SHA 검증 통과 **153종**만 provisional_candidate, **7종**은 B-C=0·이웃 누락·지도 경계 등으로 신규 완료 계산 제외.
- 전체 84 TMX 고유 10,042종에서 **7054종 관찰 기록 (70.24%)**, 미관찰 **2988종**. 공식 Local ID↔PNG/TileZed·정체 최종 인증 각 0. 준비된 ABCD 증거는 정체 완료가 아님.
- 물리 SQLite analysis/current/v145/MANIFEST.json, SHA 4c045c742bf4f5b62dae66b8f2a8a42d35f8a364d7d23b46ada65643736e7d13, **207개 테이블**(v144 이전 206테이블과 전체 기존 행 수 보존, 신규 153행 1테이블). PRAGMA integrity_check=ok. 증거 review/v145_abc_1680_1839 에 CSV·PNG ZIP·접촉시트·예외표 저장.
- 기존 수동80·사용자 제외14·기존5409, 사용자 held D2/JUMBO20, 원본 PNG/TMX 및 과거 DB 불변. D 다른 A 동일 TMX 위치/층/레이어 공식 매핑 미검증, 인접격자 및 두 번째 TMX 위치는 인증 근거 아님.

---
<!-- AUTO_CHECKPOINT_START -->
## 자동 확인된 최신 진행 상태 (v145)

- TMX 고유 10,042종, 이미지 관찰 기록 7,054종 (70.24%), 미관찰 2,988종.
- 정체는 잠정 후보. 공식 PNG↔Local ID 매핑 0종, TileZed 검증 0종, 최종 인증 0종.
- 물리 SQLite: analysis/current/v145/MANIFEST.json, 207테이블, SHA256 4c045c742bf4f5b62dae66b8f2a8a42d35f8a364d7d23b46ada65643736e7d13.
- 기존 사용자 수동 80종, 제외 14종, 보류 D 2종과 JUMBO 20종 및 원본 PNG/TMX는 보존.
- D는 동일 (tile_set_name, local_id)의 다른 A를 원래 B TMX의 동일 좌표·층·레이어에 치환한 비교임. 과거 두 번째 TMX 위치·인접격자 D는 인증되지 않음.
- 아래 버전별 상세 인수인계는 그대로 보존.
<!-- AUTO_CHECKPOINT_END -->

## v144 최신 실제 A/B/C 이미지 검수 — 학교·극장·농장·숙박시설 (2026-10-27)

- 인덱스 **1520~1679**의 기존 A 원본, B 실제 TMX 주변, C 원래 GID 단일 제거 및 차이 접촉시트 019·020 **160종 직접 시각 관찰**. 학교 게시판·그림·극장 영화간판과 경계선·농가 여물통/지붕·숙박시설 벽·계단 등 외형, 부분 역할, 재질, 증거, 신뢰도 기술.
- 원본 PNG 전체 및 A RGBA 픽셀 SHA256, **실제 원래 TMX raw GID·층·레이어·x/y**, B/C/차이 원본 ZIP SHA·CRC 및 DB 무결성 검사 통과한 **149종만 `provisional_candidate` 신규 관찰 기록**. 나머지 **11종**(1524,1530,1546,1588,1590,1595,1597,1598,1601,1602,1675)은 B−C=0·이웃 누락·지도끝 등 비교 근거 부족으로 새 관찰 완료에서 제외. **투명 판정 아님**.
- 84 TMX 고유 10,042종 가운데 **6,901종 이미지 관찰 기록 (68.72%)**, **3,141종 미관찰**. 원래 수동80, 사용자 제외14, D 보류2, JUMBO20, 원본 5,409 및 이전 인증·검증 이력 보존. 신규 물체 후보도 공식 PNG↔Local ID 매핑 0, TileZed 검증 0, 최종 정체 인증 0; 기존 D 인접 격자·두 번째 TMX 위치를 사용자 정의 같은 키 다른 A 비교 인증으로 간주하지 않음.
- 물리 SQLite `analysis/current/v144/MANIFEST.json`: SHA256 `90d4cb0e60cdfaa60f5868e986771119a430fb9762c9f6b0a1ad566f891cc08c`, **206테이블** (부모 v143의 205 물리 테이블 및 기존 모든 행 수 불변 + v144 149행 1개 테이블), PRAGMA integrity_check=ok. 새 근거는 `review/v144_abc_1520_1679/VISUAL_REVIEW.csv`, `MANUAL_VISUAL_NOTES.json`, `EXCLUDED_EXCEPTIONS.csv`, 접촉시트, `ABC_EVIDENCE_VERIFIED.zip` (원본 A/B/C/차이 이미지 총 596개)에 보관. 원본 PNG/TMX/이전 SQLite를 직접 수정하지 않음.
- 다음 미관찰 3,141종 분석을 계속하며, 공인 TileZed 소스·원본 아틀라스 매핑은 별도 단계로만 인증. 폐기 범용 TMX 평면도 엔진 사용 금지. Minecraft 전체 블록 벽 취향과 PZ 선형 벽 좌표 충돌은 여전히 미해결.

---
## v143 신규 원본 A/B/C 의료시설·공원·경찰서·학교 타일 시각 검수 (2026-10-27)

- 인덱스 1360~1519의 기존 A017/A018 타일 원본, 실제 TMX 맥락 B017/B018, 대상 하나 제거 C·B−C 접촉시트 **160종을 직접 시각 관찰**. 대형 의료용 링형 장비·공원 그네와 미끄럼틀·경찰서 철살문·안내문자·학교 책상·칠판·교실 표시 등 외형, 재질, 부분 역할과 잠정 신뢰도를 기록. 글자형·바닥형 픽셀은 낮은 신뢰도 유지.
- PNG 파일 SHA256, 정확한 A RGBA 크롭 픽셀 SHA, 실제 TMX raw GID·층·레이어·x/y, B/C/DELTA 이미지 ZIP SHA 및 CRC 검증 통과 **152종만 `provisional_candidate` 신규 관찰**. **8종** (1362,1363,1461,1462,1501,1502,1503,1504)은 비교 결과 또는 장면 정보가 부족해 관찰 완료에서 제외했으며 투명 인증하지 않음.
- 전체 10,042 고유 타일 중 **6,752종 개별 이미지 관찰 기록 (67.24%)**, **3,290종 미관찰**. 기존 5,409에서 9종, 신규 4,633에서 3,281종 미관찰. 공식 A PNG↔Local ID/TileZed 및 정체 최종 인증 **각 0종**. 과거 인접 격자 D/두 번째 사용 위치는 사용자 정의 D 동일키 다른 A 원위치 삽입 공식 증거가 아님.
- 새 물리 SQLite `analysis/current/v143/MANIFEST.json`: SHA256 `50c0bfcf1129f2843846254a5172f41966859fa090eeb27009d977239699a557`, **205테이블** (v142 이전 204개 테이블·모든 행 수 보존 + v143 관찰 152행 1개 테이블). `PRAGMA integrity_check=ok`.
- 시각 근거 `review/v143_public_1360_1519/VISUAL_REVIEW.csv`, `MANUAL_VISUAL_NOTES.json`, `EXCLUDED_EXCEPTIONS.csv`, `ABC_EVIDENCE_VERIFIED.zip` (원본 A/B/C/DIFF 608파일), `sheets/proof_*.jpg`, `MANIFEST.json`. 사용자 수동80·제외14·보류 D2·JUMBO20, 기존 5,409 및 원본 PNG/TMX·과거 모든 DB 무변경. 폐기 평면도 엔진 금지.

---
## v142 직접 이미지 검수 — 1200~1359, 2026-10-27

- 이미 생성된 A015/A016 원본 PNG 타일, 원래 TMX B 맥락과 대상 1개 제거 C·B−C 접촉시트 **160개를 실제 시각 관찰**. 조명·헛간 외벽/지붕·은행 단말기·사무 책상·묘비/비석·교회 십자가/첨탑·의료용 침상/수액걸이 등 외형, 역할, 재질, 신뢰도를 개별 잠정 기록.
- 원본 PNG 파일 SHA와 정확한 A RGBA 픽셀 SHA, 실제 TMX raw GID·층·레이어·x/y, B/C/DELTA 파일 SHA와 ZIP CRC 재검증을 통과한 **141종만 `provisional_candidate`**로 신규 관찰. **19종 예외**는 원래 B−C 무변화·이웃 누락·지도 경계 등을 분리하여 관찰 수치에서 제외. 투명 또는 최종 정체로 인증 금지.
- 누적 관찰 **6,600 / 10,042종 (65.72%)**, 잔여 미관찰 **3,442종**. 기존 5,409 중 미관찰 9종과 신규 4,633 중 미관찰 3,433종 포함. Local ID↔원본 PNG의 공인 매핑 검증, TileZed 검증, 최종 사물 정체 인증 **모두 0**. 현재 사용자 정의 D (같은 tile_set_name/local_id의 다른 A를 동일 B 위치·층·레이어에 대입) 공식 검증 없음.
- 물리 DB `analysis/current/v142/MANIFEST.json`: sha256 `31494a2daf3decea44fa8354d8f1b598f7d1bfd1876cc77678b16474687653b8`, **204개 테이블**, 부모 v141 203테이블과 이전 모든 행 수 보존, 141 신규행 1 테이블만 추가. `PRAGMA integrity_check=ok`.
- 리뷰·원본 픽셀 증거 `review/v142_community_1200_1359/VISUAL_REVIEW.csv`, `EXCLUDED_EXCEPTIONS.csv`, `sheets/proof_*.jpg`, `ABC_EVIDENCE_VERIFIED.zip` (A/B/C/DIFF 네 개씩), `MANUAL_VISUAL_NOTES.json`. 기존 5,409, 사용자 수동80·제외14, D held2, 기존 JUMBO held20, 원본 84 TMX 및 PNG·과거 모든 물리 DB 무변경. 폐기 TMX 범용 평면도 엔진 사용 금지.

---
## v141 최신: 산업설비·철도·트럭 부품 A/B/C 실제 시각 검수 (2026-10-27)

- 신규 인덱스 **1040~1199**에서 이미 생성된 A 원본/원래 TMX B 맥락/C 제거·픽셀 차이 접촉시트 **160종을 눈으로 직접 검수**. 산업용 금속 보·배관·수직 캐비닛·공작 설비·철도 출입문·트럭 격벽/차체 패널·조명 등 외형·재질·부분 역할·신뢰도 잠정 기록.
- 각 결과에 대해 원본 PNG 파일 및 RGBA 픽셀 SHA256, 실제 TMX raw GID·층·레이어·좌표, B/C/DELTA 증거 이미지 바이트 해시와 ZIP CRC 검증. **142종만 `provisional_candidate` 신규 관찰**, 18종은 B−C 차이0·주변 누락·지도 경계 등 검수 예외로 분리하고 **관찰 완료에 불포함**. 투명 타일 인증으로 오인 금지.
- 전체 84 TMX 10,042종 중 **6,459종 개별 이미지 관찰 기록 (64.32%)**, **3,583종 미관찰**. 기존 5,409에서 9종 미관찰과 신규 4,633 중 3,574종 미관찰을 포함. 정체 이미지/Local ID 공식 대응·TileZed·최종 사물 인증 **각각 0종**. 동일키 다른 A를 같은 B 위치에 삽입하는 사용자 정의 D도 공식 매핑 없이는 최종 인증 불가.
- 새 물리 SQLite `analysis/current/v141/MANIFEST.json`: SHA256 `9623eec65d81ccf52738adc60dc1bb355faec9bcd02a2d17d9d45a6887c0fe38`, **203테이블**. 부모 v140의 202개 테이블/모든 기존 행 수 그대로 유지, 신규 142행 1개 테이블 추가, `PRAGMA integrity_check=ok`.
- 이미지·DB 증거 `review/v141_industry_1040_1199/MANUAL_VISUAL_NOTES.json`, `VISUAL_REVIEW.csv`, `sheets/proof_*.jpg`, `ABC_EVIDENCE_VERIFIED.zip` (568개 원본 A/B/C/DELTA), `EXCLUDED_EXCEPTIONS.csv`, `MANIFEST.json`. 사용자 검수80·제외14·기존5409·원래 D 보류2·JUMBO 보류20, 모든 원본 PNG/TMX와 이전 SQLite 그대로 보존.
- 남은 3,583종은 아직 시각 검수 미완료. ABCD 증거 생산과 최종 사물 인증은 다른 단계이며 임의 Local ID/인접격자 D의 다른 A를 공식 매핑처럼 사용하지 않는다.

---
## v140 최신 신규 타일 A/B/C 시각 검수 — 880~1039 (2026-10-27)

- 이미 만든 원본 A/실제 TMX 주변 B/대상 제거 C 접촉시트 011·012 **160종 직접 눈으로 판독**, 문양/바닥재/러그/침대/의자/선반/수납장/테이블/산업용 패널의 외형·부분 역할·재질·신뢰도를 개별 기록. 대상마다 원본 PNG 바이트·RGBA 픽셀 SHA, TMX GID·층·레이어·정확한 좌표, 기존 B/C/DELTA 이미지 SHA·ZIP CRC 재확인.
- **132종만 신규 `provisional_candidate` 관찰 기록**, 다른 **28종은 B−C 무변화·주변 누락·지도끝 등 근거 부족으로 기록 승격 제외**. 구체적 인덱스는 `review/v140_abc_880_1039/EXCLUDED_EXCEPTIONS.csv`. 투명 인증은 하지 않음.
- 누적 전체 84 TMX의 10,042종 가운데 **6,317종 개별 이미지 관찰 기록 (62.91%)**, 미관찰 **3,725종**. 이전 v139 6,185에 비중복 132종 추가. 기존 5,409종 중 미관찰 9종 및 신규 4,633종 중 미관찰 3,716종 포함. 공식 PNG↔Local ID 대응·TileZed·사물 최종 정체 인증 **모두 0종**이며 이미지로 추정한 후보 이름은 확정이 아님.
- 물리 SQLite `analysis/current/v140/MANIFEST.json`: SHA256 `eef72c11e3daf3bd5032ceba259d58ffaa5309897f755caa50e6e9dbeb4a8d78`, **202테이블**. 이전 v139 201개 물리 테이블·모든 기존 행 수 그대로 유지, 새로운 132행 `v140_visual_review` 1개 테이블만 추가. `PRAGMA integrity_check=ok`.
- 증거 `review/v140_abc_880_1039/VISUAL_REVIEW.csv`, `MANUAL_VISUAL_NOTES.json`, `sheets/proof_*.jpg`, 원본 A/B/C/DELTA 528개 파일 ZIP `ABC_EVIDENCE_VERIFIED.zip`, 제외 28종 CSV.
- 사용자 보류 D 2종/JUMBO20, 기존 5,409, 수동80, 제외14, 원본 84 TMX/원본 PNG/모든 과거 DB 변형 없음. 현재 정의 D인 *같은 키의 다른 A를 원래 B 위치·층·레이어에 대입*한 공식 대응 검증은 미완료. 과거 두 번째 TMX 위치/인접격자 D는 동일 정의의 인증이 아님. 폐기 평면도 엔진 사용 금지, Minecraft 전체 블록 벽 선호와 선형 벽 좌표 문제는 미해결.

---
## v139 최신 타일 정체 이미지 분석 — A/B/C 원본 실검수 160종 (2026-10-27)

- 이미 생성된 A/B/C 접촉시트 009·010을 실제로 관찰하고 신규 인덱스 **720~879, 160종** 외형·부품·재질의 잠정 후보를 정리. A 원본 PNG/RGBA SHA와 실제 TMX의 raw GID·층·레이어·x/y, B/C/차이 이미지 바이트 SHA·ZIP CRC 검사를 통과한 **149종**만 신규 `provisional_candidate`. 예외 **11종**(741,782,783,792,794,796,797,822,833,840,876)은 B−C 0·지도끝·이웃 누락 등의 검수 조건 미충족으로 관찰 완료에서 제외.
- 전체 10,042종 중 **6,185종 관찰 기록 (61.59%)**, **3,857종 미관찰**. 기존 5,409의 9종 미관찰과 신규 4,633 중 미관찰 3,848종 포함. 정체와 공식 A 로컬ID↔PNG 매핑, TileZed 최종 인증 각각 **0종**. D는 동일 키 다른 A의 같은 TMX 배치로 공식 검증되지 않았고 인접격자/과거 두 번째 위치는 인증 근거가 아님.
- 물리 SQLite `analysis/current/v139/MANIFEST.json`: SHA256 `e8aa0a4d9372cbb3a7ccaf54f28c0c089ae536219224ddfe15b35c1295884fa9`, **201테이블**, 부모 v138 200테이블·모든 기존 행 수 그대로 보존, 149행 1테이블만 추가, PRAGMA integrity_check=ok.
- 새 근거 `review/v139_abc_720_879/VISUAL_REVIEW.csv`, `MANUAL_VISUAL_NOTES.json`, `ABC_EVIDENCE_VERIFIED.zip` (원본 A/B/C/DIFF 4×149), `sheets/proof_*.jpg`, `EXCLUDED_EXCEPTIONS.csv`. 원본 PNG/TMX, 기존 5,409/사용자 수동80/제외14, 별도 D 보류2/JUMBO 보류20, 과거 모든 DB 및 이미지 그대로 보존.
- 최종 목표인 전체 3,857 미관찰 타일은 아직 완료하지 못함. 준비된 ABCD 이미지의 생산 완료율과 개별 정체 검수 진행률 혼동 금지.

---
## v138 최신 PNG/TMX 기반 시각 정체 분석 — PR #95~#99 (2026-10-27)

**실제 작업 범위**: 사용자 지시대로 기존 보류 D 2종 및 JUMBO 20종은 건드리지 않고, 이미 생성된 A/B/C 비교 증거를 **직접 눈으로 판독**하였다. 검사 근거는 (1) 원본 PNG 바이트 SHA256·A 크롭 RGBA 픽셀 해시, (2) 실제 원본 TMX의 raw GID·층·레이어·x/y, (3) B 5×5 원본과 정확히 같은 층·레이어·좌표에서 타일 하나를 제거한 C와 픽셀차이 ZIP SHA/CRC다. 인접 그리드 후보 D와 과거 두 번째 TMX 위치 D는 사물 정체의 공식 인증에 **사용하지 않음**.

| 병합 PR | 범위 | 신규 관찰 잠정 후보 | 검수 대상 중 제외 |
|---|---|---:|---:|
| [#95](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/95) | v134: 캠핑·목재 180~319 | 129 | 11 |
| [#96](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/96) | v135: 녹지·폐기물·철탑 400~479 (JUMBO 기존 held 20 제외) | 57 | 3 |
| [#97](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/97) | v136: 송전 철탑 480~559 | 80 | 0 |
| [#98](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/98) | v137: 식물·울타리 560~639 | 79 | 1 |
| [#99](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/99) | v138: 욕실·카운터·문 640~719 | 76 | 4 |

**합계: 신규 비중복 개별 이미지 관찰 421종**, 출처 시트 직접 판독 검수 대상 440종 중 19개 신규 완료 제외(이미 보류 20종 재분석하지 않음). 신규 421종 전부 `provisional_candidate`, **Local ID 아틀라스 공식 매핑 검증 0·TileZed 검증 0·정체 최종 인증 0**. 실물 이미지/주변 비교로 유추한 물체 명칭과 역할은 최종 확인 아님. 이번 요청 기준 총 **6,036 / 10,042종 관찰 기록 (60.11%)**, **4,006종 미관찰**. ABCD 실험 이미지가 이미 생성되었어도 개별 사물 판독/공식 매핑이 자동 완성되는 것은 아니다.

**DB**: `analysis/current/v138/MANIFEST.json` — SHA256 `973fe1337392be6b3099e54570569742930e90af7bcb68c8a3128d6660a495db`, **200 물리 테이블**. v137까지 199테이블과 모든 과거 행 수 보존, v138 관찰 76행 테이블만 추가, PRAGMA integrity_check=ok. 원본 PNG/TMX, 기존 5,409종의 기록, 사용자 수동80·제외14, 과거 버전 물리 SQLite 전부 보존. 증거는 `review/v134_visual_180_319/`부터 `review/v138_bath_counters_doors_640_719/`까지의 `VISUAL_REVIEW.csv`, 4개/타일 원본 비교 `ABC_EVIDENCE_VERIFIED.zip`, `sheets/proof_*.jpg`, 제외항목 CSV 및 매니페스트.

향후 단계는 **미관찰 4,006종의 개별 실물 관찰**과 원본 TileZed tiledefinitions/PNG-Local ID 대응 공인 검증, 기존 19건의 새 제외 사유 재검토다. 사용자 정의 D = 같은 키의 다른 A를 원래 B TMX 정확히 같은 위치·층·레이어에 치환하는 것; 4,628 인접 격자 D는 미인증이다. 폐기한 범용 TMX 평면도 엔진을 재사용하지 않으며 Minecraft 전체 블록 벽 선호·PZ 선형 벽 좌표 충돌은 미해결.

---
## v133 최신 실제 ABCD 이미지 정체 분석 (2026-10-27)

- **병합 PR #93**: [v133 32종 원본 A/B/C/D 시각 검수](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/93), [Actions 성공 검증](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40463349746).
- **새 시각 관찰 32종**: 신규 타일 인덱스 360~399 중 32종 `provisional_candidate`. A 원본 PNG 바이트와 RGBA SHA256, 원래 TMX raw GID·층·레이어·x/y 및 B/C/차이 이미지 해시 확인. D는 **다른 Local ID일 수 있는 인접 격자 가설**이므로 사물 정체 인증 근거에 사용 금지. 해당 구간 8개 인덱스 [363,364,377,378,381,382,388,397]은 이번 신규 분석에서 제외/미분류.
- 시각 결과: `review/v133_visual32/VISUAL_REVIEW_32.csv`, `sheets/visual_00.jpg`~`03.jpg`, 실제 PNG 160장 `ABC_D_32_PROOF.zip`. 물체 외형, 후보 정체, 부품, 재질, 신뢰도, 근거 기록; 공식 Local ID 매핑·TileZed·최종 사물 인증 **모두 0**.
- **84 TMX 전체 고유 10,042종 기준 개별 이미지 관찰 누계 5,615/10,042 (55.92%)**, 미관찰 4,427. v132의 5,583종 + 신규 겹치지 않는 32종. 수동 80, 제외 14, 기존 5,409 모두 보존.
- **실물 v133 통합 SQLite**: `analysis/current/v133/MANIFEST.json`, SHA256 `bf85d911bd8ba27aa20fcd38e923de9555196b03cc2fc8d95eb3bb7f4f0b3bc3` (93,839,360 bytes). v132 194개 테이블과 모든 기존 행 수 그대로 보존하고 `v133_visual_review_32` 32행 1테이블만 추가하여 총 **195테이블**. `PRAGMA integrity_check=ok`, ZIP CRC·해시 검증 통과.
- 사용자 요구대로 원래 보류 D 2종은 **이번 작업 대상 제외**. 기존 v132 JUMBO 20종(그중 A3 격자 반복 의심 7종)도 `held` 그대로 유지. B−C 0 사례 215건·이웃 누락8·지도 경계48 미검증이며 투명 인증 금지.
- 보류 건은 삭제하지 않고 이력 보존. 과거 폐기한 범용 평면도 엔진 사용 금지. 얇은 벽보다 전체 Minecraft 블록 느낌 선호 및 벽 좌표 충돌 미해결.

---
## v132 최신 작업 — 실제 PNG/TMX 재검증·신규 3종 시각 후보·JUMBO A3 20종 감사 (2026-10-27)

- **병합된 PR #91**: [v132 원본 이미지와 TMX 실제 검수](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/91), 검증된 [Actions run 40460201283](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40460201283). 원본 v131 `main` `5bae2a6ef593b074f8731a19c48ad0bff5a5eff1`에서 추가, 기존 역사 불변.
- **새 이미지 직접 관찰 3종**: `vegetation_foliage_01/{0,1,3}`. 실제 서로 다른 원본 PNG 2개, 기존 A/B/C/D 이미지 직접 판독, 정확한 원본 TMX raw GID·층·레이어·좌표 및 원본 PNG 픽셀 SHA 검증. 낮은 갈색 관목·자줏빛 세로 관목·작은 녹색 관목은 **`provisional_candidate`**이고 `certified`가 아니다.
- **JUMBO A3 20종**: 원본 PNG 바이트·RGBA 크롭 SHA와 실제 TMX raw GID·Local ID 수치 대응 물리 확인, A3 시각 접촉시트 2장 검토. **7종 A3 크롭에 수관/나무의 상하 반복이 보이므로 잘못된 격자·멀티프레임 가능성**. 모두 `held`: 원본 정의로 A3 타일 프레임 자체가 공식 대응한다고 검증하지 않음. 기록: `review/v132_visual3_jumbo20/JUMBO_VISUAL_FINDINGS.md`.
- **미검수 우선순위 271행**: 기존 C B−C 차이0 215, B 이웃 누락8, 지도 가장자리48. 고유 타일 271종으로 중복 없이 센 값이 아니며 아직 해당 사례 전부 시각 판독한 것도 아니다. 보류/가림/차이0을 투명 인증하지 않는다. 전화기·전선 15×15 추가 검수는 미수행.
- **누적 이미지 개별 관찰 기록 5,583/10,042** (v131 5,580 + 신규 비중복 3), 미관찰 4,459. JUMBO A3 소스 검수20은 공식 정체 관찰 개수에 중복/확정 계상하지 않는다.
- **새 물리 통합 DB v132** `analysis/current/v132/MANIFEST.json`: 이전 v131 **193테이블/기존 모든 행 수 보존** + 새 `v132_visual3_jumbo20` (3 후보 + 20 보류) = **194테이블**, `PRAGMA integrity_check=ok`. SHA256 `4f4ce7be16a382457de1b4e1b6618452c3509957c697e8ba18de870fb213ddad` (93,802,496 bytes). 복원: `python3 scripts/restore_unified_v132.py /tmp/pz_v132.sqlite` (대상 파일 존재 시 덮어쓰기 거부).
- **공식 PNG↔TMX Local ID 매핑/TileZed/정체 최종 인증 각각 0종**. D는 여전히 *동일 키의 다른 A 후보를 정확히 같은 B TMX 위치·층·레이어에 치환한 비교*이고, v131의 인접 PNG 격자 4,628은 다른 ID일 수 있는 미검증 실험이다.
- **불변**: 84개 TMX 범위 10,042, 기존 5,409(새 분석 제외), 수동80·사용자 제외14, 기존 원본 PNG/TMX, 모든 v131 이하 SQLite와 이미지·사용자 철회 지시, 폐기 평면도 엔진 재사용 금지. 마인크래프트는 얇은 벽이 아니라 전체 블록 느낌을 선호하고 좌표 충돌 미해결.

검증 자료: `review/v132_visual3_jumbo20/README.md`, `VISUAL_OBSERVATIONS_3.csv`, `JUMBO_AUDIT_20.csv`, `PRIORITY_271_EXCEPTIONS.csv`, `VISUAL_3_ABCDE.jpg`, `JUMBO_20_sheet_{0,1}.jpg`, `analysis/current/v132/MANIFEST.json`.

---
## 최신 v131 — 신규 4,633종 D 전체 상태·실제 후보 재조립 완료 (2026-10-27)

- **D 현재 정의**: 같은 타일의 다른 A 이미지 후보를 **기존 B의 정확히 같은 TMX 위치·층·레이어에** 대입하여 기존 B/C와 비교. v124의 두 번째 TMX 사용 위치는 보조 위치 색인일 뿐 현재 D 단계 의미와 다름.
- **v131 PR #89 main 병합, Actions 40449775698 PASS**. 이전 v126/v129/v130 800키 결과 재사용 + 처음부터 미실행했던 **3,832키 12개 병렬 배치** 실제 조립 및 인수인계. 신규 총 4,633키 중 원본 A 있는 4,632키는 **4,631종 실험 D 생성**, 1종 후보 없음 보류. **원본 A PNG 없는 1종** 별도 보류. 즉 전체 상태 4,633/4,633행 확보, D 후보 미실행 0.
- 생성된 D의 A 근거: **인접 격자 크롭 4,628종(다른 Local ID일 수 있음)**, 다른 동명 PNG 이미지 3종(공식 매핑 미검증). **같은 Local ID의 올바른 A 매핑 검증 0종**, TileZed 검증 0종, 최종 정체 인증 0종. 이는 **후보 이미지 실험 완료**이지 공식 정답의 D 검증 완료 아님.
- 원본 B↔대체 D 픽셀 변화 **4,469종**, B−D 변화 0 **162종**, 원본 B−C 변화 0 **215종**. 변화 없음은 투명 타일 확정 아님.
- 보류 2종: `floors_interior_tilesandwood_01/74` (다른 A 후보 없음), `overlay_graffiti_wall_02/2` (정확한 원본 PNG 없음). 둘 다 투명/정체 없음으로 확정 금지.
- **전체 D 결과**: `review/v131_D_remaining_3832/D_FULL_SCOPE_4633_STATUS.csv`, 전수 SHA/ZIP/접촉시트·별도 `batch_*/` 12개, `D_ALL_HELD.csv`, `MANIFEST.json`, `QUALITY_AUDIT.md`. 모든 인덱스의 원래 TMX/레이어/GID와 증거 경로 추적 가능.
- **최신 물리 통합 DB v131**: `analysis/current/v131/MANIFEST.json`, 복원 `python3 scripts/restore_unified_v131.py /tmp/pz_v131.sqlite`. SHA-256 **fbf5530e23120a32fbd9664d3533a41b1be4d1a9bab39956e00b67fa15988029**. 부모 v130 **192개 테이블 전부 보존** + `v131_D_full_4633` 4,633행, 총 **193테이블**, SQLite integrity_check PASS.
- 모델이 v131 접촉시트 2장(광고·통신 설비, 실내 벽)을 직접 열어 인접 격자 가설이 다른 사물로 대체되는 사례 확인. 모든 4,631종의 정체를 시각 판독한 것이 아니며 **누적 관찰 5,580/10,042종 그대로**.
- 과거 5,409종, 수동 검수80, 사용자 제외14, 원본 PNG/TMX, 모든 역사적 v116~v130 SQLite는 무변경. 다음 유효 작업은 **공식 PNG↔Local ID/TileZed 매핑 검증과 A/B/C/D 실제 정체 시각 판독**; 미검증 인접 격자 재조립을 반복하지 말 것.

## 최신 v130 — 같은 B 위치의 다른 A 후보 D 재조립 319종, 보류 1종 (2026-10-27)

- **GitHub PR #87 / Actions 40445486110 SUCCESS**. v120 인덱스 **800~1119**, 신규 320종에서 v127 기존 후보를 원본 B의 같은 TMX·층·레이어·좌표에 치환해 비교. **실제 대체 D 이미지 319종**, **후보 없어서 보류 1종**: floors_interior_tilesandwood_01/Local ID 74.
- **B와 대체 D 픽셀 변화 291종**, 변화 없는 28종(보류 제외); 원본 B−C 차이 0은 36종(투명 아님). 후보 319종은 **모두 인접 격자 크롭**이며 **다른 Local ID의 완전히 다른 물체일 수 있다**. 공식 동일 타일 대체 A 인증·TileZed·정체 확정 **모두 0**.
- **실제 시각 점검**: 8장 시트 중 00,03,07의 3장만 모델 직접 열람. 싱크대·창틀·바닥·산업설비 중 다른 사물로 대체되는 예가 보여 그리드 후보 사용이 올바른 Local ID 대응을 증명하지 못함. 320종 개별 AI 검수 완료 아님.
- 결과 위치 **review/v130_D_alt_A_B_320/**: D_ALTERNATIVE_A_B_320.csv (320행), D_CANDIDATE_SEARCH_320.csv (2,016행), D_ALT_A_B_SCENES_320.zip, 8 JPG 시트, QUALITY_AUDIT.md, MANIFEST.json.
- **최신 물리 DB v130**: analysis/current/v130/MANIFEST.json, 복원 scripts/restore_unified_v130.py. SHA-256 **73a06594cb06b955afe2da211d16467df94756867ce4c51ba8531e921bc1f2d6**, 부모 v129 191테이블 완전 보존+신규 v130_alt_A_B_320 320행, 총 **192테이블**, SQLite integrity_check PASS.
- D의 최신 정의는 **다른 A 이미지 후보를 동일 타일의 원래 B 위치에 넣어 재조립**. v124의 다른 TMX 두 번째 위치는 역사적 보조 인덱스이며 현 D 완료 계산 대상 아님.
- 인접 후보 실험 누계 **799종**(v126 160 + v129 320 + v130 319). v128의 다른 동명 PNG 3종까지 별도 합산하면 802종 **실험 이미지**. v127 인접 후보 키 가운데 **3,829종 재조립 미실행**. 어떤 것도 공식 매핑 인증이 아님.
- 과거 기존 5,409종, 사용자 수동 검수80, 제외14, 원본 PNG/TMX, 모든 과거 SQLite 테이블 유지. **개별 시각 관찰 누계 5,580/10,042종, 정체 인증 0**. 다음은 v131 1120~1439 구간 후보 검증 및 공식 Local ID 대조.

## 최신 v129 — v127의 미검증 A 후보로 원래 B 장면 320종 실제 재조립 (2026-10-27)

- **실제 실행 완료**: GitHub Actions `40442474302` PASS, PR #85 main 병합. 기존 B 원본 TMX의 동일 좌표, 층, 레이어, raw GID **하나만** 대체 A 이미지로 바꿔 새로운 D 장면을 **320종** 만들었다 (v120 인덱스 480~799). 실제 증거 CSV 320행, 후보 감사 2,113행, 접촉시트 8장, 이미지 ZIP, 매니페스트 및 물리 SQLite.
- 원본 B ↔ 대체 D 변화 **316종**, 변화 0 **4종**. 원래 B−C 변화 0은 **9종**으로 투명 확정 금지.
- **주의: 이번 320종의 A 후보는 모두 v127에 기록된 인접 격자 위치**다. **다른 Local ID 이미지일 수 있으므로 공식 '같은 타일의 다른 A'로 인증 0종**, TileZed 인증0, 최종 정체 인증0. 접촉시트 검수 결과 실제로 서로 다른 물체 모양이 섞인 사례 확인. 실험적 재조립 완료와 대응이 맞는 D 완료를 구분한다.
- 기존 실험 v126의 인접 후보 160종을 포함하면 인접 격자 가설 실험 총 **480종**, v128에서 별도 동명 PNG 이미지 3종 재조립. v127 전체 인접 후보만 있는 키 4,628종 중 남은 실험 미실행 **4,148종**. 미확보 PNG1, 다른 후보 없음1 보류.
- **최신 물리 통합 SQLite v129**: `analysis/current/v129/MANIFEST.json`, SHA-256 `9bd69e864d1f378caf2f9fe550a15d770062c5e786c1365505c91b8c1f7a473d`. 부모 v128 190개 테이블 보존 + 새 `v129_alt_A_B_320` 320행 추가, integrity_check=ok. 원본 PNG/TMX, 기존 5,409, 수동 검수80, 사용자 제외14 영구 보존.
- 개별 시각 정체 관찰 **5,580/10,042** 그대로. 새 이미지 생성만으로 판독/정체 인증 추가하지 않는다. 상세 파일: `review/v129_D_alt_A_B_320/QUALITY_AUDIT.md`.


## 최신 v128 — 다른 원본 PNG A 후보를 원래 B 장면에서 재조립 (2026-10-27)

- 사용자 정의 D: **같은 (tile_set_name, local_id)에 해당할 수 있는 다른 A 원본 이미지를 찾고, 원래 B의 동일 TMX 좌표/레이어에서 대상 GID 이미지 하나만 교체해 5×5 장면을 재조립한다.** v124 두 번째 TMX 사용 위치는 별도 역사적 데이터이며, 인접 격자 다른 ID 크롭은 검증된 D로 승격 금지.
- **v128 PR #83**, Actions **40440952240 PASS**: v127 전수 검색에서 발견한 다른 PNG 원본 변형 3종 `vegetation_foliage_01/{0,1,3}`의 A 대체 크롭을 각 원래 B 장면에 대입해 **D 3종** 실제 생성. B↔D 변화 픽셀: 2,725 / 5,561 / 6,585. 같은 TMX 타일 GID 딱 하나만 교체했으며 인접 다른 Local ID를 사용하지 않았음.
- 결과: `review/v128_D_alt_PNG_3/D_SAME_B_COMPARE_3.jpg` (육안 검수), `D_SAME_B_VARIANT_3.zip` (원본 A·대체 A·B·C·D·절대차 PNG 18개), `D_ALT_SOURCE_B_COMPARE_3.csv`, `QUALITY_AUDIT.md`, `MANIFEST.json`.
- **최신 물리 통합 DB v128** `analysis/current/v128/MANIFEST.json`. v127 부모 SQLite **189개 테이블 보존 + 새 v128 테이블 3행**. SHA-256 `4c37f22293d1e2914f2a7b56157dd31dea2dc5908438ddc9c63607a88488004d` / `PRAGMA integrity_check = ok`. 복원 스크립트 `scripts/restore_unified_v128.py`.
- 현재 원본 다른 PNG 파일 후보 3종은 모두 B 재조립 완료했지만, **공식 PNG/TMX Local ID·TileZed 대응 및 최종 정체 인증은 0**. A1/A2/A3 다른 같은 키 크롭 0종. v127의 30,249개 이웃 격자는 **다른 타일일 수 있는 미검증 가설**이며 동일 타일 후보로 계산하지 않는다.
- 기존 5,409종·수동 검수80·제외14·원본 Tiles/TMX·과거 DB 보존. 새 시각 정체 관찰 수 추가 0, 전체 확장 고유 관찰 **5,580/10,042종 유지**. 다음은 실제 Local ID 그리드/타일 정의/멀티타일 연결의 추가 증거 확보 후 나머지 D 후보를 검증하는 단계다.


## v127 전체 D 후보 전수 검색 결과 (2026-10-27) — 최신 우선

- **D 의미**: **같은 타일 Local ID의 대체 A 이미지를 탐색한 뒤, 동일 TMX 원래 B 5×5 위치에서 후보를 치환해 비교**한다. 과거 v124의 '다른 TMX 위치' 색인은 별도 보조 기록이다.
- 원본 신규 4,633종 전수 검색(원본 PNG 확보 4,632 / 미확보 1). A1/A2/A3에서 **비동일한 보이는 별도 같은키 크롭은 0**. *다른 동명 PNG 파일* 대체 후보 3종, 단순 인접 격자 **30,249개**, 이웃 후보만 발견된 키 4,628. 다른 후보 없는 키 1, 미확보 1.
- 후보 검색 기록 50,955행, 이미지 증거 프리뷰 4,631장, 접촉시트 58장, CSV 및 SQLite v127 매니페스트: `review/v127_D_A_candidates_full4633/MANIFEST.json`, `analysis/current/v127/MANIFEST.json`.
- **중요: 인접 격자 후보는 다른 Local ID일 수 있고, 동일 타일 대응이 검증된 후보가 아니다**. 동명 PNG 3종조차 실제 타일 키 정합은 아직 미인증이며 시각 품질·B 재조립 추가 검증 필요. 이번 단계 새 B/D 이미지 재조립 0종, 직접 정체 관찰 추가 0종, 최종 인증 0종.
- SQLite 부모 v126의 188개 테이블을 그대로 보존하고 새 후보 목록 4,633행 추가. 과거 5,409·사용자 수동80·제외14·PNG/TMX·이전 DB 보존. 기존 관찰 누계는 5,580/10,042 그대로.


# D 단계 의미 정정 및 v126 실제 작업 (2026-10-27)

**사용자 지정 D는 같은 타일(Local ID)에 대해 다른 A 이미지 후보를 찾고, 그 후보로 기존 B의 원본 TMX 좌표에서 주변 5x5 이미지를 다시 조립하는 작업이다.** 과거 문서의 'D=다른 TMX 위치'는 v124에서 끝난 별도 보조 색인으로 보존하되, 향후 D 단계 완료 수에 합산하지 않는다.

- v126 PR #80 main 병합, GitHub Actions #40438258305 PASS. 신규 160종(v120 인덱스 320~479), A 후보 검색 1,120건, 동일 위치 대체 B 160장, 5패널 검수 시트 4장, 증거 ZIP/CSV, 물리 SQLite v126 (과거 187 테이블 보존+160행).
- **중요:** A1/A2 별개로 다른 유효한 원본 후보는 0건. 160종 모두 같은 PNG의 인접 격자 크롭을 이용한 '대응 미확인 후보 가설'이다. 이런 크롭은 다른 Local ID일 수 있어 정체 확정 금지. 기존 B와 달라진 장면 156, 변화 없는 장면 4, B−C 변화0 8.
- 개별 실제 물체 정체 인증 0, PNG/TMX 대응 인증 0, TileZed 인증 0. 품질 확인 파일: `review/v126_D_alt_A_B_160/QUALITY_AUDIT.md`.
- 시각 관찰 지표는 v125까지 기존5,400+신규180=5,580/10,042. v126는 렌더만 했으므로 관찰 수 추가 없음. 원본 PNG/TMX·기존5,409·사용자 수동80·사용자 제외14·과거 SQLite 모두 보존.
- v126 물리 DB SHA-256: `449124bef8c2bfd381c887d523f28b57d9d58ce4a0a066712862871adb262e4e`. 아래 v124/v122 항목은 과거 기록이다.



## 현재 최신 작업 기준 — v124 (2026-10-27)

- **PR #76 병합 / GitHub Actions 40431836972 PASS**: v120 신규 4,632종 가운데 인덱스 160~319인 **160종**의 실제 A/B/C/D 증거 4장·이미지 내장 HTML·CSV·ZIP 생성. 다른 실제 D 위치 88종, D 없음 72종, B−C 변화 0은 4종. 새 타일을 개별 이미지 정체 관찰 완료로 자동 승격하지 않음. 기존 v122의 184테이블 보존 후 v123 증거 테이블 160행 추가. \`review/v123_ABCD_next160/\`, \`analysis/current/v123/\`.
- **PR #77 병합 / GitHub Actions 40433208887 PASS**: 그 뒤 전체 남은 **4,472종**의 실제 TMX D 사용 위치 전수 색인. 84개 원본 TMX의 첫 위치 4,472/4,472 검증, D 실배치 2,791종, 다른 배치 없음 1,681종, 이 중 D가 5×5 가장자리 안에 있는 2,756종. v123의 160개 위치 결과 전부 일치. \`review/v124_D_locations_new4472/D_REAL_PLACEMENTS_4472.csv\`.
- v124는 **D 좌표만** 4,472건 기록했으며 해당 전수 D 이미지 4,472개를 조립한 것이 아니다. **A/B/C/D 이미지 증거가 있는 신규 대상은 누적 320/4,632종**, 그 중 실제 D가 존재하여 이미지가 생성된 것은 106+88=194종. 다른 4,312종은 ABCD 개별 이미지 미생성.
- 최신 물리 통합 SQLite: \`analysis/current/v124/MANIFEST.json\`, \`python3 scripts/restore_unified_v124.py /tmp/pz_latest.sqlite\`. SQLite SHA-256 \`d49ba09177b8cf393ecc6c61415ddf711e9703d244727130883f4756a337c2c4\`. 기존 185개 테이블 보존 후 \`v124_d_placement_4472\` 4,472행 추가, integrity_check = ok.
- **시각 관찰 누적 지표는 v122와 같음**: 확장 10,042 중 5,560종 시각 관찰, 원래 5,409 중 5,400종 관찰, 신규 4,633 중 160종 관찰, 전체 미관찰 4,482종. 잠정 144/보류 16은 v122 기준이며, v123/v124에서 추가로 판독한 160종이라고 혼동 금지.
- C B−C 0 215종은 투명 인증 금지. PNG/TMX Local ID·TileZed·최종 정체 인증 모두 0. 원본 PNG·TMX와 기존 5,409종, 수동 검수 80종, 사용자 제외 14종 영구 보존.

## v122 이전 직접 판독 기록 (2026-10-27)
이 문서의 아래 **v113~v120 절은 역사적 시점 기록**이다. 최신 실작업 상태는 `PROJECT_STATE.json`과 여기의 v122 수치를 우선한다.

- 원래 31_45/31_46 TMX 기준 **고유 5,409종·관찰 5,400종·미관찰 9종**은 변경하지 않았다. 과거 사용자 제외 8종과 추가 제외 6종(총 14종), 수동 검수 80종, 감사 가능한 잠정 후보 4,512종, v115 독립 계열 후보 882종 모두 보존.
- 84개 TMX 확장 범위 10,042종 = 기존 5,409종 + 신규 4,633종. 신규 A 확보 4,632종, PNG 미확보 1종 보류 `overlay_graffiti_wall_02/2`.
- v120 B 5×5 주변 장면 **4,632종**. v121 C에서 TMX 동일 원본 위치·레이어의 **GID 1개만 제거한 4,632종** (B−C 변화 **4,417종**, 변화 0 **215종**). SHA/ZIP CRC 통과, 58 검수 접촉시트. `review/v121_C_diff_new4632/`.
- v121의 첫 160종 A/B/C/D 실제 증거 생성: 둘째 실제 TMX 사용 위치 D **106종**, D 없음 **54종**, B−C 변화 0 9종, 검수 접촉시트 4장과 **이미지 내장 HTML**, CSV, 증거 ZIP. `review/v121_ABCD_first160/`.
- **v122 신규 160종 직접 이미지 판독**: 4개 접촉시트 전부 실제 모델 화면으로 열람. **잠정 후보 144종**, **보류 16종**(B−C 0인 9종 포함). 개별 특징/부품 역할/확신도를 `review/v122_AI_ABCD_160/AI_VISUAL_REVIEW_160.csv` 및 별도 SQLite 테이블에 분리 기록. 신규 미관찰 4,473종.
- **확장 범위 고유 관찰 5,560 / 10,042종(55.37%)**, 남은 미관찰 **4,482종** = 기존 9 + 신규 4,473. 최초 5,409범위 관찰 99.83%와 분모 혼동 금지.
- 최신 물리 통합 SQLite: `analysis/current/v122/`, `python3 scripts/restore_unified_v122.py /tmp/pz_latest.sqlite`; SHA-256 `abe9d410c4fb6dd4e86c19170831d00b60424270777f9155f79b9091d33c780d`. **기존 183 테이블 보존** 후 신규 `v122_ai_visual_review_160` 추가, SHA-256·PRAGMA integrity_check·중복 키·ZIP CRC **PASS** (GitHub Actions: https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40429858475).
- GitHub 반영 PR: **#73 전체 C**, **#74 160종 A/B/C/D**, **#75 신규 160종 직접 판독·SQLite** 모두 main 병합. 마지막 공식 PNG−TMX Local ID 인증, TileZed 렌더 인증, 최종 정체 인증 **0종**.
- 다음 작업: 신규 미관찰 4,473종을 우선하며, 새 160종의 낮은 확신도 후보도 독립 검증. 고유 키 중복 합산, 과거 제외 대상 재분류 및 이미지 생성만으로 관찰 승격 금지.

> GitHub 기준일: 2026-10-26. **이 문서는 PROJECT_STATE.json에서 자동 생성됩니다.**

## 최우선 목표

이름 추측이 아닌 **원본 PNG의 실제 이미지**를 TMX 주변 5×5 타일과 조립해 관찰하고, 분할된 사물의 부품 역할과 오염·벽·지붕·가구 구성 요소를 구별한다. A=원본, B=조립, C=선택 배치 제거, D=다른 위치. TileZed와의 정합 검증 없이 확정 금지.

## 기준 범위

- TMX 원본: 31_45(2).tmx, 31_46(2).tmx
- TMX 고유 사용 타일: **5,409종**, 전체 배치 302,177건.

## 실제 원본 SQLite로 중복 제거 완료 (v47)

| 범위 | 수량 |
|---|---:|
| v36 기존 이미지 관찰 | **2,509종** |
| v37~v46 별도 기록 | **477종** |
| 두 계보의 중복 키 | **402종** |
| v37~v46 중 진짜 신규 | **75종** |
| **통합 이미지 관찰** | **2,584종 / 5,409종 (47.77%)** |
| 미관찰 | **2,825종** |
| 최종 정체 인증 | **0종** |

두 실제 DB에서 (tile_set_locator, local_id) 합집합을 계산해 **2,584종**으로 검증 완료. 보고 수치 2,986을 그대로 합하지 않는다.

## 잠정 후보 수량 주의

- v36의 과거 문서 보고: 2,291종; v36 시각 증거 테이블에서 실제 키와 후보를 재검증한 수: **2,156종**. 차이 135종은 보고 및 증거 키 간 불일치로 남긴다.
- v46 직접 확인 후보: **402종**.
- 감사 가능한 잠정 후보 키 합집합: **2,302종**. **정체 확정 수가 아니다.**
- 두 기록이 다른 단어로 후보를 표시한 동일 키 **256종**: 두 가설 모두 보존, 이미지 재검토 전 자동 병합 불가.

## 원본 DB와 재현

- GitHub 복구 스크립트: `python3 scripts/restore_source_databases.py /tmp/pz_originals`
- 이 스크립트가 `analysis/archive/v36/`, `analysis/archive/v46/`의 분할 파일을 읽고 SHA-256 검증 뒤 두 원본 SQLite를 복원한다.
- 병합 경량 SQLite 복원: `python3 scripts/restore_merged_evidence.py /tmp/pz_merged.sqlite`
- 통합 표: `analysis/imports/merged_catalog_5409.csv`
- 상세 증거·후보 충돌: `analysis/imports/all_observation_records.csv`, `analysis/imports/conflicting_candidates.csv`
- SQL 원본·CSV·증거를 혼동하지 말 것. 경량 병합 DB는 모든 과거 보조 테이블을 복제한 원본 DB가 아니다.

## 최신 물리 통합 SQLite (v113)

- **v36·v46 원본 테이블 + v47 병합 색인 + v48부터 v113까지의 모든 신규 체크포인트**를 한 SQLite에서 조회할 수 있습니다.
- 단일 테이블 `tile_catalog`: **5,400/5,409종 (99.83%)**, 미관찰 9종, 잠정 후보 4,512종, 최종 인증 0종.
- SHA-256 검증과 전체 복원 방법: `analysis/current/v113/MANIFEST.json`, `scripts/restore_unified_v113.py`.
- 과거 DB는 별도 보존합니다. 최신 체크포인트 이미지의 GitHub 보관 여부: **보관됨**. 이전 버전의 로컬 보조 이미지·메타데이터는 각 버전 안내를 따릅니다.

## 최신 체크포인트 (v113)

- 새로 직접 관찰: **0종** (잠정 후보 0, 보류 0).
- 중복 제거 누적 관찰: **5,400/5,409종 (99.83%)**.
- 아직 미관찰: **9종**. 최종 인증 0종.
- 기록: `checkpoints/v113/user_review.csv` (이전 통합 DB와 별도로 보존).

## 다음 실제 작업

1. v113부터 신규 검수 대상은 analysis_queue 대신 v113_active_review_queue를 사용한다. 사용자가 8종을 활성 검수에서 제외했으며 과거 타일 키와 출처는 보존한다.
2. 남은 활성 f_bushes_1/66은 사용자 잠정 후보 풀 또는 꽃 계열 식물. 원본 A 알파 4,837픽셀이나 B-C 변화 0이므로 공식 Local ID·TileZed 정합 전 정체 확정 금지.
3. 제외 8종 중 사무실 3종은 잠정 크롭 투명, JUMBO 3종은 매핑 불확실한 빈 크롭, PNG 미확보 2종은 실제 투명 여부 미검증.
4. v36~v111 과거 DB 테이블·사용자 수동 검수 80종·PNG/TMX 원본은 삭제 또는 수정하지 않는다.

## 최신 v115 AI 실제 판독 결과 (2026-10-26)

- 기존 5,400종 이미지 관찰 중 정체 후보 미기록 888종을 A1/A2/B/C/D 74장으로 모델이 직접 재검토.
- 새 시각 후보 **882종(870 low/12 medium)**, 원본 문제로 보류 **6종**. 모두 시각적 계열·부품 *잠정 후보*이며 정체 완결 인증 아님. 기존 감사 가능 후보 **4,512종**은 변경 없음.
- 15×15 확대 **8종**의 전신주·가공 전선·통신 설비 B/C 비교. `appliances_com_01/3`은 전화·무전 통신기 형태 후보이며 가려진 대상. `appliances_com_01/96` 등은 전선 선분으로 잠정 식별.
- 실제 파일: `review/v115_ai_identity/AI_VISUAL_REVIEW_888.csv`, `review/v115_model_visual/`, `review/v115_extended_context/`, `docs/V115_AI_VISUAL_REVIEW_888.md`.
- 최신 통합 SQLite: `analysis/current/v115/MANIFEST.json` SHA-256 `4f0f0679c85d18a2ac87d440a0c41f9708348b0004e1efe231410e7f99ffae20`. 복원: `python3 scripts/restore_unified_v115.py /tmp/pz_latest.sqlite`. v115 별도 테이블에 888종 기록. 기존 관찰 5,400/5,409, 과거 후보 4,512, 미관찰 9, 사용자 제외 8, 최종 인증 0 보존.
- **주의:** 882개 전부 세부 정체를 최종 확정한 상태가 아니고 Local ID 공식 매핑·TileZed 검증은 0종. 특정 마크 블록에 자동 배정 금지.

## 최신 v116: 이미지 근거 미확보 6종 활성 제외 (2026-10-26)

- 사용자 요청에 따라 v115의 소스 이미지/격자 문제 보류 6종을 **추가 분석·재검수 대상에서 제외**했다. 기존 보류 이력 및 검수판은 그대로 보존한다.
- 이전 `v115_ai_held_queue`는 기록상 **6종**, 최신 `v116_active_v115_held_queue`는 **0종**이다. 이미지가 확인된 AI 잠정 후보 882종은 변경 없음.
- 이번 6종은 v113 이전 미관찰 사용자 제외 8종과 **서로 다른 작업 대기열의 제외**다. 과거 관찰 5,400종과 기존 감사 후보 4,512종, 최종 인증 0종도 불변.
- 최신 통합 DB 복원: `python3 scripts/restore_unified_v116.py /tmp/pz_latest.sqlite`. `analysis/current/v116/MANIFEST.json`, `checkpoints/v116/user_exclude_six.csv`, `docs/V116_USER_EXCLUDED_NO_IMAGES.md` 참조.
- **주의:** PNG 이미지가 없거나 Local ID가 불명확하다는 이유로 타일의 투명성·부재를 확정한 것은 아니다.

## v117: 84개 TMX 고유 타일 10,042종 A 후보 사전 구축 (2026-10-26)

- 이전 5,409종에 신규 **4,633종**을 더한 범위 10,042종 전체 키를 실물 PNG의 A1(TMX)·A2(TileZed)로 대조하여 **126장 A 접촉시트**와 가시성·원본 SHA 포함 CSV 작성.
- TMX/TileZed 후보 일치 **3,326종**, 단일 가시 후보 **6,673종**. 일반 타일 규격이 적용되지 않는 JUMBO/XL/XXL/그루터기 **36종**의 A3 가시 후보도 *추가 생성*.
- 총 **10,035종 가시 A 후보** 확보. 나머지 **7종 미해결(원본 PNG 이름 미확보 3, 빈 후보 크롭 4)**. 사용자 제외 14종 별도 유지. A 후보 생성은 공식 Local ID 검증 또는 정체 확정이 아님.
- 주 파일: `review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv`, `review/v117_A_candidates_10042/A_CANDIDATE_REVIEW_INDEX.html`, `review/v117_A_candidates_10042/sheets/`, `review/v117_A_candidates_10042/jumbo_a3/`.
- **최신 실제 SQLite는 아직 v116** (기존 데이터 불변). `PROJECT_STATE.json.latest_a_candidate_stage`가 최신 A 준비작업을 추적한다. 공식 매핑/최종 인증 0.
## 최신 v118: 기존 5,409종 제외 → 신규 4,633종만 A단계 (2026-10-26)

- 사용자가 기존에 분석한 5,409종을 신규 A단계에서 제외하도록 지시. 전체 10,042종에서 신규 **4,633종만** 남겼다. 기존 결과는 삭제하지 않고 재사용한다.
- `review/v118_A_new_only_4633/A_CANDIDATE_NEW_ONLY_4633.csv` 정확히 4,633키와 58장 압축 검수 시트를 생성. 기존 키·사용자 제외 14종의 유입 0건 검사 PASS.
- 신규 A1=A2 **1,544종**, 단일 가시 **3,068종**, JUMBO 잠정 A3 **20종**, 정확한 PNG 미확보 **1종(`overlay_graffiti_wall_02/2`)**. 가시 A 후보 **4,632종**.
- 검토 HTML·ZIP과 매니페스트는 `review/v118_A_new_only_4633/`. ZIP CRC PASS, 63개 항목. 정확한 이미지 Local ID 공식 매핑과 정체 최종 인증은 0이며, 후보 미확보를 투명 확정으로 처리하지 않음.
- 최신 실제 통합 SQLite는 **v116 불변**. `PROJECT_STATE.json.latest_active_a_scope`만 새 A 작업 대상으로 갱신. 이후 A 검증·B/C/D 분석은 반드시 신규 4,633키 대상으로만 진행.

## 최신 v119: 신규 대표 A 4,632종 실제 이미지 및 SHA (2026-10-26)

- 새 키 4,633 중 4,632종의 원본 알파 포함 대표 A PNG를 생성해 10개 ZIP으로 보관. A1 1,544종, A2 3,068종, JUMBO A3 20종. overlay_graffiti_wall_02/2 한 종 보류.
- 개별 출처/크롭 좌표/바이트 SHA/알파/ZIP 참조: review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv. 58장 검수판 sheets/SELECTED_A_000.jpg..057.jpg. 10개 ZIP CRC 및 4,632개 PNG 이미지-원본 RGBA 픽셀 SHA 전수 확인 통과.
- 기존 5,409키·사용자 제외 14종·기존 v116 SQLite 모두 수정하지 않았다. PROJECT_STATE.json.latest_selected_A_stage 참고.
- 이것은 **잠정 대표 이미지 배정**이다. 실제 PNG와 TMX Local ID의 공식 일치 검증 및 개별 AI/TileZed 인증 0종. JUMBO A3 프레임 혼합 가능성이 남는다.

## 최신 v120: 신규 4,632종 B 주변 장면 실제 생성 (2026-10-27)

- v119 A를 선택한 신규 **4,632키**, 전체 **84개 원본 TMX**에서 실배치 `tmx, level, layer_index, x, y, raw_gid` 확인 및 5×5 같은 층의 아이소메트릭 B 조립 **4,632건**. 기존 5,409키를 새 정체 분석 대상으로 추가하지 않는다.
- `review/v120_B_context_new4632/B_CONTEXT_4632.csv`, `PLACEMENTS_4632.csv`, `sheets/` 58접촉시트, `b_png_shards/` 12 WebP ZIP, `B_CONTEXT_4632_BROWSER.html` 오프라인 검색/2배 확대. 전수 ZIP CRC·WebP/선택 원본 SHA 검증 PASS.
- 품질: 이웃 스프라이트 누락 B **8건**(드로잉 9건), 지도의 끝에서 잘림 **48건**, 개별 스프라이트 그리기 캔버스 잘림 **23,823회**. B는 실배치 기반 **근사 렌더**이며 TileZed 공식 결과 아님.
- 현재 실제 SQLite **v116**, 이전 A **v119** 그대로. C(대상 하나 제거)와 D(다른 위치)는 미생성. `PROJECT_STATE.json.latest_B_context_stage` 참조. 1개 A 원본 미확보 보류, 사용자 제외 기존 14 유지, Local ID/정체 인증 모두 0.

## 불변 원칙

- 이미지 직접 관찰, 추론 후보, PNG-TMX Local ID 검증, TileZed 렌더 검증, 최종 인증을 분리한다.
- 역사적 v31 AI 분류를 증거로 삼지 않는다.
- 기존 `Tiles/`와 `B4220.3_MapExport_256/`의 원본은 절대로 수정하지 않는다.
- 모든 작업 종료마다 PROJECT_STATE.json과 checkpoints/를 기록하고 GitHub Actions 검증 결과를 확인한다.
