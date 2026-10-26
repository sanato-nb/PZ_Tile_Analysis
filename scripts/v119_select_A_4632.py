#!/usr/bin/env python3
"""v119: physically assign and export one source-pixel-exact representative A for all
4,632 NEW B42 TMX keys that have a visible A1/A2/A3 crop; keep the 1 no-PNG key held.

This is an auditable *provisional image assignment*, not a declaration that these
Local IDs were AI-confirmed or authoritatively TileZed-aligned.
Source imagery is never altered; v116/v117/v118 are read-only. Raw RGBA tile crops
are archived into independent indexed ZIP shards, with SHA-256 provenance.
"""
from pathlib import Path
from collections import Counter
from PIL import Image,ImageDraw,ImageFont
import csv,hashlib,io,json,math,os,zipfile
R=Path(__file__).resolve().parents[1]
V118=R/'review/v118_A_new_only_4633'
V117=R/'review/v117_A_candidates_10042'
OUT=R/'review/v119_selected_A_new4633'
SHEETS=OUT/'sheets'
SHARDS=OUT/'selected_png_shards'
for d in (OUT,SHEETS,SHARDS):d.mkdir(parents=True,exist_ok=True)
def sha(data):return hashlib.sha256(data).hexdigest()
def filehash(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for blk in iter(lambda:f.read(1024*1024),b''):h.update(blk)
    return h.hexdigest()
def readcsv(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def I(s):return int(s or 0)
base=json.loads((V118/'SUMMARY.json').read_text('utf8'))
p=V118/'A_CANDIDATE_NEW_ONLY_4633.csv'
assert filehash(p)==base['master_new_only_sha256'], 'input master changed'
rows=readcsv(p)
assert len(rows)==4633 and len({(r['tile_set_name'],r['local_id']) for r in rows})==4633
assert all(r['prior_in_5409']=='0' and r['user_excluded']=='0' for r in rows)
a3csv=readcsv(V117/'jumbo_a3/A3_CANDIDATES.csv')
a3={(x['tile_set_name'],str(I(x['local_id']))):x for x in a3csv}
assert len(a3)==36
# SHA for exact PNG source, never accept accidental matching basename from a different folder.
pnghashes={}
fontp='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
small=ImageFont.truetype(fontp,10)
font=ImageFont.truetype(fontp,13)
BOARD_W=1920;BOARD_H=1650
board=Image.new('RGB',(BOARD_W,BOARD_H),(233,240,246))
draw=ImageDraw.Draw(board)
def place_preview(im,index,label,id,choice,quality):
    global board,draw
    n=index%80
    if n==0:
        board=Image.new('RGB',(BOARD_W,BOARD_H),(233,240,246))
        draw=ImageDraw.Draw(board)
    x=(n%8)*240;y=(n//8)*165
    draw.rectangle((x+2,y+2,x+237,y+163),fill=(255,255,255),outline=(153,166,175),width=1)
    draw.text((x+8,y+9),f'{index:05d} {label[:26]}',font=small,fill=(20,35,48))
    draw.text((x+8,y+27),f'Local ID {id} | {choice} | {quality[:10]}',font=small,
              fill=(24,104,81) if choice in ('A1=A2','A1','A2') else (155,93,34))
    bg=Image.new('RGB',(224,94),(239,242,246))
    dd=ImageDraw.Draw(bg)
    for xx in range(0,224,16):
        for yy in range(0,94,16):
            if (xx//16+yy//16)%2==0:dd.rectangle((xx,yy,xx+15,yy+15),fill=(223,226,230))
    if im is None:
        dd.text((44,38),'NO EXACT PNG',font=font,fill=(154,44,44))
    else:
        thumb=im.copy();thumb.thumbnail((216,89),Image.Resampling.LANCZOS)
        bg.paste(thumb,((224-thumb.width)//2,(94-thumb.height)//2),thumb)
    board.paste(bg,(x+8,y+46))
    draw.text((x+8,y+145),'Provisional A - Local ID not certified',font=small,fill=(98,89,66))
    if n==79 or index==len(rows)-1:
        num=index//80
        board.save(SHEETS/f'SELECTED_A_{num:03d}.jpg',quality=87,optimize=True)
def geometry(s):
    if not s:return None
    parts=[int(v.strip()) for v in s.split(',')]
    assert len(parts)==4 and parts[2]>parts[0] and parts[3]>parts[1]
    return parts
COLS=['tile_set_name','local_id','representative_A','selection_status','selection_reason',
      'source_image_path','source_png_sha256','selected_rgba_pixel_sha256',
      'selected_png_file_sha256','selected_alpha_pixels','selected_alpha_bbox',
      'selected_crop_xyxy','selected_size','selected_shard','selected_zip_entry',
      'original_v118_sheet','original_v118_sheet_cell',
      'source_A1_status','source_A2_status','source_A1_alpha_pixels','source_A2_alpha_pixels',
      'candidate_decision_v118','is_jumbo_geometry_guess',
      'local_id_mapping_verified','tilezed_verified','ai_independently_verified',
      'final_identity_certified','confidence_class','review_note']
selected=[]
counts=Counter()
ZIP_CAP=500
current_zip=None;open_shard=-1
image_cache_path=None;image_cache=None
def get_source(path,expect):
    global image_cache,image_cache_path
    if path!=image_cache_path:
        image_cache=None
        pp=R/path
        assert pp.is_file(),pp
        if path not in pnghashes:
            pnghashes[path]=filehash(pp)
        assert pnghashes[path]==expect,(path,pnghashes[path],expect)
        with Image.open(pp) as src:
            image_cache=src.convert('RGBA')
        image_cache_path=path
    return image_cache
for i,r in enumerate(rows):
    name=r['tile_set_name'];lid=I(r['local_id'])
    proposal=r['new_preferred_A'];stage=r['new_candidate_decision']
    srcpath=r['source_png_path'];alpha=None;img=None;crop=None
    if proposal=='A1=A2' and stage=='proposed_consistent':
        assert r['A1_A2_identical']=='1'
        assert I(r['A1_alpha_pixels'])==I(r['A2_alpha_pixels'])>0
        assert r['A1_pixel_sha256']==r['A2_pixel_sha256']
        selectedName='A1';reason='identical_visible_A1_A2_pixel_sha256'
        confidence='two_grid_agreement_provisional'
        crop=geometry(r['A1_bbox'])
        pixel_hash=r['A1_pixel_sha256'];alpha=I(r['A1_alpha_pixels'])
    elif proposal in ('A1','A2') and stage=='proposed_one_visible_needs_ai':
        index=proposal
        assert I(r[index+'_alpha_pixels'])>0
        assert I(r[('A2' if index=='A1' else 'A1')+'_alpha_pixels'])==0
        assert r[index+'_status']=='ok'
        selectedName=index
        reason='sole_nontransparent_source_crop'
        confidence='single_grid_only_needs_local_id_check'
        crop=geometry(r[index+'_bbox'])
        pixel_hash=r[index+'_pixel_sha256'];alpha=I(r[index+'_alpha_pixels'])
    elif proposal=='A3' and stage=='proposed_jumbo_whole_sprite_grid_needs_ai':
        assert (name,str(lid)) in a3
        proof=a3[name,str(lid)]
        selectedName='A3'
        reason='provisional_jumbo_whole_sprite_atlas_grid'
        confidence='low_jumbo_alignment_and_neighbor_overlap_possible'
        crop=[int(v) for v in proof['crop_bbox'].strip('[]').split(',')]
        assert len(crop)==4
        pixel_hash=proof['pixels_sha256']
        alpha=I(proof['visible_alpha_pixels'])
        assert alpha>0
        assert r['A3_pixel_sha256']==pixel_hash
        assert r['A3_source_png_path']==srcpath
    else:
        assert stage=='no_usable_source' and proposal=='UNDECIDED',(name,lid,proposal,stage)
        selectedName='NONE'
        reason='exact_png_source_missing'
        confidence='unresolved_missing_exact_source'
        assert not srcpath
    shard=entry=img_hash=''
    if selectedName!='NONE':
        assert srcpath and r['source_png_sha256']
        baseimg=get_source(srcpath,r['source_png_sha256'])
        assert crop and 0<=crop[0]<crop[2]<=baseimg.width and 0<=crop[1]<crop[3]<=baseimg.height
        img=baseimg.crop(tuple(crop))
        assert img.getbbox() is not None,(name,lid)
        assert sha(img.tobytes())==pixel_hash,(name,lid,selectedName,'pixel SHA mismatch')
        assert sum(img.getchannel('A').histogram()[1:])==alpha,(name,lid,'alpha mismatch')
        idx=counts['selected']
        shardNo=idx//ZIP_CAP
        if shardNo!=open_shard:
            if current_zip:current_zip.close()
            path=SHARDS/f'PZ_REP_A_{shardNo:02d}.zip'
            current_zip=zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3)
            open_shard=shardNo
        entry=f'A_{i:05d}_{lid:04d}.png'
        buf=io.BytesIO()
        img.save(buf,format='PNG',compress_level=5)
        b=buf.getvalue()
        img_hash=sha(b)
        current_zip.writestr(entry,b)
        shard=f'selected_png_shards/PZ_REP_A_{open_shard:02d}.zip'
        counts['selected']+=1
        counts[selectedName]+=1
    else:
        counts['held']+=1
    place_preview(img,i,name,lid,selectedName,confidence)
    selected.append(dict(
        tile_set_name=name,local_id=lid,representative_A=selectedName,
        selection_status='selected_provisional' if img else 'held_missing_source',
        selection_reason=reason,source_image_path=srcpath,
        source_png_sha256=r['source_png_sha256'],
        selected_rgba_pixel_sha256=pixel_hash if img else '',
        selected_png_file_sha256=img_hash,
        selected_alpha_pixels=alpha if img else 0,
        selected_alpha_bbox=str(list(img.getchannel('A').getbbox())) if img else '',
        selected_crop_xyxy=','.join(map(str,crop)) if crop else '',
        selected_size=f'{img.width}x{img.height}' if img else '',
        selected_shard=shard,selected_zip_entry=entry,
        original_v118_sheet=r['new_sheet'],original_v118_sheet_cell=r['new_sheet_cell'],
        source_A1_status=r['A1_status'],source_A2_status=r['A2_status'],
        source_A1_alpha_pixels=I(r['A1_alpha_pixels']),
        source_A2_alpha_pixels=I(r['A2_alpha_pixels']),
        candidate_decision_v118=stage,
        is_jumbo_geometry_guess=int(selectedName=='A3'),
        local_id_mapping_verified=0,tilezed_verified=0,ai_independently_verified=0,
        final_identity_certified=0,confidence_class=confidence,
        review_note=('JUMBO crop may include neighbor sprites; must compare TMX/TileZed before use' if selectedName=='A3'
          else 'Grid equality proves source pixels agree, not authoritative tile ID mapping' if selectedName=='A1'
          else 'Only one visible source crop; A-to-GID association still needs contextual verification' if img
          else 'PNG exact filename absent; not transparent-certified')
    ))
    if (i+1)%500==0:print('SELECTED',i+1,'/',len(rows),'counts',dict(counts),flush=True)
if current_zip:current_zip.close()
assert len(selected)==4633 and counts['selected']==4632 and counts['held']==1
assert counts['A1']==1544 and counts['A2']+counts['A1']+counts['A3']==4632
assert counts['A3']==20
assert len({(r['tile_set_name'],r['local_id']) for r in selected})==4633
assert len(list(SHEETS.glob('SELECTED_A_*.jpg')))==58
assert len(list(SHARDS.glob('PZ_REP_A_*.zip')))==10
shard_reports=[]
for f in sorted(SHARDS.glob('PZ_REP_A_*.zip')):
    with zipfile.ZipFile(f) as z:
        bad=z.testzip()
        assert bad is None,(f,bad)
        count=len(z.namelist())
        assert 1<=count<=ZIP_CAP,(f,count)
    shard_reports.append(dict(path=f.relative_to(R).as_posix(),
      sha256=filehash(f),entries=count,bytes=f.stat().st_size,crc='PASS'))
assert sum(x['entries'] for x in shard_reports)==4632
ledger=OUT/'REPRESENTATIVE_A_4633.csv'
with ledger.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS);w.writeheader();w.writerows(selected)
held=OUT/'HELD_A_1.csv'
with held.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS);w.writeheader()
    w.writerows(x for x in selected if x['selection_status']=='held_missing_source')
assert sum(1 for x in selected if x['selection_status']=='held_missing_source')==1
manifest=dict(version='v119',kind='physically_selected_provisional_A_crops',date='2026-10-26',
  source_scope='v118_new_only_4633',
  raw_v118_csv_sha256=base['master_new_only_sha256'],
  source_range_10042=10042,
  existing_reused_excluded_from_new_assignment=5409,
  new_keys_total=4633,
  representative_A_selected=4632,
  held_missing_source=1,
  selected_A1_consistent=counts['A1'],selected_A2=counts['A2'],selected_A3=counts['A3'],
  unique_source_png_files=len(pnghashes),
  selected_images_transparent_background_preserved=True,
  selected_contact_sheet_count=58,
  png_archive_shards=shard_reports,
  selected_ledger=ledger.relative_to(R).as_posix(),
  selected_ledger_sha256=filehash(ledger),
  held_csv=held.relative_to(R).as_posix(),
  source_png_sha256=pnghashes,
  user_prior_excluded_still=14,
  AI_per_tile_visual_mapping_verified=0,
  local_id_mapping_verified=0,tilezed_verified=0,final_identity_certified=0,
  caution='All 4632 A representatives are provisional SOURCE IMAGE ASSIGNMENTS with pixel SHA verified, NOT individually AI/TileZed-certified Local ID mappings; 20 JUMBO A3 could include neighbor sprite frames, require geometric/manual review. Missing 1 not transparent-certified.')
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v119 4632 pixel-exact A source representatives, 1 held, 58 contact sheets, ZIP-shard CRC PASS',
      {k:manifest[k] for k in ('representative_A_selected','held_missing_source','selected_A1_consistent',
      'selected_A2','selected_A3','unique_source_png_files','selected_contact_sheet_count')},flush=True)
