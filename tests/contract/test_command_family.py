"""Contract tests for the command-family predicate (094, C-71…C-75, C-87).

Tasks rows T020, T021, T023, T024. The module drives the engine as a subprocess, exactly
as a consumer does: `goal-utils.py command-family --command <name> --json`. The verdict
is the lookup's `source` field (`ledger` = in family, `default` = not in family); neither
`flow_class` nor an exit code is a family criterion (C-71).

Shape pinned by this module (no contract page fixes the JSON keys):
``{"command", "unit_id", "in_family", "source", "flow_class", "marker"}`` — a degraded
lookup additionally carries the lookup's `error` label and exits 2, while a decided
`default` verdict exits 0.

Red-first note (T020 owns this module's green point): at authoring time the engine action
does not exist yet — its implementation is outside this fork's write domain — so the
action-driven tests are recorded red before the engine rows land.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"
FLOW_CLASS = REPO_ROOT / "scripts/python/flow-class-check.py"
COMMANDS_DIR = REPO_ROOT / "templates/commands"
CREATE_TEAM_SKILL = REPO_ROOT / "skills/internal/create-team/SKILL.md"

# Measured 2026-11-09 (last touching commit f7e3b9a9, before this feature's branch):
# C-74 forbids this feature from modifying flow-class-check.py, so a byte pin is the
# decidable form of "not modified". A literal pinned in a test is a sanctioned copy.
FLOW_CLASS_SHA256 = "c336bf23e3f066df9d083160f077f3fdd086c3c367afa827a0149c91c007f401"

RUN_ID = "r20261109T064500Z-094a"


def _run_engine(root: Path, *args: str) -> subprocess.CompletedProcess:
    return run_engine_in_process(ENGINE, [*args, "--repo-root", str(root), "--json"])


def _family(name: str, root: Path | None = None) -> subprocess.CompletedProcess:
    return _run_engine(root or REPO_ROOT, "command-family", "--command", name)


def _lookup(name: str) -> dict:
    proc = run_engine_in_process(
        FLOW_CLASS,
        ["--action", "lookup", "--unit-id", f"/speckit.{name}", "--format", "json"],
    )
    assert proc.returncode == 0, (
        f"the class lookup must resolve /speckit.{name}: {proc.stdout!r} {proc.stderr!r}")
    return json.loads(proc.stdout)


@pytest.fixture()
def sandbox():
    base = REPO_ROOT / ".specify/.tmp/s094"
    base.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="family-", dir=str(base)))
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _seed_bound_goal(root: Path, slug: str = "alpha") -> Path:
    """A definition in the engine-written canonical binding form (post-create state)."""
    path = root / ".specify/anchoring" / slug / "goal.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "status: active\n"
        "created: 2026-11-09\n"
        "updated: 2026-11-09\n"
        "binding:\n"
        "  owner: command-run\n"
        f"  owner_id: {RUN_ID}\n"
        "  origin: null\n"
        "---\n\n"
        f"# Goal: {slug}\n\n"
        "## Objective\n\n"
        "Stand alone while a command run reads it.\n\n"
        "## Success Criteria\n\n"
        "1. The binding is readable.\n\n"
        "## History\n\n"
        "- 2026-11-09 — created.\n",
        encoding="utf-8")
    return path


def _tree_digest(root: Path) -> dict:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


# ---------------------------------------------------------------------------
# T020 / C-71 / C-74 — the family predicate IS the declared class
# ---------------------------------------------------------------------------
def test_the_family_predicate_is_the_declared_class_not_a_hardcoded_list():
    stems = sorted(path.stem for path in COMMANDS_DIR.glob("*.md"))
    assert stems, "no command carriers found — the class predicate has no subject"

    disagreements = []
    for name in stems:
        proc = _family(name)
        assert proc.returncode == 0, (
            f"command-family {name!r} must answer from the class lookup: "
            f"{proc.stdout!r} {proc.stderr!r}")
        payload = json.loads(proc.stdout)
        record = _lookup(name)
        assert payload["command"] == name
        assert payload["unit_id"] == f"/speckit.{name}", (
            "C-71 fixes the unit-id form: a command:<name> form is rejected by the lookup")
        assert payload["source"] == record["source"], (
            "the action answers from the lookup's source field, not a second table")
        expected = record["source"] == "ledger"
        if payload["in_family"] != expected:
            disagreements.append((name, payload.get("in_family"), record["source"]))
    assert not disagreements, (
        "in_family must equal (source == ledger) for every carrier: "
        f"{disagreements}")


# ---------------------------------------------------------------------------
# T021 / C-71 / C-72 — unregistered carrier, degraded lookup, source: default
# ---------------------------------------------------------------------------
def test_an_unregistered_carrier_is_not_in_the_family_and_readability_is_not_affected(
        sandbox):
    assert not (COMMANDS_DIR / "nonexistentcommand.md").exists()
    proc = _family("nonexistentcommand")
    assert proc.returncode == 0, (
        "an unregistered unit is a decided verdict (source: default, exit 0), "
        f"not an action failure: {proc.stdout!r} {proc.stderr!r}")
    payload = json.loads(proc.stdout)
    record = _lookup("nonexistentcommand")
    assert record["source"] == "default", (
        "the measured lookup must carry the default fallback this test pins")
    assert payload["in_family"] is False, (
        "source: default is NOT in the family even though it exits 0 and carries a "
        "decided flow_class (C-71/C-72)")
    assert payload["source"] == "default"
    assert payload["marker"] == record["marker"], (
        "the action surfaces the lookup's marker instead of re-spelling it")
    assert payload.get("flow_class") == record["flow_class"], (
        "flow_class is carried through for the reader, never used as the criterion")

    # Degraded lookup: the class owner document is absent, so no verdict can be derived.
    fixture = sandbox
    shutil.copytree(REPO_ROOT / "shared/declarations", fixture / "shared/declarations")
    proc = _family("feedback", root=fixture)
    assert proc.returncode == 2, (
        "a degraded class lookup is an input error, never a guessed verdict: "
        f"{proc.stdout!r} {proc.stderr!r}")
    payload = json.loads(proc.stdout)
    assert payload["in_family"] is False, "owner-unavailable is NOT in the family"
    assert "owner-unavailable" in (proc.stdout + proc.stderr), (
        "the refusal carries the lookup's degradation label")


# ---------------------------------------------------------------------------
# T023 / C-74 / C-87 — no second whitelist, no edit of the class engine
# ---------------------------------------------------------------------------
def test_flow_class_check_is_not_modified_and_no_second_whitelist_exists():
    digest = hashlib.sha256(FLOW_CLASS.read_bytes()).hexdigest()
    assert digest == FLOW_CLASS_SHA256, (
        "flow-class-check.py MUST NOT be modified by this feature (C-74); "
        f"measured sha256 {digest}")

    engine_text = ENGINE.read_text(encoding="utf-8")
    assert "flow-class-check" in engine_text, (
        "the engine action must delegate to the class lookup (C-74)")
    assert "--action" in engine_text and "lookup" in engine_text, (
        "the delegation must be the lookup action")
    assert '"/speckit.' in engine_text or "'/speckit." in engine_text, (
        "the action must build the /speckit.<name> unit-id form (C-71)")

    scanned = [path for path in (REPO_ROOT / "scripts").rglob("*.py")]
    scanned += [path for path in (REPO_ROOT / "skills/internal/create-team").rglob("*")
                if path.is_file() and path.suffix in (".py", ".md")]
    token = re.compile(r"/speckit\.([A-Za-z0-9_-]+)")
    collection = re.compile(
        r"(?i)(command_family|family_commands|command_whitelist|command_allowlist)"
        r"\s*=\s*[\[({]")
    offenders = []
    for path in scanned:
        if path == FLOW_CLASS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(text.splitlines(), 1):
            names = set(token.findall(line))
            if len(names) >= 2:
                offenders.append(f"{path}:{lineno}: hardcoded /speckit.* list {sorted(names)}")
            if collection.search(line):
                offenders.append(f"{path}:{lineno}: second family collection")
    assert not offenders, (
        "the family has exactly one predicate (the class ledger) and one declared "
        f"addition list; found: {offenders}")

    skill_text = CREATE_TEAM_SKILL.read_text(encoding="utf-8")
    assert "command-family" in skill_text or "command_family" in skill_text, (
        "create-team is the second consumption point and must cite the engine action "
        "instead of keeping a list (C-74)")


# ---------------------------------------------------------------------------
# T024 / C-75 — a non-family command may still read; the family is not a read gate
# ---------------------------------------------------------------------------
def test_a_non_family_command_may_still_read_but_not_create(sandbox):
    _seed_bound_goal(sandbox)
    before = _tree_digest(sandbox)

    side = _family("nonexistentcommand")
    assert side.returncode == 0, (
        f"the family verdict must resolve: {side.stdout!r} {side.stderr!r}")
    assert json.loads(side.stdout)["in_family"] is False

    read = _run_engine(sandbox, "binding", "goal", "alpha")
    assert read.returncode == 0, (
        "a command outside the family MUST still read a definition it was handed "
        f"(C-75): {read.stdout!r} {read.stderr!r}")
    payload = json.loads(read.stdout)
    assert payload["owner"] == "command-run"
    assert payload["owner_id"] == RUN_ID
    assert payload["origin"] is None
    assert _tree_digest(sandbox) == before, (
        "the family verdict is a read; it writes nothing")

    # The read path carries no family lookup: the family decides creation and ownership,
    # never readability — a gate inside the read would violate C-75.
    engine_text = ENGINE.read_text(encoding="utf-8")
    read_body = engine_text.split("def read_binding(", 1)[1].split("\ndef ", 1)[0]
    payload_body = engine_text.split("def binding_payload(", 1)[1].split("\ndef ", 1)[0]
    for body, name in ((read_body, "read_binding"), (payload_body, "binding_payload")):
        assert "command-family" not in body and "command_family" not in body, (
            f"{name} must not consult the family predicate (C-75)")

    # And the creation side is gated at the declared consumption points: create-team
    # must cite the family action (asserted in T023) while no read path does.
