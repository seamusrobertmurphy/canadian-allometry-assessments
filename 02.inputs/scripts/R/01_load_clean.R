# 01_load_clean.R
# Load and clean the open ENFOR destructive-biomass dataset.
# Source: NRCan CFS, https://doi.org/10.23687/fbad665e-8ac9-4635-9f84-e4fd53a6253c
# Open Government Licence - Canada. No confidential project data are used.
#
# Units: oven-dry mass in kilograms per tree, by compartment. DBH in cm, height in m.
# Confirm units and compartment definitions against the official metadata DOC before publishing.

load_enfor <- function(path) {
  df <- read.csv(path, stringsAsFactors = FALSE, check.names = TRUE)

  # --- Province labels are not normalised (lowercase on/qc appear). Fold to upper. ---
  df$Province <- toupper(trimws(df$Province))

  # --- Species: trim whitespace and collapse case-variant labels. ---
  df$Species_E <- trimws(df$Species_E)

  # --- Year holds single years and two-season campaign ranges (e.g. "1982-1983"),
  #     plus missing values. Parse a numeric start year; keep the raw label. ---
  df$Year_raw   <- df$Year
  df$Year_start <- suppressWarnings(as.integer(substr(gsub("[^0-9-]", "", df$Year), 1, 4)))

  # --- Coerce measurement columns to numeric. ---
  num_cols <- c("Dbh", "Height", "OM_stem", "OM_stem_wood", "OM_stem_bark",
                "OM_crown", "OM_foliage_twigs", "OM_branches", "OM_total",
                "Lat", "Long")
  for (c in num_cols) if (c %in% names(df)) df[[c]] <- suppressWarnings(as.numeric(df[[c]]))

  # --- Coordinate precision flag: whole-degree coords are too coarse for a peatland
  #     overlay. Count decimal places on the raw strings before numeric coercion. ---
  dp <- function(x) {
    x <- as.character(x)
    ifelse(grepl("\\.", x), nchar(sub("^[^.]*\\.", "", x)), 0L)
  }
  raw <- read.csv(path, stringsAsFactors = FALSE, colClasses = "character")
  df$coord_dp <- pmin(dp(raw$Lat), dp(raw$Long))
  df$coord_usable_for_overlay <- df$coord_dp >= 2  # ~1 km or better

  df
}

# Filter to a clean, analysis-ready black spruce table.
black_spruce <- function(df, require_height = TRUE) {
  bs <- df[grepl("black spruce", df$Species_E, ignore.case = TRUE), ]
  bs <- bs[!is.na(bs$Dbh) & bs$Dbh > 0 & !is.na(bs$OM_total) & bs$OM_total > 0, ]
  if (require_height) bs <- bs[!is.na(bs$Height) & bs$Height > 0, ]
  bs
}

# Size strata used as an open, size-based proxy for peatland form.
# NOTE: size is not drainage. The true peatland stratum requires the spatial
# overlay (see 04_peatland_overlay.R, planned) or the Wagers et al. 2024 contrast set.
add_size_stratum <- function(bs, small_thresh = 9, verysmall_thresh = 5) {
  bs$stratum <- ifelse(bs$Dbh < verysmall_thresh, "very_small(<5cm)",
                ifelse(bs$Dbh < small_thresh,    "small(5-9cm)",
                                                 "larger(>=9cm)"))
  bs$is_small <- bs$Dbh < small_thresh
  bs
}
