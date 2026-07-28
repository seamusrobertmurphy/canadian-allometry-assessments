# metrics.R
# Fit and bias metrics for biomass equation evaluation.
# Base R only, no external dependencies.

# Relative bias (%), signed. Positive means prediction over-estimates observation.
rel_bias <- function(observed, predicted) {
  stopifnot(length(observed) == length(predicted))
  100 * sum(predicted - observed) / sum(observed)
}

# Relative RMSE (%), scaled by the mean of observations.
rel_rmse <- function(observed, predicted) {
  stopifnot(length(observed) == length(predicted))
  rmse <- sqrt(mean((predicted - observed)^2))
  100 * rmse / mean(observed)
}

# Mean absolute error (natural units).
mae <- function(observed, predicted) mean(abs(predicted - observed))

# Pseudo R-squared on the natural scale (1 - SSE/SST).
r2_nat <- function(observed, predicted) {
  sse <- sum((observed - predicted)^2)
  sst <- sum((observed - mean(observed))^2)
  1 - sse / sst
}

# Convenience: all metrics as a one-row data frame.
eval_metrics <- function(observed, predicted, label = NA_character_) {
  data.frame(
    stratum      = label,
    n            = length(observed),
    mean_obs     = mean(observed),
    rel_bias_pct = rel_bias(observed, predicted),
    rel_rmse_pct = rel_rmse(observed, predicted),
    r2           = r2_nat(observed, predicted),
    stringsAsFactors = FALSE
  )
}
