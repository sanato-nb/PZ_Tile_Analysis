# v92 신규 12종 A/B/C/D 직접 시각 검수 보고서 (2026-10-26)

## 출처와 판독
- 중앙 `main`의 `PROJECT_STATE.json` 및 `analysis/current/v91/MANIFEST.json`을 우선 확인한 뒤, v91 물리 통합 SQLite `analysis_queue` 미관찰 1,232종에서 12개 고유 키를 선별했다.
- 원본 `Tiles/2x/*.png`와 `B4220.3_MapExport_256/tmx/31_45.tmx`, `31_46.tmx`를 GitHub Actions 실행 환경에서 읽어 A 원본 PNG 조각, B 같은 층 5×5 조립, C 대상 레이어 단일 배치 제거, D 다른 TMX 사용 위치, ABCD 비교판을 생성했다.
- `checkpoints/v92_preview/review_sheets/sheet_000.jpg`, `sheet_001.jpg` 두 접촉판과 **12종의 개별 `*_ABCD.jpg` 12개를 직접 열어 시각 판독**했다. 단순 타일셋명 또는 기존 AI 후보에 의존하지 않았다.
- 결과: **12종 신규 관찰, 잠정 후보 9종, 정체 보류 3종**, 기존 v91 관찰과 중복 0종. `observations.tsv`와 `observations.csv`에 외형, 부품 역할, 후보, 보류, TMX 위치, GID, 원본 해시, B-C 차이를 별도 필드로 기록한다.

## 관찰 내용과 보류
- `walls_interior_house_04/80,82,85,88,91`: 각각 올리브색 단면 벽, 2면 직각 코너, 연청색 단면 벽, 직사각 창 개구부 벽, 노란색 문 개구부 벽. A 형태와 B-C 실제 배치 변화, D 다른 사용 장면을 교차 확인하여 잠정 후보로 기록.
- `walls_detailing_01/49,50,51`: 적갈색 톱니 모양 수직 띠가 벽돌 벽 모서리에 나타남. 방향·음영 차이는 공식 매핑 전까지 잠정 후보.
- `walls_detailing_01/61`: 회백색 반복 사각 무늬의 가로 장식 띠. B/D에서 현관 난간 상부와 연결되므로 잠정 후보로 기록하되 구조 부품인지 장식 몰딩인지는 미확정.
- **보류 3종**: `walls_detailing_01/22`는 흰 외벽 가로띠이나 정확한 이음 위치 불명(B-C 1,105px); `street_curbs_01/62`는 작은 삼각 쐐기(B-C 154px, 주변 PNG 누락 1건); `walls_detailing_01/55`는 매우 작은 갈색 세로 조각(B-C 89px). 세 항목 모두 원본 A 외형은 보존하되 `identity_candidate`를 공란으로 둔다.

## 품질과 계보
- A/B/C/D/ABCD **총 60 JPEG**와 접촉판 2개를 별도 보존. 생성 워크플로에서 각 JPEG 로딩 및 고유 키 12개 검사를 수행한다.
- 원본 PNG/TMX SHA-256은 `checkpoints/v92_preview/EVIDENCE_MANIFEST.json`에 기록. 원본 PNG 실제 높이와 TMX 선언 높이의 불일치(`height_mismatch`)가 12종 모두 존재한다.
- 공식 PNG–TMX Local ID 정합, TileZed 렌더, 최종 인증은 **전부 0**. 근사 아이소메트릭 합성은 공식 TileZed 결과가 아니다.
- v36·v46 원본 SQLite, v47~v91 누적 테이블, 기존 체크포인트, 원본 PNG·TMX, 사용자 수동 검수 80종과 재검수 의견은 삭제·수정·자동 합산하지 않는다.
- 통합 SQLite 생성 시 `PRAGMA integrity_check`, 기존 테이블 보존, 기존 `observed_any=0` 전제, 중복 키 검사, 압축 7조각 SHA-256 왕복 검증을 필수로 수행한다.

**최종 인증을 주장하지 않는다.** 이 보고서는 실제 PNG/TMX 근거를 열어 확인한 시각 판독과 잠정 정체 가설의 구분을 위한 기록이다.
