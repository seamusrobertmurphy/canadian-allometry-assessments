# 03b_cross_validation.R
# Monte Carlo leave-group-out cross-validation (LGOCV), DBH-class stratified,
# matching the regime in the author's uncertainty ebook (chapter 1, 100 iterations,
# 80/20 split). Replaces the plain 5-fold CV in 03_fit_and_bias.R for the
# out-of-sample uncertainty estimates the paper reports.
#
# Why stratified and Monte Carlo: a single split at small n is unstable, and an
# unstratified split under-samples the large-tree tail that carries most biomass.

.dbh_class <- function(dbh) cut(dbh, breaks = c(0,5,9,15,25,100),
                                labels = c("0-5","5-9","9-15","15-25",">25"),
                                include.lowest = TRUE)

# One stratified 80/20 draw of row indices.
.stratified_train_idx <- function(dbh, p = 0.8) {
  cls <- .dbh_class(dbh)
  idx <- integer(0)
  for (lv in levels(cls)) {
    rows <- which(cls == lv)
    if (length(rows) == 0) next
    idx <- c(idx, sample(rows, max(1, floor(length(rows) * p))))
  }
  sort(idx)
}

# Monte Carlo LGOCV for the national-form model on a data set, returning pooled
# out-of-sample metrics overall and by size stratum.
mc_lgocv <- function(data, form = "dbh", iters = 100, p = 0.8, seed = 8787) {
  set.seed(seed)
  obs <- pred <- strat <- vector("list", iters)
  for (i in seq_len(iters)) {
    tr_idx <- .stratified_train_idx(data$Dbh, p)
    tr <- data[tr_idx, ]; te <- data[-tr_idx, ]
    if (nrow(te) < 5) next
    coefs <- fit_national_form(tr, form)
    pr <- predict_total(te$Dbh, te$Height, coefs, form)$total
    obs[[i]]   <- te$OM_total
    pred[[i]]  <- pr
    strat[[i]] <- te$stratum
  }
  o <- unlist(obs); pr <- unlist(pred); st <- unlist(strat)
  overall <- eval_metrics(o, pr, "MC-LGOCV national -> all (pooled OOS)")
  by_str <- do.call(rbind, lapply(sort(unique(st)), function(s)
    eval_metrics(o[st == s], pr[st == s], paste0("MC-LGOCV national -> ", s))))
  rbind(overall, by_str)
}
