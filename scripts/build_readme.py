#!/usr/bin/env python3
"""Assemble README rankings from workbook input columns and supplemental CSV rows."""

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime, timezone
from math import isfinite
from pathlib import Path
import re
import sys

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "gpu": ("GPU", "VRAM", ("new", "used")),
    "cpu": ("CPU", None, ("new", "used")),
    "gpu_system": ("GPU system", "VRAM", ("new", "used")),
    "ddr": ("DDR memory", "RAM", ("new", "used")),
    "cpu_system": ("CPU systems", "RAM", ("new", "used")),
    "embedded": ("Embedded systems", "RAM", ("new", "used")),
}


@dataclass(frozen=True)
class Option:
    category: str
    condition: str
    vendor: str
    model: str
    memory_gb: float | None
    bandwidth_gbs: float | None
    price_usd: float | None
    price_date: str
    price_basis: str
    availability: str
    source: str
    notes: str = ""

    @property
    def name(self):
        return f"{self.vendor} {self.model}".strip()


def number(value):
    if value is None or value == "":
        return None
    result = float(value)
    if not isfinite(result) or result <= 0:
        raise ValueError(f"Expected a positive finite number, got {value!r}")
    return result


def date_text(value):
    if isinstance(value, (datetime, date)):
        return value.date().isoformat() if isinstance(value, datetime) else value.isoformat()
    if value is None or value == "":
        return ""
    return date.fromisoformat(str(value)).isoformat()


def worksheet_records(sheet):
    """Find the header by its labels, ignoring titles, notes and trailing blanks."""
    rows = iter(sheet.values)
    for row in rows:
        if "Vendor" in row and "Price (USD)" in row:
            headers = row
            break
    else:
        raise ValueError(f"{sheet.title}: missing Vendor / Price (USD) header")
    for row in rows:
        record = dict(zip(headers, row))
        if record.get("Vendor"):
            yield record


def workbook_options(path):
    with (path.parent / "data/workbook_overrides.csv").open(newline="", encoding="utf-8") as stream:
        overrides = {}
        for row in csv.DictReader(stream):
            key = (row["sheet"], row["model"])
            if key in overrides:
                raise ValueError(f"Duplicate workbook override: {key}")
            if row["category"] not in CATEGORIES or row["condition"] not in ("new", "used"):
                raise ValueError(f"Invalid category or condition in workbook override: {key}")
            overrides[key] = row
    workbook = load_workbook(path, data_only=True, read_only=True)
    options = []
    try:
        for sheet_name in ("GPU", "CPU", "SoM", "Platform"):
            for row in worksheet_records(workbook[sheet_name]):
                category, model_field, memory_field = {
                    "GPU": ("gpu", "Model", "Memory (GB)"),
                    "CPU": ("cpu", "Model", "Max memory (GB)"),
                    "SoM": ("embedded", "Module", "Max memory (GB)"),
                    "Platform": ("gpu_system", "System", "Total memory (GB)"),
                }[sheet_name]
                model = row[model_field]
                override = overrides.get((sheet_name, model))
                if override:
                    # Refresh price observations without rewriting the baseline workbook.
                    for field, column in {
                        "price_usd": "Price (USD)", "price_date": "Price date",
                        "price_basis": "Price basis", "availability": "Availability",
                        "source": "Source",
                    }.items():
                        if override.get(field):
                            row[column] = override[field]
                    if override.get("notes"):
                        row["Notes"] = " ".join(filter(None, [row.get("Notes"), override["notes"]]))
                bandwidth_field = "Peak bandwidth (GB/s)"
                if sheet_name == "Platform":
                    bandwidth_field = "Peak / aggregate bandwidth (GB/s)"
                    if override is None:
                        continue  # Only explicitly categorized platforms are ranked.
                # Condition describes this price, not the product's availability.
                basis = str(row.get("Price basis") or "")
                condition = "used" if re.search(r"\bused\b|refurb", basis, re.I) else "new"
                memory = row.get(memory_field)
                notes = str(row.get("Notes") or "")
                if override:
                    category = override["category"]
                    condition = override["condition"]
                    if override["memory_gb"]:
                        memory = override["memory_gb"]
                options.append(Option(
                    category, condition, str(row["Vendor"]), str(model),
                    number(memory), number(row.get(bandwidth_field)),
                    number(row.get("Price (USD)")), date_text(row.get("Price date")),
                    basis, str(row.get("Availability") or ""),
                    str(row.get("Source") or ""), notes,
                ))
    finally:
        workbook.close()
    return options


def csv_options(path):
    with path.open(newline="", encoding="utf-8") as stream:
        result = []
        for line, row in enumerate(csv.DictReader(stream), 2):
            try:
                if row["category"] not in CATEGORIES:
                    raise ValueError(f"Unknown category {row['category']!r}")
                if row["condition"] not in ("new", "used"):
                    raise ValueError(f"Unknown condition {row['condition']!r}")
                for field in ("vendor", "model", "price_basis", "source"):
                    if not row[field].strip():
                        raise ValueError(f"Missing {field}")
                result.append(Option(
                    row["category"], row["condition"], row["vendor"], row["model"],
                    number(row["memory_gb"]), number(row["bandwidth_gbs"]),
                    number(row["price_usd"]), date_text(row["price_date"]),
                    row["price_basis"], row["availability"], row["source"], row["notes"],
                ))
            except (ValueError, KeyError) as error:
                raise ValueError(f"{path}:{line}: {error}") from error
    return result


def validate_unique(options):
    seen = set()
    for option in options:
        key = (option.category, option.condition, option.vendor.casefold(), option.model.casefold())
        if key in seen:
            raise ValueError(f"Duplicate option: {option.category}/{option.condition}/{option.name}")
        seen.add(key)


def is_available(option):
    status = re.sub(r"[-–—_]+", " ", f"{option.availability} {option.price_basis}".casefold())
    return not re.search(r"\bout\s+of\s+stock\b|\bsold\b|\bsoldout\b|\bended\b|"
                         r"\bunavailable\b|\bdiscontinued\b", status)


def top_ten(options, category, condition, metric):
    candidates = [o for o in options if o.category == category and o.condition == condition
                  and is_available(o) and o.price_usd is not None and getattr(o, metric) is not None]
    return sorted(candidates, key=lambda o: (
        -getattr(o, metric) / o.price_usd, o.price_usd, o.name.casefold()
    ))[:10], len(candidates)


def escape(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(
        ">", "&gt;").replace("|", "&#124;").replace("\n", " ").replace("\r", " ")


def source_links(source):
    urls = list(dict.fromkeys(re.findall(r"https?://[^\s]+", source)))
    return ", ".join(f"[source{index if len(urls) > 1 else ''}](<{url}>)"
                     for index, url in enumerate(urls, 1)) or "—"


def render_table(options, category, condition, metric, label):
    top, count = top_ten(options, category, condition, metric)
    unit = "GB" if metric == "memory_gb" else "GB/s"
    lines = [f"### {label} per $", ""]
    if count < 10:
        lines += [f"Coverage: {count} qualifying option{'s' if count != 1 else ''} after availability filtering; fewer than ten recorded.", ""]
    lines += [f"| Rank | Option | {unit} | Price (USD) | {unit}/$ | Availability | Sources |",
              "| ---: | --- | ---: | ---: | ---: | --- | --- |"]
    for rank, option in enumerate(top, 1):
        value = getattr(option, metric)
        lines.append(f"| {rank} | {escape(option.name)} | {value:,.2f} | ${option.price_usd:,.2f} | "
                     f"{value / option.price_usd:.4f} | {escape(option.availability) or '—'} | "
                     f"{source_links(option.source)} |")
    if not top:
        lines += ["", "No qualifying options recorded."]
    return "\n".join(lines)


def render_rankings(options, updated_at=None):
    validate_unique(options)
    if updated_at is None:
        updated_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    lines = ["<!-- Generated by scripts/build_readme.py. Edit source data, not these tables. -->",
             "", f"Last updated: {updated_at}"]
    for category, (title, capacity_label, conditions) in CATEGORIES.items():
        for condition in conditions:
            lines += ["", f"## {title} {condition.title()}", ""]
            if capacity_label:
                lines += [render_table(options, category, condition, "memory_gb", capacity_label), ""]
            lines += [render_table(options, category, condition, "bandwidth_gbs", "Bandwidth")]
    return "\n".join(lines)


def build(root, updated_at=None):
    options = workbook_options(root / "hardware_database.xlsx") + csv_options(root / "data/options.csv")
    template = (root / "docs/README.template.md").read_text(encoding="utf-8")
    if template.count("{{RANKINGS}}") != 1:
        raise ValueError("README template must contain exactly one {{RANKINGS}} marker")
    return template.replace("{{RANKINGS}}", render_rankings(options, updated_at)).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if README.md needs regeneration")
    args = parser.parse_args()
    try:
        destination = ROOT / "README.md"
        updated_at = None
        if args.check and destination.exists():
            match = re.search(r"^Last updated: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$",
                              destination.read_text(encoding="utf-8"), re.MULTILINE)
            if match:
                updated_at = match.group(1)
        rendered = build(ROOT, updated_at=updated_at)
        if args.check:
            if not destination.exists() or destination.read_text(encoding="utf-8") != rendered:
                print("README.md is out of date; run make readme", file=sys.stderr)
                return 1
            print("README.md is up to date")
        else:
            destination.write_text(rendered, encoding="utf-8")
            print("Generated README.md")
    except (ValueError, KeyError, OSError) as error:
        print(f"Cannot generate README: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
