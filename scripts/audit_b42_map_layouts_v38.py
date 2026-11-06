"""Audit missing desk partners across all layers and render frequent warning-group layouts."""
import bisect
import csv
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path('analysis/furniture_full_b42/2026-11-06')
OUT = ROOT / 'map_review_v38'
OFFICE = 'location_business_office_generic_01'
MAPS = Path('B4220.3_MapExport_256/tmx')


def read(path):
    with path.open(encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))


def save(name, columns, rows):
    with (OUT/name).open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(rows)


def neighbors():
    prior = ROOT/'office_subsets_v37'
    templates = {}
    for row in read(prior/'V37_SUBSETS.csv'):
        parts = json.loads(row['relative_parts'])
        for n,x,y in parts:
            templates[n] = [(k,dx-x,dy-y) for k,dx,dy in parts if k != n]
    targets = read(prior/'V37_UNMATCHED.csv')
    requests = defaultdict(set)
    for r in targets:
        x,y,z,n = (int(r[k]) for k in ['world_x','world_y','level','local_id'])
        for dx,dy in {(dx,dy) for _,dx,dy in templates[n]} | {(0,0),(0,1),(1,0),(-1,0),(0,-1)}:
            wx,wy = x+dx,y+dy
            requests[wx//256,wy//256].add((z,wx,wy))
    cells = defaultdict(list)
    for (cx,cy), points in requests.items():
        path = MAPS/f'{cx}_{cy}.tmx'
        root = ET.parse(path).getroot()
        assert root.get('width') == root.get('height') == '256'
        sheets = sorted((int(t.get('firstgid')),t.attrib['name']) for t in root.findall('tileset'))
        starts = [start for start,_ in sheets]
        by_level = defaultdict(list)
        for z,x,y in points:
            by_level[z].append((x,y))
        for i,lay in enumerate(root.iter('layer')):
            z = int(lay.attrib['level'])
            if z not in by_level:
                continue
            d = lay.find('data')
            assert d.get('encoding')=='csv' and lay.get('width')==lay.get('height')=='256'
            assert not any(int(lay.get(k,0)) for k in ('x','y','offsetx','offsety'))
            v = np.fromstring(d.text.strip().rstrip(','),sep=',',dtype=np.uint32)
            assert len(v)==65536
            for x,y in by_level[z]:
                raw = int(v[(y%256)*256+x%256])
                if raw:
                    gid=raw & 0x0fffffff
                    j=bisect.bisect_right(starts,gid)-1
                    assert j>=0
                    cells[z,x,y].append([i,lay.get('name'),sheets[j][1],gid-starts[j],raw>>28])
    results=[]
    for r in targets:
        x,y,z,n = (int(r[k]) for k in ['world_x','world_y','level','local_id'])
        center=cells[z,x,y]
        assert sum(t[2:]==[OFFICE,n,0] for t in center)>=int(r['copies'])
        for k,dx,dy in templates[n]:
            data=cells[z,x+dx,y+dy]
            office=[t[3] for t in data if t[2]==OFFICE]
            status='expected_present' if k in office else 'other_office_tile' if office else 'other_tiles_only' if data else 'empty'
            results.append([n,z,x,y,k,x+dx,y+dy,status,json.dumps(office),json.dumps(data)])
    save('V38_EXPECTED_CELLS.csv',['source_id','level','world_x','world_y','expected_id','expected_x','expected_y','status','office_ids','all_layers'],results)
    save('V38_NEIGHBORS.csv',['level','world_x','world_y','all_layers'],[(z,x,y,json.dumps(cells[z,x,y])) for points in requests.values() for z,x,y in sorted(points)])
    assert sum(int(r['copies']) for r in targets)==174


def patterns():
    prior=ROOT/'warning_layouts_v36'
    rows=read(prior/'V36_COMPONENTS.csv')
    atlas_by_group={r['group']:r['atlas'] for r in read(prior/'V36_DIRECTION_SUMMARY.csv')}
    counts=Counter((r['group'],r['facing'],r['normalized_parts']) for r in rows if r['has_flags']=='0')
    records=[]
    for (group,face,shape),count in counts.most_common():
        records.append((group,atlas_by_group[group],face,shape,count))
    save('V38_ALL_LAYOUT_FREQUENCIES.csv',['group','atlas','facing','normalized_parts','occurrences'],records)
    # Select the most recurrent compact multi-part layouts in each atlas, with
    # up to three examples per facing and group. Single sprites stay in the CSV.
    pages=defaultdict(list)
    kept=Counter()
    for group,atlas,face,shape,count in records:
        parts=json.loads(shape)
        if count<2 or not 2<=len(parts)<=8 or len({n for n,x,y in parts})!=len(parts):
            continue
        if kept[group,face]>=3:
            continue
        kept[group,face]+=1
        pages[atlas].append((group,face,parts,count))
    selected=[]
    for atlas,items in sorted(pages.items()):
        with Image.open(Path('Tiles/2x')/(atlas+'.png')) as raw:
            src=raw.convert('RGBA')
        assert src.width%128==0
        columns=src.width//128
        canvas=Image.new('RGB',(720,((len(items)+2)//3)*190),'#e7e5dd')
        draw=ImageDraw.Draw(canvas)
        for i,(group,face,parts,count) in enumerate(items):
            coords=[(n,(x-y)*64,(x+y)*32) for n,x,y in sorted(parts,key=lambda p:(p[1]+p[2],p[1],p[0]))]
            left=min(x for n,x,y in coords)
            cropped=Image.new('RGBA',(max(x for n,x,y in coords)-left+128,max(y for n,x,y in coords)+256))
            for n,x,y in coords:
                a,b=n%columns*128,n//columns*256
                assert b+256<=src.height
                cropped.alpha_composite(src.crop((a,b,a+128,b+256)),(x-left,y))
            assert cropped.getbbox()
            pic=cropped.crop(cropped.getbbox());pic.thumbnail((220,144))
            x=i%3*240;y=i//3*190
            canvas.paste(pic,(x+5,y+36),pic)
            draw.text((x+5,y+4),f'{i+1}  {face}  count {count}',fill='#202020')
            draw.text((x+5,y+18),','.join(str(n) for n,_,_ in parts),fill='#202020')
            selected.append([atlas,i+1,group,face,json.dumps(parts),count])
        canvas.save(OUT/f'V38_{atlas}.png')
    save('V38_RENDER_INDEX.csv',['atlas','panel','group','facing','parts','occurrences'],selected)
    assert sum(counts.values())==len(rows)==9308


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    neighbors()
    patterns()
