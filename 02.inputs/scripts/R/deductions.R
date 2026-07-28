# deductions.R
# Turn an allometric relative RMSE into a carbon-credit uncertainty deduction,
# under the two standards this paper touches. This operationalises the paper's
# headline result: a bias/uncertainty difference expressed as a credit haircut.
#
# Provenance of the two rules:
#  - ART-TREES Equation 11, as implemented in the author's uncertainty ebook
#    (training/uncertainty, chapter 1). Maps a relative RMSE directly to a deduction.
#  - ACR IFM on Canadian Forestlands v1.0, Equations 22-24, as examined in
#    acr-methodology-citation-audit.md. Maps TOTAL project uncertainty to a deduction.
#
# IMPORTANT scoping note. The two rules take different inputs. ART-TREES maps the
# allometric relative RMSE more or less directly. ACR maps TOTAL project uncertainty,
# which is the allometric term propagated (ACR Eq. 22) with every other pool and
# activity-data uncertainty. So art_trees_deduction() can take the allometric
# relative RMSE as-is, whereas acr_ifm_deduction() should be fed a propagated total,
# with the allometric relative RMSE used only as a lower-bound proxy when the full
# propagation is not yet built.

# ---- ART-TREES Equation 11 -------------------------------------------------
# UA_t = 0.524417 * (HW90 / 1.645006), HW90 = relRMSE/100. Returns deduction in %.
# Verified against the ebook worked examples: 15.2% -> 4.85%, 18.9% -> 6.03%.
art_trees_deduction <- function(rel_rmse_pct) {
  hw90 <- rel_rmse_pct / 100
  ua   <- 0.524417 * (hw90 / 1.645006)
  100 * ua
}

# ---- ACR IFM (Canadian Forestlands) v1.0, Eq. 22-24 ------------------------
# Combine baseline and with-project uncertainty into a total (Eq. 22), then apply
# the deduction rule (Eq. 23). The printed threshold/floor render ambiguously in
# the source PDF (bold-glyph extraction); they are parameters here and MUST be
# confirmed against the methodology text before any published number is quoted.
acr_total_uncertainty <- function(dC_bsl, unc_bsl_pct, dC_p, unc_p_pct) {
  # Eq. 22: magnitude-weighted combination of the two stock-change uncertainties.
  num <- sqrt((abs(dC_bsl) * unc_bsl_pct)^2 + (abs(dC_p) * unc_p_pct)^2)
  den <- abs(dC_bsl) + abs(dC_p)
  num / den
}

acr_ifm_deduction <- function(total_unc_pct, threshold_pct = 12, floor_ded_pct = 2) {
  # As printed (Eq. 23): at or below threshold a fixed floor deduction applies;
  # above threshold the deduction is the excess over the threshold.
  # NOTE: reconcile against the ACR +/-10% precision requirement; the threshold
  # and floor values are unverified pending a clean read of the methodology.
  ifelse(total_unc_pct <= threshold_pct, floor_ded_pct, total_unc_pct - threshold_pct)
}

# ---- Financial translation (shared) ----------------------------------------
# Revenue consequence of a deduction, for a stated project size and price.
credit_revenue_impact <- function(deduction_pct, project_tonnes, price_per_tonne) {
  frac <- deduction_pct / 100
  data.frame(
    deduction_pct   = deduction_pct,
    credits_deducted = round(project_tonnes * frac),
    revenue_loss     = round(project_tonnes * price_per_tonne * frac),
    stringsAsFactors = FALSE
  )
}
