"""Unit tests for the decision-governance checker ``scripts/python/validate-decisions.py``.

Feature 107. This module owns the checker's own interface surface and, in later packages,
the record-judging unit tests (M-01 / M-03 / M-04 reverse samples, the C-107 replay test).
Landed by package P1: ``test_cli_surface`` only.

``test_cli_surface`` (T006, red-first; green at T007) pins ``contracts/enforcement-boundary``
C-404 together with ``shared/definitions/script-interface-definitions.md``:

* ``-h`` and ``--help`` answer the same body;
* ``--version`` prints one line ``<script-name> <framework-version>``;
* an undeclared option exits non-zero, and the declared action set is exactly
  ``records|payload|chain|inventory`` (a fifth value is an argument error);
* exit codes are 0 = pass / 1 = a documented check failed / 2 = input or argument error,
  as stated in the help body's ``exit-codes:`` label;
* a run creates no file inside the repository (before/after snapshot over the trees a
  checker could plausibly touch, with bytecode writing disabled for the subprocess).

The test drives the engine as a real process (``subprocess``) so the version line and the
undeclared-option refusal are observed exactly as a shell caller observes them.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "validate-decisions.py"

#: The closed declared action set (T007). Order is part of the help rendering.
ACTIONS = ("records", "payload", "chain", "inventory")

#: Trees a read-only run could plausibly touch (its own source, its mirror, the spec dir
#: passed as ``--spec``, the fixture dir passed as ``--fixture``).
SNAPSHOT_TREES = (
    "scripts/python",
    ".specify/scripts/python",
    ".specify/specs/107-decision-governance",
    "tests/fixtures/decision-governance",
)

VERSION_LINE_RE = re.compile(r"^validate-decisions\.py \S+$")


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
        for path in sorted(base.rglob("*")):
            if "__pycache__" in path.parts:
                continue
            if path.is_file():
                stat = path.stat()
                entries.append((str(path.relative_to(ROOT)), stat.st_size, stat.st_mtime_ns))
    return entries


def test_cli_surface() -> None:
    assert ENGINE.is_file(), f"missing checker: {ENGINE}"

    # --help / -h: one body, exit 0.
    short = run_engine("-h")
    long = run_engine("--help")
    assert short.returncode == 0, f"-h exited {short.returncode}: {short.stderr}"
    assert long.returncode == 0, f"--help exited {long.returncode}: {long.stderr}"
    assert short.stdout == long.stdout, "-h and --help answer different bodies"
    help_text = short.stdout

    # The declared action set is exactly the four, rendered by argparse's choices.
    assert "{%s}" % ",".join(ACTIONS) in help_text, (
        "help does not render the closed action set {records,payload,chain,inventory}"
    )
    assert "--action" in help_text and "--carrier" in help_text and "--json" in help_text

    # The four mandatory help labels: usage/options come from argparse; the two labelled
    # lines are ours (owner: shared/definitions/script-interface-definitions.md § 2).
    assert "side-effects:" in help_text, "help body lacks the side-effects label"
    exit_lines = [ln for ln in help_text.splitlines() if ln.strip().startswith("exit-codes:")]
    assert exit_lines, "help body lacks the exit-codes label"
    exit_line = exit_lines[0]
    # C-404: 0 = pass / 1 = documented check failed / 2 = input or argument error.
    for code in ("0", "1", "2"):
        assert code in exit_line, f"exit-codes label does not state the {code} meaning: {exit_line!r}"

    # --version: one line, <script-name> <framework-version>, exit 0.
    version = run_engine("--version")
    assert version.returncode == 0, f"--version exited {version.returncode}: {version.stderr}"
    vlines = [ln for ln in version.stdout.splitlines() if ln.strip()]
    assert len(vlines) == 1, f"--version printed {len(vlines)} line(s): {vlines}"
    assert VERSION_LINE_RE.match(vlines[0]), f"malformed version line: {vlines[0]!r}"

    # An undeclared option is refused non-zero, with a diagnostic.
    bogus = run_engine("--bogus")
    assert bogus.returncode != 0, "an undeclared option exited 0"
    assert "unrecognized option" in bogus.stderr, bogus.stderr

    # A fifth action value is an argument error (argparse's invalid-choice exit 2).
    bad_action = run_engine("--action", "bogus")
    assert bad_action.returncode == 2, (
        f"--action bogus exited {bad_action.returncode}, expected 2: {bad_action.stderr}"
    )
    assert "invalid choice" in bad_action.stderr, bad_action.stderr

    # Read-only: a run creates no file inside the repository.
    before = snapshot()
    run_engine("--action", "inventory",
               "--spec", ".specify/specs/107-decision-governance",
               "--fixture", "tests/fixtures/decision-governance", "--json")
    run_engine("--action", "records", "--spec", ".specify/specs/107-decision-governance")
    after = snapshot()
    assert before == after, (
        "a run changed the repository tree: "
        f"created={sorted(set(after) - set(before))[:3]} removed={sorted(set(before) - set(after))[:3]}"
    )


# --------------------------------------------------------------------------- #
# US2 — option-set closure and AI replay (T018)
# --------------------------------------------------------------------------- #

M03 = ROOT / "tests" / "fixtures" / "decision-governance" / "m03"

CHOSEN_RE = re.compile(r"(?m)^- \*\*chosen_option\*\*:\s*(.*)$")
LABEL_RE = re.compile(r"(?m)^\s{2,}-\s+label:\s*(.+)$")
PREDICATE_RE = re.compile(r"(?m)^\s{2,}predicate:\s*(min|max)\(([A-Za-z0-9_]+)\)\s*$")
INPUTS_RE = re.compile(r"(?m)^\s{2,}inputs:\s*(.+)$")


def run_records(*args: str) -> subprocess.CompletedProcess:
    return run_engine("--action", "records", *args)


def replay_choice(record_text: str) -> str:
    """Re-derive the chosen option from the record's own predicate and recorded inputs.

    The replay fixture records, as ``rationale`` continuation lines, one closed predicate
    form — ``min(<dimension>)`` / ``max(<dimension>)`` — plus a per-option input line. The
    first declared option wins ties, so the replay is deterministic for one record text.
    """
    labels = [label.strip() for label in LABEL_RE.findall(record_text)]
    predicate = PREDICATE_RE.search(record_text)
    inputs = INPUTS_RE.search(record_text)
    assert predicate and inputs, "the fixture does not record a decision predicate and its inputs"
    direction, _dimension = predicate.group(1), predicate.group(2)
    values: dict[str, float] = {}
    for part in inputs.group(1).split(";"):
        key, _, raw = part.partition("=")
        if key.strip():
            values[key.strip()] = float(raw)
    ordered = [label for label in labels if label in values]
    assert ordered and len(ordered) == len(labels), (
        f"recorded inputs cover {sorted(values)}, not every option label {labels}"
    )
    pick = min if direction == "min" else max
    return pick(ordered, key=lambda label: values[label])


def test_m03_option_set_reverse_samples() -> None:
    """C-106 / M-03: each degenerate option-set form turns red; a completed set is green."""
    red_samples = {
        "red-empty-set.md": "empty option set",
        "red-duplicate-label.md": "duplicate option label",
        "red-other-without-path.md": "other",
        "red-missing-reversibility.md": "missing option element",
        "red-missing-evidence.md": "missing option element",
        "red-single-without-forced.md": "forced",
        "red-count-mismatch.md": "declared count",
    }
    before = snapshot()
    for name, needle in red_samples.items():
        path = M03 / name
        assert path.is_file(), f"missing fixture: {path}"
        red = run_records("--carrier", str(path))
        assert red.returncode == 1, (
            f"{name} exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
        )
        assert "M-03" in red.stdout, f"{name} carries no M-03 verdict: {red.stdout!r}"
        payload = json.loads(run_records("--carrier", str(path), "--json").stdout)
        verdict = next(v for v in payload["violations"] if v["rule"] == "M-03")
        assert verdict["path"].endswith(name), verdict
        assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
        assert needle in verdict["message"], (
            f"{name}: message {verdict['message']!r} lacks {needle!r}"
        )

    for name in ("green-complete.md", "green-single-forced.md"):
        ok = run_records("--carrier", str(M03 / name))
        assert ok.returncode == 0, (
            f"{name} exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
        )
        assert not re.search(r"(?m)^M-03 ", ok.stdout), (
            f"{name} still carries an M-03 verdict: {ok.stdout!r}"
        )
    assert snapshot() == before, "a run mutated the repository tree"


def test_ai_replay_deterministic() -> None:
    """C-107: the recorded inputs + predicate re-derive the chosen option; mismatches show."""
    green = M03 / "ai-replay-green.md"
    mismatch = M03 / "ai-replay-mismatch.md"
    for path in (green, mismatch, M03 / "red-chosen-not-member.md"):
        assert path.is_file(), f"missing fixture: {path}"

    text = green.read_text(encoding="utf-8")
    first = replay_choice(text)
    second = replay_choice(text)
    assert first == second == "plan-a", (
        f"replay is not deterministic on the same record text: {first!r} then {second!r}"
    )
    recorded = CHOSEN_RE.search(text).group(1).strip()
    assert first == recorded, (
        f"replay re-derived {first!r} but the record chose {recorded!r}"
    )

    mismatch_text = mismatch.read_text(encoding="utf-8")
    recorded_bad = CHOSEN_RE.search(mismatch_text).group(1).strip()
    assert replay_choice(mismatch_text) != recorded_bad, (
        "a doctored record replays to its recorded choice; the mismatch would be undetectable"
    )

    # The chosen option is a named member of the closed set (M-03 membership leg).
    not_member = run_records("--carrier", str(M03 / "red-chosen-not-member.md"))
    assert not_member.returncode == 1, (
        f"a chosen option outside the set exited {not_member.returncode}, expected 1: "
        f"{not_member.stdout} {not_member.stderr}"
    )
    assert "M-03" in not_member.stdout, (
        f"the membership verdict does not carry M-03: {not_member.stdout!r}"
    )
    ok = run_records("--carrier", str(green))
    assert ok.returncode == 0, (
        f"the replayable record exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
