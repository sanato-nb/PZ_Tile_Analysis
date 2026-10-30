#!/usr/bin/env python3
"""v251: source-hash-verified A-only contacts for all and ONLY held 188 single-use keys."""
from pathlib import Path
import csv,hashlib,zipfile,json,io,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
S=R/"review/v119_selected_A_new4633"
O=R/"review/v251_held188_single_location_Afirst_2026-10-30"
O.mkdir(parents=True,exist_ok=True)
read=lambda p:list(csv.DictReader(p.open("r",encoding="utf-8-sig",newline="")))
sha=lambda data:hashlib.sha256(data).hexdigest()
census=read(R/"review/v246_held439_real_alt_TMX_2026-10-30/HELD439_ALTERNATE_SITE_CENSUS.csv")
source=read(R/"review/v246_held439_real_alt_TMX_2026-10-30/ALL_HELD_REAL_TMX_OCCURRENCES.csv")
v245=read(R/"review/v245_held439_complete_A_png_sha_2026-10-30/HELD_439_ORIGINAL_A_RGBA_VERIFIED.csv")
old={x["source_key"]:x for x in v245}
m=json.loads((S/"MANIFEST.json").read_text(encoding="utf8"))
ledger_path=S/"REPRESENTATIVE_A_4633.csv"
assert sha(ledger_path.read_bytes())==m["selected_ledger_sha256"]
ledger=read(ledger_path)
scope=sorted([x for x in census if int(x["alternative_real_positions"])==0],key=lambda x:int(x["source_index"]))
assert len(scope)==188 and all(int(x["total_real_occurrences"])==1 for x in scope)
keyset={x["source_key"] for x in scope}
assert len(keyset)==188
actual={x["source_key"]:x for x in source if x["source_key"] in keyset}
assert len(actual)==188
archmeta={Path(x["path"]).name:x for x in m["png_archive_shards"]}
zipnames={ledger[int(x["source_index"])]["selected_shard"] for x in scope}
zips={}
for name in sorted(zipnames):
 p=S/name
 assert sha(p.read_bytes())==archmeta[p.name]["sha256"]
 zips[name]=zipfile.ZipFile(p)
try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",14)
except OSError:font=ImageFont.load_default()
W,H=490,380
result=[]
for page in range(math.ceil(len(scope)/16)):
 board=Image.new("RGB",(W*4,H*4),"#e7edf3");d=ImageDraw.Draw(board)
 for j,r in enumerate(scope[page*16:(page+1)*16]):
  idx=int(r["source_index"]);x=ledger[idx];key=r["source_key"]
  assert key==f'{x["tile_set_name"]}/{int(x["local_id"])}'
  assert key in old
  data=zips[x["selected_shard"]].read(x["selected_zip_entry"])
  assert sha(data)==x["selected_png_file_sha256"]
  with Image.open(io.BytesIO(data)) as img:A=img.convert("RGBA")
  assert sha(A.tobytes())==x["selected_rgba_pixel_sha256"]
  alpha=sum(A.getchannel("A").histogram()[1:]);assert alpha==int(x["selected_alpha_pixels"]) and alpha>0
  assert sha(A.tobytes())==old[key]["selected_A_RGBA_sha256"]
  bbox=A.getchannel("A").getbbox();assert bbox is not None
  px=j%4*W;py=j//4*H
  d.rectangle((px+3,py+3,px+W-4,py+H-4),fill="white",outline="#b2c0cf")
  d.text((px+12,py+11),f'#{idx} {key[:48]}',font=font,fill="#203547")
  checker=Image.new("RGB",(W-28,H-112),"#f1f5f9");z=ImageDraw.Draw(checker)
  for iy in range(0,checker.height,20):
   for ix in range(0,checker.width,20):
    if (ix//20+iy//20)%2==0:z.rectangle((ix,iy,ix+19,iy+19),fill="#dce4eb")
  # Tight bbox only for seeing small images; original A anchor/alpha untouched in ZIP and ledger
  cut=A.crop((max(bbox[0]-3,0),max(bbox[1]-3,0),min(A.width,bbox[2]+3),min(A.height,bbox[3]+3)))
  fac=min((checker.width-20)/cut.width,(checker.height-20)/cut.height,9)
  cut=cut.resize((max(1,round(cut.width*fac)),max(1,round(cut.height*fac))),Image.Resampling.NEAREST)
  checker.paste(cut,((checker.width-cut.width)//2,(checker.height-cut.height)//2),cut)
  board.paste(checker,(px+14,py+43))
  d.text((px+12,py+316),f'A alpha:{alpha}; actual TMX: {actual[key]["tmx"]}',font=font,fill="#52697d")
  d.text((px+12,py+339),f'L{actual[key]["level"]} layer{actual[key]["layer_index"]} @{actual[key]["x"]},{actual[key]["y"]} rawGID {actual[key]["raw_gid"]}',font=font,fill="#52697d")
  result.append(dict(source_index=idx,source_key=key,source_atlas=x["source_image_path"],
   source_atlas_historical_sha256=x["source_png_sha256"],
   original_A_crop_xyxy=x["selected_crop_xyxy"],original_A_canvas=f"{A.width}x{A.height}",
   A_alpha_bbox=str(bbox),A_nontransparent_alpha_pixels=alpha,
   A_png_SHA256=x["selected_png_file_sha256"],A_RGBA_SHA256=x["selected_rgba_pixel_sha256"],
   original_source_zip=x["selected_shard"],original_source_zip_entry=x["selected_zip_entry"],
   ZIP_SHA_verified=1,A_png_sha_verified=1,A_RGBA_sha_verified=1,A_nontransparent_verified=1,
   only_real_TMX=actual[key]["tmx"],only_real_TMX_sha=actual[key]["tmx_sha256"],
   only_real_layer_index=actual[key]["layer_index"],only_real_level=actual[key]["level"],
   only_real_x=actual[key]["x"],only_real_y=actual[key]["y"],only_real_raw_gid=actual[key]["raw_gid"],
   no_other_TMX_location=1,removed_due_missing_A_or_full_transparency=0,
   real_BC_newly_rendered=0,official_identity_certified=0))
 board.save(O/f"A_ONLY_SINGLE188_{page:02d}.png",optimize=True)
 print("A page",page,"passed",len(result),flush=True)
assert len(result)==188
with (O/"A_ORIGINAL_188_SHA_AND_ONLY_REAL_TMX.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
manifest=dict(version="v251",source="v246 no-alt unique keys and v119/v245 original A",
 total_eligible_single_location=188,missing_A=0,fully_transparent_A=0,source_A_PNG_verified=188,
 source_A_RGBA_verified=188,source_zip_sha_verified=len(zips),contact_pages=math.ceil(188/16),
 original_A_anchor_preserved_in_v119=True,original_atlas_sha_newly_recomputed=False,
 new_qualitative_individual_reviews_after_contact_generation=0,
 true_original_TMX_BC_newly_rendered=0,official_mapping_certification=0,identity_certification=0)
(O/"A_ONLY_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(manifest),flush=True)
