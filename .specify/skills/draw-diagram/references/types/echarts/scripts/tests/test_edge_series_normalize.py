"""Positive/negative cases for references/types/echarts/scripts/normalize-edge-series.py.

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

SCRIPT = Path(__file__).resolve().parents[1] / "normalize-edge-series.py"


class NormalizeCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_option(self, name, data):
        path = self.root / f"{name}.option.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def run_cli(self, args, **kwargs):
        return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True, timeout=120, **kwargs)

    def test_clean_option_has_no_drift(self):
        path = self.write_option("clean", fixtures.option())
        completed = self.run_cli(["--check", "--source", str(path)])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["mutations"], [])

    def test_rotation_drift_is_detected_and_repaired(self):
        def mutate(data):
            for item in data["series"][2]["data"]:
                if item["semanticId"] == "r1":
                    item["symbolRotate"] = 90
        path = self.write_option("rotated", fixtures.mutate_option(mutate))
        checked = self.run_cli(["--check", "--source", str(path)])
        self.assertEqual(checked.returncode, 1)
        payload = json.loads(checked.stdout)
        kinds = [mutation["kind"] for mutation in payload["mutations"]]
        self.assertIn("arrow-rotation", kinds)
        output = self.root / "rotated.fixed.json"
        written = self.run_cli(["--write", "--source", str(path), "--output", str(output)])
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        again = self.run_cli(["--check", "--source", str(output)])
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)

    def test_degenerate_final_segment_is_repaired(self):
        def mutate(data):
            for item in data["series"][1]["data"]:
                if item["semanticId"] == "r2":
                    item["coords"] = [[210, 85], [210, 110], [450, 110], [450, 104], [450, 105]]
            for item in data["series"][2]["data"]:
                if item["semanticId"] == "r2":
                    item["symbolRotate"] = 0
        path = self.write_option("degenerate", fixtures.mutate_option(mutate))
        checked = self.run_cli(["--check", "--source", str(path)])
        self.assertEqual(checked.returncode, 1)
        payload = json.loads(checked.stdout)
        kinds = [mutation["kind"] for mutation in payload["mutations"]]
        self.assertIn("final-segment", kinds)
        output = self.root / "degenerate.fixed.json"
        written = self.run_cli(["--write", "--source", str(path), "--output", str(output)])
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        repaired = json.loads(output.read_text(encoding="utf-8"))
        coords = next(item["coords"] for item in repaired["series"][1]["data"] if item["semanticId"] == "r2")
        self.assertGreater(coords[-1][1], 99.0)
        self.assertLess(coords[-1][1], 104.0)
        again = self.run_cli(["--check", "--source", str(output)])
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)

    def test_detached_label_is_snapped(self):
        def mutate(data):
            for item in data["series"][3]["data"]:
                if item["semanticId"] == "r2":
                    item["value"] = [330, 140]
        path = self.write_option("label", fixtures.mutate_option(mutate))
        checked = self.run_cli(["--check", "--source", str(path)])
        self.assertEqual(checked.returncode, 1)
        payload = json.loads(checked.stdout)
        kinds = [mutation["kind"] for mutation in payload["mutations"]]
        self.assertIn("label-anchor", kinds)
        output = self.root / "label.fixed.json"
        written = self.run_cli(["--write", "--source", str(path), "--output", str(output)])
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        repaired = json.loads(output.read_text(encoding="utf-8"))
        point = next(item["value"] for item in repaired["series"][3]["data"] if item["semanticId"] == "r2")
        self.assertAlmostEqual(point[1], 110.0, places=2)

    def test_write_refuses_existing_output_and_source_overwrite(self):
        path = self.write_option("refuse", fixtures.option())
        existing = self.root / "existing.json"
        existing.write_text("{}", encoding="utf-8")
        completed = self.run_cli(["--write", "--source", str(path), "--output", str(existing)])
        self.assertEqual(completed.returncode, 2)
        same = self.run_cli(["--write", "--source", str(path), "--output", str(path)])
        self.assertEqual(same.returncode, 2)

    def test_served_html_source_is_supported(self):
        html = self.root / "served.html"
        html.write_text(fixtures.served_html(fixtures.option()), encoding="utf-8")
        completed = self.run_cli(["--check", "--source", str(html)])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["source"]["format"], "served-html")

    def test_unknown_and_missing_arguments(self):
        self.assertEqual(self.run_cli(["--help-extra"]).returncode, 2)
        self.assertEqual(self.run_cli(["--check"]).returncode, 2)
        path = self.write_option("args", fixtures.option())
        self.assertEqual(self.run_cli(["--write", "--source", str(path)]).returncode, 2)
        self.assertEqual(self.run_cli(["--check", "--source", str(path), "--output", str(self.root / "x.json")]).returncode, 2)
        help_run = self.run_cli(["--help"])
        self.assertEqual(help_run.returncode, 0)
        version_run = self.run_cli(["--version"])
        self.assertEqual(version_run.returncode, 0)
        self.assertIn("normalize-edge-series.py", version_run.stdout)

    def test_missing_arrow_pair_is_not_applicable(self):
        def mutate(data):
            data["series"] = [series for series in data["series"] if series.get("id") != "edge-arrows"]
        path = self.write_option("no-arrows", fixtures.mutate_option(mutate))
        completed = self.run_cli(["--check", "--source", str(path)])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "not_applicable")


if __name__ == "__main__":
    unittest.main()
