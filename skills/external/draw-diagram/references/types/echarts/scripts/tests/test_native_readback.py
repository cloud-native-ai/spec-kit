"""Positive/negative cases for references/types/echarts/scripts/native-readback.py.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/references/types/echarts/scripts/tests/ -q
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fixtures

SCRIPT = Path(__file__).resolve().parents[1] / "native-readback.py"


class ReadbackCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "semantics.json").write_text(json.dumps(fixtures.semantics()), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def run_readback(self, option_data, svg_text=None, name="case"):
        source = self.root / f"{name}.option.json"
        source.write_text(json.dumps(option_data, ensure_ascii=False), encoding="utf-8")
        svg_path = None
        if svg_text is not None:
            svg_path = self.root / f"{name}.svg"
            svg_path.write_text(svg_text, encoding="utf-8")
        output = self.root / f"{name}.report.json"
        command = [
            sys.executable, str(SCRIPT),
            "--source", str(source),
            "--semantics", str(self.root / "semantics.json"),
            "--output", str(output),
        ]
        if svg_path is not None:
            command += ["--svg", str(svg_path)]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=120)
        report = json.loads(output.read_text(encoding="utf-8")) if output.exists() else None
        return completed, report

    def test_positive_native_passes(self):
        completed, report = self.run_readback(fixtures.option())
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(report["semantic"]["status"], "pass")
        self.assertEqual(report["visual"]["status"], "pass", report["visual"]["issues"])
        self.assertEqual(report["overall"], "pass")
        self.assertEqual(report["visual"]["crossings"]["count"], 0)
        ids = [node["id"] for node in report["actual"]["nodes"]]
        self.assertIn("a1", ids)
        zones = {node["id"]: node["zone"] for node in report["actual"]["nodes"] if node["id"]}
        self.assertEqual(zones["a1"], "zA")

    def test_positive_with_rendered_svg_passes(self):
        completed, report = self.run_readback(fixtures.option(), fixtures.svg())
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(report["visual"]["status"], "pass", report["visual"]["issues"])
        svg = report["visual"]["svg"]
        self.assertEqual(svg["texts"]["missingTotal"], 0)
        self.assertEqual(svg["texts"]["extraTotal"], 0)
        self.assertEqual(svg["arrowCount"], 3)
        self.assertEqual(svg["identity"]["status"], "partial")

    def test_served_html_source_is_supported(self):
        html = fixtures.served_html(fixtures.option())
        source_name = "served"
        path = self.root / f"{source_name}.html"
        path.write_text(html, encoding="utf-8")
        output = self.root / "served.report.json"
        completed = subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--source", str(path),
                "--semantics", str(self.root / "semantics.json"),
                "--output", str(output),
            ],
            capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["source"]["format"], "served-html")
        self.assertEqual(report["semantic"]["status"], "pass")

    def test_category_index_membership_mutation_fails(self):
        def mutate(data):
            for node in data["series"][0]["data"]:
                if node.get("id") == "b1":
                    node["category"] = 0
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "membership")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["element_zone_mismatches"])
        self.assertEqual(report["semantic"]["status"], "fail")

    def test_node_id_mutation_fails(self):
        def mutate(data):
            for node in data["series"][0]["data"]:
                if node.get("id") == "b2":
                    node["id"] = "b2-renamed"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "node-id")
        self.assertEqual(completed.returncode, 1)
        self.assertIn("b2", report["semantic"]["diffs"]["missing_element_ids"])
        self.assertIn("b2-renamed", report["semantic"]["diffs"]["extra_element_ids"])

    def test_parent_mutation_fails(self):
        def mutate(data):
            for category in data["series"][0]["categories"]:
                if category["zoneId"] == "zC":
                    category["parent"] = None
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "parent")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["zone_parent_mismatches"])

    def test_reversed_relation_fails(self):
        def mutate(data):
            for item in data["series"][1]["data"]:
                if item["semanticId"] == "r2":
                    item["srcId"], item["dstId"] = item["dstId"], item["srcId"]
            for item in data["series"][0]["links"]:
                if item.get("semanticId") == "r2":
                    item["source"], item["target"] = item["target"], item["source"]
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "reversed")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["relation_direction_mismatches"])

    def test_label_mutation_fails(self):
        def mutate(data):
            for item in data["series"][3]["data"]:
                if item["semanticId"] == "r2":
                    item["name"] = "invokes"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "label")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["relation_label_mismatches"])

    def test_duplicate_ids_fail(self):
        def mutate(data):
            for node in data["series"][0]["data"]:
                if node.get("id") == "b2":
                    node["id"] = "b1"
                    node["name"] = "Gamma"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "duplicate")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["duplicate_element_ids"])

    def test_relation_color_mutation_fails(self):
        def mutate(data):
            for item in data["series"][1]["data"]:
                if item["semanticId"] == "r2":
                    item["lineStyle"]["color"] = "#123456"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "color")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["relation_color_mismatches"])

    def test_extra_legend_color_meaning_fails(self):
        def mutate(data):
            data["legend"]["data"].append("#aa0000 = ingest path")
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "legend")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["legend_color_semantics"])

    def test_container_endpoint_expansion_fails(self):
        def mutate(data):
            for node in data["series"][0]["data"]:
                if node.get("id") == "b2":
                    node["category"] = 2
            for item in data["series"][1]["data"]:
                if item["semanticId"] == "r3":
                    item["dstId"] = "b2"
            for item in data["series"][2]["data"]:
                if item["semanticId"] == "r3":
                    item["dstId"] = "b2"
            for item in data["series"][0]["links"]:
                if item.get("semanticId") == "r3":
                    item["target"] = "b2"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "container")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["expanded_container_endpoints"])
        self.assertTrue(report["semantic"]["diffs"]["relation_endpoint_mismatches"])

    def test_flipped_arrow_fails_without_svg(self):
        def mutate(data):
            for item in data["series"][2]["data"]:
                if item["semanticId"] == "r1":
                    item["symbolRotate"] = 90
        completed, report = self.run_readback(fixtures.mutate_option(mutate), None, "rot-native")
        self.assertEqual(completed.returncode, 1)
        kinds = [issue["kind"] for issue in report["visual"]["issues"]]
        self.assertIn("arrow-direction", kinds)
        self.assertIn("arrow-tip-off-target", kinds)

    def test_flipped_arrow_fails_from_svg(self):
        completed, report = self.run_readback(
            fixtures.option(), fixtures.svg_with_arrow_mutated("r1", 90), "rot-svg"
        )
        self.assertEqual(completed.returncode, 1)
        kinds = [issue["kind"] for issue in report["visual"]["issues"]]
        self.assertIn("arrow-direction", kinds)

    def test_svg_missing_label_fails(self):
        completed, report = self.run_readback(fixtures.option(), fixtures.svg_without_label("calls"), "text-missing")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["visual"]["svg"]["texts"]["missingTotal"] >= 1)

    def test_unsupported_symbol_is_partial(self):
        def mutate(data):
            for series in data["series"]:
                if series.get("id") == "edge-arrows":
                    series["symbol"] = "arrow"
                    for item in series["data"]:
                        item.pop("symbol", None)
        completed, report = self.run_readback(fixtures.mutate_option(mutate), None, "unsupported")
        self.assertEqual(completed.returncode, 3, completed.stdout + completed.stderr)
        self.assertEqual(report["overall"], "partial")

    def test_endpoint_identity_forms_pass(self):
        def mutate(data):
            for link in data["series"][0]["links"]:
                if link["semanticId"] == "r1":
                    link["source"] = 0
                    link["target"] = 1
                if link["semanticId"] == "r2":
                    link["target"] = "Gamma"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "identity-forms")
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(report["semantic"]["diffs"]["graph_link_endpoint_mismatches"], [])

    def test_ambiguous_name_endpoint_is_partial(self):
        def mutate(data):
            for link in data["series"][0]["links"]:
                if link["semanticId"] == "r1":
                    link["target"] = "Beta"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "ambiguous")
        self.assertEqual(completed.returncode, 3, completed.stdout + completed.stderr)
        self.assertEqual(report["overall"], "partial")
        self.assertTrue(report["unsupported"])

    def test_graph_link_mismatch_fails(self):
        def mutate(data):
            for link in data["series"][0]["links"]:
                if link["semanticId"] == "r2":
                    link["target"] = "b2"
        completed, report = self.run_readback(fixtures.mutate_option(mutate), fixtures.svg(), "link-mismatch")
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(report["semantic"]["diffs"]["graph_link_endpoint_mismatches"])

    def test_refuses_overwrite_and_unknown_flags(self):
        source = self.root / "overwrite.option.json"
        source.write_text(json.dumps(fixtures.option()), encoding="utf-8")
        output = self.root / "existing.json"
        output.write_text("{}", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--source", str(source),
             "--semantics", str(self.root / "semantics.json"), "--output", str(output)],
            capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(completed.returncode, 2)
        unknown = subprocess.run(
            [sys.executable, str(SCRIPT), "--help-extra"],
            capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(unknown.returncode, 2)
        help_run = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True, timeout=60)
        self.assertEqual(help_run.returncode, 0)
        version_run = subprocess.run([sys.executable, str(SCRIPT), "--version"], capture_output=True, text=True, timeout=60)
        self.assertEqual(version_run.returncode, 0)
        self.assertIn("native-readback.py", version_run.stdout)


if __name__ == "__main__":
    unittest.main()
