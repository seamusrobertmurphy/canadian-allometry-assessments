# run_all.R
# Orchestrates the open ENFOR black-spruce equation comparison.
# Run from the analysis/ directory:  Rscript run_all.R
#
# No external packages required (base R + stats only).

# Resolve this script's directory under Rscript (via --file=) or fall back to cwd.
script_dir <- function() {
  a <- commandArgs(FALSE)
  f <- sub("^--file=", "", a[grepl("^--file=", a)])
  if (length(f)) dirname(normalizePath(f)) else getwd()
}
root <- script_dir()

source(file.path(root, "R", "metrics.R"))
source(file.path(root, "R", "01_load_clean.R"))
source(file.path(root, "R", "02_national_equation.R"))
source(file.path(root, "R", "03_fit_and_bias.R"))
source(file.path(root, "R", "03b_cross_validation.R"))
source(file.path(root, "R", "diagnostics.R"))
source(file.path(root, "R", "deductions.R"))

data_path <- normalizePath(file.path(root, "..", "data", "enfor",
                                     "EnforCanadaBiomassFinalData_v2007-ENG.csv"))

message("Loading ENFOR from: ", data_path)
df <- load_enfor(data_path)
bs <- add_size_stratum(black_spruce(df, require_height = TRUE))
message(sprintf("Black spruce with DBH+height: %d trees (%d small <9cm, %d very small <5cm)",
                nrow(bs), sum(bs$Dbh < 9), sum(bs$Dbh < 5)))

for (form in c("dbh", "dbh_h")) {
  cat("\n=====================  FORM:", form, " =====================\n")
  res <- run_bias_analysis(bs, form = form)
  cat("\n-- National-form coefficients (open reproduction) --\n")
  print(res$national_coefs[, c("component", "form", "b1", "b2", "b3", "n")], row.names = FALSE)
  cat("\n-- National model, overall --\n");        print(res$national_overall, row.names = FALSE)
  cat("\n-- National model, by size stratum --\n"); print(res$national_by_stratum, row.names = FALSE)
  cat("\n-- Stratum-specific model on small trees (5-fold CV) --\n")
  print(res$stratum_specific_small, row.names = FALSE)
}

# ---- Diagnostics (justify the log form) ----
cat("\n=====================  DIAGNOSTICS  =====================\n")
dg <- diagnostic_block(bs)
cat("\nNormality of total AGB (natural scale):\n");  print(dg$normality_natural, row.names = FALSE)
cat("\nNormality of log-model residuals:\n");        print(dg$normality_logresid, row.names = FALSE)
cat("\nBreusch-Pagan, linear model:\n");             print(dg$bp_natural, row.names = FALSE)
cat("\nBreusch-Pagan, log-log model:\n");            print(dg$bp_log, row.names = FALSE)

# ---- Monte Carlo LGOCV (out-of-sample) ----
cat("\n=====================  MC-LGOCV (100x, DBH-stratified)  =====================\n")
for (form in c("dbh", "dbh_h")) {
  cat("\n-- form:", form, "--\n")
  print(mc_lgocv(bs, form = form, iters = 100), row.names = FALSE)
}

# ---- Deduction reporting (the money sentence) ----
cat("\n=====================  CREDIT DEDUCTION  =====================\n")
# Use the DBH+height national out-of-sample relative RMSE on the small stratum as the
# allometric uncertainty input (placeholder until published coefficients are loaded).
mc <- mc_lgocv(bs, form = "dbh_h", iters = 100)
small_relrmse <- mc$rel_rmse_pct[grepl("5-9cm", mc$stratum)][1]
if (length(small_relrmse) && is.finite(small_relrmse)) {
  cat(sprintf("Allometric relative RMSE on small stratum (OOS): %.1f%%\n", small_relrmse))
  cat(sprintf("ART-TREES Eq.11 deduction: %.2f%%\n", art_trees_deduction(small_relrmse)))
  cat(sprintf("ACR IFM deduction (threshold/floor UNVERIFIED): %.2f%%\n",
              acr_ifm_deduction(small_relrmse)))
  print(credit_revenue_impact(art_trees_deduction(small_relrmse),
                              project_tonnes = 1e6, price_per_tonne = 5), row.names = FALSE)
}

cat("\nDone. See analysis/README.md for interpretation and next stages.\n")
