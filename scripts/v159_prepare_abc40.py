#!/usr/bin/env python3
"""Source-backed A/B/C image proof preparation ONLY. Does not certify or add observations."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, io, json, hashlib, zipfile, re, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
O=R/'review/v159_abc_3760_3799'
S=O/'prep';S.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
A=rows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
B=rows(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')
C=rows(R/'review/v121_C_diff_new4632/C_B_DIFFERENCE_4632.csv')
assert len(A)==4633 and len(B)==len(C)==4632
def key(r):return r['tile_set_name'],int(r['local_id'])
bmap={key(r):r for r in B};cmap={key(r):r for r in C}
assert len(bmap)==len(cmap)==4632
old=rows(R/'analysis/imports/merged_catalog_5409.csv')
oldkeys={(r['tile_set_locator'],int(r['local_id'])) for r in old}
archives={};tmxs={}
def readzip(rel,entry,expected):
 p=R/rel
 if rel not in archives:
  archives[rel]=zipfile.ZipFile(p)
  assert archives[rel].testzip() is None,rel
 data=archives[rel].read(entry)
 assert sha(data)==expected,(rel,entry)
 return data
def checktmx(r):
 name=r['tmx_file'];p=R/'B4220.3_MapExport_256/tmx'/name
 assert sha(p.read_bytes())==r['tmx_sha256']
 if name not in tmxs:
  root=ET.parse(p).getroot()
  tmxs[name]=(root,list(root.iter('layer')),sorted((int(z.get('firstgid')),z.get('name')) for z in root.findall('tileset') if z.get('name')))
 root,layers,firsts=tmxs[name]
 layer=layers[int(r['source_layer_index'])]
 w,h=int(root.get('width')),int(root.get('height'))
 x,y=int(r['source_x']),int(r['source_y'])
 assert 0<=x<w and 0<=y<h
 gids=[int(q) for q in re.findall(r'\d+',layer.find('data').text or '')]
 assert len(gids)==w*h and gids[y*w+x]==int(r['source_raw_gid'])
 lv=layer.get('level')
 if lv is None:
  z=layer.find("properties/property[@name='level']")
  lv=(z.get('value') or z.text or '0') if z is not None else '0'
 assert int(lv)==int(r['source_level'])
 gid=int(r['source_raw_gid'])&0x0fffffff
 first,name=max((z for z in firsts if z[0]<=gid))
 assert (name,gid-first)==key(r)
 return first
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
result=[]
for ix in range(3760,3800):
 a=A[ix];k=key(a)
 assert k in bmap and k in cmap
 b=bmap[k];c=cmap[k]
 assert k not in oldkeys
 assert a['selection_status']=='selected_provisional'
 first=checktmx(b)
 p=R/a['source_image_path'];source=p.read_bytes()
 assert sha(source)==a['source_png_sha256']
 with Image.open(io.BytesIO(source)) as im:atlas=im.convert('RGBA')
 box=tuple(int(x) for x in a['selected_crop_xyxy'].strip('[]').split(','))
 assert len(box)==4 and 0<=box[0]<box[2]<=atlas.width and 0<=box[1]<box[3]<=atlas.height
 crop=atlas.crop(box)
 assert sha(crop.tobytes())==a['selected_rgba_pixel_sha256']
 bp='review/v120_B_context_new4632/'+b['B_zip_shard']
 cp='review/v121_C_diff_new4632/'+c['C_zip_shard']
 dp='review/v121_C_diff_new4632/'+c['DIFF_zip_shard']
 bi=readzip(bp,b['B_zip_entry'],b['B_webp_file_sha256'])
 ci=readzip(cp,c['C_zip_entry'],c['C_webp_file_sha256'])
 di=readzip(dp,c['DIFF_zip_entry'],c['DIFF_png_file_sha256'])
 with Image.open(io.BytesIO(bi)) as im:bim=im.convert('RGB')
 with Image.open(io.BytesIO(ci)) as im:cim=im.convert('RGB')
 with Image.open(io.BytesIO(di)) as im:dim=im.convert('RGB')
 assert bim.size==cim.size==dim.size==(800,580)
 assert int(c['removed_exactly_one_raw_gid'])==1
 reasons=[]
 if int(c['B_minus_C_changed_pixels'])<=0:reasons.append('B_C_zero')
 if int(b['neighbor_tiles_skipped'])>0:reasons.append('missing_neighbors')
 if b['scene_truncated_at_map_edge']=='1':reasons.append('map_edge')
 result.append(dict(index=ix,tile_set_name=k[0],local_id=k[1],A_png=a['source_image_path'],A_png_sha256=a['source_png_sha256'],
 A_rgba_pixel_sha256=a['selected_rgba_pixel_sha256'],A_crop_xyxy=a['selected_crop_xyxy'],
 tmx=b['tmx_file'],tmx_sha256=b['tmx_sha256'],level=b['source_level'],layer_index=b['source_layer_index'],
 x=b['source_x'],y=b['source_y'],raw_gid=b['source_raw_gid'],firstgid=first,
 B_sha256=b['B_webp_file_sha256'],C_sha256=c['C_webp_file_sha256'],delta_sha256=c['DIFF_png_file_sha256'],
 B_C_changed_pixels=c['B_minus_C_changed_pixels'],exception=';'.join(reasons),visual_observed=0,certified=0))
 page=(ix-3760)//5;pos=(ix-3760)%5
 if pos==0:
  sheet=Image.new('RGB',(1640,1320),'#edf1f4');draw=ImageDraw.Draw(sheet)
 y=pos*264
 draw.rectangle((3,y+2,1635,y+261),fill='#ffffff',outline='#9eafbc',width=2)
 label=str(ix)+'  '+k[0]+'/'+str(k[1])+'  B-C pixels '+str(c['B_minus_C_changed_pixels'])+'  '+','.join(reasons)
 draw.text((10,y+7),label,font=font,fill='#172b3b')
 for j,(title,im) in enumerate([('A ORIGINAL',crop),('B ORIGINAL TMX',bim),('C ONE REMOVED',cim),('B-C DELTA',dim)]):
  xx=j*410
  draw.text((xx+10,y+30),title,font=font,fill='#3e586b')
  thumb=im.copy();thumb.thumbnail((398,204))
  xy=(xx+(408-thumb.width)//2,y+51+(204-thumb.height)//2)
  if thumb.mode=='RGBA':sheet.paste(thumb,xy,thumb)
  else:sheet.paste(thumb,xy)
 if pos==4:sheet.save(S/f'proof_{page:02}.jpg',quality=90,optimize=True)
for a in archives.values():a.close()
assert len(result)==40
with (O/'SOURCE_A_B_C_CHECKS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
files=[O/'SOURCE_A_B_C_CHECKS.csv',*sorted(S.glob('*.jpg'))]
manifest=dict(version='v159_prep',scope=[3760,3799],source_verified=40,provisional_promoted=0,certified=0,
 exceptions=[dict(index=x['index'],reason=x['exception']) for x in result if x['exception']],
 proof_sha256={str(p.relative_to(O)):sha(p.read_bytes()) for p in files})
(O/'PREP_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(list(S.glob('*.jpg')))==8
print('PASS prepared 40 A/B/C/DELTA source verified images; exceptions',manifest['exceptions'])
