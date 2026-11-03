# PZwiki 가구 전체 목록과 B42 전체 원본 TileDef 대조

이 대조는 원래 로즈우드에 사용된 4,248개 타일만 분석한 표의 한계를 보완하는 작업이야.

기존 v259 원본 7개 .tiles 정의의 모든 원본 타일 키와 실제 PNG 논리 셀 자료를 사용했어.

## 실제 결과

- ALL_IDS_IN_FULL_TILEDEF_AND_PNG_CELLS: 1256 위키 행

- NO_WIKI_IMAGE_SPRITE_ID: 11 위키 행

- ALL_TILEDEF_IDS_NOT_ALL_LINKED_TO_PNG: 1 위키 행

로즈우드에서 사용되지 않은 위키 행 가운데 **698개**는 B42 전체 원본 정의에서 이미지 파일명의 일부/모든 타일 키를 확인했어. 사용되지 않았다고 해서 게임에 없는 가구가 아님.

## 추가 자료

- WIKI_1268_GLOBAL_ORIGINAL_TILEDEF.csv : 1,268개 원본 위키 행에 전체 TileDef 정의 연결 상태, 원본 이름, GroupName, Facing, SpriteGridPos, Material, IsoType 추가.

- WIKI_IMAGE_SPRITE_ORIGINAL_PROPERTIES.csv : 한 장 위키 이미지에 여러 번호가 들어 있을 때 번호별 원본 정의를 분리해서 표시.

- WIKI_OUTSIDE_ROSEWOOD_BUT_IN_ORIGINAL_TILEDEF.csv : 로즈우드 맵에는 등장하지 않았지만 B42 전체 원본에는 존재하는 이미지 ID.

- WIKI_IDS_NOT_FOUND_IN_FULL_TILEDEF.csv : 현재 버전 타일 정의에서 일치하지 않는 위키 이미지 ID. 없는 가구라 단정하지 않음.

- MULTIPART_NAME_DISAGREEMENT.csv : 같은 위키 이미지 여러 부품에서 원본 이름/그룹이 다른 검수 대상.

## 판정 제한

명칭/그룹이 동일하거나 타일 ID가 일치하는지 여부는 가구의 3D 형상·게임 Moveable 시스템·설치 기능을 보증하지 않아. 게임 버전 차이와 위키 원본 추출 누락 가능성을 보존하고, 어떠한 모델도 자동 병합하거나 원본을 덮어쓰지 않았어.
