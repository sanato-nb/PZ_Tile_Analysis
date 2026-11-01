#!/usr/bin/env python3
"""Batch 05: direct original Decocraft BBMODEL rendering in desktop Blockbench 5.2.2.
Only authored source models and original variant source textures; no synthetic props.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch05_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/05_041_050/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
("wall_sink_white","Sink","White Hanging"),
("round_sink_silver","Sink","White"),
("kitchen_sink_silver","Sink","Dark Industrial"),
("kitchen_sink_black","Sink","Dark Industrial"),
("square_sink_silver","Sink","Dark Industrial"),
("crt_tv","Television","ValuTech"),
("tv_old","Television","ValuTech"),
("tv_small","Television","ValuTech"),
("rattan_couch_left_brown","Couch","Blue Rattan"),
("rattan_couch_right_brown","Couch","Blue Rattan"),
("rattan_couch_center_brown","Couch","Blue Rattan"),
("rattan_couch_center_gray","Couch","Blue Rattan"),
("rattan_armchair_brown","Couch","Blue Rattan"),
("cottage_coffee_table","Low Table","Light"),
("cottage_coffee_table_long","Low Table","Light"),
("rattan_coffee_table_brown","Low Table","Light"),
("bamboo_coffee_table_square_yellow","Low Table","Light"),
("china_cabinet_open_white","Shelves","Large Shop"),
("locker_yellow","Locker","Yellow Wall"),
("locker_gray","Locker","Yellow Wall"),
("monitor_1_white","Computer","Desktop"),
("monitor_2_white","Computer","Desktop"),
("spice_rack_white","Shelves","Metal Wall"),
("drying_rack_black","Shelves","Metal Wall")
]
if __name__=="__main__":
    env["main"]()
