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
receipt** in exactly **one** commit for that run. A record file that appeared in the artifact commit MUST NOT appear
again in the close-out commit, and a record file the close-out could not include is listed in the report rather than
silently dropped.

**One commit covers all record classes.** The four record classes (feedback / exec-quant / session / run determination)
are not split into per-class commits: attribution's unit is one run, so one hash names the whole set. The hash written
into the receipt (C-3) is therefore that single commit's hash — the same value for every row of `covered[]`. A run that
produced records of only some classes still gets one commit covering exactly the classes it produced.

(FR-006; clarify C-10, A4, A6)

**C-3** — The records are settled by a receipt, not by rewriting or deleting the records.

The close-out writes one receipt per run — a new file, never an edit of an existing one — naming every record file the
commit covered, that file's action, the hash of the commit that carried it, and a **pointer** to the read rule of the
engine that consumes that record class. The close-out MUST NOT modify, truncate or delete a record file itself; that
lifecycle belongs to the retention lane the receipt points at. Two writers never contend, because each run writes a
distinct timestamp-named path.

**The hash is per-row but single-valued per run.** `covered[]` carries one `commit` field per row (see
`data-model.md` E-4), and C-2 fixes that the run produces exactly one records commit — so every row of one receipt
names the same hash. Writing the hash per row rather than once at the head is deliberate: it is the field that keeps a
future model (a class settled in a later commit) expressible without a schema change, and it makes the receipt's
self-description local to the row a reader is looking at. The invariant a guard asserts is C-2's, not the field's
arity: **within one receipt, all `commit` values are equal**.

(FR-028; clarify C-10, A4, A19)

**C-4** — The report is mandatory and states absence explicitly.

Every close-out ends with a report that names: the receipt path (or `none` with the reason), the records commit hash
(or `not-created` with the reason), the merge outcome, one row per push target with its result, and any other line's
uncommitted files as deviations. A step that did not run says it did not run; omission is a defect, and "nothing to do"
is itself a reportable outcome.

(FR-007; SC-007)

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

**The old sentence is named, not paraphrased.** The clause binds two decidable facts: (a) the identifiability of the
sentence being replaced — the owner's own sentence asserting that the step does not push is the object of the edit, and
the guard locates it by that assertion rather than by line number, so an edited-but-still-contradictory wording fails;
and (b) the **absence** of the old assertion from every surface this feature writes. Both are file reads, so no
subprocess is needed and clarify C-8's finding (no existing test anchors the sentence) is answered by this feature's own
guard rather than by inheriting an anchor that does not exist.

(FR-008; clarify C-8)

**C-8** — Every unattended mechanism calls this one step; none keeps a second one.

The close-out is not re-implemented per caller. Each unattended mechanism that today commits, merges or pushes reaches
this step **by pointer** to this owner, and the driver's existing close is one instance of it, not a sibling mechanism.
The pointer duty is an existence assertion over a closed, named set of mechanisms — the SDD driver's close, periodic
house-keeping, and the feedback digest — and the absence of a second implementation is a negative search over the
repository. Adding a fourth mechanism to that set is a revision of this clause, not a silent extension of the search.

**One consequence fixes the driver's authority.** Reaching this step by pointer gives the driver the *sequence*, not a
new permission: under a strategy that does not authorize a push, the driver's close ends where it ends today, at the
local merge. A pointer that silently widened the driver's authority would be a second owner wearing a reference.

(FR-020; clarify C-14, A9; SC-005)

**C-9** — The compiled wrap-up faces are rendered by the registry, never authored.

The wrap-up surfaces of each artifact-producing command and skill are generated: one handler row (or one handler plus
its bindings) is added to the probe registry, and the faces are produced by the registry's own compile action. No
compiled face is hand-edited, and the new row's order MUST NOT collide with an existing `wrap-up` handler's order — the
order it takes is the next free one in that sequence, measured rather than assumed.

Authoring a generated face by hand is the failure this clause exists to forbid: the next compile would then overwrite
the author's text and the change would vanish silently.

(FR-021)

**C-10** — The user-facing instruction surface gains a pointer, not the rules.

The `## Git Workflow` section of the instructions template and its runtime projection keep their existing
pointer-not-restatement shape. At most one line is added, and only if a reader cannot otherwise reach the close-out step
from that section; the rules stay in the owners this document names. That section already names close-out among the
mechanisms that trigger unattended commit/merge/push, so the default is **no edit**, and a measurement decides it.

(FR-022; clarify C-15)
