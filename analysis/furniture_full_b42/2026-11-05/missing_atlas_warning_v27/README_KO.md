# B42 가구 원본 근거 검증 v27: 미연결 23그룹·89타일 및 경고 474건

기존 v26 전체 SQLite와 원본 TileDef·Wiki 연결 증거·이미지 820건 및 초기 속성 195,265행을 그대로 보존했습니다. 신규 해결 건수를 부풀리지 않습니다.

현재 원본 Git 및 사용자 Drive의 Tiles/2x에서 정확한 PNG 파일명 3종이 누락돼 있습니다.
- crafted_03.png: source-only 17그룹 / 17 원본 타일
- lighting_indoor_01_on.png: source-only 5그룹 / 24 원본 타일 (lighting_indoor_01.png 임의 대체 금지)
- e_newsnow_ground_1.png: source-only 1그룹 / 48 원본 타일 (가구인지 의문이 있는 눈 지면 타일셋)
3종 PNG의 정확한 원본 파일 확보 전에는 픽셀·가구 정체를 인증할 수 없습니다.

경고 474건: MULTIPLE_NO_GRID 250, MULTIPLE_EXACT_WIKI_ROWS 125, MISSING_GRID 52, DUPLICATE_POSITION 27, INCOMPLETE_GRID 14, MULTIPLE_RAW_CAPACITIES 5, MULTIPLE_CONTAINER_TYPES 1.
매 경고별로 source_key/원본 SpriteGridPos/이미지 인덱스/추가 확인이 필요한 규칙을 다시 대조해 CSV 및 SQLite로 정리했습니다. 해결 판정 0/474, 원본 PNG 미연결 해결 0/23.
위키 최신성은 확인되지 않았으며, 외형이나 이름만으로 실제 게임 객체의 동일성을 인증하지 않습니다. 마인크래프트 구현, Lua loot/TMX 맵 작업 보류.
