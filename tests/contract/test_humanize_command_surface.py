"""Structural contract tests for the /speckit.humanize command surface (feature 062).

Owns the C-1..C-10 structural assertions of
``.specify/specs/062-humanize-command/contracts/command-surface.md`` — thin-entry
template shape, single-skill delegation, skill frontmatter + self-sufficiency,
generated per-tool copies, docs page content points, registry rows, the skill-side
probe unit + compiled Wrap-up face (Simple command ⇒ no command-side wrap-up),
zero-new-runtime-surface, the two downstream pinned tests' updated literals, and the
detector-honesty wording scan.

Red-Green discipline (Constitution IV, template-only form): this file landed BEFORE
the artifacts exist; red = an asserted path/literal is not there yet. Shared-String
literals below are pinned copies of the owner table in
``.specify/specs/062-humanize-command/requirements.md`` § Shared Strings — a
legitimate duplicate under the drift-detection rule of
``.specify/shared/guidelines/one-source-of-truth.md``.

C-4's baseline zero-drift leg (``regen-command-copies.py --check`` vs
``notes/baseline-regen-check.txt``) and C-9's full-suite ``comm -13`` leg are
runtime gates recorded in ``verification.md``, not in-test assertions.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

TEMPLATE = REPO_ROOT / "templates" / "commands" / "humanize.md"
SKILL_SRC = REPO_ROOT / "skills" / "external" / "humanize" / "SKILL.md"
SKILL_RUNTIME = REPO_ROOT / ".specify" / "skills" / "humanize" / "SKILL.md"
DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "commands" / "humanize.md"
COPIES = [
    REPO_ROOT / ".claude" / "commands" / "speckit.humanize.md",
    REPO_ROOT / ".github" / "prompts" / "speckit.humanize.prompt.md",
    REPO_ROOT / ".opencode" / "command" / "speckit.humanize.md",
    REPO_ROOT / ".qoder" / "commands" / "speckit.humanize.md",
]
REGISTRY = REPO_ROOT / ".specify" / "memory" / "features.md"
FEATURE_DETAILS = REPO_ROOT / ".specify" / "memory" / "features" / "062.md"
PROBE_DEFS = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
CONTRACT_027 = (
    REPO_ROOT / ".specify" / "specs" / "027-feedback-mechanism"
    / "contracts" / "command-classification.md"
)
BASELINE_FAILED = (
    REPO_ROOT / ".specify" / "specs" / "062-humanize-command"
    / "notes" / "baseline-failed-tests.txt"
)

# Shared Strings (pinned from requirements.md § Shared Strings).
STR_001 = "/speckit.humanize"
STR_002_VALUES = ("professional", "humorous", "empathetic", "colloquial")
STR_003_EXTS = (".md", ".markdown", ".txt")
STR_004_FLAGS = ("--tone", "--audience", "--file", "--inline", "--output", "--force")

DELEGATION_PATH = ".specify/skills/humanize/SKILL.md"
SKILL_ID_LITERAL = f'skill_id: "<SKILL:{DELEGATION_PATH}>"'

# Thinness: behavioral-detail keywords a thin entry must never restate
# (C-1: the FR-003..FR-006 workflow lives in the skill, not the template).
THIN_FORBIDDEN_DETAIL = ("rubric", "评审记录", "评分表", "盲评")


def _frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[:end] if end != -1 else ""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# C-1 — thin entry: frontmatter, sections, Simple shape, no workflow restate
# ---------------------------------------------------------------------------

def test_c01_thin_entry_shape():
    assert TEMPLATE.is_file(), f"thin command template missing: {TEMPLATE}"
    text = _read(TEMPLATE)
    fm = _frontmatter(text)
    assert "description:" in fm, "template frontmatter lacks description (trigger words)"
    assert "short-description:" in fm, "template frontmatter lacks short-description"
    assert "scripts:" not in fm, "template must not declare a scripts: block (Simple)"
    for section in ("## User Input", "## Glossary", "## Handoffs"):
        assert section in text, f"template body lacks {section}"
    assert "$ARGUMENTS" in text, "template lacks $ARGUMENTS wiring"
    assert "user-input-protocol" in text, "template lacks User Input Protocol reference"
    assert "FR-018" in text, "template lacks FR-018 call-syntax declaration pointer"
    assert "--" in text, "template lacks the -- option-termination declaration"
    for flag in STR_004_FLAGS:
        assert flag in text, f"template lacks call-syntax option {flag} (STR-004)"
    # Simple-class shape: no command-side wrap-up / feedback step at all.
    assert "## Wrap-up" not in text, "Simple command must not carry ## Wrap-up"
    assert "feedback-utils.py" not in text, "Simple command must not carry feedback step"
    assert "probe-utils.py" not in text, "Simple command must not carry a wrap-up face"
    assert STR_001 in text, f"template lacks the command identity literal {STR_001}"
    # Zero restatement of the FR-003..FR-006 behavioral details (C-1 thinness).
    body_lines = [ln for ln in text.splitlines() if not ln.startswith("|")]
    assert len(body_lines) <= 120, (
        f"template body has {len(body_lines)} non-table lines — thin entry exceeded"
    )
    lowered = text.lower()
    for word in THIN_FORBIDDEN_DETAIL:
        assert word not in lowered and word not in text, (
            f"template restates behavioral workflow detail ({word!r}) — belongs to the skill"
        )


# ---------------------------------------------------------------------------
# C-2 — exactly one skill delegation, command→skill direction only
# ---------------------------------------------------------------------------

def test_c02_single_skill_delegation():
    text = _read(TEMPLATE)
    skill_mentions = text.count("SKILL.md")
    assert skill_mentions == 1, (
        f"delegation must name exactly one skill (found {skill_mentions} SKILL.md mentions)"
    )
    assert DELEGATION_PATH in text, f"template must delegate to {DELEGATION_PATH}"
    # No back-reference: the skill body never points at the command template.
    skill_text = _read(SKILL_SRC)
    assert "templates/commands/humanize.md" not in skill_text, (
        "skill body must not back-reference the command template (C-2 direction)"
    )


# ---------------------------------------------------------------------------
# C-3 — skill frontmatter + self-sufficient body
# ---------------------------------------------------------------------------

def test_c03_skill_frontmatter_and_self_sufficient():
    assert SKILL_SRC.is_file(), f"external skill missing: {SKILL_SRC}"
    text = _read(SKILL_SRC)
    fm = _frontmatter(text)
    assert "name: humanize" in fm, "skill frontmatter lacks name: humanize"
    assert "classification: external" in fm, "skill frontmatter lacks classification: external"
    assert SKILL_ID_LITERAL in fm, f"skill frontmatter lacks {SKILL_ID_LITERAL}"
    assert "description:" in fm, "skill frontmatter lacks description with trigger words"
    # Self-sufficiency: inline minimal operational facts a bare host needs.
    for value in STR_002_VALUES:
        assert value in text, f"skill body lacks tone value {value}"
    for flag in STR_004_FLAGS:
        assert flag in text, f"skill body lacks call option {flag}"
    assert "保真" in text, "skill body lacks the fidelity floor (FR-007)"
    assert "按数据" in text or "数据处理" in text, (
        "skill body lacks the data-not-instructions declaration (FR-029)"
    )
    for ext in STR_003_EXTS:
        assert ext in text, f"skill body lacks supported extension {ext} (FR-019)"


# ---------------------------------------------------------------------------
# C-4 — generated per-tool copies (existence + generated header)
# ---------------------------------------------------------------------------

def test_c04_generated_copies_present():
    for copy in COPIES:
        assert copy.is_file(), f"generated copy missing: {copy}"
        text = _read(copy)
        assert "AUTO-GENERATED" in text or "regen-command-copies" in text, (
            f"{copy} lacks the do-not-hand-edit generated header"
        )
        assert STR_001 in text, f"{copy} lacks the command identity literal"


# ---------------------------------------------------------------------------
# C-5 — docs page content points
# ---------------------------------------------------------------------------

def test_c05_docs_page_content():
    assert DOCS_PAGE.is_file(), f"docs page missing: {DOCS_PAGE}"
    text = _read(DOCS_PAGE)
    assert "内联" in text and "文件" in text, "docs page lacks input-form coverage"
    assert "不写入" in text, "docs page lacks the default no-file-write statement"
    for value in STR_002_VALUES:
        assert value in text, f"docs page lacks tone value {value}"
    assert "FR-007" in text, "docs page lacks the fidelity boundary pointer (FR-007)"
    assert "FR-029" in text, "docs page lacks the data-not-instructions pointer (FR-029)"
    assert "不承诺" in text, "docs page lacks the detector no-promise statement (SC-009)"


# ---------------------------------------------------------------------------
# C-6 — feature registry rows resolve
# ---------------------------------------------------------------------------

def test_c06_registry_rows_resolve():
    assert FEATURE_DETAILS.is_file(), f"feature details file missing: {FEATURE_DETAILS}"
    assert REGISTRY.is_file(), f"feature registry missing: {REGISTRY}"
    reg = _read(REGISTRY)
    row = [ln for ln in reg.splitlines() if "062-humanize-command" in ln]
    assert row, "registry lacks a 062-humanize-command row"
    assert any(".specify/specs/062-humanize-command/requirements.md" in ln for ln in row), (
        "062 registry row does not point at its requirements.md"
    )


# ---------------------------------------------------------------------------
# C-7 — skill-side probe unit + compiled Wrap-up face; no command unit (Simple)
# ---------------------------------------------------------------------------

def test_c07_skill_probe_unit_and_compiled_wrapup():
    defs = _read(PROBE_DEFS)
    unit_row = [ln for ln in defs.splitlines()
                if ln.startswith("| skill-humanize-wrapup ")]
    assert unit_row, "probe-definitions lacks the skill-humanize-wrapup unit row"
    assert any("skill:humanize" in ln and "wrap-up" in ln for ln in unit_row), (
        "skill-humanize-wrapup unit row does not bind skill:humanize at wrap-up"
    )
    assert any("h-docs-sync-eval" in ln and "skill-humanize-wrapup" in ln
               for ln in defs.splitlines()), (
        "skill-humanize-wrapup lacks the h-docs-sync-eval @point:wrap-up binding"
    )
    # Simple class: no command-side unit row was added.
    assert not any(ln.startswith("| /speckit.humanize ") for ln in defs.splitlines()), (
        "Simple command must not get a probe command unit"
    )
    # The compiled face lands in the skill (source and synced runtime copy).
    for path in (SKILL_SRC, SKILL_RUNTIME):
        text = _read(path)
        assert "## Wrap-up" in text, f"{path} lacks the compiled ## Wrap-up face"
        assert "AUTO-GENERATED by probe-utils.py" in text, (
            f"{path} Wrap-up face must be compiled, not hand-written"
        )
        assert "feedback-utils.py" in text, (
            f"{path} Wrap-up face lacks the feedback record invocation"
        )


# ---------------------------------------------------------------------------
# C-8 — zero new runtime surface; existing distribution consumed as-is
# ---------------------------------------------------------------------------

def test_c08_no_runtime_surface():
    for path in (REPO_ROOT / "src" / "specify_cli", REPO_ROOT / "scripts"):
        for py in path.rglob("*.py"):
            if "test" in py.name:
                continue
            assert "humanize" not in py.read_text(encoding="utf-8", errors="replace").lower() or py.name == "conftest.py", (
                f"unexpected humanize runtime surface in {py} (C-8: no new runtime)"
            )
    pyproject = _read(REPO_ROOT / "pyproject.toml")
    assert "humanize" not in pyproject.lower(), "no new dependency may mention humanize"
    assert "generate_commands" in _read(REPO_ROOT / "src" / "specify_cli" / "__init__.py"), (
        "existing generate_commands distribution mechanism must stay untouched"
    )
    for engine in ("scripts/python/regen-command-copies.py",
                   "scripts/python/sync-mirrors.py"):
        assert (REPO_ROOT / engine).is_file(), f"distribution engine missing: {engine}"


# ---------------------------------------------------------------------------
# C-9 — baseline + the two downstream pinned tests updated in the same batch
# ---------------------------------------------------------------------------

def _import_test_module(name: str):
    path = REPO_ROOT / "tests" / "contract" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_c09_baseline_no_new_failures():
    assert BASELINE_FAILED.is_file(), (
        f"frozen failed-test baseline missing: {BASELINE_FAILED}"
    )
    contract = _read(CONTRACT_027)
    row = [ln for ln in contract.splitlines() if ln.startswith("| `humanize`")]
    assert row, "027 classification table lacks a humanize row"
    assert any("**Simple**" in ln for ln in row), "humanize must be classified Simple"
    result = [ln for ln in contract.splitlines() if "**Result**" in ln]
    assert result and "23 complex" in result[0] and "4 simple" in result[0], (
        "027 Result line must read 23 complex / 4 simple after humanize"
    )
    feedback_mod = _import_test_module("test_feedback_command_classification.py")
    assert "humanize" in feedback_mod.SIMPLE_COMMANDS, (
        "test_feedback_command_classification must derive humanize as Simple"
    )
    guards_mod = _import_test_module("test_skill_layer_visibility_guards.py")
    assert "humanize" in guards_mod.EXTERNAL_SKILLS, (
        "test_skill_layer_visibility_guards EXTERNAL_SKILLS must include humanize"
    )


# ---------------------------------------------------------------------------
# C-10 — detector-honesty wording across all static faces
# ---------------------------------------------------------------------------

DETECTOR_TERMS = ("检测器", "detector", "AI 内容检测")
FORBIDDEN_DETECTOR_CLAIMS = (
    "绕过检测", "规避检测", "bypass detection", "undetectable",
    "不被 AI 检测", "保证通过检测", "100% 通过",
)
HONEST_MARKERS = ("不承诺", "不保证", "无法保证", "不能保证")


def test_c10_detector_honesty_wording():
    surfaces = [p for p in (TEMPLATE, SKILL_SRC, SKILL_RUNTIME, DOCS_PAGE, *COPIES)
                if p.is_file()]
    assert surfaces, "no humanize surfaces exist yet (expected red before implementation)"
    for path in surfaces:
        lines = _read(path).splitlines()
        for i, line in enumerate(lines):
            if any(term in line for term in DETECTOR_TERMS):
                window = "\n".join(lines[i:i + 2])
                assert any(marker in window for marker in HONEST_MARKERS), (
                    f"{path}:{i + 1} mentions a detector without a no-promise statement "
                    f"(C-10/SC-009): {line.strip()[:80]!r}"
                )
            lowered = line.lower()
            for claim in FORBIDDEN_DETECTOR_CLAIMS:
                assert claim.lower() not in lowered, (
                    f"{path}:{i + 1} carries a forbidden detector claim {claim!r}"
                )
