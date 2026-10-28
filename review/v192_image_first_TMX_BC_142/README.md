# v192 142종 재개검수: 원본 스프라이트 A 이미지 자체 + 실제 TMX B/C 교차대조

v191에서 원본 A를 직접 시각 검수한 132종 중, 분명한 물체/부품 형상 high60/medium49를 낮음~중간 신뢰도의 **원본 A 기반 잠정 이미지 관찰 109종**으로 새로 등록. 각 기록은 원본 A PNG SHA256·RGBA 픽셀 SHA256와 TMX 원본 바이트 SHA256·layer/level/좌표/raw GID 및 firstgid 원본키 대응을 검사함.

**중요**: 이들 중 99종은 진짜 TMX B-C=0으로 가려져 있어, 실제 배치에서 사물이 보인다는 뜻이 아님. 원본 A 자체를 보고 형상을 추론한 provisional_identity_part_candidate이며 투명/확정 식별/공식 TileZed 인증이 아님. 다른 10종은 B-C 양수이지만 6종의 주변 스프라이트 누락 가능성을 포함해 개별 증거 한계를 기록함. 원본 A가 너무 작은 조각 23종과 정확한 A 자체가 없는 10종은 33종 보류. 진단용 마스킹 이미지는 실제 B/C나 사용자 D로 계산하지 않음.

누적 원본 A 잠정 관찰 기록을 9,898에서 10,007 /10,042(99.65%)로 갱신. 원본 고유 미관찰 33 + 과거 회계 차이2 = 35 기록상 미관찰. 공식 PNG↔Local ID/TileZed/실물 최종 인증은 여전히0. 부모 v190 물리 SQLite252개 테이블 모든 행·값/수 유지, 신규 v192 개별 142행 1테이블로 물리 253테이블.
증거: 원본 시각 관찰 review/v191_reopen142_A_first/sheets/ 및 MANUAL_A_IMAGE_OBSERVATIONS_142.json, 원본 TMX B/C review/v182_occlusion202/sheets/ 및 OCCLUSION_PROOF.part*.bin (ZIP CRC·SHA checked), 이번 교차대조 CROSSCHECK_142.csv와 MANIFEST.json.
