# v116 · 원본 이미지 없는 6종 분석 제외 (사용자 지시)

**적용 범위:** v115 AI 시각 재검수에서 원본 PNG 또는 `Local ID`에 맞는 유효 크롭을 확보하지 못한 **보류 6종만** 앞으로의 활성 재검수에서 제외한다.

| 타일셋 | Local ID | v115 검수판 | 결과 |
|---|---:|---|---|
| `e_carolinasilverbellJUMBO_1` | 1 | [#123](../review/v115_model_visual/sheet_010.jpg) | 활성 검수 제외 |
| `e_dogwoodJUMBO_1` | 1 | [#124](../review/v115_model_visual/sheet_010.jpg) | 활성 검수 제외 |
| `e_redmapleJUMBO_1` | 1 | [#125](../review/v115_model_visual/sheet_010.jpg) | 활성 검수 제외 |
| `vegetation_groundcover_01` | 22 | [#705](../review/v115_model_visual/sheet_058.jpg) | 활성 검수 제외 |
| `vegetation_trees_01` | 8 | [#712](../review/v115_model_visual/sheet_059.jpg) | 활성 검수 제외 |
| `vegetation_trees_01` | 10 | [#713](../review/v115_model_visual/sheet_059.jpg) | 활성 검수 제외 |

## 실제 기록과 집계

- `checkpoints/v116/user_exclude_six.csv`에 6개 `(tile_set_locator, local_id)`와 사용자의 제외 이유, 원본 검수판을 저장했다.
- `v116_user_excluded_missing_image` SQLite 테이블 **6개**와 `tile_catalog.v116_exclude_missing_image` 표시를 추가한다.
- **v115의 보류 이력 6종을 삭제하지 않는다.** v116에서 사용하는 `v116_active_v115_held_queue`는 **0종**이며 `v116_active_v115_review_queue`에는 이미지 판독 후보 **882종**만 남는다. **확정 정체 882종이라는 뜻이 아니다.**
- v113에서 이전에 별도로 제외한 미관찰 **8종**도 유지된다. 이번 6종은 별도 분류이며 원래 이미지 관찰 5,400종·기존 후보 4,512종·전체 TMX 5,409종이라는 역사적 수치는 그대로다.
- **공식 Local ID 매핑·TileZed 검증·최종 정체 인증은 전부 0종.** PNG가 없거나 잘못 자른 타일을 '실제 투명'으로 판정하지 않는다.
- 사용자가 재검수를 원하면 이 사용자 제외 표시를 되돌릴 수 있다.

**근거:** [v115 AI 원본 검수 결과](../review/v115_ai_identity/AI_VISUAL_REVIEW_888.csv) · [v115 검수판](../review/v115_model_visual/) · [사용자 제외 CSV](../checkpoints/v116/user_exclude_six.csv).
