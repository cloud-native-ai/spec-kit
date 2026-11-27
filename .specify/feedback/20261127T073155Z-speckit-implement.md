---
id: "20261127T073155Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "r20261127T053750Z-109a-p3"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
feature: "109-prompt-adherence"
feature_id: "109"
disposition: "ignored"
partial: false
created: "2026-11-27T07:31:55Z"
summary: "Implement P3 (T017–T026) for 109-prompt-adherence. Landed the owner guard red-first (red run 3 failed / 7 passed, each failure the named missing-coverage-map assertion, no import errors) and closed it"
disposition_reason: "introspection:introspection-20261127T162331Z:excluded"
---

## Review
Implement P3 (T017–T026) for 109-prompt-adherence. Landed the owner guard red-first (red run 3 failed / 7 passed, each failure the named missing-coverage-map assertion, no import errors) and closed it green with the engine guard (40 passed). Authored the premise chain and machine-parsed coverage map in the owner document: twelve AB-NN assumed behaviors dense in document order, six sensor targets resolving to the six catalog row ids and six blind-spot targets resolving to the six register ids. Extended the engine guard red-first with the --check-coverage legs (red run 5 failed / 25 passed: clean, four doctored copies covering all five checks, and the unusable-owner degradation) and implemented the action (exit 0 with the zero-findings line, exit 1 with the sorted finding list, exit 2 when the owner document is unusable). Took SC-004's reading: exit 0 zero findings on the delivered document; a doctored copy exits 1 naming the dangling target and the now-uncited catalog row. Authored the read-only containment guard (baseline hash manifest captured by the test immediately before each reading; comparison unit the 14 declared store roots projected as .specify/<store-name>/ through declaration_reader; allowed delta none; bytecode caches excluded by name; zero-write-point AST scan; comparator drill; determinism judged separately by run-A/run-B equality) and closed it green (5 passed; before/after manifest identical at 4 populated roots / 7 files). Authored the init fixture (fresh project initialized from this repository's framework sources contains the owner document, the five facts and the engine; the installed entry answers --version; the socket-blocked bare invocation exits 0 with explicit not_evaluated / Unobserved lines, per-store reasons and all six blind spots; no instructions section and no command or skill surface; C-037 inventory-only scope) and closed it green (7 passed).

## Optimization Points
- Red-first evidence now carries T017, T019, T021, T022, T025 and T026 sections with real commands, outputs and exit codes. Staged state declared honestly: --since/--until still exits 2 with a not-delivered message until US4 (T028); output caps ride T028 and audit replay T032. Known baseline, not a regression: the .specify mirrors of the owner document and the engine are still MISS/DIFF until T033's single projection. The T019 unreadable-owner leg passed at red time because the owner degradation path pre-exists the action; disclosed in the evidence rather than counted as a closure. No anomalies.
