# Live-Spec Audit — Batch 10 (6 specs)

- **Tree**: main tree `/storage/project/cloud-native-ai/spec-kit`, branch `master`
- **Audit-time commit**: `6fb8093c4` — "merge(layout): move the project anchors out of memory/ …"
- **Mode**: read-only; the only write is this file
- **Note**: the anchor-layout rename landed **during** this audit (it was a branch at start, merged to `master` before the reference pass completed). All counts below are against the post-rename tree. References to `.specify/memory/{constitution.md,features.md,features/<ID>.md,glossary.md,register.md}` are therefore **dead-with-successor**: they now resolve under `.specify/` and are flagged separately, not counted as ordinary rot.

## Method

- **Extraction**: every unique literal token matching `.specify/…`, `scripts/…`, `skills/…`, `templates/…`, `shared/…`, `tests/…` across each spec's `*.md` artifacts (`requirements/plan/tasks/contracts/data-model/quickstart/research/verification/feature-ref/notes`), punctuation-trimmed.
- **alive** = filesystem entry exists now; **archived-elsewhere** = target verified under `.specify/archive/`; **dead** = neither. Non-literal tokens (globs, `{…}` placeholders, `...` elisions) are treated structurally, not as paths.
- **Verdict rule**: `BROKEN` if any **pointer** (normative/instructional path), **guard**, or **implementation claim** fails; dated-record mentions, fixture-internal tokens, `.specify/.tmp/` scratch, and anchor-move refs are reported but do not by themselves flip the verdict (each is labelled).
- **Registry** now lives at `.specify/features.md`; per-feature details at `.specify/features/<ID>-<slug>.md` (post-rename layout).

## Batch Summary

| Spec | refs | alive | archived | dead | verdict |
|------|-----:|------:|---------:|-----:|---------|
| 023-agent-framework-redesign | 59 | 34 | 0 | 25 | BROKEN |
| 036-team-summary | 89 | 70 | 1 | 18 | BROKEN |
| 049-docs-reconcile | 48 | 39 | 0 | 9 | BROKEN |
| 062-humanize-command | 158 | 144 | 0 | 14 | BROKEN |
| 074-goal-team-sdd-unification | 104 | 95 | 0 | 9 | BROKEN |
| 084-harness-triple-structure | 760 | 705 | 0 | 55 | BROKEN |

`dead` is the mechanical count (includes anchor-move refs, dated-record mentions and scratch paths). Each section adjudicates them into broken pointers vs. non-pointers.

---

## 023-agent-framework-redesign

**Counts**: 59 refs / 34 alive / 0 archived / 25 dead — adjudicated: 13 tokens in 8 stale-pointer groups, 2 missing guards, 3 anchor-move refs, 7 non-pointer tokens (external research refs, prose, elision).

**Registry**: binder row **019 (Agents Command)** resolves — Details `.specify/features/019-agents-command.md` exists; Spec Path `.specify/specs/023-agent-framework-redesign/requirements.md` exists. Separate anomaly: row **023 (Prompt Template Quality, Draft)** has Spec Path `-` while its Details cell now points at `.specify/features/023-agent-framework-redesign.md` whose content title is "Prompt Template Quality" (slug/title mismatch; see anomaly line).

**Broken pointers**
- `.specify/specs/023-agent-framework-redesign/quickstart.md:22` → `skills/create-agent/templates/agent-role-team-supervisor-template.md`: missing. Canonical dir `skills/internal/create-agent/templates/` now holds 11 `agent-capacity-*` / project/self-improvement templates; no role/stage/supervisor names remain.
- `…/quickstart.md:21` → `skills/create-agent/templates/agent-stage-*.md`: missing; no `agent-stage-*` template exists anywhere.
- `…/plan.md:71` → `skills/improve-agent/SKILL.md`: now `skills/internal/improve-agent/SKILL.md` (`.specify` mirror: `.specify/skills/internal/improve-agent/`).
- `…/plan.md:72` → `skills/organize-agents/SKILL.md`: skill renamed to `create-team` (`.specify/features/027-feedback-mechanism.md` records "create-team (renamed from organize-agents)"); no `organize-agents` skill exists.
- `…/tasks.md:169` → `.specify/skills/organize-agents/`: now `.specify/skills/internal/create-team/`.
- `…/tasks.md:126` → `tests/scenarios/multi-agent-orchestration/team-loop-scenario.md`: missing (directory holds `parallel-dispatch-scenario.md`, `serial-chain-scenario.md`, `README` only).
- `…/plan.md:100` → `.specify/agents/ux-analyst.agent.md` and `agent-role-ux-analyst-template.md`: missing; UX analyst is now `skills/internal/create-agent/templates/agent-capacity-ux-analyst-template.md` (the same line already carries a "Superseded 2026-07-10" note).
- `…/tasks.md:103–106` → `agent-subrole-{executor,evaluator,improver}-template.md`, `agent-role-meta-coordinator-template.md`: missing; replaced by `agent-capacity-*` templates + `agent-supervision-delegation.md`.

**Guards**
- MISSING `tests/unit/test_agent_deprecated_terms.py` — named at `verification.md:52` (SC-002 "PASSES"); absent from tree and from `.specify/archive/`.
- MISSING `tests/unit/test_agent_reference_integrity.py` — named at `verification.md:60` (SC-004 "PASSES"); absent from tree and archive.
- Alive: `tests/integration/test_agents_creation.py`, `tests/integration/test_persistent_agent_lifecycle.py`.

**Spot-checks**
1. SC-003 "15 agent-* templates canonical under `skills/internal/create-agent/templates/`" — **FAIL**: 11 files, names migrated to `agent-capacity-*`.
2. SC-001 single command surface `templates/commands/agents.md` — **PASS**: file exists.
3. SC-005 Layer-2 scenario `tests/scenarios/conceptual-model/role-stage-type-conformance-scenario.md` — **PASS**: exists.

**Anchor-move refs**: `plan.md:26` `.specify/memory/constitution.md` → `.specify/constitution.md`; `plan.md:80` `.specify/memory/features.md` → `.specify/features.md`; `plan.md:81` `.specify/memory/features/019.md` → `.specify/features/019-agents-command.md`.

**Verdict: BROKEN** — 8 stale-pointer groups, 2 missing guards, 1 false implementation claim.

---

## 036-team-summary

**Counts**: 89 refs / 70 alive / 1 archived / 18 dead — adjudicated: 8 tokens in 5 stale-pointer groups, 1 missing guard, 3 anchor-move refs, 2 negative-path refs (absence intended), 3 glob refs that resolve (`gantt.puml`/`milestones.puml`/`wbs.puml`), 1 inner-capture token.

**Registry**: binder row **027 (Team Management)** resolves — Details `.specify/features/027-feedback-mechanism.md` exists; Spec Path `.specify/specs/036-team-summary/requirements.md` exists. The detail file's slug (`feedback-mechanism`) does not match its content title ("Team Management") — rename anomaly.

**Broken pointers**
- `quickstart.md:69–70` (also `plan.md:16`) → `skills/create-team/scripts/build-summary-input.py`: pre-consolidation path; resolves to `skills/internal/create-team/scripts/build-summary-input.py` (verified `--help` exit 0).
- `quickstart.md:11` → `skills/summarize-project/scripts/validate-project-input.py`: resolves to `skills/internal/summarize-project/scripts/validate-project-input.py` (verified `--blank-form` exit 0).
- `plan.md:11,26,73` → `.specify/goal/<goal-slug>/`: `.specify/goal` is absent; goal archive renamed to `.specify/anchoring/<goal-slug>/` (094 goal→anchoring). A sample goal (`090-re-anchoring`) holds `goal.md`.
- `contracts/summary-writeset.contract.md:40` → `.specify/agents/execution/scripts/**`: `.specify/agents/execution/` contains only `configs/`.
- `research.md:121` → `.specify/project/summary/`: absent; `.specify/project/` holds `project.md` + wbs/gantt/milestones `.puml/.svg/.png` (10 files).

**Guards**
- MISSING `tests/contract/test_goal_identity.py` — named at `tasks.md:84,87`; absent from tree and archive.
- Alive: `test_summary_form_generator.py`, `test_summary_trigger.py`, `test_summary_writeset.py`, `test_team_item_ledger.py`, plus all five integration tests named by the spec.

**Archived-elsewhere (not broken)**
- `feature-ref.md:32` `.specify/specs/.archive/026-agent-team-management/` → `.specify/archive/spec/026-agent-team-management/` (verified).

**Not broken (asserted-absence refs)**: `contracts/team-project-form.contract.md:40`, `contracts/items-ledger.contract.md:27` name `.specify/teams/.work/**` and `.specify/agents/execution/logs/**` as forbidden inputs; their absence is intended.

**Spot-checks**
1. Generator path claim (quickstart) — pointer **FAIL** (old path); behaviour **PASS** at the consolidated path.
2. Validator `--blank-form` — **PASS**, exit 0 at `skills/internal/summarize-project/scripts/validate-project-input.py`.
3. SC-003 "10 files in `.specify/project/`" — **PASS**: exactly 10 files.

**Anchor-move refs**: `plan.md:50` constitution; `checklists/requirements.md:55` `features.md` + `features/027.md` → `.specify/features.md`, `.specify/features/027-feedback-mechanism.md`.

**Verdict: BROKEN** — 5 stale-pointer groups + 1 missing guard.

---

## 049-docs-reconcile

**Counts**: 48 refs / 39 alive / 0 archived / 9 dead — adjudicated: 3 stale-pointer groups, 3 missing guards, 3 anchor-move refs, 0 non-pointers.

**Registry**: binder row **037 (Docs Command)** resolves — Details `.specify/features/037-goal-registry.md` exists; Spec Path `.specify/specs/033-docs-command/requirements.md` exists (the 049 spec is the fourth follow-up bound via `feature-ref.md`). Detail filename slug (`goal-registry`) mismatches its content title ("Docs Command").

**Broken pointers**
- `quickstart.md:12,21` → `.specify/docs/target-structure.md`: the whole `.specify/docs/` tree is absent. The live owner now declares **`docs/.speckit/target-structure.md`** (`templates/commands/docs.md:42`, `skills/external/create-docs/SKILL.md:30`).
- `quickstart.md:40` → `.specify/docs/audit/`: audit output is now `docs/.speckit/audit/<ts>-docs-audit.md` (`skills/external/create-docs/scripts/docs-utils.py:798`).
- `quickstart.md:128` → `scripts/python/docs-utils.py`: root engine absent; resolves to `skills/external/create-docs/scripts/docs-utils.py` (mirror: `.specify/skills/create-docs/scripts/docs-utils.py`; `--help` exit 0).

**Guards**
- MISSING `tests/contract/test_docs_action_routing.py` — named at `tasks.md:27,103` (and quickstart run set).
- MISSING `tests/contract/test_docs_skill_pair.py` — named at `tasks.md:27,104`, `quickstart.md:122`.
- MISSING `tests/contract/test_docs_reconcile_orchestration.py` — named at `tasks.md:27,131`.
- None of the successors (`test_docs_command_template.py`, `test_docs_utils_cli.py`, `test_docs_target_structure_declaration.py`, `test_docs_gate_driver.py`, `test_docs_step_injection.py`) carries the action-routing/orchestration contract names (grep for the routing ids found no hits).

**Spot-checks**
1. Declaration location claim `.specify/docs/target-structure.md` — **FAIL** (owner declares `docs/.speckit/target-structure.md`).
2. Engine path claim `scripts/python/docs-utils.py` — **FAIL** (skill-local engine is live; interface works).
3. GATE-1 runnable set (`tasks.md:27`, 8 files) — **FAIL**: 3 of 8 named files missing.

**Anchor-move refs**: `plan.md:34` constitution; `tasks.md:157` `features.md` + `features/037.md` → `.specify/features.md`, `.specify/features/037-goal-registry.md`.

**Verdict: BROKEN** — declaration/engine location drift + 3 missing contract guards.

---

## 062-humanize-command

**Counts**: 158 refs / 144 alive / 0 archived / 14 dead — adjudicated: 5 tokens in 1 stale-pointer group (skill rename), 7 anchor-move refs, 2 non-pointer tokens (prose/import example).

**Registry**: row **062 (Humanize Command)** resolves — Details `.specify/features/062-humanize-command.md` exists; Spec Path `.specify/specs/080-humanize-run-output/requirements.md` exists (extension binding). Inconsistency: `feature-ref.md:4` claims "本规格 ↔ Feature 062 自身，1:1", but the row's Spec Path points at the 080 extension, not 062.

**Broken pointers**
- `plan.md:86`, `quickstart.md:40,149,155` → `skills/external/humanize/` (and `skills/external/humanize/SKILL.md`): skill renamed; resolves to `skills/external/humanize-conclusion/SKILL.md`.
- `.specify/skills/humanize/` (plan.md:106, quickstart.md:40) → `.specify/skills/humanize-conclusion/SKILL.md` (verified).

**Guards**
- 0 missing. All named modules exist: `tests/contract/test_humanize_command_surface.py`, `test_feedback_command_classification.py`, `test_skill_layer_visibility_guards.py`, `test_run_skills_wiring.py`, `test_phase2_bindings.py`, `test_probe_registry_umbrella.py`, `test_compile_propagation_order.py`, and `tests/fixtures/humanize/diff_protected.py`.

**Spot-checks**
1. Skill path claim `skills/external/humanize/` — **FAIL** (now `humanize-conclusion`).
2. Command surface `templates/commands/humanize.md` — **PASS**: exists and line 46 mandates delegation to `.specify/skills/humanize-conclusion/SKILL.md`.
3. Guard module `tests/contract/test_humanize_command_surface.py` — **PASS**: exists.

**Anchor-move refs**: `plan.md:27` constitution; `plan.md:41` `features/` dir; `plan.md:159` `features.md`; `contracts/command-surface.md:16` `features/062.md`; `requirements.md:26` `glossary.md`; `review.md:219` `register.md` → all under `.specify/` now.

**Verdict**: **BROKEN** — stale skill path (rename); behaviour surface and guards intact.

**Verdict (080-humanize-run-output)**: **BROKEN** — the extension criterion cites the pre-rename skill path; its behaviour surface and guards are intact; the anchor-move and stale-skill refs are the only defects.

---

## 074-goal-team-sdd-unification

**Counts**: 104 refs / 95 alive / 0 archived / 9 dead — adjudicated: 5 tokens in 2 stale-pointer groups (parent `notes/`, pre-consolidation dispatch path), 3 anchor-move refs, 1 elision token.

**Registry**: row **074** resolves — Details `.specify/features/074-goal-team-sdd-unification.md` exists; Spec Path `.specify/specs/074-goal-team-sdd-unification/requirements.md` exists. Inconsistency: status cell reads **Ready for Review** while the row's dated entry says "Feature status advanced `Planned` → `Implemented`".

**Broken pointers**
- `tasks.md:31,75–77,244,250–251` → `.specify/specs/074-goal-team-sdd-unification/notes/{pre-change-measurements,quickstart-run,red-first-evidence}.md`: absent at the parent path. The same three carriers exist in **both live slices**: `.specify/specs/074a-authorized-routing/notes/` and `.specify/specs/074b-nested-governance/notes/` (verified). Parent `tasks.md` still shows 57 `[ ]` rows (the registry explicitly discloses the parent as a read-only split object whose delivery is carried by 074a/074b).
- `research.md:146` → `create-team/scripts/dispatch.sh`: pre-consolidation; resolves to `skills/internal/create-team/scripts/dispatch.sh` (mirror `.specify/skills/internal/create-team/scripts/dispatch.sh`).

**Guards**
- **0 missing**. All 20 named test files exist, including `test_sdd_routing_engine.py`, `test_sdd_routing_definitions.py`, `test_sdd_authorization.py`, `test_sdd_invocation_governance.py`, `test_nested_sdd_invocation.py`, `test_nested_run_report.py`, `test_flow_class_{correctness,ledger}.py`, `test_team_command_routing.py`, and the fixtures.

**Spot-checks**
1. Routing engine `sdd-route.py` — **PASS**: exists at `.specify/scripts/python/sdd-route.py`; `--help` exposes `route|authorize|golden` (read-only engine).
2. `sdd-invocation` capability/seat policy — **PASS**: present in `.specify/skills/internal/run-agent/SKILL.md`, `.specify/skills/internal/create-team/references/create-mode.md`, `shared/definitions/subagent-definitions.md`, and eight live team files.
3. Guard set for routing/authorization — **PASS**: all files exist.

**Anchor-move refs**: `plan.md:83` constitution; `plan.md:88` `features/074.md`; `tasks.md:254` `features.md` → `.specify/features/074-goal-team-sdd-unification.md`.

**Verdict: BROKEN (low severity)** — dead refs are confined to the disclosed-void parent artifact plus one pre-consolidation research mention; every normative implementation surface and guard is alive.

---

## 084-harness-triple-structure

**Counts**: 760 refs / 705 alive / 0 archived / 55 dead — adjudicated: 8 tokens in 6 broken groups, 1 missing guard name, 6 anchor-move refs, 41 non-pointer tokens (15 `.specify/.tmp/` scratch paths, ~20 diffstat/ellipsis inner captures, fixture/glob/prose tokens).

**Registry**: row **084** resolves — Details `.specify/features/084-harness-triple-structure.md` exists; Spec Path `.specify/specs/084-harness-triple-structure/requirements.md` exists; status `Completed`.

**Broken pointers / claims**
- `requirements.md:201` (STR-006 exclusion row) → `skills/external/humanize/`: skill renamed; live successor `skills/external/humanize-conclusion/`. The live declaration was already corrected (`shared/declarations/exclusions/no-machine-fact.yaml:94`), so the spec table is the stale surface.
- `review.md:343` → `tests/contract/test_harness_triple_contract.py` (claimed "68 passed"): missing; live module is `tests/contract/test_harness_triple_structure.py` (21 test defs).
- `review-r1.md:458` → `.specify/templates/plan.md` / `templates/plan.md`: absent; live templates are `templates/plan-template.md` / `.specify/templates/plan-template.md`.
- `review-r1.md:463` → `.specify/templates/commands/implement.md`: absent; live command is `templates/commands/implement.md`.
- `quickstart.md:94` → `test-evidence/triple-verify.json`: absent (the documented `--json-out` artefact was never landed).
- `review-r2.md:259` / `review.md:134` → `test-evidence/head-failed.txt`: absent; already disclosed as open (review-r2 F2: "two closed rows name evidence carriers that do not exist").
- **Implementation claim (SC-002)** — stated: "declarations 24; consistency declarations→carriers **32/32**, carriers→declarations **16/16**; unclassified 0; exit 0". Measured on this tree with the spec's own command (`python3 scripts/python/harness-triple-check.py --action verify|coverage --repo . --format text`, no `--json-out`, no write): declarations→carriers **47/51**, carriers→declarations **16/101**, `verify` and `coverage` exit **1**, with 2 `unclassified-candidate` findings — `shared/workflow/execution-topology.md` and `skills/internal/create-team/SKILL.md`. The 092 A2 recheck recorded only exclusion-row drift; the carrier-consistency faces have since regressed.

**Guards**
- MISSING name: `tests/contract/test_harness_triple_contract.py` (review.md:343); live successor `test_harness_triple_structure.py` exists.
- Alive named guards: `test_acceptance_*`, `test_harness_triple_structure.py`, `test_requirements_checker.py`, `test_compile_embeds.py`, `test_document_structure_gate.py`, and the fixture tree under `tests/fixtures/harness-triple-structure/`.

**Spot-checks**
1. Engine interface — **PASS**: `scripts/python/harness-triple-check.py` and `.specify/scripts/python/harness-triple-check.py` exist; `--help` exposes `coverage|verify|lookup`, exit codes 0/1/2 documented, "flag-only invocation writes nothing".
2. Exclusion-row count — **PASS**: 35 (`no-harness-asset.yaml`) + 38 (`no-machine-fact.yaml`) = **73**, matching SC-002.
3. SC-002 consistency/zero-findings claim — **FAIL** (reading above: 47/51, 16/101, 2 unclassified, exit 1).

**Anchor-move refs**: `plan.md:49` constitution; `plan.md:250` `features/081.md`; `code-review-20261105T160943Z.md:28` `features.md`; `:30` `features/084.md`; `review-r2.md:113` `register.md`; `plan.md:250` `features/` dir → `.specify/{constitution.md,features.md,features/081-acceptance-hardening.md,features/084-harness-triple-structure.md,register.md}`.

**Verdict: BROKEN** — one live claim now false (SC-002), one missing guard name, one stale exclusion row, two stale review targets, two absent evidence carriers (one self-disclosed).

---

ANOMALY: the anchor-layout rename merged mid-audit (commit `6fb8093c4`) and its detail-file naming is misaligned for five registry rows — row 023 (Prompt Template Quality) → `features/023-agent-framework-redesign.md`, row 027 (Team Management) → `features/027-feedback-mechanism.md`, row 036 (Dogfooding Practice) → `features/036-team-summary.md`, row 037 (Docs Command) → `features/037-goal-registry.md`, row 049 (Derivation Command) → `features/049-docs-reconcile.md` — every Details cell resolves, but the filename slug names a different requirement/feature than the file's content title.

SPEC-AUDIT-LIVE-10-DONE
