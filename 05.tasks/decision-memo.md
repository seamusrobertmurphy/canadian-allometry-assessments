# Decision Memo (v2): Direction, Venue, Dataset, and Headline Result

**To:** Author (Seamus Murphy)
**From:** claude-science-library writing team
**Date:** 2026-07-15
**Supersedes:** decision-memo v1 (same date), which weighed the framings before the direction was set
**Inputs folded in:** Task Request 1 (inputs and outputs), Task Request 2 (direction and order of work), and the examination of the ACR IFM Canadian methodology v1.0
**Companion files:** `annotated-bibliography.md`, `acr-methodology-citation-audit.md`

Task Request 2 asked for one thing first: a one-page memo fixing the four choices everything else follows from, the framing, the target journal, the open dataset, and the single headline result. Here they are, with the reasoning compressed behind them.

## The four choices

**Framing: technical commentary first (Task Request 1, Option A), the systematic review held as a second-stage expansion.** This matches Task Request 2's recommendation and v1's. The commentary lands a sharp, specific claim on a single open dataset, suits the origin, and can be grown into the review from the same bibliography if a venue wants it. The review is also gated by paywall access to the core CJFR papers, which the commentary is not, so leading with the commentary is the lower-risk path as well as the faster one.

**Target journal: Carbon Balance and Management, with Canadian Journal of Forest Research as the fallback.** Carbon Balance and Management fits on scope (carbon accounting and MRV integrity), is open access, which suits a manuscript deliberately stripped of confidential content, and already hosts the Vorster et al. 2020 uncertainty paper the argument leans on. CJFR is the alternative if a forest-science home is preferred over a carbon-policy one, at the cost of a paywall and a narrower readership. For the eventual review, hold Environmental Reviews.

**Open dataset: ENFOR destructive-biomass data as the spine, National Forest Inventory ground plots for the landscape step, Wagers et al. 2024 peatland data as the contrast set if archived with the paper.** All are open, national, and defensible. ENFOR is the actual sample the national equations were fitted on, which makes it the honest ground for a bias demonstration or a re-fit. The Clay Belt data stays private validation the reader never sees.

**Headline result: the national-versus-stratum-specific biomass gap for lowland peatland black spruce, expressed twice, as a carbon quantity and as an offset uncertainty deduction under the ACR Canadian IFM methodology.** One clean number, carried through to the credit consequence. The peatland stratum is where Wagers measured a roughly twelve percent national-model underestimate at the tree level and 13.6 percent at the plot level, and it is the stratum that dominates lowland boreal projects. Expressing the gap as both a per-hectare carbon quantity and an uncertainty deduction is what turns an allometry result into an MRV result.

## Why the ACR methodology examination sharpens all four

The citation examination gave the paper its regulatory anchor and firmed up the headline result. The methodology names the Canadian National Biomass equations (Ung 2008, Lambert 2005) as the "preferred equations" and admits a stratum-specific alternative only as an undefined option: "locally calibrated equations may be used when available and have undergone proper independent peer review." It is dated September 2021, so it cannot and does not cite the 2024 peatland evidence, and it cites no ecosystem-specific equation at all. That is the argument in one instrument: a live Canadian standard defaults to a nationally calibrated equation that the post-2021 record shows is biased low on the dominant project stratum, and leaves the correction optional and unspecified.

Two consequences for the choices above. It fixes ACR as the named standard for the headline result, because the methodology gives the exact machinery, an uncertainty-deduction rule keyed to the ACR ±10 percent precision requirement (its Equations 22 to 24) that a bias or an inflated uncertainty term feeds directly into as a credit haircut. And it hands the paper quotable, public, non-confidential text, the "preferred equations" and local-calibration clauses, so the regulatory hook rests entirely on an open document. A minor audit flag from the same examination, the methodology's biomass-to-carbon fraction of 0.5 against the IPCC 0.47 default, is worth a sentence in the paper but is not the thesis.

## Working thesis, restated for the manuscript

Nationally calibrated allometry trades ecosystem accuracy for national consistency and enforced component additivity. In atypical strata such as peatland conifer that trade is no longer defensible for carbon quantification without a bias correction or a stratum-specific equation, and the convenience of one national equation set has outrun its fitness for the stands where offsets are increasingly sited. The Fradette et al. 2021 finding disciplines the claim: national equations get the total roughly right in open woodlands and err in the components, so the paper asserts ecosystem-specific bias where it is measured, in peatland black spruce, not across all atypical stands.

## Order of work from here (Task Request 2)

Secure and profile ENFOR plus NFI before any analysis, confirming the peatland or lowland black spruce records the comparison needs are present. Reconstruct the equation comparison on that open data, national versus stratum-specific or bias-corrected. Quantify the one headline result as a carbon quantity and an ACR uncertainty deduction. Draft the commentary around it. Clear confidentiality last, confirming no Clay Belt identifiers, plot data, or derived figures remain.

## Non-negotiables carried forward

The Clay Belt origin is motivation only and is never named or shown. The published claim rests entirely on open, citable data with a data-availability statement. Every paywalled primary source (Lambert 2005, Ung 2008, Wagers 2024, Parresol 2001) is read in full through institutional access before it is characterised, not paraphrased from abstracts. This is the one standing dependency: the review stage cannot responsibly start until that access is in hand, and even the commentary's characterisations of those four papers should be upgraded from abstract to full text before submission.

## Still open for the author

Whether a modest re-fit or only a bias quantification is in scope for the commentary. Whether to secure CJFR full-text access now to keep the review stage on schedule. Whether anyone on the verification team is owed co-authorship or acknowledgement given the origin. None of these blocks acquiring ENFOR and drafting the methods, which is the next step.
