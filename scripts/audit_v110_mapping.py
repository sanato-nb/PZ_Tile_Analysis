#!/usr/bin/env python3
"""TMX 선언 격자와 TileZed 타일정의 텍스트 및 원본 PNG 실제 격자 불일치 탐색 (인증 아님)."""
import json,re
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'Tiles/tiledefinitions.tiles.txt').read_text('utf8')
defs={}
for block in re.findall(r'tileset\s*\{(.*?)\}',text,re.S):
    fm=re.search(r'file\s*=\s*(\S+)',block)
    sz=re.search(r'size\s*=\s*(\d+)\s*,\s*(\d+)',block)
    if fm and sz:defs[fm.group(1)]=(int(sz.group(1)),int(sz.group(2)))
target=['d_generic_1','d_wallcracks_1','f_bushes_1','e_cockspurhawthornJUMBO_1','jumbo_tree_01']
out={}
for mapname in ('31_45.tmx','31_46.tmx'):
    root=ET.parse(ROOT/'B4220.3_MapExport_256/tmx'/mapname).getroot()
    for t in root.findall('tileset'):
        name=t.attrib['name']
        if name not in target:continue
        im=t.find('image')
        if im is None:continue
        tw,th=int(t.attrib['tilewidth']),int(t.attrib['tileheight'])
        iw,ih=int(im.attrib['width']),int(im.attrib['height'])
        png=ROOT/'Tiles/2x'/(name+'.png')
        item=dict(map=mapname,firstgid=int(t.attrib['firstgid']),tile_width=tw,tile_height=th,
                  tmx_image_width=iw,tmx_image_height=ih,
                  tmx_columns=iw//tw,tmx_rows=ih//th,tiledef_grid=defs.get(name),
                  png_exists=png.exists())
        if png.exists():
            with Image.open(png) as p:
                item.update(png_width=p.width,png_height=p.height)
                if name in defs:
                    cols,rows=defs[name]
                    item.update(tiledef_crop_width=p.width//cols,tiledef_crop_height=p.height//rows,
                                tiledef_exact_divisible=(p.width%cols==0 and p.height%rows==0),
                                tiledef_matches_2x=(p.width==cols*tw*2 and p.height==rows*th*2))
        out.setdefault(name,[]).append(item)
path=ROOT/'audits/v110_mapping_probe.json'
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n','utf8')
print('TMX_TILEDEF_PNG_PROBE',json.dumps(out,ensure_ascii=False))
