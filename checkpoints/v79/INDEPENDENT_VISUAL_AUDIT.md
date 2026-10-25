# v79 독립 이미지 판독 기록 (2026-10-26)

## 범위와 원칙
- 기준: v78 통합 SQLite `analysis_queue` 미관찰 고유 키 1,980종.
- 원본 GitHub PNG/TMX에서 생성한 A 원본 크롭, B 같은 층 5×5 근사 아이소메트릭, C 대상 배치 하나만 제거, D 다른 실제 TMX 위치, ABCD 비교판 **12개를 직접 열어 시각 관찰**했다.
- v79 신규 12종: 잠정 후보 **8**, 정체 보류 **4**, 신규 키 중복 **0**(DB 대조는 빌드 검증 대상).
- 이미지 기반 정체는 공식 Local ID 매핑 또는 TileZed 검증이 아니다. 모든 `mapping_verified=0`, `tilezed_verified=0`, `final_certified=0`.

## 개별 직접 판독
| 키 | B-C 변화 | 판정 | A/B/C/D에서 확인한 핵심 |
|---|---:|---|---|
| fixtures_sinks_01/33 | 9836 | 잠정 | 금속 싱크볼·스프링형 수전·하부 격자 선반이 함께 사라짐 |
| fixtures_sinks_01/35 | 0 | 보류 | A는 싱크대 외형이지만 벽돌 벽에 가려 B와 C 동일 |
| furniture_storage_01/25 | 5934 | 잠정 | 검정색 키 큰 장의 한쪽 문판·상판·측면 |
| furniture_storage_01/33 | 7178 | 잠정 | 검정색 2단 서랍장, D에서는 침대 옆 협탁 |
| blends_natural_01/88 | 492 | 보류 | 가느다란 갈색 풀·흙 경계 조각, B/C 기여 작고 D 불명확 |
| blends_natural_01/91 | 491 | 보류 | 마른 풀의 사선 선형 가장자리, 석벽·지면에 가림 |
| blends_natural_02/8 | 814 | 잠정 | 청회색 수면과 갈색 흙 사이 사선 물가 연결띠 |
| blends_natural_02/11 | 787 | 잠정 | 반대 방향의 청회색 물결 경계띠 |
| blends_street_01/0 | 0 | 보류 | A는 회색 아스팔트 바닥 전체이나 B/C 동일 |
| blends_street_01/1 | 2136 | 잠정 | 회색 도로 패치 삼각 경계, 중앙선 부근 |
| blends_street_01/2 | 2511 | 잠정 | 균열선이 있는 회색 아스팔트 삼각 패치 |
| blends_street_01/3 | 2318 | 잠정 | 측면 균열선과 삼각형 회색 보수 포장 |

## 독립성·위험·검증 범위
- 타일셋명은 키 식별 용도로만 사용했고 정체 근거는 **A 외형, B-C 대상 제거 효과, D 다른 실제 사용 위치**에 한정했다. v31 AI분류를 재사용하지 않았다.
- 원본 PNG 물리 높이와 TMX 선언 높이 불일치가 모든 신규 키에서 발견된다. 원본 이미지에서 실제 외형을 관찰했더라도 PNG–TMX Local ID 공식 대응을 최종 인증할 수 없다.
- 주변 PNG 누락이 있는 물가 타일과 작은 B-C 변화의 풀 가장자리 타일은 보수적으로 판정했다.
- 원본 증거: `checkpoints/v79_preview/`의 A/B/C/D/ABCD **60 JPEG** 및 `EVIDENCE_MANIFEST.json`; 레코드: `checkpoints/v79/observations.tsv`.
- 원본 SHA-256, PNG/JPEG 로딩, 원본 TMX 위치·raw GID, B-C 변화, SQLite 무결성, 이전 테이블 보존, ZIP CRC는 **GitHub Actions 검증 결과 확인 전에는 PASS로 간주하지 않는다**.
- 사용자 직접 검수 80종과 기존 v36~v78 데이터·체크포인트·원본 PNG/TMX는 수정하지 않는다.
