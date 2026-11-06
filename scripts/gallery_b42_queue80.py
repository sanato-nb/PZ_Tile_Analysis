"""Extract the 80 queued entries' original tile images and available wiki references."""
import base64
import csv
import hashlib
import io
import json
import subprocess
import sqlite3
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin,urlsplit,quote
import requests
from PIL import Image

ROOT=Path('analysis/furniture_full_b42/2026-11-06')
BASE=ROOT/'registry_map_v39'
OUT=ROOT/'queue80_gallery'
ATLAS=Path('Tiles/2x')
OUT.mkdir(exist_ok=True)
def encoded(image):
    img=image.convert('RGBA')
    box=img.getbbox()
    if not box:
        return None
    img=img.crop(box)
    img.thumbnail((440,360),Image.Resampling.NEAREST)
    data=io.BytesIO()
    img.save(data,format='PNG',optimize=True)
    return base64.b64encode(data.getvalue()).decode()

def wiki(url):
    url=urljoin('https://pzwiki.net/',url)
    if urlsplit(url).hostname not in ('pzwiki.net','theindiestone.com','projectzomboid.com'):
        return None
    try:
        resp=requests.get(url,headers={'User-Agent':'PZ-Tile-Analysis/1.0 (furniture catalog review)'},timeout=7)
        resp.raise_for_status()
        return encoded(Image.open(io.BytesIO(resp.content)))
    except (requests.RequestException,OSError,ValueError):
        return None

def review(entry):
    ref=entry['wiki_image']
    if not entry['images'] and ref:
        content=wiki(ref)
        if content:
            entry['images'].append({'name':'위키 참고 이미지','data':content,'source':ref,'kind':'wiki'})
    if not entry['images']:
        for k in entry['keys'][:2]:
            sprite=k.replace('/','_')+'.png'
            sprite=sprite[0].upper()+sprite[1:]
            h=hashlib.md5(sprite.encode()).hexdigest()
            url=f'https://pzwiki.net/w/images/{h[0]}/{h[:2]}/{quote(sprite)}'
            content=wiki(url)
            if content:
                entry['images'].append({'name':k,'data':content,'source':url,'kind':'wiki'})
                break
    return entry

with tempfile.TemporaryDirectory() as tmp:
    with zipfile.ZipFile(BASE/'B42_FURNITURE_V39.zip') as z:
        name,=[n for n in z.namelist() if n.endswith('.sqlite')]
        z.extract(name,tmp)
    db=sqlite3.connect(Path(tmp)/name)
    db.row_factory=sqlite3.Row
    records=[]
    for row in csv.DictReader((BASE/'V39_80_MAP_EVIDENCE_QUEUE.csv').open()):
        entry_id=row['entry_id']
        e=db.execute('select * from registry_entry where entry_id=?',(entry_id,)).fetchone()
        keys=[r[0] for r in db.execute('select source_key from registry_entry_tile where entry_id=? order by case evidence when "EXACT_WIKI_IMAGE_SPRITE_KEY" then 0 else 1 end, source_key',(entry_id,))]
        records.append(dict(id=entry_id,name=e['display_name'],status=row['map_evidence'],keys=keys,wiki_image=e['photo_url'],article=e['article_url'],images=[]))
    paths=sorted({str(ATLAS/(k.split('/')[0]+'.png')) for e in records for k in e['keys']})
    existing=set(subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD','Tiles/2x'],text=True).splitlines())
    paths=[p for p in paths if p in existing]
    subprocess.run(['git','sparse-checkout','add','--stdin'],input='\n'.join('/'+p for p in paths)+'\n',text=True,check=True)
    for p in paths:
        atlas=Image.open(p).convert('RGBA')
        cols=atlas.width//128
        for e in records:
            for k in e['keys']:
                sheet,num=k.split('/')
                if sheet!=Path(p).stem: continue
                n=int(num); x=(n%cols)*128;y=(n//cols)*256
                if y+256>atlas.height:continue
                data=encoded(atlas.crop((x,y,x+128,y+256)))
                if data:e['images'].append(dict(name=k,data=data,source=p,kind='tile'))
    with ThreadPoolExecutor(max_workers=6) as pool:
        records=list(pool.map(review,records))
    # Compare exact atlas names in the official mapping pack when local assets are absent.
    import re
    from html import unescape
    official='https://projectzomboid.com/tools/Tiles-August-28-2026.zip'
    missing_sheets={k.split('/')[0] for e in records if not e['images'] for k in e['keys']}
    if missing_sheets:
        try:
            from remotezip import RemoteZip
            with RemoteZip(official,timeout=12) as archive:
                for member in archive.namelist():
                    leaf=Path(member)
                    if leaf.stem not in missing_sheets or leaf.suffix!='.png' or '/2x/' not in '/'+member: continue
                    atlas=Image.open(io.BytesIO(archive.read(member))).convert('RGBA')
                    for e in records:
                        for k in e['keys']:
                            sh,n=k.split('/')
                            if sh!=leaf.stem: continue
                            x=int(n)%(atlas.width//128)*128;y=int(n)//(atlas.width//128)*256
                            data=encoded(atlas.crop((x,y,x+128,y+256)))
                            if data:e['images'].append(dict(name=k,data=data,source=official+'#'+member,kind='official'))
        except Exception as exc:
            print('optional official archive',type(exc).__name__)
    def article_ref(e):
        if e['images'] or not e['article'] or '/wiki/' not in e['article']:return
        if e['name'] in ('Decorations','Signs','Painting'):return
        try:
            html=requests.get(e['article'],timeout=10).text
            from bs4 import BeautifulSoup
            soup=BeautifulSoup(html,'html.parser')
            image=soup.select_one('table.infobox img, .infobox img')
            if image:
                url=urljoin(e['article'],image.get('src',''))
                data=wiki(url)
                if data:e['images'].append(dict(name='관련 문서의 대표 그림',source=url,kind='article',data=data))
        except (ValueError,requests.RequestException):pass
    with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(article_ref,records))
    assert len(records)==len({e['id'] for e in records})==80
    for i in range(0,80,5):
        (OUT/f'cards_{i//5:02}.json').write_text(json.dumps(records[i:i+5],ensure_ascii=False))
