---
id: "20261027T091844Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261027T091830Z-072a"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "072-client-self-improvement"
feature_id: "072"
partial: false
created: "2026-10-27T09:18:44Z"
summary: "Unattended requirements stage for a new feature: derived the number with the project script (072, branch switch suppressed so the run stays on the spine's branch and the worktree is not moved), read t"
---

## Review
Unattended requirements stage for a new feature: derived the number with the project script (072, branch switch suppressed so the run stays on the spine's branch and the worktree is not moved), read the brief's verified baseline, and drafted requirements.md from the owner documents rather than from recall (feedback-step red lines and the custom-unit record contract, the self-improvement definition and workflow, the code-review non-interactive path, the two-hats criterion). The brief's Q1-Q10 are adjudicated in the spec with rejected readings and their costs. Deterministic gates: validate-requirements.py status=ok (0 error / 0 warning), decomposition-check --mode plan proceed (29/30), pre-analyze-check --stage requirements pass (errors=0, advisories all naming the lazily-created probes directory). Two framework gaps surfaced and are recorded as points; the run itself completed with no anomaly left unreported.

## Optimization Points
- The scaffold script (`create-new-requirements.sh`) has no way to suppress its `git checkout -b`: an unattended stage subagent must not switch branches, so this run had to shim `git` on PATH to keep the step's numbering/directory creation while dropping the branch switch. A `--no-branch` flag (or honoring a "no branch switch" env contract) would remove that workaround and make the stage reproducible without a shim.
- `pre-analyze-check.py` reports a dead-backticked-path advisory for directories the engines create lazily (here `.specify/memory/feedback/probes/`, created at the first probe injection). There is no way to declare such a path as expected, so every specification that names it carries a permanent advisory and the advisory count stops distinguishing real drift from known-lazy paths.
- Token-efficiency self-check: no wholesale dump of machine-managed stores (feedback/exec-quant inventories were read as directory listings and single-entry listings only), no deterministic work handed to the LLM (validation, decomposition and pre-analyze verdicts all came from the scripts), and no repeated read of the same large document beyond the authority docs the brief named. `token-efficiency` observation: the brief plus the pre-existing specification conventions cost most of the pre-draft reads; a machine-generated digest of "which precedent spec sections are mandatory" would have replaced several thousand lines of reading.
