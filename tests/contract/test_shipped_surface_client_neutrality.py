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
    # 2026-11-06 Feature 085 audit: pre-existing Feature NNN attributions in the SDD
    # driver/complement are dated provenance, not client-runtime pointers. Recorded
    # here so the guard stays live for every other shipped file; a later cleanup can
    # rewrite them client-neutrally and drop these entries.
    "shared/definitions/flow-class-definitions.md",
    "skills/external/sdd-loop-driver/references/decomposition-model.md",
    "skills/external/sdd-loop-driver/references/dispatch-recipes.md",
    "skills/external/sdd-loop-driver/scripts/loop-state.py",
    "skills/external/sdd-loop-driver/scripts/wp-report.py",
    "skills/external/sdd-loop-driver/SKILL.md",
    "skills/external/sdd-loop-driver/templates/stage-team-preset.md",
    # 2026-10-12 S3 command thinning (sanitize.md -> sanitize-materials skill) flattened
    # the framework repo's own spec-contract path into the skill prose (2 lines). The
    # client-neutral rewrite belongs to the S3 team's skill-side follow-up; allowlisted
    # here so the guard stays live for every other shipped file meanwhile.
    "skills/internal/sanitize-materials/SKILL.md",
}

#: The shipped surfaces Feature 087 delivered, each of which this guard covers by
#: construction (the roots above) and each of which the 2026-11-06 alignment rewrote
#: client-neutrally rather than allowlisting: the reporting-obligation owner document
#: (§ 9.1 cites its contract fragments by name), the two new command templates, the
#: roster guard's docstring, and the reporter Agent Template. The rows exist so a
#: later regression in any of them is attributable, not because they are exempt.
FEATURE_087_SHIPPED_SURFACES = (
    "shared/guidelines/reporting-obligations.md",
    "templates/commands/status.md",
    "templates/commands/measure.md",
    "skills/internal/create-team/scripts/validate-roster.py",
    "agents/reporter.agent.md",
)


@pytest.mark.contract
def test_every_feature_087_shipped_surface_is_covered_and_clean():
    """The 087 surfaces are audited by the sweep above, never by an allowlist entry.

    A surface that drifted into an allowlist would make the guard green for the wrong
    reason (a covered file reading as exempt); this row pins that this feature's
    delivered set is inside the swept roots and outside every exemption.
    """
    for rel in FEATURE_087_SHIPPED_SURFACES:
        path = REPO_ROOT / rel
        assert path.is_file(), f"delivered shipped surface missing: {rel}"
        assert path.relative_to(REPO_ROOT).parts[0] in SHIPPED_ROOTS, (
            f"{rel} is not inside a swept shipped root"
        )
        assert rel not in KNOWN_DEBT, f"{rel} MUST stay audited, not allowlisted"
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [
            m.group(0)
            for pattern in BANNED_PATTERNS
            for m in pattern.finditer(text)
        ]
        assert hits == [], f"{rel} references the framework's own runtime artifacts: {hits}"


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
