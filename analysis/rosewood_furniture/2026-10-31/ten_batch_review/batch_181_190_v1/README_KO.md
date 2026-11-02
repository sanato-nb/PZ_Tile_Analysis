# 로즈우드 가구 19차 — 181~190 수동 시각 재검수

- 날짜: 2026-11-02 (KST)
- 독립 레인 C / 원본 기준: `work/rosewood-manual-batch10-091-100-20261101`
- 이번 범위: 181~190번 정확히 10종, 다른 레인의 171~180·191~200번은 건드리지 않음
- **시각적으로 조건부 승인한 완성형 가구: 0종. 보류: 10종. 인게임 1:1 인증: 0종.**
- 실제 한 작업: GitHub에 저장된 **PZ 완성형 10장과 원본 모드 렌더/모델 9건의 좌우 비교 JPG를 각각 육안 재판독**, PZ 원본 프리뷰 10장 재확인, #189에 대해 실제 Macaw's dark-oak 옷장 네이티브 렌더 추가 확인, 잘못된 기존 후보 9건 명시적으로 보류.
- **새 Blockbench 실행/새 렌더링/실제 Forge 게임 실행은 수행하지 않음.** 기존 비교 JPG 10장은 원본 파일을 그대로 복사한 증거이며, 기존 이미지에 적힌 `NOT_VISUALLY_REVIEWED`는 **이미지 생성 당시 상태**이다. 본 문서와 CSV가 2026-11-02 수동 재판독 기록이다. 기존 JPG를 새로 렌더했다고 주장하지 않음.
- 원본 PZ PNG 10장, 비교 JPG 10장, Macaw's dark-oak 대체 렌더 1장을 별도 보관. SHA-256은 JPG 10장과 대체 렌더 1장에 대해 직접 계산하여 `SOURCE_SHA256.csv`에 기록함. PZ PNG는 Git blob SHA-1과 원본 경로로 추적 가능하며 이번 SHA-256 표에는 포함하지 않음.

## 10종 재판독 요약

| 번호 | 원본 PZ 가구 | 기존 MC 후보 | 판정과 이유 |
|---|---|---|---|
| 181 | Deluxe / Espresso | NONE | **보류** — 은색 상판과 검정 본체, 전면 다중 추출구·노브·드립 트레이가 있는 소형 탁상형 에스프레소 머신. 실물 MC 모델 증거 없음. |
| 182 | Counter / Bar Corner | decocraft:diner_counter_corner_black | **보류** — PZ는 따뜻한 갈색 목재의 ㄱ자 홈이 있는 평면 상판과 목재 측면. MC는 검정·흰색 수평 줄무늬의 모서리 카운터로 코너 형상만 유사하며 재질·색·패널 전부 다름. |
| 183 | Counter / Cantina Food | mcwfurnitures:acacia_counter | **보류** — PZ는 금속 음식 진열대·유리 상부 후드·지지대·급식용 트레이. MC는 단순 불투명 아카시아 통나무 카운터로 유리 후드·트레이가 전혀 없음. |
| 184 | Cabinet / China | mcwfurnitures:acacia_double_kitchen_cabinet | **보류** — PZ는 2칸 가로폭의 진한 목재 장식장으로 상부 유리문 3칸과 하부 서랍·수납장 결합. MC는 낮은 불투명 회색·주황색 주방장 1블록 파트로 2×1 전체 조립·유리문·높이 미재현. |
| 185 | Counter / Oakwood Floating | mcwfurnitures:acacia_counter | **보류** — PZ는 벽에 매다는 밝은 갈색 2문 상부 수납장으로 바닥과 떨어진 설치·문손잡이가 특징. MC는 바닥형 아카시아 카운터 단순 덩어리로 부착 방식과 문 형태 모두 다름. |
| 186 | Locker / Green Wall | decocraft:locker_green | **보류** — PZ는 어두운 녹회색의 낮고 넓은 벽형 양문 철망/천공문 로커. MC의 locker_green 소스 렌더는 파란색 단일 높은 문과 자물쇠·루버가 보여 색상·문 수·비율이 모두 다름. |
| 187 | Shelves / Generic Cooled | handcrafted:acacia_shelf | **보류** — PZ는 흰색 높은 오픈형 다단 냉장 진열대, 전면 4~5단 선반과 상단 캐노피가 있음. MC는 갈색 목재 2칸 서랍형/책장형 모델로 개방형 선반·냉장 기능·재질이 불일치. |
| 188 | Shower / Wall | pfm:basic_shower_handle | **보류** — PZ 원본은 벽의 샤워 헤드와 여러 조절 밸브가 분리된 모습. MC는 작은 단일 손잡이 부품으로 샤워 헤드·배관·설치 높이·방향이 빠져 있음. |
| 189 | Wardrobe / Dark Fancy | mcwfurnitures:acacia_double_wardrobe | **보류** — PZ는 검정색 키 큰 2단 옷장, 양문 중앙에 가는 은색 손잡이. MC 아카시아는 회색·주황색이며 불일치. 별도 확인한 dark_oak_double_wardrobe 실제 렌더는 색감은 더 낫지만 문손잡이·상하 1×2 전체 결합이 검증되지 않음. |
| 190 | Counter / Spiffos | mcwfurnitures:acacia_counter | **보류** — PZ는 주황색 상판, 붉은 갈색 몸체, 녹색 가로띠가 있는 스피포스 카운터. MC 아카시아는 회색 몸체·갈색 상판으로 프랜차이즈 색상과 패널 구조가 없음. |

## 확인한 중요한 오류

1. **182 바 코너:** 코너의 꺾인 윤곽만 일부 비슷하며, PZ 갈색 목재와 MC 검정·흰색 줄무늬 외장은 완전히 다름. 색·재질 불일치를 1:1로 오인하면 안 됨.
2. **184 중국식 장식장:** PZ 2×1 가로 장식장 + 상부 유리문/하부 서랍. Macaw's 단일 주방장 파트는 전체 가구가 아님.
3. **185 공중 수납장:** PZ `IsHigh` 및 `MoveType=WallObject`; MC 아카시아 카운터는 바닥 설치형이므로 공간 배치가 잘못됨.
4. **186 녹색 벽형 로커:** `decocraft:locker_green`의 기존 Blockbench 렌더는 파란색 높은 단문 로커로 표시됨. 이름의 green만 보고 통과하면 안 됨.
5. **187 냉장 선반:** PZ `container=fridge`, 전기 부품과 흰색 오픈 선반. 일반 목재 선반은 냉장 진열대 대체로 부적합.
6. **188 벽 샤워:** 단일 샤워 핸들만 있는 모델을 샤워 헤드·밸브가 포함된 전체 샤워기로 판정하지 않음.
7. **189 검정 옷장:** `mcwfurnitures:dark_oak_double_wardrobe` 실제 원본 렌더를 추가 비교했으나 어두운 색만 유사함. PZ 1×2 전체 상하 조립, 검정 표면, 은색 세로 손잡이 재현은 확인되지 않아 승인하지 않음.

## 파일

- `cards/181_PZ_MC.jpg` ~ `cards/190_PZ_MC.jpg`: **기존 원본 비교 이미지 10장** (새로 생성하지 않음)
- `pz_previews/`: PZ 완성형 원본 이미지 10장
- `alternatives/189_macaws_dark_oak_double_wardrobe.png`: Macaw's dark oak 옷장 기존 실제 소스 모델 렌더
- `BATCH_181_190_MANUAL_VISUAL_REVIEW.csv`: 개별 가구 수동 판정 및 근거
- `BATCH_181_190_DEFERRED_OTHER_MODS.csv`: 10종 보류 및 재검색 지시
- `SOURCE_SHA256.csv`: 11개 재사용 증거 이미지 SHA-256
- `MANIFEST.json`: 범위·상태·근거 출처

## 출처·한계

기존 근거는 이 저장소의 `analysis/rosewood_furniture/2026-10-31/all_357_complete_native_comparisons_v1/cards/`, `complete_furniture_visual_3d_v1/previews/`, `native_real_mod_models_remaining_v1/`에서 가져옴. 모드의 원본 `.bbmodel`/JSON·텍스처를 직접 새로 열거나 런타임 설치하지 못했으므로 기존 원본 렌더의 출처 메타데이터에 의존한다. 실물 기능, 충돌 판정, 방향·설치 높이·멀티블록 결합은 별도 Minecraft Forge 1.20.1 실행 검증 전까지 **미인증**. 전체 357종의 최종 승인과는 구분하여 수동 검수 기록 수만 누적한다.
