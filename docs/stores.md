# Stores and price retrieval

Retrieval checks: **2026-10-22**, using public web search and page extraction without login or checkout.
These checks establish that fields were readable in returned pages; they are not an uptime guarantee, a seller
endorsement or proof that cached inventory remains available. Recheck exact offers on every research run.

Use the [shared listing contract](../prompts/research-hardware/listings.md) plus a store prompt below. The first four
are preferred starting points because their sampled pages exposed prices and purchase/stock status. The last two
are secondary sources with readable fields but no eligible offer in the sampled pages.

| Store | Useful HWDB coverage | Retrieval route | Observed result / limitation | Prompt |
| --- | --- | --- | --- | --- |
| Newegg | New/used GPU, CPU, DDR, GPU/CPU systems | Search/category cards, then exact item | Matching SKU, USD price and Add to cart readable; marketplace seller and configuration must match | [Newegg](../prompts/research-hardware/stores/newegg.md) |
| eBay marketplace | New/used GPU, CPU, DDR, systems and embedded | Live browser search → exact `/itm/` page; indexed/category fallback | New and Used searches worked live; item pages reveal stale stock and pickup-only offers hidden by search cards | [eBay](../prompts/research-hardware/stores/ebay.md) |
| Adafruit | New embedded boards/kits | Exact `/product/ID` page | Selected RAM variant, price and In stock readable; sibling variants differ | [Adafruit](../prompts/research-hardware/stores/adafruit.md) |
| Seeed Studio | New embedded systems/modules, GPU systems | Exact SKU product page | Main price and In stock readable; quantity tiers and variant controls need care | [Seeed](../prompts/research-hardware/stores/seeed.md) |
| The Server Store | Preconfigured CPU/GPU systems, mainly used/refurbished | Product index → exact configured product | Total price, RAM and explicit stock readable; both sampled servers were out of stock | [The Server Store](../prompts/research-hardware/stores/server-store.md) |
| Mac-Ave | Used unified-memory GPU systems | Shop Used → exact product | Sale price, chip, RAM and condition readable; sampled Mac was discontinued/out of stock | [Mac-Ave](../prompts/research-hardware/stores/mac-ave.md) |

## Reproducible checks

For current GPU offers, use the [live-browser pricing procedure](gpu-prices.md), tested for both New and Used.
It includes successful item checks and examples rejected for stock or delivery. Search-card prices alone are not
eligible: one card remained in New results after its item page reported out of stock.

The same live workflow now covers CPU, DDR, GPU-system, CPU-system and embedded prices. The
[refresh audit](../data/price_refresh.json) accounts for all 72 original non-GPU rows, including 20 excluded for lack
of a verified current matching offer and two additional used embedded candidates. Exact item specifics prevented
accepting a white Corsair DDR5 kit for the black kit's MPN. Complete-server checks distinguish installed RAM from
configuration choices; search Error Pages are recorded as access failures, not evidence that stock is zero.

The subsequent [top-ten expansion](../data/top_ten_expansion.json) verifies 52 selected offers: 49 additional
configurations and three replacements of existing records. It fills all 22 metric tables using eBay plus Newegg
for new/refurbished servers and processors/memory, and Adafruit for embedded boards. Newegg item pages expose the
selected New/Used offer, marketplace seller and US delivery. Preserve `?Item=` when it selects that seller.
An alternate used price can precede the selected new price; Back Order is ineligible. Server bandwidth checks
combine installed DIMM counts with CPU/OEM operating rates and documented population rules, with assumptions
retained in notes. See the updated store prompts for the 4400 MT/s HPE and 1866 MT/s Xeon downclock examples.

These are extraction examples, not rows to import without a fresh eligibility check. Amounts describe the returned
snapshots and exclude any separately shown shipping or tax.

- **Newegg:** [server category](https://www.newegg.com/Server-System/SubCategory/ID-386) exposed HPE P93189-005,
  64GB (2×32GB), $8,493 and Add to cart. Follow the matching item to verify seller and selected offer.
- **eBay:** [V100 SXM2 16GB item](https://www.ebay.com/itm/820137427098) exposed US $173.41, Used, more than ten
  available, an active purchase control and US delivery in the live browser refresh. Earlier indexed extraction
  showed $153.86 from an older snapshot; use the live price. The [GPU price refresh](gpu-prices.md#database-refresh)
  records the coverage and source-table locations.
- **Adafruit:** [Raspberry Pi 5 8GB, product 5813](https://www.adafruit.com/product/5813) exposed $200, In stock and a
  two-unit limit. The sibling 2GB variant was out of stock; its status must not be applied to the 8GB product.
- **Seeed:** [reComputer J3011](https://www.seeedstudio.com/reComputer-J3011-p-5590.html) exposed SKU 110110147,
  Orin Nano 8GB, $749 and In stock. The separate 10+ tier was $741, which is not the one-unit price.
- **The Server Store:** [R630 192GB configuration](https://www.theserverstore.com/dell-poweredge-r630-36-core-virtualization-server-192gb-3x-800gb-ssd-h730p.html)
  exposed $699 and Out of Stock, quantity zero. The URL says 800GB SSD while the title says 960GB; do not infer
  delivered storage from the slug. [R730xd 64GB configuration](https://www.theserverstore.com/dell-poweredge-r730xd-20-core-64gb-truenas-server-72tb-24tb.html)
  likewise exposed $999 and zero stock. Both are rejection checks, not eligible listings.
- **Mac-Ave:** [M1 Ultra Mac Studio, 64GB/1TB](https://www.mac-ave.com/product/used-mac-studio-m1-ultra-64gb-1tb-ssd/)
  exposed a $1,999 sale price and Discontinued / Out Of Stock. Reject it.

## Sources that need another route

- [ARACE Milk-V Jupiter NX](https://arace.tech/products/milk-v-jupiter-nx?variant=43904659718324) could not be opened
  by the page-extraction tool in this check. Keep it a lead until a browser or another public route verifies the
  exact RAM variant, price, currency and availability.
- [Pimoroni Raspberry Pi 5](https://shop.pimoroni.com/products/raspberry-pi-5) was readable, but the tested extraction
  did not establish a selected variant's USD price and stock. Its location controls affect currency and taxes.
  Verify a US-region variant before adding a USD offer; do not treat the store as a confirmed USD extraction source.
- Manufacturer launch articles and specification sheets establish MSRP history or specifications, not current
  stocked retail offers. Reddit seller posts are secondary leads, not store inventory; check sold/completed status
  and freshness before considering them, and do not contact sellers as part of price retrieval.

To add a store, test an exact listing for identity, configuration, one-unit price, currency, condition and stock.
Record the URL, retrieval date and failures here, then add a short store prompt that extends the shared contract.
Classify a store as a preferred starting point only after a sampled page exposes an eligible purchase offer.
