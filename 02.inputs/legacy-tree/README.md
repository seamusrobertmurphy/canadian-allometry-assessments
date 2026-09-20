# LegacyTreeData: individual-tree destructive measurements

The **independent** side of the analysis. Western larch (*Larix occidentalis*) is absent
from Canada's national species set, so these trees were never used to fit the coefficient
under test. That independence is what makes the 47 percent underestimate a real test rather
than a residual check.

This folder supplies **two separate samples** that share no individual trees:

1. **Bark mass** (`tree.txt`): 13 western larch with oven-dry stem-bark weight, 6.9 to
   19.8 cm DBH, one site. Fits the local equation.
2. **Stem taper** (`stem.txt`): 15 western larch (16.3 to 39.4 cm) and 42 tamarack (12.2
   to 31.5 cm) with paired outside-bark and inside-bark diameters at breast height. Tests
   bark allocation on larger trees, using measured diameters only, with no assumed density.

The taper trees begin where the mass sample ends, which is the whole point: the local
equation is applied to inventory stands averaging 32 cm, well beyond its calibration.

## Source and licence

- **Title:** LegacyTreeData: an online repository of individual-tree and stand-level biomass data
- **Publisher:** University of Idaho Library / Virginia Tech
- **DOI:** https://doi.org/10.7294/W4VD6WC6
- **Portal:** https://www.legacytreedata.org
- **Licence:** CC BY (reuse permitted with attribution)
- **Cite as:** Radtke, P., Walker, D., Frank, J., et al. (2021). LegacyTreeData: an online repository of tree measurement data.

## How to download

The repository distributes the whole holding as one archive of pipe/comma-delimited text
tables. Request or export the full dataset from `legacytreedata.org`, then extract the
tables below into this folder. No subsetting is needed, since the analysis filters in code.

## Files

| File | Rows | Size | In git | Used by |
|---|---:|---:|:---:|---|
| `tree.txt` | 250,386 | 40 MB | **no** | tree-level record: species, DBH, component dry weights |
| `stem.txt` | 2,774,773 | 132 MB | **no** | stem taper: paired outside/inside-bark diameters by height |
| `section.txt` | 28,902 | 4 MB | yes | sectional measurements |
| `location.txt` | 23,029 | 2 MB | yes | site and study metadata |
| `branch.txt`, `core.txt`, `disk.txt` | n/a | 1 to 3 MB | yes | not used by this analysis |
| `Data_Dictionary.pdf` | n/a | 1 MB | yes | **read this first.** Defines every column code |
| `FileDescriptions.rtf` | n/a | small | yes | table-level descriptions |

`tree.txt` and `stem.txt` are **excluded from git**. `stem.txt` at 132 MB exceeds GitHub's
100 MB per-file hard limit; `tree.txt` is omitted for bulk. Both are openly redownloadable,
so restore them here and the pipeline runs unchanged.

## Columns the analysis reads

**From `tree.txt`**, keyed by `author, loc, spcd, treeno`:

| Column | Meaning |
|---|---|
| `spcd` | FIA species code. **73 = western larch**, 71 = tamarack |
| `st_ob_d_bh` | stem diameter outside bark at breast height (inches) |
| `st_bk_dw` | stem bark dry weight (pounds) |
| `st_wd_dw` | stem wood dry weight (pounds) |
| `ag_dw` | total aboveground dry weight (pounds) |

**From `stem.txt`**, same four-part key:

| Column | Meaning |
|---|---|
| `st_ht` | height of the section on the stem (feet). Breast height is `4.5` |
| `st_ob_d` | section diameter outside bark (inches) |
| `st_ib_d` | section diameter inside bark (inches) |

## Gotchas

- **Units are imperial.** Inches, pounds, feet. Converted in code: `IN2CM = 2.54`,
  `LB2KG = 0.453592`, `FT2M = 0.3048`.
- **Breast height is a float match on `st_ht == 4.5`**, in the source units, not metric 1.3 m.
- **Duplicate breast-height sections exist** for some trees; the analysis keeps one section
  per tree by deduplicating on the four-part key.
- **A few malformed rows.** R's `read.csv` absorbs them; the earlier Python implementation
  used `on_bad_lines="skip"`. Row counts above are as R reads them.
- **Not every tree carries every measurement.** The western-larch bark-mass filter
  (`spcd == 73` with a non-missing `st_bk_dw`) reduces 96 candidate trees to **13**.
- **Component definitions differ from ENFOR** in detail and were reconciled only as far as
  the metadata allow. The residual difference is carried in the paper as a limitation.

## Provenance of the two western-larch samples

Bark mass is a single site (Gower 1987, Washington Cascades). Taper is `FMSC_Validation_R6`,
Umatilla National Forest, Blue Mountains. Tamarack taper spans three sites
(`FMSC-Validation/R9_Chippewa`, `Hansen/26_1`, `Hansen/55_1`), which is why the tamarack
trend survives leave-one-out and the western-larch trend does not. Both western-larch
samples are interior Pacific Northwest, the same regional population as British Columbia's
larch but not the inventory's own trees.
