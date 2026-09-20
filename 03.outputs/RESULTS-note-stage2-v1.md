# Stage 2 results: province-wide test on the BC VRI

Date: 2026-07-16. Produced by `02.inputs/scripts/stage2_vri_province.py` from the WFS pull
`02.inputs/vri/vri_larch.csv`. Tables T6-T7 in `03.outputs/tables/`, figures F5-F7.

## Data

BC Vegetation Resources Inventory (VEG_COMP_LYR_R1_POLY), pulled from the BC Data Catalogue
public WFS: 78,634 larch-leading polygons (SPECIES_CD_1 in LW, LT); 67,409 retained after
dropping polygons with missing QMD, stems, or area. Attributes: quadratic mean diameter
(QUAD_DIAM_125), live stems/ha, height, age, BEC zone, area, label centroid, and the VRI's own
volume-based bark biomass. Bark per hectare was computed as stems/ha x bark(QMD) under the
national generic conifer equation and the Stage 1 species-specific refit; carbon fraction 0.47.

## Table 6. VRI larch resource

| Leading species | Polygons | Area (ha) | Mean QMD (cm) | Mean height (m) | Mean age | Mean stems/ha | VRI bark (Mg/ha) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Western larch | 45,934 | 376,455 | 32.0 | 26.3 | 108 | 507 | 19.70 |
| Tamarack | 21,475 | 162,543 | 18.0 | 11.9 | 106 | 563 | 2.08 |

Western-larch stands average QMD 32 cm, well above the destructive sample ceiling of 20 cm, so
the western-larch refit is extrapolated at province scale.

## Table 7. Province-wide larch stem-bark carbon, national vs refit

| Leading species | Area (ha) | National (Mg C) | Refit (Mg C) | Difference (Mg C) | % | Refit 95% CI (Mg C) |
|---|---:|---:|---:|---:|---:|---|
| Western larch | 376,455 | 3,153,542 | 5,030,901 | +1,877,360 | +60% | 1.88M - 11.18M |
| Tamarack | 162,543 | 435,730 | 382,066 | -53,665 | -12% | 0.33M - 0.43M |
| All larch | 538,998 | 3,589,272 | 5,412,967 | +1,823,695 | +51% | 2.28M - 11.03M |

Cross-check: our national QMD-based bark correlates r = 0.78 with the VRI's independent
volume-based bark and totals 90% of it, supporting the stand-level approach.

## Reading

Correcting the western-larch bark bias adds about 1.9 Tg C (+60%) to provincial western-larch
stem-bark carbon over 376,000 ha; tamarack falls 12%; net larch bark carbon rises about 51%
(+1.8 Tg C). The spatial pattern is coherent: the correction concentrates in the southeast
interior where western larch grows, and is near zero for boreal tamarack in the northeast
(Figure F6). The Monte Carlo interval for western larch is wide (1.9 to 11.2 Tg C) because the
refit rests on 13 small trees and is extrapolated to 32 cm QMD stands; the direction is secure,
the magnitude provisional. This is the same lesson DellaSala et al. (2022) drew for the VRI, a
material and correctable under-count, made specific here to the western-larch bark pool.

## Caveats

- Extrapolation: the western-larch refit (fit to 20 cm) is applied to stands averaging 32 cm QMD.
- QMD single-tree scaling under-represents the stand diameter distribution (Jensen); it is applied
  identically to national and refit, so the difference is robust, absolute levels approximate.
- The VRI bark used for cross-check is volume-based (Boudewyn 2007), not the Lambert/Ung DBH
  equation evaluated in Stage 1.
