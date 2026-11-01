#!/usr/bin/env python3
"""Render 25 independently identified Decocraft 1.20.1 original BBMODEL/texture candidates.
The script reuses the vetted source downloader, texture sha and desktop Blockbench renderer,
changing only the source model test list and output path.
"""
import runpy
from pathlib import Path
p=Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")
env=runpy.run_path(str(p),run_name="batch06_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/06_051_060/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
  [
    "diner_table_round_black",
    "Dark Round Table",
    ""
  ],
  [
    "bamboo_coffee_table_round_yellow",
    "Dark Round Table",
    ""
  ],
  [
    "wooden_table_ebony",
    "Dark Round Table",
    ""
  ],
  [
    "wooden_table_oak",
    "Table",
    "Large Simple"
  ],
  [
    "wooden_table_birch",
    "Table",
    "Large Simple"
  ],
  [
    "cottage_coffee_table_long",
    "Table",
    "Large Simple"
  ],
  [
    "diner_table_gray",
    "Table",
    "Large Simple"
  ],
  [
    "wooden_table_spruce",
    "Table",
    "Large Simple"
  ],
  [
    "cottage_coffee_table",
    "Low Table",
    "Fancy"
  ],
  [
    "cottage_coffee_table_oval",
    "Low Table",
    "Fancy"
  ],
  [
    "bedside_table_ebony",
    "Low Table",
    "Fancy"
  ],
  [
    "double_bed_oak_white",
    "Bed",
    "Large Oak"
  ],
  [
    "double_bed_birch_white",
    "Bed",
    "Large Oak"
  ],
  [
    "stove",
    "Oven",
    "Modern"
  ],
  [
    "pizza_oven",
    "Oven",
    "Modern"
  ],
  [
    "trash_can",
    "Bin",
    "Wheelie"
  ],
  [
    "pedal_trash_can",
    "Bin",
    "Wheelie"
  ],
  [
    "trash_can_open",
    "Bin",
    "Wheelie"
  ],
  [
    "school_chair_gray",
    "Chair",
    "Grey Plastic"
  ],
  [
    "school_chair_light_gray",
    "Chair",
    "Grey Plastic"
  ],
  [
    "diner_chair_gray",
    "Chair",
    "Grey Plastic"
  ],
  [
    "piano_bench_spruce",
    "Bench",
    "Park"
  ],
  [
    "filing_cabinet_white",
    "Drawers",
    "Fancy"
  ],
  [
    "bedside_table_white",
    "Drawers",
    "Fancy"
  ],
  [
    "modular_desk_drawers_white",
    "Drawers",
    "Fancy"
  ]
]
if __name__=="__main__":
    env["main"]()
