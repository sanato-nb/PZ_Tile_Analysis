# v90 원본 PNG·TMX A/B/C/D 12종 독립 시각 판독 — 중복 미계상

- 검수일: 2026-10-26.
- 기준: 중앙 main의 v89 통합 SQLite (고유 5,409, 누적 관찰 3,805, 미관찰 1,604, 잠정 후보 3,228, 최종 인증 0).
- 원본 증거: `work/v90-visual-review-20261026-1156` 브랜치의 `checkpoints/v90_preview/`에서 GitHub Actions로 생성한 12종 A/B/C/D+ABCD 비교판 총 60 JPEG. [생성 검증 실행](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40261720484).
- **12종의 ABCD 비교판을 각각 직접 열어 시각 확인**했고, `INDEPENDENT_SECOND_OPINION_12_NONCOUNTING.tsv`에 원본 외형, 잠정 정체, 부품 역할, 보류 이유를 별도 기록했다.
- 독립 검수 결과: 잠정 후보 **10종**, 정체 보류 **2종**. `walls_decoration_01/11`은 B-C 변화 **1픽셀**이라 보류했고, `walls_detailing_01/2`는 수직 몰딩의 정확한 구조적 역할이 불명확하여 보류했다.
- 독립 키 12종은 병행 생성된 `work/v90-visual-review-20261026` 브랜치의 v90 증거 대기열 **240종에 모두 포함**된다. 두 브랜치의 12개 키에 대해 주요 TMX 위치, B-C 픽셀 변화, 주변 누락 수, PNG 상태, 원본 PNG/TMX SHA-256 메타데이터가 **모두 일치**한다.
- **신규 관찰 누적 증가 0종**: 이 문서는 병행 분석에 대한 독립 의견이며 `tile_catalog`, `analysis_queue`, `PROJECT_STATE.json`, `docs/HANDOFF.md` 및 통합 SQLite를 수정하지 않는다. 향후 v90 본 검수가 통합되더라도 별도 검수 의견으로 보존하고 중복 계상하지 않는다.
- 두 브랜치의 생성 증거는 근사 아이소메트릭이며 공식 PNG–TMX Local ID 및 TileZed 검증이 없다. 12종 모두 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.
- 원본 v36·v46 DB, 모든 과거 체크포인트, 사용자 수동 검수 80종과 재검수 계보를 변경하지 않았다. 이전 후보를 덮어쓰거나 단정하지 않았다.

## 검수 결과 요약

| 키 | 독립 판독 | 상태 | B-C 픽셀 변화 |
|---|---|---|---:|
| walls_decoration_01/11 | 푸른 회색 벽 부착 판; 기능 불명 | 보류 | 1 |
| walls_detailing_01/2 | 연회색 수직 몰딩; 정확한 구조 역할 불명 | 보류 | 764 |
| walls_detailing_02/8 | 흰색 벽 상부 장식 몰딩 끝 조각 | 잠정 후보 | 1,142 |
| walls_exterior_house_01/7 | 붉은 벽돌 외벽의 세로 경계 | 잠정 후보 | 1,105 |
| walls_exterior_house_02/4 | 베이지 석재 외벽 패널 | 잠정 후보 | 902 |
| walls_exterior_roofs_30_04/65 | 석재 무늬 박공 아래 삼각 외벽 | 잠정 후보 | 1,440 |
| walls_exterior_roofs_30_06/67 | 연노란 수평 사이딩 박공 외벽 | 잠정 후보 | 3,462 |
| walls_exterior_roofs_30_16/11 | 베이지 수직 판재 박공 외벽 | 잠정 후보 | 580 |
| walls_interior_bathroom_01/2 | 청록색 띠가 있는 백색 타일 벽 코너 | 잠정 후보 | 3,801 |
| walls_interior_house_04/5 | 연분홍 실내 벽 패널 | 잠정 후보 | 3,244 |
| lighting_indoor_02/1 | 검은 관절식 책상 스탠드 | 잠정 후보 | 1,577 |
| lighting_outdoor_01/3 | 검은 클래식 야외 가로등 | 잠정 후보 | 2,746 |

자세한 외형 관찰과 잠정 후보·보류 사유, 인증 플래그는 TSV 참조.
