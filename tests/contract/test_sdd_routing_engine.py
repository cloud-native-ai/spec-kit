"""Contract tests: the deterministic routing decision (slice 074a, task T018).

What this pins
--------------
`contracts/routing-decision.md` C-23, C-24, C-28 and C-29, executed through the two
verdict-producing actions of the read-only engine `scripts/python/sdd-route.py`:

1. **Determinism** — the same five declared inputs produce byte-identical output, and the
   reason code is the first *declared* row of the owner document's vocabulary whose
   condition held, while every triggered condition id is carried too (C-24, SC-002).
2. **Precedence** — [[STR-006]] first, then [[STR-004]], then [[STR-005]]: an adjudicate
   condition outranks every sdd condition, and nothing falls through to direct (C-23).
3. **Exit alphabet, two values only** — `0` for *every* produced verdict including
   adjudicate, `2` for input errors, and no third code (C-28).
4. **Read-only** — neither action writes a file (C-28).
5. **The facts live in the owner document** — the value domains, the verdict table, the
   precedence and the reason codes are read at run time; this file proves it by mutating a
   *copy* of the owner document and requiring the engine to follow the mutation, and by
   scanning the engine source for any copy of those four facts (C-28, FR-014).
6. **The golden table is judged, not copied** — `--action golden` parses the owner's
   § Golden case table and judges every row; no second copy of the rows exists here (C-29).

Vocabulary discipline: the three verdict literals pinned below are `[[STR-004]]` /
`[[STR-005]]` / `[[STR-006]]` of `requirements.md` § Shared Strings — a literal pinned in a
test to detect drift, which is one of the three legitimate duplicates. The closed
vocabularies themselves (domains, verdict table, precedence, reason codes) are read out of
`shared/definitions/sdd-routing-definitions.md` at test time, never restated here.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "sdd-route.py"
OWNER_DOC = REPO_ROOT / "shared" / "definitions" / "sdd-routing-definitions.md"

#: `[[STR-004]]` / `[[STR-005]]` / `[[STR-006]]` — verdict literals, pinned to detect drift.
SDD = "sdd"
DIRECT = "direct"
ADJUDICATE = "adjudicate"


# ---------------------------------------------------------------------------
# Reading the owner document (the test's own parser — independent of the engine's)
# ---------------------------------------------------------------------------


def _owner_text() -> str:
    assert OWNER_DOC.is_file(), f"owner document missing: {OWNER_DOC}"
    return OWNER_DOC.read_text(encoding="utf-8")


def _sections(text: str) -> dict:
    sections: dict = {}
    current = None
    buffer: list = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip()
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def _rows(body: str) -> list:
    rows = []
    for line in body.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    return rows


def _bare(cell: str) -> str:
    return cell.strip().strip("`").strip()


def _section_body(name: str) -> str:
    body = _sections(_owner_text()).get(name)
    assert body is not None, (
        f"owner document has no '## {name}' section; the routing facts MUST land there "
        f"(C-17): sections present: {sorted(_sections(_owner_text()))}"
    )
    return body


def _inputs() -> dict:
    """`{input id: {"flag": "--x", "domain": (value, ...)}}`, in declared order."""
    body = _section_body("Inputs")
    table = [row for row in _rows(body) if len(row) >= 3 and "--" in row[0]]
    assert len(table) == 5, f"§ Inputs declares {len(table)} machine-readable input rows, not 5"
    inputs = {}
    for row in table:
        tokens = re.findall(r"`([^`]+)`", row[0])
        input_id = tokens[0]
        flag = next((token for token in tokens if token.startswith("--")), None)
        assert flag is not None, f"§ Inputs row {input_id!r} names no CLI flag"
        domain = tuple(_bare(part) for part in row[2].split("/") if part.strip())
        assert domain, f"§ Inputs row {input_id!r} declares no closed domain"
        inputs[input_id] = {"flag": flag, "domain": domain}
    return inputs


def _flag_map() -> dict:
    return {input_id: spec["flag"] for input_id, spec in _inputs().items()}


def _verdict_rows() -> dict:
    body = _section_body("Verdict table")
    rows = [row for row in _rows(body) if len(row) >= 3 and _bare(row[0]) in (SDD, DIRECT, ADJUDICATE)]
    assert len(rows) == 3, f"§ Verdict table declares {len(rows)} verdict rows, not 3"
    return {
        _bare(row[0]): {
            "mode": _bare(row[1]).lower(),
            "conditions": tuple(re.findall(r"`([^`]+)`", row[2])),
        }
        for row in rows
    }


def _precedence() -> tuple:
    body = _section_body("Precedence")
    line = next(
        (line for line in body.splitlines() if line.count("`") >= 6 and ">" in line),
        None,
    )
    assert line is not None, "§ Precedence declares no machine-readable precedence line"
    order = tuple(_bare(token) for token in re.findall(r"`([^`]+)`", line))
    assert set(order) == {SDD, DIRECT, ADJUDICATE}, (
        f"the precedence line MUST order the three verdicts: {order}"
    )
    return order


def _reason_rows() -> list:
    body = _section_body("Reason codes")
    rows = []
    for row in _rows(body):
        if len(row) < 4 or not row[0].isdigit():
            continue
        rows.append(
            {
                "order": int(row[0]),
                "code": _bare(row[1]),
                "verdict": _bare(row[2]),
                "condition": None if _bare(row[3]) in ("—", "-", "") else _bare(row[3]),
            }
        )
    assert rows, "§ Reason codes declares no reason-code row"
    assert [row["order"] for row in rows] == sorted(row["order"] for row in rows), (
        "§ Reason codes rows MUST be numbered in their declared (code-taking) order"
    )
    return rows


def _reason(condition: str | None) -> str:
    """The reason code bound to a condition id (or the row that has no condition id)."""
    for row in _reason_rows():
        if row["condition"] == condition:
            return row["code"]
    raise AssertionError(f"§ Reason codes binds no reason code to condition {condition!r}")


def _golden_rows() -> list:
    body = _section_body("Golden case table")
    rows = _rows(body)
    assert rows, "§ Golden case table declares no row"
    header = rows[0]
    inputs = list(_inputs())
    index = {name: header.index(name) for name in inputs if name in header}
    assert set(index) == set(inputs), (
        f"§ Golden case table header MUST carry a column per input: {header}"
    )
    rationale_at = next((i for i, cell in enumerate(header) if "rationale" in cell.lower()), None)
    out = []
    for row in rows[1:]:
        inputs_declared = {
            name: (None if row[index[name]] in ("—", "-", "") else row[index[name]])
            for name in inputs
        }
        out.append(
            {
                "case_id": row[0],
                "inputs": inputs_declared,
                "rationale": None
                if rationale_at is None or row[rationale_at] in ("—", "-", "")
                else row[rationale_at],
                "expected_verdict": _bare(row[-3]),
                "expected_reason_code": _bare(row[-2]),
                "face": row[-1],
            }
        )
    return out


# ---------------------------------------------------------------------------
# Driving the engine
# ---------------------------------------------------------------------------


def _run(argv: list, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *argv],
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
    )


@pytest.fixture(autouse=True)
def _routing_actions_present():
    """Fail on absence for the right reason.

    The parser names the actions it accepts in its invalid-choice diagnostic; asserting on
    that text means a missing action fails here instead of being read as "the verdict was
    adjudicate", which is the classic false green for this slice's two exit meanings.
    """
    diagnostic = _run(["--action", "__absent-action__"])
    offered = diagnostic.stderr + diagnostic.stdout
    missing = [action for action in ("route", "golden") if action not in offered]
    assert not missing, (
        f"--action {' / '.join(missing)} missing from {ENGINE} (delivered by task T019); "
        f"the parser offered: {offered.strip()!r}"
    )


def _argv(
    action: str = "route",
    *,
    nature=None,
    traceability=None,
    blast_radius=None,
    reversibility=None,
    complexity=None,
    rationale=None,
    recorded_at=None,
    actor=None,
    owner_doc: Path | None = None,
    fmt: str = "json",
) -> list:
    argv = ["--action", action, "--format", fmt]
    flags = _flag_map()
    for input_id, value in (
        ("change_nature", nature),
        ("traceability", traceability),
        ("blast_radius", blast_radius),
        ("reversibility", reversibility),
        ("complexity", complexity),
    ):
        if value is not None:
            argv += [flags[input_id], str(value)]
    if rationale is not None:
        argv += ["--rationale", rationale]
    if recorded_at is not None:
        argv += ["--recorded-at", recorded_at]
    if actor is not None:
        argv += ["--actor", actor]
    if owner_doc is not None:
        argv += ["--owner-doc", str(owner_doc)]
    return argv


def _route(**kwargs):
    """Run `--action route` and return `(record_or_None, proc)`."""
    proc = _run(_argv("route", **kwargs))
    try:
        record = json.loads(proc.stdout)
    except json.JSONDecodeError:
        record = None
    return record, proc


def _golden(**kwargs):
    proc = _run(_argv("golden", **kwargs))
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = None
    return payload, proc


def _mutate(tmp_path: Path, old: str, new: str, name: str = "owner.md") -> Path:
    """A temp copy of the owner document with one substitution, verified to have happened."""
    text = _owner_text()
    assert text.count(old) == 1, (
        f"mutation target {old!r} appears {text.count(old)} times in the owner document; "
        f"a mutation that does not bite proves nothing"
    )
    path = tmp_path / name
    path.write_text(text.replace(old, new), encoding="utf-8")
    return path


def _fingerprint(*paths: Path) -> dict:
    return {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


# ---------------------------------------------------------------------------
# 1. Determinism and the shape of the record
# ---------------------------------------------------------------------------


def test_route_is_deterministic():
    kwargs = dict(
        nature="feature",
        traceability="required",
        blast_radius="cross-cutting",
        reversibility="hard",
        complexity="standard",
    )
    first = _run(_argv("route", **kwargs))
    second = _run(_argv("route", **kwargs))
    assert first.returncode == 0, f"a produced verdict exits 0 (C-28): {first.stderr!r}"
    assert second.returncode == 0
    assert first.stdout == second.stdout, (
        "the same inputs MUST produce byte-identical output, so two evaluations are "
        "comparable (C-24, SC-002)"
    )
    assert first.stdout.strip(), "route MUST emit a record"


def test_route_feature_scale_returns_sdd():
    """quickstart S1 — the feature-scale change (FR-009, first condition)."""
    record, proc = _route(
        nature="feature",
        traceability="required",
        blast_radius="cross-cutting",
        reversibility="hard",
        complexity="standard",
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record is not None, f"--format json MUST emit a record: {proc.stdout!r}"
    assert record["verdict"] == SDD, (
        f"a feature-scale change MUST route to the SDD flow: {record!r}"
    )
    assert record["reason_code"] == _reason("nature-feature"), (
        "the reason code MUST be the first declared reason row whose condition held (C-24)"
    )
    assert record["inputs"] == {
        "change_nature": "feature",
        "traceability": "required",
        "blast_radius": "cross-cutting",
        "reversibility": "hard",
        "complexity": "standard",
    }, f"the record MUST carry the five declared inputs (C-23): {record!r}"


def test_route_bounded_maintenance_returns_direct():
    """quickstart S2 — a bounded maintenance change (FR-010, every condition holds)."""
    record, proc = _route(
        nature="maintenance",
        traceability="not-required",
        blast_radius="local",
        reversibility="reversible",
        complexity="standard",
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record is not None
    assert record["verdict"] == DIRECT, (
        f"with every direct condition satisfied the verdict is direct: {record!r}"
    )
    assert record["reason_code"] == _reason(None), (
        f"the direct verdict's reason row carries no condition id (C-24): {record!r}"
    )


def test_record_carries_the_e4_face_and_invents_no_clock():
    record, proc = _route(
        nature="maintenance",
        traceability="not-required",
        blast_radius="local",
        reversibility="reversible",
        complexity="trivial",
    )
    assert proc.returncode == 0
    assert record is not None
    assert set(record["inputs"]) == set(_inputs()), (
        f"the record MUST carry all five inputs (C-23): {record!r}"
    )
    assert record.get("override") is None, (
        f"route produces the pre-override verdict; the override slot is for the caller "
        f"(C-25): {record!r}"
    )
    assert record.get("recorded_at") is None, (
        "the engine MUST NOT read a clock — a timestamp would break the byte-identical "
        "property C-24 requires; recorded_at comes from the caller"
    )
    assert record.get("effective_blast_radius") in _inputs()["blast_radius"]["domain"], (
        f"the record MUST carry the derived effective radius, inside the declared domain: "
        f"{record!r}"
    )

    stamped, _ = _route(
        nature="maintenance",
        traceability="not-required",
        blast_radius="local",
        reversibility="reversible",
        complexity="trivial",
        recorded_at="2026-10-29T00:00:00Z",
        actor="seat-example",
    )
    assert stamped["recorded_at"] == "2026-10-29T00:00:00Z", (
        "a caller-supplied timestamp is carried verbatim (C-27)"
    )
    assert stamped["actor"] == "seat-example"
    assert stamped["verdict"] == record["verdict"], (
        "stamping the record MUST NOT change the verdict"
    )


# ---------------------------------------------------------------------------
# 2. Precedence and adjudication
# ---------------------------------------------------------------------------


def test_missing_input_never_returns_direct():
    """quickstart S3 — an absent tier does not fall through to direct (C-23)."""
    record, proc = _route(
        nature="maintenance",
        traceability="not-required",
        blast_radius="local",
        reversibility="reversible",
    )
    assert proc.returncode == 0, (
        f"adjudicate is a produced verdict, not an error status (C-28): "
        f"rc={proc.returncode} err={proc.stderr!r}"
    )
    assert record is not None
    assert record["verdict"] == ADJUDICATE, (
        f"a required input is missing, so every supplied value pointing at direct is not "
        f"enough: {record!r}"
    )
    assert record["verdict"] != DIRECT
    assert record["reason_code"] == _reason("input-missing")
    assert "input-missing" in record["triggered_conditions"], (
        f"the record MUST name the condition that fired: {record!r}"
    )


def test_ambiguous_value_returns_adjudicate():
    record, proc = _route(
        nature="maintenance",
        traceability="not-required",
        blast_radius="local",
        reversibility="reversible",
        complexity="__outside-every-declared-domain__",
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record["verdict"] == ADJUDICATE
    assert record["reason_code"] == _reason("input-ambiguous"), (
        f"a value outside the closed domain is ambiguous, never coerced (C-23): {record!r}"
    )


def test_conflicting_inputs_return_adjudicate():
    """quickstart S3, second form: a feature change cannot be a bounded correction."""
    record, proc = _route(
        nature="feature",
        traceability="not-required",
        blast_radius="local-bounded-definition-correction",
        reversibility="reversible",
        complexity="trivial",
        rationale="tighten one sentence in one definition file",
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record["verdict"] == ADJUDICATE, (
        f"the conflict set's enumerated combination MUST adjudicate (C-24): {record!r}"
    )
    assert record["reason_code"] == _reason("input-conflicting")
    assert "input-conflicting" in record["triggered_conditions"]


def test_adjudicate_outranks_every_sdd_condition():
    """Precedence: [[STR-006]] first, then [[STR-004]] (C-23)."""
    record, proc = _route(
        nature="feature",
        traceability="required",
        blast_radius="cross-cutting",
        reversibility="hard",
        complexity="__outside-every-declared-domain__",
    )
    assert proc.returncode == 0
    assert "nature-feature" in record["triggered_conditions"], (
        f"the sdd branch MUST be reachable in this case, otherwise the precedence is not "
        f"being tested: {record!r}"
    )
    assert record["verdict"] == ADJUDICATE, (
        f"an adjudicate condition outranks every sdd condition: {record!r}"
    )


def test_reason_code_follows_the_declared_order_and_carries_every_condition():
    record, proc = _route(
        nature="feature",
        traceability="required",
        blast_radius="cross-cutting",
        reversibility="hard",
        complexity="high-stakes",
    )
    assert proc.returncode == 0
    held = set(record["triggered_conditions"])
    rows = _reason_rows()
    expected = next(
        row["code"]
        for row in rows
        if row["verdict"] == SDD and (row["condition"] is None or row["condition"] in held)
    )
    assert record["reason_code"] == expected, (
        f"several sdd conditions fired; the reason code MUST be the first one in the "
        f"owner's declared order: {record!r}"
    )
    assert record["reason_code"] == _reason("nature-feature")
    sdd_conditions = set(_verdict_rows()[SDD]["conditions"])
    assert sdd_conditions <= held, (
        f"every triggered condition MUST be carried, not only the one that named the "
        f"reason code (C-24): missing {sorted(sdd_conditions - held)}"
    )


def test_definition_class_defaults_to_cross_cutting():
    """C-20 — a plain local radius is not accepted as equivalent."""
    record, proc = _route(
        nature="definition-class",
        traceability="not-required",
        blast_radius="local",
        reversibility="reversible",
        complexity="trivial",
    )
    assert proc.returncode == 0
    assert record["effective_blast_radius"] == "cross-cutting", (
        f"a definition-class change is cross-cutting by default (C-20): {record!r}"
    )
    assert record["verdict"] == SDD, (
        f"the cross-cutting default MUST keep it out of the direct branch: {record!r}"
    )
    assert record["reason_code"] == _reason("blast-cross-cutting")


def test_bounded_definition_correction_with_rationale_returns_direct():
    """C-20 / FR-010 — the escape is a distinct declared value with a non-empty rationale."""
    record, proc = _route(
        nature="definition-class",
        traceability="not-required",
        blast_radius="local-bounded-definition-correction",
        reversibility="reversible",
        complexity="trivial",
        rationale="tighten one sentence in one definition file",
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record["verdict"] == DIRECT, (
        f"a bounded correction satisfying every remaining condition routes to direct: "
        f"{record!r}"
    )
    assert record["effective_blast_radius"] == "local-bounded-definition-correction"


def test_bounded_definition_correction_without_rationale_is_a_missing_input():
    record, proc = _route(
        nature="definition-class",
        traceability="not-required",
        blast_radius="local-bounded-definition-correction",
        reversibility="reversible",
        complexity="trivial",
    )
    assert proc.returncode == 0
    assert record["verdict"] == ADJUDICATE, (
        f"a bounded correction with no rationale is a missing input, never an assumed one "
        f"(C-20): {record!r}"
    )
    assert record["reason_code"] == _reason("input-missing")


# ---------------------------------------------------------------------------
# 3. Exit alphabet and read-only behaviour
# ---------------------------------------------------------------------------


def test_exit_alphabet_has_exactly_two_meanings(tmp_path):
    produced = [
        _argv(
            "route",
            nature="feature",
            traceability="required",
            blast_radius="cross-cutting",
            reversibility="hard",
            complexity="standard",
        ),
        _argv(
            "route",
            nature="maintenance",
            traceability="not-required",
            blast_radius="local",
            reversibility="reversible",
            complexity="standard",
        ),
        _argv(
            "route",
            nature="maintenance",
            traceability="not-required",
            blast_radius="local",
            reversibility="reversible",
        ),
        _argv(
            "route",
            nature="maintenance",
            traceability="not-required",
            blast_radius="local",
            reversibility="reversible",
            complexity="__outside-every-declared-domain__",
        ),
        _argv("golden"),
    ]
    for argv in produced:
        proc = _run(argv)
        assert proc.returncode == 0, (
            f"every produced verdict exits 0, adjudicate included (C-28): "
            f"rc={proc.returncode} argv={argv[2:]} err={proc.stderr!r}"
        )

    missing_doc = tmp_path / "absent-owner.md"
    proc = _run(_argv("route", nature="feature", owner_doc=missing_doc))
    assert proc.returncode == 2, (
        f"an unreadable owner document is an input error, not a verdict (C-28): "
        f"rc={proc.returncode} out={proc.stdout!r}"
    )
    assert proc.stdout.strip() == "", "an input error emits no verdict on stdout"

    garbled = tmp_path / "garbled-owner.md"
    text = _owner_text()
    start = text.index("## Verdict table")
    end = text.index("## Precedence")
    garbled.write_text(text[:start] + text[end:], encoding="utf-8")
    proc = _run(_argv("route", nature="feature", owner_doc=garbled))
    assert proc.returncode == 2, (
        f"a document missing one of the four facts is an input error, never a degraded "
        f"verdict: rc={proc.returncode} out={proc.stdout!r}"
    )
    assert "Verdict table" in proc.stderr, (
        f"the diagnostic MUST name the surface it could not read: {proc.stderr!r}"
    )


def test_route_and_golden_write_no_file(tmp_path):
    working = tmp_path / "cwd"
    working.mkdir()
    engine_before, doc_before = _fingerprint(ENGINE, OWNER_DOC)
    _run(_argv("route", nature="feature", traceability="required"), cwd=working)
    _run(_argv("route", nature="definition-class", blast_radius="local"), cwd=working)
    _run(_argv("golden"), cwd=working)
    assert list(working.iterdir()) == [], (
        "the engine is read-only: no file may be created in the working directory (C-28)"
    )
    assert _fingerprint(ENGINE, OWNER_DOC) == {
        str(ENGINE): engine_before,
        str(OWNER_DOC): doc_before,
    }, "the engine MUST NOT rewrite itself or its owner document (C-28)"


# ---------------------------------------------------------------------------
# 4. The four facts are read from the owner document, never copied into the engine
# ---------------------------------------------------------------------------


def test_engine_carries_no_second_copy_of_the_owner_facts():
    source = ENGINE.read_text(encoding="utf-8")
    normalized = re.sub(r"[^0-9A-Za-z_]+", "", source)
    findings = []

    for row in _reason_rows():
        if f'"{row["code"]}"' in source or f"'{row['code']}'" in source:
            findings.append(f"reason code {row['code']!r} is written into the engine")
        for other in _reason_rows():
            if other is row:
                continue
            sequence = row["code"] + other["code"]
            if sequence in normalized:
                findings.append(f"reason codes {row['code']!r} + {other['code']!r} are adjacent")

    for verdict in _precedence():
        if f'"{verdict}"' in source or f"'{verdict}'" in source:
            findings.append(f"verdict literal {verdict!r} is written into the engine")

    for input_id, spec in _inputs().items():
        for value in spec["domain"]:
            if f'"{value}"' in source or f"'{value}'" in source:
                findings.append(f"domain value {input_id}={value!r} is written into the engine")
        sequence = "".join(spec["domain"])
        if sequence and sequence in normalized:
            findings.append(f"the {input_id} domain is written out as a sequence in the engine")

    for verdict, row in _verdict_rows().items():
        sequence = "".join(row["conditions"])
        if sequence and sequence in normalized:
            findings.append(f"the {verdict} condition list is written out in the engine")

    assert not findings, (
        "the engine MUST take the value domains, the verdict table, the precedence and the "
        "reason codes from the owner document at run time (C-28, FR-014):\n"
        + "\n".join(findings)
    )


def test_route_follows_a_renamed_reason_code(tmp_path):
    original = _reason("nature-feature")
    renamed = _mutate(tmp_path, f"`{original}`", "`capability-change-renamed`")
    record, proc = _route(
        nature="feature",
        traceability="required",
        blast_radius="cross-cutting",
        reversibility="hard",
        complexity="standard",
        owner_doc=renamed,
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record["reason_code"] == "capability-change-renamed", (
        f"the reason code MUST come from the owner document at run time, not from the "
        f"engine: {record!r}"
    )


def test_route_follows_a_reordered_precedence(tmp_path):
    body = _section_body("Precedence")
    line = next(
        (line for line in body.splitlines() if line.count("`") >= 6 and ">" in line), None
    )
    assert line is not None
    reordered = (
        line.replace(f"`{ADJUDICATE}`", "__first__")
        .replace(f"`{SDD}`", f"`{ADJUDICATE}`")
        .replace("__first__", f"`{SDD}`")
    )
    assert reordered != line and reordered.count("`") >= 6
    mutated = _mutate(tmp_path, line, reordered)
    record, proc = _route(
        nature="feature",
        traceability="required",
        blast_radius="cross-cutting",
        reversibility="hard",
        complexity="__outside-every-declared-domain__",
        owner_doc=mutated,
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record["verdict"] == SDD, (
        f"with the precedence reversed the same inputs MUST follow the mutated document — "
        f"the order is data, not code (C-28): {record!r}"
    )


def test_route_follows_a_mutated_value_domain(tmp_path):
    reversible, hard = _inputs()["reversibility"]["domain"]
    mutated = _mutate(tmp_path, f"`{reversible}` / `{hard}`", f"`{reversible}` / `{hard}-narrowed`")
    record, proc = _route(
        nature="maintenance",
        traceability="not-required",
        blast_radius="local",
        reversibility=hard,
        complexity="standard",
        owner_doc=mutated,
    )
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    assert record["verdict"] == ADJUDICATE, (
        f"a value no longer in the mutated domain MUST be ambiguous — the domain is read "
        f"from the document (C-28): {record!r}"
    )
    assert record["reason_code"] == _reason("input-ambiguous")


# ---------------------------------------------------------------------------
# 5. The golden table is judged, not copied
# ---------------------------------------------------------------------------


def test_golden_judges_every_row_of_the_owner_table():
    rows = _golden_rows()
    payload, proc = _golden()
    assert proc.returncode == 0, (
        f"golden judges every row and produces a verdict per row, so it exits 0 (C-28): "
        f"rc={proc.returncode} err={proc.stderr!r}"
    )
    assert payload is not None, f"--format json MUST emit a payload: {proc.stdout!r}"
    assert payload["case_count"] == len(rows), (
        f"golden MUST judge every row of the owner's table ({len(rows)}), not a subset: "
        f"{payload['case_count']}"
    )
    assert [case["case_id"] for case in payload["cases"]] == [row["case_id"] for row in rows], (
        "the judged order MUST be the table's order, so the output is reproducible"
    )
    for case, row in zip(payload["cases"], rows):
        assert case["expected_verdict"] == row["expected_verdict"]
        assert case["expected_reason_code"] == row["expected_reason_code"]
        assert case["actual_verdict"] == row["expected_verdict"], (
            f"case {row['case_id']!r} ({row['face']}) judged {case['actual_verdict']!r}, "
            f"expected {row['expected_verdict']!r}: {case!r}"
        )
        assert case["actual_reason_code"] == row["expected_reason_code"], (
            f"case {row['case_id']!r} took reason code {case['actual_reason_code']!r}, "
            f"expected {row['expected_reason_code']!r}"
        )
        assert case["match"] is True
    assert payload["all_match"] is True


def test_golden_output_is_byte_identical_across_runs():
    first, first_proc = _golden()
    second, second_proc = _golden()
    assert first_proc.returncode == 0 and second_proc.returncode == 0
    assert first_proc.stdout == second_proc.stdout, (
        "re-judging the same table MUST produce byte-identical output (C-24, C-29)"
    )
    assert first["case_count"] == second["case_count"]


def test_ambiguous_and_conflicting_rows_never_return_direct():
    payload, proc = _golden()
    assert proc.returncode == 0, f"rc={proc.returncode} err={proc.stderr!r}"
    faced = {
        "ambiguous": _reason("input-ambiguous"),
        "conflicting": _reason("input-conflicting"),
        "missing": _reason("input-missing"),
    }
    seen = {}
    for case in payload["cases"]:
        for name, code in faced.items():
            if case["expected_reason_code"] == code:
                seen.setdefault(name, []).append(case)
    for name in ("ambiguous", "conflicting"):
        assert seen.get(name), (
            f"the golden table MUST cover the {name} face with a row of its own (C-29)"
        )
        for case in seen[name]:
            assert case["actual_verdict"] == ADJUDICATE, (
                f"the {name} row {case['case_id']!r} MUST adjudicate, not "
                f"{case['actual_verdict']!r} (C-23)"
            )
            assert case["actual_verdict"] != DIRECT
