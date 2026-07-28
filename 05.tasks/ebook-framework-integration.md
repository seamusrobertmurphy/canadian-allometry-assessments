# Integrating the uncertainty ebook's allometry framework into the paper

Source reviewed: `training/uncertainty`, chapter 1 (Allometry), the author's own prior work. This memo maps that chapter's method and design onto the Canadian allometry paper, says what to adopt unchanged, what to adapt, and what the paper adds beyond the ebook. Prepared 2026-07-15.

## What the ebook already gives us

The chapter is a complete uncertainty-to-deduction pipeline for allometric carbon accounting, built and coded in R. Its spine, in the order it runs: frame model choice as money (RMSE drives the credit deduction drives dollars); classify equations by scope (species, genus, biome-generic, environmentally-conditioned) and select them by a four-criterion hierarchy (geographic proximity, taxonomic specificity, DBH-range coverage, sample size); test the distribution (skew, kurtosis, Shapiro-Wilk) and the variance structure (Breusch-Pagan) to justify a log transform; optimise by log-transformation with disciplined back-transformation and a DBH-class-stratified split; cross-validate out-of-sample with 100-iteration Monte Carlo leave-group-out; then convert relative RMSE into an ART-TREES Equation 11 deduction and a revenue figure.

That is, in miniature, the exact machine our paper's headline result needs. The paper does not have to invent the uncertainty-to-credit chain; it inherits it and points it at a different contrast.

## Adopt unchanged

Three elements port directly and I have started wiring them into the analysis code.

The back-transformation discipline is already in our fitting module: the ENFOR fit uses a log-log model with the Baskerville/Sprugel correction, which is the ebook's central methodological insistence. Keep it and cite the rationale the ebook lays out.

The deduction mapping is now coded (`analysis/R/deductions.R`). The ART-TREES Equation 11 function reproduces the ebook exactly, verified against its worked examples (15.2 percent relative RMSE gives a 4.85 percent deduction, 18.9 percent gives 6.03 percent). This is what turns our relative-RMSE number into the credit consequence the paper promises.

The distributional and heteroscedasticity diagnostics (Shapiro-Wilk, Breusch-Pagan) should be run on the ENFOR black spruce exactly as the ebook runs them, both because they justify the log form and because they are documentation the MRV reader expects.

## Adapt

Two elements need a change of axis or standard.

The contrast axis differs. The ebook compares species versus genus versus pan-tropical generic equations on one stand. Our paper compares the national equation against an ecosystem-specific (peatland) equation on the national black spruce sample. Same design, different question: not "how specific is the taxonomy" but "how specific is the ecosystem calibration". The ebook's four-criterion selection hierarchy is still the argument, but for us it becomes the case that a peatland stratum-specific equation should be selected over the national default, because geographic and ecological proximity and small-tree DBH coverage are exactly where the national set fails. That reframing also connects to the ACR methodology's "locally calibrated equations may be used when peer reviewed" clause: the ebook's selection logic is the technical content of that clause.

The deduction standard differs, and this is the sharper divergence. The ebook maps uncertainty through ART-TREES Equation 11. Our paper is anchored on the ACR IFM Canadian methodology, whose deduction rule (Equations 22 to 24, keyed to the plus-or-minus 10 percent precision requirement) is different in both form and input. ART-TREES takes the allometric relative RMSE more or less directly; ACR takes a propagated total project uncertainty. I have coded both in `deductions.R`, with the ACR threshold and floor flagged as unverified pending a clean read of the methodology (the source PDF renders those digits ambiguously). Presenting the same allometric error under both standards is itself a result: it shows the credit consequence is standard-dependent, and it lets the paper speak to an ACR audience while staying legible to the larger ART-TREES and VCS readership the ebook targets.

## Extend beyond the ebook

The paper's genuine addition is the component and additivity dimension. The ebook works with whole-tree aboveground biomass and a single power law. The national equations are component models (wood, bark, branches, foliage) fitted by nonlinear seemingly-unrelated regression under an additivity constraint, and our analysis already fits them componentwise. So the paper extends the ebook's framework from whole-tree AGB into the additive-component setting, and can ask the question the ebook never had to: does the additivity constraint that makes the national equations attractive cost accuracy in the atypical stratum, and is the sum, which is what the carbon account needs, worth that cost. That is new, and it is the paper's own contribution on top of the inherited machine.

A second extension is spatial. The ebook stratifies by DBH class as a size proxy. Our paper replaces that proxy with a soil-based peatland stratum from the planned overlay, which is a stronger and more defensible stratification than size alone. The ebook's stratified-split discipline still applies; only the stratifying variable improves.

## Concrete changes to our R analysis

Done: back-transformation with correction factor (in `02_national_equation.R`), and the deduction module (`deductions.R`, ART-TREES verified, ACR parameterised and flagged).

Next, to align fully with the ebook: replace the plain 5-fold cross-validation in `03_fit_and_bias.R` with 100-iteration Monte Carlo leave-group-out stratified by DBH class, matching the ebook's regime; add the Shapiro-Wilk and Breusch-Pagan diagnostic block on the black spruce; and add a small reporting step that runs the fitted relative RMSE through `deductions.R` for a stated Canadian project size, producing the paper's money sentence under both ACR and ART-TREES.

## On citing the ebook

The chapter is the author's own and is grey literature, so the paper should reuse its framework and cite the primary methods it rests on (Roxburgh 2015 for sample size, Duncanson 2021 for protocol, the ART-TREES standard for Equation 11, Chave for the generic comparison), rather than cite the ebook as authority. The ebook can be acknowledged as the methodological antecedent, or released as a companion training resource the paper points to for the full worked pipeline. Either keeps the provenance clean while letting the paper stand on peer-reviewed sources.
