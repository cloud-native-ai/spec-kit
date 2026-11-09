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

(FR-003)

**C-3** — The default is `ask`, and absence is indistinguishable from it.

When the `Closeout` row is missing, its effective value is `ask`. No surface may treat an absent row as
`commit+merge+push`, and no surface may infer a value from a neighbouring row. `ask` is the only value that never
pushes on its own; `commit+merge+push` is the only value that authorizes a push without a per-run decision.

(FR-001, FR-019)

**C-4** — The read-only role marking overrides the remotes declaration.

A remote the block marks as a read-only upstream is never a push target, whether or not it appears in
`Closeout remotes` and whether or not a caller's instruction names it. The exclusion is by **role**, read from the
block, never by matching a remote's name against a hardcoded list. An empty `Closeout remotes` degrades the push step to
"skipped, and the report says why"; it MUST NOT fall back to the repository's configured remotes.

(FR-002, FR-013)

**C-5** — An unestablished or unusable block is a reported stop, not a guessed model.

Three states are distinguished, and a consumer MUST NOT collapse them:

| State | Detection | Behaviour |
|-------|-----------|-----------|
| Block missing, or markers unbalanced | the file is absent, or `GIT_WORKFLOW_START` / `GIT_WORKFLOW_END` are not paired | report "workflow state surface unavailable"; skip merge and push; the artifact commit still stands |
| Block present, model still the placeholder | the `Workflow model` line still carries the Bootstrap placeholder literal | report "workflow not declared"; treat as no pushable remote; degrade to local commit + merge |
| Block present, model declared | any other value | derive the sequence (C-6) |

The close-out MUST NOT run Bootstrap, MUST NOT create a branch set, and MUST NOT write the block.

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
