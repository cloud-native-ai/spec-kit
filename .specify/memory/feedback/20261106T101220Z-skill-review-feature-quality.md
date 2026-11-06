---
id: "20261106T101220Z-skill-review-feature-quality"
unit_id: "skill:review-feature-quality"
unit_type: "skill"
run_id: "r20261106T100730Z-087rev"
scope: "local"
probe: "skill-review-feature-quality-wrapup"
kind: "internal"
slice: "skills"
feature: "087-arch-diagram-docs"
feature_id: "087"
partial: false
created: "2026-11-06T10:12:20Z"
summary: "Artifact segment blocked: expected set 10/11 with verification.md missing (P0 F1), two normative contradictions (F2 docs/ Out of Scope vs FR-001, F3 fixture invariant vs DoD-4), plus assertion-name/po"
---

## Review
Artifact segment blocked: expected set 10/11 with verification.md missing (P0 F1), two normative contradictions (F2 docs/ Out of Scope vs FR-001, F3 fixture invariant vs DoD-4), plus assertion-name/pointer/count drift (F12-F20). Implementation segment blocked: source-only reference reads satisfied (F4), suffix list misses HTML/PDF/drawio/excalidraw (F5), shipped skills link spec-local contracts (F6).

## Optimization Points
- A shipped skill must reach its normative record schema through a distributed reference; the authoring repo's .specify/specs/<feature>/contracts path is dead in every client project.
