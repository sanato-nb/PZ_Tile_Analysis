#!/usr/bin/env python3
"""Ninth group (081..090) manually checked against complete PZ assets and actual
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
N=B/"09_081_090/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_081_090_v1"
DECISIONS=json.loads(r'''[{"i":81,"src":"new","model":"cottage_coffee_table_oval","candidate":"","second":"Re:Deco glass coffee table or vanilla glass panes with dark oak frame (source/game geometry not verified)","status":"DEFER_TWO_TILE_OVAL_WOOD_FRAME_GLASS_COFFEE_TABLE","shape":"Long 2-tile oval low coffee table with deep rich brown curved wood perimeter, transparent glass top center and slim end supports, enclosed lower curved wooden shelf","size":"PZ 2 original sprite parts / source 1×2; Minecraft source candidate model height/2-block placement not established","why":"PZ 완성형은 긴 타원형·가장자리가 둥글게 이어진 진갈색 목재 프레임과 투명 유리 상판을 지닌 낮은 2타일 테이블이다. 이전 Macaw Glass Table은 상판 평판 한 장만 남아 실제 장식 프레임과 다리 부분을 전혀 확인할 수 없다. 새 Cottage Coffee Table Oval의 19큐브 BBMODEL은 길쭉한 갈색 목재 낮은 테이블이지만 상판 전체가 불투명 목재이며 타원형 유리 인셋·곡선 테두리·하단 선반이 없어서 완성형과 다르다. Rattan Coffee Table도 직조 사각 상자라 불합격.","followup":"Re:Deco 1.20.1 Forge coffee tables/display cases 또는 다른 모드의 2×1 glass-oval wooden frame 실제 JSON·텍스처 확인; PZ 2타일 조립/MC 설치 블록 수 테스트."},{"i":82,"src":"new","model":"diner_table_round_black","candidate":"","second":"decocraft:bamboo_coffee_table_round_yellow [wrong lattice legs/color]; Furnitury pedestal wood cafe table (unverified)","status":"DEFER_OAK_ROUND_TRIPOD_TABLE","shape":"Brown wood circular tabletop with slight straight segments, single brown slim central shaft and three splayed brown feet, 1 tile","size":"PZ 1×1 round pedestal 3-foot table; MC model single block nominal, height untested","why":"PZ 원본은 중간 갈색 원목 원형 상판과 갈색 중심 기둥·삼발이 다리다. 예전 Macaw Acacia Coffee Table은 짙은 회색 정사각 돌판처럼 렌더돼 전혀 어울리지 않았다. 새 Diner Table Round Black은 상판 원형과 한 기둥·삼발이 형태는 맞으나 실제 검정 금속 상판/회색 철제 다리로 목제 재질·색상이 반대다. Bamboo Round Yellow는 격자형 4다리라 더 다르다. 외형을 정확하게 유지하려면 목제 삼발이 모델을 찾아야 함.","followup":"1.20.1 Forge brown solid-wood round pedestal table, three short wooden feet variant. Vanilla oak slabs+fence+trapdoor are schematic only and require placement/collision."},{"i":83,"src":"new","model":"closet_6_birch","candidate":"","second":"mcwfurnitures:birch_double_wardrobe; Furnection wardrobe (source model not re-rendered)","status":"DEFER_TWO_TILE_DOUBLE_WARDROBE_TWO_BOTTOM_DRAWERS","shape":"Two connected PZ sprites form pale blond wood full-height double-door wardrobe with round brown center door pulls, two horizontal lower drawers each with pair round brown knobs, flat top, light side panel","size":"PZ 2×1 from 2 assembled sprites; wardrobe full height, MC source narrow 1-block and bottom drawer missing","why":"PZ는 밝은 갈색 두 문짝과 아래 서랍 2단(각 손잡이 2개)이 함께 있는 2칸 완성형 옷장이다. 기존 Macaw Acacia Double Wardrobe 렌더는 회색 나뭇결과 큰 붉은 문 일부만 나온 비정상 가구였다. 새 Decocraft Closet 6 Birch는 흰 나무색의 길고 가는 단문 옷장이며 하부 서랍이 아예 없다. Closet 2/4 Birch는 문 없이 옷이 걸린 열린 선반이고 Closet 3 Birch는 3단 서랍만 있다. 정확한 양문+2단 서랍 가구 미발견.","followup":"Macaw Double Wardrobe 원본 마크 모델 전체·멀티블록 생성 상태 정확히 열어보기. Furnection Forge 1.20.1 및 기타 실제 2칸+2단 서랍 옷장 모델 검증."},{"i":84,"src":"new","model":"bottom_cabinet_corner_inner_birch","candidate":"","second":"decocraft:bottom_cabinet_corner_outer_1_birch; vanilla stripped birch planks + trapdoor corner possible but game collision untested","status":"DEFER_BIRCHWOOD_INNER_CORNER_BROWN_COUNTERTOP","shape":"Plain honey/tan birch cabinet corner block with brown/tan wood top featuring right-angle inward square cut-out, light brown uniformly colored front/side, no visible white stone top","size":"PZ 1×1 single corner cabinet, inward cutout and direction matter; MC 1×1 model square/white top","why":"원본은 연갈색/벌꿀색 나무 코너 카운터로 오른쪽 뒤에 직각 홈이 있고 상판과 몸체가 거의 같은 계열의 갈색이다. 이전 Decocraft Diner Counter Corner Black은 줄무늬 검정 금속 카운터라 종류·재질 모두 틀렸다. 새 Bottom Cabinet Corner Inner Birch는 밝은 나무 몸체지만 상판이 새하얀 타일이고 렌더상 안쪽 L홈이 드러나지 않아 원본 같은 연결용 코너라고 확증할 수 없다. Outer 1/2도 동일한 상판·코너 결합 불확실성.","followup":"PZ facing별 실제 노치 좌표/방향, Decocraft 상부를 내려다보는 시점 3D 회전 확인 후 상판이 갈색인 모드/바닐라 연결형 코너 검색."},{"i":85,"src":"new","model":"wooden_table_spruce","candidate":"","second":"decocraft:cottage_coffee_table_long [low table with curved legs]; Re:Deco connecting tables (not source-rendered)","status":"DEFER_TWO_TILE_LONG_DARK_WOOD_DINING_TABLE","shape":"Long 2×1 classic dark brown solid wood rectangular dining table with thick plank top and only four plain square timber legs at outermost corners, no central supports","size":"PZ 2 joined tiles; MC inspected single square spruce table; connected 2×1 geometry not validated","why":"PZ 원본은 2타일 길이의 짙은 갈색 원목 상판과 네 모서리에 곧게 내려가는 두꺼운 나무 다리 네 개뿐이다. 기존 Decocraft Table Setting Double은 테이블이 아니라 접시·컵 세트로 잘못 매칭되었다. 새 Decocraft Wooden Table Spruce는 갈색 나무 재질이 유사하지만 정사각형 1칸이며 다리에 장식 고리가 있고 두 개를 붙이면 중간에 다리가 중복될 가능성이 높다. Cottage Coffee Table Long은 낮은 커피 테이블이라 높은 식탁과 안 맞는다.","followup":"2블록을 연결할 때 중앙 다리가 제거되는 Java 1.20.1 Forge 원목 테이블 모드·멀티블록 실제 모델 확인; 바닐라 다크오크 반블록/울타리 2×1 충돌 검증."},{"i":86,"src":"new","model":"wooden_table_ebony","candidate":"","second":"decocraft:cottage_coffee_table [brown but all-wood plain top]","status":"DEFER_SINGLE_SQUARE_INLAID_FANCY_WOOD_TABLE","shape":"Compact 1×1 square fancy medium brown wooden table with DARK rectangular central inset/possibly glass or leather, four stout straight brown legs, decorative corner square joinery","size":"PZ 1×1 fancy inlaid table; MC 1×1 source square, panel not present","why":"PZ 원본은 정사각 갈색 목제 프레임 안에 짙은 와인색/진갈색 직사각 인레이 상판이 구분되어 있고 네 다리와 모서리 장식이 보인다. 기존 Macaw Acacia Coffee Table는 회색 두꺼운 직사각 석판만 보여 틀렸다. 새 Decocraft Wooden Table Ebony는 어두운 목제 4다리와 정사각 비율은 있지만 상판이 한 가지 검정 나무색이며 중앙 이중 소재 패널·모서리 장식이 없다. Cottage Coffee Table도 단색 나무판이므로 원본 Fancy 구분 요소를 재현 못한다.","followup":"inlaid dark-center square wood end table, stained glass inset dark center table. Re:Deco display cases/tables actual models compare; 바닐라 카펫+목재 트랩도어 조합 높이 체크."},{"i":87,"src":"new","model":"diner_table_light_gray","candidate":"","second":"wooden_table_white [single ornate wooden table]; other 2×1 cream folding table mod unverified","status":"DEFER_TWO_TILE_LIGHT_SMOOTH_TRESTLE_TABLE","shape":"Long 2×1 smooth cream or pale light-gray rectangular tabletop, two separate folding dark metal T-shaped trestle end legs connected by supports, no four wooden corner legs","size":"PZ 2 original sprites length 2; MC Diner Table inspected 1×1 square top and single center pedestal","why":"원본은 가로로 두 타일 합쳐진 크림/밝은 회색 길쭉한 가판 상판과 좌우 양끝의 철제 접이식 T형 받침대가 있는 테이블이다. 기존 Decocraft Table Setting Double는 접시·유리컵 세트일 뿐 테이블이 아니다. 새 Decocraft Diner Table Light Gray는 밝은 상판은 비슷하지만 1×1 정사각이고 중앙에 단 하나 금속 기둥·바닥판이 있어 양끝 T형 2다리 구조가 전혀 다르다. Wooden Table White는 흰 4개의 나무장식 다리로 역시 잘못된 유형이다.","followup":"industrial folding conference/trestle table 2×1 1.20.1 Forge mod; dark metal T-end legs; PZ2타일 연결·실제 마크 2칸 배치와 탁자 아래 통로 확인."},{"i":88,"src":"new","model":"washer","candidate":"decocraft:washer","second":"refurbished_furniture:washer [runtime game model/blue variant unverified]; decocraft:dryer [wrong visible drum]","status":"CONDITIONAL_FRONT_LOADING_WASHER_DRYER_BLUE_TOP_MISMATCH","shape":"Single 1×1 white/light gray front-loading combo washer-dryer, conspicuously bright BLUE solid top/control fascia, right large round glass door and compact black square buttons panel","size":"PZ 1×1; Decocraft washer one-unit front-loader; Minecraft actual combo dryer function and placed size not tested","why":"PZ 원본은 파란 상판과 상부 파란 조작부, 아래 흰 네모 본체에 커다란 앞쪽 원형 세탁기 도어가 있는 콤보 세탁건조기다. 기존 Decocraft Washer 렌더는 전체 회색이라 사용자 구별점인 파란색이 사라지고 일부 모델만 보이는 것처럼 보여 원래 반려였다. 이번 실제 Decocraft Washer 30큐브 BBMODEL은 회색/흰 몸체·원형 유리 전면도어·위쪽 검정 조작부를 온전하게 보여 전체 구조가 비슷하다. 하지만 **파란 상판/파란 조작부가 아예 없고**, 게임에서 세탁+건조 둘 다 가능한지 확인하지 않아 조건부로만 유지한다.","followup":"blue-top front-loading washer/dryer variant from other Forge 1.20.1 mods; 실제 건조 기능·1×1 설치·PZ 우측 도어 위치 일치 확인."},{"i":89,"src":"new","model":"tv_old","candidate":"","second":"Simple Radio 1.20.1 Forge decorative antenna (JAR model not verified), J Radio antenna tiers (not Yagi verified)","status":"DEFER_TWO_TILE_OUTDOOR_YAGI_TV_AERIAL_ANTENNA","shape":"Outdoor rooftop OLD TV Yagi-like aerial: tall gray metal vertical mast with TWO multi-pronged long horizontal fishbone antenna arrays attached high and low; source PZ two-part isometric preview has stray detached metal fragment","size":"PZ 2 original sprites connected provisionally as 1×2; rooftop mast must be installed through 2+ vertical blocks, exact height unknown","why":"PZ 이름 Antenna/Old TV는 TV 본체가 아니라 야외 지붕용 금속 Yagi형 안테나 두 벌을 하나의 세로 기둥에 단 물체다. 기존에 마크 후보가 없었고, 새 Decocraft TV Old를 직접 렌더해 보니 나무 케이스·화면·토끼귀 2개가 달린 소형 브라운관 TV로 원본의 긴 수십 개 금속 막대와 전혀 다른 물건이다. Simple Radio의 장식용 Antenna 및 J Radio의 여러 antenna tiers는 1.20.1 Forge 공개 설명에서 확인했지만 실제 Yagi 모양인지는 모델을 확보하지 않아 보류.","followup":"https://www.curseforge.com/minecraft/mc-mods/simple-voice-radio/files/5411185 / https://www.curseforge.com/minecraft/mc-mods/j-radio 에서 원본 안테나 블록 모델 비교. 철창+피뢰침+엔드막대 등 바닐라 조합은 좌우 방사형 안테나 재현·배치 충돌 확인 전까지만 구상."},{"i":90,"src":"new","model":"double_bed_spruce_white","candidate":"","second":"decocraft:double_bed_black_white, decocraft:double_bed_oak_white (both have checker bedding and ornate pickets); vanilla white bed×2 seam wrong","status":"DEFER_MODERN_DOUBLE_BED_DARK_SOLID_WOOD_WHITE_MATTRESS","shape":"Modern 2×2 double bed: smooth large WHITE unpatterned mattress with tiny pillow seam, DARK rich reddish brown SOLID wooden rectangular headboard and closed full skirt/platform frame on 3 sides, no pickets at foot","size":"PZ 4 source sprite parts form 2×2 rectangle; Decocraft source double beds not placed in Minecraft engine; still 2×2 collision/footprint untested","why":"PZ 원본은 2×2 큰 현대식 흰색 단색 침대 매트리스와 짙은 적갈색 나무 프레임, 막힌 넓은 목재 머리판과 발판 없는 박스형 침대틀이다. 기존 Decocraft Double Bed Birch Black는 밝은 세로살 나무 침대틀에 검정 체크 침구라 완전히 틀렸다. 새 Spruce White는 나무 프레임 색상과 흰 침구가 더 비슷하나 침구 전체가 회색 체크무늬, 분리된 베개가 돌출되고 머리판·발쪽 난간이 세로살 장식 구조라 가장 중요한 깨끗한 흰색·막힌 플랫 플랫폼 형태와 다르다. Black White/Oak White도 동일한 구조적 문제를 해결하지 못한다.","followup":"Forge 1.20.1 dark walnut/mahogany platform double bed with smooth solid white mattress, flat solid rectangular headboard and 2×2 installed footprint. Vanilla 2 white beds adjacent produces seam so not matching as single bed."}]''')
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
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 081–090</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 4차 081~090</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(81,91))
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
 writecsv(OUT/"BATCH_081_090_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[81,82,83,84,85,86,87,89,90]
 writecsv(OUT/"BATCH_081_090_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_071_080_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:9]]==["001-010","011-020","021-030","031-040","041-050","051-060","061-070","071-080","081-090"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:8])
 groups[8]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[8]["review_file"]="batch_081_090_v1/BATCH_081_090_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"081-090","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":9,"batches_unreviewed":27,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=[
 "# 로즈우드 357종 — 9차 081~090번 원본 완성 가구 개별 시각 검수",
 "PZ B42 완성형 타일을 실제로 보고, Minecraft 1.20.1 Forge Decocraft 배포 원본 BBMODEL/텍스처 28종을 실제 Blockbench 5.2.2로 열어 각각 렌더링 후 구조·재질·색·크기를 대조. 모델 소스 SHA-256 보존.",
 "조건부 후보 1건(088), 기존/새 가구 미일치로 보류 9건(081,082,083,084,085,086,087,089,090). 원본 자동 357 후보를 정답으로 취급하지 않으며 1:1 외형/실제 마크 게임 설치·충돌·기능 인증 0.",
 "## 항목별 판정"
 ]
 for a in review:
  lines.append("- **%03d %s / %s** → %s | %s. %s"%(a["index"],a["pz_name"],a["pz_style"],
   a["new_candidate_id"] or "적합한 후보 미확인",a["review_status"],a["manual_review_reason"]))
 lines.extend([
 "## 다음에 찾을 다른 모드/바닐라",
 "081 곡선 타원 유리 상판 2타일 테이블/086 어두운 중심 인레이 탁자/085 긴 갈색 목제 식탁: Re:Deco Vanilla Inspired Furniture가 1.20.1 Forge를 지원하며 Coffee Tables/Tables/Counters를 제공함 (https://modrinth.com/mod/redeco). 아직 개별 가구 모델의 기하/크기 렌더 미검증.",
 "089 옥외 Yagi TV 안테나: Simple Radio 1.20.1 Forge에 장식 Antenna 블록 (https://www.curseforge.com/minecraft/mc-mods/simple-voice-radio/files/5411185), J Radio 1.20.1 Forge에 계층형 안테나 (https://www.curseforge.com/minecraft/mc-mods/j-radio). 두 모드의 실제 안테나 JAR 모델을 아직 렌더하지 않음. 검증 전까지 PZ 다수 가로 막대가 있는 2타일 안테나 대체품으로 승인 금지.",
 "083 2칸 목제 양문+하단 2개 서랍 옷장과 090 2×2 짙은 나무 현대식 흰 침대는 기존 Decocraft/단일 Macaw 프리뷰에서 중요한 구성 요소가 빠졌으므로 1:1 매칭을 보류한다.",
 "088 Combo Washer Dryer Blue: Decocraft Washer 실제 원본 모델은 정면 유리 도어가 있어 구조상 유사하나 파란 상판·파란 조작부가 없어 조건부. 세탁과 건조 두 기능 모두 검증 전.",
 "84 코너 상판 각도, 85·87 2칸 테이블 연결, 90 2×2 침대 모델 경계, 89 야외 높이/방향은 실제 MC 설치 테스트가 필요함.",
 "## 진행 범위",
 "전체 36묶음 중 9개(001~090), 90/357 스타일 개별 검수. 나머지 27묶음 미검수. 다음 091~100.",
 "## 산출 파일",
 "- INDEX.html 및 cards/: 10개 PZ 완성형 좌우 원본 Blockbench 비교 JPG. 반려 후보는 실제로 비교해 틀린 이유 표시",
 "- BATCH_081_090_MANUAL_VISUAL_REVIEW.csv: 원본 속성·기존/신규 ID·원본 모델 SHA-256·크기·보류 이유",
 "- BATCH_081_090_DEFERRED_OTHER_MODS.csv: 9종 다른 모드/바닐라 재검토 목록",
 "- BATCHES_ALL_357_PROGRESS.csv: 누적 36그룹 검수 추적",
 "- 28개 원본 모델 비교 자료: ten_batch_review/09_081_090/extra_decocraft_render/",
 "- 외부 유료/저작권 모드 원본 JAR 및 원본 텍스처는 재배포하지 않는다. 렌더 결과와 해시를 검수용으로만 보관."
 ])
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_081_090_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH09_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
