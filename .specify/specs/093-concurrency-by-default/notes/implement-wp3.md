# Implement record — WP3-owners (feature 093)

**Package**: `WP3-owners` (declared-order fold 3)
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-wp3` — branch `093-wp3`, based on `7ec5cc05`
**Date**: 2026-11-09
**Mode**: one fork-worker executor, serial (the FR-035 fork carrier was authored by this package but not exercised by this dispatch; see § Concurrency reading)
**Rows**: 30 of 30 closed (T037, T041, T060, T061, T078, T100, T114–T115, T120–T122, T132, T135, T139–T140, T142, T144–T151, T153–T158)

---

## 1. Per-row closure table

| Row | Surface(s) written | What landed | Evidence |
|-----|-------------------|-------------|----------|
| T037 | `shared/definitions/subagent-definitions.md` | New § The Concurrency Obligation: the three-part obligation (consider-first / default-concurrent / named-reason + reading triple), each separately checkable, one statement with a four-grain pointer table (skill/command, goal slice, team, loop stage). `[green C-042]` | `test-evidence/wp3-obligation-owner.txt`; commit `217342364` |
| T041 | three projection trees | Sources carry the obligation identically (the pointer block is byte-identical on 29/29 command templates; the agent files are mirrored sources). Mirror engine reading: exit 2 with a drift set **exactly equal** to the edited-source projection (zero unexpected pairs) — regeneration is the driver's integration step per the dispatch instruction | `test-evidence/wp3-mirror-reading.txt` |
| T060 | `subagent-definitions.md`, `decomposition-model.md` | Default-concurrent obligation stated (obligation owner) and "serial carries a named reason code + evidence + reading" stated in decomposition-model § 13 | `wp3-obligation-owner.txt`, `wp3-decomposition-model.txt`; commits `217342364`, `98d7b2021` |
| T061 | `wp-gate.py` | WG-15 extended with the **unit-level form**: non-read-only unit with an empty write domain → `write-domain-empty`; directory-level entry (glob metacharacter, or a path resolving to an existing directory) → `write-domain-directory`; read-only units keep their empty domain. No other check in the file changed | `test-evidence/wp3-wp-gate-wg15.txt` (five-case probe + 113 existing tests green); commit `f4523d4d5` |
| T078 | `wp-gate.py` | Same change closes the file-level enforcement: the WG-15 write-domain judgement is file-level only; overlap judgement unchanged; `decomposition-model.md` § 12 records the extended WG-15 description | same as T061 |
| T100 | `skills/internal/run-agent/SKILL.md` | Multi-unit duty routing rule (FR-024): capability judged from the **existing** `capability-tools` key, no new frontmatter key; incapable recipient → route to a capable executor and record the routing decision; a serialised multi-unit duty is a defect. Carrier pointer to the two process carriers | `test-evidence/wp3-executor-grains.txt`; commit `c8ab8395c` |
| T114 | `skills/internal/create-team/SKILL.md` | Member class + stated concurrency capability: class from the fact (pointer), concurrency statement derivable from classes + slot cap, no instantiation above it, capability read + reduction reported | `wp3-executor-grains.txt`; commit `c8ab8395c` |
| T115 | `create-team/references/conceptual-model.md` | § Seat territories judged at binding time: undeclared → `territory-undeclared` red; intersecting → `territory-intersect` red before any run; file-level path sets; measured 2/12 undeclared; capability bound reported. `[green C-067]` | `wp3-executor-grains.txt`; commit `c8ab8395c` |
| T120 | `skills/internal/create-plan/SKILL.md` | Step 4.5: plan stage default-concurrent, `decompose-plan-v1` partition, serial names a code + evidence, records its own reading triple | `wp3-executor-grains.txt`; commit `c8ab8395c` |
| T121 | `skills/internal/run-team/SKILL.md` | § 6 Orchestrate: seats are units, default-concurrent, reason code when serial, reading triple recorded (`not_evaluated` literal, never 0), in-process path BANNED. `[green C-046]` | `wp3-executor-grains.txt`; commit `c8ab8395c` |
| T122 | `templates/plan-template.md` + 29 `templates/commands/*.md` | One authored pointer text on every command surface and the plan template — obligation text and class table reached by path, no repo-specific fact, no rule restated. `[green C-061]` `[green C-072]` | 29/29 count in `wp3-executor-grains.txt`; commit `8183093bc` |
| T132 | four concept owners | `subagent-definitions.md`, `goal-definitions.md`, `conceptual-model.md`, `decomposition-model.md` reach the facts by path (`concurrency-class` / `serial-reason` / `effective-concurrency` / `concurrency-slot-and-reserve`); no tuning value restated. Class-anchor sections (`#class-*`) stay WP5's T034–T036 | `wp3-obligation-owner.txt`, `wp3-decomposition-model.txt` |
| T135 | `shared/definitions/goal-definitions.md` | Exactly one new § Target concurrency; goal/target model untouched (targets still carry no dependency edges); class/condition owners cited | `wp3-executor-grains.txt`; commit `377986b84` |
| T139 | driver `SKILL.md`, `dispatch-recipes.md` | `analyze` default = N concurrent SDD Analysis Workers; N from stage team config / spine `agent_concurrency_requested`; (a) file-level read domains, pre-dispatch intersection red; (b) deterministic consolidation (read-domain order → finding-id order, duplicates first-declared with suppression pointer); (c) reading triple + per-Worker `executor_id` / `verifier_id`. `[green C-093]` | `test-evidence/wp3-analyze-and-fork.txt`; commits `a1e0435d2` |
| T140 | `decomposition-model.md` § 20.1 | `analyze` no longer defaults to `off`: every stage resolves through `decomposition-coverage.yaml`; feature-level `off` stays the hard opt-out; precedence recorded; built-in default list removed (fact is the owner) | `wp3-decomposition-model.txt`; commit `98d7b2021` |
| T142 | `dispatch-recipes.md` (§ 本地原生拓扑, § Recipe 2 usage note, § Recipe 5, header), driver `SKILL.md` | The fork model: separate `qodercli` child processes through `stage-runner.sh` (stdin prompt, stream-json, sentinel), pool bound = runtime `nproc` reading, in-process fan-out not counted as concurrency; the old "MUST NOT launch qodercli locally" rule disposed. `[green C-094]` | `wp3-analyze-and-fork.txt`; commit `a1e0435d2` |
| T144 | `sdd-house-keeping/SKILL.md`, `references/maintenance-recipes.md` | Fork default / subprocess carrier / in-process BANNED in HR7, the remote-shape line, and the `## Subagent Delegation` carrier block | `test-evidence/wp3-carrier-ban.txt`; commit `1bac1d6e1` |
| T145 | `sdd-project-setup/SKILL.md`, `references/setup-recipes.md` | Same rewrite at the dispatch-carrier paragraph, S2.5 carrier, HR9 and the delegation block | `wp3-carrier-ban.txt`; commit `1bac1d6e1` |
| T146 | `watch-model.md`, `stage-prompts.md` | Watch model applies to **process-carried** dispatch including the local fork carrier (same signals/positive evidence/sentinel); the two-topology rule becomes fork/subprocess with the ban; U3 section converged | `wp3-carrier-ban.txt`; commit `93754347a` |
| T147 | `coaching-skills/SKILL.md` § Boundaries | Fork carrier first (same-family through `stage-runner.sh`), subprocess for heterogeneous agents, `run-agent` resolves/relays, in-process BANNED | `wp3-carrier-ban.txt`; commit `93754347a` |
| T148 | `analyze-artifacts/references/validation-and-report.md` | Dispatch-carrier paragraph: two legal process carriers (fork / subprocess; read-only allowlist and `--no-session-persistence` unchanged), in-process must not be a carrier, session-creation API prohibition kept | `wp3-carrier-ban.txt`; commit `93754347a` |
| T149 | `shared/workflow/execution-topology.md` | Carrier decision: local dispatch = fork carrier, heterogeneous = subprocess carrier, in-process BANNED; analysis/validation fan-out keeps its scope and points at the two carriers | `wp3-carrier-ban.txt`; commit `93754347a` |
| T150 | `shared/workflow/external-dispatch-recipes.md` | SDD boundary + Recipe 7 rewritten to the fork/subprocess carriers with the ban; remote topology and read-only flags unchanged | `wp3-carrier-ban.txt`; commit `93754347a` |
| T151 | `shared/definitions/agent-definitions.md` | Execution layer row, Instance → Execution bullet and the Driving-Subagents dispatch bullet each name the two carriers and pin the in-process ban | `wp3-carrier-ban.txt`; commit `93754347a` |
| T153 | `decomposition-model.md` § 13.4 (+ § 13.2 / § 17.1 convergence) | Local dispatch = fork carrier / subprocess carrier, in-process BANNED, serial names a code; remote, SD-13/SD-15 unchanged; the host-condition sentence now speaks about process carriers | `wp3-decomposition-model.txt`; commit `98d7b2021` |
| T154 | `stage-team-preset.md` (~L74) | `stage-worker` fill sentence = fork carrier locally, subprocess carrier for heterogeneous agents, in-process BANNED; seat structure and slot-cap projection unchanged | `wp3-carrier-ban.txt`; commit `93754347a` |
| T155 | `subagent-definitions.md` modes | Native-mode row/note no longer "native is the default"; the parallel forms are fork + subprocess; Mode Selection row and "When in doubt" rewritten; Visibility Contract and session-creation-API prohibition unchanged | `wp3-obligation-owner.txt`; commit `217342364` |
| T156 | `templates/instructions-template.md`, `.specify/instructions.md` | Template gains a **Testing** line (runner only, default xform, path/arg forwarding, raw forms never the entry). Live instructions refreshed through the instructions flow (targeted section update; non-destructive; one line in/out) | `test-evidence/wp3-instructions-refresh.txt`; commit `6759ab415` |
| T157 | `stage-prompts.md` § 第②段, `dispatch-recipes.md` § 阶段子代理预算与分段 | One test-entry sentence each: entry = `scripts/bash/run-tests.sh` (default xdist form; paths/args forwarded); dispatch brief must not carry an interpreter-level test command. Grep shows no raw invocation | `test-evidence/wp3-test-entry.txt`; commit `a1e0435d2`, `93754347a` |
| T158 | `implement-feature/SKILL.md`, `agents/sdd-implement-executor.agent.md`, `agents/sdd-implement-coordinator.agent.md`, + measured sweep (`create-skills/SKILL.md`, `merge-skills/…/decommission-and-wiring.md`, `non-disposable-definitions.md`, `docs/reference/history/00-cross-cutting-lessons.md`) | Runner-only MUST form (raw interpreter-level forms and output-piping forbidden); agents gain the runner name; every measured offender reworded to the runner form without losing its lesson; scan over the T159 scan set = zero invocation-shaped hits | `wp3-test-entry.txt`; commit `6759ab415` |

---

## 2. Verification readings

| Reading | Command | Result | Evidence |
|---------|---------|--------|----------|
| WG-15 both directions | five-case probe (`--check preflight`, temp repo with an existing `shared/` dir) | file-level → admit; empty → `write-domain-empty`; existing dir → `write-domain-directory`; glob → `write-domain-directory`; read-only empty → admit | `wp3-wp-gate-wg15.txt` |
| Existing wp-gate suites | `bash scripts/bash/run-tests.sh tests/unit/test_wp_gate.py tests/contract/test_sdd_loop_driver_wp_gate.py tests/integration/test_wp_coordination_dry_runs.py -q` | **113 passed** (no regression from the WG-15 extension) | `wp3-wp-gate-wg15.txt` |
| Mirror reading (T041) | `python3 scripts/python/sync-mirrors.py --check` | **exit 2** — drift set equals exactly the edited-source projection (29 command templates × 3 tool copies + 29 `.github/prompts`, 2 templates, 16 skills, 6 shared, 2 agents); zero unexpected pairs | `wp3-mirror-reading.txt` |
| Raw-invocation scan (T158) | invocation-shaped grep over `skills/ templates/ agents/ shared/ docs/reference/ .specify/instructions.md` | **zero hits** outside the T159 allowlist; remaining `pytest` occurrences are prose mentions only | `wp3-test-entry.txt` |
| Full suite (context) | `bash scripts/bash/run-tests.sh -q` | 255 failed / baseline 161 → 94 new names, classified in § 4. The great majority are mirror-parity tests that clear at regeneration; the semantic re-pin set is named there | `test-evidence/wp3-full-suite-after-edits.txt` |
| Old-rule scan | `grep -rn "MUST NOT 启动 qodercli\|MUST NOT launch qodercli\|host-native first" shared/ skills/ agents/ templates/` | zero hits | `wp3-carrier-ban.txt` |

---

## 3. Commits (branch `093-wp3`, no push)

```
217342364 feat(093-wp3): T037 T060 T132 T155 — concurrency obligation owner and the two-carrier mode selection
98d7b2021 feat(093-wp3): T060 T140 T153 — serial-reason default, analyze coverage, local dispatch convergence
f4523d4d5 feat(093-wp3): T061 T078 — WG-15 unit-level file-level write-domain form
377986b84 feat(093-wp3): T135 — target-concurrency paragraph in goal-definitions
c8ab8395c feat(093-wp3): T100 T114 T115 T120 T121 — coordinator routing, team capability and territory gate, plan/team default-concurrent
8183093bc feat(093-wp3): T122 — concurrency obligation pointer on plan-template and the 29 command surfaces
a1e0435d2 feat(093-wp3): T139 T142 T157 — analyze wave, fork mechanism and test entry in the driver surfaces
1bac1d6e1 feat(093-wp3): T144 T145 — fork/subprocess carriers and the in-process ban in house-keeping and project-setup
93754347a feat(093-wp3): T146 T147 T148 T149 T150 T151 T154 T157 — carrier ban across the remaining dispatch-declaring surfaces
6759ab415 feat(093-wp3): T156 T157 T158 — test-entry rule, live instructions refresh and the measured raw-pytest sweep
<final>     feat(093-wp3): T041 — evidence files and the WP3 implement record
```

---

## 4. Residual risks and handoff obligations (measured, not inferred)

### 4.1 Re-pin set — tests that pin the rule this package disposed (outside WP3's write domain)

Designed red-first (declared by T152, cleared when WP4's T152 lands):

- `tests/contract/test_sdd_loop_driver_skill.py::test_c23_local_native_subagent_default`
- `tests/contract/test_sdd_project_setup_skill.py::test_local_default_and_native_subagent`
- `tests/contract/test_coaching_run_contract.py::test_c12_one_dispatch_mechanism_with_a_recorded_mode`
- `tests/contract/test_sdd_carrier_contract.py::test_shared_carrier_owner_has_both_rules`, `::test_house_keeping_local_and_remote_shapes`, `::test_loop_driver_local_native_and_remote_cli`, `::test_shared_dispatch_doc_marks_local_variant_non_default`, `::test_setup_local_and_remote_shapes`

**Gap (not in T152's four-module list)** — three additional modules pin the old synchronous-local-native rule and must be added to the re-pin scope:

- `tests/contract/test_validation_carrier_contract.py::test_sdd_driver_carveout_is_visible[source]` — asserts the literal `阶段派发 MUST NOT 启动 qodercli` in the driver SKILL (the rule FR-035 disposes).
- `tests/contract/test_sdd_loop_driver_wp_coordination.py::test_sd_07_local_native_topology_and_serial_fallback` — asserts `"qodercli" not in` the decomposition model and the `parallel-native` / `serial-native` / `host-no-parallel-native` topology vocabulary (070-owned simulator outputs; FR-035 falsifies the former).
- `tests/contract/test_sdd_house_keeping_skill.py::test_target_resolution_traps` — asserts `MUST NOT 启动 \`qodercli\`` in the house-keeping text.

**Gap (Feature 077 byte-baseline pins)** — T122 legitimately changes all 29 shipped command templates; five of them carry the 077 stage-class wiring card whose byte-restore baseline is frozen:

- `tests/contract/test_stage_class_wiring.py` — 8 tests (`stripping_the_card_restores_the_baseline_bytes[...]` × 7, plus the humanize/doc pin path); the card-strip remainder now includes the obligation pointer.
- `tests/contract/test_humanize_command_surface.py::test_wc13_stage_class_pin_remeasured` — the pre-077 bytes pin for `humanize.md`.

The 077 test itself documents that its baseline is refreshed when a later feature legitimately moves the file (087 T063 did exactly that), so the fix is a **dated re-baseline**, not a weakening. FR-033's disposal list does not name 077 — that omission is the finding.

### 4.2 Regeneration debt (driver's integration step, not a defect)

All mirror-parity new-reds (the `test_mirror_parity_suite` parametrizations, `*_mirror*`, `test_source_and_mirror_are_byte_identical`, `test_di_05_delivery_and_mirror`, per-tool-copy and `sync_mirrors_check_clean` failures) are consequences of editing sources without regenerating; `sync-mirrors.py --write` + `regen-command-copies.py` clear them (T130).

### 4.3 Full-suite comparison noise

The trigger-engine / trigger-tuning family and `test_clause_coverage` (c20, c5) show order- and state-dependent results between the full run and isolated runs (they are partly in, partly out of the frozen baseline). Re-measure the delta after regeneration before adjudicating them; none of them reads a path this package edited except through the shared mirror tree.

### 4.4 Deliberate boundaries

- `host-no-parallel-native` survives only as a **dated supersession record** in `decomposition-model.md` § 13.2; the closed vocabulary's code `host-no-parallel` is the operative value.
- The concurrency-class fact's `#class-concurrent-by-default` / `#class-partition-required` / `#class-serial-only` anchors are **not** created here — they are WP5's T034–T036; this package authored the three-part obligation they sit beside.
- `dispatch-recipes.md` will also be edited by 094 wp05; the driver serializes the two write lines (T157's sentence is additive and scoped).
- `.specify/instructions.md` was refreshed through the instructions flow (targeted section update), not hand-edited as a framework source; its compatibility symlinks (AGENTS.md etc.) follow the file.

---

## 5. Concurrency reading of this dispatch (honest record)

- `requested`: 1 (the driver dispatched WP3 as a single fork-worker unit)
- `effective`: `not_evaluated` — one executor produces no interval overlap to measure
- `effective_reason`: `mechanism-not-yet-landed` — the FR-035 fork carrier is authored by this package (T142) but this dispatch ran before the regenerated runner path was exercised; no concurrency is claimed, and no serial run is presented as concurrent

---

## 6. Anomaly line

`ANOMALY: three test modules beyond T152's four-module list, and the Feature 077 byte-baseline pins (2 modules), assert the pre-093 carrier/verbatim-template state and are now red by design — they need a re-pin / dated re-baseline by an owner outside WP3's write domain; all other new reds are regeneration debt.`
