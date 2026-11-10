# Spec Repair — 086-efficient-test-execution

**Date**: 2026-11-10
**Tree**: main working tree `/storage/project/cloud-native-ai/spec-kit` (no worktree, no branch switch)
**Spec under repair**: `.specify/specs/086-efficient-test-execution/` — **live**, not archived
(`.specify/archive/specs/086-efficient-test-execution/` does not exist)
**Prior audit**: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-12.md` §
`086-efficient-test-execution` (verdict **BROKEN**) and the deterministic settled scan
`spec-audit-settled.json` → `.specify/specs/086-efficient-test-execution`: `kind: live`, `refs: 215`,
`alive: 190`, `dead: 25`, `dead_list`: 20 distinct paths.

## 1. Method

1. Extracted every path-like token from all 59 files under the spec directory into a scratch scan
   (`.specify/.tmp/repair-086/`), resolved each token against the current tree (file or directory
   existence), and kept the dead set.
2. Classified every dead occurrence with the file role as the primary discriminator (policy below).
3. Fixed only the live normative artifacts; left dated records byte-identical; ignored non-references.
4. Re-ran the scan and the validators over the edited spec.

The audit's `dead_list` grammar is narrower (195 refs for this spec); the re-scan uses a wider token
grammar (1451 refs) and therefore surfaces more dead *occurrences*, including dated-record and
non-reference hits. Both readings are reported so the numbers reconcile.

### Disposition policy

- **live normative pointer** — a place whose purpose is to tell the reader where an owner doc, skill,
  contract, template or store lives **now**: artifact/binding headers, registry tables, plan write-scopes
  and gates, contract MUST statements, data-model locations, checklist bindings, review citations.
  Fixed to the existing live target.
- **dated record citation** — a recorded reading, recorded command, transcript, or scratch path:
  everything under `test-evidence/`, `checkpoints/`, `notes/`, plus `verification.md`,
  `coverage-baseline.txt`, every `.specify/.tmp/**` path, `code-review.md` (a rendered receipt:
  diffstat plus `file.NNN.path=` output), and the verbatim evidence quotes / recorded command lines
  inside `review.md`. Left byte-identical.
- **non-reference** — placeholders (`<name>`, `<type>`, brace-expansion examples), ellipses inside
  transcripts, and prose shorthand that is not a path. Ignored.

## 2. Counts

| Quantity | Occurrences | Distinct tokens |
|---|---|---|
| **Dead total (pre-fix scan)** | **230** | **69** |
| **live-fixed** | **51** | 11 (10 targets; one target appears in both `.specify/…` and leading-slash form) |
| **dated-kept** | **165** | 46 |
| **non-reference** | **14** | 12 |

Post-fix re-scan of the same directory: **179 dead occurrences** = 165 dated-kept + 14 non-reference.
Every remaining dead token is inside a dated record, a transient `.specify/.tmp/` scratch path, or a
non-reference fragment. **No live normative pointer remains dead.**

Reconciliation with the prior audit: its 20 listed dead paths are dispositioned as
live-fixed 5 (`.specify/goal`, `.specify/goal/`, `.specify/skills/external/sdd-loop-driver/`,
`.specify/specs/086-efficient-test-execution/team/`, `scripts/audit-test-budget.py`),
dated-kept 14 (the 13-entry `.specify/.tmp/086/*` family plus the retired spec-local
`goal/086-efficient-test-execution/goal.md`), and non-reference 1 (`docs/serial`).
Its five "anchor-moved" groups — `constitution.md` 24×, `features.md` 13×, `features/086.md` 15×,
`features/085.md` 1×, `register.md` 1× — are all live-fixed where they act as pointers; the residual
occurrences sit in dated records.

## 3. Per-entry disposition

### 3.1 live-fixed (51 occurrences → 10 targets)

| Dead reference | Occ. | Where | After |
|---|---|---|---|
| `.specify/memory/constitution.md` | 16 | plan.md×5, tasks.md×5, requirements.md×2, contracts/principle-landing.contract.md, data-model.md, feature-ref.md, research.md | `.specify/constitution.md` |
| `.specify/memory/features/086.md` | 11 | feature-ref.md×2, plan.md×2, review.md×2, tasks.md×2, checklists/requirements-quality-2026-11-06.md, checklists/requirements.md, contracts/dogfood-and-preservation.contract.md | `.specify/features/086-efficient-test-execution.md` |
| `.specify/memory/features.md` | 9 | tasks.md×3, feature-ref.md×2, plan.md×2, contracts/dogfood-and-preservation.contract.md, requirements.md | `.specify/features.md` |
| `.specify/goal` | 4 | tasks.md×2, contracts/dogfood-and-preservation.contract.md, plan.md | `.specify/anchoring` |
| `.specify/goal/` | 4 | plan.md×2, contracts/dogfood-and-preservation.contract.md, requirements.md | `.specify/anchoring/` |
| `/.specify/memory/features/086.md` (leading-slash form) | 2 | review.md×2 | `/.specify/features/086-efficient-test-execution.md` |
| `.specify/memory/features/085.md` | 1 | plan.md | `.specify/features/085-sdd-temporary-goal-team.md` |
| `.specify/memory/register.md` | 1 | review.md | `.specify/register.md` |
| `.specify/skills/external/sdd-loop-driver/` | 1 | contracts/budget-ledger-parser.contract.md | `.specify/skills/sdd-loop-driver/` |
| `.specify/specs/086-efficient-test-execution/team/` | 1 | data-model.md | `.specify/teams/086-efficient-test-execution/` |
| `scripts/audit-test-budget.py` (wrap continuation of the mirror path) | 1 | contracts/budget-ledger-parser.contract.md | `skills/external/sdd-loop-driver/scripts/audit-test-budget.py` |

Targets verified to exist before editing: `.specify/constitution.md`, `.specify/features.md`,
`.specify/features/086-efficient-test-execution.md`, `.specify/features/085-sdd-temporary-goal-team.md`,
`.specify/register.md`, `.specify/anchoring/086-efficient-test-execution/goal.md`,
`.specify/teams/086-efficient-test-execution/team.md`,
`.specify/skills/sdd-loop-driver/scripts/audit-test-budget.py`,
`skills/external/sdd-loop-driver/scripts/audit-test-budget.py`.

Two non-path edits accompany the fixes: the contract's mirror path was re-joined onto one line
(it had been hard-wrapped between `…sdd-loop-driver/` and `scripts/…`), and comment columns in the
`plan.md` write-scope block plus the `tasks.md` parallel example were re-aligned after the shorter paths.

### 3.2 dated-kept (165 occurrences → 46 tokens)

| Dead reference | Occ. | Where | After / note |
|---|---|---|---|
| `.specify/memory/constitution.md` | 17 | review.md×4, test-evidence/checklist-gates.txt×4, code-review.md×2, test-evidence/downstream-init.txt×2, test-evidence/mutation-legs-runner.txt×2, verification.md×2, test-evidence/mirror-parity.txt | left unchanged (live equivalent `.specify/constitution.md`) |
| `.specify/memory/features.md` | 14 | test-evidence/clarify-gates.txt×3, code-review.md×2, test-evidence/plan-gates.txt×2, checkpoints/01-requirements.md, checkpoints/02-clarify.md, checkpoints/03-plan.md, checkpoints/13-review.md, review.md, test-evidence/completion-gate.txt, verification.md | left unchanged (live equivalent `.specify/features.md`) |
| `.specify/memory/features/086.md` | 14 | test-evidence/clarify-gates.txt×3, code-review.md×2, test-evidence/plan-gates.txt×2, checkpoints/01-requirements.md, checkpoints/02-clarify.md, checkpoints/03-plan.md, checkpoints/13-review.md, review.md, test-evidence/completion-gate.txt, verification.md | left unchanged (live equivalent `.specify/features/086-efficient-test-execution.md`) |
| `.specify/.tmp/086/baseline-failed.txt` | 8 | research.md×5, checkpoints/01-requirements.md, plan.md, test-evidence/plan-gates.txt | left unchanged (transient scratch) |
| `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md` | 8 | checkpoints/01-requirements.md, 02-clarify.md, 03-plan.md, 04-tasks.md, 05-checklist.md, 06-analyze.md, 07-implement-preflight.md, code-review.md | left unchanged (dated; archived copy at `.specify/archive/goal-team/trees/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md`, live goal at `.specify/anchoring/086-efficient-test-execution/goal.md`) |
| `.specify/.tmp/086/s5-auto-names.txt` | 7 | test-evidence/scheduling-experiment.txt×4, quickstart.md×2, test-evidence/full-run-budget.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/s5-lf-names.txt` | 7 | test-evidence/scheduling-experiment.txt×4, quickstart.md×2, test-evidence/full-run-budget.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/us1-parallel.txt` | 7 | test-evidence/parallel-safety.txt×4, tasks.md, test-evidence/full-run-budget.md, test-evidence/parallel-safety-attribution.md | left unchanged (transient scratch) |
| `.specify/goal` | 7 | test-evidence/completion-gate.txt×3, test-evidence/preservation-085.txt×2, test-evidence/plan-gates.txt, verification.md | left unchanged (live store `.specify/anchoring/`) |
| `skills/contracts/skill-format.md` | 7 | coverage-baseline.txt×7 | left unchanged; token is a fragment of the captured baseline entry `017-consolidate-draft-skills/contracts/skill-format.md#C-00n` (archived at `.specify/archive/specs/017-consolidate-draft-skills/contracts/skill-format.md`) |
| `.specify/.tmp/086/` | 6 | tasks.md×4, research.md, review.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/gate-scan-baseline.json` | 5 | tasks.md×2, plan.md, research.md, test-evidence/plan-gates.txt | left unchanged (transient scratch) |
| `.specify/.tmp/086/mutations/sandbox/` | 5 | test-evidence/closure-diff.txt×2, test-evidence/full-run-budget.md, test-evidence/parallel-safety-attribution.md, test-evidence/serial-exceptions.txt | left unchanged (transient scratch) |
| `.specify/.tmp/086/parallel-failed.txt` | 4 | research.md×3, checkpoints/01-requirements.md | left unchanged (transient scratch) |
| `.specify/skills/external/sdd-loop-driver/scripts/audit-test-budget.py` | 4 | test-evidence/tasks-gates.txt×2, test-evidence/plan-gates.txt, test-evidence/repair-gates.txt | left unchanged (recorded gate output; live mirror `.specify/skills/sdd-loop-driver/scripts/audit-test-budget.py`) |
| `.specify/.tmp/086/baseline.log` | 3 | test-evidence/baseline.txt×2, checkpoints/01-requirements.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/s8-parallel.txt` | 3 | quickstart.md×3 | left unchanged (transient scratch) |
| `.specify/.tmp/086/s8-serial.txt` | 3 | quickstart.md×3 | left unchanged (transient scratch) |
| `.specify/goal/` | 3 | test-evidence/baseline.txt×2, test-evidence/preservation-085.txt | left unchanged (live store `.specify/anchoring/`) |
| `.specify/.tmp/086/analyze-coverage.json` | 2 | checkpoints/06-analyze.md, test-evidence/analyze-findings.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/parallel.log` | 2 | checkpoints/01-requirements.md, test-evidence/baseline.txt | left unchanged (transient scratch) |
| `.specify/project/goal/` | 2 | test-evidence/baseline.txt×2 | left unchanged (captured assertion text) |
| `.specify/specs/086-efficient-test-execution/team/086-efficient-test-execution/team.md` | 2 | checkpoints/03-plan.md, code-review.md | left unchanged (dated; live team at `.specify/teams/086-efficient-test-execution/team.md`) |
| `/scripts/audit-test-budget.py` | 2 | code-review.md×2 | left unchanged (truncated diffstat fragment) |
| `skills/external/humanize/SKILL.md` | 2 | test-evidence/baseline.txt×2 | left unchanged (captured assertion listing; skill is now `humanize-conclusion`) |
| `.specify/.tmp/086/c1-preservation-085.txt` | 1 | test-evidence/dogfood-record.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/isolation-probe.txt` | 1 | tasks.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/s1-names.txt` | 1 | quickstart.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/s2-names.txt` | 1 | quickstart.md | left unchanged (transient scratch) |
| `.specify/.tmp/086/s4-names.txt` | 1 | quickstart.md | left unchanged (transient scratch) |
| `.specify/.tmp/hk-20261105T130452Z/sanitize.json` | 1 | test-evidence/baseline.txt | left unchanged (transient scratch) |
| `.specify/.tmp/hk-sanitize-apply.json` | 1 | test-evidence/baseline.txt | left unchanged (transient scratch) |
| `.specify/.tmp/test-parallel-eval/full-parallel.log` | 1 | test-evidence/baseline.txt | left unchanged (transient scratch) |
| `.specify/.tmp/test-parallel-eval/full-serial.log` | 1 | test-evidence/baseline.txt | left unchanged (transient scratch) |
| `.specify/goal/086-efficient-test-execution/` | 1 | checkpoints/01-requirements.md | left unchanged (dated checkpoint prose) |
| `.specify/specs/067-loop-efficiency-hardening/test-evidence/closure-failures.txt` | 1 | test-evidence/budget-ledger.txt | left unchanged (recorded command in a dated ledger) |
| `.specify/specs/086-efficient-test-execution/checkpoints/01` | 1 | test-evidence/dogfood-record.md | left unchanged (prose ellipsis `checkpoints/01-…-10-…md`) |
| `.specify/specs/086-efficient-test-execution/checkpoints/04` | 1 | test-evidence/parallel-safety-attribution.md | left unchanged (prose ellipsis `checkpoints/04-…`) |
| `/.specify/memory/evidence/ev-20261106-052108-project` | 1 | test-evidence/baseline.txt | left unchanged (captured pytest temp-dir output) |
| `/.specify/memory/features/086.md` (leading-slash form) | 1 | test-evidence/completion-gate.txt | left unchanged (captured JSON `claimed_status_source`, host temp worktree) |
| `/feedback/20261106T041131Z-speckit-clarify.md` | 1 | code-review.md | left unchanged (truncated diffstat path) |
| `/feedback/20261106T042143Z-speckit-plan.md` | 1 | code-review.md | left unchanged (truncated diffstat path) |
| `/feedback/20261106T042146Z-skill-create-plan.md` | 1 | code-review.md | left unchanged (truncated diffstat path) |
| `skills/external/humanize/references/report-shape.md` | 1 | test-evidence/baseline.txt | left unchanged (captured assertion listing) |
| `skills/external/humanize/references/run-mode.md` | 1 | test-evidence/baseline.txt | left unchanged (captured assertion listing) |
| `skills/external/sdd-loop-driver/contracts/test-budget.md` | 1 | test-evidence/plan-gates.txt | left unchanged (recorded gate reading; live owner `.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md`) |

`review.md` occurrences intentionally kept as dated readings: line 176 (the recorded
`closure-acceptance-check.py` command that produced the copied `final_path` record), line 230
(task-replay prose), and lines 199 / 377 / 381 (verbatim quotes of `test-evidence/downstream-init.txt`
and its dated analysis).

`code-review.md` is a rendered review receipt (`renderer=text`, `file.NNN.path=…`); its 13 dead tokens
are captured diffstat and `file.NNN.path=` output, so none was rewritten.

### 3.3 non-reference (14 occurrences → 12 tokens)

| Dead reference | Occ. | Where | Note |
|---|---|---|---|
| `.specify/.tmp/086/{baseline` | 2 | checkpoints/02-clarify.md×2 | brace-expansion example (`.specify/.tmp/086/{baseline,parallel}.log`) |
| `.specify/shared/<type>/` | 2 | test-evidence/baseline.txt×2 | `<type>` placeholder |
| `.specify/.../final-failed.txt` | 1 | test-evidence/closure-diff.txt | ellipsis in a transcript |
| `.specify/.t...l-serial.log` | 1 | test-evidence/baseline.txt | ellipsis in a transcript |
| `.specify/shared/guidelines/<name>.md` | 1 | test-evidence/baseline.txt | `<name>` placeholder |
| `.specify/skills/<name>/` | 1 | test-evidence/baseline.txt | `<name>` placeholder |
| `/docs/closure` | 1 | checkpoints/09-implement-wave2.md | prose shorthand ("registry/docs/closure") |
| `/tests/085` | 1 | checkpoints/07-implement-preflight.md | prose shorthand ("no source/tests/085 path touched") |
| `docs/serial` | 1 | checkpoints/08-implement-wave1.md | prose shorthand ("docs/serial marker") |
| `feedback/exec-quant` | 1 | checkpoints/04-tasks.md | prose ("feedback/exec-quant records") |
| `shared/<type>/` | 1 | test-evidence/baseline.txt | `<type>` placeholder |
| `skills/external/create-docs/SKIL...external/coaching-skills/SKILL.md` | 1 | test-evidence/baseline.txt | two assertion fragments concatenated |

## 4. Files changed (12, all inside the spec directory)

`checklists/requirements.md`, `checklists/requirements-quality-2026-11-06.md`,
`contracts/budget-ledger-parser.contract.md`, `contracts/dogfood-and-preservation.contract.md`,
`contracts/principle-landing.contract.md`, `data-model.md`, `feature-ref.md`, `plan.md`,
`requirements.md`, `research.md`, `review.md`, `tasks.md`.

No dated record file was modified: `test-evidence/**`, `checkpoints/**`, `notes/**`, `verification.md`,
`coverage-baseline.txt` and `code-review.md` are byte-identical.

**Registry row**: no change needed — `.specify/features.md` row `086` already uses the current layout
(`Feature Details .specify/features/086-efficient-test-execution.md`, `Spec Path
.specify/specs/086-efficient-test-execution/requirements.md`) and the detail file exists.

## 5. Validator readings

| Validator | Command | Reading |
|---|---|---|
| `validate-requirements.py` | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/086-efficient-test-execution/requirements.md` | `status: ok`; `id-contiguous`, `doc-order`, `ref-resolvable`, `marker-count`, `dup-id`, `path-marker` all **pass**; 335 lines, 45 definition rows, 7 shared strings; **0 error(s), 0 warning(s)**; exit 0 |
| `validate-tasks.py` | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/086-efficient-test-execution/tasks.md` | **PASS**; 0 error(s), 0 warning(s); 52 green claims; exit 0 |
| `validate-decision-tensions.py` | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/086-efficient-test-execution` | 339 lines, 3 record(s), channel `value_domain=HIGH-or-0, high=0`; **0 error(s), 0 warning(s)**; exit 0 |

The two required validators (`validate-requirements.py`, `validate-tasks.py`) and the plan's own
decision-tension validator all read clean after the repair. No file in this spec declares another
path-resolving validator.

## 6. Anomaly

ANOMALY: none in this repair — the 12-file change set is confined to the spec directory and no dated
record was rewritten; the shared main tree concurrently carries unrelated modified files from other
repair runs (observed only, never touched).

SPEC-REPAIR-086-DONE
