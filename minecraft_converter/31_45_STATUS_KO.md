# 31_45 TMX → Minecraft Java 시범 변환 (2026-11-09)

## 원본 데이터 및 변경 분리
- 원본: `B4220.3_MapExport_256/tmx/31_45.tmx`; 좌표·지하층 매칭은 `Kentucky.pzw`에서 검증.
- 별도 작업 브랜치: `work/minecraft-31-45-preview-20261109` (기존 31_46 브랜치에서 분기, 기존 결과물 미수정).
- 지도 크기 256×256; 전역 X **7936..8191**, Z **11520..11775**. 31_46 구역 바로 북쪽.
- 원본 TMX 직접 확인: **413개** 타일셋, **67개** CSV 레이어, **170,836건** 비어 있지 않은 배치, 지면 Floor **65,536칸**, Level -1..7.
- Level별 비영 GID 건수: -1 3,729, 0 122,412, 1 23,691, 2 14,821, 3 5,255, 4 827, 5 79, 6 14, 7 8.
- 원본 개별 물리 계단/에스컬레이터 스프라이트는 **273건**: -1 24, Level0 153, Level1 78, Level2 18. 스프라이트 개수는 실제 보행 계단의 완성/검증을 의미하지 않으므로 이번 프리뷰에서 계단은 설치하지 않는다.
- 출처와 충돌 없이 인식 가능한 상하 층의 구조 바닥 후보: -1 **1,162칸**, +1 **6,020칸**, +2 **3,629칸**, +3 **1,320칸**, +4 **29칸**. 모두 실제 `floors_*` 원본 타일 또는 음층 `Floor` 레이어 위 명시적 지면이다. 단, 전체 지도 재현이 아니라 **원본 타입 기반 후보**이며, 모든 층의 안전한 보행 연결은 아직 검증되지 않았다.
- 31_46과 다른 점: 지하 레벨(-1)의 명시적 바닥 셀이 있으므로 Y60의 기본 채움 돌을 **그 좌표에서만** 구조 바닥으로 교체하고, 셀별 Y61..63 공간을 비운다. PZW의 Basement 메타데이터는 물리 층과 직접 연결 확정하지 않는다.

## 원본 PNG 비교 반영
- `Tiles/2x/floor_carpet_motif.png`: 다양한 색의 카펫 패턴. 개별 Local ID별 양모 블록으로 근사.
- `Tiles/2x/floors_exterior_tilesandstone_01.png`: 베이지·벽돌·회색 포장재. 돌/벽돌 계열 블록으로 근사.
- `Tiles/2x/blends_natural_02.png`: 회청색 돌계열 자연 경계 조각; 물로 단정하지 않음.
- `Tiles/2x/location_shop_mall_01.png`: 수많은 벽/가구 부품이 혼재한다. Floor에서 많이 쓰인 **Local ID 22**만 포장된 바닥으로 별도 매핑, 그 외 일괄 바닥 확정 금지.
- `Tiles/2x/street_trafficlines_01.png`: 기존 31_46 황색 선 16/18/20/22에 더해 회색/밝은 선 0/2/4/6을 확인. 텍스처는 마인크래프트 지면을 솟게 하지 않는 간이 16×16 패턴.
- `jumbo_tree_01/0`의 49개 배치는 원본 외형 미검증으로 아직 생성하지 않는다.

## 생성·검증
```bash
python -m unittest discover -s minecraft_converter/tests -v
python minecraft_converter/converter.py \
  --tmx B4220.3_MapExport_256/tmx/31_45.tmx \
  --pzw B4220.3_MapExport_256/Kentucky.pzw \
  --v259-html floorplan/current/v259_floorplan.html \
  --output minecraft_converter/output_31_45 \
  --preview-world --data-version 3465
```
GitHub Actions `pz-minecraft-31-45-preview.yml`은 실제 TMX의 레이어·GID 수와 월드 청크·층별 원본 바닥·ZIP 무결성을 검사한다. 성공 시 아래 파일을 작업 브랜치에 저장:
- `previews/31_45_preview_world.zip` — 31_45 전용 월드 및 `resources.zip`
- `previews/31_45_report.json`, `31_45_floor_stair_audit.json`, `31_45_road_terrain_audit.json`
- `previews/31_45_source_placements.jsonl.gz`, `31_45_edges.json`, `31_45_furniture_parts.json`, `31_45_warnings.csv`.

**주의:** 원본 스프라이트의 실제 정체·다칸 조합·물리 벽·안전한 계단 보행·지하층 전체 공간 형상과 게임 클라이언트 표시를 인증한 완성 지도가 아니다. 미확인 바닥/가구는 원본 기록에 남긴다. 본 브랜치에서 `31_46` 프리뷰 원본은 교체하지 않으며 `main` 병합은 하지 않는다.
