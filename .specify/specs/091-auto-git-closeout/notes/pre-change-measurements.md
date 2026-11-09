# Pre-change measurements — feature 091 (implement entry, 2026-11-09)

Every reading below was taken **before** this feature wrote any of the five surfaces it
edits. They are the baseline object that T014 (no restated model fact), T060/T047
(confirmation-gate closed-set comparison) and T062/T054 (instructions pointer measurement)
compare against.

## T003 — the three modules `plan.md` EP-003 names, and the gate scan

    /usr/bin/python3 -m pytest tests/contract/test_git_workflow_instructions_block.py \
        tests/contract/test_wrap_up_wording_gate_safe.py tests/contract/test_mirror_parity_suite.py -q
    -> 835 passed in 1.21s   (exit 0)

That is the re-measured value; `tasks.md` § Premises records `835 passed` from generation
time and the number reproduces exactly.

    python3 scripts/python/scan-confirmation-gates.py
    -> blocking confirmation gates: 27
         destructive: 20
         governance_kept: 7
       violations (reversible gates still blocking): 0
       (exit 0)

**This scan is SC-004's baseline object.** The comparison unit is the **gate name set**, not
the total: `scan-confirmation-gates.py` prints a total and two class subtotals and does not
print names, so the name-level reading is taken by the guard from the live scan of the
pre-change tree recorded here (27 blocking gates: 20 destructive + 7 governance-kept), and
the pre-existing pin `tests/contract/test_wrap_up_wording_gate_safe.py::test_confirmation_gate_budget_unchanged`
asserting `== 27` stays untouched (`plan.md` finding F-2).

## T004 — the five surfaces this feature edits, before any edit

Recorded so "this feature's addition" is decidable against a snapshot, per
`closeout-declaration.contract.md` C-2's companion assertion.

### 1. `skills/external/git-utils/assets/git-workflow-block.md` (the shipped block template)

- Managed block rows before: **1** (`Workflow model: <MODEL>`), plus the bracketed guidance
  comment above it and the `**Last updated**: <DATE>` row.
- Markers `<!-- GIT_WORKFLOW_START -->` / `<!-- GIT_WORKFLOW_END -->` present and paired.
- Occurrences of `Closeout` / `closeout`: **0**.
- The file-level comment block above the title documents the four-model menu in prose
  (single-branch / dual-branch / temp-branch / MAIN-PRE-DEV three-tier) — that comment is
  pre-existing and is **not** a table inside the managed block.
- `git ls-files` state: tracked, clean at `abe26a2c`.

### 2. `.specify/workflow/git.md` (this project's instance — the one client-side file)

- Managed block rows before: 6 —
  `Workflow model`, `Trunk`, `Feature branch convention`, `.gitexcludes`,
  `⚠ NOT a sync peer`, `⚠ Remote roles`, plus `Last updated`.
- Declared model: 临时分支（trunk-based）, trunk `master`.
- Remotes: `origin` (read-only upstream, MUST NOT push), `github` / `gitlab` / `gitee`
  (three mirrors of the same fork).
- Occurrences of the word `closeout` (no hyphen): **0**. The hyphenated prose `close-out`
  appears 2× pre-existing in this file and in the block asset — which confirms research R2:
  the **name** does not exist yet.

#### Managed-block row snapshot (read by T014's guard)

The row sets below are the pre-change state T014 compares against, written as a list so the
guard reads them mechanically instead of re-parsing prose. Labels are lower-cased.

### block-asset

- **workflow model**
- **last updated**

### state-file

- **workflow model**
- **trunk**
- **feature branch convention**
- **`.gitexcludes`**
- **⚠ not a sync peer**
- **⚠ remote roles**
- **last updated**

### 3. `skills/external/git-utils/SKILL.md`

- `grep -rc closeout skills/external/git-utils/SKILL.md` -> **0**.
- Scope-A operation set before this feature: operations A–G (three-tier A/B/C, D rebase,
  E custom, F `.gitexcludes`, G verify). No `closeout` operation.
- Scope-A entry-mode table before: three rows (block filled? × operation argument?) —
  Bootstrap / 全维度体检 / 定向收敛.
- § Resources `References` list before: 6 scope-A rows + 5 fleet + 2 submodule + 4 server.

### 4. `shared/workflow/artifact-commit-step.md` § Boundaries

- 3 bullets: "Not a status transition.", "**Not a substitute for pushing.** This step
  commits locally. Pushing is a shared-state action governed by the framework-level git
  workflow state file (`.specify/workflow/git.md`) and requires its own authorization.",
  "**Read-only commands** that produce no artifact … skip this step and say so in one line,
  rather than creating an empty commit."
- The sentence this feature revises in place is the second bullet's first clause:
  **"This step commits locally."** combined with its subject line
  **"Not a substitute for pushing."** The guard locates it by the assertion (the bullet whose
  subject is that the step does not push), never by line number
  (`closeout-lifecycle.contract.md` C-7).
- The file has 3 H2 sections: `## The step`, `## Boundaries`, `## Why a shared owner rather
  than five copies`. A new close-out section does not exist.

### 5. The probe handler table — `shared/definitions/probe-definitions.md` § Handler

- `wrap-up` lifecycle-point handler orders in use: **10, 15, 20, 30, 40, 50**
  (`h-run-determination`, `h-exec-quant`, `h-feedback-record`, `h-threshold-notice`,
  `h-token-reflection`, `h-docs-sync-eval`).
- Next free order: **60** — re-measured here rather than inherited from A-G2's generation-time
  note. Re-derivation command:
  `sed -n '/^## Handler/,/^## HandlerBinding/p' shared/definitions/probe-definitions.md`
- Handler rows before: 9 (6 wrap-up + 2 situation/phase-boundary + 1 gate).
- No `close-out` / `closeout` row exists.

## The instructions surface (feeds T054 / T062)

- `templates/instructions-template.md` § `## Git Workflow` before: one paragraph (the pointer
  section). It names the unattended mechanisms as "SDD driver, house-keeping, feedback digest,
  **close-out**" and points at `.specify/workflow/git.md` as the single source of truth for
  every git operation, with "Procedure: the skill and its references."
- `.specify/instructions.md` § `## Git Workflow`: byte-identical paragraph (this repo's
  projection of the same template section).
- Measured conclusion for T054: a reader starting from that section already reaches the
  close-out through two names — the mechanism list names "close-out", and the pointer chain
  (`.specify/workflow/git.md` → the `git-utils` skill → its references) reaches the step.
  What is **not** reachable yet is the new reference file itself; T054 decides whether that
  gap is a pointer line or a "no edit" by measurement, and T062 asserts the reading.
