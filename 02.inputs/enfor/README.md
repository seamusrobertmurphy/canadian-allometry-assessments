# ENFOR — Energy from the Forest Biomass destructive-biomass sample

The **calibration** side of the analysis. This is the pan-Canadian destructive sample that
Canada's national biomass equations were actually fitted on, which makes the tamarack arm an
honest in-sample adequacy check: if the coefficient cannot recover the trees it was built
from, nothing downstream is trustworthy. It does — relative bias −0.6 percent — and that
internal control is what licenses the western-larch comparison.

Tamarack (*Larix laricina*) is the **only larch in the national species set**. It is
therefore both the in-sample control and the nearest-congener substitute a practitioner
might reach for when estimating western larch.

## Source and licence

- **Title:** Biomass of trees sampled across Canada as part of the Energy from the Forest Biomass (ENFOR) Program
- **Publisher:** Natural Resources Canada, Canadian Forest Service
- **Portal:** https://open.canada.ca/data/en/dataset/fbad665e-8ac9-4635-9f84-e4fd53a6253c
- **DOI:** https://doi.org/10.23687/fbad665e-8ac9-4635-9f84-e4fd53a6253c
- **Licence:** Open Government Licence – Canada (reuse permitted with attribution)
- **Sampling:** 1978–1983; record published 2017
- **Cite as:** Ung, C.-H., Lambert, M.C., Raulier, F., Guo, J., Bernier, P.Y. (2017). Biomass of trees sampled across Canada as part of the Energy from the Forest Biomass (ENFOR) Program.

## How to download

Both files download directly from the Open Canada portal record above — no request or
account needed. French-language equivalents exist at the same record and were not pulled.

## Files

| File | Rows | Size | In git |
|---|---:|---:|:---:|
| `EnforCanadaBiomassFinalData_v2007-ENG.csv` | 9,454 trees | 1 MB | yes |
| `EnforCanadaBiomassMetadata_v2010-ENG.doc` | — | 3 MB | yes |

**Read the metadata document before analysis.** It defines the oven-dry-mass compartments
and the compilation corrections.

## Columns the analysis reads

One row per destructively sampled tree. Oven-dry mass in kilograms by compartment.

| Column | Meaning |
|---|---|
| `Species_E` | English species name — matched on `tamarack` |
| `Dbh` | diameter at breast height, cm |
| `Height` | total height, m |
| `OM_stem_bark` | stem bark oven-dry mass, kg — **the focal component** |
| `OM_stem_wood` | stem wood oven-dry mass, kg |
| `OM_total` | total aboveground oven-dry mass, kg |

Also present and unused here: `OM_stem`, `OM_crown`, `OM_foliage_twigs`, `OM_branches`,
`Province`, `Year`, `Location`, `Plot`, `Tree`, `Lat`, `Long`.

## The tamarack subset

Filtering to tamarack gives **575 records**; requiring a parseable DBH and a non-missing
stem-bark mass leaves **n = 439**, spanning **1.8 to 44.5 cm DBH**, stem bark complete for
every retained record.

That matters for the argument: the national fit drew 575 tamarack trees from this archive,
and the retained 439 span its full reported extent (1.8–44.5 cm DBH, 2.2–30.5 m height, per
Lambert et al. 2005). The coefficient is therefore tested across the whole interval it was
fitted on, not a favourable slice of it.

## Gotchas

- **Encoding is Latin-1**, not UTF-8. Read with `fileEncoding = "latin1"` or the species
  names arrive mangled.
- **Species labels carry variants.** A loose substring match returns more rows than an exact
  label match. The analysis matches case-insensitively on `tamarack`.
- **Province labels are not normalised** — lowercase `on`/`qc` appear beside `ON`/`QC`. Fold
  before any by-province summary. Not used in the current analysis.
- **Coordinates are coarse**, whole-degree in places. Do not treat `Lat`/`Long` as plot-precise.
- **No site, drainage, ecosite or wetland attribute exists.** There is no column marking a
  tree's site type. This ruled out an earlier peatland-stratified design; see
  `README-manifest.md` for that assessment, which describes a **superseded** scope.
- **Component definitions differ from LegacyTreeData** in detail. Reconciled as far as the
  metadata allow; the residual difference is carried in the paper as a limitation.

## Related

`README-manifest.md` in this folder is the original acquisition profile from 2026-07-15. It
is retained for provenance but was written under the earlier **black-spruce peatland**
framing, which the manuscript no longer uses. Trust this file for the current scope.
