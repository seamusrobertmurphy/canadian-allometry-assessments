#!/usr/bin/env python3
"""
Stage 1: component-wise accuracy and uncertainty of the national biomass coefficients
for larch, and larch-specific refits. Modelled on Xing (2019) accuracy/uncertainty and
Delcourt (2022) statistics and visualization.

Datasets (open):
  tamarack (Larix laricina)  -- ENFOR, in-sample (national calibration data). metric.
  western larch (L. occidentalis) -- LegacyTreeData, independent. imperial -> metric.

Components: stem bark (focal), stem wood, total AGB.
National coefficients: generic Conifers (operative predictor for the unlisted western larch)
and Tamarack larch, DBH and DBH+height forms, read from 02.inputs/larch/*.csv.

Outputs: 03.outputs/tables/*.csv and 03.outputs/figures/*.png
Run from repo root:  python3 02.inputs/scripts/stage1_accuracy_refit.py
Deps: numpy, pandas, scipy, matplotlib.
"""
import csv, math, os, numpy as np, pandas as pd
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(42)
ROOT="."
TBL=os.path.join(ROOT,"03.outputs","tables"); FIG=os.path.join(ROOT,"03.outputs","figures")
os.makedirs(TBL,exist_ok=True); os.makedirs(FIG,exist_ok=True)
IN2CM,FT2M,LB2KG=2.54,0.3048,0.453592

def num(x):
    try: return float(x)
    except: return None

# ---------- national coefficients ----------
def load_coef():
    C={}
    for r in csv.DictReader(open(f"{ROOT}/02.inputs/larch/nfi_tree-level_allometric_dbh.csv",encoding="latin-1")):
        C[(r["Species"],"dbh",r["Component"])]=(float(r["a"]),float(r["b"]),None)
    for r in csv.DictReader(open(f"{ROOT}/02.inputs/larch/nfi_tree-level_allometric_dbh-height.csv",encoding="latin-1")):
        C[(r["Species"],"dbhh",r["Component"])]=(float(r["a"]),float(r["b"]),float(r["c"]))
    return C
COEF=load_coef()
COMPS=["Wood","Bark","Branches","Foliage"]

def pred_comp(sp,form,comp,d,h):
    a,b,c=COEF[(sp,form,comp)]
    return a*d**b if form=="dbh" else (a*d**b*h**c if h else np.nan)
def pred(sp,form,comp,d,h):
    if comp=="total": return sum(pred_comp(sp,form,k,d,h) for k in COMPS)
    return pred_comp(sp,form,{"bark":"Bark","wood":"Wood"}[comp],d,h)

# ---------- observed data ----------
def load_data():
    tam=[]
    for r in csv.DictReader(open(f"{ROOT}/02.inputs/enfor/EnforCanadaBiomassFinalData_v2007-ENG.csv",encoding="latin-1")):
        if "tamarack" in (r.get("Species_E") or "").lower():
            d,h,bk,wd,tot=num(r["Dbh"]),num(r["Height"]),num(r["OM_stem_bark"]),num(r["OM_stem_wood"]),num(r["OM_total"])
            if d and bk is not None:
                tam.append(dict(sp="tamarack",dbh=d,h=h,bark=bk,wood=wd,total=tot))
    wl=[]
    for r in csv.DictReader(open(f"{ROOT}/02.inputs/legacy-tree/tree.txt",encoding="latin-1")):
        if r.get("spcd")=="73":
            d,bk,wd,tot=num(r["st_ob_d_bh"]),num(r["st_bk_dw"]),num(r["st_wd_dw"]),num(r["ag_dw"])
            if d and bk is not None:
                wl.append(dict(sp="western larch",dbh=d*IN2CM,h=None,
                               bark=bk*LB2KG,wood=(wd*LB2KG if wd else None),total=(tot*LB2KG if tot else None)))
    return tam,wl
TAM,WL=load_data()

# ---------- metrics ----------
def metrics(obs,prd):
    obs=np.asarray(obs,float); prd=np.asarray(prd,float)
    m=np.isfinite(obs)&np.isfinite(prd); obs,prd=obs[m],prd[m]
    if len(obs)<2: return dict(n=len(obs),mean_obs=np.nan,bias=np.nan,rel_bias=np.nan,rmse=np.nan,rel_rmse=np.nan,r2=np.nan)
    e=prd-obs
    ss_res=np.sum(e**2); ss_tot=np.sum((obs-obs.mean())**2)
    return dict(n=len(obs),mean_obs=obs.mean(),bias=e.mean(),
                rel_bias=100*e.sum()/obs.sum(),rmse=math.sqrt((e**2).mean()),
                rel_rmse=100*math.sqrt((e**2).mean())/obs.mean(),
                r2=(1-ss_res/ss_tot) if ss_tot>0 else np.nan)

def classes(rows):
    return {"all":rows,"<20":[r for r in rows if r["dbh"]<20],
            "20-40":[r for r in rows if 20<=r["dbh"]<40],">40":[r for r in rows if r["dbh"]>=40]}

# ================= TABLE 1: descriptive stats =================
def descr(rows,key):
    v=np.array([r[key] for r in rows if r.get(key) is not None],float)
    if len(v)==0: return dict(n=0)
    return dict(n=len(v),mean=v.mean(),sd=v.std(ddof=1) if len(v)>1 else np.nan,
                min=v.min(),max=v.max())
rows_t1=[]
for name,rows in [("tamarack (ENFOR)",TAM),("western larch (LegacyTreeData)",WL)]:
    for key,lab in [("dbh","DBH (cm)"),("h","Height (m)"),("bark","Stem bark (kg)"),
                    ("wood","Stem wood (kg)"),("total","Total AGB (kg)")]:
        d=descr(rows,key); d.update(dataset=name,variable=lab); rows_t1.append(d)
T1=pd.DataFrame(rows_t1)[["dataset","variable","n","mean","sd","min","max"]]
T1.to_csv(f"{TBL}/T1_descriptive_stats.csv",index=False)

# ================= TABLE 2: national coefficients =================
rows_t2=[]
for sp in ["Conifers","Tamarack larch"]:
    for form in ["dbh","dbhh"]:
        for comp in COMPS:
            a,b,c=COEF[(sp,form,comp)]
            rows_t2.append(dict(coefficient=sp,form=("DBH" if form=="dbh" else "DBH+H"),
                                component=comp,a=a,b=b,c=c))
T2=pd.DataFrame(rows_t2); T2.to_csv(f"{TBL}/T2_national_coefficients.csv",index=False)

# ================= TABLE 3: accuracy of national coefficients =================
rows_t3=[]
for spname,rows in [("tamarack",TAM),("western larch",WL)]:
    for comp in ["bark","wood","total"]:
        for coefsp in ["Conifers","Tamarack larch"]:
            for form in ["dbh","dbhh"]:
                if form=="dbhh" and not any(r["h"] for r in rows): continue
                for cls,sub in classes(rows).items():
                    if not sub: continue
                    obs=[r[comp] for r in sub]
                    prd=[pred(coefsp,form,comp,r["dbh"],r["h"]) for r in sub]
                    m=metrics(obs,prd)
                    rows_t3.append(dict(species=spname,component=comp,coefficient=coefsp,
                        form=("DBH" if form=="dbh" else "DBH+H"),dbh_class=cls,**m))
T3=pd.DataFrame(rows_t3)
T3.to_csv(f"{TBL}/T3_accuracy_national.csv",index=False)

# ================= TABLE 4: larch-specific refits =================
def loglog_fit(d,y):
    d=np.asarray(d,float); y=np.asarray(y,float)
    X=np.column_stack([np.ones_like(d),np.log(d)]); ly=np.log(y)
    beta,_,_,_=np.linalg.lstsq(X,ly,rcond=None)
    resid=ly-X@beta; n=len(y); see=math.sqrt((resid**2).sum()/(n-2))
    cov=see**2*np.linalg.inv(X.T@X); se=np.sqrt(np.diag(cov))
    cf=math.exp(see**2/2)
    pred_y=cf*np.exp(X@beta)
    return dict(a=math.exp(beta[0])*cf,b=beta[1],a_se=abs(math.exp(beta[0])*cf)*se[0],b_se=se[1],
                cf=cf,see=see,**{f"fit_{k}":v for k,v in metrics(y,pred_y).items()})
def wnls_fit(d,y):
    d=np.asarray(d,float); y=np.asarray(y,float)
    f=lambda d,a,b:a*d**b
    p0=[0.02,2.1]
    popt,_=curve_fit(f,d,y,p0=p0,maxfev=10000)
    resid=y-f(d,*popt)
    # variance exponent c: log(resid^2) ~ log(d); slope=2c
    mask=np.abs(resid)>0
    cvar=np.polyfit(np.log(d[mask]),np.log(resid[mask]**2),1)[0]/2
    sigma=d**cvar
    popt,pcov=curve_fit(f,d,y,p0=popt,sigma=sigma,absolute_sigma=False,maxfev=10000)
    se=np.sqrt(np.diag(pcov)); pred_y=f(d,*popt)
    return dict(a=popt[0],b=popt[1],a_se=se[0],b_se=se[1],c_var=cvar,
                **{f"fit_{k}":v for k,v in metrics(y,pred_y).items()})
def cv_refit(rows,comp,national_sp="Conifers"):
    # LOO for small n, else 10-fold; compare national vs log-log refit out of sample
    d=np.array([r["dbh"] for r in rows]); y=np.array([r[comp] for r in rows])
    n=len(rows); k=n if n<30 else 10
    idx=np.arange(n); np.random.shuffle(idx); folds=np.array_split(idx,k)
    no,npd,ro,rp=[],[],[],[]
    for fo in folds:
        te=set(fo.tolist()); tr=[i for i in idx if i not in te]
        fit=loglog_fit(d[tr],y[tr])
        for i in fo:
            no.append(y[i]); npd.append(pred(national_sp,"dbh",comp,d[i],None))
            ro.append(y[i]); rp.append(fit["a"]*d[i]**fit["b"])
    return metrics(no,npd),metrics(ro,rp)
rows_t4=[]
for spname,rows in [("tamarack",TAM),("western larch",WL)]:
    for comp in ["bark","wood","total"]:
        d=[r["dbh"] for r in rows]; y=[r[comp] for r in rows if r[comp] is not None]
        d=[r["dbh"] for r in rows if r[comp] is not None]
        if len(y)<5: continue
        ll=loglog_fit(d,y); wn=wnls_fit(d,y)
        natcv,refcv=cv_refit([r for r in rows if r[comp] is not None],comp)
        base=dict(species=spname,component=comp,N=len(y),dbh_min=min(d),dbh_max=max(d),
                  cv_nat_rel_bias=natcv["rel_bias"],cv_nat_rel_rmse=natcv["rel_rmse"],
                  cv_refit_rel_bias=refcv["rel_bias"],cv_refit_rel_rmse=refcv["rel_rmse"])
        rows_t4.append(dict(method="log-log OLS (Baskerville-Sprugel)",a=ll["a"],a_se=ll["a_se"],
            b=ll["b"],b_se=ll["b_se"],c_var=np.nan,cf=ll["cf"],
            rmse=ll["fit_rmse"],rel_rmse=ll["fit_rel_rmse"],r2=ll["fit_r2"],**base))
        rows_t4.append(dict(method="weighted NLS (DBH^2c)",a=wn["a"],a_se=wn["a_se"],
            b=wn["b"],b_se=wn["b_se"],c_var=wn["c_var"],cf=np.nan,
            rmse=wn["fit_rmse"],rel_rmse=wn["fit_rel_rmse"],r2=wn["fit_r2"],**base))
T4=pd.DataFrame(rows_t4)
T4.to_csv(f"{TBL}/T4_larch_refits.csv",index=False)

# ================= TABLE 5: descriptive + Shapiro-Wilk on response and residuals =================
rows_t5=[]
for spname,rows in [("tamarack",TAM),("western larch",WL)]:
    y=np.array([r["bark"] for r in rows],float)
    d=np.array([r["dbh"] for r in rows],float)
    fit=loglog_fit(d,y); resid=np.log(y)-np.log(fit["a"]/fit["cf"])-fit["b"]*np.log(d)
    for lab,v in [("stem bark (kg)",y),("log stem bark",np.log(y)),("log-log residuals",resid)]:
        W,p=stats.shapiro(v)
        rows_t5.append(dict(species=spname,variable=lab,n=len(v),mean=v.mean(),
            sd=v.std(ddof=1),se=v.std(ddof=1)/math.sqrt(len(v)),
            skew=stats.skew(v),kurtosis=stats.kurtosis(v),shapiro_W=W,shapiro_p=p))
T5=pd.DataFrame(rows_t5); T5.to_csv(f"{TBL}/T5_normality.csv",index=False)

# ================= FIGURES =================
CFG=dict(dpi=150,bbox_inches="tight")
col={"tamarack":"#2c7fb8","western larch":"#d95f0e"}
# refit params (bark) for curves
barkfit={sp:loglog_fit([r["dbh"] for r in rows],[r["bark"] for r in rows])
         for sp,rows in [("tamarack",TAM),("western larch",WL)]}

# Fig 1: bark vs DBH per species with national + refit curves; log-log inset
fig,ax=plt.subplots(1,2,figsize=(11,4.5))
for sp,rows in [("tamarack",TAM),("western larch",WL)]:
    d=np.array([r["dbh"] for r in rows]); y=np.array([r["bark"] for r in rows])
    ax[0].scatter(d,y,s=14,alpha=.5,color=col[sp],label=sp)
    xs=np.linspace(d.min(),d.max(),100)
    ax[0].plot(xs,COEF[("Conifers","dbh","Bark")][0]*xs**COEF[("Conifers","dbh","Bark")][1],
               "--",color=col[sp],lw=1,alpha=.9)
    ax[0].plot(xs,barkfit[sp]["a"]*xs**barkfit[sp]["b"],"-",color=col[sp],lw=1.8)
    ax[1].scatter(np.log(d),np.log(y),s=14,alpha=.5,color=col[sp])
ax[0].set_xlabel("DBH (cm)"); ax[0].set_ylabel("Stem bark (kg)")
ax[0].set_title("Stem bark vs DBH (dashed: national Conifers; solid: larch refit)")
ax[0].legend(frameon=False,fontsize=9)
ax[1].set_xlabel("log DBH"); ax[1].set_ylabel("log stem bark"); ax[1].set_title("Log-log")
fig.tight_layout(); fig.savefig(f"{FIG}/F1_bark_vs_dbh.png",**CFG); plt.close(fig)

# Fig 2: observed vs predicted (national Conifers, DBH), 1:1
fig,ax=plt.subplots(figsize=(5.2,5))
for sp,rows in [("tamarack",TAM),("western larch",WL)]:
    o=np.array([r["bark"] for r in rows]); p=np.array([pred("Conifers","dbh","bark",r["dbh"],None) for r in rows])
    ax.scatter(o,p,s=16,alpha=.5,color=col[sp],label=sp)
lim=[0,max(max([r["bark"] for r in TAM]),max([r["bark"] for r in WL]))*1.05]
ax.plot(lim,lim,"k-",lw=1); ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel("Observed stem bark (kg)"); ax.set_ylabel("Predicted (national Conifers, kg)")
ax.set_title("Observed vs predicted stem bark"); ax.legend(frameon=False,fontsize=9)
fig.tight_layout(); fig.savefig(f"{FIG}/F2_obs_vs_pred.png",**CFG); plt.close(fig)

# Fig 3: relative bias by diameter class (national Conifers, bark)
fig,ax=plt.subplots(figsize=(6.2,4.2))
clslabels=["<20","20-40",">40"]; x=np.arange(len(clslabels)); w=.36
for i,(sp,rows) in enumerate([("tamarack",TAM),("western larch",WL)]):
    vals=[]
    for cls in clslabels:
        sub=classes(rows)[cls]
        vals.append(metrics([r["bark"] for r in sub],[pred("Conifers","dbh","bark",r["dbh"],None) for r in sub])["rel_bias"] if sub else np.nan)
    ax.bar(x+(i-.5)*w,vals,w,color=col[sp],label=sp)
ax.axhline(0,color="k",lw=.8); ax.set_xticks(x); ax.set_xticklabels([f"{c} cm" for c in clslabels])
ax.set_ylabel("Relative bias (%)"); ax.set_title("National Conifers stem-bark bias by diameter class")
ax.legend(frameon=False,fontsize=9)
fig.tight_layout(); fig.savefig(f"{FIG}/F3_relbias_by_class.png",**CFG); plt.close(fig)

# Fig 4: log-log residuals vs fitted (refit diagnostics)
fig,ax=plt.subplots(1,2,figsize=(11,4.2))
for j,(sp,rows) in enumerate([("tamarack",TAM),("western larch",WL)]):
    d=np.array([r["dbh"] for r in rows]); y=np.array([r["bark"] for r in rows])
    f=barkfit[sp]; fitted=np.log(f["a"]/f["cf"])+f["b"]*np.log(d); resid=np.log(y)-fitted
    ax[j].scatter(fitted,resid,s=16,alpha=.5,color=col[sp]); ax[j].axhline(0,color="k",lw=.8)
    ax[j].set_xlabel("Fitted (log kg)"); ax[j].set_ylabel("Residual (log)"); ax[j].set_title(f"{sp}")
fig.suptitle("Log-log residuals vs fitted (stem-bark refit)")
fig.tight_layout(); fig.savefig(f"{FIG}/F4_residuals.png",**CFG); plt.close(fig)

# ================= console summary =================
pd.set_option("display.width",180,"display.max_columns",30)
print("\n===== TABLE 1 descriptive ====="); print(T1.to_string(index=False,float_format=lambda x:f"{x:.2f}"))
print("\n===== TABLE 3 accuracy (stem bark, overall + classes) =====")
print(T3[(T3.component=="bark")&(T3.coefficient=="Conifers")][["species","form","dbh_class","n","bias","rel_bias","rmse","rel_rmse","r2"]].to_string(index=False,float_format=lambda x:f"{x:.2f}"))
print("\n===== TABLE 4 refits (stem bark) =====")
print(T4[T4.component=="bark"][["species","method","a","a_se","b","b_se","c_var","cf","rel_rmse","r2","cv_nat_rel_rmse","cv_refit_rel_rmse"]].to_string(index=False,float_format=lambda x:f"{x:.3f}"))
print("\n===== TABLE 5 normality (stem bark) =====")
print(T5.to_string(index=False,float_format=lambda x:f"{x:.3f}"))
print("\nFigures written to 03.outputs/figures/ ; tables to 03.outputs/tables/")
