#!/usr/bin/env python3
"""v127 review extraction: all variant-source candidates, source-missing and no-alternative."""
from pathlib import Path
import csv,hashlib,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
O=R/'review/v127_D_A_candidates_full4633'
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
ledger=rows(O/'D_CANDIDATE_LEDGER_4633.csv')
trials=rows(O/'D_ALL_CANDIDATE_TRIALS.csv')
bykey=lambda r:(r['tile_set_name'],r['local_id'])
variants=[r for r in ledger if int(r['exact_basename_variant_candidates'])>0]
none=[r for r in ledger if r['search_status']=='no_distinct_visible_alternative']
held=[r for r in ledger if r['search_status']=='held_no_source_PNG']
assert len(variants)==3 and len(none)==1 and len(held)==1
keys={bykey(r) for r in variants}
vr=[r for r in trials if bykey(r) in keys and r['category']=='same_basename_atlas_variant' and r['result']=='distinct_visible_unverified_correspondence']
assert len(vr)==3
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
tiny=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
board=Image.new('RGB',(1120,960),(245,247,249));d=ImageDraw.Draw(board)
details=[]
def cropped(path,coords):
    p=R/path
    if not p.exists():return None
    box=tuple(int(v) for v in coords.strip('[]').split(','))
    with Image.open(p) as im: return im.convert('RGBA').crop(box)
def present(im,x,y):
    if im is None:return
    t=im.copy();t.thumbnail((300,210))
    board.paste(t,(x+(320-t.width)//2,y+(210-t.height)//2),t)
for i,original in enumerate(variants):
    key=bykey(original)
    matches=[r for r in vr if bykey(r)==key]
    assert len(matches)==1
    alt=matches[0]
    a=cropped(original['source_png'],original['original_bbox'])
    b=cropped(alt['source_path'],alt['source_crop'])
    assert a is not None and b is not None
    assert hashlib.sha256(a.tobytes()).hexdigest()==original['original_rgba_sha256']
    assert hashlib.sha256(b.tobytes()).hexdigest()==alt['rgba_sha256']
    y=i*320
    d.rectangle((10,y+10,1110,y+312),fill='white',outline=(138,157,174),width=2)
    d.text((24,y+20),str(key[0])+'/'+str(key[1])+'    index='+original['index'],font=font,fill=(25,43,61))
    d.text((45,y+55),'Original selected A',font=tiny,fill=(47,73,95))
    d.text((575,y+55),'Same-basename PNG variant (UNVERIFIED)',font=tiny,fill=(169,92,30))
    present(a,55,y+88);present(b,585,y+88)
    d.text((25,y+291),str(alt['source_path'])[:125],font=tiny,fill=(70,78,88))
    details.append(dict(index=int(original['index']),tile_set_name=key[0],local_id=int(key[1]),
        original_png=original['source_png'],original_crop=original['original_bbox'],
        variant_png=alt['source_path'],variant_crop=alt['source_crop'],
        variant_rgba_sha256=alt['rgba_sha256'],status='same_basename_other_png_not_mapping_certified'))
img=O/'D_EXACT_BASENAME_VARIANTS_3.jpg'
board.save(img,quality=90,optimize=True)
out=dict(source='v127_D_A_candidates_full4633',candidate_variant_count=3,
    variant_tile_keys=details,
    no_other_visible_alternative=[dict(index=int(r['index']),tile_set_name=r['tile_set_name'],local_id=int(r['local_id'])) for r in none],
    original_PNG_missing=[dict(index=int(r['index']),tile_set_name=r['tile_set_name'],local_id=int(r['local_id'])) for r in held],
    comparison_image=img.relative_to(R).as_posix(),
    comparison_image_sha256=hashlib.sha256(img.read_bytes()).hexdigest(),
    mapping_verified=0,tilezed_verified=0,final_certified=0,
    disclaimer='Variants share basename, not verified same TMX Local ID. Neighbors not same tile.')
(O/'PRIORITY_VARIANTS_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'PRIORITY_VARIANTS_3.md').write_text(
 '# v127 동일 타일셋명 다른 PNG 버전 A 후보 3종\n\n'+
 '\n'.join('- '+q['tile_set_name']+'/'+str(q['local_id'])+' / '+q['variant_png']+' / 정합 **미인증**' for q in details)+
 '\n\n'+
 '추가 이미지 후보 없는 1종: '+', '.join(x['tile_set_name']+'/'+str(x['local_id']) for x in out['no_other_visible_alternative'])+
 '\n원본 PNG 미확보 1종: '+', '.join(x['tile_set_name']+'/'+str(x['local_id']) for x in out['original_PNG_missing'])+
 '\n\n정의: 다른 원본 PNG 이미지 탐색 단계이며, 5×5 B 재조립 및 공식 ID 인증은 아직 안 했다.\n',
 encoding='utf8')
print('PASS v127 highlights',json.dumps(out,ensure_ascii=False),flush=True)
