# B42 가구 원장 v10 — 타일 ID에서 가구를 찾는 원본 역조회 색인

원본 TileDef와 위키 ID의 연결만 재구성해 이미지를 추가 검수하지 않고 TMX에서 바로 사용할 역방향 인덱스를 만들었어.

핵심 SQLite 조회: SELECT * FROM v10_tile_reverse WHERE source_key='furniture_shelving_01/24';

v10_tile_reverse는 정확한 위키 이미지 ID / 같은 이름에 따른 미확정 확장 / 위키에 없는 원본 타일을 별도로 기록해. v10_reverse_edge는 원본 타일 14,195개 연결의 증거를 하나씩 추적해.

v10_group_direction_candidate는 원본 Facing과 SpriteGridPos 및 조립 후보를 보존해. v10_group_function_summary는 1,852 원본 그룹의 컨테이너 종류 및 서로 다른 원본 용량을 보존하며 용량을 합산하지 않아.

v10_lookup_issues에는 여러 위키 항목을 가리키는 원본 타일과 같은 이름 확장 후보, 위키 직접 ID가 없는 수납 타일을 따로 표시했어.

주의: 하나의 정확한 위키 이미지 ID가 연결되어도 게임의 Moveable Object identity가 확정된 것은 아니야. 아이템 생성 Lua, 방별 loot, TMX의 실제 객체 인스턴스 및 마크 구현 방식은 여전히 미설정이야.
