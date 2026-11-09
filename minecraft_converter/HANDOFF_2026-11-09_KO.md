# 작업 인수인계 — PZ B42 → Minecraft 맵 변환 (2026-11-09)

> **목적:** 새 채팅 또는 다른 개발자/AI가 이전 작업을 안전하게 이어가도록, 실제 완료 범위·사용자 확정 사양·데이터·재현 방법·금지사항을 분리한다.
> 
> **상태:** 원본 `31_46.tmx`에 기반한 **Minecraft Java 1.20.1 임시 프리뷰** 생성 완료. 최종 맵·원본 전체 모델링·상호작용 구현은 미완성. **원본 TMX/PZW/v259/타일 분석 DB는 변경하지 않는다.**

## 0. 지금 무엇을 하고 있는가

좀보이드 B42의 256×256 TMX 셀을 Minecraft 실제 월드의 전역 좌표에 1:1로 복원하는 프로젝트다. 사용자 스크린샷에서 첫 프리뷰는 밭이 잔디로 통일되어 있었고, 원본 `Tiles/2x/*.png`의 인덱스를 대조해 흙·고랑·밀·마른 줄기·침엽수·관목을 복원했다. 사용자는 게임에서 새 프리뷰를 직접 열고 넓은 밭·도로·나무 배치를 촬영했으며, **하늘색 유리는 아직 모델이 없는 가구의 임시 표시임을 확인**했다.

사용자가 **반복적인 설정 선택 질문을 중단하고 실제 작업 중심으로 진행**하도록 지시했다. 가구는 Codex가 따로 모델링 중이며, 모델을 변환기에서 강제로 줄이거나 형태/색상을 바꾸지 않고 그대로 배치한다. 이상하면 **모델 자체를 수정**한다.

## 1. 저장소에서 읽을 순서

1. [INDEX_KO.md](INDEX_KO.md) — 문서/파일 시작점
2. [PROJECT_STATUS_KO.md](PROJECT_STATUS_KO.md) — 실제 결과와 미완료 항목
3. [DECISIONS_KO.md](DECISIONS_KO.md) — 사용자 확정 원칙
4. [README.md](README.md) — 실제 코드 실행 방법과 한계
5. [converter.py](converter.py), [floor_stair_stage.py](floor_stair_stage.py), [tile_visual_audit.py](tile_visual_audit.py) — 구현 코드
6. [previews/31_46_report.json](previews/31_46_report.json)와 [previews/31_46_floor_stair_audit.json](previews/31_46_floor_stair_audit.json) — 현 생성물의 검증 수치
7. [NEXT_CHAT_PROMPT_KO.txt](NEXT_CHAT_PROMPT_KO.txt) — 그대로 복사 가능한 첫 메시지

저장소 https://github.com/sanato-nb/PZ_Tile_Analysis
작업 브랜치 `work/minecraft-31-46-preview-20261108` — [Draft PR #322](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/322). **`main` 병합은 승인 전까지 금지.**

## 2. 원본 파일·좌표 검증

- `B4220.3_MapExport_256/tmx/31_46.tmx`와 `B4220.3_MapExport_256/Kentucky.pzw`를 직접 읽어 cell `(31,46)`, `native-256`, `worldOrigin=(0,0)` 확인.
- Minecraft 월드 좌표 X `7936..8191` / Z `11776..12031` (TMX Y는 Minecraft Z).
- `31_46.tmx`: 타일셋 **413종**, CSV 레이어 **22개**, Level **0..6**, 타일 배치 레코드 **131,341건**, Level 0 바닥 `Floor` **65,536칸**.
- 원본 SHA256: `5eb55362bafb6235e6f609a65675f083189ebb8a706829d12bb9da0abcd39603` (현재 [프리뷰 보고서](previews/31_46_report.json) 값). 소스 변경 시 비교.
- 주의: Level 1~6의 타일은 주로 천장·지붕·기타 조각이다. 위층/지하층의 **검증된 보행 바닥은 현재 0칸**이며, 이것을 오류라며 임의 채우면 안 된다.

## 3. 현재 생성되는 월드의 내용

- 실제 Java Anvil 구조(`level.dat`, `.mca`), 가로 16×16 청크 × 16×16 = **256청크**.
- 바닥 Y=64, 아래 Y=63·62 흙, Y=61~57 돌. 빈 월드·평원 바이옴, 검수용 크리에이티브, 자연 몹 생성 중지, 낮·맑음 고정.
- 원본 `blends_natural_01`, `vegetation_farm_01` 등 PNG를 대조해 **갈색 밭·경작지**와 **익은 밀 17,571칸 / 마른 줄기 7,034칸** 생성. 바닐라 블록 근사이며 원본 PNG 텍스처 완전 일치는 아니다.
- 원본 침엽수 스프라이트 **172건** 및 관목 **261건**을 바닐라 나무/나뭇잎으로 근사. 보호 영역 밖으로 침범하는 잎은 잘라내며 보고서의 잘림 기록 **193**.
- 대형 나무 관련 **45건**은 원본 이미지/구조 확증이 부족해 미변환.
- 가구/가전 관련 원본 타일 부품 **164건** 중 **133칸**을 하늘색 유리 또는 카펫 임시 표시. 다칸 가구의 완성된 모델 객체가 아니라 **원본 타일 부품 단위 임시 배치**라는 한계가 있다. 유리는 원본 유리 물체를 뜻하지 않는다.
- 원본 레이어·타일 GID·방향 비트·좌표·후보 속성은 압축 로그로 내보낸다. `31_46_report.json`의 경고 24건은 **잔여 경고 일부**이며 정확도/검수율 점수가 아니다.

## 4. 계단/지하실 주의 (가장 중요한 오판 방지)

- 실제 `31_46.tmx`에 `fixtures_stairs_01` 및 에스컬레이터 타일 **0건**. 확인된 상층 보행 바닥 **0칸**.
- 원본 PZW에는 Basement 메타데이터 **1영역**이 있다. 로컬 `(72,119)`, 크기 `12×10`, 전역 `(8008,11895)`, StairDirection=W 및 StairX=1, StairY=0. 이는 **지하실 실물 공간이나 계단 블록의 물리 도면이 아니다**. 해당 땅을 파지 않았고 파서는 안 된다.
- `floor_stair_stage.py`는 원본 계단 3타일 + 검증된 다음 층 착지 1칸이 확인된 경우에만 단계적 계단을 계획하며, 원본이 없으면 생성 거부.
- `previews/stairs_3plus1_walkability_demo.zip`은 3계단+착지 동작을 시험하려고 **독립 제작한 합성 월드**이다. 실제 `31_46`에 있는 구조라고 말하면 안 된다.
- 게임 안에서 실제 보행 가능 여부의 사용자 직접 검수는 미완료.

## 5. 확정 설계 중 미구현인 것

`DECISIONS_KO.md`가 전체 기준. 현재 *선호한 사양*과 *실제 구현*을 항상 분리할 것.

- 물/수심/바닥 재질·단계별 깊이, 도로 차선·횡단보도·정지선 커스텀 텍스처, 전체 식생과 실제 형태는 미완성.
- 외벽·문·창·지붕, 차량·도로 시설물, 울타리, 조명 일부, 오염은 1차 작업에서 의도적으로 제외(원본 자료는 보존).
- Codex 3D 가구 실제 모델 연결·앵커/방향/다칸 병합/충돌·상호작용은 미완료; 현재 유리 플레이스홀더만 있음.
- v259 2D 평면도 엔진을 자동 오류 지도와 연계하는 것, CSV+JSON 검수 보고서 통합, 청크별 체크포인트/재개, 인접 경계 자동 보정, 안전한 본월드 구역 교체는 향후 구현할 설계.
- 최종 Minecraft 버전 및 모드 로더는 미정. **DataVersion 3465 / Java 1.20.1은 프리뷰 전용**.
- **원본 뜻을 모르는 타일을 이름만 보고 가구/나무/바닥으로 확정 금지.** 별도 타일 시각 분석 DB의 '이미지를 봄'과 '정체 인증'을 혼동하지 않는다.

## 6. 검증/재현 명령

저장소 루트에서 Python 3.9+:

```bash
python -m unittest discover -s minecraft_converter/tests -v
python minecraft_converter/converter.py \
  --tmx B4220.3_MapExport_256/tmx/31_46.tmx \
  --pzw B4220.3_MapExport_256/Kentucky.pzw \
  --v259-html floorplan/current/v259_floorplan.html \
  --output minecraft_converter/output \
  --preview-world --data-version 3465
```

테스트/자동화: [워크플로](../.github/workflows/pz-minecraft-31-46-preview.yml), [성공 실행 #42551539062](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/42551539062).

생성 결과:
- `output/31_46_preview_world.zip`: 실제 31_46 프리뷰
- `output/report.json`, `output/floor_stair_audit.json`, `output/warnings.csv`
- `output/source_placements.jsonl.gz`, `output/edges.json`, `output/furniture_parts.json`
- `output/stairs_3plus1_walkability_demo.zip`: **합성 테스트 월드**

CI 업로드 아티팩트는 기본 **14일 보존**, 반면 `previews/`의 월드 ZIP/보고서/별도 계단 데모는 작업 브랜치에 남는다. 원본 보존이 최우선이며, ZIP과 `report.json`의 숫자는 재생성 시 다시 확인한다.

## 7. 실제 작업 우선순위

1. **지금 바로:** `31_46`의 도로 표시·가장자리·트랙/흙길·작은 식생·대형 나무 등 빠진 시각 요소를 원본 TMX+PNG 기준으로 검증·매핑하여 업데이트. 현재 사용자 비교 스크린샷을 시각적 회귀 근거로 이용하되 '대략 유사'와 '정확히 일치'를 구분.
2. 원본에서 확인된 실내/건물 바닥만 적용. 현재 31_46은 확인된 상층 바닥이 없으므로 강제로 생성하지 말 것.
3. 향후 다른 TMX 구역에서 실제 계단 데이터를 확보하면 3단+착지 1칸·4블록 층고 통행 검수.
4. Codex 가구 모델 파일이 실제로 준비되면 연동표·방향·기준점·다칸 객체로 교체. **모델 외형 수정은 Codex 모델 측에서**.
5. v259 기반 오류 지도, 기계 판독용 CSV/JSON, 경계·체크포인트·증분 생성 기능을 추가하면서 구역 확대.

## 8. 진행 방식·보안 및 인수인계 원칙

- 개발을 진행하다 꼭 필요한 결정이 없는 한 사용자에게 연속 선택지를 제시하지 말 것.
- 기존 `main`·원본 TMX·PZW·PNG·v259·타일 DB·다른 가구 브랜치는 수정/삭제/병합하지 말 것.
- 현재 Draft PR #322의 브랜치에서 구현·검수 후 링크와 변경 파일, 직접 검증한 숫자만 보고할 것.
- 파일이 실제 실행·GitHub 저장/다운로드되기 전 성공이라고 말하지 말 것.
- CI 통과는 **게임 화면/충돌/보행 검증 통과를 뜻하지 않음**. 실제 Minecraft 실행은 스크린샷으로 사용자 검수 받았던 범위만 기록.
- 다른 채팅 시작 메시지는 [NEXT_CHAT_PROMPT_KO.txt](NEXT_CHAT_PROMPT_KO.txt) 그대로 사용.
