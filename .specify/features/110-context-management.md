# Feature Detail: Context Management（上下文的声明、组合与只读审计）

**Feature ID**: 110
**Name**: Context Management（上下文的声明、组合与只读审计）
**Description**: 上下文的声明、组合与只读审计：两轴模型、五种物化形态与层级合法性、十八个上下文事实类及 owner/cap、组合触发点、只读审计引擎与分发。
**Status**: Ready for Review
**Created**: 2026-11-27
**Last Updated**: 2026-11-27

## Overview

Ported from the closed ai-harness `093-context-management` capability as additive surfaces: four declaration facts (categories/classes/forms/layers), one owner document, a read-only `context-audit.py` engine with two actions and nine check rules, an ambient instructions section within the existing budget, and a framework-map registration row. Existing owners stay unchanged; no store layout or decision-governance change.

## Latest Review

2026-11-27 `/speckit.review` (four segments + ARC), records `.specify/specs/110-context-management/review.md` and `code-review.md`. ARC: `accept`; `final_path` pass 9 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 9; comparison `agree`; no `F-ACCEPTANCE`. Code segment: zero `blocking` entries, gate `allow`, segment verdict `not-evaluated` (400 legal non-code/generated skips earn no coverage credit; all 29 code-path files reviewed). Findings: 0 P0 / 6 P1 / 5 P2 (process F1–F4; artifact F5–F8; implementation F9–F11), all recorded with evidence in `review.md` §3. Status `Implemented → Ready for Review` accepted (four conjunctive conditions hold).

## Key Changes

1. `shared/declarations/facts/context-*.yaml` four closed vocabularies; `shared/definitions/context-management-definitions.md` owner.
2. `scripts/python/context-audit.py` — read-only audit with declared exit codes and presence vocabulary; layout read through `declaration_reader`; no ported `store_layout.py`.
3. Instructions ambient section within the ~790 B headroom; framework-map row; mirror projection.
4. Contract/integration guards and evidence; analyze repairs AN-01 (seven-trigger composers) and AN-04 (audited-source read boundary).

## Implementation Notes

- Tasks T001–T039 closed in four serial packages; GATE-1…GATE-10 green; the crew-side `verification-input.md` is derived spec-side into `verification.md` by the driver at review hand-off.
- Analyze round 2: open C 0 / H 0 / M 10 / L 15 deferred.
- Registry row added by driver repair (the branch is based pre-109; reconcile with master's 109/111 rows at U6).

## Status Criteria

- Implemented: tasks closed, verification derived, gates green (met 2026-11-27).
- Ready for Review requires the four-segment review + ARC acceptance.
