# Data manifest

Every dataset the analysis uses, where it came from, and how to get it back. Four files are
deliberately excluded from git (see `.gitignore`) because they are large and openly
redownloadable; `stem.txt` at 131 MB also exceeds GitHub's 100 MB per-file limit. Restore
them into the paths below and the pipeline runs unchanged.

| Path | Size | In git | Source |
|---|---:|:---:|---|
| `enfor/EnforCanadaBiomassFinalData_v2007-ENG.csv` | 0.9 MB | yes | ENFOR programme, Natural Resources Canada. OGL-Canada. DOI 10.23687/fbad665e-8ac9-4635-9f84-e4fd53a6253c |
| `legacy-tree/stem.txt` | 131 MB | **no** | LegacyTreeData, CC BY. DOI 10.7294/W4VD6WC6 |
| `legacy-tree/tree.txt` | 39 MB | **no** | LegacyTreeData, as above |
| `legacy-tree/location.txt`, `section.txt`, `branch.txt`, `core.txt`, `disk.txt` | < 3 MB each | yes | LegacyTreeData, as above |
| `tallo/Tallo.csv` | 47 MB | **no** | Tallo database (Jucker et al. 2022), CC BY. Not used by the current analysis; retained for reference |
| `vri/vri_larch.csv` | 14 MB | **no** | BC Vegetation Resources Inventory, `WHSE_FOREST_VEGETATION.VEG_COMP_LYR_R1_POLY`, larch-leading polygons. OGL-British Columbia, BC Data Catalogue |
| `larch/`, `scripts/` | small | yes | Derived inputs and the analysis pipeline |

## Which files each stage needs

- **Stage 1** (`stage1_accuracy_refit.py`): `enfor/` CSV and `legacy-tree/tree.txt`.
- **Stage 1b** (`stage1b_bark_geometry.py`): `legacy-tree/stem.txt` and `tree.txt`. This is
  the only stage that needs `stem.txt`, and it reads just the breast-height sections.
- **Stage 2** (`stage2_vri_province.py`) and **Stage 2b** (`stage2b_affleck_comparator.py`):
  `vri/vri_larch.csv`.

## Retrieval notes

LegacyTreeData is distributed as a single archive; extract `stem.txt` and `tree.txt` into
`legacy-tree/`. Both are comma-delimited with a small number of malformed rows, which the
scripts skip with `on_bad_lines="skip"`. Units are imperial (inches, pounds, feet) and are
converted in code.

The VRI extract was pulled from the BC Data Catalogue web feature service filtered to
`SPECIES_CD_1 IN ('LW','LT')`. `stage2_vri_province.py` documents the request; the cached
CSV is a convenience, not a dependency of the method.

## Interpreter

The Python stages need `matplotlib`, `scipy` and `pandas`. On this machine those live under
`/opt/local/bin/python3.13`, not the default `python3` (3.12). The manuscript's setup chunk
calls 3.13 explicitly.
