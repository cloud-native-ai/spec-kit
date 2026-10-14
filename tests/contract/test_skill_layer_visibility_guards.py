"""Contract guards for the two-layer skills visibility split (goal skill-layer-install-separation, criterion 2).

Guard 1 — 平铺发现面只注册 external: a one-level scan of the runtime skills root
(``.specify/skills/*/SKILL.md``) must only ever surface external-layer skills; the
nested ``internal/`` subtree contributes nothing to that face.

Guard 2 — internal 路径可解析: every internal-layer skill must be resolvable via its
explicit nested path ``.specify/skills/internal/<name>/SKILL.md``, and no internal
name may appear flat at the discovery root.

Both guards carry anti-vacuous sentinels (non-empty discovery set, existing internal
subtree) and a red-first drill: the same check functions are exercised on a synthetic
mini-tree in a broken state (must report) and a fixed state (must not), so a green
real-tree run is known to be discriminating.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SKILLS = ROOT / ".specify" / "skills"

# Pinned census (classification v3): 11 external / 35 internal. These literals are a
# drift detector for the split — update only together with the classification record.
# 17 -> 11 on 2026-10-12: the six draw-* engine skills were merged into draw-diagram as
# internal engine layers under draw-diagram/references/types/<engine>/ (capability
# inheritance recorded in that skill's references/merge-provenance.md), so they are no
# longer independently discovered skills.
# 15 -> 35 on 2026-10 (S3 command thinning): the executable logic of twenty /speckit.*
# commands moved into command-carrier internal skills (analyze-artifacts, create-plan,
# manage-constitution, ...), all nesting under .specify/skills/internal/<name>/ and
# none surfacing on the flat discovery face — which is exactly what these guards pin.
EXTERNAL_SKILLS = {
    "create-docs", "improve-docs", "create-skills", "improve-skills", "create-pages",
    "database-utils", "document-utils", "draw-diagram", "merge-skills",
    "think-skills", "git-workspace",
}
INTERNAL_SKILLS = {
    "analyze-artifacts", "archive-session", "clarify-artifact", "code-review",
    "collect-evidence", "create-agent", "create-checklist", "create-plan",
    "create-requirements", "create-tasks", "create-team", "create-tools",
    "derive-architecture", "implement-feature", "improve-agent", "improve-team",
    "improve-tools", "manage-agents", "manage-constitution", "manage-features",
    "manage-feedback", "manage-goal", "manage-history", "manage-instructions",
    "manage-todo", "memory-recall", "memory-record", "research-feature",
    "review-sdd-process", "run-agent", "run-interview", "sanitize-materials",
    "self-improvement", "study-project", "summarize-project",
}


def flat_discovery_names(skills_root: Path) -> list[str]:
    """One-level discovery: every dir at the root exposing a SKILL.md."""
    return sorted(
        d.name
        for d in skills_root.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )


def flat_discovery_offenders(skills_root: Path, allowed: set[str]) -> tuple[list[str], list[str]]:
    seen = flat_discovery_names(skills_root)
    return seen, [n for n in seen if n not in allowed]


def internal_resolution_gaps(
    skills_root: Path, internal_names: set[str]
) -> tuple[list[str], list[str]]:
    """Returns (missing nested paths, flat leaks at the discovery root)."""
    missing = [
        n for n in sorted(internal_names)
        if not (skills_root / "internal" / n / "SKILL.md").is_file()
    ]
    flat_leaks = [n for n in sorted(internal_names) if (skills_root / n).exists()]
    return missing, flat_leaks


# ---------------------------------------------------------------------------
# Standing guards on the real tree
# ---------------------------------------------------------------------------

def test_flat_discovery_surfaces_external_layer_only():
    seen, offenders = flat_discovery_offenders(RUNTIME_SKILLS, EXTERNAL_SKILLS)
    # Sentinels: the face is non-empty and the exclusion is meaningful.
    assert len(seen) == 11, (
        f"flat discovery saw {len(seen)} skills, expected exactly the 11 external "
        f"ones — a count both proves non-vacuity and pins the split: {seen}"
    )
    internal_dir = RUNTIME_SKILLS / "internal"
    assert internal_dir.is_dir(), "internal/ subtree missing — guard 1's exclusion is vacuous"
    internal_nested = [d for d in internal_dir.iterdir() if (d / "SKILL.md").is_file()]
    # 35 既有 + 057 run-skills（Phase 3 落地）= 36；T012 落 run-team 后由同任务更新为 37
    assert len(internal_nested) == 36, (
        f"internal subtree carries {len(internal_nested)} skills, expected 36 — "
        f"guard 1 only proves something when internal skills actually exist"
    )
    assert offenders == [], f"flat discovery leaked non-external skills: {offenders}"


def test_internal_skills_resolve_by_explicit_path_only():
    missing, flat_leaks = internal_resolution_gaps(RUNTIME_SKILLS, INTERNAL_SKILLS)
    assert missing == [], (
        f"internal skills not resolvable via .specify/skills/internal/<name>/SKILL.md: {missing}"
    )
    assert flat_leaks == [], (
        f"internal skills leaked into the flat discovery root (would be registered): {flat_leaks}"
    )


# ---------------------------------------------------------------------------
# Red-first drills: the check functions must go red on a broken tree.
# ---------------------------------------------------------------------------

def _mk_skill(path: Path, name: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")


def test_drill_flat_discovery_red_then_green(tmp_path: Path):
    skills_root = tmp_path / ".specify" / "skills"
    _mk_skill(skills_root / "demo-ext", "demo-ext")
    _mk_skill(skills_root / "internal" / "demo-int", "demo-int")

    seen, offenders = flat_discovery_offenders(skills_root, {"demo-ext"})
    assert seen == ["demo-ext"] and offenders == [], "baseline drill tree must be green"

    _mk_skill(skills_root / "rogue-skill", "rogue-skill")  # break: a non-external flat dir
    seen, offenders = flat_discovery_offenders(skills_root, {"demo-ext"})
    assert offenders == ["rogue-skill"], "broken tree must surface the rogue flat skill (red)"

    shutil.rmtree(skills_root / "rogue-skill")  # fix
    _, offenders = flat_discovery_offenders(skills_root, {"demo-ext"})
    assert offenders == [], "restored tree must go green again"


def test_drill_internal_resolution_red_then_green(tmp_path: Path):
    skills_root = tmp_path / ".specify" / "skills"
    _mk_skill(skills_root / "demo-ext", "demo-ext")
    _mk_skill(skills_root / "internal" / "demo-int", "demo-int")

    missing, flat_leaks = internal_resolution_gaps(skills_root, {"demo-int"})
    assert missing == [] and flat_leaks == [], "baseline drill tree must be green"

    shutil.rmtree(skills_root / "internal" / "demo-int")  # break: nested path gone
    missing, _ = internal_resolution_gaps(skills_root, {"demo-int"})
    assert missing == ["demo-int"], "broken tree must report the unresolvable internal (red)"

    _mk_skill(skills_root / "internal" / "demo-int", "demo-int")  # fix
    actual = None
    actual = skills_root / "demo-int"
    _mk_skill(actual, "demo-int")  # also simulate a flat copy leak
    missing, flat_leaks = internal_resolution_gaps(skills_root, {"demo-int"})
    assert missing == [] and flat_leaks == ["demo-int"], (
        "nested restored but flat leak present must red-lines the flat-leak half"
    )
    shutil.rmtree(actual)
    missing, flat_leaks = internal_resolution_gaps(skills_root, {"demo-int"})
    assert missing == [] and flat_leaks == [], "fully restored tree must go green again"
