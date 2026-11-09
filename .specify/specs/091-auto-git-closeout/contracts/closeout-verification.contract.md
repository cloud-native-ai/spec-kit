# Contract — Close-out Verification

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)
**Owns**: what the guard module must assert, how the fixtures are built, and the two closed-set claims.

**C-1** — Structural clauses are asserted by reading files, not by running git.

The declaration rows and their value domain, the presence of the four model sequences in the command reference, the
lifecycle section and its revised push boundary, the pointer from each unattended mechanism, the absence of a second
branch table, and the scope-A operation's existence are all file reads. They run without a subprocess and without
network, so a fast loop stays fast.

(FR-023)

**C-2** — Behavioural clauses are asserted on end state, not on command strings.

Each of the four models gets one fixture repository plus one local bare remote, and the assertion is on the resulting
state: which branches exist, where each HEAD points, which commits are reachable from the push target, and what the
remote actually holds. A string assertion on "the command was printed" is not evidence that the branch moved.

(FR-024; SC-001)

**C-3** — Two failure fixtures, and a mutation that proves they can go red.

A rejected-push fixture (the remote advanced after fetch) and a merge-conflict fixture each assert: non-zero outcome,
the failing stage named, the exact command present in the report, and the remote's prior state unchanged by any forced
write. The guard also carries a mutation arm: injecting an automatic retry into the implementation MUST turn it red.

(FR-024; SC-003)

**C-4** — The destructive boundary is a closed-set claim with its three elements named in the test.

SC-004 and SC-008 compare the confirmation-gate scan against a baseline captured in the same run, compare **gates by
name** rather than by count, and name the owner that supplies the admissible-difference rule. The test MUST NOT
introduce a second equality constant for the total; an existing pin of that total belongs to another owner and is not
re-asserted here. Two mutation arms prove decidability: removing one gate reds the comparison, and copying the gate
list's plain text into any surface reds the structural assertion.

(FR-026; SC-004, SC-008; plan finding F-2)

**C-5** — The dry run is evidence, not a new artifact.

A dry run on this repository derives the sequence for the currently declared model and strategy, prints it, and writes
nothing to any remote. Its record lives in the feature's evidence directory. No separate verification document is
produced, and the dry run MUST NOT be counted as proof that a push works.

(FR-025; SC-006)
