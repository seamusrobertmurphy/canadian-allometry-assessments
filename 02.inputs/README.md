# Data manifest

Every dataset the analysis uses, where it came from, and how to get it back. Each subfolder
carries its own README with the source, licence, download route, column definitions and
gotchas — **read those before using the data**. This file is the index.

| Folder | Dataset | Role | README |
|---|---|---|---|
| `enfor/` | ENFOR destructive biomass, NRCan | tamarack bark mass, n = 439. The national calibration sample, so an in-sample control | [README](enfor/README.md) |
| `legacy-tree/` | LegacyTreeData | western-larch bark mass (n = 13) **and** an independent taper sample (15 western larch, 42 tamarack) | [README](legacy-tree/README.md) |
| `larch/` | National allometric coefficients (Lambert 2005 / Ung 2008) | the equations under test | [README](larch/README.md) |
| `vri/` | BC Vegetation Resources Inventory | 67,409 larch-leading polygons the equations are applied across | [README](vri/README.md) |
| `tallo/` | Tallo global allometry database | **not used**; retained for reference | [README](tallo/README.md) |
| `scripts/` | legacy code | **not used**; the analysis lives in the manuscript | [README](scripts/README.md) |

## Runtime guide

The analysis is in R code inside `01.manuscript/canadian-allometry-forest-science.qmd`. There
are no separate scripts to run — rendering the manuscript runs the pipeline.

| Chunk | Reads |
|---|---|
| `national-coefficients` | `larch/nfi_tree-level_allometric_dbh.csv`, `..._dbh-height.csv` |
| `destructive-data` | `enfor/EnforCanadaBiomassFinalData_v2007-ENG.csv`, `legacy-tree/tree.txt` |
| `taper-data` | `legacy-tree/stem.txt`, `legacy-tree/tree.txt` |
| `inventory`, `comparator` | `vri/vri_larch.csv` |

`stem.txt` is read by one chunk only, which keeps just the breast-height sections.

