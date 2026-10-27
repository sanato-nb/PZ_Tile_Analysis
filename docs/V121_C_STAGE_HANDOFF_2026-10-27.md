# v121 C단계 작업 중단 후 인수인계 (2026-10-27)

**상태:** 사용자 채팅 중단과 관계없이 C단계 GitHub Actions [40354707694](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40354707694)는 **completed / success**로 종료됨. 원본 B 재현·C 이미지·B−C 이미지 검증·artifact 업로드·브랜치 커밋 모두 성공. 따라서 처음부터 재실행할 필요 없음.

## 범위와 단계

- 84개 TMX (`26_43` ~ `37_49`, x=26~37/y=43~49); 전체 고유 **10,042종** = 기존 분석 5,409 + 새 4,633.
- **기존 5,409종은 새 A/B/C 분석 대상에서 제외**, 기존 결과만 재사용. 14개 사용자 검수 제외 이력 보존(투명 인증 아님).
- 새 4,633종 중 **`overlay_graffiti_wall_02/2` 1종 정확한 PNG 미확보로 보류**, 나머지 **4,632종**이 A/B/C 대상.
- A v119: 대표 원본 RGBA PNG **4,632종** (A1 1,544; A2 3,068; JUMBO 잠정 A3 20) · 원본 SHA 보관. B v120: 실제 TMX 층/레이어/좌표/GID 기반 5×5 **4,632장**, 58접촉시트.
- **C v121 실제 완료**: 원본 GID 1개만 동일 층·레이어·좌표에서 빼서 C **4,632장** 생성. 원래 B WebP **4,632건 바이트 동일 SHA 재현 검증 통과**. B−C 차이 PNG **4,632장**.
- v121 계산 결과: **4,417종 픽셀 변화 있음 / 215종 0픽셀**, C ZIP 12개, 차이 PNG ZIP 12개, B/C/Diff 3열 비교판 58장. ZIP CRC/SHA 모두 성공.
- **D(두 번째 맵 배치)**는 아직 수행하지 않았다. 공식 Local ID/TileZed 매핑 검증, 타일 정체 최종 인증은 0종. 최신 물리 통합 SQLite는 **v116**으로 **변경하지 말 것**.

## 다음 채팅에서 즉시 열 파일

| 성격 | 파일 경로 |
|---|---|
| 진행 및 규칙 | `PROJECT_STATE.json`, `AGENTS.md`, `docs/HANDOFF.md` |
| C 사실/근거 통계 | `review/v121_C_diff_new4632/MANIFEST.json` |
| C 대상별 메타데이터 | `review/v121_C_diff_new4632/C_B_DIFFERENCE_4632.csv` |
| C 원본 4,632장 | `review/v121_C_diff_new4632/c_png_shards/` (ZIP 12개) |
| B−C 빨간 차이 원본 | `review/v121_C_diff_new4632/difference_png_shards/` (PNG ZIP 12개) |
| 3열 비교판 58장 | `review/v121_C_diff_new4632/sheets/C_B_DIFF_000.jpg` ~ `057.jpg` |
| 차이 0으로 판정된 목록 | `review/v121_C_diff_new4632/ZERO_DELTA_REVIEW.csv` |
| 실제 생성·검증 코드 | `scripts/v121_generate_C_diff_new4632.py`, `.github/workflows/v121-C-difference-4632.yml` |
| B 좌표/원본 증거 | `review/v120_B_context_new4632/B_CONTEXT_4632.csv`, `PLACEMENTS_4632.csv` |
| 신규 A와 원본 해시 | `review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv` |

큰 `C_B_DIFFERENCE_4632.csv`를 GitHub 커넥터 `fetch_file`로 불러오면 내용이 빈 것처럼 보일 수 있음. 이는 API 대용량 반환 문제일 수 있으니 Actions와 원본 파일을 기준으로 확인.

## **품질 검증 미완** (매우 중요)

1. `scripts/v121_generate_C_diff_new4632.py`의 `difference_exact()`는 RGB 채널 차이를 `.convert('L')`로 변환 후 0 아닌 값을 세는데, 명도 반올림 때문에 **작은 특정 RGB 채널 변화가 0으로 소실될 가능성**이 있음. 215건 zero-delta는 **RGB 채널 OR 방식으로 재검증**해야 함. 위 4,417/215는 현 버전 계산 결과(잠정), 최종 정밀 변화 분류 아님.
2. B와 C가 같아도 가림, 캔버스 잘림, 잘못된 A/Local ID 맵핑, 레이어 문제 가능. **투명 타일이라고 판정하지 말 것.**
3. v119 A1/A2/A3는 대표 이미지 잠정 배정이고 공식 매핑 인증 아님. JUMBO 20종의 원본 프레임 경계에 이웃 나무가 섞일 수 있음.
4. B 장면 중 8건은 주변 PNG 누락, 48건은 지도의 5×5 경계 잘림, 23,823회는 개별 큰 스프라이트 드로잉의 캔버스 잘림(=실패 장면 수 아님).
5. `scripts/v121_make_C_browser.py`는 존재하지만 `review/v121_C_diff_new4632/C_B_DIFF_BROWSER_4632.html`은 아직 생성된 것으로 확인되지 않음. 필요 시 브라우저 생성 및 검증.
6. 사용자가 폐기하라고 한 과거 TMX→마크 평면도 엔진을 다시 사용하지 말 것.

## 작업 재개 순서

1. GitHub `main` 및 v121 브랜치/PR/상태 파일을 확인하고 **완료된 C 소스와 증거를 보존하여 인계·병합**.
2. 가장 먼저 B−C 0픽셀 215종부터 정확한 RGB 채널 OR 차이 여부 재검증, 필요하면 전체 수치 정정.
3. B/C/차이 이미지 58장을 직접 시각 검토하여 벽·전선·기기·가구·큰 나무의 부품 정체를 판독; provisional/held/certified 상태 엄격 구분.
4. 필요 시 15×15 주변 확장. 다음 단계 D는 실제 다른 배치가 **존재할 때만** 생성(없으면 없음).
5. 기존 v116 SQLite, 원본 PNG/TMX, 5,409종 이력, 사용자 제외 14종 보존. 공식 맵핑 미인증 상태에서 Minecraft 블록에 확정 배정하지 말 것.

**이 문서를 새 채팅에서 먼저 읽고 실제 GitHub 연결로 계속 작업할 것. 계획만 쓰고 끝내지 말 것.**

- 기준 GitHub 원격: https://github.com/sanato-nb/PZ_Tile_Analysis
- 기록 브랜치: `work/v121-C-diff-new4632-20261027`
- 실행 성공: https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40354707694
- v121 메타데이터 SHA-256: `d462eb0f02cec4072be20aabc7201ab9d87284db1978c9d2d18058fb12748733`
