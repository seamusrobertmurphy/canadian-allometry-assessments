# Results note v0: first open run on ENFOR black spruce

Date: 2026-07-15. Status: pipeline demonstration on an open re-fit and a size proxy,
not yet a peatland-drainage result. Numbers below are from `verify_python_mirror.py`;
the R code (`run_all.R`) implements the identical logic and should reproduce them.

## Sample

1,813 black spruce with both DBH and height, of which 483 are below 9 cm DBH and
203 below 5 cm. This is the largest single-species sample in ENFOR.

## What the first run shows

Fitting the national equation form to the whole black-spruce population and then
looking at bias by size class, the pooled model is accurate in aggregate and on
large trees but badly biased on small trees.

DBH-only form:

| Stratum | n | mean obs (kg) | rel. bias % | rel. RMSE % | R2 |
|---|---|---|---|---|---|
| national -> all | 1813 | 70.7 | +5.5 | 21.4 | 0.957 |
| national -> larger (>=9 cm) | 1330 | 93.7 | +4.8 | 18.7 | 0.941 |
| national -> small (5-9 cm) | 280 | 10.6 | +29.7 | 38.7 | 0.247 |
| national -> very small (<5 cm) | 203 | 2.6 | +14.3 | 50.1 | 0.413 |
| stratum-specific (CV) -> small (<9 cm) | 483 | 7.2 | +7.2 | 31.1 | 0.832 |

Adding height (DBH+height form) cuts overall bias from +5.5% to +1.5% and lifts
overall R2 from 0.957 to 0.967, but the small-tree bias barely moves (+28.3% at
5 to 9 cm). A stratum-specific fit on the small trees, scored out-of-sample by
cross-validation, cuts small-tree bias to about +7% and lifts small-tree R2 from
0.25 to 0.83.

## Reading it honestly

Three points, one of them a caution.

The pipeline works and the headline shape is real: a nationally pooled fit carries
a large, systematic size-dependent bias on small black spruce, roughly 28 to 30
percent at 5 to 9 cm, and a stratum-specific equation largely removes it. That is
the Wagers et al. (2024) argument reproduced on open data: one calibration does not
serve the small-tree stratum.

Height helps the aggregate but not the small trees, which speaks directly to the
DBH-only versus DBH+height open question: the height term earns its place on the
population but does not rescue the atypical stratum.

The caution, which must not be buried: the bias here is an over-estimate, the
opposite sign to Wagers' roughly 12 percent under-estimate on peatland black spruce.
Two reasons, both expected. The coefficients are an open re-fit, not the published
SUR-additive parameters. And the stratum is small trees, not peatland trees; ENFOR
small black spruce are largely young upland trees, whose form a pooled power law
over-predicts, whereas Wagers' trees are stunted peatland trees the national model
under-predicts. Size is not drainage. This is exactly why the next stage, the
peatland soil overlay, is not optional: it is what turns a size-class demonstration
into the peatland claim the paper is about.

## Immediate next steps

Transcribe the published black-spruce coefficients and re-run so the comparison uses
the authoritative national equations. Then build the peatland classification from the
well-georeferenced sites against a Canadian peatland or wetland layer and IPCC Tier 1
Histosol data, and re-cut the bias analysis on a soil-based peatland stratum.
