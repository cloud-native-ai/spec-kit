"""Per-test team-tree builder and read-only snapshot oracle for Feature 103 (team view).

Every tree is created under pytest ``tmp_path``; nothing here writes ``.specify/teams/``
(R-13, FR-021, SC-002). The builder emits the closed-subset frontmatter the view reads —
scalars, inline lists, nested maps (bounded depth) and block sequences of maps — and can be
told to emit the two named corrupt variants instead.

Two helpers are shared by all four test files:
``build_team(root, slug, ...)`` -> the created team directory;
``snapshot(root)`` -> ``{relative_path: sha256}`` for the read-only oracle.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

DEFAULT_MATRIX_HEADER = ("role", "stage", "type", "agent", "lifecycle", "responsibility")

DEFAULT_BODY = """## Goal

Fixture goal used by the team-view tests.

## Static Structure

| role | stage | type | agent | lifecycle | responsibility |
|------|-------|------|-------|-----------|----------------|
| executor | executor | Worker | agent-a | temporary | produce the fixture artifact |
| evaluator | evaluator | Worker | agent-b | temporary | verify the fixture artifact |

## Dynamic Structure

**Pattern**: serial — one fixture stage, quality-first handoff.

## Self-Improvement Contract

- Subject: this persisted fixture team definition.
"""


def _scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    needs_quotes = (
        text == ""
        or text.strip() != text
        or any(ch in text for ch in ':#[]{},"\'')
    )
    return json.dumps(text, ensure_ascii=False) if needs_quotes else text


def _inline(value) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(_inline(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(
            "%s: %s" % (key, _inline(item)) for key, item in value.items()
        ) + "}"
    return _scalar(value)


def render_frontmatter(data: dict) -> str:
    """Render a dict as the closed-subset YAML the team view's parser accepts."""
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append("%s:" % key)
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    lines.append("  %s:" % sub_key)
                    for deep_key, deep_value in sub_value.items():
                        lines.append("    %s: %s" % (deep_key, _inline(deep_value)))
                else:
                    lines.append("  %s: %s" % (sub_key, _inline(sub_value)))
        elif isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
            lines.append("%s:" % key)
            for item in value:
                first = True
                for item_key, item_value in item.items():
                    prefix = "  - " if first else "    "
                    if isinstance(item_value, dict):
                        lines.append("%s%s:" % (prefix, item_key))
                        for deep_key, deep_value in item_value.items():
                            lines.append("      %s: %s" % (deep_key, _inline(deep_value)))
                    else:
                        lines.append("%s%s: %s" % (prefix, item_key, _inline(item_value)))
                    first = False
        else:
            lines.append("%s: %s" % (key, _inline(value)))
    return "\n".join(lines) + "\n"


def default_frontmatter(slug: str) -> dict:
    return {
        "slug": slug,
        "name": "Fixture Team %s" % slug,
        "description": "Fixture team built by team_view_fixtures",
        "pattern": "serial",
        "lifecycle_state": "active",
        "created": "2026-01-01",
        "updated": "2026-01-02",
        "binding": {"owner": "human", "owner_id": "human", "origin": slug},
        "members": [
            {"agent": "agent-a", "role": "executor", "lifecycle": "temporary"},
            {"agent": "agent-b", "role": "evaluator", "lifecycle": "temporary"},
        ],
        "config": {"isolation": "none"},
    }


def build_team(
    root,
    slug: str,
    *,
    frontmatter=None,
    body=None,
    reports=(),
    items_lines=(),
    spine=(),
    corrupt=None,
) -> Path:
    """Create ``<root>/.specify/teams/<slug>/`` and return the team directory.

    ``frontmatter`` is a dict (rendered by :func:`render_frontmatter`) or raw text written
    verbatim between the ``---`` fences. ``reports`` holds ``(name, text)`` pairs written
    under ``runs/``. ``items_lines`` entries are dicts (JSON-encoded) or raw strings,
    one line each in ``items.jsonl``. ``spine`` names empty continuous-operating files.
    ``corrupt`` is ``None``, ``"missing-team-md"`` (directory only) or
    ``"unparseable-frontmatter"`` (a ``team.md`` whose frontmatter is outside the subset).
    """
    root = Path(root)
    team_dir = root / ".specify" / "teams" / slug
    team_dir.mkdir(parents=True, exist_ok=True)

    if corrupt == "missing-team-md":
        return team_dir
    if corrupt == "unparseable-frontmatter":
        (team_dir / "team.md").write_text(
            "---\nslug: [unclosed\nmembers: {tabs:\tbroken\n---\n\n## Goal\n\nbroken\n",
            encoding="utf-8",
        )
        return team_dir
    if corrupt is not None:
        raise ValueError("unknown corrupt variant: %r" % (corrupt,))

    if frontmatter is None:
        frontmatter_text = render_frontmatter(default_frontmatter(slug))
    elif isinstance(frontmatter, str):
        frontmatter_text = frontmatter.rstrip("\n") + "\n"
    else:
        frontmatter_text = render_frontmatter(frontmatter)
    body_text = DEFAULT_BODY if body is None else body
    (team_dir / "team.md").write_text(
        "---\n" + frontmatter_text + "---\n\n" + body_text, encoding="utf-8"
    )

    if reports:
        runs = team_dir / "runs"
        runs.mkdir(parents=True, exist_ok=True)
        for name, text in reports:
            (runs / name).write_text(text, encoding="utf-8")

    if items_lines:
        rendered = []
        for entry in items_lines:
            if isinstance(entry, dict):
                rendered.append(json.dumps(entry, ensure_ascii=False))
            else:
                rendered.append(str(entry))
        (team_dir / "items.jsonl").write_text("\n".join(rendered) + "\n", encoding="utf-8")

    for name in spine:
        (team_dir / name).write_text("", encoding="utf-8")

    return team_dir


def report_text(
    *,
    outcome: str = "completed",
    target: str | None = None,
    result_summary: str | None = "Fixture result summary.",
    verification: str | None = "Fixture verification.",
    nested_runs: str | None = None,
    anomalies: str | None = None,
) -> str:
    """A report body in the report-contract shape; ``None`` omits the optional segment."""
    lines = [
        "# Team Run Report: Fixture",
        "",
        "- **Team**: fixture · **Goal**: fixture-goal · **Pattern**: serial · "
        "**Outcome**: %s" % outcome,
        "- **Target 指派**: %s" % (target if target is not None else "无（goal 整体）"),
        "",
    ]
    if result_summary is not None:
        lines += ["## Result Summary", "", result_summary, ""]
    if verification is not None:
        lines += ["## Verification", "", verification, ""]
    if nested_runs is not None:
        lines += ["## Nested SDD Runs", "", nested_runs, ""]
    if anomalies is not None:
        lines += [
            "- outcome: completed · artifact paths: fixture · evidence paths: fixture · "
            "routing-verdict reference: missing · anomalies: %s" % anomalies,
            "",
        ]
    return "\n".join(lines)


def snapshot(root) -> dict:
    """``{relative_path: sha256}`` over every file under ``root`` (the read-only oracle)."""
    root = Path(root)
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }
