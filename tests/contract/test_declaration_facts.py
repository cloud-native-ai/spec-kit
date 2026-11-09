"""Contract tests for the two 094 declaration facts and their registration.

Feature 094, `contracts/command-family-and-declarations.md` C-76…C-87; tasks rows
T025, T026, T027, T051, T053, T054, T055, T056, T057, T058. Every fact is read through
the layer's one parser (`scripts/python/declaration_reader.py`, `parse_subset`) and
every decision is driven through the engine CLI a consumer actually calls — never
through a helper only the test can reach.

The threshold value is deliberately NOT pinned in this module: it is read from the fact
file so changing the declared number stays a one-file edit (C-82). The same reason keeps
T054's guard free of the number: an absent fact must refuse, never fall back to one.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
READER = REPO_ROOT / "scripts/python/declaration_reader.py"
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"
FACTS_DIR = REPO_ROOT / "shared/declarations/facts"
FAMILY_FACT = FACTS_DIR / "goal-team-command-family.yaml"
THRESHOLD_FACT = FACTS_DIR / "goal-team-handoff-threshold.yaml"
FAMILY_SLUG = "goal-team-command-family"
THRESHOLD_SLUG = "goal-team-handoff-threshold"

MANDATORY_FACT_KEYS = {"fact", "kind", "statement", "consumers", "former_carriers"}

# The contract keys that existed before this feature's registration. T056 is additive:
# every one of them survives, and the new section is the only addition (C-86).
PRE_EXISTING_CONTRACT_KEYS = {
    "schema", "yaml_subset", "fact_kinds", "completeness_states",
    "exclusion_reasons", "exit_codes", "required_fact_keys",
    "required_exclusion_keys", "gate_call_sites",
}

TASK_ROW = "- [ ] T{n:03d} deliver the fixture row"


def _load_reader():
    spec = importlib.util.spec_from_file_location("declaration_reader_094", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dr = _load_reader()


def _fact_text(path: Path) -> str:
    assert path.is_file(), f"declaration fact missing: {path}"
    return path.read_text(encoding="utf-8")


def _fact_body(path: Path) -> dict:
    body = dr.parse_subset(_fact_text(path), str(path))
    assert isinstance(body, dict), f"{path} does not parse as a mapping"
    return body


def _threshold() -> int:
    """The declared threshold, read from its one owner — never a literal in this file.

    The layer's subset parser yields scalars as strings, so the integer lives in the
    scalar's shape; the consumer validates and converts it (C-85).
    """
    statement = _fact_body(THRESHOLD_FACT)["statement"]
    value = statement["threshold"]
    assert re.fullmatch(r"[0-9]+", str(value)), (
        f"threshold must be an integer literal, got {value!r}")
    return int(value)


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args, "--repo-root", str(root), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)


def _tasks_file(directory: Path, count: int) -> Path:
    path = directory / f"tasks-{count}.md"
    rows = "\n".join(TASK_ROW.format(n=index)
                     for index in range(1, count + 1))
    path.write_text(f"# Tasks\n\n{rows}\n", encoding="utf-8")
    return path


@pytest.fixture()
def sandbox():
    """The sanctioned scratch root (`.specify/.tmp/`), one directory per test."""
    base = REPO_ROOT / ".specify/.tmp/s094"
    base.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="decl-", dir=str(base)))
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _declaration_fixture(sandbox: Path, *, drop_threshold: bool = False) -> Path:
    """A repo root carrying the declaration layer, the class owner and the carriers."""
    shutil.copytree(REPO_ROOT / "shared/declarations", sandbox / "shared/declarations")
    definitions = sandbox / "shared/definitions"
    definitions.mkdir(parents=True)
    shutil.copyfile(REPO_ROOT / "shared/definitions/flow-class-definitions.md",
                    definitions / "flow-class-definitions.md")
    shutil.copytree(REPO_ROOT / "templates/commands", sandbox / "templates/commands")
    if drop_threshold:
        (sandbox / "shared/declarations/facts" / THRESHOLD_FACT.name).unlink()
    return sandbox


# ---------------------------------------------------------------------------
# T025 / C-76 / C-78 — the command-family fact carries its mandatory keys
# ---------------------------------------------------------------------------
def test_the_command_family_fact_carries_its_mandatory_keys():
    body = _fact_body(FAMILY_FACT)
    missing = MANDATORY_FACT_KEYS - set(body)
    assert not missing, f"command-family fact lacks mandatory key(s): {sorted(missing)}"
    assert body["fact"] == FAMILY_SLUG
    assert body["kind"] == "closed-set"
    statement = body["statement"]
    assert isinstance(statement, list), (
        "statement is the explicit addition list; the empty list is legal (C-76)")
    assert all(isinstance(name, str) and "/" not in name for name in statement), (
        f"statement entries are bare command stems: {statement!r}")
    consumers = body["consumers"]
    assert any("goal-utils.py" in str(item) for item in consumers), (
        "the engine read action is a declared consumption point (C-74)")
    assert any("create-team" in str(item) for item in consumers), (
        "create-team is the second declared consumption point (C-74)")
    # C-73's carrier: the first evidence command must exist as a command template.
    assert (REPO_ROOT / "templates/commands/feedback.md").is_file(), (
        "/speckit.feedback is the first evidence command (C-73)")


# ---------------------------------------------------------------------------
# T027 / C-78 — both new facts parse under the layer's subset
# ---------------------------------------------------------------------------
def test_both_new_facts_parse_under_the_declaration_subset():
    for path in (FAMILY_FACT, THRESHOLD_FACT):
        body = _fact_body(path)
        missing = MANDATORY_FACT_KEYS - set(body)
        assert not missing, f"{path.name} lacks mandatory key(s): {sorted(missing)}"
    # The reader discovers both by glob — the file, not a second list, is the identity.
    assert dr.load_fact(str(REPO_ROOT), FAMILY_SLUG)["stem"] == FAMILY_FACT.stem
    assert dr.load_fact(str(REPO_ROOT), THRESHOLD_SLUG)["stem"] == THRESHOLD_FACT.stem
    contract = dr.load_contract(str(REPO_ROOT))
    assert set(contract["required_fact_keys"]) == MANDATORY_FACT_KEYS, (
        "the layer's mandatory-key set and this module's copy disagree")


# ---------------------------------------------------------------------------
# T053 / C-79 / C-80 — threshold fact declares boundary and the timing pair
# ---------------------------------------------------------------------------
def test_the_handoff_threshold_fact_declares_the_boundary_and_the_timing_pair():
    body = _fact_body(THRESHOLD_FACT)
    assert body["fact"] == THRESHOLD_SLUG
    assert body["kind"] == "threshold"
    statement = body["statement"]
    assert isinstance(statement, dict), "the threshold statement is a mapping"
    assert statement["metric"] == "task-count"
    assert re.fullmatch(r"[0-9]+", str(statement["threshold"])), (
        "threshold must be an integer literal")
    assert statement["boundary"] == "exclusive", (
        "complex iff task count > threshold; equality stays on the simple side")
    assert statement["on_direct"] == "none", (
        "a direct run creates no goal/team (FR-039)")
    assert statement["on_handoff"] == "after-tasks-u4", (
        "a handoff run creates goal/team after tasks U4 (FR-039)")
    assert any("goal-utils.py" in str(item) for item in body["consumers"]), (
        "the handoff-decision action is the declared consumption point (C-81)")


# ---------------------------------------------------------------------------
# T026 / C-77 — a declared addition without a carrier is an input error
# ---------------------------------------------------------------------------
def test_a_declared_addition_without_a_carrier_is_an_input_error(sandbox):
    root = _declaration_fixture(sandbox)
    fact = root / "shared/declarations/facts" / FAMILY_FACT.name
    text = fact.read_text(encoding="utf-8")
    assert "statement: []" in text, "the fact's empty addition list moved; update this fixture"
    fact.write_text(
        text.replace("statement: []", "statement:\n  - ghostcommand"), encoding="utf-8")
    assert not (root / "templates/commands/ghostcommand.md").exists()

    proc = _run(root, "command-family", "--command", "feedback")
    assert proc.returncode == 2, (
        "a declared addition whose carrier does not exist is an input error at read "
        f"time (C-77); got exit {proc.returncode}: {proc.stdout!r} {proc.stderr!r}")
    assert "ghostcommand" in (proc.stdout + proc.stderr), (
        "the refusal must name the addition without a carrier")


# ---------------------------------------------------------------------------
# T051 / C-79 / C-80 — one declared value decides complexity AND creation timing
# ---------------------------------------------------------------------------
def test_the_threshold_decides_both_complexity_and_creation_timing(sandbox):
    threshold = _threshold()

    at_boundary = _tasks_file(sandbox, threshold)
    proc = _run(REPO_ROOT, "handoff-decision", "--tasks", str(at_boundary))
    assert proc.returncode == 0, (
        f"handoff-decision failed: {proc.stdout!r} {proc.stderr!r}")
    payload = json.loads(proc.stdout)
    assert payload["task_count"] == threshold, (
        "the measured task count is the count of task rows")
    assert payload["threshold"] == threshold, (
        "the declared threshold is reported, not restated by the engine")
    assert payload["decision"] == "direct", (
        "equality is on the simple side: complex iff task count > threshold")
    assert payload["creation"]["on_direct"] == "none", (
        "the direct decision's creation timing comes from the same statement")

    above = _tasks_file(sandbox, threshold + 1)
    proc = _run(REPO_ROOT, "handoff-decision", "--tasks", str(above))
    assert proc.returncode == 0, (
        f"handoff-decision failed: {proc.stdout!r} {proc.stderr!r}")
    payload = json.loads(proc.stdout)
    assert payload["task_count"] == threshold + 1
    assert payload["decision"] == "handoff", (
        "one row above the threshold is complex")
    assert payload["creation"]["on_handoff"] == "after-tasks-u4", (
        "the handoff decision's creation timing comes from the same statement")


# ---------------------------------------------------------------------------
# T054 / C-81 / C-83 — an absent fact refuses, never a built-in number
# ---------------------------------------------------------------------------
def test_handoff_decision_refuses_when_the_fact_is_unavailable(sandbox):
    root = _declaration_fixture(sandbox, drop_threshold=True)
    tasks = _tasks_file(root, 3)

    proc = _run(root, "handoff-decision", "--tasks", str(tasks))
    assert proc.returncode == 2, (
        "an unavailable fact exits 2 (owner-unavailable), never a default: "
        f"got {proc.returncode}: {proc.stdout!r} {proc.stderr!r}")
    combined = proc.stdout + proc.stderr
    assert "owner-unavailable" in combined, (
        f"the refusal names the degradation label; got {combined!r}")
    payload = json.loads(proc.stdout)
    assert payload.get("decision") is None, (
        "no decision may be produced from a missing fact")
    assert payload.get("threshold") is None, (
        "never fall back to a built-in threshold number (C-81)")


# ---------------------------------------------------------------------------
# T056 / C-83 / C-84 / C-85 — both facts are registered with subset and domain
# ---------------------------------------------------------------------------
def test_both_facts_are_registered_with_subset_and_value_domain():
    contract = dr.load_contract(str(REPO_ROOT))
    missing = PRE_EXISTING_CONTRACT_KEYS - set(contract)
    assert not missing, (
        f"registration is additive; pre-existing contract keys vanished: {sorted(missing)}")
    rows = contract.get("registered_facts")
    assert isinstance(rows, list) and rows, (
        "contract.yaml carries a registered_facts sequence (C-83)")
    registered = {row.get("fact"): row for row in rows if isinstance(row, dict)}
    for slug, domain in ((FAMILY_SLUG, "closed-set"),
                         (THRESHOLD_SLUG, "threshold+timing-map")):
        assert slug in registered, f"{slug} is not registered (C-83)"
        row = registered[slug]
        assert row.get("subset_id") == "declaration-subset/v1", (
            f"{slug} is written in the declaration subset grammar (C-84)")
        assert row.get("value_domain") == domain, (
            f"{slug} registers its closed value domain (C-85)")
        keys = row.get("statement_keys") or []
        assert keys, f"{slug} names the statement keys it validates"
        # The registration is only meaningful if the reader can see the facts it names.
        assert dr.load_fact(str(REPO_ROOT), slug)["body"]["fact"] == slug

    family_keys = set(registered[FAMILY_SLUG]["statement_keys"])
    assert family_keys == {"statement"}, (
        "the family statement is the addition list")
    threshold_keys = set(registered[THRESHOLD_SLUG]["statement_keys"])
    assert {"metric", "threshold", "boundary", "on_direct", "on_handoff"} <= threshold_keys, (
        "the threshold registration names every statement key the consumer validates")


# ---------------------------------------------------------------------------
# T055 / C-82 — the threshold literal lives only in its fact file
# ---------------------------------------------------------------------------
#: The three surface families the row names: engine constants, driver sentences and
#: command templates. The `.specify/` mirrors are byte-identical projections of these
#: sources (`sync-mirrors.py --check`), so scanning the sources covers both forms
#: without reporting every hit twice. Third-party skills ship their own unrelated
#: thresholds and exit codes, so the scan stays on the surfaces that carry this fact.
THRESHOLD_SCAN_SURFACES = (
    "scripts/python/goal-utils.py",       # the engine that could hold a constant
    "skills/external/sdd-loop-driver",    # driver sentences
    "templates/commands",                 # command templates
)
THRESHOLD_SCAN_SUFFIXES = (".py", ".md", ".sh", ".yaml", ".yml", ".json")
THRESHOLD_CONTEXT = re.compile(r"threshold|阈值|task[_-]?count|任务数", re.IGNORECASE)


def test_the_threshold_literal_exists_only_in_its_fact_file():
    threshold = _threshold()
    number = re.compile(r"(?<![0-9])%d(?![0-9])" % threshold)
    offenders = []
    for surface in THRESHOLD_SCAN_SURFACES:
        root = REPO_ROOT / surface
        paths = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in THRESHOLD_SCAN_SUFFIXES:
                continue
            for lineno, line in enumerate(
                    path.read_text(encoding="utf-8").splitlines(), 1):
                if THRESHOLD_CONTEXT.search(line) and number.search(line):
                    offenders.append(
                        f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}")
    assert not offenders, (
        f"the declared threshold {threshold} MUST stay a one-file edit (C-82); it is "
        "restated in a threshold sentence outside "
        f"{THRESHOLD_FACT.relative_to(REPO_ROOT)}:\n" + "\n".join(offenders))
    assert str(_fact_body(THRESHOLD_FACT)["statement"]["threshold"]) == str(threshold), (
        "the owner is the fact file; the guard must read the same number it scanned for")


# ---------------------------------------------------------------------------
# T057 / C-84 / C-85 — another grammar or another domain is refused at load
# ---------------------------------------------------------------------------
def test_a_fact_in_another_grammar_is_refused_at_load(sandbox):
    root = _declaration_fixture(sandbox)
    tasks = _tasks_file(root, 2)
    contract_path = root / "shared/declarations/contract.yaml"
    fact_path = root / "shared/declarations/facts" / THRESHOLD_FACT.name
    contract_text = contract_path.read_text(encoding="utf-8")
    fact_text = fact_path.read_text(encoding="utf-8")

    # Control: the unmutated fixture answers both questions, so every refusal below is
    # caused by the mutation alone and not by the fixture.
    proc = _run(root, "handoff-decision", "--tasks", str(tasks))
    assert proc.returncode == 0, (
        f"the unmutated fixture must decide: {proc.stdout!r} {proc.stderr!r}")
    proc = _run(root, "command-family", "--command", "feedback")
    assert proc.returncode == 0, (
        f"the unmutated fixture must answer the family lookup: "
        f"{proc.stdout!r} {proc.stderr!r}")

    # A fact file written outside the subset grammar is refused when it is loaded.
    fact_path.write_text(fact_text.replace(
        "boundary: exclusive", "boundary: [exclusive]"), encoding="utf-8")
    proc = _run(root, "handoff-decision", "--tasks", str(tasks))
    assert proc.returncode == 2, (
        "a fact written outside the subset grammar is an input error at load: "
        f"got {proc.returncode}: {proc.stdout!r} {proc.stderr!r}")
    combined = proc.stdout + proc.stderr
    assert "owner-unavailable" in combined, (
        f"the refusal names the degraded load; got {combined!r}")
    assert "outside the subset" in combined, (
        f"the refusal names the grammar breach; got {combined!r}")
    fact_path.write_text(fact_text, encoding="utf-8")

    # A fact registered under a grammar the shared reader does not implement.
    contract_path.write_text(contract_text.replace(
        "  - fact: goal-team-handoff-threshold\n    subset_id: declaration-subset/v1",
        "  - fact: goal-team-handoff-threshold\n    subset_id: yaml/v0"), encoding="utf-8")
    proc = _run(root, "handoff-decision", "--tasks", str(tasks))
    assert proc.returncode == 2, (
        f"another registered grammar must be refused: {proc.stdout!r} {proc.stderr!r}")
    combined = proc.stdout + proc.stderr
    assert "declaration-invalid" in combined, (
        f"the refusal names the declaration label; got {combined!r}")
    assert "yaml/v0" in combined and "declaration-subset/v1" in combined, (
        "the refusal names both grammars")
    payload = json.loads(proc.stdout)
    assert payload["decision"] is None and payload["threshold"] is None, (
        "no decision may be produced from a fact refused at load (C-84)")

    contract_path.write_text(contract_text.replace(
        "  - fact: goal-team-command-family\n    subset_id: declaration-subset/v1",
        "  - fact: goal-team-command-family\n    subset_id: yaml/v0"), encoding="utf-8")
    proc = _run(root, "command-family", "--command", "feedback")
    assert proc.returncode == 2, (
        "the family consumer refuses another registered grammar too: "
        f"{proc.stdout!r} {proc.stderr!r}")
    assert "declaration-invalid" in (proc.stdout + proc.stderr)

    # Both consumers validate against the registered value_domain, never a private copy.
    for old_domain, new_domain, args in (
        ("value_domain: closed-set", "value_domain: ordered-operator-table",
         ("command-family", "--command", "feedback")),
        ("value_domain: threshold+timing-map", "value_domain: closed-set",
         ("handoff-decision", "--tasks", str(tasks))),
    ):
        contract_path.write_text(contract_text.replace(old_domain, new_domain),
                                 encoding="utf-8")
        proc = _run(root, *args)
        assert proc.returncode == 2, (
            f"a registered domain the consumer does not implement must be refused: "
            f"{proc.stdout!r} {proc.stderr!r}")
        combined = proc.stdout + proc.stderr
        assert "declaration-invalid" in combined, (
            f"the refusal names the declaration label; got {combined!r}")
        assert new_domain.split(": ")[1] in combined, (
            "the refusal names the registered domain")
        assert old_domain.split(": ")[1] in combined, (
            "the refusal names the domain this consumer implements")

    # Restored, the fixture decides again: the refusal tracks the registration only.
    contract_path.write_text(contract_text, encoding="utf-8")
    proc = _run(root, "handoff-decision", "--tasks", str(tasks))
    assert proc.returncode == 0, (
        f"the restored fixture must decide again: {proc.stdout!r} {proc.stderr!r}")


# ---------------------------------------------------------------------------
# T058 / C-86 / C-87 — additive registration; both consumers inside the owned engines
# ---------------------------------------------------------------------------
IN_SCOPE_CONSUMERS = {
    "scripts/python/goal-utils.py",
    "skills/internal/create-team/SKILL.md",
}
OUT_OF_SCOPE_SCRIPTS = (
    "scripts/python/flow-class-check.py",
    "skills/external/sdd-loop-driver/scripts/run-stage.sh",
    "skills/external/sdd-loop-driver/scripts/stage-runner.sh",
)


def test_registration_is_additive_and_both_consumers_are_in_scope():
    contract_path = REPO_ROOT / "shared/declarations/contract.yaml"
    contract = dr.load_contract(str(REPO_ROOT))

    # C-86 — nothing pre-existing was renamed or removed; the registration sequence is
    # the one addition, appended after every key it must not disturb.
    vanished = PRE_EXISTING_CONTRACT_KEYS - set(contract)
    assert not vanished, f"pre-existing contract keys vanished: {sorted(vanished)}"
    assert set(contract) - PRE_EXISTING_CONTRACT_KEYS == {"registered_facts"}, (
        "the registration is the only change to contract.yaml (C-86); unexpected keys: "
        f"{sorted(set(contract) - PRE_EXISTING_CONTRACT_KEYS - {'registered_facts'})}")
    top_level = re.findall(r"^([a-z_]+):", contract_path.read_text(encoding="utf-8"),
                           re.MULTILINE)
    assert top_level[-1] == "registered_facts" and top_level.count("registered_facts") == 1, (
        "the registration is appended as the last top-level section, never interleaved")

    rows = contract["registered_facts"]
    assert sorted(row["fact"] for row in rows) == sorted((FAMILY_SLUG, THRESHOLD_SLUG)), (
        "one registration row per new fact, no duplicates")

    # C-87 — every declared consumption point exists and lives in an engine this feature
    # owns or modifies: `goal-utils.py` and the `create-team` skill.
    for slug in (FAMILY_SLUG, THRESHOLD_SLUG):
        consumers = {str(item) for item in _fact_body(FACTS_DIR / f"{slug}.yaml")["consumers"]}
        stray = consumers - IN_SCOPE_CONSUMERS
        assert not stray, (
            f"{slug} declares consumption point(s) outside goal-utils.py / create-team: "
            f"{sorted(stray)} (C-87)")
        for consumer in consumers:
            assert (REPO_ROOT / consumer).is_file(), (
                f"{slug} declares a consumer that does not exist: {consumer}")

    engine_text = (REPO_ROOT / "scripts/python/goal-utils.py").read_text(encoding="utf-8")
    for action in ("command-family", "handoff-decision"):
        assert f'"{action}"' in engine_text, (
            f"the engine does not implement the {action!r} action (C-74/C-81)")
    skill_text = (REPO_ROOT / "skills/internal/create-team/SKILL.md").read_text(
        encoding="utf-8")
    for invocation in ("command-family --command", "handoff-decision --tasks"):
        assert invocation in skill_text, (
            f"create-team does not invoke the {invocation!r} consumption point (C-74)")

    for path in OUT_OF_SCOPE_SCRIPTS:
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        for slug in (FAMILY_SLUG, THRESHOLD_SLUG):
            assert slug not in text, (
                f"{path} MUST NOT consume {slug}; the consumption points stay in "
                "goal-utils.py and create-team (C-87)")
