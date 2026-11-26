"""Positive/negative cases for references/types/d3js/scripts/build-native.py.

Covers the generation-layer contract:
- deterministic output; one and only one executable data script (no escaped duplicate);
- vendor-first D3 loading with zero external URL dependencies;
- generated HTML validates semantically through native-readback.py;
- overwrite refusal, invalid SDS/plan refusal and the CLI interface;
- label placement reports no fallback / collisions on a roomy fixture;
- reusable sources contain no private business data, user paths or server addresses.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/references/types/d3js/scripts/tests/test_build_native.py -q
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
BUILD = SCRIPTS / "build-native.py"
READBACK = SCRIPTS / "native-readback.py"
ENGINE = SCRIPTS.parent
VIEWER_JS = ENGINE / "assets" / "viewer.js"
VIEWER_CSS = ENGINE / "assets" / "viewer.css"


def sds():
    return {
        "title": "Synthetic Test Graph",
        "diagram_class": "topology",
        "engine": "d3js",
        "fidelity_intent": "fresh",
        "layout_policy": "optimize",
        "weight_plan": {"tiers": [
            {"t": "T1", "targets": "zones"},
            {"t": "T2", "targets": "elements"},
            {"t": "T3", "targets": "relations"},
        ]},
        "elements": [
            {"id": "a1", "label": "Alpha One", "zone": "za"},
            {"id": "a2", "label": "Alpha Two", "zone": "za"},
            {"id": "b1", "label": "Beta One", "zone": "zb"},
            {"id": "b2", "label": "Beta Two", "zone": "zb"},
            {"id": "n1", "label": "内层节点", "zone": "zb_inner"},
        ],
        "zones": [
            {"id": "za", "label": "Zone A", "parent": None},
            {"id": "zb", "label": "Zone B", "parent": None},
            {"id": "zb_inner", "label": "Inner", "parent": "zb"},
        ],
        "relations": [
            {"id": "E1", "from": "a1", "to": "a2", "color": "#112233"},
            {"id": "E2", "from": "a2", "to": "b1", "label": "sync", "color": "#445566"},
            {"id": "E3", "from": "b2", "to": "zb_inner", "color": "#778899"},
            {"id": "E4", "from": "a1", "to": "zb", "color": "#aabbcc"},
        ],
    }


def plan():
    return {
        "columns": [["za"], ["zb"]],
        "zone_cols": {"za": 2, "zb": 2},
        "children_layout": {"zb": "stack"},
    }


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp(prefix="d3js-build-tests-"))
        cls.sds_path = cls.root / "sds.json"
        cls.sds_path.write_text(json.dumps(sds(), ensure_ascii=False), encoding="utf-8")
        cls.plan_path = cls.root / "plan.json"
        cls.plan_path.write_text(json.dumps(plan(), ensure_ascii=False), encoding="utf-8")
        cls.semantics_path = cls.root / "semantics.json"
        cls.semantics_path.write_text(json.dumps(
            {key: sds()[key] for key in ("title", "diagram_class", "elements", "zones", "relations")},
            ensure_ascii=False), encoding="utf-8")
        cls.vendor_path = cls.root / "d3.v7.min.js"
        cls.vendor_path.write_text("var d3 = {};\n", encoding="utf-8")
        cls.counter = 0

    def outdir(self, label):
        type(self).counter += 1
        path = self.root / ("out-%s-%02d" % (label, type(self).counter))
        path.mkdir()
        return path

    def build(self, out, html="chart.html", sds_path=None, plan_path=None, extra=()):
        args = [sys.executable, str(BUILD),
                "--sds", str(sds_path or self.sds_path),
                "--out", str(out), "--html", html,
                "--layout-plan", str(plan_path or self.plan_path),
                "--d3-vendor", str(self.vendor_path)] + list(extra)
        return subprocess.run(args, capture_output=True, text=True, timeout=300)

    def readback(self, out, html="chart.html"):
        report = out / "readback.json"
        run = subprocess.run([sys.executable, str(READBACK),
                              "--source", str(out / html),
                              "--semantics", str(self.semantics_path),
                              "--output", str(report)],
                             capture_output=True, text=True, timeout=120)
        data = json.loads(report.read_text(encoding="utf-8")) if report.exists() else None
        return run, data

    def test_builds_deterministically(self):
        first = self.outdir("det")
        second = self.outdir("det")
        run1 = self.build(first)
        run2 = self.build(second)
        self.assertEqual(run1.returncode, 0, run1.stderr)
        self.assertEqual(run2.returncode, 0, run2.stderr)
        html1 = (first / "chart.html").read_bytes()
        html2 = (second / "chart.html").read_bytes()
        self.assertEqual(html1, html2)
        report = json.loads((first / "chart.layout-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["counts"]["elements"], 5)
        self.assertEqual(report["counts"]["zones"], 3)
        self.assertEqual(report["counts"]["relations"], 4)
        self.assertEqual(report["counts"]["labeled"], 1)

    def test_single_data_script_and_no_external_urls(self):
        out = self.outdir("single")
        run = self.build(out)
        self.assertEqual(run.returncode, 0, run.stderr)
        page = (out / "chart.html").read_text(encoding="utf-8")
        self.assertEqual(page.count("const SDS"), 1)
        self.assertEqual(page.count("const SDS = {"), 1)
        self.assertNotIn("&quot;", page)
        # SVG namespace URIs appear inside the inline viewer code; what matters is that
        # no element LOADS a remote resource.
        self.assertNotRegex(page, r'(?:src|href)="https?://')
        self.assertIn('src="vendor/d3.v7.min.js"', page)
        self.assertTrue((out / "vendor" / "d3.v7.min.js").is_file())
        report = json.loads((out / "chart.layout-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["d3_asset"]["mode"], "local-vendor")
        self.assertEqual(report["d3_asset"]["external_dependencies"], [])

    def test_generated_html_validates_semantically(self):
        out = self.outdir("semantic")
        run = self.build(out)
        self.assertEqual(run.returncode, 0, run.stderr)
        readback_run, report = self.readback(out)
        self.assertEqual(report["semantic"]["status"], "pass", readback_run.stdout)
        self.assertEqual(report["extraction"]["status"], "ok")
        self.assertEqual(report["records"]["elements"][2]["id"], "b1")
        self.assertEqual(report["semantic"]["duplicate_labels"]["actual_elements"], {})

    def test_label_placement_has_no_fallback_or_collisions(self):
        out = self.outdir("labels")
        run = self.build(out)
        self.assertEqual(run.returncode, 0, run.stderr)
        report = json.loads((out / "chart.layout-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["labels"]["issues"], [])
        self.assertEqual(report["labels"]["collisions"]["label_vs_card"], [])
        self.assertEqual(report["labels"]["collisions"]["label_vs_label"], [])
        self.assertEqual(report["labels"]["collisions"]["label_vs_edge"], [])
        self.assertEqual(report["route_failures"], [])
        self.assertEqual(report["solid_hits"], [])
        self.assertIsInstance(report["crossings"]["count"], int)
        self.assertIsInstance(report["collinear"]["total_px"], (int, float))

    def test_overwrite_is_refused(self):
        out = self.outdir("overwrite")
        first = self.build(out)
        self.assertEqual(first.returncode, 0, first.stderr)
        second = self.build(out)
        self.assertEqual(second.returncode, 2)
        self.assertIn("refusing to overwrite", second.stderr)

    def test_invalid_sds_is_refused(self):
        broken = sds()
        broken["relations"][0]["to"] = "missing"
        path = self.write_json("broken-endpoint.json", broken)
        out = self.outdir("broken")
        run = self.build(out, sds_path=path)
        self.assertEqual(run.returncode, 2)
        self.assertIn("unknown to endpoint", run.stderr)
        duplicate = sds()
        duplicate["elements"].append(dict(duplicate["elements"][0]))
        path = self.write_json("duplicate.json", duplicate)
        out = self.outdir("duplicate")
        run = self.build(out, sds_path=path)
        self.assertEqual(run.returncode, 2)

    def test_plan_must_place_every_top_zone(self):
        incomplete = {"columns": [["za"]]}
        path = self.write_json("incomplete-plan.json", incomplete)
        out = self.outdir("plan")
        run = self.build(out, plan_path=path)
        self.assertEqual(run.returncode, 2)
        self.assertIn("does not place top-level zones", run.stderr)

    def test_help_version_and_unknown_flag(self):
        help_run = subprocess.run([sys.executable, str(BUILD), "--help"],
                                  capture_output=True, text=True, timeout=60)
        version_run = subprocess.run([sys.executable, str(BUILD), "--version"],
                                     capture_output=True, text=True, timeout=60)
        unknown_run = subprocess.run([sys.executable, str(BUILD), "--nope"],
                                     capture_output=True, text=True, timeout=60)
        self.assertEqual(help_run.returncode, 0)
        self.assertIn("--sds", help_run.stdout)
        self.assertEqual(version_run.returncode, 0)
        self.assertIn("build-native", version_run.stdout)
        self.assertEqual(unknown_run.returncode, 2)

    def test_reusable_sources_carry_no_private_data(self):
        forbidden = ("璇玑", "/Users/", "xuanji-render", "六引擎", "qodercli-e2e")
        for path in (BUILD, READBACK, VIEWER_JS, VIEWER_CSS):
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, "%s contains %r" % (path.name, token))

    def write_json(self, name, payload):
        path = self.root / name
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path


if __name__ == "__main__":
    unittest.main()
