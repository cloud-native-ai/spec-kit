"""Shared parametrized mirror-parity suite (spec 067 T019 — plan W3, FR-014 / FR-018).

Table source of truth is the engine: ``scripts/python/sync-mirrors.py`` owns
``MIRROR_PAIRS`` and the enumeration/compare semantics (``iter_files`` /
``compare_pair``). This suite importlib-loads the engine and derives its whole
parameter table from it — no pair is restated here (One Source of Truth /
Tool Reuse), so a pair or file the engine learns about is covered here
automatically. House loading pattern: ``tests/contract/helpers_prompt_assets.py``
(also loads this same engine module by path).

What each test pins:

* ``test_mirror_file_byte_identical`` — one param per SOURCE file across all
  engine pairs; asserts the mirror twin is present and byte-identical. This is
  the ``compare_pair`` missing/differing half, per file, with both paths in the
  param id (FR-020: a failure names its own source→mirror file pair and the
  node id is directly re-runnable).
* ``test_pair_mirror_extras_match_engine_strictness`` — the ``extra_in_dst``
  half at exactly the engine's strictness: strict pairs (``scripts``) fail on
  mirror-only ORPHAN files; lenient pairs keep the engine's note-only
  semantics (a mirror-only file is NOT a failure here either — the suite does
  not tighten the engine, per T019's non-strict exception rule).

Scope note: ``templates/commands`` per-tool copies are not a ``MIRROR_PAIRS``
entry (the engine CLI delegates them to ``regen-command-copies.py``) and are
intentionally outside this pair-table suite.

Known-red note (T019): params whose file pair is currently drifted are
EXPECTED failures — the real mirror drift behind the mirror-class baseline
failures (SC-008 relative semantics, T023 owns the mechanism-side sync fix).
No folded test may be deleted to make this suite look greener (FB-07); fold
discipline (T020–T022) points case-merge ledger rows at these params
(``test-evidence/test-consolidation-ledger.md``).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]


def _load_engine():
    path = ROOT / "scripts" / "python" / "sync-mirrors.py"
    spec = importlib.util.spec_from_file_location("_sync_mirrors_parity_engine", path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SYNC_MIRRORS = _load_engine()
REPO_ROOT = SYNC_MIRRORS.REPO_ROOT


def _file_pair_params():
    """One param per canonical source file, table derived from the engine."""
    params = []
    for src_name, dst_name, _strict_extras, exclude_parts in SYNC_MIRRORS.MIRROR_PAIRS:
        src_root = REPO_ROOT / src_name
        dst_root = REPO_ROOT / dst_name
        for rel in SYNC_MIRRORS.iter_files(src_root, exclude_parts):
            rel_posix = Path(rel).as_posix()
            params.append(pytest.param(
                (src_root, dst_root, rel),
                id=f"{src_name}/{rel_posix}->{dst_name}/{rel_posix}",
            ))
    return params


@pytest.mark.parametrize("file_pair", _file_pair_params())
def test_mirror_file_byte_identical(file_pair):
    src, dst, rel = file_pair
    mirror = dst / rel
    assert mirror.is_file(), f"mirror file missing: {mirror} (engine compare_pair MISS)"
    assert (src / rel).read_bytes() == mirror.read_bytes(), (
        f"mirror drift: {mirror.relative_to(REPO_ROOT)} "
        "(engine compare_pair DIFF; sync fix owned by 067 T023)"
    )


def _pair_params():
    return [
        pytest.param(
            REPO_ROOT / src_name,
            REPO_ROOT / dst_name,
            strict_extras,
            exclude_parts,
            id=f"{src_name}->{dst_name}",
        )
        for src_name, dst_name, strict_extras, exclude_parts in SYNC_MIRRORS.MIRROR_PAIRS
    ]


@pytest.mark.parametrize("src,dst,strict_extras,exclude_parts", _pair_params())
def test_pair_mirror_extras_match_engine_strictness(src, dst, strict_extras, exclude_parts):
    if not src.exists():
        # Engine main() skips a placeholder-only source pair (mirror is canonical).
        pytest.skip(f"placeholder-only source pair: {src} (engine skips; mirror canonical)")
    _missing, _differing, extra = SYNC_MIRRORS.compare_pair(src, dst, exclude_parts)
    if strict_extras:
        assert not extra, (
            "mirror-only ORPHAN files in a strict pair (engine --check exits 2): "
            + ", ".join(f"{dst}/{rel}" for rel in extra)
        )
    # Lenient pairs: the engine reports mirror-only files as notes, never
    # failures — this suite keeps that exact semantics, no extra tightening.
