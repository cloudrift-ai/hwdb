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
- The latest [price-refresh audit](data/price_refresh.json) accounts for every CPU, DDR, GPU-system, CPU-system and embedded row: 52 existing observations verified, 20 without a verified offer excluded, and two used embedded options added. Unverified rows retain historical prices/dates in source data; their unavailable status keeps them out of current rankings. “No verified offer” describes this search, not worldwide stock.
- GPU tables cover discrete cards/modules. GPU-system tables cover GPU and AI-accelerator systems, including unified-memory systems. Dedicated GPU memory excludes host RAM; shared unified memory is counted once. DGX Station GB300 uses **252 GB HBM**, because its recorded bandwidth is GPU HBM bandwidth, rather than the workbook's 748 GB combined CPU/GPU capacity. Multi-accelerator bandwidth and capacity are aggregate figures, not a single unified pool.
- V100 variants are separate candidates: PCIe 16GB/32GB, the HPE PCIe FHHL 16GB card, SXM2 16GB/32GB, SXM3 32GB and V100S PCIe 32GB. SXM modules require a compatible carrier, power delivery and cooling. They do not plug directly into a desktop PCIe slot. Adapter bundles are identified separately; module-only prices exclude the adapter and cooling.
- CPU rankings use processor-only prices, **excluding RAM**, boards and other platform costs. Peak bandwidth assumes the supported memory configuration is populated; it is not measured application throughput.
- CPU-system rankings use the price of the **complete server with installed RAM**. Barebones chassis and CPU/motherboard bundles are excluded. Capacity is the included RAM, not the platform maximum. Bandwidth uses the installed DIMM speed and populated channels; where those are unknown, the server appears only in the capacity ranking. Bandwidth summed across sockets/nodes is aggregate NUMA bandwidth, not the bandwidth available to a single core.
- DDR rankings cover separately priced DIMMs/kits, not CPU memory limits. Bandwidth is theoretical payload bandwidth at the stated transfer rate and channel count; ECC bits do not add payload bandwidth. Two-DIMM kits assume two independent 64-bit channels. Each DDR5 DIMM's two 32-bit subchannels together provide 64 payload bits. Installing more DIMMs on one channel does not multiply channel bandwidth. Rated XMP/EXPO speeds require a compatible CPU and board configuration.
- Embedded rankings cover new and used SoMs, developer kits and embedded boards with included RAM. Bare mobile SoCs without a priced memory configuration are excluded. Module prices can exclude carriers, storage, cooling and power supplies; see the recorded price basis.
- GB and GB/s retain the source table's conventions. Sources, estimates and configuration caveats remain in the workbook and supplemental CSV. Prices exclude any unrecorded shipping, tax and infrastructure costs.
- GPU New and Used prices were refreshed from live eBay item pages for the existing GPU candidates. These are selected one-unit asking prices with active purchase controls and US delivery, not market-wide minima or medians. Exact board, seller, visible feedback and shipping observations are retained in the CSV notes. Shipping is excluded from ranking prices; low-feedback sellers remain explicitly identified.
- The other categories now also use verified live eBay asking offers. CPU prices exclude RAM; CPU systems include the stated installed RAM, with absent drives disclosed. Module/carrier bundles and complete developer kits are identified in notes. Price-only refreshes preserve the workbook and use CSV overrides. Shipping quotes depend on the displayed US destination and are recorded separately; seller quality and freight accuracy are not established by a price observation.

<!-- Generated by scripts/build_readme.py. Edit source data, not these tables. -->

Last updated: 2026-10-22T19:48:19Z

## GPU New

### VRAM per $

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Intel Arc A770 16GB | 16.00 | $498.75 | 0.0321 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/168805452318>), [source2](<https://www.sparkle.com.tw/files/20240126145107552.pdf>) |
| 2 | AMD Radeon RX 6800 | 16.00 | $500.00 | 0.0320 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/187352880329>), [source2](<https://www.xfxforce.com/shop/xfx-speedster-swft-319-amd-radeon-tm-rx-6800-core-2>) |
| 3 | NVIDIA GeForce RTX 5050 8GB | 8.00 | $325.00 | 0.0246 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/168808537628>), [source2](<https://www.nvidia.com/en-sg/geforce/graphics-cards/50-series/rtx-5050/>) |
| 4 | NVIDIA GeForce RTX 5060 Ti 16GB | 16.00 | $749.99 | 0.0213 | 2 available | [source1](<https://www.ebay.com/itm/840015736032>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-5060-desktop-family-laptop-5060-coming-soon/>), [source3](<https://id.msi.com/Graphics-Card/GeForce-RTX-5060-Ti-16G-GAMING-OC/Specification>) |
| 5 | NVIDIA GeForce RTX 5060 Ti 8GB | 8.00 | $475.00 | 0.0168 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/257780137418>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-5060-desktop-family-laptop-5060-coming-soon/>), [source3](<https://us.msi.com/Graphics-Card/GeForce-RTX-5060-Ti-8G-GAMING/Specification>) |
| 6 | NVIDIA GeForce RTX 5070 | 12.00 | $800.00 | 0.0150 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/920064026275>), [source2](<https://www.nvidia.com/es-la/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/>), [source3](<https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5070-family/>) |
| 7 | NVIDIA GeForce RTX 5070 Ti | 16.00 | $1,200.00 | 0.0133 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/365631706301>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/>) |
| 8 | NVIDIA GeForce RTX 5080 | 16.00 | $1,600.00 | 0.0100 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/187049316024>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/>) |
| 9 | NVIDIA RTX PRO 6000 Blackwell | 96.00 | $17,499.95 | 0.0055 | 5 available | [source1](<https://www.ebay.com/itm/127889254783>), [source2](<https://marketplace.nvidia.com/en-us/enterprise/laptops-workstations/nvidia-rtx-pro-6000-blackwell-workstation-edition/>) |
| 10 | NVIDIA GeForce RTX 5090 | 32.00 | $7,075.00 | 0.0045 | More than 10 available | [source1](<https://www.ebay.com/itm/365705052856>), [source2](<https://www.gigabyte.com/Graphics-Card/GV-N5090WF3OC-32GD/sp>) |

### Bandwidth per $

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Intel Arc A770 16GB | 560.00 | $498.75 | 1.1228 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/168805452318>), [source2](<https://www.sparkle.com.tw/files/20240126145107552.pdf>) |
| 2 | AMD Radeon RX 6800 | 512.00 | $500.00 | 1.0240 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/187352880329>), [source2](<https://www.xfxforce.com/shop/xfx-speedster-swft-319-amd-radeon-tm-rx-6800-core-2>) |
| 3 | NVIDIA GeForce RTX 5050 8GB | 320.00 | $325.00 | 0.9846 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/168808537628>), [source2](<https://www.nvidia.com/en-sg/geforce/graphics-cards/50-series/rtx-5050/>) |
| 4 | NVIDIA GeForce RTX 5060 Ti 8GB | 448.00 | $475.00 | 0.9432 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/257780137418>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-5060-desktop-family-laptop-5060-coming-soon/>), [source3](<https://us.msi.com/Graphics-Card/GeForce-RTX-5060-Ti-8G-GAMING/Specification>) |
| 5 | NVIDIA GeForce RTX 5070 | 672.00 | $800.00 | 0.8400 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/920064026275>), [source2](<https://www.nvidia.com/es-la/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/>), [source3](<https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5070-family/>) |
| 6 | NVIDIA GeForce RTX 5070 Ti | 896.00 | $1,200.00 | 0.7467 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/365631706301>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/>) |
| 7 | NVIDIA GeForce RTX 5080 | 960.00 | $1,600.00 | 0.6000 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/187049316024>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/>) |
| 8 | NVIDIA GeForce RTX 5060 Ti 16GB | 448.00 | $749.99 | 0.5973 | 2 available | [source1](<https://www.ebay.com/itm/840015736032>), [source2](<https://www.nvidia.com/en-us/geforce/news/rtx-5060-desktop-family-laptop-5060-coming-soon/>), [source3](<https://id.msi.com/Graphics-Card/GeForce-RTX-5060-Ti-16G-GAMING-OC/Specification>) |
| 9 | NVIDIA GeForce RTX 5090 | 1,792.00 | $7,075.00 | 0.2533 | More than 10 available | [source1](<https://www.ebay.com/itm/365705052856>), [source2](<https://www.gigabyte.com/Graphics-Card/GV-N5090WF3OC-32GD/sp>) |
| 10 | NVIDIA RTX PRO 6000 Blackwell | 1,792.00 | $17,499.95 | 0.1024 | 5 available | [source1](<https://www.ebay.com/itm/127889254783>), [source2](<https://marketplace.nvidia.com/en-us/enterprise/laptops-workstations/nvidia-rtx-pro-6000-blackwell-workstation-edition/>) |

## GPU Used

### VRAM per $

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | NVIDIA Tesla M40 24GB | 24.00 | $139.99 | 0.1714 | 3 available | [source](<https://www.ebay.com/itm/407192112450>) |
| 2 | NVIDIA Tesla P100 PCIe 16GB | 16.00 | $127.63 | 0.1254 | More than 10 available | [source1](<https://www.ebay.com/itm/227544442858>), [source2](<https://images.nvidia.com/content/pdf/tesla/whitepaper/pascal-architecture-whitepaper.pdf>) |
| 3 | NVIDIA Tesla V100 SXM2 16GB | 16.00 | $173.41 | 0.0923 | More than 10 available; SXM2 carrier required | [source1](<https://www.ebay.com/itm/820137427098>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 4 | NVIDIA Tesla P40 24GB | 24.00 | $270.00 | 0.0889 | 4 available | [source](<https://www.ebay.com/itm/407266889692>) |
| 5 | NVIDIA Tesla V100 SXM3 32GB | 32.00 | $570.00 | 0.0561 | 4 available; SXM3 carrier required | [source1](<https://www.ebay.com/itm/137466175144>), [source2](<https://www.nvidia.com/en-sg/data-center/v100/>) |
| 6 | NVIDIA Tesla V100 PCIe 16GB | 16.00 | $299.00 | 0.0535 | More than 10 available | [source1](<https://www.ebay.com/itm/267791789788>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 7 | AMD Instinct MI50 32GB | 32.00 | $629.00 | 0.0509 | 8 available | [source](<https://www.ebay.com/itm/205802298789>) |
| 8 | NVIDIA Tesla V100 SXM2 16GB + PCIe adapter / air cooler | 16.00 | $338.98 | 0.0472 | More than 10 available; aftermarket adapter bundle | [source1](<https://www.ebay.com/itm/820215542468>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 9 | NVIDIA Tesla V100 PCIe 32GB | 32.00 | $704.99 | 0.0454 | More than 10 available | [source1](<https://www.ebay.com/itm/327316565001>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 10 | NVIDIA Tesla V100 SXM2 32GB | 32.00 | $799.90 | 0.0400 | More than 10 available | [source](<https://www.ebay.com/itm/287621214160>) |

### Bandwidth per $

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | NVIDIA Tesla P100 PCIe 16GB | 732.00 | $127.63 | 5.7353 | More than 10 available | [source1](<https://www.ebay.com/itm/227544442858>), [source2](<https://images.nvidia.com/content/pdf/tesla/whitepaper/pascal-architecture-whitepaper.pdf>) |
| 2 | NVIDIA Tesla V100 SXM2 16GB | 900.00 | $173.41 | 5.1900 | More than 10 available; SXM2 carrier required | [source1](<https://www.ebay.com/itm/820137427098>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 3 | NVIDIA Tesla V100 PCIe 16GB | 900.00 | $299.00 | 3.0100 | More than 10 available | [source1](<https://www.ebay.com/itm/267791789788>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 4 | NVIDIA Tesla V100 SXM2 16GB + PCIe adapter / air cooler | 900.00 | $338.98 | 2.6550 | More than 10 available; aftermarket adapter bundle | [source1](<https://www.ebay.com/itm/820215542468>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 5 | NVIDIA Tesla V100 PCIe FHHL 16GB (HPE Q8Z50A) | 900.00 | $399.99 | 2.2501 | More than 10 available | [source1](<https://www.ebay.com/itm/267806098645>), [source2](<https://www.hpe.com/psnow/doc/c04123180>) |
| 6 | NVIDIA Tesla M40 24GB | 288.00 | $139.99 | 2.0573 | 3 available | [source](<https://www.ebay.com/itm/407192112450>) |
| 7 | AMD Instinct MI50 32GB | 1,000.00 | $629.00 | 1.5898 | 8 available | [source](<https://www.ebay.com/itm/205802298789>) |
| 8 | NVIDIA Tesla V100 SXM3 32GB | 900.00 | $570.00 | 1.5789 | 4 available; SXM3 carrier required | [source1](<https://www.ebay.com/itm/137466175144>), [source2](<https://www.nvidia.com/en-sg/data-center/v100/>) |
| 9 | NVIDIA Tesla P40 24GB | 347.00 | $270.00 | 1.2852 | 4 available | [source](<https://www.ebay.com/itm/407266889692>) |
| 10 | NVIDIA Tesla V100 PCIe 32GB | 900.00 | $704.99 | 1.2766 | More than 10 available | [source1](<https://www.ebay.com/itm/327316565001>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |

## CPU New

### Bandwidth per $

Coverage: 6 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Ampere Altra Max M128-30 | 204.80 | $1,016.00 | 0.2016 | 7 available | [source1](<https://www.ebay.com/itm/318903589256>), [source2](<https://d1o0i0v5q5lp8h.cloudfront.net/ampere/live/assets/documents/Altra_Max_Rev_A1_DS_v1.05_20220728.pdf>) |
| 2 | AMD EPYC 7543P | 204.80 | $1,260.00 | 0.1625 | 7 available | [source1](<https://www.ebay.com/itm/188046400426>), [source2](<https://www.amd.com/pt/products/processors/server/epyc/7003-series/amd-epyc-7543p.html>) |
| 3 | AMD EPYC 9654 | 460.80 | $3,350.00 | 0.1376 | More than 10 available | [source1](<https://www.ebay.com/itm/175701978779>), [source2](<https://www.amd.com/en/products/processors/server/epyc/4th-generation-9004-and-8004-series/amd-epyc-9654.html>) |
| 4 | AMD EPYC 9965 | 614.00 | $5,682.47 | 0.1081 | More than 10 available | [source1](<https://www.ebay.com/itm/800683314273>), [source2](<https://www.amd.com/en/products/processors/server/epyc/9005-series/amd-epyc-9965.html>) |
| 5 | Intel Xeon 6980P | 844.80 | $15,312.00 | 0.0552 | 2 available | [source1](<https://www.ebay.com/itm/188079218032>), [source2](<https://www.intel.com/content/www/us/en/products/sku/240777/intel-xeon-6980p-processor-504m-cache-2-00-ghz/specifications.html>) |
| 6 | AMD Threadripper PRO 9995WX | 409.60 | $12,500.00 | 0.0328 | 2 available; one CPU per lot | [source1](<https://www.ebay.com/itm/366639575885>), [source2](<https://www.amd.com/en/products/processors/workstations/ryzen-threadripper.html>) |

## CPU Used

### Bandwidth per $

Coverage: 9 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | AMD EPYC 7551 | 170.62 | $25.58 | 6.6702 | More than 10 available | [source1](<https://www.ebay.com/itm/366735132359>), [source2](<https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/other/56301-memory-population-guidelines-epyc-processors.pdf>) |
| 2 | AMD EPYC 7402P | 204.80 | $59.95 | 3.4162 | More than 10 available | [source1](<https://www.ebay.com/itm/168251673337>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |
| 3 | AMD EPYC 7302P | 204.80 | $62.95 | 3.2534 | 5 available | [source1](<https://www.ebay.com/itm/960100845450>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |
| 4 | AMD EPYC 7402 | 204.80 | $69.00 | 2.9681 | 3 available | [source1](<https://www.ebay.com/itm/800162127887>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |
| 5 | AMD EPYC 7302 | 204.80 | $106.99 | 1.9142 | More than 10 available | [source1](<https://www.ebay.com/itm/405427667072>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |
| 6 | AMD EPYC 7502 | 204.80 | $149.00 | 1.3745 | 3 available | [source1](<https://www.ebay.com/itm/389827234686>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |
| 7 | AMD EPYC 7542 | 204.80 | $368.00 | 0.5565 | More than 10 available | [source1](<https://www.ebay.com/itm/174885200753>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |
| 8 | AMD EPYC 7532 | 204.80 | $425.00 | 0.4819 | 2 available | [source1](<https://www.ebay.com/itm/405996790809>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |
| 9 | AMD EPYC 7742 | 204.80 | $758.00 | 0.2702 | More than 10 available | [source1](<https://www.ebay.com/itm/174213203980>), [source2](<https://www.amd.com/en/products/processors/server/epyc/7002-series.html>) |

## GPU system New

### VRAM per $

Coverage: 7 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Apple Mac mini M4 16GB / 256GB | 16.00 | $669.00 | 0.0239 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/257805084125>), [source2](<https://www.apple.com/newsroom/2024/10/apples-new-mac-mini-is-more-mighty-more-mini-and-built-for-apple-intelligence/>), [source3](<https://support.apple.com/en-us/121555>) |
| 2 | Apple Mac Studio M1 Max 32GB / 512GB | 32.00 | $1,654.00 | 0.0193 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/227552573296>), [source2](<https://www.apple.com/newsroom/2022/03/apple-unveils-all-new-mac-studio-and-studio-display/>), [source3](<https://support.apple.com/en-us/111900>) |
| 3 | Apple Mac mini M4 Pro 24GB / 512GB | 24.00 | $1,249.00 | 0.0192 | 3 available | [source1](<https://www.ebay.com/itm/366153422358>), [source2](<https://www.apple.com/newsroom/2024/10/apples-new-mac-mini-is-more-mighty-more-mini-and-built-for-apple-intelligence/>), [source3](<https://support.apple.com/en-us/121555>) |
| 4 | NVIDIA DGX Spark | 128.00 | $7,070.00 | 0.0181 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/206643873787>), [source2](<https://docs.nvidia.com/dgx/dgx-spark/hardware.html>) |
| 5 | Apple Mac Studio M2 Ultra 64GB / 1TB | 64.00 | $3,899.00 | 0.0164 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/147597112420>), [source2](<https://www.tdsynnex.com/na/us/apple/wp-content/uploads/sites/49/2023/06/Mac-Studio-%E2%80%94-First-Look.pdf>), [source3](<https://support.apple.com/en-us/111835>) |
| 6 | Apple Mac mini M2 8GB / 256GB | 8.00 | $590.00 | 0.0136 | 5 available | [source1](<https://www.ebay.com/itm/128150434275>), [source2](<https://www.apple.com/newsroom/2023/01/apple-introduces-new-mac-mini-with-m2-and-m2-pro-more-powerful-capable-and-versatile-than-ever/>), [source3](<https://support.apple.com/en-us/111837>) |
| 7 | Apple Mac Studio M4 Max 36GB / 512GB | 36.00 | $2,699.00 | 0.0133 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/298596372842>), [source2](<https://www.apple.com/newsroom/2025/03/apple-unveils-new-mac-studio-the-most-powerful-mac-ever/>), [source3](<https://support.apple.com/en-us/122211>) |

### Bandwidth per $

Coverage: 7 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Apple Mac Studio M1 Max 32GB / 512GB | 400.00 | $1,654.00 | 0.2418 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/227552573296>), [source2](<https://www.apple.com/newsroom/2022/03/apple-unveils-all-new-mac-studio-and-studio-display/>), [source3](<https://support.apple.com/en-us/111900>) |
| 2 | Apple Mac mini M4 Pro 24GB / 512GB | 273.00 | $1,249.00 | 0.2186 | 3 available | [source1](<https://www.ebay.com/itm/366153422358>), [source2](<https://www.apple.com/newsroom/2024/10/apples-new-mac-mini-is-more-mighty-more-mini-and-built-for-apple-intelligence/>), [source3](<https://support.apple.com/en-us/121555>) |
| 3 | Apple Mac Studio M2 Ultra 64GB / 1TB | 800.00 | $3,899.00 | 0.2052 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/147597112420>), [source2](<https://www.tdsynnex.com/na/us/apple/wp-content/uploads/sites/49/2023/06/Mac-Studio-%E2%80%94-First-Look.pdf>), [source3](<https://support.apple.com/en-us/111835>) |
| 4 | Apple Mac mini M4 16GB / 256GB | 120.00 | $669.00 | 0.1794 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/257805084125>), [source2](<https://www.apple.com/newsroom/2024/10/apples-new-mac-mini-is-more-mighty-more-mini-and-built-for-apple-intelligence/>), [source3](<https://support.apple.com/en-us/121555>) |
| 5 | Apple Mac mini M2 8GB / 256GB | 100.00 | $590.00 | 0.1695 | 5 available | [source1](<https://www.ebay.com/itm/128150434275>), [source2](<https://www.apple.com/newsroom/2023/01/apple-introduces-new-mac-mini-with-m2-and-m2-pro-more-powerful-capable-and-versatile-than-ever/>), [source3](<https://support.apple.com/en-us/111837>) |
| 6 | Apple Mac Studio M4 Max 36GB / 512GB | 410.00 | $2,699.00 | 0.1519 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/298596372842>), [source2](<https://www.apple.com/newsroom/2025/03/apple-unveils-new-mac-studio-the-most-powerful-mac-ever/>), [source3](<https://support.apple.com/en-us/122211>) |
| 7 | NVIDIA DGX Spark | 273.00 | $7,070.00 | 0.0386 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/206643873787>), [source2](<https://docs.nvidia.com/dgx/dgx-spark/hardware.html>) |

## GPU system Used

### VRAM per $

Coverage: 7 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Supermicro / Intel SYS-820GH-TNR2 with 8x Gaudi2 | 768.00 | $30,155.73 | 0.0255 | 2 available | [source](<https://www.ebay.com/itm/377517265816>) |
| 2 | Apple Mac Studio M1 Max 32GB / 512GB | 32.00 | $1,309.99 | 0.0244 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/336789674454>), [source2](<https://support.apple.com/en-us/111900>) |
| 3 | Apple Mac Studio M1 Ultra 64GB / 1TB | 64.00 | $2,699.00 | 0.0237 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/128137935700>), [source2](<https://support.apple.com/en-us/111900>) |
| 4 | Apple Mac mini M2 Pro 16GB / 512GB | 16.00 | $674.95 | 0.0237 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/206639109051>), [source2](<https://support.apple.com/en-us/111837>) |
| 5 | Apple Mac mini M2 Pro 32GB / 1TB | 32.00 | $1,565.00 | 0.0204 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/800743788326>), [source2](<https://support.apple.com/en-us/111837>) |
| 6 | Apple Mac Studio M2 Max 32GB / 1TB | 32.00 | $2,189.99 | 0.0146 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/336766575807>), [source2](<https://support.apple.com/en-us/111835>) |
| 7 | NVIDIA DGX-1 with 8x V100 SXM2 32GB | 256.00 | $20,000.00 | 0.0128 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/117477149565>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |

### Bandwidth per $

Coverage: 7 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Supermicro / Intel SYS-820GH-TNR2 with 8x Gaudi2 | 19,600.00 | $30,155.73 | 0.6500 | 2 available | [source](<https://www.ebay.com/itm/377517265816>) |
| 2 | NVIDIA DGX-1 with 8x V100 SXM2 32GB | 7,200.00 | $20,000.00 | 0.3600 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/117477149565>), [source2](<https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf>) |
| 3 | Apple Mac Studio M1 Max 32GB / 512GB | 400.00 | $1,309.99 | 0.3053 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/336789674454>), [source2](<https://support.apple.com/en-us/111900>) |
| 4 | Apple Mac Studio M1 Ultra 64GB / 1TB | 800.00 | $2,699.00 | 0.2964 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/128137935700>), [source2](<https://support.apple.com/en-us/111900>) |
| 5 | Apple Mac mini M2 Pro 16GB / 512GB | 200.00 | $674.95 | 0.2963 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/206639109051>), [source2](<https://support.apple.com/en-us/111837>) |
| 6 | Apple Mac Studio M2 Max 32GB / 1TB | 400.00 | $2,189.99 | 0.1826 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/336766575807>), [source2](<https://support.apple.com/en-us/111835>) |
| 7 | Apple Mac mini M2 Pro 32GB / 1TB | 200.00 | $1,565.00 | 0.1278 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/800743788326>), [source2](<https://support.apple.com/en-us/111837>) |

## DDR memory New

### RAM per $

Coverage: 9 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Corsair Vengeance LPX CMK32GX4M2E3200C16 32GB (2x16GB DDR4-3200) | 32.00 | $179.99 | 0.1778 | 3 available | [source](<https://www.ebay.com/itm/880020343617>) |
| 2 | Corsair Vengeance RGB Pro CMW32GX4M2E3200C16 32GB (2x16GB DDR4-3200) | 32.00 | $200.00 | 0.1600 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/318829381313>) |
| 3 | GeIL ORION GAOG432GB3200C18ADC 32GB (2x16GB DDR4-3200) | 32.00 | $216.49 | 0.1478 | More than 10 available | [source](<https://www.ebay.com/itm/800013079894>) |
| 4 | G.SKILL Ripjaws V F4-3200C16D-32GVK 32GB (2x16GB DDR4-3200) | 32.00 | $229.99 | 0.1391 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/327379307061>) |
| 5 | TEAMGROUP T-Force Vulcan Z TLZGD432G3200HC16FDC01 32GB (2x16GB DDR4-3200) | 32.00 | $247.49 | 0.1293 | More than 10 available | [source](<https://www.ebay.com/itm/303856987561>) |
| 6 | Crucial Pro CP2K16G4DFRA32A 32GB (2x16GB DDR4-3200) | 32.00 | $249.99 | 0.1280 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/389447703301>) |
| 7 | TEAMGROUP T-Force Delta RGB TF3D432G3200HC16FDC01 32GB (2x16GB DDR4-3200) | 32.00 | $296.39 | 0.1080 | 2 available | [source](<https://www.ebay.com/itm/336434192278>) |
| 8 | Corsair Vengeance CMK32GX5M2D6000Z38 32GB (2x16GB DDR5-6000) | 32.00 | $494.49 | 0.0647 | More than 10 available | [source](<https://www.ebay.com/itm/298522267634>) |
| 9 | G.SKILL Ripjaws S5 F5-5600J3636D32GX2-RS5W 64GB (2x32GB DDR5-5600) | 64.00 | $1,232.02 | 0.0519 | 2 available | [source](<https://www.ebay.com/itm/398415031948>) |

### Bandwidth per $

Coverage: 9 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Corsair Vengeance LPX CMK32GX4M2E3200C16 32GB (2x16GB DDR4-3200) | 51.20 | $179.99 | 0.2845 | 3 available | [source](<https://www.ebay.com/itm/880020343617>) |
| 2 | Corsair Vengeance RGB Pro CMW32GX4M2E3200C16 32GB (2x16GB DDR4-3200) | 51.20 | $200.00 | 0.2560 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/318829381313>) |
| 3 | GeIL ORION GAOG432GB3200C18ADC 32GB (2x16GB DDR4-3200) | 51.20 | $216.49 | 0.2365 | More than 10 available | [source](<https://www.ebay.com/itm/800013079894>) |
| 4 | G.SKILL Ripjaws V F4-3200C16D-32GVK 32GB (2x16GB DDR4-3200) | 51.20 | $229.99 | 0.2226 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/327379307061>) |
| 5 | TEAMGROUP T-Force Vulcan Z TLZGD432G3200HC16FDC01 32GB (2x16GB DDR4-3200) | 51.20 | $247.49 | 0.2069 | More than 10 available | [source](<https://www.ebay.com/itm/303856987561>) |
| 6 | Crucial Pro CP2K16G4DFRA32A 32GB (2x16GB DDR4-3200) | 51.20 | $249.99 | 0.2048 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/389447703301>) |
| 7 | Corsair Vengeance CMK32GX5M2D6000Z38 32GB (2x16GB DDR5-6000) | 96.00 | $494.49 | 0.1941 | More than 10 available | [source](<https://www.ebay.com/itm/298522267634>) |
| 8 | TEAMGROUP T-Force Delta RGB TF3D432G3200HC16FDC01 32GB (2x16GB DDR4-3200) | 51.20 | $296.39 | 0.1727 | 2 available | [source](<https://www.ebay.com/itm/336434192278>) |
| 9 | G.SKILL Ripjaws S5 F5-5600J3636D32GX2-RS5W 64GB (2x32GB DDR5-5600) | 89.60 | $1,232.02 | 0.0727 | 2 available | [source](<https://www.ebay.com/itm/398415031948>) |

## DDR memory Used

### RAM per $

Coverage: 4 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Kingston KVR21R15D4/16 16GB (1x16GB DDR4-2133 RDIMM) | 16.00 | $59.99 | 0.2667 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/128138099828>) |
| 2 | Samsung M393A4K40CB1-CRC4Q 32GB (1x32GB DDR4-2400 RDIMM) | 32.00 | $139.00 | 0.2302 | 3 available | [source](<https://www.ebay.com/itm/227577844676>) |
| 3 | SK hynix HMA84GR7JJR4N-VK 32GB (1x32GB DDR4-2666 RDIMM) | 32.00 | $189.99 | 0.1684 | 3 available | [source](<https://www.ebay.com/itm/227577414940>) |
| 4 | Corsair Vengeance LPX CMK64GX4M2E3200C16 64GB (2x32GB DDR4-3200) | 64.00 | $804.97 | 0.0795 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/206642886531>) |

### Bandwidth per $

Coverage: 4 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Kingston KVR21R15D4/16 16GB (1x16GB DDR4-2133 RDIMM) | 17.06 | $59.99 | 0.2844 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/128138099828>) |
| 2 | Samsung M393A4K40CB1-CRC4Q 32GB (1x32GB DDR4-2400 RDIMM) | 19.20 | $139.00 | 0.1381 | 3 available | [source](<https://www.ebay.com/itm/227577844676>) |
| 3 | SK hynix HMA84GR7JJR4N-VK 32GB (1x32GB DDR4-2666 RDIMM) | 21.33 | $189.99 | 0.1123 | 3 available | [source](<https://www.ebay.com/itm/227577414940>) |
| 4 | Corsair Vengeance LPX CMK64GX4M2E3200C16 64GB (2x32GB DDR4-3200) | 51.20 | $804.97 | 0.0636 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/206642886531>) |

## CPU systems New

### RAM per $

Coverage: 4 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | HPE ProLiant DL365 G11 P93189-005 / EPYC 9115 / 64GB | 64.00 | $10,251.39 | 0.0062 | 2 available | [source](<https://www.ebay.com/itm/407177066417>) |
| 2 | HPE ProLiant ML30 Gen11 P86770-005 / Xeon 6325P / 32GB | 32.00 | $5,552.16 | 0.0058 | More than 10 available | [source](<https://www.ebay.com/itm/307051297379>) |
| 3 | HPE ProLiant MicroServer Gen11 P86811-005 / Xeon 6315P / 16GB | 16.00 | $2,850.00 | 0.0056 | 3 available | [source](<https://www.ebay.com/itm/188714801862>) |
| 4 | HPE ProLiant DL20 Gen11 P83282-005 / Xeon 6325P / 32GB | 32.00 | $6,068.09 | 0.0053 | 4 available | [source1](<https://www.ebay.com/itm/307195851431>), [source2](<https://www.hpe.com/psnow/doc/a50009219enw>) |

### Bandwidth per $

Coverage: 1 qualifying option after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | HPE ProLiant DL20 Gen11 P83282-005 / Xeon 6325P / 32GB | 38.40 | $6,068.09 | 0.0063 | 4 available | [source1](<https://www.ebay.com/itm/307195851431>), [source2](<https://www.hpe.com/psnow/doc/a50009219enw>) |

## CPU systems Used

### RAM per $

Coverage: 2 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | Dell PowerEdge R740xd / 2x Xeon Gold 6130 / 256GB | 256.00 | $1,818.00 | 0.1408 | Active Buy It Now; US delivery | [source](<https://www.ebay.com/itm/128133563986>) |
| 2 | Dell PowerEdge R740 / 2x Xeon Platinum 8160 / 128GB | 128.00 | $1,524.95 | 0.0839 | 2 available | [source](<https://www.ebay.com/itm/389354651938>) |

### Bandwidth per $

Coverage: 0 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |

No qualifying options recorded.

## Embedded systems New

### RAM per $

Coverage: 3 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | NVIDIA Jetson AGX Orin 64GB | 64.00 | $3,199.00 | 0.0200 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/278440864845>), [source2](<https://developer.nvidia.com/embedded/faq>) |
| 2 | NVIDIA Jetson Orin Nano Super Developer Kit 8GB | 8.00 | $479.99 | 0.0167 | 5 available | [source1](<https://www.ebay.com/itm/307210826593>), [source2](<https://www.nvidia.com/en-au/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>), [source3](<https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>) |
| 3 | NVIDIA Jetson Orin NX 16GB | 16.00 | $999.99 | 0.0160 | More than 10 available | [source1](<https://www.ebay.com/itm/197871033036>), [source2](<https://developer.nvidia.com/embedded/faq>) |

### Bandwidth per $

Coverage: 3 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | NVIDIA Jetson Orin Nano Super Developer Kit 8GB | 102.00 | $479.99 | 0.2125 | 5 available | [source1](<https://www.ebay.com/itm/307210826593>), [source2](<https://www.nvidia.com/en-au/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>), [source3](<https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>) |
| 2 | NVIDIA Jetson Orin NX 16GB | 102.40 | $999.99 | 0.1024 | More than 10 available | [source1](<https://www.ebay.com/itm/197871033036>), [source2](<https://developer.nvidia.com/embedded/faq>) |
| 3 | NVIDIA Jetson AGX Orin 64GB | 204.80 | $3,199.00 | 0.0640 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/278440864845>), [source2](<https://developer.nvidia.com/embedded/faq>) |

## Embedded systems Used

### RAM per $

Coverage: 3 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB | Price (USD) | GB/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | NVIDIA Jetson Xavier NX 16GB | 16.00 | $700.00 | 0.0229 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/257297923330>), [source2](<https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-xavier-nx/>) |
| 2 | NVIDIA Jetson Orin NX 16GB | 16.00 | $800.00 | 0.0200 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/147617714182>), [source2](<https://developer.nvidia.com/embedded/faq>) |
| 3 | NVIDIA Jetson Orin Nano Super Developer Kit 8GB | 8.00 | $550.00 | 0.0145 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/188643881194>), [source2](<https://www.nvidia.com/en-au/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>), [source3](<https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>) |

### Bandwidth per $

Coverage: 3 qualifying options after availability filtering; fewer than ten recorded.

| Rank | Option | GB/s | Price (USD) | GB/s/$ | Availability | Sources |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | NVIDIA Jetson Orin Nano Super Developer Kit 8GB | 102.00 | $550.00 | 0.1855 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/188643881194>), [source2](<https://www.nvidia.com/en-au/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>), [source3](<https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/>) |
| 2 | NVIDIA Jetson Orin NX 16GB | 102.40 | $800.00 | 0.1280 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/147617714182>), [source2](<https://developer.nvidia.com/embedded/faq>) |
| 3 | NVIDIA Jetson Xavier NX 16GB | 59.70 | $700.00 | 0.0853 | Active Buy It Now; US delivery | [source1](<https://www.ebay.com/itm/257297923330>), [source2](<https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-xavier-nx/>) |
