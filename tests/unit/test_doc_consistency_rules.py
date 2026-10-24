"""Unit tests for the doc-consistency rules (069a, T014).

Owns the rule mechanics of
``.specify/specs/069a-flow-classification-docs-gates/contracts/doc-consistency-checker.md``
that a whole-repository contract test cannot isolate:

* C-2  the closed exclusion list — path level (``notes/``, ``review.md``,
       ``verification.md``) and line level (fenced code, table separators, pure
       link lines, short lines, pure date/version lines) never produce a finding;
* C-3  the as-of form and the ``not-evaluated`` degradation outside git;
* C-5  normalisation (list prefix / whitespace / trailing punctuation / ASCII
       case), the two duplicate thresholds (exact >= 24 chars; ratio >= 0.90 and
       >= 40 chars), same-file repetition not reported, and the fix direction;
* C-6  count delegation degradation is an explicit ``not-run`` **with a reason**;
* C-1  ``--faces`` really narrows the run, ``--format text`` is actionable, and
       ``--json-out`` writes exactly one file and nothing else.

The engine is a script (no import contract), so these unit tests drive it through
its CLI on small fixtures — behaviour, not internals. Red-first
(Constitution IV): the engine does not exist yet, so ``_run`` asserts the path
first.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "python" / "doc-consistency-check.py"
CHECKER_REL = "scripts/python/doc-consistency-check.py"

def _header(tag: str) -> str:
    """A reader declaration unique to *tag* (identical declarations would collide)."""
    return (
        "# Fixture %s\n\n**Readers**: 评审者\n"
        "**Reading scenario**: 合并前核对 %s 的相关事实。\n\n" % (tag, tag)
    )

LONG_A = "The framework keeps exactly one authoritative definition point per fact."
LONG_B = "The framework keeps only one authoritative definition point per fact."
UNRELATED = "Deployment topology and runtime capacity are reviewed elsewhere entirely."
NEAR_SHORT_A = "abcdefghij0123456789klmnopqrst"
NEAR_SHORT_B = "abcdefghij0123456789klmnopqrstu"
REAL_COPY = "这条断言在框架里只允许有一个所有者，其他位置一律改为引用它。"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    assert CHECKER.is_file(), (
        "doc-consistency checker missing: %s — expected at T020/T021 (069a). "
        "Red is the intended pre-implementation state for T014." % CHECKER_REL
    )
    return subprocess.run(
        [sys.executable, str(CHECKER), *args],
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), "expected JSON on stdout (stderr: %r)" % proc.stderr
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "stdout is not JSON (%s); head=%r" % (exc, proc.stdout[:400])
        ) from exc


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _verify(*args: str, cwd: Path | None = None) -> tuple[subprocess.CompletedProcess, dict]:
    proc = _run("--action", "verify", "--format", "json", *args, cwd=cwd)
    return proc, (_json(proc) if proc.stdout.strip() else {})


def _rules(doc: dict) -> list[str]:
    return [finding.get("rule", "") for finding in doc.get("findings", [])]


def _duplicates(doc: dict) -> list[dict]:
    return [f for f in doc.get("findings", []) if f.get("rule") == "duplicate-fact"]


def _pair(tmp_path: Path, left: str, right: str) -> tuple[Path, Path]:
    return (
        _write(tmp_path / "a.md", _header("a") + left + "\n"),
        _write(tmp_path / "b.md", _header("b") + right + "\n"),
    )


# --------------------------------------------------------------------------- #
# C-5 — normalisation and thresholds
# --------------------------------------------------------------------------- #
def test_normalisation_ignores_prefix_whitespace_case_and_trailing_punctuation(tmp_path):
    left = "- The framework keeps exactly one authoritative definition point per fact."
    right = "  the framework keeps exactly one authoritative   definition point per fact"
    a, b = _pair(tmp_path, left, right)
    proc, payload = _verify("--path", str(a), "--path", str(b), "--faces", "duplicate")
    assert proc.returncode == 1, "normalised-equal lines must be reported as a duplicate"
    assert _duplicates(payload), "expected duplicate-fact after normalisation, got %r" % _rules(payload)


def test_short_identical_lines_are_not_duplicates(tmp_path):
    short = "同一条很短的断言"
    a, b = _pair(tmp_path, short, short)
    proc, payload = _verify("--path", str(a), "--path", str(b), "--faces", "duplicate")
    assert proc.returncode == 0, "a line shorter than 24 chars must not be a duplicate finding"
    assert _duplicates(payload) == []


def test_fuzzy_ratio_threshold_needs_40_chars(tmp_path):
    # One-character difference on a 30-char line: ratio is high, but length < 40.
    a, b = _pair(tmp_path, NEAR_SHORT_A, NEAR_SHORT_B)
    proc, payload = _verify("--path", str(a), "--path", str(b), "--faces", "duplicate")
    assert proc.returncode == 0, (
        "a near copy shorter than 40 chars is below the detection floor (not a finding)"
    )
    assert _duplicates(payload) == []


def test_fuzzy_ratio_threshold_reports_near_copies(tmp_path):
    a, b = _pair(tmp_path, LONG_A, LONG_B)
    proc, payload = _verify("--path", str(a), "--path", str(b), "--faces", "duplicate")
    assert proc.returncode == 1, "a >= 40 char near copy (ratio >= 0.90) must be reported"
    findings = _duplicates(payload)
    assert findings, "expected duplicate-fact for the near copy"
    assert findings[0].get("counterpart"), "the near copy must locate its counterpart"
    assert findings[0].get("fix_direction"), "the finding must carry the fix direction"
    assert "引用" in findings[0]["fix_direction"], (
        "the fix direction must be 'turn it into a reference', got %r"
        % findings[0]["fix_direction"]
    )


def test_unrelated_long_lines_are_not_duplicates(tmp_path):
    a, b = _pair(tmp_path, LONG_A, UNRELATED)
    proc, payload = _verify("--path", str(a), "--path", str(b), "--faces", "duplicate")
    assert proc.returncode == 0, "unrelated sentences must not be reported"
    assert _duplicates(payload) == []


def test_same_file_repetition_is_not_reported(tmp_path):
    doc = _write(tmp_path / "a.md", _header("a") + LONG_A + "\n\n" + LONG_A + "\n")
    proc, payload = _verify("--path", str(doc), "--faces", "duplicate")
    assert proc.returncode == 0, "repetition inside one file is not a cross-file duplicate"
    assert _duplicates(payload) == []


# --------------------------------------------------------------------------- #
# C-2 — line-level exclusions
# --------------------------------------------------------------------------- #
def test_excluded_line_forms_never_produce_findings(tmp_path):
    fenced = "```\n" + LONG_A + "\n```\n"
    separator = "| --- | --- | --- | --- |\n"
    link_line = "https://example.com/a/very/long/path/that/is/longer/than/twenty/four\n"
    version_line = "v1.2.3-20261024-abcdef123456\n"
    body = fenced + separator + link_line + version_line
    a = _write(tmp_path / "a.md", _header("a") + body)
    b = _write(tmp_path / "b.md", _header("b") + body)
    proc, payload = _verify("--path", str(a), "--path", str(b), "--faces", "duplicate")
    assert proc.returncode == 0, (
        "fenced code / table separators / link lines / version lines are excluded; got %r"
        % _rules(payload)
    )
    assert _duplicates(payload) == []
    # Guard against a vacuous pass: one plain duplicated sentence must still be found.
    a = _write(tmp_path / "a.md", _header("a") + body + REAL_COPY + "\n")
    b = _write(tmp_path / "b.md", _header("b") + body + REAL_COPY + "\n")
    proc, payload = _verify("--path", str(a), "--path", str(b), "--faces", "duplicate")
    assert proc.returncode == 1, "the exclusion fixture must still catch a real duplicate"
    assert len(_duplicates(payload)) == 1, (
        "exactly the one real duplicate must be reported, got %r" % _rules(payload)
    )


def test_excluded_paths_are_not_scanned(tmp_path):
    spec = tmp_path / "specs" / "001-fixture"
    _write(
        spec / "requirements.md",
        "# Requirements\n\n" + REAL_COPY + "\n\n- **FR-001**: first.\n",
    )
    doc = _write(
        tmp_path / "doc.md",
        _header("doc") + REAL_COPY + "\n\n"
        + "只在 notes 里重复的断言，也必须被排除在扫描之外。\n\n"
        + "只在 review 里重复的断言，也必须被排除在扫描之外。\n\n"
        + "只在 verification 里重复的断言，也必须被排除在扫描之外。\n",
    )
    _write(spec / "notes" / "x.md", "只在 notes 里重复的断言，也必须被排除在扫描之外。\n")
    _write(spec / "review.md", "只在 review 里重复的断言，也必须被排除在扫描之外。\n")
    _write(spec / "verification.md", "只在 verification 里重复的断言，也必须被排除在扫描之外。\n")
    proc, payload = _verify(
        "--spec-dir", str(spec), "--path", str(doc), "--faces", "duplicate"
    )
    findings = _duplicates(payload)
    assert proc.returncode == 1, "the requirements.md copy must still be reported"
    paths = {str(f.get("path", "")) for f in findings}
    counterparts = {str(f.get("counterpart", "")) for f in findings}
    joined = " ".join(paths | counterparts)
    for excluded in ("notes/", "review.md", "verification.md"):
        assert excluded not in joined, (
            "a dated-record path (%r) produced a duplicate finding: %r" % (excluded, findings)
        )
    assert any("requirements.md" in item for item in paths | counterparts), (
        "the live spec artifact must be one side of the duplicate"
    )


# --------------------------------------------------------------------------- #
# C-3 — as-of form and degradation
# --------------------------------------------------------------------------- #
def test_asof_requires_a_full_iso_date(tmp_path):
    doc = _write(
        tmp_path / "a.md",
        _header("a") + "断言（证据：实测，as-of 2026-1-5，source: `pytest -q` exit 0）。\n",
    )
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert proc.returncode == 1
    assert "as-of-malformed" in _rules(payload), (
        "a non-padded ISO date must be as-of-malformed, got %r" % _rules(payload)
    )


def test_asof_staleness_outside_git_is_not_evaluated_with_reason(tmp_path):
    doc = _write(
        tmp_path / "a.md",
        _header("a") + "断言（证据：实测，as-of 2000-01-01，source: `pytest -q` exit 0）。\n",
    )
    proc, payload = _verify("--path", str(doc), "--faces", "evidence")
    assert proc.returncode == 0
    assert payload["faces"]["evidence"] == "not-evaluated", (
        "outside git the staleness rule is not-evaluated, never pass: %r" % payload["faces"]
    )
    reasons = json.dumps(payload, ensure_ascii=False)
    assert re.search(r"reason", reasons), "the not-evaluated state must carry a reason"


# --------------------------------------------------------------------------- #
# C-1 — face narrowing, text output, json-out
# --------------------------------------------------------------------------- #
def test_faces_selection_narrows_the_run(tmp_path):
    doc = _write(tmp_path / "a.md", "# Doc\n\n没有读者声明。\n\n" + LONG_A + "\n")
    other = _write(tmp_path / "b.md", _header("b") + LONG_A + "\n")
    proc, payload = _verify("--path", str(doc), "--path", str(other), "--faces", "duplicate")
    assert "reader-declaration-missing" not in _rules(payload), (
        "--faces duplicate must not run the reader face"
    )
    proc, payload = _verify("--path", str(doc), "--path", str(other), "--faces", "reader")
    assert "duplicate-fact" not in _rules(payload), (
        "--faces reader must not run the duplicate face"
    )
    assert "reader-declaration-missing" in _rules(payload)


def test_text_format_names_rules_and_locates_lines(tmp_path):
    doc = _write(tmp_path / "a.md", "# Doc\n\n没有读者声明。\n")
    proc = _run("--action", "verify", "--path", str(doc), "--faces", "reader", "--format", "text")
    assert proc.returncode == 1
    assert "reader-declaration-missing" in proc.stdout, (
        "text output must name the rule; got %r" % proc.stdout[:400]
    )
    assert re.search(r"a\.md:\d+", proc.stdout), (
        "text output must locate path:line; got %r" % proc.stdout[:400]
    )


def test_json_out_writes_only_the_named_file(tmp_path):
    doc = _write(tmp_path / "a.md", _header("a") + REAL_COPY + "\n")
    before = hashlib.sha256(doc.read_bytes()).hexdigest()
    out = tmp_path / "report.json"
    proc = _run(
        "--action", "verify", "--format", "json",
        "--path", str(doc), "--faces", "reader", "--json-out", str(out),
    )
    assert proc.returncode == 0, "clean reader run must exit 0 (stderr: %r)" % proc.stderr
    assert out.is_file(), "--json-out must write the report file"
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["action"] == "verify"
    assert hashlib.sha256(doc.read_bytes()).hexdigest() == before, (
        "the checker must be read-only on the checked document"
    )
    assert {p.name for p in tmp_path.iterdir()} == {"a.md", "report.json"}, (
        "no file other than --json-out may be written: %r" % sorted(p.name for p in tmp_path.iterdir())
    )


# --------------------------------------------------------------------------- #
# C-6 — delegation degradation carries a reason
# --------------------------------------------------------------------------- #
def test_count_delegation_degradation_is_explicit(tmp_path):
    spec = tmp_path / "specs" / "001-incomplete"
    _write(spec / "requirements.md", "# Requirements\n\n- **FR-001**: only one.\n")
    proc, payload = _verify("--spec-dir", str(spec), "--faces", "count")
    assert proc.returncode == 0
    assert payload["count_check"]["status"] == "not-run"
    reason = payload["count_check"].get("reason")
    assert reason, "not-run must carry a non-empty reason"
    assert payload["faces"]["count"] != "pass", (
        "an unavailable count face must never be reported as pass: %r" % payload["faces"]
    )
