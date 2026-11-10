# Live-Spec Audit — Batch 9

**Scope**: 021, 035, 048, 061, 073, 083
**Tree**: `/storage/project/cloud-native-ai/spec-kit` (master)
**Observed**: 2026-11-10 ~11:03 CST
**Mode**: read-only; no spec/source edits, no subagents, no commits.

## Method & Legend

- **refs** = distinct repository paths (`.specify/…`, `scripts/…`, `skills/…`, `templates/…`, `shared/…`,
  `tests/…`, `src/…`, `docs/…`, `agents/…`) cited by the spec's prose artifacts
  (requirements/plan/tasks/contracts/data-model/quickstart/verification/notes/feature-ref/review/audit/research).
- Excluded from the denominator: placeholder forms (`<...>`, `{...}`), brace/truncation extraction artifacts,
  spec-self paths (`.specify/specs/<own-dir>/…`), and dated per-run record filenames (22 such refs in 083).
- **alive** = exists now (direct path, or its framework mirror at the other of `scripts/…` ↔ `.specify/scripts/…`).
- **archived** = moved under `.specify/archive/`.
- **dead** = no live target; a pointer at a pre-consolidation path counts as dead.
- Line numbers are relative to the repository root.

**Mid-audit tree change**: commit `6fb8093c4` (2026-11-10 11:03:17 +0800) merged the anchor-layout rename
onto master while this audit was running. `.specify/memory/{constitution,features,glossary,register,tools}.md`
and `.specify/memory/features/<ID>.md` were live at ~10:55 and are gone at 11:03; their new homes are
`.specify/<anchor>` and `.specify/features/<NNN>-<slug>.md`. All such refs below are classified **dead
(anchor rename)** against the current tree, with the new target named.

---

## 021-agent-specific-config

**Counts**: refs 41 · alive 25 · archived 0 · dead 16

**Broken**

| Cite | Now resolves to |
|---|---|
| `plan.md:26` | `.specify/memory/constitution.md` → `.specify/constitution.md` (anchor rename) |
| `tasks.md:5` | `.specify/memory/features.md` → `.specify/features.md` (anchor rename) |
| `tasks.md:147` | `.specify/memory/features/022.md` → `.specify/features/022-ai-tools-support.md` (anchor rename) |
| `contracts/agent-specific-config.contract.md:33`; `plan.md:64-65`; `quickstart.md:82-83`; `tasks.md:95,102,109` | `skills/browser-utils/**` → **absent**; skill relocated out of repo (registry 048 row: "relocated to xuanji-extension") |
| `plan.md:66-70`; `quickstart.md:87-97` | `skills/create-agent`, `skills/improve-agent` → now `skills/internal/create-agent`, `skills/internal/improve-agent`; `skills/improve-skills` → `skills/external/improve-skills` |
| `tasks.md:65-66` | `tests/contract/test_agent_specific_config_commands.py` → **missing** (no successor found) |
| `tasks.md:128-129` | `tests/contract/test_agent_specific_config_feedback.py` → **missing** (no successor found) |
| `quickstart.md:28,68` | dated samples `.specify/memory/feedback/{agents,browser-utils}-claude-code-2026-06-25*.md` → absent (illustrative filenames) |
| `tasks.md:129` (T030) | `.specify/memory/feedback/.gitkeep` → absent (directory exists and is populated) |

**Registry row**: resolves mechanically — Feature Details `.specify/features/021-agent-specific-config.md`
exists; Spec Path `.specify/specs/009-claude-code-support/requirements.md` exists. **Content mismatch**: the
row and detail file name "Claude Code Support" and point at spec 009, not at the 021 spec directory.

**Guards**: named 3 — present 1 (`test_agent_specific_config_skills.py`, 4 tests), missing 2
(`test_agent_specific_config_commands.py`, `test_agent_specific_config_feedback.py`).

**Spot-checks**

1. `templates/commands/{tools,skills,agents}.md` — the C-001 literal section `## Agent-Specific Configuration`
   is absent from **0 of 3** command templates (tools.md:97 and skills.md:54 now route to
   `shared/workflow/agent-configuration.md`). The section survives in 6 SKILL.md files.
   Verification's "7/7 targeted files" claim no longer holds.
2. `tests/contract/test_agent_specific_config_skills.py` — 4 test functions only (skills surface);
   the claimed "37 tests across 3 files" has no live basis.
3. Reference guides — 6 live guides
   (`skills/internal/{create-agent,improve-agent}/references/`, `skills/external/improve-skills/references/`);
   `browser-utils` pair gone, so verification's "8 reference docs" is now 6.

**Verdict: BROKEN** — central command-template surface refactored away, 2/3 guards missing, browser-utils
and pre-layer skill paths dead, 3 anchor refs dead.

---

## 035-token-efficiency

**Counts**: refs 81 · alive 68 · archived 0 · dead 13

**Broken**

| Cite | Now resolves to |
|---|---|
| `plan.md:27` | `.specify/memory/constitution.md` → `.specify/constitution.md` (anchor rename) |
| `tasks.md:5` | `.specify/memory/features.md` → `.specify/features.md` |
| `tasks.md:100`; `audit.md:12,13,18,19` | `.specify/memory/features/` (dir and read instructions) → `.specify/features/` |
| `feature-ref.md:4` | `.specify/memory/features/040.md` → `.specify/features/040-agent-metadata-portability.md` |
| `audit.md:27` | `.specify/memory/glossary.md` → `.specify/glossary.md` |
| `quickstart.md:18` | `skills/{create-agent,create-team,create-tools}/SKILL.md` → `skills/internal/…` |
| `audit.md:28` | `skills/git-workflow` → absent; nearest live successor `skills/external/git-utils/` |
| `tasks.md:77` (T010) | `tests/contract/test_token_efficiency_remediation_program_first.py` → **missing** |
| `tasks.md:100` (T017) | `tests/contract/test_token_efficiency_remediation_summary_first.py` → **missing** |
| `audit.md:42` | glob `tests/contract/test_token_efficiency_remediation_*.py` → matches nothing |

**Registry row**: **does not resolve**. Row 035 is "Code Quality Tooling" (Draft) with Spec Path `-`;
`.specify/features/035-token-efficiency.md` exists but its body is the same stale "Code Quality Tooling"
feature — it does not describe the 035-token-efficiency spec.

**Guards**: named 5 (+glob) — present 3 (`test_token_efficiency_gates.py`, `_feedback.py`, `_discipline.py`),
missing 2 (`_remediation_program_first.py`, `_remediation_summary_first.py`); the glob names 0 additional
files. The discipline test covers CD-1…CD-5 but not the frozen "violating sentence disappeared" remediation pins.

**Spot-checks**

1. `shared/guidelines/token-efficiency.md` — has Program-First / Summary-First / Escalation / Small-file /
   Consumption-Observation sections; `diff -q` vs `.specify/shared/guidelines/token-efficiency.md` is
   byte-identical. PASS.
2. `shared/workflow/feedback-step.md:96` — three self-check questions plus the literal `token-efficiency`
   marker; 77 feedback entries in the store carry that marker, so `list --contains token-efficiency` is
   recoverable. PASS.
3. `templates/instructions-template.md:116` — `## Token Efficiency Discipline` ambient section present. PASS.
   (The remediation pin files themselves are the guard gap above.)

**Verdict: BROKEN** — registry row binds the wrong feature, 2 remediation guards missing, 6 anchor refs and
3 pre-layer skill refs dead.

---

## 048-derive-command

**Counts**: refs 82 · alive 73 · archived 0 · dead 9

**Broken**

| Cite | Now resolves to |
|---|---|
| `plan.md:36` | `.specify/memory/constitution.md` → `.specify/constitution.md` (anchor rename) |
| `plan.md:41`; `tasks.md:54` | `.specify/memory/features.md` → `.specify/features.md` |
| `feature-ref.md:36`; `checklists/requirements.md:67` | `.specify/memory/features/049.md` → `.specify/features/049-docs-reconcile.md` |
| `contracts/derive-command-template.md:25` | `.specify/memory/glossary.md` → `.specify/glossary.md` |
| `requirements.md:214,221`; `plan.md:108,131`; `contracts/move-library.md:88`; `feature-ref.md:16`; `data-model.md:136` | `.specify/goal/` (and `.specify/goal/<goal-slug>/`) → **absent**; the goal archive is `.specify/anchoring/` (owner: `skills/internal/manage-goal/SKILL.md:68`) |
| `contracts/move-library.md:85`; `plan.md:108` | `.specify/memory/sanitize/` → **absent**; sanitize stores are `.specify/memory/renumber/` (+ `retention/`) |
| `contracts/move-library.md:6` | `tests/contract/test_derive_move_library.py` → **missing** |
| `contracts/derivation-model.md:5` | `tests/contract/test_derive_model_enforcement.py` → **missing** |
| `contracts/derive-command-template.md:32` | `tests/contract/test_goal_command_surface.py` → **missing**; symbol `test_command_does_not_restate_the_concept` absent, nearest live file `tests/contract/test_goal_command_template.py` |

**Registry row**: **does not resolve**. Row 048 is "Browser Utils Skill (relocated…)" and its Spec Path
`.specify/specs/046-browser-site-memory/requirements.md` now resolves only at
`.specify/archive/specs/046-browser-site-memory/requirements.md` (archived). Feature Details cell
`.specify/features/048-derive-command.md` exists but describes Browser Utils, not this spec.

**Guards**: named 8 derive tests — present 8 (`test_derive_engine_contract.py`, `test_derive_command_surface.py`,
`test_derivation_definitions.py`, unit `test_derive_validate.py`/`test_derive_moves.py`, integration
`test_derive_us1/2/3.py`); missing 3 (above).

**Spot-checks**

1. `scripts/python/derive-utils.py:24-27,196` — actions `moves-list` / `moves-add` / `stats` / `validate`
   present; engine-writer marker states `moves-add` is the only writer. PASS.
2. `.specify/derive/moves.md` — M-001 row present; `.specify/derive/rest-architecture/derive.md:32,42` carries
   `## Reasoning Moves Applied` and the `| M-001 | new |` disposition log. PASS (SC-003 dogfood artifact live).
3. Command surface — 4 generated copies (`.claude`, `.github`, `.qoder`, `.opencode`) exist. Note: the
   disposition-table requirement no longer lives in `templates/commands/derive.md` (thin command surface);
   it now sits at `skills/internal/derive-architecture/SKILL.md:106`. Requirement survives, location moved.

**Verdict: BROKEN** — registry row binds Browser Utils to an archived spec, 3 named guards missing,
`.specify/goal/` and `.specify/memory/sanitize/` premises no longer exist, 4 anchor refs dead.

---

## 061-subagent-cli-config

**Counts**: refs 99 · alive 91 · archived 0 · dead 8

**Broken**

| Cite | Now resolves to |
|---|---|
| `plan.md:27` | `.specify/memory/constitution.md` → `.specify/constitution.md` (anchor rename) |
| `tasks.md:5,26`; `feature-ref.md:95`; `requirements.md:21` | `.specify/memory/features.md` → `.specify/features.md` |
| `feature-ref.md:96`; `checklists/requirements.md:36` | `.specify/memory/features/061.md` → `.specify/features/061-subagent-cli-config.md` |
| `plan.md:124` | `.specify/memory/glossary.md` → `.specify/glossary.md` |
| `plan.md:15` | `.specify/agents/execution/logs/` → **absent**; gitignored runtime dir (`.specify/.gitignore:12`); per-entry quant records live at `.specify/memory/exec-quant/records/` |
| `verification.md:145` | `.specify/agents/execution/logs/061-line-state.md` → **absent** (gitignored runtime evidence) |
| `quickstart.md:78` | `.specify/agents/execution/logs/config-snapshots/72ae1cc218e8aca8.json` → **absent** (runtime snapshot) |
| `quickstart.md:94` | `.specify/agents/execution/configs/sample-agent.yaml` → **absent** (quickstart-created fixture, not committed) |

**Registry row**: resolves — Feature Details `.specify/features/061-subagent-cli-config.md` and Spec Path
`.specify/specs/061-subagent-cli-config/requirements.md` both exist.

**Guards**: all named guards present (0 missing): `test_exec_quant_engine.py`, `test_execution_config_engine.py`,
`test_exec_quant_dispatch.py`, `test_probe_engine_action_sets.py`, `test_init_execution_config.py`,
`test_fast_fail_discipline.py`, `test_progress_reporting.py`, `test_instructions_section_propagation.py`,
`test_goal_migration.py`, `test_neutrality_budget.py`.

**Spot-checks**

1. `scripts/python/execution-config.py:7,31,47` — actions `resolve / validate / list-configs`; `CAPABILITY_MATRIX`
   with `qodercli` and `claude` rows. PASS.
2. `scripts/python/exec-quant.py:13-14,135` — `schema_version=2`, `unit_type=agent` via `agent:<slug>`,
   `collect-dispatch` in the closed action set. PASS.
3. `.specify/agents/execution/configs/_defaults.yaml` — byte-equal to `templates/execution-config-defaults.yaml`;
   `skills/internal/run-agent/references/dispatch-preflight.md:14` row ④ requires `resolve` exit 0 + non-empty
   `config_id`. PASS.

**Verdict: BROKEN** — 4 anchor refs dead; 4 runtime-evidence paths absent by design (gitignored / quickstart
fixtures), not consolidation rot. No guard or implementation claim regressed.

---

## 073-record-retention-and-housekeeping

**Counts**: refs 6 · alive 6 · archived 0 · dead 0

**Broken**: none.

**Registry row**: resolves — Feature Details `.specify/features/073-record-retention-and-housekeeping.md` and
Spec Path `.specify/specs/073-record-retention-and-housekeeping/requirements.md` both exist.

**Guards**: requirements name no test file; the implied SC-003 guards exist —
`tests/contract/test_record_retention_engine.py`, `tests/contract/test_sdd_house_keeping_skill.py`.

**Spot-checks**

1. `scripts/python/record-retention.py --help` — action set is exactly
   `scan, distill, plan, apply, status, args-manifest` (FR-001). PASS.
2. `skills/external/sdd-house-keeping/SKILL.md:25-38` — H0–H5 loop with the `sdd-project-setup` (S0–S2) /
   `sdd-loop-driver` (U0–U6) handoff contract (FR-007 / US2). PASS.
3. `templates/commands/sanitize.md:14` — accepts `--lane materials|retention|renumber|all` (superset of
   FR-006's `materials|retention|all`; `renumber` was added later). PASS.

**Verdict: INTACT**.

---

## 083-mechanism-policy-separation

**Counts**: refs 271 · alive 261 · archived 1 · dead 9

**Broken**

| Cite | Now resolves to |
|---|---|
| `plan.md:44` | `.specify/memory/constitution.md` → `.specify/constitution.md` (anchor rename) |
| `tasks.md:5`; `feature-ref.md:5`; `review.md:50,138` | `.specify/memory/features.md` → `.specify/features.md` |
| `feature-ref.md:6`; `plan.md:278-280` | `.specify/memory/features/083.md` / `.specify/memory/features/` → `.specify/features/083-mechanism-policy-separation.md` / `.specify/features/` |
| `plan.md:188,211,367`; `tasks.md:24,218` | `.specify/memory/glossary.md` → `.specify/glossary.md` |
| `feature-ref.md:37`; `research.md:47` | `.specify/specs/069*/notes/pre-change-file-hashes.txt` → **archived**: `.specify/archive/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` |
| `code-review.md:185` | `agents/sdd-executor.agent.md` → **absent** (role split; no `sdd-executor.agent.md` remains) — dated diff record |
| `code-review.md:388` | `.specify/agents/instances/sdd-requirements-executor.agent.md` → **absent** — dated diff record |
| `code-review.md:35` | `.specify/agents/templates/sdd-executor.agent.md` → **absent** — dated diff record |
| `notes/pre-change-measurements.md:151` | `skills/external/humanize/SKILL.md` → `skills/external/humanize-conclusion/SKILL.md` |

**Registry row**: resolves — Feature Details `.specify/features/083-mechanism-policy-separation.md` and Spec Path
`.specify/specs/083-mechanism-policy-separation/requirements.md` both exist.

**Guards**: named 11 mechanism/skill-reference tests all present (`test_mechanism_policy_{guard,owner_doc,
skill_wiring,missing_policy,ownership,decidability}.py`; `test_skill_reference_{grammar,failures,matrix,
command_surface,consumers}.py`). **1 broken guard dependency**: `tests/contract/test_expression_compatibility.py:63`
resolves its hash manifest from the now-archived `.specify/specs/069a-flow-classification-docs-gates`; the
missing-file assertion fires at `test_expression_compatibility.py:297` (`_read` → `expected file missing`).

**Spot-checks**

1. Owner docs — `shared/definitions/mechanism-policy-definitions.md` (Boundary Test / Misplacement Symptoms)
   and `shared/definitions/skill-reference-definitions.md` (Accepted forms / Normalization / Disambiguation /
   Failure semantics / Boundary) exist; both mirrored under `.specify/shared/definitions/`. PASS.
2. Five consumers cite the owner by path — `run-skills:16`, `create-skills:35`, `improve-skills:20`,
   `merge-skills:27`, `coaching-skills:29`. PASS.
3. `tests/fixtures/skill-reference/normalization-matrix.json` — 30 rows; `tests/contract/test_skill_reference_matrix.py`
   recomputes and prints `rows=N matched=N failed=0`. PASS. (The adjacent 069a dependency is the guard failure above.)

**Verdict: BROKEN** — 5 anchor refs dead, 1 archived-only ref, 4 dated-record refs to renamed/removed
agent paths, and the `069a` archive move breaks one named guard's fixture resolution.

---

## Batch Summary

| Spec | refs | alive | archived | dead | Verdict |
|---|---:|---:|---:|---:|---|
| 021-agent-specific-config | 41 | 25 | 0 | 16 | **BROKEN** |
| 035-token-efficiency | 81 | 68 | 0 | 13 | **BROKEN** |
| 048-derive-command | 82 | 73 | 0 | 9 | **BROKEN** |
| 061-subagent-cli-config | 99 | 91 | 0 | 8 | **BROKEN** |
| 073-record-retention-and-housekeeping | 6 | 6 | 0 | 0 | **INTACT** |
| 083-mechanism-policy-separation | 271 | 261 | 1 | 9 | **BROKEN** |
| **Total** | **580** | **524** | **1** | **55** | 1 INTACT / 5 BROKEN |

**Cross-cutting observations (not fixes)**

- Anchors: every `.specify/memory/{constitution,features,glossary,register,tools}.md` and
  `.specify/memory/features/<ID>.md` cite in these six specs is now dead; mechanical rewrite target is
  `.specify/<anchor>` / `.specify/features/<NNN>-<slug>.md`.
- Registry drift is independent of the rename: rows 021/035/048 describe different features than their spec
  directories (Claude Code Support / Code Quality Tooling / Browser Utils). 035's Spec Path is blank; 048's
  points at archived 046.
- Skill layer: pre-`internal/`+`external/` paths and `browser-utils` account for most pre-existing dead refs;
  `browser-utils` has no in-tree successor.
- One live-surface defect outside these specs was observed while tracing 048: `templates/commands/sanitize.md:26`
  still names `.specify/memory/sanitize/` for materials findings, but that directory does not exist.

**ANOMALY**: the main tree mutated mid-audit — commit `6fb8093c4` (2026-11-10 11:03:17 +0800) merged the
anchor-layout rename onto master while this read-only audit was running, flipping every
`.specify/memory/{constitution,features,glossary,register,tools}.md` / `.specify/memory/features/<ID>.md`
reference from alive (observed ~10:55) to dead (observed 11:03); registry rows 035 and 048 additionally fail
their Spec Path resolution (blank / archived 046), and `tests/contract/test_expression_compatibility.py`
(083 guard) now reads an archived 069a manifest path.

SPEC-AUDIT-LIVE-9-DONE
