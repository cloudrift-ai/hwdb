# Current GPU prices

Use live eBay search for discovery and live item pages for confirmation. This route worked in the in-app browser
on 2026-10-22 without login. Indexed web extraction remains useful for finding item URLs, but can return old prices
and stock. These are advertised purchase prices, not completed-sale valuations.

## Repeatable search

Search each GPU's exact model, VRAM and form factor separately. For example, V100 PCIe 16GB, V100 SXM2 16GB and
V100 PCIe 32GB are separate configurations. Use these search parameters:

| Parameter | Meaning in the tested search |
| --- | --- |
| `_nkw=QUERY` | URL-encoded model and configuration |
| `_sacat=27386` | Graphics/video cards category; broaden if a server module is missing |
| `LH_BIN=1` | Fixed purchase offers |
| `LH_ItemCondition=1000` | New |
| `LH_ItemCondition=3000` | Used |
| `_sop=15` | Price plus shipping, lowest first |

Examples: [new RTX 5060 Ti 16GB](https://www.ebay.com/sch/i.html?_nkw=rtx+5060+ti+16gb&_sacat=27386&LH_BIN=1&LH_ItemCondition=1000&_sop=15)
and [used RTX 3090 24GB](https://www.ebay.com/sch/i.html?_nkw=rtx+3090+24gb&_sacat=27386&LH_BIN=1&LH_ItemCondition=3000&_sop=15).
Confirm the actual selected filters and sort in the rendered page; URL parameters alone do not prove they applied.
Open-box and refurbished offers require separate searches and explicit labels. Under HWDB's two-condition schema,
record refurbished offers as used with their exact grade in the price basis; do not silently classify open box as new.

Open each candidate's actual item link, then read the primary item region and any stock banner above it:

1. Verify GPU, VRAM, PCIe/SXM generation, quantity and included adapter/cooling. Exclude accessories, empty boxes,
   waterblocks alone, broken/untested cards and modified configurations that do not match the intended model.
2. Read fixed price, USD currency, actual seller and condition. Ignore installment amounts, old prices, warranty
   add-ons, recommendations and bulk discounts. Sponsored cards are discovery leads, not price-order guarantees.
3. Reject explicit out-of-stock/ended banners, even if the search card still says Buy It Now. Require an enabled
   primary Buy It Now control with no conflicting warning, or explicit available quantity plus a purchase control.
   Watcher counts, historical sold counts and generic cart navigation do not establish availability.
4. Verify delivery to the intended country. US delivery is the default for comparable USD offers; keep pickup-only
   and non-deliverable offers separate. Record the destination context shown by the page without changing the user's
   saved address. Shipping is destination-dependent and must not be inferred from search sorting.
5. Record item price and shipping separately, plus pre-tax delivered total when shipping is known. Preserve HWDB's
   item-price ranking convention unless the user requests a change. Unknown shipping means unknown delivered total,
   not free delivery. Record seller feedback and visible condition defects as evidence, not as a guarantee.
6. Retain the canonical item URL, seller, observation time, available quantity when shown, and evidence of current
   purchase controls. Do not import an indexed price as a current observation if live confirmation fails.

For a model-level estimate, inspect several matching offers from distinct sellers. Report the lowest verified
deliverable offer and, when at least three sellers qualify, their median asking price with the sample count and
observed range. Disclose how offers were sampled; the median of a cheapest-offer sample is not a market-wide median.
Deduplicate item IDs and variants. Retain the actual selected listing as the source behind any HWDB price row.

## Browser checks

These observations demonstrate the method, not a cheapest-price survey or purchase recommendation.

| Exact listing | Condition | Item price | Shipping shown | Outcome |
| --- | --- | ---: | ---: | --- |
| [PNY RTX 5060 Ti 16GB](https://www.ebay.com/itm/840015736032), seller storefront pcrefurbplus / account loheer_0 | New | $749.99 | $7.58 | Two available, active Buy It Now; pre-tax delivered total $757.57 |
| [ASUS ROG Strix RTX 3090 24GB](https://www.ebay.com/itm/860067900179), empty_bubble | Used | $1,449.00 | $34.99 | Active Buy It Now, US delivery; total $1,483.99; seller had one feedback entry |
| [MSI VANGUARD RTX 5060 Ti 16GB](https://www.ebay.com/itm/800020842561), Newegg | New | $617.99 | — | Reject: item page says out of stock despite appearing in filtered search |
| [MSI VENTUS RTX 3090 24GB](https://www.ebay.com/itm/800742611466), exp-912983 | Used | $1,199.00 | Pickup only | Exclude from US-deliverable comparison: pickup in Wilrijk, Belgium; seller had zero feedback |

The browser showed a US shipping destination. Shipping totals above apply only to that displayed context and can
change. Stock and prices must be checked again on the next research run.

## Automation route

For a credentialed integration, eBay's [Browse API](https://developer.ebay.com/api-docs/buy/api-browse.html) provides
listing search and item refresh. Its [filters](https://developer.ebay.com/api-docs/buy/static/ref-buy-browse-filters.html)
support condition IDs, fixed-price offers and delivery country. Search, then retrieve the exact item before accepting
price and availability. Keep currency, seller, condition, delivery and variant checks equivalent to the browser flow.

This API route was researched, not executed. Production access and credentials must be established under eBay's
[Buy API requirements](https://developer.ebay.com/api-docs/buy/static/buy-requirements.html) before building around it.
The tested browser route is usable now and does not depend on obtaining API access.

## Database refresh

The live-browser refresh checked all 24 existing discrete GPU candidates: ten New and fourteen Used. Each accepted
observation has an exact item URL, one-unit USD asking price, listing condition, available quantity or active purchase
control, and US delivery. CSV notes retain the priced board, seller, visible feedback count, shipping and observation
window. Low-feedback sellers are identified explicitly. These are selected asking offers, not market-wide minima.

Current observations for workbook GPUs live in [workbook overrides](../data/workbook_overrides.csv), so a price-only
refresh preserves the baseline workbook. Supplemental GPU observations live in [options](../data/options.csv).
The generator applies nonempty override price fields before ranking. Shipping remains outside ranking prices.

Replaced [V100 PCIe 16GB offer](https://www.ebay.com/itm/206480304588) because its live page reported a completed
sale, and [V100 PCIe 32GB offer](https://www.ebay.com/itm/204348040061) because it reported out of stock. Rejected
out-of-stock Newegg listings for [5070 Ti](https://www.ebay.com/itm/306939698028) and
[5090](https://www.ebay.com/itm/800402829841), and several cheaper pickup-only offers. Retained all V100 form factors
with verified replacement or refreshed offers, including the separate SXM2 adapter/cooler bundle.
