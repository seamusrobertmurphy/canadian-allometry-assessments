#!/usr/bin/env python3
"""
Stage 2: province-wide test of the Stage 1 larch bark equations on the BC VRI.
Modelled on DellaSala et al. (2022): apply the equations to the province-wide
Vegetation Resources Inventory, quantify larch bark carbon under the national
coefficient vs the larch-specific refit, by leading species and BEC zone, with
Monte Carlo confidence intervals, and map where the correction bites.

Input:  02.inputs/vri/vri_larch.csv        (78,634 LW/LT-leading polygons, WFS pull)
        03.outputs/tables/T4_larch_refits.csv (Stage 1 refit parameters)
Output: 03.outputs/tables/T6_*.csv, T7_*.csv ; 03.outputs/figures/F5_,F6_,F7_.png

Method. VRI gives quadratic mean diameter (QMD, cm, >=12.5 cm utilisation) and live
stems/ha per polygon. Bark per ha = stems/ha * bark(QMD), using (i) the national generic
conifer DBH bark equation (Ung 2008: 0.0153*D^2.2110) and (ii) the Stage 1 species-specific
refit (western larch on LW polygons, tamarack on LT polygons). Both use the identical QMD
treatment, so the difference isolates the equation effect. Carbon = biomass * 0.47.
Applying a convex power at QMD is a first-order stand approximation (Jensen); it is applied
identically to both equations, so the correction ratio is robust. The VRI's own volume-based
bark (Boudewyn 2007) is carried as an independent cross-check.
"""
import numpy as np, pandas as pd, math, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
np.random.seed(7)
R="."; TBL=f"{R}/03.outputs/tables"; FIG=f"{R}/03.outputs/figures"
os.makedirs(TBL,exist_ok=True); os.makedirs(FIG,exist_ok=True)
CFRAC=0.47
NAT=(0.0153,2.2110)  # generic conifer stem-bark, DBH-only (Ung 2008)

# ---- Stage 1 refit parameters (log-log OLS) ----
t4=pd.read_csv(f"{TBL}/T4_larch_refits.csv")
def refit(sp):
    r=t4[(t4.species==sp)&(t4.component=="bark")&(t4.method.str.startswith("log-log"))].iloc[0]
    return float(r.a),float(r.b),float(r.a_se),float(r.b_se)
REF={"LW":refit("western larch"),"LT":refit("tamarack")}   # a,b,a_se,b_se
print("refit LW (a,b,a_se,b_se):",REF["LW"]); print("refit LT:",REF["LT"])

# ---- load + clean VRI ----
df=pd.read_csv(f"{R}/02.inputs/vri/vri_larch.csv",low_memory=False)
n0=len(df)
for c in ["QUAD_DIAM_125","BASAL_AREA","VRI_LIVE_STEMS_PER_HA","PROJ_HEIGHT_1","PROJ_AGE_1",
          "LIVE_STAND_VOLUME_125","BARK_BIOMASS_PER_HA","FEATURE_AREA_SQM","LABEL_CENTRE_X","LABEL_CENTRE_Y","SPECIES_PCT_1"]:
    df[c]=pd.to_numeric(df[c],errors="coerce")
df["area_ha"]=df["FEATURE_AREA_SQM"]/1e4
# stems/ha: use VRI; fill missing from basal area and QMD
ba_per_tree=math.pi*(df["QUAD_DIAM_125"]/200.0)**2           # m2 per tree
stems_from_ba=df["BASAL_AREA"]/ba_per_tree
df["stems_ha"]=df["VRI_LIVE_STEMS_PER_HA"].where(df["VRI_LIVE_STEMS_PER_HA"]>0, stems_from_ba)
clean=df[(df.SPECIES_CD_1.isin(["LW","LT"]))&(df.QUAD_DIAM_125>0)&(df.stems_ha>0)&(df.area_ha>0)].copy()
print(f"cleaned {len(clean)}/{n0} polygons (dropped {n0-len(clean)} missing QMD/stems/area)")

def bark_per_ha(a,b,d,stems): return stems*a*d**b/1000.0   # Mg/ha
Q=clean["QUAD_DIAM_125"].values; S=clean["stems_ha"].values; A=clean["area_ha"].values
sp=clean["SPECIES_CD_1"].values
clean["bark_nat_MgHa"]=bark_per_ha(NAT[0],NAT[1],Q,S)
a_ref=np.where(sp=="LW",REF["LW"][0],REF["LT"][0]); b_ref=np.where(sp=="LW",REF["LW"][1],REF["LT"][1])
clean["bark_ref_MgHa"]=bark_per_ha(a_ref,b_ref,Q,S)
clean["barkC_nat_Mg"]=clean["bark_nat_MgHa"]*A*CFRAC
clean["barkC_ref_Mg"]=clean["bark_ref_MgHa"]*A*CFRAC
clean["dC_MgHa"]=(clean["bark_ref_MgHa"]-clean["bark_nat_MgHa"])*CFRAC

# ---- Table 6: VRI larch resource ----
def resource(g):
    return pd.Series(dict(n_polygons=len(g),area_ha=g.area_ha.sum(),
        mean_QMD=g.QUAD_DIAM_125.mean(),mean_height=g.PROJ_HEIGHT_1.mean(),
        mean_age=g.PROJ_AGE_1.mean(),mean_stems_ha=g.stems_ha.mean(),
        mean_VRI_bark_MgHa=g.BARK_BIOMASS_PER_HA.mean()))
T6=clean.groupby(clean.SPECIES_CD_1.map({"LW":"western larch","LT":"tamarack"})).apply(resource).reset_index(names="leading_species")
T6.to_csv(f"{TBL}/T6_vri_resource.csv",index=False)

# ---- Table 7: province-wide bark carbon national vs refit + Monte Carlo CI ----
def mc_total(mask,key,ndraw=1000):
    q=Q[mask]; s=S[mask]; a=A[mask]; spm=sp[mask]
    tot=[]
    for _ in range(ndraw):
        aa=np.where(spm=="LW",np.random.normal(*REF["LW"][0::2]),np.random.normal(*REF["LT"][0::2]))
        bb=np.where(spm=="LW",np.random.normal(REF["LW"][1],REF["LW"][3]),np.random.normal(REF["LT"][1],REF["LT"][3]))
        tot.append(np.sum(s*aa*q**bb/1000.0*a*CFRAC))
    return np.percentile(tot,[2.5,97.5])
rows=[]
for lab,mask in [("western larch",sp=="LW"),("tamarack",sp=="LT"),("all larch",np.ones(len(sp),bool))]:
    natC=clean.loc[mask,"barkC_nat_Mg"].sum(); refC=clean.loc[mask,"barkC_ref_Mg"].sum()
    lo,hi=mc_total(mask,lab)
    rows.append(dict(leading_species=lab,area_ha=A[mask].sum(),
        national_barkC_Mg=natC,refit_barkC_Mg=refC,diff_Mg=refC-natC,
        diff_pct=100*(refC-natC)/natC,refit_CI95_lo=lo,refit_CI95_hi=hi))
T7=pd.DataFrame(rows); T7.to_csv(f"{TBL}/T7_province_barkC.csv",index=False)

# cross-check vs VRI's own volume-based bark
cc=clean.dropna(subset=["BARK_BIOMASS_PER_HA"])
r=np.corrcoef(cc["bark_nat_MgHa"],cc["BARK_BIOMASS_PER_HA"])[0,1]
ratio=(cc["bark_nat_MgHa"].sum()/cc["BARK_BIOMASS_PER_HA"].sum())

# ---- Figures ----
col={"LW":"#d95f0e","LT":"#2c7fb8"}
# F5: per-ha carbon difference distribution by species
fig,ax=plt.subplots(figsize=(6.2,4.2))
data=[clean.loc[sp==k,"dC_MgHa"].values for k in ["LW","LT"]]
bp=ax.boxplot(data,labels=["western larch","tamarack"],showfliers=False,patch_artist=True)
for p,k in zip(bp["boxes"],["LW","LT"]): p.set_facecolor(col[k]); p.set_alpha(.6)
ax.axhline(0,color="k",lw=.8); ax.set_ylabel("Refit - national bark carbon (Mg C/ha)")
ax.set_title("Per-hectare bark-carbon correction by leading species")
fig.tight_layout(); fig.savefig(f"{FIG}/F5_perha_diff.png",dpi=150,bbox_inches="tight"); plt.close(fig)

# F6: province map of per-ha difference (label centroids, BC Albers)
fig,ax=plt.subplots(figsize=(7,6.5))
sc=ax.scatter(clean.LABEL_CENTRE_X,clean.LABEL_CENTRE_Y,c=clean.dC_MgHa,
              s=3,cmap="RdYlBu_r",vmin=-5,vmax=15,alpha=.6)
ax.set_aspect("equal"); ax.set_xlabel("Easting (m, BC Albers)"); ax.set_ylabel("Northing (m)")
ax.set_title("Larch stem-bark carbon correction across BC (refit - national, Mg C/ha)")
plt.colorbar(sc,ax=ax,shrink=.7,label="Mg C/ha")
fig.tight_layout(); fig.savefig(f"{FIG}/F6_province_map.png",dpi=150,bbox_inches="tight"); plt.close(fig)

# F7: provincial bark carbon national vs refit with CI
fig,ax=plt.subplots(figsize=(6.2,4.2))
labs=T7.leading_species.tolist(); x=np.arange(len(labs)); w=.36
ax.bar(x-w/2,T7.national_barkC_Mg/1e6,w,label="national",color="#999999")
err=np.vstack([(T7.refit_barkC_Mg-T7.refit_CI95_lo)/1e6,(T7.refit_CI95_hi-T7.refit_barkC_Mg)/1e6])
ax.bar(x+w/2,T7.refit_barkC_Mg/1e6,w,yerr=err,capsize=4,label="refit (95% CI)",color="#31a354")
ax.set_xticks(x); ax.set_xticklabels(labs); ax.set_ylabel("Bark carbon (Tg C)")
ax.set_title("Province-wide larch stem-bark carbon"); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(f"{FIG}/F7_province_barkC.png",dpi=150,bbox_inches="tight"); plt.close(fig)

# ---- console ----
pd.set_option("display.width",180,"display.max_columns",20)
print("\n===== TABLE 6 VRI larch resource ====="); print(T6.to_string(index=False,float_format=lambda x:f"{x:.2f}"))
print("\n===== TABLE 7 province-wide bark carbon (Mg C) =====")
print(T7.to_string(index=False,float_format=lambda x:f"{x:,.0f}"))
print(f"\ncross-check: our national QMD bark vs VRI volume-based bark: r={r:.3f}, sum ratio (ours/VRI)={ratio:.2f}")
print("figures F5,F6,F7 written.")
