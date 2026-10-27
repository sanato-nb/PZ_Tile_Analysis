#!/usr/bin/env python3
"""v131: merge all v131 batch evidence and previous D, preserve complete v130 SQLite."""
import csv,json,hashlib,zipfile,sqlite3,base64,zlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
O=R/'review/v131_D_remaining_3832'
DB=R/'analysis/current/v131';DB.mkdir(parents=True,exist_ok=True)
def hashfile(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for q in iter(lambda:f.read(1048576),b''):h.update(q)
 return h.hexdigest()
def h(x):return hashlib.sha256(x).hexdigest()
def read(p):
 with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def save(p,arr):
 assert arr
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)
ranges=[(0,320)]+[(v,min(v+320,4632)) for v in range(1120,4632,320)]
assert len(ranges)==12 and sum(end-beg for beg,end in ranges)==3832
new=[];batches=[];total_trials=0
for beg,end in ranges:
 folder=O/('batch_%04d_%04d'%(beg,end-1))
 m=json.loads((folder/'MANIFEST.json').read_text('utf8'))
 assert m['source_v120_index_range']==[beg,end-1] and m['scope_new_only']==end-beg
 assert m['D_alternative_rendered']+m['D_held']==end-beg
 assert m['A_mapping_certified']==m['TileZed_certified']==m['identity_certified']==0
 assert m['B_D_changed']+m['B_D_unchanged']==m['D_alternative_rendered']
 data=read(folder/m['evidence_csv'])
 assert len(data)==end-beg and [int(x['index']) for x in data]==list(range(beg,end))
 assert hashfile(folder/m['evidence_csv'])==m['evidence_csv_sha256']
 assert hashfile(folder/m['trial_csv'])==m['trial_csv_sha256']
 assert len(read(folder/m['trial_csv']))==m['candidate_trials_recorded']
 archive=folder/m['zip_path']
 assert hashfile(archive)==m['zip_sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==m['zip_entries']
  assert m['zip_entries']==(end-beg)*3+m['D_alternative_rendered']*2
 for sheet,sha in m['review_sheet_sha256'].items():assert hashfile(folder/sheet)==sha
 for x in data:
  assert all(x[k]=='0' for k in ('correspondence_verified','tilezed_verified','identity_certified','human_visual_review_completed'))
  assert x['alternate_source_grid'] in ('adjacent_grid_not_same_key','same_basename_atlas_variant','same_key_A_grid','')
  x['source_folder']=folder.relative_to(R).as_posix()
 new+=data
 batches.append(dict(range=[beg,end-1],rendered=m['D_alternative_rendered'],held=m['D_held'],
                     changed=m['B_D_changed'],crc='PASS',manifest=(folder/'MANIFEST.json').relative_to(R).as_posix()))
 total_trials+=m['candidate_trials_recorded']
assert len(new)==3832 and len({int(x['index']) for x in new})==3832
new.sort(key=lambda x:int(x['index']))
newcsv=O/'D_NEW_REMAINING_3832.csv';save(newcsv,new)
completed={}
for key,path,lo,hi in [
 ('v126','review/v126_D_alt_A_B_160/D_ALTERNATIVE_A_B_160.csv',320,480),
 ('v129','review/v129_D_alt_A_B_320/D_ALTERNATIVE_A_B_320.csv',480,800),
 ('v130','review/v130_D_alt_A_B_320/D_ALTERNATIVE_A_B_320.csv',800,1120)]:
 r=read(R/path)
 assert len(r)==hi-lo and sorted(int(x['index']) for x in r)==list(range(lo,hi))
 for item in r:
  i=int(item['index']);assert i not in completed
  item['source_folder']='review/'+{'v126':'v126_D_alt_A_B_160','v129':'v129_D_alt_A_B_320','v130':'v130_D_alt_A_B_320'}[key]
  completed[i]=item
for item in new:
 i=int(item['index']);assert i not in completed
 completed[i]=item
assert len(completed)==4632 and set(completed)==set(range(4632))
v120=read(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')
assert len(v120)==4632
counts=Counter();full=[]
for i,b in enumerate(v120):
 x=completed[i]
 assert (b['tile_set_name'],int(b['local_id']))==(x['tile_set_name'],int(x['local_id']))
 made=x['alternate_status']=='alternative_A_hypothesis_rendered'
 counts['rendered' if made else 'held']+=1
 if made:
  counts['BD_changed' if int(x['original_B_to_D_changed_pixels'])>0 else 'BD_zero']+=1
  k=x['alternate_source_grid']
  if k in ('adjacent_grid_probe','adjacent_grid_not_same_key'):counts['neighbor']+=1
  elif k=='same_basename_atlas_variant':counts['same_basename']+=1
  elif k=='same_key_A_grid':counts['same_key']+=1
  else:raise AssertionError((i,k))
 counts['BC_zero']+=int(int(x['original_B_C_changed_pixels'])==0)
 full.append(dict(tileset=b['tile_set_name'],local_id=int(b['local_id']),index=i,
      status=x['alternate_status'],candidate_type=x['alternate_source_grid'],
      candidate_source=x['alternate_kind'],source_tmx=x['source_tmx'],
      source_level=int(x['source_level']),source_layer=int(x['source_layer_index']),
      x=int(x['source_x']),y=int(x['source_y']),raw_gid=int(x['source_raw_gid']),
      original_A_sha=x['original_rgba_sha256'],alternative_A_sha=x['alternate_rgba_sha256'],
      BC_diff=int(x['original_B_C_changed_pixels']),
      BD_diff=int(x['original_B_to_D_changed_pixels']) if made else '',
      evidence_folder=x['source_folder'],
      mapping_verified=0,tilezed_verified=0,final_certified=0,
      caution='May be completely different Local ID. Experimental D only.'))
a=read(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
missing=[r for r in a if r['selection_status']!='selected_provisional']
assert len(a)==4633 and len(missing)==1
assert (missing[0]['tile_set_name'],missing[0]['local_id'])==('overlay_graffiti_wall_02','2')
full.append(dict(tileset='overlay_graffiti_wall_02',local_id=2,index='',
    status='held_no_exact_A_source_PNG',candidate_type='',candidate_source='',
    source_tmx='',source_level='',source_layer='',x='',y='',raw_gid='',
    original_A_sha='',alternative_A_sha='',BC_diff='',BD_diff='',
    evidence_folder='review/v118_A_new_only_4633',mapping_verified=0,
    tilezed_verified=0,final_certified=0,caution='Missing A source, not transparent-certified.'))
assert len(full)==4633 and counts['rendered']+counts['held']==4632
assert counts['rendered']==counts['BD_changed']+counts['BD_zero']
overview=O/'D_FULL_SCOPE_4633_STATUS.csv';save(overview,full)
heldrows=[r for r in full if r['status']!='alternative_A_hypothesis_rendered']
save(O/'D_ALL_HELD.csv',heldrows)

parent=json.loads((R/'analysis/current/v130/MANIFEST.json').read_text('utf8'))
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert h(packed)==parent['compressed_sha256']
original=zlib.decompress(packed);assert h(original)==parent['sqlite_sha256']
path=Path('/tmp/PZ_v131_full.sqlite');path.write_bytes(original)
with sqlite3.connect(path) as db:
 tables=[r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
 assert len(tables)==192 and db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 before={t:db.execute('SELECT count(*) FROM "'+t+'"').fetchone()[0] for t in tables}
 db.execute("""CREATE TABLE v131_D_full_4633 (
 tileset TEXT, local_id INTEGER, original_index INTEGER, status TEXT,
 candidate_type TEXT, candidate_source TEXT, source_tmx TEXT,
 level INTEGER, layer INTEGER, x INTEGER, y INTEGER, raw_gid INTEGER,
 original_A_SHA TEXT, alternative_A_SHA TEXT, BC_diff INTEGER, BD_diff INTEGER,
 evidence_folder TEXT, mapping_verified INTEGER DEFAULT 0,
 tilezed_verified INTEGER DEFAULT 0, final_certified INTEGER DEFAULT 0,
 PRIMARY KEY(tileset,local_id))""")
 def ni(v):return int(v) if str(v).strip() else None
 vals=[(x['tileset'],x['local_id'],ni(x['index']),x['status'],x['candidate_type'],
        x['candidate_source'],x['source_tmx'],ni(x['source_level']),ni(x['source_layer']),
        ni(x['x']),ni(x['y']),ni(x['raw_gid']),x['original_A_sha'],x['alternative_A_sha'],
        ni(x['BC_diff']),ni(x['BD_diff']),x['evidence_folder'],0,0,0) for x in full]
 db.executemany('INSERT INTO v131_D_full_4633 VALUES ('+','.join(['?']*20)+')',vals)
 db.commit()
 assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert len(list(db.execute("SELECT name FROM sqlite_master WHERE type='table'")))==193
 assert all(db.execute('SELECT count(*) FROM "'+t+'"').fetchone()[0]==n for t,n in before.items())
 assert db.execute('SELECT count(*) FROM v131_D_full_4633').fetchone()[0]==4633
 assert db.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
 assert db.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
raw=path.read_bytes();compressed=zlib.compress(raw,8)
data=base64.b64encode(compressed).decode('ascii')
parts=[]
for i in range(0,len(data),3000000):
 p=DB/('v131.part%03d.b64'%(i//3000000))
 p.write_text(data[i:i+3000000],'ascii');parts.append(p.relative_to(R).as_posix())
assert h(zlib.decompress(base64.b64decode(''.join((R/q).read_text('ascii') for q in parts))))==h(raw)
dbm=dict(version='v131',parent='v130',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=h(raw),sqlite_bytes=len(raw),compressed_sha256=h(compressed),
 parts=parts,prior_tables_preserved=192,table_count=193,
 new_table='v131_D_full_4633',new_rows=4633,integrity_check='ok',
 official_same_key_A_mapping_verified=0,tilezed_verified=0,identity_final_certified=0)
(DB/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
manifest=dict(version='v131',D_definition='alternative A rerender at SAME original B TMX location',
 full_scope_10042=10042,old_5409_not_rerun=True,
 new_scope_4633=4633,A_available_4632=4632,A_missing_1=1,
 new_3832_batches=12,new_3832_rows=3832,prior_D_800_rows=800,
 full_target_4632_status_indexed=4632,
 D_experimental_rendered=counts['rendered'],D_held_with_A=counts['held'],
 D_all_held_including_missing_A=len(heldrows),
 grid_neighbor_hypotheses_rendered=counts['neighbor'],
 different_basename_source_PNG_rendered=counts['same_basename'],
 B_D_changed=counts['BD_changed'],B_D_zero=counts['BD_zero'],B_C_zero=counts['BC_zero'],
 candidate_trials_in_new_batches=total_trials,
 new_results_csv=newcsv.relative_to(R).as_posix(),new_results_sha256=hashfile(newcsv),
 full_status_csv=overview.relative_to(R).as_posix(),full_status_sha256=hashfile(overview),
 batches=batches,zip_CRC_all_pass=True,physical_DB=DB/'MANIFEST.json' if False else 'analysis/current/v131/MANIFEST.json',
 sqlite_sha256=h(raw),db_tables=193,
 official_same_key_A_mapping_verified=0,tilezed_verified=0,identity_final_certified=0,
 new_individual_AI_visual_reviews=0,
 warning='Gridded neighbor crops are OTHER Local ID risks. Completed experimental D coverage is NOT correct alternate A mapping.')
(O/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'README.md').write_text('# v131 full new-only D experiment\n\n'+
 'All 4633 new keys have a status in D_FULL_SCOPE_4633_STATUS.csv. Source A missing: 1.\n'+
 '12 parallel worker folders preserve selected A, alternate A, B, C, D and source SHA evidence for 3832 targets.\n'+
 'Previous 800 targets use v126/v129/v130 images. Alternative neighbor-grid images are NOT verified same Local ID.\n'+
 'All prior 192 physical SQLite tables preserved and new 4633-status table added. Certifications: 0.\n',encoding='utf8')
print('PASS v131 all',dict(counts),'SQLite',h(raw),'held',len(heldrows),flush=True)
