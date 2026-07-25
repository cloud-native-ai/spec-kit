from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import memory_utils


def _namespace(**overrides):
    base = {
        "action": "recall",
        "workspace_root": None,
        "scope": "session",
        "source": None,
        "title": None,
        "content": None,
        "content_file": None,
        "tags": None,
        "feature": None,
        "session_id": None,
        "query": None,
        "since": None,
        "limit": 5,
        "max_entries": None,
        "max_age_days": None,
        "format": "json",
    }
    base.update(overrides)
    return memory_utils.argparse.Namespace(**base)


# --------------------------------------------------------------------------- #
# Source boundary
# --------------------------------------------------------------------------- #
def test_validate_source_accepts_speckit_and_skill():
    assert memory_utils.validate_source("/speckit.plan")
    assert memory_utils.validate_source("skill:study-project")


def test_validate_source_rejects_arbitrary_text():
    assert not memory_utils.validate_source("random chat")
    assert not memory_utils.validate_source("")
    assert not memory_utils.validate_source("speckit.plan")  # missing leading slash


def test_record_rejects_invalid_source(tmp_path: Path):
    ns = _namespace(action="record", workspace_root=str(tmp_path), scope="session",
                    source="freeform conversation", title="x", content="y")
    with pytest.raises(memory_utils.MemoryError):
        memory_utils.action_record(ns)


# --------------------------------------------------------------------------- #
# Record + index
# --------------------------------------------------------------------------- #
def test_record_writes_file_and_index(tmp_path: Path):
    ns = _namespace(action="record", workspace_root=str(tmp_path), scope="session",
                    source="/speckit.tasks", title="Chose JWT", content="Decided JWT",
                    tags="decision, auth", feature="012-auth")
    result = memory_utils.action_record(ns)

    entry_file = tmp_path / result["path"]
    assert entry_file.exists()
    meta, body = memory_utils.parse_frontmatter(entry_file.read_text(encoding="utf-8"))
    assert meta["source"] == "/speckit.tasks"
    assert meta["tags"] == ["decision", "auth"]
    assert meta["feature"] == "012-auth"
    assert "Decided JWT" in body

    index = json.loads((tmp_path / ".specify/memory/session/index.json").read_text(encoding="utf-8"))
    assert index["scope"] == "session"
    assert len(index["entries"]) == 1
    assert index["entries"][0]["source"] == "/speckit.tasks"


def test_stable_slug_disambiguates_non_ascii_titles():
    # pure-ASCII titles stay clean and human-readable
    assert memory_utils.stable_slug("User prefers concise reports") == "user-prefers-concise-reports"
    # distinct CJK-only titles must not collapse to the same slug
    a = memory_utils.stable_slug("统一环境变量设计决策")
    b = memory_utils.stable_slug("记忆系统边界约定")
    assert a != b
    assert a != "entry" and b != "entry"
    # identical titles are stable (so knowledge upsert still works)
    assert memory_utils.stable_slug("统一环境变量设计决策") == a
    # mixed titles keep their ASCII prefix plus a disambiguating hash
    assert memory_utils.stable_slug("024 统一环境变量设计决策").startswith("024-")


def test_knowledge_non_ascii_titles_do_not_overwrite(tmp_path: Path):
    common = dict(action="record", workspace_root=str(tmp_path), scope="knowledge",
                  source="skill:x", tags="decision")
    memory_utils.action_record(_namespace(title="统一环境变量设计决策", content="A", **common))
    memory_utils.action_record(_namespace(title="记忆系统边界约定", content="B", **common))

    files = list((tmp_path / ".specify/memory/knowledge").glob("*.md"))
    assert len(files) == 2  # two distinct CJK titles -> two distinct files (no overwrite)

    # re-recording an identical CJK title upserts rather than adding a third file
    memory_utils.action_record(_namespace(title="记忆系统边界约定", content="B2", **common))
    files = list((tmp_path / ".specify/memory/knowledge").glob("*.md"))
    assert len(files) == 2


def test_knowledge_upsert_merges_tags(tmp_path: Path):
    common = dict(action="record", workspace_root=str(tmp_path), scope="knowledge",
                  source="skill:study-project", title="Team convention")
    memory_utils.action_record(_namespace(content="First", tags="style", **common))
    result = memory_utils.action_record(_namespace(content="Second", tags="review", **common))

    knowledge_dir = tmp_path / ".specify/memory/knowledge"
    files = list(knowledge_dir.glob("*.md"))
    assert len(files) == 1  # same slug -> single file (upsert)

    meta, body = memory_utils.parse_frontmatter(files[0].read_text(encoding="utf-8"))
    assert set(meta["tags"]) == {"style", "review"}
    assert "Second" in body

    index = json.loads((knowledge_dir / "index.json").read_text(encoding="utf-8"))
    assert len(index["entries"]) == 1


# --------------------------------------------------------------------------- #
# Recall
# --------------------------------------------------------------------------- #
def test_recall_ranks_by_keyword_overlap(tmp_path: Path):
    memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                           scope="session", source="/speckit.plan",
                                           title="Auth uses JWT tokens", content="jwt jwt",
                                           tags="auth"))
    memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                           scope="session", source="/speckit.plan",
                                           title="Database schema", content="postgres tables"))

    result = memory_utils.action_recall(_namespace(workspace_root=str(tmp_path),
                                                   scope="session", query="jwt auth"))
    assert result["matches"], "expected at least one match"
    assert "Auth" in result["matches"][0]["title"]
    # keyword-less entry must be excluded when a query is provided
    assert all("Database" not in m["title"] for m in result["matches"])


def test_recall_filters_by_tag_and_feature(tmp_path: Path):
    memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                           scope="session", source="/speckit.plan",
                                           title="A", content="body", tags="alpha", feature="001"))
    memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                           scope="session", source="/speckit.plan",
                                           title="B", content="body", tags="beta", feature="002"))

    by_tag = memory_utils.action_recall(_namespace(workspace_root=str(tmp_path),
                                                   scope="session", tags="alpha"))
    assert {m["title"] for m in by_tag["matches"]} == {"A"}

    by_feature = memory_utils.action_recall(_namespace(workspace_root=str(tmp_path),
                                                       scope="session", feature="002"))
    assert {m["title"] for m in by_feature["matches"]} == {"B"}


def test_recall_all_scope_spans_both_dirs(tmp_path: Path):
    memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                           scope="session", source="/speckit.plan",
                                           title="Session note", content="widget"))
    memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                           scope="knowledge", source="skill:x",
                                           title="Knowledge note", content="widget"))
    result = memory_utils.action_recall(_namespace(workspace_root=str(tmp_path),
                                                   scope="all", query="widget"))
    scopes = {m["scope"] for m in result["matches"]}
    assert scopes == {"session", "knowledge"}


# --------------------------------------------------------------------------- #
# Prune + reindex
# --------------------------------------------------------------------------- #
def test_prune_keeps_only_max_entries(tmp_path: Path):
    for i in range(5):
        memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                               scope="session", source="/speckit.plan",
                                               title=f"note-{i}", content=f"body {i}"))
    # ensure distinct created ordering is not required; index sorts by created desc
    result = memory_utils.action_prune(_namespace(action="prune", workspace_root=str(tmp_path),
                                                  scope="session", max_entries=2))
    assert result["remaining"] == 2
    remaining_files = list((tmp_path / ".specify/memory/session").glob("*.md"))
    assert len(remaining_files) == 2


def test_prune_requires_a_limit(tmp_path: Path):
    with pytest.raises(memory_utils.MemoryError):
        memory_utils.action_prune(_namespace(action="prune", workspace_root=str(tmp_path),
                                             scope="session"))


def test_reindex_rebuilds_from_files(tmp_path: Path):
    memory_utils.action_record(_namespace(action="record", workspace_root=str(tmp_path),
                                           scope="knowledge", source="skill:x",
                                           title="Durable", content="body", tags="k"))
    index_file = tmp_path / ".specify/memory/knowledge/index.json"
    index_file.unlink()  # simulate corruption/loss

    result = memory_utils.action_reindex(_namespace(action="reindex", workspace_root=str(tmp_path),
                                                    scope="knowledge"))
    assert result["reindexed"]["knowledge"] == 1
    rebuilt = json.loads(index_file.read_text(encoding="utf-8"))
    assert rebuilt["entries"][0]["title"] == "Durable"
    assert rebuilt["entries"][0]["tags"] == ["k"]


# --------------------------------------------------------------------------- #
# CLI entrypoint
# --------------------------------------------------------------------------- #
def test_main_record_then_recall(tmp_path: Path, capsys):
    rc = memory_utils.main([
        "--action", "record", "--workspace-root", str(tmp_path),
        "--scope", "session", "--source", "/speckit.implement",
        "--title", "CLI smoke", "--content", "widget factory",
    ])
    assert rc == 0
    capsys.readouterr()

    rc = memory_utils.main([
        "--action", "recall", "--workspace-root", str(tmp_path),
        "--scope", "session", "--query", "widget", "--format", "json",
    ])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["count"] == 1
    assert payload["matches"][0]["title"] == "CLI smoke"


def test_main_rejects_invalid_source(tmp_path: Path, capsys):
    rc = memory_utils.main([
        "--action", "record", "--workspace-root", str(tmp_path),
        "--scope", "session", "--source", "not-a-command",
        "--title", "x", "--content", "y",
    ])
    assert rc == 2
    assert "Invalid --source" in capsys.readouterr().err
