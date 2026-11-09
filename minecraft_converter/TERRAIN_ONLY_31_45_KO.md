# 31_45 바닥·층·나무·식생 전용 프리뷰 — 2026-11-09

> **실제 빌드 검증 성공 — GitHub Actions #42573144228 (2026-11-09):** 14/14 Python 단위 테스트 통과, 실제 256개 Anvil 청크 NBT의 전체 블록 팔레트 화이트리스트 검사 통과. 생성한 `previews/31_45_preview_world.zip` 내 가구 플레이스홀더·벽·전봇대·문·계단 등 **물리 오브젝트 생성 0건**, `preview_scope=terrain_floors_trees_vegetation`. 지표면 65,536칸, 지하·상층 바닥 총 12,160칸(지하 1,162칸 포함), 도로 표시 1,620칸, 낮은 식생 **10,911칸**(녹색 풀 9,943·마른 풀 514·지피식생 454). 나무 줄기 블록 4,306개, 관목 블록 1,016개. 원본 타일 배치 170,836건과 가구 부품 5,003건은 감사 로그로 보존하지만 월드에는 가구를 만들지 않는다. 미확정 대형 나무 49건과 계단 연결·정확한 도로/건물 바닥 재질은 여전히 미구현. **마인크래프트 실제 인게임 육안 검수는 아직 별도 필요.** [CI 결과](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/42573144228) · [실제 ZIP](previews/31_45_preview_world.zip) · [보고서](previews/31_45_report.json).


## 이번 사용자 지시
`31_45.tmx` 프리뷰에서 **가구, 벽, 문, 창문, 전봇대, 가로등, 표지판, 차량, 울타리, 난간, 지붕 등 구조물과 인공 오브젝트 전부 물리 생성 제외**. 마인크래프트 월드에는 바닥·층별 바닥·나무·식생만 구현한다. 도로·주차장 노면 및 표시선은 바닥 재질이므로 유지한다. 작물은 식생으로 유지한다. **계단은 아직 실제 연결이 검증되지 않아 미생성**.

## 실제 구현
- `minecraft_converter/converter.py`에 `--terrain-only` 옵션. 지금은 `31_45` 독립 GitHub Actions에서 이 옵션을 반드시 지정한다.
- 원본 Level 0 `Floor` Y64, 확인된 지하(-1)·상층(1..4) 바닥 및 안전한 지하층 셀 공간, 기존 도로 표시 Y64, 농경지, 작은 나무·관목·풀은 유지한다.
- 기존 하늘색 유리·카펫 `furniture` 배치를 완전히 비활성화한다. **객체 블록 생성 예상 0개**. 가구·전봇대 등 원본 오브젝트 데이터는 `source_placements.jsonl.gz`, `furniture_parts.json`에서 유지하므로 삭제·재매핑은 하지 않는다.
- 외형이 확인되지 않은 Level 0 `Floor` 가족의 임시 **분홍색 마젠타 블록을 중립적인 연회색 바닥 블록**으로 표시한다. 이것은 원본 재질 확정이 아니라 미매핑 바닥 표시 방법의 변경이다.
- `TERRAIN_ONLY_MATERIALS` 화이트리스트로 직렬화 **직전 모든 청크의 블록 재질을 검사**. 가구 유리·카펫/벽/문/유리창/전봇대/등/계단/울타리/차량 등 원치 않는 모델 블록을 막는다.
- CI: 신규 `tests/test_terrain_only_policy.py`로 허용/금지 블록 회귀 검증, 실제 256청크 Anvil NBT의 팔레트를 전수 검사, 원본 해시·층별 바닥·월드 ZIP·리소스 팩 무결성 검사.
- 출력: `minecraft_converter/previews/31_45_preview_world.zip`은 새로운 지형 전용 ZIP으로 갱신한다. 기존 `31_46` 브랜치와 그 월드 ZIP은 변경하지 않는다.

## 중요한 한계
- 이 모드는 **오브젝트 생성을 의도적으로 제외**하는 것이며, 좀보이드 원본에서 실제 오브젝트가 없는 맵이라는 뜻이 아니다.
- 상층 바닥은 원본 `floors_*` 타입과 PZW 좌표에 기반해 복원했으나 건물의 벽·지붕이 없으므로 허공에 떠 있는 판처럼 보이는 것이 정상이다.
- `jumbo_tree_01` 대형 나무 49건은 실제 모습이 미확정이라 생성하지 않는다. 변환한 작은 나무·관목은 바닐라 근사다.
- 물, 수심, 미확정 자연/도로 경계·실제 충돌/보행·게임 안 리소스 팩 표시까지 완성한 것은 아니다.
- 월드를 다운로드하기 전 GitHub Actions가 실제 성공했는지 `previews/31_45_report.json`의 `preview_scope`, `placeholder_parts=0` 및 팔레트 검증 결과를 반드시 확인한다.

## 실행
```bash
python -m unittest discover -s minecraft_converter/tests -v
python minecraft_converter/converter.py \
  --tmx B4220.3_MapExport_256/tmx/31_45.tmx \
  --pzw B4220.3_MapExport_256/Kentucky.pzw \
  --v259-html floorplan/current/v259_floorplan.html \
  --output minecraft_converter/output_31_45 \
  --preview-world --terrain-only --data-version 3465
```
