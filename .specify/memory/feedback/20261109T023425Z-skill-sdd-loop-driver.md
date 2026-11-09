---
id: "20261109T023425Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261109T023000Z-auto-closeout"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
feature: "091-auto-git-closeout"
feature_id: "091"
partial: false
created: "2026-11-09T02:34:25Z"
summary: "Clarify stage on a 27-FR spec: 16 adjudications landed in place (FR-028, SC-008, 3 edge cases, 9 assumptions), the declaration artifact was created after measuring that the overlap gate was green whil"
---

## Review
Clarify stage on a 27-FR spec: 16 adjudications landed in place (FR-028, SC-008, 3 edge cases, 9 assumptions), the declaration artifact was created after measuring that the overlap gate was green while comparing nothing, and the re-run produced 36 adjudicated overlaps against completed lines only. One gate defect is surfaced rather than repaired (pre-analyze-check Contract-cell parsing).

## Optimization Points
- clarify U4 overlap-check returns a VACUOUS green when the feature has no declaration artifact: decision=clear, checked=1, overlaps=0. A gate that cannot distinguish "no declaration" from "no overlap" reads the same either way; the note field is the only signal and no exit code carries it. Reproduced twice this run (before/after feature-ref.md).
- overlap-check's current-surface declaration is free-text derived from EVERY backticked path in feature-ref.md, so stating "the following documents are NOT delivered" as backticked paths silently turns read-only documents into delivery claims (64 phantom nested-path rows against one completed line). A declaration format that cannot express "these are inputs" invites exactly that mistake.
- pre-analyze-check.py Runtime Stack Contract check applies str.strip("`") to the cell before os.path.exists, so a PAIRED code span followed by prose (`` `pyproject.toml`（说明） ``) is parsed as a path and exits 2. Same artifact passed at requirements and fails at clarify on the same unchanged cell; a byte-for-byte copy with a bare Contract cell passes.
- No check name convention for run-determination.py --declared-check/--green-check: the engine requires green-check values to be a subset of declared-check values (not substrings), which is not discoverable from --help and produced two rejected invocations before the right form was found.
