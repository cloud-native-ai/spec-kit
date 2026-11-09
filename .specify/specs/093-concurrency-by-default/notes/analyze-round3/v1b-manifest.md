# V1B — Complete-correction manifest verification (analyze round 3, 2026-11-09)

Worker: V1B (read-only fork verification). Worktree: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/093-clarify`, branch `093-concurrency-by-default`, HEAD `8c90088c`. No edits, no commits, no subagents; the only file written is this note.

## 1. Commit / carrier confirmation

`git show --stat 86b9e43c` — 30 files, matching the claim: `plan.md` (+53/−), `tasks.md` (T144–T152, counts 143→152), `requirements.md` (FR-035 rewrite + dated V3 correction), `contracts/high-order-executors.contract.md` (C-094), `notes/analyze-repair2.md`, `notes/analyze-round2/*` evidence additions, `register.md`, checklists, six checkpoints, `quickstart.md`, `research.md`, `test-evidence/analyze-repair2-*`. `8c5198d7` is the spine record only (`.specify/state/093-concurrency-by-default.md`). No gate script, threshold or contract test was edited in either commit — no gate weakening by edit.

Task count 143 → 152 is the only count movement; FR count stays 35 (FR-035 rewritten in place, numbering preserved).

## 2. Per-surface audit (20 surfaces from `notes/analyze-round2/v2-gates-directive.md` § C)

Judgment rule applied (as chartered and as V2 stated it): a surface is `covered` only when a plan/tasks row names the exact surface path and its wording requires the FORK carrier (`qodercli` child processes via `scripts/stage-runner.sh`) **and** bans/rejects the host-internal in-process subagent path. The 15 newly-added surfaces are judged on T144–T152; the 5 "already scheduled" surfaces on their named pre-existing rows plus the plan manifest row.

| # | Surface | Row(s) | Exact file named | Fork carrier required | In-process path banned | Status |
|---|---|---|---|---|---|---|
| 1 | `skills/external/sdd-loop-driver/SKILL.md` | T139, T142 | yes ("the matching statements in `SKILL.md`") | yes (T142: fork model, stdin prompt, stream-json, sentinel) | yes (T142: "host-in-process fan-out not counted as concurrency", FR-035) | covered |
| 2 | `.../references/dispatch-recipes.md` | T139, T142 | yes (§ 本地原生拓扑, § Recipe 2) | yes (T142) | yes (T142) | covered |
| 3 | `.../references/watch-model.md` | T146 | yes (~L7) | yes | yes ("BANNED as a carrier") | covered |
| 4 | `.../references/decomposition-model.md` | T140 (also T060/T132 named) | yes | **no** — T140 targets § 20.1 (analyze `off`→N); the dispatch declaration at § 13.4 L184 ("Local: one native host subagent per package … No external CLI is launched locally") has no row | **no** | **wrong-target (MEDIUM)** |
| 5 | `.../references/stage-prompts.md` | T146 | yes (~L27) | yes (fork same-family) | yes ("with the ban stated") | covered |
| 6 | `.../templates/stage-team-preset.md` | T116, T133 | plan list yes; tasks rows say "the stage-team preset" only | **no** — T116 carries the team obligation + slot-cap line; T133 the slot sentence; L74 "a native subagent locally, one detached runner remotely" is not scheduled | **no** | **missing (MEDIUM)** |
| 7 | `skills/external/sdd-house-keeping/SKILL.md` | T144 | yes (L109/L140/L144) | yes (fork default; subprocess for heterogeneous) | yes (BANNED, "MUST NOT be presented as an option") | covered — explicit inversion ("dispose the old 'MUST NOT 启动 qodercli' rule in FR-033's list") |
| 8 | `skills/external/sdd-house-keeping/references/maintenance-recipes.md` | T144 | yes (H2 Carrier line ~L35) | yes | yes | covered — the old local-native carrier line is rewritten to the two carriers |
| 9 | `skills/external/sdd-project-setup/SKILL.md` | T145 + plan row 9 | yes (L57/L59/L73/L104) | yes (fork is the local default) | yes (BANNED) | covered — inversion explicit across the pair (plan row 9: invert "MUST NOT 启动 qodercli"; T145: fork default + dispose in FR-033's list) |
| 10 | `skills/external/sdd-project-setup/references/setup-recipes.md` | T145 | yes (~L109) | yes | yes | covered — the old "MUST NOT 在本地启动 qodercli" carrier paragraph is inverted |
| 11 | `skills/external/coaching-skills/SKILL.md` | T147 | yes (~L276) | yes | yes (BANNED) | covered |
| 12 | `skills/internal/analyze-artifacts/references/validation-and-report.md` | T148 | yes (~L36) | yes (both carriers) | yes ("MUST NOT be used as a carrier") | covered |
| 13 | `shared/workflow/execution-topology.md` | T149 | yes (~L33) | yes | yes (BANNED) | covered |
| 14 | `shared/workflow/external-dispatch-recipes.md` | T150 | yes (~L18, Recipe 7 ~L91) | yes | yes (BANNED) | covered |
| 15 | `shared/definitions/agent-definitions.md` | T151 | yes | yes (fork or subprocess, named per dispatch) | yes ("MUST NOT be a carrier") | covered |
| 16 | `shared/definitions/subagent-definitions.md` | T037, T060, T099, T132 | yes | **no** | **no** — no row requires the ban; the source still reads "Native is the default whenever the executing runtime supports it", "Parallel fan-out … (or native parallel calls when the runtime supports them …)" and "native first" | **missing (MEDIUM)** |
| 17 | `tests/contract/test_sdd_loop_driver_skill.py` | T152 | yes | yes | yes ("every assertion pinning 'MUST NOT launch qodercli locally' / 'host-native first' is replaced by the in-process ban plus the fork and subprocess carriers") | covered |
| 18 | `tests/contract/test_sdd_project_setup_skill.py` | T152 | yes | yes | yes (same row) | covered |
| 19 | `tests/contract/test_coaching_run_contract.py` | T152 | yes | yes | yes (same row) | covered |
| 20 | `tests/contract/test_sdd_carrier_contract.py` | T152 | yes | yes | yes (same row) | covered |

Counts under the stated rule: **17 covered / 2 missing / 1 wrong-target**. All 15 newly-added surfaces (#3, #5, #7–#15, #17–#20) pass. The three failures are among the five "already scheduled" surfaces the repair kept unchanged.

Evidence for the three failures (measured, not inferred):
- #4: `skills/external/sdd-loop-driver/references/decomposition-model.md` § 13.4 (L184) — "Local: one native host subagent per package through the existing `run-agent` dispatch path. No external CLI is launched locally…". FR-035 (§ conflicts, `requirements.md` L194) itself names this file as a conflict that "MUST 由实现期一次显式修订收敛"; no row (T140, T060, T132, or T118) names § 13.4 or SD-07/SD-08/SD-15. T140's own scope is § 20.1 (`analyze` default `off`→N).
- #6: `skills/external/sdd-loop-driver/templates/stage-team-preset.md` L74 — "`stage-worker` is filled by one execution per Work Package (**a native subagent locally, one detached runner remotely**)". T116/T133 do not touch this line.
- #16: `shared/definitions/subagent-definitions.md` § Three Execution Modes / Mode Selection — "Native is the default…", "Parallel fan-out … External (or native parallel calls…)", "When in doubt: native first…". T037/T060/T099/T132 carry the obligation/capability content but none states the ban.

## 3. Named checks

**Four HIGH surfaces — explicit inversion of the old rule: PASS.** T144 quotes and disposes the old rule for sdd-house-keeping SKILL.md and rewrites maintenance-recipes' H2 carrier line; T145 establishes the fork default + ban for sdd-project-setup SKILL.md / setup-recipes, with plan manifest row 9 spelling the inversion ("invert 'MUST NOT 启动 qodercli' (~L57/L59/L73/L104)"). The old text at all four surfaces was confirmed present on disk (house-keeping L109/L140; setup L57/L59/L73/L104; recipe carrier lines L35 and L109), so the rows target real, measured rule text.

**FR-035 — both clauses present, valid definition row: PASS.** `requirements.md` L194 now reads: independent-child-process form with exactly two legal carriers — (1) FORK form through `skills/external/sdd-loop-driver/scripts/stage-runner.sh`, (2) SUBPROCESS form for heterogeneous agents, "MUST NOT 因族差异回落到宿主内建扇出" — and the ban: "宿主内建 Agent 扇出（in-process subagent）路径 **BANNED**（…既不是缺省、也不是降级选项）… MUST NOT 以宿主内建 Agent 扇出作为并发机制". `validate-requirements.py` → `status: ok`, 47 definition rows, `0 error(s), 0 warning(s)`, EXIT 0; FR numbering unchanged (FR-001…FR-035). `contracts/high-order-executors.contract.md` C-094 matches the same two-carrier + ban shape.

**Four contract-test update rows: PASS.** T152 names all four modules and pins the assertion change. The current modules do hold the old-rule assertions to be replaced — `test_sdd_loop_driver_skill.py:570` ("原生子代理"), `test_coaching_run_contract.py:459` ("host-native subagent capability first"), `test_sdd_carrier_contract.py:94` ("MUST NOT launch \`qodercli\` locally") — so the row targets the right modules.

**No gate weakening: PASS.**
- `validate-tasks.py tasks.md` → `PASS: … — 0 error(s), 0 warning(s)`, EXIT 0.
- `validate-requirements.py requirements.md` → all six rules `pass (0)`, 337 lines / 47 definition rows, 0/0, EXIT 0.
- `decomposition-check.py --mode tasks …` → `{"decision": "proceed", "measured": {"fr_count": 35, "task_count": 152, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}`, EXIT 0.
- `pre-analyze-check.py --stage tasks` → `decision=pass errors=0 advisories=112 waived=0`, EXIT 0 (same advisory count the repair recorded).
- Package containment: parsed the `## Work Packages` table — WP1 16 + WP2 26 + WP3 24 + WP4 37 + WP5 49 = 152 tokens, 152 unique, 0 duplicates, 0 missing against T001–T152. T144–T151 sit inside the existing `WP3-owners`, T152 inside `WP4-tests`; all nine rows sit inside the existing Phase 8 heading. No new package was needed and none was declared.

## 4. Findings

| id | severity | surface | finding |
|----|----------|---------|---------|
| V1B-F1 | MEDIUM | #4 `decomposition-model.md` | wrong-target: the named row T140 corrects § 20.1 (analyze default), not the § 13.4 dispatch declaration the manifest claims to correct; the old local-native carrier line FR-035 names as a conflict has no correction row |
| V1B-F2 | MEDIUM | #6 `stage-team-preset.md` | missing: T116/T133 name the preset but carry no fork/subprocess carrier requirement and no in-process ban; L74's "a native subagent locally" is left unchanged |
| V1B-F3 | MEDIUM | #16 `subagent-definitions.md` | missing: T037/T060/T099/T132 carry no fork/subprocess carrier requirement and no ban; the "native first" / "native parallel calls" text directly contradicts FR-035 and survives all rows |

Note: V2's round-2 baseline had graded #4/#6/#16 "covered" ("already scheduled"); this re-measure applies V2's own stated judgment rule ("carries the correction content") to today's text and the three named rows do not carry it. The repair ledger's residual-risk paragraph ("The 15 surfaces … still read 'MUST NOT start qodercli locally' / 'host-native first'") likewise under-counts: these three baseline surfaces also still read the old rule and no row inverts them.

## 5. Verdict

**V1B: FAIL — 3 MEDIUM manifest gaps: #4 decomposition-model.md (row targets § 20.1, not the § 13.4 carrier declaration), #6 stage-team-preset.md (no fork/ban row for L74 native-local carrier), #16 subagent-definitions.md (no ban row; "native first" text unscheduled).** All 15 newly-added surfaces, the four HIGH explicit-inversion rows, FR-035's two clauses, the four contract-test re-pins, the gates (validate-tasks 0/0, validate-requirements 0/0, decomposition 152/160 proceed, pre-analyze pass) and the package sums are green.
