# Contract: Runner & Delivery Surface (RC-01…RC-08)

Owner of the runner-side invariants for FR-011 / FR-013 / FR-017 / FR-019 / FR-021 and
the SC-010 dependency boundary.

- **RC-01**: The canonical runner entry, its argument passthrough, and its interpreter
  resolution order stay unchanged. Slimming changes inside the runner (if any) MUST NOT
  alter which tests run, in what composition (FR-013).
- **RC-02**: `--names-out` keeps its semantics: sorted FAILED name list, one id per
  line, written in addition to the normal run; failure exit code = pytest's own result.
- **RC-03**: Serial is the default and always-runnable path. The xdist verdict for this
  spec: NOT adopted in the fixed measurement command (research R-7). If a future recorded
  scope decision adopts parallel args in the fixed command, the same command minus the
  parallel arguments MUST remain a runnable complete run, with an availability proof
  charged per FR-017(c); a degradation serial run is never budget evidence.
- **RC-04**: Contingency for the budget: if the closure-slot serial measurement exceeds
  600 s after all planned interventions, the recorded path is the requirements Edge Case
  procedure — dated evidence of measures taken plus an explicit scope revision or
  clarify escalation. Silent redefinition of the fixed command, quiet subset runs, or
  layer drops are forbidden.
- **RC-05**: Diagnostic markers may be added (e.g. slow); they MUST NOT change the
  composition of the fixed command's run (FR-011).
- **RC-06**: Delivery surface of this scope: tests/ (cases, fixtures), the canonical
  runner (only if needed), pyproject.toml (dev-side dependency group only), and this
  spec's test-evidence records. MUST NOT modify src runtime behavior to make tests
  faster; driver-face files receive reference-level updates only (FR-021).
- **RC-07**: Fixture git-hook neutralization is tests-side only: a conftest-scoped
  autouse fixture redirects the git global/system config env for the test process tree
  (fixture repos skip the host security-scanner hooks, ≈0.9 s per commit measured).
  It MUST NOT change any assertion, MUST NOT touch host git config, and MUST be scoped
  narrowly if any test is found to depend on global git config.
- **RC-08**: Test-side dependencies: dev-only dependency group at most; no runtime
  dependency expansion for the CLI package; no network steps; no resident services
  (FR-019). Verification at closure: runtime dependency diff empty (SC-010), test-side
  additions confined to the dev group, plus a retrieval check for network calls in
  changed test code.
