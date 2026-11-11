"""Init must not create a placeholder anchor beside a legacy real anchor."""
from __future__ import annotations

from pathlib import Path

import specify_cli

ANCHORS = ("constitution.md", "features.md")


def _copy_into(project: Path) -> None:
    specify_cli.copy_local_templates(project, "qoder", "sh", is_current_dir=True)


def test_init_skips_the_stub_when_a_legacy_anchor_exists(tmp_path):
    root = tmp_path / "project"
    memory = root / ".specify" / "memory"
    memory.mkdir(parents=True)
    for anchor in ANCHORS:
        (memory / anchor).write_text(
            "# Real %s\n\nProject content.\n" % anchor, encoding="utf-8"
        )

    _copy_into(root)

    for anchor in ANCHORS:
        assert not (root / ".specify" / anchor).exists(), (
            f"init created a root stub beside the legacy {anchor}"
        )
        assert (memory / anchor).read_text(encoding="utf-8").startswith("# Real ")


def test_init_still_writes_the_stub_when_no_legacy_anchor_exists(tmp_path):
    root = tmp_path / "project"
    root.mkdir()

    _copy_into(root)

    for anchor in ANCHORS:
        target = root / ".specify" / anchor
        assert target.is_file(), f"init did not create {anchor}"
        assert "This file is a placeholder" in target.read_text(encoding="utf-8")
