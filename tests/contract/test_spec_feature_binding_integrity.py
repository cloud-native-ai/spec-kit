"""Contract test: spec ↔ feature binding integrity (goal 2026-08-15 audit).

Guards against the stale-reference class found in the full specs audit: the
user flattened ``.specify/specs/.archive/`` (parallel commits a7318075 /
d70b0519), after which Feature rows still pointed at dead ``.archive/`` paths.
Deprecated specs now live under ``.specify/archive/spec/`` (new convention).

C-1: every spec path referenced by a features.md row (when not ``-``) MUST
     exist on disk.
C-2: every ACTIVE spec's numeric ``Feature ID`` binding MUST have a matching
     row in features.md.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FEATURES_MD = REPO_ROOT / ".specify" / "memory" / "features.md"
SPECS_DIR = REPO_ROOT / ".specify" / "specs"
ARCHIVE_DIR = REPO_ROOT / ".specify" / "archive" / "spec"


def _feature_rows() -> list[dict[str, str]]:
    rows = []
    for line in FEATURES_MD.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d{3})\s*\|([^|]+)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|$", line)
        if m:
            rows.append({
                "id": m.group(1).strip(),
                "status": m.group(4).strip(),
                "detail": m.group(5).strip(),
                "spec": m.group(6).strip(),
            })
    return rows


@pytest.mark.contract
def test_c1_every_referenced_spec_path_exists():
    bad = []
    for row in _feature_rows():
        spec = row["spec"]
        if spec in ("-", "") or not spec.startswith(".specify"):
            continue
        if not (REPO_ROOT / spec).exists():
            bad.append(f"Feature {row['id']}: {spec}")
    assert not bad, (
        "features.md references non-existent spec paths (stale archive/move "
        f"references): {bad}"
    )


@pytest.mark.contract
def test_c2_active_spec_feature_bindings_resolve():
    feature_ids = {row["id"] for row in _feature_rows()}
    bad = []
    for spec_dir in sorted(SPECS_DIR.iterdir()):
        if spec_dir.name.startswith(".") or not spec_dir.is_dir():
            continue
        req = spec_dir / "requirements.md"
        if not req.exists():
            continue
        m = re.search(r"\*\*Feature ID\*\*:\s*(\d{3})",
                      req.read_text(encoding="utf-8"))
        if m and m.group(1) not in feature_ids:
            bad.append(f"{spec_dir.name}: Feature {m.group(1)} has no row")
    assert not bad, f"active specs bind unregistered Features: {bad}"
