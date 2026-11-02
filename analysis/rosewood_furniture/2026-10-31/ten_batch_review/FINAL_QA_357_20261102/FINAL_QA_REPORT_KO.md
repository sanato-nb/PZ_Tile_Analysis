# 로즈우드 가구 357종 — 최종 범위·판정·중복·무결성 QA (2026-11-02)

> 범위 기준: Project Zomboid B42 로즈우드 가구 001~357. Minecraft Java 1.20.1 Forge 후보 외형 비교 기록. 이 문서는 **개별 검수 기록의 범위와 근거 문서**를 감사한다. Minecraft에 357종이 구현되거나 게임 내에서 인증되었다는 뜻이 아니다.

## 결론

- **기록 범위 357/357 = 100.0%**. 36개 정식 Draft PR의 상세 검수 CSV를 실제로 읽어 357개 `index` 값을 대조했다.
- **누락 0, 정식 범위 중복 0, 번호 오류 0**. 001~350은 10개씩 35구간, 351~357은 7개인 마지막 구간이다.
- **조건부 시각 후보 68종, 보류 289종**. 원본 상태 코드를 보존한 채 판정 분류를 표준화했다. **게임 설치/충돌/기능/1:1 인증 완료는 0종**.
- 정식 검수 PR 36개 모두 **Draft/Open/미병합**. PR #255는 131~140 사전 점검이므로 정식 집계에서 제외하고 PR #254를 사용했다.
- **36개 원본 상세 CSV와 36개 MANIFEST.json을 GitHub에서 직접 읽고 각각의 Git blob SHA를 기록**했다. 명시된 manifest 판정 개수와 정규화 CSV 개수의 충돌은 0건이다.
- 최근 GitHub Actions 실행 500개에서 **정식 PR 브랜치 32개의 성공 실행**을 확인했다. 나머지 4개는 성공 실행을 확인하지 못했다(아래).
- **중요한 제한:** 이번 QA는 JPG/ZIP 바이너리를 전량 다운로드하여 SHA-256/CRC32를 독립 재계산하지 않았다. 기존 배치의 성공 CI와 텍스트 해시 증거는 별개로 보존했다.

## 정식 36구간 상세 인덱스

| 번호 범위 | Draft PR | 개별 기록 | 조건부 | 보류 | 해당 브랜치 CI |
|---|---|---:|---:|---:|---|
|    1-10 | [#241](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/241) | 10 | 5 | 5 | 성공 |
|   11-20 | [#242](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/242) | 10 | 7 | 3 | 성공 |
|   21-30 | [#243](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/243) | 10 | 6 | 4 | 성공 |
|   31-40 | [#244](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/244) | 10 | 5 | 5 | 성공 |
|   41-50 | [#245](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/245) | 10 | 6 | 4 | 성공 |
|   51-60 | [#246](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/246) | 10 | 4 | 6 | 성공 |
|   61-70 | [#247](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/247) | 10 | 1 | 9 | 성공 |
|   71-80 | [#248](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/248) | 10 | 3 | 7 | 성공 |
|   81-90 | [#249](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/249) | 10 | 1 | 9 | 성공 |
|  91-100 | [#250](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/250) | 10 | 5 | 5 | 성공 |
| 101-110 | [#251](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/251) | 10 | 5 | 5 | 성공 |
| 111-120 | [#252](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/252) | 10 | 2 | 8 | 성공 |
| 121-130 | [#253](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/253) | 10 | 2 | 8 | 성공 |
| 131-140 | [#254](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/254) | 10 | 2 | 8 | 성공 |
| 141-150 | [#257](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/257) | 10 | 1 | 9 | 성공 |
| 151-160 | [#258](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/258) | 10 | 1 | 9 | 실행 확인 안 됨 |
| 161-170 | [#256](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/256) | 10 | 2 | 8 | 성공 |
| 171-180 | [#260](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/260) | 10 | 0 | 10 | 성공 |
| 181-190 | [#261](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/261) | 10 | 0 | 10 | 성공 |
| 191-200 | [#259](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/259) | 10 | 1 | 9 | 성공 |
| 201-210 | [#262](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/262) | 10 | 1 | 9 | 성공 |
| 211-220 | [#264](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/264) | 10 | 1 | 9 | 실행 확인 안 됨 |
| 221-230 | [#263](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/263) | 10 | 1 | 9 | 성공 |
| 231-240 | [#266](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/266) | 10 | 0 | 10 | 성공 |
| 241-250 | [#267](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/267) | 10 | 0 | 10 | 성공 |
| 251-260 | [#265](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/265) | 10 | 2 | 8 | 성공 |
| 261-270 | [#269](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/269) | 10 | 0 | 10 | 성공 |
| 271-280 | [#270](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/270) | 10 | 0 | 10 | 실행 확인 안 됨 |
| 281-290 | [#268](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/268) | 10 | 1 | 9 | 실행 확인 안 됨 |
| 291-300 | [#274](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/274) | 10 | 0 | 10 | 성공 |
| 301-310 | [#272](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/272) | 10 | 0 | 10 | 성공 |
| 311-320 | [#271](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/271) | 10 | 1 | 9 | 성공 |
| 321-330 | [#275](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/275) | 10 | 0 | 10 | 성공 |
| 331-340 | [#276](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/276) | 10 | 1 | 9 | 성공 |
| 341-350 | [#273](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/273) | 10 | 1 | 9 | 성공 |
| 351-357 | [#277](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/277) | 7 | 0 | 7 | 성공 |

## 검수 판정의 의미

- **CONDITIONAL (68):** 원본 가구와 Minecraft 후보의 일부 실루엣/색상/용도가 유사하지만 크기, 방향, 충돌, 재질, 텍스처 또는 멀티블록 조합 등이 검증되지 않았다. 자동 배치나 인게임 인증으로 승격하지 않는다.
- **DEFER (289):** 실제 모델 근거 부족, 외형·재질·색상·부품 구성 불일치, 크기·설치 위치 불일치 등의 이유로 다른 모드/바닐라/모델을 재검색해야 한다.
- 초기 001~020은 후속 CSV와 판정 코드가 달라 원본 상태 문자열을 보존하고 보수적으로 분류했다. `CLOSE_VISUAL_FUNCTION` 3건은 **조건부**(실제 인게임 인증 아님), `PROMISING_NOT_YET_BLOCKBENCH_VERIFIED`, `SEARCH_ANOTHER_MOD`, `VANILLA_FALLBACK_NOT_EXACT_NO_NATIVE_RENDER` 등 6건은 **보류**로 분류했다.
- `exact_1_to_1_approved`, `world_replacement_approved`, `game_verified` 중 YES/TRUE/1로 승인된 항목은 0건이다.

## 추가 독립 바이너리 SHA-256 표본 검사

마지막 351~357번의 **비교 JPG 7개**와 해당 **ZIP 1개**를 GitHub 원본 바이너리(base64)로 직접 읽어 SHA-256을 새로 계산했다. 8개 모두 원래 `SOURCE_SHA256.csv` 및 `ZIP_SHA256.txt`에 기록된 값과 정확히 일치했다. 바이트 수·기대 해시·재계산 해시는 `BINARY_SAMPLE_SHA256_351_357.csv`에 남겼다.

**이는 8개 표본의 해시 검증이지 36개 전체 배치 바이너리의 전수 검증은 아니다.** ZIP 내부 모든 항목의 CRC32를 별도로 풀어서 검사하지도 않았다.

## CI가 확인되지 않은 4개 독립 PR

1. [#258 — 151~160](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/258)
2. [#264 — 211~220](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/264)
3. [#270 — 271~280](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/270)
4. [#268 — 281~290](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/268)

위 4개는 GitHub 저장·검수 CSV·MANIFEST 존재를 확인했으나 **최근 500개 Actions 기록에서 해당 브랜치의 성공 실행을 찾지 못했다**. CI 성공이라고 단정하지 않는다.

## 중복·충돌·데이터 무결성

- PR #255의 131~140 사전점검과 PR #254의 정식 검수는 **범위가 겹치지만** 정식 범위 집계는 PR #254만 사용한다.
- 브랜치 이름의 `batch22`는 211~220과 221~230, `batch33`은 321~330과 331~340에서 재사용되었다. **브랜치명 숫자만으로 합산하지 않고 실제 가구 번호 구간과 PR ID로 구분**했다.
- 36개 상세 CSV의 Git blob SHA와 36개 manifest의 Git blob SHA를 인덱스에 보존했다. `source_csv_blob_sha`는 동일 구간 10행에 반복되므로 357행에 기록되지만 **고유 원본 파일은 36개**다.
- 개별 배치의 JPG SHA-256/ZIP CRC32 기록이 존재하더라도, 이번 독립 QA에서 바이너리 전체를 다시 계산하지 않았으므로 **바이너리 무결성 전수 인증은 미완료**다.
- 원본 TMX·PNG·SQLite, 기존 PR 및 다른 레인 브랜치를 수정하거나 병합하지 않았다. 결과는 독립 QA 브랜치에만 추가했다.

## 제공 파일

- `MASTER_INDEX_001_357.csv`: 357개 번호별 PZ 이름/스타일, 원본 상태 코드, 표준 판정, 사유, 재검색 요구, PR, Git blob SHA, 승인 플래그.
- `DEFERRED_BACKLOG_289.csv`: 보류 289종의 구체적 불일치 사유와 다음 조사 과제.
- `CONDITIONAL_RECHECK_068.csv`: 조건부 68종의 미검증 요소 및 재검수 목록.
- `BATCH_STATUS_36.csv`: 36개 구간별 검수·판정·CI·manifest 검증 상태.
- `QA_SUMMARY.json`: 통계·누락·중복·CI 미확인 목록·무결성 한계.
- `NORMALIZED_*.jsonl` 3개: 원본 CSV에서 변환한 357개 행. 원본 판정 문자열과 Git blob SHA 보존.
- `MANIFEST_AUDIT_*.jsonl` 3개: 36개 원본 manifest 스냅샷 및 Git blob SHA.
- `scripts/verify_rosewood_final_qa_357.py`: 구조·중복·판정·백로그 일치성 검사. JPG/ZIP 바이너리 검증은 하지 않는다.

## 보류 재검색 우선순위 (원본 PZ 분류명 기준)

보류 289종 가운데 **Counter 63종, Shelves 32종, Chair 29종, Table 27종**이 총 151종(52.2%)을 차지한다. 우선 이 네 가구 계열의 Forge 1.20.1 모델 원본·텍스처를 조사하면 가장 많은 보류 항목에 재사용 가능한 근거를 확보할 가능성이 있다. 전체 분류별 숫자는 `CATEGORY_PRIORITY.csv`를 참조한다.

## 미해결 과제와 다음 단계

1. 289개 보류 후보를 다른 Forge 1.20.1 가구 모드와 바닐라 모델에서 재검색하고 **원본 모델/텍스처의 전체 렌더**를 확보한다. 이름이 비슷하다는 이유만으로 매칭하지 않는다.
2. 68개 조건부 후보의 크기·방향·멀티블록 결합·색상·재질·충돌·상호작용을 실제 Minecraft 설치 환경에서 검증한다.
3. CI 미확인 4개 PR을 개별 재검증하고, 36개 배치의 JPG/ZIP SHA-256 및 CRC32를 **실제 바이너리로 독립 재계산**한다.
4. 개별 Draft PR은 현재 병합하지 않는다. 향후 별도 통합 절차에서 파일 충돌, 중복 브랜치 번호, 근거 데이터 누락을 해결해야 한다.

최종 결론: **개별 시각 검수 기록의 범위 확보 100.0%, 게임 적용 승인 0.0%.** 이 둘은 구분해서 보고한다.
