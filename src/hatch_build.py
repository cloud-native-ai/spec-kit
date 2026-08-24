"""Hatchling custom build hook: embed the framework source commit (043) and
stage-copy skills/ without runtime-data dirs (046).

Writes src/specify_cli/_source_commit.json at build time through the SAME
probe grammar as the CLI runtime (specify_cli._provenance._probe_head_commit,
loaded stdlib-only so it works inside the build environment) — zero second
implementation. Probe failure embeds an honest `unavailable` + reason and the
build proceeds; write failure FAILS the build (never ship a wheel whose
provenance face is silently missing).

Also registers the skills/ tree via build_data["force_include"] from a staged
copy that drops every `site` path component: browser-utils site memory is
caller-owned runtime data and must never ship in the wheel (FR-003 of spec
046). Hatchling's target-level `exclude` does not filter force-include
content (verified empirically, see specs/046-browser-site-memory/research.md
R2), so the static `"skills"` force-include line is absent from pyproject.toml
by design and the staging here is the single exclusion point. Staging failure
FAILS the build (same policy as the provenance write).

Contracts: .specify/specs/043-init-commit-stamp/contracts/build-embedding.contract.md
           .specify/specs/046-browser-site-memory/contracts/framework-exclusions.md (X-5/X-6)
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

_REPO_ROOT = Path(__file__).resolve().parents[1]  # src/hatch_build.py -> repo root
_PROVENANCE_PATH = _REPO_ROOT / "src" / "specify_cli" / "_provenance.py"
_EMBED_PATH = _REPO_ROOT / "src" / "specify_cli" / "_source_commit.json"
_CANONICAL_NAME = "specify_cli._provenance"
_SKILLS_SRC = _REPO_ROOT / "skills"
_SITE_DIR_COMPONENT = "site"  # dropped anywhere under skills/ (spec 046 X-5)


def _stage_skills(build_data):
    """Copy skills/ to a temp staging dir minus every `site` component and
    register the staged tree in force_include. Any failure fails the build."""
    if not _SKILLS_SRC.is_dir():
        raise RuntimeError(f"skills source dir missing: {_SKILLS_SRC}")
    staged_root = Path(tempfile.mkdtemp(prefix="specify-skills-"))
    staged = staged_root / "skills"
    try:
        shutil.copytree(
            _SKILLS_SRC,
            staged,
            ignore=lambda _dir, names: {
                n for n in names if n == _SITE_DIR_COMPONENT
            },
        )
    except OSError as exc:
        raise RuntimeError(f"skills staging copy failed: {exc}") from exc
    build_data.setdefault("force_include", {})[str(staged)] = "specify_cli/skills"


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
        _stage_skills(build_data)
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
