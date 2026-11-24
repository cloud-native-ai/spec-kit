---
id: "20261124T035115Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261124T024654Z-7c3e"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "103-team-view"
feature_id: "027"
disposition: "processed"
partial: false
created: "2026-11-24T03:51:15Z"
summary: "Analyze round 1 on 103-team-view (unattended, read-only): 0 CRITICAL / 0 HIGH / 4 MEDIUM / 2 LOW. E-01 coverage baseline absent (accountant status=baseline-missing) while the Feature 027 row says it i"
introspection_ref: "introspection-20261124T151412Z#F-03"
disposition_reason: "introspection:introspection-20261124T151412Z#F-03"
---

## Review
Analyze round 1 on 103-team-view (unattended, read-only): 0 CRITICAL / 0 HIGH / 4 MEDIUM / 2 LOW. E-01 coverage baseline absent (accountant status=baseline-missing) while the Feature 027 row says it is frozen; E-02 FR-018 cited on zero task rows although DoD-1 asserts full citation and its named oracle counts FRs, not citations; E-03 SC-006's only citing row (T037) cannot produce its evidence while T008 writes the covering test without citing it; F-01 two stale counts in the plan Phase 1 summary (18 vs 19 delivery entries; four vs three mapped test files); F-02 the team template's Scope pointer to goal-definitions.md § Archive Layers is dangling (owner is anchor-definitions.md), on the view's --scope inheritance path; F-03 quickstart pins three test names no task row mandates. Checks: decision-tensions ok (0 records, six labels pass); 38/38 clauses; FR citation 20/21; SC 7/7; all 12 measured premises reproduced; sync-mirrors/regen-copies/compile-embeds rc 0. Same-author gate not fired; zero-C/H coverage floor executed; no artifact writes, no commit, no push.

## Optimization Points
- 1) The analyze skill's section 3 shows account-clause-coverage.py --spec <dir>, but the program rejects --spec (rc 2); the skill should use the supported --spec-dir/positional form. 2) DoD-1 is phrased on pre-analyze-check errors=0, which counts FRs but not per-FR task citations, so a zero-cited FR cannot turn it red; add a citation-sensitive oracle. 3) create-tasks names coverage-baseline.txt as a Setup-row landing point while analyze treats freezing as the tasks-stage duty; state one timing, and have the stage evidence record freeze present/absent so a registry note cannot overstate it. 4) Registry stage notes are free prose; requiring each note to cite its evidence file path (or deriving it) would keep the registry from claiming states the evidence does not show.
