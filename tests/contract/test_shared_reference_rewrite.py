"""Contract tests: references point at the shared reference directory (Feature 029, contract C-REFS).

Every reference that previously targeted ``skills/sdd-workflow/references/`` must now target the
shared reference directory in the correct per-artefact form, with no dead links. The shared
directory is subdivided by content type: ``workflow/`` (process protocols), ``guidelines/``
(methodology), ``constants/`` (enumerated catalogs), ``definitions/`` (semantics),
``patterns/`` (design patterns).

- Command templates (``templates/commands/*.md``, ``templates/skills-template.md``) use the
  root-relative form ``shared/<type>/<f>.md`` (install-time ``rewrite_paths`` upgrades these to
  ``.specify/shared/<type>/<f>.md``). Where a command template intentionally hard-codes the
  installed path, it uses ``.specify/shared/<type>/<f>.md``.
- Sibling skills (``skills/*/SKILL.md``) use the installed-absolute form
  ``.specify/shared/<type>/<f>.md``.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# The relocated reference documents, grouped by shared/ type subdirectory.
SHARED_DOCS = {
    "workflow": {
        "agent-configuration.md",
        "feature-integration.md",
        "feedback-step.md",
        "user-input-protocol.md",
    },
    "guidelines": {
        "checklist-methodology.md",
        "requirements-guidelines.md",
    },
    "constants": {
        "clarify-taxonomy.md",
        "dfx-catalog.md",
        "ignore-patterns.md",
    },
    "definitions": {
        "tool-definitions.md",
    },
    "patterns": {
        "reconcile-pattern.md",
        "interview-pattern.md",
    },
}

SHARED_TYPES = tuple(SHARED_DOCS)


def _iter_files(*globs):
    for g in globs:
        yield from ROOT.glob(g)


def test_no_command_template_mentions_sdd_workflow():
    offenders = []
    for f in _iter_files("templates/commands/*.md", "templates/skills-template.md"):
        if "sdd-workflow" in f.read_text(encoding="utf-8"):
            offenders.append(str(f.relative_to(ROOT)))
    assert not offenders, f"command templates still mention sdd-workflow: {offenders}"


def test_no_skill_mentions_sdd_workflow():
    offenders = []
    for f in _iter_files("skills/*/SKILL.md"):
        if "sdd-workflow" in f.read_text(encoding="utf-8"):
            offenders.append(str(f.relative_to(ROOT)))
    assert not offenders, f"skills still mention sdd-workflow: {offenders}"


def test_skills_use_installed_absolute_shared_form():
    """Sibling skills reference shared docs via the installed-absolute shared path."""
    import re

    offenders = []
    bare = re.compile(r"(?<![\w./])shared/(" + "|".join(SHARED_TYPES) + r")/")
    for f in _iter_files("skills/*/SKILL.md"):
        text = f.read_text(encoding="utf-8")
        if bare.search(text):
            offenders.append(str(f.relative_to(ROOT)))
    assert not offenders, f"skills must use .specify/shared/<type>/ form: {offenders}"


def test_shared_reference_targets_resolve():
    """Every shared/<type>/<f>.md reference resolves to an existing source document."""
    import re

    missing = []
    pattern = re.compile(r"shared/(" + "|".join(SHARED_TYPES) + r")/([a-z0-9-]+\.md)")
    for f in _iter_files(
        "templates/commands/*.md",
        "templates/skills-template.md",
        "skills/*/SKILL.md",
    ):
        for subdir, name in pattern.findall(f.read_text(encoding="utf-8")):
            if not (ROOT / "shared" / subdir / name).exists():
                missing.append((str(f.relative_to(ROOT)), f"{subdir}/{name}"))
    assert not missing, f"references resolve to missing shared docs: {missing}"


def test_docs_do_not_describe_sdd_workflow_as_skill():
    """User-facing docs (excluding history/proposal) must not mention the retired sdd-workflow skill."""
    offenders = []
    for f in _iter_files(
        "docs/reference/agents/command-and-skills.md",
        "docs/reference/agents/design.md",
        "docs/reference/commands/skills.md",
        "docs/reference/commands/history.md",
        "docs/reference/skills/feedback.md",
    ):
        if "sdd-workflow" in f.read_text(encoding="utf-8"):
            offenders.append(str(f.relative_to(ROOT)))
    assert not offenders, f"docs still mention sdd-workflow: {offenders}"


def test_skill_count_wording_not_twenty_in_instructions():
    """The generated instructions skill inventory must reflect the decremented count."""
    instructions = ROOT / ".specify" / "instructions.md"
    if not instructions.exists():
        return
    text = instructions.read_text(encoding="utf-8")
    assert "20 total" not in text
    assert "sdd-workflow" not in text
