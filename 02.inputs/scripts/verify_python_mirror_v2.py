#!/usr/bin/env python3
"""Mirror v2: verifies the upgraded R logic (MC-LGOCV, diagnostics, deductions)
and prints numbers for the manuscript. R is not installed in the sandbox."""
import numpy as np, pandas as pd, os
from scipy import stats

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(ROOT, "..", "data", "enfor",
                                    "EnforCanadaBiomassFinalData_v2007-ENG.csv"))
COMPONENTS = {"wood":"OM_stem_wood","bark":"OM_stem_bark","branches":"OM_branches","foliage":"OM_foliage_twigs"}

def load():
    df = pd.read_csv(CSV)
    df["Species_E"]=df.Species_E.astype(str).str.strip()
    for c in ["Dbh","Height","OM_stem_wood","OM_stem_bark","OM_branches","OM_foliage_twigs","OM_total"]:
        df[c]=pd.to_numeric(df[c],errors="coerce")
    bs=df[df.Species_E.str.contains("black spruce",case=False,na=False)].copy()
    bs=bs[(bs.Dbh>0)&(bs.OM_total>0)&(bs.Height>0)].reset_index(drop=True)
    bs["stratum"]=np.where(bs.Dbh<5,"very_small(<5cm)",np.where(bs.Dbh<9,"small(5-9cm)","larger(>=9cm)"))
    return bs

def fit_comp(d,y,form):
    d=d[d[y]>0]
    Y=np.log(d[y].values)
    X=np.column_stack([np.ones(len(d)),np.log(d.Dbh)]+([np.log(d.Height)] if form=="dbh_h" else []))
    b,*_=np.linalg.lstsq(X,Y,rcond=None)
    resid=Y-X@b; s2=np.sum(resid**2)/(len(d)-X.shape[1]); cf=np.exp(s2/2)
    return (np.exp(b[0])*cf, b[1], (b[2] if form=="dbh_h" else np.nan))

def fit_nat(tr,form): return {k:fit_comp(tr,c,form) for k,c in COMPONENTS.items()}
def pred_tot(d,coefs,form):
    t=np.zeros(len(d))
    for k,(b1,b2,b3) in coefs.items():
        t+= b1*d.Dbh.values**b2*(d.Height.values**b3 if form=="dbh_h" else 1)
    return t
def rel_bias(o,p): return 100*np.sum(p-o)/np.sum(o)
def rel_rmse(o,p): return 100*np.sqrt(np.mean((p-o)**2))/np.mean(o)

def dbh_class(dbh):
    return pd.cut(dbh,bins=[0,5,9,15,25,100],labels=["0-5","5-9","9-15","15-25",">25"],include_lowest=True)

def mc_lgocv(bs,form,iters=100,p=0.8,seed=8787):
    rng=np.random.default_rng(seed)
    cls=dbh_class(bs.Dbh.values); O=[];P=[];S=[]
    for _ in range(iters):
        tr=[]
        for lv in cls.categories:
            rows=np.where(cls==lv)[0]
            if len(rows)==0: continue
            tr+=list(rng.choice(rows,max(1,int(np.floor(len(rows)*p))),replace=False))
        mask=np.zeros(len(bs),bool); mask[tr]=True
        trd=bs[mask]; ted=bs[~mask]
        if len(ted)<5: continue
        coefs=fit_nat(trd,form); pr=pred_tot(ted,coefs,form)
        O+=list(ted.OM_total.values); P+=list(pr); S+=list(ted.stratum.values)
    O=np.array(O);P=np.array(P);S=np.array(S)
    rows=[("all",O,P)]+[(s,O[S==s],P[S==s]) for s in ["larger(>=9cm)","small(5-9cm)","very_small(<5cm)"]]
    return [dict(stratum=s,n=len(o),rel_bias=round(rel_bias(o,p_),1),rel_rmse=round(rel_rmse(o,p_),1)) for s,o,p_ in rows]

def art(r): return 100*0.524417*((r/100)/1.645006)

bs=load()
print(f"n black spruce (DBH+H) = {len(bs)}\n")

# Diagnostics
lin=np.polyfit(bs.Dbh,bs.OM_total,1)
W,pval=stats.shapiro(bs.OM_total.sample(min(5000,len(bs)),random_state=1))
logfit=np.polyfit(np.log(bs.Dbh),np.log(bs.OM_total),1)
logresid=np.log(bs.OM_total)-(logfit[0]*np.log(bs.Dbh)+logfit[1])
Wr,pr=stats.shapiro(logresid)
# BP on linear
resid=bs.OM_total-(lin[0]*bs.Dbh+lin[1]); r2=resid**2
aux=np.polyfit(bs.Dbh,r2,1); pred_aux=aux[0]*bs.Dbh+aux[1]
R2aux=1-np.sum((r2-pred_aux)**2)/np.sum((r2-r2.mean())**2)
BP=len(bs)*R2aux
print(f"[diagnostics] AGB normality Shapiro W={W:.3f} p={pval:.2e} (skew={stats.skew(bs.OM_total):.2f})")
print(f"[diagnostics] log-resid Shapiro W={Wr:.3f} p={pr:.2e}")
print(f"[diagnostics] Breusch-Pagan (linear) LM={BP:.1f} -> p={1-stats.chi2.cdf(BP,1):.2e}\n")

for form in ["dbh","dbh_h"]:
    print(f"===== MC-LGOCV (100x, DBH-stratified), form={form} =====")
    for r in mc_lgocv(bs,form): print("  ",r)
    print()

mc=mc_lgocv(bs,"dbh_h")
small=[r for r in mc if r["stratum"]=="small(5-9cm)"][0]["rel_rmse"]
allr =[r for r in mc if r["stratum"]=="all"][0]["rel_rmse"]
print(f"[deduction] small-stratum OOS relRMSE={small}% -> ART-TREES deduction {art(small):.2f}%")
print(f"[deduction] all-black-spruce OOS relRMSE={allr}% -> ART-TREES deduction {art(allr):.2f}%")
print(f"[deduction] @1M tCO2e, $5/t: revenue loss ~ ${round(1e6*5*art(small)/100):,}")
