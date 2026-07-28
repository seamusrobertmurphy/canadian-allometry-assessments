# Handoff task request: western larch stem-bark bias paper

Prepared 2026-07-15 to carry the project into a fresh session. Review this, then start a new context. Everything needed to resume is here.

## What the paper is

A component-level allometric validation. It tests whether the **national (Lambert et al. 2005; Ung et al. 2008) stem-bark coefficient underestimates stem-bark biomass in western larch (*Larix occidentalis*)**, by a margin that grows with tree size and does not average out at the stand scale, and whether a species-specific bark coefficient is warranted. Framing is a validation-and-refinement of generalized equations, never a critique of them. Target: Forest Science or Canadian Journal of Forest Research.

Selected title: *Underestimation of stem-bark biomass by national allometric coefficients in western larch (Larix occidentalis)* — *A component-level bias assessment for British Columbia*.

## Where everything lives (repo conventions)

Numbered `NN.name` folders; every folder has an `archive/` for superseded files; the index is `INDEX.md`.

- **Master manuscript (edit only this):** `01.manuscript/canadian-allometry-forest-science.qmd` (Quarto; renders docx + html; self-contained with code appendix).
- Bibliography: `04.references/references.bib`; CSL `apa.csl`; literature PDFs in `04.references/literature/`.
- Analysis scripts (black-spruce lineage, reusable machinery): `02.inputs/scripts/R/`.
- Planning and reviews: `05.tasks/` (this file; `larch-component-bias-concept.md`; `annotated-bibliography.md`).
- Archived black-spruce manuscript snapshot: `01.manuscript/archive/`.

## Status by section

- **Abstract** — done (bark; carries placeholder result numbers as prose: ~18% mean underestimate, ~28% >40 cm, RMSE ~34% national vs ~17% species-specific, +3% stand bark carbon). Replace with computed values later.
- **Introduction** — done. Trade-off framing; all integrated literature present (Ter-Mikaelian 1997, Zianis 2005, Case 2008, Xing 2019, Vorster 2020, Ahmed 2013, Sileshi 2014, Temesgen 2015, Fradette 2021, Wagers 2024, Delcourt 2022, Williams 2017, Dirnberger 2017, DellaSala 2022, Tompalski 2026, Chojnacky 2014, Singh 2022, Lutz 2018, Mildrexler 2020; H1 mechanism cites FEIS/Scher 2002, Pausas 2015, Pellegrini 2017, Zhu 2024).
- **Hypotheses** — done. H1 (mechanistic, underestimation growing with size, not averaging out), H1a size dependence, H1b uncertainty reduction, H1c stand-level consequence.
- **Methods** — drafted skeleton (~85%), 7 subsections. Gated on data (see blockers).
- **Results / Discussion / Conclusions** — stubs, pending analysis.
- **Reproducible workflow appendix** — built; helper functions run, data-dependent chunks `eval: false` until the dataset lands at `02.inputs/larch/`.

## Blockers to clear first (in priority order)

1. **Secure the western larch destructive dataset with a stem-bark component.** Lead candidate: Inland Northwest conifer biomass programme (Affleck / University of Montana INGY; 470 felled trees, 5–105 cm DBH, stem bark measured, western larch among species). Same continuous population as BC interior larch. Alternatives: Standish et al. 1985 (BC-X-264, BC-sampled); LegacyTreeData repository. User (BC-based) may hold or can request BC data. Extract the western larch subset: total n and the count > 40 cm DBH (fills the `[ ]` blanks in Methods and the abstract).
2. **Confirm the national bark coefficient for western larch.** Determine whether Ung et al. (2008) fitted an *occidentalis*-specific stem-bark parameter set, or western larch is estimated through a pooled/higher-taxon coefficient. This defines `nat_bark()` and shapes the expected bias. Source: the paywalled Ung 2008 tables or the NRCan biomass calculator.
3. **Run the analysis** once 1–2 are in: bias by diameter class, size-dependence test, species-specific recalibration with cross-validation, stand-level propagation. Replace all placeholder numbers.

## Then

Write Results from computed values; write Discussion and Conclusions; finalize Data availability; render docx/html and fix the style-doc/scss paths in the YAML if they error.

## Citation to-verify notes (bib)

Author lists or DOIs flagged in `references.bib`: `singh2022` (given names), `zhu2024` (co-authors), `broniz2016`/`halme2023` (issue), plus verify Silva Fennica volume numbers. "Ung & Lambert 2005" is the same paper as `@lambert2005` (CJFR 35:1996–2018), not a separate reference.

## Guardrails the user has set (carry these)

- Never disparage generalized/national equations; frame as trade-off and targeted refinement.
- No citations in the abstract.
- No fabricated numbers; placeholders must be labelled; sample sizes and results come from the real dataset.
- Edit the one master `.qmd`; archive superseded files, never overwrite in place.
