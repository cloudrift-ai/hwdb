# HWDB

HWDB compares hardware by memory capacity and theoretical memory bandwidth per US dollar. The tables below rank the priced options recorded in this repository; they are not a survey of the entire market.

## Updating the README

Requires Python 3.10+ and `openpyxl`:

```sh
python3 -m pip install -r requirements.txt
make readme
make check
make test
```

Edit [hardware_database.xlsx](hardware_database.xlsx) for existing hardware or add rows to [data/options.csv](data/options.csv), then run `make readme`. The generator reads worksheet headers, computes ratios from the underlying capacity, bandwidth and price fields, and assembles this introduction with the ranking sections. Edit [docs/README.template.md](docs/README.template.md) to change the introduction. `make check` fails if the checked-in README differs from the generated result. Set `PYTHON` to select a different interpreter.

Supplemental CSV rows use categories `gpu`, `gpu_system`, `cpu`, `ddr`, `cpu_system`, or `embedded`, and conditions `new` or `used`. Record the exact priced configuration, numeric GB and GB/s values, USD price, ISO price date, price basis, availability and source URL. Leave an unknown value empty. Use the total capacity and bandwidth of the priced memory kit for DDR, the installed RAM configuration for a CPU system, and the GPU-accessible memory for a GPU system. Workbook and CSV entries with the same category, condition, vendor and model are rejected to avoid double-counting.

The workbook's `GPU`, `CPU` and `SoM` sheets feed the matching categories. Register eligible `Platform` rows in [data/workbook_overrides.csv](data/workbook_overrides.csv), distinguishing GPU systems from CPU servers. This file also supports explicit condition and memory-capacity overrides, plus current price, date, basis, availability, source and additional notes. Nonempty price-observation fields supersede the baseline workbook values; empty fields retain them. Otherwise condition is inferred from the price basis (`used`/`refurbished` versus new). The generator reads saved input values and does not recalculate Excel formulas.

## Agent workflows and store research

HWDB follows Emmy's structure: repository guidance in [AGENTS.md](AGENTS.md), reusable skills in `.agents/skills/`,
and shared task contracts in `prompts/`. [CLAUDE.md](CLAUDE.md) points to the same repository guidance.

| Task | Skill | Shared prompt |
| --- | --- | --- |
| Find or recheck priced hardware | [research-hardware](.agents/skills/research-hardware/SKILL.md) | [Listing evidence and results](prompts/research-hardware/listings.md) |
| Update data and regenerate rankings | [refresh-readme](.agents/skills/refresh-readme/SKILL.md) | [Refresh contract](prompts/refresh-readme.md) |

The [tested store catalog](docs/stores.md) links to retrieval prompts for Newegg, eBay, Adafruit, Seeed Studio,
The Server Store and Mac-Ave. It records working access routes, stock checks and limitations. Start with its preferred
stores and reject unavailable offers. Store prompts extend one shared listing contract rather than duplicating it.
The [current GPU pricing procedure](docs/gpu-prices.md) documents tested live eBay searches for New and Used offers,
item-level stock and delivery checks, and the optional API route. Research findings keep the relevant prompts and
repository guidance current.

For example: “Research ten used GPUs using the store catalog, verify prices and stock, update the source tables,
and regenerate the README.” A request to research alone returns candidates without changing hardware data.

## How to read the rankings

- Capacity per dollar is **GB / USD**. Bandwidth per dollar is **(GB/s) / USD**. Higher is better. Rankings use unrounded values, then lower price and model name to break ties. Displayed ratios have four decimal places.
- Each table contains up to ten options. Listings marked out of stock, sold, ended, unavailable or discontinued in their availability or price basis are excluded before ranking. A coverage note appears when fewer qualify. A missing price or metric excludes the entry only from the affected ranking. Empty tables mean the repository has no qualifying data.
- New and used refer to the **price observation**, not every market where a product can be found. Historical prices remain in source data with their dates and bases; entries without a verified current offer are excluded from these rankings. Availability reflects the recorded live listing and can change after retrieval. The single “Last updated” timestamp records when the rankings were generated (UTC), not a guarantee that every listing remains available.
- The earlier [price-refresh audit](data/price_refresh.json) accounts for the original CPU, DDR, GPU-system, CPU-system and embedded rows: 52 existing observations verified, 20 without a verified offer excluded, and two used embedded options added. The subsequent [coverage expansion](data/top_ten_expansion.json) adds 49 verified available configurations and updates three existing ones, filling all 22 metric tables to ten entries using eBay, Newegg and Adafruit. Unverified rows retain historical prices/dates in source data; their unavailable status keeps them out of current rankings. “No verified offer” describes this search, not worldwide stock.
- GPU tables cover discrete cards/modules. GPU-system tables cover GPU and AI-accelerator systems, including unified-memory systems. Dedicated GPU memory excludes host RAM; shared unified memory is counted once. DGX Station GB300 uses **252 GB HBM**, because its recorded bandwidth is GPU HBM bandwidth, rather than the workbook's 748 GB combined CPU/GPU capacity. Multi-accelerator bandwidth and capacity are aggregate figures, not a single unified pool.
- V100 variants are separate candidates: PCIe 16GB/32GB, the HPE PCIe FHHL 16GB card, SXM2 16GB/32GB, SXM3 32GB and V100S PCIe 32GB. SXM modules require a compatible carrier, power delivery and cooling. They do not plug directly into a desktop PCIe slot. Adapter bundles are identified separately; module-only prices exclude the adapter and cooling.
- CPU rankings use processor-only prices, **excluding RAM**, boards and other platform costs. Peak bandwidth assumes the supported memory configuration is populated; it is not measured application throughput.
- CPU-system rankings use the price of the **complete server with installed RAM**. Barebones chassis and CPU/motherboard bundles are excluded. Capacity is the included RAM, not the platform maximum. Theoretical bandwidth uses verified installed DIMM counts and operating rates, capped by CPU/OEM limits, with DIMMs placed in independent channels according to the manufacturer's recommended population rules. That population assumption is recorded in notes; these are configuration-specific theoretical figures, not measurements of a shipped machine. Where count, rate or population cannot support the calculation, the server appears only in the capacity ranking. Bandwidth summed across sockets/nodes is aggregate NUMA bandwidth, not the bandwidth available to a single core.
- DDR rankings cover separately priced DIMMs/kits, not CPU memory limits. Bandwidth is theoretical payload bandwidth at the stated transfer rate and channel count; ECC bits do not add payload bandwidth. Two-DIMM kits assume two independent 64-bit channels. Each DDR5 DIMM's two 32-bit subchannels together provide 64 payload bits. Installing more DIMMs on one channel does not multiply channel bandwidth. Rated XMP/EXPO speeds require a compatible CPU and board configuration.
- Embedded rankings cover new and used SoMs, developer kits and embedded boards with included RAM. Bare mobile SoCs without a priced memory configuration are excluded. Module prices can exclude carriers, storage, cooling and power supplies; see the recorded price basis.
- GB and GB/s retain the source table's conventions. Sources, estimates and configuration caveats remain in the workbook and supplemental CSV. Prices exclude any unrecorded shipping, tax and infrastructure costs.
- GPU New and Used prices were refreshed from live eBay item pages for the existing GPU candidates. These are selected one-unit asking prices with active purchase controls and US delivery, not market-wide minima or medians. Exact board, seller, visible feedback and shipping observations are retained in the CSV notes. Shipping is excluded from ranking prices; low-feedback sellers remain explicitly identified.
- The other categories use verified live eBay, Newegg and Adafruit asking offers. CPU prices exclude RAM; CPU systems include the stated installed RAM, with absent drives disclosed. Refurbished server offers are grouped under used, with their exact condition retained in notes. Module/carrier bundles and complete developer kits are identified in notes. Price-only refreshes preserve the workbook and use CSV overrides. Shipping quotes depend on the displayed US destination and are recorded separately; seller quality and freight accuracy are not established by a price observation.

{{RANKINGS}}
