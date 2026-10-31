#!/usr/bin/env python3
"""v257 physical integration, preserving v255, using GitHub repository .tiles.
This intentionally does not claim to contain the seven binaries from the separately uploaded tiledef.zip.
"""
from pathlib import Path
import base64,hashlib,json,shutil,sqlite3,struct,subprocess,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/current/v257'
PARENT_SHA='25df5bcd9ef1f332bc1178ae711ec09f43e070bbf8cc3c33b4e822a0a1766791'
def sha(b):return hashlib.sha256(b).hexdigest()
def tiledefs(path):
 data=path.read_bytes()
 if data[:4]!=b'tdef':raise ValueError('bad tdef header in '+str(path))
 ver,count=struct.unpack_from('<II',data,4);p=12
 def line():
  nonlocal p
  j=data.index(b'\n',p);v=data[p:j].decode('utf-8');p=j+1;return v
 for _ in range(count):
  name=line();img=line();w,h,tid,n=struct.unpack_from('<IIII',data,p);p+=16
  if not(0<w<256 and 0<h<256 and 0<n<100000):raise ValueError('bad tileset '+name)
  yield ('set',name,img,w,h,tid,n)
  for i in range(n):
   k,=struct.unpack_from('<I',data,p);p+=4
   if k>1000:raise ValueError('invalid property count')
   yield ('tile',name,i,k)
   for _ in range(k):yield ('property',name,i,line(),line())
 if p!=len(data):raise ValueError('binary has trailing data')
def snapshot(c):
 rows=c.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
 return {n:(sql,c.execute('SELECT COUNT(*) FROM "'+n.replace('"','""')+'"').fetchone()[0]) for n,sql in rows}
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 parent=OUT/'__temp_parent_v255.sqlite';output=OUT/'__temp_merged_v257.sqlite'
 if parent.exists() or output.exists():raise SystemExit('refusing overwrite of temporary files')
 subprocess.run([sys.executable,'scripts/restore_v255_master.py',str(parent)],cwd=ROOT,check=True)
 if sha(parent.read_bytes())!=PARENT_SHA:raise ValueError('v255 parent SHA mismatch')
 original=sqlite3.connect(parent);before=snapshot(original)
 assert len(before)==260 and original.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 original.close();shutil.copy2(parent,output)
 c=sqlite3.connect(output)
 c.executescript("""
CREATE TABLE v257_source_file(path TEXT PRIMARY KEY,sha256 TEXT,bytes INTEGER,summary_json TEXT);
CREATE TABLE v257_source_tileset(path TEXT,tileset TEXT,image_filename TEXT,width INTEGER,height INTEGER,tileset_id INTEGER,slots INTEGER,PRIMARY KEY(path,tileset));
CREATE TABLE v257_source_tile(path TEXT,tileset TEXT,local_id INTEGER,property_count INTEGER,PRIMARY KEY(path,tileset,local_id));
CREATE TABLE v257_source_property(path TEXT,tileset TEXT,local_id INTEGER,key TEXT,value TEXT,PRIMARY KEY(path,tileset,local_id,key));
CREATE INDEX idx_v257_tile_property ON v257_source_property(tileset,local_id,key);
CREATE TABLE v257_10042_official_match(source_key TEXT PRIMARY KEY,tile_set_name TEXT,local_id INTEGER,
 main_exists INTEGER,legacy_exists INTEGER,main_property_count INTEGER,custom_name TEXT,group_name TEXT,facing TEXT,
 sprite_grid_pos TEXT,container_type TEXT,container_capacity TEXT,material TEXT,solid TEXT,wall_n TEXT,wall_w TEXT,
 mapping_certified INTEGER NOT NULL DEFAULT 0 CHECK(mapping_certified=0),
 identity_certified INTEGER NOT NULL DEFAULT 0 CHECK(identity_certified=0));
CREATE TABLE v257_merge_receipt(key TEXT PRIMARY KEY,value TEXT);
""")
 for src in ['Tiles/newtiledefinitions.tiles','Tiles/tiledefinitions.tiles']:
  path=ROOT/src;raw=path.read_bytes();sets=[];tiles=[];props=[]
  for rec in tiledefs(path):
   if rec[0]=='set':sets.append((src,)+rec[1:])
   elif rec[0]=='tile':tiles.append((src,)+rec[1:])
   else:props.append((src,)+rec[1:])
  c.executemany('INSERT INTO v257_source_tileset VALUES (?,?,?,?,?,?,?)',sets)
  c.executemany('INSERT INTO v257_source_tile VALUES (?,?,?,?)',tiles)
  c.executemany('INSERT INTO v257_source_property VALUES (?,?,?,?,?)',props)
  c.execute('INSERT INTO v257_source_file VALUES(?,?,?,?)',(src,sha(raw),len(raw),
    json.dumps({'tilesets':len(sets),'slots':len(tiles),'properties':len(props)},ensure_ascii=False)))
  print('parsed',src,len(sets),len(tiles),len(props),flush=True)
 c.execute("""INSERT INTO v257_10042_official_match
 SELECT m.source_key,m.tile_set_name,m.local_id,
 EXISTS(SELECT 1 FROM v257_source_tile t WHERE t.path='Tiles/newtiledefinitions.tiles' AND t.tileset=m.tile_set_name AND t.local_id=m.local_id),
 EXISTS(SELECT 1 FROM v257_source_tile t WHERE t.path='Tiles/tiledefinitions.tiles' AND t.tileset=m.tile_set_name AND t.local_id=m.local_id),
 (SELECT property_count FROM v257_source_tile t WHERE t.path='Tiles/newtiledefinitions.tiles' AND t.tileset=m.tile_set_name AND t.local_id=m.local_id),
 MAX(CASE WHEN p.key='CustomName' THEN p.value END),
 MAX(CASE WHEN p.key='GroupName' THEN p.value END),
 MAX(CASE WHEN p.key='Facing' THEN p.value END),
 MAX(CASE WHEN p.key='SpriteGridPos' THEN p.value END),
 MAX(CASE WHEN p.key='container' THEN p.value END),
 MAX(CASE WHEN p.key='ContainerCapacity' THEN p.value END),
 MAX(CASE WHEN p.key='Material' THEN p.value END),
 MAX(CASE WHEN p.key='solid' THEN p.value END),
 MAX(CASE WHEN p.key='WallN' THEN p.value END),
 MAX(CASE WHEN p.key='WallW' THEN p.value END),0,0
 FROM v255_latest_preferred_10042 m
 LEFT JOIN v257_source_property p ON p.path='Tiles/newtiledefinitions.tiles' AND p.tileset=m.tile_set_name AND p.local_id=m.local_id
 GROUP BY m.source_key""")
 c.execute("""CREATE VIEW v257_master_10042 AS
 SELECT m.*,d.main_exists AS v257_main_slot_exists,d.legacy_exists AS v257_legacy_slot_exists,
 d.custom_name AS v257_original_custom_name,d.group_name AS v257_original_group_name,
 d.facing AS v257_original_facing,d.sprite_grid_pos AS v257_original_sprite_grid_pos,
 d.container_type AS v257_original_container,d.container_capacity AS v257_original_capacity,
 d.material AS v257_original_material,
 d.mapping_certified AS v257_mapping_certified,d.identity_certified AS v257_identity_certified
 FROM v255_latest_preferred_10042 m LEFT JOIN v257_10042_official_match d ON m.source_key=d.source_key""")
 facts={
 'stage':'PHYSICAL_V255_MERGED_WITH_REPO_MAIN_AND_LEGACY_TILEDEFS',
 'base_sha256':PARENT_SHA,'prior_table_count':260,
 'v255_keys':c.execute('SELECT COUNT(*) FROM v255_latest_preferred_10042').fetchone()[0],
 'v257_keys':c.execute('SELECT COUNT(*) FROM v257_master_10042').fetchone()[0],
 'match_main':c.execute('SELECT COUNT(*) FROM v257_10042_official_match WHERE main_exists=1').fetchone()[0],
 'match_legacy':c.execute('SELECT COUNT(*) FROM v257_10042_official_match WHERE legacy_exists=1').fetchone()[0],
 'has_grid_pos':c.execute('SELECT COUNT(*) FROM v257_10042_official_match WHERE sprite_grid_pos IS NOT NULL').fetchone()[0],
 'has_container':c.execute('SELECT COUNT(*) FROM v257_10042_official_match WHERE container_type IS NOT NULL').fetchone()[0],
 'held439':c.execute('SELECT COUNT(*) FROM v255_latest_held439').fetchone()[0],
 'user68':c.execute('SELECT COUNT(*) FROM v255_user68_manual_verdict').fetchone()[0],
 'active':c.execute('SELECT COUNT(*) FROM v240_active_tile_master').fetchone()[0],
 'inactive':c.execute('SELECT COUNT(*) FROM v240_excluded_archive_455').fetchone()[0],
 'uploaded_zip_7_binaries_included':False,
 'remaining_work':'Must separately apply all seven binaries from user tiledef.zip; current repository has two .tiles files only.',
 'certified_source_to_png_mapping':0,'certified_new_identity':0
 }
 assert facts['v255_keys']==facts['v257_keys']==10042 and facts['user68']==68 and facts['held439']==439
 c.executemany('INSERT INTO v257_merge_receipt VALUES(?,?)',[(k,json.dumps(v,ensure_ascii=False)) for k,v in facts.items()])
 c.commit();after=snapshot(c)
 assert all(after.get(k)==v for k,v in before.items()),'historical table modified'
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 c.close()
 data=output.read_bytes();packed=zlib.compress(data,6);enc=base64.b64encode(packed).decode('ascii')
 parts=[]
 for i,off in enumerate(range(0,len(enc),3000000)):
  name='v257.part%03d.b64'%i; (OUT/name).write_text(enc[off:off+3000000]+'\n','ascii');parts.append('analysis/current/v257/'+name)
 manifest={'version':'v257_repository_tiles_stage','parent_v255_sha256':PARENT_SHA,
  'merged_sqlite_sha256':sha(data),'merged_sqlite_bytes':len(data),
  'compressed_sha256':sha(packed),'parts':parts,'facts':facts}
 (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),'utf-8')
 (OUT/'REPORT.md').write_text('# v257 physical merge of v255 + GitHub .tiles\n\n'+
  'This branch preserves all 260 v255 tables and 10,042 keys, adds repo main and legacy tile-definition properties.\n\n'+
  '**Not yet a full merge of the separately uploaded seven-binary tiledef.zip.**\n\n'+
  '\x60\x60\x60json\n'+json.dumps(facts,indent=2,ensure_ascii=False)+'\n\x60\x60\x60\n','utf8')
 parent.unlink();output.unlink()
 print('PASS v257 physically merged; original 260 tables retained; parts',len(parts),flush=True)
if __name__=='__main__':main()
