---
name: research-hardware
description: >-
  Research priced hardware listings for HWDB, verify exact configurations and stock, or assess a store's public price
  retrieval. Use for finding new or used GPU, CPU, DDR, complete-system and embedded options or refreshing their prices.
---

# Research hardware listings

Read the repository [README](../../../README.md) for category definitions and metric conventions.
Then apply the [listing contract](../../../prompts/research-hardware/listings.md), choosing store prompts from the
[tested store catalog](../../../docs/stores.md). Read only the store prompts relevant to the requested category.

Return evidence-backed candidates and rejection reasons. Research is read-only unless the user also requested a
database update. For an update, apply verified observations through the
[README refresh workflow](../refresh-readme/SKILL.md).

For a store-access check, test price, configuration and stock extraction separately. A readable out-of-stock page
proves extraction works but supplies no eligible offer. Update the catalog with the tested URL and limitations when
the user asks to maintain store coverage. During research, also retain newly demonstrated access routes and recurring
failure modes in their owning store prompt and catalog. Update shared contracts and repository guidance when the
finding changes general instructions; keep those rules in one place and link to them.
