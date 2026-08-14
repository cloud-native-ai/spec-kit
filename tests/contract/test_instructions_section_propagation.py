"""Contract test: instructions section propagation (Constitution XI v1.10.0).

Guards the mechanism fixed on 2026-08-14: template sections MUST propagate
into the live instructions file. Before the fix, sections added to
``templates/instructions-template.md`` after a project's initial bootstrap
(e.g. ``## Dogfooding Practice``, ``## Spec Kit Framework Map``) never
reached the live ``.specify/instructions.md`` — the generator only rendered
the template for brand-new files and otherwise did nothing but back up.

C-1 (real-tree guard): every top-level ``##`` section heading present in the
template MUST exist verbatim in the live instructions file.
C-2 (mechanism behavior): the generator injects missing template sections
into an existing live file additively — never modifying or removing
existing sections — and is idempotent.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE = REPO_ROOT / ".specify" / "instructions.md"
GENERATOR = REPO_ROOT / "scripts" / "bash" / "generate-instructions.sh"


def _template_headings() -> list[str]:
    return re.findall(r"(?m)^## .+$", TEMPLATE.read_text(encoding="utf-8"))


@pytest.mark.contract
def test_c1_live_instructions_carry_all_template_sections():
    live = LIVE.read_text(encoding="utf-8")
    live_headings = set(re.findall(r"(?m)^## .+$", live))
    missing = [h for h in _template_headings() if h not in live_headings]
    assert not missing, (
        "live .specify/instructions.md is missing template-managed sections "
        f"(run scripts/bash/generate-instructions.sh to reconcile): {missing}"
    )


@pytest.mark.contract
def test_c2_generator_injects_missing_sections_additively(tmp_path: Path):
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "instructions-template.md").write_text(
        "# Instructions\n\n"
        "## Alpha\n\nalpha body\n\n"
        "## Beta\n\nbeta body\n\n"
        "## Gamma\n\ngamma body\n",
        encoding="utf-8",
    )
    live = tmp_path / ".specify" / "instructions.md"
    live.write_text(
        "# Instructions\n\n## Alpha\n\nalpha body (customized)\n\n"
        "## Project Custom\n\nkept section\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)

    result = subprocess.run(
        ["bash", str(GENERATOR)], cwd=tmp_path, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

    text = live.read_text(encoding="utf-8")
    # missing template sections injected
    assert "## Beta" in text and "beta body" in text
    assert "## Gamma" in text and "gamma body" in text
    # existing sections untouched (customized content + project-specific section)
    assert "alpha body (customized)" in text
    assert "## Project Custom" in text and "kept section" in text
    # injected in template order: Beta before Gamma
    assert text.index("## Beta") < text.index("## Gamma")

    # idempotent: a second run changes nothing
    before = live.read_bytes()
    subprocess.run(["bash", str(GENERATOR)], cwd=tmp_path,
                   capture_output=True, text=True, check=True)
    assert live.read_bytes() == before
