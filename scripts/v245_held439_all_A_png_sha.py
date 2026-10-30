#!/usr/bin/env python3
"""v245: verify all 439 held exact source A archived PNG crops, and export A-only review sheets.
Every prior A key stays held; no official mapping or semantic certification performed.
"""
from pathlib import Path
import csv,io,json,zipfile,hashlib,math
from collections import Counter
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"review/v119_selected_A_new4633"
OUT=ROOT/"review/v245_held439_complete_A_png_sha_2026-10-30"
OUT.mkdir(parents=True,exist_ok=True)
readcsv=lambda path:list(csv.DictReader(path.open("r",encoding="utf-8-sig",newline="")))
sha=lambda b:hashlib.sha256(b).hexdigest()
v119=json.loads((SOURCE/"MANIFEST.json").read_text("utf8"))
sourcefile=SOURCE/"REPRESENTATIVE_A_4633.csv"
assert sha(sourcefile.read_bytes())==v119["selected_ledger_sha256"]
ledger=readcsv(sourcefile)
held=readcsv(ROOT/"review/v238_integrated_master_2026-10-29/MASTER_HELD_439_SOURCE_VERIFIED.csv")
new28=readcsv(ROOT/"review/v244_held439_Afirst_visual_reopen_2026-10-30/A_FIRST_DIRECT_VISUAL_28_EXPERIMENT_QUEUE.csv")
seen28={x["source_key"] for x in new28}
assert len(held)==439 and len(seen28)==len(new28)==28 and len(ledger)==4633
assert len({x["source_key"] for x in held})==439
zip_meta={Path(x["path"]).name:x for x in v119["png_archive_shards"]}
needed={ledger[int(h["source_index"])]["selected_shard"] for h in held}
opened={}
for name in sorted(needed):
    p=SOURCE/name
    assert sha(p.read_bytes())==zip_meta[p.name]["sha256"],p
    opened[name]=zipfile.ZipFile(p)
assert len(opened)==10
font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
try: ft=ImageFont.truetype(font,12);small=ImageFont.truetype(font,11)
except OSError: ft=small=ImageFont.load_default()
C=8;ROWS=10;W=280;H=198
N=80
board=None;draw=None
audits=[]
def first_board():
    im=Image.new("RGB",(C*W,ROWS*H),(237,242,247));return im,ImageDraw.Draw(im)
for ordinal,h in enumerate(sorted(held,key=lambda x:int(x["source_index"]))):
    i=int(h["source_index"]);s=ledger[i];key=h["source_key"]
    assert f'{s["tile_set_name"]}/{int(s["local_id"])}'==key
    assert s["selected_shard"] in opened and s["selected_zip_entry"]
    blob=opened[s["selected_shard"]].read(s["selected_zip_entry"])
    assert sha(blob)==s["selected_png_file_sha256"],(key,"PNG SHA")
    with Image.open(io.BytesIO(blob)) as imp: A=imp.convert("RGBA")
    assert sha(A.tobytes())==s["selected_rgba_pixel_sha256"],(key,"RGBA SHA")
    alpha=A.getchannel("A")
    count=sum(alpha.histogram()[1:])
    assert count==int(s["selected_alpha_pixels"]) and count>0,(key,"alpha pixels")
    bb=alpha.getbbox()
    assert bb is not None
    if ordinal%N==0:board,draw=first_board()
    n=ordinal%N;x=(n%C)*W;y=(n//C)*H
    draw.rectangle((x+2,y+2,x+W-3,y+H-3),fill="#fff",outline="#aab9c6",width=1)
    draw.text((x+8,y+7),f'#{i:05d} {key[:33]}',font=ft,fill="#172c3a")
    chk=Image.new("RGB",(W-14,145),"#f7f9fb")
    cd=ImageDraw.Draw(chk)
    for px in range(0,chk.width,16):
      for py in range(0,chk.height,16):
        if (px//16+py//16)%2==0:cd.rectangle((px,py,px+15,py+15),fill="#e2e7eb")
    # diagnostic preview deliberately zooms alpha bbox; original tile canvas/anchor is retained separately in ledger.
    tight=A.crop((max(0,bb[0]-2),max(0,bb[1]-2),min(A.width,bb[2]+2),min(A.height,bb[3]+2)))
    tight.thumbnail((chk.width-20,chk.height-10),Image.Resampling.NEAREST)
    chk.paste(tight,((chk.width-tight.width)//2,(chk.height-tight.height)//2),tight)
    board.paste(chk,(x+7,y+30))
    text=f'alpha {count} / {"A visual28" if key in seen28 else "A review pending"}'
    draw.text((x+8,y+181),text,font=small,fill="#547487" if key not in seen28 else "#136b57")
    audits.append(dict(source_index=i,source_key=key,prior_A_visible_shape=h["A_visible_shape_from_held_reaudit"],
       original_source_png=s["source_image_path"],registered_full_source_png_sha256=s["source_png_sha256"],
       original_selected_A_crop=s["selected_crop_xyxy"],selected_A_size=s["selected_size"],alpha_bbox=str(list(bb)),
       nontransparent_alpha_pixel_count=count,
       archived_selected_A_PNG_sha256=s["selected_png_file_sha256"],
       selected_A_RGBA_sha256=s["selected_rgba_pixel_sha256"],
       reviewed_png_archive=s["selected_shard"],archived_png_entry=s["selected_zip_entry"],
       v245_archived_png_zip_sha_verified=1,v245_png_file_sha_verified=1,
       v245_png_RGBA_pixel_sha_verified=1,v245_alpha_pixel_count_verified=1,
       v244_independent_A_visual_review_done=int(key in seen28),
       v245_new_individual_identity_semantic_certification=0,
       official_mapping_verified=0,tilezed_verified=0,certified=0))
    if ordinal%N==N-1 or ordinal==len(held)-1:
        board.save(OUT/f"HELD_A_ONLY_{ordinal//N:02d}.png",optimize=True)
        print("saved",ordinal//N,flush=True)
columns=list(audits[0])
with (OUT/"HELD_439_ORIGINAL_A_RGBA_VERIFIED.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(audits)
assert len(audits)==439 and sum(x["v244_independent_A_visual_review_done"] for x in audits)==28
man={
"version":"v245","scope":"439 previously held source keys, exact selected original A source PNG pixel QA and contact sheets",
"all_held":439,"original_A_lossless_PNG_crops_verified":439,"original_A_RGBA_pixel_hashes_verified":439,
"source_ZIP_shard_sha256_verified":len(opened),"alpha_nontransparent_pixel_counts_verified":439,
"sheet_count":math.ceil(439/80),"v244_fresh_individual_A_visual_records":28,
"new_semantic_individual_reviews_from_this_v245_batch":0,
"raw_full_atlas_png_hashes_computed_in_v245":0,
"actual_original_TMX_B_C_new_renders":0,
"new_occlusion_layer_tests":0,
"current_status_change":0,
"new_mapping_certifications":0,"new_tilezed_certifications":0,"new_final_identifications":0,
"user_manual_exclusions_unmodified":True,"v240_current_active_9587_unmodified":True,
"v240_excluded_455_unmodified":True,
"original_source_atlas_PNG_and_TMX_unchanged":True,
"render_warning":"Alpha tight-bbox is used only for review-sheet readability; exact unmodified 128x256 RGBA cropped pixels and original anchors are preserved in existing v119 archive and hash ledger.",
"verified_ledger":"review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv",
"historical_held":"review/v238_integrated_master_2026-10-29/MASTER_HELD_439_SOURCE_VERIFIED.csv",
"metadata_csv":"review/v245_held439_complete_A_png_sha_2026-10-30/HELD_439_ORIGINAL_A_RGBA_VERIFIED.csv",
"sheets":"HELD_A_ONLY_00.png to HELD_A_ONLY_05.png"
}
(OUT/"MANIFEST.json").write_text(json.dumps(man,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({k:man[k] for k in ("all_held","original_A_RGBA_pixel_hashes_verified","source_ZIP_shard_sha256_verified","sheet_count")}),flush=True)
