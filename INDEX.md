# Repository Index: Canadian tree allometry paper

Map of this repository. Numbered `NN.name` top-level folders; every folder keeps an `archive/` subfolder for superseded material. Updated 2026-07-15.

## Master file

The canonical manuscript is **`01.manuscript/canadian-allometry-forest-science.qmd`**. Always edit that file; it is the single source of truth for the paper. Renders and older drafts live beside it or in `01.manuscript/archive/`.

**The manuscript is executable, and the analysis is now R.** As of 2026-07-27 the whole
pipeline is R code in the manuscript's `# Analysis` section: all four stages were ported
from Python and now run as chunks when the document is rendered, writing
`03.outputs/tables/T1..T11*.csv` and `03.outputs/figures/F1..F9*.png`, which the Tables
and Results sections then read. Prose and numbers cannot drift. Shared formatters (`sp`,
`fp`, `cnt`, `tg`, `dash`) and the shared statistics (`metrics`, `linreg`, `skew_p`,
`kurt_p`) live in the setup chunk.

Render with `quarto render 01.manuscript/canadian-allometry-forest-science.qmd`. It needs
**only R** (4.4.1, `knitr`) — base R and `stats`, no external package, no Python, no
reticulate, and no network: all four inputs are cached under `02.inputs/`. A full render
takes about 20 seconds. Every random draw (bootstrap intervals, cross-validation folds,
Monte Carlo propagation) is seeded, so the reported numbers reproduce exactly.

The R port was verified table by table against the Python outputs it replaces: every
deterministic quantity matches to machine precision. Four stochastic values shifted
slightly, as different RNG streams require, and the prose was updated to match — see
"Known reconciliation items" below.

> **The code is part of the manuscript. Never hide it.** Every chunk carries an explicit
> `#| echo: true`. The analysis chunks add `#| output: false` rather than `include: false`,
> so the code shows while the pipeline chatter does not; the eleven table chunks show both
> code and output. The html format sets `code-fold: false`, `code-tools` and `code-link` for
> the same reason. On 2026-07-22 a change added `echo: false` to all eleven table chunks and
> stripped every line of R out of the rendered document; it was reverted the same day
> (`f1368b7`). Do not repeat it. If the code ever needs hiding for a specific submission,
> ask first and do it in a branch.

## Layout

| Folder | Holds | Key files |
|---|---|---|
| `01.manuscript/` | The master manuscript and its render | `canadian-allometry-forest-science.qmd` (MASTER), `.docx` render, `references.bib` |
| `02.inputs/` | Data and analysis code | `README-data.md` (**manifest: what is and is not in git**); `enfor/`, `legacy-tree/`, `vri/`; `scripts/` (the four stages, plus the legacy R pipeline) |
| `03.outputs/` | Generated results | `RESULTS-note-stage1-v1.md`, `-stage1b-v1.md`, `-stage2-v1.md`; `tables/` (T1-T11), `figures/` (F1-F9) |
| `04.references/` | Bibliography, styles, literature | `references.bib`, `springer-basic-author-date.csl` (**the live style**; `apa.csl` is superseded), `style-formal.docx`, `literature/` (**not in git**, copyrighted PDFs) |
| `05.tasks/` | Planning and scoping memos | `TASK-REQUEST-2026-07-22-v2.md` (**current**), affleck-data-request-draft, manuscript-design-spec, decision-memo, annotated-bibliography, dataset-inventory |

## Analysis pipeline (in the manuscript)

Four stages of R, run in document order as chunks of
`01.manuscript/canadian-allometry-forest-science.qmd`. There is no separate script to run:
rendering the manuscript *is* running the pipeline.

| Stage | Chunk labels | Produces |
|---|---|---|
| 1 | `s1-coefficients`, `s1-data`, `s1-accuracy`, `s1-refit`, `s1-normality`, `s1-figures` | accuracy, refits, CV, normality; T1-T5, F1-F4 |
| 1b | `s1b-load`, `s1b-stats`, `s1b-figure` | bark geometry, scaling exponents, robustness; T8-T9, F8 |
| 2 | `s2-vri`, `s2-carbon`, `s2-figures` | province-wide application, Monte Carlo; T6-T7, F5-F7 |
| 2b | `s2b-comparator`, `s2b-figure` | Affleck 2019 comparator, three-equation bracket; T10-T11, F9 |

`02.inputs/scripts/` now holds only superseded material. The four Python stages that
produced these outputs before the port live in `02.inputs/scripts/archive/`; the older
black-spruce R pipeline (`run_all.R`, `R/*.R`, `verify_python_mirror_v2.py`) predates the
two-stage design. Neither produces the current tables.

## Archiving policy (strict)

When a file is superseded or updated, move the old version into that folder's `archive/` subfolder rather than deleting or overwriting in place. Every numbered folder and `02.inputs/scripts/` has an `archive/`. Already archived: `02.inputs/scripts/archive/verify_python_mirror.py` (v1, superseded by v2).

## Target venue

**Forest Science**, Society of American Foresters, published by **Springer Nature**.
Corrected 2026-07-22. The journal left Oxford Academic; SAF named Springer Nature its
publisher and the first Springer issues appeared January 2025, so the Oxford Academic
author instructions describe the *former* publisher and do not apply. Anything gathered
from Oxford (its "Study Implications" section, its 200-word abstract, its double-blind
policy) is superseded. Guidelines live at
`https://link.springer.com/journal/44391/submission-guidelines`.

The venue choice itself still supersedes the Carbon Balance and Management decision in
`05.tasks/decision-memo.md`, made under the earlier commentary-and-peatland framing.

A saved copy sits at `04.references/Submission guidelines | Forest Science | Springer
Nature Link.pdf`, but **it is 43 blank pages** — the print-to-PDF captured no text layer,
no fonts and no images. Do not rely on it; fetch the live page.

### What Springer requires, and where the draft stands

| Requirement | Draft as of 2026-07-27 |
|---|---|
| Original article ≤ **10,000 words including figures, tables and references** | **13,250 words in the rendered docx. BLOCKING.** Prose, captions and references are 8,160 and within the limit; the 5,090 words of displayed R code carry it over. Showing the code is a deliberate decision (see the "never hide it" note above), so resolving this is a **submission-packaging** question, not a licence to set `echo: false`: the usual route is to move the Analysis section to supplementary material or a cited code repository for the submitted copy, keeping the executable master intact. **Ask before choosing.** |
| **≤ 10 figures and tables in total** | **20 (11 tables, 9 figures). BLOCKING.** |
| Abstract **150-250 words** | **431 words. BLOCKING.** |
| **4-6 keywords** | 5, fixed 2026-07-22 |
| Citation: Springer author-date, name and year in parentheses | `springer-basic-author-date.csl`, installed 2026-07-22 |
| Submit as `.docx`; editable source files required | docx format already the target |
| **No line numbering** | none present |
| Word counts declared at end of manuscript (total incl. refs, total excl. refs, abstract, SI) | not yet added |
| Acknowledgements on the **title page**, not in the body | not yet written |
| **`Declarations` section before the references**, covering Funding, Competing interests, Ethics approval, Consent, Data/Material/Code availability, Authors' contributions | not yet written |
| Separate title page with affiliations, corresponding-author email, ORCID | author block still in the YAML |
| ORCID required for the corresponding author at submission | present in YAML |

## Scope (current decisions)

Genus-level larch (*Larix*) stem-bark bias, component-level (stem bark). Two open destructive datasets: tamarack (*L. laricina*) from ENFOR (in-sample, the national calibration data) and western larch (*L. occidentalis*) from LegacyTreeData (independent). Headline: the generic conifer coefficient underestimates western-larch stem bark ~47% while over-predicting tamarack ~19%; the two larches diverge, so a species-specific western-larch coefficient is warranted and a genus-pooled one is not. Decided 2026-07-16 (Option C, species-divergence framing). Superseded framings (black spruce peatlands; western-larch-only) live in the relevant `archive/` folders.

Extended 2026-07-21 with two validation stages. Stage 1b confirms the species divergence on
independent taper trees to 39.4 cm and puts the bark-area exponent at 2.56 for western larch
against 1.36 for tamarack. Stage 2b applies the published Affleck (2019) western-larch
equation, fitted to 105 cm, as an external comparator. **The provincial correction is now
reported as a bracket, +37 to +60 percent (1.2 to 1.9 Tg C), not a point estimate.**

## Exemplar papers (what the manuscript is modelled on)

Fixed in `05.tasks/manuscript-design-spec.md`. All three PDFs are in `04.references/literature/`.

| Paper | Journal | Supplies |
|---|---|---|
| Delcourt et al. 2022 | Biogeosciences | Statistical apparatus and component-equation table format |
| Xing et al. 2019 | Can. J. For. Res. | Accuracy-and-uncertainty assessment by component |
| DellaSala et al. 2022 | Ecosphere | Province-wide VRI application; **sets the scale target**, ~8,000 words, 7 tables, 7 figures |

Note: the Xing PDF is filed under a misspelled name in some older listings. The first author
is **Dingliang Xing**; the bib key `xing2019` is correct.

Similarly, `04.references/literature/Ung & Lambert 2005 National Canadian allometrics.pdf`
is **Lambert, Ung & Raulier 2005** (CJFR 35:1996-2018), not an Ung paper. Ung, Bernier &
Guo 2008 (CJFR 38:1123-1132) is a different paper and is **not in the repository**. The
distinction matters: the tamarack coefficients come from Lambert 2005 and the generic
conifer coefficients from Ung 2008.

## Known reconciliation items

- **Reference doc is Elsevier, by the author's choice.** The master YAML points at
  `../04.references/style-elsevier-quarto.docx` (switched 2026-07-27, superseding the
  Springer reference doc used on 2026-07-22). `style-springer-quarto.docx` is still in the
  folder. Do not "fix" this back without asking; the CSL is separate and remains
  `springer-basic-author-date.csl`.
- Canonical bibliography is `04.references/references.bib` (single copy); ENFOR is cited as `@enfor2017`.
- **Four stochastic numbers moved in the 2026-07-27 R port** and the prose was updated to
  match. R's RNG cannot reproduce NumPy's stream, so the seeded draws differ: tamarack
  cross-validated relative RMSE 27.5 → **27.6** (ten-fold shuffle); the western-larch
  bark-share bootstrap interval 21.5-27.4 → **21.5-27.5** and tamarack's 12.2-14.4 →
  **12.3-14.4**; the western-larch Monte Carlo interval 1.9-11.2 → **2.1-11.5 Tg C**. Two
  further prose figures were corrected against the pipeline rather than changed by it: the
  tamarack `<20 cm` bias reads **10.1%** (the Python table always said 10.148; the prose had
  rounded to 10.2), and the western-larch bias bootstrap lower bound is **-49.3%**, not
  -49.2. The bark-fraction SD for western larch is **3.0**, not 2.9. Every deterministic
  quantity is unchanged and was diffed table by table against the Python outputs.
- **Figure 6 has no basemap.** It plots VRI polygon label centroids as a bare scatter in BC
  Albers with no province outline, so nothing orients the reader (chunk `s2-figures` in the
  manuscript). A boundary is now available at
  `02.inputs/vri/bc_boundary_3005.geojson` (48 KB, Natural Earth 1:50m admin-1, public
  domain, dissolved to British Columbia and reprojected to EPSG:3005, simplified 500 m).
  It reads with `jsonlite`, so plotting it adds one common dependency. **Not yet
  wired into any figure.**
- **Figure 9b overstates what it shows.** Both curves are deterministic ratios of power
  laws, not data (chunk `s2b-figure` in the manuscript). `refit/national` reduces exactly to
  `3.076 d^-0.1855`; `Affleck/national` reduces to about `0.266 d^0.468` once the fitted
  height relation `h = 1.737 d^0.783` is substituted. Three problems: the caption claims
  both exceed the national coefficient across the operational range, but Affleck sits
  *below* it until **17.8 cm** and reads 0.60 at 6 cm; the grid starts at 6 cm while the
  VRI western-larch stands run **13.9 to 111.0 cm** QMD, so the left third of the panel
  describes stands that do not exist; and panel (a) shades its extrapolation while panel
  (b) shades nothing. The two ratio curves cross at 43.9 cm, which is what the caption's
  "near 45 cm" refers to and is correct.
- Large-tree bark mass is **resolved** as of 2026-07-21. Affleck (2019, FEM 432:179-188), a
  PDF already in `04.references/literature/`, publishes a western-larch (LAOC) stembark
  equation, `0.001910 d^1.636 h^1.332`, fitted within a 470-tree sample to 105 cm. Stage 2b
  (chunk `s2b-comparator`) applies it province-wide as an
  independent comparator: it confirms the direction of the bias and brackets the provincial
  correction at +37 to +60 percent. It exceeds our refit above 45 cm, so our extrapolation is
  the conservative one in large trees. Remaining gap is the component definition (Affleck is
  30 cm stump to 5 cm top), not the diameter range.
- Large-tree size-dependence in bark *geometry* is **partly resolved** as of 2026-07-21. Stage 1b
  (chunks `s1b-*`, `03.outputs/RESULTS-note-stage1b-v1.md`) uses
  LegacyTreeData stem taper to measure bark geometry on an independent western-larch sample to
  39.4 cm, confirming the species divergence and putting the bark-area exponent above isometry.
  It is geometry, not mass, so destructive bark mass across the operational diameter range is
  still the priority: see `05.tasks/affleck-data-request-draft.md` (drafted, **not yet sent**).
