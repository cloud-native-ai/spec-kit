"""Contract test: Feedback Entry & Store file schema.

Enforces ``contracts/feedback-entry-schema.md`` for Feature 028:
frontmatter fields; body has ``## Review`` + ``## Optimization Points`` with
>=1 bullet; ``scope: local``; ``<YYYYMMDDTHHMMSSZ>-<unit-slug>.md`` naming;
``entries`` sorted ``created`` desc; ``count_since_submission`` invariant;
``reindex`` preserves ``submitted_at``.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

FILENAME_RE = re.compile(r"^\d{8}T\d{6}Z-[a-z0-9-]+\.md$")


def _record(workspace_root: Path, **kw):
    args = [
        "--action", "record", "--workspace-root", str(workspace_root),
        "--unit-id", kw.get("unit_id", "/speckit.plan"),
        "--unit-type", kw.get("unit_type", "command"),
        "--run-id", kw.get("run_id", "schema-run"),
        "--review", kw.get("review", "A prose review of the run."),
        "--points", kw.get("points", "One optimization point"),
    ]
    if kw.get("feature"):
        args += ["--feature", kw["feature"]]
    if kw.get("partial"):
        args += ["--partial"]
    return feedback_utils.main(args)


@pytest.mark.contract
def test_entry_file_frontmatter_and_body(feedback_store: Path):
    _record(feedback_store, unit_id="/speckit.plan", run_id="fm-run",
            feature="027-feedback-mechanism")
    files = list((feedback_store / ".specify/memory/feedback").glob("*.md"))
    entry = next(f for f in files if f.name != ".gitkeep")
    meta, body = feedback_utils.parse_frontmatter(entry.read_text(encoding="utf-8"))

    assert meta["unit_id"] == "/speckit.plan"
    assert meta["unit_type"] == "command"
    assert meta["run_id"] == "fm-run"
    assert meta["scope"] == "local"
    assert meta["feature"] == "027-feedback-mechanism"
    assert meta["partial"] is False
    assert "created" in meta and meta["created"].endswith("Z")
    assert "summary" in meta
    # body has both required sections with >=1 bullet
    assert "## Review" in body
    assert "## Optimization Points" in body
    bullets = [ln for ln in body.splitlines() if ln.strip().startswith("- ")]
    assert len(bullets) >= 1


@pytest.mark.contract
def test_entry_filename_convention(feedback_store: Path):
    _record(feedback_store, unit_id="skill:analysis-project", unit_type="skill",
            run_id="name-run")
    files = [f for f in (feedback_store / ".specify/memory/feedback").glob("*.md")]
    assert files
    for f in files:
        assert FILENAME_RE.match(f.name), f.name
        assert "skill-analysis-project" in f.name


@pytest.mark.contract
def test_scope_is_always_local(feedback_store: Path):
    _record(feedback_store, unit_id="/speckit.tasks", run_id="scope-run")
    files = [f for f in (feedback_store / ".specify/memory/feedback").glob("*.md")]
    for f in files:
        meta, _ = feedback_utils.parse_frontmatter(f.read_text(encoding="utf-8"))
        assert meta["scope"] == "local"


@pytest.mark.contract
def test_index_entries_sorted_created_desc(feedback_store: Path):
    _record(feedback_store, unit_id="/speckit.plan", run_id="r1")
    _record(feedback_store, unit_id="/speckit.tasks", run_id="r2")
    _record(feedback_store, unit_id="/speckit.implement", run_id="r3")
    index = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    assert index["store"] == "feedback"
    created = [e["created"] for e in index["entries"]]
    assert created == sorted(created, reverse=True)


@pytest.mark.contract
def test_count_since_submission_invariant(feedback_store: Path):
    _record(feedback_store, unit_id="/speckit.plan", run_id="c1")
    _record(feedback_store, unit_id="/speckit.tasks", run_id="c2")
    index = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    assert index["count_since_submission"] == 2


@pytest.mark.contract
def test_partial_run_labels_review(feedback_store: Path):
    _record(feedback_store, unit_id="/speckit.implement", run_id="partial-run",
            review="Only setup completed.", partial=True)
    files = [f for f in (feedback_store / ".specify/memory/feedback").glob("*.md")]
    entry = next(f for f in files if "partial-run" not in f.name or True)
    text = entry.read_text(encoding="utf-8")
    meta, body = feedback_utils.parse_frontmatter(text)
    assert meta["partial"] is True
    review_section = body.split("## Optimization Points")[0]
    assert "**Partial run**" in review_section


@pytest.mark.contract
def test_reindex_preserves_submitted_at(feedback_store: Path):
    _record(feedback_store, unit_id="/speckit.plan", run_id="ri1")
    feedback_utils.main([
        "--action", "mark-submitted", "--workspace-root", str(feedback_store),
    ])
    index_before = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    submitted_at = index_before["submitted_at"]
    assert submitted_at is not None

    feedback_utils.main([
        "--action", "reindex", "--workspace-root", str(feedback_store),
    ])
    index_after = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    assert index_after["submitted_at"] == submitted_at
