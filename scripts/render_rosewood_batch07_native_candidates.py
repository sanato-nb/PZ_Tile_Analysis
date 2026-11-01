#!/usr/bin/env python3
"""Batch 07: authentic Decocraft source BBMODEL 1.20.1 textures and Blockbench 5.2.2 screenshots.
No source file is modified; every visible model is from source, and comparison is not game-certified.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch07_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/07_061_070/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "closet_3_oak",
    "Wardrobe",
    "Oak"
  ],
  [
    "closet_5_oak",
    "Wardrobe",
    "Oak"
  ],
  [
    "closet_6_oak",
    "Wardrobe",
    "Oak"
  ],
  [
    "closet_1_oak",
    "Wardrobe",
    "Oak"
  ],
  [
    "rattan_armchair_brown",
    "Chair",
    "Blue Rattan"
  ],
  [
    "rattan_armchair_gray",
    "Chair",
    "Blue Rattan"
  ],
  [
    "rattan_armchair_light_gray",
    "Chair",
    "Blue Rattan"
  ],
  [
    "bedside_table_oak",
    "Drawers",
    "Light Wood"
  ],
  [
    "bedside_table_birch",
    "Drawers",
    "Light Wood"
  ],
  [
    "modular_desk_drawers_oak",
    "Drawers",
    "Light Wood"
  ],
  [
    "diner_counter_corner_light_gray",
    "Counter",
    "Steel Corner"
  ],
  [
    "diner_counter_corner_gray",
    "Counter",
    "Steel Corner"
  ],
  [
    "bottom_cabinet_corner_outer_1_white",
    "Counter",
    "Steel Corner"
  ],
  [
    "china_cabinet_open_oak",
    "Shelves",
    "Big Wall"
  ],
  [
    "spice_rack_oak",
    "Shelves",
    "Big Wall"
  ],
  [
    "decobench",
    "Bench",
    "Fancy Outdoors"
  ],
  [
    "rattan_couch_left_brown",
    "Bench",
    "Fancy Outdoors"
  ],
  [
    "cottage_coffee_table",
    "Low Table",
    "Brown"
  ],
  [
    "bedside_table_open_2_ebony",
    "Low Table",
    "Brown"
  ],
  [
    "bedside_table_open_1_oak",
    "Low Table",
    "Brown"
  ],
  [
    "chair_1_cherry",
    "Chair",
    "Red Wooden"
  ],
  [
    "chair_2_cherry",
    "Chair",
    "Red Wooden"
  ],
  [
    "school_chair_red",
    "Chair",
    "Red Wooden"
  ],
  [
    "wooden_table_birch",
    "Table",
    "Large Light Oak"
  ],
  [
    "wooden_table_oak",
    "Table",
    "Large Light Oak"
  ],
  [
    "cottage_coffee_table_long",
    "Table",
    "Large Light Oak"
  ],
  [
    "toilet_white",
    "Toilet",
    "Hanging"
  ]
]
if __name__=="__main__": env["main"]()
