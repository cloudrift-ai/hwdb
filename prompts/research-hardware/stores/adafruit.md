# Adafruit

Apply [the shared listing contract](../listings.md). Search `site:adafruit.com/product/` for the board and RAM size.
Open the exact numeric product URL; an example is <https://www.adafruit.com/product/5813> for Raspberry Pi 5 8GB.

Read the selected product ID, RAM size, main price and stock together. Related variants are often listed on the same
page with different prices and availability; follow their links rather than attaching the cheapest price to the
largest RAM configuration. Optional case and cable checkboxes are extra costs, not included accessories. Record
quantity limits. Use the US storefront's USD price and obtain missing memory-bandwidth specifications from primary
hardware documentation. Return the shared result; an out-of-stock sibling does not make every RAM variant unavailable.

The live search route `https://www.adafruit.com/search?q=QUERY` exposes product IDs, prices and available quantities;
open each chosen numeric product page to verify it. On 2026-10-22, Pi 5 1/4/8/16GB, Pi 4 4/8GB and Pi 500 8GB were
available, while Pi 5 2GB, Pi 4 1/2GB and Pi 500+ were unavailable. These are dated examples, not reusable stock data.
Do not equate a search for Compute Module 5 with the Compute Module 4 accessories returned by loose matching.
Retain unknown shipping as unknown: the public product page's price excludes any checkout shipping quote.

For bandwidth, distinguish DRAM rating from the board's operating interface. Raspberry Pi's official Pi 5 launch
article specifies 32-bit LPDDR4X-4267 and Pi 4's effective 2000 MT/s interface. Thus Pi 5/Pi 500 calculate to
17.068 GB/s and Pi 4 to 8 GB/s theoretical; do not assign Pi 4 12.8 GB/s from its 3200-rated memory label alone.
