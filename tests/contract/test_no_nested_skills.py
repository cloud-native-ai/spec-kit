"""Contract test: no skill may contain another skill (nested-skill guard).

Failure mode this prevents
--------------------------
A skill directory that itself contains a second ``SKILL.md`` means another skill
was copied or linked *inside* it. The usual cause is a shell operation whose
destination already existed as a directory::

    ln -s /path/to/yuque-workspace skills/draw-echarts   # -> skills/draw-echarts/yuque-workspace
    cp -R /path/to/yuque-workspace skills/draw-echarts   # same nesting

Verified on macOS/BSD ``ln``: when the destination is a **real directory**,
neither ``-f`` nor ``-n`` prevents this and the command still exits 0, so the
mistake is silent. (``-n`` only helps when the destination is a symlink to a
directory.) Python's ``Path.symlink_to`` / ``os.symlink`` raise FileExistsError
instead, so this trap is shell-specific.

Why a test rather than a one-off cleanup: `skills/draw-echarts/yuque-workspace`
entered the source tree in 8da8b853 (2026-05-18) and was removed from the source
in 21604dd5 (2026-05-24) -- but `specify init` distributes with
``copytree(dirs_exist_ok=True)``, an additive merge that never deletes. Every
project initialised in that window kept a permanent copy, so one mistake stayed
visible in `.specify/skills/` long after the source was clean. Catching it before
commit is the only cheap fix.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOTS = ["skills", ".specify/skills"]

# Vendored / generated trees may legitimately contain files named SKILL.md
# (e.g. node_modules/playwright-core ships two). They are not skills.
VENDOR_DIRS = {"node_modules", "__pycache__", ".git", ".venv"}


def _nested_skill_files(skill_dir: Path):
    """SKILL.md files below a skill's own root -- i.e. an embedded skill."""
    found = []
    for path in skill_dir.rglob("SKILL.md"):
        rel = path.relative_to(skill_dir)
        if len(rel.parts) == 1:
            continue  # the skill's own SKILL.md
        if VENDOR_DIRS.intersection(rel.parts):
            continue
        found.append(path.relative_to(ROOT))
    return found


@pytest.mark.contract
class TestNoNestedSkills:
    @pytest.mark.parametrize("root_name", SKILL_ROOTS)
    def test_no_skill_contains_another_skill(self, root_name):
        root = ROOT / root_name
        if not root.is_dir():
            pytest.skip(f"{root_name} not present")

        offenders = []
        for skill_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            offenders.extend(_nested_skill_files(skill_dir))

        assert not offenders, (
            f"Nested skill(s) found under {root_name}/ -- a skill must never "
            "contain another skill:\n  "
            + "\n  ".join(str(p) for p in offenders)
            + "\n\nUsual cause: a copy/symlink whose destination already existed "
            "as a directory, so the payload landed inside it (silent, exit 0). "
            "Delete the nested copy, then re-place the skill at the skills root."
        )

    def test_every_skill_has_exactly_one_root_skill_file(self):
        """Sanity anchor: each skill dir owns a SKILL.md at its root."""
        root = ROOT / "skills"
        missing = [
            d.name
            for d in sorted(p for p in root.iterdir() if p.is_dir())
            if not (d / "SKILL.md").is_file()
        ]
        assert not missing, f"skill dirs without a root SKILL.md: {missing}"
