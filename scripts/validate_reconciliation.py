#!/usr/bin/env python3
"""Audit restored source SQLite databases and the v47 merged output."""
from pathlib import Path
import sqlite3,csv,json,sys
root=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]) if len(sys.argv)>1 else root/'restored_sources'
a=sqlite3.connect(src/'tile_visual_v36.sqlite')
b=sqlite3.connect(src/'tile_visual_v46.sqlite')
assert a.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert b.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
A={(x,int(y)) for x,y in a.execute('select tile_set_locator,local_id from v36_full_scope where v36_visual_review_any=1')}
B=set()
for version in (37,38,39,41,42,43,44,45,46):
 B|={(x,int(y)) for x,y in b.execute(f'select tile_set,local_id from v{version}_evidence')}
assert (len(A),len(B),len(A&B),len(A|B))==(2509,477,402,2584)
with (root/'analysis/imports/merged_catalog_5409.csv').open(encoding='utf-8-sig',newline='') as f:
 rows=list(csv.DictReader(f))
assert len(rows)==5409
assert sum(int(row['observed_any']) for row in rows)==2584
assert sum(int(row['provisional_candidate_any_auditable']) for row in rows)==2302
s=json.loads((root/'PROJECT_STATE.json').read_text('utf8'))
assert s['reconciliation']['merged_unique_observed']==2584
print('PASS v36/v46 original sources and merged catalog: 5409 scoped, 2584 observed, overlap 402')
