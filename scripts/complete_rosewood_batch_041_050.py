#!/usr/bin/env python3
"""Fifth group (041..050) manually checked against complete PZ assets and actual
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
N=B/"05_041_050/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_041_050_v1"
DECISIONS=json.loads(r'''[{"i":41,"src":"new","model":"wall_sink_white","candidate":"decocraft:wall_sink_white","second":"decocraft:round_sink_silver","status":"STRONG_VISUAL_CONDITIONAL_WALL_SINK","shape":"White oval ceramic wall-hung basin, paired taps and visible exposed drain below; no stand","size":"PZ 1×1 wall appliance; MC wall sink is 1-block source model; actual wall mount and water functions untested","why":"좀보이드 원본은 흰색 벽걸이 세면대, 금속 수전 둘, 아래 배수구가 보임. 새 Decocraft Wall Sink White 실제 모델은 흰색 몸체/수전/아래 배수 파이프가 갖춰져 기존 Refurbished 분홍색 단일 평판보다 매우 적합. 다만 정사각형 볼과 높은 뒷판은 원본 둥근 도기와 비율 차이.","followup":"벽 장착 위치·높이·배수관·게임 사용 기능 확인. 렌더를 1:1 외형 확정으로 오인 금지."},{"i":42,"src":"new","model":"crt_tv","candidate":"decocraft:crt_tv","second":"decocraft:tv_old","status":"STRONG_VISUAL_CONDITIONAL_RETRO_CRT","shape":"Compact dark gray/black CRT television with protruding deep rear casing, tabletop portable 1990s style","size":"PZ 1×1 small CRT; native MC model 1-block nominal, visual view angle difference","why":"원본 ValuTech TV는 두껍고 뒤로 튀어나온 검정/회색 브라운관 TV(원본 좌우 비교는 뒷면 시점). 새 Decocraft CRT TV는 검은색 두꺼운 박스형 모니터와 전면 화면을 갖추어 기존 Refurbished의 큐브형 그래픽보다 명확히 낫다. Tv Old는 나무 외장·안테나가 달려 시대와 외형이 다름.","followup":"TV 전면/뒷면 양방향 렌더와 실제 바닥/탁자 설치 높이, 신호 표시/작동 여부 확인."},{"i":43,"src":"new","model":"rattan_couch_left_brown","candidate":"decocraft:rattan_couch_left_brown + decocraft:rattan_couch_right_brown","second":"decocraft:rattan_couch_center_brown","status":"CONDITIONAL_TWO_PART_RATTAN_COUCH","shape":"Two-tile connected rattan wicker two-seat sofa: brown woven arms and frame with dark gray seat and bolster cushions","size":"PZ completed 2×1 two sprites; MC left+right modules each separate; final 2-block placement, adjacency and connection untested","why":"기존 Macaw Blue Couch는 파란색 단일 블록/좌석이며 갈색 라탄 질감이 없어 전혀 맞지 않는다. 새 Decocraft Rattan Couch Brown 왼쪽·오른쪽 모델은 실제 원본 소스에서 등받이·라탄 옆면·다리·좌석을 각각 확인한 완전형 모듈이다. 하지만 쿠션은 크림색으로 원본의 짙은 회색과 색상이 어긋나며, 두 블록으로 붙인 조립 완성형은 아직 게임에서 확인하지 않았다. 카드에는 좌우 단독 모듈을 각각 보여준다.","followup":"PZ 2타일 완성 조립 재점검, 두 Decocraft 모듈을 실제 인접 배치한 최종 렌더 필요. 회색 쿠션 변형/리텍스처 검사; 2-seat 기능 확인."},{"i":44,"src":"new","model":"round_sink_silver","candidate":"decocraft:round_sink_silver","second":"decocraft:square_sink_silver","status":"CONDITIONAL_WHITE_INSET_BASIN","shape":"Compact white oval ceramic inset basin with simple short double chrome taps, no tall backsplash","size":"PZ 1×1 inset bowl; MC rounded sink nominal 1-block component, counter embed untested","why":"원본은 얕고 둥근 흰색 매입형 도기 세면대에 짧은 금속 수도꼭지들이 있다. 새 Decocraft Round Sink Silver는 흰 둥근 물받이·수전이 비슷하지만 팔각형 볼, 긴 한 개 수전, 큰 받침/배수구가 달라 모양이 정확히 같지는 않다. 기존 Refurbished는 평판만 나온 불완전 모델이므로 교체.","followup":"원본과 같은 짧은 두 손잡이 도기 세면대 모드 찾아 비교. 실제 수납장 안에 매립되는지 확인."},{"i":45,"src":"new","model":"bamboo_coffee_table_square_yellow","candidate":"decocraft:bamboo_coffee_table_square_yellow","second":"decocraft:cottage_coffee_table","status":"CONDITIONAL_LOW_LIGHT_TABLE_LATTICE","shape":"Short light honey-brown square/slightly oblong coffee table with flat wooden top and four plain stout legs","size":"PZ 1×1 low table, lower than dining table; MC single nominal source asset; leg heights differ","why":"원본은 밝은 황갈색 매끈한 낮은 탁자와 굵은 네 다리. 새 Decocraft Bamboo Square Yellow는 비슷한 밝은 목재 상판·낮은 크기를 갖지만 옆면이 X자 라탄 격자라 원본의 열린 네 다리 구조와 다름. Cottage Coffee Table은 다리는 간결하지만 색상이 매우 어두워 보조 대안. 기존 Macaw는 회색 매끈한 석판처럼 나타나 부적합.","followup":"마크 바닐라 참나무 덫문/얇은 상판+다리 조합, Re:Deco 밝은 커피테이블 실제 블록 렌더 및 설치 공간 확인."},{"i":46,"src":"new","model":"china_cabinet_open_white","candidate":"","second":"Wan's Storage Shelves / shop shelving (model ID unverified)","status":"DEFER_LARGE_SHOP_SHELVES_NEED_FRONT_AND_FOOTPRINT","shape":"PZ 2×1 multi-tile tall beige/gold commercial store shelving; reference appears viewed from largely blank rear; true front not verified","size":"PZ assembled 2×1; requires equivalent two-block commercial freestanding shelving with shelves on other side","why":"원본 2개 타일을 합친 상점 진열대인데 현재 그림은 넓고 매끈한 뒷판이 강조되어 실제 상품 진열 선반 쪽 전면이 불분명하다. 기존 Handcrafted Acacia Shelf는 폭 1칸 짜리 닫힌 목제 상자 같아 비율과 종류가 다름. 추가 Decocraft China Cabinet White도 문·접시·서랍이 있는 가정용 찬장으로 상점 전용 2칸 선반과 불일치. 원본 반대 시점 확인 전 확정 불가.","followup":"PZ 2개 타일 조립을 180° 회전해 전면 선반을 확인, Wan's Storage Shelves 모드의 2칸 모듈 원본 모델/길이 확인."},{"i":47,"src":"new","model":"kitchen_sink_black","candidate":"decocraft:kitchen_sink_black","second":"decocraft:kitchen_sink_silver","status":"CONDITIONAL_DARK_INDUSTRIAL_INSET_SINK","shape":"Narrow rectangular deep steel inset sink with dark gray rim, tall arched chrome faucet and short control","size":"PZ 1×1 industrial inset sink; MC black faucet/sink block component, countertop insertion not tested","why":"원본 Dark Industrial Sink는 진회색 은색 철제 사각 볼, 높은 꺾인 수도꼭지. 새 Kitchen Sink Black은 사각 볼·높은 호형 수전·어두운 손잡이로 기존 Paladin 평판 모델보다 좋다. 다만 모델의 바닥 몸체가 흰색이며 수전 전체가 검게 바뀌어서 원본 금속 광택과 상충. Silver 변형과 색상 재비교 필요.","followup":"Metal bowl/rim darkness과 faucet chrome 차이를 원본 방향별 비교. 다른 카운터와 결합 설치 가능한지 확인."},{"i":48,"src":"new","model":"monitor_1_white","candidate":"","second":"Noish's Furniture: Electronics / Retro Monitor + Keyboard; exact block ID and render unverified","status":"DEFER_BEIGE_CRT_DESKTOP_COMPUTER","shape":"Complete 1990s beige desktop PC: thick CRT monitor, beige horizontal computer case beneath, separate light keyboard in front","size":"PZ source 1×1 tabletop complete computer; Minecraft must fit monitor+keyboard+base together, maybe composite","why":"PZ는 오래된 베이지색 CRT 모니터, 수평 케이스, 키보드가 모두 있는 완성 데스크톱. 기존 Refurbished Computer는 금색 큰 정육면체 한 부품만 렌더링되어 매칭 불가능. 새 Decocraft Monitor 1 White는 모니터와 키보드 형태가 있지만 화면이 얇은 현대식 LCD, 화려한 방송용 조작패널, 별도 CRT 몸체가 없어 원본과 크게 다르다. 다른 전자기기 모드를 조사해야 한다.","followup":"Noish's Furniture: Electronics (Forge 1.20.1)의 retro computer monitors, PC towers and keyboards 및 Retro PC 1.20.1 Forge JAR 원본 모델 분석. 완성형 CRT+본체+키보드 조립 필요."},{"i":49,"src":"new","model":"locker_yellow","candidate":"","second":"decocraft:locker_yellow [actual native BBMODEL renders blue single door; rejected]","status":"DEFER_YELLOW_TWO_DOOR_LOCKER","shape":"Two tall separate hinged doors in one yellow/beige steel locker, centered rectangular handles, front vents","size":"PZ 1×1 tall yellow double-door locker; MC 1×1 but visual door count/color wrong","why":"원본은 두 개의 문과 가운데 손잡이 두 개가 있는 노란색 금속 사물함. Decocraft Locker Yellow와 Gray의 실모델을 모두 렌더했지만 노란색이 적용되지 않고 파란색 단일 루버 도어로 나왔으며 문 개수·힌지/손잡이가 원본과 달라. 색상 레이어 로더 문제 가능성을 배제할 수 없지만 단순히 노란색이라고 ID가 붙었다고 승인하면 안 됨.","followup":"모델 렌더러의 variant atlas 결합 정확성 우선 검증. 이후 노란 양문형 철제 락커 모드 또는 좌우 두 개 합성형 멀티블록 실제 모델 검색."},{"i":50,"src":"new","model":"drying_rack_black","candidate":"","second":"Vanilla: 2 iron trapdoors at distinct heights + iron bars (schematic only, collisions not verified)","status":"DEFER_DOUBLE_WALL_WIRE_SHELVES","shape":"Two vertically stacked black/gray wire-mesh wall-mounted tray shelves, open metal lattice baskets, no legs","size":"PZ 1×1 wall-mounted visually two vertical tiers; Minecraft requires separate horizontal supports at different Y with wall attachment","why":"PZ 원본은 벽에 매달린 2단 금속 격자형 얕은 바구니 선반이다. 기존 Handcrafted Acacia Shelf는 문 있는 나무 수납장처럼 나와 부적합. 새 Decocraft Drying Rack Black은 건조 접시와 바닥 받침대가 있는 독립형이라 다른 가구이고 Spice Rack White는 흰 통조림 양념장이라 철망과 달라. 바닐라 철 덫문/쇠창살로 선반을 근사할 수는 있으나 한 블록 내부 중첩·벽 부착 방식이 아직 검증되지 않았다.","followup":"벽걸이 2단 금속 와이어 선반을 제공하는 Forge 1.20.1 모드 탐색; 바닐라 철 덫문 2단 실제 배치/충돌, wall anchor 가능 여부 테스트."}]''')
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
 if a["i"]==43:
  # Two real source-model module screenshots side-by-side. NOT a fabricated seamless connected render.
  for filename,cx,label in [
   ("rattan_couch_left_brown_BLOCKBENCH_VIEWPORT.png",845,"LEFT MODULE"),
   ("rattan_couch_right_brown_BLOCKBENCH_VIEWPORT.png",1173,"RIGHT MODULE")]:
   with Image.open(N/filename) as z:
    z=cropped(z);z.thumbnail((310,295),Image.Resampling.LANCZOS)
    im.paste(z,(int(cx-z.width/2),int(265-z.height/2)),z)
   d.text((cx-65,420),label,font=font(12),fill=(50,75,94))
 else:
  with Image.open(source) as z:
   z=cropped(z);z.thumbnail((584,350),Image.Resampling.LANCZOS)
   im.paste(z,(int(1009-z.width/2),int(268-z.height/2)),z)
 d.line((19,475,1330,475),fill=(176,188,200),width=2)
 d.text((25,491),("PZ parts: "+original["pz_parts"]+"  / footprint: "+original["pz_grid"]+
   " | "+a["size"])[:125],font=font(11),fill=(46,68,83))
 label="Proposed: "+(a["candidate"] or "NO ACCEPTABLE MATCH – inspected model REJECTED")
 d.text((25,517),(label+"  / inspected "+a["model"])[:130],font=font(11),fill=(52,66,83))
 d.text((25,543),("Manual review: "+a["status"])[:128],font=font(12),fill=(131,64,59))
 d.text((25,574),"Source-backed render, not actual connected gameplay/size verification. Multipart sofa modules shown separately.",font=font(11),fill=(125,82,72))
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
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 041–050</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 4차 041~050</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(41,51))
 proofs={}
 for srcroot in (N,):
  f=srcroot/"NATIVE_BLOCKBENCH_PROOF.json"
  assert f.is_file(),f
  proofs[str(srcroot)]={
   x["id"]:x for x in json.loads(f.read_text("utf8")) if x.get("loaded_verified") and x.get("native_model_screenshot")
  }
 review=[]
 for dec in DECISIONS:
  o=original[dec["i"]-1]
  assert int(o["index"])==dec["i"]
  source={"new":N}[dec["src"]]
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
 writecsv(OUT/"BATCH_041_050_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[46,48,49,50]
 writecsv(OUT/"BATCH_041_050_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_021_030_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:5]]==["001-010","011-020","021-030","031-040","041-050"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:4])
 groups[4]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[4]["review_file"]="batch_041_050_v1/BATCH_041_050_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"041-050","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":5,"batches_unreviewed":31,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=[
 "# 로즈우드 357 가구 — 5차 041~050 개별 시각 검수",
 "좀보이드 원본 완성형 10개와 배포 Decocraft 1.20.1 Forge JAR 안의 실제 BBMODEL 및 원본 텍스처 24개를 Blockbench 5.2.2로 열고 검수.",
 "실제로 원본과 같은 유형/색/모듈 연결인지 검증되지 않은 물건은 끝까지 보류. 이 배치는 실제 Minecraft 게임 내 작동·자동치환 승인 0건.",
 "## 10종 수동 개별 검수"
 ]
 for a in review:
  lines.append("- **%03d %s / %s** → %s | %s. %s"%(a["index"],a["pz_name"],a["pz_style"],
   a["new_candidate_id"] or "적합한 후보 없음",a["review_status"],a["manual_review_reason"]))
 lines.extend([
 "## 추가 모드·바닐라 검수 보류",
 "046: 2×1 상점 선반의 전면/후면 조립 시점 문제. 048: 베이지 CRT+본체+키보드(다른 전자기기 모드 필요). 049: 노란 양문 락커(현재 파란 단문 모델 오류). 050: 2단 벽걸이 와이어 바스켓(현재 건조대 모델 부적합).",
 "048 검색 모드: https://www.curseforge.com/minecraft/mc-mods/noishs-furniture-electronics (Forge 1.20.1) 및 https://modrinth.com/mod/decorative-computers (1.20.1 Forge 지원). 실제 모델 ID/3D 렌더는 아직 확인 전.",
 "043 두 타일 라탄 소파: 좌/우 모듈 원본 각각을 오른쪽 비교 판에 병렬로 표시했지만 실제 MC 2칸 연결 상태를 렌더한 것이 아니다. 서로 연결되는지, 쿠션이 짙은 회색인지 검사 후 확정할 것.",
 "045 밝은 낮은 탁자: Bamboo Coffee Table Square Yellow는 색상·높이만 비슷하고 옆에 십자 격자가 있어 실제 모양 불일치. 바닐라/다른 모드 재검색.",
 "## 이후 작업",
 "전체 36개 묶음 중 5개(001~050) 완료 = 개별 검토 50/357. 나머지 31묶음은 QUEUED. 다음 작업은 051~060번.",
 "## 산출물",
 "- INDEX.html + cards/: 완성형 PZ와 출처 인증 Blockbench 모델 10종 비교 이미지",
 "- BATCH_041_050_MANUAL_VISUAL_REVIEW.csv: 원본 속성·이전 매핑·대안·형태·크기·검수 근거·원본 소스 해시",
 "- BATCH_041_050_DEFERRED_OTHER_MODS.csv: 추가 검색 4종",
 "- BATCHES_ALL_357_PROGRESS.csv: 36묶음 상태 추적",
 "- 원본 PZ PNG, MC 모드 JAR/BBMODEL을 재배포하지 않음. 파생 검수 그림과 원본 해시만 보관."
 ])
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_041_050_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH05_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
