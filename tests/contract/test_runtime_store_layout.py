"""105 runtime store layout — closed inventory, declaration, framework map, mirror set, two writers.

Red-first: authored before the declaration, the framework-map rows and the seeded init exist
(tasks.md T002). Each function below names the contract clause it pins:

* C-1 target layout          -> ``test_inventory_is_closed``
* C-6 machine declaration    -> ``test_declaration_equals_inventory_and_consumer_sets``
* C-3 ownership + C-5 map    -> ``test_framework_map_rows_and_tombstone``
* C-2 retired container      -> ``test_repo_has_no_retired_root`` (dogfood closes it in US5)
* SC-007 mirror member set   -> ``test_mirror_member_set`` (US5 regenerates the mirrors)
* FR-025 per-store layout    -> ``test_two_writers_distinct_paths``

The baseline children below are the measured `git ls-tree -d 23938f22e:.specify/memory` set
(12 entries); the requirements Store Inventory is the human side of the same closed set.
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
