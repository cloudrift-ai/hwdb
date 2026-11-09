# Data conventions

Detailed rules for recording hardware data. The [README](../README.md) gives the reader-facing summary; this file
owns the details. Edit data, then run `make readme`, `make check` and `make test`.

## Sources

- `hardware_database.xlsx`: the `GPU`, `CPU` and `SoM` sheets feed the `gpu`, `cpu` and `embedded` categories. The
  generator reads saved cell values by header name and does not recalculate formulas. `Platform` and `Accelerator`
  rows are ranked only when registered in the overrides file.
- `data/workbook_overrides.csv`: keyed by `sheet` and `model`; every row must match an existing workbook row. It sets
  category, condition and optional display names, and nonempty `memory_gb`, `bandwidth_gbs`, `tops`, `tops_type`,
  `tops_source`, `price_usd`, `price_date`, `price_basis`, `availability` and `source` replace the workbook values;
  empty fields keep them. `notes` are appended. Use it for price-only refreshes so the workbook baseline stays
  untouched.
- `data/options.csv`: supplemental rows. Categories are `gpu`, `gpu_system`, `cpu`, `ddr`, `cpu_system` and
  `embedded`; conditions are `new` and `used`. Record the exact priced configuration, numeric GB and GBps, USD price,
  ISO price date, price basis, availability and source URLs (space-separated). Leave unknown values empty.
  DDR rows also require `modules` and `memory_type`.
- The same category, condition, vendor, model and memory size may not appear twice across the workbook and the CSV.

## Names

- `model` is the short display name shown in the README, ideally at most 27 characters with the vendor. Drop what
  other columns show (memory size, DDR module count and type), storage, retail part numbers and redundant branding
  (GeForce, Tesla, Jetson, PowerEdge, ProLiant, Vengeance). Keep what tells configurations apart: form factor (PCIe,
  SXM2, FHHL), CPU count and model for systems, adapter or kit bundles, and the exact SKU for DDR.
- Record the full listing name, part numbers and other configuration details in notes, for example
  `Full listing name: ...`.
- Variants that differ only in memory size share a model and are told apart by `memory_gb`.
- Workbook rows keep their workbook names; set `display_vendor` and `display_model` in the overrides to shorten them.
- Ranked metrics, category tables and worksheet columns are declared once in `METRICS`, `CATEGORIES` and `SHEETS` in
  [scripts/build_readme.py](../scripts/build_readme.py).

## Sources

- Every ranked row needs the live offer URL and at least one specification URL that states its capacity, bandwidth
  inputs or exact SKU. Research audits live in `data/price_refresh.json`, `data/top_ten_expansion.json` and dated
  `data/offer_research_*.json` files. Prefer vendor product pages, datasheets and QuickSpecs. Use a parts database or
  marketplace spec listing only for discontinued parts with no vendor page, such as older server RDIMMs.
- Tested 2026-11-08: AMD per-SKU CPU specs for older parts live under
  `amd.com/en/support/downloads/drivers.html/processors/...`; the former product URLs return 404 and
  `/en/products/cpu/<sku>` redirects to a generic table. amd.com, hpe.com and crucial.com often time out or reject
  automated fetches; a browser or `curl` with a browser user agent works. eBay, Newegg and Intel return 403 to plain
  HTTP checks, so a 403 is not evidence of a dead link.

## Compute (TOPS)

- `tops` is dense peak throughput in TOPS (TFLOPS for floating-point types) for the fastest natively supported
  tensor/matrix data type, named in `tops_type` (NVFP4, FP4, FP8, INT4, INT8, BF16, FP16, FP32). Set both or neither.
  `tops_source` holds the specification URLs; put the basis and any formula in notes.
- Use vendor figures when published. Halve figures quoted with structured sparsity.
- Without tensor/matrix units, use the fastest native arithmetic type (packed FP16, INT8 dot product, else FP32).
- CPUs: calculated per socket as cores × base clock × ops/cycle/core, a multiply-accumulate counting as two ops,
  using AMX, VNNI/SDOT or SIMD FMA as the hardware supports. Systems sum all sockets or accelerators.
- Jetson modules use NVIDIA's combined GPU + DLA figure. Apple Macs use the Neural Engine figure Apple publishes.
- Workbook rows take TOPS from `data/workbook_overrides.csv`; the workbook has no TOPS column.

## Availability and condition

- Rows whose availability or price basis says out of stock, sold, ended, unavailable or discontinued are excluded
  from rankings. A missing price or metric excludes a row only from the affected table.
- Without an override, condition is `used` when the price basis says used or refurbished, otherwise `new`.
- Rows without a verified current offer keep their historical price and date, marked
  `Unavailable: no verified current ... offer`. "No verified offer" describes the search, not worldwide stock.
- [price_refresh.json](../data/price_refresh.json) records the first non-GPU refresh;
  [top_ten_expansion.json](../data/top_ten_expansion.json) records the later coverage expansion. Keep both as history.
- Prices are single asking offers. Shipping, delivered totals, seller and feedback go in notes, not the ranked price.

## Category details

- **GPU**: discrete cards and modules. Dedicated memory excludes host RAM. V100 forms are distinct candidates
  (PCIe 16/32GB, HPE PCIe FHHL 16GB, SXM2 16/32GB, SXM3 32GB, V100S PCIe 32GB). Adapter bundles are named separately;
  module-only prices exclude the adapter and cooling.
- **GPU systems**: GPU and AI-accelerator systems, including unified-memory systems. Count GPU-accessible memory;
  unified memory is counted once. DGX Station GB300 uses 252 GB HBM, matching its GPU HBM bandwidth, rather than its
  748 GB combined CPU/GPU capacity. Multi-accelerator figures are aggregates.
- **CPU**: processor-only price, excluding RAM, board and platform. Peak bandwidth assumes the supported memory
  configuration is fully populated.
- **DDR**: separately priced DIMMs or kits. Capacity and bandwidth are for the whole kit. Record the module count in
  `modules` and the generation, rated speed and RDIMM marking in `memory_type` (for example `DDR4-2400 RDIMM`).
  `model` holds the exact kit or module SKU and `series` the product line (for example `Vengeance LPX`; empty for
  unbranded server RDIMMs). Tables show vendor and series, with the SKU in a collapsed part. Bandwidth is payload
  bandwidth at the rated transfer rate; ECC bits add none. Two-DIMM kits assume two independent 64-bit channels; a
  DDR5 DIMM's two 32-bit subchannels together give 64 payload bits. XMP/EXPO speeds need a compatible CPU and board.
- **CPU systems**: complete servers with installed RAM; barebones chassis and CPU/board bundles are excluded. Capacity
  is installed RAM. Bandwidth uses verified installed DIMM count and operating rate, capped by CPU/OEM limits, assuming
  the manufacturer's recommended channel population; record that assumption in notes. Use the vendor's
  speed-by-DIMMs-per-channel table: the Dell R740 technical guide runs 8GB 1R PC4-2933 RDIMMs at 2666 MT/s. If count,
  rate or population is unknown, leave bandwidth empty. Multi-socket figures are aggregate NUMA bandwidth. Refurbished
  servers are `used`; disclose absent drives.
- **Embedded**: SoMs, developer kits and boards with included RAM. Bare mobile SoCs without a priced memory
  configuration are excluded. Identify module/carrier bundles and complete kits in notes.
