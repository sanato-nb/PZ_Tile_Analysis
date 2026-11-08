# Project Zomboid B42 → Minecraft: 31_46 preview converter

**Status: first real-file preview, NOT a completed reconstruction.**
The source geometry is real. Preview floor materials are provisional family-level
colors, not verified per-sprite identities. Do not merge with a playthrough save.

## Verified original

* TMX: B4220.3_MapExport_256/tmx/31_46.tmx (256×256)
* World: B4220.3_MapExport_256/Kentucky.pzw (native-256, origin 0,0, cell 31,46)
* Global Minecraft bounds: X 7936–8191, Z 11776–12031.
* Level 0 surface Y=64. Dirt Y=63–62; stone Y=61–57.
* Source: 413 tilesets, 22 layers, seven levels with data (0–6).
* 131,341 nonzero source placement records; 65,536 Level 0 Floor cells.

## Run

Requires Python 3.9+ and no external Python packages.

~~~sh
python minecraft_converter/converter.py \
  --tmx B4220.3_MapExport_256/tmx/31_46.tmx \
  --pzw B4220.3_MapExport_256/Kentucky.pzw \
  --v259-html floorplan/current/v259_floorplan.html \
  --output minecraft_converter/output \
  --preview-world --data-version 3465
~~~

DataVersion 3465 = Minecraft Java 1.20.1 **disposable testing target**.
The final game version and mod loader are still undecided.

## Files

* 31_46_preview_world.zip — real Java world directory, level.dat + Anvil region.
* report.json — generation counts and limits.
* source_placements.jsonl.gz — EVERY nonzero GID, layer, floor, position,
  candidate ID and available v259 source properties.
* furniture_parts.json — source-backed furniture/appliance tile PARTS,
  not confirmed complete object instances.
* edges.json — four boundary strips, for future neighboring TMX comparison.
* warnings.csv — unresolved ground identities and ambiguous furniture candidates.

The GitHub Actions workflow pz-minecraft-31-46-preview.yml validates
the original tile counts, 256 chunks, and ZIP contents, then uploads the result.

## Implemented in this preview

Verified global coordinates, original TMX CSV layer parsing, lossless placement
logging, v259 candidate metadata, conservative Level 0 surface preview,
2 dirt + 5 stone below surface, family-whitelisted furniture placeholders,
void world / plains biome / fixed daytime / clear weather / creative mode /
disabled natural mob spawning, and real Java Anvil chunks.

## Still deferred, NOT presented as complete

Original sprite-level material certification; water and underwater geometry;
road textures; trees, farmland and vegetation shapes; verified upper-floor
surfaces and walkable stairs; exact full-model furniture instance matching;
collision model geometry; review-map UI; chunk checkpoints; protected world
replacement; in-game launch verification.

Important: v259 furniture candidates also match farmland plants, vegetation,
doors, windows, and external installations. They must NOT all receive furniture
placeholder blocks. Only source families starting with furniture_, appliances_,
fixtures_counters_, fixtures_bathroom_, or fixtures_sinks_ receive provisional
furniture markers. Every excluded record is still in the source archive.

This work is isolated on branch work/minecraft-31-46-preview-20261108.
Neither original TMX/PZW data nor the v259 source is modified.
