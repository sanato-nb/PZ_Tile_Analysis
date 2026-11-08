#!/usr/bin/env python3
"""Generate visual proof sheets from PZ original 2x tile atlases used in 31_46."""
import argparse
from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
SHEETS={
 "blends_natural_01":[16,21,22,23,24,27,28,31,32,37,38,39,48,53,54,55,64,69,70,71,80,85,86,87,89,90,91],
 "vegetation_farm_01":[0,1,2,3,4,5,6,7,8,9,16,17,18,19,24,25,26,27,32,33,34,35,36,37,38,39],
 "blends_street_01":[8,9,10,16,21,32,37,48,53,54,55,64,69,70,71,80,85,86,87],
 "blends_grassoverlays_01":[0,1,2,3,4,5,16,17,18,19,24,25,26,27,28,29,32,33,34,35,40,41,42,43,48,49,56,57,64,65],
 "vegetation_trees_01":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
 "vegetation_foliage_01":[8,9,10,11,12,13,14],
}
def main():
 p=argparse.ArgumentParser();p.add_argument("--tiles",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
 args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 for name,ids in SHEETS.items():
  file=args.tiles/(name+".png")
  if not file.exists():file=args.tiles.parent/(name+".png")
  if not file.exists():
   print("SKIP missing reference atlas:",name);continue
  im=Image.open(file).convert("RGBA")
  tw=im.width//8
  # Original 2x atlas has 8 sprite columns and twofold image resolution.
  th=tw*2
  print(name,im.size,"sprite",tw,th)
  cw,ch=180,186;columns=6;rows=(len(ids)+columns-1)//columns
  sheet=Image.new("RGB",(columns*cw,rows*ch),(240,242,244));draw=ImageDraw.Draw(sheet)
  for i,index in enumerate(ids):
   x,y=i%columns*cw,i//columns*ch
   if (index//8+1)*th>im.height:continue
   sprite=im.crop(((index%8)*tw,(index//8)*th,(index%8+1)*tw,(index//8+1)*th))
   sprite.thumbnail((160,156))
   # checkerboard to reveal transparency / edge patterns
   sheet.paste((220,220,220),(x+4,y+4,x+175,y+161))
   sheet.paste(sprite,(x+(cw-sprite.width)//2,y+4),sprite)
   draw.text((x+8,y+166),f"{name}/{index}",fill=(15,26,39))
  out=args.output/(name+"_contact.png");sheet.save(out)
  print("Saved",out)
if __name__=="__main__":main()
