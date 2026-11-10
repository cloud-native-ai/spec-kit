"""Contract cases for the session scan cache (098 US3, C-001…C-004, C-007, C-010, C-011).

Owner of the propositions: `.specify/specs/098-suite-speed-optimizations/contracts/
scan-cache.contract.md`. Judgement surface: the factory in `tests/conftest.py` and the
payload it hands to consumers — never a re-implementation of the accountant here.

Cases:

1. ``test_c002_the_managed_surfaces_are_exactly_the_two_declared`` — the factory's
   surface enum is closed at the two managed surfaces; a third surface needs a contract
   revision first.
2. ``test_c003_the_factory_keeps_no_mtime_or_persistent_cache`` — static: the factory
   block carries no mtime/staleness token and no on-disk store. Freshness comes from
   session boundaries only (C-003 forbids in-session staleness detection).
3. ``test_c007_the_corpus_build_is_in_process_over_the_house_pattern`` — static: the
   corpus build loads `scripts/python/account-clause-coverage.py` with
   ``importlib.util.spec_from_file_location`` and wraps ``_corpus_files`` with a counter;
   it never shells out.
4. ``test_c001_c011_one_build_and_one_traversal_serve_two_consumers`` — two consumer
   requests for one key return the same entry, ``build_count == 1`` and
   ``traversals == 1``; a third surface request on another key builds independently.
5. ``test_c001_the_variant_is_part_of_the_key`` — a different variant (baseline path) is
   a different entry, so arguments that change the payload can never collide.
6. ``test_c004_a_consumer_mutation_never_reaches_the_store`` — consumer access returns a
   deep copy; in-place mutation of one copy is invisible to the next access.
7. ``test_c010_a_new_session_observes_a_tampered_corpus`` — the cross-session drill: a
   tmp corpus is built in one subprocess session, tampered, and rebuilt in a new session;
   the affected fields MUST change. A stale or constant cache fails this case.

Drill corpora live under pytest's ``tmp_path`` — the shared cache is only ever built over
read-only framework inputs or throwaway copies, never over a tree a case writes into
(C-005: the mutating cases keep their own per-test fixtures).
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
CONFTEST = ROOT / "tests" / "conftest.py"
REAL_SPECS = ROOT / ".specify" / "specs"
SPEC_053 = REAL_SPECS / "053-machine-decidable-artifacts"

BLOCK_BEGIN = "scan-cache begin"
BLOCK_END = "scan-cache end"


def _conftest_module():
    """The conftest module as a plain module object (the factory's home)."""
    assert CONFTEST.is_file(), f"missing fixture factory host: {CONFTEST}"
    spec = importlib.util.spec_from_file_location(
        "_scan_cache_conftest_under_test", CONFTEST
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _factory_block() -> str:
    """The factory section of conftest, bracketed by its own begin/end markers."""
    source = CONFTEST.read_text(encoding="utf-8")
    start = source.find(BLOCK_BEGIN)
    end = source.find(BLOCK_END)
    assert start != -1 and end != -1 and end > start, (
        "tests/conftest.py MUST bracket the scan-cache factory between "
        f"{BLOCK_BEGIN!r} and {BLOCK_END!r} comment markers; the static checks below "
        "judge that block and nothing else"
    )
    return source[start:end]


def _make_corpus(tmp_path: Path) -> Path:
    """A one-spec throwaway corpus with one contract clause, a tasks claim and a baseline."""
    corpus = tmp_path / "corpus"
    spec_dir = corpus / "001-alpha"
    (spec_dir / "contracts").mkdir(parents=True)
    (spec_dir / "requirements.md").write_text(
        "# Spec: 001-alpha\n\n## Functional Requirements\n\n"
        "- **FR-001**: one requirement.\n",
        encoding="utf-8",
    )
    (spec_dir / "contracts" / "c.md").write_text(
        "# Contract: c\n\n**C-1** [制品类] first clause. (FR-001)\n", encoding="utf-8"
    )
    (spec_dir / "tasks.md").write_text(
        "# Tasks: 001-alpha\n\n- [ ] T001 Pin it [green: contracts/c.md#C-1]\n",
        encoding="utf-8",
    )
    (spec_dir / "coverage-baseline.txt").write_text(
        "# coverage-baseline: drill fixture (header only, no names)\n", encoding="utf-8"
    )
    return spec_dir


DRILL_DRIVER = """
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("_drill_conftest", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
cache = module.ScanCache()
entry = cache.corpus(sys.argv[2])
payload = entry.payload
print(json.dumps({
    "worker": entry.worker,
    "build_count": entry.build_count,
    "traversals": entry.traversals,
    "scanned_total": payload["scanned"]["total"],
    "clause_universe": payload["clause"]["universe"],
    "uncovered": payload["clause"]["uncovered"],
}))
"""


def _run_drill_session(driver: Path, spec_dir: Path) -> dict:
    """One subprocess session: a fresh cache builds the tmp corpus and reports it."""
    proc = subprocess.run(
        [sys.executable, str(driver), str(CONFTEST), str(spec_dir)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        timeout=180,
    )
    assert proc.returncode == 0, (
        "the drill session MUST build and report:\n" + proc.stdout + proc.stderr
    )
    return json.loads(proc.stdout)


# --------------------------------------------------------------------------- #
# C-002 — the managed surface enum is closed
# --------------------------------------------------------------------------- #


def test_c002_the_managed_surfaces_are_exactly_the_two_declared():
    module = _conftest_module()
    surfaces = tuple(getattr(module, "SCAN_SURFACES", ()))
    assert surfaces == ("framework-specs-corpus", "framework-root-inputs"), (
        "the managed surfaces are exactly two (C-002): the accountant payload over "
        ".specify/specs and the framework-root inputs the coverage-receipt cases read; "
        f"a third surface requires revising the contract first — got {surfaces!r}"
    )


# --------------------------------------------------------------------------- #
# C-003 — no in-session staleness detection, no on-disk cache
# --------------------------------------------------------------------------- #


def test_c003_the_factory_keeps_no_mtime_or_persistent_cache():
    block = _factory_block()
    mtime_tokens = re.findall(r"st_mtime|getmtime|os\.stat\(|[^a-z_]\.stat\(", block)
    assert mtime_tokens == [], (
        "C-003 forbids in-session staleness detection: freshness is provided by session "
        f"boundaries, never by mtime or content polling — found {mtime_tokens}"
    )
    persistence_tokens = re.findall(r"pickle|shelve|sqlite3", block)
    assert persistence_tokens == [], (
        "C-003 forbids cross-session persistence: the cache is in memory only — "
        f"found {persistence_tokens}"
    )


# --------------------------------------------------------------------------- #
# C-007 — the build mechanics: in-process, house pattern, counted traversal
# --------------------------------------------------------------------------- #


def test_c007_the_corpus_build_is_in_process_over_the_house_pattern():
    block = _factory_block()
    for token in ("spec_from_file_location", "account-clause-coverage.py", "_corpus_files"):
        assert token in block, (
            f"the corpus build MUST use the house pattern ({token}): the fixture loads "
            "the accountant in-process and counts its _corpus_files traversals (C-007)"
        )
    assert "subprocess" not in block, (
        "the corpus build MUST NOT shell out: the cache exists to retire per-consumer "
        "subprocess scans, so a subprocess in the factory block defeats its own subject"
    )


# --------------------------------------------------------------------------- #
# C-001 / C-011 — one build, one traversal, many consumers
# --------------------------------------------------------------------------- #


def test_c001_c011_one_build_and_one_traversal_serve_two_consumers(scan_cache, tmp_path):
    assert re.search(
        r'@pytest\.fixture\(scope="session"\)\s*\ndef scan_cache\(', _factory_block()
    ), (
        "the factory fixture MUST be session-scoped (C-001/C-003): the lifetime is the "
        "session, so a per-test build (CA-M1) is a contract violation, not an optimisation"
    )
    spec_dir = _make_corpus(tmp_path)

    first = scan_cache.corpus(spec_dir)
    second = scan_cache.corpus(spec_dir)

    assert first is second, (
        "two consumer requests for one key MUST return the one built entry; a per-test "
        "build (CA-M1) is exactly the mutation this case exists to catch (C-001/C-011)"
    )
    assert first.build_count == 1, (
        f"build_count MUST be 1 for (worker, surface, root, variant); got {first.build_count}"
    )
    assert first.traversals == 1, (
        "the build MUST call _corpus_files exactly once (C-007/C-011); "
        f"got {first.traversals}"
    )
    assert first.access_count >= 2, (
        "this case is two consumers; the entry MUST count every access so the "
        f"build-count probe can distinguish consumers from builds — got {first.access_count}"
    )
    payload = first.payload
    assert payload["scanned"]["total"] == 1, payload["scanned"]
    assert payload["clause"]["universe"] == 1, payload["clause"]


def test_c001_the_variant_is_part_of_the_key(scan_cache, tmp_path):
    spec_dir = _make_corpus(tmp_path)
    default = scan_cache.corpus(spec_dir)
    again = scan_cache.corpus(spec_dir)
    assert again is default

    other_baseline = spec_dir / "other-baseline.txt"
    divergent = scan_cache.corpus(spec_dir, baseline=other_baseline)

    assert divergent is not default, (
        "the variant is part of the cache key (C-001): a different baseline path changes "
        "the payload and MUST build its own entry instead of reusing the first"
    )
    assert divergent.build_count == 1
    assert divergent.traversals == 1


# --------------------------------------------------------------------------- #
# C-004 — read-only store, deep-copy consumer access
# --------------------------------------------------------------------------- #


def test_c004_a_consumer_mutation_never_reaches_the_store(scan_cache, tmp_path):
    spec_dir = _make_corpus(tmp_path)
    entry = scan_cache.corpus(spec_dir)

    stored = entry.payload
    tampered = entry.payload
    assert tampered is not stored, "consumer access MUST return a fresh copy, not the store"
    tampered["scanned"]["total"] = -1
    tampered["scanned"]["named_files"].append("tampered/contract.md")
    tampered["clause"]["uncovered"].clear()

    fresh = entry.payload
    assert fresh == stored, (
        "a mutation of the returned copy reached the stored payload (CA-M2); consumers "
        "must never observe each other's writes (C-004)"
    )


# --------------------------------------------------------------------------- #
# C-010 — the cross-session mutation drill
# --------------------------------------------------------------------------- #


def test_c010_a_new_session_observes_a_tampered_corpus(tmp_path):
    spec_dir = _make_corpus(tmp_path)
    driver = tmp_path / "drill_session.py"
    driver.write_text(DRILL_DRIVER, encoding="utf-8")

    before = _run_drill_session(driver, spec_dir)
    assert before["build_count"] == 1 and before["traversals"] == 1, before
    assert before["scanned_total"] == 1, before
    assert before["clause_universe"] == 1, before

    (spec_dir / "contracts" / "extra.md").write_text(
        "# Contract: extra\n\n**C-9** [制品类] tampered-in clause. (FR-001)\n",
        encoding="utf-8",
    )

    after = _run_drill_session(driver, spec_dir)
    assert after["build_count"] == 1 and after["traversals"] == 1, after
    assert after["scanned_total"] == before["scanned_total"] + 1, (
        "a new session MUST rebuild and see the tampered corpus (C-010): a cache that "
        f"returned a stale or constant payload would repeat {before}, got {after}"
    )
    assert after["clause_universe"] == before["clause_universe"] + 1, (before, after)
    assert any(name.endswith("#C-9") for name in after["uncovered"]), after["uncovered"]
