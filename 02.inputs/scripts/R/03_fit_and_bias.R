# 03_fit_and_bias.R
# Headline analysis: does the national-form fit, calibrated on the whole
# black-spruce population, carry a systematic bias on the small-tree stratum
# (the open, size-based proxy for peatland form), and does a stratum-specific
# fit remove it? This reproduces the Wagers et al. (2024) logic on open ENFOR data.
#
# IMPORTANT framing: ENFOR has no drainage/peatland attribute, so this is a
# size-class demonstration of the pipeline, not yet a peatland-drainage claim.
# The peatland claim needs the spatial overlay (04, planned) or the Wagers contrast set.

# k-fold out-of-sample predictions of TOTAL AGB for a stratum-specific model,
# so the stratum-specific fit is not evaluated on its own training rows.
cv_predict_total <- function(data, form = "dbh", k = 5, seed = 42) {
  set.seed(seed)
  fold <- sample(rep_len(seq_len(k), nrow(data)))
  pred <- rep(NA_real_, nrow(data))
  for (f in seq_len(k)) {
    tr <- data[fold != f, ]; te <- data[fold == f, ]
    coefs <- fit_national_form(tr, form)
    pr <- predict_total(te$Dbh, te$Height, coefs, form)
    pred[fold == f] <- pr$total
  }
  pred
}

run_bias_analysis <- function(bs, form = "dbh") {
  # 1. National analogue: fit the national form on the full black-spruce population.
  nat_coefs <- fit_national_form(bs, form)
  nat_pred  <- predict_total(bs$Dbh, bs$Height, nat_coefs, form)$total
  bs$pred_national <- nat_pred

  # 2. National-model bias by size stratum.
  strata <- split(bs, bs$stratum)
  nat_by_stratum <- do.call(rbind, lapply(names(strata), function(s) {
    d <- strata[[s]]
    eval_metrics(d$OM_total, d$pred_national, label = paste0("national -> ", s))
  }))
  nat_overall <- eval_metrics(bs$OM_total, bs$pred_national, "national -> all")

  # 3. Stratum-specific model on the small-tree subset, out-of-sample via CV.
  small <- bs[bs$is_small, ]
  strat_metrics <- NULL
  if (nrow(small) >= 50) {
    small_pred <- cv_predict_total(small, form, k = 5)
    strat_metrics <- eval_metrics(small$OM_total, small_pred,
                                  "stratum-specific(CV) -> small(<9cm)")
  }

  list(
    form            = form,
    national_coefs  = nat_coefs,
    national_overall = nat_overall,
    national_by_stratum = nat_by_stratum,
    stratum_specific_small = strat_metrics
  )
}
