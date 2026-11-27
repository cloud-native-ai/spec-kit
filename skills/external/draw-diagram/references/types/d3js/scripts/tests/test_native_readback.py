"""Positive/negative cases for references/types/d3js/scripts/native-readback.py.

Covers the repaired defects and the interface contract:
- documentation / escaped / commented-out data copies are never extracted;
- ambiguous or non-literal data blocks are explicit, never guessed;
- changed IDs, endpoints, membership, parents, labels and colors are detected;
- duplicate labels are preserved per ID; container endpoints are not expanded;
- SVG identity works through data-* attributes and the documented legacy
  node-/zone-/edge- prefix mapping (never arbitrary substring matches);
- legend semantics are declared: business kinds / undeclared text are refused;
- --help/--version/unknown flags/overwrite refusal and partial outcomes.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/references/types/d3js/scripts/tests/test_native_readback.py -q
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "native-readback.py"


def records():
    return {
        "title": "Synthetic",
        "diagram_class": "topology",
        "engine": "d3js",
        "fidelity_intent": "fresh",
        "layout_policy": "optimize",
        "elements": [
            {"id": "a", "label": "Alpha", "zone": "z1", "box": {"x": 10, "y": 10, "w": 80, "h": 40}},
            {"id": "b", "label": "Beta", "zone": "z1", "box": {"x": 200, "y": 10, "w": 80, "h": 40}},
            {"id": "c", "label": "Beta", "zone": "z2", "box": {"x": 10, "y": 180, "w": 80, "h": 40}},
        ],
        "zones": [
            {"id": "z1", "label": "Zone 1", "parent": None, "box": {"x": 0, "y": 0, "w": 300, "h": 100}},
            {"id": "z2", "label": "Zone 2", "parent": None, "box": {"x": 0, "y": 150, "w": 300, "h": 100}},
        ],
        "relations": [
            {"id": "r1", "from": "a", "to": "b", "label": "sync", "color": "#112233",
             "route": [{"x": 90, "y": 30}, {"x": 200, "y": 30}]},
            {"id": "r2", "from": "a", "to": "z2", "color": "#445566",
             "route": [{"x": 50, "y": 50}, {"x": 50, "y": 150}]},
        ],
    }


def semantics(data=None):
    payload = data or records()
    return {
        "title": payload["title"],
        "diagram_class": payload["diagram_class"],
        "elements": [{"id": item["id"], "label": item["label"], "zone": item["zone"]}
                     for item in payload["elements"]],
        "zones": [{"id": item["id"], "label": item["label"], "parent": item["parent"]}
                  for item in payload["zones"]],
        "relations": [{"id": item["id"], "from": item["from"], "to": item["to"],
                       "label": item.get("label"), "color": item["color"]}
                      for item in payload["relations"]],
    }


def page(data=None, extra_scripts="", decoy=True, commented_decoy=False):
    payload = data or records()
    literal = json.dumps(payload, ensure_ascii=False)
    parts = ["<!DOCTYPE html><html><head><title>t</title></head><body>"]
    if decoy:
        parts.append('<pre><code>const SDS = { &quot;elements&quot;: [], &quot;zones&quot;: [], '
                     '&quot;relations&quot;: [] }</code></pre>')
    if commented_decoy:
        parts.append("<script>// const SDS = {\"elements\": [], \"zones\": [], \"relations\": []};\n"
                     "const unrelated = 1;</script>")
    parts.append("<script>\nconst SDS = " + literal + ";\n</script>")
    parts.append(extra_scripts)
    parts.append("</body></html>")
    return "".join(parts)


def svg(data=None, legacy=False, drop_node=None, rename_node=None, business_kind=False,
        undeclared_text=False, legacy_legend=False):
    payload = data or records()
    nodes = []
    for item in payload["elements"]:
        node_id = item["id"]
        if node_id == drop_node:
            continue
        if node_id == rename_node:
            node_id = node_id + "x"
        attrs = "" if legacy else ' data-node-id="%s"' % node_id
        zone_attr = "" if legacy else ' data-zone="%s"' % item["zone"]
        box = item["box"]
        nodes.append(
            '<g class="node" id="node-%s"%s%s transform="translate(%d,%d)">'
            '<rect width="%d" height="%d"/><text class="node-label">%s</text></g>'
            % (node_id, attrs, zone_attr, box["x"], box["y"], box["w"], box["h"], item["label"]))
    zones = []
    for item in payload["zones"]:
        attrs = "" if legacy else ' data-zone-id="%s"' % item["id"]
        parent = "" if legacy else ' data-parent="%s"' % (item["parent"] or "")
        box = item["box"]
        zones.append(
            '<g class="zone" id="zone-%s"%s%s>'
            '<rect x="%d" y="%d" width="%d" height="%d"/>'
            '<text class="zone-label">%s</text></g>'
            % (item["id"], attrs, parent, box["x"], box["y"], box["w"], box["h"], item["label"]))
    edges = []
    labels = []
    for item in payload["relations"]:
        attrs = "" if legacy else (' data-edge-id="%s" data-from="%s" data-to="%s"'
                                   % (item["id"], item["from"], item["to"]))
        route = item["route"]
        d = "M" + " L".join("%s,%s" % (point["x"], point["y"]) for point in route)
        edges.append('<g class="edge" id="edge-%s"%s data-color="%s">'
                     '<path class="edge-line" stroke="%s" d="%s"/></g>'
                     % (item["id"], attrs, item["color"], item["color"], d))
        if item.get("label"):
            labels.append('<text class="edge-label" data-edge-id="%s" x="140" y="18">%s</text>'
                          % (item["id"], item["label"]))
    if legacy_legend:
        legend = '<g id="legend-panel" data-legend="1"><text class="legend-title">Legend</text>' \
                 '<line x1="10" y1="40" x2="40" y2="40" stroke="#112233"/>' \
                 '<text class="legend-text">relationship line 1.6px</text></g>'
    else:
        kind = "business" if business_kind else "style"
        legend = ('<g id="legend-panel" data-legend="1"><text class="legend-title">Legend</text>'
                  '<g class="legend-item" data-legend-kind="%s" data-swatch-color="#666666">'
                  '<line x1="10" y1="40" x2="40" y2="40" stroke="#666666"/>'
                  '<text class="legend-text">relationship line 1.6px</text></g>'
                  % kind)
        if undeclared_text:
            legend += '<text class="legend-text">采集/上报链路</text>'
        legend += "</g>"
    return ('<svg xmlns="http://www.w3.org/2000/svg" id="arch-svg" viewBox="0 0 320 260">'
            '<g id="layer-zones">' + "".join(zones) + '</g>'
            '<g id="layer-edges">' + "".join(edges) + '</g>'
            '<g id="layer-labels">' + "".join(labels) + '</g>'
            '<g id="layer-nodes">' + "".join(nodes) + '</g>'
            + legend + "</svg>")


class ReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp(prefix="d3js-readback-tests-"))
        cls.semantics_path = cls.root / "semantics.json"
        cls.semantics_path.write_text(json.dumps(semantics(), ensure_ascii=False), encoding="utf-8")
        cls.counter = 0

    def write(self, name, content):
        path = self.root / name
        path.write_text(content, encoding="utf-8")
        return path

    def run_cli(self, source, svg_path=None, expectations=None):
        type(self).counter += 1
        out = self.root / ("report-%02d.json" % self.counter)
        args = [sys.executable, str(SCRIPT), "--source", str(source),
                "--semantics", str(self.semantics_path), "--output", str(out)]
        if svg_path is not None:
            args += ["--svg", str(svg_path)]
        completed = subprocess.run(args, capture_output=True, text=True, timeout=120)
        report = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
        return completed, report

    def html_and_report(self, **kwargs):
        source = self.write("page-%02d.html" % type(self).counter, page(**kwargs))
        completed, report = self.run_cli(source)
        return completed, report

    def svg_and_report(self, **kwargs):
        source = self.write("page-svg-%02d.html" % type(self).counter, page())
        rendered = self.write("render-%02d.svg" % type(self).counter, svg(**kwargs))
        completed, report = self.run_cli(source, rendered)
        return completed, report

    # ---- extraction ---------------------------------------------------------
    def test_extracts_real_script_over_documentation_copy(self):
        completed, report = self.html_and_report(decoy=True)
        self.assertEqual(completed.returncode, 3, completed.stderr)  # no SVG -> partial
        self.assertEqual(report["semantic"]["status"], "pass")
        self.assertEqual(report["extraction"]["status"], "ok")
        self.assertEqual(len(report["extraction"]["candidates"]), 1)
        self.assertEqual(report["records"]["elements"][0]["id"], "a")

    def test_commented_out_decoy_is_ignored(self):
        completed, report = self.html_and_report(decoy=True, commented_decoy=True)
        self.assertEqual(report["extraction"]["status"], "ok")
        self.assertEqual(len(report["extraction"]["candidates"]), 1)
        self.assertEqual(report["semantic"]["status"], "pass")

    def test_ambiguous_data_blocks_are_refused(self):
        other = records()
        other["title"] = "Other"
        extra = "<script>const DATA = %s;</script>" % json.dumps(other)
        completed, report = self.html_and_report(extra_scripts=extra)
        self.assertEqual(completed.returncode, 3)
        self.assertEqual(report["overall"], "unsupported")
        self.assertEqual(report["extraction"]["status"], "ambiguous")
        self.assertEqual(len(report["extraction"]["candidates"]), 2)
        self.assertIsNone(report["records"])

    def test_non_literal_data_block_is_unsupported(self):
        source = self.write("nonliteral.html",
                            "<html><body><script>const SDS = JSON.parse(atob('e30='));</script>"
                            "</body></html>")
        completed, report = self.run_cli(source)
        self.assertEqual(completed.returncode, 3)
        self.assertEqual(report["extraction"]["status"], "unsupported")

    # ---- semantic diffs -----------------------------------------------------
    def test_changed_element_id_is_detected(self):
        data = records()
        data["elements"][0]["id"] = "a2"
        completed, report = self.html_and_report(data=data)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(report["semantic"]["status"], "fail")
        self.assertIn("a", report["semantic"]["diff"]["elements"]["missing"])
        self.assertIn("a2", report["semantic"]["diff"]["elements"]["extra"])

    def test_changed_endpoint_direction_is_detected(self):
        data = records()
        data["relations"][0]["from"], data["relations"][0]["to"] = "b", "a"
        completed, report = self.html_and_report(data=data)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(report["semantic"]["diff"]["relations"]["endpoint_mismatch"][0]["id"], "r1")

    def test_changed_membership_and_parent_are_detected(self):
        data = records()
        data["elements"][0]["zone"] = "z2"
        data["zones"][1]["parent"] = "z1"
        completed, report = self.html_and_report(data=data)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(report["semantic"]["diff"]["elements"]["zone_mismatch"][0]["id"], "a")
        self.assertEqual(report["semantic"]["diff"]["zones"]["parent_mismatch"][0]["id"], "z2")

    def test_changed_label_and_color_are_detected(self):
        data = records()
        data["relations"][0]["label"] = "async"
        data["relations"][1]["color"] = "#000000"
        completed, report = self.html_and_report(data=data)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(report["semantic"]["diff"]["relations"]["label_mismatch"][0]["id"], "r1")
        self.assertEqual(report["semantic"]["diff"]["relations"]["color_mismatch"][0]["id"], "r2")

    def test_duplicate_labels_are_preserved_and_dedupe_is_detected(self):
        completed, report = self.html_and_report()
        self.assertEqual(report["semantic"]["duplicate_labels"]["actual_elements"]["Beta"], ["b", "c"])
        data = records()
        data["elements"] = [item for item in data["elements"] if item["id"] != "c"]
        data["relations"] = [item for item in data["relations"] if item["id"] != "r2"]
        data["zones"] = data["zones"][:1]
        completed, report = self.html_and_report(data=data)
        self.assertEqual(completed.returncode, 1)

    def test_container_endpoint_expansion_is_detected(self):
        data = records()
        data["relations"][1]["to"] = "c"
        completed, report = self.html_and_report(data=data)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(report["semantic"]["diff"]["container_expanded"][0]["zone"], "z2")
        self.assertEqual(report["semantic"]["diff"]["container_expanded"][0]["member"], "c")

    # ---- SVG identity / labels / legend ------------------------------------
    def test_svg_pass_with_declared_legend(self):
        completed, report = self.svg_and_report()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(report["overall"], "pass")
        self.assertEqual(report["visual"]["status"], "pass")
        self.assertEqual(report["visual"]["checks"]["legend"]["format"], "declared")
        self.assertEqual(report["visual"]["checks"]["geometry"]["crossings_count"], 0)

    def test_svg_legacy_prefix_identity(self):
        completed, report = self.svg_and_report(legacy=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        modes = report["visual"]["checks"]["identity"]["modes"]
        self.assertIn("legacy-prefix", modes["node"])
        self.assertIn("legacy-prefix", modes["edge"])

    def test_svg_substring_coincidence_is_not_identity(self):
        completed, report = self.svg_and_report(rename_node="a")
        self.assertEqual(completed.returncode, 1)
        missing = report["visual"]["checks"]["identity"]["nodes"]["missing"]
        extra = report["visual"]["checks"]["identity"]["nodes"]["extra"]
        self.assertIn("a", missing)
        self.assertIn("ax", extra)

    def test_svg_missing_node_is_detected(self):
        completed, report = self.svg_and_report(drop_node="b")
        self.assertEqual(completed.returncode, 1)
        self.assertIn("b", report["visual"]["checks"]["identity"]["nodes"]["missing"])

    def test_business_legend_kind_is_detected(self):
        completed, report = self.svg_and_report(business_kind=True)
        self.assertEqual(completed.returncode, 1)
        codes = [issue["code"] for issue in report["visual"]["issues"]]
        self.assertIn("extra-legend-semantics", codes)

    def test_undeclared_legend_text_is_detected(self):
        completed, report = self.svg_and_report(undeclared_text=True)
        self.assertEqual(completed.returncode, 1)
        codes = [issue["code"] for issue in report["visual"]["issues"]]
        self.assertIn("undeclared-legend-text", codes)

    def test_legacy_legend_is_partial_not_pass(self):
        completed, report = self.svg_and_report(legacy_legend=True)
        self.assertEqual(completed.returncode, 3)
        self.assertEqual(report["visual"]["status"], "partial")
        self.assertEqual(report["visual"]["checks"]["legend"]["format"], "undeclared")

    # ---- interface ----------------------------------------------------------
    def test_help_and_version_need_no_output(self):
        help_run = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                                  capture_output=True, text=True, timeout=60)
        version_run = subprocess.run([sys.executable, str(SCRIPT), "--version"],
                                     capture_output=True, text=True, timeout=60)
        self.assertEqual(help_run.returncode, 0)
        self.assertIn("--source", help_run.stdout)
        self.assertEqual(version_run.returncode, 0)
        self.assertIn("native-readback", version_run.stdout)

    def test_unknown_flag_is_usage_error(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "--not-a-flag"],
                             capture_output=True, text=True, timeout=60)
        self.assertEqual(run.returncode, 2)

    def test_overwrite_is_refused(self):
        source = self.write("overwrite.html", page())
        out = self.root / "existing-report.json"
        out.write_text("{}", encoding="utf-8")
        run = subprocess.run([sys.executable, str(SCRIPT), "--source", str(source),
                              "--semantics", str(self.semantics_path), "--output", str(out)],
                             capture_output=True, text=True, timeout=120)
        self.assertEqual(run.returncode, 2)
        self.assertIn("refusing to overwrite", run.stderr)

    def test_dtd_in_svg_is_refused(self):
        source = self.write("dtd.html", page())
        rendered = self.write("dtd.svg", '<!DOCTYPE svg [<!ENTITY x "y">]>' + svg())
        completed, report = self.run_cli(source, rendered)
        self.assertEqual(completed.returncode, 2)
        self.assertIsNone(report)


if __name__ == "__main__":
    unittest.main()
