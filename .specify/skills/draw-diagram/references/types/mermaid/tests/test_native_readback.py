"""Positive and negative cases for the Mermaid native readback.

The fixtures are synthetic on purpose: they exercise the real `.mmd` grammar
and the real Mermaid SVG markup shapes (nested root translates, node rects,
cluster rects, M/L polylines, edgeLabel groups) without any private business
graph, count or absolute path.

Covered: clean pass, semantic data-loss/mutation, container endpoint landing on
a member, hidden layout edges kept separate, real edge-through-node geometry,
label binding, legend-like extra text, unsupported SVG geometry, unsupported
source constructs, overwrite refusal and unknown-flag rejection.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/references/types/mermaid/tests/ -q
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MMD_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = MMD_ROOT / "scripts" / "native-readback.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


READBACK = load_module("mermaid_native_readback", SCRIPT)

SEMANTICS = {
    "title": "Readback Test",
    "diagram_class": "topology",
    "fidelity_intent": "reproduction",
    "layout_policy": "optimize",
    "elements": [
        {"id": "a", "label": "Alpha", "zone": "z1"},
        {"id": "b", "label": "Beta", "zone": "z1"},
        {"id": "e", "label": "Epsilon", "zone": "z1"},
        {"id": "c", "label": "Gamma", "zone": "z1a"},
        {"id": "d", "label": "Delta", "zone": "z1a"},
    ],
    "zones": [
        {"id": "z1", "label": "Zone One", "parent": None},
        {"id": "z1a", "label": "Inner", "parent": "z1"},
    ],
    "relations": [
        {"id": "r1", "from": "a", "to": "b", "label": "calls", "color": "#111111"},
        {"id": "r2", "from": "b", "to": "z1a", "color": "#111111"},
        {"id": "r3", "from": "c", "to": "d", "color": "#222222"},
    ],
    "counts": {"elements": 5, "zones": 2, "relations": 3},
}


def mmd_source(relations=None, extra_lines=None):
    relations = relations if relations is not None else [
        "  a -->|calls| b",
        "  b --> z1a",
        "  c --> d",
    ]
    extra = extra_lines or []
    lines = [
        "%%{init: {\"theme\": \"base\"}}%%",
        "flowchart TD",
        '  subgraph z1["Zone One"]',
        '    a["Alpha"]',
        '    b["Beta"]',
        '    e["Epsilon"]',
        '    subgraph z1a["Inner"]',
        '      c["Gamma"]',
        '      d["Delta"]',
        "    end",
        "  end",
        "%% ---- relations ----",
    ]
    lines.extend(relations)
    lines.extend(extra)
    lines.extend([
        "  classDef comp fill:#ffffff",
        "  class a,b,c,d,e comp",
        "  linkStyle 0,1 stroke:#111111,stroke-width:1.5px",
        "  linkStyle 2 stroke:#222222,stroke-width:1.5px",
    ])
    return "\n".join(lines) + "\n"


def offset_path(d, tx, ty):
    def sub(match):
        return "%s%s,%s" % (match.group(1), float(match.group(2)) - tx, float(match.group(3)) - ty)
    return re.sub(r"([ML])\s*(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", sub, d)


def node_g(nid, index, x, y, w=40, h=16, label=None, offset=(0, 0)):
    return (
        '<g class="node default comp" id="mmd-flowchart-%s-%d" transform="translate(%s,%s)">'
        '<rect class="basic label-container" x="%s" y="%s" width="%s" height="%s"></rect>'
        '<g class="label"><text>%s</text></g></g>'
        % (nid, index, x - offset[0], y - offset[1], -w / 2.0, -h / 2.0, w, h, label or nid)
    )


def cluster_g(zid, x, y, w, h, label, offset=(0, 0)):
    return (
        '<g class="cluster " id="mmd-%s"><rect x="%s" y="%s" width="%s" height="%s"></rect>'
        '<g class="cluster-label"><text>%s</text></g></g>'
        % (zid, x - offset[0], y - offset[1], w, h, label)
    )


def path_el(path_id, d, invisible=False, offset=(0, 0)):
    cls = (" edge-thickness-invisible edge-pattern-solid" if invisible
           else " edge-thickness-normal edge-pattern-solid")
    return '<path id="mmd-%s" data-et="edge" class="%s" d="%s"></path>' % (
        path_id, cls, offset_path(d, offset[0], offset[1]))


def label_group(edge_id, x, y, text, offset=(0, 0)):
    return (
        '<g class="edgeLabel" transform="translate(%s,%s)">'
        '<g class="label" data-id="%s" transform="translate(0,-10)">'
        '<g><rect x="-10" y="-5" width="20" height="10"></rect>'
        '<text><tspan>%s</tspan></text></g></g></g>'
        % (x - offset[0], y - offset[1], edge_id, text)
    )


def build_svg(epsilon_y=240, extra_texts=None, r2_path="M80,168L200,160",
              curved=False, translate=(0, 0), layout_path_d="M100,278L180,278",
              extra_paths=None):
    tx, ty = translate
    clusters = [cluster_g("z1", 10, 10, 380, 290, "Zone One", translate),
                cluster_g("z1a", 200, 100, 150, 120, "Inner", translate)]
    nodes = [
        node_g("a", 1, 60, 60, label="Alpha", offset=translate),
        node_g("b", 2, 60, 160, label="Beta", offset=translate),
        node_g("e", 3, 60, epsilon_y, label="Epsilon", offset=translate),
        node_g("c", 4, 250, 150, label="Gamma", offset=translate),
        node_g("d", 5, 330, 150, label="Delta", offset=translate),
    ]
    paths = [
        path_el("L_a_b_0", "M60,68L60,152", offset=translate),
        path_el("L_b_z1a_0", r2_path, offset=translate),
        path_el("L_c_d_0", "M270,158C280,158 300,158 310,158" if curved else "M270,158L310,158",
                offset=translate),
    ]
    if layout_path_d:
        paths.append(path_el("L_e_a_0", layout_path_d, invisible=True, offset=translate))
    if extra_paths:
        paths.extend(extra_paths)
    labels = [label_group("L_a_b_0", 60, 110, "calls", translate)]
    transform_attr = ' transform="translate(%s,%s)"' % (tx, ty) if (tx or ty) else ""
    body = (
        '<svg id="mmd" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">'
        "<style>#mmd{font-size:16;fill:#0f172a;}</style>"
        '<g class="root"%s>'
        '<g class="clusters">%s</g>'
        '<g class="edgePaths">%s</g>'
        '<g class="edgeLabels">%s</g>'
        '<g class="nodes">%s</g>'
        "</g>"
        "%s"
        "</svg>"
    ) % (transform_attr, "".join(clusters), "".join(paths), "".join(labels), "".join(nodes),
         "".join("<text>%s</text>" % t for t in (extra_texts or [])))
    return body


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def run(args):
    proc = subprocess.run([sys.executable, "-B", str(SCRIPT)] + list(args),
                          capture_output=True, text=True, timeout=120)
    return proc.returncode, proc.stdout, proc.stderr


class ReadbackCase(unittest.TestCase):
    def make(self, raw_dir, mmd=None, svg=None, semantics=None):
        tmp = Path(raw_dir)
        src = write(tmp / "diagram.mmd", mmd if mmd is not None else mmd_source())
        svg_path = write(tmp / "diagram.svg", svg if svg is not None else build_svg())
        sem = write(tmp / "semantics.json",
                    json.dumps(semantics if semantics is not None else SEMANTICS, ensure_ascii=False))
        return tmp, src, svg_path, sem

    def read(self, tmp, src, svg_path, sem, *extra):
        out = tmp / "report.json"
        code, stdout, stderr = run(["--source", str(src), "--semantics", str(sem),
                                    "--svg", str(svg_path), "--output", str(out)] + list(extra))
        report = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
        return code, report, stdout + stderr

    def test_clean_case_passes(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 0, output)
            self.assertEqual(report["overall"], "pass", report["overall"])
            self.assertEqual(report["semantic"]["diffs"]["hardDiffCount"], 0)
            self.assertEqual(report["visual"]["checks"]["edgeThroughNode"]["count"], 0)
            self.assertEqual(report["visual"]["checks"]["edgeCrossings"]["count"], 0)
            endpoints = report["visual"]["checks"]["containerEndpoints"]["items"]
            self.assertEqual(len(endpoints), 1)
            self.assertEqual(endpoints[0]["relation"], "r2")
            self.assertEqual(endpoints[0]["assessment"], "cluster-border")
            label = report["visual"]["checks"]["labelBinding"]["items"][0]
            self.assertTrue(label["found"] and label["textMatches"], label)
            self.assertIn("distanceToEdgePx", label)

    def test_edge_through_node_is_measured_as_partial(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, svg=build_svg(epsilon_y=110))
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 3, output)
            self.assertEqual(report["visual"]["status"], "partial")
            pairs = report["visual"]["checks"]["edgeThroughNode"]["pairs"]
            self.assertEqual(len(pairs), 1, pairs)
            self.assertEqual(pairs[0]["edge"], "L_a_b_0")
            self.assertEqual(pairs[0]["node"], "e")
            self.assertGreater(pairs[0]["clippedLengthPx"], 10)

    def test_hidden_layout_edges_are_counted_separately(self):
        svg = build_svg(layout_path_d="M20,160L160,160")
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, svg=svg)
            code, report, output = self.read(tmp, src, svg_path, sem)
            checks = report["visual"]["checks"]
            self.assertEqual(checks["edgeThroughNode"]["count"], 0, checks["edgeThroughNode"])
            self.assertEqual(checks["layoutEdgeThroughNode"]["count"], 1,
                             checks["layoutEdgeThroughNode"])
            self.assertEqual(checks["layoutEdgeThroughNode"]["pairs"][0]["node"], "b")

    def test_container_endpoint_landing_on_member_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, svg=build_svg(r2_path="M80,168L250,150"))
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertEqual(report["visual"]["status"], "fail")
            self.assertTrue(any("lands on member" in d for d in report["visual"]["hardDefects"]),
                            report["visual"]["hardDefects"])

    def test_label_text_mismatch_fails(self):
        svg = build_svg().replace("<tspan>calls</tspan>", "<tspan>rings</tspan>")
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, svg=svg)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertTrue(any("label text mismatch" in d for d in report["visual"]["hardDefects"]),
                            report["visual"]["hardDefects"])

    def test_legend_like_extra_text_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, svg=build_svg(extra_texts=["图例: 红色=采集链路"]))
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertTrue(report["visual"]["checks"]["visibleText"]["legendLike"])
            self.assertTrue(any("legend-like" in d for d in report["visual"]["hardDefects"]))

    def test_unsupported_curve_is_partial_not_pass(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, svg=build_svg(curved=True))
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 3, output)
            self.assertTrue(report["visual"]["checks"]["unsupportedGeometry"])
            self.assertEqual(report["overall"], "partial")

    def test_nested_root_translate_is_applied(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(
                raw, svg=build_svg(epsilon_y=110, translate=(60, 60)))
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 3, output)
            pairs = report["visual"]["checks"]["edgeThroughNode"]["pairs"]
            self.assertTrue(any(p["node"] == "e" for p in pairs), pairs)
            endpoints = report["visual"]["checks"]["containerEndpoints"]["items"]
            self.assertEqual(endpoints[0]["assessment"], "cluster-border", endpoints[0])

    def test_missing_relation_fails(self):
        mmd = mmd_source(relations=["  a -->|calls| b", "  b --> z1a"])
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertIn("r3", report["semantic"]["diffs"]["missingRelations"])

    def test_endpoint_change_fails(self):
        mmd = mmd_source(relations=["  a -->|calls| b", "  b --> z1a", "  c --> e"])
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            changes = report["semantic"]["diffs"]["relationChanges"]
            self.assertTrue(any(c["relation"] == "r3" for c in changes), changes)

    def test_label_change_fails(self):
        mmd = mmd_source(relations=["  a -->|rings| b", "  b --> z1a", "  c --> d"])
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertTrue(any(c.get("field") == "label" for c in
                                report["semantic"]["diffs"]["relationChanges"]))

    def test_color_family_change_fails(self):
        mmd = mmd_source().replace("linkStyle 0,1 stroke:#111111",
                                   "linkStyle 0,1 stroke:#999999")
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertTrue(report["semantic"]["diffs"]["colorFamilyChanges"])

    def test_zone_membership_change_fails(self):
        mmd = mmd_source().replace('    b["Beta"]\n', "")
        mmd = mmd.replace('      c["Gamma"]', '      b["Beta"]\n      c["Gamma"]')
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertTrue(any(c["id"] == "b" for c in
                                report["semantic"]["diffs"]["elementZoneChanges"]))

    def test_container_endpoint_expanded_to_member_fails(self):
        mmd = mmd_source(relations=["  a -->|calls| b", "  b --> c", "  c --> d"])
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            self.assertTrue(any(item["relation"] == "r2" for item in
                                report["semantic"]["diffs"]["containerEndpointExpanded"]))

    def test_layout_edge_cannot_stand_in_for_a_business_relation(self):
        mmd = mmd_source(relations=["  b --> z1a", "  c --> d", "  a ~~~ b"])
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 1, output)
            diffs = report["semantic"]["diffs"]
            self.assertTrue(diffs["missingRelations"], diffs)
            self.assertTrue(any(x["from"] == "a" and x["to"] == "b"
                                for x in diffs["layoutEdgeLeaks"]), diffs)

    def test_unsupported_construct_is_partial(self):
        mmd = mmd_source(relations=["  a -->|calls| b", "  b --> z1a", "  c & d --> a"])
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw, mmd=mmd)
            code, report, output = self.read(tmp, src, svg_path, sem)
            self.assertEqual(code, 3, output)
            self.assertEqual(report["semantic"]["status"], "partial")
            self.assertTrue(report["unsupported"])

    def test_report_without_svg_is_not_evaluated(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw)
            out = tmp / "report-nosvg.json"
            code, stdout, stderr = run(["--source", str(src), "--semantics", str(sem),
                                        "--output", str(out)])
            report = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(code, 3, stdout + stderr)
            self.assertEqual(report["visual"]["status"], "not_evaluated")
            self.assertEqual(report["overall"], "partial")

    def test_existing_output_is_refused(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp, src, svg_path, sem = self.make(raw)
            out = write(tmp / "report.json", "{}")
            code, stdout, stderr = run(["--source", str(src), "--semantics", str(sem),
                                        "--svg", str(svg_path), "--output", str(out)])
            self.assertEqual(code, 4, stdout + stderr)

    def test_unknown_flag_is_rejected(self):
        code, stdout, stderr = run(["--source", "x", "--semantics", "y", "--output", "z",
                                    "--pretty"])
        self.assertEqual(code, 2)
        self.assertIn("unrecognized option", stderr)

    def test_missing_input_returns_five(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            code, stdout, stderr = run(["--source", str(tmp / "nope.mmd"),
                                        "--semantics", str(tmp / "nope.json"),
                                        "--output", str(tmp / "out.json")])
            self.assertEqual(code, 5, stdout + stderr)

    def test_help_and_version(self):
        code, stdout, _ = run(["--help"])
        self.assertEqual(code, 0)
        for token in ("usage:", "options:", "side-effects:", "exit-codes:"):
            self.assertIn(token, stdout)
        code, stdout, _ = run(["--version"])
        self.assertEqual(code, 0)
        self.assertRegex(stdout.strip(), r"^native-readback\.py \S+$")


if __name__ == "__main__":
    unittest.main()
