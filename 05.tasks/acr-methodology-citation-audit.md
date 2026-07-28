# Citation Examination: ACR IFM on Canadian Forestlands, v1.0 (September 2021)

What the methodology cites, whether it cites it correctly, and what it does not cite that the current science and this audit require. Prepared 2026-07-15 as part of the Clay Belt (ACR1235) verification and the companion allometry paper. Source examined: `ACR-IFM-Canada-Methodology-v1.0.pdf`, 60 pages, 44 numbered footnotes.

## How the methodology cites

The document has no consolidated reference list. Every citation is a numbered footnote on the page where it is used, forty-four in total. Some are literature references, the rest point to standards (ISO 14064-2, the IPCC guidance) or are explanatory notes. The same works are re-cited under new footnote numbers when they recur, so Ung 2008 and Lambert 2005 each appear twice (footnotes 17 and 22, 18 and 23). For a verifier this matters: there is no single page to check the reference base against, and confirming any cited value means locating the footnote at its point of use.

## The citations that govern this audit

The biomass quantification rests on a short, specific chain of citations. These are the ones the verification turns on.

| Footnote | Work | Role in the methodology |
|---|---|---|
| 17, 22 | Ung, C.-H., Bernier, P.Y., Guo, X. 2008. Canadian national biomass equations: new parameter estimates that include British Columbia data. Can. J. For. Res. 38:1123–1132 | First-choice aboveground component equations |
| 18, 23 | Lambert, M.-C., Ung, C.-H., Raulier, F. 2005. Canadian national tree aboveground biomass equations. Can. J. For. Res. 35(8):1996–2018 | Fallback aboveground equations where Ung 2008 lacks the species |
| 20 | Kull, S.J., et al. 2019. Operational-scale Carbon Budget Model of the Canadian Forest Sector (CBM-CFS3) v1.2 user's guide. NRCan CFS | Alternative carbon pathway via merchantable yield tables |
| 21 | Li, Z., Kurz, W.A., Apps, M.J., Beukema, S.J. 2003. Belowground biomass dynamics in the CBM-CFS. Can. J. For. Res. 33(1):126–136 | Root biomass, the belowground pool |
| 19 | Kershaw, J.A., et al. 2016. Forest Mensuration, 5th ed. Wiley/Blackwell | Biomass expansion factors and bigBAF subsampling |

The operative instruction sits in section 3.3.1.1: "The Canadian National Biomass equations are the preferred equations for estimating per tree biomass components. Locally calibrated equations may be used when available and have undergone proper independent peer review." Section 3.3.1.2 then directs the user to Ung 2008 by species where available, Lambert 2005 otherwise, the Table 4 forms when both DBH and height are measured, the Table 3 forms when only DBH is, and to avoid the pooled "All Softwoods" or "All Species" equations except where nothing species-specific exists. Biomass is converted to carbon by a factor of 0.5 (section 3.3.1.2, Step 4).

Three features of this citation base are the hinge of both the audit and the paper. It makes the national equations the default, not merely an option. It builds in a diameter-only versus diameter-plus-height choice by pointing at two different tables in the same papers. And it leaves one door open, a peer-reviewed local calibration, through which a stratum-specific equation could lawfully enter.

## Accuracy of the cited records

The five allometry-chain citations are bibliographically correct as printed, checked against the published records. Ung 2008 is CJFR 38(5):1123–1132, given here as 38:1123–1132, correct bar the omitted issue number. Lambert 2005 is 35(8):1996–2018, correct. Li 2003 is 33(1):126–136, correct. The CBM-CFS3 v1.2 user's guide and Forest Mensuration 5th edition are cited correctly. The only defect is a cosmetic one: footnote 18 prints "aboveground biomass equation s" with a broken word, a typesetting artifact, not a citation error. The standards and IPCC references (GPG-LULUCF 2003, IPCC 2006 guidelines, ISO 14064-2:2006) are the expected and current-for-2021 sources.

One substantive observation, not a citation defect but worth recording for the audit. The biomass-to-carbon fraction is fixed at 0.5, while the IPCC 2006 default the methodology otherwise leans on is 0.47 for aboveground biomass. A 0.5 fraction raises the carbon estimate by roughly six percent relative to 0.47, which for a removals project is the non-conservative direction. It is a defensible and common choice, but it is a parameter the verifier should confirm the project applies consistently across baseline and project, ex ante and ex post, as the methodology requires.

## What the methodology does not cite, and why it matters

The methodology cites no ecosystem-specific or peatland-specific biomass equation. Its entire tree-biomass basis is the national Lambert and Ung set plus the national CBM-CFS3 pathway. This is not an oversight by the drafters. The methodology is dated September 2021, and the strongest contrary evidence, Wagers et al.'s peatland black spruce component equations showing the national model underestimates total biomass by about twelve percent in exactly this stratum, was not published until 2024. Fradette et al. 2021, which found the national equations underestimate branch biomass in eastern open woodlands, predates the methodology but is likewise not cited. The methodology's citation base therefore reflects the national-equation consensus as it stood in 2021, before the peatland-specific record matured.

That timing is the whole point of the "locally calibrated equations may be used when available and have undergone proper independent peer review" clause. It is the only mechanism in the document through which a corrected equation can displace the national default, and it is silent on who judges the calibration adequate, on what geographic or ecological match is required, and on whether the verifier can compel its use where the national equation is demonstrably biased on the dominant stratum. For a lowland peatland black spruce project, the methodology points hard at a national equation that the post-2021 literature shows is biased low on the very stratum that carries the project, while leaving the remedy optional and undefined. That gap is the audit's live question and the paper's thesis in a single sentence.

## Bearing on the paper

The paper can cite this methodology as the concrete regulatory instrument that installs the national equations as the default conversion from inventory to biomass in Canadian IFM, and it can quote the "preferred equations" and peer-reviewed local-calibration clauses verbatim, since the methodology is a public ACR document carrying no confidential project content. The argument then writes itself: a standard that defaults to a nationally calibrated equation, admits a stratum-specific correction only as an undefined option, and predates the peatland evidence, is exactly where a measured twelve percent bias becomes an MRV and offset-integrity problem rather than an academic one. Nothing in this examination draws on Clay Belt data; it rests entirely on the public methodology and the open literature.
