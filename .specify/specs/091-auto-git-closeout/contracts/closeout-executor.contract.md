# Contract — Close-out Executor

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)
**Owns**: the `closeout` operation's positioning in the git skill, the four model sequences, and the failure discipline.

**C-1** — One named operation, in the existing scope, with no second engine.

`skills/external/git-utils/SKILL.md` declares a named `closeout` operation inside scope A. Its position among the
skill's existing entry modes is determined by the two axes the skill already uses (block filled? operation argument
present?): close-out is the "filled + argument" case and joins the existing directed-convergence operations. The
feature introduces no second skill, no second engine, and no new dispatch table.

**The non-goals are an owned negative assertion, not a preamble.** Each item the feature forbids is discharged here, by
a statement whose subject is the absence of the thing:

| Non-goal | What the guard asserts is absent |
|----------|----------------------------------|
| a new `/speckit.*` command | no command surface is added for close-out; the operation lives in the existing skill |
| a daemon or scheduler | no process, timer or watcher is introduced; every invocation is caller-initiated |
| a second branch registry | no store other than the managed block records branch facts (see `closeout-declaration.contract.md` C-2) |
| an automatic force-push | the sequence contains no forced update that runs without its own gate (C-5) |
| code-host PR/MR automation | no remote API is contacted, so no PR/MR state participates in any decision (A17) |

The first three are file-and-search assertions over the repository; the last two are the behavioural arms C-5 already
owns. This clause is where the *set* is owned, so a reviewer reads one place to know what the feature refuses to be.

(FR-009, FR-027; clarify C-11c)

**C-2** — Undeclared and unusable states are refused, not guessed.

The operation refuses to derive a sequence when the model is undeclared, the block is missing, or the directory is not a
git repository. Each refusal is a distinct, named outcome with its own reason in the report. Refusal is the correct
behaviour: a guessed model is how a close-out pushes the wrong branch.

These three are the whole set of refusals, and they are exactly the three states
`closeout-declaration.contract.md` C-5 tabulates. A fourth "refuse because something looked odd" is not authorised: an
unrecognised condition is reported with the state it was read as, not promoted into a new refusal kind.

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

The substitution token is the literal `<remote>`, and the guard asserts on that token rather than on a description of
it: a surface that says "the remote is substituted" but writes a concrete name still fails.

(FR-002, FR-013; plan finding F-1)

**C-8** — The strongest strategy value is settled by a runnable transition, not by the declaration's prose.

`commit+merge+push` is the only value that authorizes a push without a per-run decision, and the sentence saying so
already exists (`closeout-declaration.contract.md` C-7). What a reader can *check* is the transition it implies, so the
carrier is behavioural and lives here:

| Declared value | Authorized action set | Transition |
|----------------|-----------------------|------------|
| `commit+merge+push` | routine steps of the derived sequence, push included | `derived → executed` |
| `commit+merge` | commit and merge, no push | `derived → executed`, push step `skipped (not authorized)` |
| `commit-only` | commit, no merge, no push | `derived → executed`, merge and push `skipped (not authorized)` |
| `ask` / absent | none | `derived → presented`, run ends, nothing executed |

"Routine" is the boundary: an action outside the four models' declared sequences is never routine, whatever the value
says. The table is the **only** place the value→authority mapping is written; C-7 of the declaration page says *what*
the strongest value authorizes and this table says *what happens* under each value, by pointer and not by a second
wording.

**Why a transition rather than a sentence.** A placeholder row that merely restates "the strongest value authorizes the
routine steps" is unverifiable — it can be true of any implementation. A transition can be exercised: the guard drives
each of the four values through the derivation and asserts the terminal state above. That is also why the declaration
page carries no runnable arm: the declaration is text a project edits, while the transition is behaviour this feature's
guard owns.

(FR-017, FR-019; clarify C-11c)
