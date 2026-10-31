# v83 독립 시각 판독 감사 기록 (2026-10-26)

원본 PNG 개별 타일 A, TMX 동일 층 5×5 조립 B, 대상 배치 하나 제거 C, 다른 실제 사용 위치 D를 생성한 뒤 12종의 ABCD 비교판을 직접 열어 판독했다. PNG/TMX 공식 Local ID 정합과 TileZed 검증은 수행하지 않았으므로 최종 인증은 0종이다. v82 이전 관찰·원본 자산 및 사용자 수동 검수 80종은 별도 보존한다.

| 고유 키 | 판독 | 잠정 정체 또는 보류 | B-C 원본 변화 | 신뢰도 |
|---|---|---|---:|---|
| fixtures_stairs_01/9 | candidate | 검정색 개방형 금속 계단의 4단 분할 조각 | 8768 | high |
| fixtures_stairs_01/10 | candidate | 검정색 개방형 금속 계단의 3단 분할 조각 | 6165 | high |
| furniture_storage_01/50 | held | 배치 기여·정체 불명 | 0 | low |
| furniture_storage_01/56 | candidate | 연갈색 1도어·2서랍 키 큰 수납장 | 11645 | high |
| blends_street_01/57 | candidate | 연베이지 자갈 질감의 얇은 사선 경계 오버레이 | 338 | low |
| blends_street_01/58 | candidate | 밝은 자갈·포장 경계의 반대 방향 가는 사선 | 334 | low |
| blends_street_01/59 | held | 배치 기여·정체 불명 | 0 | low |
| blends_street_01/65 | candidate | 회색 아스팔트 패치의 위쪽 삼각형 경계 | 1998 | medium |
| blends_street_01/66 | candidate | 회색 아스팔트 패치의 아래쪽 삼각형 경계 | 2014 | medium |
| blends_street_01/67 | candidate | 회색 아스팔트 패치의 왼쪽 삼각형 경계 | 2051 | medium |
| blends_street_01/68 | candidate | 회색 아스팔트 패치의 오른쪽 삼각형 경계 | 1145 | medium |
| blends_street_01/69 | candidate | 짙은 회색 아스팔트 바닥 기본 타일 | 3947 | high |

증거 출처: `checkpoints/v83_preview/EVIDENCE_MANIFEST.json`, `checkpoints/v83/observations.tsv`, 이미지 60장 및 `checkpoints/v83/ZIP_CRC_REPORT.json`. 모든 신규 키에서 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`으로 유지. PNG 물리 높이와 TMX 선언 높이 불일치(`height_mismatch`) 기록. 보류 2종: `furniture_storage_01/50` 및 `blends_street_01/59` (두 건 모두 B-C 0픽셀).
