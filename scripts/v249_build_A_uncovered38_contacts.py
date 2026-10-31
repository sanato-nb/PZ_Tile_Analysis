#!/usr/bin/env python3
"""Build two reviewer-friendly evidence sheets from already verified v249 full panels."""
from pathlib import Path
import csv,io,math
from PIL import Image,ImageDraw,ImageChops,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review/v249_held251_occlusion38_diagnostics_2026-10-30"
rows=list(csv.DictReader((OUT/"38_TARGET_STEPWISE_OCCLUSION_DIAGNOSTICS.csv").open(encoding="utf-8-sig",newline="")))
assert len(rows)==38
try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",16)
except OSError:font=ImageFont.load_default()
CW,CH=480,335
for page in range(2):
 sub=rows[page*20:(page+1)*20]
 board=Image.new("RGB",(CW*4,CH*5),(232,237,242));d=ImageDraw.Draw(board)
 for i,r in enumerate(sub):
  x=(i%4)*CW;y=(i//4)*CH
  d.rectangle((x+3,y+3,x+CW-3,y+CH-3),fill="white",outline="#adbdc9",width=2)
  d.text((x+12,y+12),f'#{r["source_index"]}  {r["source_key"][:42]}',fill="#203c4a",font=font)
  a=Image.open(OUT/r["diagnostic_contact"]).convert("RGB")
  raw=a.crop((0,115,450,650))
  blank=Image.new("RGB",raw.size,(248,250,252))
  delta=ImageChops.difference(raw,blank).convert("L")
  mask=delta.point(lambda v:255 if v>8 else 0)
  bb=mask.getbbox()
  if bb:
   orig=raw.crop((max(0,bb[0]-6),max(0,bb[1]-6),min(raw.width,bb[2]+6),min(raw.height,bb[3]+6)))
  else:orig=raw
  orig.thumbnail((215,240),Image.Resampling.NEAREST)
  scene=a.crop((1350,205,1800,535))
  scene.thumbnail((230,240),Image.Resampling.NEAREST)
  d.text((x+13,y+43),"ORIGINAL A",font=font,fill="#536877")
  d.text((x+247,y+43),"TARGET LAST (DIAGNOSTIC)",font=font,fill="#b05a25")
  board.paste(orig,(x+13+(220-orig.width)//2,y+70+(240-orig.height)//2))
  board.paste(scene,(x+245+(225-scene.width)//2,y+70+(240-scene.height)//2))
  d.text((x+12,y+316),f'same layer {r["later_same_layer_culprits"]}  later layers {r["later_different_layer_culprits"]}',font=font,fill="#496173")
 name=f"ALL38_ORIGINAL_A_VS_UNCOVERED_{page:02d}.png"
 board.save(OUT/name,optimize=True)
 print(name,flush=True)
