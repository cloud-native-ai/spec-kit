# Contract — Close-out Executor

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)
**Owns**: the `closeout` operation's positioning in the git skill, the four model sequences, and the failure discipline.

**C-1** — One named operation, in the existing scope, with no second engine.

`skills/external/git-utils/SKILL.md` declares a named `closeout` operation inside scope A. Its position among the
skill's existing entry modes is determined by the two axes the skill already uses (block filled? operation argument
present?): close-out is the "filled + argument" case and joins the existing directed-convergence operations. The
feature introduces no second skill, no second engine, and no new dispatch table.

(FR-009; clarify C-6)

**C-2** — Undeclared and unusable states are refused, not guessed.

The operation refuses to derive a sequence when the model is undeclared, the block is missing, or the directory is not a
git repository. Each refusal is a distinct, named outcome with its own reason in the report. Refusal is the correct
behaviour: a guessed model is how a close-out pushes the wrong branch.

(FR-009, FR-016)

**C-3** — Four models, four derived sequences.

The operation derives the sequence from the declared model. The four shapes are:

| Model | Derived sequence |
|-------|------------------|
| single-branch | commit on the trunk → push the trunk |
| dual-branch | commit on the daily branch → sync/merge per the declared relation → push |
| temp-branch | cut the short-lived branch (or reuse it only if this line owns it) → commit → merge back to the trunk → delete the local branch → push the trunk |
| three-tier | commit on DEV → merge DEV→PRE → merge PRE→MAIN → push each declared branch |

A sequence MUST NOT skip an intermediate branch the model declares, and a model's projection names only its own
branches. The steps are derived per invocation; a hardcoded per-project sequence is the defect this clause forbids.

(FR-010; SC-001)

**C-4** — Short-lived branches: local only, deleted only after a landed merge.

The temp-branch model never creates the short-lived branch on any remote, so the close-out never deletes a remote
branch. The local branch is deleted only after the merge into the trunk actually succeeded; a name collision with
another line's branch is a reported stop, never a reuse and never a deletion.

(FR-015; clarify C-13, A5)

**C-5** — Fail at the first failure, hand back the command, never retry.

A conflict, a non-fast-forward or a rejected push stops the line at that step. The failing stage and the exact command
are written where the run's state is recorded and printed in the report. The close-out performs no automatic retry, no
`--force`, and no `--force-with-lease` unless that specific action passes its own confirmation.

(FR-011, FR-012; SC-003)

**C-6** — Staging is by explicit path; the working tree's other occupants are reported.

The close-out stages the paths it produced, by name. It MUST NOT use a whole-tree staging form, and it MUST NOT stash,
reset or clean a path it does not own. Files belonging to another line are reported as an upstream deviation in the
report, which is the only place they appear.

(FR-014)

**C-7** — Push targets come from the declaration, are substituted, and never carry a literal remote name.

The command surface for close-out resolves `<remote>` from `Closeout remotes` after the read-only role check (see
`closeout-declaration.contract.md` C-4). The close-out path therefore contains **no** hardcoded remote literal — a
project whose upstream is the default-named remote cannot be pushed by accident. This rule applies to the new close-out
reference; pre-existing examples elsewhere in the skill are reported, not silently rewritten.

(FR-002, FR-013; plan finding F-1)
