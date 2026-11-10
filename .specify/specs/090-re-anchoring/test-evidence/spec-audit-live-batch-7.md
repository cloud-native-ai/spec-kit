# Read-only live-spec audit — batch 7 (7 specs)

**Audit date**: 2026-11-10 · **Tree**: main worktree `/storage/project/cloud-native-ai/spec-kit` (master) · **Mode**: read-only (no spec/source edits, no subagents, no commits).

**Scanned artifacts per spec**: `requirements.md`, `plan.md`, `tasks.md` (+ `tasks-081a/b/c.md`), `contracts/**`, `data-model.md`, `quickstart.md`, `verification.md`, `notes/**`. Extraction = unique path tokens with a leading `(^|[^A-Za-z0-9._/-])` boundary, prefixes `.specify/ scripts/ skills/ templates/ shared/ tests/`, first occurrence kept.

**Classification**
- **alive** — literal path exists now; a bare `scripts|skills|templates|shared|tests/…` token also counts alive when its `.specify/` mirror exists; pattern tokens count alive when their static prefix directory exists.
- **archived** — target exists under `.specify/archive/` (spec dirs under `archive/spec{,s}/`, goal/team trees under `archive/goal-team/trees/`).
- **moved** — the anchor-layout rename (merge commit `6fb8093c4`, landed on master during this audit) relocated the target: `.specify/memory/{constitution,glossary,register,tools}.md` → `.specify/*.md`, `.specify/memory/features.md` → `.specify/features.md`, `.specify/memory/features/<N>.md` → `.specify/features/<N>-<slug>.md`, `.specify/goal/…` → `.specify/anchoring/…`. Target verified to exist; **not** counted as dead.
- **dead** — no target anywhere (a pointer at a pre-consolidation path counts dead; dead patterns included).

## Batch summary

| spec | refs | alive | archived | dead | verdict |
|------|------|-------|----------|------|---------|
| 018-cli-priority-support | 43 | 29 | 0 | 11 | **BROKEN** |
| 033-docs-command | 49 | 42 | 0 | 5 | **BROKEN** |
| 045-sanitize-command | 73 | 60 | 0 | 12 | **BROKEN** |
| 059-exec-quant-recording | 54 | 48 | 0 | 3 | **INTACT** |
| 071-review-code-integration | 112 | 101 | 1 | 6 | **INTACT** |
| 081-acceptance-hardening | 208 | 189 | 0 | 13 | **BROKEN** |
| 094-goal-team-parallel | 292 | 227 | 25 | 31 | **BROKEN** |

`moved` (not in the six columns above): 018=3, 033=2, 045=1, 059=3, 071=4, 081=6, 094=9 — all verified to resolve at the post-rename path.

---

## 018-cli-priority-support

**Counts**: refs 43 · alive 29 (28 literal + 1 pattern) · archived 0 · dead 11 · moved 3.

**Registry**: row 018 exists with Feature Details `.specify/features/018-cli-priority-support.md` (file exists; content is Feature Detail "Configuration Management"), but **Spec Path is `-` and no registry row points to `018-cli-priority-support`** → the row for this spec does not resolve. (Pre-rename it pointed to `.specify/memory/features/018.md`, same mismatch.)

**Guards**: 13 named guard tests alive (4 contract, 4 integration, 5 unit). Missing named guards (9 path-named + 1 prose-only):

- `.specify/specs/018-cli-priority-support/tasks.md:98` → `tests/integration/test_codex_init.py` — missing (nearest live: `tests/contract/test_codex_init_contract.py`).
- `.specify/specs/018-cli-priority-support/tasks.md:127` → `tests/contract/test_tier_ordering_contract.py` — missing.
- `.specify/specs/018-cli-priority-support/tasks.md:129` → `tests/integration/test_tier_menu_ordering.py` — missing.
- `.specify/specs/018-cli-priority-support/tasks.md:160` → `tests/unit/test_command_template_variants.py` — missing.
- `.specify/specs/018-cli-priority-support/tasks.md:162` → `tests/integration/test_deep_adaptation_multi_tool.py` — missing.
- `.specify/specs/018-cli-priority-support/tasks.md:163` → `tests/integration/test_instructions_sync.py` — missing.
- `.specify/specs/018-cli-priority-support/tasks.md:188` → `tests/integration/test_ai_tools_command_coverage.py` — missing.
- `.specify/specs/018-cli-priority-support/tasks.md:192` → `tests/contract/test_ai_tools_support_contract.py` — missing.
- `.specify/specs/018-cli-priority-support/tasks.md:193` → `tests/contract/test_ai_tools_support_surfaces.py` — missing.
- `.specify/specs/018-cli-priority-support/plan.md:96` → `test_codex_support_surfaces.py` — missing (only the `_contract` variant exists).

**Broken list (dead)**

- `.specify/specs/018-cli-priority-support/plan.md:86` → `scripts/bash/update-agent-context.sh` — file does not exist (no archived copy; `scripts/bash/` now holds check-prerequisites/collect-history/generate-instructions etc.).
- `.specify/specs/018-cli-priority-support/tasks.md:171` → `.specify/scripts/bash/update-agent-context.sh` — same missing file.
- The nine missing test paths above (tasks.md:98,127,129,160,162,163,188,192,193) → no target; nothing under `.specify/archive/`.

**Moved (anchor rename; target exists)**: `quickstart.md:61` `.specify/memory/constitution.md`; `plan.md:92` `.specify/memory/features/022.md`; `plan.md:93` `.specify/memory/features.md`.

**Spot-checks (3)**

1. File/symbol: `src/specify_cli/__init__.py:64` `AGENT_CONFIG` — present.
2. Symbol: `src/specify_cli/__init__.py:1020` `_ASSISTANT_TIERS` — present (consumed at :1356/:1359 tier1/tier2 partitioning).
3. Behaviour surface: `src/specify_cli/__init__.py:1342` `audit_capability_matrix()` — present.

**Verdict: BROKEN** — 9 missing guard tests + removed `update-agent-context.sh` script (2 refs) + registry row with no Spec Path / no binding to this spec dir.

---

## 033-docs-command

**Counts**: refs 49 · alive 42 (37 literal + 5 patterns) · archived 0 · dead 5 · moved 2.

**Registry**: row for this spec = **037** (`Spec Path: .specify/specs/033-docs-command/requirements.md`, exists). Feature Details cell = `.specify/features/037-goal-registry.md`, file exists, content = Feature Detail "Docs Command" — cell resolves, but the **filename slug (`goal-registry`) does not match its content** (rename paired detail N with spec-dir N's slug). Row 033 (Agent Project Context Parameterization) is a different Draft feature, Spec Path `-`.

**Guards**: all 7 named tests alive — `tests/contract/test_docs_command_template.py`, `test_docs_step_injection.py`, `test_docs_utils_cli.py`, `test_feedback_command_classification.py`, `test_shared_reference_rewrite.py`, `tests/integration/test_docs_command_scenarios.py`, `test_docs_notes_lifecycle.py`; fixture `tests/fixtures/docs_command/` present. (Prose-named `test_ai_tools_command_coverage.py` is missing, already absent when the plan was written.)

**Broken list (dead)**

- `.specify/specs/033-docs-command/quickstart.md:23` → `.specify/scripts/python/docs-utils.py` — moved to the skill: `.specify/skills/create-docs/scripts/docs-utils.py` (source `skills/external/create-docs/scripts/docs-utils.py`); six quickstart command lines (:23,26,29,30,33,36,45) point at the pre-consolidation path.
- `.specify/specs/033-docs-command/quickstart.md:11` → `.specify/docs/audit/` — no such tree; the live create-docs contract puts run artifacts under `docs/.speckit/` (`SKILL_WORKDIR/docs/.speckit/`), which is itself not materialized in this repo.
- `.specify/specs/033-docs-command/contracts/docs-command-template.md:16` → `.specify/docs/plans/` — same migration (dead).
- `.specify/specs/033-docs-command/contracts/docs-command-template.md:16` → `.specify/docs/target-structure.md` — same migration; live location is `docs/.speckit/target-structure.md` (dead).
- `.specify/specs/033-docs-command/verification.md:45` → `.specify/docs/audit/20260728T082822Z-docs-audit.md` — claimed produced audit record absent.

**Moved (anchor rename; target exists)**: `plan.md:31` `.specify/memory/constitution.md`; `tasks.md:5` `.specify/memory/features.md`.

**Spot-checks (3)**

1. File: `templates/commands/docs.md` — present; headings are `## User Input / ## Glossary / ## Outline / ## Wrap-up / ## Handoffs`. Contract C-3 (`contracts/docs-command-template.md`) still requires `## Feedback` + `## Documentation` headings — the live template compiles both into `## Wrap-up` (contract-vs-template drift, no path break).
2. Mirror: `.specify/skills/create-docs/SKILL.md` is byte-identical to `skills/external/create-docs/SKILL.md` (cmp clean) — C-12 holds.
3. Command: `scripts/python/regen-command-copies.py --check` exists (:103, :125); `docs-utils.py --action` choices include `scan/expire/clean/archive-check/stats/validate` (:835).

**Verdict: BROKEN** — relocated `docs-utils.py` command path + four stale `.specify/docs/` contract/runtime paths (now `docs/.speckit/`) + missing audit evidence file.

---

## 045-sanitize-command

**Counts**: refs 73 · alive 60 (52 literal + 8 patterns) · archived 0 · dead 12 (11 literal + 1 pattern) · moved 1.

**Registry**: row for this spec = **047** (`Spec Path: .specify/specs/045-sanitize-command/requirements.md`, exists). Details = `.specify/features/047-feedback-introspection.md`, file exists, content = Feature Detail "Framework Material Hygiene" — filename slug/content mismatch (same rename artifact). Separate observation: row **045** is "Framework Source Provenance" and its Spec Path points at `.specify/specs/043-init-commit-stamp/requirements.md` (exists, correct subject) — feature-number/spec-number divergence is pre-existing.

**Guards**: 11 named sanitize tests alive (`tests/contract/test_sanitize_engine_contract.py`, `test_sanitize_template.py`, `tests/unit/test_sanitize_checks_{index,migration,mirror,refs}.py`, `test_sanitize_semantic.py`, `test_sanitize_store.py`, `tests/integration/test_sanitize_us{1,2,3}.py`). Missing: `tests/unit/test_sanitize_engine.py` (plan.md:89) — the engine suite lives at `tests/contract/test_sanitize_engine_contract.py`.

**Broken list (dead)**

- `.specify/specs/045-sanitize-command/plan.md:89` → `tests/unit/test_sanitize_engine.py` — missing; coverage exists as `tests/contract/test_sanitize_engine_contract.py`.
- `.specify/specs/045-sanitize-command/quickstart.md:51` → `tests/fixtures/sanitize/sample` — missing; fixtures are `tests/fixtures/sanitize/{correctness,stale-todo}` (the walk-through command would fail).
- `.specify/specs/045-sanitize-command/quickstart.md:7` → `.specify/memory/todo/20260812-evidence-session-backlog.md` — absent (only `20261030-suite-speed-optimizations.md`).
- `.specify/specs/045-sanitize-command/plan.md:9,40,90` and `quickstart.md:34` → `.specify/memory/sanitize/findings.json`, `.specify/memory/sanitize/cleanup-plan.json`, `.specify/memory/sanitize/` — store not materialized (engine default `STORE_REL = .specify/memory/sanitize/findings.json`, sanitize-utils.py:49; created on first run).
- `.specify/specs/045-sanitize-command/data-model.md:92` → `.specify/memory/draft/` — absent (declared candidate scan path; sanitize treats it as empty).
- `.specify/specs/045-sanitize-command/contracts/sanitize-detection-rules.md:46` → `.specify/tools` — intentionally absent legacy-residue detection target (C-22; live records are `.specify/memory/tools/`).
- `.specify/specs/045-sanitize-command/contracts/sanitize-detection-rules.md:36` → `templates/instances/execution` — prose fragment; `.specify/agents/templates/instances/execution` also absent in this tree.
- `.specify/specs/045-sanitize-command/quickstart.md:40` → `.specify/memory/todo/20260812-...md`; `contracts/sanitize-engine.md:24` → `.specify/memory/todo/xxx.md` — illustrative placeholders.
- `.specify/specs/045-sanitize-command/plan.md:58` → `.specify/archive/memory/<原相对路径>` — future archive root; `.specify/archive/memory/` does not exist (dead pattern).

**Moved (anchor rename; target exists)**: `plan.md:27` `.specify/memory/constitution.md`.

**Spot-checks (3)**

1. Mirror: `scripts/python/sanitize-utils.py` ↔ `.specify/scripts/python/sanitize-utils.py` byte-identical (C-13 holds).
2. Symbol: `src/specify_cli/__init__.py:868/912/935/944` `_OBSOLETE_SKILLS / _OBSOLETE_SKILL_FILES / _OBSOLETE_COMMANDS / _OBSOLETE_TEMPLATES` — present (C-12 registry source).
3. Command surface: `scripts/python/sanitize-utils.py:1053` `--action` = `collect/record/status/apply`; `templates/commands/sanitize.md` present.

**Verdict: BROKEN** — renamed/lost guard-test name, missing fixture `tests/fixtures/sanitize/sample`, unmaterialized sanitize store and stale quickstart todo example.

---

## 059-exec-quant-recording

**Counts**: refs 54 · alive 48 (45 literal + 3 patterns) · archived 0 · dead 3 (2 literal + 1 pattern) · moved 3.

**Registry**: row 059 resolves — Details `.specify/features/059-exec-quant-recording.md` exists (content matches), Spec Path `.specify/specs/059-exec-quant-recording/requirements.md` exists.

**Guards**: all named tests alive — `tests/contract/test_exec_quant_engine.py` (50 tests), `test_probe_engine_action_sets.py`, `test_compile_propagation_order.py`, `test_wrap_up_line_budget.py`; integration feedback suite glob `tests/integration/test_feedback_*.py` resolves.

**Dead (all runtime-by-design, not link rot)**

- `.specify/specs/059-exec-quant-recording/notes/quickstart-run.md:85` → `.specify/memory/feedback/packages/feedback-20261016T053231Z.zip` — removed after verification (documented in verification.md:43).
- `.specify/specs/059-exec-quant-recording/notes/quickstart-run.md:80` → `.specify/memory/feedback/packages/feedback-<ts>.zip` — pattern; dir created on demand by `feedback-utils.py:2069-2070` (`mkdir(parents=True)`).
- `.specify/specs/059-exec-quant-recording/verification.md:43` → `.specify/memory/feedback/packages` — absent now, recreated by `--action package`.

**Moved (anchor rename; target exists)**: `plan.md:27` `.specify/memory/constitution.md`; `tasks.md:5` `.specify/memory/features.md` and `.specify/memory/features/059.md`.

**Spot-checks (3)**

1. Mirror: `scripts/python/exec-quant.py` ↔ `.specify/scripts/python/exec-quant.py` byte-identical.
2. Storage surface: `.specify/memory/exec-quant/records.jsonl` exists; first record carries `kind: speckit.exec-quant`, `agent.{name,version,binary}` with `provenance: measured`.
3. Command surface: engine `--action` choices include `collect/list-records/score` (exec-quant.py:1442); record schema fields match the design.

**Verdict: INTACT** — every static reference resolves; the three dead entries are removed/on-demand packaging outputs explicitly documented as such.

---

## 071-review-code-integration

**Counts**: refs 112 · alive 101 (90 literal + 11 patterns) · archived 1 · dead 6 · moved 4.

**Registry**: row 071 resolves — Details `.specify/features/071-review-code-integration.md` exists (content matches), Spec Path `.specify/specs/071-review-code-integration/requirements.md` exists.

**Guards**: all named tests alive (16 modules incl. `test_review_code_composition.py`, `test_status_gate_owner.py`, `test_coverage_receipt.py`, `test_code_review_skill_contract.py`, `test_review_feedback_boundary.py`, `test_review_docs_isomorphism.py`, `test_review_p1_review_loop.py`, `test_expression_compatibility.py`, `test_scripts_distribution_parity.py`, `test_compile_embeds.py`, `test_loop_state_engine.py`). Fixture `tests/fixtures/review_git_repo.py` present.

**Archived (resolves)**: `notes/red-first-evidence.md:759` → `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` exists under `.specify/archive/specs/069a-flow-classification-docs-gates/notes/`.

**Dead (runtime/temp/disposable by documented design)**

- `.specify/specs/071-review-code-integration/plan.md:102` → `scripts/git-delta-review.sh` — tree-relative entry under `skills/internal/code-review/`; actual file alive at `skills/internal/code-review/scripts/git-delta-review.sh`.
- `.specify/specs/071-review-code-integration/notes/red-first-evidence.md:326` → `.specify/specs/071-fixture-demo` — disposable fixture repository used by quickstart scenario D.
- `.specify/specs/071-review-code-integration/notes/red-first-evidence.md:850` → `.specify/teams/.work` — git-ignored working snapshot (`.specify/.gitignore`), documented as such.
- `.specify/specs/071-review-code-integration/notes/quickstart-run.md:178,250` → `.specify/.tmp/quickstart-071[/missing.md]` — sanctioned scratch, teardown documented in the same note.
- `.specify/specs/071-review-code-integration/notes/quickstart-run.md:223` → `.specify/specs/071-review-code-integration/code-review-20261027T084638Z.md` — rotated record, explicitly removed ("no `code-review*.md` remains after teardown").

**Moved (anchor rename; target exists)**: `plan.md:37` `.specify/memory/constitution.md`; `tasks.md:26` `.specify/memory/features/071.md`; `tasks.md:174` `.specify/memory/features.md`; `notes/quickstart-run.md:157` `.specify/goal/command-logic-as-classified-skills/summary/assets/wbs.png` → exists at `.specify/anchoring/command-logic-as-classified-skills/summary/assets/wbs.png`.

**Spot-checks (3)**

1. File: `templates/commands/review.md:75` — Segment 4 (`code-review`), deterministic `base..head` resolution delegated to `git-delta-review.sh`.
2. Command: `skills/internal/code-review/scripts/git-delta-review.sh` — `base/start/receipt` subcommands and `--since/--head/--renderer` present (help block :61–:83).
3. Behaviour surface: gate owner row = `templates/feature-details-template.md:63` § Canonical Status State Machine; blocking existence test at :100–:101; pinned by `tests/contract/test_status_gate_owner.py` (exists).

**Verdict: INTACT** — every non-runtime reference resolves; the six dead entries are fixture/scratch/rotated artifacts that the spec itself documents as removed.

---

## 081-acceptance-hardening

**Counts**: refs 208 · alive 189 (160 literal + 29 patterns) · archived 0 · dead 13 (11 literal + 2 patterns) · moved 6.

**Registry**: row 081 resolves — Details `.specify/features/081-acceptance-hardening.md` exists (content matches), Spec Path `.specify/specs/081-acceptance-hardening/requirements.md` exists.

**Guards**: all named tests alive (23 contract modules incl. `test_closure_acceptance_check.py`, `test_acceptance_state_machine.py`, `test_acceptance_premises.py`, `test_acceptance_review_composition.py`, `test_gate_wiring_081.py`, `test_line_state_blocked.py`, `test_premise_carrier_contract.py`, `test_requirements_checker.py`, `test_review_feedback_boundary.py`, `test_status_gate_owner.py`) and `tests/integration/test_acceptance_smoke.py`; all fixture cases under `tests/fixtures/acceptance-hardening/` resolve.

**Broken list (dead)**

- `.specify/specs/081-acceptance-hardening/tasks-081c.md:124` → `skills/internal/review-sdd-process/references` — **genuine dead**: the skill directory contains only `SKILL.md`.
- `.specify/specs/081-acceptance-hardening/data-model.md:148` → `.specify/memory/features/<ID>.md` — pre-rename anchor pattern; post-rename convention is `.specify/features/<ID>-<slug>.md` (dead pattern).
- `.specify/specs/081-acceptance-hardening/tasks.md:49` → `.specify/memory/features/*.md` — same pre-rename pattern (dead pattern).
- `.specify/specs/081-acceptance-hardening/tasks-081a.md:127` → `.specify/.tmp/081a-head-failed.txt`; `notes/red-first-evidence.md:183,199` → `.specify/.tmp/081a-head-failed-clean.txt`, `…-final.txt` — sanctioned scratch, gone.
- `.specify/specs/081-acceptance-hardening/tasks-081b.md:126` → `.specify/.tmp/081b-closure-verdict.json`; `tasks-081c.md:140` → `.specify/.tmp/081c-closure-verdict.json`; `verification.md:77` → `.specify/.tmp/081d-closure-verdict.json` — scratch, gone.
- `.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081b.md:134,135` → `.specify/.tmp/probe-specA`, `probe-specB`; `notes/red-first-evidence-081d.md:20` → `.specify/.tmp/081d-t001-probe` — scratch, gone.
- `.specify/specs/081-acceptance-hardening/notes/red-first-evidence.md:162` → `skills/external/coaching-skills/references/prompt-templates.md->.specify/skills/coaching-skills/references/prompt-templates.md` — diff-notation artifact; both real paths exist.

**Moved (anchor rename; target exists)**: `plan.md:35` `.specify/memory/constitution.md`; `plan.md:231` `.specify/memory/features`; `plan.md:242` `.specify/memory/features/071.md`; `plan.md:243` `.specify/memory/features/077.md`; `quickstart.md:137` `.specify/memory/features.md`; `verification.md:81` `.specify/memory/features/081.md`.

**Spot-checks (3)**

1. Mirror + contract: `scripts/python/closure-acceptance-check.py` ↔ `.specify/scripts/python/` byte-identical; exit codes `0=accept, 1=block, 2=input missing` (:41).
2. Owner doc: `shared/workflow/acceptance-hardening.md:176` § Closure Verdict present.
3. Behaviour surface: `templates/commands/review.md:85` § The Acceptance Reality Check (not a fifth segment, no model judgement); `templates/feature-details-template.md:100-101` states the blocking existence test.

**Verdict: BROKEN** — one genuine dead directory (`skills/internal/review-sdd-process/references`), two pre-rename anchor patterns, and nine scratch references that are gone by design.

---

## 094-goal-team-parallel

**Counts**: refs 292 · alive 227 (173 literal + 54 patterns) · archived 25 · dead 31 (19 literal + 12 patterns) · moved 9.

**Registry**: row 094 resolves — Details `.specify/features/094-goal-team-parallel.md` exists (content matches), Spec Path `.specify/specs/094-goal-team-parallel/requirements.md` exists.

**Guards**: `tests/contract/test_archive_migration.py` and `test_migration_interruption.py` exist (plan S2). Missing:

- `.specify/specs/094-goal-team-parallel/plan.md:354` → `test_residual_probe.py` — missing (S2 names it; no equivalent module found).
- `.specify/specs/094-goal-team-parallel/contracts/owner-rewrites-and-tests.md:128` → `tests/contract/test_command_run_goal_team.py` — missing; **disclosed** in tasks.md:180-181 (T016/T017 "CLOSED BY DELEGATION under ruling R2 … never authored").

**Archived (resolves)**: 23 refs to 085–094 goal/team trees (e.g. `notes/pre-change-measurements.md:28-49`) resolve under `.specify/archive/goal-team/trees/<dir>/{goal,teams}/…`; `notes/review-implementation-code.md:90` → `069b-isomorphism-migration-metrics` tree and `notes/analyze-round3/w3-trunk-reconciliation.md:170,266` → `092-non-disposable` resolve under `.specify/archive/specs/`. Two old spec-local `team` dirs (`091-auto-git-closeout/team`, `085-sdd-temporary-goal-team/team`) are archived in substance under the `teams/` subtree (plural) — count above includes them.

**Broken list (dead)**

- `.specify/specs/094-goal-team-parallel/plan.md:248` → `.specify/templates/commands` — no such directory in this tree (command templates live at `templates/commands/`).
- `.specify/specs/094-goal-team-parallel/notes/red-first-evidence.md:6` → `shared/workflows/feedback-step.md` — typo; actual owner is `shared/workflow/feedback-step.md` (singular).
- `.specify/specs/094-goal-team-parallel/notes/review-implementation-code.md:92` → `.specify/teams/team.md` — old global team file; post-094 model is `.specify/teams/<slug>/team.md`.
- `.specify/specs/094-goal-team-parallel/notes/review-implementation-code.md:82` → `scripts/territory-check.py` — tree-relative under `skills/internal/create-team/`; actual file alive at `skills/internal/create-team/scripts/territory-check.py`.
- `.specify/specs/094-goal-team-parallel/requirements.md:10` → `.specify/specs/091-auto-git-closeout/team` — old spec-local team dir (archived in substance; path itself dead).
- `.specify/specs/094-goal-team-parallel/quickstart.md:49,59` → `test-evidence/residual-before.json`, `test-evidence/migration-applied.json` — runtime outputs absent from the 274-file evidence set.
- `.specify/specs/094-goal-team-parallel/quickstart.md:35,36` → `.specify/.tmp/s094/s1[/.specify/specs/900-fixture]`; `tasks.md:143` → `.specify/.tmp/s094/probe/.specify/specs/900-fixture`; `notes/analyze-round4/fix-w1.md:69` → `.specify/.tmp/s092/probe/.specify/specs/900-fixture`; `notes/analyze-round1-repair.md:11` → `.specify/.tmp/s092-repair/add_cites.py`; `notes/analyze-round3/repair-r2.md:69` → `.specify/.tmp/s092`; `verification.md:21` → `.specify/.tmp/sdd-loop/tmp/gate1-094-failed.txt`; `notes/repairwave.md:5` → `.specify/.tmp/sdd-loop/worktrees/094-repairwave` — sanctioned scratch, gone.
- `.specify/specs/094-goal-team-parallel/quickstart.md:42` → `.specify/anchoring/demo-command-goal/goal.md`; `quickstart.md:103` → `.specify/teams/demo-crew/team.md`; `notes/analyze-round4/fix-w2.md:21` → `.specify/goal/demo-command-goal/goal.md`; `notes/implement-wp06.md:17` → `.specify/specs/900-fixture/goal` — demo/fixture outputs never created in the real tree.
- dead patterns (12): `.specify/goal/**` (plan.md:11), `.specify/goal/*/goal.md` (notes/analyze-round2-findings.md:86), `.specify/goal/<slug>` / `<goal-slug>` / `<goal_slug>` forms (notes/implement-wp06.md:54, analyze-round4/fix-w1.md:18,19,63, analyze-round3/w3-trunk-reconciliation.md:215, closure-readings.md:92, implement-wp01.md:105), `.specify/specs/092-non-disposable/{data-model` (notes/review-implementation-code.md:90), `.specify/specs/092-non-disposable/*` and `.specify/specs/069b-isomorphism-migration-metrics/*` (notes/review-consolidated.md:37) — pre-rename `goal/` root and archived-spec globs.

**Moved (anchor rename; target exists)**: `plan.md:16` `.specify/goal`; `plan.md:59` `.specify/memory/constitution.md`; `plan.md:64` `.specify/memory/features.md` and `.specify/memory/features/094.md`; `requirements.md:262` `.specify/memory/features/092.md`; `notes/analyze-round3-findings.md:49` `.specify/memory/register.md`; `notes/review-implementation-code.md:90` `.specify/memory/features/090.md`; `notes/analyze-round3/w2-traceability.md:114` `.specify/memory/features/094-goal-team-parallel.md` (hybrid form) → `.specify/features/094-goal-team-parallel.md`; `notes/analyze-round4/vc-anchoring.md:110` `.specify/specs/092-goal-team-parallel` → renumbered `.specify/specs/094-goal-team-parallel`.

**Spot-checks (3)**

1. Command/behaviour: `scripts/python/goal-utils.py:82` `ARCHIVE_SCOPES = ("goal","teams","auto")`; `resolve_scope()` :153 owns the path rule; `probe-residual` / `migrate-archive` actions implemented (:2518-2520).
2. Files: `.specify/anchoring/094-goal-team-parallel/goal.md` and `.specify/teams/094-goal-team-parallel/team.md` exist with `binding:` blocks (owner/owner_id/origin).
3. Behaviour surface — **partial mismatch**: the live `team.md` still carries `scope: spec` (a value FR-025 declares out of domain) and its territory names `.specify/memory/features.md` / `.specify/memory/features/094.md` (post-rename dead). The engine's closed set is correct; the archived team record is legacy data needing a post-rename/scope sweep. `test_archive_migration.py` and `test_migration_interruption.py` exist; `test_residual_probe.py` does not.

**Verdict: BROKEN** — two missing guards (one disclosed), stale `.specify/templates/commands`, `shared/workflows/` typo, old global `.specify/teams/team.md`, and pre-rename `goal/` patterns; runtime/temp/demo refs account for the rest.

---

## Cross-batch notes

- **Anchor-rename casualties are systemic**: 28 refs across the batch point at pre-rename anchors (`.specify/memory/{constitution,features*}.md`, `.specify/goal/…`). They were alive before merge `6fb8093c4` and are dead-by-relocation now; all have verified post-rename targets and are reported under `moved`, not `dead`.
- **Registry details filenames post-rename are slug-mispaired for four rows**: `.specify/features/018-cli-priority-support.md` holds "Configuration Management", `033-docs-command.md` holds "Agent Project Context Parameterization", `037-goal-registry.md` holds "Docs Command", `045-sanitize-command.md` holds "Framework Source Provenance", `047-feedback-introspection.md` holds "Framework Material Hygiene". Cells resolve (files exist, contents match the row name) but the filename slug was taken from the same-numbered *spec dir*, not the feature. Row 018's Spec Path is `-`; no row points at `018-cli-priority-support`.
- **Batch-wide dead mix**: 81 dead refs = 9 truly missing static targets + named-guard drift (10 names in 018, 1 in 045, 2 in 094) + stale pre-consolidation paths (033 docs-utils / `.specify/docs/*`; 094 `.specify/templates/commands`) + runtime/scratch outputs documented as removed + pre-rename patterns.

Anomaly: the anchor-layout rename (`.specify/memory/` → `.specify/` root) landed on master mid-audit as merge `6fb8093c4`, so 28 references flipped from alive to dead-by-relocation during the run and the registry's per-feature detail filenames now pair feature ID N with spec-dir N's slug (five rows' slugs contradict their content); this is a live-transition artifact, not pre-existing rot.

SPEC-AUDIT-LIVE-7-DONE
