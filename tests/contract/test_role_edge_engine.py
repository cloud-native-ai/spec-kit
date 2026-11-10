"""Contract tests: the read-only role-edge judgement engine (Feature 095, T011 / T029).

Rule owner: ``shared/definitions/superagent-definitions.md`` ([[STR-004]]). Executable
interface: ``contracts/role-edge-engine.contract.md`` C-1…C-11.

What this pins (US1 / T011)

* C-1/C-2 — the CLI surface (``--action report|query``, the four roots, ``--format``,
  ``--help`` / ``--version``, undeclared-option rejection) and the closed exit codes,
  including the required-vs-optional root split (``--registry-dir`` may be absent).
* C-3/C-4 — the report and query schemas, including ``executors[].role_set_marker``
  (``"dual-role"`` on A, ``null`` elsewhere) and the two distinct unresolvable-identity
  behaviours (record-side → ``dangling-parent``; queried identity → exit 2).
* C-5 — the closed four-kind violation set.
* C-6 — zero write points, asserted structurally (AST scan) and behaviourally (the
  fixture tree is byte-identical after a run).
* C-7 — determinism (two consecutive runs are byte-identical).
* C-8 — a conflict row names the field, both paths and the edge identity.
* C-9 — strict input: an unknown value inside a known table is a named ``2``; the
  declared-role value ``superagent`` is known input, never malformed.
* C-11 — the three mutation drills: type-based classification red, an injected
  violation red, and an explicit ``superagent`` assertion with no parenthood red while
  a ``dispatch_duty: granted`` declaration without children stays green.

US3 / T029 appends the three real forms' direction and depth assertions plus the
direction-reversal mutation at the bottom of this file.

Red-first (Constitution IV): at T011 neither the engine nor the fixture set exists, so
every leg fails on its own named missing-artifact assertion — never on an import or
collection error. The engine is loaded lazily only where its importable interface is
the subject.
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
ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
ENGINE_MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "role-edge-check.py"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "superagent-role"

CLOSED_VIOLATION_KINDS = {
    "self-dispatch",
    "dangling-parent",
    "unbacked-role-claim",
    "depth-inconsistent",
}
REPORT_KEYS = {
    "schema_version",
    "action",
    "inputs",
    "roots",
    "executors",
    "edges",
    "violations",
    "conflicts",
    "summary",
}
EXECUTOR_KEYS = {"id", "parent", "roles", "role_set_marker", "depth", "sources"}
EDGE_KEYS = {
    "parent",
    "child",
    "attempt",
    "role_declaration",
    "dispatch_duty",
    "depth",
    "source",
}
QUERY_KEYS = {
    "schema_version",
    "action",
    "edge_exists",
    "edge",
    "parent",
    "child",
    "violations",
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _engine() -> Path:
    assert ENGINE.is_file(), (
        "engine missing: scripts/python/role-edge-check.py (T015)"
    )
    return ENGINE


def _fixture(name: str) -> Path:
    base = FIXTURE_ROOT / name
    assert base.is_dir(), f"fixture missing: tests/fixtures/superagent-role/{name}"
    for part in ("state", "teams", "logs", "registry"):
        assert (base / part).is_dir(), f"fixture root missing: {name}/{part}"
    return base


def _roots(name: str, registry: bool = True) -> list:
    base = _fixture(name)
    args = [
        "--state-dir",
        str(base / "state"),
        "--teams-dir",
        str(base / "teams"),
        "--logs-dir",
        str(base / "logs"),
    ]
    if registry:
        args += ["--registry-dir", str(base / "registry")]
    return args


def run_engine(*args) -> subprocess.CompletedProcess:
    engine = _engine()
    return subprocess.run(
        [sys.executable, str(engine)] + [str(item) for item in args],
        capture_output=True,
        text=True,
        timeout=180,
    )


def _report(name: str, registry: bool = True) -> tuple:
    proc = run_engine("--action", "report", *_roots(name, registry))
    model = json.loads(proc.stdout) if proc.stdout.strip() else None
    return proc, model


def _executors(model: dict) -> dict:
    return {entry["id"]: entry for entry in model["executors"]}


def _load_engine():
    engine = _engine()
    spec = importlib.util.spec_from_file_location(
        "role_edge_check_under_test", str(engine)
    )
    assert spec and spec.loader, "engine not loadable via importlib file location"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pyproject_version() -> str:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    assert match, "pyproject.toml carries no version field"
    return match.group(1)


def _tree_hashes(root: Path) -> dict:
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return hashes


def _copy_fixture(name: str, tmp_path: Path) -> Path:
    base = _fixture(name)
    target = tmp_path / name.replace("/", "-")
    shutil.copytree(base, target)
    return target


def _run_on_base(base: Path, *extra) -> subprocess.CompletedProcess:
    args = [
        "--state-dir",
        str(base / "state"),
        "--teams-dir",
        str(base / "teams"),
        "--logs-dir",
        str(base / "logs"),
        "--registry-dir",
        str(base / "registry"),
    ]
    return run_engine("--action", "report", *args, *extra)


def _write_mapping_report(base: Path, slug: str, stamp: str, rows: list) -> Path:
    runs = base / "teams" / slug / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    path = runs / f"{stamp}-report.md"
    body = [
        "# Team Run Report: fixture",
        "",
        "## Execution Detail",
        "",
        "| label | role | dispatch_duty | workspace | parent |",
        "|-------|------|---------------|-----------|--------|",
    ]
    for row in rows:
        body.append("| " + " | ".join(str(cell) for cell in row) + " |")
    body.append("")
    path.write_text("\n".join(body), encoding="utf-8")
    return path


def _write_registry_entry(base: Path, line_id: str) -> Path:
    directory = base / "registry"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{line_id}.json"
    path.write_text(
        json.dumps({"schema_version": 1, "line_id": line_id, "run_id": f"r-{line_id}"}),
        encoding="utf-8",
    )
    return path


# --------------------------------------------------------------------------- #
# C-1 / C-2 / XXI — CLI surface and exit codes
# --------------------------------------------------------------------------- #
def test_help_version_and_undeclared_option():
    """C-1: help carries the four labels, version has one line, unknown option is a 2."""
    help_proc = run_engine("--help")
    assert help_proc.returncode == 0, help_proc.stderr
    body = help_proc.stdout
    assert "usage:" in body.lower(), "help must state the usage form"
    assert "--action" in body, "help must list the recognized options"
    assert "Side effects:" in body, "help must state whether the script has side effects"
    assert "Exit codes:" in body, "help must state the exit-code meanings"

    short = run_engine("-h")
    assert short.returncode == 0
    assert short.stdout == body, "-h and --help must produce the same body"

    version = run_engine("--version")
    assert version.returncode == 0
    lines = version.stdout.strip().splitlines()
    assert len(lines) == 1, f"--version must print exactly one line, got {lines!r}"
    name, _, value = lines[0].partition(" ")
    assert name == "role-edge-check.py"
    assert value == _pyproject_version(), (
        "--version must read the framework version from pyproject.toml at run time"
    )

    bad = run_engine("--no-such-option")
    assert bad.returncode == 2, bad.stderr
    assert bad.stdout == "", "an undeclared option must not reach the action"
    assert "unrecognized" in bad.stderr.lower() or "invalid" in bad.stderr.lower()


def test_required_roots_fatal_and_registry_optional(tmp_path):
    """C-2: the three primary roots are required; the registry root is cross-check only."""
    base = _copy_fixture("empty", tmp_path)
    for option, part in (
        ("--state-dir", "state"),
        ("--teams-dir", "teams"),
        ("--logs-dir", "logs"),
    ):
        args = [
            "--state-dir",
            str(base / "state"),
            "--teams-dir",
            str(base / "teams"),
            "--logs-dir",
            str(base / "logs"),
        ]
        missing = base / ("missing-" + part)
        index = args.index(option)
        args[index + 1] = str(missing)
        proc = run_engine("--action", "report", *args)
        assert proc.returncode == 2, (option, proc.stdout, proc.stderr)
        assert option in proc.stderr, proc.stderr
        assert str(missing) in proc.stderr, proc.stderr

    proc, model = _report_on_base_without_registry(base)
    assert proc.returncode == 0, proc.stderr
    assert model["inputs"]["registry"] == "absent", model["inputs"]
    assert model["summary"]["edges"] == 0


def test_mirror_copy_answers_help_and_version():
    """The runtime mirror carries the same interface (T017: pair parity is pinned here)."""
    assert ENGINE_MIRROR.is_file(), (
        "engine mirror missing: .specify/scripts/python/role-edge-check.py (T017)"
    )
    version = subprocess.run(
        [sys.executable, str(ENGINE_MIRROR), "--version"],
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert version.returncode == 0, version.stderr
    lines = version.stdout.strip().splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("role-edge-check.py "), lines

    help_proc = subprocess.run(
        [sys.executable, str(ENGINE_MIRROR), "--help"],
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert help_proc.returncode == 0, help_proc.stderr
    assert "--action" in help_proc.stdout
    assert ENGINE_MIRROR.read_bytes() == ENGINE.read_bytes(), (
        "the mirror copy must be byte-identical to the engine source"
    )


def _report_on_base_without_registry(base: Path) -> tuple:
    args = [
        "--action",
        "report",
        "--state-dir",
        str(base / "state"),
        "--teams-dir",
        str(base / "teams"),
        "--logs-dir",
        str(base / "logs"),
        "--registry-dir",
        str(base / "no-such-registry"),
    ]
    proc = run_engine(*args)
    model = json.loads(proc.stdout) if proc.stdout.strip() else None
    return proc, model


# --------------------------------------------------------------------------- #
# C-3 — the report schema over the clean chain
# --------------------------------------------------------------------------- #
def test_report_schema_clean_chain():
    """root→A→B: two edges, A is dual-role at depth 1, B depth 2, no violations."""
    proc, model = _report("root-a-b")
    assert proc.returncode == 0, proc.stderr
    assert model is not None
    assert REPORT_KEYS <= set(model), sorted(model)
    assert model["schema_version"] == 1
    assert model["action"] == "report"

    executors = _executors(model)
    assert set(executors) == {"root", "A", "B"}, sorted(executors)
    for entry in model["executors"]:
        assert set(entry) == EXECUTOR_KEYS, sorted(entry)

    assert executors["root"]["roles"] == ["superagent"]
    assert executors["root"]["role_set_marker"] is None
    assert executors["root"]["depth"] == 0
    assert executors["root"]["parent"] is None

    assert executors["A"]["roles"] == ["subagent", "superagent"]
    assert executors["A"]["role_set_marker"] == "dual-role"
    assert executors["A"]["depth"] == 1
    assert executors["A"]["parent"] == "root"

    assert executors["B"]["roles"] == ["subagent"]
    assert executors["B"]["role_set_marker"] is None
    assert executors["B"]["depth"] == 2
    assert executors["B"]["parent"] == "A"

    identities = [(e["parent"], e["child"], e["attempt"]) for e in model["edges"]]
    assert identities == sorted(identities), "edges must sort by (parent, child, attempt)"
    assert set(identities) == {("root", "A", "1"), ("A", "B", "1")}, identities
    for edge in model["edges"]:
        assert set(edge) == EDGE_KEYS, sorted(edge)
        assert edge["role_declaration"] in ("subagent", "superagent")
        assert edge["dispatch_duty"] in ("granted", "not-granted")
        assert edge["source"]["carrier"] in (
            "team-report",
            "driver-spine",
            "run-agent-label",
        )

    edge_a = next(e for e in model["edges"] if e["child"] == "A")
    assert edge_a["role_declaration"] == "superagent"
    assert edge_a["dispatch_duty"] == "granted"
    assert edge_a["depth"] == 1
    assert edge_a["source"]["carrier"] == "team-report"
    assert str(edge_a["source"]["path"]).endswith("20261110T000000Z-report.md")

    edge_b = next(e for e in model["edges"] if e["child"] == "B")
    assert edge_b["depth"] == 2
    assert edge_b["source"]["carrier"] == "driver-spine"

    assert model["violations"] == []
    assert model["conflicts"] == []
    summary = model["summary"]
    assert summary == {
        "edges": len(model["edges"]),
        "executors": len(model["executors"]),
        "violations": 0,
        "conflicts": 0,
    }
    assert model["roots"] == ["root"]


def test_importable_interface_matches_report():
    """C-1: report ≡ evaluate_role_model(read_carrier_inputs(...))."""
    module = _load_engine()
    base = _fixture("root-a-b")
    inputs = module.read_carrier_inputs(
        state_dir=base / "state",
        teams_dir=base / "teams",
        logs_dir=base / "logs",
        registry_dir=base / "registry",
    )
    model = module.evaluate_role_model(inputs)
    proc = run_engine("--action", "report", *_roots("root-a-b"))
    assert proc.returncode == 0, proc.stderr
    assert model == json.loads(proc.stdout)


# --------------------------------------------------------------------------- #
# C-4 — pair query and the two unresolvable-identity behaviours
# --------------------------------------------------------------------------- #
def test_query_pair_and_unresolvable_identities():
    """A known pair answers boolean existence; an unknown queried identity is a 2."""
    proc = run_engine(
        "--action", "query", "--parent", "root", "--child", "A", *_roots("root-a-b")
    )
    assert proc.returncode == 0, proc.stderr
    answer = json.loads(proc.stdout)
    assert QUERY_KEYS <= set(answer), sorted(answer)
    assert answer["action"] == "query"
    assert answer["edge_exists"] is True
    assert answer["edge"] is not None
    assert answer["child"]["role_set_marker"] == "dual-role"
    assert answer["child"]["depth"] == 1
    assert answer["parent"]["id"] == "root"
    assert answer["parent"]["depth"] == 0

    absent = run_engine(
        "--action", "query", "--parent", "root", "--child", "B", *_roots("root-a-b")
    )
    assert absent.returncode == 0, absent.stderr
    payload = json.loads(absent.stdout)
    assert payload["edge_exists"] is False
    assert payload["edge"] is None
    assert payload["child"]["id"] == "B"

    unknown = run_engine(
        "--action", "query", "--parent", "root", "--child", "nobody", *_roots("root-a-b")
    )
    assert unknown.returncode == 2, unknown.stderr
    assert "--child" in unknown.stderr
    assert "nobody" in unknown.stderr

    incomplete = run_engine("--action", "query", *_roots("root-a-b"))
    assert incomplete.returncode == 2, incomplete.stderr


# --------------------------------------------------------------------------- #
# C-5 — the closed violation set, one fixture per kind
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "fixture,kind",
    [
        ("violations/self-dispatch", "self-dispatch"),
        ("violations/dangling-parent", "dangling-parent"),
        ("violations/unbacked-claim", "unbacked-role-claim"),
        ("violations/depth-cycle", "depth-inconsistent"),
    ],
)
def test_violation_fixtures_each_kind_in_isolation(fixture, kind):
    proc, model = _report(fixture)
    assert proc.returncode == 1, (proc.stdout, proc.stderr)
    kinds = {row["kind"] for row in model["violations"]}
    assert kinds == {kind}, kinds
    for row in model["violations"]:
        assert row["kind"] in CLOSED_VIOLATION_KINDS
        assert row["subjects"], row
        assert row["paths"], row
        assert set(row) == {"kind", "subjects", "paths"}, sorted(row)


def test_dangling_parent_names_both_sides_and_the_path():
    proc, model = _report("violations/dangling-parent")
    assert proc.returncode == 1
    row = model["violations"][0]
    assert "ghost" in row["subjects"], row
    assert "orphan" in row["subjects"], row
    assert any(str(path).endswith("-report.md") for path in row["paths"]), row


# --------------------------------------------------------------------------- #
# C-8 — conflicts name the field, both paths and the edge identity
# --------------------------------------------------------------------------- #
def test_conflict_rows_name_both_paths_and_edge_identity():
    proc, model = _report("conflict")
    assert proc.returncode == 0, proc.stderr
    assert model["violations"] == []
    conflicts = model["conflicts"]
    assert len(conflicts) == 1, conflicts
    row = conflicts[0]
    assert set(row) == {"field", "paths", "edge"}, sorted(row)
    assert row["field"] == "dispatch_duty"
    assert len(row["paths"]) >= 2
    assert len(set(row["paths"])) == len(row["paths"])
    assert row["edge"] == {"parent": "root", "child": "C1", "attempt": "1"}


# --------------------------------------------------------------------------- #
# C-9 — strict input
# --------------------------------------------------------------------------- #
def test_malformed_value_is_named_and_exits_two():
    proc, model = _report("malformed")
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    assert model is None
    assert "malformed" in proc.stderr.lower()
    assert "-report.md" in proc.stderr
    assert "role" in proc.stderr


def test_malformed_row_shape_is_named_and_exits_two(tmp_path):
    base = _copy_fixture("root-a-b", tmp_path)
    path = base / "teams" / "broken" / "runs" / "20261110T050000Z-report.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "\n".join(
            [
                "# Team Run Report: fixture",
                "",
                "## Execution Detail",
                "",
                "| label | role | dispatch_duty | workspace | parent |",
                "|-------|------|---------------|-----------|--------|",
                "| short | subagent | granted |",
                "",
            ]
        ),
        encoding="utf-8",
    )
    proc = _run_on_base(base)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    assert "columns" in proc.stderr.lower()
    assert "-report.md" in proc.stderr


def test_empty_set_is_explicit_and_clean():
    proc, model = _report("empty")
    assert proc.returncode == 0, proc.stderr
    assert model["summary"]["edges"] == 0
    assert model["edges"] == []
    assert model["executors"] == []
    assert model["violations"] == []
    assert model["conflicts"] == []
    assert model["roots"] == []


# --------------------------------------------------------------------------- #
# C-6 — zero write points, structural and behavioural
# --------------------------------------------------------------------------- #
def test_engine_has_zero_write_points_in_source():
    source = _engine().read_text(encoding="utf-8")
    tree = ast.parse(source)
    write_calls = {
        "write_text",
        "write_bytes",
        "mkdir",
        "makedirs",
        "unlink",
        "rmdir",
        "rename",
        "replace",
        "remove",
        "rmtree",
        "copy",
        "copyfile",
        "copytree",
        "move",
        "touch",
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
        assert name not in write_calls, f"write-capable call in engine: {name}"
        if name == "open":
            mode = None
            if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                mode = node.args[1].value
            for keyword in node.keywords:
                if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
                    mode = keyword.value.value
            assert mode is None or isinstance(mode, str)
            assert not mode or not any(flag in mode for flag in "wax+"), (
                f"write-mode open in engine: {mode!r}"
            )
    assert "tempfile" not in source, "the engine must not create temporary files"


def test_fixture_tree_is_byte_identical_after_a_run():
    before = _tree_hashes(FIXTURE_ROOT)
    proc, _model = _report("root-a-b")
    assert proc.returncode == 0, proc.stderr
    after = _tree_hashes(FIXTURE_ROOT)
    assert before == after, "the engine wrote into the fixture tree"


# --------------------------------------------------------------------------- #
# C-7 — determinism
# --------------------------------------------------------------------------- #
def test_two_runs_are_byte_identical():
    first = run_engine("--action", "report", *_roots("root-a-b"))
    second = run_engine("--action", "report", *_roots("root-a-b"))
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    text_first = run_engine("--action", "report", "--format", "text", *_roots("root-a-b"))
    text_second = run_engine(
        "--action", "report", "--format", "text", *_roots("root-a-b")
    )
    assert text_first.stdout == text_second.stdout
    assert "summary edges=" in text_first.stdout, "text output must summarize the set"


# --------------------------------------------------------------------------- #
# C-11 — the three mutation drills
# --------------------------------------------------------------------------- #
def test_mutation_type_based_classification_turns_red():
    """A classifier that assigns roles by executor type contradicts the pinned answer."""
    module = _load_engine()
    base = _fixture("root-a-b")
    kwargs = dict(
        state_dir=base / "state",
        teams_dir=base / "teams",
        logs_dir=base / "logs",
        registry_dir=base / "registry",
    )
    pinned = module.evaluate_role_model(module.read_carrier_inputs(**kwargs))
    assert _executors(pinned)["A"]["roles"] == ["subagent", "superagent"]
    assert _executors(pinned)["A"]["role_set_marker"] == "dual-role"

    original = module._roles_for
    try:
        module._roles_for = lambda is_parent, is_child: ["subagent"]
        mutated = module.evaluate_role_model(module.read_carrier_inputs(**kwargs))
    finally:
        module._roles_for = original

    entry_a = _executors(mutated)["A"]
    assert entry_a["roles"] == ["subagent"]
    assert entry_a["role_set_marker"] is None
    assert (entry_a["roles"], entry_a["role_set_marker"]) != (
        ["subagent", "superagent"],
        "dual-role",
    )


def test_mutation_injected_violation_turns_red(tmp_path):
    """An injected dangling-parent row flips a clean tree to exit 1."""
    base = _copy_fixture("root-a-b", tmp_path)
    _write_mapping_report(
        base,
        "injected",
        "20261110T030000Z",
        [("ghost-child", "subagent", "not-granted", "work/ghost-child", "no-such-parent")],
    )
    proc = _run_on_base(base)
    assert proc.returncode == 1, (proc.stdout, proc.stderr)
    model = json.loads(proc.stdout)
    kinds = {row["kind"] for row in model["violations"]}
    assert "dangling-parent" in kinds, kinds
    dangling = [row for row in model["violations"] if row["kind"] == "dangling-parent"]
    assert any("no-such-parent" in row["subjects"] for row in dangling)


def test_unbacked_superagent_claim_red_and_granted_without_children_green(tmp_path):
    proc, model = _report("violations/unbacked-claim")
    assert proc.returncode == 1
    assert {row["kind"] for row in model["violations"]} == {"unbacked-role-claim"}

    base = _copy_fixture("empty", tmp_path)
    _write_mapping_report(
        base,
        "granted",
        "20261110T000000Z",
        [("G", "subagent", "granted", "work/G", "root")],
    )
    legal = _run_on_base(base)
    assert legal.returncode == 0, (legal.stdout, legal.stderr)
    payload = json.loads(legal.stdout)
    assert payload["violations"] == []
    executor = _executors(payload)["G"]
    assert executor["roles"] == ["subagent"]
    assert payload["summary"]["edges"] == 1


# --------------------------------------------------------------------------- #
# US3 / T029 — the three real forms: direction, depth and the reversal drill
# --------------------------------------------------------------------------- #
def test_three_forms_local_team():
    """Local qodercli as root; the team members as its children (root→member only)."""
    proc, model = _report("local-team")
    assert proc.returncode == 0, proc.stderr
    assert model["summary"]["edges"] == 3
    executors = _executors(model)
    assert set(executors) == {"root", "alice", "bob", "carol"}
    assert executors["root"]["depth"] == 0
    assert executors["root"]["roles"] == ["superagent"]
    for member in ("alice", "bob", "carol"):
        assert executors[member]["depth"] == 1, member
        assert executors[member]["parent"] == "root", member
        assert executors[member]["roles"] == ["subagent"], member
    assert {edge["parent"] for edge in model["edges"]} == {"root"}
    assert model["violations"] == []


def test_three_forms_remote_topology():
    """Desktop session as root; the remote qodercli execution as its subagent."""
    proc, model = _report("remote-topology")
    assert proc.returncode == 0, proc.stderr
    assert model["summary"]["edges"] == 1
    edge = model["edges"][0]
    assert edge["parent"] == "remote-builder"
    assert edge["child"] == "remote--20261110T000000Z--worker"
    assert edge["source"]["carrier"] == "run-agent-label"
    assert edge["role_declaration"] == "subagent"
    assert edge["dispatch_duty"] == "not-granted"
    executors = _executors(model)
    assert executors["remote-builder"]["depth"] == 0
    assert executors[edge["child"]]["depth"] == 1
    assert executors[edge["child"]]["parent"] == "remote-builder"
    assert model["violations"] == []


def test_three_forms_fanout_10():
    """A is a subagent of root and the superagent of ten children; depths 0 / 1 / 2."""
    proc, model = _report("fanout-10")
    assert proc.returncode == 0, proc.stderr
    assert model["summary"]["edges"] == 11
    executors = _executors(model)
    children = {"child-%02d" % index for index in range(1, 11)}
    assert set(executors) == {"root", "A"} | children
    assert executors["root"]["depth"] == 0
    assert executors["A"]["depth"] == 1
    assert executors["A"]["role_set_marker"] == "dual-role"
    for child in children:
        assert executors[child]["depth"] == 2, child
        assert executors[child]["parent"] == "A", child
        assert executors[child]["roles"] == ["subagent"], child
    a_edges = [edge for edge in model["edges"] if edge["parent"] == "A"]
    assert len(a_edges) == 10
    assert {edge["child"] for edge in a_edges} == children
    assert model["violations"] == []


def test_three_forms_direction_reversal_turns_red(tmp_path):
    """Reversing root and A on the fan-out edge breaks the pinned direction and depths."""
    base = _copy_fixture("fanout-10", tmp_path)
    _write_registry_entry(base, "A")
    report_path = next((base / "teams").glob("*/runs/*-report.md"))
    text = report_path.read_text(encoding="utf-8")
    reversed_text = text.replace(
        "| A | superagent | granted | work/A | root |",
        "| root | subagent | granted | work/root | A |",
    )
    assert reversed_text != text, "the A row is missing from the fixture report"
    report_path.write_text(reversed_text, encoding="utf-8")

    proc = _run_on_base(base)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    executors = _executors(json.loads(proc.stdout))
    assert executors["A"]["depth"] == 0
    assert executors["A"]["parent"] is None
    assert executors["root"]["depth"] == 1
    assert executors["root"]["parent"] == "A"
    # the pinned orientation (root depth 0, A depth 1) is red under the reversal
    assert (executors["root"]["depth"], executors["A"]["depth"]) != (0, 1)
