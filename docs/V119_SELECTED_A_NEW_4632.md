# v119 — 신규 4,632종 대표 A 선정 및 원본 PNG 보존

## 실제 완료한 일

10,042종 전체 키 중 기존 분석한 5,409종을 신규 A 처리에서 **제외**한 뒤, v118의 새로운 4,633종 가운데 정확한 원본 PNG에서 가시 이미지가 존재하는 **4,632종의 대표 A 하나씩**을 원본 픽셀 그대로 추출했다.

| 신규 타일 상태 | 대표 A | 수량 | 선택 근거 |
|---|---|---:|---|
| A1=A2 동일 가시 | A1 | **1,544종** | TMX/TZ 두 격자에서 동일한 RGBA 픽셀 SHA |
| 한 후보만 가시 | A2 | **3,068종** | A1의 알파 0 또는 크롭 불가, A2의 실제 가시 픽셀 검증 |
| 큰 나무·그루터기 | A3 | **20종** | 별도 원본 전체 PNG를 임시 JUMBO 그리드로 추출. 프레임 정합 미검증 |
| PNG 미확보 | 미선정 | **1종** | `overlay_graffiti_wall_02 / 2` 정확한 이름의 원본 이미지 없음 |
| **합계** | | **4,633종** | |

실제로 저장한 RGBA 스프라이트는 **4,632개**이며, 총 **287개 원본 PNG**에서 추출했다. 이미지 파일 내용 SHA-256, 원본 스프라이트 RGBA 픽셀 SHA-256, 알파 픽셀 수 및 원본 타일 크롭 좌표를 검증했다.

## 파일 및 사용법

- [대표 A 전체 CSV (4,633행, 그중 4,632종 선택)](../review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv): `tile_set_name`, `local_id`, `representative_A`, `source_image_path`, `selected_crop_xyxy`, `selected_rgba_pixel_sha256`, `selected_png_file_sha256`, `selected_shard`, `selected_zip_entry`, 신뢰 수준.
- [원본 PNG 스프라이트 10개 ZIP 묶음](../review/v119_selected_A_new4633/selected_png_shards/): `PZ_REP_A_00.zip`~`PZ_REP_A_09.zip`. 각각 500개 이하, **총 4,632 PNG**.
- [대표 A 이미지 접촉시트 58장](../review/v119_selected_A_new4633/sheets/): `SELECTED_A_000.jpg`~`SELECTED_A_057.jpg`. 실제 배정한 A만 별도 표시한다.
- [선정 검증 매니페스트 및 ZIP SHA](../review/v119_selected_A_new4633/MANIFEST.json).
- [소스 미확보 1종](../review/v119_selected_A_new4633/HELD_A_1.csv).
- 이전 [v118 신규 4,633종 범위](V118_A_NEW_4633.md), [v117 전체 원본 A 후보 조사](V117_A_CANDIDATE_10042.md).

다음 B/C/D 생성 과정에서 대표 A는 CSV의 `selected_shard`와 `selected_zip_entry`가 지정하는 **PNG 파일 자체**를 사용한다. 이름이 같은 PNG가 다른 하위 폴더에 있다면 `source_image_path`의 정확한 경로와 SHA를 따라야 한다. CSV의 `selected_rgba_pixel_sha256`을 비교해 원본과 같은 RGBA인지 확인할 수 있다.

## 꼭 구분할 것

**이번 v119는 신규 A 이미지의 '잠정 대표 크롭 선정' 작업 완료**이지, AI가 4,632개 각각의 PNG와 TMX 배치를 직접 대조하여 Local ID 대응을 확정한 것은 아니다.

- A1/A2가 같아도 두 방식이 같은 격자 가정을 공유할 수 있어 **공식 TileZed 일치**를 증명하지는 못한다.
- A2만 보이는 3,068종도 그 하나를 대표 이미지로 정했을 뿐, 실제 GID/Local ID 대응은 후속 B/C/D 관찰이 필요하다.
- 특히 **JUMBO A3 20종**은 다른 나무 스프라이트가 같은 임시 격자 칸에 포함될 수 있다. 전용 배경 분리·정확한 프레임 대조가 선행돼야 한다.
- `overlay_graffiti_wall_02/2`는 **원본 이미지 미확보**이지 투명 확정이 아니다.
- 공식 PNG–TMX Local ID 매핑 인증, TileZed 독립 검증, AI 개별 매핑 인증, 최종 타일 정체 인증은 **모두 0종**.
- 기존 5,409종 및 수동 제외 이력 14종은 모두 보존했고, 물리 통합 DB는 **v116 그대로**다. 신규 분석용 A 근거만 추가했다.
