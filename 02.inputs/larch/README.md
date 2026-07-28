# National allometric coefficients (Lambert 2005 / Ung 2008)

The **predicted / national** side of the western larch stem-bark bias analysis:
the coefficient tables behind Canada's national biomass equations. These are the
`nat_bark()` comparator. Observed bark still comes from the destructive dataset
(Affleck INGY), not from here.

## Files

| File | Equation | Columns |
|---|---|---|
| `nfi_tree-level_allometric_dbh-height.csv` | Biomass_kg = a · DBH_cm^b · H_m^c | Species, Component, a, b, c, Reference |
| `nfi_tree-level_allometric_dbh.csv` | Biomass_kg = a · DBH_cm^b | Species, Component, a, b, Reference |
| `nfi_plot-level_allometric.csv` | Biomass_tha = a · Bs_m2ha^b · Bt_m2ha^c (Paré 2013) | Species, Component, a, b, c, d, e |

Components: Bark, Branches, Foliage, Wood (Stemwood at plot level). 41 tree-level
species plus the generic classes Conifers / Deciduous / All.

## Source and provenance

- Canonical: NRCan Biomass and nutrients calculator, "Allometric parameters" downloads.
  https://apps-scf-cfs.rncan.gc.ca/calc/en/biomass-calculator
- Retrieved 2026-07-16 via the byte-identical mirror in the `tesera/biomasscan`
  R package (`data-raw/`), whose `DATASET.R` records download from the NRCan page on 2023-07-11.
- Licence: Open Government Licence – Canada.
- References: Lambert, Ung & Raulier 2005 (CJFR 35:1996-2018); Ung, Bernier & Guo 2008
  (CJFR 38:1123-1132); plot-level Paré et al. 2013 (CJFR 43:599-608).
- Note: the original CSVs carry French columns (Essence_fr, Component_fr) in Latin-1
  that arrive as mojibake over HTTP; those columns are dropped here. English names,
  components, and all numeric parameters are reproduced exactly. French columns are
  not needed for the analysis.

## KEY FINDING — western larch has no national equation

The 41-species national set contains only ONE larch: **Tamarack larch (*Larix
laricina*)**. **Western larch (*Larix occidentalis*) is absent.** This resolves
blocker 2: Ung 2008 did not fit an *occidentalis* coefficient. In the national
system western larch bark is estimated by the generic **Conifers** coefficient (or
whatever congener a project substitutes). The paper therefore evaluates a generic
coefficient applied to a thick-barked species, not a species coefficient.

### Comparator bark coefficients (quick reference)

DBH + height (Biomass_kg = a · DBH^b · H^c):

- Conifers (generic):   a = 0.0101, b = 1.8486, c = 0.5525  (Ung 2008)
- Tamarack larch:       a = 0.0120, b = 1.7059, c = 0.5811  (Lambert 2005)

DBH only (Biomass_kg = a · DBH^b):

- Conifers (generic):   a = 0.0153, b = 2.2110  (Ung 2008)
- Tamarack larch:       a = 0.0174, b = 2.1109  (Lambert 2005)

Test both: generic Conifers is what an accountant is forced to use for larch;
Tamarack larch is the nearest-congener substitute.
