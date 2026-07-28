# Annotated Bibliography: Open Questions in Canadian National Tree Allometry

Shared evidence base for the planned paper on the applicability of the Canadian national aboveground biomass equations to lowland peatland black spruce, and on how allometric model choice propagates into carbon-credit quantities. Serves both candidate framings (Option A commentary, Option B review). Prepared 2026-07-15 for the `claude-science-library` writing team. Origin: ACR1235 Clay Belt IFM verification, all confidential project material excluded.

Each entry gives the verified citation, a compact description, and the relevance to the paper's argument. Verification notes flag where the handoff task request needs correcting.

---

## A. The equations in dispute

**Lambert, M.-C., Ung, C.-H., Raulier, F. 2005. Canadian national tree aboveground biomass equations. Canadian Journal of Forest Research 35(8): 1996–2018.** https://doi.org/10.1139/x05-112

The national model itself. Fitted to roughly 9,500 destructively sampled trees from the 1980s ENFOR archive, covering all of Canada except British Columbia. Biomass is split into four components, foliage, branches, stem wood, and stem bark, each a function of diameter (and optionally height), with the components constrained to sum to total and the error dependence among components of the same tree carried into both the parameter estimates and the prediction variance. This additivity, achieved by nonlinear seemingly unrelated regression, is the feature the paper interrogates. Relevance: the primary object of the dispute. Its national calibration is the null hypothesis the peatland evidence tests.

**Ung, C.-H., Bernier, P., Guo, X.-J. 2008. Canadian national biomass equations: new parameter estimates that include British Columbia data. Canadian Journal of Forest Research 38(5): 1123–1132.** https://doi.org/10.1139/X07-224

The revision that folds in the recovered BC ENFOR data and reports updated parameter estimates. Supplies both the diameter-only and the diameter-plus-height forms. Relevance: fixes which parameter set the workbook should use, and frames the diameter-only versus diameter-plus-height question directly, since both forms trace to this paper.

**Li, Z., Kurz, W.A., Apps, M.J., Beukema, S.J. 2003. Belowground biomass dynamics in the Carbon Budget Model of the Canadian Forest Sector: recent improvements and implications for the estimation of NPP and NEP. Canadian Journal of Forest Research 33(1): 126–136.** https://doi.org/10.1139/x02-165

Source of the root-to-shoot relationships used across Canadian carbon accounting: softwood belowground biomass proportional to aboveground biomass, hardwood belowground biomass a power function of aboveground biomass. Relevance: the belowground layer of the workbook stack, and a reminder that root biomass inherits every error in the aboveground estimate it is scaled from, which matters for the propagation argument. Verification note: the task request gave an abbreviated title and left the citation to confirm. This is the correct published record, CJFR 33(1): 126–136, doi:10.1139/x02-165. Confirm the exact coefficient values (task memory records hardwood BGB = 1.576·AGB^0.615, softwood BGB = 0.222·AGB) against the paper or the CBM-CFS3 documentation at drafting.

## B. The additivity method

**Parresol, B.R. 2001. Additivity of nonlinear biomass equations. Canadian Journal of Forest Research 31(5): 865–878.** https://doi.org/10.1139/x00-202

The methodological reference for enforcing additivity when component equations are nonlinear, via the seemingly-unrelated-regression approach the national equations adopt. Relevance: grounds the "additivity versus fit" thread. To argue that additivity buys internal consistency at a possible cost in accuracy far from the national mean, the paper must state clearly what additivity is and why it was imposed. This is that citation.

**Reed, D.D., Green, E.J. 1985. A method of forcing additivity of biomass tables when using nonlinear models. Canadian Journal of Forest Research 15(6): 1184–1187.**

Earlier statement of the additivity problem and one solution, using generalized least squares to force component sums to total. Relevance: gives the historical depth a review needs and shows additivity as a long-standing modelling choice rather than a Lambert-specific quirk. Verification note, important: the handoff paired Reed and Green with DOI 10.5558/tfc46402-5, but that DOI resolves to a different paper, Kozak, A. 1970, Methods for ensuring additivity of biomass components by regression analysis, The Forestry Chronicle 46(5): 402–405. Two separate additivity references were conflated. Both are legitimate and citable; use the corrected Reed and Green 1985 CJFR record above, and cite Kozak 1970 separately if the historical methods lineage is wanted.

**Kozak, A. 1970. Methods for ensuring additivity of biomass components by regression analysis. The Forestry Chronicle 46(5): 402–405.** https://doi.org/10.5558/tfc46402-5

The earliest of the additivity-methods references, and the paper the handoff DOI actually points to. Relevance: optional deep-lineage citation for Option B, establishing that forcing additivity by regression predates the nonlinear treatments by three decades.

## C. Ecosystem-specific bias and the newer equations

**Wagers, S., Castilla, G., Voicu, M., Rea, T., Sanchez-Azofeifa, G.A. 2024. New aboveground biomass equations by components for small black spruce in peatland ecosystems of Western Canada. Canadian Journal of Forest Research 54(2): 207–223.** https://doi.org/10.1139/cjfr-2023-0031

The strongest and most Clay-Belt-relevant source. New component equations (stem, branches, needles) built from 495 destructively sampled small black spruce across 56 plots in western Canadian treed peatlands. At the tree level the new models predict total biomass with relative bias of +1% against about –12% for the national model, and relative RMSE of 30% against 35%. At the plot level, where it matters for an estate, relative bias is +3.5% against –13.6% national, and relative RMSE 15.9% against 18.6%. The new equations hold up outside their own calibration set. Relevance: this is the quantitative spine. A roughly 12 to 14 percent national-model underestimate on the dominant peatland stratum is material to any carbon-credit quantity, and it converts the dispute from opinion into a measured effect. Verification note: the handoff cited this as "2023"; the DOI carries the 2023 submission stub but the paper published in 2024, volume 54, issue 2. Cite it as 2024.

**Fradette, O., Marty, C., Tremblay, P., Lord, D., Boucher, J.-F. 2021. Allometric equations for estimating biomass and carbon stocks in afforested open woodlands with black spruce and jack pine, in the Eastern Canadian boreal forest. Forests 12(1): 59.** https://doi.org/10.3390/f12010059

Parallel evidence from 167 trees across seven open woodlands in Quebec. The finding is more two-sided than the handoff implied: the national equations predict whole-tree aboveground biomass for black spruce and jack pine accurately, but underestimate branch biomass, attributed to open-woodland tree form. Adding height improves compartment fits but changes stand-level carbon little. Relevance: extends the geography of the concern to the eastern boreal and sharpens the argument by locating the national model's error in the components rather than the total. It also disciplines the thesis: in open woodlands the total is roughly right, so the paper should claim ecosystem-specific bias where it is measured, in peatland black spruce, not blanket it across all atypical stands. Verification note, important: the handoff attributed this paper to "Ali et al. 2021." The correct first author is Fradette. Use Fradette et al. 2021 throughout.

## D. Uncertainty propagation

**Vorster, A.G., Evangelista, P.H., Stovall, A.E.L., Ex, S. 2020. Variability and uncertainty in forest biomass estimates from the tree to landscape scale: the role of allometric equations. Carbon Balance and Management 15: 8.** https://doi.org/10.1186/s13021-020-00143-6 (PMC7227279)

Quantifies how much of landscape biomass-map uncertainty originates in the allometric equation itself: depending on equation and evaluation method, allometric uncertainty contributes 30 to 75 percent of total uncertainty, rivalling or exceeding remote-sensing model error, and local equations are generally most accurate. Relevance: the load-bearing citation for the propagation thread. It establishes, in the peer-reviewed record, that equation choice is a first-order and often dominant uncertainty term, which is exactly why a stratum-specific versus national comparison translates into a real offset-uncertainty deduction. Verification note: this is a US conifer study (ponderosa and lodgepole pine), so cite it for the general magnitude of the allometric uncertainty share, and carry the Canadian-specific propagation as the paper's own worked result rather than leaning on Vorster for the Canadian numbers.

## E. The national accounting alternative and underlying data

**Boudewyn, P., Song, X., Magnussen, S., Gillis, M.D. 2007. Model-based, volume-to-biomass conversion for forested and vegetated land in Canada. Canadian Forest Service Information Report BC-X-411, 112 pp.** https://cfs.nrcan.gc.ca/publications?id=27434

The volume-to-biomass pathway used in national carbon accounting (CBM-CFS3, the National Forest Inventory) in place of tree-level allometry. Builds empirical volume-to-biomass models from inventory plot data and look-up tables for non-treed vegetation. Relevance: the review owes a comparison of the two national pathways, tree-level allometry versus volume-to-biomass, and where they diverge in lowland conifer. Less central to a tight commentary, essential to Option B.

**ENFOR destructive biomass dataset. Government of Canada open data portal.** https://open.canada.ca/data/en/dataset/fbad665e-8ac9-4635-9f84-e4fd53a6253c

The actual trees the national equations were fitted on, height, diameter, and component biomass for the archival sample. Fully open. Relevance: the first-choice replacement dataset. It permits a re-fit or a direct bias demonstration on non-confidential data, and it is the defensible substitute for the Clay Belt plots the manuscript cannot use.

**Natural Resources Canada, Canadian Forest Service. Biomass and nutrients calculator.** https://apps-scf-cfs.rncan.gc.ca/calc/en/biomass-calculator

Web implementation of the national equations. Relevance: a reproducibility check for the workbook's aboveground layer and a convenient way to generate national-model predictions for the comparison without re-coding the equations.

**Paré, D., et al. 2013. Estimating stand-scale biomass, nutrient contents, and associated uncertainties for tree species of Canadian forests. Canadian Journal of Forest Research.** Open PDF on the NRCan server: https://apps-scf-cfs.rncan.gc.ca/calc/static/files/Pare_et_al_biomass_and_nutrients_for_Canadian_forests_CJFR_2013.pdf

Stand-scale application of the national equations with associated uncertainties, openly available. Relevance: a worked, citable example of scaling the national equations to the stand with uncertainty, useful as a template and as an open full-text source given the paywall constraints noted below.

---

## Access note

General web search surfaced every primary source above with correct identifiers. Full text behind the Canadian Journal of Forest Research paywall (Lambert 2005, Ung 2008, Wagers 2024, Parresol 2001) cannot be retrieved through the current tooling; abstracts, the open Paré 2013 and Fradette 2021 papers, and the NRCan calculator are reachable. Reading the four paywalled papers cover to cover, which Option B in particular requires, needs institutional or personal library access. This is the single largest tooling gap for the review framing and a reason the commentary is the lower-risk first deliverable.

The biomedical connectors (PubMed, bioRxiv, ClinicalTrials, ChEMBL) do not index forestry and returned nothing useful; do not rely on them for this topic.

---

## Additional references — western larch stem-bark paper (added 2026-07-15)

Foundational compilations and reviews of the allometric literature, plus statistical and mensuration references, sourced by the author for the larch bark manuscript.

**Ter-Mikaelian, M.T., Korzukhin, M.D. 1997. Biomass equations for sixty-five North American tree species. Forest Ecology and Management 97(1): 1–24.** https://doi.org/10.1016/S0378-1127(97)00019-4
Compiles 803 biomass equations of the power form M = aD^b for 65 North American species, tabulating total, stem wood, stem bark, foliage, and branch components with DBH range, sample size, R², fitting method, and the log-bias correction factor. The canonical North American source establishing the power form and the diversity of species- and component-specific equations, stem bark included. Relevance: the baseline reference for the bark power model, and a candidate source of published western larch bark equations for comparison.

**Zianis, D., Muukkonen, P., Mäkipää, R., Mencuccini, M. 2005. Biomass and stem volume equations for tree species in Europe. Silva Fennica Monographs 4, 63 pp.**
Compiles 607 biomass and 230 volume equations for European species, noting that most biomass equations are for aboveground components and rest on few sites and small samples. The European counterpart to Ter-Mikaelian, canonical for the heterogeneity and data-limitation of allometric equations. Relevance: anchors the point that biomass equations are numerous but uneven, which both motivates generalized equations and demands their evaluation. Author-flagged as central.

**Sileshi, G.W. 2014. A critical review of forest biomass estimation models, common mistakes and corrective measures. Forest Ecology and Management 329: 237–254.**
A critical review cataloguing recurrent statistical errors in biomass models: arbitrary analytical choices, model dredging, ignoring collinearity, misuse of R² and AIC, and neglect of model uncertainty. Relevance: the statistical-rigor reference; disciplines our bias and uncertainty evaluation, our handling of the log transformation, and our treatment of coefficient error.

**Temesgen, H., Affleck, D., Poudel, K., Gray, A., Sessions, J. 2015. A review of the challenges and opportunities in estimating above ground forest biomass using tree-level models. Scandinavian Journal of Forest Research 30(4): 326–335.** https://doi.org/10.1080/02827581.2015.1012114
A modern review of tree-level biomass estimation and its uncertainties, co-authored by D. Affleck, the lineage behind the Inland Northwest destructive dataset. Relevance: frames the tree-level modelling problem our paper sits in, and links directly to the destructive-data group.

**Sprugel, D.G. 1983. Correcting for bias in log-transformed allometric equations. Ecology 64(1): 209–210.** https://doi.org/10.2307/1937343
The two-page note deriving the correction factor CF = exp(SEE²/2) that removes the systematic underestimation introduced when mass is predicted from a log-transformed regression. Relevance: the methodological citation for the back-transformation correction applied in our species-specific recalibration.

**Bronisz, K., Zasada, M. 2016. Empirical equations for estimating aboveground biomass of young silver birch (Betula pendula Roth.). Silva Fennica 50(4).** https://doi.org/10.14214/sf.1559
Additive biomass equations for young silver birch fitted by seemingly-unrelated regression to enforce additivity, with diameter-only and diameter-plus-height variants and separate small- and large-tree models. Relevance: methodological precedent for additive component equations, diameter-plus-height forms, and size-class splitting.

**Grote, R. 2002. Foliage and branch biomass estimation of coniferous and deciduous tree species. Silva Fennica 36(4): 779–788.** https://doi.org/10.14214/sf.520
A method for estimating crown (foliage and branch) biomass from sample-branch allometry, illustrated on Norway spruce and beech. Relevance: crown-component allometry methodology, useful contrast to the stem-bark focus and for any component beyond bark.

**Halme, E., et al. 2023. Improved parametrisation of a physically-based forest reflectance model. Silva Fennica 57(1).** https://doi.org/10.14214/sf.22028
Improves a physically-based forest reflectance model using Sentinel-2 and examines how uncertain structural inputs propagate to modelled reflectance. Relevance: connects biomass and structure allometry to remote-sensing retrieval and input uncertainty; peripheral, supporting the operational-scaling thread alongside Tompalski and Ahmed.

**Curtis, R.O., Marshall, D.D. 2000. Why quadratic mean diameter? Western Journal of Applied Forestry 15(3): 137–139.**
Explains why forestry uses quadratic mean diameter rather than the arithmetic mean as the stand average of tree diameter. Relevance: the mensuration convention underpinning the diameter summary used in our stand-level propagation.

_Bibliographic verification note: a few volume/issue/DOI fields for the Silva Fennica and review items are marked to verify in `references.bib`._
