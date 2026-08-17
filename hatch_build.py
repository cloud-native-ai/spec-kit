"""Hatchling custom build hook: embed the framework source commit (043).

Writes src/specify_cli/_source_commit.json at build time through the SAME
probe grammar as the CLI runtime (specify_cli._provenance._probe_head_commit,
loaded stdlib-only so it works inside the build environment) — zero second
implementation. Probe failure embeds an honest `unavailable` + reason and the
build proceeds; write failure FAILS the build (never ship a wheel whose
provenance face is silently missing).

Contract: .specify/specs/043-init-commit-stamp/contracts/build-embedding.contract.md
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

_REPO_ROOT = Path(__file__).resolve().parent
_PROVENANCE_PATH = _REPO_ROOT / "src" / "specify_cli" / "_provenance.py"
_EMBED_PATH = _REPO_ROOT / "src" / "specify_cli" / "_source_commit.json"
_CANONICAL_NAME = "specify_cli._provenance"


def _load_module():
    """Load specify_cli._provenance under its canonical name — when the
    package is already imported (tests), the existing module object is
    reused so the hook provably shares the single probe grammar."""
    module = sys.modules.get(_CANONICAL_NAME)
    if module is None:
        spec = importlib.util.spec_from_file_location(
            _CANONICAL_NAME, _PROVENANCE_PATH)
        module = importlib.util.module_from_spec(spec)
        sys.modules[_CANONICAL_NAME] = module
        spec.loader.exec_module(module)
    return module


class SourceCommitHook(BuildHookInterface):
    def initialize(self, version, build_data):
        prov = _load_module()
        commit, reason = prov._probe_head_commit(_REPO_ROOT)
        payload = {"commit": commit or "unavailable",
                   "embedded_at": prov.utc_compact_stamp()}
        if commit is None:
            payload["reason"] = reason or "source commit unresolvable"
        try:
            _EMBED_PATH.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"source-commit embedding failed: {exc}") from exc
        # Explicit injection: the wheel's file set is not guaranteed to pick
        # up files written during initialize, so register the archive path.
        build_data.setdefault("force_include", {})[str(_EMBED_PATH)] = (
            "specify_cli/" + _EMBED_PATH.name)
