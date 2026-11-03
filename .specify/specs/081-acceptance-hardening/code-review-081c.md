# Code Review — Feature 081, slice 081c

**Range**: `c46da4d2..e5afed1f` — 7 commits, 67 changed files, 4 748 changed lines
**Renderer**: `renderer: text` (no interactive terminal; no `delta` rendering is claimed, and none of
the four forbidden phrases appears in this record)
**Triage**: `run` — `git-delta-review.sh triage` on this tree reports
`base=c46da4d2 head=e5afed1f changed_files=67 triage=run basis=code path in the committed delta`
**Base source**: `explicit` (the dispatched range). Disclosure: `git-delta-review.sh base --spec
.specify/specs/081-acceptance-hardening` independently resolves `base=cb841d90`,
`base_source=feature-first-commit` — the **feature's** first commit, not this slice's. The command
passes a caller's explicit values through and invents no default, so the explicit pair governs; both
readings are recorded rather than silently reconciled.
**Scope**: `templates/commands/{review,checklist}.md`, `templates/review-template.md`,
`shared/workflow/acceptance-hardening.md`, `shared/definitions/{flow-class,probe}-definitions.md`,
`skills/internal/{review-feature-quality/**,review-sdd-process,code-review}/`,
`docs/reference/commands/review.md`, `tests/contract/{test_acceptance_review_composition,
test_review_code_composition,test_review_feedback_boundary,test_client_guard_sweep,
test_review_docs_isomorphism,test_gate_wiring_081,test_skill_layer_visibility_guards,
test_expression_compatibility,test_migration_distribution}.py`,
`tests/fixtures/acceptance-hardening/{review-implemented-clean,review-implemented-blocked,
expected-artifact-missing}/`, the generated mirrors and the four per-tool command copies, and the
slice's own `.specify/specs/081-acceptance-hardening/` artifacts.
**Excluded**: the analyze/checklist records dated before `c46da4d2` (spec-freeze inputs, judged by the
process and artifact segments, not here); `.venv/` copies.

## Findings

### important

1. **The `P0`/`P1`/`P2` meanings are defined a second time, with different content** —
   `skills/internal/review-feature-quality/references/artifact-and-implementation-review.md:81-87`
   (§ A.4 "Severity assignment") assigns a meaning to each of the three tokens. The two owner
   statements this slice also landed say that is not allowed:
   `skills/internal/review-feature-quality/SKILL.md:52-53` — "the meanings are written once, in the
   report template's severity table, and are not repeated here" — and
   `skills/internal/review-sdd-process/SKILL.md:50-51` — "not a second copy of those meanings". The
   second set is not a paraphrase: `templates/review-template.md:58` defines `P0` as "Blocks correct
   use of spec-kit, or creates silent corruption risk. Fix before next spec." while § A.4 defines it as
   "a reader acting on the artifacts would be misled, or the slice's acceptance claim is false";
   `P1` is "Recurring friction across specs" against "a defect every later slice pays for". A finding
   can be `P0` under one and `P2` under the other, so the severity counts in a report become a function
   of which file the grader opened. § A.4's own `P1` definition — "the same fact stated twice" — is
   satisfied by § A.4 itself.
2. **Slots `### 2.2` and `### 2.3` forbid the content they mandate** —
   `templates/review-template.md:92` (and `:115`): "this slot carries no opinion body and no per-item
   count", followed at `:105-107` (and `:131-133`) by a findings table templated one row per finding
   whose last cell is glossed at `:281` as "One sentence naming the defect and the section that would
   fix it". The two instructions cannot both be obeyed; obeying the preamble removes the only place
   the artifact and implementation findings live, which SC-006 requires a produced `review.md` to
   carry with severity, path and line. `### 2.1`'s identical preamble is coherent because that slot
   has no findings table and points at this record; the middle two copied the sentence and then added
   the table. It was ordered that way: `tasks.md:124` (T006) asked for both in one row.
3. **`### 2.1` mandates coverage-receipt counts that nothing requires the run to produce** —
   `templates/review-template.md:80` requires `[CHANGED_COUNT] / [JUDGED_COUNT] / [SKIPPED_COUNT] /
   [GAP_COUNT]` "copied field by field from the coverage receipt block; never recomputed,
   re-aggregated, or read off the record's prose". The `code-review` skill has the step
   (`skills/internal/code-review/scripts/git-delta-review.sh receipt`, step 4 of its non-interactive
   path), but `/speckit.review` § Composition never invokes it, and this feature's two archived records
   carry no receipt block (measured: `grep` for a receipt in `code-review-081a.md` /
   `code-review-081b.md` finds nothing; the most recent record that has one is
   `.specify/specs/071-review-code-integration/code-review.md`). The first composed run therefore
   cannot fill the field from the record it describes — it must either fabricate four integers or
   disclose a hand count, and the field's own wording forbids the second. This run discloses.

### suggestion

4. **The command's registration face still describes a two-segment review** —
   `templates/commands/review.md:2-3`: `description: Critically review the SDD process for the current
   feature and produce a self-contained, improvement-focused report…` and
   `short-description: 批判性评审当前特性的 SDD 过程，出具改进导向报告`. That is the text an agent CLI
   shows when a user picks the command; the command now also judges the artifact set and the
   implementation delta, runs ARC and writes a second artifact. The slice treated the equivalent text
   as in scope elsewhere — `docs/reference/commands/review.md:3` was rewritten to the four-segment
   wording, and the process skill's `description` was reworded for the same reason — and
   `templates/commands/review.md:139` declares only `scripts:`, `## Wrap-up` and `## Handoffs`
   unchanged, so this face was neither frozen nor updated.
5. **The docs page asserts it restates nothing and restates the owner on the next line** —
   `docs/reference/commands/review.md:33`: "this page states the surface and restates none of that
   content", then `:42`: the artifact segment's judgment object as "completeness, internal consistency,
   traceability, dependency and premise ownership, acceptance honesty" — the same five nouns, in the
   same order, as `shared/workflow/acceptance-hardening.md:493-495`'s boundary sentence, one parenthetical
   dropped. The owner forbids it at `shared/workflow/acceptance-hardening.md:463` and names the docs
   page among the surfaces that must reach it "by path plus `§ Review Composition`". The guard
   (`tests/contract/test_review_docs_isomorphism.py`) only requires the four segment *concepts*, so the
   column can become a pointer without a red test.
6. **`[ARC_VERDICT]` is a four-way hole squeezed into a binary field** —
   `templates/review-template.md:149` offers `agree | refused`, glossed at `:288` as "`agree` when the
   claimed status survives the copied record, `refused` when it does not", while
   `templates/commands/review.md:95` states that a `block` verdict "refuses the transition on its own,
   whatever the claim reads". For a feature claimed `Blocked` (the normal state of a feature mid-slice)
   the two rules point in opposite directions and no sentence maps `accept`/`block` onto
   `agree`/`refused`. Every review of a blocked feature meets this case; this one did.

### praise

- `test_the_judges_reject_near_misses_so_no_leg_is_a_bare_string_test`
  (`tests/contract/test_acceptance_review_composition.py:1187`) proves each of the three custom
  judges can reject a near miss — `"\`line\` (optional)"` is caught while `"never optional"` is not, a
  three-count summary fails the seven-key record test, and `blocking-unresolved` is not read as
  `blocking`. Guarding the guards is the difference between a leg that can go red and one that cannot.
- `test_d5_the_competing_reading_reads_full_coverage_on_the_same_fixture` computes the losing
  denominator on the same fixture and asserts the two readings *differ*. A leg that only asserted
  `6 / 7` could pass over a fixture where both readings agree; this one cannot.
- `test_f3_the_refusal_fires_on_the_blocked_case_and_cannot_fire_on_negative` proves the conjunction in
  both directions — it fires on `review-implemented-blocked` and is asserted **absent** for `negative`
  (`claimed_status: Planned`). That is what makes T015/T016 necessary rather than decorative.
- `test_b2_the_segment_skill_paths_and_their_anchors_resolve_on_disk` resolves every `Skill` runtime
  path to a file and every `§ Segment A/B` pointer to a heading, with the source path as a fallback and
  both paths named in the failure message — a pointer that does not resolve is the defect, not a
  typo to be discovered later.
- The four guard re-pins each carry, in the module's own docstring, what the assertion used to read,
  why it moved, and what would still be red had it not; none was deleted, and the pins remain verbatim
  (`test_client_guard_sweep.py:367`, `test_review_feedback_boundary.py:108` and `:139`,
  `test_expression_compatibility.py:144`, `test_migration_distribution.py:98` and `:119`).

### nitpick

- `_sweep()` in `test_acceptance_review_composition.py:307` re-walks and re-reads every markdown
  file under four roots once per fragment (three fragments in `test_c1`, one in `test_d2`), and
  `_md_files`'s `.venv` exclusion is dead code because none of the four roots contains a `.venv`. A
  module-level cache would cut the walk by ~4×; the whole eleven-module close set runs in 21.9 s today,
  so this is tidiness, not cost.
- `_closed_reason_prefixes()` (`:995-996`) parses `requirements.md`'s `## Shared Strings` table with a
  local regex while the module docstring says it "re-implements no parser". The regex is two lines and
  reads its owner rather than copying it, so the claim is directionally right — but it is a parser.

### question

- Three separate modules now assert the same four-unit census surface with three different mechanisms
  (`test_acceptance_review_composition.py` leg (h) on the command's feedback-boundary section,
  `test_client_guard_sweep.py` on a verbatim sentence in the code skill,
  `test_review_feedback_boundary.py` on the unit ids plus the real feedback engine). RC-19 named two
  pins; the third is new. Is the intended owner "one pin per carrier" (which is what exists) or "one
  pin, cited from the carriers"? Nothing states it, and the next carrier will have to guess whether it
  owes a fourth.

## Coverage

This record carries the engine's **coverage receipt block**, generated in the 081c review-fix with
`git-delta-review.sh receipt --review-file … --since c46da4d2 --head e5afed1f --renderer text` plus legal
skip reasons (`non-code-file` for fixture data, `generated` for the regenerated copies). The table below is
copied from that block; the receipt itself is the authoritative record.

| Field | Value | Basis |
|-------|-------|-------|
| Changed files | 67 | `git-delta-review.sh diff --files` (also `git diff --name-only \| wc -l`) |
| Judged | 29 | per the receipt block; the judged set is enumerated there |
| Skipped, with reason | 38 | per the receipt block: fixture data (`non-code-file`) and regenerated copies (`generated`); the independent parity checks remain the verification for the latter |
| Gap | 0 | 29 + 38 = 67; no file is unaccounted for |

Judged set (29, enumerated by the receipt block; principal files): `templates/commands/review.md`, `templates/commands/checklist.md`,
`templates/review-template.md`, `shared/workflow/acceptance-hardening.md`,
`skills/internal/review-feature-quality/SKILL.md`,
`skills/internal/review-feature-quality/references/artifact-and-implementation-review.md`,
`skills/internal/review-sdd-process/SKILL.md`, `skills/internal/code-review/SKILL.md`,
`docs/reference/commands/review.md`, `tests/contract/test_acceptance_review_composition.py`,
`test_review_code_composition.py`, `test_review_feedback_boundary.py`, `test_client_guard_sweep.py`,
`test_review_docs_isomorphism.py`, `test_gate_wiring_081.py`, `test_skill_layer_visibility_guards.py`,
`test_expression_compatibility.py`, `test_migration_distribution.py`,
`.specify/specs/081-acceptance-hardening/{notes/red-first-evidence-081c.md,tasks.md,verification.md}`,
`.specify/specs/081-acceptance-hardening/test-evidence/{closure-verdict-081c.json,smoke-081b.txt,
tasks-081c-part3-tests.txt,tasks-081c-slice-tests.txt,tasks-081c-t012.txt}`,
`.specify/state/081-acceptance-hardening.md`.

**Uncommitted scope**: none at the start of this run — `git status --short` over the reviewed paths was
clean. The only paths this review wrote are this record and `review.md`; no implementation, task,
verification or commit was touched.

## Gate

No `blocking` entry. The three `important` findings (1, 2, 3) and the three suggestions were answered in
the 081c review-fix (see § Review-fix dispositions); the code-segment gate is no longer
`blocking-unresolved`. The feature's own claim (`Blocked`, 2 of 3 call sites) still has not earned
`Ready for Review` — that is an acceptance-axis fact, not a code finding.

Measured readings behind the verdict (all re-run in this review, not inherited):

| Reading | Command | Result |
|---------|---------|--------|
| the slice's own contract module | `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_review_composition.py -q` | green (part of the 239 below) |
| the eleven-module close set | `bash scripts/bash/run-tests.sh <the 11 modules T014 names> -q` | `239 passed in 21.89s`, exit 0 |
| the feature smoke | `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` | `1 passed in 1.69s`, exit 0; the evidence file is byte-identical before and after |
| per-tool copies | `python3 scripts/python/regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.`, exit 0 |
| mirrors | `python3 scripts/python/sync-mirrors.py --check` | exit 0 — 22 / 409 / 138 / 3 / 119 / 62 files |
| unit rosters | `flow-class-check.py --action check`; `probe-utils.py --action probes --reconcile`; `probe-utils.py --action compile-embeds --check` | `80 units, 0 findings, gaps=0`; `118 internal + 0 external, 76 embeds`; `76 units, zero drift` |
| acceptance | `closure-acceptance-check.py --spec-dir .specify/specs/081-acceptance-hardening --json` | `verdict: block`, exit 1, `zero-final-path-pass`, `pass=0 blocked=1 deferred=0 partial=1 fail=0 unknown=0 total=2` |

The feature remains `Blocked`.



> **未提交范围（未评审）**: 8 个未提交路径未计入本次评审对象（.specify/specs/081-acceptance-hardening/contracts/review-composition.contract.md, .specify/specs/081-acceptance-hardening/tasks.md, shared/workflow/acceptance-hardening.md, skills/internal/code-review/SKILL.md, skills/internal/review-feature-quality/references/artifact-and-implementation-review.md, templates/commands/review.md, templates/review-template.md, .specify/specs/081-acceptance-hardening/review.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=c46da4d217aa1126e0bdf6b2ba3a4358f91bb01d
head=e5afed1fd15e02eab3510f9f817056a62489e09d
base_source=explicit
renderer=text
changed_files=67
judged_files=29
skipped_files=38
gap_files=0
lines_added=4466
lines_deleted=282
file.01.path=.claude/commands/speckit.checklist.md
file.01.verdict=skipped
file.01.reason=generated
file.02.path=.claude/commands/speckit.review.md
file.02.verdict=skipped
file.02.reason=generated
file.03.path=.github/prompts/speckit.checklist.prompt.md
file.03.verdict=skipped
file.03.reason=generated
file.04.path=.github/prompts/speckit.review.prompt.md
file.04.verdict=skipped
file.04.reason=generated
file.05.path=.opencode/command/speckit.checklist.md
file.05.verdict=skipped
file.05.reason=generated
file.06.path=.opencode/command/speckit.review.md
file.06.verdict=skipped
file.06.reason=generated
file.07.path=.qoder/commands/speckit.checklist.md
file.07.verdict=skipped
file.07.reason=generated
file.08.path=.qoder/commands/speckit.review.md
file.08.verdict=skipped
file.08.reason=generated
file.09.path=.specify/shared/definitions/flow-class-definitions.md
file.09.verdict=skipped
file.09.reason=generated
file.10.path=.specify/shared/definitions/probe-definitions.md
file.10.verdict=skipped
file.10.reason=generated
file.11.path=.specify/shared/workflow/acceptance-hardening.md
file.11.verdict=skipped
file.11.reason=generated
file.12.path=.specify/skills/internal/code-review/SKILL.md
file.12.verdict=skipped
file.12.reason=generated
file.13.path=.specify/skills/internal/review-feature-quality/SKILL.md
file.13.verdict=skipped
file.13.reason=generated
file.14.path=.specify/skills/internal/review-feature-quality/references/artifact-and-implementation-review.md
file.14.verdict=skipped
file.14.reason=generated
file.15.path=.specify/skills/internal/review-sdd-process/SKILL.md
file.15.verdict=skipped
file.15.reason=generated
file.16.path=.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081c.md
file.16.verdict=reviewed
file.17.path=.specify/specs/081-acceptance-hardening/tasks.md
file.17.verdict=reviewed
file.18.path=.specify/specs/081-acceptance-hardening/test-evidence/closure-verdict-081c.json
file.18.verdict=reviewed
file.19.path=.specify/specs/081-acceptance-hardening/test-evidence/smoke-081b.txt
file.19.verdict=reviewed
file.20.path=.specify/specs/081-acceptance-hardening/test-evidence/tasks-081c-part3-tests.txt
file.20.verdict=reviewed
file.21.path=.specify/specs/081-acceptance-hardening/test-evidence/tasks-081c-slice-tests.txt
file.21.verdict=reviewed
file.22.path=.specify/specs/081-acceptance-hardening/test-evidence/tasks-081c-t012.txt
file.22.verdict=reviewed
file.23.path=.specify/specs/081-acceptance-hardening/verification.md
file.23.verdict=reviewed
file.24.path=.specify/state/081-acceptance-hardening.md
file.24.verdict=reviewed
file.25.path=.specify/templates/review-template.md
file.25.verdict=skipped
file.25.reason=generated
file.26.path=docs/reference/commands/review.md
file.26.verdict=reviewed
file.27.path=shared/definitions/flow-class-definitions.md
file.27.verdict=reviewed
file.28.path=shared/definitions/probe-definitions.md
file.28.verdict=reviewed
file.29.path=shared/workflow/acceptance-hardening.md
file.29.verdict=reviewed
file.30.path=skills/internal/code-review/SKILL.md
file.30.verdict=reviewed
file.31.path=skills/internal/review-feature-quality/SKILL.md
file.31.verdict=reviewed
file.32.path=skills/internal/review-feature-quality/references/artifact-and-implementation-review.md
file.32.verdict=reviewed
file.33.path=skills/internal/review-sdd-process/SKILL.md
file.33.verdict=reviewed
file.34.path=templates/commands/checklist.md
file.34.verdict=reviewed
file.35.path=templates/commands/review.md
file.35.verdict=reviewed
file.36.path=templates/review-template.md
file.36.verdict=reviewed
file.37.path=tests/contract/test_acceptance_review_composition.py
file.37.verdict=reviewed
file.38.path=tests/contract/test_client_guard_sweep.py
file.38.verdict=reviewed
file.39.path=tests/contract/test_expression_compatibility.py
file.39.verdict=reviewed
file.40.path=tests/contract/test_gate_wiring_081.py
file.40.verdict=reviewed
file.41.path=tests/contract/test_migration_distribution.py
file.41.verdict=reviewed
file.42.path=tests/contract/test_review_code_composition.py
file.42.verdict=reviewed
file.43.path=tests/contract/test_review_docs_isomorphism.py
file.43.verdict=reviewed
file.44.path=tests/contract/test_review_feedback_boundary.py
file.44.verdict=reviewed
file.45.path=tests/contract/test_skill_layer_visibility_guards.py
file.45.verdict=reviewed
file.46.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/contracts/fixture.contract.md
file.46.verdict=skipped
file.46.reason=non-code-file
file.47.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/data-model.md
file.47.verdict=skipped
file.47.reason=non-code-file
file.48.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/feature-detail.md
file.48.verdict=skipped
file.48.reason=non-code-file
file.49.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/feature-registry.md
file.49.verdict=skipped
file.49.reason=non-code-file
file.50.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/plan.md
file.50.verdict=skipped
file.50.reason=non-code-file
file.51.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/requirements.md
file.51.verdict=skipped
file.51.reason=non-code-file
file.52.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/tasks.md
file.52.verdict=skipped
file.52.reason=non-code-file
file.53.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/test-evidence/smoke.txt
file.53.verdict=skipped
file.53.reason=non-code-file
file.54.path=tests/fixtures/acceptance-hardening/expected-artifact-missing/verification.md
file.54.verdict=skipped
file.54.reason=non-code-file
file.55.path=tests/fixtures/acceptance-hardening/review-implemented-blocked/feature-detail.md
file.55.verdict=skipped
file.55.reason=non-code-file
file.56.path=tests/fixtures/acceptance-hardening/review-implemented-blocked/feature-registry.md
file.56.verdict=skipped
file.56.reason=non-code-file
file.57.path=tests/fixtures/acceptance-hardening/review-implemented-blocked/plan.md
file.57.verdict=skipped
file.57.reason=non-code-file
file.58.path=tests/fixtures/acceptance-hardening/review-implemented-blocked/requirements.md
file.58.verdict=skipped
file.58.reason=non-code-file
file.59.path=tests/fixtures/acceptance-hardening/review-implemented-blocked/tasks.md
file.59.verdict=skipped
file.59.reason=non-code-file
file.60.path=tests/fixtures/acceptance-hardening/review-implemented-blocked/verification.md
file.60.verdict=skipped
file.60.reason=non-code-file
file.61.path=tests/fixtures/acceptance-hardening/review-implemented-clean/feature-detail.md
file.61.verdict=skipped
file.61.reason=non-code-file
file.62.path=tests/fixtures/acceptance-hardening/review-implemented-clean/feature-registry.md
file.62.verdict=skipped
file.62.reason=non-code-file
file.63.path=tests/fixtures/acceptance-hardening/review-implemented-clean/plan.md
file.63.verdict=skipped
file.63.reason=non-code-file
file.64.path=tests/fixtures/acceptance-hardening/review-implemented-clean/requirements.md
file.64.verdict=skipped
file.64.reason=non-code-file
file.65.path=tests/fixtures/acceptance-hardening/review-implemented-clean/tasks.md
file.65.verdict=skipped
file.65.reason=non-code-file
file.66.path=tests/fixtures/acceptance-hardening/review-implemented-clean/test-evidence/smoke.txt
file.66.verdict=skipped
file.66.reason=non-code-file
file.67.path=tests/fixtures/acceptance-hardening/review-implemented-clean/verification.md
file.67.verdict=skipped
file.67.reason=non-code-file
<!-- coverage-receipt:end -->

## Review-fix dispositions (081c)

| Finding | Disposition | Evidence |
|---|---|---|
| 1 / A2 — second severity meaning set | **Fixed**: § A.4 now points at the owner's severity table and states only the grading procedure; the owner table carries the reader-consequence scope note | `skills/internal/review-feature-quality/references/artifact-and-implementation-review.md`; reduced-set rerun 239 passed |
| 2 / I4 — receipt not required | **Fixed**: the command's code-segment Outputs require the `receipt` block, the code skill marks step 4 mandatory in a composed run, the template field treats a missing receipt as an input error, and this record now carries the block | `templates/commands/review.md`; `skills/internal/code-review/SKILL.md`; `templates/review-template.md` |
| 3 / F2 — rotation form | **Fixed**: the owner states `<record>-<slice>.md` with the timestamp fallback; the command points at it; `test_c12` re-pinned with its reason | `shared/workflow/acceptance-hardening.md` § Records and rotation; `tests/contract/test_review_code_composition.py` |
| 4 / I3 — registration face | **Fixed**: `description` and `short-description` describe four segments + ARC | `templates/commands/review.md` frontmatter |
| 5 / A7 — docs page restates the owner | **Fixed**: the judgment-object cells are pointers to § Review Composition; segment names and skill paths remain | `docs/reference/commands/review.md` |
| 6 / I2 — ARC verdict alphabet | **Fixed**: the owner and the template state the `accept`/`block` ↔ `agree`/`refused` mapping, including the `Blocked` claim | `shared/workflow/acceptance-hardening.md`; `templates/review-template.md` |
| nitpick — `_sweep()` re-walk / local regex | **Recorded**: tidiness, no verdict impact | this section |
| question — three census mechanisms | **Recorded**: one pin per carrier is the current owner; a fourth carrier would owe its own pin | this section |
