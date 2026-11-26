"""Scope guards: closed carrier set, one contract, zero second mechanism (US4 / T026).

Rule owner: ``shared/definitions/superagent-definitions.md`` § Termination. Pinning
clauses: ``contracts/carrier-conformance.contract.md`` C-22 (closed inventory, no second
value table / evidence matrix / carrier-private judgment copy) and C-24 (zero second
mechanism); ``contracts/enforcement-and-migration.contract.md`` C-25 (read-only judgment
face) and C-30 (the guard itself can go red — the meta-mutation record lives in
``test-evidence/mutation-drill.md``).

What this pins

* the carrier inventory is exactly C1…C6 in both the owner page and ``data-model.md`` E8,
  and every C-ID is referenced by at least one test in this settlement test set;
* the engine reads only the four attempt-writing carriers (C5/C6 contribute no reader);
* no declaration surface carries a second settlement value *table* (the owner page is the
  only one); Python defines the value set / classes / violation kinds exactly once;
* the engine's import set, call set and CLI option surface add no scheduler, store,
  queue, notification channel or child list — no write, non-zero kill, retry, delete or
  push authority (AST scan);
* ``dispatch.sh`` writes its additive records only inside the existing ``${LOG_DIR}``;
* ``probe-definitions.md`` gains no probe class and the observer stays optional.
"""

from __future__ import annotations

import ast
import importlib.util
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"
DATA_MODEL = (
    REPO_ROOT / ".specify" / "specs" / "106-background-silent-failure" / "data-model.md"
)
ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
DISPATCH = REPO_ROOT / "skills" / "internal" / "create-team" / "scripts" / "dispatch.sh"
PROBE_DEFS = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
TESTS_DIR = REPO_ROOT / "tests" / "contract"

CLOSED_CARRIERS = {"C1", "C2", "C3", "C4", "C5", "C6"}
SETTLEMENT_VALUES = (
    "completed",
    "failed",
    "anomaly",
    "cancelled",
    "running",
    "silent-end",
    "unknown",
)
DECLARATION_SURFACES = ("shared", "skills", "templates", "agents", "docs")
ENGINE_ALLOWED_IMPORTS = {
    "__future__",
    "argparse",
    "collections",
    "datetime",
    "importlib",
    "json",
    "os",
    "pathlib",
    "re",
    "sys",
    "time",
}
DESTRUCTIVE_ATTRS = {
    "write_text",
    "write_bytes",
    "unlink",
    "mkdir",
    "touch",
    "rmdir",
    "chmod",
    "rename",
    "replace",
    "symlink_to",
    "hardlink_to",
}
DESTRUCTIVE_OS = {
    "remove",
    "unlink",
    "rename",
    "replace",
    "rmdir",
    "removedirs",
    "makedirs",
    "mkdir",
    "chmod",
    "system",
    "popen",
    "fork",
    "forkpty",
    "execv",
    "execve",
    "spawnv",
}
ENGINE_CLI_OPTIONS = {
    "-h",
    "--help",
    "--version",
    "--action",
    "--parent",
    "--child",
    "--state-dir",
    "--teams-dir",
    "--logs-dir",
    "--registry-dir",
    "--live-window",
    "--wait-deadline",
    "--start-grace",
    "--format",
}


def _read(path: Path) -> str:
    assert path.is_file(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec and spec.loader, f"module not loadable: {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _table_ids(text: str, marker: str) -> set:
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.startswith(marker)]
    assert starts, f"carrier table section missing: {marker}"
    ids = set()
    for line in lines[starts[0] + 1 :]:
        if line.startswith("## ") or line.startswith("### "):
            break
        match = re.match(r"^\|\s*(C\d+)\s*\|", line)
        if match:
            ids.add(match.group(1))
    return ids


# --------------------------------------------------------------------------- #
# closed inventory C1…C6
# --------------------------------------------------------------------------- #
def test_carrier_inventory_is_closed_at_c1_to_c6():
    assert _table_ids(_read(OWNER), "### Carrier Evidence") == CLOSED_CARRIERS
    assert _table_ids(_read(DATA_MODEL), "## E8 ") == CLOSED_CARRIERS


def test_every_carrier_id_is_referenced_by_at_least_one_settlement_test():
    names = []
    for path in sorted(TESTS_DIR.glob("test_settlement_*.py")):
        names.extend(re.findall(r"def (test_[a-z0-9_]+)\(", _read(path)))
    missing = []
    for carrier in sorted(CLOSED_CARRIERS):
        number = carrier[1:]
        if not any(re.search(r"c%s[^0-9]" % number, name) for name in names):
            missing.append(carrier)
    assert not missing, f"carrier IDs with no referencing test: {missing}"


def test_the_engine_reads_only_the_four_attempt_writing_carriers():
    engine = _load_module("role_edge_scope", ENGINE)
    assert engine.SETTLE_CARRIERS == (
        "c1-fork",
        "c2-subprocess",
        "c3-team-seat",
        "c4-native",
    )
    text = _read(ENGINE)
    assert '"c5-' not in text and '"c6-' not in text, (
        "C5/C6 write no attempt record and must contribute no direct reader"
    )


# --------------------------------------------------------------------------- #
# no second value table / evidence matrix / carrier-private judgment copy
# --------------------------------------------------------------------------- #
def _value_tables(text: str) -> list:
    offenders = []
    for block in re.findall(r"(?m)(?:^\|.*\|\s*$\n?)+", text):
        present = {value for value in SETTLEMENT_VALUES if f"`{value}`" in block}
        if len(present) >= 4:
            offenders.append(sorted(present))
    return offenders


def test_no_second_settlement_value_table_on_declaration_surfaces():
    offenders = []
    for surface in DECLARATION_SURFACES:
        root = REPO_ROOT / surface
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.resolve() == OWNER.resolve():
                continue
            tables = _value_tables(_read(path))
            if tables:
                offenders.append((path.relative_to(REPO_ROOT).as_posix(), tables))
    assert not offenders, (
        f"a second settlement value table exists outside the owner page: {offenders}"
    )


def test_value_set_classes_and_violation_kinds_have_one_definition_point():
    definitions = []
    for root_name in ("scripts", "src", "skills"):
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            text = _read(path)
            if re.search(r"(?m)^SETTLEMENT_(VALUES|CLASSES|VIOLATION_KINDS)\s*=", text):
                definitions.append(path.relative_to(REPO_ROOT).as_posix())
    assert definitions == ["scripts/python/role-edge-check.py"], definitions


# --------------------------------------------------------------------------- #
# zero second mechanism — engine AST surface
# --------------------------------------------------------------------------- #
def test_engine_imports_stay_within_the_read_only_allowlist():
    tree = ast.parse(_read(ENGINE))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    assert modules <= ENGINE_ALLOWED_IMPORTS, modules - ENGINE_ALLOWED_IMPORTS


def test_engine_has_no_write_kill_retry_delete_or_push_call():
    tree = ast.parse(_read(ENGINE))
    banned = []
    kill_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute):
            owner = func.value.id if isinstance(func.value, ast.Name) else None
            if owner == "os" and func.attr == "kill":
                signal_arg = node.args[1] if len(node.args) >= 2 else None
                kill_calls.append(signal_arg)
                if not (
                    isinstance(signal_arg, ast.Constant) and signal_arg.value == 0
                ):
                    banned.append("os.kill with a non-zero signal")
                continue
            if owner == "os" and func.attr in DESTRUCTIVE_OS:
                banned.append("os.%s" % func.attr)
            elif func.attr in DESTRUCTIVE_ATTRS:
                banned.append(".%s(" % func.attr)
        elif isinstance(func, ast.Name) and func.id == "open":
            mode = node.args[1] if len(node.args) >= 2 else None
            if isinstance(mode, ast.Constant) and isinstance(mode.value, str):
                if set(mode.value) & set("wax+"):
                    banned.append("open(mode=%r)" % mode.value)
    assert not banned, f"the engine gained destructive authority: {banned}"
    assert kill_calls, "the liveness probe disappeared; expected one os.kill(pid, 0)"


def test_engine_cli_surface_adds_no_storage_root_or_channel():
    engine = _load_module("role_edge_scope_cli", ENGINE)
    parser = engine.build_parser()
    options = {option for action in parser._actions for option in action.option_strings}
    assert options == ENGINE_CLI_OPTIONS, options ^ ENGINE_CLI_OPTIONS


def test_dispatch_sh_writes_settlement_records_only_inside_the_existing_log_dir():
    text = _read(DISPATCH)
    assert text.count("mkdir -p") == 1, "a second storage root appeared in dispatch.sh"
    for line in text.splitlines():
        if "mkdir -p" in line:
            assert 'mkdir -p "${LOG_DIR}"' in line, line
    for suffix in (".attempt", ".end"):
        assert '"${LOG_DIR}/${LABEL}%s"' % suffix in text, (
            f"the additive {suffix} record left the existing log dir"
        )


def test_no_new_probe_class_or_observer_dependency():
    probe = _read(PROBE_DEFS).lower()
    for token in ("settlement", "silent-end"):
        assert token not in probe, f"a probe class grew out of the settlement contract: {token}"
    owner = _read(OWNER)
    assert "MUST NOT be the only settlement carrier" in owner
    assert "a line without an observer still settles" in owner
