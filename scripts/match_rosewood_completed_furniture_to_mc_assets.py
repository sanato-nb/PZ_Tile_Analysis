#!/usr/bin/env python3
"""Match 357 complete PZ furniture model styles to existing MC Forge JAR blockstate asset IDs.
An asset candidate is NOT a visually certified model or a runtime-registered block.
"""
import csv,json,re,zipfile
from pathlib import Path
from collections import defaultdict,Counter

D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
OUT=D/"minecraft_real_furniture_matches_v3"
ASSETS=D/"minecraft_actual_mod_registry_v2/REAL_MOD_ASSET_CANDIDATES.csv"
PZ=D/"complete_furniture_visual_3d_v1/ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv"
GEO=D/"complete_furniture_visual_3d_v1/geometry_samples/3D_GEOMETRY_EVIDENCE.csv"
ALI={
"Chair":"chair|seat","Couch":"couch|sofa","Bench":"bench","Ottoman":"ottoman|footstool",
"Stool":"stool","Bed":"bed","Beds":"bed","Table":"table","Low Table":"table",
"Dark Round Table":"table","Oak Round Table":"table","Light Round Table":"table",
"Round Table":"table","Fancy Table":"table","Fancy Dark Table":"table",
"Shelves":"shelf|shelves|rack|bookcase","Drawers":"drawer|dresser",
"Wardrobe":"wardrobe|closet","Cabinet":"cabinet|cupboard",
"Locker":"locker","Chest":"chest","Cartbox":"box|cardboard|crate",
"Desk":"desk","Sink":"sink|basin","Counter":"counter|cabinet|worktop",
"Toilet":"toilet","Shower":"shower","Bath":"bath|bathtub",
"Fridge":"fridge|refrigerator","Freezer":"freezer","Oven":"oven|stove",
"Hood":"hood|extractor","Microwave":"microwave","Toaster":"toaster",
"Dishwasher":"dishwasher","Barbecue":"barbecue|grill",
"Washing Machine":"washer|washing_machine","Clothing Dryer":"dryer",
"Combo Washer Dryer":"washer|dryer","Blower":"blower|dryer",
"Computer":"computer|desktop","Television":"television|tv","Radio":"radio",
"Antenna":"antenna","Dish":"satellite|dish","Terminal":"terminal|computer",
"Projector":"projector","Walkie Talkie":"radio","Piano":"piano",
"Grand Piano":"piano","Jukebox":"jukebox","Drum":"drum",
"Microphone":"microphone","Speaker Cabinet":"speaker","Amplifier":"amplifier",
"Stand":"stand|rack","Mirror":"mirror","Lamp":"lamp","Fireplace":"fireplace",
"Round Bin":"bin|trashcan|trash_can","Recycle Bin":"bin|trashcan|trash_can",
"Green Garbage Bin":"bin|trashcan|trash_can","Bin":"bin|trashcan|trash_can",
"Dumpster":"dumpster|bin","Public Garbage Bin":"bin|trashcan|trash_can",
"Box":"box|crate","X-press":"coffee|coffee_machine",
"Deluxe":"espresso|coffee_machine","Industrial 2000":"fryer",
"Industrial":"fryer|oven","Machine":"pinball|arcade",
"Bowling Machine":"bowling","Bowling Rack":"bowling|rack",
"Hamster Wheel":"hamster|wheel","Contraption":"exercise|fitness",
"Generator":"generator","Sign":"sign"
}
SYN={
"grey":{"grey","gray"},"blue":{"blue"},"white":{"white"},"black":{"black"},
"green":{"green"},"red":{"red"},"brown":{"brown"},"yellow":{"yellow"},
"orange":{"orange"},"purple":{"purple"},"beige":{"beige","tan"},
"oak":{"oak"},"birchwood":{"birch"},"birch":{"birch"},
"metal":{"metal","steel","iron"},"steel":{"metal","steel","iron"},
"chrome":{"chrome","steel"},"wooden":{"oak","wood","wooden"},
"rattan":{"rattan","wicker"},"industrial":{"industrial"},
"antique":{"vintage","antique","retro"},"modern":{"modern"},
"corner":{"corner"},"bunk":{"bunk"},"wall":{"wall"},
"large":{"large","double"},"small":{"small","mini"}
}
# Curated direct checks from actual downloaded JAR blockstate filenames, never invented IDs.
# "visual" means source complete furniture was viewed against the PZ neutral 3D sample,
# but MC model is still NOT visually verified until its geometry is inspected.
CURATED={
 ("Bed","Large Oak"):("decocraft:double_bed_oak_white","DOUBLE_OAK_BED_FOOTPRINT_REVIEW"),
 ("Couch","Blue Rattan"):("mcwfurnitures:blue_couch","COLOR_AND_SEATING_SIMILARITY_RATTAN_NOT_VERIFIED"),
 ("Shelves","Large Metal"):("","NO_SUITABLE_METAL_SHELVING_BLOCK_IN_INSPECTED_JAR_IDS"),
 ("Chair","Grey"):("decocraft:school_chair_gray","GREY_SCHOOL_CHAIR_MORE_LIKELY_THAN_BULKY_ARMCHAIR_3D_NEEDS_TEXTURE_REVIEW"),
 ("Table","Large Oak"):("mcwfurnitures:oak_table","OAK_TABLE_NAME_AND_MATERIAL"),
 ("Fridge","White"):("pfm:white_fridge","WHITE_FRIDGE_FUNCTION_AND_COLOR"),
 ("Oven","Modern"):("pfm:gray_stove","STOVE_REPLACES_OVEN_CHECK_FRONT_SHAPE"),
 ("Toilet","Fancy"):("pfm:basic_toilet","TOILET_FUNCTION_SHAPE_STYLE_REVIEW"),
 ("Bath","Large Deluxe"):("refurbished_furniture:white_bath","WHITE_BATH_SOURCE_SPRITE_2_PARTS_MC_LINKED_HEAD_FOOT_CHECK"),
 ("Wardrobe","Oak"):("mcwfurnitures:oak_double_wardrobe","OAK_DOUBLE_WARDROBE"),
 ("Computer","Desktop"):("refurbished_furniture:computer","COMPUTER_FUNCTION_BUT_PZ_CRT_1990S_STYLE_UNVERIFIED"),
 ("Television","Antique"):("decocraft:crt_tv","RETRO_CRT_TV_SHAPE_MORE_PROMISING"),
 ("Microwave","Chrome"):("pfm:iron_microwave","SILVER_MICROWAVE_STYLE_REVIEW"),
 ("Counter","Steel"):("","WOODEN_COUNTERS_NOT_A_METAL_WORK_COUNTER"),
 ("Machine","PAWS Pinball"):("","NO_PINBALL_MACHINE_IN_INSPECTED_JAR_ASSETS"),
 ("Jukebox","Oldies"):("decocraft:jukebox","JUKEBOX_FUNCTION_MODEL_REVIEW"),
 ("Piano","Western"):("decocraft:piano_upright_spruce","UPRIGHT_WOODEN_PIANO_MODEL_REVIEW"),
 ("Grand Piano","Black"):("decocraft:piano_black","BLACK_PIANO_NOT_YET_VERIFIED_AS_GRAND"),
 ("Locker","Metal"):("decocraft:locker_gray","METAL_GREY_LOCKER_MODEL_ID_VERIFIED_VISUAL_NEEDS_INSPECTION"),
 ("Table","Pool"):("decocraft:pool_table","POOL_TABLE_FUNCTION_SHAPE_REVIEW"),
 ("Machine","Kaboom Arcade"):("decocraft:arcade_machine_pacman","ARCADE_MACHINE_DIFFERENT_GAME_SKIN"),
 ("Machine","Dr. Oids Arcade"):("decocraft:arcade_machine_space_invaders","ARCADE_MACHINE_DIFFERENT_GAME_SKIN")
}
BAD_ACCESSORIES={
 "Piano":["bench","stool"],"Grand Piano":["bench","stool"],
 "Oven":["hood","extractor","stovetop"],"Bed":["bedside"],
 "Television":["flipbook"],
 "Table":["coffee","end","side","bedside"],
 "Fridge":["open_bottom","open_top","open_full"]
}
def read(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(p,rows):
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def tokens(s):return re.findall(r"[a-z0-9]+",str(s).lower())
def alias_hit(s,alias):
 a="_".join(tokens(alias));s="_".join(tokens(s))
 return bool(re.search(r"(?:^|_)"+re.escape(a)+r"(?:_|$)",s))
def primary_aliases(name,group):
 if name=="Machine":
  return ["pinball"] if "pinball" in group.lower() else ["arcade"]
 if name=="CustomName":return []
 return ALI.get(name,"").split("|") if name in ALI else tokens(name)
def score(pz,mc):
 name=pz["CustomName"];group=pz["GroupName"]
 aliases=primary_aliases(name,group)
 hits=[a for a in aliases if a and alias_hit(mc["path_id"]+" "+mc["display_name"],a)]
 if not hits:return None
 if any(word in mc["path_id"] for word in BAD_ACCESSORIES.get(name,[])):
  return None
 hit=max(hits,key=len)
 candidate=set(tokens(mc["path_id"]+" "+mc["display_name"]))
 group_tokens=tokens(group)
 matched=[];contra=[]
 s=58 if alias_hit(mc["path_id"],name) else 53
 if name=="Counter" and hit=="cabinet":s-=7
 if name=="Bed" and hit=="bed" and group.lower().startswith("large"):s-=3
 for tok in group_tokens:
  if tok not in SYN:continue
  if candidate&SYN[tok]:matched.append(tok);s+=8
  elif tok in {"blue","red","green","white","black","grey","brown","yellow","purple"}:
   others={"blue","red","green","white","black","grey","gray","brown","yellow","purple","orange","pink"}
   if candidate&others:contra.append(tok+">"+"/".join(sorted(candidate&others)));s-=19
  elif tok in {"metal","steel","chrome"} and candidate&{"oak","wood","birch","spruce"}:
   contra.append(tok+">wood");s-=12
 if name=="Television" and "Antique" in group and not candidate&{"antique","retro","vintage","old"}:s-=8
 if name=="Shelves" and "Metal" in group and "bookcase" in candidate:s-=8
 if name=="Computer" and "Desktop" in group and candidate&{"laptop"}:s-=16
 if "corner" in group_tokens and "corner" not in candidate:s-=8
 if "bunk" in group_tokens and "bunk" not in candidate:s-=10
 pref=pz.get("minecraft_primary_mod","").lower()
 preferred={"paladins":"paladin","macaws":"macaw","refurbished":"refurbished","decocraft":"decocraft",
 "handcrafted":"handcrafted","arcade":"arcade","immersive":"immersive"}
 if preferred.get(mc["source_mod"],"source-no-match") in pref:s+=5
 if int(mc["model_name_count"] or 0)>0:s+=3
 return dict(score=s,hit=hit,style="|".join(matched),conflict="|".join(contra),mc=mc)
def main():
 if OUT.exists() and any(OUT.iterdir()):raise FileExistsError(OUT)
 OUT.mkdir(parents=True,exist_ok=True)
 pz=read(PZ);mods=read(ASSETS);geom=read(GEO)
 assert len(pz)==357 and len(mods)>5000
 assert all(x["evidence_type"]=="BLOCKSTATE_JSON" for x in mods)
 geokeys={(x["CustomName"],x["GroupName"]):x for x in geom}
 index=defaultdict(list)
 for mc in mods:
  for token in set(tokens(mc["path_id"]+" "+mc["display_name"])):index[token].append(mc)
 found=[];candidates=[];stat=Counter()
 for row in pz:
  opts={}
  for alias in primary_aliases(row["CustomName"],row["GroupName"]):
   for token in tokens(alias):
    for mc in index.get(token,[]):opts[mc["source_mod"]+"|"+mc["registry_id"]]=mc
  matched=[]
  for mc in opts.values():
   data=score(row,mc)
   if data:matched.append(data)
  matched.sort(key=lambda x:x["score"],reverse=True)
  choices=[];seen=set()
  for x in matched:
   mod=x["mc"]["source_mod"]
   if mod in seen:continue
   choices.append(x);seen.add(mod)
   if len(choices)==3:break
  best=choices[0] if choices else None
  reviewed=CURATED.get((row["CustomName"],row["GroupName"]))
  override_note=""
  if reviewed is not None:
   required_id,override_note=reviewed
   if not required_id:
    best=None
    choices=[]
   else:
    asset=next((m for m in mods if m["registry_id"]==required_id),None)
    if asset is None:raise RuntimeError("Curated ID not found in actual jar: "+required_id)
    hit=score(row,asset)
    if hit is None:
     hit=dict(score=50,hit="CURATED_CATEGORY",style="",conflict="",mc=asset)
    choices=[hit]+[c for c in choices if c["mc"]["registry_id"]!=required_id][:2]
    best=choices[0]
  if not best or best["score"]<43:state="NO_REAL_ASSET_CANDIDATE"
  elif best["score"]>=67 and best["style"]:state="NAME_AND_STYLE_CANDIDATE"
  elif best["score"]>=56:state="FUNCTION_OR_NAME_CANDIDATE"
  else:state="BROAD_SUBSTITUTE_CANDIDATE"
  if reviewed is not None and not reviewed[0]:
   state="NO_SUITABLE_SHAPE_OR_MATERIAL_IN_INSPECTED_MODS"
  elif reviewed is not None and reviewed[0]:
   state="MANUALLY_SELECTED_REAL_JAR_ASSET_REVIEW_GEOMETRY"
  geo=geokeys.get((row["CustomName"],row["GroupName"]),{})
  data=dict(pz_model_name=row["CustomName"],pz_model_style=row["GroupName"],
      pz_complete_png_path=row["preview_path"],
      pz_public_3d_obj_ids=row["reference_3d_model_ids"],
      pz_3d_reference_status=row["reference_3d_binding_coverage"],
      pz_3d_geometry_bbox_xyz=geo.get("raw_model_bbox_xyz",""),
      pz_3d_geometry_png=geo.get("side_by_side_preview",""),
      pz_original_sprite_parts=row["representative_num_parts"],
      pz_original_sprite_grid=row["representative_sprite_grid_positions"],
      rosewood_core_provisional_instances=row["core_placed_object_candidates"],
      match_class=state,
      curated_asset_verification_note=override_note,
      manual_curated_from_verified_jar_asset="YES" if reviewed else "NO",
      mc_primary_mod=best["mc"]["source_mod"] if best else "",
      mc_primary_blockstate_id=best["mc"]["registry_id"] if best else "",
      mc_primary_blockstate_resource=best["mc"]["evidence_path"] if best else "",
      mc_primary_model_resource_refs=best["mc"]["referenced_models"] if best else "",
      match_search_score=best["score"] if best else 0,
      name_alias_hit=best["hit"] if best else "",
      style_token_match=best["style"] if best else "",
      style_conflicts=best["conflict"] if best else "",
      mc_alternative_id_1=choices[1]["mc"]["registry_id"] if len(choices)>1 else "",
      mc_alternative_id_2=choices[2]["mc"]["registry_id"] if len(choices)>2 else "",
      whole_furniture_geometry_required="YES" if int(row["representative_num_parts"])>1 else "SINGLE_TILE_OR_UNKNOWN",
      mc_mod_loaded_in_game="NOT_TESTED",
      mc_real_block_registry_confirmed="NOT_TESTED",
      mc_visual_3d_equivalence_verified="NO",
      next_step="Compare complete PZ PNG and public 3D bbox to actual MC block model & textures")
  found.append(data);stat[state]+=1
  for rank,x in enumerate(choices,1):
   mc=x["mc"]
   candidates.append(dict(pz_name=row["CustomName"],pz_style=row["GroupName"],rank=rank,
      mod=mc["source_mod"],blockstate_id=mc["registry_id"],asset_path=mc["evidence_path"],
      referenced_models=mc["referenced_models"],score=x["score"],
      alias=x["hit"],style_match=x["style"],style_conflict=x["conflict"],
      original_full_png=row["preview_path"],visual_verified="NO"))
 write(OUT/"ROSEWOOD_357_PZ_TO_REAL_MINECRAFT_BLOCKSTATE_MATCH.csv",found)
 write(OUT/"ALL_RANKED_MATCHED_MC_BLOCKSTATE_IDS.csv",candidates)
 counts=[dict(mod=x,status=y,count=v) for (x,y),v in sorted(Counter((r["mc_primary_mod"],r["match_class"]) for r in found).items())]
 write(OUT/"STATUS_BY_MOD.csv",counts)
 manifest=dict(pz_styles=357,mc_blockstate_asset_ids_audited=len(mods),
    mapped_styles=sum(v for k,v in stat.items() if k!="NO_REAL_ASSET_CANDIDATE"),
    no_blockstate_name_match=stat["NO_REAL_ASSET_CANDIDATE"],
    status_counts=dict(stat),candidate_rows=len(candidates),
    actual_3d_equivalence_verified=0,
    limitation="Asset blockstates exist in downloaded Forge JAR but runtime registration, rendered MC shape and source model material equivalence not verified.",
    source_inventory="../minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 keys=[("Bed","Large Oak"),("Couch","Blue Rattan"),("Shelves","Large Metal"),
 ("Chair","Grey"),("Fridge","White"),("Oven","Modern"),("Toilet","Fancy"),
 ("Bath","Large Deluxe"),("Wardrobe","Oak"),("Computer","Desktop"),
 ("Television","Antique"),("Microwave","Chrome"),("Counter","Steel"),
 ("Table","Large Oak"),("Machine","PAWS Pinball"),("Jukebox","Oldies"),
 ("Piano","Western"),("Grand Piano","Black")]
 selected=[next((r for r in found if r["pz_model_name"]==n and r["pz_model_style"]==g),None) for n,g in keys]
 selected=[r for r in selected if r]
 lines=["# 로즈우드 357개 완성 가구 → 실제 모드 JAR에 존재하는 블록 모델 후보",
 "","Minecraft Java 1.20.1 Forge 모드 7개의 실제 JAR에 존재하는 blockstates/*.json 경로를 기반으로 원본 357종을 비교.",
 "","## 집계 결과"]
 lines += ["- "+k+": "+str(v)+"종" for k,v in sorted(stat.items(),key=lambda x:-x[1])]
 lines += ["","## 실제 블록 자산 ID로 대응한 대표 가구",
 "| 원본 완성 가구 | 부품 수 | 실제 MC 블록 상태 자산 ID | 근거 수준 |","|---|---:|---|---|"]
 for r in selected:
  lines.append("| "+r["pz_model_name"]+" / "+r["pz_model_style"]+
    " | "+str(r["pz_original_sprite_parts"])+" | "+
    (r["mc_primary_blockstate_id"] or "없음")+" | "+r["match_class"]+" |")
 lines += ["","## 중요한 제한",
 "- 실제 모드 JAR의 블록상태 모델을 직접 읽어 확인했지만, 해당 ID가 게임에 등록되어 사용되는지는 미검증이다.",
 "- 원본 PNG의 다칸 가구는 전체를 하나로 보고 평가한다. Minecraft 가구 1블록으로 자동 대체할 경우 크기와 외형이 달라질 수 있다.",
 "- 모델의 색상·질감·3D 윤곽 일치 여부는 아직 별도 렌더 검증 전이다. 위 표는 존재하는 Minecraft 블록 자산 기반 후보이며 '정확하게 같다'는 확정이 아니다.",
 "- 모드가 동적으로 생성하는 가구는 blockstates/ JSON 파일을 사용하지 않을 수도 있어 누락될 수 있다.",
 "- JAR과 텍스처 파일 자체는 재배포하지 않고 자산 경로와 원본 버전 해시만 남겼다.",
 "","## 파일",
 "- ROSEWOOD_357_PZ_TO_REAL_MINECRAFT_BLOCKSTATE_MATCH.csv: 357종 완성 가구 PNG·PZ3D·실존 MC 블록 상태 ID 매핑",
 "- ALL_RANKED_MATCHED_MC_BLOCKSTATE_IDS.csv: 각 가구에 대해 최대 3개 실제 모드 후보",
 "- STATUS_BY_MOD.csv: 1순위 모드별 잠정 검색 근거 집계",
 "- ../minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json: 모드 실제 버전/다운로드 해시 증거",
 "","**확정된 마인크래프트 3D 외형 1:1 대응:** 현재 0종. 나머지는 실제 모델 검수 후보다."]
 (OUT/"README_KO.md").write_text("\n".join(lines)+"\n",encoding="utf8")
 with zipfile.ZipFile(OUT/"ROSEWOOD_357_REAL_MINECRAFT_MATCHES.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in OUT.iterdir():
   if f.name!="ROSEWOOD_357_REAL_MINECRAFT_MATCHES.zip":z.write(f,f.name)
 print(json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
