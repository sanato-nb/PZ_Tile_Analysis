#!/usr/bin/env python3
"""Seventh group (061..070) manually checked against complete PZ assets and actual
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
N=B/"07_061_070/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_061_070_v1"
DECISIONS=json.loads(r'''[{"i":61,"src":"new","model":"closet_6_oak","candidate":"","second":"mcwfurnitures:oak_double_wardrobe; Furnection wardrobe Forge 1.20.1 (both require direct re-render)","status":"DEFER_OAK_DOUBLE_DOOR_WARDROBE_BOTTOM_DRAWER","shape":"Tall dark warm oak two-door wardrobe, TWO centered vertical metal handles and full-width single shallow bottom drawer with two knobs, complete 2-sprite 1×2 composition","size":"PZ original 2 connected sprites, 1×2 vertical footprint in source metadata; MC actual 2-block size not verified","why":"PZ 전체는 짙은 오크색 양문형 옷장+하단 긴 한 칸 서랍, 가로폭 2칸으로 완성된다. Decocraft Closet 6 Oak는 밝은 오크 단문형으로 바닥 서랍과 두 손잡이가 없고, Closet 3 Oak는 3단 서랍장, Closet 5 Oak는 열린 의류칸이므로 모두 다른 물건이다. 기존 Macaw oak_double_wardrobe의 소스 렌더도 실제 문/하단 서랍을 보여주지 못한다. 다른 모드 검증 전 최종 선택 불가.","followup":"Macaw's Oak Double Wardrobe 정식 모델/멀티블록 2×1 완전 로드, Furnection 1.20.1 Forge wardrobe source 검수, 하단 서랍과 양문 배치 대조."},{"i":62,"src":"new","model":"rattan_armchair_brown","candidate":"decocraft:rattan_armchair_brown","second":"decocraft:rattan_armchair_gray","status":"CONDITIONAL_RATTAN_ARMCHAIR_CUSHION_COLOR_MISMATCH","shape":"One-seat low brown wicker armchair with thick rounded armrests, one deep gray back cushion and dark gray seat padding, exposed little legs","size":"PZ 1×1 original single-tile seating; MC source single armchair nominal 1 block, actual sitting/hitbox not checked","why":"PZ는 갈색 라탄을 둘러 엮은 양 팔걸이와 짙은 회색 직물 등받이/좌석 쿠션의 1인 소파이다. 새 Decocraft Rattan Armchair Brown 원본 10큐브 모델은 갈색 라탄 직조 프레임·양쪽 팔걸이·좌석 쿠션 형태가 가까워 기존 PFM Blue Arm Chair(파란 직육면체 렌더)보다 훨씬 낫다. 다만 실제 MC는 쿠션이 흰색으로 차이가 크고 등받이가 직각 평판이라 원본의 둥근 등받이와 다름.","followup":"회색 또는 짙은 회색 쿠션 텍스처를 가진 브라운 라탄 변형 모델, 동일 1×1 설치/좌석 기능 검증."},{"i":63,"src":"new","model":"modular_desk_drawers_oak","candidate":"","second":"decocraft:modular_desk_drawers_oak [rejected 2 drawer]; mcwfurnitures:birch_triple_drawer (game model unverified)","status":"DEFER_LIGHT_WOOD_DRAWERS_REAR_VIEW_UNKNOWN","shape":"PZ current preview is BACK of small light oak/beige chest of drawers, flat vertical rear panel without visible handles, height around 1 block","size":"PZ 1×1; 3D front view not verified, exact drawer count must be established before match","why":"PZ 원본 사진에 연갈색 뒷판만 보여 전면 서랍의 개수·손잡이 배치가 확인되지 않았다. 과거 Macaw Bookshelf Drawer의 렌더는 초록색 얇은 판이라 가구의 전면과 무관. Decocraft Modular Desk Drawers Oak는 2단 서랍과 은색 손잡이로 실모델은 완성됐지만 원본의 전면이 확인되지 않아 닮았다고 승인할 근거가 없다.","followup":"PZ 원본 다른 Facing 방향 스프라이트나 Viewpoint 해당 모델을 180° 회전해 전면 서랍 수/색/손잡이 확인; 그 뒤 1×1 2/3단 가구 모드 비교."},{"i":64,"src":"new","model":"diner_counter_corner_light_gray","candidate":"","second":"Furnection stainless kitchen corners; More Decor counters edges (source model unverified)","status":"DEFER_STAINLESS_CORNER_SOLID_RECTANGULAR","shape":"Stainless silver commercial kitchen inner corner counter, flat metallic top and gray solid cabinet, distinct squared L-shaped notch on rear/right","size":"PZ 1×1 metal inner corner piece, needs alignment and orientation to adjacent industrial counters","why":"PZ 원본은 은색 균일 금속 상판에 직각으로 꺾인 L자 코너 홈이 있고 측면은 매끈한 회색 금속 함체. 새 Decocraft Diner Counter Corner Light Gray는 45도처럼 둥글게 모서리가 잘린 카페 카운터이며 수평 줄무늬와 검정 바닥이 있어 직각 스테인리스 주방 코너와 불일치. 기존 Black variant는 더 색이 달라 승인 불가.","followup":"Skniro's Furniture, Furnection, More Decor 1.20.1 Forge stainless corner counter actual JSON/placement and inward notch; vanilla iron blocks create 1×1 solid corner but no exact notch."},{"i":65,"src":"new","model":"spice_rack_oak","candidate":"","second":"Handcrafted shelf / Macaw's bookshelf empty forms not validated; vanilla oak trapdoors + shelves assembly concept","status":"DEFER_THREE_OPEN_WALL_SHELVES_WOOD","shape":"Tall one-tile wall/display wooden shelf with three large entirely EMPTY brown horizontal shelves in front of beige backing and darker vertical wood borders","size":"PZ 1×1 tall 3-level open shelving; wall attachment and depth need verify","why":"PZ는 벽 쪽 베이지 나무 뒷판에 돌출된 갈색 넓은 수평 선반 3칸이 비어 있는 구조다. 기존 Handcrafted Acacia Shelf는 불투명 상자처럼 렌더돼 전면이 제대로 보이지 않는다. 새 Decocraft China Cabinet Open Oak는 유리 찬장, 접시/서랍/문까지 있어 수납 종류가 다르고, Spice Rack Oak는 매우 작은 양념병 2단이라 선반 수·크기·비품 내용이 모두 어긋난다.","followup":"비어 있는 목재 선반 3단 높이와 뒷판을 가진 1×1 소스 모델 탐색. 바닐라 트랩도어/슬랩+배경 통나무 구조가 한 칸에 설치 가능한지 게임 검증."},{"i":66,"src":"new","model":"decobench","candidate":"","second":"Just Outdoor Stuffs 1.20.1 Forge two-person benches (model ID unverified)","status":"DEFER_ORNATE_OUTDOOR_METAL_WOOD_TWO_SEAT_BENCH","shape":"Two-sprite 2×1 decorative outdoors bench, many pale timber slats across back AND seat, black wrought-iron ornate scrollwork arms/legs both ends, complete two-seater","size":"PZ 2×1 connected sprites; MC must 2 adjacent places with armrests/back and two-player seating; none game certified","why":"원본은 2칸 긴 목재 가로살 좌석·등받이와 검정 금속 곡선 양 팔걸이/다리로 꾸민 공원 벤치다. 예전 Decocraft Gym Bench는 역기 운동 장비, 이번 Decocraft Decobench 실제 모델은 이름과 다르게 작업 도구/파란 제작판이 달린 실내 작업대(!)이므로 또 잘못된 종류. Rattan Couch Left도 1인 실내 라탄 좌석이며 야외 벤치가 아님.","followup":"Just Outdoor Stuffs 1.20.1 Forge garden/patio bench 2인용 실제 JAR blockstate와 model, 금속 양끝 팔걸이와 2칸 길이 확인. 다른 야외 공원벤치 모드 검색."},{"i":67,"src":"new","model":"bedside_table_open_2_ebony","candidate":"","second":"Handcrafted low wood shelf/TV stand 1×1 (actual JSON not validated)","status":"DEFER_LOW_BROWN_OPEN_SHELF_TABLE","shape":"Low dark reddish-brown short side/coffee table with plain flat rectangular top, open storage cavity in front (two horizontal shelves), compact four solid side supports","size":"PZ 1×1 and LOW (less than full block), open shelf required; MC bedside table drawer height exceeds it","why":"PZ는 낮고 짙은 갈색 상판 아래 전면이 열려 있는 2단 선반형 커피테이블/TV장. 기존 Decocraft Rattan Coffee Table은 밝은 회색 상판과 라탄 외벽으로 열린 앞면이 보이지 않아 불합격. 새 Bedside Table Open 2 Ebony는 뚜껑 열려 나온 서랍 2개와 커다란 높이의 협탁으로 실제로는 '개방형 선반'이 아니며 PZ의 낮은 높이도 맞지 않는다.","followup":"Forge 1.20.1 낮은 개방 2단 목재 TV stand/coffee table JSON 모델. 바닐라 다크오크 반블록/덫문+선반 구조 1×1 설치 높이 검증."},{"i":68,"src":"new","model":"chair_1_cherry","candidate":"","second":"pfm:oak_chair_classic_red (native import incomplete), Decocraft chair_2_cherry X-back wrong","status":"DEFER_DARK_RED_SIMPLE_WOODEN_CHAIR","shape":"Dark burgundy red painted wooden kitchen chair; four thin straight legs, single short HORIZONTAL rectangular slat back with large clear gap under, solid reddish seat","size":"PZ 1×1 small chair; MC chair nominal 1 source block","why":"PZ는 짙은 와인색 붉은 목제 의자, 등받이에는 한 개의 짧은 수평대만 있고 아래가 뚫린 단순한 형태. 기존 PFM Oak Chair Classic Red는 좌석/등받이가 아닌 일부 목재 다리/네온 색 선분만 표시된 부품 불완전 렌더. 새 Decocraft Chair 1 Cherry는 연분홍 벚나무색에 많은 세로살 등받이가 있고, Chair 2 Cherry는 X자 교차살, School Chair Red는 금속다리 플라스틱 소재라 모두 원본 색·등받이 구조 불일치.","followup":"어두운 적갈색 페인트 1가로대 등받이 4다리 의자 제공하는 모드 모델을 source-level로 검증."},{"i":69,"src":"new","model":"wooden_table_birch","candidate":"","second":"handcrafted:birch_table / Furnection light wood table 2-block connectivity not source verified; vanilla birch slab+fence 2×1 schematic","status":"DEFER_LONG_LIGHT_OAK_TABLE_TWO_TILE_FOUR_PLAIN_LEGS","shape":"Two-sprite 1×2/rotated 2×1 long rectangular light creamy oak dining table, completely flat wood top, four straight slim square timber legs, no lower shelves","size":"PZ 2 joined sprites, 1×2 in source; MC selected Decocraft wooden table is 1×1 and ornate legs, not 2×1","why":"PZ 완성형은 2칸 긴 크림색 나무 상판과 각 모서리의 가는 직선 목제 다리 4개다. 기존 Macaw Dark Oak Glass Table은 유리판 한 장만 로드됐고 목재 색부터 다름. 새 Decocraft Wooden Table Birch는 나무재질과 상판 색은 가깝지만 1칸 정사각형에 굵고 장식적인 다리 4개이고 두 개를 나란히 두면 중앙 이음매·다리가 중복될 수 있어 PZ 완성형 2칸 식탁 대체로 인증할 수 없다.","followup":"2칸 연결 시 중간 다리가 자동 삭제되는 1.20.1 Forge 테이블 모드, 바닐라 birch slab/trapdoor+fence real placement/height verify."},{"i":70,"src":"new","model":"toilet_white","candidate":"","second":"Toilet Real 1.20.1 Forge wall urinal; Toilet Remake urinal block (neither native 3D validated)","status":"DEFER_HANGING_WALL_URINAL_MISNAMED_TOILET","shape":"WHITE WALL-MOUNTED MENS URINAL, tall compact vertical open bowl, short metal top flush valve and rear drain, NO floor toilet tank or seat","size":"PZ 1×1 wall-mounted fixture; standing game player interact; adjacent wall and wall collision yet to verify","why":"중요: PZ 이름 'Toilet/Hanging'이지만 원본 이미지는 바닥에 설치하는 변기가 아니라 벽에 매다는 흰색 남성 소변기다. 기존 PFM Basic Toilet은 앉는 일반 양변기라 오매칭이고 이번 Decocraft Toilet White 실모델(93 cubes)도 뚜껑·좌석·물통 있는 일반 변기다. 다른 1.20.1 Forge Toilet Real과 Toilet Remake는 소변기 설치를 제공하지만 공식 모델/벽걸이 형태의 JAR 렌더는 확인하지 못했기에 아직 승인하지 않는다.","followup":"https://modrinth.com/mod/toiletreal 1.20.1 Forge GeckoLib requirements and urinal source JAR; https://www.curseforge.com/minecraft/mc-mods/toilet-remake 1.20.1 Forge urinal source model inspect. Actual wall mounting geometry and shape compare, no false toilet substitution."}]''')
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
  if source is None:
   d.rounded_rectangle((713,125,1298,394),radius=12,outline=(160,90,80),width=3)
   d.text((733,203),"NO SOURCE-VERIFIED EQUIVALENT",font=font(18),fill=(131,66,61))
   d.text((733,242),"Other mod model pending visual verification",font=font(12),fill=(121,75,68))
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
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 061–070</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 4차 061~070</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(61,71))
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
  source={"new":N,"none":None}[dec["src"]]
  e=proofs[str(source)].get(dec["model"]) if source else None
  assert e or dec["src"]=="none",(dec,e)
  f=source/e["native_model_screenshot"] if e else None
  assert f is None or f.is_file(),f
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
    "visually_inspected_model_id":"decocraft:"+dec["model"] if e else "NO_RELEVANT_NATIVE_MODEL",
    "native_source_model_sha256":e["source_sha256"] if e else "",
    "native_source_variant_sha256":e["variant_sha256"] if e else "",
    "native_model_cubes":e["cubes"] if e else 0,
    "native_source_screenshot_path":str(f.relative_to(D)) if f else "",
    "pz_shape_features":dec["shape"],
    "size_and_placement_notes":dec["size"],
    "review_status":dec["status"],
    "manual_review_reason":dec["why"],
    "followup_requirement":dec["followup"],
    "exact_1_to_1_visual_match_approved":"NO",
    "approved_for_minecraft_world_replacement":"NO",
    "card_path":fn
  })
 writecsv(OUT/"BATCH_061_070_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[61,63,64,65,66,67,68,69,70]
 writecsv(OUT/"BATCH_061_070_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_051_060_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:7]]==["001-010","011-020","021-030","031-040","041-050","051-060","061-070"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:6])
 groups[6]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[6]["review_file"]="batch_061_070_v1/BATCH_061_070_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"061-070","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":7,"batches_unreviewed":29,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=[
 "# 로즈우드 357종 — 7차 061~070 원본 가구 10개 시각 비교",
 "Decocraft 배포 원본 1.20.1 Forge .bbmodel/PNG 27종을 Blockbench 5.2.2에서 모두 열고 실제 렌더링. 1~2 스프라이트로 이뤄진 완성형 PZ 가구 10종과 각각 대조.",
 "원본/기존 부정확한 가구를 정답으로 승인하지 않음: 조건부 적합 1종(062), 외형/설치방식 부적합·검증 미완 9종 별도 보류. 마크 월드 안의 설치·충돌·기능 최종 승인 0종.",
 "## 항목별 실제 육안 판정"
 ]
 for a in review:
  lines.append("- **%03d %s / %s** → %s | %s. %s"%(a["index"],a["pz_name"],a["pz_style"],
   a["new_candidate_id"] or "적합한 후보 미발견",a["review_status"],a["manual_review_reason"]))
 lines.extend([
 "## 새로운 다른 모드 검색 근거 (개별 가구 모델 미검증)",
 "061 옷장·064 스테인리스 코너·069 2칸 테이블: Furnection Forge 1.20.1 https://modrinth.com/mod/lyivxs-furniture (옷장, 테이블, 주방 카운터 제공). 실제 2문+서랍/모서리 형태와 1.20.1 설치 조건 확인 전 미확정.",
 "066 공원 벤치: Just Outdoor Stuffs https://modrinth.com/project/6hCfRrRD (Forge 1.20.1, 2인용 야외 벤치 설명). 실제 검정 금속 팔걸이/나무살 모델 여부 미검증.",
 "070 명칭은 Toilet/Hanging이나 원본은 벽걸이 소변기. Toilet Real https://modrinth.com/mod/toiletreal (1.20.1 Forge, urinal 있음), Toilet Remake https://www.curseforge.com/minecraft/mc-mods/toilet-remake (1.20.1 Forge, urinal 있음)를 정확한 기능 후보로 기록. 실제 원본 모델 구조/설치/의존성 검증 전에는 매칭 확정하지 않음.",
 "063 원본 현재 스프라이트는 서랍장 뒷면이라 전면의 실제 손잡이·서랍 수 확인까지 후보 확정 금지.",
 "061과 066과 069는 2개 스프라이트로 구성되는 완성형 가구이다. 오른쪽 1칸 모델 하나를 곧바로 완성형 대체라고 표현하지 않는다.",
 "## 총진행",
 "36묶음 중 7묶음(001~070), 70/357개 스타일별 개별 검수 완료. 나머지 29묶음 미검수. 다음 구간 071~080.",
 "## 패키지",
 "- INDEX.html 및 cards/: PZ 완성형과 실제 원본 Blockbench 모델 좌우 10종 비교",
 "- BATCH_061_070_MANUAL_VISUAL_REVIEW.csv: 원본 속성, 이전 오매칭, 새/보류 판단과 원본 모델 SHA-256",
 "- BATCH_061_070_DEFERRED_OTHER_MODS.csv: 부적합 9종 후속 재검토 목록",
 "- BATCHES_ALL_357_PROGRESS.csv: 36묶음 누적 상태",
 "- 27개 source-backed Blockbench 렌더: ten_batch_review/07_061_070/extra_decocraft_render/"
 ])
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_061_070_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH07_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
