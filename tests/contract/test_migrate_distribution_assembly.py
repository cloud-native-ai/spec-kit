"""Contract: /speckit.migrate distribution assembly (097 T039).

Claims: contracts/migrate-template.md T-4 and SC-009 / FR-021 — the shipped
command is assembled, not merely present: the source template carries its
frontmatter, all four per-tool copies are generated with an ``AUTO-GENERATED``
marker naming the source template, the Qoder copy's description derives from
``short-description``, the command reference page carries the execution flow,
options, outcomes/exit codes, records and boundaries, ``COMMAND_BASELINE``
carries ``migrate`` at its new pinned length, the retired mirror face carries no
copy, and ``regen-command-copies.py --check`` is clean.

Red-first note: this row's prerequisites are T036–T038, so the module is green
at authoring; its job is to keep the assembly decidable after the fact.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "commands" / "migrate.md"
DOC = REPO_ROOT / "docs" / "reference" / "commands" / "migrate.md"
DISTRIBUTION_TEST = REPO_ROOT / "tests" / "contract" / "test_migration_distribution.py"
RETIRED_MIRROR = REPO_ROOT / ".specify" / "templates" / "commands" / "migrate.md"
REGEN = REPO_ROOT / "scripts" / "python" / "regen-command-copies.py"

COPIES = (
    REPO_ROOT / ".github" / "prompts" / "speckit.migrate.prompt.md",
    REPO_ROOT / ".claude" / "commands" / "speckit.migrate.md",
    REPO_ROOT / ".qoder" / "commands" / "speckit.migrate.md",
    REPO_ROOT / ".opencode" / "command" / "speckit.migrate.md",
)
MARKER = "AUTO-GENERATED from templates/commands/migrate.md"
SHORT_DESCRIPTION_RE = re.compile(r"^short-description:\s*(.+)$", re.MULTILINE)
QODER_FRONTMATTER_RE = re.compile(r"\A---\ndescription: ([^\n]+)\n---\n")
DOC_OUTCOME_ROW_RE = re.compile(r"^\|\s*`([a-z]+)`\s*\|[^|]*\|\s*(\d)\s*\|", re.M)
OUTCOME_EXIT = {"clean": "0", "planned": "1", "applied": "0", "blocked": "3"}
OPTIONS = ("--dry-run", "--apply", "--workspace", "--format")


def _read(path: Path, label: str) -> str:
    assert path.is_file(), f"{label} missing: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# T-4 — source template and generated copies
# ---------------------------------------------------------------------------


def test_source_template_present_with_its_frontmatter() -> None:
    text = _read(TEMPLATE, "source template")
    assert text.startswith("---\n"), "source template must open with frontmatter"
    assert re.search(r"^description:\s*\S", text, re.M), "description key missing"
    assert SHORT_DESCRIPTION_RE.search(text), "short-description key missing"


def test_all_four_copies_carry_the_auto_generated_marker() -> None:
    missing_or_unmarked = []
    for copy in COPIES:
        if not copy.is_file():
            missing_or_unmarked.append(f"{copy.relative_to(REPO_ROOT)} (missing)")
            continue
        if MARKER not in copy.read_text(encoding="utf-8"):
            missing_or_unmarked.append(
                f"{copy.relative_to(REPO_ROOT)} (no AUTO-GENERATED marker naming the source)"
            )
    assert not missing_or_unmarked, (
        "every per-tool copy must be generated from the source template: "
        f"{missing_or_unmarked!r}"
    )


def test_qoder_copy_description_comes_from_the_short_description() -> None:
    template = _read(TEMPLATE, "source template")
    short = SHORT_DESCRIPTION_RE.search(template)
    assert short, "the source template lost its short-description"
    qoder_copy = COPIES[2]
    frontmatter = QODER_FRONTMATTER_RE.match(_read(qoder_copy, "Qoder copy"))
    assert frontmatter, "the Qoder copy must carry a generated description frontmatter"
    assert frontmatter.group(1) == short.group(1).strip(), (
        "the Qoder copy's description must be the template's short-description"
    )


# ---------------------------------------------------------------------------
# T-4 — command reference page
# ---------------------------------------------------------------------------


def test_command_doc_page_carries_the_required_faces() -> None:
    text = _read(DOC, "command reference page")

    missing_options = [option for option in OPTIONS if option not in text]
    assert not missing_options, f"reference page omits options: {missing_options!r}"

    rows = dict(DOC_OUTCOME_ROW_RE.findall(text))
    assert rows == OUTCOME_EXIT, (
        "the reference page must carry the outcome/exit-code table verbatim: "
        f"expected {OUTCOME_EXIT!r}, parsed {rows!r}"
    )

    assert ".specify/memory/migrate/receipts/<run-id>.json" in text, (
        "the reference page must name the receipt landing point"
    )
    assert ".specify/archive/migrate/<run-id>/" in text, (
        "the reference page must name the archive root"
    )

    assert "specify init" in text and "neither install nor init" in text, (
        "the reference page must carry the `specify init` boundary"
    )
    assert "/speckit.sanitize" in text, (
        "the reference page must carry the sanitize-lane boundary"
    )


# ---------------------------------------------------------------------------
# T-4 — frozen baseline, retired mirror face, regenerator check
# ---------------------------------------------------------------------------


def test_command_baseline_contains_migrate_at_the_new_length() -> None:
    spec = importlib.util.spec_from_file_location(
        "_migrate_097_distribution_baseline", DISTRIBUTION_TEST
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert "migrate" in module.COMMAND_BASELINE, (
        "COMMAND_BASELINE must carry `migrate` (FR-021)"
    )
    # Live fact update (Feature 101, 2026-11-12): `/speckit.anchor` joined the shipped
    # command set, so the baseline list grew 31 -> 32. The pin follows the measured list
    # in test_migration_distribution.py, whose own header asserts 32.
    assert len(module.COMMAND_BASELINE) == 32, (
        f"COMMAND_BASELINE length must be the pinned 32, got {len(module.COMMAND_BASELINE)}"
    )


def test_retired_mirror_face_carries_no_migrate_copy() -> None:
    assert not RETIRED_MIRROR.exists(), (
        ".specify/templates/commands/ is the retired mirror face — a migrate copy "
        "there would be a second, hand-synced distribution path"
    )


def test_regen_check_is_clean() -> None:
    proc = subprocess.run(
        [sys.executable, str(REGEN), "--check"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, (
        "regen-command-copies.py --check must exit 0 (T-4); "
        f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
    )
    assert "OK" in proc.stdout, f"unexpected regenerator output: {proc.stdout!r}"
