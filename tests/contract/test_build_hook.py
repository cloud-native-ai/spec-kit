"""Contract tests for the build-time source-commit embedding hook (043, T012).

Contract: .specify/specs/043-init-commit-stamp/contracts/build-embedding.contract.md

The hatchling build API exists only inside the build environment, so this suite
injects a stub module before loading the src-tree hook file. Pins: the embedded
file's fields, the honest-unavailable degradation, the same-probe-grammar
object identity (no second git implementation), the write-failure = build-failure
semantics, and the pyproject/.gitignore declarations.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

import specify_cli as sc

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "src" / "hatch_build.py"
EMBED = REPO_ROOT / "src/specify_cli/_source_commit.json"

pytestmark = pytest.mark.contract

FAKE = "a" * 40
TS_RE_STRING = "embedded_at"


def _stub_hatchling(monkeypatch):
    interface = types.ModuleType("hatchling.builders.hooks.plugin.interface")
    interface.BuildHookInterface = object
    hatchling = types.ModuleType("hatchling")
    builders = types.ModuleType("hatchling.builders")
    hooks = types.ModuleType("hatchling.builders.hooks")
    plugin = types.ModuleType("hatchling.builders.hooks.plugin")
    monkeypatch.setitem(sys.modules, "hatchling", hatchling)
    monkeypatch.setitem(sys.modules, "hatchling.builders", builders)
    monkeypatch.setitem(sys.modules, "hatchling.builders.hooks", hooks)
    monkeypatch.setitem(sys.modules, "hatchling.builders.hooks.plugin", plugin)
    monkeypatch.setitem(
        sys.modules, "hatchling.builders.hooks.plugin.interface", interface)


@pytest.fixture()
def hook_module(monkeypatch):
    _stub_hatchling(monkeypatch)
    spec = importlib.util.spec_from_file_location("hatch_build_test", HOOK)
    module = importlib.util.module_from_spec(spec)
    sys.modules["hatch_build_test"] = module
    spec.loader.exec_module(module)
    return module


def _patch_prov(monkeypatch, module, value):
    fake = types.SimpleNamespace(
        _probe_head_commit=lambda d: value,
        utc_compact_stamp=lambda: "20260817T000000Z")
    monkeypatch.setattr(module, "_load_module", lambda: fake)


def test_hook_file_exists():
    assert HOOK.is_file(), f"build hook missing: {HOOK}"


def test_embeds_commit_on_probe_success(hook_module, monkeypatch):
    _patch_prov(monkeypatch, hook_module, (FAKE, None))
    hook_module.SourceCommitHook().initialize("standard", {})
    payload = json.loads(EMBED.read_text(encoding="utf-8"))
    assert payload["commit"] == FAKE
    assert "reason" not in payload
    assert TS_RE_STRING in payload


def test_embeds_unavailable_with_reason_on_probe_failure(
        hook_module, monkeypatch):
    _patch_prov(monkeypatch, hook_module, (None, "not a git work tree"))
    hook_module.SourceCommitHook().initialize("standard", {})
    payload = json.loads(EMBED.read_text(encoding="utf-8"))
    assert payload["commit"] == "unavailable"
    assert payload["reason"] == "not a git work tree"


def test_hook_reuses_the_single_probe_grammar(hook_module):
    probe = hook_module._load_module()._probe_head_commit
    assert probe is sc._probe_head_commit, \
        "the build hook MUST reuse specify_cli's probe — zero second grammar"


def test_write_failure_fails_the_build(hook_module, monkeypatch):
    _patch_prov(monkeypatch, hook_module, (FAKE, None))

    def boom(path, *a, **k):
        raise OSError("read-only")
    monkeypatch.setattr(Path, "write_text", boom)
    with pytest.raises(RuntimeError):
        hook_module.SourceCommitHook().initialize("standard", {})


def test_declarations_are_in_place():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.hatch.build.hooks.custom]" in pyproject
    assert 'path = "src/hatch_build.py"' in pyproject
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "src/specify_cli/_source_commit.json" in gitignore
