"""Contract tests for the goal write-set allow-list (037-goal-registry, T003).

Source contract: .specify/specs/037-goal-registry/contracts/goal-writeset-migration.contract.md

The summary/SUMMARIZE step writes ONLY into the goal's derived subtree. This suite
pins the allow-list formulation and the six invariant groups it protects — in
particular that the authored ``goal.md`` is itself an invariant group, which is the
new constraint requirement 037 adds on top of 036's deny-list.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_MAPPING = REPO_ROOT / "skills/create-team/references/summary-mapping.md"
MIRROR_MAPPING = REPO_ROOT / ".specify/skills/create-team/references/summary-mapping.md"
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"

NEW_DELIVERY_ROOT = ".specify/goal"
OLD_DELIVERY_ROOT = ".specify/project/goal"

pytestmark = pytest.mark.contract


def _read(path: Path) -> str:
    assert path.is_file(), f"expected surface missing: {path}"
    return path.read_text(encoding="utf-8")


class TestWriteSetAllowList:
    """WS-1/WS-2: a single writable subtree, with the definition excluded."""

    def test_generator_targets_the_goal_archive_summary_subtree(self):
        text = _read(GENERATOR)
        assert f'"{NEW_DELIVERY_ROOT}' in text or f"'{NEW_DELIVERY_ROOT}" in text, (
            "generator must construct its delivery directory under "
            f"{NEW_DELIVERY_ROOT}/<goal-slug>/summary"
        )

    def test_generator_writes_under_a_summary_subdirectory(self):
        """The derived output is confined to summary/ so the allow-list is one subtree."""
        text = _read(GENERATOR)
        construction = [
            line for line in text.splitlines() if "delivery_dir" in line and "=" in line
        ]
        assert construction, "no delivery_dir construction site found in the generator"
        joined = "\n".join(construction)
        assert "summary" in joined, (
            "delivery_dir must resolve inside the goal's summary/ subtree; found:\n"
            + joined
        )

    def test_generator_no_longer_references_the_old_delivery_root(self):
        text = _read(GENERATOR)
        assert OLD_DELIVERY_ROOT not in text, (
            f"generator still references the pre-migration root {OLD_DELIVERY_ROOT}"
        )


class TestInvariantGroups:
    """WS-2: the write-set table must name every protected group, goal.md included."""

    REQUIRED_GROUPS = (
        "goal.md",
        ".specify/teams",
        "summarize-project",
        ".specify/agents",
        ".specify/project",
    )

    @pytest.mark.parametrize("group", REQUIRED_GROUPS)
    def test_mapping_names_each_invariant_group(self, group):
        text = _read(CANONICAL_MAPPING)
        assert group in text, (
            f"summary-mapping.md must name '{group}' among the write-set invariants"
        )

    def test_mapping_declares_the_definition_is_not_writable_by_the_refresh(self):
        """The distinguishing 037 rule: the authored definition is off-limits."""
        text = _read(CANONICAL_MAPPING)
        assert re.search(r"goal\.md", text), "goal.md not mentioned in summary-mapping.md"
        window = "\n".join(
            line for line in text.splitlines() if "goal.md" in line
        )
        assert re.search(r"MUST NOT|不变|不得|禁", window), (
            "summary-mapping.md mentions goal.md but states no prohibition on writing it;\n"
            f"matched lines:\n{window}"
        )

    def test_mapping_mirror_is_byte_identical(self):
        assert _read(CANONICAL_MAPPING) == _read(MIRROR_MAPPING), (
            "summary-mapping.md and its .specify mirror diverged — "
            "run scripts/python/sync-mirrors.py --write"
        )


class TestAtomicityAndSerialization:
    """WS-3/WS-4: atomic replace plus a lock inside the derived subtree."""

    def test_generator_writes_atomically(self):
        text = _read(GENERATOR)
        assert "os.replace" in text, "atomic same-directory replace not found"

    def test_refresh_lock_lives_inside_the_derived_subtree(self):
        text = _read(GENERATOR)
        assert ".refresh.lock" in text, "refresh lock path not found in the generator"

    def test_serialized_exit_code_is_distinct(self):
        text = _read(GENERATOR)
        assert "EXIT_SERIALIZED" in text, (
            "a yielding refresh must exit with a distinct serialized code, not no-op"
        )
