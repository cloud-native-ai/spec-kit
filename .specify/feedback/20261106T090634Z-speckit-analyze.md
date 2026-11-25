---
id: "20261106T090634Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261106T040353Z-087a-rev"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "087-speckit-visualization"
feature_id: "087"
disposition: "processed"
partial: false
created: "2026-11-06T09:06:34Z"
summary: "Round-5 revision analyze: GATE GREEN (C0/H0/M0, 17 LOW). New slice FR-023..FR-029 <-> C-53..C-72 <-> T055-T078 <-> 40 delivered paths <-> scenarios I-M <-> SC-011..SC-014 verified consistent; five val"
introspection_ref: "introspection-20261108T192504Z#F-12"
disposition_reason: "introspection:introspection-20261108T192504Z#F-12"
---

## Review
Round-5 revision analyze: GATE GREEN (C0/H0/M0, 17 LOW). New slice FR-023..FR-029 <-> C-53..C-72 <-> T055-T078 <-> 40 delivered paths <-> scenarios I-M <-> SC-011..SC-014 verified consistent; five validators rerun and archived; four known anomalies re-examined (only the Phase-8 prose cross-reference and the 28-vs-40 residue reproduce).

## Optimization Points
- F-24 highest priority: three artifact sentences claim the exec-quant reader de-duplicates by record identity, while load_records() is a plain concatenation of the legacy stream and the per-record directory; F-19: C-47 points the not-evaluated marker literal at reporting-obligations.md sec 9, which carries no such literal, and three literals (not evaluated / not_evaluated / -) coexist with no stated relation; F-20: FR-023 leans on an 'entry bound' the status line does not declare (FR-012 bounds only the digest); F-21: C-46 closes the guard at thirteen propositions and no FR declares the element's relation to it; F-23: A22's 186/151/35 store counts measure 187/152/35 today and EP-011's '36 of 245, all carried' is wrong (35 valued, mixed provenance).
