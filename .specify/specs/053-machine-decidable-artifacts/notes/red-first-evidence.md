# Red-first evidence — Feature 053

**Purpose**: every test that MUST go red before its subject exists gets its command, real output and exit status recorded here (Tests Mode = ON, Constitution Principle IV). Red-first output is pasted, never predicted.

**Capture date**: 2026-10-03 · **BASE SHA**: see `pre-change-measurements.md`

<!-- entries are appended per task; each carries the task id, the command, the verbatim failing output and the exit code -->

## T004 — tests/contract/test_clause_forms.py (2026-10-03)

```
$ bash .specify/scripts/bash/run-tests.sh -q tests/contract/test_clause_forms.py
^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'clause_extract'
=========================== short test summary info ============================
ERROR tests/contract/test_clause_forms.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.09s
EXIT=2
```

Red for the right reason: the subject module does not exist yet. 24 test functions collected-by-intent (the suite errors at import, so collection is interrupted — that is the expected red form for a missing module, not a syntax defect in the test file).

## T007 — tests/contract/test_checker_form.py (2026-10-03)

```
$ bash .specify/scripts/bash/run-tests.sh -q tests/contract/test_checker_form.py
17 failed, 17 passed, 11 skipped
```

Red for the right reason: `scripts/python/validate-requirements.py` does not exist, and this suite makes an absent in-phase subject a **failure**, not a skip (a skip would have let the suite look green with its subject missing). The 11 skips are the `account-clause-coverage.py` parametrizations, whose owner is T024/T025 in US3 — each skip names that.

Three assertion defects in this suite were found by running it and attributed to the **assertion** side, not the subject:
- C-12's proxy looked for the skeleton criterion in the two contracts; neither states it (and adding a clause would move a pinned count), so the truth source is the checker's own docstring — test rewritten to assert that.
- C-26's grep for `goal_utils.EXIT` matched **this suite's own source** (the needle was written as an instance); the test now excludes itself — the same trap recorded earlier in this feature's history.
- C-28's regex assumed `help=` sits on the `add_parser(` line; it does not, so the extraction returned nothing and would have passed vacuously. Rewritten with `ast`, plus a floor on the number of extracted helps so an empty extraction fails instead of passing.

## T009 / T010 — validate-requirements.py on reality (2026-10-03)

**FR-043 real-artifact run** (this spec's own requirements.md):

```
$ python3 scripts/python/validate-requirements.py .specify/specs/053-machine-decidable-artifacts/requirements.md
file: .specify/specs/053-machine-decidable-artifacts/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 317 lines, 60 definition rows, 10 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

**SC-001 — the four broken copies, built by quickstart 场景 3's block run VERBATIM** (extracted from the file and executed, not retyped). Each names exactly its own class; zero cross-masking:

| copy | construction | labels reported | exit |
|---|---|---|---|
| b1 | `grep -v '^- \*\*FR-030\*\*'` | `id-contiguous` only — "the FR sequence skips FR-030" | 1 |
| b2 | the `REORDER_EOF` heredoc moving SC-002 after SC-005 | `doc-order` only — `ORDER BREAK: SC-002 after SC-005` (the STR-002 literal) | 1 |
| b3 | `sed 's/\[\[STR-005\]\]/[[STR-999]]/'` | `ref-resolvable` only — 4 errors + 1 warning, all that label | 1 |
| b4 | `sed` inserting `[NEEDS CLARIFICATION: probe]` | `marker-count` only | 1 |

Residue after the battery: `\rm -rf $tmp` then `ls -d $tmp | wc -l` → **0**.

**Whole-corpus run (44 specs)** — recorded because it is the honest denominator, not a cherry-picked three:

```
exit 0: 26 specs   ·   exit non-zero: 18 specs
non-zero by label set: {('ref-resolvable',): 14, ('doc-order','ref-resolvable'): 1, ('id-contiguous',): 3}
```

Spot-checked, all **true positives**: `016`/`020` have `Consumed by` cells naming FRs whose rows re-type the literal instead of citing `[[STR-nnn]]` (exactly the drift C-15 exists to catch); `040-agent-metadata-portability:176` really does define `FR-023a`, a letter suffix this spec's own edge cases judge a format violation. So the 18 are pre-existing debt in specs written before the citation convention, not checker noise. GATE-10's "three real specs exit 0" is satisfied from the 26 (first three: `001-unify-command-handoffs`, `003-speckit-agents-command`, `006-add-qoder-support`).

**Consequence worth recording**: FR-012/C-18 make `/speckit.requirements` STOP on any ERROR, so re-running that command against one of the 18 debt-carrying specs will now halt where it previously did not. That is the intended behavior for a newly written spec; the debt itself is out of this feature's scope (FR-027's philosophy — do not require retrofitting existing specs) and is recorded here rather than fixed in passing.

**Two subject defects found by running, and one premise falsified:**
- padding was measured on the parsed integer, so every `FR-001` was reported as unpadded — the digits must be kept as written;
- the Shared Strings table was matched on the code-span-stripped view, where the backticked `` `STR-001` `` cell is erased → 0 strings found and 24 false dangling-reference errors. Structure is matched on the fence-blanked original; only *mention* scanning uses the stripped view;
- the quickstart's b1 originally deleted `FR-023`, which two other rows cite in prose — that would have fired `ref-resolvable` too and broken SC-001's zero-cross-masking. The scenario's premise block had only ever verified "a gap appears", never "only one class reports". Switched to `FR-030` (measured: 20 FR ids have zero non-definition mentions).

## T016 — US1 story checkpoint (2026-10-03)

Independent Test, all three legs run:

1. **Checker on three real specs → exit 0 each**: `001-unify-command-handoffs`, `003-speckit-agents-command`, `006-add-qoder-support` (chosen from the 26 of 44 that pass; the distribution is recorded in the T010 entry above rather than hidden).
2. **Four broken copies → exit 1 each, naming exactly its own class**: see the T010 table (4/4, zero cross-masking, residue 0 after `\rm -rf $tmp`).
3. **Transitional copies retired**: `grep -c '```awk' shared/constants/clarify-taxonomy.md` → **0**; `Until that validator ships` → **0**; `validate-requirements.py` mentioned **2×** in that file (the invariant now points at the checker).

Suite state: `test_clause_forms.py` + `test_checker_form.py` + `test_requirements_checker.py` + `test_clarify_semantic_completeness.py` → **76 passed, 11 skipped, 0 failed** (the 11 skips are `account-clause-coverage.py` parametrizations owned by T024/T025, each naming its owner).

Mirrors: `scripts/python` EXIT=2 with only the recorded pre-existing `trigger-utils.py` (no NEW drift); `shared/guidelines` and `shared/constants` EXIT=0; all three mirrors byte-identical (`cmp`). Per-tool copies regenerated, `regen-command-copies.py --check` EXIT=0, and all 4 `speckit.requirements` copies carry the new invocation line.

Hygiene: `scan-confirmation-gates.py --summary` → **23 / 13 / 10 / 0**. A BLOCKING_RE pass over all 14 files this story touched found **1** hit — `tests/contract/test_clarify_semantic_completeness.py:68`'s `PREEXISTING_GATE_FRAGMENT` constant, which `git diff` confirms this phase did not add, and `tests/` is not in `SCAN_DIRS` (`templates/commands`, `skills`, `shared`), so the budget is unaffected. `templates/commands/requirements.md` repo-name hits: **0**.

**Process deviation, disclosed (Phase 3)**: `gate-check.py` was run BEFORE the edits for Phases 1 and 2, but for Phase 3 it was run only after the edits landed. The retroactive verdict is `allow` for all six paths, EXIT=0 — no DENY or CONFIRM row, so nothing was written that the gate would have blocked; the ordering is still wrong and MUST be carried into `verification.md` `notes=` at T049. Phases 4-8 run the gate before their first edit.
