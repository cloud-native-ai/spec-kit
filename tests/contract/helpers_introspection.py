"""Shared fixtures for req-047 introspection contract tests."""

from __future__ import annotations

import json
from pathlib import Path

from tests.script_api import feedback_utils


def _record(workspace: Path, run_id: str, kind: str | None = None) -> str:
    """Record one feedback entry and return its id."""
    rc = feedback_utils.main([
        "--action", "record", "--workspace-root", str(workspace),
        "--unit-id", "/speckit.plan", "--unit-type", "command",
        "--run-id", run_id, "--review", f"review for {run_id}",
        "--points", "point",
    ])
    assert rc == 0
    index = json.loads(
        (workspace / ".specify/memory/feedback/index.json").read_text())
    eid = index["entries"][-1]["id"]
    if kind:  # simulate an external entry by patching kind end-to-end
        entry_file = workspace / ".specify/memory/feedback" / index["entries"][-1]["file"]
        text = entry_file.read_text(encoding="utf-8")
        entry_file.write_text(text.replace('kind: ""', f'kind: "{kind}"'),
                              encoding="utf-8")
        index["entries"][-1]["kind"] = kind
        (workspace / ".specify/memory/feedback/index.json").write_text(
            json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return eid


def _report_text(report_id: str, entries: list[str], excluded: list[str] | None = None,
                 findings_extra: str = "", supersedes: str | None = None,
                 status: str = "draft") -> str:
    excluded = excluded or []
    member_lines = ", ".join(f"{e}(成立)" for e in entries)
    excluded_lines = "\n".join(f"- {e} — 排除理由" for e in excluded) or "无"
    sup = f'"{supersedes}"' if supersedes else "null"
    return f"""---
id: "{report_id}"
created: "2026-08-28T00:00:00Z"
status: "{status}"
scope_filter: "disposition=open"
scope_entries: {json.dumps(entries + excluded)}
supersedes: {sup}
confirmed_at: null
---

# Introspection Report: {report_id}

## Findings

### F-01: 问题陈述

- **根因**: 根因陈述
- **证据锚点**: templates/commands/plan.md:10
- **成员条目**: {member_lines}
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 方案
{findings_extra}
## Excluded

{excluded_lines}
"""


def _write_report(workspace: Path, report_id: str, text: str,
                  subdir: bool = True) -> Path:
    base = workspace / ".specify/memory/feedback"
    if subdir:
        base = base / "introspection"
        base.mkdir(parents=True, exist_ok=True)
    path = base / f"{report_id}.md"
    path.write_text(text, encoding="utf-8")
    return path
