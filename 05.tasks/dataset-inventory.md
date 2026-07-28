# Candidate datasets — western larch / larch bark bias paper

Compiled 2026-07-16 from datasets examined this session. "Observed bark" = a felled tree
with a measured stem-bark mass or volume. "Predicted" = the national coefficient side.
Verified counts are from direct inspection of the files; items marked *to confirm* were
not yet opened.

## Tier 1 — destructive tree data with a bark measurement (the observed side)

| Dataset | Larch present | Bark variable(s) | n (larch) | Size range | Geography | Access | Verdict |
|---|---|---|---|---|---|---|---|
| **LegacyTreeData** (Radtke 2021, VT; DOI 10.7294/W4VD6WC6) | Western larch (spcd 73) + tamarack | `st_bk_dw` (stem bark dry wt), `st_wdbk_dw`, `tt_wdbk_dw`, branch bark; plus bark **volume** `ST_BK_CV*`, bark SG/MC fields | 85 WL total; **stem-bark mass n=13** (DBH 6.9–19.8 cm); `st_wdbk_dw` n=42 | WL to **55 cm** (7 trees >40 cm), but the >40 cm trees are taper-only (no stem-bark mass) | Montana (Brown, Kloeppel), Washington (Gower = the 13 bark trees), Oregon (Umatilla), + Kozak (no coords, likely BC) | **Open, CC BY**; local copy `/Users/seamus/Downloads/14099516` | Real WL bark, small–mid trees only. Units: **inches / pounds**. |
| **ENFOR** (Ung, Lambert, Raulier, Guo, Bernier 2017; DOI 10.23687/fbad665e-8ac9-4635-9f84-e4fd53a6253c) | **Tamarack only** (*L. laricina*); western larch absent | `OM_stem_bark` (kg, oven-dry) — complete for all trees | Tamarack: AB 20, MB ≥20; SK/NT *to confirm* | Tamarack to ~38 cm | Boreal Canada, all provinces | **Open, OGL-Canada** | Gold-standard bark, but wrong larch **and** it is the coefficient's own training data (circular). |
| **Affleck INGY** (Affleck 2018, *For. Ecol. Manage.* 432:179–188) | **Western larch** among 4 conifers | stem wood/bark from taper + density | **470 trees, 84 stands** | **to 105 cm DBH** (the large trees) | Inland NW USA (MT/ID/WA) | **By request** — David Affleck, UMontana INGY cooperative | The only source with large western larch + bark. Access barrier. |
| **Standish 1985** (Info. Rep. BC-X-264) | Western larch | component equations incl. bark | equations, not raw trees | — | **British Columbia** | CFS Pacific Forestry Centre; raw trees *to confirm* | BC-native, but published as equations. |

## Tier 2 — not yet opened, worth a look for observed bark

| Dataset | Note | Access |
|---|---|---|
| Faurot 1977 (USFS Res. Pap. INT-196) | Western larch stem + bark residue | Open PDF, FS TreeSearch — *to confirm per-tree bark* |
| Brown 1978 (USFS Res. Pap. INT-197) | Rocky Mountain conifer crown weights incl. larch | Open PDF — *to confirm* |
| BAAD (Falster et al. 2015) | Global destructive biomass + components | Open, GitHub — *to confirm WL* |
| GlobAllomeTree (FAO) | Western larch equations incl. bark | Open — equations + source refs |

## Predicted side (already in hand)

| Dataset | Use |
|---|---|
| **NRCan national coefficients** (Lambert 2005 / Ung 2008) | The comparator `nat_bark()`. Downloaded to `02.inputs/larch/`. Western larch is **not** a listed species → generic **Conifers** coefficient (operative predictor) + **Tamarack larch** as nearest congener. |

## Out for the bias test (no bark, no felled trees)

| Dataset | Why |
|---|---|
| Tallo (Jucker 2022) | Stem diameter, height, crown only — no mass/bark. (Larix extract was *L. gmelinii*, Asian.) |
| NTEMS layers (Annual Tree Species, Gross Stem Volume, Basal Area, Forest Structure) | 30 m modelled rasters; no trees, no bark. Upscaling context only. |
| SCANFI v1/v2 | 30 m modelled rasters; western larch not a mapped species. |
| Beaudoin 2014 kNN maps; NFI ground/photo plots | Modelled maps / standing inventory; no destructive bark. |

## Honest read

- **Open + western larch + real bark, now:** only LegacyTreeData (13 stem-bark trees ≤20 cm; up to ~n=42 for stem wood+bark to ~40 cm). Small trees.
- **Large western larch + bark:** only Affleck (request).
- **ENFOR** is superb bark data but tamarack, boreal, and the coefficient's training set.

The paper's original large-tree, size-dependence thesis needs Affleck. What is fully
open today supports a smaller claim (bias of the generic conifer coefficient on the
small–mid western larch that exists, plus a tamarack cross-check on ENFOR).
