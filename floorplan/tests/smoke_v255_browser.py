#!/usr/bin/env python3
"""v255 real Chromium floorplan smoke test: latest 439 metadata, user 68, intact geometry."""
from pathlib import Path
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
R=Path(__file__).resolve().parents[2]
html=R/"floorplan/current/v255_floorplan_latest_user_priority.html"
assert html.exists()
opts=Options()
for flag in ["--headless=new","--no-sandbox","--disable-dev-shm-usage","--window-size=1440,980"]:opts.add_argument(flag)
driver=webdriver.Chrome(options=opts)
try:
 driver.get(html.resolve().as_uri())
 wait=WebDriverWait(driver,90)
 wait.until(lambda d:d.execute_script("return v243Definitions.size===10042 && v255Definitions.size===439"))
 counts=driver.execute_script("""return {
 active:[...v243Definitions.values()].filter(x=>x.active_flag===1).length,
 inactive:[...v243Definitions.values()].filter(x=>x.active_flag===0).length,
 latest:v255Definitions.size,
 user:[...v255Definitions.values()].filter(x=>x.latest_user_choice).length,
 mouse:v255Definitions.get('constructedobjects_01/18'),
 fence:v255Definitions.get('walls_garage_02/23'),
 excluded:getTile('constructedobjects_01',18)._v243.active,
 hasHeld:getTile('constructedobjects_01',18)._v255,
 isPillar:isPillar(getTile('walls_exterior_house_01',35))
 }""")
 assert (counts["active"],counts["inactive"],counts["latest"],counts["user"])==(9587,455,439,68),counts
 assert counts["excluded"] is False and "쥐덫" in counts["mouse"]["latest_visual_candidate_KO"],counts
 assert "난간" in counts["fence"]["latest_visual_candidate_KO"],counts
 assert counts["isPillar"] is True
 inp=driver.find_element(By.ID,"files")
 real=R/"B4220.3_MapExport_256/tmx/31_46.tmx"
 if real.exists():
  inp.send_keys(str(real))
  WebDriverWait(driver,150).until(lambda d:d.execute_script(
    "return !!(model && model.filename==='31_46.tmx' && model.stats.placed>1000)"))
  print("real TMX placed",driver.execute_script("return model.stats.placed"))
 # also test actual inspector metadata on a synthetic tile of a held source
 tmp=Path(tempfile.mkdtemp(prefix="pz-v255-"))
 gid=[0]*25
 gid[2+2*5]=19  # constructedobjects_01 local18 firstgid=1
 synth=tmp/"held_5x5.tmx"
 synth.write_text('<map version="1.10" tiledversion="1.10" orientation="orthogonal" width="5" height="5" tilewidth="32" tileheight="32" infinite="0">'
 '<tileset firstgid="1" name="constructedobjects_01" tilewidth="32" tileheight="32" tilecount="100" columns="10"/>'
 '<layer name="FloorOverlay" width="5" height="5"><data encoding="csv">'+','.join(map(str,gid))+'</data></layer></map>',encoding="utf8")
 driver.execute_script("arguments[0].value=''",inp)
 inp.send_keys(str(synth))
 WebDriverWait(driver,60).until(lambda d:d.execute_script("return !!(model && model.filename==='held_5x5.tmx' && model.stats.placed===1)"))
 driver.execute_script("inspect(2,2)")
 t=driver.find_element(By.ID,"details").text
 assert "쥐덫" in t and "v255" in t and "활성" in t,(t[:1000],counts)
 print("PASS v255: 10042/9587/455, 439 latest visual held, 68 user, no activation; A-first user in inspector")
finally:
 driver.quit()
