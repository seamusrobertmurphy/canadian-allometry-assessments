# A Vorster-style study in Canada: feasibility, approach, and the hard parts

Advisory prepared 2026-07-15, reviewing Vorster et al. (2020, Carbon Balance and Management) against what open Canadian data now allow. Short version: a Canadian replication is not only feasible, it is better resourced than the US original in most respects, because Canada has since published open national plot data, an open national spatialised inventory, and open national peatland maps. The binding constraints are narrow and specific, and they sit almost entirely on the independent-evaluation and geolocation sides, not on the mapping side.

## What Vorster actually did

The paper's contribution is not a biomass map. It is an honest partition of where a biomass map's error comes from. They built local component equations for three species from a small destructive sample (40 trees total: 20 lodgepole pine, 10 ponderosa pine, 10 Douglas-fir), by nonlinear seemingly-unrelated regression in the log form with additive components. They then estimated biomass on 418 FIA inventory plots three ways: their local equations, the national Jenkins et al. equations, and the FIA Component Ratio Method. They mapped plot biomass across 1.56 million hectares with a single 2001 Landsat scene plus 302 spectral, texture, climate, and geomorphometric predictors, reduced by variable selection, fitted with random forest. Finally they propagated two error sources to the map, allometric error and remote-sensing prediction error, at tree, plot, and pixel scale, using two versions of the allometric error: one from the equation fit, and one from an independent set of 285 destructively sampled trees from the Legacy Tree Database. The headline is that allometric error contributed 30 to 75 percent of total map uncertainty, rivalling or exceeding the remote-sensing model. That is the sentence our paper already leans on.

## The Canadian data chain, ingredient by ingredient

| Vorster ingredient | Open Canadian equivalent | State and constraint |
|---|---|---|
| Local destructive equations (40 trees) | ENFOR national destructive archive (about 9,500 trees, 1,764 black spruce) plus Wagers et al. 2024 peatland black spruce (495 trees) | Open. Canada is far richer here than Vorster's 40 trees. ENFOR is the national set; Wagers is the ecosystem-specific set. |
| National comparison equations (Jenkins, FIA-CRM) | Lambert 2005 / Ung 2008 national equations, and the CBM-CFS3 volume-to-biomass pathway | Open equations; the national-versus-stratum-specific contrast is exactly our paper. |
| FIA inventory plots (418, tree-level, public) | NFI ground plots (open.canada.ca, Open Government Licence) and the Multi-Agency Ground Plot (MAGPlot) database | NFI ground plots are open with tree-level measurements. MAGPlot adds provincial plots but some jurisdictions gate access behind a Data Use Agreement. This is the main access nuance, softer than expected. |
| Landsat scene + 302 predictors + random forest map | SCANFI, the Spatialised Canadian NFI, 30 m, 1985 to 2025, plus Beaudoin et al. 2014 kNN biomass and Matasci et al. 2018 NTEMS structure | Open. Canada already has the national biomass/structure map Vorster had to build from scratch. This removes most of the mapping labour. |
| Climate and topographic layers | ClimateNA / AdaptWest, CDEM | Open, national. Not a constraint. |
| Independent evaluation set (285 Legacy trees) | No single consolidated open legacy biomass database; ENFOR or held-out Wagers plots are the candidates | The real gap. See challenges. |
| Peatland stratification (not in Vorster) | Canadian National Wetlands Inventory (2024, expanded 2025 to about 33 percent of Canada), Canadian Wetland Inventory Map v3A, and a boreal peatland sub-class map circa 2020 | Open raster. Makes the peatland stratum, our novel axis, genuinely mappable. |

## Feasibility verdict

Feasible, and stronger than the original on three of its four data legs. The allometric leg is data-rich where Vorster was data-poor: he built equations from ten to twenty trees per species and openly worried that his local equations were unreliable for it; Canada has hundreds to thousands of destructively sampled black spruce. The mapping leg is largely pre-built: SCANFI and the Beaudoin and Matasci products give an open national biomass surface, so a Canadian study can either reuse them as the remote-sensing layer or rebuild a scene-level map in the Vorster manner. The stratification leg is a Canadian advantage Vorster never had: open national peatland maps let the study replace a size proxy with a soil-based peatland stratum, which is the whole point of our paper.

## The greatest challenges, ranked

The hardest problem is the independent evaluation dataset. Vorster's key methodological move, the one that flips allometric error from a modest term to the dominant one, was evaluating the equations against trees that were not used to fit them. In Canada there is no consolidated open "Legacy Tree Database" for peatland black spruce. ENFOR cannot be both the national fitting sample and the independent evaluator without circularity, and Wagers is a single archive. A credible Canadian study needs a genuinely independent peatland destructive set, which likely means assembling one from provincial or research sources, or carefully partitioning ENFOR and Wagers with explicit spatial or campaign separation. This is the make-or-break constraint and it should be scoped first.

Second is geolocation precision and plot confidentiality. Vorster extracted 302 predictors at exact FIA plot locations. Canadian NFI and FIA-style plots have fuzzed or restricted coordinates for confidentiality, and ENFOR coordinates, as we already found, are site-level and mixed precision. Any pixel-scale propagation therefore inherits location error, and a Canadian study must either work at the plot or site scale or negotiate precise coordinates under agreement.

Third is the provincial-data patchwork. MAGPlot consolidates provincial plots but access varies by jurisdiction and by Data Use Agreement, so a truly pan-Canadian, fully-open plot base is not guaranteed; the open NFI ground-plot sample is thinner than the US FIA grid.

Fourth is component and moisture heterogeneity. Vorster spent real effort reconciling component definitions across three equation systems and converting green mass to dry for many Legacy trees. A Canadian synthesis across ENFOR, Wagers, and provincial sources will face the same reconciliation, plus the additivity constraint the national equations impose, which Vorster's log form sidesteps.

## Recommended approach and staging

Stage it, and let the constraints set the boundary. The tree-and-plot-scale uncertainty partition, national versus peatland-specific black spruce, is feasible today on fully open data (ENFOR, Wagers, open NFI ground plots), and it is the core of the commentary the decision memo already commits to. Do that first. The landscape extension, the distinctive Vorster contribution of partitioning allometric against remote-sensing error across a mapped area, is feasible as a second, larger study precisely because SCANFI and the national biomass products remove the mapping burden, but it should be gated on solving the independent-evaluation problem and securing plot geolocation. In other words, the Vorster design splits cleanly along our existing plan: its allometric-uncertainty half is our near-term paper, and its map-propagation half is the review-scale or follow-on study, contingent on one dataset we do not yet have.

## Sources

- Vorster et al. 2020, Carbon Balance and Management 15:8 — https://doi.org/10.1186/s13021-020-00143-6
- ENFOR destructive-biomass dataset — https://doi.org/10.23687/fbad665e-8ac9-4635-9f84-e4fd53a6253c
- Wagers et al. 2024, CJFR 54(2):207–223 — https://doi.org/10.1139/cjfr-2023-0031
- Canada's NFI Ground Plot Data (open) — https://open.canada.ca/data/en/dataset/35c3556c-e48d-41a7-ac50-652257b0a8e8
- Multi-Agency Ground Plot (MAGPlot) database — https://open.canada.ca/data/en/dataset/8824392d-464e-413d-8bde-eaed61c79743
- SCANFI spatialised national inventory — https://open.canada.ca/data/en/dataset/18e6a919-53fd-41ce-b4e2-44a9707c52dc
- Beaudoin et al. 2014, kNN forest attributes — https://doi.org/10.1139/cjfr-2013-0401
- Canadian National Wetlands Inventory (ECCC) — https://www.canada.ca/en/environment-climate-change/services/wildlife-habitat/canadian-national-wetland-inventory.html
- Boreal peatland sub-class map (circa 2020) — https://zenodo.org/records/10627580
