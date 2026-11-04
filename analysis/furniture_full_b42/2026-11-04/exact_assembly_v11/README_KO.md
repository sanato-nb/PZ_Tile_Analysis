# B42 가구 DB v11 — 원본 SpriteGridPos의 타일별 좌표를 확정적으로 연결

v10의 sprite ID 목록과 그리드 목록은 각각 정렬되어 있어서 두 목록을 단순 zip으로 엮으면 잘못된 배치가 될 수 있어. v11은 각 원본 타일 행의 SpriteGridPos를 직접 읽어 원본 TileSet/LocalID와 정확하게 연결했어.

v11_direction_template: 전체 3,840개의 그룹×Facing 조립 후보의 원본 좌표 및 검토 상태.

v11_tile_position: 각 타일 ID별 원본 SpriteGridPos, 템플릿 내 상대 x/y, 해당 타일의 수납 유형·용량·위치, Wiki 직접 번호.

v11_source_warning: 중복 좌표, 불완전 격자, 원본 Facing 충돌, 상이한 수납 용량, 여러 위키 앵커.

원본 격자가 직사각형인 후보 843개가 존재하지만 이것이 843개의 게임 내 가구 개체라는 의미는 아냐. 같은 이름 그룹의 여러 종류/변형과 실제 TMX 배치 확인은 별도 작업이야. 수납 용량은 부품별로 보존하고 합산하지 않았어.

조회 예시:

SELECT source_key, relative_x,relative_y,source_container,source_capacity_raw FROM v11_tile_position WHERE group_id='FUR-000429796F297C17' AND Facing='E' ORDER BY relative_y,relative_x;

원본 파일, 위키 자료, v10 DB를 보존하고 이미지 전수 재검수나 마크 구현 선택은 하지 않았어.
