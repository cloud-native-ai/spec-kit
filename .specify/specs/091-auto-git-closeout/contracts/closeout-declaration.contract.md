# Contract — Close-out Declaration

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)
**Owns**: the two declaration rows in the git-workflow managed block, their value domain, and what the block may not gain.

**C-1** — The managed block carries exactly two new rows, with fixed names.

The block between `<!-- GIT_WORKFLOW_START -->` and `<!-- GIT_WORKFLOW_END -->` gains:

- a line whose label is **`Closeout`**, whose value is one of `commit+merge+push`, `commit+merge`, `commit-only`, `ask`;
- a line whose label is **`Closeout remotes`**, whose value is a comma-separated list of remote names, or an
  explicitly empty list.

Both rows MUST appear in the shipped block template (`skills/external/git-utils/assets/git-workflow-block.md`) in
placeholder form, so a newly initialized project is offered them during Bootstrap. Both rows MUST also appear in this
project's own instance file with this project's values.

(FR-001, FR-002, FR-004)

**C-2** — The block MUST NOT gain a second branch table or a restated model menu.

The block already owns the model declaration and the branch roles; the four-model menu belongs to the `git-utils` skill.
A project reading only its state file reaches the models through the skill, and the block may carry **at most one
pointer line** naming that skill. A second table listing models × branches inside the managed block is a defect this
clause forbids, and a structural test asserts its absence.

**The guard's scope is the block, on both surfaces — not one file.** "The block may not gain a second branch table" is a
proposition about the managed block's contents, and the block exists twice: once as the shipped template asset and once
as this project's instance. A guard that read only the shipped asset would leave the instance free to grow the very
table the clause forbids, and a guard that read only the instance would miss the template every new project receives.
The assertion therefore runs over **both** surfaces with the same predicates. Pre-existing rows of the instance are not
retroactively a defect: C-6's companion assertion compares against the pre-change snapshot, so what is judged is *this
feature's addition*, on either surface.

(FR-003)

**C-3** — The default is `ask`, and absence is indistinguishable from it.

When the `Closeout` row is missing, its effective value is `ask`. No surface may treat an absent row as
`commit+merge+push`, and no surface may infer a value from a neighbouring row. `ask` is the only value that never
pushes on its own; `commit+merge+push` is the only value that authorizes a push without a per-run decision.

(FR-001, FR-019)

**C-4** — The read-only role marking overrides the remotes declaration.

A remote the block marks as a read-only upstream is never a push target, whether or not it appears in
`Closeout remotes` and whether or not a caller's instruction names it. The exclusion is by **role**, read from the
block, never by matching a remote's name against a hardcoded list.

**Two absences, one outcome, distinguished reasons.** An *empty* `Closeout remotes` and an *absent* `Closeout remotes`
row both mean "no pushable remote": the push step is skipped, and the report says why. They are written as one outcome
on purpose — a project that deleted the row did not thereby gain a remote list — but the report names which of the two
it read, because a reader debugging a silent push needs to know whether their row was empty or gone. Neither may fall
back to the repository's configured remotes.

(FR-002, FR-013; clarify C-12)

**C-5** — An unestablished or unusable block is a reported stop, not a guessed model.

Three states are distinguished, and a consumer MUST NOT collapse them:

| State | Detection | Behaviour |
|-------|-----------|-----------|
| Block missing, or markers unbalanced | the file is absent, or `GIT_WORKFLOW_START` / `GIT_WORKFLOW_END` are not paired | report "workflow state surface unavailable"; skip merge and push; the artifact commit still stands |
| Block present, model still the placeholder | the `Workflow model` line still carries the Bootstrap placeholder literal | report "workflow not declared"; treat as no pushable remote; degrade to local commit + merge |
| Block present, model declared | any other value | derive the sequence (C-6) |

The close-out MUST NOT run Bootstrap, MUST NOT create a branch set, and MUST NOT write the block.

**The model axis and the remote axis are orthogonal, and the table is the model axis alone.** Rows 2 and 3 answer *"is
the model usable?"*; C-4 answers the independent question *"is there a pushable remote?"*. A declared model with no
pushable remote is **not** row 2 — it degrades the push step to "skipped, and the report says why" under C-4, and the
merge still runs. Collapsing the remote axis into the model axis would report "workflow not declared" against a project
that declared its workflow perfectly well — the defect H-04 named. Conversely, row 2's "treat as no pushable remote" is
a consequence of not knowing the model, not a second finding: such a project is reported once, under the model axis.

**Relation to the `ask` axis.** `ask` is a third, independent axis (C-3) and it does not move a project between these
rows. A project may be at row 3 *and* declare `ask`; then the sequence is derived (row 3) and presented rather than
executed (C-3) — derivation and authorization are different questions. Row 2 is the only state in which the close-out
cannot derive at all, and it is therefore the only one that is described as "degraded" rather than "presented".

(FR-009, FR-016; clarify C-2 / C-7 / A13)

**C-6** — The declaration is the model's only consumer-side copy.

Two facts are inherited by reference and MUST NOT be restated in the block: the merge form (fast-forward or merge
commit) and the conflict policy. Both are derived from the declared model's semantics as the skill defines it. Adding
either as a new block row would be the duplicate fact C-2 forbids.

(FR-003; clarify A16)

**C-7** — The declaration is the standing authorization, and nothing more.

`commit+merge+push` authorizes the routine actions **inside** the derived sequence. It does not authorize, and MUST NOT
be read as authorizing: a force-push, a push to a read-only upstream, or a destructive operation on a cross-project
shared branch. Those keep their own gate, whose owner is `shared/guidelines/confirmation-gates.md` — this contract
references that owner and MUST NOT restate its lists.

(FR-017, FR-018)
