#!/usr/bin/env python3
"""v108 미관찰 99종 중 병행 v109 48키를 제외하고 실제 다른 TMX 사용 위치를 탐색한다. 비계상."""
import bisect, collections, json, sqlite3, subprocess, sys
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={tuple(x) for x in [["furniture_seating_indoor_03",146],["location_community_medical_01",138],["walls_interior_bathroom_01",86],["floors_rugs_01",127],["signs_one-off_09",172],["street_decoration_01",82],["furniture_seating_indoor_03",148],["location_community_medical_01",148],["walls_interior_bathroom_01",107],["floors_rugs_01",128],["signs_one-off_09",173],["street_decoration_01",87],["location_community_medical_01",149],["floors_rugs_01",129],["signs_one-off_09",174],["street_decoration_01",90],["location_community_medical_01",152],["floors_rugs_01",134],["signs_one-off_09",175],["location_community_medical_01",153],["floors_rugs_01",135],["signs_one-off_09",176],["signs_one-off_09",177],["signs_one-off_09",178],["signs_one-off_09",179],["signs_one-off_09",180],["signs_one-off_09",181],["signs_one-off_09",182],["signs_one-off_09",183],["signs_one-off_09",184],["signs_one-off_09",185],["signs_one-off_09",186],["signs_one-off_09",187],["signs_one-off_09",188],["signs_one-off_09",189],["signs_one-off_09",190],["signs_one-off_09",191],["signs_one-off_09",296],["signs_one-off_09",297],["signs_one-off_09",298],["signs_one-off_09",299],["signs_one-off_09",304],["signs_one-off_09",305],["signs_one-off_09",306],["signs_one-off_09",307],["signs_one-off_09",308],["carpentry_02",112],["d_generic_1",22]]}
subprocess.run([sys.executable,str(ROOT/'scripts/restore_unified_v108.py'),'/tmp/pz_v108_D_scan.sqlite'],check=True)
with sqlite3.connect('/tmp/pz_v108_D_scan.sqlite') as c:
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    q={(x,int(y)) for x,y in c.execute('SELECT tile_set_locator,local_id FROM analysis_queue')}
assert len(q)==99 and EXCLUDE<=q,(len(q),len(EXCLUDE),len(EXCLUDE-q))
remaining=q-EXCLUDE
occ=collections.defaultdict(list)
for name in ('31_45.tmx','31_46.tmx'):
    tree=ET.parse(ROOT/'B4220.3_MapExport_256/tmx'/name).getroot()
    tiles=sorted((int(t.attrib['firstgid']),t.attrib['name']) for t in tree.findall('tileset'))
    gids=[x[0] for x in tiles]
    for layer in tree.findall('layer'):
        d=layer.find('data')
        if d is None or d.attrib.get('encoding')!='csv':continue
        vals=[int(v.strip()) for v in d.text.split(',') if v.strip()]
        assert len(vals)==65536
        for i,raw in enumerate(vals):
            gid=raw & 0x1fffffff
            if not gid:continue
            j=bisect.bisect_right(gids,gid)-1
            if j<0:continue
            key=(tiles[j][1],gid-gids[j])
            if key in remaining:
                occ[key].append(dict(tmx=name,level=int(layer.attrib.get('level',0)),
                                     layer=layer.attrib['name'],x=i%256,y=i//256,raw_gid=raw))
records=[]
for key in sorted(remaining):
    positions=occ.get(key,[])
    distinct=list({(p['tmx'],p['level'],p['x'],p['y']) for p in positions})
    records.append(dict(tile_set_locator=key[0],local_id=key[1],placements=len(positions),
                        distinct_sites=len(distinct),has_other_actual_site=len(distinct)>=2,
                        sites=positions[:30]))
result=dict(baseline='v108',source_queue=99,v109_excluded=48,remaining_unique=len(remaining),
            with_other_actual_site=sum(r['has_other_actual_site'] for r in records),
            no_other_site=sum(not r['has_other_actual_site'] for r in records),
            records=records,observed_count_added=0,certified_added=0,
            note='TMX 위치·GID 탐색만. PNG 이미지 A/B/C/D 판독 및 최종 인증 아님.')
out=ROOT/'audits/v110_remaining_D_scan.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS D SCAN', {k:result[k] for k in ('source_queue','v109_excluded','remaining_unique','with_other_actual_site','no_other_site')})
