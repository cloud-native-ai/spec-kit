"""Integration tests for defaults-layer seeding during init (Feature 061, US3).

Subject: ``specify_cli.ensure_agent_layer_dirs(root_path, defaults_source=None)``
and the ``copy_local_templates`` call site. The template owner is
``templates/execution-config-defaults.yaml``; seeding is absent-only and never
overwrites an existing file.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[2]
TEMPLATE = REPO_ROOT / "templates" / "execution-config-defaults.yaml"


@pytest.fixture(autouse=True)
def seeding_implemented():
    """Red-first attribution: the parameter under test must exist."""
    import inspect
    signature = inspect.signature(specify_cli.ensure_agent_layer_dirs)
    assert "defaults_source" in signature.parameters, (
        "ensure_agent_layer_dirs has no defaults_source parameter")


def target_of(ws: Path) -> Path:
    return ws / ".specify" / "agents" / "execution" / "configs" / "_defaults.yaml"


def test_seeds_when_absent(tmp_path: Path):
    ws = tmp_path / "ws"
    specify_cli.ensure_agent_layer_dirs(ws, defaults_source=TEMPLATE)
    target = target_of(ws)
    assert target.is_file()
    assert target.read_bytes() == TEMPLATE.read_bytes()


def test_second_call_is_byte_identical(tmp_path: Path):
    ws = tmp_path / "ws"
    specify_cli.ensure_agent_layer_dirs(ws, defaults_source=TEMPLATE)
    before = target_of(ws).read_bytes()
    specify_cli.ensure_agent_layer_dirs(ws, defaults_source=TEMPLATE)
    assert target_of(ws).read_bytes() == before


def test_user_edit_is_never_overwritten(tmp_path: Path):
    ws = tmp_path / "ws"
    specify_cli.ensure_agent_layer_dirs(ws, defaults_source=TEMPLATE)
    target = target_of(ws)
    target.write_text("# user edit\n", encoding="utf-8")
    specify_cli.ensure_agent_layer_dirs(ws, defaults_source=TEMPLATE)
    assert target.read_text(encoding="utf-8") == "# user edit\n"


def test_explicit_missing_source_raises(tmp_path: Path):
    ws = tmp_path / "ws"
    missing = tmp_path / "no-such-template.yaml"
    with pytest.raises(RuntimeError):
        specify_cli.ensure_agent_layer_dirs(ws, defaults_source=missing)
    assert not target_of(ws).exists()


def test_packaged_fallback_is_used(tmp_path: Path, monkeypatch):
    resource = tmp_path / "resource"
    (resource / "templates").mkdir(parents=True)
    shutil.copy2(TEMPLATE, resource / "templates" / TEMPLATE.name)
    monkeypatch.setattr(specify_cli, "get_resource_path", lambda: resource)
    ws = tmp_path / "ws"
    specify_cli.ensure_agent_layer_dirs(ws)
    assert target_of(ws).read_bytes() == TEMPLATE.read_bytes()


def test_no_source_and_no_packaged_resource_fabricates_nothing(tmp_path: Path,
                                                               monkeypatch):
    monkeypatch.setattr(specify_cli, "get_resource_path", lambda: None)
    ws = tmp_path / "ws"
    specify_cli.ensure_agent_layer_dirs(ws)
    assert not target_of(ws).exists()
