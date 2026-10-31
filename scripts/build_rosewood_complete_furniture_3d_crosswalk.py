#!/usr/bin/env python3
"""Build PZ COMPLETE furniture sprite previews, and verify public Viewpoint 3D
binding data against Rosewood tile local IDs. All matches are candidate/grounded,
not automatic certification of geometry or a Minecraft block counterpart.
No external 3D meshes or textures are redistributed.
"""
import csv,io,json,re,sqlite3,urllib.request,math,hashlib,zipfile
from collections import Counter,defaultdict
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/"analysis/rosewood_furniture/2026-10-31"
OUT=WORK/"complete_furniture_visual_3d_v1"
DB=ROOT/"analysis/current/v259/PZ_v259_all_png_tile_definitions.sqlite"
TILES=WORK/"ALL_FURNITURE_TILE_IDS.csv"
NAMES=WORK/"furniture_dedup_v1/FURNITURE_MODELS_DEDUP_NAME_GROUP.csv"
MCMAP=WORK/"mod_matching_2026-10-31/ROSEWOOD_357_FURNITURE_MOD_CANDIDATES.csv"
PUBLIC_COMMIT="318753b6811176cc4b303f4c38d59eb5fda4d834"
PUBLIC_PACK="https://raw.githubusercontent.com/Hirouou/project-viewpoint/"+PUBLIC_COMMIT+"/Scripts/Interiors/mod/42/media/modelpacks/furniturefix/pack.properties"
PUBLIC_ASSET_ROOT="https://github.com/Hirouou/project-viewpoint/blob/"+PUBLIC_COMMIT+"/Scripts/Interiors/mod/42/media/modelpacks/furniturefix/"
def loadcsv(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def outputcsv(p,cols,rows):
    with p.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
def safe(x):
    return re.sub(r"[^a-zA-Z0-9_-]","_",x)[:85]
def font(size=20):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(f).is_file():return ImageFont.truetype(f,size)
    return ImageFont.load_default()
def source_key(r):return r["tile_set_name"],int(r["local_id"])
def parse_pos(s):
    x=re.fullmatch(r"\s*(-?\d+),\s*(-?\d+)\s*",s or "")
    return tuple(map(int,x.groups())) if x else None
def make_preview(parts,orig,atlas,db,cache):
    """Crop actual source PNG pixels; paste parts using an illustrative isometric
    2x grid transform. A render preview is NOT verified sprite-part geometry."""
    # original sprite canvas 128x256 for 2x; x→(+64,+32), y→(-64,+32)
    patches=[];provenance=[];missing=0
    for r in parts:
        key=source_key(r);located=atlas.get(key)
        if not located:
            missing+=1;continue
        p=located[0];filepath=ROOT/p["png_path"]
        if not filepath.exists():
            missing+=1;continue
        if p["png_path"] not in cache:
            cache[p["png_path"]]=Image.open(filepath).convert("RGBA")
        im=cache[p["png_path"]]
        tw,th=p["cell_width"],p["cell_height"]
        x,y=int(p["column_index"]),int(p["row_index"])
        patch=im.crop((x*tw,y*th,(x+1)*tw,(y+1)*th))
        pos=parse_pos(r["SpriteGridPos"]) or (0,0)
        patches.append((patch,pos,key,p))
        provenance.append({"tileset":key[0],"local_id":key[1],"png_path":p["png_path"],
                    "sprite_grid":list(pos),"alpha_visible":p["has_visible_pixels"]})
    if not patches:return None,provenance,missing
    # adapt to actual source 2x images; 1x images use 32/16 increments.
    scale=patches[0][0].width/128
    step_x=int(round(64*scale));step_y=int(round(32*scale))
    pos_x=[step_x*(xy[0]-xy[1]) for im,xy,k,p in patches]
    pos_y=[step_y*(xy[0]+xy[1]) for im,xy,k,p in patches]
    mx=min(pos_x);my=min(pos_y)
    maxx=max(x+im.width for x,(im,xy,k,p) in zip(pos_x,patches))
    maxy=max(y+im.height for y,(im,xy,k,p) in zip(pos_y,patches))
    cw=maxx-mx;ch=maxy-my
    if cw>1900 or ch>1900:raise ValueError("bad preview dimensions")
    canvas=Image.new("RGBA",(cw+36,ch+36),(0,0,0,0))
    # behind-to-front painter order; isometric sprite order convention provisional.
    order=sorted(range(len(patches)),key=lambda i:(pos_y[i],pos_x[i]))
    for i in order:
        im,xy,k,p=patches[i]
        canvas.alpha_composite(im,(pos_x[i]-mx+18,pos_y[i]-my+18))
    bbox=canvas.getbbox()
    if bbox:canvas=canvas.crop((max(0,bbox[0]-15),max(0,bbox[1]-15),
                                 min(canvas.width,bbox[2]+15),min(canvas.height,bbox[3]+15)))
    return canvas,provenance,missing
def make_card(preview,title,subtitle,status):
    canvas=Image.new("RGB",(550,460),(236,240,243))
    dr=ImageDraw.Draw(canvas);f1=font(23);f2=font(15)
    dr.text((18,14),title[:56],font=f1,fill=(18,26,33))
    dr.text((18,46),subtitle[:86],font=f2,fill=(60,74,89))
    dr.rectangle([14,80,535,405],fill=(224,231,234),outline=(180,188,195),width=1)
    if preview is not None:
        sz=preview.size
        preview.thumbnail((495,315),Image.Resampling.LANCZOS)
        if preview.size[0] and preview.size[1]:
            canvas.paste(preview,((550-preview.width)//2,81+(322-preview.height)//2),mask=preview.getchannel("A"))
    else:dr.text((70,218),"NO VERIFIED SOURCE PNG",font=font(22),fill=(110,75,68))
    dr.text((18,423),status,font=f2,fill=(110,47,35) if "PROVISIONAL" in status else (27,82,51))
    return canvas
def normalize(n):return re.sub(r"[^a-z0-9]+","_",n.strip().lower()).strip("_")
def choose_variant(rows):
    """Pick representative group by source tileset+Facing, never mix orientations."""
    sets=defaultdict(list)
    for r in rows:sets[r["tile_set_name"],r["Facing"]].append(r)
    scored=[]
    for (name,facing),items in sets.items():
        byposition=defaultdict(list)
        for r in items:byposition[parse_pos(r["SpriteGridPos"])].append(r)
        nonnull=[p for p in byposition if p is not None]
        # pick highest observed count at each position
        unique=[sorted(rs,key=lambda x:-int(x["core_sprite_placements"]))[0] for pos,rs in byposition.items() if pos is not None]
        if not nonnull:
            unique=sorted(items,key=lambda x:-int(x["core_sprite_placements"]))[:1]
            is_multi=False;valid=True;area=1
        else:
            xs=[x for x,y in nonnull];ys=[y for x,y in nonnull]
            area=(max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)
            valid=area==len(nonnull) and len(nonnull)==len(unique)
            is_multi=len(nonnull)>1
        draw=unique if is_multi else unique[:1]
        vis_score=sum(int(r["core_sprite_placements"]) for r in draw)
        score=(1 if valid else 0,1 if is_multi else 0,len(draw),vis_score,
            1 if facing=="S" else 0,1 if facing=="E" else 0)
        scored.append((score,name,facing,draw,area,valid))
    if not scored:return None
    return sorted(scored,key=lambda x:x[0],reverse=True)[0]
def main():
    if OUT.exists() and any(OUT.iterdir()):raise FileExistsError("no overwrite "+str(OUT))
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"previews").mkdir()
    models=loadcsv(NAMES);tiles=loadcsv(TILES);mc=loadcsv(MCMAP)
    assert len(models)==len(mc)==357 and len(tiles)==4248
    mcby={(r["CustomName"],r["GroupName"]):r for r in mc}
    # Pin external Viewpoint definitions, read every model & bind line.
    request=urllib.request.Request(PUBLIC_PACK,headers={"User-Agent":"PZ-Rosewood-Source-Audit/1.0"})
    raw=urllib.request.urlopen(request,timeout=45).read().decode("utf-8-sig")
    bindings={};assets={}
    for line in raw.splitlines():
        if not line or "=" not in line or line.startswith("#"):continue
        k,v=line.split("=",1)
        if k.startswith("bind."):bindings[k[5:]]=v.split(",")[0]
        elif k.startswith("model."):assets[k[6:]]=v
    if len(bindings)<500 or len(assets)<200:
        raise RuntimeError(f"Unexpected 3D source manifest {len(bindings)} bindings {len(assets)} assets")
    external_digest=hashlib.sha256(raw.encode()).hexdigest()
    con=sqlite3.connect("file:"+str(DB.resolve())+"?mode=ro",uri=True);con.row_factory=sqlite3.Row
    atlas=defaultdict(list)
    for a in con.execute("""SELECT c.tileset,c.local_id,c.png_path,c.column_index,c.row_index,c.has_visible_pixels,
                              a.cell_width,a.cell_height
                              FROM image_cells c JOIN image_atlases a ON c.png_path=a.png_path
                              WHERE c.link_status='SOURCE_SLOT_LINKED_GRID_VERIFIED'"""):
        d=dict(a);atlas[a["tileset"],a["local_id"]].append(d)
    con.close()
    # Prefer verified highest-resolution source PNGs.
    for key in atlas:
        atlas[key].sort(key=lambda d:(0 if d["png_path"].startswith("Tiles/2x/") else 1,
                       -d["cell_width"],d["png_path"]))
    byname=defaultdict(list)
    for r in tiles:byname[(r["CustomName"],r["GroupName"])].append(r)
    cache={};audits=[];all_model_bindings=Counter();missing_png=0;full_grid=0;partial_grid=0
    for i,model in enumerate(models,1):
        k=(model["CustomName"],model["GroupName"])
        src=byname.get(k,[])
        preferred=set(model["source_tilesets"].split("|"))
        src=[r for r in src if r["tile_set_name"] in preferred]
        pick=choose_variant(src)
        if pick:
            _,tileset,facing,parts,footarea,source_grid_complete=pick
            multi=len(parts)>1
            full_grid+=int(multi and source_grid_complete)
            partial_grid+=int(multi and not source_grid_complete)
            img,provenance,missing=make_preview(parts,model,atlas,None,cache)
            missing_png+=missing
        else:
            tileset="";facing="";parts=[];footarea=0;source_grid_complete=False
            img=None;provenance=[];missing=1;missing_png+=1
        # Whole model coverage = every source tile ID in every orientation, not just selected sample
        bindings_by_key={}
        for r in src:
            sk=r["tile_set_name"]+"_"+r["local_id"]
            binding=bindings.get(sk)
            if binding and binding not in assets:binding=None
            bindings_by_key[sk]=binding
            if binding:all_model_bindings[binding]+=1
        nbind=sum(v is not None for v in bindings_by_key.values());nsource=len(bindings_by_key)
        pb=[(r["tile_set_name"]+"_"+r["local_id"],bindings_by_key.get(r["tile_set_name"]+"_"+r["local_id"])) for r in parts]
        preview_bound=sum(v is not None for key,v in pb)
        coverage=("ALL_VARIANT_PARTS_3D_BOUND" if nsource>0 and nbind==nsource else
                  "SOME_VARIANT_PARTS_3D_BOUND" if nbind else "NO_PUBLIC_3D_BINDING")
        pre_status=("ISOMETRIC_ASSEMBLY_PROVISIONAL" if len(parts)>1 else
                    "SINGLE_TILE_REFERENCE" if img is not None else "PNG_MISSING")
        title=model["CustomName"]+(" / "+model["GroupName"] if model["GroupName"] else "")
        chosen=mcby.get(k,{})
        asset_names=sorted({v for v in bindings_by_key.values() if v})
        basename=f"{i:03d}_{safe(model['CustomName'])}_{safe(model['GroupName'])}.png"
        card=make_card(img,title,"PZ "+tileset+" | facing="+facing+" | parts="+str(len(parts)),pre_status)
        card.save(OUT/"previews"/basename,optimize=True)
        audit=dict(index=i,CustomName=model["CustomName"],GroupName=model["GroupName"],
              original_model_name_key_count=int(model["model_source_keys"]),
              core_placed_object_candidates=int(model["furniture_candidate_placements"]),
              representative_tileset=tileset,representative_facing=facing,
              representative_num_parts=len(parts),representative_source_grid_area=footarea,
              rectangular_source_template=source_grid_complete,
              isometric_preview_status=pre_status,
              preview_path="previews/"+basename,
              representative_source_tile_ids="|".join(r["tile_set_name"]+"/"+r["local_id"] for r in parts),
              representative_sprite_grid_positions="|".join(r["SpriteGridPos"] for r in parts),
              pixels_missing=missing,
              total_source_tile_local_ids=nsource,source_ids_with_public_3d_bindings=nbind,
              representative_parts_with_3d_bindings=preview_bound,
              reference_3d_binding_coverage=coverage,
              reference_3d_model_ids="|".join(asset_names),
              reference_3d_model_file_urls="|".join(PUBLIC_ASSET_ROOT+assets[v] for v in asset_names),
              minecraft_primary_mod=chosen.get("primary",""),
              minecraft_alternates=chosen.get("alternates",""),
              minecraft_block_id="NOT_VERIFIED",
              minecraft_exact_visual_match="NOT_VERIFIED",
              evidence_provenance="User-provided private Tiles PNG + B42 original .tiles metadata; public authored Viewpoint 0.1.19 bindings",
              note="3D source models may be incomplete; do not redistribute model assets; source versions differ; preview shape is provisional")
        audits.append(audit)
        if i%80==0:print("completed full-form furniture preview",i,"of",len(models),flush=True)
    for im in cache.values():im.close()
    outputcsv(OUT/"ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv",list(audits[0]),audits)
    # Separate direct sprite->3D evidence table for ALL full source variants.
    mapping=[]
    for r in tiles:
        n=r["CustomName"];g=r["GroupName"]
        if (n,g) not in {(a["CustomName"],a["GroupName"]) for a in models}:continue
        sk=r["tile_set_name"]+"_"+r["local_id"]
        bind=bindings.get(sk)
        if bind and bind not in assets:bind=None
        mapping.append(dict(tileset=r["tile_set_name"],local_id=r["local_id"],
           CustomName=n,GroupName=g,Facing=r["Facing"],SpriteGridPos=r["SpriteGridPos"],
           core_sprite_parts=r["core_sprite_placements"],
           original_png_available=bool(atlas.get((r["tile_set_name"],int(r["local_id"])))),
           viewpoint_3d_model_id=bind or "",viewpoint_obj_path=assets.get(bind,"") if bind else "",
           binding_state="EXACT_SPRITE_ID_BINDING_FOUND" if bind else "NO_BINDING_IN_VIEWPOINT_SOURCE"))
    outputcsv(OUT/"ALL_SOURCE_SPRITE_TO_VIEWPOINT_3D_BINDINGS.csv",list(mapping[0]),mapping)
    # Each page is visual comparison of COMPLETE source furniture, not independent pieces.
    montage_dir=OUT/"contact_sheets";montage_dir.mkdir()
    cols=3;perpage=12
    for start in range(0,len(audits),perpage):
        page=Image.new("RGB",(550*cols,460*4),(246,248,249))
        for idx,a in enumerate(audits[start:start+perpage]):
            card=Image.open(OUT/a["preview_path"]).convert("RGB")
            page.paste(card,((idx%cols)*550,(idx//cols)*460));card.close()
        page.save(montage_dir/f"CONTACT_{start//perpage+1:03d}.jpg",quality=84,optimize=True)
    counts=Counter(a["reference_3d_binding_coverage"] for a in audits)
    from_pz=Counter(a["isometric_preview_status"] for a in audits)
    report={
        "version":"Rosewood_CompleteFurniture_3D_Audit_v1",
        "scope":"357 original CustomName/GroupName style combinations, center Rosewood; distinct models not certified",
        "source_3d_project":"Hirouou/project-viewpoint public repo version 0.1.19",
        "source_3d_commit":PUBLIC_COMMIT,"source_3d_pack_properties_sha256":external_digest,
        "source_3d_pack_models_declared":len(assets),"source_3d_pack_sprite_bindings":len(bindings),
        "total_styles":len(audits),"source_sprite_rows_audited":len(mapping),
        "complete_multi_tile_source_grid_preview_styles":full_grid,
        "partial_multi_tile_source_grid_preview_styles":partial_grid,
        "missing_source_png_cell_references":missing_png,
        "3d_binding_status_style_counts":dict(counts),
        "preview_status_style_counts":dict(from_pz),
        "mc_block_exact_confirmed":0,
        "image_and_model_notice":"Contact sheets and previews show PZ sprite compositing provisional; no exact modeled 3D renders incorporated into this report; GitHub linked OBJ remains property of its creators",
        "source_version_warning":"user's tiledef B42 20.3 vs public Viewpoint 3D 0.1.19 B42 21+",
        "3d_coverage_warning":"Exact source tile ID bind found is evidence of author mapping, not guarantee same physical grouped model and not Minecraft compatibility"
    }
    (OUT/"MANIFEST.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    doc=[
      "# 로즈우드 357 스타일: 원본 가구 완성형 PNG + 실제 3D 모드 모델 연결",
      "",
      "## 출처와 검증 범위",
      "- 원본: 로즈우드 추출 357개 CustomName/GroupName 조합, v259 원본 PNG Tiles/2x, 원본 .tiles와 SpriteGridPos",
      "- 3D: 공개 프로젝트 Hiro.uou/Viewpoint 0.1.19의 pack.properties, 3D 모델 선언 및 bind.타일셋_LocalID 정확 일치",
      "- 비교할 Minecraft 모드는 별도 357개 후보표 연결; **정확한 블록 ID는 아직 0개 확정**",
      "- 공개 3D OBJ는 권리 문제 때문에 이 결과물에 재배포하지 않고 모델 파일 URL만 남김",
      "",
      "## 실제 생성된 근거",
      f"- 가구 이름·스타일 357개 전체의 픽셀 기반 개별 참고 이미지: {len(audits)}장",
      f"- 3×4 전체 접촉시트: {math.ceil(len(audits)/perpage)}장",
      f"- 원본 SpriteGridPos를 이용한 복합 가구 임시 조립 미리보기: {full_grid}개 스타일",
      f"- 공개 Viewpoint 원본 3D 모델 선언 {len(assets)}개, 실제 스프라이트 바인딩 {len(bindings)}행",
      *(f"- 3D 소스 대응 {k}: {v}개 스타일" for k,v in sorted(counts.items())),
      f"- 3D 모델과 대응 검토에 연결한 개별 원본 타일 ID 레코드 {len(mapping)}행",
      "",
      "## 다칸 가구 안전 원칙",
      "- 2~4칸 가구는 SpriteGridPos의 조각을 한 접촉 이미지 안에 배치해서 **완성형을 참고**하고, 단일 조각을 가구 하나로 보지 않음.",
      "- 타일의 렌더링 순서와 isometric 배치는 가정이며 TMX 사용된 부품 세트와 실제 전체 가구 픽셀을 최종 인증하지 않음.",
      "- 이미지가 동일한 가구의 다방향 변형을 하나의 모델로 볼지 여부는 수동 확인이 필요함.",
      "- 원본 스프라이트가 실재해도 공개 Viewpoint 3D 모드가 해당 타일 ID에 bind를 제공하지 않으면 '미연결'로 기록.",
      "- 같은 이름+그룹으로 서로 다른 원본 타일셋이 섞일 때 대표 한 조합만 시각 예시로 사용; 원본 타일 전체와 bind는 CSV에 보존.",
      "- B42.20.3 자료와 Viewpoint용 B42.21+ 자료의 버전 차이로 스프라이트 ID가 달라질 수 있음.",
      "",
      "## 파일",
      "- ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv: 357개 스타일의 대표 완성형 참고 이미지·부품 목록·Viewpoint 3D asset 실제 bind·마크 모드 후보.",
      "- ALL_SOURCE_SPRITE_TO_VIEWPOINT_3D_BINDINGS.csv: 원본 Local ID별 공개 3D bind 확인/미확인.",
      "- contact_sheets/: 30장, 357개 스타일 완성형 시트.",
      "- previews/: 357장 개별 가구 원본 PNG 기반 조립 예시.",
      "- COMPLETE_FURNITURE_CONTACT_SHEETS.zip: 전체 접촉시트와 CSV, 보고서.",
      "- **아직 아님:** 공개 3D 모델 OBJ의 실제 색상·비례 렌더 확인; 실제 Minecraft 모드 블록 3D 모델의 화면 비교/레지스트리 ID 확정."
    ]
    (OUT/"README_KO.md").write_text("\n".join(doc)+"\n",encoding="utf-8")
    with zipfile.ZipFile(OUT/"COMPLETE_FURNITURE_CONTACT_SHEETS.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
        for p in sorted(montage_dir.glob("*.jpg")):z.write(p,"contact_sheets/"+p.name)
        for f in ["MANIFEST.json","README_KO.md","ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv",
            "ALL_SOURCE_SPRITE_TO_VIEWPOINT_3D_BINDINGS.csv"]:
            z.write(OUT/f,f)
    with zipfile.ZipFile(OUT/"COMPLETE_FURNITURE_ALL_PREVIEWS.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
        for p in sorted((OUT/"previews").glob("*.png")):z.write(p,"previews/"+p.name)
    print("RESULT",json.dumps(report,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
