#!/usr/bin/env python3
"""Third group (021..030) manually checked against complete PZ assets and actual
Decocraft Blockbench 5.2.2 renders. Four mismatch items remain deferred.
Persist all 36 batch statuses, never auto-approve visually unverified furniture.
"""
import csv,json,zipfile,html
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
SOURCE=D/"all_357_complete_native_comparisons_v1"
PZ=D/"complete_furniture_visual_3d_v1"
B=D/"ten_batch_review"
N=B/"04_031_040/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_031_040_v1"
DECISIONS=json.loads(r'''[{"i":31,"src":"new","model":"bottom_cabinet_1_ebony","candidate":"decocraft:bottom_cabinet_1_ebony","second":"decocraft:bottom_cabinet_1_spruce","status":"CONDITIONAL_WOOD_COUNTER_DOOR_MISMATCH","shape":"1×1 dark walnut wooden two-door sideboard counter; medium brown top and paired small knobs","size":"PZ 1×1 / MC 1 block modeled; in-game exact height not tested","why":"PZ는 어두운 갈색 나무의 양문 하부장과 목재 상판. 새 Decocraft Ebony는 어두운 목제 전체 형태는 비슷하지만 실제 원본은 서랍+단문(또는 한 장 문), 검정 상판이라 양문 구조가 다름. Spruce는 목재 갈색이 약간 밝고 흰 상판이어서 대안으로만. 기존 Macaw Dark Oak Counter는 통짜 블록 렌더라 거부.","followup":"목재 2도어 카운터, 같은 1×1 높이/상판을 갖는 모드 검색. 실제 문 구조 비교."},{"i":32,"src":"new","model":"coffee_grinder","candidate":"","second":"CoffeeCraft (1.20.1 Forge) — Coffee Maker Black; actual item ID and model unverified","status":"DEFER_COFFEE_MAKER_NEW_MOD","shape":"Compact modern black countertop drip coffee maker, top water chamber and circular base/cup tray","size":"PZ 1×1 appliance; should be smaller than a full Minecraft block","why":"기존 대나무 원탁 매칭은 가구 종류 자체가 틀려 폐기. 추가 확인한 Decocraft Coffee Grinder는 나무 손잡이 수동 분쇄기라 전기 드립 커피메이커가 아님. Minecraft 1.20.1 Forge CoffeeCraft 모드에 커피메이커 블록이 있다는 공개 자료는 확인했으나, 구체적인 블록 ID와 원본 모델 외형은 직접 렌더하지 못해서 보류.","followup":"https://modrinth.com/mod/coffeecraft — 배포 JAR에서 Coffee Maker Black 모델·텍스처를 실제 Blockbench로 열고 PZ 외형/크기 확인."},{"i":33,"src":"new","model":"kitchen_sink_silver","candidate":"decocraft:kitchen_sink_silver","second":"decocraft:square_sink_silver","status":"CONDITIONAL_SINK_BASIN_COUNT_MISMATCH","shape":"1×1 chrome stainless double-basin rectangular inset kitchen sink with curved faucet dividing two bowls","size":"PZ 1×1; MC chrome inset fixture, exact sink cutout/under-counter untested","why":"PZ 원본은 은색 좌우 2조 볼과 높은 곡선 수전. 새 Kitchen Sink Silver는 은색 재질·수전과 설치 용도는 가깝지만 단일 볼 형태라 쌍볼 구조를 잃음. 기존 Paladin Basic Sink는 일부 평판만 렌더돼 무효. 쌍볼 모드 모델을 계속 검색하며 이번 후보는 조건부만.","followup":"실물 1×1 2조 싱크대의 배치·기하 확인. 마크 바닐라 가마솥 두 개는 2블록으로 공간이 늘어나므로 기본 자동 대체 금지."},{"i":34,"src":"new","model":"chair_1_ebony","candidate":"decocraft:chair_1_ebony","second":"decocraft:chair_1_cherry","status":"CONDITIONAL_CHAIR_CUSHION_MISSING","shape":"1×1 dark wooden four-legged tall dining chair, five slat back and mauve/purple-pink padded cushion","size":"PZ 1×1, MC native chair nominal 1×1; seat height not measured","why":"기존 Paladin Oak Chair Classic Black은 모형 좌석과 등받이가 빠진 부분 렌더로 무효. 새 Decocraft Chair 1 Ebony는 진한 나무 프레임, 네 다리, 등받이 세로살 구성이 비슷하지만 분홍·보랏빛 방석이 없고 색상 자체도 더 검정. Cherry는 프레임이 너무 연분홍. 미세한 좌석 색상은 커스텀 리텍스처 없이는 불일치.","followup":"와인색 방석이 있는 짙은 목제 세로살 의자 모드 모델 재검색. 1×1 형태 확인."},{"i":35,"src":"new","model":"piano_bench_spruce","candidate":"","second":"handcrafted:oak_bench (source model not independently rendered)","status":"DEFER_LONG_OAK_BENCH","shape":"PZ 1×2 two-tile completed long backless oak-plank bench with narrow continuous slats and splayed end legs","size":"PZ 1×2, 2 tiles; MC piano bench unverified 1 block, too short","why":"PZ는 2타일을 합친 긴 갈색 야외 등받이 없는 벤치. 이전 Decocraft Gym Bench는 운동기구로 부적합. 새 Decocraft Decobench는 실제 목공 작업대라 전혀 다른 물건. Piano Bench Spruce는 긴 좌석 형태를 일부 갖추나 실물 길이가 짧고 피아노용 단일 스툴에 가까워 거절. Handcrafted Oak Bench는 소스 블록 ID가 존재하지만 현재 비교 렌더 미확인.","followup":"Handcrafted oak_bench/2×1 조합 가능 여부를 실제 모델과 게임 배치 검증; 바닐라 참나무 덫문+울타리 조합(인접 공간 점유) 테스트."},{"i":36,"src":"existing","model":"dryer","candidate":"","second":"wall-mounted air hand dryer from other Forge 1.20.1 bathroom mod","status":"DEFER_WALL_HAND_DRYER","shape":"Compact dark wall-mounted electric restroom hand/air dryer with front nozzle/round outlet","size":"PZ 1×1 wall fixture, protrudes from wall; MC candidate is floor appliance and wrong","why":"PZ 원본은 작은 검정 벽걸이 공기 건조기. 기존 `decocraft:dryer`는 커다란 세탁 건조기이며 원본 `.bbmodel`이 정상 표시돼도 종류가 완전히 다르므로 반려. 확인된 Decocraft JAR에는 정확한 hand dryer 모델이 없음.","followup":"Minecraft 1.20.1 Forge 욕실 장식 모드에서 벽걸이 핸드 드라이어 자산 확인; 바닐라 어두운 버튼/헤드 조합은 3D 흡사도 제한."},{"i":37,"src":"new","model":"chair_1_white","candidate":"decocraft:chair_1_white","second":"decocraft:chair_2_white","status":"STRONG_VISUAL_CONDITIONAL","shape":"Simple white-painted four-leg dining chair with thin spindle/slatted upright backrest and unupholstered seat","size":"PZ 1×1; MC 1×1 nominal chair, collision and seating unknown","why":"PZ의 흰색 나무 의자는 곧은 4다리와 세로살 등받이·평평한 좌석. Decocraft Chair 1 White는 실제 원본 20큐브 모델에서 흰 목재·세로살 4다리 형태가 상당히 닮아 기존 Paladin 반쪽 렌더보다 적합. Chair 2 White는 X등받이여서 더 다르다. 곡면·등받이 비례는 차이.","followup":"게임 실배치 좌석 높이/충돌과 흰색 변형의 게임 텍스처 일치 확인."},{"i":38,"src":"new","model":"china_cabinet_open_white","candidate":"","second":"mcwfurnitures:stripped_birch_bookshelf (actual imported preview not confirmed)","status":"DEFER_TALL_WHITE_OPEN_SHELVES","shape":"Tall narrow whitewashed wood three-tier open empty shelving/bookcase, no glass doors or decorations","size":"PZ 1×1; MC source candidate is substantially larger with several doors","why":"원본은 빈 3단 선반이 보이는 날렵한 흰 목재 책장. 기존 Decocraft Dish Rack White는 접시걸이로 틀렸고, 새 Decocraft China Cabinet Open White는 유리문·장식품·하부 서랍이 있는 거대한 찬장이어서 다른 가구. Modular Desk Storage White도 가로형 책상 장식품이다. Macaw's Stripped Birch Bookshelf는 후보 ID만 확인되어 완성 렌더 비교 전으로 보류.","followup":"Macaw's bookshelves 원본 모델 상속을 완전히 렌더하거나 Wan의 빈 흰색 3단 책장 모델·바닐라 덫문 조합 확인."},{"i":39,"src":"new","model":"bedside_table_open_1_birch","candidate":"","second":"handcrafted:birch_side_table (actual 3D source preview not verified)","status":"DEFER_SINGLE_DRAWER_OPEN_NIGHTSTAND","shape":"Light honey-oak compact bedside cabinet with single small top drawer and completely OPEN lower cubby","size":"PZ 1×1 low 1-drawer open shelf; MC tested model is different arrangement","why":"원본은 연한 갈색 1단 서랍과 아래가 빈 오픈칸 1개. Decocraft Bedside Table Open 1 Oak/Birch는 위 서랍이 열린 상태이며 아래에 또 손잡이/서랍이 있어 원본 오픈 선반과 구조가 다름. Open 2는 아랫서랍만 열린 2단 서랍장이어서 더 나쁨. 기존 Macaw acacia bookshelf drawer는 판 한 장만 표시된 불완전 렌더라 무효.","followup":"한 서랍+하단 개방 선반 1×1 nightstand 모드 모델 직접 검증; 바닐라 원목 덫문+배럴 조합도 현실적 블록 점유 검토."},{"i":40,"src":"new","model":"wooden_table_oak","candidate":"decocraft:wooden_table_oak","second":"decocraft:wooden_table_cherry","status":"CONDITIONAL_SMALL_WOOD_TABLE","shape":"Small square medium-dark brown wooden table with four straight simple chunky legs and no drawers","size":"PZ 1×1; native MC 1×1 wooden square table, visual furniture height differs","why":"PZ는 진갈색 상판과 굵은 직선 네 다리를 가진 작은 정사각 나무 탁자. Decocraft Wooden Table Oak는 네 다리/상판/탁자 역할은 같지만 상판이 밝은 베이지색이고 다리에 장식 링이 많으며 실제 높이·두께도 다름. Cherry는 분홍색이라 더 다름. 기존 Wrought Iron Small Black은 원형 금속 다리라 형태가 틀림.","followup":"진한 목재 심플 4다리 소형 탁자 모드 또는 바닐라 압력판+울타리 배치 검증."}]''')
def rows(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(p,items):
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(items[0]),extrasaction="ignore");w.writeheader();w.writerows(items)
def font(n):
 for x in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
  if Path(x).is_file():return ImageFont.truetype(x,n)
 return ImageFont.load_default()
def cropped(img):
 a=np.array(img.convert("RGBA"))
 mask=(a[:,:,:3].max(axis=2)>10)&(a[:,:,3]>4)
 y,x=np.where(mask)
 if len(x)>20:
  m=15;img=img.crop((max(0,int(x.min())-m),max(0,int(y.min())-m),
                        min(img.width,int(x.max())+m+1),min(img.height,int(y.max())+m+1)))
 return img.convert("RGBA")
def build_card(a,original,source):
 im=Image.new("RGB",(1350,600),(248,249,251));d=ImageDraw.Draw(im)
 d.rounded_rectangle((12,44,663,464),radius=9,fill=(231,237,242))
 d.rounded_rectangle((683,44,1335,464),radius=9,fill=(235,240,245))
 name=(original["pz_name"]+" / "+original["pz_style"]).strip(" /")
 d.text((19,10),str(a["i"]).zfill(3)+"  "+name,font=font(21),fill=(33,57,79))
 d.text((25,57),"PROJECT ZOMBOID / assembled original (provisional)",font=font(13),fill=(50,75,94))
 d.text((691,57),"MINECRAFT / REAL native Blockbench 5.2.2 model",font=font(13),fill=(50,75,94))
 with Image.open(PZ/original["pz_preview"]) as z:
  z=z.convert("RGBA");z.thumbnail((581,351),Image.Resampling.LANCZOS)
  im.paste(z,(int(339-z.width/2),int(258-z.height/2)),z)
 with Image.open(source) as z:
  z=cropped(z);z.thumbnail((584,350),Image.Resampling.LANCZOS)
  im.paste(z,(int(1009-z.width/2),int(268-z.height/2)),z)
 d.line((19,475,1330,475),fill=(176,188,200),width=2)
 d.text((25,491),("PZ parts: "+original["pz_parts"]+"  / footprint: "+original["pz_grid"]+
   " | "+a["size"])[:125],font=font(11),fill=(46,68,83))
 label="Proposed: "+(a["candidate"] or "NO ACCEPTABLE MATCH – inspected model REJECTED")
 d.text((25,517),(label+"  / inspected "+a["model"])[:130],font=font(11),fill=(52,66,83))
 d.text((25,543),("Manual review: "+a["status"])[:128],font=font(12),fill=(131,64,59))
 d.text((25,574),"A verified Blockbench image is not a Minecraft in-game render or proof of exact PZ visual equivalence.",font=font(11),fill=(125,82,72))
 return im
def htmlpage(items):
 block=[]
 for item in items:
  label=(item["pz_name"]+" / "+item["pz_style"]).strip(" /")
  block.append('<article><img loading="lazy" alt="'+html.escape(label,quote=True)+'" src="'+item["card_path"]+'">'+
   '<h2>'+html.escape(label)+'</h2>'+
   '<p><b>검수:</b> '+html.escape(item["review_status"])+'</p>'+
   '<p><b>실제 선정 후보:</b> <code>'+html.escape(item["new_candidate_id"] or "없음 — 후속 검토")+'</code></p>'+
   '<p><b>실제로 렌더해 비교한 모델:</b> '+html.escape(item["visually_inspected_model_id"])+'</p>'+
   '<p><b>다른 후보:</b> '+html.escape(item["secondary_candidate_id"])+'</p>'+
   '<p><b>크기:</b> '+html.escape(item["size_and_placement_notes"])+'</p>'+
   '<p><b>원본 외형:</b> '+html.escape(item["pz_shape_features"])+'</p>'+
   '<p><b>판정 이유:</b> '+html.escape(item["manual_review_reason"])+'</p>'+
   '<p><b>다음 조치:</b> '+html.escape(item["followup_requirement"])+'</p>'+
   '<details><summary>PZ 원본 메타데이터</summary><pre>'+html.escape(item["pz_properties_json"])+'</pre></details></article>')
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 031–040</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 3차 031~040</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(31,41))
 proofs={}
 for srcroot in (N,N1,N2,D/"blockbench_native_357_rematch_v1"):
  f=srcroot/"NATIVE_BLOCKBENCH_PROOF.json"
  assert f.is_file(),f
  proofs[str(srcroot)]={
   x["id"]:x for x in json.loads(f.read_text("utf8")) if x.get("loaded_verified") and x.get("native_model_screenshot")
  }
 review=[]
 for dec in DECISIONS:
  o=original[dec["i"]-1]
  assert int(o["index"])==dec["i"]
  source={"new":N,"v1":N1,"v2":N2,"existing":D/"blockbench_native_357_rematch_v1"}[dec["src"]]
  e=proofs[str(source)].get(dec["model"])
  assert e,e
  f=source/e["native_model_screenshot"]
  assert f.is_file(),f
  fn=f'cards/{dec["i"]:03d}_PZ_vs_MC.jpg'
  build_card(dec,o,f).save(OUT/fn,quality=87,optimize=True)
  review.append({
    "index":dec["i"],"pz_name":o["pz_name"],"pz_style":o["pz_style"],
    "pz_original_complete_preview":o["pz_preview"],
    "pz_parts":o["pz_parts"],"pz_footprint":o["pz_grid"],
    "pz_properties_json":o["pz_original_properties_json"],
    "previous_mc_candidate_id":o["chosen_mc_id"],
    "previous_match_needs_review":"YES",
    "new_candidate_id":dec["candidate"],
    "secondary_candidate_id":dec["second"],
    "visually_inspected_model_id":"decocraft:"+dec["model"],
    "native_source_model_sha256":e["source_sha256"],
    "native_source_variant_sha256":e["variant_sha256"],
    "native_model_cubes":e["cubes"],
    "native_source_screenshot_path":str(f.relative_to(D)),
    "pz_shape_features":dec["shape"],
    "size_and_placement_notes":dec["size"],
    "review_status":dec["status"],
    "manual_review_reason":dec["why"],
    "followup_requirement":dec["followup"],
    "exact_1_to_1_visual_match_approved":"NO",
    "approved_for_minecraft_world_replacement":"NO",
    "card_path":fn
  })
 writecsv(OUT/"BATCH_031_040_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[32,35,36,38,39]
 writecsv(OUT/"BATCH_031_040_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_021_030_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:3]]==["001-010","011-020","031-040"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:3])
 groups[3]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[3]["review_file"]="batch_021_030_v1/BATCH_031_040_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"031-040","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":4,"batches_unreviewed":32,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=["# 로즈우드 가구 357종 — 3차 031~040 실제 개별 시각 검수",
 "PZ 완성형 타일과 실제 배포 Decocraft 1.20.1 모델(.bbmodel/원본 텍스처)을 비교. 각 검수 사진의 오른쪽은 실제 Blockbench 모델이며 기존 자동 매칭은 정답으로 취급하지 않음.",
 "모델 파일 렌더링 성공=좀보이드 가구 형태 일치가 아님. 승인된 세계 적용/게임 내 작동 검증은 아직 0.",
 "## 10건 판정"]
 for a in review:
  lines.append("- **%03d %s/%s**: %s / 비교한 MC 모델 %s — %s"%
   (a["index"],a["pz_name"],a["pz_style"],a["review_status"],a["visually_inspected_model_id"],a["manual_review_reason"]))
 lines+=["## 다른 모드/바닐라 추가 검색 대상",
 "032 드립 커피머신, 035 2칸 나무 벤치, 036 벽걸이 핸드 드라이어, 038 비어 있는 흰 책장, 039 한 서랍 오픈형 협탁을 별도 CSV로 이관. 기존에 본 모드 모델은 해당 외형을 충분히 재현하지 못했으며 임의 가구로 채우지 않음.",
 "035 벤치는 2개 타일을 조합해 완성되는 긴 벤치라 1×1 피아노 벤치 후보를 자동 치환하면 안 됨. 032에는 CoffeeCraft 1.20.1 Forge에서 전용 드립 커피머신 후보를 확인했으나 실제 Blockbench 로딩은 미검증.",
 "## 다음 진행",
 "총 36개 묶음 중 4개(001~040) 시각 검수. 다음 041~050번. 뒤의 32묶음은 미검수 QUEUED 상태.",
 "## 파일",
 "- INDEX.html / cards/: 전체 10개 좌우 실제 렌더 근거",
 "- BATCH_031_040_MANUAL_VISUAL_REVIEW.csv: 원본 속성, 옛/새 모델, 형태·색상 차이와 소스 해시",
 "- BATCH_031_040_DEFERRED_OTHER_MODS.csv: 4건 추가 모드/바닐라 검색 목록",
 "- BATCHES_ALL_357_PROGRESS.csv: 그룹별 누적 검수현황",
 "- 원본 마크 모드 JAR/텍스처는 재배포하지 않고 이미지와 해시만 보관."
 ]
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_031_040_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH03_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
