# diagnostics.R
# Distributional and variance diagnostics that justify the log form and document
# the OLS assumptions, following the author's uncertainty ebook (chapter 1).
# Base R only.

# Shapiro-Wilk normality test on a numeric vector (caps at 5000 as shapiro requires).
normality_test <- function(x) {
  x <- x[is.finite(x)]
  if (length(x) > 5000) x <- sample(x, 5000)
  st <- stats::shapiro.test(x)
  data.frame(test = "Shapiro-Wilk", n = length(x),
             W = unname(st$statistic), p_value = st$p.value,
             skew = mean((x - mean(x))^3) / sd(x)^3,
             kurtosis = mean((x - mean(x))^4) / sd(x)^4,
             stringsAsFactors = FALSE)
}

# Breusch-Pagan heteroscedasticity test (Koenker studentised form), base R.
# Regresses squared residuals on the predictor; LM = n * R^2_aux ~ chi-sq(df).
breusch_pagan <- function(model) {
  r2 <- residuals(model)^2
  X  <- model.matrix(model)
  aux <- lm(r2 ~ X - 1)
  lm_stat <- length(r2) * summary(aux)$r.squared
  df <- ncol(X) - 1
  data.frame(test = "Breusch-Pagan", LM = lm_stat, df = df,
             p_value = 1 - pchisq(lm_stat, df),
             decision = ifelse(1 - pchisq(lm_stat, df) < 0.05,
                               "reject H0: heteroscedastic", "homoscedastic"),
             stringsAsFactors = FALSE)
}

# Run the standard diagnostic block on a black-spruce table for total AGB vs DBH,
# on both natural and log scales, to demonstrate the transformation rationale.
diagnostic_block <- function(bs) {
  lin <- lm(OM_total ~ Dbh, data = bs)
  log <- lm(log(OM_total) ~ log(Dbh), data = bs)
  list(
    normality_natural = normality_test(bs$OM_total),
    normality_logresid = normality_test(residuals(log)),
    bp_natural = breusch_pagan(lin),
    bp_log     = breusch_pagan(log)
  )
}
