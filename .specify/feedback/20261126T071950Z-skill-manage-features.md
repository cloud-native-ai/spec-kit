---
id: "20261126T071950Z-skill-manage-features"
unit_id: "skill:manage-features"
unit_type: "skill"
run_id: "r20261126T071500Z-fb"
scope: "local"
probe: "skill-manage-features-wrapup"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-11-26T07:19:50Z"
summary: "One fact, two carriers, two statuses: line 107's registry row read `Implemented` while .specify/features/107-decision-governance.md line 6 still read `**Status**: Planned`; the review caught the diver"
introspection_ref: "introspection-20261127T162331Z#F-05"
disposition_reason: "introspection:introspection-20261127T162331Z#F-05"
---

## Review
One fact, two carriers, two statuses: line 107's registry row read `Implemented` while .specify/features/107-decision-governance.md line 6 still read `**Status**: Planned`; the review caught the divergence and both carriers now read `Ready for Review` (line 107, review A2). manage-features owns both carriers, but its reconcile/validation path does not compare the index row against the detail file, so a status flip can land in one carrier and survive in the other until a review happens to read both.

## Optimization Points
- 1. Add a status-equality check (registry row vs detail Status field) to the manage-features reconcile/validation path, reporting the mismatched pair by file and line.
- 2. Make the status flip an atomic two-carrier update (one writer/command) so a partial flip cannot land.
- 3. Test with a fixture whose two carriers disagree, so the check is shown to go red on drift.
