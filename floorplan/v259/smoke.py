"""Exercise the standalone file in Chrome with an original, multi-floor B42 map."""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
for argument in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1600,1000"):
    options.add_argument(argument)
with webdriver.Chrome(options=options) as browser:
    browser.get((Path(__file__).resolve().parents[1]/"current/v259_floorplan.html").as_uri())
    wait = WebDriverWait(browser, 90)
    button = browser.find_element(By.ID,"sampleMap")
    wait.until(lambda _: button.is_enabled())
    button.click()
    wait.until(lambda _: browser.execute_script("return indexedModel?.filename === '31_46.tmx'"))
    assert browser.execute_script("return [...model.floors.keys()].sort()") == list(range(7))
    assert browser.execute_script("return model.stats.placed") == 131341
    browser.find_element(By.ID,"fQuery").send_keys("WIKI:PZW-0063")
    browser.find_element(By.CSS_SELECTOR,"#fResults button").click()
    detail = browser.find_element(By.ID,"details").text
    assert "WIKI:PZW-0063" in detail and "clothingwasher" in detail, detail
    assert browser.execute_script("return currentHit===0 && selected!==null")
    browser.find_element(By.ID,"fNext").click()
    assert browser.execute_script("return currentHit === 1 % furnitureLocations.get(selectedCandidate).length")
    assert browser.execute_script("return furnitureCsv('appliances_laundry_01/0')[1].includes('clothingwasher')")
    browser.find_element(By.ID,"fClear").click()
    assert browser.execute_script("return selectedCandidate === ''")
    print("PASS real TMX: 7 levels, 131341 placements, washer search, coordinates, part storage, navigation and CSV fields")
