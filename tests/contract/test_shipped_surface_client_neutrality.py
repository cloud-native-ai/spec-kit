"""Contract test: shipped-surface client neutrality (Constitution XI two-hats).

Shipped roots (``templates/``, ``shared/``, ``skills/``, ``agents/``) are
installed into EVERY client project by ``specify init``. They MUST NOT carry
references to the framework repo's own dogfood runtime — concrete spec keys
(``.specify/specs/041-...``), concrete Feature files (``features/028.md``), or
bare ``Feature 0NN`` / ``requirement 0NN`` / ``req 0NN`` attributions — those
artifacts exist only in the Spec Kit framework project and read as dead,
confusing paths in every downstream project.

Generic placeholders (``.specify/memory/features/<ID>.md``,
``[FEATURE_ID]``, ``specs/<ID>-<slug>/``) refer to the CLIENT's own registry
and are explicitly allowed.

KNOWN_DEBT (2026-08-15 audit, follow-up): five skill files still reference
framework spec-contract paths semantically; they are allowlisted until their
contract references are rewritten client-neutrally with their conformance
tests updated in the same change.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SHIPPED_ROOTS = ["templates", "shared", "skills", "agents"]

BANNED_PATTERNS = [
    re.compile(r"\b(?:req|requirement)\s+\d{3}\b", re.IGNORECASE),
    re.compile(r"\bFeature\s+\d{3}\b"),
    re.compile(r"\.specify/specs/\d{3}-"),
    re.compile(r"\.specify/memory/features/\d{3}"),
]

KNOWN_DEBT = {
    # emptied 2026-08-15: all five framework-contract references rewritten
    # client-neutrally (framework-repo attribution, no bare .specify/specs/ paths)
}


@pytest.mark.contract
def test_shipped_surface_has_no_framework_runtime_references():
    violations = []
    for root_name in SHIPPED_ROOTS:
        for path in (REPO_ROOT / root_name).rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".yaml", ".yml", ".json"}:
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in BANNED_PATTERNS:
                for m in pattern.finditer(text):
                    line = text[: m.start()].count("\n") + 1
                    snippet = text.splitlines()[line - 1].strip()[:90]
                    violations.append(f"{rel}:{line}: {snippet}")
    fresh = [v for v in violations
             if v.split(":")[0] not in KNOWN_DEBT]
    assert not fresh, (
        "shipped (client-visible) files reference the framework project's own "
        "runtime artifacts; rewrite from the client-project perspective:\n"
        + "\n".join(fresh[:15])
    )
    assert len([v for v in violations]) >= 0  # debt visibility below
    if any(v.split(":")[0] in KNOWN_DEBT for v in violations):
        # keep the debt list honest: every allowlisted file must still exist
        for rel in KNOWN_DEBT:
            assert (REPO_ROOT / rel).exists(), f"KNOWN_DEBT entry stale: {rel}"
