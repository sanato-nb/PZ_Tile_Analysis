#!/usr/bin/env python3
"""Inspect all v117 A-source exceptions without inventing corrected Local ID maps."""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parents[1];T=R/'Tiles'
out=R/'review/v117_A_candidates_10042/exceptions'
out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((R/'review/v117_A_candidates_10042/MANIFEST.json').read_text('utf8'))
names=sorted(n for n,count in manifest['source_name_status_per_tileset'].items()
  if count.get('no_visible_candidate',0) or count.get('no_usable_source',0))
assert len(names)==29
ts=ET.parse(R/'B4220.3_MapExport_256/tmx/26_43.tmx').getroot()
d={}
for x in ts.findall('tileset'):
    im=x.find('image')
    if im is None:continue
    n=x.get('name');d[n]=dict(tw=x.get('tilewidth'),th=x.get('tileheight'),
      iw=im.get('width'),ih=im.get('height'),imsource=im.get('source'))
grid={}
for b in re.findall(r'tileset\s*\{(.*?)\}',(T/'tiledefinitions.tiles.txt').read_text(),re.S):
    n=re.search(r'file\s*=\s*(\S+)',b);m=re.search(r'size\s*=\s*(\d+)\s*,\s*(\d+)',b)
    if n and m:grid[n.group(1)]=[int(m.group(1)),int(m.group(2))]
paths={}
for p in sorted(T.rglob('*.png')):
    paths.setdefault(p.stem,[]).append(p)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(fontpath,11)
large=ImageFont.truetype(fontpath,13)
sheet=Image.new('RGB',(2520,1890),(236,242,247))
draw=ImageDraw.Draw(sheet);details=[]
for i,n in enumerate(names):
    x0=(i%6)*420;y0=(i//6)*378
    draw.rectangle((x0+3,y0+2,x0+417,y0+375),fill=(255,255,255),outline=(159,173,186))
    draw.text((x0+9,y0+10),f'[{i+1:02d}] {n[:47]}',font=font,fill=(30,42,53))
    allp=paths.get(n,[])
    detail=dict(tileset=n,count=manifest['source_name_status_per_tileset'][n],
         tmx=d.get(n),tiledef_grid=grid.get(n),
         exact_name_pngs=[str(p.relative_to(R)) for p in allp])
    if allp:
        p=allp[0]
        with Image.open(p) as im:
            dims=im.size;im=im.convert('RGBA')
            bbox=im.getchannel('A').getbbox()
            display=im.copy()
        detail['png_pixels']=list(dims);detail['alpha_bbox']=list(bbox) if bbox else None
        display.thumbnail((396,287),Image.Resampling.LANCZOS)
        bg=Image.new('RGB',display.size,(237,241,244))
        bg.paste(display,(0,0),display)
        sheet.paste(bg,(x0+(420-display.width)//2,y0+34+(290-display.height)//2))
        detail['source_preview']=(out/f'original_atlas_{i+1:02d}.jpg').relative_to(R).as_posix()
        bg.save(R/detail['source_preview'],quality=88)
        draw.text((x0+8,y0+333),f'PNG {dims}   TileZed {grid.get(n)}',font=font,fill=(30,65,91))
        if d.get(n):
            draw.text((x0+8,y0+351),f'TMX img {d[n]["iw"]}x{d[n]["ih"]}, cell {d[n]["tw"]}x{d[n]["th"]}',
                font=font,fill=(30,65,91))
    else:
        draw.text((x0+25,y0+154),'EXACT-NAME PNG MISSING',font=large,fill=(152,50,44))
        detail['png_pixels']=None
    details.append(detail)
sheet.save(out/'A_43_exceptions_source_atlases.jpg',quality=89,optimize=True)
assert len(details)==29
(out/'EXCEPTIONS.json').write_text(json.dumps(dict(count_distinct_tilesets=29,
    unresolved_keys=43,names=details,
    warning='Displayed full PNG atlases are NOT per-ID A candidates. No Local ID alignment or transparency is certified.'),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS 29 exceptional PNG names shown in their full-atlas actual pixels; no inferred Local ID mapping')
