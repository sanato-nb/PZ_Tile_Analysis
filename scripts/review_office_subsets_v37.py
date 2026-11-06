"""Classify and render the 12 observed office layouts from the v36 connected sets."""
import csv
import json
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path('analysis/furniture_full_b42/2026-11-06')
SOURCE = ROOT / 'warning_layouts_v36/V36_COMPONENTS.csv'
ATLAS = Path('Tiles/2x/location_business_office_generic_01.png')
OUT = ROOT / 'office_subsets_v37'
GROUP = 'FUR-EFCE0AC5D3BB44A4'
# Local IDs in reading order as observed in the maps, indexed by style and facing.
STYLES = [
    {'E':[0,1], 'N':[8,10], 'S':[5,6], 'W':[13,14]},
    {'E':[40,41], 'N':[44,45], 'S':[42,43], 'W':[46,47]},
    {'E':[72,73,74], 'N':[80,81,82], 'S':[75,76,77], 'W':[83,84,85]},
]


def offsets(face, ids):
    return [(n,0,len(ids)-1-i) if face in 'EW' else (n,i,0)
            for i,n in enumerate(ids)]


def render(atlas, shape):
    points = [(n,64*(x-y),32*(x+y)) for n,x,y in sorted(shape,key=lambda t:t[1]+t[2])]
    min_x = min(x for n,x,y in points)
    canvas = Image.new('RGBA',(384,384))
    for n,x,y in points:
        left,top = n%8*128,n//8*256
        canvas.alpha_composite(atlas.crop((left,top,left+128,top+256)),(x-min_x,y))
    return canvas.crop(canvas.getbbox())


def run(source, atlas_path, out):
    out.mkdir(parents=True,exist_ok=True)
    with source.open() as f:
        rows=[r for r in csv.DictReader(f) if r['group']==GROUP]
    atlas=Image.open(atlas_path).convert('RGBA')
    assert atlas.width==1024 and len(rows)==5699
    counts=Counter()
    ledger=[]
    residual=[]
    for row in rows:
        assert row['has_flags']=='0'
        face=row['facing']
        parts=Counter(tuple(t) for t in json.loads(row['normalized_parts']))
        used=Counter()
        for style,facings in enumerate(STYLES,1):
            shape=offsets(face,facings[face])
            anchor,ax,ay=shape[0]
            for n,x,y in parts:
                if n!=anchor:
                    continue
                target=[(k,x+dx-ax,y+dy-ay) for k,dx,dy in shape]
                copies=min(parts[p] for p in target)
                if not copies:
                    continue
                single=sum(parts.values())==len(shape)
                counts[style,face,'isolated' if single else 'embedded']+=copies
                for p in target:
                    used[p]+=copies
                ledger.append((style,face,row['level'],int(row['min_world_x'])+x,
                               int(row['min_world_y'])+y,copies,int(single)))
        assert not (used-parts)
        for (n,x,y),copies in sorted((parts-used).items()):
            residual.append((face,row['level'],int(row['min_world_x'])+x,
                             int(row['min_world_y'])+y,n,copies))
            counts['unmatched']+=copies
    sheet=Image.new('RGB',(840,690),'#eae7df')
    draw=ImageDraw.Draw(sheet)
    summary=[]
    for i,facings in enumerate(STYLES):
        for j,face in enumerate('ENSW'):
            shape=offsets(face,facings[face])
            crop=render(atlas,shape)
            crop.thumbnail((195,162))
            x=j*210+6
            y=i*230+5
            sheet.paste(crop,(x,y+45),crop)
            draw.text((x,y+4),f"Style {i+1}   {face}   IDs "+",".join(map(str,facings[face])),fill='#242424')
            isolated=counts[i+1,face,'isolated']
            embedded=counts[i+1,face,'embedded']
            summary.append((i+1,face,json.dumps(shape),isolated,embedded,isolated+embedded))
    for file,header,data in [('V37_SUBSETS.csv',['style','facing','relative_parts','isolated','embedded','total'],summary),
                             ('V37_UNMATCHED.csv',['facing','level','world_x','world_y','local_id','copies'],residual),
                             ('V37_OCCURRENCES.csv',['style','facing','level','anchor_world_x','anchor_world_y','copies','isolated'],ledger)]:
        with (out/file).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(header);w.writerows(data)
    sheet.save(out/'V37_OFFICE_LAYOUTS.png')
    matched=sum(r[-1]*len(STYLES[r[0]-1][r[1]]) for r in summary)
    assert matched+counts['unmatched']==sum(int(r['parts']) for r in rows)
    print(summary,matched,counts['unmatched'])


if __name__=='__main__':
    run(SOURCE,ATLAS,OUT)
