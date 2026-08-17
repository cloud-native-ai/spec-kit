"""Framework source provenance core (043-init-commit-stamp).

stdlib-only on purpose: the hatchling build hook (hatch_build.py) loads this
module directly inside the build environment, where the CLI's runtime
dependencies (typer/rich) are absent. Keep this file dependency-free.

Contracts: .specify/specs/043-init-commit-stamp/contracts/
  source-stamp-resolution.contract.md (probe grammar + resolution order)
"""
from __future__ import annotations

import datetime
import json
import re
import subprocess
from pathlib import Path

_SOURCE_COMMIT_FILENAME = "_source_commit.json"
_COMMIT_ID_RE = re.compile(r"^[0-9a-f]{40}$")


def utc_compact_stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _probe_head_commit(start_dir):
    """The single git-probe grammar (043 contract §C-1): bounded
    `git -C <dir> rev-parse HEAD`, output validated as a full 40-hex id.
    Returns (commit | None, reason | None) and never raises — unavailability
    is data. The build hook reuses this same function; a second probe
    implementation must not exist."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(start_dir), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"git probe failed: {exc.__class__.__name__}"
    if proc.returncode != 0:
        return None, "git probe failed: not a git work tree"
    commit = proc.stdout.strip()
    if not _COMMIT_ID_RE.match(commit):
        return None, "git probe output failed 40-hex validation"
    return commit, None


def _read_embedded_source_commit(module_dir: Path):
    """Read the build-embedded source commit under `module_dir`. The file is
    a build artifact with untrusted content: any read/parse/shape failure is
    'no embedding', never an exception (043 contract §C-3)."""
    try:
        payload = json.loads(
            (Path(module_dir) / _SOURCE_COMMIT_FILENAME).read_text(
                encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    commit = payload.get("commit")
    if not isinstance(commit, str):
        return None
    if not (_COMMIT_ID_RE.match(commit) or commit == "unavailable"):
        return None
    return payload


def resolve_source_commit(module_dir: Path):
    """Resolve the framework's source commit (043 contract §C-2). Constant
    order: checkout git probe (fresh in dev) > build-embedded value (wheel
    installs) > unavailable. Read-only; returns
    {"commit": str | None, "origin": "git" | "embedded" | "unavailable",
     "reason": str | None} and never fabricates an id."""
    commit, reason = _probe_head_commit(module_dir)
    if commit:
        return {"commit": commit, "origin": "git", "reason": None}
    embedded = _read_embedded_source_commit(module_dir)
    if embedded is not None:
        value = embedded["commit"]
        if _COMMIT_ID_RE.match(value):
            return {"commit": value, "origin": "embedded", "reason": None}
        return {"commit": None, "origin": "embedded",
                "reason": embedded.get("reason") or "embedded source commit unavailable"}
    return {"commit": None, "origin": "unavailable",
            "reason": reason or "no embedded source commit"}
