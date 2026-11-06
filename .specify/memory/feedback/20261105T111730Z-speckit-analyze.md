---
id: "20261105T111730Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261105T074027Z-084a-r3"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "084-harness-triple-structure"
feature_id: "084"
partial: false
created: "2026-11-05T11:17:30Z"
summary: "analyze round 3 (final gate) closed the path-A reopen: GATE GREEN with CRITICAL 0 / HIGH 0 / MEDIUM 3 / LOW 2, so the feature can proceed to /speckit.implement. All four round-2 rows are closed with r"
---

## Review
analyze round 3 (final gate) closed the path-A reopen: GATE GREEN with CRITICAL 0 / HIGH 0 / MEDIUM 3 / LOW 2, so the feature can proceed to /speckit.implement. All four round-2 rows are closed with re-measured evidence (R2-01 guard test green and the offender line gone; R2-02 structurally closed — C-044 7 rows / C-045 7 rows, 8 facts onto 8 units, T015/T016 and the scope table in sync, FR-006 (i) not inverted; R2-03 banner premise true; R2-04 no action). The three new MEDIUM rows are one-line repairs on non-criterion surfaces and each is stated with its measurement: F-10 the 'no-machine-fact.yaml carries 8 rows' reading collides with the two rows T020 writes into the same file (total 10); F-11 the history-categories exclusion anchor ('five category names zero hits in .py/.sh') does not reproduce (4 of 5 occur as unrelated tokens) although the exclusion itself stands; F-12 the repaired tasks banner mis-attributes the FR-lane 0/19 reading to the unused [green:] tag where its own cited authority says the cause is the missing citation groups. Two LOW: F-13 the C-044 ARC cell over-claims that all [ARC_*] placeholders are copied from --json (11 in section 2.4, 7 are checker keys); F-14 'ARC verdict mapping' is the only in-scope roster row not written as a kebab-case fact-slug. Coverage lane re-adjudicated after the scope contraction: status=uncovered / 0 of 19 FRs / 59 beyond baseline, still non-blocking because the [green:] tag is optional by its owner and no gate consumes the accountant's verdict.

## Optimization Points
- the targeted set re-derives to the same 16 files across two different stage bases, which is evidence that the selection inputs, not the base commit, drive clause (b)
