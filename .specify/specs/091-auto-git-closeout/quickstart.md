# Quickstart — Feature 091 Automatic git Close-out

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](plan.md)

Eight walkthroughs. Scenarios **S-0** and **S-7** run on a machine today and were executed while writing this plan;
**S-1**…**S-6** describe behaviour that does not exist yet, so each names the implementation premise it rests on and
MUST NOT be read as a claim that the behaviour is live. Every command below is either executed (with its reading
pasted) or explicitly marked as not-yet-runnable.

Vocabulary used here, fixed by `requirements.md` § Clarifications: **收口 (close-out)** is the last step of a write
lifecycle — commit the run's records, then merge and push per the declared workflow model. **`Closeout`** is the
project-level declaration that names the strategy. **只读上游 (read-only upstream)** is a remote the project declares as
never pushed. **回执 (receipt)** is the one file a close-out writes to record which record files its commit covered.

---

## S-0 — Today's declaration, and why it does not yet close anything (read-only, executed now)

```bash
sed -n '/GIT_WORKFLOW_START/,/GIT_WORKFLOW_END/p' .specify/workflow/git.md
```

Reading taken on 2026-11-09: the block declares `Workflow model`: 临时分支（trunk-based）, trunk `master`, the feature-branch
convention `NNN-<slug>`, three pushable fork mirrors (`github` / `gitlab` / `gitee`) and one remote marked read-only
upstream (the default-named upstream remote). It carries **no** `Closeout` row.

```bash
grep -c "Closeout" .specify/workflow/git.md || true
```

Reading: `0`. This scenario's point is the *before* picture — the block already knows the model and the remote roles,
which is exactly the information a close-out needs, and it carries no strategy row yet.

**Premises**: the file exists and its markers are paired (an existing contract test,
`tests/contract/test_git_workflow_instructions_block.py::test_state_file_carries_the_managed_block`, asserts the pairing).

---

## S-1 — A temp-branch project with `commit+merge+push` closes on its own

**Not yet runnable** — grounds on `closeout-executor.contract.md` C-3 and FR-010.

On a project whose block declares the temp-branch model and `Closeout: commit+merge+push`, the client asks the skill
for the close-out after the records step. Expected derived sequence, in order:

1. cut or reuse the short-lived feature branch `NNN-<slug>`;
2. commit the run's records plus their receipt;
3. merge the branch back into the trunk;
4. delete the local short-lived branch (only because step 3 landed);
5. push the trunk to each remote in `Closeout remotes` — after removing any remote marked read-only upstream.

**Premises to re-measure at implement**: the trunk's actual name comes from the block, not from this document; the
short-lived branch name follows the block's convention; the project has at least one declared pushable remote.

---

## S-2 — `ask` (or no row at all) presents the sequence and stops

**Not yet runnable** — grounds on `closeout-declaration.contract.md` C-3 and C-5.

With the strategy absent or `ask`, the close-out derives the same sequence and **prints it**, ending with a line that
says the push was not performed because the project has not authorized one. Nothing is blocked, nothing waits: the
report is the deliverable, and the next user turn decides.

**Premises**: an absent row is read as `ask`; the presentation excludes every read-only-upstream remote from the printed
commands.

---

## S-3 — The remote refuses the push; the run stops and hands back the command

**Not yet runnable** — grounds on `closeout-executor.contract.md` C-5 and FR-011.

Setup for the fixture: a local bare remote, a clone, one commit pushed, then a second commit pushed from a second clone
so the first clone is behind. On the first clone's close-out, the expected outcome is: a non-zero result, a report that
names the push stage, the exact push command printed verbatim, and **no** automatic retry and **no** forced push. The
remote's history is unchanged.

**Premises**: the fixture's second clone shares the bare remote; no network is involved.

---

## S-4 — A merge conflicts; the line stops before any push

**Not yet runnable** — grounds on the same clause, second arm.

Two commits that touch the same line in the fixture produce a conflict at the merge step. Expected: the close-out stops
at the merge, reports the conflicting paths, and never reaches the push step. The report's failing stage is `merge`.

**Premises**: the fixture seeds both sides with a conflicting edit before the close-out runs.

---

## S-5 — A read-only run skips the close-out and says so

**Not yet runnable** — grounds on `closeout-lifecycle.contract.md` C-5, first fork; FR-007 and SC-007.

A command that produced no artifact and no record ends with one line stating the close-out was skipped because there was
nothing to close. No empty commit is created and no push happens.

**Premises**: "produced nothing" is judged from the run's own artifact and record outputs, not from a clean working tree
(a clean tree may still hold another line's files).

---

## S-6 — Artifacts but no records: still merge and push, and say what is missing

**Not yet runnable** — grounds on the same clause, second fork.

The artifact commit exists, the run produced no feedback / quant / session / determination record. Expected: the
close-out merges and pushes what exists, and the report carries an explicit line that this close-out included no records
commit.

**Premises**: the artifact commit was produced by the run's own earlier step; the close-out does not invent a record to
make the commit look complete.

---

## S-7 — Dry run on this repository: derive the sequence, write nothing (executed now)

```bash
grep -n "Workflow model" .specify/workflow/git.md
git branch --show-current
git remote -v
```

Readings taken on 2026-11-09: `Workflow model`: 临时分支（trunk-based）; current branch `master`; remotes
`gitee` / `github` / `gitlab` (the fork mirrors) plus one default-named remote pointing at the upstream project, which the
block marks read-only.

The derivation this project's declaration implies, computed by hand because the operation does not exist yet:

| Step | Derived action |
|------|----------------|
| 1 | cut `091-auto-git-closeout` from `master` (temp-branch model) |
| 2 | commit the run's records + receipt |
| 3 | merge the branch back into `master` |
| 4 | delete the local branch (only after the merge landed) |
| 5 | push `master` to `github`, `gitlab`, `gitee` — **not** the read-only upstream |

This scenario writes nothing and pushes nothing; it is the evidence SC-006 asks for, and its limit is explicit: it
proves the **derived target set excludes the read-only upstream**, not that any remote accepts a push.

**Premises**: the declared model is the temp-branch one; the three fork mirrors remain pushable; the upstream remote
remains marked read-only.
