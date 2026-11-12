# Red-first evidence — WP-01a (T006–T015)

Run `r20261112T064607Z-b101`, feature `101-anchor-goal-realignment`, package WP-01a.
Every reading below is a command actually executed in this package; the E2 full-suite baseline
(`test-evidence/suite-baseline-entry.txt`: rc=1, 8900 passed, 192 pre-existing failure ids,
3 skipped) is the comparison point and was **not** re-run.

## T006 — the owner file changes hands through a rename

Task obligation: `git log --follow` readings for both definition files, written into this file.

Staged diff shape (before committing):

```text
$ git diff --cached --stat -M
 shared/definitions/{goal-definitions.md => anchor-definitions.md} | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
```

Post-commit detection (`git show --stat -M --oneline HEAD`):

```text
9d9043502 refactor(101): move the definition owner file from Goal to Anchor (T006)
 shared/definitions/{goal-definitions.md => anchor-definitions.md} | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
 rename shared/definitions/{goal-definitions.md => anchor-definitions.md} (100%)
```

Pre-move blob of the Goal owner (the exact content the Anchor owner inherits and the Goal owner
is later rebuilt from, T008): `3e1c0a4f067915eb3928eb6de43737fb7e296ab9`
(`git rev-parse HEAD:shared/definitions/goal-definitions.md` on stage base `7920dc7b5`).

`git log --follow --oneline -- shared/definitions/anchor-definitions.md` (first ten rows):

```text
9d9043502 refactor(101): move the definition owner file from Goal to Anchor (T006)
8b9030371 refactor(layout): move the project anchors out of memory/ — .specify/{features,constitution,glossary,register,tools}.md + .specify/features/<NNN>-<slug>.md
91a69ed89 feat(094-wp05): peer lines, archive-layer routing and the US5 owner rewrites
377986b84 feat(093-wp3): T135 — target-concurrency paragraph in goal-definitions
8edd955d1 feat(090): anchor rename W1/W2 + 092 merge W3 (working set)
2cb68c446 feat(085): add temporary Goal/Team and stage-level concurrency
1adfa49ab feat(skill-layer-install-separation): internal/external skill layering + install split
1bc043780 feat(053-machine-decidable-artifacts): derive goal criterion subject sets from the repository instead of a retyped member list (Phase 7, US5)
b05209ee6 fix(goal): reject an empty criteria overwrite, add objective/title/boundaries, and label actions read vs write
236105385 feat(goal): add Target decomposition — run-assignable scope slices under Goal (038)
```

The chain reaches the authored history back to `a7fd58c7a finish analysis`; it is not a
"create mode 100644" first commit. `git log --follow` on the retired path
(`shared/definitions/goal-definitions.md`) reports the same chain terminating at the move commit,
which is the measured shape of "content changed owner, not content was rewritten".

Result: **PASS** — the rename is recorded with 100% similarity, and the old path has no second
live copy at this commit (T008 recreates the Goal owner as a new action-level file).
