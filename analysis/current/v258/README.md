# v258 original definition PNG tile catalog

Input: all original Tiles PNG files, seven .tiles in tiledef/tiledef.zip, historical v255 master CSV.

ALL_PNG_GRID_CELLS.csv: one row per PNG grid cell, including transparent cells and unmapped cells.
PNG_FILE_GRID_AUDIT.csv: PNG dimensions, grid sizes, match status.
SOURCE_SLOTS_NOT_LINKED_TO_PNG.csv: original slot records without safe image mapping.
SOURCE_PROPERTY_CONFLICTS.csv: all raw conflicting property values.
V255_KEYS_ABSENT_FROM_TILEDEF.csv: previous map keys without an exact original key.
PZ_v258_all_png_tile_definitions.sqlite: searchable complete source attributes and image cells.
MANIFEST.json: counts and file checks.

Matched name and grid do not establish official sprite/ID certification. Original properties describe game behavior and metadata, not necessarily the exact object or component. Historical user decisions and held statuses are preserved.
