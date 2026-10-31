# v249 — v248에서 다른 실제 배치를 찾아도 B−C=0이던 보류 38종의 정확한 가림 스프라이트 추적

**사용자 요청을 이어서 진행:** 다른 실제 TMX 위치가 없는 188종은 다시 검수하지 않고, 251종에 대한 v248 증거를 기반으로 기존 **38종 B−C=0**을 원본 A 우선으로 재감사했다. 이번 결과는 **38개 각 키마다 원래 TMX 배치에서 그려지는 순서의 정확한 raw GID**까지 조사한 것이다. 이전 v248의 '가림 원인 불명' 상태를 실제 renderer draw-order 진단으로 보완하지만 **최종 사물명 인증 또는 원장 비활성 해제는 하지 않는다**.

## 물리적으로 실행한 실험

- v248에서 기록한 각 키의 **정확한 다른 TMX 파일/층/레이어/x/y/raw GID**를 다시 열어 원본 TMX SHA-256, 원본 A RGBA SHA-256을 검사했다. 38종 모두 이전 B−C=0 결과를 픽셀 단위로 재현했다.
- 타일을 **실제 원래 순서에서 그리자마자** B/C 픽셀 차이를 측정하고, 그 뒤 5×5 원래 장면을 그리는 **각 다른 실제 sprite**마다 그 차이가 줄어드는지 검사했다. 정확한 원인 행에는 각 suppressor의 TMX 레이어/층/x/y/raw GID/키/감소한 픽셀 수가 있다.
- 38종 **전부 A의 비투명 픽셀 존재**, **38종 전부 목표 스프라이트 직후 RGB 차이 양수**, **38종 전부 최종 원래 B−C=0**이다. 원인이 뒤에 그린 원래 소스 스프라이트에 있음을 재현했다.
- 직접적으로 픽셀 변화를 줄인 후속 스프라이트 그리기 동작은 **139건**. **같은 레이어 내 다음 셀 52건**, **후속 레이어 87건**이다. 38키의 원인 위치 분포는 **같은 레이어만 8 / 뒤 레이어만 14 / 둘 다 16**이다.
- 원래 B/C 외에 **'target last'** 진단 이미지를 따로 만들었다. 이는 목표 A를 맨 끝에 그렸을 때 시각적으로 나타나는지를 비교하기 위한 **진단 실험**이며, 원래 게임 상태의 B 또는 사용자 정의 D가 아니다.
- 38종의 직접 원본 A를 개별적으로 다시 본 뒤 **형태·연결 후보·남은 의문**을 모두 개별 기술했다. 예: `appliances_laundry_01/6` 상단 뚜껑과 측면 호스가 있는 미색 세척 가전형, `appliances_refrigeration_01/36` 검은 세로 그릴 기기, `walls_exterior_roofs_08/24,25` 삼각 박공 벽면, `location_entertainment_theatre_01/172`는 매우 작은 독립 회색 픽셀뿐이므로 **이전의 긴 금속 프레임 추정이 원본 A로 뒷받침되지 않음**을 명시했다.

## 상태 숫자 (중복 없는 고유키)

| 원인/재검수 | 38종 |
|---|---:|
| 목표 A 원본 픽셀 SHA 확인, 비투명 | **38** |
| 원래 TMX B−C=0 재현 | **38** |
| 목표가 처음 그려진 직후 픽셀 차이 양수 | **38** |
| 실제 후속 raw GID 픽셀 가림 감소 이벤트 | **139** |
| 동일 레이어 안에서만 가림 | **8키** |
| 후속 레이어에서만 가림 | **14키** |
| 동일 레이어와 후속 레이어가 함께 가림 | **16키** |
| A 원본 직접 상세 형태·부품 후보 기록 | **38키** |
| 공식 Local ID/TileZed/최종 사물명 인증 | **0** |

### 구체적인 가림 원인 예

| 목표 | 마지막으로 가리거나 가장 많은 부분을 덮은 원본 타일 후보 | 이 실험에서 직접 보인 현상 |
|---|---|---|
| `appliances_laundry_01/6` | `walls_interior_house_03/21` | 같은 레이어의 기기 타일과 벽 조각으로 완전 가려짐 |
| `appliances_refrigeration_01/36` | `walls_exterior_house_01/1` | 옆 기기 타일에 일부 가리고, 다음 레이어의 외벽에 완전히 덮임 |
| `appliances_refrigeration_01/43` | `walls_commercial_01/48` | 같은 레이어의 옆 설비·상업용 벽 조각에 가려짐 |
| `floor_carpet_motif/5` | `walls_interior_house_03/20` | 바닥 문양 일부가 같은 층 구조물에 덮임 |
| `overlay_blood_floor_01/7` | `walls_commercial_01/48` | 원래 바닥 혈흔이 후속 벽/설비 렌더로 사라짐 |
| `walls_exterior_roofs_08/24` | `roofs_accents_01/28` | 지붕 박공벽 조각이 다른 원본 지붕 파트로 가려짐 |

**주의:** '가림'은 이번에 검증한 원본 TMX의 5×5 렌더러 그리기 순서상 RGB 픽셀 증거다. **게임 클라이언트의 가림 엔진이 공식적으로 똑같이 처리한다는 별도 인증은 아님**. 또한 최종 화면에서 보이지 않는 것은 타일이 존재하지 않거나 투명하다는 증거가 아니다.

## 보존 결과 파일

- [ALL_38_EXACT_OCCLUDER_CAUSE_KO.csv](ALL_38_EXACT_OCCLUDER_CAUSE_KO.csv) — 고유 키별 **실제 가림 원인 범주**, 가장 강한 뒤쪽 sprite key, raw GID와 원래 A 후보
- [A_FIRST_38_INDIVIDUAL_MORPHOLOGY_AND_PARTS.csv](A_FIRST_38_INDIVIDUAL_MORPHOLOGY_AND_PARTS.csv) — 38개의 **독립 A 원본 형태 직접 관찰**, 잠정 부품·정체, 무엇을 아직 확정 못하는지
- [EXACT_FOLLOWING_GID_CAUSAL_PIXEL_CHANGES.csv](EXACT_FOLLOWING_GID_CAUSAL_PIXEL_CHANGES.csv) — 139개 원래 가림 tile source key, TMX 좌표/층/레이어/raw GID, 직전·직후 픽셀 변화
- [38_TARGET_STEPWISE_OCCLUSION_DIAGNOSTICS.csv](38_TARGET_STEPWISE_OCCLUSION_DIAGNOSTICS.csv) — 38개 대상의 단계별 실제 B−C, RGBA, 가림 이벤트
- [원본 A와 잠깐 맨 위로 복원한 진단 사진 1](ALL38_ORIGINAL_A_VS_UNCOVERED_00.png), [진단 사진 2](ALL38_ORIGINAL_A_VS_UNCOVERED_01.png)
- `####_OCCLUDER_CAUSAL.png` **38개** — A 원본/실제 B/실제 C/target-last 진단 전체 시각 비교.
- [MANIFEST.json](MANIFEST.json) — 실험 수량·범위 및 한계.
- [v248 251종 잠정 부품 원장](../v248_held251_full_alternate_BC_2026-10-30/ALL_251_A_FIRST_OBJECT_PART_HYPOTHESES.csv) — **이 원장의 과거 보류 상태는 변경하지 않았다.**

**다음 우선 검수:** v248의 계열 수준에 그친 나머지 130종과 **큰 단색 붉은 영역이 포함된 원본 A 13종**을 원본 RGBA·부품 연결·실제 배치로 다시 검증해야 한다.

기존 v240 전체10,042 / 활성9587 / 비활성455, 사용자 보류/수동 제외, 원본 PNG/TMX, 기존 SQLite DB·과거 자료는 불변이다. 새로운 정체 공식 인증 **0**이다.
