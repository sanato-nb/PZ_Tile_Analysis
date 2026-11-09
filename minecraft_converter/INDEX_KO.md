# PZ B42 → Minecraft 맵 변환: 작업 안내 (2026-11-09)

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
