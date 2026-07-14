"""Integration test (US1): a skill records a local feedback entry.

Recording a skill feedback step writes a ``scope: local``, ``unit_type: skill``
entry referencing the skill purpose with >=1 optimization point (or the explicit
no-op sentence).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

pytestmark = pytest.mark.integration


def test_skill_record_writes_local_skill_entry(feedback_store: Path):
    rc = feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "skill:analysis-project", "--unit-type", "skill",
        "--run-id", "analysis-20260714T1000",
        "--review", "Reviewed my own run against my stated purpose (deep project analysis).",
        "--points", "Cache repeated file reads to speed up large repos",
    ])
    assert rc == 0

    files = [
        f for f in (feedback_store / ".specify/memory/feedback").glob("*.md")
    ]
    assert len(files) == 1
    meta, body = feedback_utils.parse_frontmatter(files[0].read_text(encoding="utf-8"))
    assert meta["scope"] == "local"
    assert meta["unit_type"] == "skill"
    assert meta["unit_id"] == "skill:analysis-project"
    assert "## Review" in body and "## Optimization Points" in body
    bullets = [ln for ln in body.splitlines() if ln.strip().startswith("- ")]
    assert len(bullets) >= 1


def test_skill_record_accepts_no_op_sentence(feedback_store: Path):
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "skill:draw-plantuml", "--unit-type", "skill",
        "--run-id", "clean-run",
        "--review", "Clean run against the diagram-authoring purpose.",
        "--points", "No significant optimization points identified this run.",
    ])
    index = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    assert index["entries"][0]["unit_type"] == "skill"
    assert index["count_since_submission"] == 1
