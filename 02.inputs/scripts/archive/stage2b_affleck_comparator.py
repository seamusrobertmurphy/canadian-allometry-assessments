"""
Stage 2b: an independently calibrated large-tree comparator for western-larch stem bark.

Purpose. Stages 1 and 2 rest on a western-larch bark equation fitted to 13 trees no larger
than 19.8 cm, applied to inventory stands averaging 32 cm. Affleck (2019, For. Ecol. Manage.
432:179-188) published a western-larch (LAOC) stembark equation fitted within a 470-tree
Inland Northwest destructive sample spanning 5 to 105 cm DBH, using diameter and height:

    m_bark = 0.001910 * d^1.636 * h^1.332     (kg; d in cm, h in m)

That is exactly the calibration range our own equation lacks, from the same regional
population, published and independent of both the national coefficients and our refit. The
Vegetation Resources Inventory records projected height per polygon, so the equation can be
applied province-wide alongside the other two, giving a third estimate that is neither the
national coefficient nor a small-sample extrapolation.

Definitional caveat, which the interpretation must carry. Affleck's stembark is the bark of
the main stem from a 30 cm stump to a 5 cm top. ENFOR and LegacyTreeData stem bark include
the stump section and run to the tip. Bark is proportionally thickest at the base and the
5 cm top exclusion removes a large share of a small tree's stem, so Affleck's equation is
expected to sit low relative to a whole-stem definition, and increasingly so in small trees.
The comparison is therefore most meaningful at the operational sizes that dominate the
inventory, and least meaningful below about 20 cm.

Outputs: 03.outputs/tables/T10_affleck_comparison.csv (tree level)
         03.outputs/tables/T11_province_three_equations.csv (province level)
         03.outputs/figures/F9_affleck_comparator.png
"""

import math
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(7)

R = "."
TBL = f"{R}/03.outputs/tables"
FIG = f"{R}/03.outputs/figures"
CFRAC = 0.47

NAT = (0.0153, 2.2110)          # national generic conifer stem bark, DBH form (Ung 2008)
NAT_H = (0.0101, 1.8486, 0.5525)  # national generic conifer stem bark, DBH+H form
AFF = (0.001910, 1.636, 1.332)  # Affleck 2019, LAOC stembark, DBH+H


def bark_nat(d):
    return NAT[0] * d ** NAT[1]


def bark_nat_h(d, h):
    return NAT_H[0] * d ** NAT_H[1] * h ** NAT_H[2]


def bark_affleck(d, h):
    return AFF[0] * d ** AFF[1] * h ** AFF[2]


def main():
    # ---- Stage 1 refit parameters -------------------------------------------
    t4 = pd.read_csv(f"{TBL}/T4_larch_refits.csv")
    r = t4[(t4.species == "western larch") & (t4.component == "bark")
           & (t4.method.str.startswith("log-log"))].iloc[0]
    a_ref, b_ref, a_se, b_se = float(r.a), float(r.b), float(r.a_se), float(r.b_se)
    print(f"Stage 1 western-larch refit: a={a_ref:.4f} b={b_ref:.4f}")

    # ---- tree-level comparison across the diameter range --------------------
    # heights follow the inventory's own height-diameter relation for larch-leading stands,
    # fitted below, so the comparison is anchored on the stands the equations are applied to
    df = pd.read_csv(f"{R}/02.inputs/vri/vri_larch.csv", low_memory=False)
    for c in ["QUAD_DIAM_125", "BASAL_AREA", "VRI_LIVE_STEMS_PER_HA", "PROJ_HEIGHT_1",
              "BARK_BIOMASS_PER_HA", "FEATURE_AREA_SQM"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["area_ha"] = df["FEATURE_AREA_SQM"] / 1e4
    ba_per_tree = math.pi * (df["QUAD_DIAM_125"] / 200.0) ** 2
    df["stems_ha"] = df["VRI_LIVE_STEMS_PER_HA"].where(
        df["VRI_LIVE_STEMS_PER_HA"] > 0, df["BASAL_AREA"] / ba_per_tree)
    clean = df[(df.SPECIES_CD_1.isin(["LW", "LT"])) & (df.QUAD_DIAM_125 > 0)
               & (df.stems_ha > 0) & (df.area_ha > 0)].copy()

    lw = clean[clean.SPECIES_CD_1 == "LW"].dropna(subset=["PROJ_HEIGHT_1"])
    hd = np.polyfit(np.log(lw.QUAD_DIAM_125), np.log(lw.PROJ_HEIGHT_1), 1)
    height_of = lambda d: np.exp(hd[1]) * d ** hd[0]
    print(f"VRI western-larch height-diameter: h = {np.exp(hd[1]):.3f} d^{hd[0]:.3f}")

    grid = np.array([10, 15, 20, 25, 30, 32, 40, 50, 60, 70])
    hh = height_of(grid)
    tree = pd.DataFrame(dict(
        dbh_cm=grid, height_m=hh,
        national_D=bark_nat(grid), national_DH=bark_nat_h(grid, hh),
        affleck=bark_affleck(grid, hh), refit=a_ref * grid ** b_ref))
    tree["affleck_over_national"] = tree.affleck / tree.national_D
    tree["refit_over_national"] = tree.refit / tree.national_D
    tree["refit_over_affleck"] = tree.refit / tree.affleck
    tree.to_csv(f"{TBL}/T10_affleck_comparison.csv", index=False)

    # ---- province-wide, three equations -------------------------------------
    Q = clean.QUAD_DIAM_125.values
    S = clean.stems_ha.values
    A = clean.area_ha.values
    sp = clean.SPECIES_CD_1.values
    H = clean.PROJ_HEIGHT_1.values.copy()
    missing = ~np.isfinite(H) | (H <= 0)
    H[missing] = height_of(Q[missing])   # fill from the fitted height-diameter relation
    print(f"height filled for {missing.sum()} of {len(H)} polygons")

    per_ha = lambda mass_kg: S * mass_kg / 1000.0        # Mg/ha
    clean["nat_MgHa"] = per_ha(bark_nat(Q))
    clean["aff_MgHa"] = per_ha(bark_affleck(Q, H))
    t4lt = t4[(t4.species == "tamarack") & (t4.component == "bark")
              & (t4.method.str.startswith("log-log"))].iloc[0]
    a_lt, b_lt = float(t4lt.a), float(t4lt.b)
    a_r = np.where(sp == "LW", a_ref, a_lt)
    b_r = np.where(sp == "LW", b_ref, b_lt)
    clean["ref_MgHa"] = per_ha(a_r * Q ** b_r)

    rows = []
    for lab, mask in [("western larch", sp == "LW"), ("tamarack", sp == "LT")]:
        d = clean[mask]
        a = A[mask]
        row = dict(leading_species=lab, n_polygons=int(mask.sum()), area_ha=a.sum(),
                   national_TgC=(d.nat_MgHa * a * CFRAC).sum() / 1e6,
                   refit_TgC=(d.ref_MgHa * a * CFRAC).sum() / 1e6)
        if lab == "western larch":
            row["affleck_TgC"] = (d.aff_MgHa * a * CFRAC).sum() / 1e6
        else:
            row["affleck_TgC"] = np.nan   # Affleck fitted no tamarack; LAOC only
        rows.append(row)
    prov = pd.DataFrame(rows)
    for c in ["refit", "affleck"]:
        prov[f"{c}_vs_national_pct"] = 100 * (prov[f"{c}_TgC"] / prov.national_TgC - 1)
    prov.to_csv(f"{TBL}/T11_province_three_equations.csv", index=False)

    # ---- figure --------------------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
    dd = np.linspace(6, 70, 200)
    hgrid = height_of(dd)
    ax[0].plot(dd, bark_nat(dd), "k--", lw=1.6, label="national, generic conifer")
    ax[0].plot(dd, bark_affleck(dd, hgrid), color="#7570b3", lw=1.8,
               label="Affleck 2019, western larch (to 105 cm)")
    ax[0].plot(dd, a_ref * dd ** b_ref, color="#d95f02", lw=1.8,
               label="this study, refit (to 19.8 cm)")
    ax[0].axvspan(6.9, 19.8, color="#d95f02", alpha=0.10)
    ax[0].text(13, ax[0].get_ylim()[1] * 0.55, "refit\ncalibration", ha="center",
               fontsize=8, color="#d95f02")
    ax[0].axvline(32, color="k", ls=":", lw=1.2)
    ax[0].text(33, 5, "provincial mean QMD", fontsize=8, rotation=90)
    ax[0].set_xlabel("DBH (cm)"); ax[0].set_ylabel("Stem bark (kg)")
    ax[0].set_title("(a) Three western-larch bark equations")
    ax[0].legend(frameon=False, fontsize=8, loc="upper left")

    ax[1].axhline(1.0, color="k", ls="--", lw=1.4)
    ax[1].plot(dd, bark_affleck(dd, hgrid) / bark_nat(dd), color="#7570b3", lw=1.8,
               label="Affleck / national")
    ax[1].plot(dd, (a_ref * dd ** b_ref) / bark_nat(dd), color="#d95f02", lw=1.8,
               label="refit / national")
    ax[1].axvline(32, color="k", ls=":", lw=1.2)
    ax[1].set_xlabel("DBH (cm)"); ax[1].set_ylabel("Ratio to the national coefficient")
    ax[1].set_title("(b) Departure from the national coefficient")
    ax[1].legend(frameon=False, fontsize=9)
    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{FIG}/F9_affleck_comparator.png", dpi=200)

    pd.set_option("display.width", 200, "display.max_columns", 30)
    print("\n=== T10 tree-level comparison (heights from the VRI relation) ===")
    print(tree.round(3).to_string(index=False))
    print("\n=== T11 province-wide, three equations ===")
    print(prov.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
