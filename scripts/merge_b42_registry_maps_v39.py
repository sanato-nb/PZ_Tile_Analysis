"""Add map presence and reproducible review evidence to the cumulative furniture DB."""
import csv
import hashlib
import json
import shutil
import sqlite3
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT=Path('analysis/furniture_full_b42/2026-11-06')
PACK=ROOT/'geometry_warning_v30/B42_FURNITURE_GEOMETRY_WARNINGS_V30.zip'
OUT=ROOT/'registry_map_v39'


def export(db, name, sql):
    query=db.execute(sql)
    with (OUT/(name+'.csv')).open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow([d[0] for d in query.description])
        w.writerows(query)


def run(db):
    source=defaultdict(dict)
    keys={}
    for key,group,sheet,n in db.execute('select source_key,group_id,tileset,local_id from furniture_tile'):
        assert key==f'{sheet}/{n}' and key not in keys
        keys[key]=group
        source[sheet][int(n)]=key
    assert len(keys)==8219
    by_tile=Counter()
    maps_per_tile=Counter()
    by_group=Counter()
    maps_per_group=Counter()
    coverage=[]
    first_hit={}
    for path in sorted(Path('B4220.3_MapExport_256/tmx').glob('*.tmx')):
        root=ET.parse(path).getroot()
        tilesets=sorted((int(t.attrib['firstgid']),t.attrib['name']) for t in root.findall('tileset'))
        mapping={}
        for i,(start,name) in enumerate(tilesets):
            limit=tilesets[i+1][0] if i+1<len(tilesets) else 2**28
            for local,key in source.get(name,{}).items():
                if start+local<limit:
                    mapping[start+local]=key
        hits=Counter()
        if mapping:
            mask=np.zeros(max(mapping)+2,dtype=bool)
            mask[list(mapping)]=True
            for layer in root.iter('layer'):
                d=layer.find('data')
                assert d.get('encoding')=='csv' and not d.findall('chunk')
                width=int(layer.attrib['width'])
                values=np.fromstring(d.text.strip().rstrip(','),sep=',',dtype=np.uint32)
                assert len(values)==width*int(layer.attrib['height'])
                gids=values&0x0fffffff
                indices=np.flatnonzero(mask[np.minimum(gids,len(mask)-1)])
                if len(indices):
                    unique,first,counts=np.unique(gids[indices],return_counts=True,return_index=True)
                    for g,k,n in zip(unique,first,counts):
                        key=mapping[int(g)]
                        hits[key]+=int(n)
                        if key not in first_hit:
                            idx=int(indices[k])
                            first_hit[key]=(str(path),layer.get('level'),layer.get('name'),idx%width,idx//width)
        by_tile.update(hits)
        maps_per_tile.update(hits.keys())
        group_hits=Counter()
        for k,n in hits.items():
            group_hits[keys[k]]+=n
        by_group.update(group_hits)
        maps_per_group.update(group_hits.keys())
        coverage.append((str(path),len(hits),len(group_hits),sum(hits.values())))
    assert len(coverage)==4914
    db.executescript("""
    CREATE TABLE v39_source_tile_map(source_key TEXT PRIMARY KEY, group_id TEXT, placements INTEGER, maps INTEGER,
        example_map TEXT, level INTEGER, layer TEXT, x INTEGER, y INTEGER);
    CREATE TABLE v39_source_group_map(group_id TEXT PRIMARY KEY, source_keys INTEGER, keys_seen INTEGER, placements INTEGER, maps INTEGER);
    CREATE TABLE v39_maps(path TEXT PRIMARY KEY, unique_source_keys INTEGER, unique_groups INTEGER, placements INTEGER);
    """)
    db.executemany('insert into v39_source_tile_map values(?,?,?,?,?,?,?,?,?)',(
        (k,g,by_tile[k],maps_per_tile[k],*first_hit.get(k,(None,)*5)) for k,g in sorted(keys.items())))
    groups=Counter(keys.values())
    seen=Counter(keys[k] for k in by_tile)
    db.executemany('insert into v39_source_group_map values(?,?,?,?,?)',(
        (g,n,seen[g],by_group[g],maps_per_group[g]) for g,n in sorted(groups.items())))
    db.executemany('insert into v39_maps values(?,?,?,?)',coverage)
    # Preserve the registry distinction between a wiki item and a source group.
    # Only exact, whole field values equal to a group ID are admitted as direct links.
    db.row_factory=sqlite3.Row
    registry=list(db.execute('select * from registry_entry'))
    assert len(registry)==2231
    db.execute('create table v39_registry_progress(registry_row integer primary key, entry_id text, link_fields text, direct_group_ids text, directly_linked_groups_with_map_hits integer, evidence_status text)')
    for i,row in enumerate(registry,1):
        links={k:row[k] for k in row.keys() if isinstance(row[k],str) and row[k] in groups}
        gs=sorted(set(links.values()))
        found=sum(by_group[g]>0 for g in gs)
        status='direct_group_map_presence' if found else ('direct_group_no_map_hit' if gs else 'no_direct_group_field_link')
        db.execute('insert into v39_registry_progress values(?,?,?,?,?,?)',(i,row['entry_id'],json.dumps(links),json.dumps(gs),found,status))
    # The wiki registry stores exact sprite links and group expansions in a bridge table.
    # Separate those evidence types so shared groups cannot inflate direct matches.
    db.executescript("""
    CREATE TABLE v39_candidate_map_status AS
    WITH counts AS (
        SELECT e.entry_id, e.display_name, e.source_system,
               count(t.source_key) AS linked_keys,
               sum(CASE WHEN m.placements>0 AND t.evidence='EXACT_WIKI_IMAGE_SPRITE_KEY' THEN 1 ELSE 0 END) AS exact_wiki_keys_seen,
               sum(CASE WHEN m.placements>0 AND t.evidence='SOURCE_ONLY_TILEDEF_GROUP' THEN 1 ELSE 0 END) AS source_only_keys_seen,
               sum(CASE WHEN m.placements>0 AND t.evidence='SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED' THEN 1 ELSE 0 END) AS expanded_keys_seen
        FROM registry_entry e LEFT JOIN registry_entry_tile t USING(entry_id)
        LEFT JOIN v39_source_tile_map m USING(source_key)
        GROUP BY e.entry_id,e.display_name,e.source_system
    )
    SELECT *, CASE WHEN exact_wiki_keys_seen>0 THEN 'wiki_exact_sprite_seen'
                   WHEN source_only_keys_seen>0 THEN 'source_group_tile_seen'
                   WHEN expanded_keys_seen>0 THEN 'expanded_group_only_seen'
                   WHEN linked_keys>0 THEN 'linked_but_no_map_hit'
                   ELSE 'no_source_tile_link' END AS map_evidence FROM counts;
    CREATE UNIQUE INDEX v39_candidate_map_id ON v39_candidate_map_status(entry_id);
    """)
    assert db.execute("select count(*) from v39_candidate_map_status").fetchone()[0]==2231
    assert db.execute("select count(*) from registry_entry_tile t left join v39_source_tile_map m using(source_key) where m.source_key is null").fetchone()[0]==0
    export(db,"V39_CANDIDATE_MAP_STATUS","select * from v39_candidate_map_status order by entry_id")
    for path in sorted(ROOT.glob('*/*.csv')):
        if path==OUT or path.parent==OUT or not any(path.name.startswith('V'+str(v)+'_') for v in range(31,39)):
            continue
        with path.open(encoding='utf-8-sig') as f:
            reader=csv.reader(f); head=next(reader)
            assert len(head)==len(set(head)) and all('"' not in col for col in head)
            table='evidence_'+path.stem.lower()
            db.execute('create table "'+table+'" ('+','.join('"'+col+'" TEXT' for col in head)+')')
            db.executemany('insert into "'+table+'" values('+','.join('?' for col in head)+')',reader)
    for tab in ['source_tile_map','source_group_map','registry_progress','maps']:
        export(db,'V39_'+tab.upper(),'select * from v39_'+tab)
    assert sum(by_tile.values())==sum(by_group.values())==sum(x[-1] for x in coverage)
    manifest={'map_files':len(coverage),'map_files_with_hits':sum(x[-1]>0 for x in coverage),'placements':sum(by_tile.values()),
        'source_keys':len(keys),'source_keys_seen':len(by_tile),'source_groups':len(groups),'source_groups_seen':len(by_group),
        'registry_columns':registry[0].keys(),'registry_status_counts':dict(db.execute('select evidence_status,count(*) from v39_registry_progress group by evidence_status')),
        'candidate_map_counts':dict(db.execute('select map_evidence,count(*) from v39_candidate_map_status group by map_evidence')), 'registry_rows':len(registry),'imported_evidence_tables':db.execute("select count(*) from sqlite_master where type='table' and name like 'evidence_%'").fetchone()[0]}
    db.commit()
    assert db.execute('pragma integrity_check').fetchone()[0]=='ok' and not db.execute('pragma foreign_key_check').fetchall()
    with (OUT/'MANIFEST.json').open('w') as f:
        json.dump(manifest,f,ensure_ascii=False,indent=2)


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'B42_FURNITURE_V39.sqlite'
        with zipfile.ZipFile(PACK) as z:
            name,=[n for n in z.namelist() if n.endswith('.sqlite')]
            with z.open(name) as a,p.open('wb') as b:
                shutil.copyfileobj(a,b)
        db=sqlite3.connect(p)
        run(db)
        db.close()
        dest=OUT/'B42_FURNITURE_V39.zip'
        with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            z.write(p,p.name)
        with zipfile.ZipFile(dest) as z:
            assert z.testzip() is None
