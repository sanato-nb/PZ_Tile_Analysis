#!/usr/bin/env python3
"""Audit v6 CSV evidence; never infer runtime identity or new visual inspection."""
import argparse, csv, hashlib, json, re, sqlite3
from collections import Counter, defaultdict
from pathlib import Path

BASE_COMMIT = '85c3252fa01d12f4637d44d01430130e9760f785'
FILES = ['V6_71_GROUP_RESULTS.csv', 'V6_178_WIKI_TO_TILE_REFERENCES.csv',
         'V6_ALIAS_KEYSET_CLUSTERS.csv', 'V6_146_WIKI_FUNCTION_PROPERTIES.csv',
         'V6_7_SPECIAL_MANUAL_SOURCE_PNG_REVIEWS.csv']

def read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def save(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

def normalized(name):
    return re.sub(r'\s+\(variant\s+\d+\)$', '', name, flags=re.I).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    groups, links, clusters, props, prior = [read(args.input / n) for n in FILES]
    assert list(map(len, (groups, links, clusters, props, prior))) == [71,178,73,146,7]
    gmap = {r['group_id']: r for r in groups}
    pmap = {r['wiki_id']: r for r in props}
    by_wiki = defaultdict(list)
    for row in links: by_wiki[row['wiki_id']].append(row)
    assert set(by_wiki) == set(pmap) and len(pmap) == 146
    assert len({r['original_sprite_id'] for r in links}) == 89
    assert len({(r['wiki_id'],r['original_sprite_id']) for r in links}) == 178
    prior_ids = {r['source_group'] for r in prior}
    assert len(prior_ids) == 7 and prior_ids <= set(gmap)
    policies, fields, memberships = [], [], []
    seen = set()
    for cluster in clusters:
        cid, gid = cluster['alias_cluster'], cluster['source_group']
        ids = cluster['wiki_ids'].split('|')
        keys = set(cluster['exact_original_sprite_set'].split('|'))
        assert len(ids) == 2 and not seen.intersection(ids)
        seen.update(ids)
        for wid in ids:
            refs = by_wiki[wid]
            assert {r['original_sprite_id'] for r in refs} == keys
            assert {r['alias_cluster'] for r in refs} == {cid}
            assert {r['source_group'] for r in refs} == {gid}
            assert pmap[wid]['source_group'] == gid
        rows = [pmap[i] for i in ids]
        names = {normalized(r['original_name']) for r in rows}
        conflict_fields = []
        pending_fields = []
        for field in ('wiki_capacity_raw','wiki_size_raw','wiki_encumbrance_raw',
                      'wiki_crafting_surface_raw','wiki_bed_quality_raw'):
            values = sorted({r[field] for r in rows if r[field] != ''})
            state = ('CONFLICT' if len(values)>1 else 'NOT_RECORDED' if not values
                     else 'PARTIAL_RECORD' if any(r[field]=='' for r in rows) else 'AGREEMENT')
            if state == 'CONFLICT': conflict_fields.append(field)
            pending_fields.append(dict(alias_cluster=cid,field=field,state=state,
                recorded_values_json=json.dumps(values,ensure_ascii=False),
                wiki_evidence_json=json.dumps([{ 'wiki_id':r['wiki_id'], 'value':r[field],
                    'article':r['wiki_article']} for r in rows],ensure_ascii=False)))
        if conflict_fields or gmap[gid]['classification']=='WIKI_NAME_TYPE_CONFLICT_PRIORITY':
            status='CONFLICT_KEEP_SEPARATE'
        elif len(names)==1: status='SAME_NAME_EXACT_KEYSET'
        elif gmap[gid]['classification']=='CROSS_CATEGORY_DRYING_RACK_ALIAS':
            status='DIFFERENT_NAME_EXACT_KEYSET'
        else: status='NAME_REVIEW_REQUIRED'
        blocked = status in ('CONFLICT_KEEP_SEPARATE','NAME_REVIEW_REQUIRED')
        policies.append(dict(alias_cluster=cid,source_group=gid,names=cluster['names'],
            wiki_ids=cluster['wiki_ids'],exact_original_sprite_set=cluster['exact_original_sprite_set'],
            policy=status,combined_listing_view_allowed=int(not blocked),
            conflict_fields='|'.join(conflict_fields),runtime_identity_verified=0,
            new_visual_review=0,prior_v6_visual_review=int(gid in prior_ids)))
        for r in pending_fields:
            r['usable_listing_value'] = (json.loads(r['recorded_values_json'])[0]
                if not blocked and r['state'] in ('AGREEMENT','PARTIAL_RECORD') else '')
            r['value_scope']='WIKI_LISTING_ONLY_NOT_TILEDEF_OR_RUNTIME'
            fields.append(r)
        for wid in ids:
            memberships.append(dict(alias_cluster=cid,wiki_id=wid,
                query_identity=wid if blocked else cid,policy=status))
    assert seen == set(pmap)
    # Tile attributes stay per original key; never sum container capacities across pieces.
    for key in {r['original_sprite_id'] for r in links}:
        related=[r for r in links if r['original_sprite_id']==key]
        for field in ('source_container','source_capacity','source_Facing','source_SpriteGridPos'):
            assert len({r[field] for r in related}) == 1, (key,field)
    queue=[dict(source_group=g['group_id'],names=g['wiki_names'],
                image_path='../shared_wiki_v6/'+g['original_source_png_contact_sheet'],
                status='NOT_NEWLY_VIEWED',required_action='Open original source image and record visible shape separately from name')
           for g in groups if g['group_id'] not in prior_ids]
    assert len(queue)==64
    out=args.output; out.mkdir(parents=True,exist_ok=True)
    tables={'v7_alias_policy':policies,'v7_field_resolution':fields,
            'v7_listing_membership':memberships,'v7_pending_visual_review':queue,
            'v7_preserved_wiki_properties':props,'v7_preserved_tile_references':links}
    db_path=out/'ALIAS_POLICY_OVERLAY_V7.sqlite'
    assert not db_path.exists(), 'Refuse overwriting existing output database'
    db=sqlite3.connect(db_path)
    for table, rows in tables.items():
        columns=list(rows[0])
        db.execute('CREATE TABLE '+table+' ('+','.join('"'+c+'" TEXT' for c in columns)+')')
        db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in columns)+')',
                       [tuple(r[c] for c in columns) for r in rows])
        save(out/(table.upper()+'.csv'),rows)
    db.executescript('''
    CREATE UNIQUE INDEX v7_alias_id ON v7_alias_policy(alias_cluster);
    CREATE UNIQUE INDEX v7_field_id ON v7_field_resolution(alias_cluster,field);
    CREATE UNIQUE INDEX v7_wiki_id ON v7_listing_membership(wiki_id);
    CREATE VIEW v7_queryable_listing_properties AS
      SELECT m.query_identity,p.* FROM v7_listing_membership m
      JOIN v7_preserved_wiki_properties p USING(wiki_id);
    ''')
    db.commit()
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    # SQL is an independently restorable text artifact, also safe to add to a copied v6 DB.
    sql='\n'.join(db.iterdump())+'\n'
    (out/'ALIAS_POLICY_OVERLAY_V7.sql').write_text(sql,encoding='utf-8')
    restored=sqlite3.connect(':memory:');restored.executescript(sql)
    for table, rows in tables.items():
        assert restored.execute('SELECT * FROM '+table).fetchall()==db.execute('SELECT * FROM '+table).fetchall()
    restored.close();db.close()
    counts=dict(Counter(r['policy'] for r in policies))
    manifest=dict(base_commit=BASE_COMMIT,source_files={n:hashlib.sha256((args.input/n).read_bytes()).hexdigest() for n in FILES},
        audited_groups=71,audited_clusters=73,preserved_wiki_rows=146,preserved_tile_references=178,
        policies=counts,field_states=dict(Counter(r['state'] for r in fields)),
        conflict_fields=[r for r in fields if r['state']=='CONFLICT'],
        query_identities=len({r['query_identity'] for r in memberships}),
        pending_visual_groups=64,new_visual_reviews=0,inherited_reported_visual_groups=65,
        runtime_identity_certified=0,full_v6_database_modified=False,
        sqlite_integrity='ok',sql_roundtrip='ok')
    (out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('source_files','conflict_fields')},ensure_ascii=False))

if __name__=='__main__': main()
