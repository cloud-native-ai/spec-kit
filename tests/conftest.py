import hashlib
import shutil
import subprocess
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


# --------------------------------------------------------------------------
# 067 T015: session-level read-only template snapshots + per-case clones
#
# plan §W2 行 4 / FR-016: a template tree used by many cases is snapshotted
# once per pytest session (read-only) and every case receives its own
# write-time clone — macOS APFS `clonefile` first (via `cp -c`), plain copy
# fallback everywhere else (and whenever clonefile refuses). The fallback is
# behavior-neutral: both methods must yield a byte-identical tree, which the
# helper asserts on EVERY clone, so a broken clone fails loudly instead of
# silently polluting a case. Cross-case isolation is structural: snapshots are
# never written to after creation, and each clone lands in that case's own
# tmp_path (c9's bare-start semantics are untouched by construction).
# --------------------------------------------------------------------------

_TEMPLATE_SNAPSHOT_BASE: Path | None = None


def _w2_snapshot_base(tmp_path_factory=None) -> Path:
    global _TEMPLATE_SNAPSHOT_BASE
    if _TEMPLATE_SNAPSHOT_BASE is None:
        if tmp_path_factory is not None:
            _TEMPLATE_SNAPSHOT_BASE = tmp_path_factory.mktemp("w2-template-snapshots")
        else:
            # Plain-helper callers (no fixture arg available) share a
            # tempfile-backed store; snapshots are read-only once built.
            import tempfile

            _TEMPLATE_SNAPSHOT_BASE = Path(
                tempfile.mkdtemp(prefix="w2-template-snapshots-")
            )
    return _TEMPLATE_SNAPSHOT_BASE


def _w2_tree_digest(root: Path) -> str:
    """Order-stable content digest of a file tree (relpath + bytes per entry)."""
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        h.update(p.relative_to(root).as_posix().encode("utf-8"))
        h.update(b"\0")
        if p.is_symlink():
            h.update(b"symlink:" + str(p.readlink()).encode("utf-8"))
        elif p.is_file():
            h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def _w2_clone_dir(src: Path, dst: Path, force_copy: bool = False) -> str:
    """Clone the tree at `src` to the (not-yet-existing) `dst`.

    Returns the method actually used: ``'clonefile'`` (macOS APFS clonefile,
    `cp -cR`) or ``'copy'`` (shutil.copytree fallback — used on non-darwin
    platforms, when `force_copy` is set, and whenever `cp -c` refuses, e.g. a
    non-APFS volume). Callers verify byte-identity, keeping the fallback
    behavior-neutral.
    """
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not force_copy and sys.platform == "darwin":
        proc = subprocess.run(
            ["cp", "-cR", str(src), str(dst)], capture_output=True, text=True
        )
        if proc.returncode == 0:
            return "clonefile"
    shutil.copytree(src, dst, symlinks=True)
    return "copy"


def install_template_clone(
    files: dict[str, bytes], dst: Path, tmp_path_factory=None, force_copy: bool = False
) -> str:
    """Install a template tree at `dst` as a clone of the session snapshot.

    `files` maps tree-relative paths to content. The read-only snapshot for
    this exact tree is built once per session (keyed by a content digest), so
    every case after the first pays only a clone. Self-verifying (T015
    acceptance): the clone is byte-compared against the snapshot on every
    call, and two consecutive clones are independent by construction — each
    is a separate copy in its own tmp directory; the snapshot is never
    mutated. Returns the clone method actually used ('clonefile' | 'copy').
    """
    digest = hashlib.sha256(
        b"\0".join(
            b"".join((rel.encode("utf-8"), b"\x00", content))
            for rel, content in sorted(files.items())
        )
    ).hexdigest()[:16]
    snap = _w2_snapshot_base(tmp_path_factory) / digest
    if not snap.exists():
        for rel, content in files.items():
            target = snap / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    method = _w2_clone_dir(snap, dst, force_copy=force_copy)
    assert _w2_tree_digest(snap) == _w2_tree_digest(dst), (
        f"template clone ({method}) diverged from the session snapshot {digest}"
    )
    return method
