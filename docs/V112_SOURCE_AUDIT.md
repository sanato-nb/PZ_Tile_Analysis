# B42 v112 — 남은 9종 원본 경로·레이어·Local ID 진단

기준: **v111** 완전 통합 SQLite (이미지 관찰 5,400/5,409종, 미관찰 9종, 잠정 후보 4,512종, 최종 인증 0종). **v112는 새로운 관찰을 인정하지 않는 소스 진단**이며 v111 SQLite와 과거 검수 이력을 변경하지 않는다.

## 남은 9종 검사 결과

- `location_business_office_generic_01` Local ID **9, 11, 12**: TMX `31_45.tmx` 2층 `FloorOverlay1`에 각각 실제 배치됐지만, TileZed 텍스트 정의 격자로 크롭한 A의 **알파>0 픽셀 수가 0**이다. B-C 변화는 모두 0. Local ID/원본 이미지 정합 오류 또는 빈 프레임 가능성을 구별할 공식 렌더 증거가 아직 없다.
- `f_bushes_1` Local ID **66**: A에는 **4,837개 불투명 알파 픽셀**(RGBA 바운딩박스 [17,141,103,232])이 있으나 실제 `31_45.tmx` 0층 `FloorOverlay2`의 B-C 합성 이미지 변화는 0. 같은 좌표의 더 높은 레이어는 없고 바닥·벽 관련 레이어가 아래에 존재한다. 다른 이웃 타일에 의한 가림/그리기 순서·Local ID 대응·실제 TileZed 렌더를 추가 검사해야 한다.
- `e_cockspurhawthornJUMBO_1` Local ID **0, 1**: 이미지 파일 자체는 `Tiles/2x/jumbo/e_cockspurhawthornJUMBO_1.png`에 존재한다. 기존 탑레벨 경로만 검사하여 누락으로 잘못 분류한 부분을 수정한다. 그러나 v112 현재 격자 크롭은 `width_scale_unexpected`, A 빈 프레임, B-C 0이라 두 타일의 정체는 보류한다.
- `e_redmapleJUMBO_1` Local ID **0**: `Tiles/2x/jumbo/e_redmapleJUMBO_1.png`에 실제 원본 파일이 존재한다. 동일하게 현재 크롭은 `width_scale_unexpected`로 A 빈 프레임, B-C 0. 공식 매핑 전까지 보류.
- `camping_03 (ayrton orio's conflicted copy 2025-09-10)` Local ID **19**: 완전히 일치하는 파일은 없으나 `Tiles/2x/camping_03.png`가 있다. 이름에서 Git 충돌 사본 접미사를 제거하면 일치하지만 **같은 이미지라고 검증된 것은 아니므로 자동 대체하지 않는다.**
- `jumbo_tree_01` Local ID **0**: 저장소의 `Tiles` 하위에서 동일 이름 PNG를 찾지 못했다. 원본 스프라이트와 타일 정의의 공식 출처 확인이 필요하다.

## 이번 실제 작업과 증거

1. v111의 `checkpoints/v111/unresolved_9.csv`에 기록된 9키를 기준으로 **저장소 전체 Tiles 하위 PNG**를 탐색하고 파일명 유사도·크기·SHA-256을 조사했다. 후보 파일명은 신원 확정 증거가 아니다.
2. `31_45.tmx`, `31_46.tmx`를 실제 파싱해 4개 B-C 0 타일의 정확한 좌표·GID·같은 좌표의 모든 레이어·순서·가시 여부를 확인했다.
3. `Tiles/2x/jumbo`에서 확인된 실제 PNG 2개로 **3개 타일의 A/B/C/D 이미지 15장 및 접촉판 1장**을 재생성하고 직접 시각 판독했다. 세 타일 모두 B-C 0으로, 신규 관찰·잠정 후보로 승격하지 않는다.
4. 원본 세부 기록은 `audits/v112_remaining9/SOURCE_AUDIT.json`·`SOURCE_AUDIT.csv`, 크롭 PNG 4개, `checkpoints/v112_jumbo_preview/`에 보존한다.

## 변경하지 않는 값

**누적 이미지 관찰 5,400/5,409종(99.8336%), 미관찰 9종, 감사 가능 후보 4,512종, 최종 인증 0종.** 공식 PNG–TMX Local ID 검증 0, TileZed 렌더 검증 0. v111 SQLite SHA-256 `c2d31b708d5a706709007265ce44f0bd63efed27f8acd5fe5e9b3ecdd1dce73f` 유지.

**다음 우선 작업**은 JUMBO PNG의 실제 그리드와 GID Local ID 대응 확인, `camping_03` 충돌 사본 원본 복구, `jumbo_tree_01` PNG 확보, 관목 66의 실제 레이어 합성 검증이다.
