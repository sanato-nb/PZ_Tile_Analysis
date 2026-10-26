#!/usr/bin/env python3
"""Decode exact 888 original v114 evidence images into contact sheets for literal AI visual review.
Outputs do not certify any identity. No fabricated analysis.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import re,json,base64,io,hashlib,csv
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'review/888_no_identity_candidate/PZ_888종_일괄수동검수.html'
out=ROOT/'review/v115_model_visual';out.mkdir(parents=True,exist_ok=True)
text=src.read_text('utf8')
m=re.search(r'const DATA=(\[.*?\]);\s*const KEY=',text,re.S)
assert m,'embedded 888 DATA json not found'
rows=json.loads(m.group(1))
assert len(rows)==888
per=12
for i in range(0,len(rows),per):
    grid=Image.new('RGB',(2160,3*570),(232,235,240))
    d=ImageDraw.Draw(grid)
    for j,r in enumerate(rows[i:i+per]):
        x=(j%4)*540;y=(j//4)*570
        d.rounded_rectangle((x+3,y+3,x+537,y+566),radius=8,fill=(253,253,253),outline=(135,145,154),width=2)
        title=f'{i+j:03d} {r["tileset"]}/{r["local_id"]}'
        d.text((x+8,y+12),title,fill=(16,29,42),font=ImageFont.load_default())
        d.text((x+8,y+30),f'DELTA={r["delta"]} | {r["source_status"]}',fill=(60,74,85),font=ImageFont.load_default())
        packed=r['image'].split(',',1)[1];im=Image.open(io.BytesIO(base64.b64decode(packed))).convert('RGB')
        assert im.size==(1200,270)
        # A1, A2, B, C, D individually, combine A1 and A2 top row, B,C,D bottom
        for k,box in [(0,(x+12,y+58,x+255,y+305)),(1,(x+278,y+58,x+522,y+305)),
                      (2,(x+11,y+332,x+179,y+551)),(3,(x+185,y+332,x+353,y+551)),
                      (4,(x+358,y+332,x+529,y+551))]:
            cell=im.crop((240*k,0,240*(k+1),270))
            boundw=box[2]-box[0];boundh=box[3]-box[1]
            cell.thumbnail((boundw,boundh),Image.Resampling.LANCZOS)
            grid.paste(cell,(box[0]+(boundw-cell.width)//2,box[1]+(boundh-cell.height)//2))
    name=out/f'sheet_{i//per:03d}.jpg'
    grid.save(name,quality=85,optimize=True)
    if (i//per+1)%12==0:print('SHEET',i//per+1,'/74',flush=True)
with (out/'INDEX.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['sheet','slot','index','tileset','local_id','delta','source_status'])
    for i,r in enumerate(rows):w.writerow([f'sheet_{i//per:03d}.jpg',i%per,i,r['tileset'],r['local_id'],r['delta'],r['source_status']])
manifest=dict(source='v114 888 HTML with native 1200x270 embedded WEBP evidence',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
  n=888,sheets=74,per_sheet=12,has_expanded_context=False,mapping_certified=0,
  sheet_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('sheet_*.jpg'))})
assert len(manifest['sheet_sha256'])==74
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('SUCCESS',manifest['n'],manifest['sheets'])
