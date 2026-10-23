# eBay

Apply [the shared listing contract](../listings.md). For current GPU prices, follow the tested
[GPU pricing procedure](../../../docs/gpu-prices.md). Prefer live browser search with separate New/Used filters,
fixed-price offers and price-plus-shipping sorting. Confirm the rendered filters, then open actual item pages.
Search `site:ebay.com/itm/` plus the hardware, form factor and capacity when live search is unavailable; indexed
results only discover candidates and cannot establish current price or stock. If search pages fail, try a category:
<https://www.ebay.com/b/NVIDIA-NVIDIA-Computer-Graphics-Cards-NVIDIA-Tesla-V100/27386/bn_7116863209>.

Open the exact item and read the primary purchase price, currency, condition, seller and remaining quantity.
Check stock banners above the item heading: the tested New search included a $617.99 offer whose item page explicitly
said out of stock. Require an active primary purchase control with no contrary warning; a search card is insufficient.
“Or Best Offer” does not invalidate the advertised fixed asking price. “Sold” counts can coexist with available
quantity: distinguish sales history from an ended listing. Record shipping separately; nearby free-shipping banners
can conflict with destination-specific shipping charges. A site's regional currency conversion is not the seller's
USD asking price.

Check PCIe versus SXM2/SXM3, memory size, quantity, module-only versus adapter/cooler bundle, and working versus
parts-only condition. Exclude broken/untested parts from working-hardware candidates. Prefer canonical `/itm/ID`
source URLs. A linked URL with parameters can be retried when its canonical form fails; never treat a search
snippet's price as confirmation. Return the shared result, naming the actual seller.
Do not infer that a native PCIe card is an SXM adapter from a search title alone, or the reverse. Search exclusions
can help remove accessories, but eBay can append loosely related results after exact matches; verify every item.
Record available quantity rather than historical sold counts in the availability field. Put sales history in notes
if needed: the README's conservative unavailable filter excludes entries containing the standalone word "sold".

Read seller condition notes even when the structured condition is Used. A tested Pi 5 16GB offer disclosed a
broken fan connector and was rejected in favor of a working board. For DDR, compare module count, per-module
capacity and total capacity: a generic 16GB title conflicted with an item-specific count of 24 modules. Reject
unresolved contradictions and choose a listing that explicitly states the quantity being priced. Box-only Mac
listings can match every chip/RAM search term; establish that the computer itself is included.

Check delivery eligibility separately from currency. The tested Used search included a USD-priced card available
only for pickup in Belgium. Keep pickup-only offers outside the default US-deliverable comparison. Record item price,
shipping, delivered total when known, seller feedback and defects in evidence/notes. Do not replace HWDB's item price
with a shipping-inclusive total without an explicit request. New, open-box, refurbished and used are distinct listing
conditions; retain the exact grade even where HWDB groups refurbished offers under used.

For model estimates, compare multiple exact matches from distinct sellers and report the observed sample size,
lowest verified offer and sample median when at least three sellers qualify. A single offer establishes an asking
price, not a representative market price. Recheck the selected listing before updating source tables.

For CPUs, distinguish production SKUs from ES/QS samples and OEM/vendor-locked variants, and reject motherboard/CPU
bundles when pricing a processor alone. For DDR, verify the exact MPN suffix, total capacity and included DIMM count:
a single DIMM can carry a kit part number, and a search for a black kit can return its white suffix variant.
For complete systems, establish installed RAM and CPUs from the priced configuration, not slot counts or supported
maximums. GPU-capable servers must actually include the accelerators. Embedded listings must include the module's
RAM; SD/eMMC storage, carrier-only boards and similarly named books are not memory-equipped systems.

Searches can append unrelated results after reporting zero exact matches. Treat those as new leads to validate,
never as matches to the original query. An eBay Error Page is an access failure, not zero inventory; retry once by
reloading or using the original linked item URL, then record an unverified outcome if no current offer can be read.
