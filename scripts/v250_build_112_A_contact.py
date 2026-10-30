#!/usr/bin/env python3
"""v250: exact archived source A RGBA and genuine alternate B evidence for 112 held keys."""
import csv,io,hashlib,json,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
S=R/"review/v119_selected_A_new4633"
O=R/"review/v250_held112_Afirst_individual_2026-10-30"
read=lambda p:list(csv.DictReader(p.open(encoding="utf-8-sig",newline="")))
sha=lambda x:hashlib.sha256(x).hexdigest()
m=json.loads((S/"MANIFEST.json").read_text("utf8"))
ledgerfile=S/"REPRESENTATIVE_A_4633.csv"
assert sha(ledgerfile.read_bytes())==m["selected_ledger_sha256"]
ledger=read(ledgerfile);pending=read(O/"EXACT_PENDING_112_KEY_CROSSWALK.csv")
assert len(ledger)==4633 and len(pending)==112
meta={Path(x["path"]).name:x["sha256"] for x in m["png_archive_shards"]}
needed={ledger[int(x["source_index"])]["selected_shard"] for x in pending}
zs={}
for name in needed:
 f=S/name
 assert sha(f.read_bytes())==meta[f.name]
 zs[name]=zipfile.ZipFile(f)
try:ft=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",14)
except OSError:ft=ImageFont.load_default()
W,H=510,380
output=[]
for page in range(7):
 canvas=Image.new("RGB",(W*4,H*4),"#eff3f7");d=ImageDraw.Draw(canvas)
 for j,x in enumerate(pending[page*16:(page+1)*16]):
  idx=int(x["source_index"]);info=ledger[idx]
  assert x["source_key"]==info["tile_set_name"]+"/"+str(int(info["local_id"]))
  raw=zs[info["selected_shard"]].read(info["selected_zip_entry"])
  assert sha(raw)==info["selected_png_file_sha256"]
  with Image.open(io.BytesIO(raw)) as img:A=img.convert("RGBA")
  assert sha(A.tobytes())==info["selected_rgba_pixel_sha256"]
  alpha=sum(A.getchannel("A").histogram()[1:]);assert alpha==int(info["selected_alpha_pixels"])
  bbox=A.getchannel("A").getbbox();assert bbox
  with Image.open(R/x["exact_source_qualified_BC_panel"]) as img:B=img.convert("RGB").crop((440,70,880,570))
  px=(j%4)*W;py=(j//4)*H
  d.rectangle((px+2,py+2,px+W-3,py+H-3),fill="white",outline="#b5c1ca")
  d.text((px+9,py+9),f'{idx}: {x["source_key"][:43]}',font=ft,fill="#193142")
  d.text((px+12,py+34),"SOURCE A (alpha)",font=ft,fill="#536b7a")
  d.text((px+250,py+34),"ACTUAL TMX B",font=ft,fill="#536b7a")
  chk=Image.new("RGB",(229,260),"#f7f9fc");cd=ImageDraw.Draw(chk)
  for yy in range(0,260,20):
   for xx in range(0,229,20):
    if ((xx+yy)//20)%2==0:cd.rectangle((xx,yy,xx+19,yy+19),fill="#dae2e9")
  cut=A.crop((max(0,bbox[0]-4),max(0,bbox[1]-4),min(A.width,bbox[2]+4),min(A.height,bbox[3]+4)))
  scale=min(217/cut.width,245/cut.height,8)
  cut=cut.resize((max(1,int(cut.width*scale)),max(1,int(cut.height*scale))),Image.Resampling.NEAREST)
  chk.paste(cut,((229-cut.width)//2,(260-cut.height)//2),cut)
  canvas.paste(chk,(px+8,py+57))
  B.thumbnail((257,260),Image.Resampling.NEAREST)
  canvas.paste(B,(px+244+(257-B.width)//2,py+57+(260-B.height)//2))
  d.text((px+10,py+330),f'A alpha {alpha}, bbox{bbox}',font=ft,fill="#3e5e70")
  d.text((px+10,py+350),f'B-C: {x["original_B_C_change_pixels"]}, layer: {x["through_target_layer_change_pixels"]}',font=ft,fill="#0a765d")
  output.append(dict(source_index=idx,source_key=x["source_key"],
   original_atlas_path=info["source_image_path"],registered_atlas_sha=info["source_png_sha256"],
   original_crop=info["selected_crop_xyxy"],A_RGBA_sha256=info["selected_rgba_pixel_sha256"],
   original_A_png_sha256=info["selected_png_file_sha256"],A_alpha_pixels=alpha,
   original_A_zip=info["selected_shard"],A_source_archive_SHA_rechecked=1,
   original_A_RGBA_SHA_rechecked=1,original_A_PNG_SHA_rechecked=1,
   original_BC_v248=x["exact_source_qualified_BC_panel"],new_original_BC_rendered=0,final_identity_certified=0))
 canvas.save(O/f"A_ORIGINAL_VS_ALT_B_{page:02d}.png",optimize=True)
 print("SHEET",page,flush=True)
with (O/"A_ORIGINAL_112_SHA_VERIFIED.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
assert len(output)==112
print(json.dumps(dict(keys=len(output),source_zip_shards=len(zs),original_A_pixel_shas=len(output),sheets=7,certified=0)))
