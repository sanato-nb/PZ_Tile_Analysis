#!/usr/bin/env python3
"""Batch 09: 28 authentic Decocraft JAR BBMODEL+PNG models opened in Blockbench 5.2.2,
compared with actual complete PZ furniture images (not game-world verification).
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch09_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/09_081_090/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "cottage_coffee_table_oval",
    "Table",
    "Fancy Low Glass"
  ],
  [
    "rattan_coffee_table_brown",
    "Table",
    "Fancy Low Glass"
  ],
  [
    "cottage_coffee_table_long",
    "Table",
    "Fancy Low Glass"
  ],
  [
    "bamboo_coffee_table_round_yellow",
    "Oak Round Table",
    ""
  ],
  [
    "diner_table_round_black",
    "Oak Round Table",
    ""
  ],
  [
    "wooden_table_oak",
    "Oak Round Table",
    ""
  ],
  [
    "closet_2_birch",
    "Wardrobe",
    "Light Wood"
  ],
  [
    "closet_4_birch",
    "Wardrobe",
    "Light Wood"
  ],
  [
    "closet_6_birch",
    "Wardrobe",
    "Light Wood"
  ],
  [
    "closet_3_birch",
    "Wardrobe",
    "Light Wood"
  ],
  [
    "bottom_cabinet_corner_inner_birch",
    "Counter",
    "Birchwood Corner"
  ],
  [
    "bottom_cabinet_corner_outer_1_birch",
    "Counter",
    "Birchwood Corner"
  ],
  [
    "bottom_cabinet_corner_outer_2_birch",
    "Counter",
    "Birchwood Corner"
  ],
  [
    "wooden_table_ebony",
    "Table",
    "Large Brown"
  ],
  [
    "wooden_table_spruce",
    "Table",
    "Large Brown"
  ],
  [
    "cottage_coffee_table",
    "Fancy Table",
    ""
  ],
  [
    "wooden_table_black",
    "Fancy Table",
    ""
  ],
  [
    "bedside_table_ebony",
    "Fancy Table",
    ""
  ],
  [
    "diner_table_light_gray",
    "Table",
    "Large Smooth"
  ],
  [
    "wooden_table_white",
    "Table",
    "Large Smooth"
  ],
  [
    "diner_table_black",
    "Table",
    "Large Smooth"
  ],
  [
    "washer",
    "Combo Washer Dryer",
    "Blue"
  ],
  [
    "dryer",
    "Combo Washer Dryer",
    "Blue"
  ],
  [
    "tv_old",
    "Antenna",
    "Old TV"
  ],
  [
    "double_bed_spruce_white",
    "Bed",
    "Large Modern"
  ],
  [
    "double_bed_black_white",
    "Bed",
    "Large Modern"
  ],
  [
    "double_bed_oak_white",
    "Bed",
    "Large Modern"
  ],
  [
    "double_bed_spruce_light_gray",
    "Bed",
    "Large Modern"
  ]
]
if __name__=="__main__":env["main"]()
