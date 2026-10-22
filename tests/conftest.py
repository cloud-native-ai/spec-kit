import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(autouse=True)
def _neutralize_host_git_config(tmp_path_factory, monkeypatch):
    """RC-07 (067): point GIT_CONFIG_GLOBAL / GIT_CONFIG_SYSTEM at empty temp files.

    Scope: the test process tree only (git subprocesses inherit the env). The host
    git configuration — including any global ``core.hooksPath`` hook tax — is never
    read by tests; asserts nothing changes semantically. Reversible: deleting this
    fixture restores prior behavior. Per-test temp files keep cases isolated.
    """
    cfg_dir = tmp_path_factory.mktemp("rc07-git-config")
    global_cfg = cfg_dir / "gitconfig-global"
    system_cfg = cfg_dir / "gitconfig-system"
    global_cfg.write_text("", encoding="utf-8")
    system_cfg.write_text("", encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_cfg))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(system_cfg))


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
        repo_root / "docs" / "tutorials" / "installation.md",
        repo_root / ".specify" / "instructions.md",
        repo_root / "templates" / "plan-template.md",
        repo_root / "templates" / "commands" / "agents.md",
    ]


@pytest.fixture
def claude_support_surface_files(repo_root: Path) -> list[Path]:
    return [
        repo_root / "README.md",
        repo_root / "docs" / "tutorials" / "installation.md",
        repo_root / ".specify" / "memory" / "constitution.md",
        repo_root / "templates" / "plan-template.md",
        repo_root / "templates" / "instructions-template.md",
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
    (resource_root / "templates" / "execution-config-defaults.yaml").write_text(
        "cli: qodercli\nmodel: fixture-model\n", encoding="utf-8"
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


@pytest.fixture
def claude_minimal_resource_path(tmp_path: Path) -> Path:
    resource_root = tmp_path / "resource"
    (resource_root / "templates" / "commands").mkdir(parents=True)
    (resource_root / "templates" / "commands" / "requirements.md").write_text(
        "# [COMMAND_NAME]\n\nAgent: [AGENT_NAME]\nArgs: [ARGUMENTS]",
        encoding="utf-8",
    )
    (resource_root / "templates" / "execution-config-defaults.yaml").write_text(
        "cli: qodercli\nmodel: fixture-model\n", encoding="utf-8"
    )
    (resource_root / "templates" / "claudeignore-template").write_text(
        "__pycache__/\n.venv/\n!.specify/specs/\n",
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


@pytest.fixture
def codex_minimal_resource_path(tmp_path: Path) -> Path:
    resource_root = tmp_path / "resource"
    (resource_root / "templates" / "commands").mkdir(parents=True)
    (resource_root / "templates" / "commands" / "requirements.md").write_text(
        "# [COMMAND_NAME]\n\nAgent: [AGENT_NAME]\nArgs: [ARGUMENTS]",
        encoding="utf-8",
    )
    (resource_root / "templates" / "execution-config-defaults.yaml").write_text(
        "cli: qodercli\nmodel: fixture-model\n", encoding="utf-8"
    )
    (resource_root / "templates" / "codexignore-template").write_text(
        "__pycache__/\n.venv/\n!.specify/specs/\n",
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


@pytest.fixture
def feedback_store(tmp_path: Path) -> Path:
    """Isolated feedback store workspace containing .specify/memory/feedback/."""
    store_dir = tmp_path / ".specify" / "memory" / "feedback"
    store_dir.mkdir(parents=True, exist_ok=True)
    (store_dir / ".gitkeep").touch()
    return tmp_path


@pytest.fixture
def ai_tools_resource_path(tmp_path: Path) -> Path:
    """Create a comprehensive resource root for AI tools support tests."""
    from fixtures.ai_tools_support import make_resource_with_skills

    return make_resource_with_skills(tmp_path / "resource")
