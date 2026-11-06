# Red-first evidence — Feature 088, implement Part 1 (T006, T007)

**Capture date**: 2026-11-06T06:52Z (UTC)
**Discipline**: Constitution IV (Test-First & Contract-Driven Implementation). Each test row precedes its
implementation row; the reading below is the RED state measured **before** T008/T009 existed.

## RED reading — before T008 and T009

**Command (verbatim)**:

```bash
python3 -m pytest -q tests/unit/test_status_digest_unit.py tests/contract/test_reporting_obligations.py
```

**Result**: `34 failed, 1 passed in 0.32s` (`rc=1`)

| File | Red-first row | Failing at RED | Note |
|------|---------------|----------------|------|
| `tests/unit/test_status_digest_unit.py` | T006 | 15 of 16 | the one pass is `test_engine_constants_are_the_authority_not_the_test`, a guard over the imported `STATE_VALUES` / `ACTIVE_STATES` sets and not over the missing script — it stays green by construction |
| `tests/contract/test_reporting_obligations.py` | T007 | 19 of 19 | every test asserts the owner document or a fact carried by it |

**Why this is red for the right reason**: each failing test asserts its subject's existence before its content
(`_require_engine()` / `_read()` raise an assertion naming the missing path), so the failure text is
"artifact missing", never an `ImportError`, `CollectionError` or syntax error. A red produced by a broken test file
would prove nothing about the missing implementation.

## What turns each file green

- `tests/unit/test_status_digest_unit.py` → **T009** (`scripts/python/status-digest.py`): registry resolution order,
  triplet projection, the state vocabulary quoted from the engine, the read-only boundary, the three-action surface.
- `tests/contract/test_reporting_obligations.py` → **T008** (`shared/guidelines/reporting-obligations.md`): the
  single-source-of-truth declaration with exactly eight owned facts, the four non-owned owners by path, the scope
  predicate, the one 30-second definition site, the four element labels by anchor, the three transition classes, the
  nine-term prohibition, the not-a-gate clause.

The GREEN readings are recorded in `test-evidence/implement.jsonl` (E3 rows) after the implementation lands; this
file records the RED half only, so the red→green transition stays auditable from two dated artifacts.

## Scope boundary kept deliberately

This file's tests cover **reader-level** script behaviour and **owner-document** obligations. Not asserted here, and
therefore not attributable to these two rows: the digest's bounding/ordering/`omitted`/exit-status set (T027), the
thirteen guard propositions (T033), the rendered status line (T016), the roster guard (T011), and the coaching
payload amendment (T020). Each of those rows adds its own assertions to the same files.

---

# Part 2 (US1) — RED readings before T013–T017

Two files were authored red-first for this part: `tests/contract/test_roster_reporter_seat.py` (T011) and the US1
section added to `tests/contract/test_reporting_obligations.py` (T012). The readings below were taken **before** the
implementation rows (T013 guard, T014 Template, T015 schema, T016/T017 renderer third action) existed.

## RED reading A — the roster-guard / seat contract (T011)

**Command (verbatim)**:

```bash
python3 -m pytest -q tests/contract/test_roster_reporter_seat.py
```

**Result**: `23 failed, 1 passed` (`rc=1`), taken immediately after the file was authored.

**Why this is red for the right reason**: `_run_guard()` asserts `GUARD.is_file()` before shelling out, and `_read()`
asserts the artifact path before reading it. The failure text is therefore
`roster guard missing: skills/internal/create-team/scripts/validate-roster.py — expected at T013 (087)`, not an
`ImportError` or a collection error. A red produced by a broken test file would prove nothing about the missing
implementation.

**The one pass, disclosed rather than glossed**: `test_no_parallel_reporter_key_is_introduced` passed at RED. The scan
is scoped to the fenced ```` ```markdown ```` schema block of `references/create-mode.md` (via `_schema_block()`), and
the pre-T015 schema legitimately contains no `reporter:` line — so it passes by construction, not by proving anything
about the delivered schema. An earlier form of this test scanned the whole file, which made it fail for the wrong
reason: prose elsewhere in the file may write the word and a whole-file scan would force the prose to avoid it rather
than judge the schema. The scoped form plus an explicit `assert schema, "sanity: …block must be locatable"` keeps the
test honest: it can no longer pass vacuously by finding nothing to scan.

## RED reading B — the status-report assertions (T012)

**Command (verbatim)**:

```bash
python3 -m pytest -q tests/contract/test_reporting_obligations.py
```

**Result at RED**: 3 failed, 25 passed — the three failures being
`test_reporter_template_authority_deny_list`,
`test_reporter_template_exists_on_both_sides_of_the_pair` and
`test_reporter_template_is_framework_neutral`, each failing on its own first assertion naming the missing
`agents/reporter.agent.md`. The renderer assertions could not be red here for a structural reason: `--action report`
already existed as an entry point from T009 (Part 1), so T012's render tests were authored against an action that
already existed and were red only on the *Template* artifacts. This is recorded rather than hidden — the render half of
T012 is a **regression** guard over T016/T017's shape, not a red-first guard.

## GREEN readings — after T013 … T017

| Command | Result |
|---|---|
| `python3 -m pytest -q tests/contract/test_roster_reporter_seat.py` | `24 passed` |
| `python3 -m pytest -q tests/contract/test_reporting_obligations.py` | `28 passed` |
| `python3 -m pytest -q tests/unit/test_status_digest_unit.py tests/contract/test_reporting_obligations.py tests/contract/test_roster_reporter_seat.py tests/contract/test_progress_reporting.py` | `75 passed` (`rc=0`) |

## A discovered-correctness defect found by T018's real-roster render (disclosed)

The guard's first form parsed only single-line scalars, so it exited `2` (input error) on **every** real roster in the
tree — all 13 of them use a folded `goal: >` block scalar, and several use nested block sequences under
`territory.write`. That is a **correctness** defect in the code, not an ambiguity about intent: C-16 says a
`reporting-reason`-less roster with no seat is the `absent-seat` defect (exit 1), and silently classifying 13 real
rosters as unreadable would have made the guard useless on exactly the artifacts it exists to judge. It was fixed in
place (block scalars consumed; deeper-indented nested entries skipped, since only `config.reporting-reason` and the
members' own fields are ever read) and disclosed here. After the fix, all 13 real rosters return the correct
`absent-seat` / `rc=1`, and the fixture returns `conforming` / `rc=0`.

## A test-side registration the new Template required (disclosed)

`tests/contract/test_fast_fail_discipline.py` holds a **bounded** enumeration of the framework Agent presets
(`FACTORY_PRESETS`) plus two counts over it (`C-10`: 16 presets; `C-12`: 16 presets + 2 authoring texts = 18). Adding
`agents/reporter.agent.md` is exactly the case the enumeration's own assertion message anticipates ("update the
enumeration deliberately"), so the constant and both counts were updated to 17 / 19. The Template's clause interval is
byte-identical to the owner literal, which is what makes that registration a green reading rather than a waiver.

A second-order effect, reverted rather than committed: running the render engine for the new Template rewrote **60
unrelated** per-tool agent copies across the four host trees. Those were reverted, leaving only the four new
`reporter` copies. The pre-existing `C-11` / `G-9` failures remain identical to the recorded baseline
(`baseline-full-suite-20261106T063158Z.log` lines 1203–1204) — same assertions, same `sdd-analysis-worker` class of
file, no path this part touched.

### Correction to the paragraph above (measured, after the re-render)

The 60 unrelated per-tool copies were reverted, but a **second** finding surfaced while doing so and is worth
recording because it silently produces wrong output: `from specify_cli import render_agents_for_tool` resolves to the
**installed** package (`/usr/local/lib/python3.11/site-packages/specify_cli/__init__.py`), whose renderer does **not**
apply the body-rewrite rule. Rendering through the installed package writes per-tool copies whose clause interval still
reads `` `shared/guidelines/fast-fail.md` `` instead of the runtime `` `.specify/shared/guidelines/fast-fail.md` ``,
so `C-11` fails on the new file for a reason that looks like a source defect but is a stale-install artifact.

The correct render for this tree is the repo source:

```bash
python3 -c "import sys; sys.path.insert(0,'src'); from pathlib import Path; import specify_cli; \
  [specify_cli.render_agents_for_tool(Path('.'), t) for t in ('qoder','claude','copilot','opencode')]"
```

After that render, the four `reporter` copies carry `.specify/shared/guidelines/fast-fail.md` inside the clause
interval and `test_i11` returns to its **recorded baseline** failure
(`.qoder/agents/sdd-analysis-worker.agent.md`, the same file the baseline log names at line 1203). The manifest
`.specify/agents/.render-manifest.json` was reverted to its committed state so the change surface carries only the
four new `reporter` copies — the manifest is a whole-tree record and rewriting it for one new file would misreport
every other agent's render state.
