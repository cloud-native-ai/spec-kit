"""T094 — a guarded shell script's help still carries its original body.

The generator replaced every `usage()` body with a generic four-label block; the
pre-existing driver tests caught two (watch-target, stage-runner) and this guard
covers the rest: if a script defines its own `usage()`, `_sig_usage` must call it.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract
ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"

SAMPLES = {
    "skills/external/sdd-loop-driver/scripts/watch-target.sh": ["--raw-stream", "0 DONE", "15 INCOMPLETE"],
    "skills/external/sdd-loop-driver/scripts/stage-runner.sh": ["Exit code equals"],
    "skills/external/sdd-loop-driver/scripts/run-stage.sh": ["--line-id", "--registry"],
    "skills/external/draw-diagram/references/types/excalidraw/scripts/render-excalidraw.sh": ["Usage: render-excalidraw.sh"],
    "skills/internal/code-review/scripts/git-delta-review.sh": ["USAGE:"],
}


def test_every_guarded_script_with_a_usage_body_calls_it():
    for path in sorted(SKILLS.rglob("*.sh")):
        text = path.read_text(encoding="utf-8")
        if "_sig_usage" not in text or "usage() {" not in text:
            continue
        m = re.search(r"_sig_usage\(\) \{(.*?)\n\}", text, re.S)
        assert m, f"{path}: _sig_usage has no body"
        assert re.search(r"\busage\b", m.group(1)), (
            f"{path}: _sig_usage must call the script's own usage(); got:\n{m.group(1)}"
        )


@pytest.mark.parametrize("rel,tokens", sorted(SAMPLES.items()))
def test_help_still_contains_the_original_tokens(rel, tokens):
    script = ROOT / rel
    assert script.is_file(), rel
    proc = subprocess.run(["bash", str(script), "--help"], capture_output=True,
                          text=True, timeout=20, stdin=subprocess.DEVNULL)
    assert proc.returncode == 0, proc.stderr
    for token in tokens:
        assert token in proc.stdout, f"{rel}: help lost {token!r}"


def test_no_script_prints_a_doubled_label():
    for path in sorted(SKILLS.rglob("*.sh")):
        text = path.read_text(encoding="utf-8")
        if "_sig_usage" not in text:
            continue
        proc = subprocess.run(["bash", str(path), "--help"], capture_output=True,
                              text=True, timeout=20, stdin=subprocess.DEVNULL)
        if proc.returncode != 0:
            continue
        assert "side-effects: side-effects:" not in proc.stdout, f"{path}: doubled side-effects label"
        assert "exit-codes: exit-codes:" not in proc.stdout, f"{path}: doubled exit-codes label"
