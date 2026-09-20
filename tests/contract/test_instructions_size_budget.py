"""Contract test: the instructions size budget report.

Guards the mechanism added after a real client project's run
(``/storage/project/kangaroo-xuanji/xuanji-images``, 2026-09-20) showed the
generator taking an already-over-budget instruction file from 42,673 B to
49,564 B (+16%) while printing nothing about size. The host AI agent CLI
noticed; the command that produced the file did not.

Three propositions are guarded here, and each is a *negative* one — "no
warning when under budget", "exit stays 0", "the command template does not
restate the number". Per this repo's blind-check lesson
(``docs/reference/history/00-cross-cutting-lessons.md`` § 十二) a guard of a
negative proposition is only evidence if it can be shown to fail, so the
over-budget and under-budget fixtures are deliberately a matched pair: the
same assertions that must be silent on one must fire on the other. That pair
IS the mutation drill — neither half is meaningful alone.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "scripts" / "bash" / "generate-instructions.sh"
COMMAND_TEMPLATE = REPO_ROOT / "templates" / "commands" / "instructions.md"

# The script owns the number; the test derives it rather than pinning a second
# copy (precedent: test_dogfooding_practice.py extracts the engine's action
# set the same way). A hard-coded budget here would drift the day the script's
# constant is retuned, and would then pass for the wrong reason.
_BUDGET_RE = re.compile(r"^INSTRUCTIONS_BUDGET_BYTES=(\d+)\s*$", re.M)


def _budget_bytes() -> int:
    m = _BUDGET_RE.search(GENERATOR.read_text(encoding="utf-8"))
    assert m, (
        "generate-instructions.sh no longer declares INSTRUCTIONS_BUDGET_BYTES "
        "as a top-level assignment — it is the single owner of the budget "
        "value, so this test cannot derive it"
    )
    return int(m.group(1))


def _make_project(tmp_path: Path, *, live_body: str | None) -> Path:
    """Minimal installed-project layout the generator can run against.

    Mirrors test_instructions_section_propagation.py's fixture, including the
    ``tools-utils.py`` symlink that ``refresh-tools.sh`` resolves from the
    project root.
    """
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "instructions-template.md").write_text(
        "# Instructions\n\n## Alpha\n\nalpha body\n\n## Beta\n\nbeta body\n",
        encoding="utf-8",
    )
    specify_py = tmp_path / ".specify" / "scripts" / "python"
    specify_py.mkdir(parents=True, exist_ok=True)
    (specify_py / "tools-utils.py").symlink_to(
        REPO_ROOT / "scripts" / "python" / "tools-utils.py"
    )
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    live = tmp_path / ".specify" / "instructions.md"
    if live_body is not None:
        live.write_text(live_body, encoding="utf-8")
    return live


def _run(tmp_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(GENERATOR)], cwd=tmp_path, capture_output=True, text=True
    )


def _over_budget_body(budget: int) -> str:
    """A live file whose sections are individually large enough to be ranked.

    Sized from the derived budget rather than a literal, so retuning the
    script's constant does not silently leave this fixture under budget.
    """
    names = ("Alpha", "Beta", "Recurring Operational Lessons", "Documentation Map")
    filler = "y" * 400
    rows_per = budget // (len(filler) + 40) // len(names) + 4
    body = "# Instructions\n\n"
    for name in names:
        rows = "\n".join(f"- {name} bullet {i}: {filler}" for i in range(rows_per))
        body += f"## {name}\n\n{rows}\n\n"
    assert len(body.encode()) > budget, (
        f"fixture is {len(body.encode())} B, which does not exceed the {budget} B budget"
    )
    return body


@pytest.mark.contract
def test_over_budget_warns_and_ranks_sections(tmp_path: Path):
    budget = _budget_bytes()
    live = _make_project(tmp_path, live_body=_over_budget_body(budget))

    result = _run(tmp_path)
    out = result.stdout + result.stderr
    # Measured after the run: the reconcile may itself inject a template
    # section, and the report describes the file as it now stands.
    expected = len(live.read_text(encoding="utf-8").encode())

    # Advisory by design: this script runs inside `specify init` for every
    # downstream project, so a non-zero exit would leave an over-budget project
    # unable to initialize or refresh at all.
    assert result.returncode == 0, result.stderr
    assert "has reached the" in out and "budget" in out, out
    assert str(expected) in out, f"the measured byte count {expected} was not reported: {out}"
    assert str(budget) in out, f"the budget {budget} was not reported: {out}"

    # The breakdown must name real headings, ranked. Without this the warning
    # is not actionable — "you are over" tells the operator nothing about what
    # to move, which is exactly why the original run had to improvise.
    ranked = re.findall(r"^\s+(\d+) B\s+(.+)$", out, re.M)
    assert ranked, f"no per-section breakdown was printed: {out}"
    sizes = [int(n) for n, _ in ranked]
    assert sizes == sorted(sizes, reverse=True), f"breakdown is not descending: {ranked}"
    names = {name.strip() for _, name in ranked}
    assert "Recurring Operational Lessons" in names, (
        f"the breakdown does not name the largest project-owned section: {names}"
    )


@pytest.mark.contract
def test_under_budget_reports_size_without_warning(tmp_path: Path):
    budget = _budget_bytes()
    # Carries every template section, so the reconcile injects nothing and the
    # reported size is the size this test wrote.
    live = _make_project(
        tmp_path,
        live_body="# Instructions\n\n## Alpha\n\nalpha body (customized)\n\n"
        "## Beta\n\nbeta body\n\n## Project Custom\n\nkept section\n",
    )

    result = _run(tmp_path)
    out = result.stdout + result.stderr
    expected = len(live.read_text(encoding="utf-8").encode())

    assert expected < budget, "fixture is not under budget"
    assert result.returncode == 0, result.stderr
    assert "has reached the" not in out, f"warning fired under budget: {out}"
    # Anti-vacuity sentinel: the size line must carry the file's real byte
    # count and the real headroom, so "no warning because it measured and was
    # under" stays distinguishable from "no warning because nothing measured".
    assert f"Instructions size: {expected} B" in out, out
    assert f"budget {budget} B" in out, out
    assert f"{budget - expected} B headroom" in out, out


@pytest.mark.contract
def test_new_file_branch_reports_size_too(tmp_path: Path):
    """A first-time bootstrap renders from the template and must also report."""
    live = _make_project(tmp_path, live_body=None)
    assert not live.exists()

    result = _run(tmp_path)
    out = result.stdout + result.stderr

    assert result.returncode == 0, result.stderr
    assert live.is_file(), "the generator did not render a new instructions file"
    expected = len(live.read_text(encoding="utf-8").encode())
    assert f"Instructions size: {expected} B" in out, out


@pytest.mark.contract
def test_report_is_idempotent(tmp_path: Path):
    budget = _budget_bytes()
    _make_project(tmp_path, live_body=_over_budget_body(budget))

    first = _run(tmp_path)
    second = _run(tmp_path)

    assert first.returncode == 0 and second.returncode == 0
    before = (tmp_path / ".specify" / "instructions.md").read_bytes()
    third = _run(tmp_path)
    assert third.returncode == 0
    assert (tmp_path / ".specify" / "instructions.md").read_bytes() == before, (
        "a repeated run changed the file — the budget report must be read-only"
    )

    def measured(out: str) -> str:
        m = re.search(r"Instructions size (\d+) B|size (\d+) B has reached", out)
        assert m, out
        return next(g for g in m.groups() if g)

    sizes = {measured(r.stdout + r.stderr) for r in (first, second, third)}
    assert len(sizes) == 1, f"the reported size varied across identical runs: {sizes}"


@pytest.mark.contract
def test_command_template_names_both_routes_without_restating_the_budget():
    text = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    budget = _budget_bytes()

    for needle in ("Route R1", "Route R2"):
        assert needle in text, f"{needle} is not documented in the command template"
    # R2's substance: a threshold, an owner document, and a mechanical
    # (never transcribed) migration with assertions in both directions.
    assert "4 KB" in text, "Route R2's relocation threshold is missing"
    assert "mechanical, never transcribed by hand" in text, (
        "Route R2 must require a scripted migration — hand transcription "
        "silently drops items and the drop is invisible afterwards"
    )
    # Action 6's attribution rule.
    assert "attribution" in text, "Action 6's attribution rule is missing"

    # R1's substance: the two filters that keep "live is bigger than template"
    # from being read as drift. Found by executing the route — its raw size
    # comparison flagged Documentation Map, Tech Stack & Resources and Project
    # Overview on a mature project, all three of which are scaffolds the project
    # is supposed to fill, so compressing them would have deleted real content.
    assert "Exclude project-filled sections first" in text, (
        "R1 must exclude sections whose template version is still a placeholder "
        "scaffold; without this filter R1 flags the largest correct sections in "
        "the file"
    )
    assert "not** an R1 candidate" in text, (
        "R1 must state the negative outcome of its pointer check — a section "
        "thicker because no owner holds the detail is a gap in the owner, not drift"
    )

    # One owner for the number: the command template references the script's
    # report and MUST NOT carry a second copy of the value.
    assert str(budget) not in text, (
        f"the command template restates the budget literal {budget}; the script's "
        "INSTRUCTIONS_BUDGET_BYTES is the only definition point"
    )
    assert "INSTRUCTIONS_BUDGET_BYTES" in text, (
        "the command template must name the owning constant instead of the value"
    )
