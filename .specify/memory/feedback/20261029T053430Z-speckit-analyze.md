---
id: "20261029T053430Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261029T053000Z-b074an2"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "074b-nested-governance"
feature_id: "074"
partial: false
created: "2026-10-29T05:34:30Z"
summary: "analyze rerun on slice 074b (read-only, one-loop limit): 0 CRITICAL / 0 HIGH / 4 MEDIUM / 5 LOW; both round-1 HIGH resolved (F-01 by the C-3/C-6 reading rule now read jointly with T018/DoD-8; F-02 by "
---

## Review
analyze rerun on slice 074b (read-only, one-loop limit): 0 CRITICAL / 0 HIGH / 4 MEDIUM / 5 LOW; both round-1 HIGH resolved (F-01 by the C-3/C-6 reading rule now read jointly with T018/DoD-8; F-02 by qualifying 074a's local FR 017 and confirmed mechanically: pre-analyze --stage plan and --stage tasks both decision=pass errors=0 advisories=21); all seven round-1 MEDIUMs verified landed at their evidence locations; 13 checklist items dispositioned (3 [Gap] items: one raised, two covered-by); 6 deterministic gates re-run green; zero artifact modified, zero commit, zero push.

## Optimization Points
- The rerun delta carried the whole verdict: naming each round-1 HIGH's evidence location made resolved-vs-carried decidable without re-running detection, and the mechanical gate (pre-analyze plan+tasks) settled F-02 with two exit-status lines rather than a reading exercise.
- F-01's repair shape mattered more than its wording: a general reading rule (red baseline id => verdict-unchanged, green => MUST pass) plus T018/DoD-8 already using verdict-unchanged makes the two criteria jointly decidable, but leaving the rule as unnumbered prose keeps it outside the clause partition, so no [green:] claim and no coverage line can see the very rule that closes the finding - a numbered or task-cited home would make it auditable.
- Reading the checklist as a dated record rather than as current truth was the right move: three of its fail rows quote design states the remediation removed (C-25 'exactly one' vs V-5 'at most one' no longer exists), so a rerun must report the checklist verdict itself as stale instead of re-raising the same 13 items.
- Cross-checking a checklist premise against the owner's body paid off: 'the handoff is one field short' does not survive reading nested-invocation.md (seven fields; the retained-branch duty is a rule on the branch value), so the disposition had to correct the premise rather than raise a requirement gap.
- The handoff-vs-section field boundary is where a rerun finds new signal: C-29's 'a field the section lists that the handoff does not carry is recorded as missing' collides with the routing-verdict reference, which the handoff schema never carries, so the clause needs instance-level wording before the report test is written.
- Small static-gate cost: six gates at ~1s each replaced any need to re-read the clause partition by hand, and the coverage accountant's own advisory lanes (495 baseline-internal uncovered, 94 unparsable) stayed exactly where the baseline froze them.
