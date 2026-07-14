"""Contract test: no dangling `organize-agents` references in active source paths (SC-004).

Enforces migration contract M6 / M7.1. The legacy skill name `organize-agents` must
not appear anywhere in the authoritative source tree after the rename to `create-team`.

Scope of the literal scan (the "active, non-archived" source SC-004 governs —
"documentation, registries, skill bodies, symlinks"):
  skills/, templates/, docs/, agents/, src/, memory/, top-level *.md,
  tests/scenarios/ (structural routing data, NOT test code), and the canonical
  runtime memory .specify/memory/ (minus the append-only historical records below).

Deliberately excluded (with rationale, so the certified scope matches SC-004):
  - tests/ EXCEPT tests/scenarios/ — test *modules* reference the literal in
    assertions (like this one). Structural scenario data under tests/scenarios/
    IS scanned because it encodes live routing tables.
  - Append-only HISTORICAL RECORDS, analogous to the "historical spec archives"
    SC-004 explicitly excludes: .specify/specs/*, .specify/memory/features.md,
    .specify/memory/features/**, .specify/memory/session/**,
    .specify/memory/knowledge/**. These legitimately describe the rename as
    provenance ("create-team (renamed from organize-agents)").
  - The .specify/skills/ runtime mirror — covered instead by the dedicated
    parity test below (a stale mirror is a structural, not a textual, defect).
  - symlinks — compatibility aliases (AGENTS.md, CLAUDE.md, ...) that resolve to
    regenerated files.
  - per-tool generated command dirs (.qoder/, .claude/, .github/, .opencode/,
    .qwen/, .hermes/, .iflow/) — regenerated from templates/commands/.
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

LEGACY_TOKEN = "organize-agents"

# Source-of-truth directories scanned in full.
ACTIVE_DIRS = ["skills", "templates", "docs", "agents", "src", "memory"]

# Additional active surfaces the previous scope missed (F1/F4):
#   - tests/scenarios: structural routing scenarios (live pointers, not test code)
#   - .specify/memory: the CANONICAL runtime memory (not the shipped default memory/)
EXTRA_DIRS = ["tests/scenarios", ".specify/memory"]

# Append-only historical records (relative-path prefixes, POSIX form). Excluded for
# the same reason SC-004 excludes historical spec archives.
HISTORICAL_RECORD_PREFIXES = (
    ".specify/specs/",
    ".specify/memory/features.md",
    ".specify/memory/features/",
    ".specify/memory/session/",
    ".specify/memory/knowledge/",
)


def _is_historical(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    return rel.startswith(HISTORICAL_RECORD_PREFIXES)


# Sanctioned exception: the CLI's obsolete-asset cleanup registry names legacy
# identifiers (like `organize-agents`) solely so init can delete them — a removal
# manifest, not a live reference. The region between these markers is stripped
# before the literal scan, so the guardrail stays fully active everywhere else.
_REGISTRY_START = "OBSOLETE-ASSET-REGISTRY:START"
_REGISTRY_END = "OBSOLETE-ASSET-REGISTRY:END"


def _strip_obsolete_registry(text: str) -> str:
    if _REGISTRY_START not in text or _REGISTRY_END not in text:
        return text
    kept, skipping = [], False
    for line in text.splitlines():
        if _REGISTRY_START in line:
            skipping = True
            continue
        if _REGISTRY_END in line:
            skipping = False
            continue
        if not skipping:
            kept.append(line)
    return "\n".join(kept)


def _iter_source_files():
    for d in ACTIVE_DIRS + EXTRA_DIRS:
        base = REPO_ROOT / d
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not (path.is_file() and not path.is_symlink()):
                continue
            if "__pycache__" in path.parts:
                continue
            if _is_historical(path):
                continue
            yield path
    for path in REPO_ROOT.glob("*.md"):
        if path.is_file() and not path.is_symlink():
            yield path


def _skill_dirs(root: Path):
    """Immediate sub-directories under `root` that contain a SKILL.md."""
    if not root.exists():
        return set()
    return {d.name for d in root.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()}


@pytest.mark.contract
class TestNoOrganizeAgentsRefs:
    def test_no_dangling_reference(self):
        offenders = []
        for path in _iter_source_files():
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if LEGACY_TOKEN in _strip_obsolete_registry(text):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        assert not offenders, (
            f"'{LEGACY_TOKEN}' still referenced in active source paths: {sorted(offenders)}"
        )

    def test_skills_mirror_parity(self):
        """The .specify/skills/ runtime mirror must match the canonical skills/ tree
        (F6): no stale `organize-agents`, and the renamed/new team skills present.

        A directory-level parity check — a stale mirror is what silently ships the
        wrong skill set at runtime even when the canonical tree is correct.
        """
        canonical = _skill_dirs(REPO_ROOT / "skills")
        mirror_root = REPO_ROOT / ".specify" / "skills"
        if not mirror_root.exists():
            pytest.skip(".specify/skills/ mirror not present (fresh checkout / pre-install)")
        mirror = _skill_dirs(mirror_root)

        assert LEGACY_TOKEN not in mirror, (
            f"stale '{LEGACY_TOKEN}' skill still present in .specify/skills/ mirror"
        )
        assert {"create-team", "improve-team"} <= mirror, (
            "team skills missing from .specify/skills/ mirror: "
            f"{sorted({'create-team', 'improve-team'} - mirror)}"
        )
        assert canonical == mirror, (
            "skills/ ↔ .specify/skills/ mirror drift — "
            f"only in canonical: {sorted(canonical - mirror)}; "
            f"only in mirror: {sorted(mirror - canonical)}"
        )
