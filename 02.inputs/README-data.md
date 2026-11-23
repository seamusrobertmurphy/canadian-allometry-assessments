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

## Files excluded from git

Four files are deliberately untracked (see `.gitignore`) because they are large and openly
redownloadable. `stem.txt` at 132 MB also exceeds GitHub's 100 MB per-file hard limit.
Restore them to the paths below and the pipeline runs unchanged.

| Path | Size | Get it from |
|---|---:|---|
| `legacy-tree/stem.txt` | 132 MB | LegacyTreeData, DOI 10.7294/W4VD6WC6 |
| `legacy-tree/tree.txt` | 40 MB | LegacyTreeData, as above |
| `vri/vri_larch.csv` | 15 MB | BC Data Catalogue WFS, filtered `SPECIES_CD_1 IN ('LW','LT')` |
| `tallo/Tallo.csv` | 47 MB | Zenodo, DOI 10.5281/zenodo.6637599 — not needed to reproduce anything |

Everything else in `02.inputs/` is tracked, including the ENFOR CSV, the coefficient tables,
the smaller LegacyTreeData tables and all metadata.

## What reads what

The analysis is R code inside `01.manuscript/canadian-allometry-forest-science.qmd`. There
are no separate scripts to run — rendering the manuscript runs the pipeline.

| Chunk | Reads |
|---|---|
| `national-coefficients` | `larch/nfi_tree-level_allometric_dbh.csv`, `..._dbh-height.csv` |
| `destructive-data` | `enfor/EnforCanadaBiomassFinalData_v2007-ENG.csv`, `legacy-tree/tree.txt` |
| `taper-data` | `legacy-tree/stem.txt`, `legacy-tree/tree.txt` |
| `inventory`, `comparator` | `vri/vri_larch.csv` |

`stem.txt` is read by one chunk only, which keeps just the breast-height sections.

## Licences

All open: ENFOR and the national coefficients under the Open Government Licence – Canada;
LegacyTreeData and Tallo under CC BY; the VRI under the Open Government Licence – British
Columbia. No confidential or third-party project data are used.

## Requirements

R 4.4.1 with `knitr`. Base R and `stats` only — no other package, no Python, no network
access at render time. Every input above is cached locally.
