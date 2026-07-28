# Manuscript design specification: two-stage larch bark allometry

Prepared 2026-07-16. This locks the manuscript design the author asked to follow, matched
to the guiding publications' word count, layout, and quantity and depth of tables and
figures. It supersedes the ad-hoc structure of the current draft.

## What we take from each guiding publication

- **Delcourt et al. (2022)** — the statistical metrics, tests, and visualization, and the
  component-equation table format (a, b with standard errors, RMSE, N, DBH range per
  component; weighted nonlinear least squares with a DBH^2c variance function; log-log with
  the Baskerville-Sprugel correction; weighted-residual diagnostics).
- **Xing et al. (2019)** — the concentrated accuracy-and-uncertainty assessment of
  allometric equations by biomass component (per-component log(a), b, SEE, R2; observed
  versus predicted; stand-level estimates carried with +/- 1 SD; bias by species and stand type).
- **DellaSala et al. (2022)** — the province-wide application on the **BC Vegetation
  Resources Inventory (VRI)**, the open Forest Resource Inventory updated annually, compared
  against field plots and a second spatial product, with carbon by pool and elevation and 95%
  confidence intervals.
- **House style (DX4205 report, S. Murphy)** — descriptive-statistics table with
  Shapiro-Wilk normality, parameter table with SE and significance stars and RMSE, scatter
  and residual-versus-fitted figures.

## Measured anatomy of the exemplars (the targets)

| Paper | Words (full PDF / est. main text) | Tables | Figures | Core statistics | Core visuals |
|---|---|---|---|---|---|
| Delcourt 2022 | 13,483 / ~7,000 | 5 + 2 appendix | 4 + 2 appendix | weighted NLS (DBH^2c), log-log + Baskerville-Sprugel, RMSE, parameter SE, R2 | site map; per-component biomass-DBH curves; weighted residuals vs fitted; stand prediction |
| Xing 2019 | 8,555 / ~5,000 | 5 | 4 | per-component log(a), b, SEE, R2; bias; stand-level +/- 1 SD | observed vs predicted (AGB, BGB); height-DBH; root:shoot vs size |
| DellaSala 2022 | 10,813 / ~7,500 | 3+ | image plates | carbon by pool and elevation; 95% CI; VRI vs field vs GlobBiomass; stock change | C-density maps; elevation profiles; pool comparisons |

Full-PDF counts include references and appendices; main-text estimates exclude them.

## Our study, two stages

- **Stage 1, destructive accuracy and uncertainty (Xing + Delcourt).** Evaluate the national
  coefficients for larch stem bark (with stem wood and total for context) against destructive
  data: **ENFOR** tamarack (*L. laricina*, in-sample, n = 439) and **LegacyTreeData** western
  larch (*L. occidentalis*, independent, n = 13, single site, DBH only, to 20 cm). Report
  bias, relative bias, RMSE, relative RMSE, R2 by species and diameter class; refit
  larch-specific equations by weighted NLS and log-log with the Baskerville-Sprugel
  correction; cross-validate; diagnose residuals.
- **Stage 2, province-wide test (DellaSala).** Apply the national and the refitted larch
  equations to the **BC VRI** (province-wide, updated annually) to estimate larch stem-bark
  and aboveground biomass and carbon at landscape scale, quantify the effect of the bias and
  its correction on provincial larch bark carbon by leading species and elevation, and carry
  the uncertainty as a Monte Carlo 95% interval, cross-checked against field or plot data
  where available.

## Target structure to match (what I will build)

Target length: **~8,000 words main text** (DellaSala scale, appropriate to a two-stage study),
**7 tables, 7 figures**, plus a residual-diagnostics appendix and the reproducible code appendix.

Tables:

1. Datasets and extents: per species, n, DBH range, height range, stem-bark and stem mass
   ranges, sites and provinces, source, units (house-style descriptive statistics).
2. National coefficients evaluated: generic Conifers and Tamarack, DBH and DBH+height forms
   (a, b, c).
3. Accuracy of the national coefficients: species by coefficient by form by diameter class,
   giving n, bias, relative bias, RMSE, relative RMSE, R2 (Xing/Delcourt metric set).
4. Refitted larch bark equations (Delcourt Table 5 format): a and b with SE, variance
   exponent c, Baskerville correction factor, RMSE, relative RMSE, R2, N, DBH range, and
   k-fold cross-validated error.
5. Descriptive statistics with Shapiro-Wilk normality on the fitted response (house style).
6. VRI larch resource: area and merchantable volume by leading species and elevation band.
7. Province-wide larch bark carbon, national versus refitted, with Monte Carlo 95% intervals.

Figures:

1. Stem-bark mass versus DBH per species, national and refitted curves overlaid, log-log inset.
2. Observed versus predicted stem bark against the 1:1 line, per species (Xing Fig 2 style).
3. Relative bias by diameter class, per species.
4. Weighted residuals versus fitted values, diagnostics (Delcourt B1/B2 style).
5. Refitted versus national bark curves across the diameter range.
6. Province map of larch bark-carbon difference, national versus refitted (DellaSala map style).
7. Provincial larch bark carbon, national versus refitted, with confidence intervals by elevation.

Statistical apparatus, matched across the exemplars: weighted NLS with DBH^2c variance
weighting and log-log with the Baskerville-Sprugel correction; bias, relative bias, RMSE,
relative RMSE, R2, SEE, parameter SEs; Shapiro-Wilk and residual diagnostics; k-fold
cross-validation; Monte Carlo uncertainty for the province-wide step; QMD for stand
aggregation (Curtis and Marshall 2000).

## Data status and build order

- Stage 1 data are in hand (ENFOR, LegacyTreeData). Tables 1 to 5 and Figures 1 to 4 can be
  built now. The western-larch constraint (n = 13, one site, DBH only, to 20 cm) limits its
  refit to the diameter-only form and is stated as a limitation.
- Stage 2 needs the **BC VRI**, open from the BC Data Catalogue (Vegetation Resources
  Inventory), plus the leading-species and elevation layers. This is an acquisition step.

Build order: (1) Stage 1 tables 1 to 5 and figures 1 to 4 from data in hand; (2) acquire the
VRI and build Stage 2 tables 6 to 7 and figures 5 to 7; (3) assemble the manuscript to the
target structure and length, modelled section by section on Delcourt, Xing, and DellaSala.
