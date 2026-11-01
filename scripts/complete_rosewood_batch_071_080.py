#!/usr/bin/env python3
"""Eighth group (071..080) manually checked against complete PZ assets and actual
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
N=B/"08_071_080/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_071_080_v1"
DECISIONS=json.loads(r'''[{"i":71,"src":"new","model":"diner_table_yellow","candidate":"","second":"decocraft:diner_table_light_gray; Furnitury small restaurant pedestal wooden table (unverified)","status":"DEFER_SQUARE_WOOD_RESTAURANT_PEDESTAL_TABLE","shape":"Light beige wood near-square single tabletop, brown thin central post, four short brown cross feet; compact high cafe bistro table","size":"PZ 1×1 single asset; square top/cross pedestal; Minecraft source inspected model nominal single block, height untested","why":"PZ 원본은 밝은 원목 정사각 상판에 갈색 가는 한 기둥과 십자 다리의 카페용 탁자다. 기존 Macaw glass table은 상판 평판 한 조각만 나타나 전혀 검증되지 않는다. 실제 Decocraft Diner Table Yellow/Light Gray는 정사각 상판과 중앙 기둥은 비슷하지만 상판이 노란 플라스틱/회색 금속이고, 넓은 사각 금속 바닥판이라 원본의 나무색/십자 발과 구조가 다르다. Round variant는 상판이 원형으로 더 어긋난다.","followup":"1.20.1 Forge 카페용 'square light-wood pedestal table with cross feet' 완성 모델 검색; vanilla spruce fence+birch trapdoor는 배치·높이·충돌 확인 후만 후보."},{"i":72,"src":"new","model":"chair_1_white","candidate":"decocraft:chair_1_white","second":"decocraft:chair_2_white [X-shaped back rejected]","status":"CONDITIONAL_WHITE_WOOD_CHAIR_BACKREST_SLATS","shape":"Ivory/cream painted compact wooden dining chair, solid pale seat and four straight slim legs; simple low back with one large rectangular opening, no armrest","size":"PZ 1×1; selected MC single full 20-cube model; runtime hitbox and seating untested","why":"PZ는 연한 크림색의 얇은 네 다리 목제 의자로 등받이에 하나의 넓은 사각 틈이 있다. 기존 PFM Oak Chair Classic White는 다리 몇 개와 붉은 막대만 나온 불완전 모델이다. 새 Decocraft Chair 1 White를 직접 렌더해 흰 목제 4다리·좌석·등받이가 모두 구현된 것을 확인했다. 다만 등받이에 세로살 여러 개가 있어 PZ의 단일 큰 사각 틈과 다르며 화이트 색감도 더 밝다. Chair 2 White는 X자라 더 멀다.","followup":"더 단순한 크림색 사각 뚫린 등받이 모델 확인, 1×1 설치/착석 기능 검증."},{"i":73,"src":"new","model":"lunch_box_red","candidate":"","second":"Hospitals - Medical Blocks & Items 1.20.1 Forge: Small/Large First Aid Kit (not native-rendered); Server meds kit item only","status":"DEFER_RED_FIRST_AID_KIT_NOT_CABINET","shape":"Small portable bright red first aid hard case, top handle, green square/white medical cross front sticker, silver clasps; not wall cabinet","size":"PZ 1×1 sprite but object occupies small fraction of tile, portable tabletop size; MC must be small not full block","why":"PZ는 빨간 사각 휴대용 구급상자에 위 손잡이, 녹색 바탕 흰 십자가 표지, 잠금쇠가 있다. 이전 Macaw Double Kitchen Cabinet은 큰 주방 수납장이어서 가구 종류 자체가 틀리다. 새 Decocraft Lunch Box Red BBMODEL도 열어 보니 음식/음료를 펼쳐 놓은 도시락 장면이라 구급상자와 전혀 다른 물건이다. Hospitals Forge 1.20.1에는 Small/Large First Aid Kit가 있지만 모델·블록 설치 가능 여부를 아직 렌더링하지 않아 매칭 확정 불가.","followup":"https://modrinth.com/mod/hospitals Forge 1.20.1 JAR의 small_first_aid_kit/large_first_aid_kit 모델·크기·십자 표식·실제 배치 가능 여부 확인. 단순 인벤토리 아이템은 가구 블록 치환 승인 금지."},{"i":74,"src":"new","model":"pedal_trash_can","candidate":"","second":"decocraft:trash_can [cylindrical corrugated round lidded can, also wrong]","status":"DEFER_TALL_GRAY_RECTANGULAR_TOP_FLAP_GARBAGE_BIN","shape":"Tall narrow grey square metal street trash bin, darker black/deep-grey pitched/hooded top with front hinged swing opening, lower body soiled metal","size":"PZ 1×1, tall bin with peaked black hood. MC pedal can low/rectangular top, not PZ","why":"PZ는 키 큰 회색 각형 쓰레기통이고 위는 짙은 회흑색 경사진 돔형/투입구 덮개다. 기존 Refurbished Recycle Bin은 하얀 상판+세로 홈의 낮은 통형 블록 일부만 보였다. 실제 Decocraft Pedal Trash Can 모델은 회색 네모 통이지만 윗면이 평평하고 바닥 페달이 노출되며 검정 높다란 쓰레기통 덮개가 없다. Decocraft Trash Can은 손잡이 원통형이라 더 다르다.","followup":"black hood/top-flap gray outdoor rectangular trash receptacle 1.20.1 Forge actual model search; vanilla gray block/trapdoor stack would need 1×1 collision placement check."},{"i":75,"src":"new","model":"dumpster","candidate":"","second":"decocraft:dumpster [blue-only actual textured variant; same dumpster class but color and industrial wear mismatch]","status":"DEFER_ORANGE_TWO_TILE_DUMPSTER_COLOR_AND_GEOMETRY","shape":"Long rusty orange/brown outdoor commercial dumpster across two original PZ tiles, thick black two-part curved corrugated hinged lids, steel exterior with rusty streaks/rectangular panels","size":"PZ 2 original parts joined; 1×2 source footprint. Decocraft model length in placed blocks untested","why":"원본은 2타일 길이의 녹슨 주황색 대형 쓰레기통과 검정 굽은 이중 뚜껑이다. Decocraft Dumpster는 실제 BBMODEL 40큐브로 대형 몸체·검정 뚜껑이 존재하여 종류/전체 비율은 비슷하지만 실제 게임용 원본 텍스처는 파란색이고 뚜껑도 검정 평판 하나처럼 보인다. 주황색 변형이나 2블록 설치 규칙은 검증되지 않았으므로 배색과 크기를 인정하지 않고 보류한다. 새 조합 텍스처를 직접 만들어 재배포하지 않는다.","followup":"Minecraft Forge 1.20.1에 실제 'orange/rusty dumpster' 배색 variant 있는지 설치 가능한 블록/모델 추가 검색. Decocraft 색상 커스터마이즈 가능성도 원본 레지스트리에서 확인; 두 타일 연결 여부 필수."},{"i":76,"src":"new","model":"lunch_box_black","candidate":"","second":"Iron Chests Forge 1.20.1 iron chest; model and dark industrial portable toolbox shape not verified","status":"DEFER_SMALL_DARK_METAL_TOOL_CHEST","shape":"Compact dark charcoal rectangular portable steel storage/tool chest with hinged flat lid, metal side pull handles, slim bright latch/lock at front; horizontally longer than tall","size":"PZ 1×1 source tile but actual object physically small and horizontally elongated; vanilla single chest differs in wood material","why":"PZ 원본은 손잡이와 잠금쇠가 있는 어두운 철제 소형 장방형 보관상자다. 기존 매칭은 실제 모델이 없는 상태였다. 새 Decocraft Lunch Box Black/Gray 역시 실제로는 도시락을 펼쳐 놓고 샌드위치·과자·음료가 바닥에 놓인 모양이므로 단순 금속 상자로 사용할 수 없다. 1.20.1 Forge Iron Chests에는 철제 보관함이 있지만 거기엔 이 원본과 같은 작은 휴대형 2:1 길이/양옆 손잡이가 있는지는 미확인.","followup":"https://modrinth.com/mod/iron-chests 실제 Iron Chest model source and a dedicated metal tool box/case mod, dark gray horizontal chest with side handles & latch model verify."},{"i":77,"src":"new","model":"microwave","candidate":"decocraft:microwave","second":"pfm:iron_microwave [previous 3D render had detached/incorrect elements]","status":"STRONG_VISUAL_CONDITIONAL_CHROME_COUNTERTOP_MICROWAVE","shape":"Small rectangular silver microwave with BLACK top, front dark window with light border and right-side vertical controls; short countertop appliance","size":"PZ 1×1 sprite with object geometry smaller than tile; Decocraft 14-cube BBMODEL model-local extents require placed-unit verification","why":"PZ는 검은 상판, 은회색 금속 본체, 왼쪽 어두운 창/사각 테두리, 오른쪽 버튼과 손잡이가 있는 전자레인지다. 기존 PFM Iron Microwave 렌더는 이상한 보라색 그림/분리된 큰 평판 때문에 완성형으로 볼 수 없다. 새 Decocraft Microwave는 실제 14큐브 원본 모델과 원본 텍스처를 모두 로드하여 앞 유리창·오른쪽 버튼·금속 하우징이 한 덩어리로 확인됨. 다만 MC 윗면은 밝은 회색이고 전면 조절부 비율이 다르며 게임 내 조리 기능은 검증되지 않았다.","followup":"검정 상판/은색 몸체를 가진 전자레인지 추가 variant 비교, 한 블록 안에서 카운터 위 설치와 요리/음식 데우기 기능 검증."},{"i":78,"src":"new","model":"bottom_cabinet_corner_inner_oak","candidate":"","second":"decocraft:bottom_cabinet_corner_outer_1_oak / outer_2_oak (top white; right-angle notch not evidenced)","status":"DEFER_BROWN_WOODEN_INNER_CORNER_NOTCH","shape":"Dark brown wood square kitchen counter with brown/tan oak plank top and visible deep right-angle INWARD L cut-out in back/right, near-vertical plain front/side panels","size":"PZ 1×1 corner fixture; needs exact inward corner notch and rotation to contiguous counters. MC color/shape unconfirmed","why":"PZ는 전체 갈색 나무로 된 카운터에 안쪽 직각으로 도려낸 L자 코너 홈이 있다. 기존 Decocraft Diner Counter Corner Black은 검정/흰색 줄무늬 금속·45도 절단 바닥이라 종류가 틀리다. 새 Decocraft Bottom Cabinet Corner Inner Oak는 목재 몸체로 개선되지만 흰색 상판이고 렌더에 PZ 같은 안쪽 직각 홈이 확인되지 않는다. Outer 1/2 모델도 흰 상판/문 패널과 일부 보이지 않는 면 때문에 코너의 정확한 맞물림을 확인할 수 없다.","followup":"PZ 1×1 L 내향 코너 실좌표와 방향 매칭, Decocraft Corner Inner Oak를 상부·모델 전체 회전해 노치가 있는지 검증. 주방 가구 모드 brown-on-brown countertop variant 검색."},{"i":79,"src":"new","model":"bottom_cabinet_1_oak","candidate":"","second":"decocraft:bottom_cabinet_island_oak (still white top, single door and drawer)","status":"DEFER_TAN_TWO_DOOR_TRAILER_KITCHEN_COUNTER","shape":"Small light tan/pine plywood trailer lower kitchen counter with rectangular plain beige top and TWO inset front cabinet doors with separate small round knobs; no top drawer","size":"PZ 1×1 single-tile low trailer cabinet, MC source nominal single block","why":"PZ는 밝은 나무톤 본체와 연베이지 상판을 가진 전면 양문형 하부장이다. 기존 Macaw Acacia Counter는 검은·붉은 큰 블록처럼 렌더되어 문 두 개가 전혀 확인되지 않는다. 새 Decocraft Bottom Cabinet 1 Oak는 색감은 근접하지만 위 서랍 1개+아래 문 1개이고 흰색 상판이라 원본의 두 문·베이지 상판과 다르다. Island Oak도 동일한 문제. 장치의 문 구조가 핵심이므로 승인하지 않는다.","followup":"Wooden two-door 1×1 lower kitchen cabinet with beige worktop, 1.20.1 Forge Furnection/Skniro’s/Handcrafted models compare. Vanilla barrel under light brown slab can approximate color only and requires game placement validation."},{"i":80,"src":"new","model":"stove","candidate":"decocraft:stove","second":"pfm:gray_stove [old incomplete line-only render]; decocraft:pizza_oven [wrong brick design]","status":"STRONG_VISUAL_CONDITIONAL_SILVER_FOUR_BURNER_OVEN","shape":"Gray silver freestanding electrical range: four dark circular stovetop burners, thin rear metal backsplash, black rounded rectangular glass oven window and door front","size":"PZ 1×1 freestanding kitchen stove. MC Decocraft source block nominal 1; functional cooking and game geometry not verified","why":"PZ는 회색 은색 몸체, 검정 상판 위 둥근 화구 4개, 뒤쪽 금속 튐방지판, 검정 유리 오븐문을 가진다. 기존 PFM Gray Stove는 길쭉한 막대 1개만 나와 오븐이 아니었다. 새 Decocraft Stove 실제 98큐브 모델은 전체 은회색 바디, 사각격자형 검정 화구 4개, 전면 조절 노브, 검정 유리 오븐창으로 외형과 종류가 상당히 비슷하다. 하지만 PZ의 동그란 화구 모양·높은 백스플래시·오븐창 곡률은 다르다.","followup":"버너 원형/사각 차이 확인, MC 실제 레시피/조리·방향별 설치·1×1 충돌 검증."}]''')
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
 d.text((25,574),"Source model image only. NOT actual Minecraft game placement or certified 1:1 visual/size equivalence.",font=font(11),fill=(125,82,72))
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
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 071–080</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 4차 071~080</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(71,81))
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
 writecsv(OUT/"BATCH_071_080_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[71,73,74,75,76,78,79]
 writecsv(OUT/"BATCH_071_080_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_061_070_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:8]]==["001-010","011-020","021-030","031-040","041-050","051-060","061-070","071-080"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:7])
 groups[7]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[7]["review_file"]="batch_071_080_v1/BATCH_071_080_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"071-080","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":8,"batches_unreviewed":28,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=[
 "# 로즈우드 357종 — 8차 071~080번 실제 가구 매칭 개별 검수",
 "Project Zomboid B42 원본 스프라이트 완성형 가구 10종과 Minecraft Java 1.20.1 Forge Decocraft 배포 BBMODEL/텍스처 27종을 Blockbench 5.2.2에서 원본 모델로 열어 대조. 자료 출처와 source SHA-256 기록.",
 "조건부 후보 3건(072,077,080), 부적합/미검증 7건(071,073,074,075,076,078,079). 원본 357 자동 후보는 정답으로 취급하지 않으며 정밀 외형 1:1 인증, Minecraft 실제 배치, 작동 검증 0건.",
 "## 개별 육안 검수"
 ]
 for a in review:
  lines.append("- **%03d %s / %s** → %s | %s. %s"%(a["index"],a["pz_name"],a["pz_style"],
   a["new_candidate_id"] or "적합한 후보 미확인",a["review_status"],a["manual_review_reason"]))
 lines.extend([
 "## 후속 다른 모드/바닐라 검색",
 "073 구급상자: PZ는 빨간 휴대용 박스+녹색 흰색 십자가, 주방 수납장 아님. https://modrinth.com/mod/hospitals 의 Small/Large First Aid Kit (1.20.1 Forge 지원) 원본 모델과 배치 블록 여부를 추후 검증한다. 장비/아이템만 있다면 맵의 물체로 바로 배치할 수 없음.",
 "075 주황 Dumpster: Decocraft Dumpster는 파란색 원본 BBMODEL 실제 렌더, 검정 뚜껑은 유사하지만 주황색/녹슨 질감/2타일 배치 불일치. 주황색 실모델 모드 또는 variant 조사.",
 "076 어두운 철제 휴대 상자: https://modrinth.com/mod/iron-chests 는 Forge 1.20.1 철제 체스트가 있지만 본 원본과 동일한 길쭉하고 작은 검정 공구상자 형태는 미검증.",
 "071 밝은 정사각 목재 탁자는 십자형 한 기둥 받침이 핵심. Decocraft Diner Table Yellow는 정사각이나 금속 받침+노란 판이어서 보류.",
 "074 회색 높은 쓰레기통에는 짙은 경사진 후드/투입구가 필요, 일반 페달통은 부적합.",
 "078 갈색 안쪽 L자 목재 코너는 흰 상판+평판 Decocraft 코너 모델과 불일치. 079 트레일러 수납장은 서랍 아닌 두 문이므로 문 수 맞춰 재검색.",
 "참고: 바닐라 블록·계단·덫문 조합은 Minecraft식 시각 보존을 우선할 수 있으나 실제 한 칸 설치 충돌/입체 높이/타일 위치 문제를 확인하기 전 최종 선택하지 않는다.",
 "## 검수 범위",
 "전체 36개 묶음 중 8개(001~080) 완료 = 80/357종 개별 원본 대조. 남은 28묶음은 QUEUED, 다음 081~090.",
 "## 증거 파일",
 "- INDEX.html 및 cards/: 좌측 실제 PZ 원본 완성형, 우측 source-authentic Blockbench 실제 렌더로 만든 10개 카드. 거절한 모델에도 명확히 NOT A MATCH 라벨을 표시",
 "- BATCH_071_080_MANUAL_VISUAL_REVIEW.csv: 원본 속성·이전 후보·새 후보·실제 모델 SHA/텍스처 해시·면적·판정",
 "- BATCH_071_080_DEFERRED_OTHER_MODS.csv: 7건 다른 모드/바닐라 추후 조사",
 "- BATCHES_ALL_357_PROGRESS.csv: 누적 36묶음 작업 현황",
 "- ten_batch_review/08_071_080/extra_decocraft_render/: 27개 실제 Blockbench 모델/출처 SHA 증거",
 "- Minecraft 게임 인게임 배치, 충돌, 가구 기능을 검증한 결과가 아님."
 ])
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_071_080_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH08_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
