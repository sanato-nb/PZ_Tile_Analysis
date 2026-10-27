#!/usr/bin/env python3
"""v130 corrected D: alternative source A hypotheses for the SAME tile key,
rendered again in the SAME original TMX B 5x5 scene by replacing one GID draw.

This is NOT a second map placement. Neighbor-grid offsets are explicit UNVERIFIED
alignment probes, never verified Local ID correspondence or certified identities.
Preserves all older 5409, manual80, exclusions14, PNG/TMX and all previous DB tables.
"""
from pathlib import Path
import os
from collections import Counter
from functools import lru_cache
import bisect,csv,hashlib,base64,zlib,html,io,json,sqlite3,re,zipfile
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageChops
R=Path(__file__).resolve().parents[1]
ROOT=R/'B4220.3_MapExport_256/tmx'
batch_id=int(os.environ.get('D_BATCH_INDEX','0'))
assert 0<=batch_id<=11
beg,end=(0,320) if batch_id==0 else (1120+(batch_id-1)*320,min(4632,1120+batch_id*320))
OUT=R/'review/v131_D_full_remaining'/('batch_%02d'%batch_id)
OUT.mkdir(exist_ok=True,parents=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):return sha(p.read_bytes())
def csvrows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bbox(st):
    if not st:return None
    x=[int(t) for t in st.strip('[]').split(',')]
    assert len(x)==4 and x[0]<x[2] and x[1]<x[3]
    return tuple(x)
def layerlevel(ly):
    if 'level' in ly.attrib:return int(ly.get('level','0'))
    z=ly.find("properties/property[@name='level']")
    return int((z.get('value') or z.text or '0') if z is not None else '0')
all_a=csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
a={(v['tile_set_name'],int(v['local_id'])):v for v in all_a if v['selection_status']=='selected_provisional'}
assert len(a)==4632
legacy=csvrows(R/'review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv')
cand={(v['tile_set_name'],int(v['local_id'])):v for v in legacy}
assert len(cand)==10042
oldkeys={(r['tile_set_locator'],int(r['local_id'])) for r in csvrows(R/'analysis/imports/merged_catalog_5409.csv')}
assert len(oldkeys)==5409 and not set(a)&oldkeys
v120file=R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv'
v120=csvrows(v120file)
metadata=json.loads((R/'review/v120_B_context_new4632/MANIFEST.json').read_text())
assert len(v120)==4632 and filesha(v120file)==metadata['metadata_sha256']
targets=v120[beg:end]
assert len(targets)==end-beg and int(targets[0].get('index',beg))>=0
assert 1<=len(targets)<=320
assert all((row['tile_set_name'],int(row['local_id'])) in a for row in targets)
assert len({(t['tile_set_name'],int(t['local_id'])) for t in targets})==320
assert not oldkeys&{(t['tile_set_name'],int(t['local_id'])) for t in targets}
def mapread(name):
    tree=ET.parse(ROOT/name).getroot()
    ts=sorted((int(x.get('firstgid')),x.get('name')) for x in tree.findall('tileset') if x.get('name'))
    first=[v[0] for v in ts]
    w,h=int(tree.get('width','256')),int(tree.get('height','256'))
    layers=[]
    for ix,ly in enumerate(tree.iter('layer')):
        dat=ly.find('data')
        assert dat is not None and dat.get('encoding')=='csv'
        vals=[int(v) for v in re.findall(r'\d+',dat.text or '')]
        assert len(vals)==w*h
        layers.append(dict(index=ix,level=layerlevel(ly),values=vals))
    return dict(ts=ts,first=first,layers=layers,w=w,h=h)
def resolve(m,raw):
    gid=raw&0x0fffffff
    if not gid:return None
    pos=bisect.bisect_right(m['first'],gid)-1
    if pos<0:return None
    return (m['ts'][pos][1],gid-m['ts'][pos][0])
@lru_cache(maxsize=5)
def atlas(path):
    if not path:return None
    with Image.open(R/path) as im:return im.convert('RGBA')
@lru_cache(maxsize=3200)
def sprite(k):
    rec=a.get(k)
    if rec:
        path=rec['source_image_path'];box=bbox(rec['selected_crop_xyxy'])
        expected=rec['selected_rgba_pixel_sha256']
    else:
        rec=cand.get(k)
        if not rec:return None
        path=rec.get('source_png_path','')
        key=rec.get('new_preferred_A','')
        if key=='A3':box=bbox(rec.get('A3_crop_bbox',''));expected=rec.get('A3_pixel_sha256','')
        elif key in ('A1','A1=A2'):box=bbox(rec.get('A1_bbox',''));expected=rec.get('A1_pixel_sha256','')
        elif key=='A2':box=bbox(rec.get('A2_bbox',''));expected=rec.get('A2_pixel_sha256','')
        else:return None
    if not path or not box or not expected:return None
    src=atlas(path)
    if src is None or box[0]<0 or box[1]<0 or box[2]>src.width or box[3]>src.height:return None
    img=src.crop(box)
    assert sha(img.tobytes())==expected,(k,'old A pixel drift')
    return img if img.getbbox() else None
def flips(img,raw):
    if raw&0x20000000:img=img.transpose(Image.Transpose.TRANSPOSE)
    if raw&0x80000000:img=img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if raw&0x40000000:img=img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return img
W,H=800,580
def scene(m,loc,replacement=None,delete=False):
    x0,y0=int(loc['source_x']),int(loc['source_y'])
    level=int(loc['source_level'])
    layerid=int(loc['source_layer_index'])
    rawtarget=int(loc['source_raw_gid'])
    index=y0*m['w']+x0
    raw=m['layers'][layerid]['values'][index]
    assert raw==rawtarget and resolve(m,raw)==(loc['tile_set_name'],int(loc['local_id']))
    canvas=Image.new('RGBA',(W,H),(237,242,247,255))
    replacement_drawn=0;misses=Counter()
    for layer in m['layers']:
        if layer['level']!=level:continue
        commands=[]
        for dy in range(-2,3):
            y=y0+dy
            if not 0<=y<m['h']:continue
            for dx in range(-2,3):
                x=x0+dx
                if not 0<=x<m['w']:continue
                p=y*m['w']+x;gid=layer['values'][p]
                if gid:commands.append((dx+dy,dy,dx,p,gid))
        commands.sort()
        for _,dy,dx,p,gid in commands:
            istarget=layer['index']==layerid and p==index and gid==rawtarget
            if istarget and delete:
                replacement_drawn+=1
                continue
            if istarget and replacement is not None:
                image=replacement
                replacement_drawn+=1
            else:
                image=sprite(resolve(m,gid))
            if image is None:misses['missing_source']+=1;continue
            image=flips(image,gid)
            px=int(W/2+(dx-dy)*58-image.width/2)
            py=int(H/2+(dx+dy)*29+34-image.height)
            if px<0 or py<0 or px+image.width>W or py+image.height>H:
                clip=(max(0,-px),max(0,-py),min(image.width,W-px),min(image.height,H-py))
                if clip[2]<=clip[0] or clip[3]<=clip[1]:
                    misses['outside_canvas']+=1
                    continue
                image=image.crop(clip);px=max(0,px);py=max(0,py)
            canvas.alpha_composite(image,(px,py))
    if replacement is not None or delete:assert replacement_drawn==1,(loc,replacement_drawn)
    return canvas.convert('RGB'),dict(misses)
def difference(a,b):
    img=ImageChops.difference(a,b).convert('L')
    return sum(px!=0 for px in img.getdata())
def choices(k):
    """Select ONLY a recorded v127 crop candidate, never invent a new source position.
    Adjacent-grid candidates may be OTHER local IDs, so status remains unverified."""
    rec=cand[k]
    original=a[k]
    src=atlas(original['source_image_path'])
    assert src is not None
    seen_original=sha(sprite(k).tobytes())
    valid=[];audit=[]
    for trial in trial_by_key.get(k,[]):
        kind=trial['category']
        if kind not in ('same_key_A_grid','same_basename_atlas_variant',
                        'adjacent_grid_not_same_key'):
            continue
        path=trial['source_path']
        rect=bbox(trial['source_crop'])
        if not path or rect is None:
            continue
        source_atlas=atlas(path)
        assert source_atlas is not None and 0<=rect[0]<rect[2]<=source_atlas.width
        assert 0<=rect[1]<rect[3]<=source_atlas.height
        im=source_atlas.crop(rect)
        digest=sha(im.tobytes())
        assert digest==trial['rgba_sha256']
        assert sum(im.getchannel('A').histogram()[1:])==int(trial['alpha_pixels'])
        assert digest!=seen_original
        item=dict(kind=trial['candidate_id'],grid=kind,box=rect,image=im,
                  sha=digest,alpha=int(trial['alpha_pixels']),
                  trust=('unverified_other_local_ID_risk' if kind=='adjacent_grid_not_same_key'
                         else 'same_basename_unverified'))
        valid.append(item)
        audit.append(dict(candidate=trial['candidate_id'],
                          status='v127_recorded_distinct_visible_candidate',
                          source_grid=kind,bbox=trial['source_crop'],
                          rgba_sha256=digest,alpha_pixels=item['alpha'],
                          confidence=item['trust']))
    valid.sort(key=lambda z:(0 if z['grid']=='same_key_A_grid'
                             else 1 if z['grid']=='same_basename_atlas_variant' else 2,
                             z['kind']))
    return valid,audit


# v127 candidate list is exhaustive over specified atlas-grid hypotheses.
v127manifest=json.loads((R/'review/v127_D_A_candidates_full4633/MANIFEST.json').read_text())
v127file=R/'review/v127_D_A_candidates_full4633/D_ALL_CANDIDATE_TRIALS.csv'
assert filesha(v127file)==v127manifest['all_trials_sha256']
all_v127_trials=csvrows(v127file)
assert len(all_v127_trials)==50955
trial_by_key={}
for t in all_v127_trials:
    if t['result']=='distinct_visible_unverified_correspondence':
        k=(t['tile_set_name'],int(t['local_id']))
        trial_by_key.setdefault(k,[]).append(t)

font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
records=[];trial_rows=[];sheets=[]
evidence=OUT/'D_ALT_A_B_SCENES.zip'
zipout=zipfile.ZipFile(evidence,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4)
cached_name=None;cached_map=None
for offset,row in enumerate(targets):
    i=beg+offset
    k=(row['tile_set_name'],int(row['local_id']))
    assert k in a and k in cand
    name=row['tmx_file']
    if name!=cached_name:
        assert filesha(ROOT/name)==metadata['source_TMX_sha256'][name]
        cached_map=mapread(name);cached_name=name
        sprite.cache_clear();atlas.cache_clear()
    original=sprite(k)
    found,attempts=choices(k)
    for t in attempts:
        trial_rows.append(dict(index=i,tile_set_name=k[0],local_id=k[1],**t))
    loc={**row,'tile_set_name':k[0],'local_id':k[1]}
    B,missB=scene(cached_map,loc)
    C,missC=scene(cached_map,loc,delete=True)
    old_delta=difference(B,C)
    Aalt=None;D=None;chosen=None;missD={}
    if found:
        chosen=found[0]
        Aalt=chosen['image']
        D,missD=scene(cached_map,loc,replacement=Aalt)
    assert D is None or D.size==B.size==C.size
    assert old_delta>=0
    d_delta=difference(D,C) if D is not None else ''
    b_to_d=difference(B,D) if D is not None else ''
    imgs=[('Aoriginal',original),('Aalternative',Aalt),('Boriginal',B),('DaltB',D),('Cremoved',C)]
    for label,img in imgs:
        if img is None:continue
        buf=io.BytesIO()
        if label.startswith('A'):
            img.save(buf,format='PNG')
            suffix='png'
        else:
            img.save(buf,format='WEBP',quality=85,method=3)
            suffix='webp'
        zipout.writestr('%s/%04d_%s.%s'%(label,i,label,suffix),buf.getvalue())
    result=dict(index=i,tile_set_name=k[0],local_id=k[1],
       original_png= a[k]['source_image_path'],original_crop=a[k]['selected_crop_xyxy'],
       original_rgba_sha256=a[k]['selected_rgba_pixel_sha256'],
       alternate_status=('alternative_A_hypothesis_rendered' if chosen else 'held_no_distinct_visible_A_hypothesis'),
       alternate_kind=chosen['kind'] if chosen else '',
       alternate_source_grid=chosen['grid'] if chosen else '',
       alternate_crop=','.join(map(str,chosen['box'])) if chosen else '',
       alternate_rgba_sha256=chosen['sha'] if chosen else '',
       alternate_alpha_pixels=chosen['alpha'] if chosen else 0,
       alternative_candidate_count=len(found),
       alternative_trials=len(attempts),
       original_B_C_changed_pixels=old_delta,
       D_alternate_B_C_changed_pixels=d_delta,
       original_B_to_D_changed_pixels=b_to_d,
       source_tmx=name,source_level=row['source_level'],
       source_layer_index=row['source_layer_index'],
       source_x=row['source_x'],source_y=row['source_y'],
       source_raw_gid=row['source_raw_gid'],
       source_tmx_sha256=metadata['source_TMX_sha256'][name],
       missing_B_json=json.dumps(missB,sort_keys=True),
       missing_D_json=json.dumps(missD,sort_keys=True),
       selected_A_used_only_as_prior_unverified=1,
       correspondence_verified=0,tilezed_verified=0,identity_certified=0,
       human_visual_review_completed=0,
       note='D = v127 recorded candidate A rendered at SAME original B position; neighbors may be DIFFERENT Local IDs. Experimental render only, no certification.')
    records.append(result)
    if offset%40==0:board=Image.new('RGB',(1920,2900),(247,249,250))
    pen=ImageDraw.Draw(board)
    slot=offset%40;xx=(slot%4)*480;yy=(slot//4)*290
    pen.rectangle((xx+1,yy+1,xx+477,yy+287),outline=(133,148,169),fill=(255,255,255))
    pen.text((xx+7,yy+8),'%03d %s/%d D=%s'%(i,k[0][:21],k[1],
           chosen['kind'] if chosen else 'HELD'),font=small,fill=(32,48,62))
    for j,(label,img) in enumerate(imgs):
        cx=xx+5+j*94
        pen.text((cx+2,yy+27),label[:12],font=small,fill=(50,72,91))
        if img is not None:
            thumb=img.copy()
            thumb.thumbnail((90,210))
            board.paste(thumb,(cx+(90-thumb.width)//2,yy+50+(210-thumb.height)//2))
        else:pen.text((cx,yy+120),'NONE',font=small,fill=(180,40,45))
    pen.text((xx+8,yy+269),'B-C %d | alt-C %s | B-D %s'%(old_delta,str(d_delta),str(b_to_d)),font=small,fill=(30,45,66))
    if offset%40==39 or offset==len(targets)-1:
        out=OUT/('ALT_A_B_sheet_%02d.jpg'%(offset//40))
        board.save(out,quality=86,optimize=True)
        sheets.append(out)
    if (offset+1)%40==0:print('GENERATED',offset+1,'/',len(targets),flush=True)
zipout.close()
assert len(records)==len(targets) and len(sheets)==(len(targets)+39)//40
assert len({(r['tile_set_name'],r['local_id']) for r in records})==320
def write_csv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
maincsv=OUT/'D_ALTERNATIVE_A_B.csv'
trials_csv=OUT/'D_CANDIDATE_SEARCH.csv'
# candidate trials may have different optional keys, normalize to a union
allcolumns=list(dict.fromkeys(k for r in trial_rows for k in r))
write_csv(maincsv,records)
with trials_csv.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=allcolumns);w.writeheader();w.writerows(trial_rows)
with zipfile.ZipFile(evidence) as z:
    assert z.testzip() is None
    expected_entries=len(targets)*3 + 2*sum(r['alternate_status']=='alternative_A_hypothesis_rendered' for r in records)
    assert len(z.namelist())==expected_entries,(len(z.namelist()),expected_entries)
rendered=sum(r['alternate_status']=='alternative_A_hypothesis_rendered' for r in records)
held=len(records)-rendered
manifest=dict(version='v131',batch=batch_id,
  corrected_D_definition='different A candidate same tile at SAME B source TMX location',
  source_v120_index_range=[beg,end-1],
  scope_new_only=len(records),D_alternative_rendered=rendered,D_held=held,
  direct_A1_A2_alternatives=sum(r['alternate_source_grid']=='same_key_A_grid' for r in records),
  grid_alignment_hypothesis_alternatives=sum(r['alternate_source_grid']=='adjacent_grid_not_same_key' for r in records),
  other_PNG_variants=sum(r['alternate_source_grid']=='same_basename_atlas_variant' for r in records),
  candidate_trials_recorded=len(trial_rows),no_final_mapping_certifications=1,
  D_scene_archive=evidence.relative_to(R).as_posix(),D_scene_archive_sha256=filesha(evidence),
  evidence_csv=maincsv.relative_to(R).as_posix(),evidence_csv_sha256=filesha(maincsv),
  trials_csv=trials_csv.relative_to(R).as_posix(),trials_csv_sha256=filesha(trials_csv),
  review_sheet_sha256={p.name:filesha(p) for p in sheets},
  correspondence_verified=0,tilezed_verified=0,identity_certified=0,human_visual_review_completed=0,
  B_to_D_changed=sum(r['original_B_to_D_changed_pixels']!='' and int(r['original_B_to_D_changed_pixels'])>0 for r in records),
  B_to_D_unchanged=sum(r['original_B_to_D_changed_pixels']!='' and int(r['original_B_to_D_changed_pixels'])==0 for r in records),
  B_to_C_zero=sum(int(r['original_B_C_changed_pixels'])==0 for r in records),
  caution='Nearby atlas-grid crop may be a DIFFERENT Local ID, not an authenticated alternate for this tile. These are experimental only.')
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'REPORT.md').write_text('# v131 D remaining — batch '+str(batch_id)+
    '\n\nRange '+str(beg)+'..'+str(end-1)+', attempted '+str(len(records))+
    ', experimental rendered '+str(rendered)+', held '+str(held)+
    '. B location reused; pixel source checks and ZIP CRC pass. All mapping/identity certifications 0.\n',encoding='utf8')
print('PASS v131 batch',batch_id, json.dumps(manifest,ensure_ascii=False),flush=True)
