"""Contract tests for 069a US3 — compatibility & distribution (T028).

Owns the compatibility face of
``.specify/specs/069a-flow-classification-docs-gates/contracts/compatibility-distribution.md``
that ``tasks.md`` T028 names, plus the three US3 invariants the slice must keep
mechanically checkable (stage integrity does not read the class; a class may
never be read as a permission to skip / shorten / reclassify a stage; the
unrefreshed form has no call sites at all):

* **C-1 zero new commands** — ``templates/commands/`` holds exactly the frozen
  27 command templates (count *and* name set), and no command file exists below
  a subdirectory; ``skills/{external,internal}/*/SKILL.md`` holds exactly the
  frozen 52 skill units (51 at the 069a baseline; 2026-10-30 Feature 078 renames
  one of them in place, so the count is unchanged).
* **C-2 zero project-side storage** — nothing under ``.specify/memory/`` is a
  second classification store (no classification-named file, no ledger-style
  row, no ``flow_class`` assignment).
* **C-3 one-package atomicity** — the four payload classes (``shared/``,
  ``scripts/``, ``templates/``, ``skills/``) ship from the same wheel: the
  first three through ``pyproject.toml`` ``force-include``, ``skills/``
  through ``src/hatch_build.py`` staging.
* **C-4 unrefreshed form** — at the pre-change HEAD the two command templates
  and the two skills carry **no** call site; the wiring exists only in the
  current tree, so an unrefreshed project behaves exactly as before.
* **C-5 wiring surface is closed** — the 25 non-wiring templates and 49
  non-wiring skills reference neither engine nor either owner document; the 74
  non-wiring sources keep the sha256 recorded in
  ``notes/pre-change-file-hashes.txt``; ``src/specify_cli/``, ``AGENTS.md`` and
  ``.specify/instructions.md`` are untouched relative to the baseline.
* **C-6 additive one-line pointer** — ``shared/workflow/feedback-step.md``
  gains exactly one added line (the orthogonal-axis pointer) and loses
  nothing: the pre-existing complexity criterion and red-line paragraphs are
  byte-identical.
* **C-7 mirrors** — every one of the seven owned sources that has a mirror is
  byte-identical to it. The four new payloads may still be mirror-absent at
  US3 (their mirrors land in T033); a mirror that exists MUST never drift, so
  no mirror can be hand-edited and none can silently disappear.
* **C-9 earlier specs** — 062 / 067 / 068 ``requirements.md`` stay
  byte-identical (SC-008).
* **Stage integrity** — the stage-integrity section of the gate owner reads no
  class key and no lookup; the skip/shorten/reclassify triad appears exactly
  once in the two owner documents and that one occurrence is the rejection
  rule, stated without exception.

Red-first (Constitution IV): the two ``C-6`` legs fail until T029 adds the
pointer line — everything else pins invariants US1/US2 already established, so
its job is to catch a regression of the compatibility surface, not to be red
for its own sake. Failure messages name the frozen value and the contract
clause, never a bare assertion.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "069a-flow-classification-docs-gates"
HASH_MANIFEST = SPEC_DIR / "notes" / "pre-change-file-hashes.txt"

# The slice's pre-change baseline (notes/pre-change-measurements.md § header).
PRE_CHANGE_HEAD = "01d1feaa08d4541be2b59af30aa8c2e87128e55a"

COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SKILLS_DIR = REPO_ROOT / "skills"
MEMORY_DIR = REPO_ROOT / ".specify" / "memory"

CLASS_OWNER = "shared/definitions/flow-class-definitions.md"
GATE_OWNER = "shared/workflow/expression-gates.md"
FEEDBACK_STEP = REPO_ROOT / "shared" / "workflow" / "feedback-step.md"

# The wiring surface (C-5): the only four files allowed to name an engine/owner.
WIRING_TEMPLATES = ("docs.md", "humanize.md")
# 2026-10-30 Feature 077 widens the closed surface by the seven stage templates —
# the same proposition ("only a designated roster names the engine or an owner"),
# a larger roster. Kept apart from WIRING_TEMPLATES because the frozen-hash leg
# above still means "069a's 25-template non-wiring complement".
POST_077_WIRING_TEMPLATES = (
    "requirements.md",
    "clarify.md",
    "plan.md",
    "tasks.md",
    "checklist.md",
    "analyze.md",
    "implement.md",
)
WIRING_SKILLS = (
    "skills/external/create-docs/SKILL.md",
    "skills/external/humanize/SKILL.md",
)

# C-1 frozen denominator: 27 command templates (stem == `/speckit.<stem>`).
FROZEN_COMMANDS = (
    "agents",
    "analyze",
    "checklist",
    "clarify",
    "constitution",
    "derive",
    "docs",
    "feature",
    "feedback",
    "goal",
    "history",
    "humanize",
    "implement",
    "improve",
    "instructions",
    "interview",
    "plan",
    "requirements",
    "research",
    "review",
    "sanitize",
    "session",
    "skills",
    "tasks",
    "team",
    "todo",
    "tools",
)

# C-1 frozen denominator: 52 skill units, layer-qualified so a layer move or a
# rename is a failure rather than a silent re-count.
#
# 2026-10-30 (Feature 078): the pre-existing external mental-simulation unit is
# renamed to `coaching-skills` in place (FR-001/FR-018). The roster therefore swaps
# one name for another and the count stays 52 = 15 external + 37 internal — a
# name change is recorded here deliberately, not re-counted as a new skill. The
# retired literal is not written in this file: these four frozen rosters are
# inside A10's closed surface, where SC-006 permits it exactly once (the CLI
# upgrade-registry entry), so the hash-manifest handoff below derives it instead.
FROZEN_SKILLS = (
    "external/coaching-skills",
    "external/create-docs",
    "external/create-pages",
    "external/create-skills",
    "external/database-utils",
    "external/document-utils",
    "external/draw-diagram",
    "external/git-utils",
    "external/humanize",
    "external/improve-docs",
    "external/improve-skills",
    "external/merge-skills",
    "external/sdd-house-keeping",
    "external/sdd-loop-driver",
    "external/sdd-project-setup",
    "internal/analyze-artifacts",
    "internal/archive-session",
    "internal/clarify-artifact",
    "internal/code-review",
    "internal/collect-evidence",
    "internal/create-agent",
    "internal/create-checklist",
    "internal/create-plan",
    "internal/create-requirements",
    "internal/create-tasks",
    "internal/create-team",
    "internal/create-tools",
    "internal/derive-architecture",
    "internal/implement-feature",
    "internal/improve-agent",
    "internal/improve-team",
    "internal/improve-tools",
    "internal/manage-agents",
    "internal/manage-constitution",
    "internal/manage-features",
    "internal/manage-feedback",
    "internal/manage-goal",
    "internal/manage-history",
    "internal/manage-instructions",
    "internal/manage-todo",
    "internal/memory-recall",
    "internal/memory-record",
    "internal/research-feature",
    "internal/review-sdd-process",
    "internal/run-agent",
    "internal/run-interview",
    "internal/run-skills",
    "internal/run-team",
    "internal/sanitize-materials",
    "internal/self-improvement",
    "internal/study-project",
    "internal/summarize-project",
)

# C-5: no engine, no owner document may be named outside the wiring surface.
ENGINE_OR_OWNER_TOKENS = (
    "flow-class-check.py",
    "expression-gates.md",
    "doc-consistency-check.py",
    "flow-class-definitions.md",
)

# SC-008 frozen hashes (notes/pre-change-measurements.md § 5).
FROZEN_SPEC_HASHES = {
    ".specify/specs/062-humanize-command/requirements.md":
        "987b24ea1f98abb2a01d14779814eab28416f4ad1cbd81a36d51efb72d5f9da0",
    ".specify/specs/067-loop-efficiency-hardening/requirements.md":
        "29e26b701ebef9d80782b9a215ef97759290a384d898cb3320cfedde161fa0cd",
    ".specify/specs/068-exec-quant-feedback-channel/requirements.md":
        "ec20d5e28bd0eb5e2afdbd851cb753ef6e1c37a1c24e66b196f9305f18b45af7",
}

# C-7: the seven owned sources and their mirror targets (mirror paths follow
# sync-mirrors.py MIRROR_PAIRS: shared -> .specify/shared, scripts ->
# .specify/scripts, skills/external -> .specify/skills flat).
MIRROR_PAIRS = {
    "shared/definitions/flow-class-definitions.md":
        ".specify/shared/definitions/flow-class-definitions.md",
    "shared/workflow/expression-gates.md":
        ".specify/shared/workflow/expression-gates.md",
    "shared/workflow/feedback-step.md":
        ".specify/shared/workflow/feedback-step.md",
    "scripts/python/flow-class-check.py":
        ".specify/scripts/python/flow-class-check.py",
    "scripts/python/doc-consistency-check.py":
        ".specify/scripts/python/doc-consistency-check.py",
    "skills/external/create-docs/SKILL.md":
        ".specify/skills/create-docs/SKILL.md",
    "skills/external/humanize/SKILL.md":
        ".specify/skills/humanize/SKILL.md",
}

# The four new payloads whose mirrors land in T033 (Polish). Absence is allowed
# for exactly these; any other absent mirror is a regression.
NEW_PAYLOAD_SOURCES = frozenset({
    "shared/definitions/flow-class-definitions.md",
    "shared/workflow/expression-gates.md",
    "scripts/python/flow-class-check.py",
    "scripts/python/doc-consistency-check.py",
})

LEDGER_ROW_RE = re.compile(
    r"^\s*\|\s*`?(?:/speckit\.[a-z0-9-]+|skill:[a-z0-9-]+)`?\s*\|\s*"
    r"(?:execution|expression)\s*\|"
)
CLASS_ASSIGN_RE = re.compile(
    r"""flow_class["']?\s*[:=]\s*["']?(?:execution|expression)\b"""
)
CLASS_FILE_NAME_RE = re.compile(r"(flow[-_]?class|classification)", re.IGNORECASE)

# Stage-skip vocabulary and the only acceptable polarity for a mention.
SKIP_TRIAD = ("跳过", "缩短", "改判")
SKIP_TOKENS = ("跳过", "缩短", "改判")
SKIP_LATIN_TOKENS = ("skip", "exempt")
# A mention is acceptable only when it forbids the move (or states that no
# exception exists). A permission-shaped sentence carries none of these.
NEGATION_MARKERS = (
    "拒绝",
    "MUST NOT",
    "不得",
    "无例外",
    "不豁免",
    "不把",
    "不因",
    "不被",
    "不构成",
    "不改变",
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "expected file missing: %s" % path.relative_to(REPO_ROOT)
    return path.read_text(encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(REPO_ROOT), capture_output=True, text=True
    )


def _git_show(rev_path: str) -> str:
    """Content of ``<rev>:<path>``; a missing object is a hard failure.

    A silent skip here would turn "the unrefreshed form has no call site" into a
    claim nobody checked, so the object is required.
    """
    proc = _git("show", rev_path)
    assert proc.returncode == 0, (
        "git object unavailable: %s — the compatibility face is anchored on the "
        "pre-change HEAD recorded in notes/pre-change-measurements.md (stderr: %r)"
        % (rev_path, proc.stderr)
    )
    return proc.stdout


def _section(text: str, heading: str) -> str:
    """Body of the ``## <heading>`` section, up to the next level-2 heading."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            continue
        if start is not None and line.startswith("## "):
            return "\n".join(lines[start:index])
    assert start is not None, "section %r missing" % heading
    return "\n".join(lines[start:])


def _hash_manifest() -> dict[str, str]:
    text = _read(HASH_MANIFEST)
    entries: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.match(r"^([0-9a-f]{64})  (.+)$", line)
        assert match, "malformed manifest line: %r" % line
        entries[match.group(2)] = match.group(1)
    return entries


# --------------------------------------------------------------------------- #
# C-5 retired-path register (2026-10-30, Feature 078 rename)
# --------------------------------------------------------------------------- #
# 069a's hash manifest is a dated record and is not rewritten, so it still lists
# the skill source that Feature 078 renamed; that path no longer exists on disk.
# The register derives the retired side mechanically from the manifest (the unique
# entry gone from disk) and states only the *new* name as the mapping target — the
# retired literal is never spelled here, because these rosters sit inside A10's
# closed wiring surface, where SC-006 permits it exactly once (the CLI upgrade-
# registry entry). Exactly one manifest path may be gone, otherwise the mapping
# stops being decidable, so the freeze keeps catching drift instead of degrading
# into an empty assertion (plan § Decision Tensions T-001).
RENAMED_SKILL_REL = "skills/external/coaching-skills/SKILL.md"


def _retired_skill_register(manifest: dict[str, str]) -> dict[str, str]:
    missing = sorted(rel for rel in manifest if not (REPO_ROOT / rel).is_file())
    assert len(missing) == 1, (
        "the retired-path register expects exactly one manifest entry gone from "
        "disk (the 2026-10-30 Feature 078 rename); got %r" % missing
    )
    retired = missing[0]
    assert (REPO_ROOT / retired).parent.parent == (
        REPO_ROOT / RENAMED_SKILL_REL
    ).parent.parent, "a rename must stay inside its layer: %s -> %s" % (
        retired,
        RENAMED_SKILL_REL,
    )
    return {retired: RENAMED_SKILL_REL}


# --------------------------------------------------------------------------- #
# C-1 — zero new commands / frozen inventories
# --------------------------------------------------------------------------- #
def test_c1_zero_new_commands():
    template_files = sorted(COMMANDS_DIR.glob("*.md"))
    stems = sorted(path.stem for path in template_files)
    assert stems == sorted(FROZEN_COMMANDS), (
        "command template name set drifted (C-1: zero new / renamed / deleted "
        "commands). expected %d, found %d; symmetric difference: %r"
        % (
            len(FROZEN_COMMANDS),
            len(stems),
            sorted(set(stems) ^ set(FROZEN_COMMANDS)),
        )
    )
    nested = sorted(
        path.relative_to(COMMANDS_DIR).as_posix()
        for path in COMMANDS_DIR.rglob("*")
        if path.is_file() and path.parent != COMMANDS_DIR
    )
    assert not nested, (
        "command files must be flat under templates/commands/ (C-1); found: %r" % nested
    )


def test_c1_skill_inventory_is_frozen():
    found = sorted(
        "%s/%s" % (layer, directory.name)
        for layer in ("external", "internal")
        for directory in (SKILLS_DIR / layer).iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    )
    assert found == sorted(FROZEN_SKILLS), (
        "skill inventory drifted (C-1: zero new / renamed / deleted skills). "
        "expected %d, found %d; symmetric difference: %r"
        % (
            len(FROZEN_SKILLS),
            len(found),
            sorted(set(found) ^ set(FROZEN_SKILLS)),
        )
    )
    orphans = sorted(
        directory.relative_to(SKILLS_DIR).as_posix()
        for layer in ("external", "internal")
        for directory in (SKILLS_DIR / layer).iterdir()
        if directory.is_dir() and not (directory / "SKILL.md").is_file()
    )
    assert not orphans, (
        "skill directories without SKILL.md would escape the inventory (C-1): %r"
        % orphans
    )


# --------------------------------------------------------------------------- #
# C-5 — non-wiring sources keep their frozen bytes; framework paths untouched
# --------------------------------------------------------------------------- #
# The historical pre-change hash stays untouched. This allowlist names every
# post-baseline drift with its reason AND the markers its intended content must
# still carry, so the guard keeps working in both directions: a drift not named
# here stays red, and a named drift is re-asserted on content instead of being
# waved through. Each entry is measured against its own markers — a marker list
# shared by every entry would let one file's content vouch for another's.
#
# 2026-10-25: a later fix legitimately edits one non-wiring source — the loop
# driver gained the per-window iteration token (Qoder duplicate-call guard).
# 2026-10-27 (Feature 071): the review × code-review composition legitimately
# edits two more — the command template gains its composition and applicability
# triage sections (FR-001/FR-003/FR-008) and the code-review skill body gains the
# renderer-absence rewrite plus the `receipt --review-file` path (FR-013/FR-023).
# Both are declared surfaces of Feature 071 and are pinned by
# `tests/contract/test_review_code_composition.py`, `test_code_review_skill_contract.py`
# and `test_coverage_receipt.py`; this entry records the drift, it does not
# authorize any other.
ALLOWED_POST_BASELINE_CHANGES = {
    "skills/internal/create-team/SKILL.md": {
        "reason": "2026-10-29 Feature 074b adds the mandatory `## Nested SDD Runs` report section (report contract)",
        "markers": ("## Nested SDD Runs", "Nested SDD Runs section"),
    },
    "skills/internal/run-agent/SKILL.md": {
        "reason": "2026-10-29 Feature 074a wires the pre-dispatch governance probe to sdd-route.py authorize",
        "markers": ("sdd-invocation", "authorize"),
    },
    "skills/external/sdd-loop-driver/SKILL.md": {
        "reason": "2026-10-25 watch iteration token (Hard Requirement 9; watch-model §3.2)",
        "markers": ("监听签名唯一", "--iter"),
    },
    "templates/commands/review.md": {
        "reason": (
            "2026-10-27 Feature 071 composes the review command's two segments "
            "(FR-008 gate ownership; FR-001/FR-003 the composed surface): the "
            "`## Composition` and `## Applicability triage` sections are that "
            "feature's declared surfaces, pinned by "
            "tests/contract/test_review_code_composition.py"
        ),
        "markers": ("## Composition", "## Applicability triage"),
    },
    "skills/internal/code-review/SKILL.md": {
        "reason": (
            "2026-10-27 Feature 071 rewrites the renderer-absence clause instead of "
            "deleting it (FR-013) and adds the `receipt --review-file` step (FR-023), "
            "pinned by tests/contract/test_code_review_skill_contract.py and "
            "tests/contract/test_coverage_receipt.py"
        ),
        "markers": ("renderer: text", "receipt --review-file"),
    },
    "skills/internal/review-sdd-process/SKILL.md": {
        "reason": (
            "2026-10-27 Feature 071 rewrites the sibling-skill boundary wording: "
            "\"the two are unrelated, keep them separate\" is false once "
            "`/speckit.review` composes both, so the skill declares its own judgment "
            "object and the command's fixed order instead (FR-025 / C-29), pinned by "
            "tests/contract/test_code_review_skill_contract.py"
        ),
        "markers": ("judgment object", "fixed order"),
    },
    # 2026-10-27 (Feature 072, client self-improvement): four more non-wiring
    # sources gain their declared 072 segments — the two command templates and
    # two skill bodies named in C-56's edit surface. Compatibility plan +
    # non-precedential declaration: .specify/specs/072-client-self-improvement/
    # notes/compatibility-plan-c61.md and .specify/memory/features/072.md. Each
    # drift is pinned by a Feature 072 contract suite, cited per entry; this
    # records the drift, it does not authorize any other.
    "templates/commands/feedback.md": {
        "reason": (
            "2026-10-27 Feature 072 extends the Path A reference bullet with the "
            "client carrier-assignment closure (exactly three carriers, one per "
            "entry, undecided reported) and the read-only client-metrics pointer "
            "(FR-021/FR-026), pinned by "
            "tests/contract/test_client_package_exclusion.py"
        ),
        "markers": ("载体指派闭集恰三", "client-metrics"),
    },
    "templates/commands/improve.md": {
        "reason": (
            "2026-10-27 Feature 072 adds the custom-subject why segment (observation "
            "source and fail-closed run-determination disclosure) to the target "
            "section (FR-016/FR-017), pinned by "
            "tests/contract/test_client_improve_loop.py"
        ),
        "markers": ("Custom-subject why segment", "运行判定历史未评估"),
    },
    "skills/internal/manage-feedback/SKILL.md": {
        "reason": (
            "2026-10-27 Feature 072 adds A4's carrier assignment for digested client "
            "entries and the one-per-entry client carrier rule (contracts "
            "digest-and-carriers.md C-26/C-27), pinned by "
            "tests/contract/test_client_package_exclusion.py"
        ),
        "markers": ("Client carriers are one-per-entry", "exactly one"),
    },
    "skills/internal/self-improvement/SKILL.md": {
        "reason": (
            "2026-10-27 Feature 072 adds the custom-subject observation-source "
            "bullet (the engine's source contract fail-closes for custom units, so "
            "the why segment discloses 运行判定历史未评估), pinned by "
            "tests/contract/test_client_improve_loop.py"
        ),
        "markers": ("Custom-subject observation source", "运行判定历史未评估"),
    },
    # 2026-10-29 renumber lane (sanitize --lane renumber): two non-wiring skills
    # gain the one sanctioned exception to their "never renumber" rule —
    # duplicate-ID collision repair, which only re-labels a duplicated definition.
    # Pinned by tests/contract/test_sanitize_renumber_lane.py and
    # tests/unit/test_renumber_engine.py.
    "skills/internal/create-tasks/SKILL.md": {
        "reason": (
            "2026-10-29 renumber lane: the rerun contract names its sole exception "
            "(duplicate-ID collision repair by /speckit.sanitize --lane renumber) "
            "so the append-only rule stops reading as absolute"
        ),
        "markers": ("one sanctioned exception", "/speckit.sanitize --lane renumber"),
    },
    "skills/internal/implement-feature/SKILL.md": {
        "reason": (
            "2026-10-29 renumber lane: the append-tasks directive names the same "
            "sole exception, scoped to a duplicated definition"
        ),
        "markers": ("one sanctioned exception", "/speckit.sanitize --lane renumber"),
    },
    # 2026-10-27 Directory Governance amendment (trunk): two non-wiring skills
    # legitimately gained their Directory Governance segments; each entry carries
    # the needles its change must contain.
    "skills/external/sdd-project-setup/SKILL.md": {
        "reason": "2026-10-27 Directory Governance (Hard Requirements 10-11)",
        "markers": ("目标项目治理优先", "目录创建限于规范落点"),
    },
    "skills/internal/manage-constitution/SKILL.md": {
        "reason": "2026-10-27 Directory Governance MUST-include entry (Principle XVII)",
        "markers": ("Directory Governance (Named, Documented, Ignored When Temporary)",),
    },
    "skills/internal/sanitize-materials/SKILL.md": {
        "reason": "2026-10-27 Feature 073 record-retention lane (sanitize --lane retention)",
        "markers": ("--lane materials|retention|renumber|all", "record-retention.py", "Receipt red line"),
    },
    "templates/commands/sanitize.md": {
        "reason": "2026-10-27 Feature 073 record-retention lane entry and delegation",
        "markers": ("--lane materials|retention|renumber|all", "record-retention.py", "renumber-utils.py"),
    },
    # 2026-10-28 trunk fix(sdd-loop-driver): read-only stages account for the
    # wrap-up bookkeeping entries; the analyze surface scopes its read-only
    # promise to artifacts. Both are non-wiring sources and are pinned by
    # tests/contract/test_sdd_loop_driver_wrapup_accounting.py.
    "skills/internal/analyze-artifacts/SKILL.md": {
        "reason": "2026-10-28 trunk: read-only on artifacts + wrap-up bookkeeping exception",
        "markers": ("strictly read-only on artifacts", "wrap-up engine entries"),
    },
    "templates/commands/analyze.md": {
        "reason": "2026-10-28 trunk: analyze command read-only-on-artifacts wording",
        "markers": ("read-only **on artifacts**", "Wrap-up bookkeeping entries"),
    },
    # 2026-10-30 (Feature 078): the rename touches two non-wiring sources inside
    # 069a's non-wiring complement — the `/speckit.skills` route table (one
    # modify-family row repointed, five rows kept) and the run-skills skill's
    # routing pointer. Both are declared edit surfaces of Feature 078 (FR-019 /
    # FR-022) and are pinned by tests/contract/test_coaching_wiring_contract.py;
    # this records the drift, it does not authorize any other.
    "templates/commands/skills.md": {
        "reason": "2026-10-30 Feature 078 repoints the modify-family route row at the coaching skill",
        "markers": ("coaching-skills", "skills/external/coaching-skills/SKILL.md"),
    },
    "skills/internal/run-skills/SKILL.md": {
        "reason": "2026-10-30 Feature 078 updates the run-skills routing-family pointer",
        "markers": ("coaching-skills",),
    },
}

# 2026-10-30 Feature 077 stage-wiring amendment. 069a's manifest is that slice's
# window record ("the slice may only touch W1-W4"); it stays at 74 sources with its
# 25/49 counts untouched. 077 legitimately wires seven further stage templates, so
# each records itself here with the content its card must carry — the same
# mechanism the two entries above use, and the reason this leg still proves
# "no unannounced edit" rather than "no edit ever".
for _stage in ("requirements", "clarify", "plan", "tasks", "checklist",
               "analyze", "implement"):
    ALLOWED_POST_BASELINE_CHANGES["templates/commands/%s.md" % _stage] = {
        "reason": "2026-10-30 Feature 077 stage-wiring: one class-read card per stage",
        "markers": ("spec:<spec 目录名>", "--action lookup", "owner-unavailable"),
    }

# The historical baseline stays; a later amendment that legitimately edits an
# untouchable path records itself here with the content it must carry.
ALLOWED_POST_BASELINE_PATHS = {
    ".specify/instructions.md": (
        "2026-10-27 Directory Governance pointer in the Temporary Directory Discipline section",
        ("directory-governance.md",),
    ),
    "src/specify_cli/__init__.py": (
        "2026-10-29 Feature 074a adds the sdd-invocation neutral key and its validator allowlist",
        ("sdd-invocation", "NEUTRAL_AGENT_METADATA_KEYS"),
    ),
}


def test_c5_non_wiring_files_keep_their_frozen_hashes():
    manifest = _hash_manifest()
    templates = [rel for rel in manifest if rel.startswith("templates/commands/")]
    skills = [rel for rel in manifest if rel.startswith("skills/")]
    assert len(manifest) == 74, "hash manifest must cover 74 sources, found %d" % len(manifest)
    assert len(templates) == 25, "hash manifest must cover 25 templates, found %d" % len(templates)
    assert len(skills) == 49, "hash manifest must cover 49 skills, found %d" % len(skills)
    assert not any(rel.endswith(tuple(WIRING_TEMPLATES)) for rel in templates), (
        "the manifest is the NON-wiring complement; it still lists a wiring template"
    )
    assert not any(rel in WIRING_SKILLS for rel in skills), (
        "the manifest is the NON-wiring complement; it still lists a wiring skill"
    )

    # 2026-10-30 (Feature 078): the one renamed skill source is resolved through
    # the register above, then re-asserted on content at its new path — the
    # manifest entry itself stays untouched as 069a's dated record.
    retired = _retired_skill_register(manifest)

    drifted: list[str] = []
    missing: list[str] = []
    for rel, expected in sorted(manifest.items()):
        if rel in retired:
            continue
        path = REPO_ROOT / rel
        if not path.is_file():
            missing.append(rel)
            continue
        if _sha256(path) != expected:
            if rel in ALLOWED_POST_BASELINE_CHANGES:
                continue
            drifted.append(rel)
    assert not missing, (
        "non-wiring source disappeared (C-5, zero new commands/skills): %r" % missing
    )
    assert not drifted, (
        "non-wiring source changed (C-5: the slice may only touch W1-W4 and the "
        "feedback-step pointer). drifted: %r" % drifted
    )
    for retired_rel, replacement_rel in retired.items():
        assert not (REPO_ROOT / retired_rel).exists(), (
            "the retired source came back at its manifest path: %s" % retired_rel
        )
        replacement = _read(REPO_ROOT / replacement_rel)
        for marker in ("name: coaching-skills", "classification: external"):
            assert marker in replacement, (
                "the replacement of %s must carry the rename's own content: %r "
                "missing from %s (2026-10-30, Feature 078)"
                % (retired_rel, marker, replacement_rel)
            )

    for rel, allowance in ALLOWED_POST_BASELINE_CHANGES.items():
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        for marker in allowance["markers"]:
            assert marker in text, (
                "allowed post-baseline change must carry its own intended content: "
                "%s is missing marker %r (%s)" % (rel, marker, allowance["reason"])
            )
        assert rel in manifest, (
            "%s is allowlisted but is not a manifest entry, so the freeze never "
            "covered it and the allowance is vacuous" % rel
        )


def test_c5_untouchable_framework_paths_are_unchanged():
    # Slice-scoped completion guard: it answers "did 069a touch these?" — a later
    # feature that legitimately edits them refreshes its own baseline record.
    proc = _git(
        "diff",
        "--name-only",
        PRE_CHANGE_HEAD,
        "--",
        "src/specify_cli",
        "AGENTS.md",
        ".specify/instructions.md",
    )
    assert proc.returncode == 0, "git diff failed: %r" % proc.stderr
    changed = [
        line.strip() for line in proc.stdout.splitlines()
        if line.strip() and line.strip() not in ALLOWED_POST_BASELINE_PATHS
    ]
    assert not changed, (
        "paths the slice must not touch changed relative to %s: %r"
        % (PRE_CHANGE_HEAD[:8], changed)
    )
    for rel, (reason, needles) in ALLOWED_POST_BASELINE_PATHS.items():
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        missing = [needle for needle in needles if needle not in text]
        assert not missing, (
            "allowed post-baseline path change must carry its intended content: %s (%s); "
            "missing %r" % (rel, reason, missing)
        )


# --------------------------------------------------------------------------- #
# C-2 — zero project-side classification storage
# --------------------------------------------------------------------------- #
def test_c2_no_project_side_classification_store():
    offenders: list[str] = []
    for path in sorted(MEMORY_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        if CLASS_FILE_NAME_RE.search(path.name):
            offenders.append("%s — classification-named file" % rel)
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if LEDGER_ROW_RE.match(line):
                offenders.append("%s:%d — ledger-style unit/class row" % (rel, number))
            elif CLASS_ASSIGN_RE.search(line):
                offenders.append("%s:%d — flow_class assignment" % (rel, number))
    assert not offenders, (
        "C-2: no classification data may be stored project-side (the ledger is "
        "the owner document, delivered with shared/). found:\n- "
        + "\n- ".join(offenders)
    )


# --------------------------------------------------------------------------- #
# C-5 — the wiring surface is closed
# --------------------------------------------------------------------------- #
def test_c5_wiring_surface_is_closed():
    offenders: list[str] = []
    for path in sorted(COMMANDS_DIR.glob("*.md")):
        if path.name in WIRING_TEMPLATES + POST_077_WIRING_TEMPLATES:
            continue
        text = path.read_text(encoding="utf-8")
        offenders.extend(
            "%s -> %s" % (path.relative_to(REPO_ROOT).as_posix(), token)
            for token in ENGINE_OR_OWNER_TOKENS
            if token in text
        )
    for skill_file in sorted(SKILLS_DIR.glob("external/*/SKILL.md")) + sorted(
        SKILLS_DIR.glob("internal/*/SKILL.md")
    ):
        if skill_file.relative_to(REPO_ROOT).as_posix() in WIRING_SKILLS:
            continue
        text = skill_file.read_text(encoding="utf-8")
        offenders.extend(
            "%s -> %s" % (skill_file.relative_to(REPO_ROOT).as_posix(), token)
            for token in ENGINE_OR_OWNER_TOKENS
            if token in text
        )
    assert not offenders, (
        "C-5: wiring is closed to W1-W4; extra references found:\n- "
        + "\n- ".join(offenders)
    )


# --------------------------------------------------------------------------- #
# C-4 — the unrefreshed form carries no call site
# --------------------------------------------------------------------------- #
def test_c4_unrefreshed_form_has_no_call_sites():
    targets = (
        "templates/commands/docs.md",
        "templates/commands/humanize.md",
    ) + WIRING_SKILLS
    tokens = ENGINE_OR_OWNER_TOKENS + ("--action lookup",)
    for rel in targets:
        old = _git_show("%s:%s" % (PRE_CHANGE_HEAD, rel))
        hits = [token for token in tokens if token in old]
        assert not hits, (
            "%s already carried %r at the pre-change HEAD — an unrefreshed "
            "project would then have a call site without the owner/engine (C-4)"
            % (rel, hits)
        )
    # Positive control: the same files DO carry the wiring now, so the check
    # above is measuring the slice's own addition rather than a constant.
    assert "flow-class-check.py" in _read(COMMANDS_DIR / "docs.md")
    assert "flow-class-check.py" in _read(SKILLS_DIR / "external" / "humanize" / "SKILL.md")


# --------------------------------------------------------------------------- #
# C-3 — one package carries all four payload classes
# --------------------------------------------------------------------------- #
def test_c3_payloads_ship_in_one_package():
    pyproject = _read(REPO_ROOT / "pyproject.toml")
    for payload in ("shared", "scripts", "templates"):
        pattern = r'^"%s"\s*=\s*"specify_cli/%s"' % (payload, payload)
        assert re.search(pattern, pyproject, re.MULTILINE), (
            "C-3: payload %r is not force-included in the wheel" % payload
        )
    hatch = _read(REPO_ROOT / "src" / "hatch_build.py")
    assert "_stage_skills" in hatch and '"specify_cli/skills"' in hatch, (
        "C-3: skills/ must ride the same wheel through the hatch_build staging copy"
    )


# --------------------------------------------------------------------------- #
# C-7 — mirrors never drift (the four new payloads may land in T033)
# --------------------------------------------------------------------------- #
def test_c7_mirrors_are_byte_identical():
    problems: list[str] = []
    for source_rel, mirror_rel in sorted(MIRROR_PAIRS.items()):
        source = REPO_ROOT / source_rel
        mirror = REPO_ROOT / mirror_rel
        assert source.is_file(), "owned source missing: %s" % source_rel
        if not mirror.is_file():
            if source_rel not in NEW_PAYLOAD_SOURCES:
                problems.append("%s — mirror disappeared" % mirror_rel)
            continue
        if source.read_bytes() != mirror.read_bytes():
            problems.append("%s — mirror differs from %s" % (mirror_rel, source_rel))
    assert not problems, (
        "C-7: mirrors are projections of the framework source, never hand-edited "
        "(absence is tolerated only for the four new payloads until T033):\n- "
        + "\n- ".join(problems)
    )


# --------------------------------------------------------------------------- #
# C-4 — the refreshed client shape resolves the owner it ships
# --------------------------------------------------------------------------- #
def _client_shape(tmp_path: Path) -> Path:
    """Materialise what ``specify init`` + the payload produce in a client project.

    Only ``.specify/`` exists: the engine at ``.specify/scripts/python/``, the
    owner at ``.specify/shared/definitions/`` and the skill at the flattened
    ``.specify/skills/create-docs/``. No source tree, no ``templates/``, no
    top-level ``skills/``.
    """
    client = tmp_path / "client"
    engine = client / ".specify" / "scripts" / "python" / "flow-class-check.py"
    engine.parent.mkdir(parents=True)
    shutil.copy2(REPO_ROOT / "scripts" / "python" / "flow-class-check.py", engine)
    owner = client / ".specify" / CLASS_OWNER
    owner.parent.mkdir(parents=True)
    shutil.copy2(REPO_ROOT / CLASS_OWNER, owner)
    skill = client / ".specify" / "skills" / "create-docs" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    shutil.copy2(
        REPO_ROOT / "skills" / "external" / "create-docs" / "SKILL.md", skill
    )
    return client


def _lookup(engine: Path, *args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(engine), "--action", "lookup", *args, "--format", "json"],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def test_c4_refreshed_client_shape_reads_the_delivered_owner(tmp_path):
    """C-4's refreshed state: the class must resolve from ``.specify/shared/…``.

    The shipped defect looked one directory too high (``<proj>/shared/…``), so
    every client call degraded to ``owner-unavailable`` + the default class.
    """
    client = _client_shape(tmp_path)
    engine = client / ".specify" / "scripts" / "python" / "flow-class-check.py"

    for extra in ([], ["--repo", str(client)]):
        proc = _lookup(engine, "--unit-id", "/speckit.docs", *extra, cwd=client)
        assert proc.returncode == 0, (
            "a refreshed client project must resolve its owner (args=%r); "
            "stderr=%r" % (extra, proc.stderr)
        )
        record = json.loads(proc.stdout)
        assert record.get("flow_class") == "expression", (
            "the ledger row must be read, not the default class: %r" % record
        )
        assert record.get("source") == "ledger", (
            "a registered unit in the delivered shape is ledger-sourced: %r" % record
        )
        assert "owner-unavailable" not in proc.stderr


def test_c4_client_shape_still_degrades_when_the_owner_is_absent(tmp_path):
    """Negative control: the fix must not turn a missing owner into a green read."""
    client = _client_shape(tmp_path)
    (client / ".specify" / CLASS_OWNER).unlink()
    engine = client / ".specify" / "scripts" / "python" / "flow-class-check.py"
    proc = _lookup(engine, "--unit-id", "/speckit.docs", cwd=client)
    assert proc.returncode == 2, "a genuinely absent owner is still exit 2"
    assert "owner-unavailable" in proc.stderr


# --------------------------------------------------------------------------- #
# C-9 — earlier specs stay byte-identical (SC-008)
# --------------------------------------------------------------------------- #
def test_c9_pre_completion_specs_stay_byte_identical():
    for rel, expected in FROZEN_SPEC_HASHES.items():
        path = REPO_ROOT / rel
        assert path.is_file(), "frozen spec missing: %s" % rel
        assert _sha256(path) == expected, (
            "SC-008: %s changed — 062 / 067 / 068 are referenced, never rewritten" % rel
        )


# --------------------------------------------------------------------------- #
# Stage integrity — no class read, skip/shorten/reclassify only as rejection
# --------------------------------------------------------------------------- #
def test_stage_integrity_section_reads_no_class():
    gates = _read(REPO_ROOT / GATE_OWNER)
    body = _section(gates, "## 阶段不变量")
    assert body.strip(), "the gate owner must carry a stage-integrity section"
    for token in ("flow_class", "flow-class-check.py", "--action lookup", "--unit-id"):
        assert token not in body, (
            "stage integrity MUST be judged from existing stage records, never "
            "from the class — found %r in the section" % token
        )
    assert "既有阶段记录" in body, (
        "the section must name the stage record as the judge"
    )
    assert re.search(r"analyze", body) and re.search(r"review", body), (
        "analyze and review must both be named as 100%% call-rate stages"
    )
    assert "100%" in body, "the 100%% call rate for analyze and review must be stated"


def test_stage_skip_claims_only_appear_as_rejection():
    owners = (REPO_ROOT / CLASS_OWNER, REPO_ROOT / GATE_OWNER)
    triad_hits: list[tuple[str, int, str]] = []
    permission_shaped: list[str] = []
    for owner in owners:
        rel = owner.relative_to(REPO_ROOT).as_posix()
        for number, line in enumerate(_read(owner).splitlines(), 1):
            lowered = line.lower()
            hits = [token for token in SKIP_TOKENS if token in line]
            hits += [token for token in SKIP_LATIN_TOKENS if token in lowered]
            # 豁免 counts only when it touches a stage or a gate (the class-neutral
            # exemption is a different subject and is owned by the ledger section).
            if "豁免" in line and re.search(r"阶段|门禁|gate|stage", line):
                hits.append("豁免")
            if not hits:
                continue
            if all(token in line for token in SKIP_TRIAD):
                triad_hits.append((rel, number, line.strip()))
            if not any(marker in line for marker in NEGATION_MARKERS):
                permission_shaped.append(
                    "%s:%d — %r (%r)" % (rel, number, line.strip(), hits)
                )
    assert not permission_shaped, (
        "a skip / shorten / reclassify mention must be forbidden, never permitted "
        "(FR-014):\n- " + "\n- ".join(permission_shaped)
    )
    assert len(triad_hits) == 1, (
        "the skip+shorten+reclassify triad must appear exactly once (the rejection "
        "rule); found %d: %r" % (len(triad_hits), triad_hits)
    )
    rel, number, line = triad_hits[0]
    assert "拒绝" in line and "无例外" in line, (
        "the single skip/shorten/reclassify occurrence must be the rejection rule "
        "stated without exception, found %s:%d — %r" % (rel, number, line)
    )
    assert rel == GATE_OWNER, (
        "the rejection rule belongs to the gate owner's stage invariants, found in %s" % rel
    )
    stages = _read(REPO_ROOT / GATE_OWNER)
    assert line in _section(stages, "## 阶段不变量"), (
        "the rejection rule must live in the gate owner's stage-integrity section"
    )


# --------------------------------------------------------------------------- #
# C-6 — the feedback-step orthogonal pointer (T029; red until it lands)
# --------------------------------------------------------------------------- #
def test_c6_feedback_step_declares_orthogonal_axes():
    text = _read(FEEDBACK_STEP)
    pointer_lines = [
        line for line in text.splitlines() if CLASS_OWNER in line
    ]
    assert pointer_lines, (
        "shared/workflow/feedback-step.md carries no pointer to %s — the "
        "complexity axis and the class axis must be declared orthogonal (FR-004 / "
        "C-6). Red is the pre-T029 state." % CLASS_OWNER
    )
    assert len(pointer_lines) == 1, (
        "the orthogonal pointer must be a single line, found %d: %r"
        % (len(pointer_lines), pointer_lines)
    )
    line = pointer_lines[0]
    lowered = line.lower()
    for token in ("orthogonal", "complexity", "gate operator"):
        assert token in lowered, (
            "the pointer line must state the orthogonal split (missing %r): %r"
            % (token, line)
        )
    assert "derived from each other" in lowered, (
        "the pointer line must forbid deriving one axis from the other: %r" % line
    )


def test_c6_feedback_step_edit_is_additive_single_line():
    proc = _git("diff", "-U0", PRE_CHANGE_HEAD, "--", "shared/workflow/feedback-step.md")
    assert proc.returncode == 0, "git diff failed: %r" % proc.stderr
    removed: list[str] = []
    added: list[str] = []
    for line in proc.stdout.splitlines():
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("-"):
            removed.append(line)
        elif line.startswith("+") and line[1:].strip():
            added.append(line[1:])
    assert not removed, (
        "C-6: the existing complexity criterion and red-line paragraphs must stay "
        "byte-identical — removed lines: %r" % removed
    )
    # 2026-10-28 trunk fix(sdd-loop-driver): a six-line additive "Feature
    # attribution" block joined the one 069a pointer line. The pin keeps its
    # additive-only intent: no existing line may be removed, and the additions
    # are exactly the pointer plus that block.
    assert len(added) == 7, (
        "C-6: the 069a pointer plus the 2026-10-28 feature-attribution block are "
        "the only additive lines; found %d: %r" % (len(added), added)
    )
    assert CLASS_OWNER in added[0], (
        "the first added line must point at %s: %r" % (CLASS_OWNER, added[0])
    )
    assert any("**Feature attribution.**" in line for line in added), (
        "the 2026-10-28 feature-attribution addition must be present: %r" % added
    )
