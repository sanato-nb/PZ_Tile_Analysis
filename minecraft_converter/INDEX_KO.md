# PZ B42 → Minecraft 맵 변환: 작업 안내 (2026-11-09)

> **31_45 신규 지형 전용 프리뷰:** [TERRAIN_ONLY_31_45_KO.md](TERRAIN_ONLY_31_45_KO.md)에서 가구/벽/전봇대 등 오브젝트 제외 규칙과 실제 검증 범위를 확인. `--terrain-only`를 사용하고 `31_46` 결과는 유지한다.


> **31_45 추가 시범 월드 (별도 브랜치):** [31_45 작업 상태](31_45_STATUS_KO.md) · [31_45 Java 월드 ZIP](previews/31_45_preview_world.zip) · [GitHub Actions #42568702826](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/42568702826). 본 브랜치의 31_45 결과는 기존 31_46 결과와 분리하여 보존한다.


> **최신 후속 작업 (2026-11-09):** 도로선 695 + 노란 연석 93 = **788칸**, 저층 식생 **12,754칸**을 실제 원본 TMX/PNG 기준으로 추가했다. [검수 문서](ROAD_TERRAIN_STAGE_2026-11-09_KO.md) · [실측 감사 JSON](previews/31_46_road_terrain_audit.json) · [새 변환 모듈](road_terrain_stage.py) · [성공한 CI #42560863076](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/42560863076). 이후의 과거 요약에서 '도로 표시 미완성'은 정밀 재현/게임 내 검수의 미완성을 뜻한다. 최신 월드에는 간이 도로 표시가 포함된다.


**여기부터 읽기.** 이 폴더는 Project Zomboid B42의 TMX를 Minecraft Java 월드로 옮기는 **실제 변환기 프로젝트**다. 타일 전체 시각 분류(v31 등) 및 가구 모델링 프로젝트의 모든 결과가 이 폴더에 포함된 것은 아니다.

- **현재 상태·검증·제약:** [PROJECT_STATUS_KO.md](PROJECT_STATUS_KO.md)
- **확정한 설계 원칙:** [DECISIONS_KO.md](DECISIONS_KO.md)
- **상세 인수인계:** [HANDOFF_2026-11-09_KO.md](HANDOFF_2026-11-09_KO.md)
- **새 채팅 첫 메시지:** [NEXT_CHAT_PROMPT_KO.txt](NEXT_CHAT_PROMPT_KO.txt)
- **실행 명령 및 기술 내용:** [README.md](README.md)
- **변환기:** [converter.py](converter.py)
- **바닥·계단 검증:** [floor_stair_stage.py](floor_stair_stage.py), [stair_walkability_demo.py](stair_walkability_demo.py)
- **자동화:** [pz-minecraft-31-46-preview.yml](../.github/workflows/pz-minecraft-31-46-preview.yml)
- **실제 원본 분석:** [31_46_source_audit.json](31_46_source_audit.json)
- **월드 및 감사 기록:** [previews/](previews/)

## 브랜치 / 리뷰
- 기준 브랜치: `work/minecraft-31-46-preview-20261108`
- 진행 리뷰: [Draft PR #322](https://github.com/sanato-nb/PZ_Tile_Analysis/pull/322)
- `main`에 자동 병합하지 않는다. 완료되지 않은 기능을 완료로 표기하지 않는다.
- 최신 성공 실행 기록: [GitHub Actions #42551539062](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/42551539062)

## 실행 파일 구분
`previews/31_46_preview_world.zip`은 **실제 31_46 지형 기반 검수용 월드**, `previews/stairs_3plus1_walkability_demo.zip`은 **원본에 없는 합성 계단 시험 월드**다. 절대 혼합하거나 계단을 실제 TMX 배치로 주장하지 말 것.

원본 전체 배치 로그 `previews/31_46_source_placements.jsonl.gz`, 구역 경계 `previews/31_46_edges.json`, 가구 타일 부품 `previews/31_46_furniture_parts.json`은 **작업 브랜치에 계속 보존**한다. CI 아티팩트도 별도로 생성되지만 14일 후 만료될 수 있다. 재구성에는 원본 TMX/PZW와 `converter.py`를 사용한다.
