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

import importlib.util
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

# --------------------------------------------------------------------------- #
# US5 — transmission chain reuse, single owner, red lines, behaviour surfaces
# (T047 red-first; green claims at T052)
# --------------------------------------------------------------------------- #

BATCH_SECTION_TOKENS = (
    ("待决策项来源清单", "Pending Source Roster"),
    ("待决策项块", "Pending Item Block"),
    ("批次状态", "Batch States"),
    ("批次呈现契约", "Batch Presentation Contract"),
    ("建议默认值与依据", "Recommended Default"),
    ("决策批次与应答", "Decision Batch"),
    ("批次处置与沉默接受默认", "Batch Disposition"),
    ("批次记录契约", "Batch Record Contract"),
    ("批次登记与来源更新", "Register Reflection"),
    ("重放契约", "Replay Contract"),
    ("完备性与拒绝", "Completeness & Refusal"),
    ("重决与取代", "Redecision"),
)


def test_transmission_reuses_107_chain(tmp_path: Path) -> None:
    """C-509: a batch decision reuses the 107 record → dispatch attempt → implementation
    receipt chain; the batch generates no second record and no second transmission path."""
    owner_text = OWNER.read_text(encoding="utf-8")
    section = _h2_section(owner_text, "重决与取代", "Redecision")
    flat = " ".join(section.split())
    assert "传递与实施" in section, (
        "§ 重决与取代 does not point at the 107 transmission owner")
    assert "审计链" in flat, "§ 重决与取代 does not name the 107 audit chain"
    assert "第二条" in flat and "MUST NOT" in flat, (
        "§ 重决与取代 does not forbid a second record or a second transmission path")

    # Executable half: the closed action set carries no transmission surface, and every
    # settled decision item yields exactly one record block.
    help_text = run_engine("--help").stdout
    assert "{scan,record,replay}" in help_text, help_text
    root = tmp_path / "batch-family"
    shutil.copytree(FIXTURES / "batch-family", root)
    scan = run_engine("scan", "--workspace-root", str(root), "--format", "json")
    assert scan.returncode == 0, scan.stderr
    presentation = tmp_path / "scan.json"
    presentation.write_text(scan.stdout, encoding="utf-8")
    reply = tmp_path / "reply.md"
    reply.write_text(
        "reply_verbatim: |\n  没有异议，按建议默认值处理。\nno_objections: true\n",
        encoding="utf-8")
    recorded = run_engine("record", "--workspace-root", str(root),
                          "--presentation", str(presentation), "--reply", str(reply),
                          "--authorization", "interactive", "--format", "json")
    assert recorded.returncode == 0, recorded.stdout + recorded.stderr
    payload = json.loads(recorded.stdout)
    text = (root / payload["record_path"]).read_text(encoding="utf-8")
    ids = re.findall(r"(?m)^### (D-\d{3}) — ", text)
    assert ids == [entry["decision_id"] for entry in payload["decisions"]], (ids, payload)
    assert len(ids) == len(set(ids)), "a decision item produced more than one record block"


def test_owner_extension_single_owner() -> None:
    """C-511: every batch face is owned additively by the one owner page and P-13 joins
    the producer inventory; no second owner page, registry, store or schema exists."""
    owner_text = OWNER.read_text(encoding="utf-8")
    for tokens in BATCH_SECTION_TOKENS:
        _h2_section(owner_text, *tokens)
    inventory = [line for line in owner_text.splitlines() if line.startswith("| P-13 |")]
    assert len(inventory) == 1, "the producer inventory carries no single P-13 row"
    assert "仅 `human-interactive`" in inventory[0], inventory[0]
    assert "批量决策面" in owner_text, (
        "the Ownership Declaration does not name the batch faces")

    # No second owner page: no other definitions page declares a batch face section.
    for path in sorted((ROOT / "shared" / "definitions").glob("*.md")):
        if path == OWNER:
            continue
        body = path.read_text(encoding="utf-8")
        for tokens in (("待决策项来源清单",), ("批次呈现契约",), ("批次记录契约",)):
            assert f"## {tokens[0]}" not in body, (
                f"a second owner page declares the batch faces: {path}")

    # Consumers reach the owner by pointer, never by a second copy of the criteria.
    for consumer in (ROOT / "templates/commands/decide.md", SKILL):
        body = consumer.read_text(encoding="utf-8")
        assert "shared/definitions/decision-definitions.md" in body, consumer

    # One schema: the batch-family field closure lives in the one checker.
    spec = importlib.util.spec_from_file_location("validate_decisions_closed", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert tuple(module.BATCH_FAMILY_FIELDS) == (
        "batch_id", "batch_disposition", "recommendation_grounding"), module.BATCH_FAMILY_FIELDS
    assert set(module.BATCH_FAMILY_FIELDS) <= set(module.ADMITTED_FIELD_LINES)

    # One store: the batch record is written through the memory engine into the existing
    # knowledge store, and the engine declares exactly one closed action tuple.
    engine = ENGINE.read_text(encoding="utf-8")
    assert "memory-utils.py" in engine and '"knowledge"' in engine, (
        "the engine no longer writes through the memory engine's knowledge scope")
    assert ".specify/knowledge/" in engine
    assert engine.count("ACTIONS = (") == 1


def test_red_lines_and_boundary(tmp_path: Path) -> None:
    """C-512: no ai-harness alignment, no network, no feedback-store write, no automatic
    transmission and no ai-autonomous presentation."""
    engine = ENGINE.read_text(encoding="utf-8")
    for banned in ("import socket", "import urllib", "http.client", "smtplib",
                   "feedback-utils", "ai-harness"):
        assert banned not in engine, f"the engine carries a forbidden surface: {banned}"
    skill = SKILL.read_text(encoding="utf-8")
    for token in ("no network", "no feedback-store write", "no automatic transmission"):
        assert token in skill, f"the skill lost its red-line statement {token!r}"
    section = _h2_section(OWNER.read_text(encoding="utf-8"), "重决与取代", "Redecision")
    flat = " ".join(section.split())
    for token in ("ai-harness", "091", "零网络", "自动传输"):
        assert token in flat, f"§ 重决与取代 lacks the boundary fact {token!r}"

    # Executable: an autonomous-only tree presents zero items and names the exclusion.
    root = tmp_path / "autonomous"
    shutil.copytree(FIXTURES / "autonomous", root)
    proc = run_engine("scan", "--workspace-root", str(root), "--format", "json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["bookkeeping"]["presented_rows"] == 0, payload["bookkeeping"]
    assert payload["items"] == [], "an ai-autonomous item was presented"
    assert any(entry["reason"] == "not-human-held"
               for entry in payload["bookkeeping"]["named_exclusions"]), payload["bookkeeping"]


def test_behavior_surfaces_named() -> None:
    """C-208: readability, consequence truthfulness and basis sufficiency stay on the
    named review surfaces (B-03 / B-08 / B-09), never claimed as machine coverage."""
    owner_text = OWNER.read_text(encoding="utf-8")
    presentation = _h2_section(owner_text, "批次呈现契约", "Batch Presentation Contract")
    flat = " ".join(presentation.split())
    for rule in ("B-03", "B-08", "B-09"):
        assert rule in flat, f"§ 批次呈现契约 does not name {rule}"
    assert "MUST NOT 被任何文档或测试声称机器覆盖" in flat, (
        "§ 批次呈现契约 does not disclaim machine coverage")
    enforcement = _h2_section(owner_text, "强制边界", "Enforcement Boundary")
    rows: dict[str, str] = {}
    for line in enforcement.splitlines():
        match = re.match(r"^\| (B-\d{2})[^|]*\|", line)
        if match:
            rows[match.group(1)] = line
    for rule in ("B-03", "B-08", "B-09"):
        assert rule in rows, f"§ 强制边界 carries no {rule} row"
        assert "不声称机器覆盖" in rows[rule], rows[rule]
        assert ("/speckit.review" in rows[rule] or "/speckit.analyze" in rows[rule]
                or "人工决策评审" in rows[rule]), rows[rule]

# --------------------------------------------------------------------------- #
# Polish — distribution closure: fresh `specify init` receives the capability
# (T055)
# --------------------------------------------------------------------------- #

PER_TOOL_COPIES = (
    ".claude/commands/speckit.decide.md",
    ".github/prompts/speckit.decide.prompt.md",
    ".qoder/commands/speckit.decide.md",
    ".opencode/command/speckit.decide.md",
)


def _run_init(project: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src") + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return subprocess.run(
        [sys.executable, "-c", "from specify_cli import main; main()",
         "init", "--here", "--ai", "qoder", "--script", "sh", "--no-git"],
        cwd=str(project), env=env, capture_output=True, text=True,
        timeout=300, check=False,
    )


def test_distribution_init_contains_decide(tmp_path: Path) -> None:
    """T055: a throwaway fresh `specify init` workspace receives `/speckit.decide`, the
    `decide-batch` skill and the engine; each of the four per-tool copies carries the edit."""
    project = tmp_path / "fresh"
    project.mkdir()
    proc = _run_init(project)
    assert proc.returncode == 0, (
        f"specify init failed (rc={proc.returncode})\n"
        f"stdout:\n{proc.stdout[-3000:]}\nstderr:\n{proc.stderr[-3000:]}")

    command = project / ".qoder" / "commands" / "speckit.decide.md"
    assert command.is_file(), "a fresh init did not receive the decide command copy"
    command_text = command.read_text(encoding="utf-8")
    for token in ("decision-batch.py", "decide-batch", "scan", "record", "replay"):
        assert token in command_text, f"the init command copy lacks {token!r}"

    skill = project / ".specify" / "skills" / "internal" / "decide-batch" / "SKILL.md"
    assert skill.is_file(), "a fresh init did not receive the decide-batch skill"
    assert "decision-batch.py" in skill.read_text(encoding="utf-8")

    engine = project / ".specify" / "scripts" / "python" / "decision-batch.py"
    assert engine.is_file(), "a fresh init did not receive the engine"
    version = subprocess.run(
        [sys.executable, str(engine), "--version"],
        capture_output=True, text=True, timeout=60, check=False,
    )
    assert version.returncode == 0, version.stderr
    assert re.match(r"^decision-batch\.py \S+$", version.stdout.strip()), version.stdout

    for rel in PER_TOOL_COPIES:
        copy = ROOT / rel
        assert copy.is_file(), f"the per-tool command copy {rel} is missing"
        body = copy.read_text(encoding="utf-8")
        for token in ("decision-batch.py", "decide-batch"):
            assert token in body, f"{rel} does not contain the edit ({token!r})"
