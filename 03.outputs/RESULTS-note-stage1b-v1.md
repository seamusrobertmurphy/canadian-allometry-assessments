# Stage 1b results: bark geometry and the size-dependence of bark allocation

Date: 2026-07-21. Produced by `02.inputs/scripts/stage1b_bark_geometry.py`
(numpy, pandas, scipy, matplotlib; run under Python 3.13, which carries matplotlib on this
machine). Tables `T8_bark_geometry.csv`, `T8b_bark_geometry_sites.csv`,
`T9_bark_area_scaling.csv`; figure `F8_bark_geometry.png`.

## Why this analysis exists

The Stage 1 western-larch bark-mass refit rests on 13 trees to 19.8 cm DBH, and Stage 2
applies it to inventory stands averaging 32 cm QMD. That extrapolation is governed by the
fitted exponent. If bark's share of the stem is constant with size, the bark exponent
matches the wood exponent and extrapolating is benign; if the share rises with size, the
bark exponent is larger and a fit calibrated on small trees understates bark in large ones.
Stage 1 could not test this because its data stop at 20 cm.

LegacyTreeData carries stem taper with paired outside-bark and inside-bark diameters. Every
tree has a section at exactly breast height (4.5 ft), so no interpolation is needed. This
supplies a second western-larch sample that shares no trees with the mass sample and covers
the diameter range the mass sample lacks. The analysis uses only measured diameters: no
assumed bark density, no imported constant.

## Samples

| Species | Source | Site | n | DBH range (cm) |
|---|---|---|---:|---|
| Western larch | LegacyTreeData, FMSC_Validation_R6 | Umatilla National Forest (Blue Mountains) | 15 | 16.3 to 39.4 |
| Tamarack | LegacyTreeData, FMSC-Validation | Chippewa | 30 | 12.2 to 31.5 |
| Tamarack | LegacyTreeData, Hansen | 26_1, 55_1 | 12 | 14.0 to 27.4 |

The western-larch bark-mass sample used in Stage 1 is Gower 1987, Chumstick Mountain,
Washington Cascades, 6.9 to 19.8 cm. **Zero trees overlap between the two western-larch
samples**, and the taper sample begins (16.3 cm) essentially where the mass sample ends
(19.8 cm) and runs to 39.4 cm, bracketing the 32 cm provincial mean QMD of Stage 2.

Both western-larch samples are interior Pacific Northwest, the same regional population as
southeast British Columbia, but neither is in British Columbia. Tamarack spans three sites;
western larch is one site. That asymmetry is a limitation of the western-larch arm.

## Table 8. Bark geometry at breast height

Bark share of the stem cross-section, f = 1 - (D_inside / D_outside)^2, the geometric
analogue of bark's share of stem mass.

| Species | n | Mean DBH (cm) | Double bark thickness (cm) | Bark share of cross-section | Bootstrap 95% CI |
|---|---:|---:|---:|---:|---|
| Western larch | 15 | 29.2 | 3.94 (SD 1.62) | 24.4% (SD 6.1) | 21.5 to 27.4% |
| Tamarack | 42 | 19.4 | 1.29 (SD 0.31) | 13.3% (SD 3.6) | 12.2 to 14.4% |

## The species contrast replicates independently

| Comparison | n (WL / tam) | WL | Tamarack | Ratio | Welch t | p | Cohen's d |
|---|---|---:|---:|---:|---:|---:|---:|
| All sizes | 15 / 42 | 24.4% | 13.3% | 1.83 | 6.63 | <0.0001 | 2.55 |
| Within 16.3 to 31.5 cm overlap | 10 / 31 | 23.5% | 12.8% | 1.84 | 5.43 | 0.0002 | 2.51 |

The contrast holds within the shared diameter band, so it is not an artefact of the western
larch sample being larger. Stage 1 measured a bark **mass** fraction ratio of 1.64
(18.9% against 11.5%) on different trees at different sites; this geometry gives 1.83 on
independent trees using a different measurement. Two independent samples, two different
quantities, the same divergence.

Area fractions exceed the Stage 1 mass fractions for both species (24.4 against 18.9 for
western larch, 13.3 against 11.5 for tamarack), which is expected: bark is proportionally
thickest near the base, so a breast-height cross-section overstates the whole-stem share,
and bark and wood differ in density. The two quantities are not interchangeable in level.
It is the **ratio between species** and the **trend with size** that transfer.

## Table 9. Size dependence and the scaling exponent

| Species | Slope of bark share per cm | Bootstrap 95% CI | Spearman rho | p | Bark area exponent b | 95% CI | p vs isometry (b = 2) |
|---|---:|---|---:|---:|---:|---|---:|
| Western larch | +0.0046 | -0.0001 to +0.0095 | +0.43 | 0.11 | 2.56 | 1.98 to 3.14 | 0.057 |
| Tamarack | -0.0042 | -0.0057 to -0.0029 | -0.59 | <0.0001 | 1.36 | 1.02 to 1.69 | 0.0004 |

Leave-one-out: the sign of the slope is stable for both species. For western larch the
slope's p reaches 0.215 in the worst leave-one-out fit, so **the positive size trend in
western larch is suggestive, not established**. The exponent is the firmer statement:
across all 15 leave-one-out fits the western-larch bark-area exponent stays above 2
(range 2.30 to 2.79), while tamarack's stays below 2 (range 1.30 to 1.39) and its negative
trend is significant at every leave-one-out fit (worst p = 0.0006) across three sites.

## What this settles, and what it does not

**Settles.** The two larches diverge in bark allocation, independently confirmed on a second
sample by a different measurement, and the divergence holds at matched diameter. It also
extends to 39.4 cm, past the 32 cm provincial mean QMD, so the species contrast is no longer
an inference from trees under 20 cm.

**Bears on the extrapolation.** Western-larch bark area scales super-isometrically
(b about 2.56, above 2 in every leave-one-out fit) while tamarack scales sub-isometrically
(b about 1.36). The Stage 1 western-larch bark-**mass** exponent, fitted on trees to 19.8 cm,
is 2.026, essentially isometric. If bark mass tracks bark area (constant bark density and
similar taper, an assumption stated as such), then the Stage 1 exponent, calibrated on small
trees, **understates** how bark accumulates in large ones. The direction of that error makes
the Stage 2 provincial correction conservative rather than inflated. This reframes the main
caveat: the extrapolation is still a limitation, but the evidence now available says it errs
low, not high.

**Does not settle.** It is not bark mass. Bark density is unmeasured in the taper sample, so
the step from area to mass rests on an assumption, and the paper must not convert this to a
mass claim. The western-larch trend rests on 15 trees at a single site in Oregon. Nothing
here removes the need for destructive western-larch bark mass across the operational
diameter range, which remains the priority.
