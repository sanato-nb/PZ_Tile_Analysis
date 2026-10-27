# 좀보이드 B42 타일 정체 분석 — 중앙 AI 작업 지침 (버전별 기록 · 현재 상태는 PROJECT_STATE.json)

## v146 식당·주유소·소매 상점 A/B/C 실제 이미지 관찰 (2026-10-27)

- 원본 A/B/C 접촉시트 1840~1999 총 160개 직접 검토; PNG 픽셀·원래 TMX GID/좌표/층/레이어, C 제거 및 B-C SHA 검증 통과 **155종**만 provisional_candidate, **5종**은 B-C=0·이웃 누락·지도 경계 등으로 신규 완료 계산 제외.
- 전체 84 TMX 고유 10,042종에서 **7209종 관찰 기록 (71.79%)**, 미관찰 **2833종**. 공식 Local ID↔PNG/TileZed·정체 최종 인증 각 0. 준비된 ABCD 증거는 정체 완료가 아님.
- 물리 SQLite analysis/current/v146/MANIFEST.json, SHA e7b053d9b5281f530e16e9bd41dd9e6f2e6f3d08c3cb2bc3a9c27ac0e23d45c1, **208개 테이블**(v145 이전 207테이블과 전체 기존 행 수 보존, 신규 155행 1테이블). PRAGMA integrity_check=ok. 증거 review/v146_abc_1840_1999 에 CSV·PNG ZIP·접촉시트·예외표 저장.
- 기존 수동80·사용자 제외14·기존5409, 사용자 held D2/JUMBO20, 원본 PNG/TMX 및 과거 DB 불변. D 다른 A 동일 TMX 위치/층/레이어 공식 매핑 미검증, 인접격자 및 두 번째 TMX 위치는 인증 근거 아님.

---
## v145 군용시설·식당 A/B/C 실제 이미지 관찰 (2026-10-27)

- 원본 A/B/C 접촉시트 1680~1839 총 160개 직접 검토; PNG 픽셀·원래 TMX GID/좌표/층/레이어, C 제거 및 B-C SHA 검증 통과 **153종**만 provisional_candidate, **7종**은 B-C=0·이웃 누락·지도 경계 등으로 신규 완료 계산 제외.
- 전체 84 TMX 고유 10,042종에서 **7054종 관찰 기록 (70.24%)**, 미관찰 **2988종**. 공식 Local ID↔PNG/TileZed·정체 최종 인증 각 0. 준비된 ABCD 증거는 정체 완료가 아님.
- 물리 SQLite analysis/current/v145/MANIFEST.json, SHA 4c045c742bf4f5b62dae66b8f2a8a42d35f8a364d7d23b46ada65643736e7d13, **207개 테이블**(v144 이전 206테이블과 전체 기존 행 수 보존, 신규 153행 1테이블). PRAGMA integrity_check=ok. 증거 review/v145_abc_1680_1839 에 CSV·PNG ZIP·접촉시트·예외표 저장.
- 기존 수동80·사용자 제외14·기존5409, 사용자 held D2/JUMBO20, 원본 PNG/TMX 및 과거 DB 불변. D 다른 A 동일 TMX 위치/층/레이어 공식 매핑 미검증, 인접격자 및 두 번째 TMX 위치는 인증 근거 아님.

---
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



## 현재 최신 v124 인수인계 (2026-10-27) — 우선

- v123은 신규 160종(인덱스 160..319) A/B/C/D 실제 이미지 증거 생성 완료, 실제 D 88종·D 미존재 72종·B−C 0은 4종. v121 첫 160종을 포함해 ABCD 이미지는 총 **320/4,632종**. v123 이미지 생성만으로 신규 시각 관찰 증가 **0종**. [PR #76](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/76).
- v124는 남은 신규 **4,472종 전체**에서 원본 84 TMX의 진짜 D 두 번째 위치 색인 완료(2,791개 존재, 1,681개 미발견). 실배치 D **좌표 목록**이고 4,472개 D 이미지 조립/판독이 아님. v123 기존 160종과 160/160 일치. [PR #77](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/77).
- 최신 물리 SQLite v124 \`analysis/current/v124/MANIFEST.json\`, \`scripts/restore_unified_v124.py\` 로 복원. SHA-256 \`d49ba09177b8cf393ecc6c61415ddf711e9703d244727130883f4756a337c2c4\`. 이전 185테이블 그대로 보존 후 D 좌표 색인 4,472행 추가. 구 버전으로 되돌리거나 덮어쓰기 금지.
- **실제 이미지 시각 관찰 공식 누계는 v122 그대로**: 신규 160종, 잠정 144·보류 16, 원래 5,409 대상 기존 관찰 5,400, 전체 5,560/10,042. D 좌표 생성은 시각 관찰로 계산 금지.
- 다음 순서: 기존 v121/v123 ABCD 증거와 v124 D 실배치 색인을 결합해 **추가 4,312종**의 D 이미지 조립 및 실제 시각 판독. D 부재는 없는 것으로 남기고 B−C 0의 215종 투명 확정 금지. PNG/TMX Local ID·TileZed·최종 정체 인증 0종; 사용자 수동 80종·제외 14종·원본 PNG/TMX·기존 5,409종 모두 보존.

## v122 시각 관찰 이전 체크포인트 (2026-10-27)
- 최신 **물리 통합 SQLite v122**: `analysis/current/v122/MANIFEST.json`, 복원 `python3 scripts/restore_unified_v122.py /tmp/pz_latest.sqlite`. v121 물리 원본의 기존 **183개 테이블**(v116 이전 182 + v121 하나)을 전부 보존하고 `v122_ai_visual_review_160`만 추가. SHA-256 `abe9d410c4fb6dd4e86c19170831d00b60424270777f9155f79b9091d33c780d`. PRAGMA integrity_check/CSV 키 중복/증거 ZIP CRC PASS (GitHub Actions 40429858475).
- **84개 TMX 확장 범위 고유 10,042종** 중 기존 **5,409종**, 신규 **4,633종**. 과거 기존 관찰은 **5,400/5,409종**, 기존 미관찰 9종(사용자 8종 제외·활성 1종)으로 그대로. 새 **160종**의 A/B/C/D 실제 접촉시트 **4장 직접 이미지 관찰**, 잠정 물체·부품 후보 **144종**, 보류 **16종**(B−C 0인 9종 포함). 고유 관찰 **5,560/10,042종(55.37%)**, 미관찰 **4,482종**(기존 9+신규 4,473). 후보는 정체 최종 인증이 아니다.
- v121의 신규 **4,632종 B/C 전체**: B 원본 바이트 일치 4,632, 원본 GID 하나만 제거한 C 4,632, B−C 변화 4,417 / 변화 0 215, 58개 접촉시트와 24개 증거 ZIP SHA/CRC PASS. 기록 `review/v121_C_diff_new4632/` (PR #73).
- v121 A/B/C/D 160종: 84개 TMX 실제 **다른 사용 위치 D 106종**, 둘째 위치 없는 **54종**, B−C 변화 0인 표본 9종. `review/v121_ABCD_first160/`의 CSV·이미지 내장 HTML·4장 접촉시트·증거 ZIP. `analysis/current/v121/` 물리 DB 보존 (PR #74).
- v122 신규 시각 판독 CSV `review/v122_AI_ABCD_160/AI_VISUAL_REVIEW_160.csv`, 보고서/증거 ZIP, DB `v122_ai_visual_review_160` (PR #75). 출처가 서로 다른 4개 접촉시트를 모델 화면으로 모두 열어 보고, 보이는 외형/정체 후보/부품 역할/확신도를 분리. 공식 PNG−TMX Local ID 매핑·TileZed·최종 정체 인증 모두 **0종**. 기존 v36~v121·수동 검수 80종·사용자 제외 14종·원본 PNG/TMX 절대 변경 금지.
- 다음 목표: **신규 미관찰 4,473종**의 A/B/C/D 실제 장면을 계속 확장하며 시각 판독. 기존 사용자 제외를 자동 복구하지 말 것. `PROJECT_STATE.json.latest_checkpoint` 및 `unified_database` v122 최우선. 기존 아래 각 버전 메모는 역사적 기록이며 대기열 기준으로 사용하지 않는다.

## 목표 및 최신 검증 기준
- B42 TMX 두 개(저장소 파일 `B4220.3_MapExport_256/tmx/31_45.tmx`, `31_46.tmx`)에서 사용한 고유 **5,409종**, 기준 배치 **302,177건**을 원본 PNG와 실제 배치로 이해한다. 최초 이름 `31_45(2).tmx` / `31_46(2).tmx`과 저장소 이름의 동일성은 공식 인증 전까지 별개로 취급한다.
- 모든 작업은 `PROJECT_STATE.json`의 `unified_database` 및 `latest_checkpoint`를 우선한다. `reconciliation`의 2,584(v47)는 과거 교집합 대조 기준이다.
- 2026-10-26 **v115(888종 AI 직접 재검수 반영): 기존 이미지 관찰 5,400/5,409종(99.8336%). 이 가운데 기존 정체 후보 미기록 888종을 74장의 A1/A2/B/C/D 원본 접촉시트로 직접 판독해 새 시각 계열·부품 잠정 후보 882종(870 low, 12 medium) 및 원본 문제 6종 보류 기록. 기존 v113 감사 가능한 잠정 후보 4,512종은 변경 없이 보존. 공식 Local ID·TileZed·최종 인증 0종. 기존 미관찰 9종 중 사용자 검수 제외 8종, 활성 검수 1종도 보존**.
- 최신 물리 통합 SQLite: `analysis/current/v116/`. 복원: `python3 scripts/restore_unified_v116.py /tmp/pz_latest.sqlite`. 압축 분할 조각의 SHA-256·SQLite 무결성·이전 테이블 보존·누적 수량 검증을 거친다.
- `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 먼저 읽는다.

## 실제 이미지 시각 분석 규칙
1. 신규 원본 이미지 관찰은 최신 DB `v113_active_review_queue`에서 미관찰 키를 선택한다. 과거 이미지 관찰이 있지만 정체 후보 없던 888종의 결과는 `v115_ai_visual_review` 테이블로 **별도 보존**하며, 이미지 관찰 수에 다시 합산하거나 공식 인증으로 승격하지 않는다.
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

## v120 신규 4,632종 B단계 원본 TMX 주변 5×5 장면 생성 (2026-10-27)
- **신규 4,632키만 대상**. 26_43~37_49 범위 원본 TMX **84개 전부**를 실제 열고 원본 SHA-256을 기존 감사 보고서와 대조해 타일의 `tmx_file, level, source_layer_index, x, y, source_raw_gid`를 정확히 기록. 기존 5,409종은 신규 분석 대상에서 제외하고, 주변을 조립하는 경우에만 기존 v117 A 후보를 참조.
- `review/v120_B_context_new4632/B_CONTEXT_4632.csv`는 실제 배치 4,632건, 같은 층 주변 5×5 아이소메트릭 근사 B **4,632개**, 개별 WebP 파일 ZIP **12묶음**, 접촉시트 `sheets/B_5x5_000.jpg..057.jpg` 총 **58장**, 오프라인 `B_CONTEXT_4632_BROWSER.html` 검색/필터/2배 확대 기능. 모든 B ZIP SHA-256/CRC 및 WebP 4,632장 decode 검증 PASS.
- 원본 타일/이웃 A 이미지의 RGBA 픽셀 SHA를 기존 v119/v117과 비교했으며 원본 변조 없음. 실제 배치 좌표 마스터 `PLACEMENTS_4632.csv`; 검수 인덱스 `B_CONTEXT_4632.csv` SHA-256 `cb98b3826ca3b1e5ecb4daca96d91c88ae7c1c6240404429d4a7224e28eb14eb`.
- 품질 한계: **8개 B장면에 이웃 PNG 누락(누락 드로잉 9건)**, **48개는 TMX 맵 가장자리 5×5 잘림**, **23,823번의 개별 스프라이트 그리기가 B 캔버스 경계에서 잘림** (장면 수가 아님). 큰 나무/벽/전선에서 가림 또는 잘림이 생길 수 있으므로 원본 TileZed 렌더 완전 재현이라고 주장 금지.
- B는 대상 타일을 제거하지 않은 **실제 원본 배치 조립**. C 제거 비교와 D 다른 위치는 아직 만들지 않음. 공식 Local ID·TileZed 검증 및 최종 정체 인증 **0종**. 사용자 제외 14종 및 v116 SQLite 보존.
- 다음 C는 B와 완전히 동일한 TMX 좌표/레이어에서 **대상 타일 1개만 제거**하여 차이를 검증하고, 전선처럼 연결된 타일은 필요시 15×15 이상의 B/C 확대 근거를 추가한다.

## v119 신규 4,632종 대표 A 실제 배정 (2026-10-26)
- 기존 5,409키는 신규 A 분석에서 완전히 제외. 신규 4,633키 중 4,632키마다 *원본 PNG의 RGBA 크롭 픽셀이 실제로 존재하는 대표 A*를 선정했다. 원본 PNG/크롭 경계/투명 픽셀/선택 PNG SHA-256과 ZIP 내부 엔트리를 review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv에 모두 기록.
- A1=A2 가시 일치 1,544키는 대표 A1, 한쪽만 가시 3,068키는 대표 A2, JUMBO 잠정 프레임 격자 20키는 대표 A3로 지정. overlay_graffiti_wall_02/2 한 키는 정확한 PNG가 없어 보류(투명 확정 금지).
- 실제 RGBA 이미지 4,632장은 review/v119_selected_A_new4633/selected_png_shards/PZ_REP_A_00.zip부터 _09.zip까지 10개 ZIP에 저장. SHA/알파 픽셀 전수 검증, 10개 ZIP CRC PASS. 대표 A만 들어간 검수판 58장: sheets/SELECTED_A_000.jpg..057.jpg.
- 실제 사용된 원본 PNG 287개. 대표 A CSV SHA-256 b8e87f48800b4064872922428c1958d11cb9c9a9dc2e3f6900b6a68613a3e45d. PROJECT_STATE.json.latest_selected_A_stage=v119.
- 후보 이미지를 실제로 저장한 것은 공식 TMX Local ID 매핑 검증과 다르다. AI 개별 매핑/TileZed/최종 정체 인증 모두 0. JUMBO A3에는 다른 나무 프레임이 섞였을 수 있으므로 검증 시 우선 다룬다.
- 원본 PNG/TMX, 기존 5,409키/수동 제외 14종, 최신 v116 물리 통합 SQLite는 불변. 뒤따르는 B/C/D 작업은 신규 키만 v119 selected_shard/selected_zip_entry로 A를 로드한다.

## v118 A단계 활성 범위: 신규 4,633종만 (2026-10-26)
- **사용자 최종 범위 지시:** `26_43`~`37_49` TMX 범위의 **전체 10,042종 중 기존 5,409종은 반드시 신규 A 작업에서 제외**하고, 오직 **신규 4,633종**을 A 후보 선정/시각 검증 대상으로 처리한다. 기존 5,409종의 결과를 지우거나 신규 분석으로 재계상하지 않는다.
- 최신 A 활성 큐 CSV: `review/v118_A_new_only_4633/A_CANDIDATE_NEW_ONLY_4633.csv` **정확히 4,633행**, `prior_in_5409=0` 및 `user_excluded=0`만 포함. 오프라인 뷰어 `NEW_ONLY_A_4633_VIEWER.html`과 58장 `sheets/new_A_000.jpg..new_A_057.jpg`. ZIP `PZ_신규4633종_A후보_검토자료.zip` CRC PASS.
- 신규 4,633종 A 상태: A1=A2 동일 가시 **1,544종**; A1/A2 중 한쪽만 가시 **3,068종**; JUMBO A3 전용 잠정 **20종**; **원본 미확보 1종 `overlay_graffiti_wall_02 / Local ID 2`**. **4,632종 가시 후보**, 1종 미확정. 이름 없는 PNG를 투명 인증하거나 대체 PNG를 임의 채택하지 않는다.
- `PROJECT_STATE.json.latest_active_a_scope`에 별도 이력 저장. 이전 `latest_a_candidate_stage` v117 전체 10,042종 및 **v116 실제 통합 SQLite** 유지. 구분: 후보 자동 생성 4,632 != AI가 정확한 Local ID를 개별 검증한 4,632. 공식 매핑·최종 정체 인증 0.
- 과거 사용자 제외 14종은 모두 기존 5,409종에 있으며 신규 4,633종 대상에는 **0종** 포함. 기존 상태/증거 자체는 보존.

## v117 84개 TMX A 후보 전체 10,042종 (2026-10-26)

- **목표 범위:** `26_43.tmx`부터 `37_49.tmx`까지 직사각형 84개에서 실제 사용된 10,042개 고유 `(tile_set_name,local_id)` / 322개 타일셋 이름. 기존 5,409키 재사용·신규 4,633키. 원본 PNG 전체 406개 중 이름 일치 PNG 319개가 이 범위에 사용됨.
- **A1**=TMX 선언 아틀라스 그리드, **A2**=TileZed 텍스트 정의 그리드. 스프라이트별 실제 픽셀/가시 픽셀 수/원본 경로/SHA를 기록. **A1=A2 동일 가시 3,326종**, 한쪽에서만 가시 **6,673종** (이 다수는 TMX 선언과 2x PNG의 규격 충돌로 A1이 부재하고 A2가 의미 있는 이미지로 보임). A1/A2 둘 다 가시지만 서로 다른 이미지인 0종.
- **A3**=JUMBO/XL/XXL 및 stump 실물 아틀라스를 모델이 확인하고 **전용 전체 나무 프레임 격자**를 적용한 **36종의 추가 가시 후보**. 개별 Local ID 매핑과 실제 스프라이트 자르기 정확성은 불확실하고 일부 XL/XXL 초안 크롭에서 아래 행 나무가 같이 보이는 점 주의.
- **전체 가시 A 후보 10,035 / 10,042종**. 미확보 7종 = 동일 이름 PNG가 없는 3종 + 현재 정해진 크롭이 투명한 4종. **7종을 투명 또는 정체 없음으로 인증하지 말 것.** 과거 사용자 제외 14종(v113 8 + v116 6) 계속 별도 표시.
- **마스터 CSV** `review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv` (SHA-256 `189700d0d6b1f0e6c20bae268a0d33e4425ca275e169987e13b2786d7dfcb7cf`). 원본 A1/A2만 담은 `A_CANDIDATE_MASTER_10042.csv` 및 `sheets/A_000.jpg..A_125.jpg` 126장, 오프라인 인덱스 `A_CANDIDATE_REVIEW_INDEX.html`도 보존. JUMBO A3 접촉판과 29종 원본 전체 아틀라스 예외 근거 추가.
- **공식 PNG–TMX 대응/TileZed 최종 검증/정체 인증: 모두 0**. 코드에 설정된 `AI_per_key_selected=0`은 이미지 후보 기계적 생성만으로 사람이/AI가 10,042 Local ID를 선택·검증한 것은 아니라는 뜻. 이 A 후보는 다음 A→B/C/D 검증의 출발점이며 기존 SQLite v116의 관찰 5,400·감사 후보 4,512·v115 시각 계열 후보 882·최종 인증 0 불변.
## v116 사용자 제외: 이미지 없는 보류 6종을 활성 검수에서 제외 (2026-10-26)
- **사용자 지시: 이미지가 없어서 검수하지 못한 6종은 앞으로 분석 대상에서 모두 제외.** 정확한 키는 `checkpoints/v116/user_exclude_six.csv`와 `docs/V116_USER_EXCLUDED_NO_IMAGES.md` 참조.
- **6종:** `e_carolinasilverbellJUMBO_1/1`, `e_dogwoodJUMBO_1/1`, `e_redmapleJUMBO_1/1`, `vegetation_groundcover_01/22`, `vegetation_trees_01/8`, `vegetation_trees_01/10`.
- 최신 DB 신규 테이블 **`v116_user_excluded_missing_image` = 6**. 앞으로 재검수 대상은 **`v116_active_v115_held_queue` = 0** / **`v116_active_v115_review_queue` = 882**로 필터할 것. 과거 `v115_ai_held_queue` 6행·`v115_ai_visual_review` 888행은 근거 보존을 위해 그대로.
- **6종 제외는 ‘투명 타일 확인’이나 ‘정체 규명 완료’가 아니다**. 유효한 A 이미지의 확보/Local ID 매핑이 되지 않아 사용자 지시에 따라 활성 작업에서만 제외한 것. 원본 PNG·TMX·기존 증거 삭제 금지.
- 누적 관찰 5,400종, 기존 4,512종 감사 후보, v115 별도 882 잠정 시각 후보, 최초 미관찰 9종(v113 사용자 제외 8종·활성 1종), 최종 정체 인증 0종 불변.
## v115 사용자 지적 반영: AI 직접 888종 시각 재검수 (2026-10-26)
- 74장 `review/v115_model_visual/sheet_000.jpg` ~ `sheet_073.jpg`의 전체 888개 키(A1/A2/B/C/D 후보·실제 TMX 장면)를 모델이 직접 화면 판독. AI 잠정 물체·부품 후보 **882종**, 보류 **6종**. 882종 중 **870종 low(주로 계열 수준), 12종 medium**, 정체 최종 인증 **0종**. 888을 100% 상세 완결 식별했다고 주장 금지.
- 사용자 관찰대로 `appliances_com_01/3`은 **송수화기형 통신기기(전화·무전 장비의 미확정 후보)**로, `appliances_com_01/96/97/108` 등은 전봇대 가로대에 연결되는 가공 전선 계열로 기록. `appliances_com_01/120/121/123/124/133`은 세로 인입선 계열. `electricity_pylon/42/45`는 격자 철골 구성부. 15×15 확대한 **8개**의 B/C/차이 증거가 `review/v115_extended_context/`에 있고 원본 라벨 변조에 따른 가짜 B−C 차이는 수정 완료.
- 원본 A1=TMX 선언 격자, A2=TileZed 텍스트 격자 잠정 후보이며 **공식 Local ID 검증 0**. B−C 0인 **332종**을 자동으로 투명·빈 것으로 판정 금지. 6종은 원본 또는 격자 소스 불확실하여 held.
- 모든 결과: `review/v115_ai_identity/AI_VISUAL_REVIEW_888.csv`, `review/v115_ai_identity/SUMMARY.json`, `docs/V115_AI_VISUAL_REVIEW_888.md`. 최신 물리 SQLite `analysis/current/v115/`에는 **독립 `v115_ai_visual_review` 테이블**, `v115_ai_candidate_queue` (882), `v115_ai_held_queue` (6)을 추가. 기존 `tile_catalog.observed_any` 5,400, `provisional_candidate_any_auditable` 4,512, `analysis_queue` 9, `v113_active_review_queue` 1, 사용자 검수 제외 8 및 최종 인증 0 그대로. `mapping_verified=tilezed_verified=final_certified=0`.
- v115 SHA-256 `4f0f0679c85d18a2ac87d440a0c41f9708348b0004e1efe231410e7f99ffae20`, GitHub Actions workflow `build-v115-unified.yml`에서 복원·PRAGMA integrity_check·이전 테이블 보존 PASS. **다음은 882종의 세부 정체·PNG 매핑 독립 검증**, 후속 신규 맵 범위 4,633종의 A 후보 선정.

## v113 사용자 수동 검수 — 8종 활성 제외, 2번 식생 잠정 (2026-10-26)
- **사용자 검수 대상 9종 중 8종(번호 1·3·4·5·6·7·8·9)은 추가 검수 제외**, **2번 `f_bushes_1/66`은 '풀 또는 꽃 계열 식물'로 낮은 확신도의 사용자 잠정 후보**. 이 의견은 사용자의 수동 판단이며 공식 PNG–TMX Local ID 및 TileZed 인증이 아니다.
- v113 전체 SQLite는 v111 SHA-256 검증본을 물리 복제. 기존 `analysis_queue` **9종 원형 보존**, 신규 뷰 **`v113_active_review_queue`는 1종만 반환**한다. v113의 다음 검수 작업은 반드시 이 뷰를 우선 사용할 것. 원본 5,409종·누적 이미지 관찰 5,400종·기존 감사 가능 후보 4,512종·최종 인증 0종은 변하지 않는다.
- **8종 제외 = 투명 인증 아님**: 사무실 3종만 *잠정 원본 크롭* 알파 0 확인, JUMBO 3종은 파일 존재/크롭 격자 불일치, 나머지 2종은 원본 파일 미확보. 기존 PNG/TMX 및 사용자 수동 검수 80종은 모두 보존한다.
- `checkpoints/v113/user_review.csv` 및 `docs/USER_REVIEW_V113.md`에 9종 수동 검수 의견, 소스 상태, 사용자 제외/활성 유지 구분을 기록. 통합 SQLite `v113_user_review` 테이블과 `tile_catalog.v113_user_review_action`·`tile_catalog.v113_user_candidate`는 해당 의견만 나타내고 관찰·최종 인증 칼럼을 올리지 않는다.
- v113 통합 SQLite SHA-256 `205e7a4e59b2e85c986662f34b36cd030555a5cc69000ed60115fee9c8475b88`, 7개 복원 조각 SHA/PRAGMA integrity_check PASS. 기존 비교판 7장 및 수동 검수 증거 14항목 ZIP CRC PASS, SHA-256 `51665ca278e72ec7ae121ae02f4b061d852287189904340172e7d76fae22bc0a`.
- **다음은 `f_bushes_1/66` 1종에 집중**, B–C 변화 0 원인과 실제 식물 형태를 공식 타일 정의·TileZed와 대조하여 재검토한다. 제외 8종은 재검수 요청 시 복구할 수 있다.

## v112 남은 9종 원본 소스 진단 (신규 관찰 0, 2026-10-26)
- **최신 승인 관찰 체크포인트는 계속 v111**(5,400/5,409종, 99.8336%; 미관찰 9종; 잠정 후보 4,512종; 최종 인증 0종). v112는 관찰 승격 없는 감사·원본 소스 추적 결과로서 `PROJECT_STATE.json` 및 통합 v111 SQLite를 덮어쓰지 않는다.
- 전체 9종 키를 `audits/v112_remaining9/SOURCE_AUDIT.json`·CSV에 기록. `location_business_office_generic_01` Local ID 9/11/12는 TileZed 텍스트 격자 A의 RGBA 알파 픽셀 **0**; `f_bushes_1/66`은 **4,837개** 불투명 픽셀이나 B-C 변화 0. 4종 TMX 실제 GID·좌표·같은 위치 레이어 순서 기록.
- 잘못 누락으로 본 JUMBO 나무 3종의 **실제 원본 PNG가 `Tiles/2x/jumbo/`에 존재**함을 발견. JUMBO 3키의 A/B/C/D JPEG **15장·검수판 1장** 직접 판독했지만 현재 격자는 `width_scale_unexpected`, A 빈 프레임, B-C 0이므로 3종 모두 미관찰 유지.
- 충돌 사본명 `camping_03 (ayrton orio's conflicted copy 2025-09-10)`에는 이름 정규화 후 `camping_03.png`가 **대체 후보**로 존재하지만 내용과 Local ID 19 대응을 미검증. `jumbo_tree_01/0`는 동일 이름 PNG 미발견. 파일명 유사도를 타일 정체 증거로 승격하지 않는다.
- 시각·파일 증거 전체는 `audits/v112_remaining9/v112_nine_unresolved_source_evidence.zip`(24항목 CRC PASS, SHA-256 `246c6361b2aa6d2eda97202d69d8429841b8b4701207d229ff51a3f59284e896`), 보고서 `docs/V112_SOURCE_AUDIT.md`, PNG 크롭 4개, 신규 JPEG 15개 및 검수판 1개로 보존.
- 다음은 **JUMBO PNG의 실제 타일 격자와 TMX GID·Local ID 대응**, 관목 오클루전, camping 충돌 원본, jumbo_tree 원본을 검증한다. 공식 매핑·TileZed·최종 인증은 모두 0.

## v111 미관찰 단일배치 21종 실제 A/B/C 시각 검수 (2026-10-26)
- v110 SQLite SHA 복원 후 미관찰 21종 전수를 TileZed 텍스트 타일정의 격자와 PNG·TMX에 대조. 16종 A/B/C/D 안내판 생성(개별 JPEG 80장, 검수판 3장), 직접 관찰. 나머지 5종은 원본 PNG 누락으로 별도 보류.
- 새 이미지 관찰 **12종**: B-C 제거 변화가 명확한 작은 식생·벽 균열·잎 없는 나무 관련 잠정 후보 12종(신뢰도 low). 가시 기여 없는 4종은 관찰 미완료, PNG 누락 5종도 미완료. 두 번째 TMX 배치 D는 16종 모두 없음. 원본 A는 TileZed 텍스트 타일정의 잠정 격자이며 공식 매핑 인증 아님.
- 누적 이미지 관찰 **5,400/5,409종(99.8336%)**, 남은 미관찰 **9종**, 감사 가능한 잠정 후보 **4,512종**, 최종 인증 0종. 이전 v36~v110 전체 SQLite 테이블, 사용자 수동 검수 80종, 원본 PNG/TMX 보존.
- `analysis/current/v111/MANIFEST.json` 통합 SQLite 크기 89,169,920 bytes, SHA-256 `c2d31b708d5a706709007265ce44f0bd63efed27f8acd5fe5e9b3ecdd1dce73f`. 7개 Base64/zlib 조각 SHA 복원, PRAGMA integrity_check PASS. `checkpoints/v111/unresolved_9.csv`와 `v111_unresolved_queue_audit` 테이블에 미해결 9종 보존.
- `checkpoints/v111/` CSV/TSV·이미지 80장 내장 HTML·89개 ZIP 항목 CRC PASS. ZIP SHA-256 `26a0eeeb46fc0c526b470d86d1ff5a510151d00517722b1188b5d350a830df42`. 원본 JPEG·접촉판은 `checkpoints/v111_singleuse_preview/` 저장.
- 공식 Local ID/TileZed 렌더 정합이 확인되지 않아 `mapping_verified=tilezed_verified=final_certified=0`. **다음 작업은 PNG 누락 5종·B-C 0인 4종의 출처와 의미를 밝히는 일**이다.

## v110 실제 D 30종 TileZed 타일정의 텍스트 격자 잠정 크롭·직접 시각 판독 (2026-10-26)
- v109 최신 물리 SQLite 미관찰 51종을 실제 TMX에서 검사. 다른 사용 위치 D가 있는 32종 중 원본 PNG가 존재하는 30종을 대상으로 A/B/C/D를 생성했고, 2종은 PNG 누락으로 보류. D 없는 나머지 19종은 엄격한 A/B/C/D 관찰 대상에서 제외했다.
- 핵심 원인: TMX 아틀라스 선언은 8열이지만 TileZed `Tiles/tiledefinitions.tiles.txt`는 `d_generic_1` 16×10, `d_wallcracks_1` 9×8, `f_bushes_1` 16×8로 실제 2x PNG 격자 치수와 정확히 맞는다. **텍스트 격자로 잠정 크롭했을 뿐 공식 Local ID 인증은 아니다.**
- 원본 A·같은 층 TMX 5×5 B·선택 배치 한 건 제거 C·다른 실제 위치 D **30종**, JPEG **150장**, 접촉판 **5장 모두 직접 시각 판독**. 원거리 D 28종, 근접 D 2종. 후보 **25종(low)**, 보류 **5종**, 기존 키 중복 0.
- 통합 **5,388/5,409종(99.6118%)**, 미관찰 **21종**, 감사 가능 잠정 후보 **4,500종**, 최종 인증 **0종**. `analysis/current/v110/MANIFEST.json` SHA-256 `cc004fb60f6df412da3068e909f9696b0d8cedf8a57d600abd383d1e214c7de0`; 압축 7조각 복원, SQLite integrity_check, 원본 PNG/TMX SHA·좌표·GID·150 JPEG 및 ZIP 159항목 CRC 통과.
- `checkpoints/v110/observations.tsv`·CSV·PSV·검수 보고서, `checkpoints/v110_tiledef_preview/`의 원본 JPEG 150장과 접촉판 5장, 이미지 내장 HTML 및 증거 ZIP 보존. `mapping_verified=tilezed_verified=final_certified=0` 유지. 사용자 수동 검수 80종과 과거 DB·체크포인트 불변.
- 다음: 미관찰 **21종**, 원본 PNG 누락 2종 및 공식 TileZed Local ID 대응 검증.

## v109 원본 A/B/C/D 신규 48종 직접 시각 판독 (2026-10-26)
- v108 SHA 검증 물리 통합 SQLite의 미관찰 99종에서 실제 신규 고유 48키를 선정했다. 원본 PNG 크롭 A, TMX 동일 층 5×5 조립 B, 동일 배치 1개 제거 C, 다른 사용 위치 D 또는 안내판을 만들어 **JPEG 240장과 접촉시트 8장 모두 직접 시각 검토**했다.
- 개별 관찰 PSV 48개를 2개 파일에 보존하고 원본 해시·GID·좌표·B-C 픽셀 차이·다른 배치 정보를 TSV/CSV로 기록했다. **잠정 정체 후보 40종(low)**, 모호·투명·변화 적은 대상 **보류 8종**, 신규 고유키 중복 0. 통합 관찰 **5,358/5,409종(99.0571%)**, 미관찰 **51종**, 감사 가능 후보 **4,475종**, 공식 인증 **0종**.
- 다른 실제 TMX 사용 D **1종**은 5칸 이상 떨어진 위치를 확인했으나 **원본 A가 투명하고 B-C 변화가 0**이라 정체 판단이 불가능하다. **근접 D 0종, 다른 D 미확보 47종**. D가 있다고 정체 인증을 올리지 않는다.
- v109 통합 SQLite: `analysis/current/v109/MANIFEST.json` 총 **89,051,136 bytes**, SHA-256 `418ba566102c6e3d727c0bf33d5a6228fb2956c7a15b4c1c6f9002fbb235ec61`. v36~v108의 모든 과거 테이블 물리 보존; 압축 Base64 7개 조각 재복원·SQLite `integrity_check`·원본 PNG/TMX SHA·GID/좌표·중복 검사 PASS.
- `checkpoints/v109/`: CSV/TSV, 이미지 **240장 내장 HTML**, ZIP 증거 252항목 CRC PASS. ZIP SHA-256 `fc9390e349fe7d2d42e31a67825deef389c1fbd4a1ec1dd3ad3eb1405683bb78`. `checkpoints/v109_preview/`의 원본 JPEG 240장, 접촉시트 8장을 보존.
- 기존 사용자 수동 검수 80종 및 v36~v108 데이터·PNG/TMX 불변. Local ID·PNG 높이·TileZed 정합 검증은 미완료 `mapping_verified=tilezed_verified=final_certified=0`. **다음은 v109 미관찰 51종**.

## v108 신규 48종 원본 PNG/TMX A/B/C/D 직접 시각 판독 (2026-10-26)
- v107 통합 SQLite 미관찰 147종에서 신규 고유 48종 선택, A 원본 PNG, B 같은 층 TMX 5×5, C 단일 배치 제거, D 실제 근접 다른 배치 3종 또는 D 미확보 안내 45종을 생성. 접촉 검수판 8장에 담긴 48종을 시각 판독하고 개별 관찰 PSV 48행 기록.
- 신규 잠정 후보 **38종(전부 low)**, 보류 **10종**, 신규 중복 0. 독립된 원거리 D는 0종. 누적 관찰 **5,310/5,409종(98.1697%)**, 미관찰 **99종**, 감사 가능 후보 **4,435종**, 최종 인증 **0종**.
- `analysis/current/v108/MANIFEST.json`: 통합 SQLite 88,944,640바이트 SHA-256 `182ce653246b0ddb01144f29df91fd97f3ff3aa3baacd54d7ea29d8de42d5bb9`. 7개 분할 조각 복원 및 SQLite integrity_check, PNG/TMX SHA·좌표/GID·키 중복·JPEG 로딩·ZIP CRC 검증 성공.
- `checkpoints/v108/` CSV·TSV·HTML(이미지 240장 내장)·ZIP 증거와 `checkpoints/v108_preview/` 원본 JPEG 240장 및 접촉판 8장 보존. 기존 v36~v107 원본과 사용자 수동 검수 80종 계보 유지.
- 공식 PNG–TMX Local ID 및 TileZed 미검증으로 `mapping_verified=tilezed_verified=final_certified=0`. 다음은 미관찰 **99종**에서 재개.

## v107 신규 48종 원본 PNG/TMX A/B/C/D 직접 시각 판독 (2026-10-26)
- SHA-256 복원 검증된 v106 통합 SQLite의 `analysis_queue` 미관찰 **195종**에서 신규 고유 **48종** 선정(과거 이미지 관찰 키와 중복 0). 실제 PNG 원본 A, 같은 층 TMX 5×5 배치 B, 해당 배치 하나를 제거한 C, 다른 실제 TMX 위치 D **10종** 또는 별도 사용 위치 미확보 **38종**을 생성했다.
- 48종의 A/B/C/D 개별 JPEG **240장** 및 6종씩 묶은 **8장의 접촉 검수판**을 모두 직접 시각 판독했다. `checkpoints/v107/review_notes_000_023.psv`와 `review_notes_024_047.psv`에 개별 외형·부품 설명을 기록했고, 후보 **34종(모두 low)**·보류 **14종**으로 분리했다.
- 누적 이미지 관찰 **5,262/5,409종(97.2823%)**, 남은 미관찰 **147종**, 감사 가능 잠정 후보 **4,397종**, 공식 최종 인증 0종. D 10종은 모두 **근접·비독립 배치**, 독립 원거리 D 0종이므로 최종 정체 인증을 올리지 않았다.
- 완전 물리 SQLite `analysis/current/v107/MANIFEST.json` **88,829,952바이트**, SHA-256 `f5684f47922b0b9d1919f27eb5720e471a59069d9512885a6a7101bd7c2c3b14`. v36~v106 모든 과거 테이블 보존 및 신규 48종만 병합. SQLite `integrity_check`, 7개 압축 조각 전체 SHA-256 복원, 원본 PNG/TMX SHA·배치 좌표/GID·키 중복·이미지 로딩 PASS.
- `checkpoints/v107/`에 관찰 TSV/CSV, 이미지 240장 내장 HTML, 증거 ZIP 252개 항목 CRC PASS. ZIP SHA-256 `b1f54eaa9b7570da0003e8e1c3d795df6c0a0b6d6861d829d70050c31da272e7`. 원본 JPEG 및 접촉판은 `checkpoints/v107_preview/`에 보존.
- PNG 높이 불일치와 공식 Local ID 및 TileZed 정합 미검증을 유지하므로 `mapping_verified=tilezed_verified=final_certified=0`. 사용자 수동 검수 80종 및 과거 모든 버전은 수정하거나 초기화하지 않았다. 다음 미관찰 **147종**에서 재개.

## v106 신규 48종 원본 PNG/TMX A/B/C/D 직접 시각 검수 (2026-10-26)
- v105 물리 통합 SQLite SHA 검증 후 `analysis_queue` 미관찰 **243종**에서 새로운 고유 **48종** 선정. 원본 타일 PNG A, 실제 TMX 같은 층 5×5 근사 B, 해당 배치 하나만 제거한 C, 실제 다른 근접 사용 위치 D **12종** 및 D 미확보 **36종**을 생성.
- 생성된 개별 JPEG **240장**·접촉 검수판 **8장**을 모두 직접 열어 외형을 판독했다. 개별 `checkpoints/v106/review_notes_*.psv` 48개 메모(2개 파일), 실제 좌표·GID·원본 해시 포함 TSV/CSV 보존. **잠정 후보 34종(전부 confidence low)**, **보류 14종**, 중복 0.
- 누적 **5,214/5,409종(96.3949%)**, **미관찰 195종**, 감사 가능한 후보 **4,363종**, 최종 인증 **0종**. 12개 다른 D는 모두 독립 원거리 검증이 아닌 근접 배치이다.
- `analysis/current/v106/MANIFEST.json`: 완전 통합 SQLite **88,727,552 bytes**, SHA-256 `053dc825c70df841d915d65ecd69d57c1857113e9e58bd092bf63a9d118b6081`; 7개 Base64 압축 조각 복원, SHA·SQLite integrity_check·모든 과거 테이블 물리 보존·원본 PNG/TMX SHA·raw GID·좌표·신규 키 검사 성공.
- `checkpoints/v106/`: JPEG 240장 내장 HTML, CSV 및 ZIP 증거 252항목 CRC PASS, ZIP SHA-256 `627ff076b6de52d5ac358fcb61076592f00ed57c55c64530654d0ffa3ed5a9e4`. 시각 원본은 `checkpoints/v106_preview/`에 보관했다.
- v36~v105 기존 데이터/체크포인트·Tiles PNG/TMX와 사용자 수동 검수 80종 계보는 불변. PNG 아틀라스 높이 불일치와 공식 Local ID·TileZed 정합 미검증으로 `mapping_verified=tilezed_verified=final_certified=0`. 다음 작업은 **v106 미관찰 195종**.

## v105 신규 48종 원본 PNG/TMX A/B/C/D 직접 시각 판독 (2026-10-26)
- v104 물리 SQLite SHA 확인 후 `analysis_queue` 미관찰 **291종**에서 다른 기록과 중복 없는 **48종** 선정. PNG A, TMX 같은 층 5×5 B, 동일 대상 배치만 제거한 C, 다른 실사용 근접 배치 D **5종** 또는 미확보 안내판 **43종**을 원본 PNG/TMX에서 생성했다.
- 48종 A/B/C/D 총 JPEG **240장**, 6종씩 배열한 시각 접촉판 **8장**을 직접 열어 외형·부품 역할을 검토하고 개별 PSV 시각 메모 **48행**을 기록했다. 잠정 후보 **39종(모두 low)**, 외형 또는 제거 차이 근거 부족으로 **9종 보류**, 신규 키 중복 0.
- 누적 관찰 **5,166/5,409종(95.5075%)**, 미관찰 **243종**, 감사 가능 잠정 후보 **4,329종**, 최종 인증 **0종**. 다른 실제 근접 D 5종은 모두 독립 원거리 장소가 아니며 43종은 실제 두 번째 배치가 없다.
- `analysis/current/v105/MANIFEST.json`: 복원되는 완전 통합 SQLite **88,625,152바이트**, SHA-256 `84fe35dc849643a028e768f578dce98e4cd609ef9d9760bf3da8a678bab6744e`. 이전 v36~v104 전체 테이블 물리 보존, 7개 분할 조각 복원, SQLite integrity_check, PNG/TMX 원본 SHA, TMX 원시 GID·좌표·B-C 차이·고유키 검사 통과.
- `checkpoints/v105/observations.tsv`·CSV, `checkpoints/v105_preview/`의 증거 JPEG와 검수판 8장, JPEG 240장 내장 HTML, 증거 ZIP 252항목 CRC PASS. ZIP SHA-256 `f23d46b0fa2f0e4e40f9d69bc9791c1b0ef45a16e74b6b8c6671fa0cdc33306d`.
- 기존 PNG/TMX 및 v36~v104 SQLite·검수 계보·사용자 수동 검수 80종을 수정하지 않았다. PNG 아틀라스 높이 불일치와 공식 Local ID·TileZed 정합 미검증을 명시하고 `mapping_verified=tilezed_verified=final_certified=0`을 유지했다. 다음 신규 시각 분석은 v105 미관찰 **243종**에서 시작한다.

## v104 신규 48종 원본 PNG/TMX A/B/C/D 시각 검수 (2026-10-26)
- 최신 v103 물리 SQLite 원본 SHA 검증·복원 후 `analysis_queue` 미관찰 339종에서 **기존 기록과 겹치지 않는 48종** 선택. `checkpoints/v104_preview/`에 원본 PNG A, 같은 층 TMX 5×5 조립 B, 한 배치 제거 C, 다른 실제 근접 TMX 사용 D 또는 미확보 안내를 **240 JPEG** 및 8개 접촉 시트로 생성.
- 8개 시트를 **모두 직접 열어** 48종의 외형·부품 역할·잠정 후보·불명확 판정을 기록한 2개 `checkpoints/v104/review_notes_*.psv` 파일과 실제 TMX 좌표/GID 및 소스 SHA를 합친 `observations.tsv`·CSV 보존.
- 신규 **48종 이미지 관찰**, **잠정 후보 35종(전부 confidence low)**, **보류 13종**, 키 중복 0. 실제 다른 근접 D **3종** 모두 5칸 미만 비독립, 다른 사용 위치 없는 45종은 D 미확보 안내. 독립 D 0종.
- 누적 **5,118/5,409종(94.6201%)**, 남은 미관찰 **291종**, 감사 가능한 잠정 후보 **4,290종**, 최종 인증 0. 이전 v36~v103 전체 물리 SQLite 테이블·체크포인트와 사용자 수동 검수 80종 계보 불변 보존.
- `analysis/current/v104/MANIFEST.json`: **88,510,464바이트**, SHA-256 `f4fc3010dd7046a3b6ff67728d01b3c3769f1dfac518e336abf369bb911f56f6`. 7개 복원 조각 SHA, PRAGMA integrity_check, CSV 48행, 이미지 내장 HTML 240장, 증거 ZIP 252항목 CRC PASS, PNG/TMX SHA·좌표·GID·중복 검사 통과.
- 공식 Local ID PNG–TMX 매핑·TileZed 검증과 물리 높이 불일치는 아직 해결되지 않았으므로 `mapping_verified=tilezed_verified=final_certified=0`. 다음 검수는 **v104 미관찰 291종**에서 시작.

## v103 신규 24종 직접 이미지 판독 (2026-10-26)
- v102 통합 SQLite `analysis_queue` 미관찰 363종에서 **기존 관찰과 중복 없는 고유 24종** 선정. 원본 PNG A, TMX 같은 층 5×5 B, 대상 배치 하나만 제거한 C, 실제 다른 배치가 없어 D 미확보 안내판 24종을 생성. **4개 접촉판을 직접 열어 시각 판독**, 모호한 4종은 개별 ABCD 비교판 추가 확대.
- 신규 이미지 관찰 **24종**, 잠정 후보 **19종(모두 low)**, 보류 **5종**(`appliances_cooking_01/78`, `furniture_bedding_01/49`, `location_trailer_02/40`, `walls_exterior_house_02/83`, `walls_exterior_roofs_09/125`). **D 실제 다른 사용 위치 0종**(24종 전부 TMX 단일 배치), 독립 D 0종. 없는 D를 실사용 증거로 계상하지 않는다.
- 누적 **5,070/5,409종(93.7327%)**, 미관찰 **339종**, 감사 가능한 잠정 후보 **4,255종**, 최종 인증 **0종**. PNG 높이 불일치 24종, 공식 Local ID·TileZed 미검증으로 `mapping_verified=tilezed_verified=final_certified=0`.
- `checkpoints/v103/observations.tsv`·CSV, `INDEPENDENT_VISUAL_AUDIT.md`, `checkpoints/v103_preview/`의 JPEG 120장과 접촉판 4장, 이미지 내장 HTML 2개(총 120장), 증거 ZIP 2개(총 132항목 CRC PASS). SHA·TMX GID·좌표·PNG 로딩·JPEG 로딩·SQLite `integrity_check`·7조각 DB 복원·이전 테이블 보존·신규 키 중복 0 GitHub Actions PASS.
- `analysis/current/v103/MANIFEST.json`: 물리 통합 SQLite **88,403,968바이트**, SHA-256 `77c2fd14ed8f341aefb16411583892e4132ac7aa6004bfaa75d147863f7b27a8`. 기존 v36~v102 DB·체크포인트, 원본 PNG/TMX, 사용자 수동 검수 80종 및 재검수 계보 보존.
- 다음은 v103 미관찰 **339종**에서 진행한다. 24종의 두 번째 실제 사용 위치는 확보되지 않았으므로 별도 검증 필요.

## v102 신규 12종 실제 A/B/C/D 직접 판독 (2026-10-26)
- v101 통합 SQLite(원본 SHA-256 검증)의 미관찰 375종에서 **실제 다른 TMX 배치가 존재하는 신규 고유 12종**만 선정. 병행 v101 신규 48종과의 교집합 0, DB 관찰 키 중복 0.
- 원본 PNG A, 같은 층 주변 5×5 TMX 근사 아이소메트릭 B, 선택 레이어 배치 1건만 제거한 C, **다른 실제 TMX 좌표 D 12종**을 생성. 12개 개별 ABCD 비교판과 접촉 검수판 2개를 **직접 열어 시각 판독**하고 `checkpoints/v102/review_notes_000_011.psv`에 특징과 후보/보류를 분리 기록.
- 신규 이미지 관찰 **12종**, 잠정 후보 **10종(모두 low)**, 보류 **2종**: `location_trailer_02/63`(무특징 황갈색 상자형 부품의 역할 불명), `industry_02/161`(금속 세로 함체이나 B-C 0픽셀). 다른 D는 전부 근접 비독립 현장, 독립 원거리 D 0.
- 누적 **5,046/5,409종(93.2890%)**, 미관찰 **363종**, 감사 가능한 잠정 후보 **4,236종**, 최종 인증 **0종**.
- `analysis/current/v102/MANIFEST.json`: 통합 SQLite **88,342,528바이트**, SHA-256 `1c81a1213fb64c095908618225dac6b3450c5b1edfd1db64fa4c2d241c2c557c`, 압축 7조각 복원 검증 통과. v101 원본 전체 테이블 물리 복제, SQLite integrity_check, 이전 계보 보존, 원본 PNG/TMX SHA·TMX GID·좌표, JPEG 60장, 이미지 내장 HTML 60장, ZIP 66항목 CRC PASS.
- 원본 `Tiles/`, `B4220.3_MapExport_256/`, v36~v101 원본 DB·체크포인트, 사용자 수동 검수 80종 및 재검수 자료는 수정/삭제하지 않았다. PNG 높이 불일치와 공식 Local ID·TileZed 미검증: `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`. 다음 작업은 v102 미관찰 363종에서 진행한다.

## v101 신규 48종 실제 A/B/C/D 시각 판독 (2026-10-26)
- v100 물리 통합 SQLite 복원·SHA 검증 후 미관찰 423종 대기열에서 고유 48종을 선정하고 실제 원본 PNG 및 TMX로 A/B/C/D 고해상도 JPEG **240장**, 6종씩 묶은 검수판 **8장**을 생성한 뒤 **8장 모두 직접 시각 판독**하여 review_notes PSV 두 파일로 기록했다.
- 신규 직접 관찰 **48종**, 잠정 후보 **35종(모두 low)**, 보류 **13종**, 중복 0. 누적 **5,034/5,409종(93.0671%)**, 미관찰 **375종**, 감사 가능한 후보 **4,226종**, 최종 인증 0종.
- D 다른 실제 근접 위치 5종은 모두 독립 현장이 아니고, 43종은 다른 실제 배치가 없어 D 안내판으로 대체. 독립 D 0. 관찰 여부와 잠정 정체가 공식 인증을 뜻하지 않는다.
- `analysis/current/v101/MANIFEST.json`에서 v100 물리 SQLite SHA·원본 테이블 보존·신규 48키 중복 없음·7개 DB 압축조각 복원·PRAGMA integrity_check 확인. `checkpoints/v101/observations.tsv`, 이미지 내장 HTML 1개, CSV, CRC 검증 증거 ZIP 1개와 `checkpoints/v101_preview/`의 240 JPEG 및 8개 검수판 보존.
- 공식 PNG-TMX Local ID, TileZed 정합과 PNG 높이 문제는 여전히 미검증. `mapping_verified=tilezed_verified=final_certified=0` 유지. 다음 작업은 **v101 미관찰 375종**.

## v100 신규 216종 실제 A/B/C/D 시각 판독 (2026-10-26)
- v98에서 240종 A/B/C/D 비교판을 생성하고 40개 검수 접촉시트를 **전부 직접 관찰**해 개별 외형·부품 역할·보류를 작성했으나, 병렬 작업에서 v99 24종이 먼저 main에 병합된 것을 발견. 기존 **24종과 정확히 겹치는 24키를 제외**하고 v99 통합 DB 대기열에서 **216종만 새로 선정**, 두 증거 매니페스트의 키·B-C 픽셀 변화·직접 시각 기록을 개별 재대조했다. 신규 중복 0.
- v99 베이스에서 독립 신규 216종의 원본 PNG A, 실제 동일 층 TMX 5×5 조립 B, 동일 레이어 배치 1건 제거 C, D의 다른 근접 배치 또는 미존재 안내, 합본 JPEG **1,080장**과 접촉판 **36장**을 `checkpoints/v100_preview/`에 새로 생성하고 원본 해시/이미지를 검증. 다른 실제 D 위치 **23종** 모두 가까운 비독립 사용, 다른 위치 없음 **193종**, 독립 D 0.
- `checkpoints/v100/review_notes_000_035.psv` 등 6개 수동 판독 PSV에 A/B/C/D 시각 기록을 유지, `scripts/build_v100_observations.py`로 원본 TMX/PNG SHA, 실제 좌표/GID와 합친 TSV/CSV 생성. 신규 이미지 관찰 **216종**, 잠정 후보 **181종(전부 low)**, 보류 **35종**, 인증 0종.
- 누적 **4,986/5,409종(92.1797%)** 이미지 관찰, 미관찰 **423종**, 감사 가능한 잠정 후보 **4,191종**. 기존 v36~v99 통합 DB와 사용자 수동 검수 80종 계보는 불변 보존.
- `analysis/current/v100/MANIFEST.json`의 물리 SQLite **88,199,168바이트**, SHA-256 `822e353d3e6d4e6ae51a933d7c388885cae34992f18331fcf9a5c51dc3702e04`. v99 물리 SQLite SHA 검증 뒤 전체 테이블 물리 복제, PRAGMA integrity_check, 이전 테이블 보존, 신규 키 중복 0, 7개 분할 조각 복원 SHA, TMX/PNG 소스 SHA 및 좌표 검증 통과.
- 216종 관찰 CSV/TSV, 이미지 360장씩 내장 HTML **3개**, 검수 증거 ZIP **3개**(각 376개 항목, 전체 1,128개 항목, CRC PASS), 고해상도 JPEG **1,080개**와 36개 검수 접촉시트 보존.
- 공식 PNG–TMX Local ID 및 TileZed 정합은 미검증, `mapping_verified=tilezed_verified=final_certified=0` 유지. **다음 작업은 최신 v100 DB 미관찰 대기열 423종에서 시작**.

## v99 신규 24종 A/B/C/D 시각 판독 (2026-10-26)
- v98 통합 SQLite `analysis_queue` 미관찰 663종에서 중복 없는 24종 선정. 원본 PNG A, TMX 같은 층 주변 5×5 B, 단일 배치 제거 C, 다른 실제 근접 위치 D 6종 또는 대체 현장 없음 안내 D 18종, ABCD 비교판 총 120 JPEG 생성. 4개 접촉 검수판 모두 직접 열어 관찰하고 모호한 3종은 원본 A 확대 확인.
- 잠정 후보 17종(전부 low), 보류 7종. B-C 0·35·22·1769·537·196·0픽셀 보류. 원본 외형·부품 역할·보류 이유는 `checkpoints/v99/review_notes_000_023.psv`와 `observations.tsv`에 별도 기록.
- 독립된 원거리 D 0종. 원본 PNG 24종 모두 물리 높이 불일치, 공식 Local ID와 TileZed 정합 미검증. `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.
- 신규 24종 중복 0. 누적 관찰 **4,770/5,409종(88.1864%)**, 미관찰 **639종**, 잠정 후보 **4,010종**, 최종 인증 **0종**.
- `analysis/current/v99/MANIFEST.json` 물리 SQLite 87,744,512바이트 SHA-256 `cd2e811d1a197e6036dc9209d667d967d34cc8011fff277575ed2d949027a793`. v98 SHA 복원 확인, SQLite integrity_check, 전체 기존 테이블 보존, 7조각 압축 복원, 원본 PNG/TMX SHA·좌표/GID, JPEG 120장 로딩, HTML 120장 내장, ZIP 128항목 CRC PASS.
- 기존 v36~v98 SQLite·체크포인트·원본 PNG/TMX 및 사용자 수동 검수 80종 계보 변경하지 않음. 다음은 v99 미관찰 639종에서 재개.

## v98 신규 180종 실제 A/B/C/D 시각 분석 (2026-10-26)
- v97 통합 SQLite에서 미관찰 **843종** 중 중복 없는 신규 **180종(96개 타일셋)** 선정. 원본 PNG A·동일 층 TMX 5×5 조립 B·동일 레이어 단일 사용 위치 제거 C·다른 실제 근접 TMX 배치 또는 독립 위치 미확보 표시 D와 ABCD 합본 총 **900 JPEG** 생성.
- 6종씩 합친 **30개 검수 접촉판을 모두 직접 열어 관찰**, 원본 외형/부품 역할/보류를 `checkpoints/v98/review_notes_*.psv` 6개 파일에 각각 30건씩 남김. `scripts/build_v98_observations.py`가 증거 매니페스트의 좌표·raw GID·원본 PNG/TMX SHA 및 180개 직접 판독 기록을 `checkpoints/v98/observations.tsv`로 결합한다.
- 신규 **잠정 후보 152종(모두 confidence low)**, **보류 28종**, 중복 0. 실제 가까운 다른 사용 D **29종**, 독립 D **0종**, D 위치 없음 **151종**. 공식 TileZed/Local ID·PNG 물리 높이 정합 미검증 상태이므로 인증 0.
- 누적 이미지 관찰 **4,746/5,409종(87.7427%)**, 남은 미관찰 **663종**, 감사 가능한 잠정 후보 **3,993종**, 최종 인증 0종.
- v97 SQLite SHA 확인 후 전체 원본 DB 및 v36~v97 모든 계보와 사용자 수동 검수 80종 별도 기록 보존. `analysis/current/v98/MANIFEST.json` 통합 DB **87,691,264바이트**, SHA-256 `fad5f9b672eccad70080111ab9bb9fd56442427e6b6f035031d67aa88e9d32dd`. DB integrity_check, 7개 분할 DB 압축 복원 SHA, 신규 키 중복, PNG/TMX SHA, JPEG 900개 및 좌표/GID 검증 통과.
- `checkpoints/v98/`에 CSV·TSV, HTML 2개(각 이미지 450개 내장) 및 증거 ZIP 2개(각 469항목, CRC PASS) 보존. 원본 비교 JPEG 900개와 접촉판 30개는 `checkpoints/v98_preview/`에 보관.
- 다음은 최신 v98 통합 SQLite `analysis_queue`의 미관찰 **663종**에서 재개. 미검증 Local ID와 TileZed 공식 일치 전에는 어떤 잠정 정체도 final 인증하지 않는다.

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
