---
name: refresh-readme
description: >-
  Update HWDB source tables and regenerate its README rankings, or rebuild and verify the README after data or prose
  changes. Use when adding researched hardware, refreshing recorded prices, or changing ranking presentation.
---

# Refresh HWDB rankings

Apply [the refresh contract](../../../prompts/refresh-readme.md). It owns input selection, evidence checks,
generation and verification. Read the [README](../../../README.md) for the current data schema and category rules.

When the request includes finding or rechecking prices, first use
[research-hardware](../research-hardware/SKILL.md). A rebuild alone does not require network research and must not
advance individual price observation dates.
