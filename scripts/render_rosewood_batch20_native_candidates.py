#!/usr/bin/env python3
"""Verify original Decocraft BBMODEL/texture and render candidate viewports in native Blockbench 5.2.2.
Only the 191–200 independent batch. This script does not approve Minecraft placement."""
from pathlib import Path
import runpy
env=runpy.run_path(str(Path(__file__).with_name("render_rosewood_batch03_native_candidates.py")),run_name="batch20_library")
env["main"].__globals__["O"]=env["D"]/"ten_batch_review/20_191_200/extra_decocraft_render"
env["main"].__globals__["TESTS"]=[
 ["jukebox","Jukebox","Oldies"],
 ["bottom_cabinet_2_white","Counter","Motel"],
 ["gym_bench","Contraption","Fitness"],
 ["pool_rack","Stand","Pool Cue"]
]
if __name__=="__main__":env["main"]()
