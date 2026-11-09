# Data conventions

Detailed rules for recording hardware data. The [README](../README.md) gives the reader-facing summary; this file
owns the details. Edit data, then run `make readme`, `make check` and `make test`.

## Sources

- `hardware_database.xlsx`: the `GPU`, `CPU` and `SoM` sheets feed the `gpu`, `cpu` and `embedded` categories. The
  generator reads saved cell values by header name and does not recalculate formulas. `Platform` and `Accelerator`
  rows are ranked only when registered in the overrides file.
- `data/workbook_overrides.csv`: keyed by `sheet` and `model`; every row must match an existing workbook row. It sets
  category and condition, and nonempty `memory_gb`, `bandwidth_gbs`, `price_usd`, `price_date`, `price_basis`,
  `availability` and `source` replace the workbook values; empty fields keep them. `notes` are appended. Use it for
  price-only refreshes so the workbook baseline stays untouched.
- `data/options.csv`: supplemental rows. Categories are `gpu`, `gpu_system`, `cpu`, `ddr`, `cpu_system` and
  `embedded`; conditions are `new` and `used`. Record the exact priced configuration, numeric GB and GBps, USD price,
  ISO price date, price basis, availability and source URLs (space-separated). Leave unknown values empty.
- The same category, condition, vendor and model may not appear in both the workbook and the CSV.
- Ranked metrics, category tables and worksheet columns are declared once in `METRICS`, `CATEGORIES` and `SHEETS` in
  [scripts/build_readme.py](../scripts/build_readme.py).

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
- **DDR**: separately priced DIMMs or kits. Capacity and bandwidth are for the whole kit. Bandwidth is payload
  bandwidth at the rated transfer rate; ECC bits add none. Two-DIMM kits assume two independent 64-bit channels; a
  DDR5 DIMM's two 32-bit subchannels together give 64 payload bits. XMP/EXPO speeds need a compatible CPU and board.
- **CPU systems**: complete servers with installed RAM; barebones chassis and CPU/board bundles are excluded.
  Capacity is installed RAM. Bandwidth uses verified installed DIMM count and operating rate, capped by CPU/OEM limits,
  assuming the manufacturer's recommended channel population; record that assumption in notes. If count, rate or
  population is unknown, leave bandwidth empty. Multi-socket figures are aggregate NUMA bandwidth. Refurbished
  servers are `used`; disclose absent drives.
- **Embedded**: SoMs, developer kits and boards with included RAM. Bare mobile SoCs without a priced memory
  configuration are excluded. Identify module/carrier bundles and complete kits in notes.
