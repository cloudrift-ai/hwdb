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
CONDITIONS = ("new", "used")


@dataclass(frozen=True)
class Metric:
    field: str
    unit: str


# Ranked metrics in table order. Each is an Option field, an optional CSV column and an optional workbook column.
METRICS = (
    Metric("memory_gb", "GB"),
    Metric("bandwidth_gbs", "GB/s"),
)


@dataclass(frozen=True)
class Category:
    title: str
    tables: dict[str, str]  # metric field -> table label; a missing metric gets no table


CATEGORIES = {
    "gpu": Category("GPU", {"memory_gb": "VRAM", "bandwidth_gbs": "Bandwidth"}),
    "cpu": Category("CPU", {"bandwidth_gbs": "Bandwidth"}),
    "gpu_system": Category("GPU system", {"memory_gb": "VRAM", "bandwidth_gbs": "Bandwidth"}),
    "ddr": Category("DDR memory", {"memory_gb": "RAM", "bandwidth_gbs": "Bandwidth"}),
    "cpu_system": Category("CPU systems", {"memory_gb": "RAM", "bandwidth_gbs": "Bandwidth"}),
    "embedded": Category("Embedded systems", {"memory_gb": "RAM", "bandwidth_gbs": "Bandwidth"}),
}


@dataclass(frozen=True)
class Sheet:
    category: str | None  # None: rank only rows registered in workbook_overrides.csv
    model_column: str
    metric_columns: dict[str, str]


SHEETS = {
    "GPU": Sheet("gpu", "Model", {"memory_gb": "Memory (GB)", "bandwidth_gbs": "Peak bandwidth (GB/s)"}),
    "CPU": Sheet("cpu", "Model", {"memory_gb": "Max memory (GB)", "bandwidth_gbs": "Peak bandwidth (GB/s)"}),
    "SoM": Sheet("embedded", "Module",
                 {"memory_gb": "Max memory (GB)", "bandwidth_gbs": "Peak bandwidth (GB/s)"}),
    "Platform": Sheet(None, "System", {"memory_gb": "Total memory (GB)",
                                       "bandwidth_gbs": "Peak / aggregate bandwidth (GB/s)"}),
    "Accelerator": Sheet(None, "Model", {"memory_gb": "Memory (GB)", "bandwidth_gbs": "Peak bandwidth (GB/s)"}),
}

# Override fields that replace a workbook price observation when nonempty.
PRICE_OVERRIDES = {
    "price_usd": "Price (USD)", "price_date": "Price date", "price_basis": "Price basis",
    "availability": "Availability", "source": "Source",
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


def validate_class(category, condition):
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category {category!r}")
    if condition not in CONDITIONS:
        raise ValueError(f"Unknown condition {condition!r}")


def read_overrides(path):
    overrides = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for line, row in enumerate(csv.DictReader(stream), 2):
            key = (row["sheet"], row["model"])
            try:
                if key in overrides:
                    raise ValueError(f"Duplicate workbook override {key}")
                if row["sheet"] not in SHEETS:
                    raise ValueError(f"Unknown sheet {row['sheet']!r}")
                validate_class(row["category"], row["condition"])
            except ValueError as error:
                raise ValueError(f"{path}:{line}: {error}") from error
            overrides[key] = row
    return overrides


def workbook_options(path):
    overrides = read_overrides(path.parent / "data/workbook_overrides.csv")
    workbook = load_workbook(path, data_only=True, read_only=True)
    options, matched = [], set()
    try:
        for sheet_name, sheet in SHEETS.items():
            for row in worksheet_records(workbook[sheet_name]):
                model = row[sheet.model_column]
                override = overrides.get((sheet_name, model))
                if override is None and sheet.category is None:
                    continue  # Only explicitly categorized rows from this sheet are ranked.
                metrics = {field: row.get(column) for field, column in sheet.metric_columns.items()}
                # Condition describes this price, not the product's availability.
                basis = str(row.get("Price basis") or "")
                category = sheet.category
                condition = "used" if re.search(r"\bused\b|refurb", basis, re.I) else "new"
                notes = str(row.get("Notes") or "")
                if override:
                    matched.add((sheet_name, model))
                    category, condition = override["category"], override["condition"]
                    # Refresh price observations and correct metrics without rewriting the baseline workbook.
                    for field, column in PRICE_OVERRIDES.items():
                        if override.get(field):
                            row[column] = override[field]
                    basis = str(row.get("Price basis") or "")
                    for metric in METRICS:
                        if override.get(metric.field):
                            metrics[metric.field] = override[metric.field]
                    notes = " ".join(filter(None, [notes, override.get("notes")]))
                options.append(Option(
                    category=category, condition=condition, vendor=str(row["Vendor"]), model=str(model),
                    price_usd=number(row.get("Price (USD)")), price_date=date_text(row.get("Price date")),
                    price_basis=basis, availability=str(row.get("Availability") or ""),
                    source=str(row.get("Source") or ""), notes=notes,
                    **{metric.field: number(metrics.get(metric.field)) for metric in METRICS},
                ))
    finally:
        workbook.close()
    if unmatched := sorted(set(overrides) - matched):
        raise ValueError(f"Workbook overrides match no workbook row: {unmatched}")
    return options


def csv_options(path):
    with path.open(newline="", encoding="utf-8") as stream:
        result = []
        for line, row in enumerate(csv.DictReader(stream), 2):
            try:
                validate_class(row["category"], row["condition"])
                for field in ("vendor", "model", "price_basis", "source"):
                    if not row[field].strip():
                        raise ValueError(f"Missing {field}")
                result.append(Option(
                    category=row["category"], condition=row["condition"], vendor=row["vendor"],
                    model=row["model"], price_usd=number(row["price_usd"]),
                    price_date=date_text(row["price_date"]), price_basis=row["price_basis"],
                    availability=row["availability"], source=row["source"], notes=row["notes"],
                    **{metric.field: number(row.get(metric.field)) for metric in METRICS},
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
    unit = next(m.unit for m in METRICS if m.field == metric)
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
    for key, category in CATEGORIES.items():
        for condition in CONDITIONS:
            tables = [render_table(options, key, condition, metric.field, category.tables[metric.field])
                      for metric in METRICS if metric.field in category.tables]
            lines += ["", f"## {category.title} {condition.title()}", "", "\n\n".join(tables)]
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
