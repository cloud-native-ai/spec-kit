# SC-010 Dependency Boundary Checks (RC-08 / quickstart S7) — 2026-10-22 · T037

**Owner of this record**: T037 (Phase 9 closure slot). **Criterion**: FR-019 / SC-010 — runtime dependency set unchanged vs pre-change (empty `pyproject.toml` runtime diff); test-side new deps 100% dev-group; zero new network calls in test code. **Implementation base commit**: `7f9033ec` (master point the feature branch cut from, per U0).

## 1. Runtime dependency diff (must be empty)

```text
$ git diff 7f9033ec..HEAD -- pyproject.toml
(no output — diff byte count: 0)
```

**PASS** — the whole `pyproject.toml` is untouched on the delivery interval, so the `[project] dependencies` (specify-cli runtime) set is bit-identical to pre-change; the optional-dev-dependencies groups are equally untouched, which trivially satisfies "any test-side new dependency must live in the dev group" — there are **zero** new dependencies of any group (expected-zero held, FR-019 first clause).

## 2. Test-side new dependencies

Consequence of §1 (empty pyproject diff): no new test dependency was introduced anywhere. `tests/` diff on the interval: 42 files, +801/−383 lines — all organizational (fold into the parametrized suite, fixture cloning, in-process rewrites), no import of a package outside the pre-existing test surface. No `requirements*.txt` / `setup.py` / `setup.cfg` changed on the interval.

## 3. Network-call scan in tests (added lines = 0)

Per tasks.md T037 literal command plus the addition-only refinement:

```text
$ git diff 7f9033ec..HEAD -- tests/ | grep -E "urllib|requests|httpx|socket"
(no output)

$ git diff 7f9033ec..HEAD -- tests/ | grep -E '^\+.*\b(urllib|requests|httpx|socket)\b'
(no output — added-line matches: 0)
```

**PASS** — zero occurrences of any network token in ANY changed line of `tests/` (stronger than required: not even removed or context lines mention them). Tests remain offline-runnable (the closure full run itself executed the whole suite on the baseline host without network steps).

## 4. Verdict

**SC-010: PASS** — all three checks green: runtime dependency diff empty; test-side new dependencies = 0 (dev-group clause vacuously satisfied, nothing to place); new network calls in test code = 0.
