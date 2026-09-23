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

# The report's table shape. One row per top-level section, six columns — the
# columns /speckit.instructions Action 2 consumes as its observation snapshot
# and Routes R1/R2 take their candidates from. Pinned by shape rather than by
# width so re-aligning the columns cannot silently un-pin the contract.
ROW_RE = re.compile(
    r"^\|\s*(?P<section>.+?)\s*"
    r"\|\s*(?P<live>\d+)\s*"
    r"\|\s*(?P<template>\d+)\s*"
    r"\|\s*(?P<delta>[+-]?\d+)\s*"
    r"\|\s*(?P<placeholder>yes|no)\s*"
    r"\|\s*(?P<owned>yes|no)\s*\|$"
)
HEADER_COLUMNS = ("section", "live B", "tmpl B", "delta", "placeholder", "project-owned")

# A template whose sections exercise all three classifications the table exists
# to make: finished normative prose (an R1 candidate), a placeholder scaffold
# (R1-excluded — the project is supposed to fill it), and a Markdown link (must
# NOT read as a placeholder, or a real R1 candidate hides behind the filter).
PLACEHOLDER_TEMPLATE = (
    "# Instructions\n\n"
    "## Alpha\n\nalpha body\n\n"
    "## Beta\n\nbeta body\n\n"
    "## Project Notes\n\n[Detected notes from the codebase]\n\n"
    "## Linked Section\n\nSee [the owner document](shared/definitions/x.md).\n"
)
CLASSIFIED_LIVE = (
    "# Instructions\n\n"
    "## Alpha\n\nalpha body (customized)\n\n"
    "## Beta\n\nbeta body\n\n"
    "## Project Notes\n\nthe project filled this scaffold in\n\n"
    "## Linked Section\n\nSee [the owner document](shared/definitions/x.md).\n\n"
    "## Recurring Operational Lessons\n\n- lesson one\n"
)


def _budget_bytes() -> int:
    m = _BUDGET_RE.search(GENERATOR.read_text(encoding="utf-8"))
    assert m, (
        "generate-instructions.sh no longer declares INSTRUCTIONS_BUDGET_BYTES "
        "as a top-level assignment — it is the single owner of the budget "
        "value, so this test cannot derive it"
    )
    return int(m.group(1))


def _rows(out: str) -> list[dict]:
    """Parse the emitted table. Anti-vacuity is the caller's job: every test
    that reads rows asserts the row set is non-empty first."""
    return [m.groupdict() for m in (ROW_RE.match(ln.strip()) for ln in out.splitlines()) if m]


def _by_section(out: str) -> dict:
    return {r["section"]: r for r in _rows(out)}


def _make_project(
    tmp_path: Path, *, live_body: str | None, template_body: str | None = None
) -> Path:
    """Minimal installed-project layout the generator can run against.

    Mirrors test_instructions_section_propagation.py's fixture, including the
    ``tools-utils.py`` symlink that ``refresh-tools.sh`` resolves from the
    project root.
    """
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "instructions-template.md").write_text(
        template_body
        or "# Instructions\n\n## Alpha\n\nalpha body\n\n## Beta\n\nbeta body\n",
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


def _run_captured(tmp_path: Path) -> str:
    result = _run(tmp_path)
    assert result.returncode == 0, result.stderr
    return result.stdout + result.stderr


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

    # The breakdown must name real headings, ranked, and must classify each one
    # — without the classification the warning is not actionable: "you are over"
    # tells the operator nothing about what to move, which is exactly why the
    # original run had to improvise (and why R1 and R2 each re-derived the same
    # facts a second time).
    rows = _rows(out)
    assert rows, f"no section table was printed: {out}"
    sizes = [int(r["live"]) for r in rows]
    assert sizes == sorted(sizes, reverse=True), f"table is not descending: {rows}"
    by_section = {r["section"]: r for r in rows}
    assert "Recurring Operational Lessons" in by_section, (
        f"the table does not name the largest project-owned section: {sorted(by_section)}"
    )
    largest = by_section["Recurring Operational Lessons"]
    assert largest["owned"] == "yes" and largest["template"] == "0", (
        f"a heading the template lacks must be classified project-owned with zero "
        f"template bytes, otherwise Route R2 cannot find its candidates: {largest}"
    )
    assert largest["placeholder"] == "no", (
        "a project-owned section has no template version, so it can carry no "
        f"template placeholder: {largest}"
    )
    # The over-budget warning still names the trigger, and the table follows it.
    assert out.index("has reached the") < out.index("| section"), out


@pytest.mark.contract
def test_table_is_emitted_under_budget_too(tmp_path: Path):
    """Action 2 consumes the table as its observation snapshot on *every* refresh,
    not only when the file is over budget — a table that appears only on the
    over-budget path would leave the under-budget run measuring by eye again."""
    budget = _budget_bytes()
    live = _make_project(tmp_path, live_body=CLASSIFIED_LIVE, template_body=PLACEHOLDER_TEMPLATE)

    out = _run_captured(tmp_path)
    assert len(live.read_text(encoding="utf-8").encode()) < budget, "fixture is not under budget"
    assert "has reached the" not in out, f"warning fired under budget: {out}"
    assert _rows(out), f"the table was suppressed under budget: {out}"


@pytest.mark.contract
def test_table_carries_the_six_columns_and_classifies_all_three_kinds(tmp_path: Path):
    """The three classifications Route R1/R2 branch on, from one fixture.

    Negative propositions here (``placeholder == no`` twice) are the reason the
    Markdown-link row exists: a link is ``[``+``]`` too, and counting it as an
    unfilled scaffold would silently drop a genuine R1 candidate behind the
    filter. Both ``no`` rows are matched pairs against the ``yes`` row.
    """
    _make_project(tmp_path, live_body=CLASSIFIED_LIVE, template_body=PLACEHOLDER_TEMPLATE)

    out = _run_captured(tmp_path)
    header = next((ln for ln in out.splitlines() if ln.strip().startswith("| section")), None)
    assert header, f"the table header row is missing: {out}"
    for column in HEADER_COLUMNS:
        assert column in header, f"column {column!r} missing from the header: {header}"

    rows = _by_section(out)
    assert rows, f"no rows parsed: {out}"
    # Anti-vacuity sentinel: the fixture has a preamble plus five `## ` sections.
    # A parser that silently matched one row would make every lookup below a
    # KeyError instead of a verdict, and a table that dropped rows would pass.
    assert len(rows) >= 6, f"expected the fixture's 6 rows, parsed {sorted(rows)}"

    # (1) template-owned finished prose — an R1 candidate.
    assert rows["Alpha"]["owned"] == "no" and rows["Alpha"]["placeholder"] == "no", rows["Alpha"]
    assert int(rows["Alpha"]["template"]) > 0, rows["Alpha"]
    # (2) template-owned placeholder scaffold — R1-excluded.
    assert rows["Project Notes"]["placeholder"] == "yes", (
        f"a template section still carrying a bracket token must be marked: {rows['Project Notes']}"
    )
    assert rows["Project Notes"]["owned"] == "no", rows["Project Notes"]
    # (3) project-owned — Route R2's pool.
    assert rows["Recurring Operational Lessons"]["owned"] == "yes", rows
    # The link row is the negative control for (2).
    assert rows["Linked Section"]["placeholder"] == "no", (
        "a Markdown link was counted as an unfilled placeholder, which hides a "
        f"real Route R1 candidate: {rows['Linked Section']}"
    )
    assert rows["Linked Section"]["owned"] == "no", rows["Linked Section"]

    # delta is derived, so it must agree with the two columns it is derived from
    # on every row — a stale delta is worse than none, because R1 ranks by it.
    for name, row in rows.items():
        assert int(row["delta"]) == int(row["live"]) - int(row["template"]), (
            f"{name}: delta {row['delta']} != live {row['live']} - template {row['template']}"
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


# --------------------------------------------------------------------------------------
# The command side of the same contract: the table the script emits has to be *consumed*
# as an artifact. Every assertion below is scoped to the one line that carries the rule,
# because "the phrase appears somewhere in a 200-line command" is a pin that keeps
# passing after the rule has drifted out of the step that needs it.
# --------------------------------------------------------------------------------------

ARTIFACT_COMMIT_PEER = REPO_ROOT / "templates" / "commands" / "requirements.md"


def _line(text: str, marker: str) -> str:
    """The single line carrying ``marker``. Bullets in this template are one line
    each; a second match means the rule was restated, which is itself the defect."""
    hits = [ln for ln in text.splitlines() if marker in ln]
    assert len(hits) == 1, f"expected exactly one line carrying {marker!r}, got {len(hits)}"
    return hits[0]


def _section(text: str, heading: str, end: str) -> str:
    i = text.index(heading)
    j = text.index(end, i)
    assert j > i, f"{end!r} does not follow {heading!r}"
    return text[i:j]


@pytest.mark.contract
def test_action_2_consumes_the_script_table_as_the_observation_snapshot():
    """F-11②: the snapshot is a transcription of the script's table plus one
    agent-supplied column. Without this the sizes and both classifications get
    re-derived by eye, and R1/R2 each derive them a third and fourth time."""
    text = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    inventory = _line(text, "**Inventory sections (mandatory artifact — observation snapshot)**")

    assert "Action 1's section table" in inventory, (
        "Action 2 must name the script's table as the snapshot's source"
    )
    assert "never by re-measuring the file by eye" in inventory
    for column in HEADER_COLUMNS:
        assert column in inventory, (
            f"Action 2 does not carry the table's {column!r} column, so the step "
            "cannot be checked against the table it claims to consume"
        )
    # The route-candidate claim: R1/R2 draw from the snapshot and nothing else.
    assert "only** from it" in inventory, (
        "Action 2 must state that Routes R1/R2 take their candidates only from the "
        "snapshot — otherwise the filter is advisory and the routes re-derive it"
    )
    # The one column the script cannot supply stays the agent's job.
    assert "hand-authored / non-reproducible" in inventory


@pytest.mark.contract
def test_r1_opens_with_the_machine_checked_filter():
    """F-11③: the placeholder filter is the route's first act and reads a column,
    so it cannot be skipped by starting from a size-ranked shortlist."""
    text = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    r1 = _line(text, "- **Route R1 —")

    assert "Filter before reading any prose" in r1
    assert "`placeholder=yes`" in r1 and "`project-owned=yes`" in r1
    assert "machine-checked columns of the script's table" in r1, (
        "R1 must name the filter as a lookup on the script's columns, not a judgement"
    )
    # The discriminator itself, stated mechanically.
    assert "{{VAR}}" in r1
    # Ordering is the substance: filter first, pool second.
    assert r1.index("Filter before reading any prose") < r1.index("candidate pool"), (
        "R1 must filter before it forms the candidate pool"
    )
    assert "largest `delta` first" in r1, "R1 must rank by the table's delta column"


@pytest.mark.contract
def test_r2_reads_its_pool_from_the_project_owned_column():
    text = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    r2 = _line(text, "- **Route R2 —")
    assert "`project-owned=yes`" in r2, (
        "Route R2's pool is the table's project-owned rows; re-deriving it from "
        "'headings the template lacks' is the second derivation F-11 removes"
    )


@pytest.mark.contract
def test_action_3_carries_the_backup_retention_rule():
    """F-11⑤: which backups are still load-bearing, and where the rest are named.

    The keep-set literal (``newest 5``) is pinned here deliberately — the command
    template is its only definition point, and a silent retune should fail a test
    rather than pass unnoticed.
    """
    text = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    retention = _line(text, "**Backup retention rule**")

    assert "keep-set" in retention
    assert "newest 5" in retention
    assert "absent from the live file" in retention, (
        "a backup still holding an unrecovered heading must stay in the keep-set "
        "however old it is — that is the half of the rule that prevents data loss"
    )
    assert "residual report" in retention, "the complement must be named in the report"
    assert "prunable set" in retention
    # Non-destructive: the command names the prunable set, it does not prune.
    assert "never removes a backup itself" in retention, (
        "pruning backups is a destructive action this command does not carry; "
        "dropping this clause would turn a report line into a deletion"
    )
    # Action 7 is the slot the naming lands in, and it points back rather than
    # restating the rule.
    report_slot = _line(text, "**Name the prunable backups**")
    assert "Action 3" in report_slot, (
        "Action 7 must reach the retention rule by reference — restating it would "
        "give the keep-set two owners"
    )


@pytest.mark.contract
def test_command_template_embeds_artifact_commit_in_the_shared_pointer_form():
    """F-11④: instructions.md was the sixth artifact-producing command and the
    only one without the step. Pinned by *identity* with a peer carrier, because
    the owner is `.specify/shared/workflow/artifact-commit-step.md` — a per-command
    restatement of its rules is exactly the drift the owner exists to prevent."""
    text = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    assert "## Artifact Commit" in text, "the Artifact Commit step is missing"
    assert text.index("## Documentation") < text.index("## Artifact Commit") < text.index(
        "## Handoffs"
    ), "Artifact Commit must sit in the same slot the peer commands use"

    mine = _section(text, "## Artifact Commit", "## Handoffs")
    peer = _section(
        ARTIFACT_COMMIT_PEER.read_text(encoding="utf-8"), "## Artifact Commit", "## Handoffs"
    )
    assert mine == peer, (
        "instructions.md's Artifact Commit section diverged from the shared pointer "
        "form carried by the other artifact-producing commands"
    )
    assert "artifact-commit-step.md" in mine, "the pointer to the owner is missing"
    assert "git add -A" in mine, "the never-`git add -A` reminder is missing"
