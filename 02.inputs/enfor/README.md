# ENFOR destructive-biomass dataset: manifest and profile

Acquired 2026-07-15 for the Canadian allometry commentary. This is the open, non-confidential dataset that replaces the Clay Belt material as the paper's analytical spine. It is the actual sample the national equations were fitted on, which makes it the honest ground for a bias demonstration.

## Source and licence

- **Title:** Biomass of trees sampled across Canada as part of the Energy from the Forest Biomass (ENFOR) Program
- **Publisher:** Natural Resources Canada, Canadian Forest Service
- **Portal record:** https://open.canada.ca/data/en/dataset/fbad665e-8ac9-4635-9f84-e4fd53a6253c
- **DOI:** https://doi.org/10.23687/fbad665e-8ac9-4635-9f84-e4fd53a6253c
- **Licence:** Open Government Licence – Canada (reuse permitted with attribution)
- **Temporal coverage:** 1978–1983 (sampling); record published 2017
- **Cite as:** Ung, C.-H., Lambert, M.C., Raulier, F., Guo, J., Bernier, P.Y. 2017. Biomass of trees sampled across Canada as part of the Energy from the Forest Biomass (ENFOR) Program.

## Files in this folder

- `EnforCanadaBiomassFinalData_v2007-ENG.csv` — the data, 9,454 tree records (English).
- `EnforCanadaBiomassMetadata_v2010-ENG.doc` — official field-and-column metadata (English). Read this before analysis; it defines the oven-dry-mass compartments and the compilation corrections.

The French-language equivalents exist at the same portal record and were not pulled.

## What the data contains

One row per destructively sampled tree. Columns: `ident, No, Province, Year, Location, Plot, Tree, Species_E, Dbh, Height, OM_stem, OM_stem_wood, OM_stem_bark, OM_crown, OM_foliage_twigs, OM_branches, OM_total, Lat, Long`. Biomass is oven-dry mass in kilograms by compartment (stem wood, stem bark, branches, foliage and twigs) plus totals, alongside diameter at breast height, total height, and coarse location.

## Profile relevant to the paper

The target stratum is well represented. Black spruce is the single most-sampled species, 1,764 records (1,813 on a loose text match, see hygiene note), spanning diameters from 0.7 to 38.4 cm with a median of 13.5 cm. Height is recorded for every black spruce row, which is what the diameter-only versus diameter-plus-height comparison needs. The small-tree tail that matters most for peatland stands is present but modest: 483 black spruce records below 9 cm DBH and 203 below 5 cm. Provincial spread is eastern-weighted and useful, with Quebec (933), Newfoundland and Labrador (300), Yukon (290), and Ontario the main contributors, and a small British Columbia set (60) reflecting the Ung 2008 addition. The whole dataset holds 9,454 trees across roughly 45 species after label cleanup.

## The one structural limitation, and what it means for the method

ENFOR carries no site, drainage, ecosite, wetland, or peatland attribute. There is no column that marks a tree as growing on peatland. This is the decisive fact for the analysis design. The paper cannot select a "peatland black spruce" stratum directly from ENFOR the way the Clay Belt inventory allowed. Three workable routes follow, in preference order:

1. Use ENFOR as the national reference set and the Wagers et al. 2024 peatland black spruce data as the external contrast set, which is exactly the design the decision memo already records. ENFOR shows what the national equations were fitted to; Wagers supplies the peatland-specific truth.
2. Approximate a stunted, small-tree black spruce subset within ENFOR by diameter and height, as a size proxy for open peatland form, with the clear caveat that size is not drainage.
3. Join ENFOR lat/long to an external peatland or wetland map (for example a national peatland layer) to tag likely peatland origin. The coordinates are coarse (whole-degree in the sampled head rows), so treat any such tag as approximate and secondary.

Route 1 is the honest headline design. Routes 2 and 3 are supporting sensitivity checks, not the main claim.

## Data-hygiene notes for the analysis script

Province labels are not normalised: lowercase `on` and `qc` appear alongside `ON` and `QC` and must be folded before any by-province summary. The species field has minor label variants (the loose black spruce match returns 49 more rows than the exact label), so build a clean species lookup before fitting. Coordinates in the inspected rows are whole-degree and coarse; do not treat lat/long as plot-precise.

## Drafted data-availability statement

"The tree-level biomass data underlying this study are openly available from Natural Resources Canada, Canadian Forest Service, as the Energy from the Forest Biomass (ENFOR) dataset (https://doi.org/10.23687/fbad665e-8ac9-4635-9f84-e4fd53a6253c), under the Open Government Licence – Canada. Peatland black spruce contrast data are from Wagers et al. (2024). No confidential or third-party project data were used." (Adjust once the Wagers archive status is confirmed.)
