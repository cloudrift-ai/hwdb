# Seeed Studio

Apply [the shared listing contract](../listings.md). Search `site:seeedstudio.com` for an exact reComputer, Jetson or
embedded board model, then open its product page. Example:
<https://www.seeedstudio.com/reComputer-J3011-p-5590.html>.

Read SKU, product heading, processor, RAM, main one-unit price and “In stock” status. Variant controls can list Orin
Nano and NX, multiple RAM sizes and wireless choices on one page. Use only the configuration tied to the displayed
SKU and price; switch to an exact linked SKU or report ambiguity. Do not use the “10+” price for a single system.
Distinguish an assembled reComputer with carrier/storage from a bare Jetson module, and record included components.
Confirm storefront currency before emitting `price_usd`. Return the shared result with manufacturer specifications
for the exact module and operating mode when calculating bandwidth.
