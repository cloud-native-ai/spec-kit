# Contract — Close-out Verification

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)
**Owns**: what the guard module must assert, how the fixtures are built, and the two closed-set claims.

**C-1** — Structural clauses are asserted by reading files, not by running git.

The declaration rows and their value domain, the presence of the four model sequences in the command reference, the
lifecycle section and its revised push boundary, the pointer from each unattended mechanism, the absence of a second
branch table, and the scope-A operation's existence are all file reads. They run without a subprocess and without
network, so a fast loop stays fast.

**"No subprocess" scopes this clause, not its siblings.** The boundary between C-1 and C-2/C-3 is about *what proves
what*, not about a ban on running git: a structural predicate may not shell out (a block's rows, a pointer line, an
operation's presence are all readable), while a behavioural predicate must (a branch's end state cannot be read out of
a document). The guard module therefore carries both arms, and the reason is the blind-check lesson: a text search is
evidence about text only. The failure C-1 forbids is *using* a git run as evidence for a text proposition, or a text
match as evidence for a behaviour.

**The clause-form owner is reached by pointer.** These four pages use the closed `**C-N**` form, which is one of the
forms `shared/definitions/contract-clause-definitions.md` defines; that document owns the form set and this one declares
no new form.

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

**C-6** — The stability claim is a closed-set claim with all three elements, or it is not an acceptance basis.

Any assertion that "the rest of the behaviour is unaffected" is judged against
`shared/guidelines/closed-set-claims.md` and MUST name all three of its required elements — the baseline reference
object, the comparison unit, and the owner that supplies the admissible-difference set. A claim missing any one of the
three MUST NOT be used as an acceptance basis, however plausible it reads. The comparison C-4 performs is the concrete
instance; this clause is the rule that makes C-4's shape non-optional, so a later stage cannot substitute a softer
"nothing else changed" for it.

(FR-026; SC-004, SC-008)

**C-7** — The instruction surface's pointer duty is measured, and the measurement is the evidence.

The `## Git Workflow` section is asserted for one proposition only: whether a reader can reach the close-out step from
it. The assertion is a pointer-existence read, not a content review, and its outcome decides the delivery row rather
than the other way round — if the section already reaches the step, the guard records that reading and the row produces
no diff; if a reader cannot reach it, exactly one pointer line is added and the same guard then passes. Either way the
guard is written first, so "no edit" is a measured conclusion and not an omission.

The section MUST NOT gain a restatement of the close-out rules under this clause: FR-022 forbids restating them, and a
guard that accepted a restatement would turn the pointer duty into a licence for a second owner.

(FR-022; clarify C-15; SC-005)
