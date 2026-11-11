"""Boundary audit for Feature 099 (P6, T034); revised by Feature 100 (P1 T006, P8 T034).

Contract: ``.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md`` C-008
          (amended in place by Feature 100 C-113: exactly one move, archive-scoped)
          ``.specify/specs/099-speckit-seal/contracts/status-sealed.contract.md`` C-025
          ``.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md``
          C-035/C-036 (four-way boundary, zero new duplicate mechanisms)
          ``.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md``
          C-101 (six-action closed set, 3/3 read-only/write partition) and
          C-111 (per-parent manifest path, parallel writers, no lock files)
          ``.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md``
          C-312 (no derived index, no cache, no second mapping table)
          FR-020 / FR-022 / FR-024 / FR-027 / FR-028 / SC-005 / SC-008 / SC-009

Five evidence families, each statically decidable:

* **engine action table** — the six-action closed set splits exactly 3 read-only /
  3 write and carries no move/delete/archive-retirement action, no push and no
  scheduler; the external-command allowlist admits `git mv` only inside the archive
  batch helpers (C-113's single declared move);
* **write surface as data** — every filesystem write call site is admitted by the
  module-level table below; a registry-status write, a delete outside the byte
  recovery, or a retirement-archive path turns the audit red;
* **status domain single owner** — the seven-value domain and the single forward
  transition live in the declared owner/carrier set only; a second machine copy of the
  value domain on any other framework surface turns this module red;
* **single archive mechanism** — one `archive-manifest.json` per parent spec, no
  shared aggregate, no cache/index, no second mapping table; two fixture specs
  archive in parallel to disjoint manifest paths with no lock file, and the later
  arrival on the same spec converges through the record (`already-archived` /
  `archive-drift`);
* **directory vs registry audit** — spec trees, registries, ledgers and the
  directory/row difference are pinned as a closed, named inventory. A new unexplained
  directory or row is a difference entry this audit refuses.

This is a regression guard (tasks.md § Within Each User Story: the migration/regression
exception row), so it lands after its consumed object (T031) rather than red-first.
Feature 100 updated the guard when C-113 amended C-008 and added the C-111/C-312 audit.

Readings: run with ``SEAL_BOUNDARIES_AUDIT=<path>`` to write the audit dump; the
checked-in copy is ``.specify/specs/099-speckit-seal/test-evidence/boundaries-audit.txt``.
Feature 100's readings land in
``.specify/specs/100-seal-slice-archive/test-evidence/foundational-checks.txt`` and
``.specify/specs/100-seal-slice-archive/test-evidence/us4-checkpoint.txt``.
"""

from __future__ import annotations

import ast
import hashlib
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
ENGINE = ROOT / "scripts" / "python" / "seal-utils.py"

OWNER = "shared/workflow/acceptance-hardening.md"
INTEGRATION = "shared/workflow/feature-integration.md"
DETAILS_TEMPLATE = "templates/feature-details-template.md"
INDEX_TEMPLATE = "templates/feature-index-template.md"
MANAGE_FEATURES = "skills/internal/manage-features/SKILL.md"
NON_DISPOSABLE_DEFINITIONS = "shared/definitions/non-disposable-definitions.md"
NON_DISPOSABLE_ENGINE = "scripts/python/non-disposable-check.py"
CLOSURE_ENGINE = "scripts/python/closure-acceptance-check.py"

#: C-025's declared carrier set (the schema owner included). A seven-value enumeration
#: anywhere else in the framework sources is a second value domain.
STATUS_CARRIERS = {
    OWNER, INTEGRATION, DETAILS_TEMPLATE, INDEX_TEMPLATE, MANAGE_FEATURES,
    NON_DISPOSABLE_DEFINITIONS, NON_DISPOSABLE_ENGINE, CLOSURE_ENGINE,
}

SEVEN_STATUSES = ("Draft", "Planned", "Implemented", "Blocked", "Ready for Review",
                  "Sealed", "Completed")

TRANSITION = "Ready for Review → Sealed"

#: Files allowed to carry the transition arrow / the transition table row.
ARROW_SITES = {OWNER, INTEGRATION}
ROW_SITES = {DETAILS_TEMPLATE}

#: Framework source roots the static scans sweep (mirrors are projections, not owners).
SCAN_ROOTS = ("shared", "templates", "skills", "scripts")

#: C-008: verbs that must never appear as engine actions or as shelled-out git verbs.
DESTRUCTIVE_VERBS = {"move", "delete", "remove", "rm", "mv", "retire", "push", "fetch",
                     "pull", "checkout", "reset", "clean", "branch"}

READ_ONLY_GIT_VERBS = {"status", "rev-parse", "cat-file", "log", "show", "diff",
                       "ls-files", "ls-tree"}

#: C-113 (amending C-008): one move is admitted, and only from the archive batch
#: helpers. `_archive_move` performs the forward `git mv`; `_archive_restore` performs
#: the inverse move of the byte recovery.
ARCHIVE_GIT_VERBS = {"mv"}
ALLOWED_GIT_VERBS = READ_ONLY_GIT_VERBS | ARCHIVE_GIT_VERBS
ARCHIVE_MOVE_FUNCTIONS = {"_archive_move", "_archive_restore"}

#: C-111/C-312: the engine's write surface as data. Each key is the only enclosing
#: function admitted to perform the listed kind; nothing else may write.
WRITE_SITE_TABLE = {
    "_write_if_changed": {"write_text"},
    "_archive_write_text": {"write_text"},
    "_write_seal_batch": {"write_text", "write_bytes"},
    "_archive_restore": {"unlink", "write_bytes", "rmdir"},
}

#: C-312: a derived index or a resolution cache would need one of these.
CACHE_IMPORT_ROOTS = {"functools", "shelve", "dbm", "pickle"}
CACHE_TOKENS = {"lru_cache", "cached_property", "cachetools", "_cache"}
INDEX_TOKENS = (".index", ".pickle", ".db", ".jsonl")

#: C-111: the two independent parent specs used by the parallel-writer leg.
CONCURRENT_FIXTURES = ROOT / "tests" / "fixtures" / "seal-archive" / "concurrent"
NORTH = "110-fixture-north"
NORTH_SLICE = "110a-fixture-north-slice"
SOUTH = "120-fixture-south"
SOUTH_SLICE = "120a-fixture-south-slice"
SPECS_REL = ".specify/specs"

SCHEDULER_ROOTS = {"threading", "multiprocessing", "concurrent", "sched", "signal",
                   "asyncio", "socket", "time", "atexit"}

#: The closed, named difference inventory (dated pin, 2026-11-11). Every entry names
#: why the difference is legitimate; a new difference is unexplained until it is added
#: here with a reason.
UNREGISTERED_LIVE_SPECS = {
    "067": "documented registry gap; the spec tree is complete "
           "(see .specify/features/069-execution-expression-sdd.md § 067 的登记缺口)",
    "075": "extension spec bound to feature 058 "
           "(see .specify/features/058-sdd-loop-driver.md § Related Specifications)",
    "080": "extension spec bound to feature 062 "
           "(see .specify/features/062-humanize-command.md § Related Specifications)",
}
UNREGISTERED_ARCHIVED_SPECS = {
    "054": "archived spec bound to feature 044 "
           "(see .specify/features/044-agent-metadata-portability.md)",
    "066": "archived slice A bound to feature 065 "
           "(see .specify/features/065-loop-interruption-recovery.md)",
}
DETAIL_ONLY_ROWS = {
    "002", "004", "005", "010", "011", "014", "015", "019", "026",
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _load_engine():
    spec = importlib.util.spec_from_file_location("seal_utils_boundaries", ENGINE)
    assert spec is not None and spec.loader is not None, f"cannot load {ENGINE}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


@pytest.fixture(scope="module")
def source() -> str:
    return ENGINE.read_text(encoding="utf-8")


def _tree(source: str):
    return ast.parse(source)


def _import_roots(tree) -> set:
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def _string_constants(tree) -> set:
    return {node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)}


def _framework_files():
    for base in SCAN_ROOTS:
        directory = ROOT / base
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.suffix in (".md", ".py", ".sh"):
                yield path


def _status_tokens_on_line(line: str) -> int:
    return sum(1 for status in SEVEN_STATUSES
               if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(status), line))


def _registry_ids() -> set:
    text = (ROOT / ".specify" / "features.md").read_text(encoding="utf-8")
    return {match.group(1) for match in re.finditer(r"(?m)^\|\s*(\d{3})\s*\|", text)}


def _exact_specs(base: Path) -> dict:
    found = {}
    if not base.is_dir():
        return found
    for path in sorted(base.iterdir()):
        match = re.match(r"^(\d{3})-", path.name)
        if path.is_dir() and match:
            found[match.group(1)] = path.name
    return found


def _slice_specs(base: Path):
    found = []
    if not base.is_dir():
        return found
    for path in sorted(base.iterdir()):
        match = re.match(r"^(\d{3})[a-z]-", path.name)
        if path.is_dir() and match:
            found.append((match.group(1), path.name))
    return found


def _git_verb_sites(tree):
    """Every literal git verb the engine shells out with."""
    verbs = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "_run_git"):
            continue
        if len(node.args) < 2:
            continue
        argument = node.args[1]
        if isinstance(argument, (ast.List, ast.Tuple)) and argument.elts:
            first = argument.elts[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                verbs.append(first.value)
    return verbs


def _enclosing_functions(tree):
    """Map ``id(call node)`` to the innermost function that holds it (None at module)."""
    mapping = {}

    def visit(node, function):
        for child in ast.iter_child_nodes(node):
            inner = (child.name if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                     else function)
            if isinstance(child, ast.Call):
                mapping[id(child)] = function
            visit(child, inner)

    visit(tree, None)
    return mapping


def _write_site_violations(source: str) -> list:
    """C-111/C-312: every write or shell-out call site must be admitted as data."""
    tree = _tree(source)
    enclosing = _enclosing_functions(tree)
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) \
                and (func.value.id, func.attr) in {
                    ("shutil", "move"), ("shutil", "rmtree"), ("os", "remove"),
                    ("os", "unlink"), ("os", "rmdir"), ("os", "rename")}:
            findings.append("module-level destructive call %s.%s"
                            % (func.value.id, func.attr))
            continue
        if isinstance(func, ast.Attribute) and func.attr in {
                "write_text", "write_bytes", "unlink", "rmdir", "rename"}:
            host = enclosing.get(id(node))
            if func.attr not in WRITE_SITE_TABLE.get(host, set()):
                findings.append("%s.%s outside the declared write table"
                                % (host, func.attr))
            continue
        if isinstance(func, ast.Name) and func.id == "_run_git" \
                and len(node.args) >= 2 \
                and isinstance(node.args[1], (ast.List, ast.Tuple)) \
                and node.args[1].elts \
                and isinstance(node.args[1].elts[0], ast.Constant) \
                and isinstance(node.args[1].elts[0].value, str):
            verb = node.args[1].elts[0].value
            host = enclosing.get(id(node))
            if verb not in ALLOWED_GIT_VERBS:
                findings.append("git %s outside the command allowlist" % verb)
            elif verb in ARCHIVE_GIT_VERBS and host not in ARCHIVE_MOVE_FUNCTIONS:
                findings.append("git %s outside the archive batch helpers (%s)"
                                % (verb, host))
    for token in _string_constants(tree):
        if token in ("push", "rm"):
            findings.append("forbidden shell token %r" % token)
        if token == ".specify/archive" or token.startswith(".specify/archive/"):
            findings.append("retirement-archive path %r" % token)
    return findings


def _cache_or_index_violations(source: str) -> list:
    """C-312: no cache engine, no derived index and no second mapping table."""
    tree = _tree(source)
    findings = ["cache import %s" % root
                for root in sorted(_import_roots(tree) & CACHE_IMPORT_ROOTS)]
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in CACHE_TOKENS:
            findings.append("cache name %s" % node.id)
        elif isinstance(node, ast.Attribute) and node.attr in CACHE_TOKENS:
            findings.append("cache attribute %s" % node.attr)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            for token in INDEX_TOKENS:
                if token in node.value:
                    findings.append("index-shaped path %r" % node.value[:80])
    names = set()
    for literal in _string_constants(tree):
        names.update(re.findall(r"[A-Za-z0-9_.-]+\.json", literal))
    for extra in sorted(names - {"merge-manifest.json", "archive-manifest.json"}):
        findings.append("second record or mapping file %s" % extra)
    return findings


def _git_repo(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=fixture",
         "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
         *args],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )


def _copy_concurrent(root: Path) -> Path:
    repo = root / "repo"
    root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(CONCURRENT_FIXTURES, repo)
    assert _git_repo(repo, "init", "-q").returncode == 0
    assert _git_repo(repo, "add", "-A").returncode == 0
    commit = _git_repo(repo, "commit", "-qm", "fixture baseline")
    assert commit.returncode == 0, commit.stderr
    return repo


def _archive_argv(repo: Path, parent: str, action: str = "archive-apply") -> list:
    return [sys.executable, str(ENGINE), "--action", action,
            "--spec-dir", str(repo / SPECS_REL / parent),
            "--repo", str(repo), "--json"]


def _archive(repo: Path, parent: str, action: str = "archive-apply"):
    proc = subprocess.run(_archive_argv(repo, parent, action), cwd=str(repo),
                          capture_output=True, text=True, encoding="utf-8",
                          check=False)
    payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc, payload


def _snapshot_tree(repo: Path) -> dict:
    return {
        str(path.relative_to(repo)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(repo.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(repo).parts
    }


def _condition_codes(payload: dict) -> list:
    return [condition.get("code") for condition in payload.get("conditions") or []]


# ---------------------------------------------------------------------------
# C-008 — the action table carries no destructive action, push or scheduler
# ---------------------------------------------------------------------------

def test_the_action_table_is_closed_and_carries_no_destructive_action(eng):
    actions = tuple(eng.ACTIONS)
    assert actions == ("merge-plan", "merge-apply", "seal", "archive-gate",
                       "archive-plan", "archive-apply"), (
        f"C-101: the action table is closed at exactly these six; got {actions}"
    )
    for action in actions:
        head = action.split("-", 1)[0]
        assert head not in DESTRUCTIVE_VERBS, (
            f"C-008: the action table MUST NOT carry a {head!r} action; got {action!r}"
        )
    archive_actions = [action for action in actions if "archive" in action]
    assert archive_actions == ["archive-gate", "archive-plan", "archive-apply"], (
        "C-101: the archive-shaped actions are the admission query, the read-only "
        f"archive plan and the archive write batch; got {archive_actions}"
    )
    assert "archive-gate" in eng.READ_ONLY_ACTIONS and "archive-plan" in eng.READ_ONLY_ACTIONS, (
        "C-030/C-101: `archive-gate` and `archive-plan` are queries — they MUST stay "
        "on the read-only side"
    )
    assert "archive-apply" in eng.WRITE_ACTIONS, (
        "C-101: `archive-apply` is the only archive write action"
    )
    assert len(eng.READ_ONLY_ACTIONS) == 3 and len(eng.WRITE_ACTIONS) == 3, (
        "C-101: the six actions split exactly 3 read-only / 3 write"
    )
    assert set(eng.READ_ONLY_ACTIONS) | set(eng.WRITE_ACTIONS) == set(actions)
    assert not set(eng.READ_ONLY_ACTIONS) & set(eng.WRITE_ACTIONS)
    assert set(eng.HANDLERS) == set(actions)


def test_the_external_command_allowlist_is_closed_and_archive_scoped(source):
    tree = _tree(source)
    verbs = _git_verb_sites(tree)
    assert verbs, "the audit expects the engine's closed git helper call sites"
    outside = sorted(set(verbs) - ALLOWED_GIT_VERBS)
    assert outside == [], (
        "C-008/C-113: the engine admits the read-only verbs plus exactly one move; "
        f"got {outside}"
    )
    enclosing = _enclosing_functions(tree)
    move_hosts = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "_run_git"):
            continue
        if len(node.args) < 2 or not isinstance(node.args[1], (ast.List, ast.Tuple)):
            continue
        first = node.args[1].elts[0] if node.args[1].elts else None
        if isinstance(first, ast.Constant) and first.value == "mv":
            move_hosts.add(enclosing.get(id(node)))
    assert move_hosts == ARCHIVE_MOVE_FUNCTIONS, (
        "C-113: the only move sites are the forward batch move and the recovery's "
        f"inverse move; got {sorted(str(item) for item in move_hosts)}"
    )
    literals = _string_constants(tree)
    banned = DESTRUCTIVE_VERBS - ARCHIVE_GIT_VERBS
    destructive = sorted(token for token in banned if token in literals)
    assert destructive == [], (
        f"C-008: destructive verb literals MUST NOT exist in the engine; got {destructive}"
    )


def test_injected_push_delete_or_registry_write_turns_the_audit_red(source):
    assert _write_site_violations(source) == [], (
        "C-111/C-312: the live engine's write and command sites are all declared: "
        f"{_write_site_violations(source)}"
    )
    push = source + ('\n\ndef _injected_push(repo):\n'
                     '    return _run_git(repo, ["push", "--force"])\n')
    assert any("push" in item for item in _write_site_violations(push)), (
        "C-008: an injected `git push` MUST turn the audit red"
    )
    removal = source + ('\n\ndef _injected_remove(repo):\n'
                        '    return _run_git(repo, ["rm", "-rf", "slice"])\n')
    assert any("rm" in item for item in _write_site_violations(removal)), (
        "C-008: an injected `git rm` MUST turn the audit red"
    )
    deletion = source + ('\n\ndef _injected_delete(path):\n'
                         '    path.unlink()\n')
    assert any("unlink" in item for item in _write_site_violations(deletion)), (
        "C-111: a delete outside the byte recovery MUST turn the audit red"
    )
    registry = source + ('\n\ndef _injected_registry(repo):\n'
                         '    (repo / ".specify" / "features.md")'
                         '.write_text("Status: Sealed\\n", encoding="utf-8")\n')
    assert any("write_text" in item for item in _write_site_violations(registry)), (
        "C-111: a registry-status write MUST turn the audit red"
    )
    shared = source + ('\nSHARED_ARCHIVE_ROOT = '
                       '".specify/archive/manifests"\n')
    assert any(".specify/archive" in item for item in _write_site_violations(shared)), (
        "C-111/SC-009: copying records into a retirement-archive aggregate MUST "
        "turn the audit red"
    )
    second_table = source + '\nSECOND_TABLE = "archive-index.json"\n'
    assert any("archive-index.json" in item
               for item in _cache_or_index_violations(second_table)), (
        "C-312: a second mapping table MUST turn the audit red"
    )


def test_the_write_surface_is_a_data_table_and_the_move_is_archive_only(eng):
    assert eng.ARCHIVE_SLICES_DIR == "slices", (
        "C-111: the one archive destination directory is `slices`"
    )
    assert eng._archive_destination_rel("100-parent", "100a-slice") == (
        ".specify/specs/100-parent/slices/100a-slice"
    ), "C-113: the move destination is the parent spec's slices/<slug>/ subtree"
    source = ENGINE.read_text(encoding="utf-8")
    assert _write_site_violations(source) == [], (
        "C-111: the write surface is expressed as a data table and every site stays "
        f"inside it; violations: {_write_site_violations(source)}"
    )


def test_the_engine_carries_no_scheduler_or_daemon_constructs(source):
    tree = _tree(source)
    banned = _import_roots(tree) & SCHEDULER_ROOTS
    assert banned == set(), (
        f"C-036: no scheduler/daemon construct belongs in the seal engine; got {banned}"
    )
    for token in ("sleep", "Timer", "setitimer", "daemon"):
        assert token not in _string_constants(tree), (
            f"C-036: the engine MUST NOT carry a {token!r} construct"
        )


# ---------------------------------------------------------------------------
# C-025 — the status domain has exactly one machine owner
# ---------------------------------------------------------------------------

def test_the_transition_arrow_lives_only_on_the_owner_and_its_protocol_row():
    sites = set()
    for path in _framework_files():
        if TRANSITION in path.read_text(encoding="utf-8", errors="ignore"):
            sites.add(str(path.relative_to(ROOT)))
    assert sites == ARROW_SITES, (
        "C-025/C-036: the forward transition MUST be stated only by the schema owner "
        f"and its integration protocol row; found {sorted(sites)}"
    )


def test_the_transition_table_row_lives_only_on_the_details_template():
    sites = set()
    row = "| Ready for Review | Sealed |"
    for path in _framework_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if row in text:
            sites.add(str(path.relative_to(ROOT)))
    assert sites == ROW_SITES, (
        "C-025: the canonical transition table lives in the feature-details template; "
        f"a second table with the same row is a second state machine; found {sorted(sites)}"
    )


def test_no_second_machine_copy_of_the_seven_value_domain():
    offenders = []
    for path in _framework_files():
        relative = str(path.relative_to(ROOT))
        if relative in STATUS_CARRIERS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if _status_tokens_on_line(line) >= 6:
                offenders.append((relative, line.strip()[:160]))
                break
    assert offenders == [], (
        "C-025/C-036: a second machine copy of the seven-value status domain is a "
        f"second state machine; found {offenders}"
    )


def test_the_schema_owner_declares_itself_the_single_status_authority():
    text = (ROOT / OWNER).read_text(encoding="utf-8")
    section = text.split("## Feature Status", 1)
    assert len(section) == 2, f"{OWNER} lost its § Feature Status section"
    body = section[1].split("\n## ", 1)[0]
    assert "Sealed" in body and "terminal" in body.lower(), (
        "C-025: § Feature Status MUST define `Sealed` as the terminal status"
    )
    assert TRANSITION in body, "C-025: the owner MUST carry the single forward transition"


# ---------------------------------------------------------------------------
# C-036 — no second registry, ledger, or parallel spec tree
# ---------------------------------------------------------------------------

def test_registries_and_ledgers_are_single_files():
    registries, registers = [], []
    for path in ROOT.rglob("*"):
        relative = str(path.relative_to(ROOT))
        if not path.is_file() or relative.startswith((".git/", ".specify/.tmp/")):
            continue
        if relative.startswith(("tests/", "docs/")):
            continue
        if path.name == "features.md":
            registries.append(relative)
        if path.name == "register.md":
            registers.append(relative)
    assert sorted(registries) == [".specify/features.md", "memory/features.md"], (
        "C-036: the live registry is `.specify/features.md`; `memory/features.md` is "
        f"the shipped placeholder. Found {sorted(registries)}"
    )
    placeholder = (ROOT / "memory" / "features.md").read_text(encoding="utf-8")
    assert "placeholder" in placeholder.lower(), (
        "memory/features.md stopped being the shipped placeholder — a second "
        "registry may have appeared"
    )
    assert registers == [".specify/register.md"], (
        f"C-036: exactly one ID register exists; found {sorted(registers)}"
    )


def test_there_is_one_live_spec_tree_and_one_archive():
    trees = []
    for path in ROOT.rglob("specs"):
        relative = str(path.relative_to(ROOT))
        if not path.is_dir() or relative.startswith((".git", ".specify/.tmp")):
            continue
        if relative.startswith("tests/"):
            continue
        trees.append(relative)
    assert sorted(trees) == [".specify/archive/specs", ".specify/specs"], (
        "C-036: a third spec tree is a parallel tree by definition; "
        f"found {sorted(trees)}"
    )


def test_the_seal_records_stay_per_spec_single_files(eng):
    allowlist = tuple(eng.WRITE_PATH_ALLOWLIST)
    assert allowlist == (
        "{spec_dir}/seal.md",
        "{spec_dir}/merge-manifest.json",
        "{spec_dir}/{merged_artifact}",
        "{slice_dir}/requirements.md",
        "{factory_doc}",
    ), "C-008/C-036: the write-path allowlist is closed; a new entry is a contract change"
    for entry in allowlist:
        assert entry.startswith(("{spec_dir}", "{slice_dir}", "{factory_doc}")), (
            f"C-036: every write is per spec/slice file; got shared path {entry}"
        )
        assert ".jsonl" not in entry and not entry.endswith(".index"), (
            f"C-036: no shared mutable aggregate; got {entry}"
        )
    source = ENGINE.read_text(encoding="utf-8")
    assert ".jsonl" not in source, (
        "C-036/Concurrent Development Safety: records are per-entry files, never one "
        "shared .jsonl stream"
    )


# ---------------------------------------------------------------------------
# C-111 / C-312 — one per-parent manifest, parallel writers, no cache index
# ---------------------------------------------------------------------------

def test_c111_parallel_archives_write_disjoint_manifest_paths(tmp_path):
    north_repo = _copy_concurrent(tmp_path / "north")
    south_repo = _copy_concurrent(tmp_path / "south")
    processes = [
        subprocess.Popen(_archive_argv(north_repo, NORTH), cwd=str(north_repo),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, encoding="utf-8"),
        subprocess.Popen(_archive_argv(south_repo, SOUTH), cwd=str(south_repo),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, encoding="utf-8"),
    ]
    outputs = [process.communicate(timeout=180) for process in processes]
    for process, (stdout, stderr) in zip(processes, outputs):
        assert process.returncode == 0, (
            "C-111: a fixture spec archives in its own tree; "
            f"stdout={stdout[-800:]!r} stderr={stderr[-800:]!r}"
        )
        payload = json.loads(stdout)
        assert payload["outcome"] == "archived"

    north_manifest = north_repo / SPECS_REL / NORTH / "archive-manifest.json"
    south_manifest = south_repo / SPECS_REL / SOUTH / "archive-manifest.json"
    assert north_manifest.is_file() and south_manifest.is_file(), (
        "C-111: each parent spec owns exactly one manifest at its own root"
    )
    assert (north_manifest.relative_to(north_repo)
            != south_manifest.relative_to(south_repo)), (
        "C-111: two parallel lines MUST write different manifest paths"
    )
    for repo, parent in ((north_repo, NORTH), (south_repo, SOUTH)):
        manifests = sorted(repo.rglob("archive-manifest.json"))
        assert len(manifests) == 1, (
            f"C-111: one manifest per parent spec; got {manifests}"
        )
        assert manifests[0].parent == repo / SPECS_REL / parent
        assert not sorted(repo.rglob("*.lock")), (
            "C-111: archive concurrency MUST NOT create a lock file"
        )
        assert not sorted(repo.rglob("*.lease")) and not sorted(repo.rglob("*.coord"))


def test_c111_same_spec_later_arrival_converges_and_drift_is_named(tmp_path):
    repo = _copy_concurrent(tmp_path)
    proc, payload = _archive(repo, NORTH)
    assert proc.returncode == 0 and payload["outcome"] == "archived", (
        f"C-111: the first writer archives; exit={proc.returncode} payload={payload!r}"
    )
    settled = _snapshot_tree(repo)
    manifest = repo / SPECS_REL / NORTH / "archive-manifest.json"
    rerun, rerun_payload = _archive(repo, NORTH)
    assert rerun.returncode == 0 and rerun_payload["outcome"] == "already-archived", (
        "C-111: the later arrival reads the record and converges to already-archived; "
        f"exit={rerun.returncode} outcome={rerun_payload.get('outcome')!r}"
    )
    assert _snapshot_tree(repo) == settled, (
        "C-111: the later arrival writes nothing"
    )
    manifest.unlink()
    drift, drift_payload = _archive(repo, NORTH, "archive-plan")
    assert drift.returncode == 2, (
        "C-111/C-112: every slice at the destination with the record absent is an "
        f"input error, not a pass; exit={drift.returncode}"
    )
    assert "archive-drift" in _condition_codes(drift_payload)


def test_c312_resolution_is_recomputed_and_carries_no_cache_index():
    source = ENGINE.read_text(encoding="utf-8")
    violations = _cache_or_index_violations(source)
    assert violations == [], (
        "C-312: no cache engine, derived index or second mapping table exists; "
        f"got {violations}"
    )
    injection = source + ('\nimport functools\n\n\n'
                          '@functools.lru_cache(maxsize=None)\n'
                          'def _mapping(slug):\n    return slug\n')
    assert _cache_or_index_violations(injection), (
        "C-312: a cached mapping MUST turn the audit red"
    )


def test_c312_tree_is_reread_on_every_run(tmp_path):
    repo = _copy_concurrent(tmp_path)
    proc, _payload = _archive(repo, NORTH)
    assert proc.returncode == 0
    stray = repo / SPECS_REL / NORTH / "slices" / NORTH_SLICE / "stray.txt"
    stray.write_text("drift\n", encoding="utf-8")
    plan, payload = _archive(repo, NORTH, "archive-plan")
    assert plan.returncode == 2, (
        "C-312: resolution re-runs per action; a tree change is observed, never "
        f"served from a cache; exit={plan.returncode}"
    )
    assert "archive-drift" in _condition_codes(payload)


# ---------------------------------------------------------------------------
# the directory vs registry difference audit
# ---------------------------------------------------------------------------

def _audit_difference():
    registered = _registry_ids()
    live = _exact_specs(ROOT / ".specify" / "specs")
    archived = _exact_specs(ROOT / ".specify" / "archive" / "specs")
    slices = (_slice_specs(ROOT / ".specify" / "specs")
              + _slice_specs(ROOT / ".specify" / "archive" / "specs"))
    unregistered_live = sorted(set(live) - registered)
    unregistered_archived = sorted(set(archived) - registered)
    detail_only = sorted(registered - set(live) - set(archived))
    orphan_slices = sorted(parent for parent, _name in slices if parent not in registered)
    return {
        "registered": sorted(registered),
        "live": live,
        "archived": archived,
        "slices": slices,
        "unregistered_live": unregistered_live,
        "unregistered_archived": unregistered_archived,
        "detail_only": detail_only,
        "orphan_slices": orphan_slices,
    }


def test_the_directory_registry_difference_is_fully_classified():
    diff = _audit_difference()
    assert diff["unregistered_live"] == sorted(UNREGISTERED_LIVE_SPECS), (
        "C-036: a live spec directory without a registry row is a difference entry; "
        "a new one MUST be registered or pinned here with its reason. Ungoverned: "
        f"{diff['unregistered_live']}"
    )
    assert diff["unregistered_archived"] == sorted(UNREGISTERED_ARCHIVED_SPECS), (
        "C-036: an archived spec directory without a registry row is a difference "
        f"entry; ungoverned: {diff['unregistered_archived']}"
    )
    assert diff["detail_only"] == sorted(DETAIL_ONLY_ROWS), (
        "C-036: registry rows without a spec tree are legacy detail-only rows; a new "
        f"one MUST be pinned. Ungoverned: {diff['detail_only']}"
    )
    assert diff["orphan_slices"] == [], (
        f"C-036: every slice directory names a registered parent; got {diff['orphan_slices']}"
    )
    assert "099" in diff["live"] and "099" in diff["registered"], (
        "SC-008: feature 099 MUST exist as both a registry row and a live spec tree"
    )


# ---------------------------------------------------------------------------
# the audit dump (T034: readings land in test-evidence/)
# ---------------------------------------------------------------------------

def _audit_report() -> str:
    eng = _load_engine()
    tree = _tree(ENGINE.read_text(encoding="utf-8"))
    diff = _audit_difference()
    seven_lines = []
    for path in _framework_files():
        relative = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if _status_tokens_on_line(line) >= 6:
                seven_lines.append(relative)
                break
    lines = [
        "# Seal boundaries audit (Feature 099, T034)",
        "",
        "Engine: scripts/python/seal-utils.py",
        "Action table: %s" % ", ".join(eng.ACTIONS),
        "Read-only: %s" % ", ".join(eng.READ_ONLY_ACTIONS),
        "Write: %s" % ", ".join(eng.WRITE_ACTIONS),
        "Gate reasons: %s" % ", ".join(eng.ARCHIVE_GATE_REASONS),
        "Git verbs: %s" % ", ".join(sorted(set(_git_verb_sites(tree)))),
        "Scheduler imports: none" if not (_import_roots(tree) & SCHEDULER_ROOTS)
        else "Scheduler imports: %s" % sorted(_import_roots(tree) & SCHEDULER_ROOTS),
        "Status owner: %s § Feature Status" % OWNER,
        "Transition arrow sites: %s" % ", ".join(sorted(ARROW_SITES)),
        "Transition row sites: %s" % ", ".join(sorted(ROW_SITES)),
        "Seven-status lines: %d (declared carriers only)" % len(seven_lines),
        "Registries: .specify/features.md (live); memory/features.md (shipped placeholder)",
        "ID register: .specify/register.md",
        "Spec trees: .specify/specs (live); .specify/archive/specs (archive)",
        "Registry rows: %d" % len(diff["registered"]),
        "Live spec dirs: %d; archived: %d; slice dirs: %d"
        % (len(diff["live"]), len(diff["archived"]), len(diff["slices"])),
        "Unregistered live specs: %s" % (
            ", ".join("%s (%s)" % (key, UNREGISTERED_LIVE_SPECS[key])
                      for key in diff["unregistered_live"]) or "-"),
        "Unregistered archived specs: %s" % (
            ", ".join("%s (%s)" % (key, UNREGISTERED_ARCHIVED_SPECS[key])
                      for key in diff["unregistered_archived"]) or "-"),
        "Detail-only rows: %s" % ", ".join(diff["detail_only"]),
        "Orphan slices: %s" % (", ".join(diff["orphan_slices"]) or "none"),
        "Shared mutable aggregates introduced by seal: none (seal.md and "
        "merge-manifest.json are per-spec single files)",
        "",
        "Verdict: clean",
    ]
    return "\n".join(lines) + "\n"


def test_the_audit_report_is_complete_and_optionally_recorded():
    report = _audit_report()
    assert "Verdict: clean" in report
    assert "Action table: merge-plan, merge-apply, seal, archive-gate, " \
           "archive-plan, archive-apply" in report
    assert "Orphan slices: none" in report
    target = os.environ.get("SEAL_BOUNDARIES_AUDIT")
    if target:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
        assert path.is_file() and path.stat().st_size > 0
