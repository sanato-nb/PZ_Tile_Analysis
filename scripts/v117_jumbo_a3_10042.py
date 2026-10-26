#!/usr/bin/env python3
"""v117 JUMBO A3 fallback: propose visually observed whole-atlas sprite grids for 36
exceptional source-available keys, while retaining all A1/A2 evidence.
A3 is provisional, not an official TileZed map. Zero-alpha does not prove transparency.
"""
from pathlib import Path
from collections import Counter
import csv,json,hashlib
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v117_A_candidates_10042'
master=OUT/'A_CANDIDATE_MASTER_10042.csv'
with master.open('r',encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==10042
def guess_grid(name,im):
    w,h=im.size
    if 'JUMBOXXL' in name and (w,h)==(5376,3072):return (6,2),'whole_sprite_columns_6_rows_2_from_atlas'
    if 'JUMBOXL' in name and (w,h)==(3840,2304):return (6,2),'whole_sprite_columns_6_rows_2_from_atlas'
    if 'JUMBO_1' in name and w==768 and h in (2048,3072):
        return (2,h//512),'whole_sprite_columns_2_rows_'+str(h//512)+'_from_atlas'
    if name=='e_stumps_JUMBOXXL' and (w,h)==(1024,6144):
        return (8,24),'stump_small_sprite_grid_8x24_provisional'
    return None,'no_supported_A3_manual_grid'
def hashpix(im):return hashlib.sha256(im.tobytes()).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(fontfile,13)
small=ImageFont.truetype(fontfile,11)
canvas=Image.new('RGB',(1800,1800),(239,243,248))
draw=ImageDraw.Draw(canvas)
fallback=OUT/'jumbo_a3'
fallback.mkdir(exist_ok=True)
details=[];stats=Counter()
for r in rows:
    decision=r['candidate_decision']
    if decision=='no_usable_source' and r['source_png_path'] and 'JUMBO' in r['tile_set_name']:
        p=R/r['source_png_path']
        with Image.open(p) as image:im=image.convert('RGBA')
        grid,method=guess_grid(r['tile_set_name'],im)
        lid=int(r['local_id'])
        if grid is not None:
            cols,rr=grid
            w,h=im.size;sw=w//cols;sh=h//rr
            if lid<cols*rr:
                x=(lid%cols)*sw;y=(lid//cols)*sh
                tile=im.crop((x,y,x+sw,y+sh))
                alpha=sum(tile.getchannel('A').histogram()[1:])
                if alpha>0:
                    stats['recovered_A3']+=1
                    n=stats['recovered_A3']-1
                    thumb=tile.copy();thumb.thumbnail((205,155),Image.Resampling.LANCZOS)
                    cell=Image.new('RGBA',(210,158),(244,247,249,255))
                    cell.alpha_composite(thumb,((210-thumb.width)//2,(158-thumb.height)//2))
                    x0=(n%6)*300;y0=(n//6)*300
                    draw.rectangle((x0+2,y0+2,x0+295,y0+297),fill='white',outline=(167,181,193))
                    draw.text((x0+9,y0+9),str(n+1).zfill(2)+' '+r['tile_set_name'][:32],font=small,fill=(29,44,56))
                    draw.text((x0+9,y0+31),'Local ID '+str(lid)+' / A3 grid '+str(cols)+'x'+str(rr),font=small,fill=(45,90,110))
                    canvas.paste(cell.convert('RGB'),(x0+42,y0+58))
                    draw.text((x0+8,y0+233),f'A3 alpha {alpha:,} | crop {sw}x{sh}',font=small,fill=(40,67,79))
                    draw.text((x0+8,y0+253),'UNVERIFIED Local ID mapping',font=small,fill=(158,74,26))
                    detail=dict(tile_set_name=r['tile_set_name'],local_id=lid,
                      source_png_path=r['source_png_path'],guess_grid=f'{cols}x{rr}',
                      crop_bbox=[x,y,x+sw,y+sh],visible_alpha_pixels=alpha,
                      pixels_sha256=hashpix(tile),approach=method,
                      whole_atlas_preview=next(
                        (d['source_preview'] for d in json.loads((OUT/'exceptions/EXCEPTIONS.json').read_text('utf8'))['names']
                          if d['tileset']==r['tile_set_name'] and 'source_preview' in d),None),
                      manual_full_atlas_visually_inspected=True,
                      ai_per_local_id_mapping_verified=False,official_tilezed_verified=False)
                    details.append(detail)
                    r['A3_status']='proposed_visible'
                    r['A3_source_png_path']=r['source_png_path']
                    r['A3_grid']=detail['guess_grid']
                    r['A3_crop_bbox']=','.join(map(str,detail['crop_bbox']))
                    r['A3_alpha_pixels']=alpha
                    r['A3_pixel_sha256']=detail['pixels_sha256']
                    r['new_preferred_A']='A3'
                    r['new_candidate_decision']='proposed_jumbo_whole_sprite_grid_needs_ai'
                else:stats['A3_empty']+=1
        if r.get('A3_status')!='proposed_visible':
            r['A3_status']=method if grid is None else 'A3_crop_not_visible'
    if 'new_preferred_A' not in r:
        r['new_preferred_A']=r['preferred_A']
        r['new_candidate_decision']=r['candidate_decision']
        r.setdefault('A3_status','')
        r.setdefault('A3_source_png_path','')
        r.setdefault('A3_grid','')
        r.setdefault('A3_crop_bbox','')
        r.setdefault('A3_alpha_pixels',0)
        r.setdefault('A3_pixel_sha256','')
    stats[r['new_candidate_decision']]+=1
assert sum(v for k,v in stats.items() if k.startswith('proposed') or k.startswith('no_') or k=='needs_ai_comparison')==10042
csvpath=OUT/'A_CANDIDATE_COMBINED_10042.csv'
fields=list(rows[0])
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
canvas.save(fallback/'A3_JUMBO_review_sheet.jpg',quality=91,optimize=True)
with (fallback/'A3_CANDIDATES.csv').open('w',encoding='utf-8-sig',newline='') as f:
    columns=list(details[0]);writer=csv.DictWriter(f,fieldnames=columns)
    writer.writeheader();writer.writerows(details)
assert stats['recovered_A3']==len(details)
outcomes=Counter(r['new_candidate_decision'] for r in rows)
assert sum(outcomes.values())==10042
summary=dict(version='v117-a3',all_keys=10042,
    original_A1_A2_consistent=outcomes['proposed_consistent'],
    original_one_visible=outcomes['proposed_one_visible_needs_ai'],
    A3_jumbo_guessed=outcomes['proposed_jumbo_whole_sprite_grid_needs_ai'],
    still_no_visible=outcomes['no_visible_candidate'],
    still_no_source=outcomes['no_usable_source'],
    candidates_with_visible_A=10042-outcomes['no_visible_candidate']-outcomes['no_usable_source'],
    new_mapping_verified=0,AI_per_key_selected=0,final_certified=0,
    sources='TileZed text + TMX 26_43 declarations + exact name PNG and 29 whole atlas previews',
    full_ledger='review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv',
    full_ledger_sha256=sha(csvpath),
    jumbo_A3_preview='review/v117_A_candidates_10042/jumbo_a3/A3_JUMBO_review_sheet.jpg',
    caution='A3 entire sprite grid visually plausible; PNG/TMX Local ID association not officially verified, no transparency certified')
(fallback/'A3_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v117 augmented',json.dumps(summary,ensure_ascii=False),flush=True)
