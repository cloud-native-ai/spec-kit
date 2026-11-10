# Read-only live-spec audit — batch 3 (7 specs)

- **Date**: 2026-11-10
- **Tree**: MAIN `/storage/project/cloud-native-ai/spec-kit` (branch `master`)
- **Mode**: read-only; no spec/source edits, no subagents, no commits. This file is the only write.
- **Specs**: 009-claude-code-support · 029-glossary-mechanism · 041-refactor-feedback-probe · 055-conflict-free-stores · 067-loop-efficiency-hardening · 077-doc-sdd-integration · 089-script-interface-contract

## State change during the audit

The anchor-layout rename landed on `master` mid-audit as merge `6fb8093c4` (`move the project anchors out of memory/`). Before it: `.specify/memory/{features.md,features/<NNN>.md,constitution.md,glossary.md,register.md}` resolved. After it: those paths are **dead**, and the same objects live at `.specify/{features.md,constitution.md,glossary.md,register.md}` and `.specify/features/<NNN>-<slug>.md`. The specs in this batch were **not** rewritten by the merge. All counts below are against the post-merge tree; anchor-class breakage is tagged `ANCHOR` and kept separate from content breakage. The registry itself was rewritten and its Feature Details cells now use the new layout.

- **Anchor-class dead refs introduced by the merge**: 114 occurrences across 26 unique paths in these seven specs (per spec: 009 ×12, 029 ×31, 041 ×1, 055 ×1, 067 ×3, 077 ×35, 089 ×31).
- **Registry slug observations**: the merge named feature-detail files from the *spec directory* number, not the feature identity. Content is correct in each case, but three names point at unrelated slugs: `021-agent-specific-config.md` (contains Claude Code Support), `028-sdd-workflow-refactor.md` (contains Feedback Mechanism), `031-task-complexity-rubric.md` (contains Glossary Mechanism).

## Method

- **Artifact scope**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `review.md`, `code-review.md`, `feature-ref.md`, plus `contracts/**`, `checklists/**`, `notes/**`, `checkpoints/**`. Recorded `test-evidence/**`, `verification-scratch/**`, `baseline-*.txt` and `*.jsonl` were excluded (dated recordings, not live pointers).
- **Classification**: **alive** = resolves literally (or via the `.specify/` projection for a bare `shared|scripts|skills|templates` token); **archived-elsewhere** = resolves under `.specify/archive/` with a parent-directory match; **dead** = no target. Per the audit rule, a pointer at a pre-consolidation path is dead.
- **Noise handling**: wildcard/placeholder tokens are excluded from `refs`; prose enumerations, `$TMP` fixtures, deliberately non-existent negative examples and ephemeral `.specify/.tmp/` scratch are annotated rather than treated as content breakage.
- **What moves**: `.specify/memory/features.md → .specify/features.md`; `.specify/memory/features/<NNN>.md → .specify/features/<NNN>-<slug>.md`; `.specify/memory/{constitution,glossary,register}.md → .specify/{constitution,glossary,register}.md`. Tool records under `.specify/memory/tools/` and `.specify/tools.md` do not move.

---

## 009-claude-code-support (Feature 021 · Claude Code Support)

**Counts**: refs 42 · alive 28 · archived 0 · dead 14 (10 content, 4 anchor)

**Registry**: row `021` → Feature Details `.specify/features/021-agent-specific-config.md` (exists; content title “Claude Code Support”, Feature ID 021); Spec Path `.specify/specs/009-claude-code-support/requirements.md` (exists). Resolves; filename slug is unrelated (see above). Requirements header says `Draft` while the registry says `Implemented`.

**Dead — content (10)**
- `tests/unit/test_claude_support_surfaces.py` — tasks.md:47 (T005 `[x]`; also :61 T008 `[x]`, :160 T047 `[x]`) → missing.
- `tests/unit/test_claude_support_matrix.py` — tasks.md:60 (T007 `[x]`) → missing.
- `tests/contract/test_claude_support_contract.py` — tasks.md:59 → missing.
- `tests/contract/test_claude_init_contract.py` — tasks.md:87 → missing.
- `tests/integration/test_claude_init.py` — tasks.md:88 → missing.
- `tests/contract/test_claude_refresh_contract.py` — tasks.md:124 → missing.
- `tests/unit/test_claude_refresh_helpers.py` — tasks.md:128 → missing.
- `tests/integration/test_claude_distribution.py` — tasks.md:159 → missing.
- `tests/unit/test_claude_distribution.py` — tasks.md:161 → missing.
- `tests/contract/test_claude_support_surfaces_contract.py` — tasks.md:158 → missing.

**Dead — anchor (4)**: `.specify/memory/constitution.md` ×6 (plan.md:99) → `.specify/constitution.md`; `.specify/memory/features.md` ×2 (plan.md:108) → `.specify/features.md`; `.specify/memory/features/020.md` (research.md:13) → `.specify/features/020-speckit-todo-command.md`; `.specify/memory/features/021.md` ×3 (tasks.md:37) → `.specify/features/021-agent-specific-config.md`.

**Guards**: 4 live Claude tests — `tests/integration/test_claude_refresh.py`, `tests/integration/test_claude_validation.py`, `tests/unit/test_claude_command_generation.py`, `tests/unit/test_claude_ignore_policy.py`. 10 of the 13 test files the spec names are missing (renamed/consolidated); 4 of those names sit on tasks already `[x]`.

**Spot-checks**
1. `src/specify_cli/__init__.py:65` contains `"claude"` in `AGENT_CONFIG` — **PASS**.
2. `.claude/commands/speckit.*.md` = 29 files; `CLAUDE.md -> .specify/instructions.md` symlink — **PASS**.
3. `tests/unit/test_claude_support_surfaces.py` claimed delivered (T005/T008/T047) — **FAIL** (missing).

**Verdict: BROKEN** — 10 dead test pointers (4 on completed tasks) plus 4 anchor-class refs.

---

## 029-glossary-mechanism (Feature 031 · Glossary Mechanism)

**Counts**: refs 32 · alive 28 · archived 0 · dead 4 (all anchor)

**Registry**: row `031` → Feature Details `.specify/features/031-task-complexity-rubric.md` (exists; content title “Glossary Mechanism”, Feature ID 031); Spec Path `.specify/specs/029-glossary-mechanism/requirements.md` (exists). Resolves; filename slug is unrelated. Requirements header says `Draft` while the registry says `Implemented`.

**Dead — content**: none.

**Dead — anchor (4)**: `.specify/memory/glossary.md` ×26 (contracts/glossary-file-format.md:3) → `.specify/glossary.md`; `.specify/memory/features.md` ×3 (requirements.md:13) → `.specify/features.md`; `.specify/memory/constitution.md` (plan.md:29) → `.specify/constitution.md`; `.specify/memory/features/031.md` (tasks.md:161) → `.specify/features/031-task-complexity-rubric.md`.

**Guards**: `tests/contract/test_glossary_mechanism.py` and `tests/unit/test_glossary_utils.py` both exist.

**Spot-checks**
1. `scripts/python/glossary-utils.py` exposes `detect-conflict` and `add` (conflict-guarded) — **PASS**.
2. `templates/glossary-template.md` and `.specify/glossary.md` exist — **PASS**.
3. Instruction seeding wired: `scripts/bash/generate-instructions.sh:363-366` invokes `glossary-utils.py` non-destructively — **PASS**.

**Verdict: BROKEN (anchor-rename only)** — content and guards are intact; the 4 dead paths are the 114-occurrence layout class with known one-line targets.

---

## 041-refactor-feedback-probe (Feature 028 · Feedback Mechanism)

**Counts**: refs 37 · alive 33 · archived 0 · dead 4 (1 content, 1 anchor, 2 runtime-lazy)

**Registry**: row `028` → Feature Details `.specify/features/028-sdd-workflow-refactor.md` (exists; content title “Feedback Mechanism”, Feature ID 028); Spec Path `.specify/specs/027-feedback-mechanism/requirements.md` (exists). Resolves; filename slug is unrelated. The row points at the base feature spec, not this refactor spec.

**Dead — content (1 real)**
- `.specify/specs/041-refactor-feedback-probe/data-model.md:85` → `.specify/memory/feedback/index.json` — missing; the mirror index was retired by Feature 055 (per-entry `.md` + `state/` topology).
- Contract-surface drift: `contracts/engine-cli.md` C-3.1/C-3.2/C-3.3 (`probes`), C-6 (`probe-inject`), C-7.1 (`map`) name `scripts/python/feedback-utils.py` as the engine. Its current actions are `record/status/list/dispose/mark-submitted/reindex/package/cleanup/upstream/migrate-legacy/introspect-register/args-manifest/ingest-exec-quant/client-metrics`; the probe actions moved to `scripts/python/probe-utils.py:1427` (Feature 056).

**Dead — runtime-lazy (2, not breakage)**: `.specify/memory/feedback/probes/` (plan.md:81) and the `ext-myteam-…` example (quickstart.md:55). `probe-utils.py` creates `feedback_dir/probes` on demand; absence in this repo means no external probe registered.

**Dead — anchor (1)**: `.specify/memory/constitution.md` (plan.md:29) → `.specify/constitution.md`.

**Correction**: `skills/feedback.md` was a tokenization artifact of the live `docs/reference/skills/feedback.md` and is counted alive.

**Guards**: `tests/contract/test_feedback_probe_cli.py`, `test_feedback_probe_entry_schema.py`, `test_feedback_probe_registry.py`, plus the three other cited test names — all exist.

**Spot-checks**
1. `feedback-utils.py --action dispose` (C-2.5) — **PASS**.
2. Probe surface exists, relocated: `probe-utils.py --action probes|map|probe-inject` — **PASS** (moved, not lost).
3. `index.json` mirror claimed as engine-owned store — **FAIL** (retired by 055).

**Verdict: BROKEN** — one dead store pointer, one relocated engine surface, one anchor ref.

---

## 055-conflict-free-stores (Feature 055 · Conflict-Free Stores)

**Counts**: refs 5 · alive 3 · archived 0 · dead 2 (1 anchor, 1 by-design)

**Registry**: row `055` → Feature Details `.specify/features/055-conflict-free-stores.md` (exists); Spec Path `.specify/specs/055-conflict-free-stores/requirements.md` (exists). Resolves.

**Dead — content (by design)**: `.specify/specs/055-conflict-free-stores/requirements.md:6` → `.specify/memory/feedback/index.json` — absent; this is the Input quote naming the artifact the feature eliminates.

**Dead — anchor (1)**: `.specify/specs/055-conflict-free-stores/requirements.md:64` → `.specify/memory/features.md` — now `.specify/features.md`.

**Guards**: `tests/contract/test_store_state_protocol.py` exists (the cited two-branch merge protocol suite).

**Spot-checks**
1. `write_text_atomic` implemented at `scripts/python/feedback-utils.py:342` and `scripts/python/memory-utils.py:248` — **PASS**.
2. `.specify/memory/feedback/state/` materialized (`threshold.json`, `submitted-at.json`); no `index.json`; entries are per-file `.md` — **PASS**.
3. `tests/contract/test_store_state_protocol.py` present — **PASS**.

**Verdict: BROKEN (anchor-rename only)** — the content dead item is the feature’s declared target; the anchor ref has a known new path.

---

## 067-loop-efficiency-hardening (Feature 058 evolution · Loop Efficiency Hardening)

**Counts**: refs 56 · alive 52 · archived 0 · dead 4 (2 content, 2 anchor)

**Registry**: no row `067` and no `067` detail file — by design (requirements `Binding rationale`: evolution spec of Feature 058, no new Feature ID). Binds through row `058` → Feature Details `.specify/features/058-sdd-loop-driver.md` (exists) and Spec Path `.specify/specs/058-sdd-loop-driver/requirements.md` (exists). Resolves.

**Dead — content (2)**
- `checklists/test-slimming-2026-10-22.md:123` → `.specify/specs/063-sdd-loop-efficiency/contracts/test-budget.md` — missing; no `063-sdd-loop-efficiency` directory exists anywhere (live `.specify/specs/063-review-p1-governance` has no `test-budget.md` and no `TB-04`).
- `review.md:6` → `.specify/specs/063-sdd-loop-efficiency/review.md` — same missing spec tree.

**Dead — anchor (2)**: `.specify/memory/constitution.md` ×2 (notes/state-spine.md:20) → `.specify/constitution.md`; `.specify/memory/features/058.md` (verification.md:166) → `.specify/features/058-sdd-loop-driver.md`.

**Guards**: all 13 cited test names exist, including `tests/contract/test_run_tests_runner_contract.py`, `tests/contract/test_measurement_instruments.py`, `tests/contract/test_instructions_size_budget.py`, `tests/unit/test_loop_state_engine.py`.

**Spot-checks**
1. `scripts/bash/run-tests.sh` default is process parallelism (`-n <effective> --dist load`, documented at line 9) — **PASS**.
2. Runner-contract and measurement guard tests exist — **PASS**.
3. `063-sdd-loop-efficiency` TB-04 cross-reference — **FAIL** (no target).

**Verdict: BROKEN** — two cross-references to a deleted spec directory plus two anchor refs; its own implementation surfaces are intact.

---

## 077-doc-sdd-integration (Feature 077)

**Counts**: refs 233 · alive 216 · archived 0 · dead 17 (5 anchor, 3 genuine content, 9 by-design/scratch)

**Registry**: row `077` → Feature Details `.specify/features/077-doc-sdd-integration.md` (exists); Spec Path `.specify/specs/077-doc-sdd-integration/requirements.md` (exists). Resolves; status `Ready for Review` (requirements header still `Draft`).

**Dead — genuine content (3)**
- `plan.md:101` → `scripts/python/flow-class-spec-check.py` — missing; live checker is `scripts/python/flow-class-check.py`.
- `checklists/readiness-2026-10-30.md:200` → `.specify/memory/features/069a.md` — missing under both layouts; only `069` exists.
- `checklists/readiness-2026-10-30.md:200` → `.specify/memory/features/069b.md` — missing under both layouts.

**Dead — anchor (5 unique paths)**: constitution.md ×2 (plan.md:42) → `.specify/constitution.md`; features.md ×21 (readiness:209) → `.specify/features.md`; features/069.md (readiness:200) → `.specify/features/069-execution-expression-sdd.md`; features/077.md ×10 (readiness:211) → `.specify/features/077-doc-sdd-integration.md`; register.md (requirements.md:54) → `.specify/register.md`.

**Dead — by-design/scratch (9)**: `fx-declared` / `fx-absent` / `fx-bad` fixture trees and their `requirements.md` (temp fixtures under `$TMP`, quickstart.md:49-54), the deliberate `does-not-exist` negative example, `.specify/.tmp/sdd-loop/tmp/plan077` (run scratch), and `scripts/python/docs-structure-check.py` (the rejected alternative in plan T-003; the binding decision is `doc-consistency-check.py --action structure`).

**Guards**: `tests/contract/test_expression_gate_wiring.py` exists; all 15 cited test names exist.

**Spot-checks**
1. `shared/workflow/expression-gates.md` exists — **PASS**.
2. `scripts/python/doc-consistency-check.py` implements `--action structure` (`STRUCTURE_ACTION`, four faces) — **PASS**.
3. Stage-command wiring present in `templates/commands/{requirements,clarify,plan,tasks,analyze,checklist,implement,docs,humanize}.md` — **PASS**; the plan’s proposed `flow-class-spec-check.py` name is stale.

**Verdict: BROKEN** — three genuine dead pointers and five anchor-class paths; guards and implementation surfaces otherwise intact.

---

## 089-script-interface-contract (Feature 089)

**Counts**: refs 146 · alive 130 · archived 2 · dead 14 (9 anchor, 5 content)

**Registry**: row `089` → Feature Details `.specify/features/089-script-interface-contract.md` (exists); Spec Path `.specify/specs/089-script-interface-contract/requirements.md` (exists). Resolves.

**Dead — content (5)**
- `tasks.md:206` (T059 `[X]`) → `.specify/specs/089-script-interface-contract/test-evidence/T056-bash-backfill.txt` — missing; the directory holds `T058-skills-backfill.txt`, not this claimed backfill evidence.
- Scratch (not breakage): `.specify/.tmp/086-probe/` (plan.md:231), `.specify/.tmp/086-sandbox/` (tasks.md:102), `.specify/.tmp/sic.json` and `.specify/.tmp/sic-rule.json` (quickstart.md:72-73).

**Dead — anchor (9 unique paths)**: constitution.md ×16 → `.specify/constitution.md`; features.md ×5 → `.specify/features.md`; feature details 064/069/081/082/085/086/089 → `.specify/features/<NNN>-<slug>.md`.

**Archived-elsewhere (2)**: `.specify/specs/089-script-interface-contract/goal/script-interface-contract/goal.md` → `.specify/archive/goal-team/trees/089-script-interface-contract/goal/script-interface-contract/goal.md` (checkpoints/01:14); `.specify/specs/089-script-interface-contract/team/089-script-interface-contract/team.md` → `.specify/archive/goal-team/trees/089-script-interface-contract/teams/089-script-interface-contract/team.md` (checkpoints/03:21).

**Guards**: `tests/contract/test_script_interface_contract.py` exists; all 11 cited test names exist.

**Spot-checks**
1. `scripts/python/script-interface-check.py` and `scripts/python/script_interface_cli.py` exist — **PASS**.
2. Five landing points: `templates/constitution-template.md` principle `XX`, live `.specify/constitution.md` principle `XXI`, `skills/internal/manage-constitution/SKILL.md` `MUST include` list — **PASS**.
3. T059’s claimed backfill evidence file — **FAIL** (missing).

**Verdict: BROKEN** — one missing evidence pointer plus nine anchor-class paths; implementation surfaces and guards intact.

---

## Batch summary (post-rename tree)

| spec | refs | alive | archived | dead | verdict |
|------|------|-------|----------|------|---------|
| 009-claude-code-support | 42 | 28 | 0 | 14 | **BROKEN** |
| 029-glossary-mechanism | 32 | 28 | 0 | 4 | **BROKEN** (anchor only) |
| 041-refactor-feedback-probe | 37 | 33 | 0 | 4 | **BROKEN** |
| 055-conflict-free-stores | 5 | 3 | 0 | 2 | **BROKEN** (anchor only) |
| 067-loop-efficiency-hardening | 56 | 52 | 0 | 4 | **BROKEN** |
| 077-doc-sdd-integration | 233 | 216 | 0 | 17 | **BROKEN** |
| 089-script-interface-contract | 146 | 130 | 2 | 14 | **BROKEN** |
| **batch total** | **551** | **490** | **2** | **59** | 7 BROKEN (2 anchor-only) |

Dead composition: anchor-class 26 unique paths (114 occurrences, all seven specs) · content 10 in 009 · 1 in 041 · 2 in 067 · 3 in 077 · 1 in 089 · by-design/scratch counts 055 ×1, 077 ×9, 089 ×4. Prose tokens and placeholder patterns were excluded from `refs`.

ANOMALY: the anchor rename merged mid-audit (`6fb8093c4`) leaving 114 pre-consolidation refs dead across all seven specs, while independently 009 marks 61 tasks `[x]` yet 10 named test files (4 on completed tasks) do not exist, 041’s `probe-inject|probes|map` moved to `probe-utils.py` and its `index.json` was retired by 055, and the renamed registry detail files for 021/028/031 carry slugs from unrelated specs.

SPEC-AUDIT-LIVE-3-DONE
