# Retrieve hardware listings

Inputs: a hardware query, optional HWDB category and condition, optional store selection, and a candidate limit
(default ten). Cover both new and used when no condition is specified. Use the category definitions and bandwidth
conventions in [README](../../README.md). Select stores from [the catalog](../../docs/stores.md) and apply their
linked prompts in addition to this contract.

## Evidence and eligibility

- Discover with search, then open the exact retailer listing. Record the seller, SKU/variant, condition, one-unit
  purchase price, explicit currency and stock evidence. A marketplace is not the seller.
- Prefer a live browser or authenticated current-inventory API for current prices. If indexed extraction supplies
  the lead, confirm it through the live item page. Read stock warnings above the product heading as well as purchase
  controls; search results can retain unavailable products.
- Reject out-of-stock, sold, ended, unavailable and discontinued listings. Also reject unknown stock for a new
  shopping observation, auctions without a fixed purchase price, quote-only pages and contradictory configurations.
  A generic Add to Cart button does not override an explicit stock warning.
- Use the current purchase price, not a crossed-out price, financing payment, trade-in, rebate, membership price,
  bulk tier or unselected variant's minimum. A kit price buys the complete kit; do not divide the price while keeping
  the full kit's capacity. Record shipping and tax treatment separately in notes when known.
- Verify delivery eligibility for the requested market (default US for USD comparisons). Keep pickup-only offers
  separate. Record item price, shipping and pre-tax delivered total independently when known; unknown shipping is
  not zero. Rankings continue to use item prices unless their methodology is explicitly changed.
- Use USD offers for database-ready candidates. Report other currencies separately unless conversion was requested;
  a conversion requires a dated exchange-rate source. Never infer that an unqualified dollar sign means USD.
- Search snippets and archived/indexed pages are discovery evidence, not proof of live stock. Tools can return
  cached pages: retain their age when exposed and mark freshness unverified if a current retrieval cannot confirm
  the offer. Do not advance a price observation date to today's date just because an old snapshot was opened today.
- Obtain missing hardware specifications from manufacturer documentation and cite it separately. Do not infer a
  server's bandwidth from its maximum supported RAM or DIMM rating alone; installed channels and operating speed
  must support the calculation. Leave unknown metrics null. Keep module, adapter bundle and complete system separate.
- Confirm exact SKU suffixes and included quantity in item specifics or seller configuration details when titles
  are generic. A query match alone is insufficient. Keep unknown server bandwidth empty even when total RAM is known.
- Prefer exact item pages. A category card is acceptable only when its price, seller, condition and availability
  unambiguously identify the same SKU/configuration; retain both the category and item URLs as evidence.
- If a page is blocked or omits price/stock, try a public category page or a linked exact variant once. A normal
  browser may resolve client-rendered fields when available. If evidence still fails, report the limitation and
  move to another store rather than guessing. Do not add items to a cart or contact sellers to establish a price.

## Result

Return a JSON object with `candidates`, `rejected` and `limitations` arrays. Each candidate has `option` and `evidence`.
`option` uses the CSV field names below; numeric values are numbers, unknown metrics are null, and all other fields
are strings. Source URLs are space-separated. A candidate must have a verified price and at least one relevant
metric; CPU candidates require bandwidth. Rejected entries need URL and reason; limitations describe incomplete
coverage, access or freshness.

```json
{
  "option": {
    "category": "gpu",
    "condition": "used",
    "vendor": "NVIDIA",
    "model": "Tesla V100 SXM2 16GB",
    "memory_gb": 16,
    "bandwidth_gbs": 900,
    "price_usd": 173.41,
    "price_date": "2026-10-22",
    "price_basis": "Used seller asking price; module only",
    "availability": "More than 10 available",
    "source": "https://www.ebay.com/itm/820137427098",
    "notes": "Example shape only; reverify the offer. SXM2 carrier and cooling excluded."
  },
  "evidence": {
    "seller": "seller name from listing",
    "sku_or_variant": "V100-SXM2-16GB",
    "retrieved_at": "ISO UTC timestamp",
    "price_url": "https://www.ebay.com/itm/820137427098",
    "stock_url": "https://www.ebay.com/itm/820137427098",
    "spec_urls": [],
    "price_and_stock_observation": "Concise paraphrase of fields actually retrieved",
    "delivery": "Destination context and delivery eligibility; identify pickup-only offers",
    "shipping_usd": null,
    "delivered_total_usd": null,
    "seller_feedback": "Visible feedback count/rating, if shown",
    "freshness": "live confirmation or explicit snapshot limitation"
  }
}
```

The example is one candidate, not a current offer or permission to reuse its values. Apply the same evidence standard
to every candidate. Research alone does not authorize writing source tables; when an update was requested, pass
accepted options to [the refresh contract](../refresh-readme.md).
