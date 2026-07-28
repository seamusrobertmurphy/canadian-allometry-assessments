# Task request: next steps in manuscript development

Prepared 2026-07-22. Supersedes `HANDOFF-2026-07-16.md`, whose scope questions are settled.
Resume from commit `5ad33e2`.

## Where the manuscript stands

A complete draft with real numbers throughout, main text about 6,600 words against an 8,000
target, 11 tables and 9 figures. Every number verifies against the pipeline, all
cross-references resolve, and the document renders clean to docx. Rendering re-runs the
whole analysis, so prose and numbers cannot drift.

The scientific argument is in three parts, and all three now have data behind them.
Tamarack is well served by its own national coefficient and over-predicted by the generic
conifer coefficient. Western larch, which the national system never fitted, is
underestimated by that generic coefficient. The two larches diverge in bark investment, so
the warranted correction is species-specific rather than genus-level. The provincial
consequence is an increase of 37 to 60 percent in western-larch stem-bark carbon, bracketed
by two independently calibrated equations.

**Target venue: Forest Science** (Oxford Academic, Society of American Foresters).
**Exemplars:** Delcourt et al. 2022 (statistics and table format), Xing et al. 2019
(accuracy assessment), DellaSala et al. 2022 (province-wide application; sets the scale
target). PDFs of all three are in `04.references/literature/`.

## The work, in priority order

### 1. Forest Science formatting (blocking for submission)

The YAML still carries the settings of an earlier venue guess. Replace
`../04.references/style-springer-quarto.docx` with a Forest Science reference doc and
`apa.csl` with the SAF author-date style. Confirm against the journal's current author
guidelines: word limit, abstract length, whether tables and figures are embedded or
submitted separately, and the reference format. This is mechanical but must be done against
the live guidelines rather than from memory.

### 2. Finish the executable integration — DONE 2026-07-22

Tables T8 to T11 are generated in R from the pipeline CSVs. Tables T1 to T7 are still typed
markdown carrying numbers copied by hand, which is exactly the drift risk the integration
was meant to remove. Convert them the same way, using the existing chunks as the pattern.
`03.outputs/tables/T1_descriptive_stats.csv` through `T7_province_barkC.csv` hold everything
they need.

All eleven tables now build from the CSVs. The conversion caught three defects that the
typed tables had hidden:

- **A wrong number.** @tbl-accuracy gave the tamarack DBH+H R squared as 0.95; the pipeline
  says 0.9554, so the table now reads 0.96. No prose cited the old value.
- **A suppressed number.** The same table showed a dash for the R squared of the tamarack
  coefficient applied to western larch. It is 0.07, and is now shown. If the dash was
  deliberate, restore it in the chunk rather than in the CSV.
- **Two formatting bugs in the existing T8/T9 chunks.** Column names written `95%% CI`
  rendered literally with the double percent, and a named `sapply` in T8 leaked an extra
  unlabelled row-name column. Both fixed. T11's area also disagreed with T9's by one
  hectare through truncation rather than rounding; both now use the shared `cnt()`.

### 3. Reconcile the stem-bark component definitions (the largest remaining uncertainty)

The 37 to 60 percent bracket is wide mostly because the two western-larch equations define
stem bark differently. Affleck's runs from a 30 cm stump to a 5 cm top; ENFOR and
LegacyTreeData include the stump and run to the tip. Our equation is more than twice
Affleck's at 10 cm and crosses below it by 45 cm, a pattern consistent with that truncation.

Two routes, cheapest first. Recompute our own equation on a stump-to-5 cm-top basis using
the LegacyTreeData section data already in hand, which would make the two directly
comparable without any new data. Failing that, request section-level data from Affleck; the
draft in `affleck-data-request-draft.md` has been rewritten for this narrower purpose and is
no longer load-bearing.

### 4. Read the two paywalled coefficient papers in full — HALF DONE 2026-07-22

Lambert et al. (2005) and Ung et al. (2008) are the coefficients the paper evaluates and
corrects, and they have been characterised from abstracts. This is a standing dependency
carried from the original decision memo and is not defensible at submission. Institutional
access needed.

**Lambert et al. (2005) is read**, from
`04.references/literature/Ung & Lambert 2005 National Canadian allometrics.pdf` (filed under
a misleading name; it is Lambert, Ung & Raulier 2005, CJFR 35:1996-2018, 23 pp). Verified
against the source and now in the manuscript:

- The calibration is **8,636 trees across 33 species**, not "thousands" (Table 1).
- Tamarack contributed **575 trees**, spanning 1.8 to 44.5 cm DBH and 2.2 to 30.5 m
  (Table 2). Our 439-record ENFOR extract spans that full extent, so the in-sample arm
  tests the coefficient across the whole interval it was fitted on. This is now stated in
  Methods and is the firmest available answer to the job-6 worry about overreading
  in-sample status.
- The **tamarack bark coefficients match the paper digit for digit**: DBH a = 0.0174,
  b = 2.1109; DBH+H a = 0.0120, b = 1.7059, c = 0.5811 (Table 3).
- The **generic coefficients do not**. Lambert's Softwood bark is a = 0.0162, b = 2.1959,
  where the operational table we evaluate carries a = 0.0153, b = 2.2110. The generic class
  we depend on is therefore the Ung (2008) re-estimate, not Lambert's. Methods now says so
  and gives both pairs. `02.inputs/larch/README.md` already had the attribution right.

**Ung et al. (2008) is still unread** and now carries more weight than before, because the
operative generic conifer coefficient is its estimate rather than Lambert's. CJFR 38:1123-1132,
doi 10.1139/X07-224. Institutional access still needed.

### 5. Close the remaining length and structure gap

About 1,400 words below the DellaSala-scale target. The honest places to add are a fuller
treatment of what the bark geometry can and cannot support, and the MRV and offsets material
that was compressed to a single Discussion paragraph when the framing moved away from Carbon
Balance and Management. Add the sections Forest Science expects and the draft lacks:
acknowledgements, funding, conflict of interest, author contributions.

### 6. Referee pass before submission

Run `verifying-results-before-claiming` and `peer-review` against the full draft. Give
particular attention to three claims: that the western-larch size trend is reported as
suggestive rather than established (Spearman p = 0.11, n = 15, one site); that the
area-to-mass step in the Stage 1b argument is stated as an untested assumption; and that the
in-sample status of the tamarack arm is not overread.

## Standing constraints

Framing is validation-and-refinement of the national equations, never a critique of them.
No fabricated numbers, and placeholders labelled as such. Edit the one master `.qmd`. Move
superseded files into the relevant `archive/`, never delete or overwrite in place. The Clay
Belt origin is motivation only and is never named or shown.

## Known traps

The manuscript needs `/opt/local/bin/python3.13`, not the default `python3` (3.12), which
lacks matplotlib. Stage 1b resolves its paths relative to the script directory while the
other stages resolve to the repository root; the setup chunk handles this and a naive
rerun from the wrong directory will not.

Four large data files are excluded from git and must be restored locally before the
pipeline will run. See `02.inputs/README-data.md`.
