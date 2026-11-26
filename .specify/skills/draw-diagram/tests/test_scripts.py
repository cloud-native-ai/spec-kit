"""Positive/negative cases for the draw-diagram executable layer.

check-manifest.py: a good delivery passes; each bad-product mutation (fake hash,
input echo, readback theatre, hard-failure contradiction, absolute path, missing
export, unmeasured crossings, bare satisfaction claim, drawio recount mismatch)
is refused with its own code.

handoff.py: shared semantics cold-start produces per-engine SDS without any
geometry; broken semantics (unknown endpoint, duplicate id, counts mismatch) and
overwrite attempts are refused.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/tests/test_scripts.py -q
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECK = SKILL_ROOT / "scripts" / "check-manifest.py"
HANDOFF = SKILL_ROOT / "scripts" / "handoff.py"

DRAWIO_XML = """<mxfile compressed="false" host="check-manifest-test">
  <diagram id="architecture" name="Architecture Test">
    <mxGraphModel page="1" pageScale="1" pageWidth="400" pageHeight="300">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="zoneA" value="Zone A" vertex="1" parent="1" style="swimlane;container=1;">
          <mxGeometry x="0" y="0" width="400" height="300" as="geometry"/>
        </mxCell>
        <mxCell id="a" value="Alpha" vertex="1" parent="zoneA" style="">
          <mxGeometry x="20" y="40" width="80" height="40" as="geometry"/>
        </mxCell>
        <mxCell id="b" value="Beta" vertex="1" parent="zoneA" style="">
          <mxGeometry x="200" y="40" width="80" height="40" as="geometry"/>
        </mxCell>
        <mxCell id="r1" value="calls" edge="1" parent="1" source="a" target="b" style="">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

SVG = '<svg xmlns="http://www.w3.org/2000/svg"><text>Alpha</text></svg>\n'


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def good_manifest(delivery: Path) -> dict:
    source = delivery / "architecture.drawio"
    return {
        "engine": "drawio",
        "engine_version": "not_exposed",
        "layout_policy": "optimize",
        "ldm_sha256": hashlib.sha256(b"frozen-ldm-bytes").hexdigest(),
        "runtime_conditions": {
            "executor": "not_provided",
            "model": "not_provided",
            "context_window": "not_provided",
            "reasoning_effort": "not_provided",
            "config_root": "not_provided",
        },
        "source": {"path": "architecture.drawio", "format": "drawio", "sha256": sha256(source)},
        "exports": [
            {"path": "out.svg", "format": "svg", "width": 400, "height": 300, "produced_by": "render-service POST /svg"}
        ],
        "readback": {
            "method": "architecture.py validate",
            "elements": 2,
            "zones": 1,
            "relations": 1,
            "labels": 1,
            "parents": "verified",
            "directions": "verified",
        },
        "axes": {
            "semantic": "pass",
            "visual": "pass",
            "interaction": "not_applicable",
            "engineering": "pass",
        },
        "crossings": {"measured": True, "count": 0, "collinear_length": 0, "report_ref": None},
        "hard_failures": [],
        "unresolved": [],
        "user_evaluation": "not_available",
    }


def make_delivery(tmp_path: Path) -> tuple[Path, dict]:
    delivery = tmp_path / "delivery"
    delivery.mkdir()
    write(delivery / "architecture.drawio", DRAWIO_XML)
    write(delivery / "out.svg", SVG)
    manifest = good_manifest(delivery)
    return delivery, manifest


def run_check(delivery: Path, manifest: dict) -> tuple[int, dict]:
    path = delivery / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--manifest", str(path), "--json"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    verdict = json.loads(proc.stdout)
    return proc.returncode, verdict


def codes(verdict: dict) -> set[str]:
    return {item["code"] for item in verdict["violations"]}


class ManifestCheckerPositive(unittest.TestCase):
    def test_good_delivery_passes_with_native_recount(self):
        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            delivery, manifest = make_delivery(Path(raw))
            rc, verdict = run_check(delivery, manifest)
            self.assertEqual(rc, 0, verdict)
            self.assertEqual(verdict["status"], "pass")
            self.assertEqual(verdict["native_recount"]["status"], "recounted")
            self.assertEqual(verdict["native_recount"]["cells"], {"elements": 2, "zones": 1, "relations": 1})


class ManifestCheckerNegatives(unittest.TestCase):
    def assert_refused(self, mutate, expected_code):
        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            delivery, manifest = make_delivery(Path(raw))
            mutate(delivery, manifest)
            rc, verdict = run_check(delivery, manifest)
            self.assertEqual(rc, 1, verdict)
            self.assertEqual(verdict["status"], "fail")
            self.assertIn(expected_code, codes(verdict), verdict)

    def test_fake_source_hash_is_refused(self):
        def mutate(delivery, manifest):
            manifest["source"]["sha256"] = "0" * 64

        self.assert_refused(mutate, "source-hash")

    def test_input_echo_is_refused(self):
        def mutate(delivery, manifest):
            manifest["ldm_sha256"] = manifest["source"]["sha256"]

        self.assert_refused(mutate, "ldm-echo")

    def test_semantic_pass_without_real_readback_is_refused(self):
        def mutate(delivery, manifest):
            manifest["readback"]["method"] = "input-copy"

        self.assert_refused(mutate, "readback-missing")

    def test_semantic_pass_without_direction_readback_is_refused(self):
        def mutate(delivery, manifest):
            manifest["readback"]["directions"] = "not_checked"

        self.assert_refused(mutate, "semantic-no-directions")

    def test_hard_failure_cannot_be_offset_by_pass_axes(self):
        def mutate(delivery, manifest):
            manifest["hard_failures"] = ["label bound to the wrong relation"]

        self.assert_refused(mutate, "hard-failure-contradiction")

    def test_absolute_paths_are_refused(self):
        def mutate(delivery, manifest):
            manifest["source"]["path"] = "/Users/someone/architecture.drawio"

        self.assert_refused(mutate, "path-absolute")

    def test_missing_export_is_refused(self):
        def mutate(delivery, manifest):
            manifest["exports"][0]["path"] = "missing.svg"

        self.assert_refused(mutate, "export-missing")

    def test_visual_pass_without_measured_crossings_is_refused(self):
        def mutate(delivery, manifest):
            manifest["crossings"]["measured"] = False

        self.assert_refused(mutate, "visual-no-crossings")

    def test_bare_satisfaction_claim_is_refused(self):
        def mutate(delivery, manifest):
            manifest["user_evaluation"] = "satisfied"

        self.assert_refused(mutate, "user-eval-claim")

    def test_drawio_native_recount_mismatch_is_refused(self):
        def mutate(delivery, manifest):
            manifest["readback"]["elements"] = 3

        self.assert_refused(mutate, "native-recount-mismatch")

    def test_unknown_field_is_refused(self):
        def mutate(delivery, manifest):
            manifest["diagram_url"] = "https://example.invalid"

        self.assert_refused(mutate, "schema-extra")

    def test_empty_exports_are_refused(self):
        def mutate(delivery, manifest):
            manifest["exports"] = []

        self.assert_refused(mutate, "exports-empty")


SEMANTICS = {
    "title": "Handoff Test",
    "diagram_class": "topology",
    "fidelity_intent": "reproduction",
    "layout_policy": "optimize",
    "confirmed_decisions": ["A and B stay siblings"],
    "weight_plan": {"tiers": [{"t": "T1", "targets": "zones"}, {"t": "T3", "targets": "relations"}]},
    "zones": [
        {"id": "z1", "label": "Zone One", "members": ["a", "b"], "box": {"x": 0, "y": 0, "w": 400, "h": 300}},
    ],
    "elements": [
        {"id": "a", "label": "Alpha", "zone": "z1", "box": {"x": 10, "y": 10, "w": 80, "h": 40}},
        {"id": "b", "label": "Beta", "zone": "z1"},
        {"id": "c", "label": "Gamma", "zone": "z1"},
    ],
    "relations": [
        {"id": "r1", "from": "a", "to": "b", "label": "calls", "via": [{"x": 1, "y": 2}], "source_side": "right"},
        {"id": "r2", "from": "b", "to": "c"},
    ],
    "counts": {"elements": 3, "zones": 1, "relations": 2},
}


def run_handoff(tmp_path: Path, semantics: dict, *extra: str) -> tuple[int, str]:
    semantics_path = tmp_path / "semantics.json"
    semantics_path.write_text(json.dumps(semantics, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir(exist_ok=True)
    proc = subprocess.run(
        [sys.executable, str(HANDOFF), "--semantics", str(semantics_path), "--out", str(out), *extra],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return proc.returncode, proc.stdout + proc.stderr


class HandoffPositive(unittest.TestCase):
    def test_cold_start_strips_geometry_and_writes_per_engine_sds(self):
        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            rc, output = run_handoff(tmp, SEMANTICS, "--engines", "drawio,mermaid")
            self.assertEqual(rc, 0, output)
            out = tmp / "out"
            index = json.loads((out / "handoff.json").read_text(encoding="utf-8"))
            self.assertEqual(sorted(index["engines"]), ["drawio", "mermaid"])
            self.assertEqual(index["layout_policy"], "optimize")
            self.assertIn("element:a.box", index["dropped_geometry"])
            self.assertIn("relation:r1.via", index["dropped_geometry"])
            self.assertIn("zone:z1.box", index["dropped_geometry"])
            for engine in ("drawio", "mermaid"):
                sds = json.loads((out / f"sds-{engine}.json").read_text(encoding="utf-8"))
                dumped = json.dumps(sds, ensure_ascii=False)
                self.assertNotIn('"box"', dumped, f"{engine}: geometry leaked into the cold-start SDS")
                self.assertNotIn('"via"', dumped, f"{engine}: waypoints leaked into the cold-start SDS")
                self.assertEqual(sds["layout_policy"], "optimize")
                self.assertEqual(sds["fidelity_intent"], "reproduction")
                self.assertEqual(sds["dispatch"]["generate_geometry"], "engine")
                self.assertIn("manifest", " ".join(sds["dispatch"]["required_artifacts"]))
                self.assertEqual(len(sds["elements"]), 3)
                self.assertEqual(len(sds["relations"]), 2)


class HandoffNegatives(unittest.TestCase):
    def test_unknown_relation_endpoint_is_refused(self):
        import tempfile

        bad = json.loads(json.dumps(SEMANTICS))
        bad["relations"][0]["to"] = "does-not-exist"
        with tempfile.TemporaryDirectory() as raw:
            rc, output = run_handoff(Path(raw), bad)
            self.assertEqual(rc, 1, output)
            self.assertIn("does-not-exist", output)

    def test_duplicate_element_id_is_refused(self):
        import tempfile

        bad = json.loads(json.dumps(SEMANTICS))
        bad["elements"][1]["id"] = "a"
        with tempfile.TemporaryDirectory() as raw:
            rc, output = run_handoff(Path(raw), bad)
            self.assertEqual(rc, 1, output)
            self.assertIn("duplicate element id", output)

    def test_counts_mismatch_is_refused(self):
        import tempfile

        bad = json.loads(json.dumps(SEMANTICS))
        bad["counts"]["relations"] = 99
        with tempfile.TemporaryDirectory() as raw:
            rc, output = run_handoff(Path(raw), bad)
            self.assertEqual(rc, 1, output)
            self.assertIn("does not match", output)

    def test_unknown_engine_is_refused(self):
        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            rc, output = run_handoff(Path(raw), SEMANTICS, "--engines", "drawio,graphviz")
            self.assertEqual(rc, 2, output)
            self.assertIn("graphviz", output)

    def test_existing_outputs_are_not_overwritten(self):
        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            first, output = run_handoff(tmp, SEMANTICS, "--engines", "drawio")
            self.assertEqual(first, 0, output)
            second, output = run_handoff(tmp, SEMANTICS, "--engines", "drawio")
            self.assertEqual(second, 1, output)
            self.assertIn("refusing to overwrite", output)


if __name__ == "__main__":
    unittest.main()
