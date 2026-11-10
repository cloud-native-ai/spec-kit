"""Contract test: zero second mechanism (095 T041).

Owner of the design contract: ``.specify/specs/095-superagent-role/contracts/harness-landing.contract.md``
C-3 (the six structural assertions) and C-5 (this module is the audit). The audit is a test,
not a prose claim: it classifies the feature's declared change set and scans the new/changed
sources, so a second persistence root, registry, renderer or dispatcher — or a write point on
the judgement face — turns it red. Each leg carries a seeded mutation proving the check is
not blind (the repository's blind-check lesson: a check that cannot be shown to fail proves
nothing).

The change-set inventory below is the audit subject. It lists the authored files only —
generated mirrors of the five skill surfaces are covered by the mirror-parity suite and are
not restated here. The one new directory set is declarative test data under
``tests/fixtures/superagent-role/``; fixture-internal ``state/`` / ``registry/`` / ``logs/``
segments are test data, never runtime roots.

Red-first (Constitution IV): authored before T042 adds the template pointer section, so the
owner-rules leg fails on its own "section missing" assertion — never on an import error.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
ENGINE_MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "role-edge-check.py"
DIGEST = REPO_ROOT / "scripts" / "python" / "status-digest.py"
OWNER = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"

OWNER_POINTER = ".specify/shared/definitions/superagent-definitions.md"
SECTION_HEADING = "## Super Agent (相对逻辑角色)"

#: Authored change set: (category, repo-relative path). Categories are the C-3 vocabulary.
CHANGE_SET = (
    ("engine", "scripts/python/role-edge-check.py"),
    ("engine-mirror", ".specify/scripts/python/role-edge-check.py"),
    ("digest", "scripts/python/status-digest.py"),
    ("digest-mirror", ".specify/scripts/python/status-digest.py"),
    ("owner", "shared/definitions/superagent-definitions.md"),
    ("owner-mirror", ".specify/shared/definitions/superagent-definitions.md"),
    ("pointer", "shared/definitions/agent-definitions.md"),
    ("pointer", "shared/definitions/subagent-definitions.md"),
    ("pointer", "shared/definitions/framework-map.md"),
    ("template", "templates/instructions-template.md"),
    ("live", ".specify/instructions.md"),
    ("skill", "skills/internal/run-agent/SKILL.md"),
    ("skill", "skills/internal/create-team/SKILL.md"),
    ("skill", "skills/internal/create-team/references/patterns.md"),
    ("skill", "skills/external/sdd-loop-driver/SKILL.md"),
    ("skill", "skills/external/sdd-loop-driver/references/stage-prompts.md"),
    ("test", "tests/contract/test_superagent_definitions.py"),
    ("test", "tests/contract/test_role_edge_engine.py"),
    ("test", "tests/contract/test_role_transition_payload.py"),
    ("test", "tests/contract/test_status_digest_roles.py"),
    ("test", "tests/contract/test_instructions_budget_superagent_section.py"),
    ("test", "tests/contract/test_superagent_zero_mechanism.py"),
    ("test", "tests/contract/test_fast_fail_discipline.py"),
    ("fixture", "tests/fixtures/superagent-role"),
)

#: The roots the change set may touch. A path outside them would be a new surface.
ALLOWED_ROOTS = (
    "scripts/python/",
    ".specify/scripts/python/",
    "shared/definitions/",
    ".specify/shared/definitions/",
    "templates/",
    ".specify/instructions.md",
    "skills/",
    "tests/",
)

#: Directory segments that store state. A new one outside the fixture tree is a second root.
STATE_SEGMENTS = frozenset(
    {"state", "states", "store", "stores", "registry", "registries", "queue", "queues",
     "outbox", "cache", "database", "db"}
)

#: A registry/index file name: the shape a second index of executions or edges would take.
REGISTRY_FILE = re.compile(r"(registry|index|store)[^/]*\.(json|jsonl|ya?ml|db|sqlite)$", re.I)

#: A role-specific renderer is the defect C-3.3 names (same shape as the digest contract's).
SECOND_RENDERER = re.compile(r"def\s+\w*render\w*role|def\s+\w*role\w*render")

SPAWN_MODULES = frozenset({"subprocess", "multiprocessing", "threading", "asyncio", "concurrent"})
SPAWN_CALLS = frozenset({"system", "fork", "execv", "execvp", "execl", "execle", "spawnl", "spawnv", "popen"})

WRITE_CALLS = frozenset(
    {"write_text", "write_bytes", "mkdir", "makedirs", "unlink", "rmdir", "rename",
     "replace", "remove", "rmtree", "copy", "copyfile", "copytree", "move", "touch"}
)

#: Owner rules that must stay reachable by pointer, never copied into a new surface.
RULE_OWNER_POINTERS = ("The Concurrency Obligation", "reporting-obligations.md", "sdd-route.py")

#: Closed set of owner-rule literals a copied rule would carry (each lives at its owner).
FORBIDDEN_RULE_LITERALS = (
    "先想并发",
    "串行须具名理由并记读数",
    "能并发则并发",
    "汇报内容下限",
    "四要素",
    "sdd-capability-or-contract-change",
    "38400",
    "38,400",
    "INSTRUCTIONS_BUDGET_BYTES",
)

#: The nine item ids are owned by the owner page; the wiring surfaces carry pointers only.
NINE_ITEM_SLUGS = (
    "role-activation-scope",
    "self-identity-parent-edge",
    "downward-obligation-checklist",
    "concurrency-budget-ref",
    "reporting-path",
    "state-carriers-writer-boundary",
    "attention-classes-escalation",
    "depth-remaining-prohibitions",
    "aggregate-return-contract",
)

SKILL_SURFACES = (
    "skills/internal/run-agent/SKILL.md",
    "skills/internal/create-team/SKILL.md",
    "skills/internal/create-team/references/patterns.md",
    "skills/external/sdd-loop-driver/SKILL.md",
    "skills/external/sdd-loop-driver/references/stage-prompts.md",
)


# --------------------------------------------------------------------------- #
# pure classifiers (the seeded mutations call them directly)
# --------------------------------------------------------------------------- #
def _read(relative: str) -> str:
    path = REPO_ROOT / relative
    assert path.is_file(), f"missing required file: {relative}"
    return path.read_text(encoding="utf-8")


def _persistence_violations(change_set) -> list[str]:
    violations = []
    for category, path in change_set:
        if category == "fixture":
            continue
        if not any(path == root or path.startswith(root) for root in ALLOWED_ROOTS):
            violations.append(f"{path}: outside the framework roots")
        if set(Path(path).parts) & STATE_SEGMENTS:
            violations.append(f"{path}: state-storing directory segment")
        if category not in {"engine", "engine-mirror", "digest", "digest-mirror", "owner",
                            "owner-mirror", "pointer", "template", "live", "skill", "test",
                            "fixture"}:
            violations.append(f"{path}: unknown category {category!r}")
    engines = [path for category, path in change_set if category == "engine"]
    if len(engines) != 1:
        violations.append(f"expected exactly one new engine file, found {engines}")
    return violations


def _registry_violations(change_set) -> list[str]:
    violations = []
    for category, path in change_set:
        if category == "fixture" or path.startswith("tests/fixtures/"):
            continue
        if REGISTRY_FILE.search(path):
            violations.append(f"{path}: registry/index-shaped file in the change set")
        if {"registry", "registries", "index", "indexes", "store", "stores"} & set(Path(path).parts):
            violations.append(f"{path}: registry-shaped directory segment")
    return violations


def _second_renderer_offenders(source: str) -> list[str]:
    return [match.group(0) for match in SECOND_RENDERER.finditer(source)]


def _spawn_violations(source: str) -> list[str]:
    violations = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in SPAWN_MODULES:
                    violations.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in SPAWN_MODULES:
                violations.append(f"from {node.module} import ...")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in SPAWN_CALLS:
                violations.append(f"call .{node.func.attr}()")
    return violations


def _write_violations(source: str) -> list[str]:
    violations = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
        if name in WRITE_CALLS:
            violations.append(f"write-capable call {name}()")
        if name == "open":
            mode = None
            if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                mode = node.args[1].value
            for keyword in node.keywords:
                if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
                    mode = keyword.value.value
            if isinstance(mode, str) and any(flag in mode for flag in "wax+"):
                violations.append(f"write-mode open {mode!r}")
    return violations


def _section(text: str, heading: str) -> str:
    parts = re.split(r"(?m)^(## .+)$", text)
    sections = {parts[i]: parts[i] + parts[i + 1] for i in range(1, len(parts) - 1, 2)}
    assert heading in sections, f"section {heading!r} is missing from the subject file"
    return sections[heading]


# --------------------------------------------------------------------------- #
# C-3.1 — no new persistence root
# --------------------------------------------------------------------------- #
def test_c3_1_no_new_persistence_root():
    """The change set adds documentation, one engine, tests and fixtures — no state root."""
    assert _persistence_violations(CHANGE_SET) == []
    for _, path in CHANGE_SET:
        assert (REPO_ROOT / path).exists(), f"declared change-set path missing: {path}"

    seeded = CHANGE_SET + (("store", "state/role-store/index.json"),)
    assert _persistence_violations(seeded), (
        "a seeded second persistence root was not detected"
    )


# --------------------------------------------------------------------------- #
# C-3.2 — no new registry
# --------------------------------------------------------------------------- #
def test_c3_2_no_new_registry():
    """No second index of executions or edges; the existing registry stays the only one."""
    assert _registry_violations(CHANGE_SET) == []

    engine = _read("scripts/python/role-edge-check.py")
    assert "resolve_registry_dir" in engine, (
        "the engine must resolve the registry root from the existing line-registry owner"
    )
    digest = _read("scripts/python/status-digest.py")
    assert digest.count('glob("*.json")') == 1, (
        "the digest's legacy registry read must remain its only registry glob"
    )

    seeded = CHANGE_SET + (("store", "registry/role-edges.json"),)
    assert _registry_violations(seeded), "a seeded second registry was not detected"


# --------------------------------------------------------------------------- #
# C-3.3 — no second renderer
# --------------------------------------------------------------------------- #
def test_c3_3_no_second_renderer():
    """`status-digest.py` stays the only digest renderer; no role-specific renderer appears."""
    digest = _read("scripts/python/status-digest.py")
    engine = _read("scripts/python/role-edge-check.py")

    renderer_modules = sorted(
        path.name
        for path in (REPO_ROOT / "scripts" / "python").glob("*.py")
        if re.search(r"(?m)^def render_digest", path.read_text(encoding="utf-8", errors="ignore"))
    )
    assert renderer_modules == ["status-digest.py"], (
        f"digest renderer modules: {renderer_modules}"
    )
    assert _second_renderer_offenders(engine) == [], (
        "the judgement engine carries a role-specific renderer"
    )
    assert _second_renderer_offenders(digest) == [], (
        "the digest carries a second, role-specific renderer"
    )
    assert "render_digest" not in engine, "the engine must not render the digest"

    tree = ast.parse(digest)
    action = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "action_digest"
    )
    calls = [
        node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", None)
        for node in ast.walk(action)
        if isinstance(node, ast.Call)
    ]
    assert calls.count("render_digest_table") == 1, (
        "action_digest must delegate to the one table renderer; calls=%r" % calls
    )

    seeded = digest + "\n\ndef render_role_view(state):\n    return ''\n"
    assert _second_renderer_offenders(seeded), "a seeded second renderer was not detected"


# --------------------------------------------------------------------------- #
# C-3.4 — no second dispatcher / scheduler / queue / transport
# --------------------------------------------------------------------------- #
def test_c3_4_no_second_dispatcher():
    """The feature adds no dispatcher, scheduler, queue or transport."""
    for relative in ("scripts/python/role-edge-check.py", "scripts/python/status-digest.py"):
        assert _spawn_violations(_read(relative)) == [], (
            f"{relative} imports or calls a process-spawn API"
        )
    dispatcher_paths = [
        path
        for _, path in CHANGE_SET
        if not path.startswith("tests/fixtures/")
        and re.search(r"(dispatch|scheduler|queue|outbox)", path, re.I)
    ]
    assert dispatcher_paths == [], f"dispatcher-shaped paths in the change set: {dispatcher_paths}"
    assert "def dispatch" not in _read("scripts/python/role-edge-check.py")

    seeded = _read("scripts/python/role-edge-check.py") + "\nimport subprocess\n"
    assert _spawn_violations(seeded), "a seeded spawn import was not detected"


# --------------------------------------------------------------------------- #
# C-3.5 — the judgement face is read-only
# --------------------------------------------------------------------------- #
def test_c3_5_judgement_face_is_read_only():
    """Zero write points in the engine source, and its runtime mirror stays byte-identical."""
    engine = _read("scripts/python/role-edge-check.py")
    assert _write_violations(engine) == [], "the judgement face has a write point"
    assert "tempfile" not in engine, "the engine must not create temporary files"
    assert ENGINE_MIRROR.is_file(), "the engine's runtime mirror is missing"
    assert ENGINE.read_bytes() == ENGINE_MIRROR.read_bytes(), (
        "the engine drifted between framework source and runtime mirror"
    )

    seeded = engine + "\n\ndef _leak(path):\n    path.write_text('x')\n"
    assert _write_violations(seeded), "a seeded write point was not detected"


# --------------------------------------------------------------------------- #
# C-3.6 — owner rules are pointed at, never copied
# --------------------------------------------------------------------------- #
def test_c3_6_owner_rules_not_copied():
    """Concurrency, reporting and authorization stay with their owners; surfaces carry pointers."""
    owner = _read("shared/definitions/superagent-definitions.md")
    missing = [pointer for pointer in RULE_OWNER_POINTERS if pointer not in owner]
    assert not missing, f"owner rules not reached by pointer from the owner page: {missing}"

    section = _section(_read("templates/instructions-template.md"), SECTION_HEADING)
    assert not re.search(r"(?m)^\|", section), "the pointer section carries a table"
    assert not re.search(r"(?m)^#{3,} ", section), "the pointer section carries a sub-heading"
    for literal in FORBIDDEN_RULE_LITERALS:
        assert literal not in owner, f"owner rule text {literal!r} copied onto the owner page"
        assert literal not in section, f"owner rule text {literal!r} copied into the section"

    for relative in SKILL_SURFACES:
        text = _read(relative)
        assert OWNER_POINTER in text, f"{relative} lost the owner-page pointer"
        leaked = [slug for slug in NINE_ITEM_SLUGS if slug in text]
        assert not leaked, f"{relative} copied the injection item ids: {leaked}"

    seeded = section + "\n- 先想并发\n"
    assert "先想并发" in seeded and any(
        literal in seeded for literal in FORBIDDEN_RULE_LITERALS
    ), "a seeded copied rule literal was not detected"
