# 02_national_equation.R
# The Canadian national tree aboveground biomass equation form
# (Lambert et al. 2005; reparameterised in Ung et al. 2008), plus fitting.
#
# Model form, per component k in {wood, bark, branches, foliage}:
#   DBH-only  (their Table 3):  y_k = b1_k * D^b2_k
#   DBH+height(their Table 4):  y_k = b1_k * D^b2_k * H^b3_k
# Total aboveground biomass is the sum of components. In the published national
# model the components are fitted jointly by nonlinear seemingly-unrelated
# regression so they are additive and cross-component error dependence is modelled.
#
# Two coefficient sources are supported:
#   (a) PUBLISHED coefficients (authoritative). Drop the Lambert 2005 / Ung 2008
#       black-spruce parameters into coefficients/national_published.csv and load
#       them with load_coefficients(). This is what the manuscript must ultimately use.
#   (b) OPEN REPRODUCTION. fit_national_form() re-fits the same functional form to
#       the ENFOR data (the very sample the national equations were fitted on),
#       giving a fully open, runnable analogue while (a) is being sourced.

COMPONENTS <- c(wood = "OM_stem_wood", bark = "OM_stem_bark",
                branches = "OM_branches", foliage = "OM_foliage_twigs")

# ---- Prediction from a coefficient table -----------------------------------
# coefs: data frame with columns component, form ("dbh" or "dbh_h"), b1, b2, b3.
predict_component <- function(dbh, height, b1, b2, b3 = NA, form = "dbh") {
  if (form == "dbh_h") b1 * dbh^b2 * height^b3 else b1 * dbh^b2
}

predict_total <- function(dbh, height, coefs, form = "dbh") {
  cc <- coefs[coefs$form == form, ]
  total <- rep(0, length(dbh))
  parts <- list()
  for (i in seq_len(nrow(cc))) {
    p <- predict_component(dbh, height, cc$b1[i], cc$b2[i],
                           if ("b3" %in% names(cc)) cc$b3[i] else NA, form)
    parts[[cc$component[i]]] <- p
    total <- total + p
  }
  list(total = total, components = parts)
}

# ---- Fitting the national form to data (open reproduction) ------------------
# Log-log OLS per component with Baskerville/Sprugel back-transform correction
# CF = exp(sigma^2 / 2). Returns a coefficient table on the natural scale.
fit_component_loglog <- function(data, y_col, form = "dbh") {
  d <- data[data[[y_col]] > 0 & data$Dbh > 0, ]
  if (form == "dbh_h") {
    d <- d[d$Height > 0, ]
    m <- lm(log(d[[y_col]]) ~ log(d$Dbh) + log(d$Height))
    b3 <- unname(coef(m)[3])
  } else {
    m <- lm(log(d[[y_col]]) ~ log(d$Dbh))
    b3 <- NA_real_
  }
  sigma2 <- summary(m)$sigma^2
  cf <- exp(sigma2 / 2)
  b1 <- exp(unname(coef(m)[1])) * cf   # intercept back-transformed with correction
  b2 <- unname(coef(m)[2])
  data.frame(component = NA, form = form, b1 = b1, b2 = b2, b3 = b3,
             cf = cf, n = nrow(d), sigma = sqrt(sigma2), stringsAsFactors = FALSE)
}

# Fit all four components on a given training set and return a coefficient table.
fit_national_form <- function(train, form = "dbh", components = COMPONENTS) {
  rows <- lapply(names(components), function(k) {
    r <- fit_component_loglog(train, components[[k]], form)
    r$component <- k
    r
  })
  do.call(rbind, rows)
}

# Load published coefficients (authoritative path) from a tidy CSV.
load_coefficients <- function(path) {
  read.csv(path, stringsAsFactors = FALSE)
}
