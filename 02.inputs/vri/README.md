# BC Vegetation Resources Inventory — larch-leading polygons

The operational inventory the equations are applied to. This is where a tree-level
coefficient bias becomes a carbon number: British Columbia derives forest biomass from VRI
stand volume through the national volume-to-biomass conversion, so any bias in the
underlying component relationships propagates to every hectare it reports.

Reissued annually, and used for provincial greenhouse-gas reporting, offset accounting and
land-use analysis — which is why a correction carried into it would flow into stock-change
monitoring rather than a one-off restatement.

## Source and licence

- **Layer:** `WHSE_FOREST_VEGETATION.VEG_COMP_LYR_R1_POLY` (VRI — Forest Vegetation Composite Rank 1)
- **Publisher:** Province of British Columbia, Ministry of Forests
- **Portal:** BC Data Catalogue — https://catalogue.data.gov.bc.ca/dataset/vri-forest-vegetation-composite-rank-1-layer-r1-
- **Licence:** Open Government Licence – British Columbia
- **Projection:** BC Albers, EPSG:3005
- **Retrieved:** 2026-07-16

## How to download

Pulled from the public **WFS** endpoint of the BC Data Catalogue, filtered server-side to
larch-leading polygons:

```
SPECIES_CD_1 IN ('LW','LT')
```

`LW` = western larch, `LT` = tamarack. That returns **78,634 polygons** (51,400 western-larch-leading,
27,234 tamarack-leading). The cached CSV here is a convenience, not a dependency of the
method — any equivalent extract carrying the columns below reproduces the analysis.

Service endpoint: `https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_VEGETATION.VEG_COMP_LYR_R1_POLY/ows`
(WFS 2.0.0, `outputFormat=csv`). The layer is large; always filter by species server-side.

## Files

| File | Rows | Size | In git | Notes |
|---|---:|---:|:---:|---|
| `vri_larch.csv` | 78,634 | 15 MB | **no** | the extract. Redownloadable from the WFS query above |
| `bc_boundary_3005.geojson` | — | 1 MB | yes | Natural Earth 1:50m admin-1, public domain, dissolved to BC, reprojected to EPSG:3005, simplified 500 m. **Not yet used** — intended to give Figure 6 a basemap |

## Columns the analysis reads

| Column | Meaning |
|---|---|
| `SPECIES_CD_1` | leading species code (`LW` / `LT`) |
| `QUAD_DIAM_125` | quadratic mean diameter, cm, at a 12.5 cm utilisation level |
| `VRI_LIVE_STEMS_PER_HA` | live stems per hectare |
| `BASAL_AREA` | stand basal area, m²/ha — fills stems/ha where it is missing |
| `PROJ_HEIGHT_1` | projected stand height, m |
| `PROJ_AGE_1` | projected stand age, years |
| `FEATURE_AREA_SQM` | polygon area, m² |
| `BARK_BIOMASS_PER_HA` | the inventory's own volume-based bark biomass — used only as an independent cross-check |
| `LABEL_CENTRE_X`, `LABEL_CENTRE_Y` | polygon label centroid, BC Albers — used for the map |
| `BEC_ZONE_CODE` | biogeoclimatic zone |

## Cleaning, and what it drops

Polygons are retained only where leading species is `LW` or `LT` **and** QMD, stems/ha and
area are all present and positive. That takes **78,634 → 67,409**, dropping 11,225. Where
`VRI_LIVE_STEMS_PER_HA` is missing or zero, stems/ha is recovered from basal area and QMD
as `BASAL_AREA / (π·(QMD/200)²)`.

Resulting resource: **45,934 western-larch-leading polygons over 376,455 ha** (mean QMD
32 cm, mean height 26 m) and **21,475 tamarack-leading over 162,543 ha** (18 cm, 12 m).

## Gotchas

- **QMD is a stand mean, and the bark equation is a convex power.** Evaluating at QMD
  under-represents the diameter distribution (Jensen's inequality), so absolute levels are
  a first-order approximation. It is applied identically to every equation compared, so the
  **correction ratio is robust while absolute totals are approximate.** The paper states this.
- **Western-larch mean QMD is 32 cm**, well above the 19.8 cm ceiling of the destructive
  sample. The local equation is therefore extrapolated at inventory scale — the single
  largest source of uncertainty in the paper, and why a published 105 cm equation is
  brought in to bracket it.
- **`BARK_BIOMASS_PER_HA` is a different procedure**, not the diameter equation under test.
  It comes from the national volume-to-biomass conversion (Boudewyn et al. 2007) and is used
  only to situate the estimate: r = 0.78, our total 90 percent of theirs.
- **Carbon fraction is 0.47** (IPCC), marginally below the 0.5 the inventory uses.
- Numeric columns arrive as text with empty strings; all are coerced with `as.numeric` and
  the coercion warnings suppressed.
