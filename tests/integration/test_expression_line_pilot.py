"""Expression-line pilot — one declared-``expression`` line through the eight stage operators (077, P1-a).

What this file is
-----------------
The 077 review (``review.md`` F1 / ``code-review.md`` round) found that four Success
Criteria were ``partial`` for one and the same reason: no expression-class line had ever
been run through the gates, so "the mechanism exists" had never been observed as "the
mechanism fired". This module is that line — a **synthetic fixture pilot with
gate-level real execution**: every operator below is the shipped engine, run as a
subprocess against a fixture repository laid out exactly like a real one
(``.specify/specs/<name>/``), and every verdict is read from an exit code or an output
line, never from a hand-written expectation.

It is deliberately **not** a customer line, and it does not claim to be one: the fixture
is three files under ``tests/fixtures/expression_line/``, the repository is built in
``tmp_path`` and thrown away. What it does claim is narrower and checkable: on a line
whose ``requirements.md`` declares ``**Flow Class**: expression``, the eight operator
rows below each ran, each returned a verdict, and none returned ``not-evaluated``.

The eight operator rows (this table is the pilot's own; it maps one row onto each gate a
line has to pass between ``requirements`` and ``closure``)
-----------------------------------------------------------------
===========  ===================================================================  ==================================
row          operator                                                             stage it stands for
===========  ===================================================================  ==================================
S1           ``flow-class-check.py --action lookup --unit-id spec:<fixture>``     entry read (every stage)
S2           ``validate-requirements.py <fixture requirements.md>``                 requirements
S3           ``doc-consistency-check.py --action structure --path <doc>``           plan / implement structure
S4           ``doc-consistency-check.py --action verify --faces … --path <doc>``    implement four faces
S5           ``validate-decision-tensions.py --spec <fixture spec>``                 plan
S6           seven ``templates/commands/*.md`` carry the wiring card               distribution / stage wiring
S7           ``docs-utils.py --action validate``                                     build sub-row
S8           ``audit-test-budget.py --stage-check closure`` (docs-gate-full slots)  closure
===========  ===================================================================  ==================================

Non-vacuity: two mutation controls live beside the rows — dropping the reader
declaration from the delivered document must turn S3 red, and dropping
``selection_basis`` from the closure slot row must turn S8's audit red. A pilot whose
rows stay green under those mutations would prove nothing.

Literals are not copied: the four structure headings are read from the checker module's
own constants (``STRUCTURE_HEADING`` / ``STRUCTURE_SUBSECTIONS``), and the payload's
closed ``error`` domain is read from the engine's own output.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "expression_line"
FLOW_ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
DOC_CHECKER = REPO_ROOT / "scripts" / "python" / "doc-consistency-check.py"
REQUIREMENTS_VALIDATOR = REPO_ROOT / "scripts" / "python" / "validate-requirements.py"
DECISION_TENSIONS = REPO_ROOT / "scripts" / "python" / "validate-decision-tensions.py"
DOCS_UTILS = REPO_ROOT / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py"
AUDIT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "audit-test-budget.py"
OWNER_DOC = REPO_ROOT / "shared" / "definitions" / "flow-class-definitions.md"
TEMPLATES = REPO_ROOT / "templates" / "commands"

# The seven wired stage templates (contracts/stage-wiring.md C-001). `docs` and
# `humanize` are outside this roster on purpose: their wiring card is a different,
# older one and is not part of 077's surface.
WIRED_TEMPLATES = (
    "requirements",
    "clarify",
    "plan",
    "tasks",
    "checklist",
    "analyze",
    "implement",
)
WIRING_HEADING = "### 类别读取与文档型门禁"

SPEC_NAME = "777-expression-line-pilot"
DELIVERED_NAME = "pilot-line.md"

# One docs-gate-full slot row, in the field set owned by
# `skills/external/sdd-loop-driver/references/efficiency-model.md` §2.8. The pilot
# asserts the *shape* (the audit accepts it and reports `row 2: missing …` when a field
# disappears), never a number the pilot did not measure.
DOCS_GATE_COMMAND = (
    "python3 scripts/python/doc-consistency-check.py --action verify "
    "--faces reader,evidence,duplicate,count --path docs/%s; "
    "python3 scripts/python/doc-consistency-check.py --action structure "
    "--spec-dir .specify/specs/%s --path docs/%s; "
    "python3 skills/external/create-docs/scripts/docs-utils.py --action validate"
    % (DELIVERED_NAME, SPEC_NAME, DELIVERED_NAME)
)


# --------------------------------------------------------------------------- #
# the fixture repository
# --------------------------------------------------------------------------- #
class Pilot:
    """A fixture repository shaped like a real one, plus the paths the rows need."""

    def __init__(self, root: Path):
        self.root = root
        self.spec_dir = root / ".specify" / "specs" / SPEC_NAME
        self.requirements = self.spec_dir / "requirements.md"
        self.plan = self.spec_dir / "plan.md"
        self.delivered = root / "docs" / DELIVERED_NAME

    def copy(self, destination: Path) -> "Pilot":
        """A second, independent tree — for the mutation controls."""
        shutil.copytree(self.root, destination)
        return Pilot(destination)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )


def build_pilot(root: Path) -> Pilot:
    """Materialise the fixture line: three fixture files, the owner, and one commit.

    The commit is not decoration: the ``evidence`` face reads a fact's ``as-of``
    against repository history, and it reports ``not-evaluated`` — never a pass — when
    the subject is not a working tree. A pilot repository that is not a repository
    would therefore degrade the very row it exists to exercise.
    """
    assert FIXTURES.is_dir(), "expression-line fixture missing: %s" % FIXTURES
    assert OWNER_DOC.is_file(), "the class owner document is missing: %s" % OWNER_DOC
    assert _git(root, "--version").returncode == 0 or shutil.which("git"), (
        "git is required: the evidence face reads history, and without it the pilot "
        "would measure its own degradation instead of the gate"
    )

    pilot = Pilot(root)
    _write(pilot.requirements, (FIXTURES / "requirements.md").read_text(encoding="utf-8"))
    _write(pilot.plan, (FIXTURES / "plan.md").read_text(encoding="utf-8"))
    _write(pilot.delivered, (FIXTURES / "doc.md").read_text(encoding="utf-8"))

    # The class owner is the framework's own document, copied — not a stub. A stub
    # would let the pilot pass on a ledger the real engine would never see.
    _write(root / "shared" / "definitions" / "flow-class-definitions.md",
           OWNER_DOC.read_text(encoding="utf-8"))

    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=pilot", "-c", "user.email=pilot@example.invalid",
         "commit", "-q", "-m", "fixture: expression-line pilot")
    return pilot


@pytest.fixture
def pilot(tmp_path: Path) -> Pilot:
    return build_pilot(tmp_path / "repo")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run_posix(script: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    assert script.is_file(), "engine missing: %s" % script
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _checker_module():
    """The structure literals' code-first owner — imported, never hand-copied."""
    spec = importlib.util.spec_from_file_location("_pilot_doc_checker", DOC_CHECKER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _json_or_fail(proc: subprocess.CompletedProcess, what: str):
    assert proc.stdout.strip(), (
        "%s produced no stdout (rc=%d, stderr=%r)" % (what, proc.returncode, proc.stderr)
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - engine contract violation
        raise AssertionError(
            "%s did not emit JSON (%s); head=%r" % (what, exc, proc.stdout[:400])
        ) from exc


# --------------------------------------------------------------------------- #
# S1 — the entry read: a declared expression line resolves as expression
# --------------------------------------------------------------------------- #
def _row_s1(p: Pilot) -> dict:
    proc = _run_posix(
        FLOW_ENGINE, "--repo", str(p.root), "--action", "lookup",
        "--unit-id", "spec:%s" % SPEC_NAME, "--format", "json",
        cwd=p.root,
    )
    record = _json_or_fail(proc, "S1 flow-class-check")
    verdict = "pass" if (
        proc.returncode == 0
        and record.get("flow_class") == "expression"
        and record.get("source") == "declaration"
        and record.get("marker") is None
    ) else "fail"
    return {
        "row": "S1",
        "operator": "flow-class-check.py --action lookup spec:%s" % SPEC_NAME,
        "rc": proc.returncode,
        "verdict": verdict,
        "detail": "flow_class=%r source=%r marker=%r error=%r"
                  % (record.get("flow_class"), record.get("source"),
                     record.get("marker"), record.get("error")),
    }


def test_s1_the_line_resolves_as_expression_from_its_declaration(pilot):
    row = _row_s1(pilot)
    assert row["verdict"] == "pass", (
        "the fixture line declares `**Flow Class**: expression`, so the entry read must "
        "answer expression / source=declaration / exit 0; got rc=%d %s"
        % (row["rc"], row["detail"])
    )


# --------------------------------------------------------------------------- #
# S2 — requirements stage: the spec is structurally sound
# --------------------------------------------------------------------------- #
def _row_s2(p: Pilot) -> dict:
    proc = _run_posix(REQUIREMENTS_VALIDATOR, str(p.requirements), cwd=p.root)
    labels = [
        line.strip() for line in proc.stdout.splitlines() if line.strip().startswith("[")
    ]
    verdict = "pass" if proc.returncode == 0 and "status: ok" in proc.stdout else "fail"
    return {
        "row": "S2",
        "operator": "validate-requirements.py <fixture requirements.md>",
        "rc": proc.returncode,
        "verdict": verdict,
        "detail": "status=%r labels=%r"
                  % ("ok" if "status: ok" in proc.stdout else "not-ok", labels),
    }


def test_s2_the_fixture_spec_passes_the_requirements_gate(pilot):
    row = _row_s2(pilot)
    assert row["verdict"] == "pass", (
        "the fixture requirements must pass every structural label (id-contiguous / "
        "doc-order / ref-resolvable / marker-count / dup-id); got rc=%d %s"
        % (row["rc"], row["detail"])
    )


# --------------------------------------------------------------------------- #
# S3 — plan / implement structure: plan side + two-way, zero findings
# --------------------------------------------------------------------------- #
def _row_s3(p: Pilot) -> dict:
    proc = _run_posix(
        DOC_CHECKER, "--action", "structure", "--spec-dir", str(p.spec_dir),
        "--path", str(p.delivered), "--format", "json", cwd=p.root,
    )
    payload = _json_or_fail(proc, "S3 --action structure")
    subsections = payload.get("subsections") or {}
    verdict = "pass" if (
        proc.returncode == 0
        and payload.get("status") == "ok"
        and payload.get("two_way") == "run"
        and not payload.get("findings")
        and subsections and all(subsections.values())
    ) else "fail"
    return {
        "row": "S3",
        "operator": "doc-consistency-check.py --action structure --path <delivered>",
        "rc": proc.returncode,
        "verdict": verdict,
        "detail": "status=%r two_way=%r findings=%d subsections=%r codes=%r"
                  % (payload.get("status"), payload.get("two_way"),
                     len(payload.get("findings") or []), subsections,
                     [item.get("rule") for item in payload.get("findings") or []]),
    }


def test_s3_the_structure_gate_is_green_on_both_sides(pilot):
    row = _row_s3(pilot)
    assert row["verdict"] == "pass", (
        "an expression line's plan must carry the four subsections and the delivered "
        "document must match the chapter tree with zero findings; got rc=%d %s"
        % (row["rc"], row["detail"])
    )


# --------------------------------------------------------------------------- #
# S4 — implement: the four faces
# --------------------------------------------------------------------------- #
def _row_s4(p: Pilot) -> dict:
    proc = _run_posix(
        DOC_CHECKER, "--action", "verify", "--spec-dir", str(p.spec_dir),
        "--path", str(p.delivered), "--faces", "reader,evidence,duplicate,count",
        "--format", "json", cwd=p.root,
    )
    payload = _json_or_fail(proc, "S4 --action verify")
    faces = payload.get("faces") or {}
    verdict = "pass" if (
        proc.returncode == 0
        and faces
        and all(status == "pass" for status in faces.values())
        and not payload.get("findings")
    ) else "fail"
    return {
        "row": "S4",
        "operator": "doc-consistency-check.py --action verify --faces reader,evidence,duplicate,count",
        "rc": proc.returncode,
        "verdict": verdict,
        "detail": "faces=%r findings=%d" % (faces, len(payload.get("findings") or [])),
    }


def test_s4_the_delivered_document_passes_all_four_faces(pilot):
    row = _row_s4(pilot)
    assert row["verdict"] == "pass", (
        "the delivered document carries the reader lines and one evidenced assertion, so "
        "all four faces must be `pass` and the run must exit 0; got rc=%d %s"
        % (row["rc"], row["detail"])
    )


# --------------------------------------------------------------------------- #
# S5 — plan: decision tension records
# --------------------------------------------------------------------------- #
def _row_s5(p: Pilot) -> dict:
    proc = _run_posix(DECISION_TENSIONS, "--spec", str(p.spec_dir), cwd=p.root)
    labels = [
        line.strip() for line in proc.stdout.splitlines() if line.strip().startswith("[")
    ]
    verdict = "pass" if proc.returncode == 0 and "status: ok" in proc.stdout else "fail"
    return {
        "row": "S5",
        "operator": "validate-decision-tensions.py --spec <fixture spec>",
        "rc": proc.returncode,
        "verdict": verdict,
        "detail": "status=%r labels=%r"
                  % ("ok" if "status: ok" in proc.stdout else "not-ok", labels),
    }


def test_s5_the_plan_carries_one_complete_decision_tension_record(pilot):
    row = _row_s5(pilot)
    assert row["verdict"] == "pass", (
        "T-001 carries the six fields and maps its expected_sacrifice onto SC-001 Source "
        "in the same feature's requirements; got rc=%d %s" % (row["rc"], row["detail"])
    )


# --------------------------------------------------------------------------- #
# S6 — distribution: the seven stage templates carry the wiring card
# --------------------------------------------------------------------------- #
def _row_s6() -> dict:
    counts = {}
    for stem in WIRED_TEMPLATES:
        path = TEMPLATES / ("%s.md" % stem)
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        lines = text.split("\n")
        counts[stem] = {
            "files": 1 if path.is_file() else 0,
            "headings": lines.count(WIRING_HEADING),
            "lookups": text.count("flow-class-check.py"),
        }
    verdict = "pass" if all(
        item["files"] == 1 and item["headings"] == 1 and item["lookups"] == 1
        for item in counts.values()
    ) else "fail"
    return {
        "row": "S6",
        "operator": "templates/commands/{7} — wiring card presence",
        "rc": 0,
        "verdict": verdict,
        "detail": counts,
    }


def test_s6_every_stage_template_carries_exactly_one_wiring_card():
    row = _row_s6()
    assert row["verdict"] == "pass", (
        "each of the seven stage templates must carry the wiring card exactly once and "
        "call the engine exactly once; got %r" % (row["detail"],)
    )


# --------------------------------------------------------------------------- #
# S7 — build sub-row: the docs space is clean
# --------------------------------------------------------------------------- #
def _row_s7(p: Pilot) -> dict:
    proc = _run_posix(DOCS_UTILS, "--action", "validate", "--root", str(p.root), cwd=p.root)
    payload = _json_or_fail(proc, "S7 docs-utils validate")
    violations = payload.get("violations")
    verdict = "pass" if proc.returncode == 0 and violations == [] else "fail"
    return {
        "row": "S7",
        "operator": "docs-utils.py --action validate --root <pilot repo>",
        "rc": proc.returncode,
        "verdict": verdict,
        "detail": "violations=%r" % (violations,),
    }


def test_s7_the_delivered_document_adds_no_docs_space_violation(pilot):
    row = _row_s7(pilot)
    assert row["verdict"] == "pass", (
        "the pilot tree is new, so its baseline is the empty set: validate must report "
        "zero violations, not merely 'no new ones'; got %s" % (row["detail"],)
    )


# --------------------------------------------------------------------------- #
# S8 — closure: the two docs-gate-full slots are accepted by the unchanged audit
# --------------------------------------------------------------------------- #
def _slot_rows() -> list[dict]:
    return [
        {
            "seq": 1,
            "slot": "baseline",
            "stage": "implement",
            "purpose": "implement-start-docs-gate",
            "trigger": "scheduled",
            "at": "2026-10-30T00:10:00Z",
            "command": DOCS_GATE_COMMAND,
            "selection_basis": "docs-gate-full",
            "rc": 0,
            "passed": 1,
            "failed": 0,
            "failed_names_path": "docs-gate-operator-ids.txt",
            "baseline_compare": "na",
            "evidence_ptr": ".specify/specs/%s/test-evidence/baseline-docs-gate.txt" % SPEC_NAME,
        },
        {
            "seq": 2,
            "slot": "closure",
            "stage": "review",
            "purpose": "final-closure-docs-gate",
            "trigger": "scheduled",
            "at": "2026-10-30T02:00:00Z",
            "command": DOCS_GATE_COMMAND,
            "selection_basis": "docs-gate-full",
            "rc": 0,
            "passed": 1,
            "failed": 0,
            "failed_names_path": "docs-gate-operator-ids.txt",
            "baseline_compare": "comm -13 baseline-operator-ids.txt final-operator-ids.txt -> 0 new failed operators",
            "evidence_ptr": ".specify/specs/%s/test-evidence/closure-docs-gate.txt" % SPEC_NAME,
        },
    ]


def _write_spine(p: Pilot, rows: list[dict], name: str = "spine.md") -> Path:
    path = p.root / ".specify" / ".tmp" / name
    body = ["# Line State Spine — expression-line pilot (fixture)", ""]
    body.append("<!-- test-budget:begin -->")
    body.extend(json.dumps(row, ensure_ascii=False) for row in rows)
    body.append("<!-- test-budget:end -->")
    _write(path, "\n".join(body) + "\n")
    return path


def _audit(p: Pilot, spine: Path) -> tuple[int, list[str]]:
    proc = _run_posix(
        AUDIT, "--spine", str(spine), "--spec-dir", str(p.spec_dir),
        "--stage-check", "closure", cwd=p.root,
    )
    return proc.returncode, proc.stdout.splitlines()


def _row_s8(p: Pilot) -> dict:
    spine = _write_spine(p, _slot_rows())
    rc, lines = _audit(p, spine)
    summary = next((line for line in lines if line.startswith("slots=")), "")
    reasons = [line for line in lines if line.startswith("reason=")]
    slot_reasons = [line for line in reasons if "stage evidence file missing" not in line]
    # The pilot measured the slot half only: the six per-stage evidence files are not
    # part of the eight operator rows, so a `stage evidence file missing` reason is
    # expected and does not bear on this row. Any *other* reason is a slot violation.
    verdict = "pass" if (
        summary == "slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=6 "
                   "environment_failures=0"
        and not slot_reasons
    ) else "fail"
    return {
        "row": "S8",
        "operator": "audit-test-budget.py --spine <fixture> --stage-check closure",
        "rc": rc,
        "verdict": verdict,
        "detail": "summary=%r slot_violations=%r" % (summary, slot_reasons),
    }


def test_s8_the_two_docs_gate_slots_are_accepted_by_the_unchanged_audit(pilot):
    row = _row_s8(pilot)
    assert row["verdict"] == "pass", (
        "two `docs-gate-full` rows (one baseline, one closure) must be accepted with the "
        "slot counters unchanged; got %s" % (row["detail"],)
    )


def test_s8_a_missing_slot_field_is_named_by_the_audit(pilot):
    """The negative control: the field set is pinned, not merely tolerated."""
    rows = _slot_rows()
    rows[1].pop("selection_basis")
    spine = _write_spine(pilot, rows, name="spine-mutated.md")
    _rc, lines = _audit(pilot, spine)
    assert "reason=row 2: missing selection_basis" in lines, (
        "dropping a field of the docs-gate-full row must be named by the audit; if the "
        "mutated run stayed identical, S8's green would prove nothing. lines=%r" % (lines,)
    )


# --------------------------------------------------------------------------- #
# The chain — every row on one tree, in order
# --------------------------------------------------------------------------- #
def test_the_pilot_line_runs_all_eight_rows_in_order(pilot):
    rows = [_row_s1(pilot), _row_s2(pilot), _row_s3(pilot), _row_s4(pilot),
            _row_s5(pilot), _row_s6(), _row_s7(pilot), _row_s8(pilot)]
    transcript = ["row | verdict | rc | operator", "--- | ------- | -- | --------"]
    transcript += [
        "%s | %s | %d | %s" % (row["row"], row["verdict"], row["rc"], row["operator"])
        for row in rows
    ]
    transcript += ["", "detail per row:"] + [
        "  %s: %s" % (row["row"], row["detail"]) for row in rows
    ]
    print("\n".join(transcript))
    assert [row["row"] for row in rows] == ["S%d" % n for n in range(1, 9)], (
        "the eight rows must run in the table's order"
    )
    assert all(row["verdict"] == "pass" for row in rows), (
        "not-evaluated is not a pass: every row must carry a positive verdict.\n%s"
        % "\n".join(transcript)
    )


# --------------------------------------------------------------------------- #
# Non-vacuity — a broken line must turn the gate red
# --------------------------------------------------------------------------- #
def test_s4_turns_red_when_the_delivered_reader_declaration_disappears(pilot):
    """SC-003 / SC-004's "delete the reader declaration" leg, on the pilot's own text."""
    mutated = pilot.copy(pilot.root.parent / "mutated-reader")
    text = mutated.delivered.read_text(encoding="utf-8")
    stripped = "\n".join(
        line for line in text.splitlines() if not line.startswith("**Readers**:")
    )
    _write(mutated.delivered, stripped + "\n")
    row = _row_s4(mutated)
    assert row["verdict"] == "fail", (
        "a delivered document that lost its reader declaration must not pass the four "
        "faces; got %s" % (row["detail"],)
    )
    assert "'reader': 'fail'" in row["detail"], (
        "the red must be the reader face, not an unrelated face: %s" % (row["detail"],)
    )


def test_s3_turns_red_when_the_chapter_tree_subsection_disappears(pilot):
    mutated = pilot.copy(pilot.root.parent / "mutated-tree")
    literal = _checker_module().STRUCTURE_SUBSECTIONS[0]
    text = mutated.plan.read_text(encoding="utf-8")
    assert literal in text, "fixture precondition: the plan carries %r" % literal
    _write(mutated.plan, text.replace(literal + "\n", "### Chapter Tree (misplaced)\n", 1))
    row = _row_s3(mutated)
    assert row["verdict"] == "fail", (
        "a plan whose chapter tree is not at the registered heading must not pass the "
        "structure gate; got %s" % (row["detail"],)
    )
    assert "'subsection-missing'" in row["detail"] or "subsection-missing" in row["detail"], (
        "the red must name the closed code for a missing subsection: %s" % (row["detail"],)
    )
