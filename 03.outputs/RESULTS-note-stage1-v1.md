# Stage 1 results: component-wise accuracy and larch refits (open data)

Date: 2026-07-16. Produced by `02.inputs/scripts/stage1_accuracy_refit.py` (numpy, pandas,
scipy, matplotlib). Tables in `03.outputs/tables/`, figures in `03.outputs/figures/`.
Sign convention: relative bias = 100(predicted - observed)/observed; negative = underestimate.

## Table 1. Datasets and extents

| Dataset | Variable | n | Mean | SD | Min | Max |
|---|---|---:|---:|---:|---:|---:|
| Tamarack (ENFOR, in-sample) | DBH (cm) | 439 | 15.46 | 8.92 | 1.80 | 44.50 |
| | Height (m) | 439 | 12.76 | 5.96 | 2.20 | 30.45 |
| | Stem bark (kg) | 439 | 7.96 | 8.62 | 0.07 | 62.40 |
| | Stem wood (kg) | 439 | 81.87 | 98.17 | 0.28 | 742.40 |
| | Total AGB (kg) | 439 | 109.01 | 126.76 | 0.42 | 938.88 |
| Western larch (LegacyTreeData, independent) | DBH (cm) | 13 | 12.37 | 4.17 | 6.86 | 19.81 |
| | Height (m) | 0 | - | - | - | - |
| | Stem bark (kg) | 13 | 8.56 | 6.04 | 2.81 | 20.82 |
| | Stem wood (kg) | 13 | 40.43 | 32.57 | 7.98 | 111.31 |
| | Total AGB (kg) | 13 | 51.47 | 40.34 | 11.11 | 137.12 |

Western larch carries no recorded height and no stem bark above 20 cm, so it is evaluated in
the diameter-only form.

## Table 3. Accuracy of the national coefficients, stem bark (excerpt)

| Species | Coefficient | Form | Class | n | Bias (kg) | Rel. bias | RMSE (kg) | Rel. RMSE | R2 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| Tamarack | Tamarack | DBH+H | all | 439 | -0.05 | -0.6% | 1.82 | 22.9% | 0.95 |
| Tamarack | Conifers | DBH | all | 439 | +1.48 | +18.6% | 3.43 | 43.1% | 0.84 |
| Tamarack | Conifers | DBH | <20 | 299 | +0.32 | +10.2% | 1.02 | 32.5% | 0.87 |
| Tamarack | Conifers | DBH | 20-40 | 139 | +3.96 | +22.1% | 5.89 | 32.9% | 0.25 |
| Western larch | Conifers | DBH | all | 13 | -4.02 | -47.0% | 4.82 | 56.3% | 0.31 |
| Western larch | Tamarack | DBH | all | 13 | -4.60 | -53.8% | 5.60 | 65.4% | - |

The generic Conifers coefficient over-predicts tamarack bark and increasingly so with size
(+10% below 20 cm, +22% at 20 to 40 cm), while its predecessor tamarack coefficient is
near-unbiased on its own calibration data. The same generic coefficient underestimates
western-larch bark by 47%. (Full species x component x coefficient x class matrix in
`T3_accuracy_national.csv`.)

## Table 4. Larch-specific stem-bark refits

| Species | Method | a | a (SE) | b | b (SE) | c (var) | CF | Rel. RMSE | R2 | CV rel. RMSE: national -> refit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Tamarack | log-log OLS (Baskerville-Sprugel) | 0.018 | 0.001 | 2.101 | 0.017 | - | 1.031 | 27.5% | 0.936 | 43.1% -> 27.5% |
| Tamarack | weighted NLS (DBH^2c) | 0.019 | 0.001 | 2.092 | 0.018 | 1.837 | - | 27.3% | 0.936 | 43.1% -> 27.5% |
| Western larch | log-log OLS (Baskerville-Sprugel) | 0.047 | 0.012 | 2.026 | 0.102 | - | 1.007 | 7.7% | 0.987 | 56.3% -> 9.3% |
| Western larch | weighted NLS (DBH^2c) | 0.031 | 0.006 | 2.187 | 0.073 | -1.073 | - | 6.4% | 0.991 | 56.3% -> 9.3% |

A western-larch bark equation cuts cross-validated relative RMSE from 56% (generic Conifers)
to 9%, with R2 of 0.99. The log-log and weighted-NLS fits agree for tamarack; for western
larch the weighted-NLS variance exponent is unstable at n = 13 (negative), so the log-log fit
is preferred there. (Stem wood and total AGB refits in `T4_larch_refits.csv`.)

## Table 5. Normality (stem bark)

| Species | Variable | n | Skew | Kurtosis | Shapiro W | Shapiro p |
|---|---|---:|---:|---:|---:|---:|
| Tamarack | stem bark (kg) | 439 | 1.75 | 4.59 | 0.820 | <0.001 |
| Tamarack | log stem bark | 439 | -0.55 | -0.55 | 0.956 | <0.001 |
| Tamarack | log-log residuals | 439 | -0.72 | 2.69 | 0.967 | <0.001 |
| Western larch | stem bark (kg) | 13 | 0.89 | -0.60 | 0.851 | 0.029 |
| Western larch | log stem bark | 13 | 0.23 | -1.18 | 0.925 | 0.290 |
| Western larch | log-log residuals | 13 | -0.19 | -0.67 | 0.965 | 0.824 |

The log transform normalizes the western-larch response (raw p = 0.029; residuals p = 0.82),
justifying the log-log fit. For tamarack the large sample makes Shapiro-Wilk significant on
small departures, but skew and kurtosis of the residuals are modest.

## Figures

- F1 `F1_bark_vs_dbh.png` - stem bark vs DBH per species, national Conifers (dashed) and larch refit (solid), with a log-log panel.
- F2 `F2_obs_vs_pred.png` - observed vs predicted stem bark (national Conifers) against the 1:1 line.
- F3 `F3_relbias_by_class.png` - relative bias of the national Conifers coefficient by diameter class.
- F4 `F4_residuals.png` - log-log residuals vs fitted, refit diagnostics per species.

## What Stage 1 establishes

The generic conifer coefficient, the operative national predictor for the unlisted western
larch, underestimates western-larch stem bark by 47% and a species-specific equation removes
almost all of that error (cross-validated relative RMSE 56% to 9%, R2 0.99). The same generic
coefficient over-predicts tamarack bark and worsens with size, whereas tamarack's own national
coefficient is near-unbiased. A species-specific western-larch bark coefficient is warranted; a
genus-pooled larch coefficient is not. Constraint: the western-larch sample is n = 13, one
site, diameter-only, to 20 cm; Stage 2 tests the equations province-wide on the BC VRI.
