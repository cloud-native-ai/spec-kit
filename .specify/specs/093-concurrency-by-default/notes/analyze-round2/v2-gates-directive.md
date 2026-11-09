# V2 — Gates + Concurrency-Directive Verification (analyze round 2, 2026-11-09)

Worker: V2 (read-only fork verification). Worktree: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/093-clarify`, branch `093-concurrency-by-default`, HEAD `c5abfaaa`.
Full captured outputs: `test-evidence/v2-gates-small.txt`, `test-evidence/v2-account-clause-coverage.txt`, `test-evidence/v2-pre-analyze-check.txt`.

## A. Gate readings (verbatim)

| # | Gate (explicit flags, from worktree root) | Reading (verbatim) | Verdict |
|---|---|---|---|
| A1 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/093-concurrency-by-default/requirements.md` | `status: ok` — `[id-contiguous] pass (0)`, `[doc-order] pass (0)`, `[ref-resolvable] pass (0)`, `[marker-count] pass (0)`, `[dup-id] pass (0)`, `[path-marker] pass (0)`; `scanned: 335 lines, 47 definition rows, 11 shared strings`; `0 error(s), 0 warning(s)`; `EXIT=0` | PASS |
| A2 | `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/093-concurrency-by-default --corpus-root <worktree>/.specify/specs` | `status: baseline-missing`; `[fr-uncovered] pass (0) — 35 of 35 FRs cited from citation groups`; `[clause-uncovered] fail (656)`, `[clause-unparsable] fail (116)`, `[coverage-baseline-delta] fail (656)`; `ERROR frozen baseline not found: .specify/specs/093-concurrency-by-default/coverage-baseline.txt`; `companion (must be non-empty on a green run): claimed clauses 37, scanned files 319, clause universe 2210, FR universe 35`; `657 error(s), 1 warning(s)`; `EXIT=2` | EXPECTED — `baseline-missing` on the clause lane; FR lane GREEN (35/35) |
| A3 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md` | `PASS: .specify/specs/093-concurrency-by-default/tasks.md — 0 error(s), 0 warning(s)`; `EXIT=0` | PASS |
| A4 | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/093-concurrency-by-default` | `status: ok` — `[dtr-anchor] pass (0)`, `[dtr-section-missing] pass (0)`, `[dtr-record-incomplete] pass (0)`, `[dtr-tension-id] pass (0)`, `[dtr-rejected-form] pass (0)`, `[expected-sacrifice-unmapped] pass (0)`; `scanned: 415 lines, 5 record(s)`; `channel: value_domain=HIGH-or-0, high=0`; `0 error(s), 0 warning(s)`; `EXIT=0` | PASS |
| A5 | `pre-analyze-check.py --repo <worktree> --spec-dir .specify/specs/093-concurrency-by-default --stage requirements` | `{"stage": "requirements", "decision": "pass", ...}` — `pre-analyze-check: stage=requirements decision=pass errors=0 advisories=111 waived=0`; `EXIT=0` | PASS |
| A6 | same, `--stage plan` | `{"stage": "plan", "decision": "pass", ...}` — `pre-analyze-check: stage=plan decision=pass errors=0 advisories=111 waived=0`; `EXIT=0` | PASS |
| A7 | same, `--stage tasks` | `{"stage": "tasks", "decision": "pass", ...}` — `pre-analyze-check: stage=tasks decision=pass errors=0 advisories=111 waived=0`; `EXIT=0` | PASS |
| A8 | `decomposition-check.py --mode tasks --requirements .../requirements.md --tasks .../tasks.md` | `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 35, "task_count": 143, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}`; `EXIT=0` | PASS |

Gate summary: 7 PASS, 1 EXPECTED (`baseline-missing`), 0 unexpected failures. The FR coverage lane is green at 35/35; no `coverage-baseline.txt` exists yet, so the clause lane's red is the declared expected state, not a regression.

## B. Directive encoding vs USER RULINGS (2026-11-09)

| Ruling | Where encoded | Reading | Verdict |
|---|---|---|---|
| B1 FR-034 — analyze defaults to N concurrent SDD Analysis Workers; N from stage team config / spine `agent_concurrency_requested`, never fixed; serial only with a named closed-vocabulary reason | `requirements.md` L192 (FR-034), L323 (ruling record); `contracts/high-order-executors.contract.md` C-093 L66-72; `tasks.md` T013, T139–T141; plan L351–359 | N source named as "该阶段的团队配置 / 状态脊 `agent_concurrency_requested`"; "MUST NOT 在本规格中固化数字"; serial `N = 1` only "[[STR-003]] 的封闭词表给出具名理由码"; three co-requirements (read-domain exclusion, deterministic consolidation, reading triple + executor/verifier ids) all present | PASS |
| B2 FR-035 — FORK carrier via `skills/external/sdd-loop-driver/scripts/stage-runner.sh` (stdin prompt, stream-json, sentinel); host-internal in-process subagent path BANNED, not presented as an option; heterogeneous agents use subprocess | `requirements.md` L194 (FR-035), L325 (ruling record); C-094 L76-82; T142, T143; plan L360–372; script exists at `skills/external/sdd-loop-driver/scripts/stage-runner.sh` and its `.specify/` projection (both 12485 B, executable) | Fork form, stdin prompt, `--output-format stream-json`, sentinel, runtime `nproc` bound, and the in-process ban ("MUST NOT 被计为满足 FR-005(d)", T142 "host-in-process fan-out not counted", T143 rejects such a record) all encoded. **"heterogeneous agents use subprocess" is nowhere encoded**: 0 hits for `heterogeneous` / `subprocess` / `异构` across the whole spec tree. Substantively subsumed by FR-035's universal "every concurrent unit MUST be an independent qodercli child process" (no per-agent-type exception exists), but the ruling's sentence has no literal landing | PARTIAL — fork + ban PASS; heterogeneous→subprocess clause ABSENT (MEDIUM) |
| B3 SC-006 stays `not_evaluated` until the mechanism lands | `plan.md` L342, L387 (R-5); `tasks.md` L341, L369, L413, T110, T111; `checkpoints/02-clarify.md` L16, `04-tasks.md` L19/L27/L50, `05-checklist.md` L8; `quickstart.md` L116 | Plan: "SC-006's real-run evidence is deferred to a later run and written as `not_evaluated`"; tasks: "if the implement executor runs serially, SC-006 MUST be recorded `not_evaluated` — not `0`, not an estimate, not 'concurrency proven by fixtures'"; T110 records the not-yet-landed code + `effective: not_evaluated`; checkpoint 04 tracks "至少一个真实执行体完成 6 包 worktree 并发与确定性集成 | **not_evaluated** (unchanged, and named as a gap)". No artifact claims SC-006 evaluated | PASS |

## C. Complete-correction manifest coverage (plan/tasks rows)

Judgment rule: a surface is `covered` only when a plan/tasks row names the surface path and carries the correction content; generic sweep rows (T039/T040: "`skills/internal/**`, `skills/external/**`… pointer", "every execution body") neither name the surface nor carry the fork/in-process ban and are not counted as coverage.

| # | Framework surface (manifest) | Tasks row(s) | Status | Severity if missing |
|---|---|---|---|---|
| 1 | `skills/external/sdd-loop-driver/SKILL.md` | T139 (analyze default), T142 (fork model); also T105 | covered by T139/T142 | — |
| 2 | `skills/external/sdd-loop-driver/references/dispatch-recipes.md` | T139, T142 | covered by T139/T142 | — |
| 3 | `skills/external/sdd-loop-driver/references/watch-model.md` | none (0 hits for `watch`/`watch-model` in plan or tasks) | **missing** | MEDIUM |
| 4 | `skills/external/sdd-loop-driver/references/decomposition-model.md` | T140 (§ 20.1 analyze default), T118; also T060/T132 | covered by T140 | — |
| 5 | `skills/external/sdd-loop-driver/references/stage-prompts.md` | none (0 hits) | **missing** | MEDIUM |
| 6 | `skills/external/sdd-loop-driver/templates/stage-team-preset.md` | T116 (team obligation into the preset, C-068), T133 (slot sentence pointer); plan L201 lists the file | covered by T116 (+T133) | — |
| 7 | `skills/external/sdd-house-keeping/SKILL.md` | none — only a passing grain mention in T117 ("entry for house-keeping"), no row for this SKILL.md | **missing** | HIGH (in-process ban absent from an sdd-* skill) |
| 8 | `skills/external/sdd-house-keeping/references/maintenance-recipes.md` | none | **missing** | HIGH |
| 9 | `skills/external/sdd-project-setup/SKILL.md` | none — only a passing grain mention in T117 ("step for project-setup") | **missing** | HIGH (in-process ban absent from an sdd-* skill) |
| 10 | `skills/external/sdd-project-setup/references/setup-recipes.md` | none | **missing** | HIGH |
| 11 | `skills/external/coaching-skills/SKILL.md` | none (0 hits) | **missing** | MEDIUM |
| 12 | `skills/internal/analyze-artifacts/references/validation-and-report.md` | none (0 hits) | **missing** | MEDIUM |
| 13 | `shared/workflow/execution-topology.md` | none (0 hits) | **missing** | MEDIUM |
| 14 | `shared/workflow/external-dispatch-recipes.md` | none (0 hits) | **missing** | MEDIUM |
| 15 | `shared/definitions/agent-definitions.md` | none (only `subagent-definitions.md` appears) | **missing** | MEDIUM |
| 16 | `shared/definitions/subagent-definitions.md` | T037 (three-part obligation), T060 (default + exception), T099 (dispatch-capability section), T132 (concept owner) | covered by T037/T060/T099/T132 | — |
| 17 | `tests/contract/test_sdd_loop_driver_skill` | none (0 hits in plan or tasks) | **missing** | MEDIUM |
| 18 | `tests/contract/test_sdd_project_setup_skill` | none | **missing** | MEDIUM |
| 19 | `tests/contract/test_coaching_run_contract` | none | **missing** | MEDIUM |
| 20 | `tests/contract/test_sdd_carrier_contract` | none | **missing** | MEDIUM |

Counts: **5 covered / 15 missing** of 20 surfaces. Severities: **4 HIGH** (#7–#10: the in-process ban and the concurrency correction have no scheduled landing in either sdd-* skill — sdd-house-keeping and sdd-project-setup are untouched by the manifest's scope while their SKILL.md files remain unpinned by any contract test row), **11 MEDIUM** (#3, #5, #11–#15, #17–#20). Plan-side note: plan L195–224 planned-files list likewise omits #3, #5, #7–#15; only #1/#2/#4/#6/#16 appear (plan L198–201), so the gap is present in both artifacts, not only in tasks.md.

## Verdict

Gate lane is fully green (A). Directive lane: FR-034 PASS, SC-006 PASS, FR-035 PARTIAL (heterogeneous→subprocess clause absent). Manifest lane: 15 of 20 named surfaces carry no plan/tasks row, 4 of them HIGH (internal-subagent ban absent from sdd-house-keeping and sdd-project-setup).

V2: FAIL — 15/20 manifest surfaces missing (HIGH: sdd-house-keeping SKILL.md + maintenance-recipes.md, sdd-project-setup SKILL.md + setup-recipes.md; MEDIUM: watch-model.md, stage-prompts.md, coaching-skills SKILL.md, analyze-artifacts validation-and-report.md, execution-topology.md, external-dispatch-recipes.md, agent-definitions.md, test_sdd_loop_driver_skill, test_sdd_project_setup_skill, test_coaching_run_contract, test_sdd_carrier_contract); FR-035 heterogeneous→subprocess clause absent
