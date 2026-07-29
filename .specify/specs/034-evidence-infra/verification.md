# Verification Log — 034-evidence-infra

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=59df9b24
baseline_date=2026-07-29
baseline_branch=034-evidence-infra

baseline_pytest_failed=84
baseline_pytest_passed=878
baseline_pytest_skipped=1
baseline_feedback_entries=57
baseline_skills_count=23

# -- /speckit.implement results --

run_date=2026-07-29
tasks_total=41
tasks_completed=41
tasks_deferred=0
deferred_tasks=

# Regression proof: comm -13 baseline-failed.txt current-failed.txt = 0 new failures
regression_pytest_failed=84
regression_pytest_passed=953
regression_new_failures=0
regression_method=failure-set diff (baseline-failed.txt vs current, comm -13)
tests_js_pass=182
tests_js_fail=0
new_contract_tests=62 (test_evidence_utils_cli 15 + test_evidence_findings_schema 19 + test_evidence_step_conformance 28)
new_integration_tests=13 (test_evidence_python_lanes 8 + test_evidence_compare_verdict 5)

# -- Success Criteria --

SC-001_status=pass
SC-001_value=tests/js 182/182 pass; session-analysis facts + core-change-watch project-profile manual runs emitted valid JSON (exit 0); UPSTREAM.md manifest matches directory tree (incl. asset-eval addition logged)
SC-001_note=asset-eval/ discovered as required import of asset-integrity.mjs during copy; added to subset + UPSTREAM.md manifest

SC-002_status=pass
SC-002_value=34/34 contract tests green (CLI C-E1..E11 + findings C-F1..F14); verdict-field recursive blacklist zero hits; evidenceState enum closed
SC-002_note=real collect on this repo: ev-20260729-073639-project (3 Node lanes)

SC-003_status=pass
SC-003_value=No-Node run (nodejs stripped from PATH): session/project/assets unavailable with reasons, runs=partial + feedback=available delivered 6 evidence items, exit 0
SC-003_note=also covered by TestNoNodeDegradation integration test

SC-004_status=pass
SC-004_value=feedback lane entries=57/58 matching index.json dynamic count at each collect; runs lane teamsScanned=2 (bh-port-monitor full + draw-plantuml-optimizer partial); redaction spot-check zero raw secrets/paths (C-F7 + critique-mask test)
SC-004_note=recurrence signal verified against constructed fixtures (3/6 recurrence); live store has 0 recurring themes (topic normalization is conservative) — consistent with manual uniq -cd spot check showing no exact duplicate points

SC-005_status=pass
SC-005_value=collect-evidence skill: orchestration run exercised (doctor + collect + latest reuse path); zero verdict-language (structural test); diff -rq mirrors identical; skill format checks green
SC-005_note=runtime-mode gate added after regression flagged Feature-028 conformance (caught by test_runtime_mode_gate)

SC-006_status=pass
SC-006_value=Dogfood loop on skill:improve-skills complete (collect ev-20260729-074502 → frozen triage → targeted change → intervention.json); 3 improve SKILL.md reference evidence-step.md + Unobserved red line (28/28 conformance); improve-team direct STATE.md/run-log parsing removed (grep-asserted); pre/post diffs preserved retained features
SC-006_note=triage record: .specify/specs/034-evidence-infra/dogfood-improve-skills.md

SC-007_status=pass
SC-007_value=Round-2 collect (ev-20260729-074720) + compare cited round-1 intervention, verdict=Unobserved (no comparable signal delta yet), written back to ledger; zero "fixed" claims
SC-007_note=honest-Unobserved is the correct outcome per FR-011 when no comparable data exists between rounds

SC-008_status=pass
SC-008_value=doctor probed all 8 supported tools (qoder+claude detected locally); platform-adapter-survey.md delivered with sequencing recommendation (claude verify-and-fill first)
SC-008_note=in-boundary deliverable only (Clarify Q3); new adapters are follow-up iterations

# -- Notes --

notes=Node 25.9.0 exceeds upstream engines ceiling (<25): doctor reports satisfies=false honestly; engine subset runs correctly on Node 25 in practice (182/182 tests, real collects) — no lane degradation observed. Engine copy required two boundary excisions logged in UPSTREAM.md: findings-recommend import removed from agent-lint (identity passthrough), asset-eval added to subset. tests/js facade invocations rewritten to direct capability CLIs (better-harness-cli not copied). Two verdict-layer upstream tests dropped (assert the excluded findings-recommend catalog). run-tests.sh runner used for baseline + regression with failure-set diff. Known baseline drift NOT touched per plan: .specify/skills historic 5/23 mirror gap (this spec mirrors only its own 4 skills), pre-existing 84 failing tests.
glossary_proposals=泳道(Lane)、证据合同(Evidence Contract)、干预台账(Intervention Ledger) — origin=auto, status=proposed, pending user confirmation
