"""Contract guard: read-only containment, offline privacy and boundary discipline (Feature 110).

Clauses carried here: C-029 (no composition is persisted), C-035 (read-only, offline and
private), C-041 (containment claims are decidable) and C-045 (no new command, skill, gate,
store or network path).

Containment-claim discipline (C-041, `shared/guidelines/closed-set-claims.md`):
* **baseline referent** — the SHA-256 tree manifest taken immediately before the action in
  this same test run, never a checked-in digest;
* **comparison unit per artifact class** — per tree: one entry per path carrying its kind
  (`file:<sha256>`, `dir`, `symlink:<target>`); bytecode caches are excluded by name;
* **mechanically derived allowed-delta set** — empty (the audit writes nothing);
* **complement assertion** — the same manifest re-taken after the action must be equal, and
  the action's own process must have attempted no socket connection;
* **no undefined aggregate words** — "identical" means the two manifests compare equal
  entry-for-entry, and "zero new files" means `added == []` over that same comparison.

The repository-tree leg excludes the VCS internals and the roots other framework writers
own concurrently (state, memory tiers, feedback and scratch); those exclusions are named
here, never silent, and the fixture-tree legs carry the strong no-exclusion comparison.

Authored red-first (C-040): the engine does not exist yet at this point of the run, so the
whole module is expected to fail before the implementation rows land.
"""
from __future__ import annotations

import ast
import hashlib
import socket
from pathlib import Path

import pytest

from fixtures.context_management_support import (
    ENGINE,
    REPO_ROOT,
    copy_case_to,
    run_engine,
    tree_manifest,
    manifest_delta,
)
from tests.script_api import run_engine_in_process

pytestmark = pytest.mark.contract

FIXTURE_CASES = ("all-present", "absence-mixed", "concept-missing")
ACTIONS = (("--action", "manifest", "--layer", "project"), ("--action", "check"))
CONCURRENT_PREFIXES = (
    ".git/",
    ".pytest_cache/",
    ".venv/",
    ".specify/state/",
    ".specify/session/",
    ".specify/knowledge/",
    ".specify/exec-quant/",
    ".specify/feedback/",
    ".specify/.tmp/",
)
FORBIDDEN_NETWORK_MODULES = ("socket", "ssl", "http", "urllib", "requests", "httpx", "ftplib", "smtplib")
FORBIDDEN_WRITE_CALLS = {
    "write_text", "write_bytes", "mkdir", "makedirs", "touch", "unlink", "rmdir",
    "copyfile", "copytree", "move", "rename",
}


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repository_manifest() -> dict:
    manifest = {}
    for path in sorted(REPO_ROOT.rglob("*")):
        relative = path.relative_to(REPO_ROOT).as_posix()
        if any(relative.startswith(prefix) for prefix in CONCURRENT_PREFIXES):
            continue
        if "__pycache__" in relative.split("/"):
            continue
        if path.is_symlink():
            manifest[relative] = "symlink:" + str(path.readlink())
        elif path.is_dir():
            manifest[relative] = "dir"
        else:
            manifest[relative] = "file:" + _digest(path)
    return manifest


def _assert_contained(before: dict, after: dict, label: str) -> None:
    added, removed, changed = manifest_delta(before, after)
    assert added == [], f"{label}: the action created file(s): {added}"
    assert removed == [], f"{label}: the action removed file(s): {removed}"
    assert changed == [], f"{label}: the action changed file(s): {changed}"
    assert before == after, f"{label}: the tree manifest must be identical before and after"


# --------------------------------------------------------------------------- #
# C-035 / C-041 — containment claims are decidable
# --------------------------------------------------------------------------- #
def test_containment_claims_are_decidable(tmp_path: Path):
    assert ENGINE.is_file(), f"audit engine missing: {ENGINE}"
    for case in FIXTURE_CASES:
        root = copy_case_to(tmp_path / case, case)
        for action in ACTIONS:
            before = tree_manifest(root)
            completed = run_engine(root, *action)
            assert completed.returncode in (0, 1, 2), (
                f"{case} {action}: exit status outside the declared set: {completed.returncode}")
            after = tree_manifest(root)
            _assert_contained(before, after, f"fixture {case} {action}")

    repo_before = _repository_manifest()
    repo_result = run_engine(REPO_ROOT, "--action", "check")
    assert repo_result.returncode in (0, 1, 2)
    repo_after = _repository_manifest()
    _assert_contained(repo_before, repo_after, "repository tree --action check")


def test_no_action_writes_or_opens_a_socket(tmp_path: Path, monkeypatch):
    attempts = []

    def blocked(*args, **kwargs):
        attempts.append((args, kwargs))
        raise AssertionError("the audit opened a network socket")

    monkeypatch.setattr(socket, "socket", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)

    for case in FIXTURE_CASES:
        root = copy_case_to(tmp_path / case, case)
        for action in ACTIONS:
            before = tree_manifest(root)
            result = run_engine_in_process(ENGINE, (*action, "--workspace-root", str(root)))
            assert result.returncode in (0, 1, 2), (
                f"{case} {action}: exit status outside the declared set: {result.returncode}")
            after = tree_manifest(root)
            _assert_contained(before, after, f"in-process {case} {action}")
    assert attempts == [], f"a socket entry point was reached: {attempts}"


# --------------------------------------------------------------------------- #
# C-029 — no composition is persisted; the engine carries no write path
# --------------------------------------------------------------------------- #
def _engine_tree():
    assert ENGINE.is_file(), f"audit engine missing: {ENGINE}"
    source = ENGINE.read_text(encoding="utf-8")
    return source, ast.parse(source)


def _imported_modules(tree) -> set:
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    return imported


def test_no_composition_is_persisted():
    source, tree = _engine_tree()
    imported = _imported_modules(tree)
    assert imported & set(FORBIDDEN_NETWORK_MODULES) == set(), (
        f"the engine imports a network-capable module: {sorted(imported & set(FORBIDDEN_NETWORK_MODULES))}")
    write_calls = []
    open_modes = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else (
            func.id if isinstance(func, ast.Name) else "")
        if name in FORBIDDEN_WRITE_CALLS:
            write_calls.append(name)
        if name == "open":
            modes = [kw.value.value for kw in node.keywords
                     if kw.arg == "mode" and isinstance(kw.value, ast.Constant)]
            if any(isinstance(mode, str) and set(mode) & set("wax+") for mode in modes):
                open_modes.append(modes)
            for arg in node.args[1:2]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if set(arg.value) & set("wax+"):
                        open_modes.append(arg.value)
    assert write_calls == [], f"the engine calls a write-shaped method: {sorted(set(write_calls))}"
    assert open_modes == [], f"the engine opens a file for writing: {open_modes}"


# --------------------------------------------------------------------------- #
# C-045 — no new command, skill, gate, store or network path
# --------------------------------------------------------------------------- #
def test_no_new_command_skill_gate_store_or_network(tmp_path: Path):
    commands_dir = REPO_ROOT / "templates" / "commands"
    if commands_dir.is_dir():
        naming = [path.name for path in sorted(commands_dir.glob("*.md"))
                  if "context-audit" in path.read_text(encoding="utf-8", errors="ignore")]
        assert naming == [], f"the feature ships a command wrapper: {naming}"
    skills_root = REPO_ROOT / "skills"
    if skills_root.is_dir():
        naming = [str(path.relative_to(REPO_ROOT)) for path in sorted(skills_root.rglob("SKILL.md"))
                  if "context-audit" in path.read_text(encoding="utf-8", errors="ignore")]
        assert naming == [], f"the feature ships a skill wrapper: {naming}"

    _source, tree = _engine_tree()
    imported = _imported_modules(tree)
    assert imported & set(FORBIDDEN_NETWORK_MODULES) == set(), (
        "the audit path reaches a network-capable module")

    # The runtime-store roster is the one declaration; the feature adds no store root.
    from fixtures.context_management_support import declaration_reader

    reader = declaration_reader()
    fact = reader.load_fact(REPO_ROOT, "runtime-store-layout")
    body = fact["body"]
    assert isinstance(body, dict) and body.get("statement"), (
        "the runtime-store roster declaration must stay readable")
    roster_text = str(body["statement"]).lower()
    for invented in ("context-store", "context-cache", "context-index"):
        assert invented not in roster_text, f"a context store root entered the roster: {invented}"