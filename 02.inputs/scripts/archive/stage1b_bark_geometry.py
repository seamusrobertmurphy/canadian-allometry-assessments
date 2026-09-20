"""
Stage 1b: bark geometry at breast height, and the size-dependence of bark allocation.

Purpose. The Stage 1 western-larch bark-mass refit rests on 13 trees to 19.8 cm DBH
(Gower 1987, Washington Cascades), but Stage 2 applies it to inventory stands averaging
32 cm QMD. The extrapolation is governed by the fitted exponent b: if bark's share of the
stem is constant with size, b for bark matches b for wood and the extrapolation is benign;
if bark's share rises with size, b for bark is larger and the Stage 1 fit, calibrated on
small trees, understates bark in large ones.

LegacyTreeData carries stem taper with paired outside-bark and inside-bark diameters for a
second, independent western-larch sample (FMSC_Validation_R6, Umatilla National Forest,
n = 15, 16.3 to 39.4 cm DBH) that shares no trees with the mass sample and covers precisely
the diameter range the mass sample lacks. Tamarack has the same measurements (n = 42, 12.2
to 31.5 cm), giving a within-genus control.

This module uses no assumed bark density and no imported constant. It works entirely in
measured diameters, so it tests the exponent and the species contrast directly.

Outputs: 03.outputs/tables/T8_bark_geometry.csv, T9_bark_area_scaling.csv
         03.outputs/figures/F8_bark_geometry.png
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

RNG = np.random.default_rng(20260721)
IN_TO_CM = 2.54
BH_FT = 4.5  # breast height in the source units (feet)
N_BOOT = 10000

DATA = "../legacy-tree"
TAB = "../../03.outputs/tables"
FIG = "../../03.outputs/figures"

SPP = {73: "western larch", 71: "tamarack"}
KEY = ["author", "loc", "spcd", "treeno"]


def load_breast_height():
    """Paired outside/inside bark diameters at breast height, one row per tree."""
    stem = pd.read_csv(f"{DATA}/stem.txt", low_memory=False, on_bad_lines="skip")
    tree = pd.read_csv(f"{DATA}/tree.txt", low_memory=False, on_bad_lines="skip")

    larix = tree[tree.spcd.isin(SPP)][KEY].drop_duplicates()
    bh = (
        stem[stem.st_ht == BH_FT]
        .merge(larix, on=KEY)
        .dropna(subset=["st_ob_d", "st_ib_d"])
        .copy()
    )
    # one section per tree at breast height; guard against duplicate records
    bh = bh.drop_duplicates(subset=KEY)

    bh["species"] = bh.spcd.map(SPP)
    bh["dbh_ob"] = bh.st_ob_d * IN_TO_CM          # diameter outside bark, cm
    bh["dbh_ib"] = bh.st_ib_d * IN_TO_CM          # diameter inside bark, cm
    bh["dbt"] = bh.dbh_ob - bh.dbh_ib             # double bark thickness, cm
    bh["bark_ratio"] = bh.dbh_ib / bh.dbh_ob      # inside/outside diameter ratio
    # bark share of stem cross-section: the geometric analogue of bark's share of stem mass
    bh["f_area"] = 1.0 - bh.bark_ratio ** 2
    # bark cross-sectional area at breast height, cm^2
    bh["a_bark"] = (np.pi / 4.0) * (bh.dbh_ob ** 2 - bh.dbh_ib ** 2)
    return bh


def boot_ci(x, fn, n=N_BOOT):
    x = np.asarray(x)
    draws = [fn(RNG.choice(x, size=x.size, replace=True)) for _ in range(n)]
    return np.percentile(draws, [2.5, 97.5])


def describe(bh):
    rows = []
    for sp, g in bh.groupby("species"):
        lo, hi = boot_ci(g.f_area.values, np.mean)
        rows.append(dict(
            species=sp, n=len(g),
            dbh_min=g.dbh_ob.min(), dbh_max=g.dbh_ob.max(), dbh_mean=g.dbh_ob.mean(),
            dbt_mean=g.dbt.mean(), dbt_sd=g.dbt.std(ddof=1),
            f_area_mean=g.f_area.mean(), f_area_sd=g.f_area.std(ddof=1),
            f_area_lo=lo, f_area_hi=hi,
        ))
    return pd.DataFrame(rows)


def species_contrast(bh, band=None):
    """Welch t-test on bark area fraction; optionally within a shared diameter band."""
    d = bh
    label = "all sizes"
    if band is not None:
        d = bh[(bh.dbh_ob >= band[0]) & (bh.dbh_ob <= band[1])]
        label = f"{band[0]:.1f}-{band[1]:.1f} cm overlap"
    wl = d[d.species == "western larch"].f_area.values
    tm = d[d.species == "tamarack"].f_area.values
    t, p = stats.ttest_ind(wl, tm, equal_var=False)
    # Hedges-corrected standardized difference
    s = np.sqrt(((wl.size - 1) * wl.var(ddof=1) + (tm.size - 1) * tm.var(ddof=1))
                / (wl.size + tm.size - 2))
    d_eff = (wl.mean() - tm.mean()) / s
    return dict(comparison=label, n_wl=wl.size, n_tm=tm.size,
                f_wl=wl.mean(), f_tm=tm.mean(), ratio=wl.mean() / tm.mean(),
                t=t, p=p, cohens_d=d_eff)


def size_trend(g):
    """Linear trend in bark area fraction with diameter."""
    res = stats.linregress(g.dbh_ob.values, g.f_area.values)
    # bootstrap the slope: small samples, so do not lean on the normal-theory SE alone
    idx = np.arange(len(g))
    slopes = [stats.linregress(g.dbh_ob.values[i], g.f_area.values[i]).slope
              for i in (RNG.choice(idx, size=idx.size, replace=True) for _ in range(N_BOOT))]
    lo, hi = np.percentile(slopes, [2.5, 97.5])
    return dict(slope=res.slope, slope_lo=lo, slope_hi=hi, r=res.rvalue,
                p=res.pvalue, intercept=res.intercept)


def area_scaling(g):
    """Power fit A_bark = a * D^b on logs; b > 2 means bark share rises with size."""
    x, y = np.log(g.dbh_ob.values), np.log(g.a_bark.values)
    res = stats.linregress(x, y)
    n = len(g)
    tcrit = stats.t.ppf(0.975, n - 2)
    b_lo, b_hi = res.slope - tcrit * res.stderr, res.slope + tcrit * res.stderr
    # test the exponent against isometry (b = 2)
    t_iso = (res.slope - 2.0) / res.stderr
    p_iso = 2 * (1 - stats.t.cdf(abs(t_iso), n - 2))
    return dict(n=n, a=np.exp(res.intercept), b=res.slope, b_se=res.stderr,
                b_lo=b_lo, b_hi=b_hi, r2=res.rvalue ** 2,
                t_vs_isometry=t_iso, p_vs_isometry=p_iso)


def robustness(g):
    """Leave-one-out stability and a distribution-free check on the size trend.

    Small single-site samples invite a spurious trend from one influential tree, so the
    slope and the area exponent are refitted with each tree dropped in turn, and the
    monotone association is checked without the linear-normal assumption.
    """
    n = len(g)
    d, f, a = g.dbh_ob.values, g.f_area.values, g.a_bark.values
    slopes, pvals, exps = [], [], []
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        lr = stats.linregress(d[m], f[m])
        slopes.append(lr.slope); pvals.append(lr.pvalue)
        exps.append(stats.linregress(np.log(d[m]), np.log(a[m])).slope)
    rho, p_rho = stats.spearmanr(d, f)
    return dict(loo_slope_min=min(slopes), loo_slope_max=max(slopes),
                loo_sign_stable=bool(np.all(np.sign(slopes) == np.sign(slopes[0]))),
                loo_p_max=max(pvals),
                loo_exponent_min=min(exps), loo_exponent_max=max(exps),
                loo_exponent_all_above_2=bool(min(exps) > 2.0),
                spearman_rho=rho, spearman_p=p_rho)


def main():
    bh = load_breast_height()

    # --- Table 8: descriptive geometry and species contrast -------------------
    desc = describe(bh)
    overlap = (max(bh[bh.species == "western larch"].dbh_ob.min(),
                   bh[bh.species == "tamarack"].dbh_ob.min()),
               min(bh[bh.species == "western larch"].dbh_ob.max(),
                   bh[bh.species == "tamarack"].dbh_ob.max()))
    contrasts = pd.DataFrame([species_contrast(bh), species_contrast(bh, overlap)])

    desc.to_csv(f"{TAB}/T8_bark_geometry.csv", index=False)

    # --- Table 9: size dependence and area scaling ----------------------------
    rows = []
    for sp, g in bh.groupby("species"):
        r = {"species": sp}
        r.update(size_trend(g))
        r.update({f"scal_{k}": v for k, v in area_scaling(g).items()})
        r.update({f"rob_{k}": v for k, v in robustness(g).items()})
        rows.append(r)
    scaling = pd.DataFrame(rows)
    scaling.to_csv(f"{TAB}/T9_bark_area_scaling.csv", index=False)

    # provenance: how many sites carry each species, recorded with the results
    prov = (bh.groupby(["species", "author", "loc"])
              .agg(n=("dbh_ob", "size"), dbh_min=("dbh_ob", "min"),
                   dbh_max=("dbh_ob", "max"), f_area=("f_area", "mean"))
              .reset_index())
    prov.to_csv(f"{TAB}/T8b_bark_geometry_sites.csv", index=False)

    # --- Figure 8 -------------------------------------------------------------
    colours = {"western larch": "#d95f02", "tamarack": "#1b9e77"}
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))

    for sp, g in bh.groupby("species"):
        ax[0].scatter(g.dbh_ob, 100 * g.f_area, s=34, alpha=0.85,
                      color=colours[sp], label=f"{sp} (n = {len(g)})")
        xx = np.linspace(g.dbh_ob.min(), g.dbh_ob.max(), 50)
        tr = size_trend(g)
        ax[0].plot(xx, 100 * (tr["intercept"] + tr["slope"] * xx),
                   color=colours[sp], lw=1.6)
    ax[0].axvspan(20, 44, color="grey", alpha=0.10)
    ax[0].text(26.0, ax[0].get_ylim()[1] * 0.99, "beyond the bark-mass sample",
               ha="center", va="top", fontsize=8, color="grey")
    ax[0].axvline(32.0, color="k", ls=":", lw=1.2)
    ax[0].text(32.4, ax[0].get_ylim()[0] + 1.0, "provincial mean QMD",
               fontsize=8, rotation=90, va="bottom")
    ax[0].set_xlabel("Diameter outside bark at breast height (cm)")
    ax[0].set_ylabel("Bark share of stem cross-section (%)")
    ax[0].set_title("(a) Bark allocation against tree size")
    ax[0].legend(frameon=False, fontsize=9)

    for sp, g in bh.groupby("species"):
        ax[1].scatter(g.dbh_ob, g.a_bark, s=34, alpha=0.85, color=colours[sp])
        sc = area_scaling(g)
        xx = np.linspace(g.dbh_ob.min(), g.dbh_ob.max(), 50)
        ax[1].plot(xx, sc["a"] * xx ** sc["b"], color=colours[sp], lw=1.6,
                   label=f"{sp}: b = {sc['b']:.2f} [{sc['b_lo']:.2f}, {sc['b_hi']:.2f}]")
    # isometric reference (b = 2), anchored on the pooled midpoint so it is comparable
    mid_d, mid_a = bh.dbh_ob.median(), bh.a_bark.median()
    xx = np.linspace(bh.dbh_ob.min(), bh.dbh_ob.max(), 50)
    ax[1].plot(xx, mid_a * (xx / mid_d) ** 2.0, color="k", ls="--", lw=1.1,
               label="isometry (b = 2)")
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("Diameter outside bark at breast height (cm)")
    ax[1].set_ylabel("Bark cross-sectional area (cm$^2$)")
    ax[1].set_title("(b) Scaling of bark area (isometry: b = 2)")
    ax[1].legend(frameon=False, fontsize=9)

    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{FIG}/F8_bark_geometry.png", dpi=200)

    # --- console report -------------------------------------------------------
    pd.set_option("display.width", 200, "display.max_columns", 50)
    print("\n=== T8 bark geometry at breast height ===")
    print(desc.round(3).to_string(index=False))
    print("\n=== species contrast (bark share of cross-section) ===")
    print(contrasts.round(4).to_string(index=False))
    print("\n=== T9 size dependence and area scaling ===")
    cols = [c for c in scaling.columns if not c.startswith("rob_")]
    print(scaling[cols].round(4).to_string(index=False))
    print("\n=== robustness (leave-one-out, Spearman) ===")
    print(scaling[["species"] + [c for c in scaling.columns if c.startswith("rob_")]]
          .round(4).to_string(index=False))
    print("\n=== sites ===")
    print(prov.round(3).to_string(index=False))

    # coherence with the Stage 1 mass fractions (18.9% WL, 11.5% tamarack of stem mass)
    print("\n=== coherence with Stage 1 stem-bark mass fractions ===")
    for sp, mass_frac in [("western larch", 18.9), ("tamarack", 11.5)]:
        g = bh[bh.species == sp]
        print(f"{sp:15s} area fraction at BH {100*g.f_area.mean():5.1f}% "
              f"| Stage 1 mass fraction of stem {mass_frac:4.1f}%")


if __name__ == "__main__":
    main()
