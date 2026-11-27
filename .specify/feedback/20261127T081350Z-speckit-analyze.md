---
id: "20261127T081350Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261127T071500Z-111a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "111-general-best-practices"
feature_id: "111"
partial: false
created: "2026-11-27T08:13:50Z"
summary: "Analyze round 1 for 111-general-best-practices: full read-only consistency analysis over requirements / checklists / plan / data-model / quickstart / feature-ref / tasks / four contracts produced 12 f"
---

## Review
Analyze round 1 for 111-general-best-practices: full read-only consistency analysis over requirements / checklists / plan / data-model / quickstart / feature-ref / tasks / four contracts produced 12 findings (CRITICAL 1, HIGH 2, MEDIUM 3, LOW 6). CRITICAL: the promotion rule is attributed to knowledge-promotion.md which does not define a feedback-to-owner-file promotion (its threshold is 2+ user emphasis), while C-305 forbids what C-104(c)/C-302/T009 require the manifest to state - the plan's Constitution Check XIV pass is unsupported. HIGH: A-17/FR-004/C-301/T009 require observation notes carrying the marker and stem, but feedback-utils record has no notes field (args-manifest: unit-id/run-id/review/points; action_record ignores --notes; compose_entry writes frontmatter + Review + Optimization Points) and no ad-hoc unit/run-id convention; the C-404/T004 shared prelude asserts .specify/shared/best-practices/ exists, but T008/T010 claim green before T012 regenerates the mirror. MEDIUM: the manifest's mandated spec-local entry-shape contract pointer is not distributed by specify init (downstream dangling pointer); second-mechanism detection is phrased five ways with C-304 (exact names) and C-404(d) (wildcard) disagreeing; the containment residual predicate in GATE-7/T019 omits the per-entry qualifier C-406 carries so an aggregate append could pass. LOW x6: unverified map-row adjacency/Notes elements; seed source-line exempt-vs-absent; A-15 module-wide vs manifest-only table scope; six unregistered guard literals; undefined same-change referent; init-drill CLI form (closed downstream in tasks). Machinery verified green: validate-requirements 0/0 (220 lines), validate-tasks 0/0, 9 FR / 7 SC / 7 STR / 21 A / 3 US / 11 Edge / 3 RS / 24 clauses / 19 tasks / 5 EP / 9 scenarios / 40 CHK, FR 9/9 cited by contracts, 24 green tags each clause once, mirror 117-file baseline rc 0, containment 72 paths all inside FR-009, source module 61 lines with the three adaptation points. Report: test-evidence/analyze-round1-report.md; findings: test-evidence/analyze-round1-findings.jsonl (12 records).

## Optimization Points
- durable note: feedback-utils record silently accepts then drops --notes; anyone following A-17 literally loses the [best-practice] marker without an error.
