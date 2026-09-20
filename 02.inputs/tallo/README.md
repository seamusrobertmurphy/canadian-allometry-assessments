# Tallo: global tree allometry and crown architecture database

> **Not used by the current analysis.** Retained for reference and for possible future work
> on the larch height–diameter relation. Nothing in the manuscript reads this folder.

Tallo was assessed early as a candidate source of larch allometry across Alberta and British
Columbia. It was set aside because it carries **stem diameter, height and crown dimensions
but no component dry masses**, and stem bark mass is exactly what this paper needs. The
component data came instead from ENFOR and LegacyTreeData.

## Source and licence

- **Title:** Tallo: a global tree allometry and crown architecture database
- **Authors:** Jucker, T., et al. (2022), *Global Change Biology* 28:5254–5268
- **DOI (paper):** https://doi.org/10.1111/gcb.16302
- **DOI (data):** https://doi.org/10.5281/zenodo.6637599
- **Repository:** Zenodo
- **Licence:** CC BY 4.0
- **Scale:** ~500,000 trees, ~5,000 species, globally distributed

## How to download

From the Zenodo record above. The archive contains `Tallo.csv` plus its metadata and
reference tables. Extract into this folder.

## Files

| File | Size | In git | Notes |
|---|---:|:---:|---|
| `Tallo.csv` | 47 MB | **no** | the full database. Redownload from Zenodo |
| `Tallo_metadata.csv` | small | yes | column definitions, read first |
| `Tallo_references.csv` | small | yes | source citation for every contributing study |

A derived larch extract lives one folder over, at
`../larch/tallo_larix-alberta-british-columbia-allometry.xlsx`, holding *Larix* records filtered to
Alberta and British Columbia, kept from that early assessment.

## What it contains

One row per tree: species, stem diameter, height, crown radius and crown depth, with
coordinates and a reference key back to the contributing study. Useful for height–diameter
and crown-architecture work.

## Why it does not appear in the manuscript

The paper is a **component-level** assessment, stem bark specifically. Tallo has no mass
compartments, so it cannot evaluate a bark coefficient or fit one. Where a height–diameter
relation was needed (for the published comparison equation, which takes diameter and
height), it was fitted from the inventory's own projected heights instead, so the comparison
stays anchored on the stands the equations are actually applied to.
