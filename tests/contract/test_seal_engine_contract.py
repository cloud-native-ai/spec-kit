"""Contract tests for the seal engine CLI surface (Feature 099, work package P2).

Contract: ``.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md``
          (C-001's action-set owner, revised in place to six values by Feature 100 C-101)
          ``.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md``
          C-101 / C-115 — the six-action closed set and the unchanged CLI surface.
Clauses:  C-001 … C-010 — the six-action closed set, the three-value exit domain,
          zero-side-effect ``--help`` / ``--version``, undeclared-option rejection,
          the closed option surface, the two-phase declaration, stdout-only
          reports, the write-path allowlist, the literal ``.specify`` mirror guard
          and the stable ``--json`` payload.

Red-first: this file landed before ``scripts/python/seal-utils.py`` existed; the
red reading lives in ``.specify/specs/099-speckit-seal/notes/red-first-evidence.md``.
The Feature 100 expansion to six actions was written red first; that reading lives
in ``.specify/specs/100-seal-slice-archive/notes/red-first-evidence.md``.
Every assertion is written to survive P3–P6: the action bodies are not pinned,
only the surface the later work packages must keep.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
ENGINE_HELPER = REPO_ROOT / "scripts" / "python" / "script_interface_cli.py"

ACTIONS = ("merge-plan", "merge-apply", "seal", "archive-gate",
           "archive-plan", "archive-apply")
READ_ONLY_ACTIONS = ("merge-plan", "archive-gate", "archive-plan")
WRITE_ACTIONS = ("merge-apply", "seal", "archive-apply")

#: C-004's closed option surface (``-h``/``--help`` come from argparse itself).
DECLARED_OPTIONS = {
    "--action", "--spec-dir", "--repo", "--feature-detail", "--feature-registry",
    "--json", "-h", "--help", "--version",
}

FORBIDDEN_FLAGS = ("--force", "--no-verify", "--waive")

#: C-002: the exit domain, written as data so a fourth value cannot slip in silently.
EXIT_DOMAIN = (0, 1, 2)

VERDICT_TO_EXIT = {"ok": 0, "refused": 1, "error": 2}

#: C-008: destructive filesystem operations the engine's action table must never carry.
DESTRUCTIVE_MODULE_ATTRS = {
    ("shutil", "move"), ("shutil", "rmtree"),
    ("os", "remove"), ("os", "unlink"), ("os", "rmdir"), ("os", "rename"),
}
DESTRUCTIVE_PATH_ATTRS = {"unlink", "rmdir", "rename"}

#: FR-021: stdlib-only. ``script_interface_cli`` ships beside the engine by the same
#: ``scripts/`` mirror and is the contract-mandated guard.
ALLOWED_IMPORT_ROOTS = {
    "__future__", "argparse", "collections", "copy", "datetime", "hashlib", "io",
    "itertools", "json", "os", "pathlib", "re", "shutil", "subprocess", "sys",
    "tempfile", "typing", "unicodedata", "script_interface_cli",
}

MIRROR_CODE = "mirror-copy"
SPEC_DIR_CODE = "spec-dir-invalid"


# ---------------------------------------------------------------------------
# fixtures and helpers
# ---------------------------------------------------------------------------

def _load_engine():
    assert ENGINE.is_file(), (
        "engine missing: scripts/python/seal-utils.py has not landed (T017); "
        "this is the expected red-first reading for T016"
    )
    spec = importlib.util.spec_from_file_location("seal_utils_under_test", ENGINE)
    assert spec is not None and spec.loader is not None, f"cannot load {ENGINE}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


@pytest.fixture(scope="module")
def engine() -> Path:
    assert ENGINE.is_file(), (
        "engine missing: scripts/python/seal-utils.py has not landed (T017); "
        "this is the expected red-first reading for T016"
    )
    return ENGINE


@pytest.fixture(scope="module")
def source(engine: Path) -> str:
    return engine.read_text(encoding="utf-8")


def _make_spec(root: Path, name: str = "099-fixture-spec") -> Path:
    spec_dir = root / ".specify" / "specs" / name
    spec_dir.mkdir(parents=True, exist_ok=True)
    (spec_dir / "requirements.md").write_text(
        "# Requirements: fixture\n\n- **FR-001**: fixture requirement\n",
        encoding="utf-8",
    )
    return spec_dir


def _run(engine: Path, args, cwd: Path):
    return subprocess.run(
        [sys.executable, str(engine), *args],
        cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", check=False,
    )


def _snapshot(root: Path) -> dict:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def _payload(proc) -> dict:
    assert proc.stdout.strip(), (
        f"expected a stdout payload; exit={proc.returncode} stderr={proc.stderr[-800:]!r}"
    )
    return json.loads(proc.stdout)


def _codes(payload: dict) -> list:
    return [c.get("code") for c in payload.get("conditions", [])]


def _install_copy(engine: Path, target_dir: Path) -> Path:
    """Install the engine (plus the guard helper it imports) at ``target_dir``."""
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(engine, target_dir / ENGINE.name)
    shutil.copy2(ENGINE_HELPER, target_dir / ENGINE_HELPER.name)
    return target_dir / ENGINE.name


def _import_roots(tree: ast.AST) -> set:
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def _call_arg_strings(tree: ast.AST):
    """Every string literal inside a subprocess/os.system argv, for the push scan."""
    exec_attrs = {"run", "call", "check_call", "check_output", "Popen", "system"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute) or func.attr not in exec_attrs:
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                yield sub.value


def _write_calls(node: ast.AST) -> list:
    """Write calls inside an AST subtree (C-005: the evaluate phase owns none)."""
    found = []
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        func = sub.func
        if isinstance(func, ast.Attribute) and func.attr in ("write_text", "write_bytes"):
            found.append(func.attr)
        elif isinstance(func, ast.Attribute) and func.attr == "replace" \
                and isinstance(func.value, ast.Name) and func.value.id == "os":
            found.append("os.replace")
        elif isinstance(func, ast.Name) and func.id == "open":
            modes = [a.value for a in sub.args if isinstance(a, ast.Constant)
                     and isinstance(a.value, str)]
            if any(any(flag in mode for flag in "wax+") for mode in modes):
                found.append("open-write")
    return found


# ---------------------------------------------------------------------------
# C-001 / 100 C-101 — the action set is exactly six, and there is no seventh
# ---------------------------------------------------------------------------

def test_c001_action_set_is_exactly_the_six(eng):
    assert tuple(eng.ACTIONS) == ACTIONS, (
        "C-001/C-101: the engine's action set MUST be exactly the six closed actions"
    )
    parser = eng.build_parser()
    action = next(a for a in parser._actions if a.dest == "action")
    assert set(action.choices) == set(ACTIONS)
    assert len(action.choices) == 6


def test_c001_dispatch_table_covers_exactly_the_six(eng):
    assert set(eng.HANDLERS) == set(ACTIONS), (
        "C-001/C-101: every declared action has exactly one dispatch entry and no other"
    )
    assert len(eng.HANDLERS) == 6


def test_c001_undeclared_action_is_rejected_with_exit_two_and_echoes_name(engine, tmp_path):
    spec_dir = _make_spec(tmp_path)
    before = _snapshot(tmp_path)
    proc = _run(engine, ["--action", "archive-everything", "--spec-dir", str(spec_dir)], tmp_path)
    assert proc.returncode == 2, (
        f"C-001: an undeclared action MUST exit 2; got {proc.returncode}"
    )
    assert "archive-everything" in (proc.stdout + proc.stderr), (
        "C-001: the rejection MUST echo the action name"
    )
    assert _snapshot(tmp_path) == before, "a rejected action MUST NOT touch the tree"


# ---------------------------------------------------------------------------
# C-002 — the exit domain is exactly three values
# ---------------------------------------------------------------------------

def test_c002_exit_code_domain_is_exactly_three_values(eng, source):
    assert (eng.EXIT_OK, eng.EXIT_REFUSED, eng.EXIT_INPUT_ERROR) == EXIT_DOMAIN
    assert tuple(eng.EXIT_CODES) == EXIT_DOMAIN
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and isinstance(node.func.value, ast.Name) \
                and node.func.value.id == "sys" and node.func.attr == "exit":
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, int):
                    assert arg.value in EXIT_DOMAIN, (
                        f"C-002: sys.exit({arg.value}) leaves the closed exit domain"
                    )


def test_c002_every_invocation_family_stays_inside_the_domain(engine, tmp_path):
    spec_dir = _make_spec(tmp_path)
    families = [
        ["--help"],
        ["--version"],
        ["--bogus"],
        ["--action", "bogus", "--spec-dir", str(spec_dir)],
        ["--action", "merge-plan"],                                  # --spec-dir missing
        ["--action", "merge-plan", "--spec-dir", str(tmp_path / "absent")],
    ] + [
        ["--action", action, "--spec-dir", str(spec_dir), "--json"] for action in ACTIONS
    ]
    for argv in families:
        proc = _run(engine, argv, tmp_path)
        assert proc.returncode in EXIT_DOMAIN, (
            f"C-002: {argv!r} exited {proc.returncode}; the domain is exactly 0/1/2"
        )


# ---------------------------------------------------------------------------
# C-003 — --help / --version are zero-side-effect; undeclared options are red
# ---------------------------------------------------------------------------

def test_c003_help_answers_zero_side_effect_and_carries_the_cli_labels(engine, tmp_path):
    before = _snapshot(tmp_path)
    proc = _run(engine, ["--help"], tmp_path)
    assert proc.returncode == 0, f"C-003: --help MUST exit 0; got {proc.returncode}"
    assert _snapshot(tmp_path) == before, "C-003: --help MUST NOT touch the workspace"
    for label in ("usage", "options", "side-effects:", "exit-codes:"):
        assert label in proc.stdout.lower(), (
            f"C-003: the help body MUST carry the {label!r} label"
        )
    for action in ACTIONS:
        assert action in proc.stdout, (
            f"C-101: the help body MUST list the {action!r} action label"
        )


def test_c003_version_answers_one_line_identity_zero_side_effect(engine, tmp_path):
    before = _snapshot(tmp_path)
    proc = _run(engine, ["--version"], tmp_path)
    assert proc.returncode == 0, f"C-003: --version MUST exit 0; got {proc.returncode}"
    lines = [line for line in proc.stdout.strip().splitlines() if line.strip()]
    assert len(lines) == 1, f"C-003: --version prints exactly one line; got {lines!r}"
    assert re.fullmatch(r"seal-utils\.py \S+", lines[0]), (
        f"C-003: the version line is `<script-name> <version>`; got {lines[0]!r}"
    )
    assert _snapshot(tmp_path) == before, "C-003: --version MUST NOT touch the workspace"


@pytest.mark.parametrize("argv", [
    ["--bogus", "--action", "merge-plan", "--spec-dir", "{spec}"],
    ["--version", "--bogus"],
    ["--action", "merge-plan", "--spec-dir", "{spec}", "--", "--bogus"],
])
def test_c003_undeclared_option_is_rejected_before_any_action(engine, tmp_path, argv):
    spec_dir = _make_spec(tmp_path)
    argv = [a.replace("{spec}", str(spec_dir)) for a in argv]
    before = _snapshot(tmp_path)
    proc = _run(engine, argv, tmp_path)
    assert proc.returncode == 2, (
        f"C-003: any undeclared option MUST be rejected with 2; got {proc.returncode} "
        f"for {argv!r}"
    )
    assert _snapshot(tmp_path) == before, "C-003: a rejected option MUST NOT reach an action"


# ---------------------------------------------------------------------------
# C-004 — the option surface is closed
# ---------------------------------------------------------------------------

def test_c004_option_surface_is_closed(eng):
    parser = eng.build_parser()
    options = {opt for action in parser._actions for opt in action.option_strings}
    assert options == DECLARED_OPTIONS, (
        f"C-004: the declared option surface is closed; measured {sorted(options)}"
    )


def test_c004_spec_dir_is_required_with_no_default(eng):
    parser = eng.build_parser()
    spec_dir = next(a for a in parser._actions if a.dest == "spec_dir")
    assert spec_dir.required is True, "C-004: --spec-dir is required"
    assert spec_dir.default is None, "C-004: --spec-dir carries no default"


def test_c004_missing_spec_dir_exits_two(engine, tmp_path):
    proc = _run(engine, ["--action", "merge-plan"], tmp_path)
    assert proc.returncode == 2, f"C-004: a missing --spec-dir exits 2; got {proc.returncode}"


def test_c004_no_bypass_flags_exist(eng):
    options = {opt for a in eng.build_parser()._actions for opt in a.option_strings}
    for flag in FORBIDDEN_FLAGS:
        assert flag not in options, f"C-004: bypass flag {flag} MUST NOT exist"


# ---------------------------------------------------------------------------
# C-005 — judgment and write are two declared phases
# ---------------------------------------------------------------------------

def test_c005_read_only_and_write_actions_partition_the_closed_set(eng):
    assert tuple(eng.READ_ONLY_ACTIONS) == READ_ONLY_ACTIONS
    assert tuple(eng.WRITE_ACTIONS) == WRITE_ACTIONS
    assert len(eng.READ_ONLY_ACTIONS) == 3 and len(eng.WRITE_ACTIONS) == 3, (
        "C-101: the six actions split exactly 3 read-only / 3 write"
    )
    assert set(eng.READ_ONLY_ACTIONS) | set(eng.WRITE_ACTIONS) == set(eng.ACTIONS)
    assert not set(eng.READ_ONLY_ACTIONS) & set(eng.WRITE_ACTIONS)


def test_c005_seal_declares_evaluate_before_apply(eng, source):
    assert callable(eng.evaluate_seal), "C-005: the seal judgment phase is declared"
    assert callable(eng.apply_seal), "C-005: the seal write phase is declared"
    tree = ast.parse(source)
    handler = next(
        (n for n in ast.walk(tree)
         if isinstance(n, ast.FunctionDef) and n.name == "action_seal"), None,
    )
    assert handler is not None, "C-005: the seal dispatcher is declared"
    calls = [c.func.id for c in ast.walk(handler)
             if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)]
    assert "evaluate_seal" in calls and "apply_seal" in calls, (
        "C-005: the seal dispatcher calls the judgment phase and the write phase"
    )
    assert calls.index("evaluate_seal") < calls.index("apply_seal"), (
        "C-005: the judgment phase runs before the write phase"
    )
    evaluate = next(
        (n for n in ast.walk(tree)
         if isinstance(n, ast.FunctionDef) and n.name == "evaluate_seal"), None,
    )
    assert not _write_calls(evaluate), (
        "C-005: evaluate_seal MUST stay read-only — the write phase owns every write"
    )


# ---------------------------------------------------------------------------
# C-006 — reports go to stdout only; refusals persist nothing
# ---------------------------------------------------------------------------

def test_c006_read_only_reports_go_to_stdout_only(engine, tmp_path):
    spec_dir = _make_spec(tmp_path)
    for action in READ_ONLY_ACTIONS:
        proc = _run(engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], tmp_path)
        assert proc.stderr == "", (
            f"C-006: {action} MUST report on stdout only; stderr={proc.stderr[-500:]!r}"
        )
        payload = _payload(proc)
        assert payload["action"] == action
        assert payload["exit_code"] == proc.returncode, (
            "C-010: the payload's exit_code matches the process exit code"
        )


def test_c006_read_only_actions_persist_nothing(engine, tmp_path):
    spec_dir = _make_spec(tmp_path)
    for action in READ_ONLY_ACTIONS:
        before = _snapshot(tmp_path)
        _run(engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], tmp_path)
        assert _snapshot(tmp_path) == before, (
            f"FR-021/C-008: read-only action {action} MUST NOT write"
        )


def test_c006_refusal_report_is_rerun_stable(engine, tmp_path):
    repo = tmp_path / "repo"
    mirror_engine = _install_copy(engine, repo / ".specify" / "scripts" / "python")
    spec_dir = _make_spec(repo)
    argv = ["--action", "merge-apply", "--spec-dir", str(spec_dir), "--json"]
    first = _run(mirror_engine, argv, repo)
    second = _run(mirror_engine, argv, repo)
    assert first.returncode == second.returncode == 2
    assert first.stdout == second.stdout, (
        "C-006: the same input MUST reproduce the same report (stable order)"
    )
    assert first.stderr == "" and second.stderr == ""


# ---------------------------------------------------------------------------
# C-007 — already-sealed is idempotent; no lock-file concurrency
# ---------------------------------------------------------------------------

def test_c007_engine_declares_no_lock_file_concurrency(source):
    tree = ast.parse(source)
    assert not (_import_roots(tree) & {"fcntl", "filelock", "portalocker"}), (
        "C-007: the engine MUST NOT depend on lock-file concurrency"
    )
    lock_names = {"flock", "lockf", "lockfile", "LockFile", "filelock"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id not in lock_names
        elif isinstance(node, ast.Attribute):
            assert node.attr not in lock_names


# ---------------------------------------------------------------------------
# C-008 — the write surface is allowlisted and statically auditable
# ---------------------------------------------------------------------------

def test_c008_write_path_allowlist_is_declared_and_closed(eng):
    assert tuple(eng.WRITE_PATH_ALLOWLIST) == (
        "{spec_dir}/seal.md",
        "{spec_dir}/merge-manifest.json",
        "{spec_dir}/{merged_artifact}",
        "{slice_dir}/requirements.md",
        "{factory_doc}",
    ), "C-008: the write-path allowlist is closed; a new entry is a contract change"


def test_c008_no_move_delete_rename_or_push_in_source(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            assert (func.value.id, func.attr) not in DESTRUCTIVE_MODULE_ATTRS, (
                f"C-008: destructive call {func.value.id}.{func.attr} MUST NOT exist"
            )
        if isinstance(func, ast.Attribute) and func.attr in DESTRUCTIVE_PATH_ATTRS:
            raise AssertionError(f"C-008: destructive call .{func.attr}() MUST NOT exist")
    for token in _call_arg_strings(tree):
        assert token not in ("push", "mv", "rm"), (
            f"C-008: the engine MUST NOT shell out to {token!r}"
        )
    assert not (_import_roots(tree) & {"sched"}), (
        "C-008: no scheduler loop belongs in the action table"
    )


def test_fr021_engine_is_stdlib_only(source):
    roots = _import_roots(ast.parse(source))
    assert roots <= ALLOWED_IMPORT_ROOTS, (
        f"FR-021: stdlib-only; unexpected imports {sorted(roots - ALLOWED_IMPORT_ROOTS)}"
    )


# ---------------------------------------------------------------------------
# C-009 — explicit paths only; the literal `.specify` component is the signal
# ---------------------------------------------------------------------------

def test_c009_mirror_copy_refuses_write_actions(engine, tmp_path):
    repo = tmp_path / "repo"
    mirror_engine = _install_copy(engine, repo / ".specify" / "scripts" / "python")
    spec_dir = _make_spec(repo)
    for action in WRITE_ACTIONS:
        proc = _run(mirror_engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], repo)
        assert proc.returncode == 2, (
            f"C-009: a mirror-copy write action exits 2; got {proc.returncode} for {action}"
        )
        payload = _payload(proc)
        assert MIRROR_CODE in _codes(payload), (
            f"C-009: the rejection names {MIRROR_CODE!r}; got {_codes(payload)!r}"
        )


def test_c009_read_actions_are_not_refused_by_the_mirror_guard(engine, tmp_path):
    repo = tmp_path / "repo"
    mirror_engine = _install_copy(engine, repo / ".specify" / "scripts" / "python")
    spec_dir = _make_spec(repo)
    for action in READ_ONLY_ACTIONS:
        proc = _run(mirror_engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], repo)
        payload = _payload(proc)
        assert MIRROR_CODE not in _codes(payload), (
            f"C-009: read action {action} runs from the mirror; it MUST NOT be refused "
            f"for {MIRROR_CODE!r}"
        )


def test_c009_an_ancestor_specify_is_not_the_mirror_signal(engine, tmp_path):
    """The worktree lives under `.specify/.tmp/...` — a literal component higher up
    the path MUST NOT trigger the mirror guard (the forbidden ancestor heuristic)."""
    repo = tmp_path / ".specify" / ".tmp" / "demo" / "repo"
    nested_engine = _install_copy(engine, repo / "scripts" / "python")
    spec_dir = _make_spec(repo)
    proc = _run(nested_engine, ["--action", "merge-apply", "--spec-dir", str(spec_dir), "--json"], repo)
    payload = _payload(proc)
    assert MIRROR_CODE not in _codes(payload), (
        "C-009: only the fixed mirror position is the signal; an ancestor `.specify` "
        "component MUST NOT be read as one"
    )


def test_c009_spec_dir_must_exist_and_contain_requirements(engine, tmp_path):
    absent = tmp_path / "no-such-spec"
    proc = _run(engine, ["--action", "merge-plan", "--spec-dir", str(absent), "--json"], tmp_path)
    assert proc.returncode == 2
    assert SPEC_DIR_CODE in _codes(_payload(proc))

    hollow = tmp_path / "hollow"
    hollow.mkdir()
    proc = _run(engine, ["--action", "merge-plan", "--spec-dir", str(hollow), "--json"], tmp_path)
    assert proc.returncode == 2
    assert SPEC_DIR_CODE in _codes(_payload(proc))


def test_c009_spec_dir_shape_is_not_a_numeric_prefix(engine, tmp_path):
    spec_dir = _make_spec(tmp_path, name="plain-fixture-spec")
    proc = _run(engine, ["--action", "merge-plan", "--spec-dir", str(spec_dir), "--json"], tmp_path)
    payload = _payload(proc)
    assert SPEC_DIR_CODE not in _codes(payload), (
        "C-009: spec-dir validation MUST NOT require a `^\\d{3}-` prefix"
    )


# ---------------------------------------------------------------------------
# C-010 — one judgment, two renderings; the machine form is stable
# ---------------------------------------------------------------------------

def test_c010_json_payload_is_canonical_and_matches_the_exit_code(engine, tmp_path):
    spec_dir = _make_spec(tmp_path)
    for action in ACTIONS:
        proc = _run(engine, ["--action", action, "--spec-dir", str(spec_dir), "--json"], tmp_path)
        payload = _payload(proc)
        canonical = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        assert proc.stdout == canonical, (
            f"C-010: {action} --json MUST be one stable JSON payload "
            "(indent=2, sort_keys=True, ensure_ascii=False)"
        )
        assert payload["verdict"] in VERDICT_TO_EXIT, (
            f"C-010: verdict {payload['verdict']!r} is outside the closed set"
        )
        assert VERDICT_TO_EXIT[payload["verdict"]] == proc.returncode == payload["exit_code"]


def test_c010_json_and_human_renderings_agree(engine, tmp_path):
    repo = tmp_path / "repo"
    mirror_engine = _install_copy(engine, repo / ".specify" / "scripts" / "python")
    spec_dir = _make_spec(repo)
    argv = ["--action", "seal", "--spec-dir", str(spec_dir)]
    human = _run(mirror_engine, argv, repo)
    machine = _run(mirror_engine, argv + ["--json"], repo)
    assert human.returncode == machine.returncode == 2
    payload = _payload(machine)
    assert _codes(payload), "the fixture path yields at least one condition"
    for condition in payload["conditions"]:
        assert condition["code"] in human.stdout, (
            f"C-010: condition {condition['code']!r} MUST appear in both renderings"
        )


def test_c010_json_payload_keeps_non_ascii_readable(engine, tmp_path):
    spec_dir = _make_spec(tmp_path, name="099-测试-spec")
    proc = _run(engine, ["--action", "merge-plan", "--spec-dir", str(spec_dir), "--json"], tmp_path)
    assert "测试" in proc.stdout, (
        "C-010: ensure_ascii=False keeps non-ASCII text readable in the payload"
    )


# ---------------------------------------------------------------------------
# 100 C-115 — the six-action CLI surface: labels, identity, rejection, no bypass
# ---------------------------------------------------------------------------

def test_c115_six_action_cli_consistency(eng, engine, tmp_path):
    spec_dir = _make_spec(tmp_path)
    before = _snapshot(tmp_path)

    help_proc = _run(engine, ["--help"], tmp_path)
    assert help_proc.returncode == 0, (
        f"C-115: --help MUST exit 0; got {help_proc.returncode}"
    )
    for action in ACTIONS:
        assert action in help_proc.stdout, (
            f"C-115: --help MUST list the six closed actions; {action!r} is missing"
        )
    declared = re.search(r"--action \{([^}]+)\}", help_proc.stdout)
    assert declared is not None, "C-115: --help MUST carry the --action choices"
    assert tuple(declared.group(1).split(",")) == ACTIONS, (
        "C-115: the declared choices are exactly the six closed actions in order"
    )

    version_proc = _run(engine, ["--version"], tmp_path)
    assert version_proc.returncode == 0, (
        f"C-115: --version MUST exit 0; got {version_proc.returncode}"
    )
    lines = [line for line in version_proc.stdout.strip().splitlines() if line.strip()]
    assert len(lines) == 1 and re.fullmatch(r"seal-utils\.py \S+", lines[0]), (
        f"C-115: --version prints exactly one identity line; got {lines!r}"
    )

    rejected = _run(engine, ["--action", "archive-plan", "--spec-dir", str(spec_dir),
                             "--force"], tmp_path)
    assert rejected.returncode == 2, (
        f"C-115: an undeclared option MUST be rejected with 2; got {rejected.returncode}"
    )

    options = {opt for a in eng.build_parser()._actions for opt in a.option_strings}
    for flag in FORBIDDEN_FLAGS:
        assert flag not in options, f"C-115: bypass flag {flag} MUST NOT exist"

    assert _snapshot(tmp_path) == before, (
        "C-115: --help / --version / a rejected option MUST NOT touch the workspace"
    )
