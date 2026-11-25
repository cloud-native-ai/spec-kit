"""105 runtime store layout — closed inventory, declaration, framework map, mirror set, two writers.

Red-first: authored before the declaration, the framework-map rows and the seeded init exist
(tasks.md T002). Each function below names the contract clause it pins:

* C-1 target layout          -> ``test_inventory_is_closed``
* C-6 machine declaration    -> ``test_declaration_equals_inventory_and_consumer_sets``
* C-3 ownership + C-5 map    -> ``test_framework_map_rows_and_tombstone``
* C-2 retired container      -> ``test_repo_has_no_retired_root`` (dogfood closes it in US5)
* SC-007 mirror member set   -> ``test_mirror_member_set`` (US5 regenerates the mirrors)
* FR-025 per-store layout    -> ``test_two_writers_distinct_paths``
* FR-027 / SC-009 closure    -> ``test_backward_incompatible_inventory_is_closed``

The baseline children below are the measured `git ls-tree -d 23938f22e:.specify/memory` set
(12 entries); the requirements Store Inventory is the human side of the same closed set.

U-03 scope decision (analyze residue, recorded here): the FR-027 forbidden-behavior words are
asserted against the inventory's **Behavior cell only**, never the whole row. BC12's change cell
legitimately names ``todo/`` (a Store Inventory member), and a whole-row scan would be red on a
correct plan. The Behavior cell is where the closed class must appear, so that cell is the guard's
scope; a forbidden word smuggled into any other cell is caught by (b)'s exact-token assertion only
if it replaces the behavior, which is the failure mode FR-027 names.
"""

from __future__ import annotations

import re
import subprocess
import sys
import threading
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "105-runtime-store-layout"
REQUIREMENTS = SPEC_DIR / "requirements.md"
PLAN = SPEC_DIR / "plan.md"
TASKS = SPEC_DIR / "tasks.md"
CONTRACTS = SPEC_DIR / "contracts"
MIGRATE_CONTRACT = CONTRACTS / "migrate-store-layout.contract.md"
STORE_CONTRACT = CONTRACTS / "store-layout.contract.md"
FRAMEWORK_MAP = REPO_ROOT / "shared" / "definitions" / "framework-map.md"
MIRROR_BASELINE = SPEC_DIR / "test-evidence" / "sync-mirrors-baseline.txt"
DECLARATION_FILE = (
    REPO_ROOT / "shared" / "declarations" / "facts" / "runtime-store-layout.yaml"
)

DECLARATION_SLUG = "runtime-store-layout"
RETIRED_ROOT = ".specify/memory"

BASELINE_CHILDREN = (
    "coaching",
    "evidence",
    "exec-quant",
    "feedback",
    "housekeeping",
    "knowledge",
    "renumber",
    "retention",
    "session",
    "todo",
    "tools",
    "trigger",
)
ON_DEMAND_STORES = ("sanitize", "migrate")
EXPECTED_STORES = tuple(sorted(BASELINE_CHILDREN + ON_DEMAND_STORES))
LEGACY_RETIRED = ("draft",)
LEGACY_NON_STORE = ("git-workflow.md",)
TABLE_MEMBERS = (
    "session",
    "knowledge",
    "feedback",
    "evidence",
    "exec-quant",
    "trigger",
    "retention",
    "renumber",
    "sanitize",
    "housekeeping",
    "coaching",
    "todo",
    "tools",
    "migrate",
    "draft",
    "git-workflow.md",
    RETIRED_ROOT,
)
LIFECYCLES = {
    "memory-tier",
    "runtime-record",
    "telemetry",
    "cache",
    "queue",
    "receipt",
    "definition-record",
    "run-report",
}

sys.path.insert(0, str(REPO_ROOT / "scripts" / "python"))
import declaration_reader  # noqa: E402  (import follows the sys.path entry above)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _declaration():
    """The layout fact body; an absent declaration is the STR-014 finding, never a pass."""
    try:
        fact = declaration_reader.load_fact(
            declaration_reader.find_repo(REPO_ROOT), DECLARATION_SLUG
        )
    except declaration_reader.DeclarationError as exc:
        pytest.fail(f"{declaration_reader.absent_label(DECLARATION_SLUG)}: {exc}")
    body = fact["body"]
    statement = body.get("statement")
    assert isinstance(statement, dict), "statement must be a mapping (data-model E-10)"
    stores = statement.get("stores")
    assert isinstance(stores, dict) and stores, "statement.stores must be a non-empty mapping"
    return body


def _inventory_rows():
    """`(row_number, member, disposition)` for every Store Inventory row."""
    rows = []
    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`[^|]*\|([^|]*)\|([^|]*)\|", line)
        if match:
            rows.append(
                (int(match.group(1)), match.group(2), match.group(3), match.group(4))
            )
    return rows


def _member_name(raw):
    """`session/` -> session; `migrate/receipts/` -> migrate; `.specify/memory/` stays the container."""
    text = raw.rstrip("/")
    return text if text == RETIRED_ROOT else text.split("/")[0]


def _map_rows():
    """`(what, where, notes)` for every three-column row of the framework map table."""
    rows = []
    for line in FRAMEWORK_MAP.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or set(stripped) <= set("|-: "):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 3:
            continue
        rows.append(tuple(cell.replace("`", "").strip() for cell in cells))
    return rows


# --------------------------------------------------------------------------- #
# C-1 — the closed inventory
# --------------------------------------------------------------------------- #
def test_inventory_is_closed():
    body = _declaration()
    statement = body["statement"]
    stores = statement["stores"]
    rows = _inventory_rows()

    assert [row[0] for row in rows] == list(range(1, 18)), "the table must hold rows 1..17"

    members = [_member_name(row[1]) for row in rows]
    assert members == list(TABLE_MEMBERS), (
        "the table must classify the closed inventory in its recorded order"
    )
    assert len(set(members)) == len(members), "every member appears exactly once"
    assert set(BASELINE_CHILDREN) | set(ON_DEMAND_STORES) == set(EXPECTED_STORES)

    assert tuple(sorted(stores)) == EXPECTED_STORES, (
        f"declaration stores must be exactly the closed set: {sorted(stores)}"
    )

    by_member = {_member_name(row[1]): row for row in rows}
    for name in BASELINE_CHILDREN + ON_DEMAND_STORES:
        disposition = by_member[name][3]
        assert f".specify/{name}/" in disposition, (
            f"row {name} must name its target root .specify/{name}/"
        )
    assert "退役" in by_member["draft"][3], "draft must be retired with no new home"
    assert "非存储" in by_member["git-workflow.md"][3], "git-workflow.md is a non-store"
    assert "墓碑" in by_member[RETIRED_ROOT][3], (
        "the container itself must be disposed as a tombstone row"
    )

    assert statement["retired_container"] == RETIRED_ROOT
    assert tuple(statement["legacy_retired"]) == LEGACY_RETIRED
    assert tuple(statement["legacy_non_store"]) == LEGACY_NON_STORE

    for name, entry in stores.items():
        assert isinstance(entry, dict), f"store {name} must be a mapping"
        assert entry.get("lifecycle") in LIFECYCLES, (name, entry.get("lifecycle"))
        owner = entry.get("owner")
        assert isinstance(owner, str) and (REPO_ROOT / owner).exists(), (name, owner)
        assert isinstance(entry.get("content_class"), str) and entry["content_class"].strip()
        non_content = entry.get("non_content")
        assert isinstance(non_content, list), f"store {name}: non_content must be a list"
        seeded = str(entry.get("seeded")).strip().lower()
        assert seeded in ("true", "false"), f"store {name}: seeded must be a boolean literal"
        assert (seeded == "true") is (name in ("session", "knowledge")), (
            f"only the two memory tiers are seeded by init; {name} is seeded={seeded}"
        )


# --------------------------------------------------------------------------- #
# C-6 — declaration membership == requirements table == code consumer set
# --------------------------------------------------------------------------- #
def _reading_consumers():
    """Files that both name the read entry and this fact slug — the actual read points."""
    candidates = sorted((REPO_ROOT / "scripts" / "python").glob("*.py"))
    candidates.append(REPO_ROOT / "src" / "specify_cli" / "__init__.py")
    readers = set()
    for path in candidates:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "declaration_reader" in text and DECLARATION_SLUG in text:
            readers.add(path.relative_to(REPO_ROOT).as_posix())
    return readers


def test_declaration_equals_inventory_and_consumer_sets():
    body = _declaration()
    statement = body["statement"]
    stores = statement["stores"]

    table_targets = {
        _member_name(row[1])
        for row in _inventory_rows()
        if _member_name(row[1]) in BASELINE_CHILDREN + ON_DEMAND_STORES
    }
    assert set(stores) == table_targets, (
        "declaration membership must equal the requirements Store Inventory targets"
    )

    declared_consumers = {
        declaration_reader.normalize_path(path) for path in body.get("consumers") or []
    }
    assert declared_consumers, "consumers must be declared"
    assert _reading_consumers() == declared_consumers, (
        "the declared consumer set must be exactly the code files that read the fact"
    )
    for path in declared_consumers:
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        assert "absent_label" in text, (
            f"{path} must use the reader's absent_label instead of inventing a fallback roster"
        )

    former = [declaration_reader.normalize_path(path) for path in body.get("former_carriers") or []]
    assert former, "former_carriers must record the literals this declaration replaces"
    assert len(former) == len(set(former)), "former_carriers must not repeat a path"

    surface = declaration_reader.load_fact(
        declaration_reader.find_repo(REPO_ROOT), "non-disposable-review-surface"
    )["body"]["statement"]
    basenames = {path.rsplit("/", 1)[-1]: path for path in surface}
    store_members = {
        basenames[name] for name in stores if name in basenames
    }
    assert store_members == {f".specify/{name}" for name in stores}, (
        "the review surface's store members must equal the declaration's store set"
    )
    assert RETIRED_ROOT not in surface, "the retired container must leave the review surface"


# --------------------------------------------------------------------------- #
# C-3 / C-5 — framework map rows and the single tombstone
# --------------------------------------------------------------------------- #
def test_framework_map_rows_and_tombstone():
    body = _declaration()
    stores = body["statement"]["stores"]
    rows = _map_rows()

    def rows_at(where):
        return [row for row in rows if row[1] == where]

    for name, entry in stores.items():
        matches = rows_at(f".specify/{name}/")
        assert len(matches) == 1, f"expected exactly one framework-map row for .specify/{name}/"
        _what, _where, notes = matches[0]
        assert f"owner: {entry['owner']}" in notes, (
            f"the .specify/{name}/ row must name its owner {entry['owner']}"
        )
        assert f"lifecycle: {entry['lifecycle']}" in notes, (
            f"the .specify/{name}/ row must name its lifecycle"
        )
        assert "content class:" in notes, (
            f"the .specify/{name}/ row must name its content class"
        )

    tombstones = rows_at(RETIRED_ROOT + "/")
    assert len(tombstones) == 1, "the retired container must hold exactly one tombstone row"
    what, _where, notes = tombstones[0]
    lowered = (what + " " + notes).lower()
    assert "tombstone" in lowered, "the retired row must say tombstone"
    assert "retired" in lowered, "the retired row must say retired"
    assert ".specify/session/" in notes and ".specify/knowledge/" in notes, (
        "the tombstone must name where agent-context memory moved"
    )
    assert "no engine" in lowered, "the tombstone must forbid engines treating it as a live store"
    assert "project memory" not in what.lower(), (
        "no live 'Project memory' row may survive the retirement"
    )


# --------------------------------------------------------------------------- #
# C-2 — dogfood closes this in US5
# --------------------------------------------------------------------------- #
def test_repo_has_no_retired_root():
    assert not (REPO_ROOT / RETIRED_ROOT).exists(), (
        f"{RETIRED_ROOT} is a retired store root; the dogfood migration (US5) must remove it"
    )


# --------------------------------------------------------------------------- #
# SC-007 — no NEW mirror drift member relative to the pinned baseline
# --------------------------------------------------------------------------- #
MEMBER_RE = re.compile(r"^(DIFF|MISS|ORPHAN)\s+(.*?)(?:OK:.*|DRIFT detected.*)?$")


def _members(text):
    return {m.group(2) for line in text.splitlines() if (m := MEMBER_RE.match(line))}


def test_mirror_member_set():
    proc = subprocess.run(
        [sys.executable, "scripts/python/sync-mirrors.py", "--check"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode in (0, 2), (
        f"sync-mirrors --check must answer 0 (clean) or 2 (drift); rc={proc.returncode}\n"
        f"{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}"
    )
    assert "DIFF" in proc.stdout or "OK" in proc.stdout, (
        f"the check printed no member list; the surface moved\n{proc.stdout[-2000:]}"
    )
    baseline = _members(MIRROR_BASELINE.read_text(encoding="utf-8"))
    assert baseline, "the pinned baseline must name its drift members"
    new_members = sorted(_members(proc.stdout) - baseline)
    assert not new_members, (
        "no NEW mirror drift member is allowed before the regeneration step (US5): "
        f"{new_members[:20]}"
    )


# --------------------------------------------------------------------------- #
# FR-025 — two writers per store land on distinct per-entry paths
# --------------------------------------------------------------------------- #
ENTRY_SHAPES = {
    "session": ("writer-a.md", "writer-b.md"),
    "knowledge": ("writer-a.md", "writer-b.md"),
    "feedback": ("20260101T000000Z-skill:alpha.md", "20260101T000001Z-skill:beta.md"),
    "evidence": (
        "ev-20260101-000000-project/findings.json",
        "ev-20260101-000001-project/findings.json",
    ),
    "exec-quant": (
        "records/20260101T000000Z-aaaa.json",
        "records/20260101T000001Z-bbbb.json",
    ),
    "trigger": ("index.json", "telemetry.jsonl"),
    "retention": (
        "receipts/20260101T000000Z-aaaa.json",
        "receipts/20260101T000001Z-bbbb.json",
    ),
    "renumber": (
        "plans/20260101T000000Z-aaaa.json",
        "plans/20260101T000001Z-bbbb.json",
    ),
    "sanitize": ("findings.json", "cleanup-plan.json"),
    "housekeeping": (
        "sdd-housekeeping-demo-20260101T000000Z.yaml",
        "sdd-housekeeping-demo-20260101T000001Z.yaml",
    ),
    "coaching": (
        "20260101T000000Z-skill:alpha/expectation.md",
        "20260101T000001Z-skill:beta/expectation.md",
    ),
    "todo": ("writer-a.md", "writer-b.md"),
    "tools": ("writer-a.md", "writer-b.md"),
    "migrate": (
        "receipts/20260101T000000Z-aaaaaaaa.json",
        "receipts/20260101T000001Z-bbbbbbbb.json",
    ),
}


def test_two_writers_distinct_paths(tmp_path: Path):
    body = _declaration()
    stores = set(body["statement"]["stores"])
    assert set(ENTRY_SHAPES) == stores, (
        "every declared store must carry its two-writer simulation"
    )

    roots = {f".specify/{name}" for name in stores}
    for name in sorted(stores):
        for other in roots - {f".specify/{name}"}:
            assert not (f".specify/{name}").startswith(other + "/"), (
                f"store root .specify/{name}/ nests under {other}/"
            )

    written = []
    for name in sorted(stores):
        root = tmp_path / ".specify" / name
        entry_a, entry_b = ENTRY_SHAPES[name]
        assert entry_a != entry_b, (name, entry_a)
        barrier = threading.Barrier(2)

        def write(relpath):
            path = root / relpath
            path.parent.mkdir(parents=True, exist_ok=True)
            barrier.wait()
            path.write_text(f"{name}:{relpath}\n", encoding="utf-8")

        threads = [
            threading.Thread(target=write, args=(relpath,))
            for relpath in (entry_a, entry_b)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        path_a, path_b = root / entry_a, root / entry_b
        assert path_a.is_file() and path_b.is_file(), (name, entry_a, entry_b)
        assert path_a != path_b, (name, entry_a, entry_b)
        assert path_a.read_text(encoding="utf-8") == f"{name}:{entry_a}\n"
        assert path_b.read_text(encoding="utf-8") == f"{name}:{entry_b}\n"
        written.extend([path_a, path_b])

    assert len(written) == len(set(written)), "two stores produced the same entry path"


# --------------------------------------------------------------------------- #
# FR-027 / SC-009 — the closed backward-incompatible change inventory (T042)
# --------------------------------------------------------------------------- #
BC_ID_RE = re.compile(r"^\|\s*(BC\d+)\s*\|")
BC_CITATION_RE = re.compile(r"#(\d+)")
BC_SAME_AS_RE = re.compile(r"同\s*(BC\d+)")
EVIDENCE_PATH_RE = re.compile(
    r"(?<![\w/.-])(?:tests|test-evidence|notes|shared|scripts|src|seed|templates|docs)/[\w./-]+"
)
EVIDENCE_TASK_RE = re.compile(r"T(\d{3})")
EVIDENCE_CLAUSE_RE = re.compile(r"(?<![\w-])([MC])-(\d+)(?!\d)")
BEHAVIOR_CLASSES = {
    "migrate:relocate",
    "migrate:container-pass",
    "compatibility-bridge",
    "no-workspace-object",
}
REFUSE_PREFIX = "migrate:refuse:"
FORBIDDEN_BEHAVIOR_WORDS = ("manual", "docs-only", "fallback", "runtime-fallback", "todo")


def _bc_rows():
    """`{id, change, source, behavior, evidence}` for every plan inventory row."""
    rows = []
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        match = BC_ID_RE.match(line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        assert len(cells) == 5, f"the BC inventory row {match.group(1)} must hold five cells"
        rows.append(
            {
                "id": cells[0],
                "change": cells[1],
                "source": cells[2],
                "behavior": cells[3],
                "evidence": cells[4],
            }
        )
    return rows


def _m5_tokens():
    """The M-5 closed refusal table's `reason` tokens."""
    text = MIGRATE_CONTRACT.read_text(encoding="utf-8")
    assert "## M-5" in text, "the migrate contract must define the M-5 refusal classes"
    section = text.split("## M-5", 1)[1].split("## M-6", 1)[0]
    tokens = set()
    for line in section.splitlines():
        match = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        if match:
            tokens.add(match.group(1))
    return tokens


def _clause_headings(path):
    return {
        f"{match.group(1)}-{match.group(2)}"
        for match in re.finditer(r"^## ([MCL])-(\d+)", path.read_text(encoding="utf-8"), re.M)
    }


def _task_ids():
    ids = set()
    for line in TASKS.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^- \[[ >X~]\] (T\d{3})\b", line)
        if match:
            ids.add(match.group(1))
    return ids


def _state_changing_inventory_rows():
    """Store Inventory rows this feature changes: relocations, retirements, the container."""
    derived = set()
    for number, _member, _classification, disposition in _inventory_rows():
        cell = disposition
        if "非存储" in cell:
            continue
        if ".specify/" in cell or "退役" in cell or "墓碑" in cell:
            derived.add(number)
    return derived


def _evidence_refs(cell, rows_by_id, seen=None):
    """Expand `同 BCnn` pointers and collect `(paths, tasks, clauses)` from one evidence cell."""
    seen = set(seen or ())
    paths = {match.group(0) for match in EVIDENCE_PATH_RE.finditer(cell)}
    tasks = {"T" + match.group(1) for match in EVIDENCE_TASK_RE.finditer(cell)}
    clauses = {
        f"{match.group(1)}-{match.group(2)}"
        for match in EVIDENCE_CLAUSE_RE.finditer(cell)
    }
    for target in BC_SAME_AS_RE.findall(cell):
        if target in seen or target not in rows_by_id:
            continue
        sub_paths, sub_tasks, sub_clauses = _evidence_refs(
            rows_by_id[target]["evidence"], rows_by_id, seen | {target}
        )
        paths |= sub_paths
        tasks |= sub_tasks
        clauses |= sub_clauses
    return paths, tasks, clauses


def test_backward_incompatible_inventory_is_closed():
    rows = _bc_rows()
    rows_by_id = {row["id"]: row for row in rows}
    assert [row["id"] for row in rows] == [
        f"BC{number:02d}" for number in range(1, len(rows) + 1)
    ], "the inventory must be a contiguous, duplicate-free BC01…BCNN set"
    assert len(rows) == 18, f"the closed inventory holds 18 rows; found {len(rows)}"

    # (a) every state-changing Store Inventory row is cited by exactly one BC row.
    cited = [
        int(number)
        for row in rows
        for number in BC_CITATION_RE.findall(row["source"])
    ]
    state_changing = _state_changing_inventory_rows()
    assert state_changing == set(range(1, 16)) | {17}, (
        "the requirements Store Inventory must classify rows 1–15 and 17 as state-changing"
    )
    assert sorted(cited) == sorted(state_changing), (
        "the inventory must cite every state-changing Store Inventory row exactly once; "
        f"cited={sorted(cited)} expected={sorted(state_changing)}"
    )

    # (b) exactly one primary behavior from the closed class set, refuse tokens from M-5.
    m5 = _m5_tokens()
    assert m5, "the M-5 table must be parseable"
    for row in rows:
        behavior = row["behavior"].replace("`", "").strip()
        assert behavior, f"{row['id']} names no behavior"
        if behavior.startswith(REFUSE_PREFIX):
            token = behavior[len(REFUSE_PREFIX):]
            assert token in m5 or (
                token.startswith("path-collision:") and "path-collision:<relpath>" in m5
            ), (
                f"{row['id']}: refusal token {token!r} is outside the closed M-5 table"
            )
        else:
            assert behavior in BEHAVIOR_CLASSES, (
                f"{row['id']}: behavior {behavior!r} is outside the closed class set"
            )

    # (c) every evidence pointer resolves to an existing path, evidence file, or task id.
    task_ids = _task_ids()
    migrate_clauses = _clause_headings(MIGRATE_CONTRACT)
    store_clauses = _clause_headings(STORE_CONTRACT)
    for row in rows:
        paths, tasks, clauses = _evidence_refs(row["evidence"], rows_by_id)
        assert paths or tasks, (
            f"{row['id']}: the evidence cell carries no resolvable test path, evidence "
            f"file, or task id: {row['evidence']!r}"
        )
        for path in sorted(paths):
            assert (REPO_ROOT / path).exists(), (
                f"{row['id']}: evidence path {path!r} does not exist"
            )
        for task in sorted(tasks):
            assert task in task_ids, (
                f"{row['id']}: evidence task {task!r} is not a tasks.md row"
            )
        for clause in sorted(clauses):
            prefix = clause[0]
            known = migrate_clauses if prefix == "M" else store_clauses
            assert clause in known, (
                f"{row['id']}: evidence clause {clause!r} has no heading in its contract"
            )

    # (d) forbidden behavior words are absent from the BEHAVIOR cell (U-03 scope: the change
    # cell legitimately names the todo/ store; the pin below keeps that scope decision honest).
    assert "todo/" in rows_by_id["BC12"]["change"], (
        "the U-03 scope decision only holds while BC12's change cell names todo/"
    )
    for row in rows:
        lowered = row["behavior"].lower()
        for word in FORBIDDEN_BEHAVIOR_WORDS:
            assert word not in lowered, (
                f"{row['id']}: forbidden behavior word {word!r} in {row['behavior']!r}"
            )
