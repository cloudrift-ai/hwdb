# Newegg

Apply [the shared listing contract](../listings.md). Search `site:newegg.com` with the exact part number or use
`https://www.newegg.com/p/pl?d=QUERY` with a URL-encoded query. For complete servers, start at
<https://www.newegg.com/Server-System/SubCategory/ID-386>.

Category cards expose title, model number, price and purchase status. Follow the matching item link to confirm the
seller, condition, included RAM and exact SKU. Product pages can omit a price that remains readable in the category;
use that fallback only when the selected offer matches exactly. “More options from” can refer to another seller or
configuration and is not the current card's price. Exclude accessories, barebones chassis and RAM-only listings from
complete-server results. A server with CPUs and RAM can qualify without drives when that omission is explicit.

On item pages, read the selected Buy New/Buy Used radio control and its associated price. An unselected used offer
can appear before the selected new price: the tested 9950X page displayed $498 used before the selected $539 new.
Keep the marketplace `?Item=...` parameter when it selects the verified seller; the same product URL can otherwise
open a different offer. Confirm the seller and shipping destination on the selected page. Exclude Back Order as
well as Out of Stock; Add to cart must be active for the selected offer.

For fixed server configurations, the specification bullets often state installed RAM as `64GB (4x16GB)` and its
DDR transfer rate. Record CPU SKU/count, DIMM count, capacity, drives and exact condition (including Refurbished).
Use CPU and OEM platform documentation to establish the operating rate: DIMM labels alone are insufficient.
Tested examples include HPE MicroServer/DL20 Gen11 running 4800-rated DIMMs at 4400 MT/s, and E5-2640 v3 limiting
2133-rated DIMMs to 1866 MT/s. Count independent populated channels under the documented OEM population rule,
state that assumption explicitly, and never multiply by empty slots or supported maximum channels. Keep bandwidth
unknown when DIMM count, speed or population cannot support a configuration-specific theoretical calculation.

The 2026-10-22 expansion verified new HPE servers and refurbished Dell/Supermicro offers from Newegg, MKTLLC,
TekBoost, Best IT Hub and AMURAS NY. These are selected asking offers, not endorsements or market estimates.

Return the shared result with both URLs when category evidence supplies the price. Do not join an old indexed title
to a newly retrieved card's price or infer stock solely from a visible price.
