---
id: "20261109T084259Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261109T064500Z-092a-analyze2"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "092-goal-team-parallel"
feature_id: "092"
partial: false
created: "2026-11-09T08:42:59Z"
summary: "Analyze round 2 on 092: independently verified the 14-item round-1 repair and delivered a NOT-READY verdict (1 CRITICAL + 4 HIGH + 4 MEDIUM + 3 LOW). 11 of 14 closure rows held. The finding that matte"
---

## Review
Analyze round 2 on 092: independently verified the 14-item round-1 repair and delivered a NOT-READY verdict (1 CRITICAL + 4 HIGH + 4 MEDIUM + 3 LOW). 11 of 14 closure rows held. The finding that matters: every mandated gate was green while two closures were recorded without their edits (commit dae4a26c never touched plan.md or feature-ref.md), one was closed at the wrong layer (C-01 landed in requirements while the contracts still carry the refuted exit-0 predicate), and one requirement (C-1's binding-on-every-definition) is unsatisfiable on the live tree because 18 pre-existing archive residents have no binding record and no FR owns the backfill. Adjudicated all four residual risks: L-03 not a blocker (free-text name field, no generator), H-01 grammar fragility real but bounded (gate proven sensitive, masking narrow), wp03's 19 rows accepted, and FR-025's data blast radius owned by migration rows while three code items remain unowned. Applied one in-passing correction (the Assumptions preamble contradicted its own merged body).

## Optimization Points
- Green-but-wrong gate surface: all six mandated gates pass while 1 CRITICAL + 4 HIGH are open. None of them reads whether a contract clause agrees with the FR it cites, whether a published map (feature-ref.md) resolves, or whether a MUST-field requirement is satisfiable on the live tree. A structural gate set cannot substitute for a semantic read; the analyze stage must keep doing that read even when every gate is green. (token-efficiency: the two defects that survived round 1 were found by a programmatic reverse map over the contracts, not by re-reading prose — extending a gate to regenerate feature-ref.md's table would have caught one of them for free.)
- A repair that records a closure MUST be verified against the diff, not the note: commit dae4a26c closed H-02/M-04 in prose while never editing plan.md or feature-ref.md. Verifier-side rule: for every "closed" row, confirm the named artifact actually changed in the repair commit's --stat.
- Unit-id grammar is duplicated in prose: contracts C-71/C-72/C-74 and T020 prescribe `command:<name>`, which both flow-class-check.py and run-determination.py reject (both accept /speckit.<stem>). Cite the engine's grammar by reference instead of restating a form in the contract layer.
