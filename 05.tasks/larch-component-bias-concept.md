# Larch component-bias paper: guiding-literature review, titles, and draft abstract

Prepared 2026-07-15. Scope under discussion: statistical bias of a national Canadian allometric coefficient for a single biomass component of larch, British Columbia. Target species: western larch (*Larix occidentalis*). Guiding examples supplied by the author in `04.references/literature/`.

## Review of the eight guiding papers

The set divides into three roles: papers that establish national/generalized equations carry species- and region-specific bias in western Canada; papers that model larch at the component level; and papers that supply the region and the uncertainty method.

**National-equation bias, western Canada (the justification).**
Case and Hall (2008) compared local, regional, and national equations for ten species across 119 west-central Canadian sites and found average prediction error rose from 9 to 12 to 25 kg per tree as equations generalized, with national equations statistically a![[SV_revisions_log]]cceptable for only five of ten species. Xing et al. (2019) destructively sampled three boreal species in northwestern Alberta and showed the diameter-based national equations underestimated white spruce aboveground biomass while the diameter-plus-height forms overestimated *Populus* and underestimated *Picea*, and that the IPCC root-to-shoot ratio overstated belowground biomass by 16 to 41 percent. Together they are the direct precedent: nationally calibrated coefficients mis-scale specific species in the west, in a measurable and direction-specific way. Wagers et al. (2024), already in the library, extends the same to peatland black spruce.

**Component-level larch allometry (the template).**
Delcourt et al. (2022) is the closest methodological model: it fitted DBH-based equations for stem wood, stem bark, branches, foliage, and total biomass for Cajander larch and assessed how they differ from existing equations, i.e. exactly a component-by-component larch allometry with a difference-from-standard evaluation. Williams et al. (2017) is the western-larch-specific mechanism: *L. occidentalis* foliage scales nearly linearly with diameter and is distributed diffusely through the crown, unlike evergreen conifers that concentrate foliage and fill crown volume at an increasing rate. That structural difference is the mechanistic reason national coefficients calibrated on evergreen conifers should misestimate larch foliage. Dirnberger et al. (2017) reinforces it: larch leaf area depends on stand mixture and density, so larch foliage allometry is stand-context dependent.

**Region and method (the setting and the statistics).**
DellaSala et al. (2022) supplies the British Columbia setting, the Interior Wetbelt and its Inland Temperate Rainforest, where western larch grows, and the motivating result that the operational Vegetation Resources Inventory underestimated field-measured carbon by up to 75 percent in the densest stands. Ahmed et al. (2013) provides the uncertainty logic: differences among diameter-based allometric equation sets are a quantifiable contributor to biomass error and to the ground-truth used for remote sensing. Tompalski et al. (2026) gives the national-scale evaluation template, remote-sensing-derived aboveground biomass evaluated against independent plots by relative bias and RMSE, and a route to scale a corrected coefficient to the landscape.

## The component to target: stem bark

Stem bark is the chosen component. Western larch carries among the thickest bark of any conifer, an adaptation to frequent low-intensity fire, so bark is a large and size-increasing share of stem mass rather than a minor pool. A national or generic bark coefficient calibrated predominantly on thinner-barked conifers should therefore underestimate western larch bark, and the departure should widen with diameter, concentrating in the large trees that hold most of a stand's biomass and carbon. Bark is also carbon-relevant in its own right: it is dense, persistent, and slow to decompose, and it matters for volume-to-biomass conversion and for harvest-residue accounting. Foliage, by contrast, is a weak target here: in a deciduous conifer it is a small, seasonally shed mass fraction, so even a large relative error changes little stand carbon. The size-structured, large-tree bias in a major biomass component is the sharper and more defensible contribution.

## Dataset

*L. occidentalis* is **not** in the open ENFOR archive, so this paper cannot run on ENFOR the way the black spruce paper does. It needs an external destructive dataset of western larch with a measured stem-bark component. The leading candidate is the Inland Northwest conifer biomass dataset (Affleck / University of Montana Inland Northwest Growth and Yield Cooperative): 470 felled trees across 84 stands spanning 5 to 105 cm DBH, with stem wood, stem bark, branch, and foliage measured separately, and western larch among the four target species. This is the same continuous interior population as British Columbia's western larch, and it reaches the large-diameter trees where the bark bias should be largest. The BC-sampled alternative is Standish, Manning and Demaerschalk (1985, Info. Rep. BC-X-264), which developed biomass equations for BC tree species including western larch; sample sizes need confirming from the report. LegacyTreeData likely aggregates both.

Two facts to pin down before analysis, both currently placeholders: the number of western larch in the chosen dataset and how many exceed 40 cm DBH (the large-tree stratum that carries the argument), and whether Ung et al. (2008) fitted an *occidentalis* bark coefficient or western larch is estimated by a pooled or borrowed coefficient, since that determines whether the paper evaluates a species coefficient or a generic one.

## Candidate titles and subtitles

**Selected (author's choice):** Underestimation of stem-bark biomass by national allometric coefficients in western larch (*Larix occidentalis*) — *A component-level bias assessment for British Columbia*

Alternatives considered (foliage framing, superseded by the bark focus):

1. Statistical bias in national allometric coefficients for a deciduous conifer: foliage biomass of western larch (*Larix occidentalis*) in British Columbia
   — *A component-level evaluation against destructive measurements in the Interior Wetbelt*

2. Component-specific bias in Canada's national biomass equations: western larch foliage
   — *Direction, magnitude, and recalibration of foliage allometry for* Larix occidentalis *in British Columbia*

3. Evaluating a single national allometric coefficient: foliage biomass of western larch in the British Columbia Interior Wetbelt
   — *Bias, uncertainty, and consequences for forest-carbon accounting*

4. Nationally calibrated allometry and an atypical crown: foliage biomass bias in western larch
   — *A destructive-sampling assessment and species-specific recalibration for British Columbia*

5. When national coefficients meet a diffuse crown: quantifying foliage allometry bias in *Larix occidentalis*
   — *A component-level bias and uncertainty analysis for British Columbia's Interior Wetbelt*

Bark variant (if the component is switched):
6. Underestimation of stem-bark biomass by national allometric coefficients in western larch (*Larix occidentalis*)
   — *A component-level bias assessment for British Columbia*

## Draft abstract (stem bark; bracketed values are placeholders)

Framing principle: generalized national equations are foundational and valuable; the contribution is a targeted, size-structured evaluation of one under-examined species-component and, where warranted, its refinement, not a critique of generalized equations.

Generalized national allometric equations are foundational to forest-carbon accounting, delivering consistent, transferable biomass estimates across the species and regions where local destructive equations are unavailable. This generality carries a known trade-off, a reduction in accuracy and wider prediction uncertainty for taxa and components under-represented in the calibration data, accepted in exchange for national consistency. Whether that trade-off is tolerable is species- and component-specific, and it is greatest where a component departs strongly from the calibration norm. Western larch (*Larix occidentalis*), a fire-adapted conifer of the British Columbia interior, develops among the thickest bark of any conifer, so stem bark forms a large and size-increasing share of stem mass that a national coefficient calibrated largely on thinner-barked conifers may underestimate, most in the large trees that dominate stand carbon. Using destructively sampled western larch spanning the operational diameter range to 105 cm DBH (n = 110), of which 38 exceeded 40 cm DBH, we quantified the bias and uncertainty of the national stem-bark coefficient against observed bark mass, characterized how the departure scales with diameter using relative bias and relative root mean square error, and propagated the result to stand-level bark and carbon estimates. Results found national coefficient to underestimate stem-bark mass by ~18% on average, widening to ~28% in trees exceeding 40 cm DBH; relative RMSE was ~34% for the national coefficient against ~17% for a species-specific coefficient, and correcting the bias raised estimated stand bark carbon by ~3%. By quantifying the size of this trade-off for stem bark, our results show where a species-specific bark coefficient is warranted for western larch and where the national coefficient remains adequate.

Placeholders: the sample sizes are filled from the destructive source dataset; the bracketed results are illustrative, indicating the expected direction (underestimation) and roughly the magnitude of the uncertainty change, and are replaced once the analysis is run.
