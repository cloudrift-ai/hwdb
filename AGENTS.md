# AGENTS.md

HWDB compares hardware memory capacity and theoretical memory bandwidth per US dollar.
Read `README.md` first; it is the project overview and index for data, workflows and store research.

## Communication

Answer first, use plain technical English, and report material findings and verification concisely.
Distinguish advertised specifications, theoretical calculations and measured performance.

## Data and generated files

- `hardware_database.xlsx` and `data/options.csv` are hardware inputs. Preserve unrelated workbook changes.
  Files under `outputs/` are historical artifacts, not the active database.
- `data/workbook_overrides.csv` classifies selected workbook platforms and corrects explicit memory/condition fields.
  It also owns current price observations for existing workbook rows; nonempty price fields supersede workbook values.
  Use it for price-only refreshes that should preserve the baseline workbook and unrelated user changes.
- `docs/README.template.md` owns README prose. Generate `README.md` with `make readme`; do not edit its tables by hand.
- `data/price_refresh.json` records the latest non-GPU refresh outcomes and evidence, including excluded rows.
  Account for every requested source row: verify an exact current offer or explicitly mark it unavailable for ranking.
  Preserve its historical price/date when no replacement is verified; never infer worldwide stock from a failed search.
- Keep price dates and price bases in source data. The README has one generation timestamp for all rankings,
  with no per-row price-date or price-basis columns.
- Preserve the flat New/Used sections and top-ten rankings, including CPU systems after DDR and used embedded systems.
  Keep PCIe, SXM, memory sizes and adapter bundles distinct. CPU prices exclude RAM; CPU systems include installed RAM.

The README owns the detailed category definitions and bandwidth conventions. Follow them rather than maintaining
another copy here. Leave unknown metrics empty and report insufficient coverage instead of inventing entries.

## Research and prompts

Use the repository skills for hardware research and README refreshes. Skills live in `.agents/skills/`; shared task
contracts live in `prompts/`. Store-specific retrieval instructions extend the shared listing contract.
The README links to their entry points and the tested store catalog.

Accept a new shopping observation only when the exact configuration, price, currency, condition and available stock
can be established from the retrieved listing. Exclude out-of-stock, sold, ended, unavailable and discontinued offers.
A search snippet, launch MSRP or cached listing alone does not establish current availability. Preserve historical
references honestly; do not silently relabel them as current retail offers.
For current prices, prefer live item pages or a current-inventory API. Check explicit stock banners and delivery
eligibility as well as purchase controls: filtered search can retain out-of-stock and pickup-only offers. Keep item
price separate from shipping and delivered cost. Use multiple sellers before describing an offer as a market estimate.

Keep rules with one owner: general repository rules here, workflow routing in skills, task contracts in prompts,
and store access findings in the store catalog. Add provider-specific agent wrappers only when an actual runner needs
them; wrappers should reference shared prompts rather than copy their instructions.
When research reveals a repeatable retrieval issue or a better working route, update the owning store prompt and
catalog during that task. Update shared prompts, affected skills and this file when their guidance changes; update
README prose through its template. Keep examples dated and distinguish tested behavior from untested API proposals.
Exact SKU suffixes, kit quantities, CPU sample/lock status and installed system RAM matter. Read item specifics or
seller configuration details when the title is ambiguous; a matching search query does not establish a matching SKU.

## Verification

Run `make readme` after changing data or README prose, then `make check`. Run `make test` for generator changes and
data changes that exercise parsing or classification. Validate changed skills with the skill-creator validator when
available, and check local Markdown links after reorganizing prompts.

Keep edits scoped to the requested work. Wrap prose at about 120 characters; tables and long URLs may exceed it.
