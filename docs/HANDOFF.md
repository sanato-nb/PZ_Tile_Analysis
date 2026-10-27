# 프로젝트 좀보이드 B42 타일 정체 분석 — 인수인계 (v124 최신)

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
