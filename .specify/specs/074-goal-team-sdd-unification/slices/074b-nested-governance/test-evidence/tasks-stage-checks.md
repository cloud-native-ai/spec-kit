# Tasks-stage deterministic checks — 074b-nested-governance

**Stage**: `/speckit.tasks` · **Slice**: `074b-nested-governance` · **Feature**: 074
**Stage base**: `ce9de5983` (plan DONE) · **Captured**: 2026-10-29
**Single-run evidence discipline**: every command below was executed once in this stage. Command
lines and their decisive output are pasted here; the one expensive run (the 19-suite targeted set)
keeps its **complete** stdout in the sanctioned ignored temp root —
`.specify/.tmp/074b-tasks-targeted.log`, with its failed-name list at
`.specify/.tmp/074b-tasks-failed.txt` — both retained rather than discarded, so no follow-up
question needs a re-run. The temp root is the one `.specify/.gitignore:30` already matches.

---

## 1. Structural validator — `validate-tasks.py`

```text
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/074b-nested-governance/tasks.md
PASS: .specify/specs/074b-nested-governance/tasks.md — 0 error(s), 0 warning(s)
exit=0
```

Adjudicated WARN: none emitted. The four green-attribution checks (`green-dangling`,
`green-cross-phase`, `green-clause-collision`, `green-path-divergence`) all report clean, so the
30 clauses are each claimed exactly once, in ascending order per contract, with no test path
carrying two different green points.

## 2. Decomposition gate — `decomposition-check.py --mode tasks`

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074b-nested-governance/requirements.md \
    --tasks .specify/specs/074b-nested-governance/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 8, "task_count": 26,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T04:51:28Z"}
exit=0
```

Row count re-derived independently:
`grep -cE '^- \[[ xX>~]\] T[0-9]+' tasks.md` → **26** (ceiling 40; 14 rows of headroom).

## 3. Clause coverage — freeze, then account

### 3a. Freeze (after the 30 `[green:]` claims landed in `tasks.md`)

```text
$ python3 .specify/scripts/python/account-clause-coverage.py \
    --spec-dir .specify/specs/074b-nested-governance --freeze \
    > .specify/specs/074b-nested-governance/coverage-baseline.txt
exit=0
```

Baseline header (verbatim):

```text
# frozen-from: .specify/specs/*/contracts/* excluding 074b-nested-governance | owner-forms: md-bold-closed,md-bold-paren,md-heading,yaml-openapi,yaml-assertions,md-none (md-none named, never silently covered) | clause-rules: shared/definitions/contract-clause-definitions.md | per-form counts: notes/clause-form-census.md | base-sha: ce9de598356a | files: 212 (parsed 118 + named 94)
```

Self-exemption audit (the baseline must not hold this slice's own clause names):

```text
$ grep -c '^074b-nested-governance/' .specify/specs/074b-nested-governance/coverage-baseline.txt
0
$ grep -c '074b-nested-governance/contracts' .specify/specs/074b-nested-governance/coverage-baseline.txt
0
```

Baseline holds 495 pre-existing uncovered names from other specs (`wc -l` = 497 with two header
lines). This slice's 30 clauses can therefore only be covered by a task row, never by its own
frozen baseline.

### 3b. Account (post-freeze)

```text
$ python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance
claimed clauses (this feature): 30
baseline: .specify/specs/074b-nested-governance/coverage-baseline.txt (495 names)
uncovered beyond baseline: 0
FR universe: 8
FR claimed: 8
FR uncovered: 0
companion (must be non-empty on a green run): claimed clauses 30, scanned files 215, clause universe 1315, FR universe 8
status: ok
exit=0
```

Pre-freeze state, recorded for the delta (plan stage left it `baseline-missing`, as designed):
`claimed clauses (this feature): 0`; `baseline: …/coverage-baseline.txt (0 names, MISSING)`;
`FR claimed: 8 / uncovered: 0`; `status: baseline-missing`; exit 2.

Clause census re-derived from disk (not from the plan's prose):

```text
$ grep -cE '^\*\*C-[0-9]+\*\*' .specify/specs/074b-nested-governance/contracts/*.md
contracts/compat-and-safety.md:12
contracts/diffusion.md:8
contracts/report-and-attribution.md:10
$ grep -ohE '^\*\*C-[0-9]+\*\*' …/contracts/*.md | wc -l
30     # ids contiguous C-1…C-30
```

## 4. Cross-artifact gate — `pre-analyze-check.py --stage tasks`

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074b-nested-governance --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=21 waived=0
exit=0
```

**Adjudication of all 21 advisories**: every one is `missing-path` and every one names one of the
three contract-test files this slice's *implementation* stage authors —
`tests/contract/test_nested_run_report.py` (7 hits: `plan.md:301`, `tasks.md:19`, `tasks.md:134`,
`quickstart.md:48`, `quickstart.md:110`, `research.md:251`, `feature-ref.md:44`,
`contracts/report-and-attribution.md:10`), `tests/contract/test_sdd_diffusion.py` (`tasks.md:19`,
`tasks.md:149`, `tasks.md:151`, `quickstart.md:120`, `research.md:252`, `feature-ref.md:45`,
`contracts/diffusion.md:10`) and `tests/contract/test_sdd_compat_containment.py` (`tasks.md:19`,
`tasks.md:171`, `tasks.md:210`, `research.md:253`, `feature-ref.md:46`,
`contracts/compat-and-safety.md:11`). Each is a *planned* path whose authoring row exists (T004,
T010, T019), so none is a phantom reference; the advisory is the expected shape at this stage and
will clear when those rows run. Zero waived — the count is adjudicated, not silenced.

Note on the JSON summary's `"clauses": 0`: pre-analyze counts clause *citations in the analysed
docs' citation groups*, not `[green:]` claims; the claim count is the accountant's number in § 3b
(30), and the two are different metrics, not a disagreement.

## 5. Test budget — targeted-set-v1 (`stage_base=tasks`), one run, no second full suite

**E3 stage-status row (six run fields)** —

| Field | Value |
|-------|-------|
| `command` | `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/074b-tasks-failed.txt <the 19 suites recorded in test-evidence/targeted-set-v1-baseline.txt>` |
| `exit_status` | `1` (one pre-existing failure; see below) |
| `counts` | `collected 290 items` → **1 failed, 289 passed** |
| `duration` | pytest `34.15s`; wall-clock `34,965 ms` |
| `failed_name_set` | `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` (1 entry) |
| `baseline_ptr` | `.specify/specs/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt` (`stage_base=33269994a`) |

Name-level comparison against the frozen baseline (identity, not counts):

```text
$ diff <(grep -E '^tests/[^ ]*::' test-evidence/targeted-set-v1-baseline.txt | sort) \
       <(sort .specify/.tmp/074b-tasks-failed.txt)
IDENTICAL name set
new failures (comm -13):        <empty>
disappeared (comm -23):         <empty>
```

The single red is the pre-existing `test_c11_gate_scan_total_unchanged` (gate total `27` vs the
frozen `23`, four gates predating this slice). It is recorded, not repaired, and no green claim is
made over it. This stage changed no executable surface (markdown and evidence files only), so the
identical result is the expected outcome; no second suite was run.

**Full-suite row**: `status=not-run-docs-only` — this stage added `tasks.md`, `coverage-baseline.txt`
and this evidence file, and touched no owner, engine, or test file. The full suite has no new
subject; its two slots belong to the implement and review stages.

## 6. Baseline surfaces re-measured at generation time (no drift)

```text
$ python3 scripts/python/sync-mirrors.py --check
exit=0 · ok templates/ 22 · skills/external/ 406 · skills/internal/ 136 · agents/ 3 · scripts/ 114 · shared/ 59

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.   exit=0

$ python3 .specify/scripts/python/flow-class-check.py --action check
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
```

## 7. Premises measured before any row cites them

| Premise | Command | Measured |
|---------|---------|----------|
| FR / SC / STR in `requirements.md` | `grep -cE '^\- \*\*FR-[0-9]+\*\*:'` / `SC-` / `^\| \`STR-[0-9]+\`'` | 8 / 2 / 7 |
| Contract clauses | `grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md` | 12 / 8 / 10 = **30** |
| Three new test files | `test -e` each | 3/3 absent (red-first precondition) |
| Edit targets + reused fixture + leaf preset | `test -e` each | 8/8 present |
| Leaf preset declaration count | `grep -c 'sdd-invocation' agents/sdd-executor.agent.md` | `0` (trap: a repo-wide grep hits design-doc prose; the unit is the shipped preset) |
| Report-contract owner site | `grep -n '### Report contract' skills/internal/create-team/SKILL.md` | `:53` (skeleton block `:57-63`) |
| `run-team` delegation | `grep -n 'target_ref' skills/internal/run-team/SKILL.md` | `:66` — keeps delegating, already carries `"target_ref": "T-<nnn>"` |
| Stage bullet site | `grep -n 'executor.*evaluator.*optimizer' …/conceptual-model.md` | `:10` |
| Authoring-baseline site | `grep -n '^## Authoring Baseline' skills/internal/run-agent/SKILL.md` | `:171` |
| Trigger discipline section set | `grep -c '^## ' shared/guidelines/proactive-trigger.md` | 10 `## ` sections; `## Promotion & Safety Boundary` at `:68` |
| Instructions pointer face | `grep -c 'sdd-routing\|sdd-invocation\|Nested SDD' templates/instructions-template.md` | `0` (new, not a rewrite) |
| Instructions byte sizes | `wc -c templates/instructions-template.md .specify/instructions.md` | 34,666 / 41,948 (both already over the 32,768 B budget → ceiling + measured delta is the criterion) |
| Ledger attribution field | `grep -n 'target_ref' …/summary-mapping.md` | `:100` (`target_ref`, `T-\d{3}`, absent = goal-wide form) |
| Containment carrier | `awk` per `## S<n>` over `^tests/` lines | 266 cases / 17 files / 7 sets (49/25/24/40/36/54/38) @ `33269994a` |
| Task rows | `grep -cE '^- \[[ xX>~]\] T[0-9]+' tasks.md` | 26 |

## 8. Clause → row partition (the claims this stage froze)

| Contract | Clauses | Rows |
|----------|---------|------|
| `contracts/report-and-attribution.md` | C-21…C-23 / C-24…C-26 / C-27…C-29 / C-30 | T005 / T006 / T007 / T008 |
| `contracts/diffusion.md` | C-13…C-14 / C-15…C-17 / C-18 / C-19 / C-20 | T011 / T012 / T013 / T014 / T015 |
| `contracts/compat-and-safety.md` | C-1…C-2 / C-3…C-6 / C-7…C-12 | T017 / T018 / T019 |

Each clause is claimed exactly once and each file's ordinals ascend with row order — the validator's
four green checks agree (§ 1), and the accountant's `claimed clauses = 30` (§ 3b) is the same fact
measured from the other side.

## 9. PLAN-EDIT declarations

None. This stage wrote `tasks.md`, `coverage-baseline.txt` and this evidence file only; no
plan-owned artifact (`plan.md`, `data-model.md`, `contracts/**`, `quickstart.md`, `research.md`,
`feature-ref.md`) was edited, so `plan_constraint` (active since 2026-10-29T04:47Z at
`plan_commit=ce9de5983`) was never engaged.

## 10. Deletion-surface audit

`git status --short` over this stage's write set shows three added paths and zero deletions:

```text
A  .specify/specs/074b-nested-governance/tasks.md
A  .specify/specs/074b-nested-governance/coverage-baseline.txt
A  .specify/specs/074b-nested-governance/test-evidence/tasks-stage-checks.md
```

No file was removed, renamed, or emptied; the parent spec and the `074a` slice show zero diff.
