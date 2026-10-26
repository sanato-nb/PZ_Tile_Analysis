# v103 독립 이미지 판독 기록 (2026-10-26)

## 검수 범위와 근거

v102 물리 통합 SQLite `analysis_queue`의 미관찰 363종을 기준으로 기존 관찰과 중복되지 않는 고유 키 24종을 선정했다. 원본 `Tiles/2x/*.png`와 `31_45.tmx`, `31_46.tmx`에서 A(원본 타일), B(동일 층 5×5 근사 아이소메트릭), C(B에서 대상 레이어의 배치 **한 건만** 제거), D(다른 실제 TMX 사용 위치 또는 **미확보 안내**)를 생성했다.

**직접 이미지 관찰**: `checkpoints/v103_preview/review_sheets/sheet_000.jpg` ~ `sheet_003.jpg`의 접촉판 4장을 열어 A/B/C/D를 판독했다. 추가로 `fixtures_counters_01/171`, `industry_01/62`, `location_community_church_small_01/42`, `location_restaurant_bar_01/18`의 개별 ABCD 고해상도 비교판 4장을 열어 모호한 부품 역할을 확인했다. 타일셋명과 과거 v31 AI 분류는 판정 근거로 사용하지 않았다.

원본 픽셀의 형태를 기록한 24개 개별 관찰과 후보, 부품 역할, 신뢰도는 `review_notes_000_023.psv`에 **서로 다른 열**로 보존한다. TMX 좌표·층·레이어·raw GID·PNG/TMX SHA-256·B-C 픽셀 변화·주변 누락은 `v103_preview/EVIDENCE_MANIFEST.json` 및 생성될 `observations.tsv`를 따른다.

## 판독 집계

| 항목 | 수량 |
|---|---:|
| A/B/C 생성 및 직접 접촉판 시각 관찰 | 24종 |
| 원본 외형과 B-C로 잠정 후보를 제시한 타일 | 19종 |
| B-C 0 또는 극소·부품 역할 불명으로 보류 | 5종 |
| 기존 관찰과 중복 | 0종 (통합 DB에서 재검증 필요) |
| 다른 실제 사용 위치 D | **0종** |
| D가 실제 사용 위치가 아닌 미확보 안내판 | **24종** |
| 독립적인 두 번째 현장 | **0종** |
| PNG 선언/물리 높이 불일치 | 24종 |
| 최종 인증 | **0종** |

보류 키: `appliances_cooking_01/78`(B-C 0), `furniture_bedding_01/49`(0), `location_trailer_02/40`(184), `walls_exterior_house_02/83`(23), `walls_exterior_roofs_09/125`(0). 이들에 대한 A 이미지가 존재해도 배치 기여나 정확한 역할을 증명하지 못한다.

잠정 후보 19종은 전부 `confidence=low`. `boulders/46`은 B 주변 PNG 누락 3건을 별도 기록한다. 다른 위치 D를 발견하지 못했으므로 **D를 실제 배치라고 주장하지 않는다**. 공식 PNG–TMX Local ID, TileZed 정합, PNG 높이 불일치가 해결되지 않았으므로 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`을 유지한다.

## 품질 게이트

`checkpoints/v103/verify_delta.py`는 원본 SHA-256, TMX 배치/GID, JPEG 120장, 키 중복, B-C 기여, D 미확보와 인증 플래그를 검사한다. `scripts/build_unified_v103.py`는 v102 물리 SQLite를 복제한 뒤 신규 24종만 추가하고 원본 테이블·계보를 보존하며 `integrity_check`와 진행률을 검사한다. `scripts/build_v103_review_html.py`는 이미지 내장 HTML 2개 및 ZIP 2개를 만들고 ZIP CRC를 확인한다. **실제 통과 여부는 GitHub Actions 결과로 별도 확인해야 한다.**

기존 v36 이후 체크포인트와 원본 PNG/TMX, 사용자 수동 검수 80종은 수정하지 않는다.
