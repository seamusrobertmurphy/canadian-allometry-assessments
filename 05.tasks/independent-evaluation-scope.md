# Scoping the independent-evaluation problem

The single constraint that decides whether the Vorster-style result is credible. Prepared 2026-07-15.

## The problem, stated precisely

The national equations (Lambert 2005, Ung 2008) were fitted on ENFOR. Any error we compute by fitting the national form to ENFOR and testing on ENFOR is in-sample, and it flatters the national model. Vorster's decisive move was to evaluate the equations against trees that were not used to fit them, which is what turned allometric error from a modest term into the dominant one. Our paper needs the same: a genuinely independent black spruce destructive dataset, ideally one that resolves drainage, so the peatland claim rests on out-of-sample evidence rather than a re-fit on the calibration data.

## Candidate external datasets, ranked

**Bond-Lamberty, Wang and Gower 2002, northern Manitoba (BOREAS).** The strongest single candidate. Six boreal species including black spruce, sampled near Thompson across 17 sites, stands aged 4 to 130 years, stem diameter 0.1 to 23.7 cm, and, decisively, each stand classified as well or poorly drained. That drainage split is a real peatland-versus-upland test of the national equations, available now without waiting for the spatial overlay. Associated with BOREAS, so the underlying biomass data are plausibly archived at the ORNL DAAC; the allometry is published in CJFR 32:1441-1450 (doi:10.1139/x02-063). Action: confirm whether tree-level biomass, not just the fitted equations, is retrievable from ORNL DAAC or on request.

**Wagers et al. 2024, western Canadian peatland black spruce.** The direct ecosystem-specific contrast, 495 trees, the exact stratum the paper is about. If the tree-level data are archived with the paper or in a repository, this is the primary external peatland evaluator. Action: check the CJFR supplement and any Dryad or federal archive; if not public, request from the authors (NRCan CFS Northern Forestry Centre).

**BOREAS destructive biomass archives at ORNL DAAC.** Beyond Bond-Lamberty, the BOREAS campaign destructively sampled black spruce in both the northern and southern study areas (Gower and colleagues). These are open through the ORNL DAAC and provide additional independent boreal black spruce. Action: pull the relevant BOREAS TE and TF biomass datasets and screen for black spruce with diameter and mass.

**Provincial permanent-sample-plot and destructive networks, via MAGPlot.** The Multi-Agency Ground Plot database consolidates provincial plots pan-Canadian; some jurisdictions release openly under a Data Use Agreement. Ontario (Clay Belt relevant) and Quebec both run large PEP networks, and Alberta holds peatland black spruce destructive work in the Wagers region (ABMI). These are mostly plot-level rather than destructive-biomass, so they serve plot-scale validation and stratification more than tree-level allometric error. Action: request the openly shareable MAGPlot black spruce subset and identify any destructive components.

**NFI ground plots.** Independent of ENFOR and open, but inventory rather than destructive, so their role is plot-scale and landscape validation, not the tree-level allometric error term.

## A defensible ENFOR/Wagers partition: three tiers

The design separates three distinct notions of error and never tests a fitted model on its own trees.

**Tier 1, leave-one-site-out within ENFOR.** ENFOR's 1,813 black spruce sit at about 60 distinct sites. Trees at one site share soil, climate, and stand history, so a tree-level split leaks information and understates error. Fit the national form on all sites but one and predict the held-out site, cycling through all sites. This is the honest internal generalization estimate, and it replaces the ordinary cross-validation currently in the code. It removes within-site optimism without needing any external data.

**Tier 2, regional transfer holdout.** Fit the national form excluding the eastern boreal target region (Quebec, Ontario, Newfoundland and Labrador, which hold most of the small-tree records and are the Clay Belt setting), then evaluate on that region. This simulates the real failure the paper is about: a nationally calibrated equation applied to a region under-represented in its calibration. The provincial counts support it (Quebec alone holds 933 black spruce and 268 of the small-tree records).

**Tier 3, external independent evaluation.** Apply the ENFOR-calibrated national equations, and ultimately the published Lambert and Ung coefficients, to Bond-Lamberty 2002 and Wagers 2024. This is the true out-of-sample test and the paper's headline. Bond-Lamberty's drainage classification lets the bias be split into well-drained and poorly-drained black spruce, which is the drainage signal the paper claims, measured directly rather than proxied by size.

## Why this is defensible, and the cleanest published form

The three tiers correspond to three questions a referee will ask: how well does the model generalise within its own sample once pseudoreplication is removed (Tier 1), how well does it transfer to an under-sampled region (Tier 2), and how well does it transfer to a different ecosystem and campaign (Tier 3). Reporting all three, as Vorster reported equation-fit error alongside independent-dataset error, is both honest and complete.

The cleanest published result avoids re-fitting entirely: transcribe the published Lambert 2005 and Ung 2008 black spruce coefficients, apply them unchanged to Bond-Lamberty and Wagers, and report the bias and relative RMSE by drainage class. That is a genuine, uncontestable independent evaluation of the national equations as the ACR methodology actually mandates them, and it sidesteps every objection about the open re-fit currently standing in as a placeholder.

## Immediate actions

Confirm tree-level retrievability of Bond-Lamberty 2002 and BOREAS black spruce from ORNL DAAC, and the archive status of Wagers 2024. Transcribe the published national coefficients so Tier 3 can run on published parameters rather than a re-fit. Implement Tier 1 leave-one-site-out in the analysis code, replacing plain cross-validation. Request the openly shareable MAGPlot black spruce subset for plot-scale support.
