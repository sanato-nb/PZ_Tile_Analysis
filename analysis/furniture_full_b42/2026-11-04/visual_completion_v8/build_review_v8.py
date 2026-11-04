"""Rebuild v8 additive review overlay. Does not modify the full source database.
Usage: python build_review_v8.py --repo REPO --output NEW_DIR
Requires Python 3 + Pillow, repository v7 ancestry and its source assets.
"""
import argparse,csv,hashlib,io,json,sqlite3,subprocess
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--output',required=True);p.add_argument('--v7',default='analysis/furniture_full_b42/2026-11-04/alias_policy_v7');a=p.parse_args()
root=Path(a.repo);out=Path(a.output);out.mkdir(parents=True,exist_ok=False)
ref='85c3252fa01d12f4637d44d01430130e9760f785'
def git(path):return subprocess.check_output(['git','-C',str(root),'show',ref+':'+path])
def read_bytes(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'))))
def read(path):return read_bytes(Path(path).read_bytes())
def save(name,rows):
 with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
v6='analysis/furniture_full_b42/2026-11-04/shared_wiki_v6/'
pending=read(Path(a.v7)/'V7_PENDING_VISUAL_REVIEW.csv') if Path(a.v7).exists() else read(root/a.v7/'V7_PENDING_VISUAL_REVIEW.csv')
notes=Path(__file__).with_name('OBSERVATIONS_64_KO.txt').read_text().splitlines()
assert len(notes)==len(pending)==64
src=sqlite3.connect(':memory:');src.deserialize(git(v6+'B42_FURNITURE_ALIASES_V6.sqlite'));src.row_factory=sqlite3.Row
assert src.execute('pragma integrity_check').fetchone()[0]=='ok'
old7=read_bytes(git(v6+'V6_7_SPECIAL_MANUAL_SOURCE_PNG_REVIEWS.csv'))
old58=read_bytes(git('analysis/furniture_full_b42/2026-11-03/full_visual_review_v5/V5_ALL_58_ACTUAL_SOURCE_PNG_GROUP_VISUAL_REVIEWS.csv'))
keys58={r['source_group_id'] for r in old58};keys7={r['source_group'] for r in old7};keys64={r['source_group'] for r in pending}
assert len(keys58)==58 and len(keys7)==7 and len(keys64)==64
assert not(keys58&keys7 or keys58&keys64 or keys7&keys64)
assert keys58|keys7|keys64=={r[0] for r in src.execute('select group_id from v6_all129_source_overlap')}
cache={};reviews=[];proof=[];links=[]
for i,(r,note) in enumerate(zip(pending,notes)):
 gid=r['source_group'];sheet=v6+'ORIGINAL_71_IMAGES/'+r['image_path'].split('/')[-1];image=git(sheet)
 cells=list(src.execute('select * from v6_original_image_cell where group_id=? order by source_key',(gid,)))
 for cell in cells:
  path=cell['png_path']
  if path not in cache:
   b=git(path);cache[path]=(Image.open(io.BytesIO(b)).convert('RGBA'),hashlib.sha256(b).hexdigest())
  im,pngsha=cache[path];x=cell['column_index']*cell['cell_width'];y=cell['row_index']*cell['cell_height'];cw=cell['cell_width'];ch=cell['cell_height']
  assert x>=0 and y>=0 and x+cw<=im.width and y+ch<=im.height
  digest=hashlib.sha256(im.crop((x,y,x+cw,y+ch)).tobytes()).hexdigest();assert digest==cell['pixel_crop_sha256']
  proof.append(dict(source_group=gid,source_key=cell['source_key'],png_path=path,png_sha256=pngsha,crop_x=x,crop_y=y,crop_width=cw,crop_height=ch,rgba_sha256=digest,hash_match=1))
 role='multi_tile_parts_candidate' if i in (28,37,60) else 'surface_tile' if i==40 else 'orientation_pair_candidate' if i==18 else 'single_sprite_object_or_module'
 reviews.append(dict(review_index=i,source_group=gid,wiki_names=r['names'],source_keys='|'.join(c['source_key'] for c in cells),observation_ko=note,visual_role=role,visual_relation='SAME_REFERENCED_SPRITES_ACROSS_CATEGORIES',evidence_scope='existing_v6_source_sprite_contact_sheet',source_sheet=sheet,source_sheet_sha256=hashlib.sha256(image).hexdigest(),source_commit=ref,direct_contact_sheet_reviewed=1,blind_review=0,runtime_identity_verified=0,assembly_verified=0,uncertainty_ko='표시된 스프라이트 형태 비교. 기존 라벨을 본 검수이며 독립 블라인드 검수 아님. 전체 방향 수·실제 조립·게임 객체 동일성은 미검증.',next_test='게임 이동식 가구 연결 규칙 및 실제 배치에서 방향/부품 관계 확인'))
 for link in src.execute('select * from v6_wiki_alias where group_id=?',(gid,)):links.append(dict(link))
assert len(proof)==73 and len(cache)==19
save('V8_NEW_64_VISUAL_REVIEWS.csv',reviews);save('V8_73_ORIGINAL_CROP_PROOFS.csv',proof);save('V8_WIKI_TILE_REFERENCES.csv',links)
coverage=[]
for gid in sorted(keys58|keys7|keys64):coverage.append(dict(source_group=gid,visual_review_record_present=1,review_version='v8' if gid in keys64 else 'v6' if gid in keys7 else 'v5',newly_viewed_this_run=int(gid in keys64),runtime_identity_verified=0))
save('V8_ALL_129_REVIEW_COVERAGE.csv',coverage)
c=sqlite3.connect(out/'V8_VISUAL_REVIEW_OVERLAY.sqlite')
for name,rows in [('v8_visual_group_review',reviews),('v8_source_crop_proof',proof),('v8_wiki_tile_reference',links),('v8_all129_review_coverage',coverage)]:
 cols=list(rows[0]);c.execute('CREATE TABLE '+name+' ('+','.join('"'+k+'" TEXT' for k in cols)+')');c.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in cols)+')',[[r[k] for k in cols] for r in rows])
c.commit();assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
sql='\n'.join(c.iterdump());(out/'V8_VISUAL_REVIEW_OVERLAY.sql').write_text(sql)
d=sqlite3.connect(':memory:');d.executescript(sql)
for name, in c.execute("select name from sqlite_master where type='table'"):
 assert c.execute('select * from '+name).fetchall()==d.execute('select * from '+name).fetchall()
manifest=dict(source_commit=ref,new_visual_groups=64,prior_visual_groups=65,total_reviewed_collision_groups=129,total_collision_groups=129,source_crop_hashes_verified=73,original_png_atlases=19,wiki_tile_references=len(links),source_only_visual_reviewed=0,source_only_groups=963,runtime_identity_verified=0,sqlite_integrity='ok',sql_roundtrip='all rows equal',scope='additive overlay; full v6 database unmodified',files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir()})
(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps(manifest,ensure_ascii=False,indent=2))
