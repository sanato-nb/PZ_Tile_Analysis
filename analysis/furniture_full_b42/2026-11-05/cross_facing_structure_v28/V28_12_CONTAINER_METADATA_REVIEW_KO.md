# v28 추가 조사 대상: 방향별 원본 수납 메타데이터 차이 12그룹

v28 전체 274개 다방향 그룹의 원본 TileDef 컨테이너 필드 대조에서 **12개 그룹의 Facing별 원본 값 집합이 다르게 기록됨**을 확인했다. 전부 4방향 원본 부품 수는 같고 이미지 아틀라스 그룹도 일치한다.

- `camping_02.png`: 11그룹. 일부 Facing의 원본 `ContainerCapacity=50`이 다른 Facing에는 존재하지 않음.
- `location_community_medical_01.png`: 1그룹. 일부 Facing의 원본 `ContainerType=desk`, `ContainerCapacity=20`이 다른 Facing에 없음.

이는 **원본 필드 차이**이지 서로 다른 게임 객체라는 증거가 아니고, 오류 확정도 아니다. 현재는 동일/다른 런타임 객체 인증 0건이며 정확한 B42 게임 오브젝트의 SpriteGrid/수납 속성 처리 규칙 확인 전까지 보류한다.

## 대상 그룹 ID

- `FUR-02AA3E6ABAA20478` — camping_02.png
- `FUR-06A9BDDBAAB92F0D` — camping_02.png
- `FUR-3285178149E8AA38` — camping_02.png
- `FUR-36367E59DEE33AD3` — camping_02.png
- `FUR-365C070B8F866E81` — location_community_medical_01.png
- `FUR-3D07B321EFADA411` — camping_02.png
- `FUR-4B40D6FC3C3EEA00` — camping_02.png
- `FUR-4EFC2060BA5A57ED` — camping_02.png
- `FUR-76359DBA8F97C0EB` — camping_02.png
- `FUR-8F53B9A40C57599C` — camping_02.png
- `FUR-BA73ACC4A6860BCC` — camping_02.png
- `FUR-D8E9F8FF258438A0` — camping_02.png

상세 값은 `V28_12_CROSS_FACING_CONTAINER_METADATA_VARIATIONS.csv`와 `V28_274_GROUP_SOURCE_FACING_COMPARISONS.csv`를 참조한다.
