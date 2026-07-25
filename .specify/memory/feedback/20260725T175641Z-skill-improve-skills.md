---
id: "20260725T175641Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "feedback-triage-groupB-20260726"
scope: "local"
feature: "feedback-system"
partial: false
created: "2026-07-25T17:56:41Z"
summary: "Group B command-layer optimization batch (B1-B3): applied 11 triaged feedback items to requirements/clarify/plan/tasks/implement/review command templates plus requirements/plan/tasks templates, create"
---

## Review
Group B command-layer optimization batch (B1-B3): applied 11 triaged feedback items to requirements/clarify/plan/tasks/implement/review command templates plus requirements/plan/tasks templates, created scripts/python/regen-command-copies.py to make per-tool fan-out deterministic (fixed 6 qwen TOML + 4 opencode + 1 constitution-mirror drift files), and verified zero regression via stash-based failure-set diff against clean HEAD (both sets 106F+13E, byte-identical). Coverage-check-first habit again saved rework: several queued items were already absorbed by prior evolution.

## Optimization Points
- The stash-based failure-set diff again proved its worth and surfaced a caveat: the failure baseline is only valid against the SAME commit — a new HEAD commit (23e17835) invalidated the recorded 52F+13E baseline, so always re-derive the baseline from the clean tree at the CURRENT HEAD instead of trusting a count recorded in an earlier session.
- regen-command-copies.py eliminated an entire class of hand-sync drift (found stale opencode/qwen copies mid-run); the remaining risk is agents editing templates but forgetting to run it — the new implement.md bullet mitigates this, and a pre-commit `--check` hook would close it fully.
