#!/usr/bin/env python3
"""Headless Chrome smoke test of the real v243 legacy-engine+v240 database integration."""
from pathlib import Path
import tempfile,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

ROOT=Path(__file__).resolve().parents[2]
html=ROOT/"floorplan/current/v243_floorplan_v240_priority.html"
assert html.exists()
tmp=Path(tempfile.mkdtemp(prefix="pz-v243-"))
gid=[0]*25
gid[2+2*5]=9              # advertising_01 local 8, firstgid 1
gid[3+3*5]=235            # walls_exterior_house_01 local 35, firstgid 200
tmx=tmp/"smoke_floorplan_5x5.tmx"
tmx.write_text(
'<map version="1.10" tiledversion="1.10" orientation="orthogonal" renderorder="right-down" width="5" height="5" tilewidth="32" tileheight="32" infinite="0">'
'<tileset firstgid="1" name="advertising_01" tilewidth="32" tileheight="32" tilecount="100" columns="10"/>'
'<tileset firstgid="200" name="walls_exterior_house_01" tilewidth="32" tileheight="32" tilecount="100" columns="10"/>'
'<layer name="FloorOverlay" width="5" height="5"><data encoding="csv">'+','.join(map(str,gid))+'</data></layer>'
'</map>',encoding="utf8")
opts=Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1440,980")
driver=webdriver.Chrome(options=opts)
try:
    driver.get(html.resolve().as_uri())
    wait=WebDriverWait(driver,45)
    wait.until(lambda d:d.execute_script("return v243Definitions.size") == 10042)
    a=driver.execute_script("""return getTile('advertising_01',8)._v243""")
    assert a["active"] is True and "광고판" in (a["A_visible_shape_note"]+a["object_identity_candidate"]),a
    assert driver.execute_script("return isPillar(getTile('walls_exterior_house_01',35))") is True
    assert driver.execute_script("return v243Definitions.size") == 10042
    assert driver.execute_script("return Array.from(v243Definitions.values()).filter(x=>x.active_flag===0).length") == 455
    assert driver.execute_script("return Array.from(v243Definitions.values()).filter(x=>x.active_flag===1).length") == 9587
    legacy=driver.execute_script("""const [sheet,tiles]=Object.entries(catalog.tilesets).find(([s,v])=>Object.keys(v).some(id=>!v243Definitions.has(s+'/'+id)));const id=Object.keys(tiles).find(i=>!v243Definitions.has(sheet+'/'+i));return {sheet,id,ok:!!getTile(sheet,Number(id))}""")
    assert legacy["ok"],legacy
    driver.find_element(By.ID,"files").send_keys(str(tmx))
    wait.until(lambda d:d.execute_script("return model && model.stats.placed === 2"))
    assert driver.execute_script("return model.layers.length") == 1
    assert driver.execute_script("return model.stats.missing") == 0
    driver.execute_script("inspect(2,2)")
    info=driver.find_element(By.ID,"details").text
    assert "v240" in info and "광고판" in info and "A 외형" in info,info[:700]
    driver.execute_script("inspect(3,3)")
    info2=driver.find_element(By.ID,"details").text
    assert "기둥" in info2,info2[:700]
    # Exercise one real B42 256x256 TMX file, not only a synthetic example.
    real=ROOT/"B4220.3_MapExport_256/tmx/31_46.tmx"
    if real.exists():
        inp=driver.find_element(By.ID,"files")
        driver.execute_script("arguments[0].value=''",inp)
        inp.send_keys(str(real))
        WebDriverWait(driver,150).until(lambda d:d.execute_script("return model && model.filename==='31_46.tmx' && model.stats.placed>1000"))
        realCount=driver.execute_script("return model.stats.placed")
        realFloors=driver.execute_script("return model.floors.size")
        assert realCount>1000 and realFloors>=1,(realCount,realFloors)
        print("PASS 31_46 real original TMX parsed:",realCount,"GID placements;",realFloors,"floors")
    driver.save_screenshot(str(tmp/"v243_smoke_browser.png"))
    print("PASS headless Chrome actual TMX 2 tiles, A-first overrides, pillar correction, legacy fallback and 10042/9587/455.")
finally:
    driver.quit()
