# B42 타일 v113 — 사용자 직접 검수 반영

## 판정 결과

- **1·3·4·5·6·7·8·9번 (8종):** 사용자의 판단에 따라 **향후 활성 검수 대기열에서 제외**. 원본 타일셋·TMX·과거 SQLite 및 미관찰 원본 대기열에서는 삭제하지 않는다.
- **2번 `f_bushes_1` Local ID 66 (1종):** **'풀 또는 꽃 계열 식물'**로 사용자 잠정 후보를 기록. 정확한 식물 종류 및 타일 조각 역할은 미확정. 원본 A에는 4,837개 가시 알파 픽셀이 있지만 B-C 변화 0이므로 PNG–TMX Local ID 정합·TileZed 검증·최종 인증은 0이다.

### 원본 증거별 차이 (투명이라고 단정하지 않음)

| 검수 번호 | 타일 ID | 처리 | 실제 원본 상태 |
|---|---|---|---|
| 1 | `location_business_office_generic_01/9` | 활성 검수 제외 | verified empty alpha in provisional crop |
| 2 | `f_bushes_1/66` | 활성 유지 · 풀/꽃 잠정 후보 | visible source alpha bc delta zero |
| 3 | `location_business_office_generic_01/11` | 활성 검수 제외 | verified empty alpha in provisional crop |
| 4 | `location_business_office_generic_01/12` | 활성 검수 제외 | verified empty alpha in provisional crop |
| 5 | `camping_03 (ayrton orio's conflicted copy 2025-09-10)/19` | 활성 검수 제외 | exact source missing |
| 6 | `e_cockspurhawthornJUMBO_1/0` | 활성 검수 제외 | nested png blank provisional crop mapping unverified |
| 7 | `e_cockspurhawthornJUMBO_1/1` | 활성 검수 제외 | nested png blank provisional crop mapping unverified |
| 8 | `e_redmapleJUMBO_1/0` | 활성 검수 제외 | nested png blank provisional crop mapping unverified |
| 9 | `jumbo_tree_01/0` | 활성 검수 제외 | exact source missing |

**주의:** 제외 8종 중 사무실 3종만 *현재 잠정 격자 크롭*의 알파 픽셀이 0으로 확인됐다. JUMBO 3종은 소스 PNG가 존재하지만 크롭 격자 불일치로 빈 A가 나타났고, 다른 2종은 정확한 PNG를 확보하지 못했다. 따라서 **8종 전체를 '공식 투명 타일' 또는 '이미지 관찰 완료'로 바꾸지 않는다.**

## 체크포인트 통계 (불변)

- TMX 원본 고유 키: **5,409종**
- 과거 검증 이미지 관찰: **5,400종 (99.8336%)**
- 원본 미관찰 `analysis_queue`: **9종** (원형 보존)
- 사용자 제외 검수 대상: **8종**
- 신규 `v113_active_review_queue`: **1종 (`f_bushes_1/66`)**
- 사용자 정체 잠정 후보: **1종** (기존 감사 가능 잠정 후보 4,512종과 별도)
- 공식 매핑·TileZed·최종 인증: **0종 증가**
- 검증된 v111 과거 DB 테이블과 사용자 수동 검수 80종은 보존.

## 다음 작업

활성 검수에는 2번만 남기되, 그 타일의 원본 A 식생 형태와 실제 B/C에서 변화가 없는 이유를 공식 TileZed 격자 및 TMX 렌더로 확인한다. 제외 항목은 추후 요청 시 `v113_user_review` 테이블의 상태를 수정해 되돌릴 수 있다.

증거: [이전 9종 검수판](REVIEW_UNOBSERVED_9.md) · [v112 원본 검사 결과](V112_SOURCE_AUDIT.md) · [검수 CSV](../checkpoints/v113/user_review.csv).
