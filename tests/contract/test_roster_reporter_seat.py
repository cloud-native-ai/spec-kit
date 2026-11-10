"""Contract test: the reporter seat and its roster guard (087, T011 — US1).

Layer-2 of the Feature 087 test map. This file owns the assertions over the seat half of
``contracts/reporter-seat.contract.md``: the guard script ``skills/internal/create-team/scripts/validate-roster.py``
(RS-03 C-16, RS-04 C-17, RS-08 C-21), the team-schema discriminator the seat is expressed with (RS-02 C-15) and the
runtime-omission condition (RS-05 C-18).

**Clause partition**: this file is responsible for clauses **C-14 … C-21** in total, across the rows that write it.
Its own green point is C-16 (the named-defect clause). C-19 (the Template's authority deny-list) and C-20 (the
Template's by-anchor dispatch-injection duties) are asserted here over the Template file and turned green by T014 /
T051 respectively; C-14's frontmatter key set is asserted here, while its mirror-file existence and byte-equality
reading are asserted by ``test_reporting_obligations.py`` (T012).

**Red-first (Constitution IV)**: authored before T013 (the guard script) and T014 (the Template) exist. Every test
asserts its artifact path first, so red is "artifact missing", never an ``ImportError`` or a collection error. The
verbose sub-test split a red-first file would normally show is deliberately not used: a test that imports the
missing module would error at collection and prove nothing about the missing implementation.

**What this file deliberately does NOT assert**: the seat's runtime rendering, the digest, the guard's thirteen
propositions, and the owner document. Those belong to their own rows.
"""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process
import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
GUARD = REPO_ROOT / "skills" / "internal" / "create-team" / "scripts" / "validate-roster.py"
CREATE_MODE = REPO_ROOT / "skills" / "internal" / "create-team" / "references" / "create-mode.md"
SKILL = REPO_ROOT / "skills" / "internal" / "create-team" / "SKILL.md"
TEMPLATE = REPO_ROOT / "agents" / "reporter.agent.md"
TEMPLATE_MIRROR = REPO_ROOT / ".specify" / "agents" / "templates" / "reporter.agent.md"

#: The seat literal contract C-16 fixes; a defect line MUST name it.
SEAT_LITERAL = "reporter"

#: The three named defects of the closed set (C-16) — one name per class, distinctly detectable.
DEFECT_ABSENT = "absent-seat"
DEFECT_UNRESOLVABLE = "unresolvable-agent"
DEFECT_TWO_SEATS = "two-seats"

#: The recorded-reason closed set (C-17).
REASONS = ("all-lanes-in-session-single-interval", "host-cannot-host-reporter")

#: The neutral sibling keys contract C-14 enumerates, plus the two framework assembly keys the siblings carry.
REQUIRED_KEYS = (
    "name",
    "description",
    "user-invocable",
    "model-tier",
    "capability-tools",
    "skills",
    "run-turn-budget",
    "display-color",
)

#: Contract C-19's deny list: no tool that dispatches, launches a process, authorizes, retries or terminates.
DENIED_TOOLS = ("Agent", "Task", "Bash", "Kill", "Retry", "Approve", "Dispatch", "Workflow")


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
def _team_md(slug: str = "fixture-team", members: str = "", config: str = "") -> str:
    """A minimal but schema-shaped roster: frontmatter + the persisted sections the schema requires."""
    return (
        "---\n"
        "name: Fixture Team\n"
        "slug: %s\n"
        "description: A roster fixture for the reporter-seat guard.\n"
        "goal: prove the seat guard judges the closed defect set.\n"
        "pattern: parallel\n"
        "created: 2026-11-06\n"
        "updated: 2026-11-06\n"
        "members:\n"
        "%s"
        "config:\n"
        "%s"
        "---\n"
        "\n"
        "## Goal\n\nFixture goal.\n\n"
        "## Static Structure\n\nRoster table.\n\n"
        "## Dynamic Structure\n\nPattern description.\n\n"
        "## Self-Improvement Contract\n\n- Subject: this fixture.\n"
        % (slug, members, config or "  parallelism: 1\n")
    )


SEAT_MEMBER = (
    "  - agent: reporter\n"
    "    role: reporter\n"
    "    lifecycle: persistent\n"
    "    reporting-territory:\n"
    "      read: [\".specify/teams/fixture-team/**\"]\n"
    "      write: [\".specify/teams/fixture-team/runs/status.live.log\"]\n"
    "    reporting-cadence: default\n"
)

WORKER_MEMBER = (
    "  - agent: skill-verifier\n"
    "    role: verifier\n"
    "    lifecycle: temporary\n"
)


def _write_team(tmp_path: Path, slug: str = "fixture-team", members: str = "", config: str = "") -> Path:
    team_dir = tmp_path / slug
    team_dir.mkdir(parents=True, exist_ok=True)
    path = team_dir / "team.md"
    path.write_text(_team_md(slug, members, config), encoding="utf-8")
    return path


def _run_guard(path: Path, *extra) -> subprocess.CompletedProcess:
    assert GUARD.is_file(), (
        "roster guard missing: %s — expected at T013 (087). Red is the intended pre-implementation"
        " state for T011." % GUARD.relative_to(REPO_ROOT)
    )
    return run_engine_in_process(GUARD, [str(path), *extra])


def _read(path: Path) -> str:
    assert path.is_file(), "expected artifact missing: %s" % path.relative_to(REPO_ROOT)
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# C-16 / RS-03 — the closed defect set, one exact named-defect text per class
# --------------------------------------------------------------------------- #
def test_compliant_roster_passes_with_exit_zero(tmp_path):
    """A roster carrying one reporter seat is conforming: exit 0, no defect line."""
    roster = _write_team(tmp_path, members=WORKER_MEMBER + SEAT_MEMBER)
    proc = _run_guard(roster)

    assert proc.returncode == 0, (
        "a roster with exactly one role: reporter member must be conforming; rc=%s "
        "stdout=%r stderr=%r" % (proc.returncode, proc.stdout, proc.stderr)
    )
    assert DEFECT_ABSENT not in proc.stdout
    assert DEFECT_TWO_SEATS not in proc.stdout


def test_absent_seat_is_a_named_defect(tmp_path):
    """No ``role: reporter`` member → exit 1 and a single line naming ``reporter`` and the team slug."""
    roster = _write_team(tmp_path, members=WORKER_MEMBER)
    proc = _run_guard(roster)

    assert proc.returncode == 1, "a missing seat must exit 1; rc=%s" % proc.returncode
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    assert len(lines) == 1, "a named defect is exactly one line; got %r" % (lines,)
    defect = lines[0]
    assert DEFECT_ABSENT in defect, (
        "the absent-seat defect must be named %r so a caller can tell it from the other two; got %r"
        % (DEFECT_ABSENT, defect)
    )
    assert SEAT_LITERAL in defect, "the defect must name the seat literal %r" % SEAT_LITERAL
    assert "fixture-team" in defect, "the defect must name the team slug; got %r" % defect


def test_unresolvable_agent_is_a_named_defect(tmp_path):
    """The seat's agent resolves to neither the shipped template nor a seat instance → its own named defect."""
    unresolvable = SEAT_MEMBER.replace("agent: reporter", "agent: no-such-reporter-template")
    roster = _write_team(tmp_path, members=WORKER_MEMBER + unresolvable)
    proc = _run_guard(roster)

    assert proc.returncode == 1, "an unresolvable seat must exit 1; rc=%s" % proc.returncode
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    assert len(lines) == 1, "a named defect is exactly one line; got %r" % (lines,)
    defect = lines[0]
    assert DEFECT_UNRESOLVABLE in defect, (
        "the unresolvable-agent defect must be named %r; got %r" % (DEFECT_UNRESOLVABLE, defect)
    )
    assert SEAT_LITERAL in defect and "fixture-team" in defect


def test_two_reporter_seats_are_a_named_defect_not_a_pass(tmp_path):
    """Two ``role: reporter`` members is the seat's cardinality defect, not a pass (data-model E1, INV-03)."""
    roster = _write_team(tmp_path, members=WORKER_MEMBER + SEAT_MEMBER + SEAT_MEMBER)
    proc = _run_guard(roster)

    assert proc.returncode == 1, (
        "a two-seat roster must be a defect, never a pass; rc=%s stdout=%r"
        % (proc.returncode, proc.stdout)
    )
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    assert len(lines) == 1, "a named defect is exactly one line; got %r" % (lines,)
    defect = lines[0]
    assert DEFECT_TWO_SEATS in defect, (
        "the two-seats defect must be named %r; got %r" % (DEFECT_TWO_SEATS, defect)
    )
    assert SEAT_LITERAL in defect and "fixture-team" in defect


def test_the_three_defect_names_are_distinct(tmp_path):
    """The set is closed and each member is detectable apart from the others (C-16 §3)."""
    absent = _run_guard(_write_team(tmp_path / "a", slug="team-a", members=WORKER_MEMBER)).stdout
    unresolvable = _run_guard(
        _write_team(
            tmp_path / "b",
            slug="team-b",
            members=WORKER_MEMBER
            + SEAT_MEMBER.replace("agent: reporter", "agent: nope-template"),
        )
    ).stdout
    two = _run_guard(
        _write_team(tmp_path / "c", slug="team-c", members=WORKER_MEMBER + SEAT_MEMBER + SEAT_MEMBER)
    ).stdout
    readings = {
        DEFECT_ABSENT: absent,
        DEFECT_UNRESOLVABLE: unresolvable,
        DEFECT_TWO_SEATS: two,
    }
    for name, output in readings.items():
        assert name in output, "defect %r is not named in its own fixture output %r" % (name, output)
        others = [other for other in readings if other != name]
        assert not any(other in output for other in others), (
            "defect %r also carries %r; the three classes must stay tellable apart"
            % (name, [other for other in others if other in output])
        )


def test_input_error_exits_two(tmp_path):
    """A missing file is an input error (exit 2), never a named defect (exit 1)."""
    missing = tmp_path / "no-such-team" / "team.md"
    proc = _run_guard(missing)
    assert proc.returncode == 2, (
        "an unreadable input must exit 2; rc=%s stdout=%r stderr=%r"
        % (proc.returncode, proc.stdout, proc.stderr)
    )


def test_the_defect_set_is_closed_at_three_names():
    """The script's defect-name vocabulary is exactly the three C-16 names plus the reason-value defect."""
    text = _read(GUARD)
    names = set(re.findall(r"(?:DEFECT_[A-Z_]+)\s*=\s*[\"']([a-z0-9-]+)[\"']", text))
    assert {DEFECT_ABSENT, DEFECT_UNRESOLVABLE, DEFECT_TWO_SEATS} <= names, (
        "the guard must declare its defect names as constants; found %r" % (sorted(names),)
    )
    structural = set(names)
    extra = structural - {
        DEFECT_ABSENT,
        DEFECT_UNRESOLVABLE,
        DEFECT_TWO_SEATS,
        "out-of-domain-reason",
    }
    assert not extra, (
        "a fourth structural defect class was added; C-16 closes the set at three names"
        " (the reason-domain defect is RS-04's). Extra: %r" % (sorted(extra),)
    )


# --------------------------------------------------------------------------- #
# C-17 / RS-04 — the recorded reason: accepted, echoed, and its domain closed
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("reason", REASONS)
def test_recorded_reason_is_conforming_and_echoed(tmp_path, reason):
    """Either accepted reason judges the roster conforming and is echoed so a reader sees it."""
    config = "  parallelism: 1\n  reporting-reason: %s\n" % reason
    roster = _write_team(tmp_path, members=WORKER_MEMBER, config=config)
    proc = _run_guard(roster)

    assert proc.returncode == 0, (
        "a recorded reason %r must be conforming; rc=%s stdout=%r" % (reason, proc.returncode, proc.stdout)
    )
    assert reason in proc.stdout, (
        "the guard must echo the recorded reason so a recorded omission is distinguishable from a"
        " forgotten seat; got %r" % proc.stdout
    )


def test_out_of_domain_reason_is_a_named_defect(tmp_path):
    """A ``reporting-reason`` outside the closed set is a defect of its own, not a pass."""
    config = "  parallelism: 1\n  reporting-reason: we-did-not-want-one\n"
    roster = _write_team(tmp_path, members=WORKER_MEMBER, config=config)
    proc = _run_guard(roster)

    assert proc.returncode == 1, (
        "an out-of-domain reason must be a defect; rc=%s stdout=%r" % (proc.returncode, proc.stdout)
    )
    defect = proc.stdout.strip()
    assert "out-of-domain-reason" in defect, (
        "the out-of-domain-reason defect must name itself; got %r" % defect
    )
    assert "we-did-not-want-one" in defect, (
        "the defect must echo the offending value so a reader can see what was recorded; got %r" % defect
    )


# --------------------------------------------------------------------------- #
# C-18 / RS-05 — the runtime-omission condition is exactly FR-021's, both conjuncts
# --------------------------------------------------------------------------- #
def test_runtime_omission_condition_states_both_conjuncts():
    """Every lane executed by the current session, AND the whole run inside one cadence interval."""
    text = _read(CREATE_MODE)
    lowered = text.lower()
    assert "all-lanes-in-session-single-interval" in text, (
        "the schema must name the reason value the condition records"
    )
    conjunct_one = (
        "every lane" in lowered
        or "all lanes" in lowered
        or "全部 lane" in text
        or "每个 lane" in text
    )
    assert conjunct_one, (
        "the first conjunct (every lane executed by the current session) must be stated"
    )
    conjunct_two = (
        "one cadence interval" in lowered
        or "inside one cadence" in lowered
        or "一个周期间隔内" in text
        or "单个周期间隔" in text
    )
    assert conjunct_two, (
        "the second conjunct (the whole run expected to finish inside one cadence interval) must be stated"
    )


def test_runtime_omission_states_the_consequence():
    """Under the condition the orchestrating session carries the reporting duty itself."""
    text = _read(CREATE_MODE).lower()
    assert (
        "orchestrating session carries" in text
        or "carries the reporting duty itself" in text
        or "编排会话自己承担汇报职责" in text
        or "编排会话承担" in text
    ), "the schema must state that the orchestrating session then carries the reporting duty itself"


def test_runtime_omission_condition_is_not_widened():
    """Two conjunctive facts, not a per-team judgement — the 'and' form is explicit."""
    text = _read(CREATE_MODE)
    lowered = text.lower()
    assert "and" in lowered or "且" in text, "the two conjuncts must be joined conjunctively"
    assert "must not be widened" in lowered or "不得放宽" in text or "MUST NOT 被按队伍逐个判断放宽" in text, (
        "the condition must state that it is not widened by a per-team judgement"
    )


# --------------------------------------------------------------------------- #
# C-15 / RS-02 — the seat is a members[] row, and no parallel ``reporter:`` key exists
# --------------------------------------------------------------------------- #
def test_team_schema_keeps_members_and_adds_the_reporter_discriminator():
    """``members[]`` stays the one expression point; ``role: reporter`` is the discriminator."""
    text = _read(CREATE_MODE)
    assert "members:" in text, "the team schema must keep its members block"
    assert "role: reporter" in text, (
        "the schema must state the discriminator literally as `role: reporter`"
    )


def test_team_schema_carries_the_two_seat_specific_keys():
    """``reporting-territory`` (read + write lists) and ``reporting-cadence`` appear in the schema."""
    text = _read(CREATE_MODE)
    assert "reporting-territory" in text, "the seat's territory key must appear in the schema"
    assert "reporting-cadence" in text, "the seat's cadence key must appear in the schema"
    seat_block = _section(text, "reporting-territory")
    assert "read" in seat_block and "write" in seat_block, (
        "the territory key must be declared as a read list plus a write list"
    )


def test_no_parallel_reporter_key_is_introduced():
    """A top-level ``reporter:`` block would be a second place roster membership is expressed (C-15).

    The scan is scoped to the persisted-schema code block: prose elsewhere in the file may legitimately write
    ``reporter:`` inside a sentence, and a scan that flags prose would force the prose to avoid the word rather than
    judge the schema.
    """
    schema = _schema_block(_read(CREATE_MODE))
    assert schema, "sanity: the persisted `team.md` schema block must be locatable"
    offenders = [line for line in schema.splitlines() if re.match(r"^reporter:\s*(\S.*)?$", line)]
    assert not offenders, (
        "the schema must not introduce a parallel top-level `reporter:` key; found %r" % (offenders,)
    )


# --------------------------------------------------------------------------- #
# C-14 / RS-01 — the Template's frontmatter key set
# --------------------------------------------------------------------------- #
def test_reporter_template_carries_the_neutral_key_set():
    """The Template declares the neutral sibling keys, and it is a dispatched seat, not a user command."""
    text = _read(TEMPLATE)
    parts = text.split("---", 2)
    assert len(parts) >= 3, "the Template must open with a YAML frontmatter block"
    frontmatter = parts[1]
    for key in REQUIRED_KEYS:
        assert re.search(r"^%s:" % re.escape(key), frontmatter, re.M), (
            "the reporter Template must carry the neutral key %r its siblings carry (C-14)" % key
        )
    assert re.search(r"^user-invocable:\s*false\s*$", frontmatter, re.M), (
        "a seat is dispatched, not invoked by a user: user-invocable MUST be false"
    )


def test_reporter_template_declares_the_dispatch_injection_duties():
    """The seat is itself dispatchable, so it carries the paired-delimiter clause its siblings carry."""
    text = _read(TEMPLATE)
    assert text.count("<!-- fast-fail-clause:begin -->") == 1, (
        "the Template must carry exactly one fast-fail clause block (the owner literal, re-filled not edited)"
    )
    assert text.count("<!-- fast-fail-clause:end -->") == 1


# --------------------------------------------------------------------------- #
# C-19 / RS-06 — the Template's authority is read + write-own-stream, and nothing else
# --------------------------------------------------------------------------- #
def test_reporter_template_capability_tools_pass_the_deny_list():
    """No dispatch, spawn, authorize, retry or terminate tool reaches a reporter seat."""
    text = _read(TEMPLATE)
    frontmatter = text.split("---", 2)[1]
    match = re.search(r"^capability-tools:\s*\[(.*?)\]", frontmatter, re.M | re.S)
    assert match, "the Template must declare capability-tools as a list"
    tools = [item.strip() for item in match.group(1).split(",") if item.strip()]
    denied = [tool for tool in tools if tool in DENIED_TOOLS]
    assert not denied, (
        "a reporter observes and reports; these tools would give it dispatch/authority power: %r"
        % (denied,)
    )
    assert "Read" in tools, "the reporter must at least be able to read the state it reports"


def test_reporter_template_states_the_observe_and_report_boundary():
    """The body carries the boundary clause and the defect condition for writing outside the artifact."""
    lowered = _read(TEMPLATE).lower()
    assert "observe" in lowered and "report" in lowered, (
        "the body must state the observe-and-report boundary"
    )
    assert "defect" in lowered, (
        "the body must state that mutating anything outside its own stream artifact is a defect"
    )
    assert "stream artifact" in lowered, (
        "the body must name the one write surface it owns"
    )


# --------------------------------------------------------------------------- #
# C-20 / RS-07 — the seat carries its dispatch-injection duties by reference
# --------------------------------------------------------------------------- #
def test_template_reaches_both_injection_sections_by_anchor():
    """Both owner sections must resolve, and the Template must cite them rather than copy them."""
    text = _read(TEMPLATE)
    fast_fail = REPO_ROOT / "shared" / "guidelines" / "fast-fail.md"
    progress = REPO_ROOT / "shared" / "guidelines" / "progress-reporting.md"
    assert "fast-fail.md" in text, "the Template must point at shared/guidelines/fast-fail.md"
    assert "子代理派发注入" in text, (
        "the Template must cite the fast-fail owner by its section anchor, not only by path"
    )
    assert "progress-reporting.md" in text, (
        "the Template must point at shared/guidelines/progress-reporting.md"
    )
    assert "子代理与委托" in text, (
        "the Template must cite the progress-reporting injection section by its anchor"
    )
    assert fast_fail.is_file() and progress.is_file(), "the two pointed-at owners must exist"
    assert "## 子代理派发注入" in _read(fast_fail), "the fast-fail anchor must resolve to a real section"
    assert "## 子代理与委托(派发时注入)" in _read(progress), (
        "the progress-reporting anchor must resolve to a real section"
    )


def test_template_does_not_copy_either_clause():
    """A copy of either clause inside the Template is the defect C-20 names."""
    text = _read(TEMPLATE)
    fast_fail = _read(REPO_ROOT / "shared" / "guidelines" / "fast-fail.md")
    begin = fast_fail.index("<!-- fast-fail-clause:begin -->") + len("<!-- fast-fail-clause:begin -->")
    end = fast_fail.index("<!-- fast-fail-clause:end -->")
    owner_clause = fast_fail[begin:end].strip()
    assert owner_clause, "sanity: the owner clause interval is non-empty"

    # The Template carries its sibling's fast-fail block by construction (the byte-identical copy), but it MUST NOT
    # carry the progress-reporting injection section's text.
    progress = _read(REPO_ROOT / "shared" / "guidelines" / "progress-reporting.md")
    progress_section = _section(progress, "## 子代理与委托(派发时注入)")
    assert progress_section, "sanity: the progress-reporting injection section exists"
    body = "\n".join(
        line for line in progress_section.splitlines()[1:] if line.strip() and not line.startswith("#")
    ).strip()
    distinctive = [frag for frag in body.split("\n") if len(frag.strip()) > 30]
    copied = [frag for frag in distinctive[:3] if frag.strip() in text]
    assert not copied, (
        "the Template restates the progress-reporting injection clause instead of referencing it: %r"
        % (copied,)
    )


# --------------------------------------------------------------------------- #
# C-21 / RS-08 — stdlib-only, single file, reachable from the create procedure
# --------------------------------------------------------------------------- #
def test_guard_is_a_single_stdlib_only_file():
    """Plain ``python3`` runs it: no installed package, one file, standard library imports only."""
    tree = ast.parse(_read(GUARD), filename=str(GUARD))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    third_party = sorted(
        name for name in imported if name not in sys.stdlib_module_names and name != "__future__"
    )
    assert not third_party, "the roster guard must import only the standard library; found %r" % (
        third_party,
    )
    siblings = sorted(p.name for p in GUARD.parent.glob("validate-roster*"))
    assert siblings == ["validate-roster.py"], (
        "the guard is one file; a split companion would break the single-file shape (RS-08): %r"
        % (siblings,)
    )


def test_guard_is_called_from_the_create_procedure():
    """The obligation is reachable from a numbered create step, without a separate command (C-21)."""
    for path in (SKILL, CREATE_MODE):
        text = _read(path)
        if "validate-roster.py" in text:
            return
    pytest.fail(
        "neither %s nor %s names the guard script, so the obligation is unreachable from the create"
        " procedure" % (SKILL.relative_to(REPO_ROOT), CREATE_MODE.relative_to(REPO_ROOT))
    )


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _section(text: str, needle: str) -> str:
    """Return the block around ``needle`` (a heading or a key), bounded by blank lines / next heading."""
    lines = text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if needle in line and (line.startswith("#") or ":" in line)),
        None,
    )
    if start is None:
        return ""
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("## ") or line.strip() == "```":
            end = index
            break
    return "\n".join(lines[start:end])


def _schema_block(text: str) -> str:
    """Return the first fenced ```markdown block — the persisted `team.md` schema."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "```markdown"), None)
    if start is None:
        return ""
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() == "```"), len(lines))
    return "\n".join(lines[start + 1 : end])
