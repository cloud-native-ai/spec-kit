# Review — Feature 081, slice 081a

**Date**: 2026-11-03
**Branch**: `081-acceptance-hardening`
**Reviewed range**: `f9f6d4f3..d0186dc5` (review run); P0/P1 fixes landed in `0277b00f`
**Status**: `Blocked` — SC-001 blocked (1/3 call sites), SC-002 partial; closure checker `block` / exit 1 / `zero-final-path-pass`

## Verdict

The strict gate works: no artifact reads `Implemented`, both status carriers read `Blocked`, and the closure checker refuses the feature. The review found **P0=1, P1=5, P2=9**. The P0 and all P1 items were repaired in `0277b00f`; the P2 items were fixed or recorded. The feature remains `Blocked` because the remaining final-path acceptance is owned by 081b/081c/081d, not because of a review blocker.

## Findings and disposition

| ID | Severity | Location | Finding | Disposition |
|---|---|---|---|---|
| F2 | **P0** | `templates/commands/{tasks,implement}.md`; `tests/contract/test_stage_class_wiring.py` | 081 gate lines lived inside the 077 wiring card, so stripping the card removed the gate and no assertion noticed | Fixed: lines moved to their semantic homes; `BASELINE_SHA256` for tasks/implement re-measured with a dated reason; `templates/commands/implement.md` assertion added |
| F1 | P1 | `tasks.md` DoD-2 vs `notes/red-first-evidence.md` | DoD-2 claimed 4/4 red-first; only T007/T010 had red runs | Fixed: DoD-2 states 2/4 red-first and explains T008/T009 |
| F3 | P1 | `tasks.md` Slice Boundary; `verification.md` SC-003 | Vocabulary coverage claimed 2/3; actual is 1/3 (only feature-details) | Fixed: 1/3 recorded; the registry-holds-`Blocked` window is explicitly owned by 081d |
| F4 | P1 | FR-006 vs checker/contracts/plan/data-model/RC-14 | Three-key `final_pass/blocked/deferred` vs the owner's bucket shape | Fixed: one six-bucket `final_path` + total shape across the artifacts; checker emits it |
| F5 | P1 | `verification.md` acceptance summary | Hand-written `blocked=2` disagreed with the checker's `blocked=1 / partial=1` | Fixed: summary is copied from `closure-verdict.json` |
| F6 | P1 | contract traceability; `quickstart.md` | 081d carriers (`test_audit_writes_nothing`, `audit-history/`) cited as existing | Fixed: marked 081d |
| F7 | P2 | owner doc / checker `FINAL_PATH_BUCKETS` | `partial` had no bucket; a `partial` final SC counted as `unknown` | Fixed: `partial` is a first-class bucket; `unknown` only for a missing row |
| F8 | P2 | `templates/commands/tasks.md` + four copies | Lost opening `**` in a bullet | Fixed |
| F9 | P2 | contract C-03 | Spec-local claim-carrier resolution not recorded | Fixed |
| F10 | P2 | `validate-requirements.py` docstring | Stated an undeclared spec is outside the closure system; checker defaults to execution | Fixed: reason corrected; behavior unchanged |
| F11 | P2 | `quickstart.md`; `data-model.md` fixture table | Stale “does not exist” statements; 081b/081d fixture rows looked missing | Fixed |
| F12 | P2 | `tests/integration/test_acceptance_smoke.py` | Smoke rewrites its own tracked evidence | Recorded as a known item; 081d |
| F13 | P2 | `src/specify_cli/__init__.py` | Resolver parent-parent fallback could adopt a non-repo `templates/` | Fixed with a repo-root marker guard |
| F14 | P2 | `skills/internal/implement-feature/SKILL.md`; `templates/commands/implement.md` | Implement gate is prose + a test; no wrong-status audit yet | Recorded; `--audit-existing` is 081d |
| F15 | P2 | `.specify/state` only | Driver-completion disclosures were not reachable from the feature artifacts | Fixed: `notes/driver-completions.md` |

## Acceptance Reality Check

```
final_path  pass=0  blocked=1  deferred=0  partial=1  fail=0  unknown=0  total=2
claimed     Blocked
checker     verdict=block, exit 1, reason=zero-final-path-pass
tasks       closed=23  deferred=1 (T024)  open=0
```

`Blocked` is the honest state: no final-path criterion passes, the three implement/review/driver call sites are 1/3, and the review/driver sites are 081c/081d work. `Implemented → Ready for Review` is not applicable because the feature is not `Implemented`; `Blocked → Ready for Review` is illegal by design.

## Scope of the remaining work

- **081b**: runtime-stack/premises/inherited-blocker checks and `test_acceptance_premises.py`.
- **081c**: `review-feature-quality`, the four-segment review composition and the review call site.
- **081d**: `manage-features`/feature-index vocabularies, `--audit-existing`, driver line-state `blocked` and the driver closure/merge site, coverage/schema guard, final smoke.
- T024 is deferred to 081d; the registry currently reads `Blocked` while `manage-features` does not yet admit it — the documented window, not a pass.
