---
id: "20261109T085734Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261109T090000Z-analyze-repair2"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "092-goal-team-parallel"
feature_id: "092"
partial: false
created: "2026-11-09T08:57:34Z"
summary: "Analyze-repair round 2 on the MAIN tree closed the assigned 1 CRITICAL + 4 HIGH + 1 MEDIUM. The load-bearing lesson: two of the six findings (H-2 stale generated map, H-5 a decision record disagreeing"
---

## Review
Analyze-repair round 2 on the MAIN tree closed the assigned 1 CRITICAL + 4 HIGH + 1 MEDIUM. The load-bearing lesson: two of the six findings (H-2 stale generated map, H-5 a decision record disagreeing with its FR) are invisible to every green gate, because no gate re-derives a generated artifact or compares a decision record to the FR it names — the conformance layer can therefore drift silently while all six gates stay green. Both were repaired by making the artifact re-derivable (the generating snippet is embedded in feature-ref.md) rather than by hand-editing cells, but the structural blind spot itself (round-2 § 6 item 8) is still open and is the first thing a later round should close.

## Optimization Points
- p1|One spec-edit slice cost three validate-tasks iterations because green-cross-phase compares clause ordinals against ROW order within one contract; appending new clauses to a contract forces the green row to move to the contract's tail, not to the story block it belongs to. Record the rule where the next author will read it: "a new clause goes at the contract tail and its green row goes after the rows claiming the earlier clauses".
- p2|A gated artifact can still be wrong when no gate reads it: feature-ref.md's FR map and a decision-tension record's decision both passed every gate while stale. Prefer embedding the generating command in the artifact so a reviewer can re-derive it, and prefer a test that diffs the regenerated form.
- p3|The fast-fail 'correction vs decision' test was load-bearing twice this round (H-3 option a vs b; H-5 edit vs note). Both were decisions; writing each antithesis and anti-metric into notes/analyze-round2-repair.md § 2 took less space than a later re-litigation would have.
- p4|Repairing a contract clause's literal grammar text (C-71) risks a second error: the first draft claimed both engines share one grammar, and re-measurement showed run-determination adds custom:<owner>/<name>. Reference an owner-literal by path instead of restating it.
