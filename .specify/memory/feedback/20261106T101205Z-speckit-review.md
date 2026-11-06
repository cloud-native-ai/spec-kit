---
id: "20261106T101205Z-speckit-review"
unit_id: "/speckit.review"
unit_type: "command"
run_id: "r20261106T100730Z-087rev"
scope: "local"
probe: "speckit-review-wrapup"
kind: "internal"
slice: "commands"
feature: "087-arch-diagram-docs"
feature_id: "087"
partial: false
created: "2026-11-06T10:12:05Z"
summary: "Four-segment review completed: process blocked (stage closed without verification.md), artifact blocked (1 P0: verification.md absent), implementation blocked (checker semantics and a shipped-skill po"
---

## Review
Four-segment review completed: process blocked (stage closed without verification.md), artifact blocked (1 P0: verification.md absent), implementation blocked (checker semantics and a shipped-skill portability defect), code blocked (2 blocking, 6 important, 1 suggestion); ARC input error because verification.md is missing. Feature stays Planned; no status flip.

## Optimization Points
- The implement stage can close U4 while verification.md is absent; seed the file and gate U4 on its existence.
- Shipped skills under skills/external/ are flattened to .specify/skills/, so links written as ../../specs/087-... are dead in client projects; the skill-authoring guidance should require a shipped-reference target.
- build_fixtures.py --check verifies only path presence; a bare --help rebuilds the fixtures and a record-content drift still prints OK. Make the check byte-exact and reject unknown flags.
