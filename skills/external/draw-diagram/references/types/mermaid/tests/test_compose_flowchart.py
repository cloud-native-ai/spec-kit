"""Positive and negative cases for compose-flowchart.py.

The generator is exercised on synthetic semantics only; the round-trip check
parses its own output back with native-readback.py's Mermaid parser and diffs
it against the same semantics.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/references/types/mermaid/tests/ -q
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MMD_ROOT = Path(__file__).resolve().parents[1]
COMPOSE = MMD_ROOT / "scripts" / "compose-flowchart.py"
READBACK = MMD_ROOT / "scripts" / "native-readback.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RB = load_module("mermaid_native_readback_for_compose", READBACK)

SEMANTICS = {
    "title": "Compose Test",
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

FLOW_SEMANTICS = {
    "elements": [
        {"id": "n", "label": "Second", "zone": "z1"},
        {"id": "m", "label": "First", "zone": "z1"},
    ],
    "zones": [{"id": "z1", "label": "Zone", "parent": None}],
    "relations": [{"id": "r1", "from": "m", "to": "n", "color": "#333333"}],
    "counts": {"elements": 2, "zones": 1, "relations": 1},
}

ISOLATED_SEMANTICS = {
    "elements": [
        {"id": "x", "label": "X", "zone": "z1"},
        {"id": "y", "label": "Y", "zone": "z1"},
        {"id": "z", "label": "Z", "zone": "z1"},
    ],
    "zones": [{"id": "z1", "label": "Zone", "parent": None}],
    "relations": [],
    "counts": {"elements": 3, "zones": 1, "relations": 0},
}


def run(args):
    proc = subprocess.run([sys.executable, "-B", str(COMPOSE)] + list(args),
                          capture_output=True, text=True, timeout=120)
    return proc.returncode, proc.stdout, proc.stderr


class ComposeCase(unittest.TestCase):
    def compose(self, tmp, semantics, *extra, name="diagram.mmd"):
        sem = Path(tmp) / "semantics.json"
        sem.write_text(json.dumps(semantics, ensure_ascii=False), encoding="utf-8")
        out = Path(tmp) / name
        code, stdout, stderr = run(["--semantics", str(sem), "--output", str(out)] + list(extra))
        text = out.read_text(encoding="utf-8") if out.exists() else None
        return code, text, stdout + stderr

    def test_round_trip_semantics(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, SEMANTICS)
            self.assertEqual(code, 0, output)
            model = RB.parse_mermaid(text)
            diffs = RB.semantic_diff(model, SEMANTICS)
            self.assertEqual(diffs["hardDiffCount"], 0, diffs)
            self.assertEqual(len(model.nodes), 5)
            self.assertEqual(len(model.zones), 2)
            self.assertEqual(len(model.business), 3)
            self.assertEqual(model.direction, "TD")
            self.assertEqual(model.unsupported, [])

    def test_init_directive_is_well_formed(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, SEMANTICS)
            self.assertEqual(code, 0, output)
            first = text.splitlines()[0]
            self.assertTrue(first.startswith("%%{init:"), first)
            self.assertTrue(first.endswith("}%%"), first)

    def test_link_style_indices_follow_relation_order(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, SEMANTICS)
            self.assertEqual(code, 0, output)
            model = RB.parse_mermaid(text)
            colors = RB.business_color_map(model)
            self.assertEqual(colors.get(0), "#111111")
            self.assertEqual(colors.get(1), "#111111")
            self.assertEqual(colors.get(2), "#222222")

    def test_container_endpoint_is_kept_verbatim(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, SEMANTICS)
            self.assertEqual(code, 0, output)
            self.assertIn("  b --> z1a", text)
            model = RB.parse_mermaid(text)
            self.assertEqual(model.business[1]["to"], "z1a")

    def test_isolated_scaffold_only_chains_untouched_members(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, SEMANTICS)
            self.assertEqual(code, 0, output)
            self.assertNotIn("~~~", text)
            code, text, output = self.compose(raw, ISOLATED_SEMANTICS, name="isolated.mmd")
            self.assertEqual(code, 0, output)
            self.assertIn("  x ~~~ y", text)
            self.assertIn("  y ~~~ z", text)
            model = RB.parse_mermaid(text)
            self.assertEqual(len(model.business), 0)
            self.assertEqual(len(model.layout), 2)

    def test_all_scaffold_chains_connected_members_too(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, SEMANTICS, "--scaffold", "all")
            self.assertEqual(code, 0, output)
            self.assertIn("  a ~~~ b", text)
            self.assertIn("  b ~~~ e", text)
            self.assertIn("  c ~~~ d", text)

    def test_member_order_flow_ranks_sources_first(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, FLOW_SEMANTICS)
            self.assertEqual(code, 0, output)
            self.assertLess(text.index('n["Second"]'), text.index('m["First"]'))
            code, text, output = self.compose(raw, FLOW_SEMANTICS, "--member-order", "flow",
                                              name="flow.mmd")
            self.assertEqual(code, 0, output)
            self.assertLess(text.index('m["First"]'), text.index('n["Second"]'))

    def test_existing_output_is_refused(self):
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, SEMANTICS)
            self.assertEqual(code, 0, output)
            code, text, output = self.compose(raw, SEMANTICS)
            self.assertEqual(code, 4, output)
            self.assertIn("refusing to overwrite", output)

    def test_unknown_endpoint_is_refused(self):
        bad = json.loads(json.dumps(SEMANTICS))
        bad["relations"][0]["to"] = "nope"
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, bad)
            self.assertEqual(code, 1, output)
            self.assertIn("nope", output)
            self.assertIsNone(text)

    def test_duplicate_element_id_is_refused(self):
        bad = json.loads(json.dumps(SEMANTICS))
        bad["elements"][1]["id"] = "a"
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, bad)
            self.assertEqual(code, 1, output)
            self.assertIn("duplicate element id", output)

    def test_counts_mismatch_is_refused(self):
        bad = json.loads(json.dumps(SEMANTICS))
        bad["counts"]["relations"] = 99
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, bad)
            self.assertEqual(code, 1, output)
            self.assertIn("but file has", output)

    def test_pipe_in_label_is_refused(self):
        bad = json.loads(json.dumps(SEMANTICS))
        bad["relations"][0]["label"] = "a|b"
        with tempfile.TemporaryDirectory() as raw:
            code, text, output = self.compose(raw, bad)
            self.assertEqual(code, 1, output)
            self.assertIn("unsupported character", output)

    def test_unknown_flag_is_rejected(self):
        code, stdout, stderr = run(["--semantics", "x", "--output", "y", "--fancy"])
        self.assertEqual(code, 2)
        self.assertIn("unrecognized option", stderr)

    def test_missing_input_returns_five(self):
        with tempfile.TemporaryDirectory() as raw:
            code, stdout, stderr = run(["--semantics", str(Path(raw) / "nope.json"),
                                        "--output", str(Path(raw) / "out.mmd")])
            self.assertEqual(code, 5, stdout + stderr)

    def test_help_and_version(self):
        code, stdout, _ = run(["--help"])
        self.assertEqual(code, 0)
        for token in ("usage:", "options:", "side-effects:", "exit-codes:"):
            self.assertIn(token, stdout)
        code, stdout, _ = run(["--version"])
        self.assertEqual(code, 0)
        self.assertRegex(stdout.strip(), r"^compose-flowchart\.py \S+$")


if __name__ == "__main__":
    unittest.main()
