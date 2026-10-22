"""Contract test: non-entity probe catalog (Feature 056 / US1, data-model §3).

The catalog chapter collects code-internal micro-probes as pure pointers
(path + one-line semantics). Hard constraints:
- every entry's path MUST resolve on disk (pointer reachability);
- entries MUST NOT restate behavior rules (One Source of Truth) — enforced as
  a one-line shape plus a length ceiling;
- the catalog MUST NOT participate in registry counting — catalog entries stay
  pure pointers and never become Objects.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.script_api import ROOT, probe_utils
DEFS = ROOT / "shared" / "definitions" / "probe-definitions.md"
CATALOG_HEADING = "非实体 probe 目录"

# Pinned drift-detector: real code-internal micro-probes (paths existence-checked
# at authoring time, 2026-10-13). A path that stops existing turns the test red.
EXPECTED_ENTRIES: dict[str, str] = {
    "scripts/bash/check-prerequisites.sh": "writability",
    "scripts/python/derive-utils.py": "probe-links",
    "scripts/python/sanitize-utils.py": "probe-roots",
    "scripts/python/validate-tasks.py": "read-only governor",
    "scripts/python/clause_extract.py": "mutual-exclusion",
}
ENTRY_RE = re.compile(r"^- `([^`]+)` — (.+)$", re.MULTILINE)


def _catalog_section(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"## {CATALOG_HEADING}":
            start = i + 1
            break
    if start is None:
        return ""
    body: list[str] = []
    for line in lines[start:]:
        if line.strip().startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def test_catalog_section_exists() -> None:
    text = DEFS.read_text(encoding="utf-8")
    body = _catalog_section(text)
    assert body.strip(), f"missing '## {CATALOG_HEADING}' chapter in probe-definitions.md"


def test_catalog_entries_are_reachable_pointers() -> None:
    text = DEFS.read_text(encoding="utf-8")
    body = _catalog_section(text)
    entries = dict(ENTRY_RE.findall(body))
    missing = sorted(set(EXPECTED_ENTRIES) - set(entries))
    assert not missing, f"catalog missing pointer entries: {missing}"
    for rel in sorted(EXPECTED_ENTRIES):
        assert (ROOT / rel).is_file(), f"catalog pointer target does not exist: {rel}"


def test_catalog_entries_match_expected_probe_semantics() -> None:
    text = DEFS.read_text(encoding="utf-8")
    body = _catalog_section(text)
    entries = dict(ENTRY_RE.findall(body))
    for rel, marker in sorted(EXPECTED_ENTRIES.items()):
        assert marker in entries.get(rel, ""), (
            f"catalog entry for {rel} must name micro-probe '{marker}'"
        )


def test_catalog_entries_stay_pointer_shaped() -> None:
    text = DEFS.read_text(encoding="utf-8")
    body = _catalog_section(text)
    for raw in body.splitlines():
        line = raw.strip()
        if not line.startswith("- "):
            continue
        m = ENTRY_RE.match(line)
        assert m, f"catalog entry is not a pure pointer (path + one-line semantics): {line!r}"
        assert len(m.group(2)) <= 120, f"catalog semantics line too long (rule restatement risk): {line!r}"


def test_catalog_does_not_participate_in_registry_counts() -> None:
    registry = probe_utils.load_probe_registry(ROOT)
    internal = len(registry["objects"])
    external = len(registry["external"])
    assert registry["errors"] == [], f"registry structural errors: {registry['errors']}"
    assert external == 0, "external probes must stay out of the framework registry"
    # 72 既有 + 14 散布探测点入册 + 20 reconcile 缺口补登 + 057 新增 2 个 skill-wrapup Object + 059 新增 4 个 exec-quant Object（同任务更新计数契约）
    # stale-pin update (067 T025, 2026-10-22): 112 -> 116; +4 Objects registered by
    # pre-067 features (063 evidence/gate objects etc.; the engine-loaded registry
    # already holds 116 at branch point 7f9033ec, errors-free at HEAD).
    assert internal == 116, (
        f"catalog leaked into the engine population or Objects drifted: internal={internal}"
    )
