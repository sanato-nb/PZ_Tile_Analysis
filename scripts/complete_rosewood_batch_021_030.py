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
N=B/"03_021_030/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_021_030_v1"
DECISIONS=json.loads(r'''[{"i":21,"src":"new","model":"bathtub_white","candidate":"decocraft:bathtub_white","second":"decocraft:bathtub_clawfoot_silver","status":"STRONG_VISUAL_CONDITIONAL","size":"PZ 1×2 (2 sprites); Minecraft 2-block bathtub footprint not independently confirmed","shape":"White rectangular recessed bathtub with chrome end faucet; multi-tile assembled","why":"원본 PZ는 두 타일로 구성되는 긴 흰색 욕조. Decocraft Bathtub White는 하얀 사각 욕조·내부 공간·끝 수전 모양이 매우 가깝다. 단 PZ 조립 프리뷰에 떨어져 보이는 수도꼭지 한 조각은 조립 미확정이므로 시각 검수 전 수정 필요. MC 실제 배치 면적과 연결 기능은 미확인.","followup":"PZ SpriteGridPos 두 부품의 수도꼭지 중첩/조립 좌표 재검증. 실제 마크 설치 폭과 수도 기능 확인."},{"i":22,"src":"new","model":"rectangular_mirror_silver","candidate":"","second":"decocraft:middle_cabinet_white","status":"DEFER_MEDICINE_CABINET_MISSING","size":"PZ wall fixture 1×1; depth unverified","shape":"Small white wall-mounted mirrored medicine CABINET with opening/storage body","why":"PZ는 옆면 깊이와 작은 문/손잡이가 있는 벽걸이 약품장. 실제 Decocraft Rectangular Mirror Silver는 거울뿐이라 수납 몸체가 없다. Middle Cabinet White는 몸체만 있고 거울이 없다. 둘 모두 원본의 문+거울+수납 기능을 동시에 갖추지 못하므로 기존 Macaw 주방장 매칭도 반려하고 보류.","followup":"Minecraft 1.20.1 Forge 욕실 모드의 거울문 약품장 실제 모델 추가 검색. 바닐라 거울 대안만으로 기능 대체 금지."},{"i":23,"src":"new","model":"bedside_table_ebony","candidate":"decocraft:bedside_table_ebony","second":"decocraft:modular_desk_drawers_oak","status":"CONDITIONAL_DRAWERS_STYLE_MISMATCH","size":"PZ 1×1, 3 drawers; Minecraft standalone cabinet game dimensions unverified","shape":"Dark polished wood chest with three stacked drawers and small round brass pulls","why":"원본은 진갈색 캐비닛형 3단 서랍장과 황동 원형 손잡이. Bedside Table Ebony는 2단 서랍장으로 어두운 갈색 톤·4다리는 비슷하지만 서랍 개수, 손잡이 모양, 가구 높이가 다르다. Modular Desk Drawers Oak도 2단에 색상이 밝아 대안으로만 기록.","followup":"다른 모드의 진갈색 3단 서랍장 1×1 모델 탐색. 현재 2단 모델 최종 승인 금지."},{"i":24,"src":"new","model":"wooden_table_oak","candidate":"","second":"decocraft:kitchen_table_oak","status":"DEFER_TWO_TILE_TABLE_FOOTPRINT","size":"PZ 2×1 complete table, 2 original sprites; inspected Minecraft asset appears 1×1","shape":"Long rectangular medium brown tabletop supported by four thin dark legs","why":"원본 완성형 테이블은 2개 타일로 연결된 길쭉한 직사각 탁자이며 가느다란 검은 다리 네 개가 있다. Decocraft Wooden Table Oak는 목재 단색 1×1 정사각 탁자에 굵고 장식적인 다리라 비율·재질·부피가 다르다. Kitchen Table Oak도 흰 상판이므로 부적합. 기존 Macaw Oak Table의 큐브형 렌더 역시 원본과 불일치.","followup":"2×1 직사각 연결 테이블 모드, 멀티블록 테이블 조립 규칙, 또는 바닐라 진한 반블록+지지대 배치 가능성(블록 높이 충돌 포함) 검증."},{"i":25,"src":"v1","model":"bottom_cabinet_1_white","candidate":"decocraft:bottom_cabinet_1_white","second":"decocraft:bottom_cabinet_2_white","status":"CONDITIONAL_WHITE_COUNTER_DOORS","size":"PZ 1×1 white cabinet; Minecraft 1×1 cabinet candidate, height/interaction untested","shape":"Off-white 2-door cabinet with full light top and two thin vertical handles","why":"원본은 크림색 두 문짜리 카운터. Decocraft Bottom Cabinet 1 White는 흰색 몸체가 가깝지만 위 한 서랍+아래 한 문, 상판 목재색이라 2도어 크림색 원본과 차이. Bottom Cabinet 2 White는 서랍 4개라 더 나쁨. 기존 1 White를 조건부 후보로만 유지.","followup":"크림/연회색 2도어 낮은 하부장 모드 신규 검색 또는 다른 white cabinet 변형 확인."},{"i":26,"src":"new","model":"china_cabinet_open_oak","candidate":"","second":"handcrafted:acacia_shelf","status":"DEFER_LOW_OPEN_SHELF","size":"PZ 1×1 low three-tier open shelf, Minecraft height should be low","shape":"Small light oak 3-level open shelving with visible bare horizontal shelves, no door/glass","why":"원본은 높이가 낮은 개방형 목재 3단 선반. Decocraft China Cabinet Open Oak는 거대한 유리문/접시/서랍이 붙은 장식장이라 종류가 다르다. 기존 Handcrafted Acacia Shelf는 실제 렌더가 원본과 달리 전면이 막힌 진열장 형태로 나와 승인 불가.","followup":"Wan Storage Shelves의 낮은 오크 3단 조립형 실제 모델, 바닐라 덫문/계단 수평 선반 조합의 블록 충돌과 높이, 다른 선반 모드 확인."},{"i":27,"src":"v2","model":"bottom_cabinet_1_oak","candidate":"decocraft:bottom_cabinet_1_oak","second":"decocraft:bottom_cabinet_2_oak","status":"CONDITIONAL_WOODEN_COUNTER_DOORS","size":"PZ 1×1 oak 2-door lower cabinet; MC 1-block candidate","shape":"Warm medium brown oak lower kitchen cabinet with TWO front doors and plain brown slab countertop","why":"원본은 중간 갈색 오크 2도어 캐비닛과 갈색 목제 상판. Bottom Cabinet 1 Oak는 목재 색감은 가깝지만 상판 흰색, 상단 서랍+하부 단문 구성이며 Bottom Cabinet 2 Oak는 4단 서랍이라 더 부적합. 기존 Macaw Dark Oak Counter는 어두운 직육면체라 더 멀어 조건부 1 Oak로 교체 제안.","followup":"오크 2도어·갈색 상판 세트 모드에서 다시 검색. 다중 문 구조 필요."},{"i":28,"src":"new","model":"trash_can_open","candidate":"","second":"decocraft:waste_basket_black","status":"DEFER_GREEN_OPEN_METAL_BIN","size":"PZ 1×1 dark green cylindrical open bin","shape":"Open-top dark green solid metal cylinder with black liner and horizontal pressed hoops","why":"PZ 원본은 짙은 초록색 원통 몸체와 검정 테두리 비닐이 있는 개방 쓰레기통. Decocraft Trash Can Open은 회색 골판형 큰 쓰레기통으로 뚜껑이 옆에 떨어져 있으며 검정 격자 바구니는 철망형이라 외형이 달라. 기존 Paladin Mesh Trashcan도 격자·초록 배경이 뒤엉킨 부분 렌더로 승인 불가.","followup":"1.20.1 Forge에서 초록색 솔리드 개방형 금속 쓰레기통/산업용 빈 실제 모델 탐색. 정확 색상 변형 확인."},{"i":29,"src":"new","model":"kitchen_sink_silver","candidate":"decocraft:kitchen_sink_silver","second":"decocraft:square_sink_silver","status":"STRONG_VISUAL_CONDITIONAL","size":"PZ 1×1 countertop industrial inset sink; MC sink embedded geometry, mounting and plumbing untested","shape":"White/light gray rectangular inset industrial sink with tall curved chrome faucet and small controls","why":"PZ 원본은 얕은 네모 물받이와 높게 굽은 금속 수도꼭지. Decocraft Kitchen Sink Silver 모델은 사각 물받이·높은 호스형 수전·금속 색상이 꽤 닮았다. Square Sink Silver도 유사하지만 베이슨 형태가 다르므로 전자를 우선. 원본은 독립 받침 없는 인셋형이라 싱크 하부 조합 공간이 맞는지 필요.","followup":"바닥/카운터와 겹치지 않는 모델 배치와 물 공급/상호작용 확인."},{"i":30,"src":"new","model":"school_chair_blue","candidate":"decocraft:school_chair_blue","second":"decocraft:diner_chair_blue","status":"CONDITIONAL_BLUE_SCHOOL_CHAIR","size":"PZ 1×1 four-leg blue plastic/metal frame school chair; MC 1×1 single chair","shape":"Blue molded one-piece plastic curved back with cutout handle and blue seat on black curved metal legs","why":"PZ는 등받이 중앙에 손잡이 구멍이 뚫린 파란 플라스틱 의자와 검정 가는 금속 다리. School Chair Blue는 파란 시트·등받이·금속 다리 구성이 맞지만 등받이가 네모이고 손잡이 대신 회색 박음점, 좌석이 직사각이라 상당한 차이. Diner Chair Blue는 흰 줄무늬가 있어 더 멀다. 조건부만.","followup":"플라스틱 손잡이 구멍이 있는 학교/회의실 의자 모델 추가 모드 탐색."}]''')
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
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 021–030</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 3차 021~030</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(21,31))
 proofs={}
 for srcroot in (N,N1,N2):
  f=srcroot/"NATIVE_BLOCKBENCH_PROOF.json"
  assert f.is_file(),f
  proofs[str(srcroot)]={
   x["id"]:x for x in json.loads(f.read_text("utf8")) if x.get("loaded_verified") and x.get("native_model_screenshot")
  }
 review=[]
 for dec in DECISIONS:
  o=original[dec["i"]-1]
  assert int(o["index"])==dec["i"]
  source={"new":N,"v1":N1,"v2":N2}[dec["src"]]
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
 writecsv(OUT/"BATCH_021_030_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[22,24,26,28]
 writecsv(OUT/"BATCH_021_030_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_011_020_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:3]]==["001-010","011-020","021-030"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:2])
 groups[2]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[2]["review_file"]="batch_021_030_v1/BATCH_021_030_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"021-030","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":3,"batches_unreviewed":33,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=["# 로즈우드 가구 357종 — 3차 021~030 실제 개별 시각 검수",
 "PZ 완성형 타일과 실제 배포 Decocraft 1.20.1 모델(.bbmodel/원본 텍스처)을 비교. 각 검수 사진의 오른쪽은 실제 Blockbench 모델이며 기존 자동 매칭은 정답으로 취급하지 않음.",
 "모델 파일 렌더링 성공=좀보이드 가구 형태 일치가 아님. 승인된 세계 적용/게임 내 작동 검증은 아직 0.",
 "## 10건 판정"]
 for a in review:
  lines.append("- **%03d %s/%s**: %s / 비교한 MC 모델 %s — %s"%
   (a["index"],a["pz_name"],a["pz_style"],a["review_status"],a["visually_inspected_model_id"],a["manual_review_reason"]))
 lines+=["## 다른 모드/바닐라 추가 검색 대상",
 "022 거울문 약품장, 024 긴 2×1 4다리 테이블, 026 키 낮은 3단 빈 선반, 028 초록색 개방 철제 쓰레기통을 별도 CSV로 이관. 기존에 본 모드 모델은 해당 외형을 충분히 재현하지 못했으며 임의 가구로 채우지 않음.",
 "021 욕조는 두 타일 합본의 수도꼭지가 떨어져 표시될 수 있어 PZ 조립도 재검증 필요.",
 "## 다음 진행",
 "총 36개 묶음 중 3개(001~030) 시각 검수. 다음 031~040번. 뒤의 33묶음은 미검수 QUEUED 상태.",
 "## 파일",
 "- INDEX.html / cards/: 전체 10개 좌우 실제 렌더 근거",
 "- BATCH_021_030_MANUAL_VISUAL_REVIEW.csv: 원본 속성, 옛/새 모델, 형태·색상 차이와 소스 해시",
 "- BATCH_021_030_DEFERRED_OTHER_MODS.csv: 4건 추가 모드/바닐라 검색 목록",
 "- BATCHES_ALL_357_PROGRESS.csv: 그룹별 누적 검수현황",
 "- 원본 마크 모드 JAR/텍스처는 재배포하지 않고 이미지와 해시만 보관."
 ]
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_021_030_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH03_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
