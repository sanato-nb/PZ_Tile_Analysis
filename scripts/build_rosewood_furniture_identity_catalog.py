#!/usr/bin/env python3
"""Create source-grounded Rosewood furniture identity hierarchy; never overmerge."""
from pathlib import Path
from collections import defaultdict,Counter
import csv,json,hashlib,re,shutil,zipfile,html

R=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
X=R/"complete_furniture_visual_3d_v1"
O=R/"furniture_identity_catalog_20261103"
def load(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def save(p,rows):
 assert rows,"empty output "+str(p)
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows)
def sid(*parts):
 return hashlib.sha1("\x1f".join(parts).encode("utf8")).hexdigest()[:12].upper()
def key(x):
 return x["CustomName"],x["GroupName"]
def uniq(xs):
 return sorted(set(x for x in xs if x))
def u(xs):
 return "|".join(uniq(xs))
def props(x):
 return json.loads(x.get("original_properties_json") or "{}")
def gridpos(v):
 m=re.fullmatch(r"\s*(-?\d+)\s*,\s*(-?\d+)\s*",v or "")
 return tuple(map(int,m.groups())) if m else None
def risk(a,b):
 af=set(a["directions"].split("|"));bf=set(b["directions"].split("|"))
 ma=set(filter(None,a["viewpoint_ids"].split("|")));mb=set(filter(None,b["viewpoint_ids"].split("|")))
 if af&bf and ma and mb and not ma&mb:return "HIGH_SAME_FACING_DIFFERENT_3D_ASSET","DO_NOT_MERGE_UNTIL_PNG_AND_3D_REVIEW"
 if not af&bf and ma and mb and ma==mb:return "LIKELY_SAME_DESIGN_COMPLEMENTARY_DIRECTIONS","CONFIRM_VISUALLY_FIRST"
 if not af&bf and ma and mb and ma&mb:return "LIKELY_SAME_DESIGN_SHARED_3D_PARTS","CONFIRM_VISUALLY_FIRST"
 if af&bf and (not ma or not mb):return "OVERLAPPING_FACING_MISSING_3D_EVIDENCE","COMPARE_PNG_3D_BEFORE_MERGING"
 return "SAME_NAME_CROSS_TILESET","COMPARE_SOURCE_PREVIEWS"
def main():
 assert not O.exists(),"Refuse overwrite"
 (O/"reference_previews").mkdir(parents=True)
 styles=load(X/"ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv")
 links=load(X/"ALL_SOURCE_SPRITE_TO_VIEWPOINT_3D_BINDINGS.csv")
 defs=load(R/"ALL_FURNITURE_TILE_IDS.csv")
 basic=load(R/"furniture_dedup_v1/FURNITURE_MODELS_DEDUP_NAME_GROUP.csv")
 unnamed=load(R/"furniture_dedup_v1/UNNAMED_ASSET_KEYS_NOT_VALIDATED_MODELS.csv")
 assert (len(styles),len(links),len(defs),len(basic))==(357,1347,4248,357)
 assert [int(x["index"]) for x in styles]==list(range(1,358))
 sk={key(x):x for x in styles}
 assert len(sk)==357
 definitions={x["source_key"]:x for x in defs}
 metadata={key(x):x for x in basic}
 families=sorted({x["CustomName"] for x in styles},key=str.casefold)
 assert len(families)==79
 fid={n:"FAM-"+str(i).zfill(3) for i,n in enumerate(families,1)}
 grouped=defaultdict(list)
 for x in links:
  src=x["tileset"]+"/"+x["local_id"]
  assert src in definitions,src
  assert key(x)==key(definitions[src]),src
  assert key(x) in sk,key(x)
  grouped[key(x)].append(x)
 assert len(grouped)==357
 out_styles=[];out_sheets=[];out_templates=[];out_sources=[];out_groups=[];out_issues=[];out_cross=[];struct=[]
 cat=defaultdict(list)
 model_to_styles=defaultdict(set)
 for x in styles:
  sty="STYLE-"+sid(x["CustomName"],x["GroupName"])
  group_id=fid[x["CustomName"]]
  members=grouped[key(x)]
  bysheet=defaultdict(list)
  for m in members:bysheet[m["tileset"]].append(m)
  allproperties=defaultdict(set)
  sheetrecords=[];faced=[]
  for sheet,items in sorted(bysheet.items()):
   v_id="SOURCE-"+sid(x["CustomName"],x["GroupName"],sheet)
   seen=uniq(t["Facing"] or "(unset)" for t in items)
   modids=uniq(t["viewpoint_3d_model_id"] for t in items)
   sheetrecord=dict(style_id=sty,source_variant_id=v_id,CustomName=x["CustomName"],
    GroupName=x["GroupName"],tileset=sheet,directions="|".join(seen),
    direction_count=len(seen),sprite_ids="|".join(t["local_id"] for t in items),
    source_sprite_count=len(items),viewpoint_ids="|".join(modids),
    has_proven_distinct_3d_design="NO")
   sheetrecords.append(sheetrecord)
   out_sheets.append(sheetrecord)
   for direction in seen:
    group=[t for t in items if (t["Facing"] or "(unset)")==direction]
    positions=[gridpos(t["SpriteGridPos"]) for t in group]
    placed=[p for p in positions if p is not None]
    if not placed:
     width=height=1
     status="MULTIPLE_LOCAL_IDS_WITHOUT_GRID" if len(group)>1 else "SINGLE_SPRITE_NO_GRID"
    else:
     width=max(p[0] for p in placed)-min(p[0] for p in placed)+1
     height=max(p[1] for p in placed)-min(p[1] for p in placed)+1
     status=("MIXED_GRID_AND_NONGRID" if len(placed)!=len(group)
      else "DUPLICATE_GRID_CELLS" if len(set(placed))!=len(placed)
      else "INCOMPLETE_GRID" if width*height!=len(placed)
      else "RECTANGULAR_GRID_COMPLETE")
    record=dict(style_id=sty,source_variant_id=v_id,CustomName=x["CustomName"],
     GroupName=x["GroupName"],tileset=sheet,facing=direction,
     source_sprite_ids="|".join(sheet+"/"+t["local_id"] for t in group),
     source_grid_positions="|".join(t["SpriteGridPos"] or "(no grid)" for t in group),
     sprite_count=len(group),source_footprint=str(width)+"x"+str(height),
     width=width,height=height,grid_status=status,
     reference_3d_model_ids=u(t["viewpoint_3d_model_id"] for t in group),
     status_note="ORIENTATION_TEMPLATE_NOT_A_SEPARATE_FURNITURE")
    out_templates.append(record);faced.append(record)
   for item in items:
    source=sheet+"/"+item["local_id"]
    data=definitions[source]
    p=props(data)
    for k in ["CustomItem","IsoType","container","ContainerCapacity","Material","MaterialType",
     "IsMoveAble","BlocksPlacement","Surface","PickUpWeight","ItemHeight","CanScrap"]:
     if k in p and p[k] not in ("",None):allproperties[k].add(str(p[k]))
    if item["viewpoint_3d_model_id"]:model_to_styles[item["viewpoint_3d_model_id"]].add(sty)
    out_sources.append(dict(style_id=sty,source_variant_id=v_id,
     tileset=sheet,local_id=item["local_id"],source_key=source,
     CustomName=x["CustomName"],GroupName=x["GroupName"],
     Facing=item["Facing"],SpriteGridPos=item["SpriteGridPos"],
     core_sprite_placements=data["core_sprite_placements"],
     pixel_status=data["pixel_status"],source_category=data["category"],
     original_properties_json=data["original_properties_json"],
     viewpoint_model_id=item["viewpoint_3d_model_id"],
     viewpoint_binding=item["binding_state"]))
  warnings=[]
  if len(sheetrecords)>1:warnings.append("CROSS_TILESET_SAME_NAMED_STYLE")
  if any(q["grid_status"] in ("MULTIPLE_LOCAL_IDS_WITHOUT_GRID","MIXED_GRID_AND_NONGRID","DUPLICATE_GRID_CELLS","INCOMPLETE_GRID") for q in faced):warnings.append("SOURCE_GRID_AMBIGUITY")
  if len(allproperties.get("CustomItem",()))>1:warnings.append("PICKUP_ITEM_PROPERTY_VARIATION")
  if len(allproperties.get("IsoType",()))>1:warnings.append("ISO_TYPE_PROPERTY_VARIATION")
  if len(uniq(t["Facing"] for t in members))==1:warnings.append("ONLY_ONE_DIRECTION_RECORDED")
  if x["reference_3d_binding_coverage"]=="NO_PUBLIC_3D_BINDING":warnings.append("PUBLIC_3D_REFERENCE_NOT_FOUND")
  if x["CustomName"].lower() in ("customname","groupname","unknown","none"):warnings.append("SUSPICIOUS_NAME_LABEL")
  preview=Path(x["preview_path"]).name
  srcimg=X/"previews"/preview
  assert srcimg.exists(),srcimg
  shutil.copy2(srcimg,O/"reference_previews"/preview)
  propjson=json.dumps({k:sorted(v) for k,v in sorted(allproperties.items())},ensure_ascii=False,sort_keys=True)
  row=dict(index=int(x["index"]),style_id=sty,family_id=group_id,
   CustomName=x["CustomName"],GroupName=x["GroupName"],
   display_name=(x["GroupName"]+" " if x["GroupName"] else "")+x["CustomName"],
   family_category=metadata[key(x)]["source_categories"],
   source_tileset_count=len(sheetrecords),source_tilesets=u(bysheet),
   sprite_source_count=len(members),
   source_facings=u(t["Facing"] for t in members),
   source_facing_count=len(uniq(t["Facing"] for t in members)),
   source_oriented_templates=len(faced),
   representative_sprite_parts=x["representative_num_parts"],
   representative_grid_area=x["representative_source_grid_area"],
   has_multipart_source_template="YES" if any(q["grid_status"]=="RECTANGULAR_GRID_COMPLETE" and q["sprite_count"]>1 for q in faced) else "NOT_CONFIRMED",
   original_properties_json=propjson,
   CustomItem_values="|".join(sorted(allproperties.get("CustomItem",[]))),
   IsoType_values="|".join(sorted(allproperties.get("IsoType",[]))),
   Material_values="|".join(sorted(allproperties.get("Material",[]))),
   original_preview_path="reference_previews/"+preview,
   public_3d_binding=x["reference_3d_binding_coverage"],
   viewpoint_model_ids=u(t["viewpoint_3d_model_id"] for t in members),
   viewpoint_source_url=x["reference_3d_model_file_urls"],
   issues="|".join(warnings),
   physical_design_identity_verified="NO",
   minecraft_model_approved="NO",
   identity_status="UNVERIFIED_PHYSICAL_DESIGN",
   legacy_357_index=x["index"])
  out_styles.append(row)
  cat[x["CustomName"]].append(row)
  if warnings:out_issues.append(dict(index=x["index"],style_id=sty,CustomName=x["CustomName"],
   GroupName=x["GroupName"],issues="|".join(warnings),source_preview=row["original_preview_path"]))
  struct.append(dict(style_id=sty,family_id=group_id,
   index=int(x["index"]),name=x["CustomName"],group=x["GroupName"],
   source_tilesets=sheetrecords,
   source_orientation_grid_templates=faced,
   original_properties=json.loads(propjson),
   viewpoints=row["viewpoint_model_ids"].split("|") if row["viewpoint_model_ids"] else [],
   preview=row["original_preview_path"],review_flags=warnings,
   certified_same_3d_design=False))
  if len(sheetrecords)>1:
   assert len(sheetrecords)==2,"unexpected more than two tile sets"
   a,b=sheetrecords
   typ,action=risk(a,b)
   out_cross.append(dict(index=x["index"],style_id=sty,
    CustomName=x["CustomName"],GroupName=x["GroupName"],
    tileset_a=a["tileset"],facings_a=a["directions"],viewpoint_a=a["viewpoint_ids"],
    tileset_b=b["tileset"],facings_b=b["directions"],viewpoint_b=b["viewpoint_ids"],
    evidence_class=typ,action=action,physical_equivalence_confirmed="NO"))
 for name in sorted(cat,key=lambda n:(-len(cat[n]),n.casefold())):
  v=cat[name]
  out_groups.append(dict(family_id=fid[name],CustomName=name,styles=len(v),
    source_tileset_variants=sum(z["source_tileset_count"] for z in v),
    sprite_refs=sum(z["sprite_source_count"] for z in v),
    multi_part_styles=sum(int(z["representative_sprite_parts"])>1 for z in v),
    style_ids="|".join(z["style_id"] for z in v),
    style_names="|".join(z["GroupName"] or "(none)" for z in v),
    do_not_auto_merge_different_styles="YES"))
 assert (len(out_styles),len(out_sheets),len(out_sources),len(out_groups),len(out_cross))==(357,362,1347,79,5)
 save(O/"CATALOG_357_STYLES.csv",out_styles)
 save(O/"FAMILIES_79.csv",out_groups)
 save(O/"SOURCE_TILESET_VARIANTS_362.csv",out_sheets)
 save(O/"ORIENTATION_GRID_TEMPLATES.csv",out_templates)
 save(O/"SOURCE_SPRITES_1347.csv",out_sources)
 save(O/"SAME_NAME_MULTIPLE_TILESETS_5.csv",out_cross)
 save(O/"NEEDS_IDENTITY_REVIEW.csv",out_issues)
 unmatched=[x for x in unnamed if x["zone"]=="CORE" and x["scope"]=="CORE_FURNITURE"]
 assert unmatched
 save(O/"UNNAMED_CORE_ASSETS_NOT_IN_357.csv",unmatched)
 shared=[dict(viewpoint_model_id=model,style_ids="|".join(sorted(styles)),
  assessment="SAME_SOURCE_3D_REFERENCE_NOT_PROOF_OF_SAME_COMPLETE_FURNITURE")
  for model,styles in sorted(model_to_styles.items()) if len(styles)>1]
 if shared:save(O/"SHARED_VIEWPOINT_MODEL_REVIEW.csv",shared)
 (O/"FURNITURE_IDENTITY.json").write_text(json.dumps(struct,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 counts=Counter(r["public_3d_binding"] for r in out_styles)
 orient=Counter(int(r["source_facing_count"]) for r in out_styles)
 grid=Counter(r["grid_status"] for r in out_templates)
 cross=Counter(r["evidence_class"] for r in out_cross)
 manifest=dict(style_labels=357,broad_furniture_names=79,source_tile_records=1347,
  named_source_tileset_variants=362,oriented_source_templates=len(out_templates),
  source_facing_counts=dict(sorted(orient.items())),
  representative_multitile_styles=sum(int(x["representative_sprite_parts"])>1 for x in out_styles),
  cross_tileset_overlap_candidates=5,cross_tileset_risk_counts=dict(cross),
  original_3d_binding_coverage=dict(counts),source_grid_validation=dict(grid),
  unnamed_core_asset_keys=len(unmatched),
  unnamed_core_placed_candidates=sum(int(x["placed_sprite_objects"]) for x in unmatched),
  shared_3d_reference_across_named_styles=len(shared),
  physical_unique_designs="NOT_CERTIFIED",
  game_runtime_verified=0,source_files_overwritten=False)
 (O/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 txt=["# 로즈우드 원본 가구 정체 목록 (2026-11-03)",
 "## 357종이라는 숫자의 정확한 의미",
 "357개는 방향을 한 차례 합친 CustomName + GroupName 조합이야. 79개 CustomName은 넓은 종류이지 실제 디자인 수가 아니고, 357개도 최종 서로 다른 완성형 가구 3D 디자인 수가 아니야.",
 "원본 타일 ID 1,347개를 정의 파일·방향·SpriteGridPos·기능 속성·Viewpoint 참고 모델에 연결했고, 타일셋 출처를 보존한 스타일은 362개야.",
 "## 동일 이름·스타일이 두 타일셋에서 나타나는 5개"]
 for x in out_cross:txt.append("- "+x["CustomName"]+" / "+x["GroupName"]+
  " : "+x["tileset_a"]+" ["+x["facings_a"]+"] / "+x["tileset_b"]+" ["+x["facings_b"]+"] => "+x["evidence_class"])
 txt.extend(["Counter / Wooden Corner은 같은 방향 네 가지가 두 타일셋에 존재하지만 서로 다른 Viewpoint OBJ 연결명을 갖고 있어 **잘못 합쳐졌을 가능성을 반드시 확인**해야 해. Chair / Modern White 등은 같은 3D 모델이 두 방향 그룹에 나뉘어 있으므로 방향별 자산 분리일 가능성이 높아.",
 "## 가구 정체 계층",
 "79 family -> 357 style labels -> 362 source tileset variants -> facing N/E/S/W(or missing) -> SpriteGridPos parts.",
 "게임 맵의 가구 배치 인스턴스는 별도 층위로 유지하고, 제작용 Blockbench 모델 수는 수동 확인 전까지 확정하지 않아.",
 "Viewpoint 모델은 공개 3D모드의 참고 바인딩이지 공식 PZ 가구 identity ID가 아냐. 원본 B42.20.3과 Viewpoint 모델 기준의 버전 차이가 있으므로 그대로 동등하다고 할 수 없어.",
 "## 원본 자료와 검수 파일",
 "- CATALOG_357_STYLES.csv : 원본 스타일 357개와 방향·부품·속성·3D 연결, 위험 표시.",
 "- FAMILIES_79.csv : 큰 가구 범주 79개(스타일을 자동 통합하지 않음).",
 "- SOURCE_TILESET_VARIANTS_362.csv : 같은 이름도 출처 타일셋이 다르면 분리 보존.",
 "- ORIENTATION_GRID_TEMPLATES.csv : 타일셋별 방향·부품과 SpriteGridPos.",
 "- SOURCE_SPRITES_1347.csv : 개별 타일마다 원본 정의 전체 속성 + 3D 모드 바인딩.",
 "- SAME_NAME_MULTIPLE_TILESETS_5.csv : 중복 통합의 근거 및 예외 5개.",
 "- UNNAMED_CORE_ASSETS_NOT_IN_357.csv : 이름 없어 357종 목록에 아예 빠진 원본 후보.",
 "- FURNITURE_IDENTITY.json : 향후 Forge 가구 모드 데이터베이스용 JSON 구조.",
 "- reference_previews/ : 기존 완성형 원본 타일 이미지 357개 그대로 복사.",
 "- INDEX.html : 79개 이름/스타일 검색·필터 가능한 오프라인 가구 도감.",
 "## 다음 검수",
 "1. 동일 이름 다중 타일셋 5종 중 Counter Wooden Corner과 Table Large Dark Oak부터 시각 검증.",
 "2. 같은 이름 다른 GroupName들이 실제 같은 형상이고 색상만 다른지 3D·PNG 대조.",
 "3. 여러 타일 가구, 일부 방향만 존재하는 가구의 조립을 점검.",
 "4. 이름 없는 물체는 최종 목록에 별도 추가 검증. 현재 357에 포함되지 않음.",
 "5. 확정된 디자인별로 Minecraft용 1개 모델 + facing/blockstate + 필요한 색상·재질 변형 설계.",
 "## 하지 않은 일",
 "357종을 모두 동일 디자인이라고 단정하지 않았고 3D모드 OBJ를 재배포하지 않았어. TMX, TileDef, PNG, 이전 매칭 결과의 어떤 원본도 변경하지 않았어."])
 (O/"README_KO.md").write_text("\n\n".join(txt)+"\n",encoding="utf8")
 md="# 좀보이드 원본 가구 357종 이미지 도감\n\n원본 PNG 조립 참고 이미지이며 Minecraft 가구 모델이 아니야. [검증 기준](README_KO.md)\n\n"
 for name in sorted(cat,key=lambda x:(-len(cat[x]),x.casefold())):
  md+="## "+name+" ("+str(len(cat[name]))+"스타일)\n\n"
  for r in cat[name]:
   md+="### "+str(r["index"]).zfill(3)+" · "+(r["GroupName"] or "(GroupName 없음)")+"\n\n"
   md+="!["+html.escape(r["display_name"])+"]("+r["original_preview_path"]+")\n\n"
   md+=("원본 방향: "+(r["source_facings"] or "미기록")+
       " / 타일셋: "+r["source_tilesets"]+" / 3D: "+r["public_3d_binding"]+"\n\n")
 (O/"FURNITURE_SOURCE_IMAGE_INDEX.md").write_text(md,encoding="utf8")
 def js(x):return json.dumps(x,ensure_ascii=False).replace("<","\\u003c")
 ui=[dict(i=r["index"],n=r["display_name"],family=r["CustomName"],
  group=r["GroupName"],img=r["original_preview_path"],f=r["source_facings"],
  sheets=r["source_tilesets"],num=r["sprite_source_count"],
  multi=r["has_multipart_source_template"]=="YES",
  bind=r["public_3d_binding"],flags=r["issues"],id=r["style_id"])
  for r in out_styles]
 htmlview='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood furniture source identity</title><style>
 body{font:14px system-ui,'Malgun Gothic',sans-serif;margin:0;background:#eaf0f4;color:#2d4051}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #cbd8e4;padding:14px 3%;z-index:2}
 h1{font-size:21px;margin:0 0 8px}header p{font-size:13px;line-height:1.5}
 nav{display:flex;gap:8px;flex-wrap:wrap}input,select{font:inherit;border:1px solid #c8d2dc;border-radius:7px;padding:9px}
 input{min-width:170px;flex:1}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr));gap:12px;padding:15px 3%}
 article{background:white;border:1px solid #d4dee5;border-radius:11px;padding:10px}
 img{width:100%;height:230px;object-fit:contain;background:#e5edf2}h2{font-size:16px}
 p{font-size:12px;line-height:1.45}code{overflow-wrap:anywhere}
 </style></head><body><header><h1>좀보이드 로즈우드 가구 정체 목록</h1>
 <p>79개 가구 이름 / 357개 명명 스타일 / 362개 원본 출처별 스타일 / 1347개 원본 타일 기록.
 이것은 최종 고유 3D 디자인 수가 아니며, 별도로 다칸·방향·원본 3D 검증이 필요함.</p>
 <nav><input id="search" placeholder="가구 이름·스타일·타일셋 검색"><select id="family"><option value="">가구 전체</option></select>
 <select id="filter"><option value="">모든 상태</option><option value="cross">타일셋 중복 5종</option>
 <option value="multi">여러 타일 조립</option><option value="no3d">3D 바인딩 없음</option></select><span id="count"></span></nav></header><main id="cards"></main>
 <script>let rows=__DATA__,search=document.getElementById('search'),fam=document.getElementById('family'),filter=document.getElementById('filter'),cards=document.getElementById('cards'),count=document.getElementById('count');
 let esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 for(let name of [...new Set(rows.map(x=>x.family))].sort()){let o=document.createElement('option');o.value=name;o.textContent=name;fam.appendChild(o)}
 function render(){let needle=search.value.trim().toLowerCase(),selected=rows.filter(r=>
 (!fam.value||r.family===fam.value) && (!filter.value||filter.value==='cross'&&r.flags.includes('CROSS_TILESET')||filter.value==='multi'&&r.multi||filter.value==='no3d'&&r.bind==='NO_PUBLIC_3D_BINDING')&&
 (r.i+' '+r.n+' '+r.family+' '+r.group+' '+r.sheets).toLowerCase().includes(needle));
 count.textContent=selected.length+' / 357';cards.innerHTML=selected.map(r=>'<article><img loading="lazy" src="'+encodeURI(r.img)+'" alt="'+esc(r.n)+'"><h2>'+String(r.i).padStart(3,'0')+' '+esc(r.n)+'</h2><p><b>가구 스타일 ID:</b> <code>'+r.id+'</code></p><p><b>방향:</b> '+esc(r.f||'미기록')+' / 원본 타일 '+r.num+'개</p><p><b>타일셋:</b> '+esc(r.sheets)+'</p><p><b>3D 참고:</b> '+esc(r.bind)+'</p><p><b>검토:</b> '+esc(r.flags||'스타일만 정리됨, 실제 동일 디자인 인증 전')+'</p></article>').join('')}
 [search,fam,filter].forEach(x=>x.addEventListener('input',render));render();</script></body></html>'''
 (O/"INDEX.html").write_text(htmlview.replace("__DATA__",js(ui)),encoding="utf8")
 with zipfile.ZipFile(O/"ROSEWOOD_FURNITURE_IDENTITY_CATALOG.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in sorted(O.rglob("*")):
   if p.is_file() and p.name!="ROSEWOOD_FURNITURE_IDENTITY_CATALOG.zip":z.write(p,p.relative_to(O))
 with zipfile.ZipFile(O/"ROSEWOOD_FURNITURE_IDENTITY_CATALOG.zip") as z:
  assert z.testzip() is None
  assert len([n for n in z.namelist() if n.startswith("reference_previews/") and n.endswith(".png")])==357
  assert "INDEX.html" in z.namelist()
 print("IDENTITY_CATALOG_COMPLETED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
