import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture
def workspace_root(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def repo_root() -> Path:
    return ROOT


@pytest.fixture
def qoder_support_surface_files(repo_root: Path) -> list[Path]:
    return [
        repo_root / "README.md",
        repo_root / "docs" / "installation.md",
        repo_root / ".specify" / "instructions.md",
        repo_root / "templates" / "plan-template.md",
        repo_root / "templates" / "commands" / "agents.md",
    ]


@pytest.fixture
def qoder_minimal_resource_path(tmp_path: Path) -> Path:
    resource_root = tmp_path / "resource"
    (resource_root / "templates" / "commands").mkdir(parents=True)
    (resource_root / "templates" / "commands" / "requirements.md").write_text(
        "# [COMMAND_NAME]\n\nAgent: [AGENT_NAME]\nArgs: [ARGUMENTS]",
        encoding="utf-8",
    )
    (resource_root / "memory").mkdir(parents=True)
    (resource_root / "memory" / "constitution.md").write_text(
        "# Constitution", encoding="utf-8"
    )
    (resource_root / "memory" / "features.md").write_text(
        "# Features", encoding="utf-8"
    )
    (resource_root / "scripts").mkdir(parents=True)
    (resource_root / "skills").mkdir(parents=True)
    return resource_root
