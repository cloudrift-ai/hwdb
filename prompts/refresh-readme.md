# Refresh HWDB data and README

Use the requested scope: rebuild only, change presentation, or update specified hardware observations.
Read `README.md` and the current source rows before editing. For price research, apply
[the listing contract](research-hardware/listings.md) before accepting an observation.

1. For existing workbook hardware, record price-only refreshes in `data/workbook_overrides.csv`; nonempty
   `price_usd`, `price_date`, `price_basis`, `availability` and `source` supersede workbook values, and `notes` append
   listing details. Retain its category, condition and memory fields. Update the workbook itself when requested,
   or add supplemental hardware rows to `data/options.csv`.
   Do not duplicate an existing `(category, condition, vendor, model)` across the workbook and CSV.
   Distinct priced configurations need distinct, explicit model names. An expired offer may be replaced by a
   verified offer for the same configuration; preserve the new seller, source and observation date.
2. Retain the CSV header and source provenance fields. Convert JSON nulls to empty CSV cells. Put price and spec URLs
   in `source`, separated by spaces, and explain calculations and excluded components in `notes`.
   A page retrieval date is not a new price date when the only evidence is an older indexed snapshot.
3. Register eligible workbook `Platform` rows in `data/workbook_overrides.csv` with the correct category, condition
   and capacity. Use installed RAM for CPU systems and GPU-accessible memory for GPU systems.
   Preserve unrelated worksheets, workbook formatting and files in `outputs/`.
4. Change introduction or methodology prose in `docs/README.template.md`. Keep its single `{{RANKINGS}}` marker.
   Keep one global README generation timestamp and the flat New/Used category sections with at most ten rows per
   metric. Do not add per-row price dates or price bases to the README.
5. Run `make readme` and `make check`. Run `make test` when changing the generator or data parsing/classification.
   Inspect the generated sections for unexpected category changes, missing variants and stock exclusions.

For a complete non-GPU price refresh, update `data/price_refresh.json` with an outcome for every original requested
row and any added candidate. Keep identity, observation window, selected item/seller/price/shipping or search URL and
rejection reason. Mark unmatched rows `Unavailable: no verified current eBay offer` to exclude historical prices;
do not advance their price dates or claim the product is globally out of stock. Record added condition counterparts
as separate candidates with the same metric evidence and explicit priced configuration.

Report what changed, verification results and remaining coverage gaps. Do not claim a generated timestamp means
every price was reverified. Finding fewer than ten eligible options is a valid outcome.
