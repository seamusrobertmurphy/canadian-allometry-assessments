# Legacy scripts — not the current analysis

> **The analysis now lives in the manuscript.** As of 2026-07-27 all four stages are
> R code in the `# Analysis` section of
> `01.manuscript/canadian-allometry-forest-science.qmd`, and they run when the document
> is rendered. Nothing in this folder produces the current tables or figures.
>
> The four Python stages that previously produced them (`stage1_accuracy_refit.py`,
> `stage1b_bark_geometry.py`, `stage2_vri_province.py`, `stage2b_affleck_comparator.py`)
> were ported to R and moved to `archive/`. Everything below describes an older
> black-spruce build that predates the two-stage larch design.

---

# ENFOR black-spruce equation analysis (R)

Open, reproducible reconstruction of the national aboveground biomass equation
comparison, built to be developed in R. No confidential project data are used.

## Run

```
cd analysis
Rscript run_all.R
```

Base R only, no packages required. Reads `../data/enfor/EnforCanadaBiomassFinalData_v2007-ENG.csv`.

## Structure

- `R/metrics.R` — relative bias, relative RMSE, R2, evaluation helper.
- `R/01_load_clean.R` — load ENFOR, normalise provinces, parse the Year field
  (single years and two-season campaign ranges), clean black spruce, flag
  coordinate precision, add size strata.
- `R/02_national_equation.R` — the national equation form (Lambert 2005 / Ung 2008):
  component power models `y = b1*D^b2` (DBH-only) and `y = b1*D^b2*H^b3` (DBH+height),
  total as the component sum. Two coefficient sources: published (authoritative,
  `coefficients/national_published.csv`) and an open re-fit to ENFOR.
- `R/03_fit_and_bias.R` — fit the national form on the whole black-spruce
  population, measure bias by size stratum, and compare against a stratum-specific
  fit evaluated out-of-sample by 5-fold cross-validation.
- `run_all.R` — orchestrates both DBH-only and DBH+height forms.
- `coefficients/national_published.csv` — schema and placeholder for the published
  black-spruce coefficients, to be filled from Lambert 2005 Table 3 and Ung 2008 Table 4.
- `verify_python_mirror.py` — a Python reimplementation used only to check the R
  numbers in this build environment (R is not installed here). Not part of the deliverable.

## Two coefficient paths

The manuscript must ultimately apply the **published** national coefficients. Until
those tables are transcribed from the paywalled papers (or read off the NRCan
calculator), the code re-fits the same functional form to ENFOR, the very sample
the national equations were built on, giving a fully open, runnable analogue.
Swap in `load_coefficients("coefficients/national_published.csv")` once populated.

## Read this before interpreting the numbers

Two limits are load-bearing. First, the current national coefficients are an open
re-fit, not the published SUR-additive parameters, so absolute bias magnitudes and
even their sign can shift once the published coefficients are used. Second, the
"small-tree" strata are a size-based proxy for peatland form, and size is not
drainage: ENFOR small black spruce are a mix of young upland and other trees, not
the stunted peatland trees Wagers et al. (2024) measured. The genuine peatland
contrast needs either the Wagers data or the spatial soil classification below.

## Next stages

1. Transcribe the published black-spruce coefficients into `national_published.csv`
   and re-run, so the comparison uses the authoritative national equations.
2. Peatland classification (`04_peatland_overlay.R`, planned): intersect the
   well-georeferenced ENFOR sites (coordinate precision >= 2 decimals) with a
   Canadian peatland or wetland layer, and/or IPCC Tier 1 soil (Histosol) data,
   to replace the size proxy with a soil-based peatland stratum.
3. Add the Wagers et al. (2024) peatland black spruce contrast set once its archive
   status is confirmed.
