# Implement part 10a — T048-T053 (Polish: mirror total, cost/structure finals, Feature index, red-flag wrap-up, structure validation, C-34)

- **stage**: implement
- **part**: 10a of 10 (the brief splits P10: this part closes T048-T053; the Completion Gate, the
  Feature status flip and the implement wrap-up are part 10b and are **not** run here)
- **part_scope**: `T048-T053`
- **stage_base**: `e3d70068`
- **test_budget**: targeted-set-v1 (E2's single full-suite run stands: 26 failed / 7156 passed /
  1 skipped; **no second full suite is run here**)
- **docs-only**: no — one contract module (`test_self_explanatory_glossary.py`, T053's C-34 assertions)
  plus four documentation artifacts; no production source file edited, no shipped template edited, no
  mirror rewritten, glossary store byte-identical

## E3 stage-status row (implement part 10a)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T048-T053 |
| status | polish-finals-green-c34-guarded-gate1-2-3-pass-gate4-deferred |
| command | (1) `python3 scripts/python/sync-mirrors.py --check`; (2) `python3 scripts/python/regen-command-copies.py --check`; (3) six `cmp -s <source> .specify/<source>`; (4) `bash scripts/bash/generate-instructions.sh`; (5) `wc -c .specify/instructions.md`; (6) `grep -n '^INSTRUCTIONS_BUDGET_BYTES='` on both trees; (7) `python3 scripts/python/scan-confirmation-gates.py --json`; (8) `python3 -m pytest tests/contract/test_self_explanatory_glossary.py -q`; (9) GATE-1 trio: `pytest test_constitution_double_landing.py test_instructions_section_propagation.py test_glossary_mechanism.py -q`; (10) the four guard modules + baseline-adjacent suites; (11) `python3 .specify/scripts/python/validate-tasks.py …tasks.md`; (12) `grep -cE '^- \[[ >]\]' …tasks.md`; (13) `python3 scripts/python/account-clause-coverage.py .specify/specs/082-self-explanatory-integration` |
| selection_basis | targeted-set-v1 — exactly the surfaces this part measures or edits: the mirror engine and the command-copy regenerator (T048/GATE-2), the generator and its budget constant (T049), the gate scanner (T049), the glossary carrier T053 lands in, the three suites GATE-1 names plus the fourth guard class `plan.md` EP-004 names, and the tasks file T052 validates |
| selected_paths | `tests/contract/test_self_explanatory_glossary.py` (edited: T053's C-34 assertions, carried unmodified from the part-9 hand-off), `tests/contract/test_constitution_double_landing.py`, `tests/contract/test_instructions_section_propagation.py`, `tests/contract/test_glossary_mechanism.py`, `tests/contract/test_mirror_parity_suite.py`, `tests/contract/test_proactive_trigger_section.py`, `tests/contract/test_self_explanatory_constitution.py`, `tests/contract/test_self_explanatory_distribution.py`; read-only subjects: `scripts/python/sync-mirrors.py`, `scripts/python/regen-command-copies.py`, `scripts/bash/generate-instructions.sh` (+ mirror), `scripts/python/scan-confirmation-gates.py`, `.specify/instructions.md`, `.specify/memory/features/082.md`, `.specify/memory/features.md`, `.specify/specs/082-self-explanatory-integration/tasks.md` |
| sufficiency | the polish rows are **measurement rows**, not new guards: their evidence is command output (exit codes, byte counts, per-file counts, the gate total) and six of the seven close nothing that a test could assert. The one row that lands a guard is T053, and its carrier is the glossary module — hence its inclusion in the selected set. GATE-1's named trio plus the fourth guard class are the complete automated judge set for the feature's four guard classes; the four feature modules are added because they own the new assertions. Sufficiency is claimed for **the measurement and edit set**; the full-suite verdict belongs to the Completion Gate, which this part does not run |
| rc | 0 (sync-mirrors), 0 (regen), 0 (six `cmp`), 0 (generator), 0 (glossary carrier, 14 passed), 0 (GATE-1 trio, 37 passed), 1 (the four-guard-plus-baseline set, 1 failed — the inherited EP-003 pin), 0 (four feature modules, 798 passed), 0 (validate-tasks), 1 (`grep -c` returning the wanted **0**), 0 (coverage accountant, `status: uncovered` by the frozen baseline's design) |
| passed / failed | 14 passed (glossary carrier, was 10 in part 9); 37 passed (GATE-1 trio); 821 passed / 1 failed (four-guard + baseline set; the failure is baseline-inherited); 798 passed (four feature modules); **new_failures: none** |
| baseline | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries); name-level comparison `LC_ALL=C comm -13` — the only failure in the selected set (`test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`) is **in** the baseline (`grep -c` → 1), so nothing is left over |
| evidence_ptr | `notes/quickstart-run.md` § T049 and § T052 (raw transcripts); `notes/red-first-evidence.md` § T051 (the four pairs, each green re-executed); `notes/pre-change-measurements.md` § T044/§ T046 (carried from part 9); this file |

## Command output, verbatim

```console
# T048 / GATE-2 — the mirror total
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
RC_SYNC=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
RC_REGEN=0

# T048 — the six mirrored sources the plan table names, byte for byte
IDENTICAL shared/definitions/self-explanatory-definitions.md
IDENTICAL shared/guidelines/self-explanatory.md
IDENTICAL shared/workflow/best-practice-optimization.md
IDENTICAL templates/constitution-template.md
IDENTICAL templates/instructions-template.md
IDENTICAL scripts/bash/generate-instructions.sh

# T049 — the budget verdict (the `within` branch is the info line + headroom; the token is never printed)
$ bash scripts/bash/generate-instructions.sh
[2026-11-05 14:28:22][1886573][INFO]Section reconcile: live instructions already carry all template sections.
[2026-11-05 14:28:22][1886573][INFO]Instructions size: 33357 B (budget 34816 B, 1459 B headroom). Section table, largest first:
success Instructions generated/updated at .specify/instructions.md
RC_GEN=0

$ wc -c .specify/instructions.md
33357 .specify/instructions.md

$ grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh .specify/scripts/bash/generate-instructions.sh
scripts/bash/generate-instructions.sh:53:INSTRUCTIONS_BUDGET_BYTES=34816
.specify/scripts/bash/generate-instructions.sh:53:INSTRUCTIONS_BUDGET_BYTES=34816

# T049 — zero new gate hits
$ python3 scripts/python/scan-confirmation-gates.py --json
total= 27
by_class= {'governance_kept': 7, 'destructive': 20}
by_verdict= {'keep_gate': 27}
violations= []
RC_SCAN=0

# T053 — the C-34 carrier (carried from the part-9 hand-off, not rewritten by this part)
$ python3 -m pytest tests/contract/test_self_explanatory_glossary.py -q
..............                                                           [100%]
14 passed in 0.18s
RC=0

# T052 / GATE-3 — no unchecked or held rows remain (the same command read 6 before this part's closures)
$ grep -cE '^- \[[ >]\]' .specify/specs/082-self-explanatory-integration/tasks.md
0
GC_RC=1     # grep's "no match" exit — the wanted absence

$ grep -cE '^- \[X\] T' .specify/specs/082-self-explanatory-integration/tasks.md
53

# T052 — structure validation
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/082-self-explanatory-integration/tasks.md
PASS (with warnings): .specify/specs/082-self-explanatory-integration/tasks.md — 0 error(s), 34 warning(s)
RC_VALIDATE=0

# T052 / GATE-1 — the named trio
$ python3 -m pytest tests/contract/test_constitution_double_landing.py \
      tests/contract/test_instructions_section_propagation.py \
      tests/contract/test_glossary_mechanism.py -q
.....................................                                    [100%]
37 passed in 1.81s
RC=0

# T052 / GATE-1 — the fourth guard class + the baseline-red-adjacent suites, name-level comparison
$ python3 -m pytest tests/contract/test_constitution_double_landing.py \
      tests/contract/test_instructions_section_propagation.py \
      tests/contract/test_glossary_mechanism.py \
      tests/contract/test_mirror_parity_suite.py \
      tests/contract/test_proactive_trigger_section.py -q --tb=no
FAILED tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged
1 failed, 821 passed in 6.80s
RC=1
$ grep -c 'test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged' baseline-failed.txt
1          # the sole failure is baseline-inherited → comm -13 leaves nothing over

# T052 — every feature guard module, no failure at all
$ python3 -m pytest tests/contract/test_mirror_parity_suite.py \
      tests/contract/test_self_explanatory_constitution.py \
      tests/contract/test_self_explanatory_distribution.py \
      tests/contract/test_self_explanatory_glossary.py -q
798 passed in 9.08s
RC=0

# T050 — clause claims, for the Feature-index entry's 条款认领数
$ python3 scripts/python/account-clause-coverage.py .specify/specs/082-self-explanatory-integration
claimed clauses (this feature): 34
uncovered beyond baseline: 1
status: uncovered
```

## What each row closed

| Row | Obligation | Verdict |
|-----|-----------|---------|
| T048 | mirror total table + `regen` unchanged-surface assertion | **PASS** — six `ok` pairs, exit 0; six `cmp` IDENTICAL; regen `OK:` with `templates/commands/` unmodified (`git diff --stat` empty) |
| T049 | generator `within` + gate total 27 + the 三件套 in the commit message | **PASS** — `within` (33357 < 34816, 1459 B headroom); `total = 27`, unchanged since T002; the 32768 → 34816 / 33357 B / reason triple is in the commit message and `notes/quickstart-run.md` § T049 |
| T050 | Feature index sync | **PASS** — `features/082.md` § Latest Review gains a `2026-11-05 tasks` entry (53 rows, `validate-tasks` PASS 0 error / 32 warnings at authoring time, 34 clause claims); `features.md` 082 status stays **`Planned`** (measured: status column = `Planned`, `git diff --stat .specify/memory/features.md` empty) |
| T051 | red-flag evidence wrap-up, four pairs with command + real output + exit code | **PASS** — `notes/red-first-evidence.md` § T051 re-executes all four green halves in this part; no pair is closed by citation alone |
| T052 | `validate-tasks` exit 0 + GATE-1…GATE-4 recorded | **PASS for gates 1-3**, GATE-4 **deferred** to 10b (`verification.md` does not exist yet; it is created by the wrap-up this part must not run) |
| T053 | C-34 naming-consistency assertions in the glossary module | **PASS** — 14 passed (10 carried + 4 C-34 assertions: STR-001/STR-003 shared portion, document titles, no third form, plus the anti-vacuity companion) |

## Why this part does not run the Completion Gate

`tasks.md` § Completion Gate's GATE-4 judges `verification.md` — a file the implement wrap-up creates.
Running gates 1-3 here and recording them (as T052 asks) is different from *completing* the gate: the
Feature status stays `Planned`, `DoD Status` stays `pending`, no `verification.md` is written, and
GATE-4 is recorded as deferred rather than as passed. The 10b dispatch owns the remaining work.

## Out of scope, verified not done

- **No Completion Gate completion**: gates 1-3 were *executed and recorded* because T052 requires their
  commands and output in `notes/quickstart-run.md`; the gate as a whole is not declared closed, and
  GATE-4 is not run.
- **No Feature status flip**: `.specify/memory/features.md` 082 row unchanged (`Planned`);
  `.specify/memory/features/082.md` `**Status**: Planned` unchanged.
- **No implement wrap-up**: no run-determination / exec-quant / feedback record written by this part.
- **No `verification.md` created.**
- **PLAN-EDIT: none** — `requirements.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`,
  `quickstart.md` and `feature-ref.md` are all unmodified (`git status` shows none of them).
- **Not pushed.**
- The glossary store is untouched by this part: T053's assertions were carried from the part-9
  hand-off, and `test_self_explanatory_glossary.py` is the only test file this part's commit carries
  (its content was authored in the hand-off; this part verified it, ran it, and closed T053).
