#!/usr/bin/env python3
"""v244: verify original exact PNG A pixels of 28 held keys, preserving original 4,633 ledger.
This is a provenance QA and crop export, not autonomous identity certification.
"""
from pathlib import Path
from collections import Counter
import hashlib,io,zipfile,csv,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
O=R/"review/v244_held439_Afirst_visual_reopen_2026-10-30"
L=R/"review/v119_selected_A_new4633"
out=O/"A_ORIGINAL_RGBA_28"
out.mkdir(parents=True,exist_ok=True)
read=lambda p:list(csv.DictReader(p.open(encoding="utf-8-sig",newline="")))
sha=lambda b:hashlib.sha256(b).hexdigest()
source=read(L/"REPRESENTATIVE_A_4633.csv")
review=read(O/"A_FIRST_DIRECT_VISUAL_28_EXPERIMENT_QUEUE.csv")
assert len(source)==4633 and len(review)==28
idxs={int(x["source_index"]):x for x in review}
assert len(idxs)==28
m=json.loads((L/"MANIFEST.json").read_text("utf8"))
source_file=L/"REPRESENTATIVE_A_4633.csv"
assert sha(source_file.read_bytes())==m["selected_ledger_sha256"]
shards={x["path"].split("/")[-1]:x for x in m["png_archive_shards"]}
parts=sorted({source[i]["selected_shard"] for i in idxs})
print("Shards needed:",parts,flush=True)
zips={}
for p in parts:
    archive=L/p
    meta=shards[archive.name]
    assert sha(archive.read_bytes())==meta["sha256"], archive
    zips[p]=zipfile.ZipFile(archive)
card_w,card_h=330,250
board=Image.new("RGB",(4*card_w,7*card_h),"#f0f3f6")
d=ImageDraw.Draw(board)
try:
    font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",13)
except OSError:
    font=ImageFont.load_default()
evidence=[]
for n,(i,reviewrow) in enumerate(sorted(idxs.items())):
    x=source[i];path=x["selected_shard"];entry=x["selected_zip_entry"]
    assert int(x["local_id"])==int(reviewrow["source_key"].split("/")[-1])
    assert x["tile_set_name"]==reviewrow["source_key"].split("/")[0]
    data=zips[path].read(entry)
    assert sha(data)==x["selected_png_file_sha256"],(i,"png bytes sha")
    with Image.open(io.BytesIO(data)) as raw: img=raw.convert("RGBA")
    assert sha(img.tobytes())==x["selected_rgba_pixel_sha256"],(i,"A RGBA sha")
    a=sum(img.getchannel("A").histogram()[1:])
    assert a==int(x["selected_alpha_pixels"]),(i,a)
    fname=f"A_{i:05d}_{x['tile_set_name']}_{int(x['local_id']):04d}.png"
    assert "/" not in fname
    (out/fname).write_bytes(data)
    xx=(n%4)*card_w; yy=(n//4)*card_h
    d.rectangle((xx+4,yy+4,xx+card_w-4,yy+card_h-4),fill="#fff",outline="#b8c2cb",width=2)
    d.text((xx+13,yy+10),f"#{i}  {x['tile_set_name']}/{x['local_id']}",font=font,fill="#122434")
    region=Image.new("RGB",(card_w-24,188),"#f3f6f9");rg=ImageDraw.Draw(region)
    for px in range(0,region.width,16):
        for py in range(0,region.height,16):
            if (px//16+py//16)%2==0:rg.rectangle((px,py,px+15,py+15),fill="#dce3e9")
    tile=img.copy();tile.thumbnail((region.width-20,region.height-10),Image.Resampling.NEAREST)
    region.paste(tile,((region.width-tile.width)//2,(region.height-tile.height)//2),tile)
    board.paste(region,(xx+12,yy+39))
    d.text((xx+13,yy+231),f"RGBA {img.width}x{img.height} / alpha {a} / provisional",font=font,fill="#455869")
    evidence.append(dict(source_index=i,source_key=reviewrow["source_key"],
         source_A_png=x["source_image_path"],
         selected_A_from_zip=path+"/"+entry,
         selected_A_rgba_sha256=x["selected_rgba_pixel_sha256"],
         selected_A_png_sha256=x["selected_png_file_sha256"],
         selected_A_alpha_pixels=a,selected_A_size=f"{img.width}x{img.height}",
         selected_A_crop=x["selected_crop_xyxy"],
         original_PNG_sha256_v119_registered=x["source_png_sha256"],
         exported_A_png=str((out/fname).relative_to(R)),
         zip_sha_verified_v244=1,PNG_sha_verified_v244=1,
         RGBA_sha_verified_v244=1,alpha_count_verified_v244=1,
         original_atlas_png_sha_newly_computed_v244=0,
         official_id_certified=0))
board.save(O/"A_ORIGINAL_RGBA_28_CONTACT.png",optimize=True)
with (O/"ORIGINAL_A_RGBA_SHA_VERIFIED_28.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(evidence[0]));w.writeheader();w.writerows(evidence)
print(json.dumps(dict(rows=len(evidence),newly_verified_RGBA=len(evidence),selected_A_archives_sha=len(zips),real_individual_RGBA_exported=len(evidence),
  contact_board=str(O/"A_ORIGINAL_RGBA_28_CONTACT.png"),
  original_PNG_archive_rehashed=False, mapping_verified=0, certified=0),ensure_ascii=False),flush=True)
