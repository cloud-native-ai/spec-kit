# Data Model — 098 Suite Speed Optimizations

**Feature**: `098-suite-speed-optimizations` → Feature 086
**Date**: 2026-11-10
**Scope**: this feature has no database and no persisted product data. The entities below are the typed
surfaces its contracts and tests exchange. Where a field is machine-consumed by a guard, its spelling is
fixed here and MUST NOT be duplicated in prose elsewhere.

## E-1 — Test tier

| field | type | domain / rule |
|-------|------|----------------|
| `tier` | enum | `fast` · `full` · `caller` |
| `excluded_slow` | integer ≥ 0 | members of the slow marker excluded by this tier from the caller's selection (0 for `tier=caller` / `tier=full`) |
| `requested_by` | enum | `default` · `--full` · caller `-m` |

Invariants:
- `tier=caller` ⇔ the caller supplied its own `-m`; then no tier exclusion is applied and `excluded_slow=0`.
- `tier=full` ⇔ `--full` present and no caller `-m`; `excluded_slow=0`.
- `tier=fast` ⇔ neither of the above; exclusion applies and `excluded_slow` is the measured enumeration.
- Only `tier=fast` may change the selection relative to the caller's request.

Resolution (state list, not a transition table): inputs `caller_m` (present/absent), `full_flag`
(present/absent), `serial_flag` (present/absent); `caller_m=present` resolves `caller`; otherwise
`full_flag=present` resolves `full`; otherwise `fast`. `serial_flag` never changes the resolved tier.

## E-2 — Slow registry row

Carrier: `test-evidence/slow-members.md`, one pipe-table row per marked test.

| column | domain / rule |
|--------|----------------|
| `test_id` | pytest node id, exactly the form `path::test_name` (or `path::Class::test`) |
| `category` | closed: `process-boundary` · `corpus-scan` |
| `reason` | one sentence naming what the test spawns/waits for or which corpus it traverses |
| `date` | ISO date the row was measured (`YYYY-MM-DD`) |

Invariants:
- The set of `test_id` values equals the set produced by `pytest --collect-only -q -m slow` for the whole
  tree, one row per id, no duplicates, no orphans.
- A registry row never carries a hardcoded total; counts are derived at guard time.
- The guard test is not itself a member.

## E-3 — Session scan cache entry

| field | type | rule |
|-------|------|------|
| `surface` | enum | `framework-specs-corpus` · `framework-root-inputs` |
| `root` | path | real framework root (default) or a tmp corpus in drills |
| `variant` | string | frozen tuple of arguments that change the payload (e.g. baseline path, freeze flag) |
| `payload` | mapping | engine result, treated as read-only |
| `build_count` | integer | number of builds for this `(worker, surface, root, variant)`; must be 1 |
| `traversals` | integer | calls to `_corpus_files` during the build; must be 1 for `framework-specs-corpus` |
| `worker` | string | xdist worker id (`gw0`, …) or `none` |

Lifecycle (state list): `absent → building → ready → (session end) released`. There is no `stale` state:
freshness is provided by session boundaries, not by mtime or content polling; a new session (including each
xdist worker) starts at `absent`. Consumer access returns a deep copy; the stored payload is never mutated.
`test_c20`'s byte-identity check is not part of this cache — it stays a separate subprocess test.

## E-4 — Injected clock

| field | type | rule |
|-------|------|------|
| `option` | switch | `--now <YYYY-MM-DDTHH:MM:SSZ>` on `feedback-utils.py` |
| `applies_to` | set | every `now_iso()` / `timestamp_id()` reading in that invocation |
| `default` | absent | real clock, unchanged behaviour |
| `granularity` | second | the injected value must be second-granularity to match the engine's stored form |

Invariants: absent option ⇒ output byte-identical to the pre-change engine; the option is documented in
`--help`; an unparsable value exits non-zero with a named error. File mtimes used by closure assertions are
controlled separately with `os.utime`.

## E-5 — Event wait

| field | type | rule |
|-------|------|------|
| `predicate` | callable → bool | the observable condition (file exists, field value, mtime advanced) |
| `timeout` | float seconds | the helper's parameter name; explicit at the call site, default 30; >30 requires a recorded reason |
| `interval` | float seconds | ≤ 0.2 |
| `failure` | test failure | named message at the call site; never `skip` / `xfail` / retry |

Invariants: the wait returns as soon as the predicate holds; polling occurs only while it does not; a
timeout surfaces the named failure.

## E-6 — Conversion manifest row

Carrier: `test-evidence/inprocess-conversion.md`, one pipe-table row per classified call site or helper.

| column | domain / rule |
|--------|----------------|
| `file` | repo-relative test or fixture path |
| `call_site` | enclosing function name plus normalized target (engine name or command kind) |
| `verdict` | `convert` · `keep` |
| `boundary_class` | required for `keep`: `cli-contract` · `signal-timeout-interrupt` · `git-external` · `process-isolation-subject` · `other-interpreter` · `global-state-unrecoverable` · `copy-topology`; `—` for `convert` |
| `reason` | one sentence; for `convert`, the equivalence route (same assertions, in-process stdout/exit capture) |

Invariants:
- Every `subprocess.run` discovered by the AST scan of `tests/` resolves to exactly one row.
- A `keep` row's class must be one of the closed set; a `convert` row must name its equivalence route.
- The guard re-scans and fails naming any unclassified call site, and fails when a converted site was
  changed back to `subprocess.run`.

## E-7 — Runner disclosure lines

Fields carried on stderr, prefix-compatible with 086 C-002/C-003:

- Mode line: `# test runner: mode=<parallel|serial> [reason=<...>] [workers=<...>] [dist=<...>]
  passes=<k> tier=<fast|full|caller> excluded_slow=<n>` — existing fields keep their position and spelling;
  the two new fields are appended.
- Header line: `# test runner: <interpreter> -m pytest <arguments actually passed to the primary pass>` —
  the injected marker expression, when present, appears here.
- Empty-selection error line: `# test runner: error=empty-selection-after-tier-exclusion tier=fast
  excluded_slow=<n>` followed by exit 2.
- Failed-name line: unchanged from 086 C-014.

## E-8 — Two-slot budget row (existing, unchanged shape)

This feature changes only the command spelling in the three owner/restatement surfaces (`--full` added);
the ledger row fields, slot count, timing and order are owned by
`.specify/skills/sdd-loop-driver/references/efficiency-model.md` §2 and are not restated here.
