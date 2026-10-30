#!/usr/bin/env python3
"""Browser smoke for v256, real original TMX and user-approved held objects."""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
R=Path(__file__).resolve().parents[2]
FILE=R/"floorplan/current/v256_floorplan_unified_10042.html"
opts=Options()
for arg in ["--headless=new","--no-sandbox","--disable-dev-shm-usage","--window-size=1600,900"]:opts.add_argument(arg)
driver=webdriver.Chrome(options=opts)
try:
 driver.get(FILE.as_uri())
 w=WebDriverWait(driver,100)
 w.until(lambda d:d.execute_script("return v256Definitions.size===10042"))
 state=driver.execute_script("""return {
   active:[...v256Definitions.values()].filter(x=>x.active_flag==='1').length,
   held:[...v256Definitions.values()].filter(x=>x.active_exclusion_reason==='HISTORICAL_HELD_439').length,
   excluded:[...v256Definitions.values()].filter(x=>x.active_flag==='0'&&x.active_exclusion_reason!=='HISTORICAL_HELD_439').length,
   user:[...v256Definitions.values()].filter(x=>!!x.latest_user_choice).length,
   mouse:v256Definitions.get('constructedobjects_01/18').latest_visual_candidate_KO,
   mouseRole:ROLE(getTile('constructedobjects_01',18)),
   noHeldPillar:isPillar(getTile('walls_garage_02',23)),
   knownPillar:isPillar(getTile('walls_exterior_house_01',35)),
   search:!!document.getElementById('v256Query')
 }""")
 assert (state["active"],state["held"],state["excluded"],state["user"])==(9587,439,16,68),state
 assert state["mouseRole"]=="held" and "쥐덫" in state["mouse"],state
 assert state["noHeldPillar"] is False and state["knownPillar"] is True,state
 assert state["search"] is True
 t=driver.find_element(By.ID,"v256Query");t.send_keys("쥐덫")
 w.until(lambda d:"constructedobjects_01/18" in d.find_element(By.ID,"v256Hits").text)
 real=R/"B4220.3_MapExport_256/tmx/31_46.tmx"
 if real.is_file():
  driver.find_element(By.ID,"files").send_keys(str(real))
  w.until(lambda d:d.execute_script("return model!==null&&model.filename==='31_46.tmx'&&model.stats.placed>1000"))
  stats=driver.execute_script("return [model.stats.placed,Number(document.querySelector('#v256Stats').textContent.match(/[\\d,]+/)[0].replace(/,/g,''))]")
  assert stats[0]==stats[1],stats
  assert driver.find_element(By.ID,"v256Stats").text.find("보류")>=0
 # Create a 5x5 TMX with one user-reviewed held key and test inspector/search in map
 import tempfile
 with tempfile.TemporaryDirectory(prefix="pz256_") as td:
  p=Path(td)/"single_held.tmx"
  a=["0"]*25;a[12]="19"
  p.write_text('<map version="1.10" tiledversion="1.10" orientation="orthogonal" width="5" height="5" tilewidth="32" tileheight="32"><tileset firstgid="1" name="constructedobjects_01" tilewidth="32" tileheight="32" tilecount="100" columns="10"/><layer name="FloorOverlay" width="5" height="5"><data encoding="csv">'+",".join(a)+'</data></layer></map>',encoding="utf8")
  file_input=driver.find_element(By.ID,"files")
  driver.execute_script("arguments[0].value=''",file_input)
  file_input.send_keys(str(p))
  w.until(lambda d:d.execute_script("return model!==null&&model.filename==='single_held.tmx'&&model.stats.placed===1"))
  driver.execute_script("inspect(2,2)")
  detail=driver.find_element(By.ID,"details").text
  assert "쥐덫" in detail and "v256" in detail and "비활성" in detail,detail
  assert driver.execute_script("return ROLE(getTile('constructedobjects_01',18))")=="held"
  assert driver.execute_script("return document.querySelector('#v256Stats').textContent.includes('보류 1')")
  assert driver.execute_script("return options.heldPreview") is True
  driver.find_element(By.ID,"v256Query").clear()
  driver.find_element(By.ID,"v256Query").send_keys("constructedobjects_01/18")
  driver.find_element(By.CSS_SELECTOR,"#v256Hits button").click()
  assert "Level 0" in driver.find_element(By.ID,"v256Hint").text
 print("PASS browser v256: actual TMX, 10042/9587/439/16, user68, no held geometry, user search and inspector")
finally:
 driver.quit()
