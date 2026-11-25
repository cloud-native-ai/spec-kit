"""105 US1 — fresh `specify init` seeds the new top-level store layout.

Red-first: authored before the package seed rename and the init seeding change (tasks.md T006).
Contract: `contracts/store-layout.contract.md` C-7 (fresh initialization) and C-2 (retired
container). The store roster is read from its one machine owner, never re-spelled here.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
RETIRED_ROOT = ".specify/memory"

sys.path.insert(0, str(REPO_ROOT / "scripts" / "python"))
import declaration_reader  # noqa: E402  (import follows the sys.path entry above)


def _declared_stores():
    body = declaration_reader.load_fact(
        declaration_reader.find_repo(REPO_ROOT), "runtime-store-layout"
    )["body"]
    return body["statement"]["stores"]


def _run_init(project: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src") + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    return subprocess.run(
        [
            sys.executable,
            "-c",
            "from specify_cli import main; main()",
            "init",
            "--here",
            "--ai",
            "qoder",
            "--script",
            "sh",
            "--no-git",
        ],
        cwd=str(project),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )


def test_fresh_init_seeds_the_new_layout(tmp_path: Path):
    stores = _declared_stores()
    project = tmp_path / "fresh"
    project.mkdir()

    proc = _run_init(project)
    assert proc.returncode == 0, (
        f"specify init failed (rc={proc.returncode})\n"
        f"stdout:\n{proc.stdout[-4000:]}\nstderr:\n{proc.stderr[-4000:]}"
    )

    specify = project / ".specify"
    assert not (specify / "memory").exists(), (
        f"{RETIRED_ROOT} must not be created by a fresh init (C-2/C-7)"
    )

    for seeded in ("session", "knowledge"):
        assert (specify / seeded).is_dir(), f"init must seed .specify/{seeded}/"
        assert (specify / seeded / ".gitkeep").is_file(), (
            f"the packaged placeholder must land under .specify/{seeded}/"
        )

    lazy = sorted(set(stores) - {"session", "knowledge"})
    for name in lazy:
        assert not (specify / name).exists(), (
            f".specify/{name}/ is created lazily by its owner, never by init"
        )

    assert (specify / "constitution.md").is_file(), "anchors stay at the .specify/ root"
    assert (specify / "features.md").is_file(), "anchors stay at the .specify/ root"

    from specify_cli import core_asset_relpaths

    assets = core_asset_relpaths()
    assert RETIRED_ROOT not in assets, "the core-asset list must drop the retired container"
    assert assets.count(".specify/session") == 1, "the core-asset list names the session tier once"
    assert assets.count(".specify/knowledge") == 1, (
        "the core-asset list names the knowledge tier once"
    )

    top_level_stores = sorted(
        path.name
        for path in specify.iterdir()
        if path.is_dir() and path.name in stores
    )
    assert top_level_stores == ["knowledge", "session"], (
        "a fresh tree must hold exactly the two seeded memory tiers"
    )
