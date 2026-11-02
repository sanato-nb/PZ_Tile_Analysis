#!/usr/bin/env python3
"""Real Decocraft BBMODEL candidates for B lane 171-180; all judgments provisional."""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch18_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/18_171_180/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "pizza_oven",
    "Oven",
    "Red"
  ],
  [
    "bottom_cabinet_2_white",
    "Wardrobe",
    "White"
  ],
  [
    "diner_chair_blue",
    "Chair",
    "Spiffos Dinner"
  ],
  [
    "dryer",
    "Clothing Dryer",
    "White"
  ],
  [
    "kitchen_sink_silver",
    "Oven",
    "Industrial"
  ],
  [
    "diner_counter_corner_black",
    "Counter",
    "Generic Shop Corner"
  ],
  [
    "bottom_cabinet_2_oak",
    "Counter",
    "Dark"
  ],
  [
    "cottage_armchair",
    "Chair",
    "Red Theatre"
  ],
  [
    "modular_desk_drawers_oak",
    "Drawers",
    "Pale"
  ],
  [
    "top_cabinet_3_oak",
    "Counter",
    "Birchwood Floating"
  ]
]
if __name__=="__main__":env["main"]()
