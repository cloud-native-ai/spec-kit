"""Contract: /speckit.migrate template is a thin projection (097 T033).

Claims: contracts/migrate-template.md T-1 (two-key frontmatter and the section
shape), T-2 (delegation only — no implementation symbols, no inspection code
fence, no confirmation-class flag), T-5 / T-6 (the four outcomes and their exit
codes restated verbatim, receipt and archive pointers reported). FR-002: the
template reaches the one deterministic engine by invocation, never by a copied
implementation; FR-022: the outcome words and exit codes are script-decidable
from the template text itself.

Red-first discipline (Constitution IV): this module is authored before
``templates/commands/migrate.md`` exists, so every assertion fails with a
"template missing" message — never a collection or import error.

The Qoder copy's generated frontmatter is deliberately NOT re-asserted here: the
generic contract test ``tests/contract/test_qoder_command_frontmatter.py``
covers every ``.qoder/commands/speckit.*.md`` file, this one included (T-4). The
last test below pins that coverage pointer so it cannot silently disappear.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "commands" / "migrate.md"
QODER_GENERIC = REPO_ROOT / "tests" / "contract" / "test_qoder_command_frontmatter.py"

# T-2: implementation-level symbols that MUST NOT appear in the projection.
FORBIDDEN_SYMBOLS = (
    "check_",
    "sanitize-utils",
    "anchor-layout-migrate",
    "sync-mirrors",
    "regen-command-copies",
    "_OBSOLETE_",
)
REQUIRED_SECTIONS = ("## User Input", "## Glossary", "## Delegation", "## Handoffs")
OUTCOME_EXIT = {"clean": "0", "planned": "1", "applied": "0", "blocked": "3"}
CONFIRMATION_FLAGS = ("--yes", "--force", "--non-interactive", "--confirm")
ALLOWED_FENCE_LANGUAGES = {"text", "bash", "sh"}

FENCE_RE = re.compile(r"^```(\w*)\s*$\n(.*?)^```\s*$", re.M | re.S)
OUTCOME_ROW_RE = re.compile(r"^\|\s*`([a-z]+)`\s*\|\s*(\d)\s*\|", re.M)


def _read_template() -> str:
    assert TEMPLATE.is_file(), (
        "templates/commands/migrate.md is missing — T035 authors the projection"
    )
    return TEMPLATE.read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    assert text.startswith("---\n"), "the template must open with a YAML frontmatter block"
    end = text.find("\n---\n", 4)
    assert end != -1, "the template frontmatter is not closed"
    return text[4:end]


def _fences(text: str) -> list[tuple[str, str]]:
    return [(match.group(1), match.group(2)) for match in FENCE_RE.finditer(text)]


# ---------------------------------------------------------------------------
# T-1 — frontmatter and section shape
# ---------------------------------------------------------------------------


def test_frontmatter_carries_exactly_two_keys() -> None:
    keys = [
        line.split(":", 1)[0].strip()
        for line in _frontmatter(_read_template()).splitlines()
        if line.strip()
    ]
    assert keys == ["description", "short-description"], (
        "T-1 fixes the frontmatter to exactly the two keys description / "
        f"short-description in that order; got {keys!r}"
    )
    values = {
        line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
        for line in _frontmatter(_read_template()).splitlines()
        if line.strip()
    }
    assert values["description"], "description must be non-empty"
    assert values["short-description"], "short-description must be non-empty"


def test_required_sections_are_present_as_headings() -> None:
    text = _read_template()
    missing = [
        section
        for section in REQUIRED_SECTIONS
        if not re.search(r"^%s$" % re.escape(section), text, re.M)
    ]
    assert not missing, f"T-1 requires these sections as headings; missing {missing}"


# ---------------------------------------------------------------------------
# T-2 — thin projection: literals yes, implementation no
# ---------------------------------------------------------------------------


def test_template_declares_the_two_delegated_commands() -> None:
    text = _read_template()
    assert "specify migrate" in text, "the dry-run literal `specify migrate` is required"
    assert "specify migrate --apply" in text, (
        "the apply literal `specify migrate --apply` is required"
    )


def test_template_carries_no_implementation_symbol() -> None:
    text = _read_template()
    present = [symbol for symbol in FORBIDDEN_SYMBOLS if symbol in text]
    assert not present, (
        "the template must reach the engine by invocation only, never by naming "
        f"its internals (T-2); found {present!r}"
    )


def test_template_has_no_inspection_code_fence() -> None:
    """Only plain text and delegation-only shell fences; no inspection implementation."""
    fences = _fences(_read_template())
    assert fences, "the template must carry its $ARGUMENTS text fence at minimum"
    offenders: list[str] = []
    for language, body in fences:
        if language not in ALLOWED_FENCE_LANGUAGES:
            offenders.append(f"{language or '(none)'} fence is not plain text or delegation shell")
            continue
        if language in {"bash", "sh"}:
            for line in body.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if not stripped.startswith("specify migrate"):
                    offenders.append(f"non-delegation command line: {stripped!r}")
    assert not offenders, (
        "T-2 forbids an inlined inspection/implementation fence; "
        f"offenders: {offenders!r}"
    )


def test_template_passes_no_confirmation_class_flag() -> None:
    text = _read_template()
    present = [flag for flag in CONFIRMATION_FLAGS if flag in text]
    assert not present, (
        "the command surface has no confirmation-class flag (T-2.4 / cli C-5); "
        f"the template must not mention {present!r}"
    )


# ---------------------------------------------------------------------------
# T-5 / T-6 — outcomes, exit codes, and record pointers restated verbatim
# ---------------------------------------------------------------------------


def test_outcome_and_exit_code_table_is_restated_verbatim() -> None:
    rows = dict(OUTCOME_ROW_RE.findall(_read_template()))
    assert rows == OUTCOME_EXIT, (
        "T-2.5 requires the four outcomes and their exit codes restated verbatim: "
        f"expected {OUTCOME_EXIT!r}, parsed {rows!r}"
    )


def test_receipt_and_archive_pointers_are_named() -> None:
    text = _read_template()
    assert ".specify/memory/migrate/receipts/<run-id>.json" in text, (
        "T-6 requires the receipt path pointer"
    )
    assert ".specify/archive/migrate/<run-id>/" in text, (
        "T-6 requires the archive root pointer"
    )
    assert "recover" in text, "T-6 requires the receipt `recover` field as the recovery route"


def test_boundary_names_the_init_repair_entry() -> None:
    text = _read_template()
    assert "specify init" in text, (
        "the boundary text must name `specify init` as the repair entry when "
        "`.specify/` is missing (cli C-2)"
    )
    assert "neither install nor init" in text, (
        "the boundary must state that this command performs neither install nor init"
    )


# ---------------------------------------------------------------------------
# T-4 — the Qoder copy's frontmatter stays covered by the generic test
# ---------------------------------------------------------------------------


def test_qoder_frontmatter_is_covered_by_the_generic_contract() -> None:
    assert QODER_GENERIC.is_file(), "the generic Qoder frontmatter contract test is missing"
    generic = QODER_GENERIC.read_text(encoding="utf-8")
    assert "QODER_DIR" in generic and "speckit.*.md" in generic, (
        "the generic test must keep covering every .qoder/commands/speckit.*.md copy"
    )
