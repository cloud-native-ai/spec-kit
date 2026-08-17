"""Contract test: every framework script must be reachable by `specify init`.

`specify init` distributes a framework tree by copying the canonical source over
the mirror -- `shutil.copytree(resource_path / "scripts", specify_dir / "scripts",
dirs_exist_ok=True)`. That is an *additive merge*: it never syncs mirror -> source
and never removes mirror files lacking a source. Consequence: a script that exists
only under `.specify/scripts/` can never reach a downstream project, no matter how
correct it looks in this repo.

`sync-mirrors.py` already detected such files, but reported them as a non-fatal
`note` and exited 0, so two orphans (`setup-plan.sh`, `update-agent-context.sh`)
persisted unnoticed. These tests keep the detection wired and fatal.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "sync-mirrors.py"


def _load_engine():
    spec = importlib.util.spec_from_file_location("sync_mirrors", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sync_mirrors"] = module
    spec.loader.exec_module(module)
    return module


sm = _load_engine()


@pytest.mark.contract
class TestScriptsDistributionParity:
    def test_scripts_pair_is_strict_about_orphans(self):
        """The scripts/ tree is framework-owned, so mirror-only files must be fatal."""
        pairs = {src: strict for src, _dst, strict, _excl in sm.MIRROR_PAIRS}
        assert "scripts" in pairs, "scripts/ must be a declared mirror pair"
        assert pairs["scripts"] is True, (
            "scripts/ must keep strict_extras=True; otherwise a .specify-only "
            "script silently becomes undistributable again"
        )

    def test_skills_pair_stays_lenient(self):
        """skills/ may legitimately hold project-local skills in the mirror."""
        pairs = {src: strict for src, _dst, strict, _excl in sm.MIRROR_PAIRS}
        assert pairs.get("skills") is False, (
            "skills/ must stay lenient so project-local skills are not flagged"
        )

    def test_compare_pair_reports_mirror_only_file_as_extra(self, tmp_path):
        """Unit-level proof that the orphan direction is actually detected."""
        src = tmp_path / "src"
        dst = tmp_path / "dst"
        (src / "bash").mkdir(parents=True)
        (dst / "bash").mkdir(parents=True)
        (src / "bash" / "shared.sh").write_text("#!/usr/bin/env bash\n")
        (dst / "bash" / "shared.sh").write_text("#!/usr/bin/env bash\n")
        (dst / "bash" / "orphan.sh").write_text("#!/usr/bin/env bash\n")

        missing, differing, extra = sm.compare_pair(src, dst)

        assert missing == []
        assert differing == []
        assert [str(p) for p in extra] == ["bash/orphan.sh"]

    def test_repo_has_no_orphan_or_drifted_scripts(self):
        """The live gate: every .specify/scripts file has a canonical source."""
        result = subprocess.run(
            [sys.executable, str(ENGINE), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            "sync-mirrors.py --check failed.\n"
            "An ORPHAN line means a mirror-only file that `specify init` can never "
            "distribute: either add the canonical source (e.g. scripts/bash/<name>.sh) "
            "or delete the mirror copy.\n"
            "A DIFF/MISS line means the mirror drifted: run "
            "`python3 scripts/python/sync-mirrors.py --write`.\n\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
