# Results note v1: genus-level larch stem-bark bias (open data)

Date: 2026-07-16. Scope C (genus-level *Larix*), decided this session. Numbers are
computed by `02.inputs/scripts/larch_bark_genus_analysis.py` (numpy only; reproducible
from the repo root). Supersedes the black-spruce `RESULTS-note-v0.md` (archived).

Sign convention: relative bias = 100·(predicted − observed) / observed. **Negative =
the national coefficient under-predicts** observed stem bark. Relative RMSE = 100·RMSE /
mean observed.

## Samples

- **Tamarack (*Larix laricina*), ENFOR — in-sample.** n = 439 with complete stem-bark
  mass, DBH and height; DBH ≤ 38 cm. ENFOR is the data the national coefficients were
  fitted on, so this arm is an in-sample adequacy check, not an independent test.
- **Western larch (*L. occidentalis*), LegacyTreeData — out-of-sample.** n = 13 with
  stem-bark mass and DBH; **no height recorded, single site**, DBH 6.9–19.8 cm. Genuinely
  independent of ENFOR. Imperial units converted to metric.
- **Western larch large trees (> 40 cm) and any tamarack bark in LegacyTreeData: none.**
  No fully-open dataset contains larch stem-bark mass above ~38 cm DBH.

## Control (validates units + coefficient code)

Applying the published **Tamarack** coefficient to ENFOR tamarack reproduces observed
bark almost exactly: relative bias −0.6 % (DBH+H), −1.5 % (DBH); relative RMSE 22.9 % /
27.3 %. As expected for the coefficient's own calibration data. Units (in→cm, ft→m,
lb→kg) and coefficient application are therefore correct.

## Findings (stem bark)

| Observed arm | National coeff | Form | n | rel. bias | rel. RMSE |
|---|---|---|---|---|---|
| Tamarack (ENFOR, in-sample) | Tamarack | DBH+H | 439 | −0.6 % | 22.9 % |
| Tamarack (ENFOR, in-sample) | **Conifers (generic)** | DBH+H | 439 | **+20.7 %** | 41.1 % |
| Tamarack (ENFOR, in-sample) | **Conifers (generic)** | DBH | 439 | **+18.6 %** | 43.1 % |
| **Western larch (out-of-sample)** | **Conifers (generic)** | DBH | 13 | **−47.0 %** | 56.3 % |
| Western larch (out-of-sample) | Tamarack | DBH | 13 | −53.8 % | 65.4 % |

Western-larch bias bootstrap 95 % CI (Conifers, DBH): (−49.2 %, −45.1 %). Every one of
the 13 trees carries 1.7–2.6× the bark the generic coefficient predicts, so the
underestimate is uniform, not outlier-driven.

**Mechanism.** Stem-bark fraction of stem mass: tamarack 11.5 % ± 3.9 (n = 439) versus
western larch 18.9 % ± 2.9 (n = 13). Western larch invests roughly 1.6× the bark share
of tamarack — the thick-bark syndrome the paper hypothesised, measured directly.

## The headline, stated honestly

The two larches depart from the national coefficients in **opposite directions**, so
"larch bark bias" is not a single genus-level effect:

1. **Western larch is badly under-served by the only coefficient available to it.**
   Western larch has no national equation, so an accountant must use the generic
   **Conifers** coefficient. That coefficient underestimates western-larch stem bark by
   ~47 % (CI −49 to −45) even in small trees (≤ 20 cm), out-of-sample and independent of
   ENFOR. This supports the paper's core mechanism.
2. **Tamarack is the counter-case.** The generic Conifers coefficient *over*-predicts
   tamarack bark (+19 %), while tamarack's own national coefficient is essentially
   unbiased (−0.6 %). Tamarack is thinner-barked than the conifer pool average.
3. **Consequence:** a species-specific *western larch* bark coefficient is warranted; a
   genus-pooled "larch" bark coefficient is not — it would average two opposite biases.
   The naive pooled refit (10-fold CV: national Conifers +16.6 % / 43.6 % → genus-refit
   +2.2 % / 30.0 %; `bark = 0.0192·DBH^2.097`) illustrates exactly this masking and
   should not be presented as the recommended fix.

## What the open data cannot support

- **Size-dependence above 40 cm.** Tamarack tops out at 38 cm, western larch at 19.8 cm
  in the open data; the pooled slope of proportional error on DBH (+0.008/cm, t = 4.4) is
  confounded by species mixing and has one tree > 40 cm. The "bias grows with size and
  concentrates in large trees" claim remains **untestable on open data** and needs the
  Affleck/INGY western-larch destructive set (470 trees to 105 cm, with height; by request).
- **Component-definition reconciliation** between LegacyTreeData `st_bk_dw` and ENFOR
  `OM_stem_bark` (bole section, top diameter, stump height) is not yet done and could
  shift the western-larch magnitude; the direction is secure, the exact percentage is not.

## Next steps

1. Fix the manuscript framing to the species-divergence result (author decision).
2. Request the Affleck/INGY western-larch data to add large trees, height, and a real
   size-dependence test; firm up western larch beyond n = 13, one site.
3. Reconcile stem-bark component definitions across the two sources.
4. Replace all placeholder numbers in the master `.qmd` with the values above.
