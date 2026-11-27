"""Contract tests for Feature 112 — Batch Decision Panel delivery surfaces.

This module pins the surfaces the batch capability MUST expose to callers: the engine
interface (C-608), the owner-page block grammar (C-103), the identifier boundary of the
user-facing body (C-204), the skill's non-recompute boundary (C-307) and, in later
packages, the transmission / single-owner / red-line guards (C-509, C-511, C-512, C-208).

Package P1 lands ``test_engine_interface_contract`` red-first; the remaining tests are
appended by the user-story packages without touching the P1 assertions.

The engine tests drive ``scripts/python/decision-batch.py`` as a real process so exit
codes, help bodies and the version line are observed exactly as a shell caller observes
them (the same shape as ``tests/unit/test_validate_decisions.py::test_cli_surface``).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "decision-batch.py"
OWNER = ROOT / "shared" / "definitions" / "decision-definitions.md"
SKILL = ROOT / "skills" / "internal" / "decide-batch" / "SKILL.md"
CHECKER = ROOT / "scripts" / "python" / "validate-decisions.py"
FIXTURES = ROOT / "tests" / "fixtures" / "decision-batch"

#: The closed declared action set (C-608). Order is part of the help rendering.
ACTIONS = ("scan", "record", "replay")

#: Trees a read-only invocation could plausibly touch: the engine sources and mirror, the
#: knowledge store (the record write target) and this feature's spec directory.
SNAPSHOT_TREES = (
    "scripts/python",
    ".specify/scripts/python",
    ".specify/knowledge",
    ".specify/specs/112-decision-batch-panel",
)

#: The version line shape: ``decision-batch.py <framework-version>``.
VERSION_LINE_RE = re.compile(r"^decision-batch\.py \S+$")


def run_engine(*args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )


def snapshot() -> list[tuple[str, int, int]]:
    """(path, size, mtime_ns) over the snapshot trees; interpreter caches excluded."""
    entries = []
    for rel in SNAPSHOT_TREES:
        base = ROOT / rel
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if "__pycache__" in path.parts:
                continue
            if path.is_file():
                stat = path.stat()
                entries.append((str(path.relative_to(ROOT)), stat.st_size, stat.st_mtime_ns))
    return entries


# --------------------------------------------------------------------------- #
# P1 — engine interface (C-608, T005 red-first; green at T006)
# --------------------------------------------------------------------------- #

def test_engine_interface_contract() -> None:
    """C-608: closed actions, help/version on every action, exit codes, read-only scan/replay."""
    assert ENGINE.is_file(), f"missing engine: {ENGINE.relative_to(ROOT)}"

    # -h / --help: one body, exit 0, the closed action set and the four help labels.
    short = run_engine("-h")
    long = run_engine("--help")
    assert short.returncode == 0, f"-h exited {short.returncode}: {short.stderr}"
    assert long.returncode == 0, f"--help exited {long.returncode}: {long.stderr}"
    assert short.stdout == long.stdout, "-h and --help answer different bodies"
    help_text = short.stdout
    assert "{%s}" % ",".join(ACTIONS) in help_text, (
        "help does not render the closed action set {scan,record,replay}"
    )
    for flag in ("--workspace-root", "--format", "--presentation", "--reply",
                 "--authorization", "--batch"):
        assert flag in help_text or any(
            flag in run_engine(action, "--help").stdout for action in ACTIONS
        ), f"no help body declares the required flag {flag}"
    for label in ("usage", "options", "side-effects:", "exit-codes:"):
        assert label in help_text, f"help body lacks the {label!r} label"
    exit_lines = [ln for ln in help_text.splitlines() if ln.strip().startswith("exit-codes:")]
    assert exit_lines, "help body lacks the exit-codes label line"
    exit_line = exit_lines[0]
    for code in ("0", "1", "2"):
        assert code in exit_line, (
            f"exit-codes label does not state the {code} meaning: {exit_line!r}"
        )

    # --version: one line on the entry and on every closed action.
    for prefix in ((),) + tuple((action,) for action in ACTIONS):
        completed = run_engine(*prefix, "--version")
        assert completed.returncode == 0, (
            f"{' '.join(prefix) or 'entry'} --version exited {completed.returncode}: "
            f"{completed.stderr}"
        )
        lines = [ln for ln in completed.stdout.splitlines() if ln.strip()]
        assert len(lines) == 1, (
            f"{' '.join(prefix) or 'entry'} --version printed {len(lines)} line(s): {lines}"
        )
        assert VERSION_LINE_RE.match(lines[0]), f"malformed version line: {lines[0]!r}"

    # An undeclared option is refused non-zero at the entry and on an action.
    for prefix in ((), ("scan",)):
        bogus = run_engine(*prefix, "--bogus")
        assert bogus.returncode != 0, f"{prefix or 'entry'} accepted --bogus"
        assert "unrecognized" in bogus.stderr.lower(), (
            f"{prefix or 'entry'} --bogus carries no diagnostic: {bogus.stderr!r}"
        )

    # scan and replay are read-only: a run creates and changes nothing in the repository.
    before = snapshot()
    scan = run_engine("scan", "--workspace-root", ".", "--format", "text")
    replay = run_engine(
        "replay", "--workspace-root", ".",
        "--batch", ".specify/knowledge/decision-batch-absent.md",
    )
    after = snapshot()
    assert scan.returncode in (0, 1, 2), f"scan exited {scan.returncode}: {scan.stderr}"
    assert replay.returncode in (0, 1, 2), f"replay exited {replay.returncode}: {replay.stderr}"
    assert before == after, (
        "a scan/replay invocation changed the repository tree: "
        f"created={sorted(set(after) - set(before))[:3]} "
        f"removed={sorted(set(before) - set(after))[:3]}"
    )

# --------------------------------------------------------------------------- #
# US1 — owner-page block grammar, identifier boundary, non-recompute skill
# (T014 red-first; green claims at T023)
# --------------------------------------------------------------------------- #

def _h2_section(text: str, *tokens: str) -> str:
    """Body of the first H2 heading carrying every token, up to the next H2 or EOF."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and all(token in line for token in tokens):
            start = index
            break
    assert start is not None, f"missing H2 section carrying {tokens!r} in the owner page"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start + 1:end])


BLOCK_FIELDS = (
    "decision_class", "subject", "same_name_conflict", "resource_locator", "context",
    "options", "basis", "origin", "created_at", "resolution",
)


def test_block_grammar_owner_extension() -> None:
    """C-103: the pending-item block grammar is owned by the extended owner page and is
    never judged as a decision record (and a record is never judged as a pending block)."""
    assert OWNER.is_file(), f"missing owner page: {OWNER.relative_to(ROOT)}"
    section = _h2_section(OWNER.read_text(encoding="utf-8"), "待决策项块", "Pending Item Block")
    flat = " ".join(section.split())
    assert "### PENDING —" in section, "the block grammar heading is not stated"
    for field in BLOCK_FIELDS:
        assert f"`{field}`" in section, f"the closed field set does not name `{field}`"
    assert "不是决策记录" in flat, (
        "the section does not state that a pending block is not a decision record"
    )
    assert "MUST NOT" in flat and "判" in flat, (
        "the section does not state the mutual non-judgement rule"
    )

    # Executable half: the 107 record grammar exits 0 over a carrier holding only
    # pending blocks and reports no record-grammar verdict for them.
    carrier = FIXTURES / "incomplete-block" / ".specify" / "specs" / "demo" / "defects.md"
    assert carrier.is_file(), f"missing fixture: {carrier}"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--action", "records", "--carrier", str(carrier)],
        capture_output=True, text=True, env=env, cwd=str(ROOT),
    )
    assert proc.returncode == 0, (
        f"the record grammar judged a pending block: rc={proc.returncode} "
        f"{proc.stdout[-600:]} {proc.stderr[-600:]}"
    )
    assert not re.search(r"(?m)^M-0[0-9] ", proc.stdout), (
        f"a record-grammar verdict fired on a pending block: {proc.stdout[-600:]}"
    )


#: Internal identifiers that MUST NOT leak into the user-facing text body (C-204):
#: field names, script names, status/reason tokens.
INTERNAL_TOKENS = (
    "decision_class", "recommended_default", "recommendation_grounding", "batch_disposition",
    "qualification", "resource_locator", "same_name_conflict", "objection_instructions",
    "decision-batch.py", "validate-decisions.py",
    "incomplete", "source-conflict", "no-default", "irreversible-default",
    "prior-decision-conflict", "eligible", "grounded", "no-evidence",
    "accepted-default", "objected-alternative", "objected-parked", "not-human-held",
    "already-resolved", "duplicate-merged",
    "class-missing", "authority-unresolved", "ambiguous-link", "missing-field",
    "option-count-mismatch", "unknown-field", "duplicate-field", "malformed-field",
)


def test_presentation_identifier_boundary(tmp_path: Path) -> None:
    """C-204: the user-facing text body carries no internal identifiers; the structured
    payload is allowed to carry them."""
    root = tmp_path / "two-source"
    shutil.copytree(FIXTURES / "two-source", root)
    proc = run_engine("scan", "--workspace-root", str(root), "--format", "text")
    assert proc.returncode == 0, f"scan --format text exited {proc.returncode}: {proc.stderr}"
    body = proc.stdout
    leaked = sorted(token for token in INTERNAL_TOKENS if token in body)
    assert not leaked, f"internal identifiers leaked into the user-facing body: {leaked}"

    machine = run_engine("scan", "--workspace-root", str(root), "--format", "json")
    assert machine.returncode == 0, machine.stderr
    payload = json.loads(machine.stdout)
    assert any("decision_class" in json.dumps(item) for item in payload["items"]), (
        "the structured payload lost its internal identifiers (it is the machine channel)"
    )


def test_skill_does_not_recompute() -> None:
    """C-307: the skill delegates the join / pointer / conflict judgements to the engine
    and performs no semantic retrieval or status override."""
    assert SKILL.is_file(), f"missing skill: {SKILL.relative_to(ROOT)}"
    text = SKILL.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "scripts/python/decision-batch.py" in text, "the skill does not name the engine"
    assert "shared/definitions/decision-definitions.md" in text, (
        "the skill does not reach the owner page by pointer"
    )
    assert "Never recompute a judged verdict" in flat, (
        "the skill does not state the non-recompute boundary"
    )
    assert "no semantic retrieval" in flat, (
        "the skill does not forbid semantic retrieval at presentation time"
    )
    assert "never overrides an engine-judged status" in flat, (
        "the skill does not forbid overriding a judged status"
    )
    for action in ("scan", "record", "replay"):
        assert action in text, f"the skill does not name the engine action {action!r}"
    # The skill reaches the exit-code surface by pointer rather than restating codes.
    assert "docs/reference/commands/decide.md" in text, (
        "the skill does not point at the command reference for the exit semantics"
    )

# --------------------------------------------------------------------------- #
# US2 — signal mapping by pointer (C-408, T025 red-first; green at T032)
# --------------------------------------------------------------------------- #

def test_signal_mapping_pointer_only() -> None:
    """C-408: the disposition→choice-signal mapping reaches the gates owner by pointer;
    the signal value domain is not restated and a park emits no signal."""
    assert OWNER.is_file()
    section = _h2_section(OWNER.read_text(encoding="utf-8"), "批次处置", "Batch Disposition")
    flat = " ".join(section.split())
    assert "shared/guidelines/confirmation-gates.md" in section, (
        "the disposition section does not reach the gates owner by pointer"
    )
    assert "accepted-default" in flat and "approved-as-is" in flat, (
        "the accepted-default signal mapping is not stated"
    )
    assert "objected-alternative" in flat and "modified" in flat, (
        "the objected-alternative signal mapping is not stated"
    )
    assert "objected-parked" in flat and "不产生选择信号" in flat, (
        "the parked disposition does not state that it emits no choice signal"
    )
    # The gates value domain stays with its owner: the section must not restate it.
    for token in ("asked-questions", "denied"):
        assert token not in flat, f"the gates value domain token {token!r} is restated here"
    # The engine computes dispositions only; it carries no second signal vocabulary.
    engine = ENGINE.read_text(encoding="utf-8")
    for token in ("approved-as-is", "asked-questions", "denied"):
        assert token not in engine, f"the engine defines a signal token {token!r}"
