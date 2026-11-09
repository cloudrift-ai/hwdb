# HWDB

HWDB ranks hardware by memory capacity, theoretical memory bandwidth and peak compute (TOPS) per US dollar. Each
table lists up to ten in-stock offers recorded in this repository; it is not a survey of the whole market.

## Reading the tables

- **GB/$**, **GBps/$** and **TOPS/$**: higher is better. Ties go to the lower price.
- **Price** is one verified asking offer for the exact configuration, excluding shipping and tax. It is not a market
  median. Out-of-stock, sold and ended offers are excluded. Listings can change after the "Last updated" time.
- **New / Used** describes the offer. Refurbished counts as used.
- **Bandwidth** is the theoretical peak from specifications, not a measurement. Multi-device and multi-socket figures
  are aggregates, not one unified pool.
- **TOPS** is dense peak throughput (no sparsity) for the fastest natively supported tensor data type, shown in the
  **Type** column (for example NVFP4, FP8, INT8). Devices without tensor units use their fastest native type. CPU
  figures are calculated at base clock from the instruction set (AMX, VNNI, SIMD FMA); multi-device systems are summed.
  TOPS across types are not equivalent work: an NVFP4 TOPS is not an FP16 TFLOPS.
- A table with fewer than ten rows has a coverage note; there were not enough verified offers.

## Categories

- **GPU**: discrete cards and modules; capacity is VRAM only. Variants (PCIe vs SXM, memory size) rank separately.
  SXM modules need a compatible carrier board, power and cooling.
- **GPU systems**: complete GPU and AI-accelerator systems, including unified-memory machines. Capacity is
  GPU-accessible memory, counted once.
- **CPU**: processor-only prices, excluding RAM and board. Bandwidth assumes every memory channel is populated.
- **DDR memory**: priced DIMMs and kits, with module count and memory type; no compute table. Bandwidth is transfer
  rate × channels; a two-DIMM kit counts as two channels.
- **CPU systems**: complete servers including installed RAM. Capacity is the installed RAM, not the platform maximum.
  Bandwidth follows the installed DIMMs; a server without enough configuration detail appears only in the capacity
  table.
- **Embedded systems**: SoMs, developer kits and boards with included RAM. Module prices may exclude the carrier
  board, storage, cooling and power supply.

## Data and updates

Hardware data lives in [hardware_database.xlsx](hardware_database.xlsx), [data/options.csv](data/options.csv) and
[data/workbook_overrides.csv](data/workbook_overrides.csv). Source links, exact configurations, sellers and
shipping are recorded there. The price research audits are in [data/price_refresh.json](data/price_refresh.json)
and [data/top_ten_expansion.json](data/top_ten_expansion.json).

Regenerate this README after changing data (Python 3.10+):

```sh
make setup
make readme
make check
make test
```

Agents research prices with the [research-hardware](.agents/skills/research-hardware/SKILL.md) skill and update
data with [refresh-readme](.agents/skills/refresh-readme/SKILL.md). Supported stores are listed in the
[store catalog](docs/stores.md). Repository rules are in [AGENTS.md](AGENTS.md).

{{RANKINGS}}
