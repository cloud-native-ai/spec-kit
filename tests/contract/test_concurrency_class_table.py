"""Enumeration-and-class contract (contracts/declaration-facts.contract.md C-014/C-015).

Rows pinned here (WP4): T027; the module carries the ``[green:]`` marker for
``contracts/declaration-facts.contract.md#C-014``.

- **C-014 / T027** — the execution-body universe is derived by enumerating the five roots'
  *patterns* at run time; the class assignment comes from ``concurrency-class.yaml``'s
  decision rule. No hand-written body list exists.
- **V-2 double-direction drift guard** — a body added to a root without a class turns the
  check red (``uncovered``/``ambiguous``, C-024), and a root silently dropped from the
  enumeration still leaves a red *assertion*: the measured root set must be the closed
  five-member set of C-005 with every count ``> 0`` on this tree.

Red-first: the engine ``scripts/python/concurrency-check.py`` lands in WP2; every engine
case below fails with a named "engine missing" assertion until then.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"

FIVE_ROOTS = ("skills", "commands", "agents", "teams", "anchoring")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run_engine(*args, cwd=None):
    assert ENGINE.is_file(), (
        "red-first: scripts/python/concurrency-check.py is the WP2 engine target and is "
        "not in this worktree yet")
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=str(cwd or REPO_ROOT), timeout=180,
    )


def _classify(repo: Path, out: Path):
    proc = _run_engine("classify", "--repo", repo, "--json-out", out)
    envelope = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
    return proc, envelope


def _reader_module():
    spec = importlib.util.spec_from_file_location("declaration_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _roots_statement():
    reader = _reader_module()
    return reader.load_fact(str(REPO_ROOT), "executor-enumeration-roots")["body"]["statement"]


def _expand(pattern: str):
    """Expand the fact's pattern grammar: ``{a,b}`` alternatives, ``<placeholder>`` -> ``*``."""
    variants = [pattern]
    while any("{" in variant for variant in variants):
        expanded = []
        for variant in variants:
            start = variant.index("{")
            end = variant.index("}", start)
            head, tail = variant[:start], variant[end + 1:]
            for option in variant[start + 1:end].split(","):
                expanded.append(head + option + tail)
        variants = expanded
    return [variant.replace("<name>", "*").replace("<stem>", "*").replace("<slug>", "*")
            for variant in variants]


def _members(root: dict):
    members = []
    for pattern in _expand(root["pattern"]):
        if pattern.endswith("/"):
            members.extend(sorted(p for p in REPO_ROOT.glob(pattern) if p.is_dir()))
        else:
            members.extend(sorted(p for p in REPO_ROOT.glob(pattern) if p.is_file()))
    return members


def _expected_counts():
    return {root["root_id"]: len(_members(root)) for root in _roots_statement()["roots"]}


def _collect_counts(node, found=None):
    """Find per-root member counts in whatever shape ``measured`` uses."""
    found = {} if found is None else found
    if isinstance(node, dict):
        for key, value in node.items():
            if key in FIVE_ROOTS and isinstance(value, int):
                found[key] = value
            _collect_counts(value, found)
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, dict):
                root = item.get("root_id") or item.get("root")
                count = item.get("count", item.get("members"))
                if root in FIVE_ROOTS and isinstance(count, int):
                    found[root] = count
            _collect_counts(item, found)
    return found


def _findings_codes(envelope):
    return [finding.get("code") for finding in envelope.get("findings", [])]


def _copy_layer(dst: Path) -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations", dst / "shared" / "declarations")
    return dst


def _drop_block(text: str, marker: str) -> str:
    """Drop one ``    - root_id: <marker>`` sequence item (through the next item or EOF)."""
    lines = text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "- root_id: %s" % marker:
            start = index
            break
    assert start is not None, "fixture premise: root %r must be present" % marker
    end = start + 1
    while end < len(lines) and not lines[end].lstrip().startswith("- root_id:"):
        end += 1
    return "".join(lines[:start] + lines[end:])


# --------------------------------------------------------------------------- #
# T027 — live enumeration
# --------------------------------------------------------------------------- #
def test_live_classify_is_green_and_counts_are_measured(tmp_path):
    proc, envelope = _classify(REPO_ROOT, tmp_path / "classify.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 0, (proc.returncode, envelope.get("findings"))
    assert envelope["decision"] == "pass", envelope.get("findings")
    assert not ({"uncovered", "ambiguous"} & set(_findings_codes(envelope))), envelope["findings"]
    counts = _collect_counts(envelope.get("measured"))
    expected = _expected_counts()
    assert set(counts) == set(FIVE_ROOTS), (
        "C-005: the measured root set must be exactly the five roots; got %s" % sorted(counts))
    for root_id, count in expected.items():
        assert counts[root_id] == count, (
            "%s: measured %d != enumerated %d (counts are measured, never stored)"
            % (root_id, counts[root_id], count))
        assert count > 0, "root %r enumerated zero members — a red assertion, not a green zero" % root_id


# --------------------------------------------------------------------------- #
# T027 — double-direction drift guard
# --------------------------------------------------------------------------- #
def test_body_added_without_a_class_turns_the_check_red(tmp_path):
    repo = _copy_layer(tmp_path)
    added = repo / "skills" / "new-skill" / "SKILL.md"
    added.parent.mkdir(parents=True)
    added.write_text(
        "---\nname: new-skill\n---\n# New Skill\n\nPartition, dispatch, record.\n",
        encoding="utf-8")
    class_fact = repo / "shared" / "declarations" / "facts" / "concurrency-class.yaml"
    text = class_fact.read_text(encoding="utf-8")
    mutated = text.replace(
        "    - name: concurrent-by-default\n", "    - name: concurrent-by-default-renamed\n", 1)
    assert mutated != text, "fixture premise: the class member must be present"
    class_fact.write_text(mutated, encoding="utf-8")
    proc, envelope = _classify(repo, tmp_path / "mutated.json")
    assert proc.returncode != 0, "a body with no resolvable class must turn the check red"
    if envelope is not None:
        assert envelope["decision"] != "pass", envelope.get("findings")


def test_removed_root_from_the_enumeration_leaves_a_red_assertion(tmp_path):
    """The assertion survives the mutation: the measured set must stay the five roots."""
    repo = _copy_layer(tmp_path)
    roots_fact = repo / "shared" / "declarations" / "facts" / "executor-enumeration-roots.yaml"
    roots_fact.write_text(
        _drop_block(roots_fact.read_text(encoding="utf-8"), "skills"), encoding="utf-8")
    proc, envelope = _classify(repo, tmp_path / "removed.json")
    if proc.returncode != 0 or envelope is None:
        return  # a parse-level refusal is also red
    counts = _collect_counts(envelope.get("measured"))
    assert set(counts) == set(FIVE_ROOTS), (
        "a silently dropped root must leave the closed-set assertion red; got %s" % sorted(counts))
