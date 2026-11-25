"""Integration tests: the memory system survives the store-layout move (Feature 105, US3 / T017).

Contract: ``contracts/memory-and-injection.contract.md`` P-1 / P-2 / P-5; requirements
FR-006 and FR-007. "Behaviorally identical except for the storage roots": the two
memory tiers move to ``.specify/session/`` and ``.specify/knowledge/`` while the scope
names, the six actions, the entry schema and the determination persistence path stay
unchanged.

Red-first (Constitution IV): this file is authored before T019's wiring lands; its
execution readings are recorded in the feature's ``notes/red-first-evidence.md``.

Every engine call goes through the shared in-process harness with an explicit
``--workspace-root`` (the two-hats guard: a test must never write into the framework
repository's own stores).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from script_api import load_engine_module, run_engine_in_process

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / "scripts" / "python" / "memory-utils.py"
DETERMINATION = ROOT / "scripts" / "python" / "run-determination.py"

SESSION_ROOT = ".specify/session/"
KNOWLEDGE_ROOT = ".specify/knowledge/"
RETIRED_ROOT = ".specify/memory"

# The pre-move record schema, pinned as a literal: the storage move MUST NOT change it.
DETERMINATION_SCHEMA_KEYS = {
    "kind",
    "schema_version",
    "unit_id",
    "unit_type",
    "run_id",
    "feature",
    "feature_id",
    "determined_at",
    "settled_at",
    "complexity",
    "qualification",
    "axes",
    "provenance",
    "change_point",
    "passive_trigger",
}

# The memory entry frontmatter keys (the memory engine's own schema, unchanged by 105).
ENTRY_META_KEYS = {
    "id",
    "scope",
    "source",
    "feature",
    "tags",
    "title",
    "created",
    "session_id",
    "summary",
}


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    (tmp_path / ".specify").mkdir(parents=True)
    return tmp_path


def _run(engine: Path, ws: Path, *args: str):
    return run_engine_in_process(engine, ["--workspace-root", str(ws), *args])


def _payload(result) -> dict:
    assert result.returncode == 0, f"engine failed: {result.stderr or result.stdout}"
    return json.loads(result.stdout)


def _record(ws: Path, scope: str, title: str, content: str, **extra: str) -> dict:
    args = ["--action", "record", "--scope", scope,
            "--source", "skill:test-memory", "--title", title, "--content", content]
    for key, value in extra.items():
        args += [f"--{key.replace('_', '-')}", value]
    return _payload(_run(MEMORY, ws, *args))


def test_session_record_recall_roundtrip_under_new_root(ws: Path):
    recorded = _record(ws, "session", "Session roundtrip",
                       "decided: keep the temporary memory system intact")
    assert recorded["scope"] == "session"
    assert recorded["path"].startswith(SESSION_ROOT), recorded["path"]

    entry = ws / recorded["path"]
    assert entry.is_file(), "the session entry must land under .specify/session/"
    assert "keep the temporary memory system intact" in entry.read_text(encoding="utf-8")
    assert not (ws / RETIRED_ROOT).exists(), "the retired container must never be created"

    recalled = _payload(_run(MEMORY, ws, "--action", "recall", "--scope", "all",
                             "--query", "temporary memory system", "--format", "json"))
    matches = recalled["matches"]
    hit = [m for m in matches if m["path"] == recorded["path"]]
    assert hit, f"recall must return the freshly recorded entry; got {matches}"
    assert hit[0]["scope"] == "session"
    for match in matches:
        assert match["path"].startswith((SESSION_ROOT, KNOWLEDGE_ROOT)), (
            f"every recalled entry must resolve under a memory root, got {match['path']}"
        )


def test_knowledge_record_recall_upsert_by_slug(ws: Path):
    first = _record(ws, "knowledge", "Durable convention", "v1 wording", tags="style")
    second = _record(ws, "knowledge", "Durable convention", "v2 wording", tags="review")
    assert first["path"] == second["path"] == KNOWLEDGE_ROOT + "durable-convention.md"

    files = list((ws / KNOWLEDGE_ROOT).glob("*.md"))
    assert [p.name for p in files] == ["durable-convention.md"], (
        "upsert-by-slug keeps exactly one file per title slug"
    )
    text = files[0].read_text(encoding="utf-8")
    assert "v2 wording" in text and "v1 wording" not in text

    recalled = _payload(_run(MEMORY, ws, "--action", "recall", "--scope", "knowledge",
                             "--query", "durable convention", "--format", "json"))
    assert recalled["matches"][0]["path"] == KNOWLEDGE_ROOT + "durable-convention.md"


def test_prune_bounds_under_new_root(ws: Path):
    for name in ("one", "two", "three"):
        _record(ws, "session", f"entry {name}", f"content {name}")

    # The age bound reads the entry's own `created` frontmatter, so an old record is
    # built by writing the entry file directly (the record action always stamps now).
    old = ws / SESSION_ROOT / "20200101T000000Z-old.md"
    old.parent.mkdir(parents=True, exist_ok=True)
    old.write_text(
        "---\nid: 20200101T000000Z-old\nscope: session\n"
        "source: skill:test-memory\ntitle: old entry\n"
        "created: 2020-01-01T00:00:00Z\ntags: []\n---\n\nold content\n",
        encoding="utf-8",
    )

    by_age = _payload(_run(MEMORY, ws, "--action", "prune", "--scope", "session",
                           "--max-age-days", "30"))
    assert old.name in by_age["removed"], "the age bound must drop the 2020 entry"
    assert by_age["remaining"] == 3

    by_count = _payload(_run(MEMORY, ws, "--action", "prune", "--scope", "session",
                             "--max-entries", "2"))
    assert by_count["remaining"] == 2, "the count bound keeps the newest two entries"
    files = sorted(p.name for p in (ws / SESSION_ROOT).glob("*.md"))
    assert len(files) == 2 and old.name not in files
    assert not (ws / RETIRED_ROOT).exists()


def test_reindex_retires_only_the_legacy_index(ws: Path):
    _record(ws, "session", "kept entry", "kept content")
    legacy = ws / SESSION_ROOT / "index.json"
    legacy.write_text(json.dumps({"scope": "session", "entries": []}), encoding="utf-8")

    first = _payload(_run(MEMORY, ws, "--action", "reindex", "--scope", "all"))
    assert first["migrated"] == ["session"], "a legacy per-scope index is retired on reindex"
    assert first["reindexed"]["session"] == 1, "entries are scan-derived, never rewritten"
    assert not legacy.exists()

    second = _payload(_run(MEMORY, ws, "--action", "reindex", "--scope", "all"))
    assert second["migrated"] == [], "reindex is idempotent"


def test_determination_persists_into_session_and_history_reads_it(ws: Path):
    (ws / SESSION_ROOT).mkdir(parents=True)
    result = _run(DETERMINATION, ws, "--json",
                  "--action", "determine",
                  "--unit-id", "skill:test-memory",
                  "--run-id", "run-001",
                  "--complexity", "complex",
                  "--feature", "105-runtime-store-layout")
    payload = _payload(result)

    persistence = payload["persistence"]
    assert persistence["adapter"] == "memory-utils-session"
    assert persistence["persisted"] is True, persistence.get("reason")
    assert persistence["path"].startswith(SESSION_ROOT), (
        f"the determination record must land in the session tier; got {persistence['path']}"
    )
    entry = ws / persistence["path"]
    assert entry.is_file()
    assert not (ws / RETIRED_ROOT).exists()

    memory_engine = load_engine_module(MEMORY)
    meta, _ = memory_engine.parse_frontmatter(entry.read_text(encoding="utf-8"))
    # Empty values are omitted by the pre-existing frontmatter writer, so the schema
    # pin is "no key outside the closed set" plus "the core keys are present".
    assert set(meta) <= ENTRY_META_KEYS, (
        f"entry frontmatter gained keys: {sorted(set(meta) - ENTRY_META_KEYS)}"
    )
    assert {"id", "scope", "source", "tags", "title", "created", "summary", "feature"} <= set(meta)
    assert meta["scope"] == "session"
    assert "run-determination" in meta["tags"]

    determination_engine = load_engine_module(DETERMINATION)
    record = determination_engine.parse_entry_body(entry.read_text(encoding="utf-8"))
    assert record is not None, "the entry body must carry the fenced determination record"
    assert set(record) == DETERMINATION_SCHEMA_KEYS, (
        f"determination record schema changed: {sorted(set(record) ^ DETERMINATION_SCHEMA_KEYS)}"
    )
    assert record["run_id"] == "run-001"
    assert record["feature"] == "105-runtime-store-layout"

    history = _payload(_run(DETERMINATION, ws, "--json", "--action", "history",
                            "--target", "skill:test-memory"))
    assert history["counts"]["total"] == 1
    assert history["records"][0]["run_id"] == "run-001"
