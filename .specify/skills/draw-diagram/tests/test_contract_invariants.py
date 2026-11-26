"""Contract invariants for the draw-diagram improvement rounds (2026-11-25).

Positive cases: the front-door branches, geometry ownership split, executable
layer (handoff + manifest checker) exist and are wired to their owners.
Negative cases: retired wording must not come back; no engine may carry this
case's instance statistics as generic limits.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/tests/test_contract_invariants.py -q
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = SKILL_ROOT / "SKILL.md"
ROUTING = SKILL_ROOT / "references" / "routing-matrix.md"
SEMANTIC = SKILL_ROOT / "references" / "semantic-model.md"
QUALITY = SKILL_ROOT / "references" / "quality-gate.md"
SCRIPTS = SKILL_ROOT / "scripts"
ENGINES = ("d3js", "drawio", "echarts", "excalidraw", "mermaid", "plantuml")

# Instance statistics from the six-engine comparison run (82 elements / 24 zones /
# 46 relations). They belong to that run's acceptance record, never to the generic
# engine entries — a number frozen here becomes a fake universal standard.
INSTANCE_STATISTICS = ("82/24/46", "R01–R46", "32 次交叉", "66 处", "62px", "100px 共线", "14px 误差", "> 8px")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FrontDoorInvariants(unittest.TestCase):
    def test_comparison_mode_has_executable_entry(self):
        skill = _read(SKILL)
        routing = _read(ROUTING)
        self.assertIn("比较/探索模式先行", skill)
        self.assertIn("§5", skill)
        self.assertIn("## 5. 比较模式", routing)
        self.assertIn("独占登记不排斥比较", skill)

    def test_comparison_does_not_unify_styles_or_rank_crossings(self):
        routing = _read(ROUTING)
        self.assertIn("不做跨引擎样式统一", routing)
        self.assertIn("不把线宽/字号/交叉数等异口径数字排成统一名次", routing)

    def test_geometry_ownership_split(self):
        skill = _read(SKILL)
        semantic = _read(SEMANTIC)
        self.assertIn("`optimize`（仅用户明示授权）", skill)
        self.assertIn("## 几何归属", semantic)
        self.assertIn("不含元素 box", semantic)
        self.assertIn("不得把 `reproduction` 偷换成 `fresh`", semantic)


class ExecutableLayerInvariants(unittest.TestCase):
    def test_quality_gate_owner_is_wired(self):
        self.assertTrue(QUALITY.is_file(), "references/quality-gate.md is missing")
        quality = _read(QUALITY)
        for needle in (
            "## 最小质量门",
            "## 硬失败与返修",
            "## 结果 manifest",
            "user_evaluation",
            "layout_policy",
            "hard_failures",
            "check-manifest.py",
            "handoff.py",
            "输入回显",
        ):
            self.assertIn(needle, quality)
        self.assertIn("[./references/quality-gate.md](./references/quality-gate.md)", _read(SKILL))
        self.assertIn("[quality-gate.md](quality-gate.md)", _read(ROUTING))

    def test_manifest_checker_refuses_echo_and_requires_native_recount(self):
        quality = _read(QUALITY)
        self.assertIn("ldm_sha256 == source.sha256", quality)
        self.assertIn("native_recount", quality)
        self.assertIn("not_supported", quality)

    def test_scripts_answer_help_and_version(self):
        for name in ("check-manifest.py", "handoff.py"):
            script = SCRIPTS / name
            self.assertTrue(script.is_file(), f"missing executable: scripts/{name}")
            for flag in ("--help", "--version"):
                proc = subprocess.run(
                    [sys.executable, str(script), flag],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                self.assertEqual(proc.returncode, 0, f"{name} {flag} failed: {proc.stderr}")

    def test_scripts_reject_undeclared_options(self):
        for name in ("check-manifest.py", "handoff.py"):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / name), "--definitely-not-an-option"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(proc.returncode, 2, f"{name} must reject undeclared options with exit 2")


class NoEvaluationInvariants(unittest.TestCase):
    def test_no_evaluation_is_not_satisfaction(self):
        skill = _read(SKILL)
        self.assertIn("无评价 = 未评价", skill)
        self.assertNotIn("视为本次绘制满意", skill)
        # Negative: the retired sentence must not reappear in any wording
        self.assertNotIn("即视为本次绘制满意", skill)


class EngineEntryInvariants(unittest.TestCase):
    def test_each_engine_carries_limits_gate_pointer_and_shortest_path(self):
        for engine in ENGINES:
            path = SKILL_ROOT / "references" / "types" / engine / f"{engine}.md"
            text = _read(path)
            self.assertIn("返修判据", text, f"{engine}: missing evidence-based limits section")
            self.assertIn(
                "[quality-gate.md](../../quality-gate.md)",
                text,
                f"{engine}: missing pointer to the quality gate",
            )
            self.assertIn("最短可运行链路", text, f"{engine}: missing shortest runnable path")

    def test_engine_entries_carry_no_instance_statistics(self):
        """The six-engine run's numbers stay in that run's acceptance record."""
        for engine in ENGINES:
            path = SKILL_ROOT / "references" / "types" / engine / f"{engine}.md"
            text = _read(path)
            for marker in INSTANCE_STATISTICS:
                self.assertNotIn(
                    marker,
                    text,
                    f"{engine}: instance statistic {marker!r} frozen into the generic entry; "
                    "move it to the run's acceptance record",
                )


if __name__ == "__main__":
    unittest.main()
