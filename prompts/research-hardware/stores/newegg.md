# Newegg

Apply [the shared listing contract](../listings.md). Search `site:newegg.com` with the exact part number or use
`https://www.newegg.com/p/pl?d=QUERY` with a URL-encoded query. For complete servers, start at
<https://www.newegg.com/Server-System/SubCategory/ID-386>.

Category cards expose title, model number, price and purchase status. Follow the matching item link to confirm the
seller, condition, included RAM and exact SKU. Product pages can omit a price that remains readable in the category;
use that fallback only when the selected offer matches exactly. “More options from” can refer to another seller or
configuration and is not the current card's price. Exclude accessories, barebones chassis and RAM-only listings from
complete-server results. A server with CPUs and RAM can qualify without drives when that omission is explicit.

Return the shared result with both URLs when category evidence supplies the price. Do not join an old indexed title
to a newly retrieved card's price or infer stock solely from a visible price.
