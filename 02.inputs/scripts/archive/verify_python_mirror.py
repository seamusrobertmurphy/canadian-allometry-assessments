#!/usr/bin/env python3
"""Python mirror of the R analysis, used only to verify the R logic and numbers
(R is not installed in the build sandbox). Same model form, same log-log fit with
Sprugel back-transform correction, same metrics. Not the deliverable; the R code is."""
import numpy as np, pandas as pd, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(ROOT, "..", "data", "enfor",
                                    "EnforCanadaBiomassFinalData_v2007-ENG.csv"))
COMPONENTS = {"wood": "OM_stem_wood", "bark": "OM_stem_bark",
              "branches": "OM_branches", "foliage": "OM_foliage_twigs"}

def load():
    df = pd.read_csv(CSV)
    df["Province"] = df["Province"].astype(str).str.upper().str.strip()
    df["Species_E"] = df["Species_E"].astype(str).str.strip()
    for c in ["Dbh","Height","OM_stem_wood","OM_stem_bark","OM_branches",
              "OM_foliage_twigs","OM_total"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    bs = df[df.Species_E.str.contains("black spruce", case=False, na=False)].copy()
    bs = bs[(bs.Dbh>0) & (bs.OM_total>0) & (bs.Height>0)]
    return bs.reset_index(drop=True)

def fit_component(d, ycol, form):
    d = d[d[ycol] > 0]
    y = np.log(d[ycol].values)
    if form == "dbh_h":
        X = np.column_stack([np.ones(len(d)), np.log(d.Dbh), np.log(d.Height)])
    else:
        X = np.column_stack([np.ones(len(d)), np.log(d.Dbh)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    sigma2 = np.sum(resid**2) / (len(d) - X.shape[1])
    cf = np.exp(sigma2 / 2)
    b1 = np.exp(beta[0]) * cf
    b2 = beta[1]
    b3 = beta[2] if form == "dbh_h" else np.nan
    return b1, b2, b3

def fit_national(train, form):
    return {k: fit_component(train, col, form) for k, col in COMPONENTS.items()}

def predict_total(d, coefs, form):
    tot = np.zeros(len(d))
    for k,(b1,b2,b3) in coefs.items():
        if form == "dbh_h":
            tot += b1 * d.Dbh.values**b2 * d.Height.values**b3
        else:
            tot += b1 * d.Dbh.values**b2
    return tot

def metrics(obs, pred, label):
    obs, pred = np.asarray(obs), np.asarray(pred)
    rb = 100*np.sum(pred-obs)/np.sum(obs)
    rr = 100*np.sqrt(np.mean((pred-obs)**2))/np.mean(obs)
    r2 = 1 - np.sum((obs-pred)**2)/np.sum((obs-np.mean(obs))**2)
    return dict(stratum=label, n=len(obs), mean_obs=round(np.mean(obs),1),
                rel_bias_pct=round(rb,1), rel_rmse_pct=round(rr,1), r2=round(r2,3))

def cv_predict_small(small, form, k=5, seed=42):
    rng = np.random.default_rng(seed)
    fold = rng.permutation(np.tile(np.arange(k), int(np.ceil(len(small)/k)))[:len(small)])
    pred = np.full(len(small), np.nan)
    for f in range(k):
        tr, te = small[fold!=f], small[fold==f]
        coefs = fit_national(tr, form)
        pred[fold==f] = predict_total(te, coefs, form)
    return pred

def stratum(dbh):
    return np.where(dbh<5,"very_small(<5cm)",np.where(dbh<9,"small(5-9cm)","larger(>=9cm)"))

bs = load()
bs["stratum"] = stratum(bs.Dbh.values)
print(f"Black spruce w/ DBH+height: {len(bs)}  (small<9cm: {(bs.Dbh<9).sum()}, very small<5cm: {(bs.Dbh<5).sum()})\n")

for form in ["dbh","dbh_h"]:
    print(f"================= FORM: {form} =================")
    coefs = fit_national(bs, form)
    for k,(b1,b2,b3) in coefs.items():
        print(f"  {k:9s} b1={b1:.5f} b2={b2:.4f}" + (f" b3={b3:.4f}" if form=="dbh_h" else ""))
    bs["pred_nat"] = predict_total(bs, coefs, form)
    rows = [metrics(bs.OM_total, bs.pred_nat, "national -> all")]
    for s in ["larger(>=9cm)","small(5-9cm)","very_small(<5cm)"]:
        d = bs[bs.stratum==s]
        rows.append(metrics(d.OM_total, d.pred_nat, f"national -> {s}"))
    small = bs[bs.Dbh<9].reset_index(drop=True)
    sp = cv_predict_small(small, form)
    rows.append(metrics(small.OM_total, sp, "stratum-specific(CV) -> small(<9cm)"))
    print(pd.DataFrame(rows).to_string(index=False))
    print()
