# Quickstart run record — Feature 053

**Purpose**: the real output of actually running this feature's `quickstart.md` scenarios, teardown steps included. A scenario is only recorded as run when its command was executed and its output pasted here.

**Capture date**: 2026-10-03 · **BASE SHA**: see `pre-change-measurements.md`

<!-- one section per scenario, in execution order -->

## 场景 6 — US3 的条款形态普查与 owner 声明(改后实跑,2026-10-04,T027)

Command: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/053-machine-decidable-artifacts`

Real output, first 11 lines — **no number in this section was copied from the scenario row**, all were re-derived by this run:

```text
spec-dir: .specify/specs/053-machine-decidable-artifacts
corpus:   .specify/specs/*/contracts/*
owner forms (shared/definitions/contract-clause-definitions.md): md-bold-closed, md-bold-paren, md-heading, yaml-openapi, yaml-assertions; md-none named
scanned 117 files: parsed 64 + named-unparseable 53 == 117  [relational sentinel OK]
  per form (counts owned by notes/clause-form-census.md, re-derive, never restate): md-bold-closed 28 files/493 clauses; md-bold-paren 1 files/10 clauses; md-heading 25 files/141 clauses; yaml-openapi 9 files/39 clauses; yaml-assertions 1 files/6 clauses; md-none 53 files/0 clauses
  zero-clause-but-parseable (parse doubt): 0
  .yaml: parsed 10 / total 10 / named 0
named-unparseable: 53 (use --list-named to expand)
clause universe: 665 distinct names over 64 parsed files (689 ids extracted)
  collapsed: 24 extracted ids share a name with another in the same file, …
```

The scenario's expected result is met literally: three numbers, **64 + 53 == 117**, the sentinel relational rather than a literal, and the named list collapsed to a count by default.

**Collapsibility (C-9), both sides measured**: default run prints **0** `  NAMED: ` lines; the same run with `--list-named` prints **53**. So the flag is what expands it, and the default really is collapsed rather than merely short.

**The two "改前可实跑" probes, re-run now that the owner document exists** — the scenario's recorded values were `10 / 0 / 0`:

| probe | 改前(scenario record) | 改后(this run) | why it moved |
|---|---|---|---|
| `grep -c '\*\*C-[0-9]* (' …/031-…/rubric-section.md` | `10` | **10** | unchanged — the fifth form's evidence is a property of that spec, not of this feature |
| clause-syntax definition hits in `templates/ shared/ docs/` | `0` | **3** across **2** files | the probe was an *absence* proof; it now finds `shared/definitions/contract-clause-definitions.md` (the owner this feature created) and `templates/tasks-template.md` (US2's `[green:]` bullet, which uses the phrase "clause id" without defining it — a usage, not a second owner) |
| `find templates -iname '*contract*' -o -iname '*clause*'` | `0` | **0** | unchanged — this feature put the owner in `shared/definitions/`, not in `templates/` |

The middle row is the one worth stating: a probe whose purpose is to prove a thing is absent must be re-read as a *presence* probe once the thing lands, or it silently becomes a check that can only fail.

**A-8, found by this run.** `clause universe` prints **665 distinct names** while **689 ids** were extracted. The owner's `yaml-openapi` form names a clause by its HTTP method key, and 8 corpus files declare the same method under several paths, so 24 operations share a name with another and a name-set collapses them. Re-derived independently before trusting the tool's own number: `extract_clauses` over the corpus gives 689 ids as a list and 665 as a set, and the 24 are distributed over exactly those 8 files (worst case: one file with five `get` keys sharing one name). Disposition: **reported, never absorbed** — both numbers print, with the cause and a pointer to `research.md` A-8, and `tests/contract/test_clause_coverage.py::test_c7b_ids_that_collapse_into_one_name_are_reported_never_absorbed` pins it against a planted two-`post` OpenAPI file. Qualifying those ids by their path is a **syntax change** belonging to the owner document, so it was escalated as A-8 rather than decided inside an implementation task; the owner document now records the fact (non-uniqueness and the duty to report both numbers) without changing the syntax.

## 场景 7 — US3 的冻结基线与 `comm -13` 比对(改后实跑,2026-10-04,T027)

**The idiom on 052's real name sets (改前可实跑, unchanged)**: baseline **76** lines, current **65**, `comm -13` delta **0** — reproducing the scenario's recorded `76 / 65 / 0`.

**The coverage baseline, frozen this phase (T026)** — at the *first* full-tree run, not the first green one, and over the corpus **excluding** this feature's own spec dir:

```text
names: 483   header lines: 2   LC_ALL=C sort -c: OK
header: # frozen-from: .specify/specs/*/contracts/* excluding 053-machine-decidable-artifacts |
        owner-forms: md-bold-closed,…,md-none (md-none named, never silently covered) |
        clause-rules: shared/definitions/contract-clause-definitions.md |
        per-form counts: notes/clause-form-census.md | base-sha: 145b69444d7d |
        files: 110 (parsed 57 + named 53)
items from 053's own spec dir inside the baseline: 0
```

The freeze面 is the census's stable **excl-053** basis — 110 files, parsed 57 + named 53 — and the header carries all four comparability facts C-23 demands (form set, rules owner, corpus selector, base SHA). Zero of this feature's own items are in it, which is what makes the gate below capable of going red.

**Live run against that baseline**, and the paired `comm -13` proof:

```text
claimed clauses (this feature): 0
baseline: …/coverage-baseline.txt (483 names)
baseline-internal existing uncovered: 483
uncovered beyond baseline: 182
FR universe: 48 | FR claimed: 48 | FR uncovered: 0
companion: claimed clauses 0, scanned files 117, clause universe 665, FR universe 48
182 error(s), 0 warning(s)          status: uncovered          ACC_EXIT=1

LC_ALL=C comm -13 coverage-baseline.txt <(live UNCOVERED names)
  → 182 names, comm stderr empty
  → of those, names NOT under 053-machine-decidable-artifacts/: 0
independently re-derived: 053's own contracts hold 182 clause ids
```

So the scenario's expected result is **not yet satisfiable, and that is the correct state at T027**: the criterion is "delta empty **AND** this feature's claimed count non-empty", and both halves fail for the same reason — the claims only land at T045. What this run proves is the stronger property the criterion exists for: the delta is *exactly* this feature's own 182 clauses and nothing else, so the baseline exempts the pre-existing 483 items of other specs while exempting **none** of 053's own. The gate is red now, for the right reason, and T045 is what turns it green — a gate that had been green all along would have been the defect FR-027 § 基线面 was amended to prevent.

**A second measured defect, in the idiom rather than the tool.** The first `comm -13` attempt printed `comm: file 1 is not in sorted order` and then reported a delta of **665** instead of 182 — a wrong verdict that still looked like output. Cause: the names are codepoint-sorted (Python's `sorted`), but glibc collation ignores `#`, `/` and `.` at the first level, so under `en_US.UTF-8` the two `#`-prefixed header lines sort *after* digit-initial names. `LC_ALL=C sort -c` accepts the file and the ambient locale rejects it at line 3. Disposition: the idiom is specified with `LC_ALL=C` in three places that a reader could reach it from — the baseline header itself, the script's docstring, and `tasks.md` GATE-8 — and pinned twice in `test_clause_coverage.py` (`test_c24…` now runs `comm` under `LC_ALL=C` with **both** sides non-empty, because with an empty baseline `comm -13` echoes all of file 2 whatever the ordering and my first version of that test passed for that weak reason; `test_c24b…` pins the file as C-sorted with exactly two header lines). The script's internal delta is a set difference and is locale-independent, so it stayed authoritative throughout — the two agreed at 182 once the locale was fixed.
