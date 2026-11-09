import csv
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/build_readme.py"
SPEC = importlib.util.spec_from_file_location("build_readme", SCRIPT)
build_readme = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_readme
SPEC.loader.exec_module(build_readme)


def option(**changes):
    return replace(build_readme.Option(
        "gpu", "new", "Vendor", "Model", 16, 256, 100,
        "2026-10-18", "Retail", "In stock", "https://example.com/item"
    ), **changes)


class RankingTests(unittest.TestCase):
    def test_rank_by_ratio_with_deterministic_ties_and_limit(self):
        rows = [option(model=str(i), memory_gb=i, price_usd=10) for i in range(1, 13)]
        rows += [option(model="cheap tie", memory_gb=6, price_usd=5)]
        ranked, count = build_readme.top_ten(rows, "gpu", "new", "memory_gb")
        self.assertEqual(count, 13)
        self.assertEqual([o.model for o in ranked], ["cheap tie", "12", "11", "10", "9", "8", "7", "6", "5", "4"])

    def test_missing_metric_only_excludes_affected_ranking(self):
        rows = [option(memory_gb=None), option(model="used", condition="used"),
                option(model="unpriced", price_usd=None)]
        self.assertEqual(build_readme.top_ten(rows, "gpu", "new", "memory_gb")[1], 0)
        self.assertEqual(build_readme.top_ten(rows, "gpu", "new", "bandwidth_gbs")[1], 1)

    def test_unavailable_listings_are_filtered_before_ranking(self):
        statuses = ["Out of stock at vendor", "OUT-OF-STOCK", "Sold; historical reference",
                    "Ended; historical reference", "Unavailable", "Discontinued / rare used",
                    "Sold out", "soldout"]
        rows = [option(model=status, availability=status, price_usd=1) for status in statuses]
        rows += [option(model="sold-price reference", availability="Common used",
                        price_basis="Recent used sold listing", price_usd=1)]
        rows += [option(model="eligible", availability="In stock", price_usd=100)]
        for metric in ("memory_gb", "bandwidth_gbs"):
            ranked, count = build_readme.top_ten(rows, "gpu", "new", metric)
            self.assertEqual(count, 1)
            self.assertEqual([o.model for o in ranked], ["eligible"])

    def test_invalid_numbers_fail_instead_of_distorting_rank(self):
        for value in (0, -1, "nan", "inf", "not a price"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                build_readme.number(value)
        self.assertIsNone(build_readme.number(""))

    def test_duplicates_fail_but_distinct_conditions_are_valid(self):
        with self.assertRaisesRegex(ValueError, "Duplicate option"):
            build_readme.validate_unique([option(), option(vendor="VENDOR")])
        build_readme.validate_unique([option(), option(condition="used")])

    def test_markdown_escaping_and_source_urls(self):
        text = build_readme.render_table(
            [option(model="A|B\n<C>", source="Specs: https://example.com/a_(b)\nPrice: https://example.com/p")],
            "gpu", "new", "memory_gb", "VRAM")
        self.assertIn("A&#124;B &lt;C&gt;", text)
        self.assertIn("[source1](<https://example.com/a_(b)>)", text)

    def test_all_requested_sections_are_flattened(self):
        text = build_readme.render_rankings([])
        self.assertEqual(text.count("### "), 32)
        self.assertEqual(text.count("## GPU Used"), 1)
        self.assertEqual(text.count("## CPU Used"), 1)
        self.assertEqual(len([line for line in text.splitlines() if line.startswith("## ")]), 12)
        self.assertLess(text.index("## DDR memory Used"), text.index("## CPU systems New"))
        self.assertLess(text.index("## CPU systems Used"), text.index("## Embedded systems New"))
        self.assertIn("## Embedded systems New", text)
        self.assertIn("## Embedded systems Used", text)

    def test_csv_invalid_input_has_line_context(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "options.csv"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(option().__dict__))
                writer.writeheader()
                writer.writerow(option(price_usd=-1).__dict__)
            with self.assertRaisesRegex(ValueError, r"options.csv:2:"):
                build_readme.csv_options(path)

    def test_workbook_price_conditions_and_gpu_memory_scope(self):
        rows = build_readme.workbook_options(SCRIPT.parents[1] / "hardware_database.xlsx")
        by_model = {o.model: o for o in rows}
        self.assertEqual(by_model["Radeon RX 6800"].condition, "new")
        self.assertEqual(by_model["EPYC 7742"].condition, "used")
        self.assertEqual(by_model["DGX Station GB300"].memory_gb, 252)
        self.assertEqual(by_model["Orion O6 64GB"].category, "embedded")
        self.assertEqual(by_model["R272-P30; M128-30; 256GB / 24SFF"].category, "cpu_system")

    def test_v100_forms_are_distinct_candidates(self):
        root = SCRIPT.parents[1]
        rows = build_readme.workbook_options(root / "hardware_database.xlsx")
        rows += build_readme.csv_options(root / "data/options.csv")
        variants = {o.model for o in rows if o.category == "gpu" and o.condition == "used"}
        self.assertTrue({
            "Tesla V100 PCIe 16GB", "Tesla V100 PCIe 32GB", "Tesla V100 SXM2 16GB",
            "Tesla V100 SXM2 32GB", "Tesla V100 SXM3 32GB",
            "Tesla V100 PCIe FHHL 16GB (HPE Q8Z50A)", "Tesla V100S PCIe 32GB",
        }.issubset(variants))

    def test_workbook_price_override_supersedes_only_nonempty_fields(self):
        root = SCRIPT.parents[1]
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            (temporary / "data").mkdir()
            (temporary / "hardware_database.xlsx").symlink_to(root / "hardware_database.xlsx")
            with (temporary / "data/workbook_overrides.csv").open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=[
                    "sheet", "model", "category", "condition", "memory_gb", "bandwidth_gbs", "price_usd", "price_date",
                    "price_basis", "availability", "source", "notes",
                ])
                writer.writeheader()
                stream.flush()
                baseline = {o.model: o for o in build_readme.workbook_options(temporary / "hardware_database.xlsx")}
                writer.writerow({"sheet": "GPU", "model": "Tesla M40 24GB", "category": "gpu",
                                 "condition": "used", "price_usd": "139.99", "price_date": "2026-10-22",
                                 "price_basis": "Used eBay asking price", "availability": "3 available",
                                 "source": "https://www.ebay.com/itm/407192112450", "notes": "Shipping extra."})
            rows = build_readme.workbook_options(temporary / "hardware_database.xlsx")
            by_model = {o.model: o for o in rows}
            refreshed = by_model["Tesla M40 24GB"]
            self.assertEqual(refreshed.price_usd, 139.99)
            self.assertEqual(refreshed.price_date, "2026-10-22")
            self.assertEqual(refreshed.price_basis, "Used eBay asking price")
            self.assertEqual(refreshed.availability, "3 available")
            self.assertEqual(refreshed.source, "https://www.ebay.com/itm/407192112450")
            self.assertEqual(refreshed.memory_gb, 24)
            self.assertEqual(refreshed.bandwidth_gbs, 288)
            self.assertIn("Needs forced airflow", refreshed.notes)
            self.assertIn("Shipping extra.", refreshed.notes)
            self.assertEqual(by_model["EPYC 7742"], baseline["EPYC 7742"])

    def write_overrides(self, directory, rows):
        root = SCRIPT.parents[1]
        temporary = Path(directory)
        (temporary / "data").mkdir()
        (temporary / "hardware_database.xlsx").symlink_to(root / "hardware_database.xlsx")
        with (temporary / "data/workbook_overrides.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=[
                "sheet", "model", "category", "condition", "memory_gb", "bandwidth_gbs", "price_usd",
                "price_date", "price_basis", "availability", "source", "notes",
            ], restval="")
            writer.writeheader()
            writer.writerows(rows)
        return temporary / "hardware_database.xlsx"

    def test_override_corrects_bandwidth_and_registers_accelerators(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_overrides(directory, [
                {"sheet": "GPU", "model": "Tesla M40 24GB", "category": "gpu", "condition": "used",
                 "bandwidth_gbs": "300"},
                {"sheet": "Accelerator", "model": "Blackhole p150a", "category": "gpu", "condition": "new"},
            ])
            by_model = {o.model: o for o in build_readme.workbook_options(path)}
        self.assertEqual(by_model["Tesla M40 24GB"].bandwidth_gbs, 300)
        self.assertEqual(by_model["Tesla M40 24GB"].memory_gb, 24)
        self.assertEqual((by_model["Blackhole p150a"].memory_gb, by_model["Blackhole p150a"].bandwidth_gbs), (32, 512))
        self.assertNotIn("Wormhole n300d", by_model)

    def test_unmatched_or_invalid_overrides_fail(self):
        for row, message in (
            ({"sheet": "GPU", "model": "No Such GPU", "category": "gpu", "condition": "new"}, "match no workbook row"),
            ({"sheet": "Nope", "model": "X", "category": "gpu", "condition": "new"}, "Unknown sheet"),
            ({"sheet": "GPU", "model": "Tesla M40 24GB", "category": "tpu", "condition": "new"}, "Unknown category"),
        ):
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(ValueError, message):
                    build_readme.workbook_options(self.write_overrides(directory, [row]))

    def test_tables_follow_metric_and_category_registries(self):
        metrics = build_readme.METRICS + (build_readme.Metric("price_usd", "USD"),)
        categories = {"gpu": build_readme.Category("GPU", {"price_usd": "Cost", "memory_gb": "VRAM"})}
        with patch.object(build_readme, "METRICS", metrics), patch.object(build_readme, "CATEGORIES", categories):
            text = build_readme.render_rankings([option()])
        headings = [line for line in text.splitlines() if line.startswith("### ")]
        self.assertEqual(headings, ["### VRAM per $", "### Cost per $"] * 2)
        self.assertIn("| Rank | Option | USD | Price | USD/$ |", text)

    def test_tops_table_shows_type_and_requires_it(self):
        row = option(tops=100, tops_type="NVFP4", tops_source="https://example.com/spec")
        text = build_readme.render_table([row], "gpu", "new", "tops", "TOPS")
        self.assertIn("| Rank | Option | TOPS | Type | Price | TOPS/$ | Sources |", text)
        self.assertIn("| 100.00 | NVFP4 | $100 | 1.0000 |", text)
        self.assertIn("(<https://example.com/spec>)", text)
        self.assertNotIn("Type", build_readme.render_table([row], "gpu", "new", "memory_gb", "VRAM"))
        with self.assertRaisesRegex(ValueError, "must be set together"):
            build_readme.render_rankings([option(tops=100)])

    def test_ddr_tables_show_modules_and_type(self):
        kit = option(category="ddr", model="Kit", modules="2", memory_type="DDR4-3200")
        text = build_readme.render_table([kit], "ddr", "new", "memory_gb", "RAM")
        self.assertIn("| Rank | Option | Modules | Type | GB | Price | GB/$ | Sources |", text)
        self.assertIn("| Vendor Kit | 2 | DDR4-3200 | 16.00 |", text)
        self.assertNotIn("Modules", build_readme.render_table([option()], "gpu", "new", "memory_gb", "VRAM"))
        with self.assertRaisesRegex(ValueError, "missing memory_type"):
            build_readme.render_rankings([option(category="ddr", modules="2")])

    def test_prices_round_to_whole_dollars(self):
        self.assertEqual([build_readme.dollars(v) for v in (498.75, 200.5, 179.49, 17499.95)],
                         ["$499", "$201", "$179", "$17,500"])

    def test_check_detects_stale_readme_without_overwriting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "README.md"
            destination.write_text("Old README\n")
            with patch.object(build_readme, "ROOT", root), \
                    patch.object(build_readme, "build", return_value="New README\n"), \
                    patch.object(sys, "argv", ["build_readme.py", "--check"]), \
                    redirect_stderr(io.StringIO()):
                self.assertEqual(build_readme.main(), 1)
            self.assertEqual(destination.read_text(), "Old README\n")
            destination.write_text("New README\n")
            with patch.object(build_readme, "ROOT", root), \
                    patch.object(build_readme, "build", return_value="New README\n"), \
                    patch.object(sys, "argv", ["build_readme.py", "--check"]), \
                    redirect_stdout(io.StringIO()):
                self.assertEqual(build_readme.main(), 0)


if __name__ == "__main__":
    unittest.main()
