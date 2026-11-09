# Contract — Close-out Lifecycle

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)
**Owns**: where the close-out step sits in a run, what it commits, the three forks it must handle, and the report it owes.

**C-1** — The step is a named section of the canonical commit owner, placed after the record-producing steps.

`shared/workflow/artifact-commit-step.md` — the file every artifact-producing command already embeds by pointer — gains
one lifecycle section named as the close-out step. Its position is **after** the artifact commit and after the
record-producing steps (feedback / documentation), and the artifact commit stays first so attribution is unchanged. No
existing step is moved or renamed.

(FR-005)

**C-2** — The commit boundary is: artifacts first, records once, never twice.

The artifact commit (existing) carries the artifact and only it. The close-out carries the run's **records and their
receipt** in a single commit. A record file that appeared in the artifact commit MUST NOT appear again in the close-out
commit, and a record file the close-out could not include is listed in the report rather than silently dropped.

(FR-006; clarify C-10)

**C-3** — The records are settled by a receipt, not by rewriting or deleting the records.

The close-out writes one receipt per run — a new file, never an edit of an existing one — naming every record file the
commit covered, that file's action, the hash of the commit that carried it, and a **pointer** to the read rule of the
engine that consumes that record class. The close-out MUST NOT modify, truncate or delete a record file itself; that
lifecycle belongs to the retention lane the receipt points at. Two writers never contend, because each run writes a
distinct timestamp-named path.

(FR-028; clarify C-10, A19)

**C-4** — The report is mandatory and states absence explicitly.

Every close-out ends with a report that names: the receipt path (or `none` with the reason), the records commit hash
(or `not-created` with the reason), the merge outcome, one row per push target with its result, and any other line's
uncommitted files as deviations. A step that did not run says it did not run; omission is a defect, and "nothing to do"
is itself a reportable outcome.

(FR-007)

**C-5** — Three forks, three distinct behaviours.

| Fork | Condition | Behaviour |
|------|-----------|-----------|
| read-only run | no artifact and no record was produced | skip the close-out entirely, state it in one line, create no empty commit |
| artifacts without records | an artifact commit exists, no record was produced | still merge and push what exists; the report states "this close-out carried no records commit" |
| other lines' dirty files | the working tree holds uncommitted paths this run did not produce | report them as an upstream deviation; never stage them; never `git add -A` |

(FR-007, FR-014; SC-007)

**C-6** — The step honours the confirmation-gate owner for every action inside it.

Routine steps of the declared sequence proceed under the declaration (see `closeout-declaration.contract.md` C-7). A step
whose class is destructive or governance-kept stops and presents before it runs. The list itself is owned by
`shared/guidelines/confirmation-gates.md`; this document references it and cites no gate by name.

(FR-012, FR-017, FR-018)

**C-7** — Existing "this step does not push" wording is revised in place, in the same owner.

The owner currently states that the artifact-commit step does not push and that pushing is separately governed. That
sentence is rewritten to: the artifact-commit step itself does not push; pushing belongs to the close-out step that
follows it. The revision lands inside the same file — no second owner, and no other surface may repeat the old wording.

(FR-008)
