#!/usr/bin/env python3
"""
Genus-level larch (Larix) stem-bark bias analysis.

Scope C (genus-level), decided 2026-07-16. Evaluates the Canadian national
biomass bark coefficients (Lambert 2005 / Ung 2008) against destructively
measured stem-bark mass for two larches:

  * Tamarack (Larix laricina)  -- ENFOR, IN-SAMPLE (ENFOR is the coefficient's
    own calibration data). Metric (cm, m, kg).
  * Western larch (L. occidentalis) -- LegacyTreeData (Radtke 2021), OUT-OF-SAMPLE.
    Imperial -> metric (in*2.54=cm, ft*0.3048=m, lb*0.453592=kg). No height; one site.

National bark coefficients (from 02.inputs/larch/README.md, byte-verified vs NRCan calculator):
  DBH-only    bark_kg = a*DBH^b            Conifers a=0.0153 b=2.2110 ; Tamarack a=0.0174 b=2.1109
  DBH+height  bark_kg = a*DBH^b*H^c        Conifers a=0.0101 b=1.8486 c=0.5525 ; Tamarack a=0.0120 b=1.7059 c=0.5811

Sign convention: rel_bias = 100*(pred-obs)/obs.  NEGATIVE = national UNDER-predicts.

Control: applying the Tamarack coefficient to ENFOR tamarack should give ~0 bias
(it is the training data); this validates units + coefficient application.

Run from the repo root (publications-academic/canadian-tree-allometry/):
    python3 02.inputs/scripts/larch_bark_genus_analysis.py
Dependencies: numpy only.
"""
import csv, math, numpy as np
np.random.seed(42)

ENFOR  = "02.inputs/enfor/EnforCanadaBiomassFinalData_v2007-ENG.csv"
LEGACY = "02.inputs/legacy-tree/tree.txt"
IN2CM, FT2M, LB2KG = 2.54, 0.3048, 0.453592
COEF = {("Conifers","dbh"):  dict(a=0.0153,b=2.2110),
        ("Tamarack","dbh"):  dict(a=0.0174,b=2.1109),
        ("Conifers","dbhh"): dict(a=0.0101,b=1.8486,c=0.5525),
        ("Tamarack","dbhh"): dict(a=0.0120,b=1.7059,c=0.5811)}

def num(x):
    try: return float(x)
    except: return None

def load():
    enfor=[]
    for r in csv.DictReader(open(ENFOR, encoding="latin-1")):
        if "tamarack" in (r.get("Species_E") or "").lower():
            dbh,h,bk,wd = num(r.get("Dbh")),num(r.get("Height")),num(r.get("OM_stem_bark")),num(r.get("OM_stem_wood"))
            if dbh and bk is not None:
                enfor.append(dict(species="tamarack",source="ENFOR",insample=True,dbh=dbh,h=h,bark=bk,wood=wd,
                                  site="ENFOR|"+(r.get("Province") or "").upper()+"|"+(r.get("Location") or "")))
    wl=[]
    for r in csv.DictReader(open(LEGACY, encoding="latin-1")):
        if r.get("spcd") in ("73","71"):
            d,bk,wd,h = num(r.get("st_ob_d_bh")),num(r.get("st_bk_dw")),num(r.get("st_wd_dw")),num(r.get("tr_ht"))
            if d and bk is not None:
                wl.append(dict(species=("western_larch" if r.get("spcd")=="73" else "tamarack"),source="Legacy",
                               insample=False,dbh=d*IN2CM,h=(h*FT2M if h else None),
                               bark=bk*LB2KG,wood=(wd*LB2KG if wd else None),site="Legacy|"+(r.get("loc") or "")))
    return enfor, [r for r in wl if r["species"]=="western_larch"], [r for r in wl if r["species"]=="tamarack"]

def predict(rows, which, form):
    p=COEF[(which,form)]
    return [ (p["a"]*r["dbh"]**p["b"]) if form=="dbh"
             else (None if not r["h"] else p["a"]*r["dbh"]**p["b"]*r["h"]**p["c"]) for r in rows ]

def metrics(obs, pred):
    o,pr=[],[]
    for a,b in zip(obs,pred):
        if b is None: continue
        o.append(a); pr.append(b)
    if not o: return None
    o,pr=np.array(o),np.array(pr); e=pr-o
    return dict(n=len(o), mean_obs=o.mean(),
                rel_bias=100*e.sum()/o.sum(), rel_rmse=100*math.sqrt((e**2).mean())/o.mean())

def report(name, rows, which, form):
    m=metrics([r["bark"] for r in rows], predict(rows,which,form))
    print(f"  {name:26s} {which:8s} {form:4s} | " +
          (f"n={m['n']:4d} meanObs={m['mean_obs']:6.2f}kg relBias={m['rel_bias']:+7.1f}% relRMSE={m['rel_rmse']:6.1f}%"
           if m else "n=0"))

def classes(rows):
    return [("<20",[r for r in rows if r['dbh']<20]),
            ("20-40",[r for r in rows if 20<=r['dbh']<40]),
            (">40",[r for r in rows if r['dbh']>=40])]

def fit_loglog(rows):
    X=np.array([[1.0,math.log(r['dbh'])] for r in rows]); y=np.array([math.log(r['bark']) for r in rows])
    beta,*_=np.linalg.lstsq(X,y,rcond=None); see=math.sqrt(((y-X@beta)**2).sum()/(len(y)-2))
    return beta, math.exp(see**2/2)   # Baskerville/Sprugel back-transform correction

def main():
    enfor, wl, lt = load()
    print(f"ENFOR tamarack n={len(enfor)} (all +H) | Legacy western larch n={len(wl)} (no H, 1 site) | Legacy tamarack bark n={len(lt)}")

    print("\n== CONTROL: Tamarack coeff on ENFOR tamarack (in-sample; expect ~0) ==")
    report("ENFOR tamarack",enfor,"Tamarack","dbhh"); report("ENFOR tamarack",enfor,"Tamarack","dbh")

    print("\n== ENFOR tamarack: generic Conifers vs Tamarack ==")
    for form in ("dbh","dbhh"):
        for which in ("Conifers","Tamarack"): report("ENFOR tamarack",enfor,which,form)

    print("\n== OUT-OF-SAMPLE western larch (DBH-only) ==")
    for which in ("Conifers","Tamarack"): report("Legacy western larch",wl,which,"dbh")

    print("\n== Genus pooled (ENFOR tamarack + WL), Conifers DBH, by class ==")
    genus=enfor+wl
    report("Larix pooled",genus,"Conifers","dbh"); report("Larix pooled",genus,"Tamarack","dbh")
    for c,sub in classes(genus):
        if sub: report(f"Larix {c}",sub,"Conifers","dbh")
        else: print(f"  Larix {c:20s} | n=0")

    # 10-fold CV: national Conifers vs genus refit
    idx=np.arange(len(genus)); np.random.shuffle(idx); folds=np.array_split(idx,10)
    no,npd,ro,rp=[],[],[],[]
    for k in range(10):
        te=set(folds[k].tolist()); tr=[genus[i] for i in idx if i not in te]; beta,cf=fit_loglog(tr)
        for i in folds[k]:
            r=genus[i]; no.append(r['bark']); npd.append(COEF[("Conifers","dbh")]["a"]*r['dbh']**COEF[("Conifers","dbh")]["b"])
            ro.append(r['bark']); rp.append(cf*math.exp(beta[0]+beta[1]*math.log(r['dbh'])))
    mn,mr=metrics(no,npd),metrics(ro,rp); beta,cf=fit_loglog(genus)
    print(f"\n== 10-fold CV (pooled, DBH-only) ==\n  national Conifers relBias={mn['rel_bias']:+.1f}% relRMSE={mn['rel_rmse']:.1f}%"
          f"\n  genus-refit      relBias={mr['rel_bias']:+.1f}% relRMSE={mr['rel_rmse']:.1f}%"
          f"\n  Larix eq: bark={cf*math.exp(beta[0]):.5f}*DBH^{beta[1]:.4f} (CF={cf:.4f})")

    # bark-fraction mechanism + WL bootstrap
    def frac(rows):
        fs=[r['bark']/(r['bark']+r['wood']) for r in rows if r['wood']]; return np.mean(fs),np.std(fs),len(fs)
    ft,fw=frac(enfor),frac(wl)
    aC,bC=COEF[("Conifers","dbh")]["a"],COEF[("Conifers","dbh")]["b"]
    def rb(s):
        o=np.array([r['bark'] for r in s]); p=np.array([aC*r['dbh']**bC for r in s]); return 100*(p-o).sum()/o.sum()
    boot=[rb([wl[i] for i in np.random.randint(0,len(wl),len(wl))]) for _ in range(5000)]
    print(f"\n== Mechanism / robustness ==\n  bark fraction tamarack={ft[0]*100:.1f}%±{ft[1]*100:.1f}  western larch={fw[0]*100:.1f}%±{fw[1]*100:.1f}"
          f"\n  WL Conifers rel bias={rb(wl):+.1f}% 95%CI=({np.percentile(boot,2.5):+.1f},{np.percentile(boot,97.5):+.1f}) n={len(wl)}")

    # Size dependence per species: proportional error vs DBH under the generic conifer coeff.
    def slope_t(rows):
        d=np.array([r['dbh'] for r in rows]); pe=np.array([(aC*r['dbh']**bC-r['bark'])/r['bark'] for r in rows])
        b1,b0=np.polyfit(d,pe,1); sse=((pe-(b1*d+b0))**2).sum()
        se=math.sqrt(sse/(len(d)-2)/((d-d.mean())**2).sum())
        return b1,b0,b1/se,len(d),d.min(),d.max()
    print("\n== Size dependence (proportional error vs DBH, generic Conifers) ==")
    for nm,rows in [("tamarack (ENFOR)",enfor),("western larch",wl)]:
        b1,b0,t,n,dmn,dmx=slope_t(rows)
        print(f"  {nm:18s}: slope={b1:+.4f}/cm intercept={b0:+.3f} t={t:+.2f} n={n} DBH=({dmn:.1f},{dmx:.1f})")

if __name__=="__main__": main()
