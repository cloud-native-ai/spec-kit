# Implementation Plan: /speckit.agents run — 显式 run 子命令与 superagent/subagent 架构自动应用（Agents Run）

**Branch**: `104-agents-run` | **Date**: 2026-11-24 | **Spec**: `.specify/specs/104-agents-run/requirements.md`
**Requirement → Feature**: `104-agents-run` → Feature 019 Agents Command
**Input**: Specification from `.specify/specs/104-agents-run/requirements.md` (24 FR / 7 SC / 8 Shared Strings; Clarifications 2026-11-24: requirements / clarify / plan-stage FR-020 amendment; Runtime Stack RS-001…RS-008)

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## Summary

The dispatch engine and the role model are both already delivered: `run-agent` dispatches native / virtual / external executions, and `superagent-definitions.md` (Feature 095) owns the relative role, the seven-field downlink, the five-element uplink, depth and state projection. What is missing is the user-visible, machine-pinned **explicit run subcommand** and the run-time wiring that makes the architecture apply automatically. This feature closes the five audited gaps with three authored-source edits, two doc-set corrections, and one test family — no second mechanism:

1. **Explicit syntax** — `templates/commands/agents.md` gains `argument-hint: "[create|refine|run] [agent-name] [task]"` ([[STR-001]]), keeps the run row of the three-skill delegation table and natural-language routing, and gains explicit-verb priority, the `missing agent name` stop ([[STR-003]]), and the never-serve statement that sharpens the existing team redirect. The run syntax is pinned verbatim across three faces: template `argument-hint`, the `run-agent` input contract, and the command reference Syntax block.
2. **Role automaticity** — `skills/internal/run-agent/SKILL.md` gains: the role-relation disclosure in the presentation (this session = the edge's superagent/root, child label, return channel, beside the existing config disclosure); the seven-field downlink carried **by pointer** to the 095 owner; the four pre-existing injections named by pointer; the five-element uplink with the incomplete-return rule; the child-label convention (existing `dispatch.sh <label>` = `run_id` = triplet prefix; retry = new label; old artifacts kept); and the narrowed SDD-probe applicability condition (a normal run is never blocked by a missing team/seat).
3. **Multi-child identity and visibility** — one run = one edge = one child; multiple runs are multiple command invocations; identity is the existing dispatch label and visibility rides the existing artifact triplet, `exec-quant` records and the `status-digest` role view. Zero new store, registry or renderer.
4. **Boundary** — single-agent semantics kept; multi-agent orchestration stays with `/speckit.team`; the SDD authorization probe applies only when the payload assigns or names an SDD driver.
5. **Docs same-source** — `docs/reference/commands/agents.md` is merged from three concatenated copies into one body; the "two capabilities" and "no-arg generates seven agents" claims are removed from the six named doc surfaces plus the routing scenario; overview / design / tutorials gain run and the third skill.

Testing splits by clause class per FR-023: artifact-class clauses are pinned by contract tests; behavior-class clauses (presentation disclosure, payload content, return completeness, runtime label uniqueness, probe application, reading recording) are evidenced by truth-source text + review + mutation drill and are never claimed as contract-covered.

## Technical Context

**Language/Version**: Markdown (command template, skill text, reference docs, contracts, tests as Python `pytest` modules); CPython `>=3.8` standard library only for the new tests.
**Primary Dependencies**: none added. Consumed read-only: `scripts/python/role-edge-check.py` (edge judgement), `scripts/python/execution-config.py` (config resolution), `skills/internal/create-team/scripts/dispatch.sh` (external dispatch carrier), `scripts/python/exec-quant.py` (quantification), `scripts/python/status-digest.py` (role view), `scripts/python/sync-mirrors.py` and `scripts/python/regen-command-copies.py` (generated copies), `scripts/bash/run-tests.sh` (unique test entry).
**Storage**: no new store, registry, queue or persistence root. Run identity reuses the existing dispatch label; visibility reuses the artifact triplet and `exec-quant` records.
**Testing**: `pytest` through the unique entry `scripts/bash/run-tests.sh` (targeted set `targeted-set-v1`; parallel default). New tests are static text/structure assertions plus one read-only engine invocation on a `tmp_path` fixture; behavior-class clauses are not asserted as contract coverage. SC-003 (pinned wiring, deletion turns red, relative name-level baseline) and SC-007 (unique entry, one green run, zero new name-level failures) are implement-stage criteria carried by the same entry.
**Target Platform**: Linux and macOS developer/CI hosts with Python 3.8+; no bash surface is changed.
**Project Type**: framework toolkit (command template + skill + reference docs + tests) — no application runtime, no new script.
**Performance Goals**: no runtime path is added; the new suite adds a handful of file reads plus one short-lived read-only engine process. No throughput target is claimed.
**Constraints**: zero new mechanisms (no skill / scheduler / queue / registry / renderer / store); role semantics stay owned by `superagent-definitions.md`; docs follow the template and skill, never the reverse; `.specify/**` mirrors and per-tool copies are regenerated, never hand-edited; the stale-literal set is closed over the seven named files.
**Scale/Scope**: 2 authored framework sources edited (`templates/commands/agents.md`, `skills/internal/run-agent/SKILL.md`), 6 named documentation surfaces + 1 routing scenario corrected, 5 new test files, 3 contracts, 9 data-model entities, 1 Feature detail note; mirrors regenerate 1 skill mirror and 4 per-tool command copies.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md`, 23 principle headings in order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every FR-001…FR-024 has a design carrier in the three contracts or `data-model.md`; `research.md` R-01…R-10 name the FRs they serve; quickstart scenarios map to the acceptance scenarios of US1–US5. |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 019 as the run mode of the same `/speckit.agents` surface; `.specify/features.md` row 019 and `019-agents-command.md` gain the plan note in this stage; 019 stays `Implemented` (no-status-regression). |
| III | Intent-Driven Development | ✅ Pass | `requirements.md` A-1…A-14 and the three Clarifications sessions carry the what/why; the design encodes them as routing rules (C-02/C-03), disclosure-not-gate (C-11), and the no-second-mechanism boundary (R-08). |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Three contracts carry `C-NN` clauses and each names its pinning test; the behavior-class split is declared clause-by-clause (FR-023) so tests assert artifacts, not fabricated behavior coverage; tasks stage writes tests before edits. |
| V | AI Agent Integration Standards | ✅ Pass | No `AGENT_CONFIG` / `_ASSISTANT_TIERS` change; per-tool command copies are regenerated by `regen-command-copies.py` (C-09), never hand-edited. |
| VI | Continuous Quality & Observability | ✅ Pass | Baseline drift was measured before design (B-06: mirrors rc 0, copies rc 0); no failing check is skipped or muted; plan-stage gates and audit dispositions land in `test-evidence/`. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Phases run in order; this stage lands Plan artifacts only, does not advance Feature 019's status, and invents no `[~]`/deferred task; Inherited Blockers declares `Dependency set: none` with its basis. |
| VIII | Code as the Single Source of Truth | ✅ Pass | Current state was measured, not assumed: `^# /speckit.agents` count = 3 (B-01), no `argument-hint` (B-02), stale literals and their files (B-03/B-04), run-agent's missing wiring (B-07); docs are corrected toward the template/skill, not the reverse. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Text + tests only: no runtime, scheduler, transmission channel or prompt-engine work; the one engine call in tests consumes the existing read-only `role-edge-check.py`; alternatives in R-01…R-10 each record the simpler choice. |
| X | Documentation Naming & Location Conventions | ✅ Pass | All edited paths are existing lowercase files; no reserved ALL-CAPS name or new directory is coined; the spec directory follows `.specify/specs/<key>/`. |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: all distributing edits land in `templates/` / `skills/` / `docs/` framework sources, then mirrors and copies regenerate; no `.specify/` runtime hand edit is planned. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Every capability reuses an existing Tool/skill/engine (run-agent, execution-config, dispatch.sh, exec-quant, role-edge-check, status-digest, sync-mirrors, regen-command-copies, run-tests); no helper script is generated. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | The feature strengthens Task Understanding (explicit syntax) and Change Validation (mutation drills SC-006, edge fixture SC-002) without a new scoring surface. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Role protocol, seven fields, five uplink elements, probe predicate, reading fields and visibility contract stay owned by their existing documents and are reached by pointer (C-12, C-15, C-17…C-19); docs follow the template; the stale-literal set is a closed, test-pinned list. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | One merged command reference; error strings and next steps name the actionable path; quickstart declares its reader baseline and per-example premises; behavior claims are not dressed as machine coverage. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Corrections applied and disclosed: the fifth enumeration face (routing scenario) was amended upstream per FR-020 before editing; stale-literal counts and the three-copy diff were measured, not assumed; audit dispositions are recorded in `test-evidence/plan-stage-2026-11-24.md`. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No directory is created; the only new files are `tests/contract/test_agents_run_*.py` in the existing `tests/contract/` with sibling-consistent names; test fixtures use pytest `tmp_path`. |
| XVIII | Grounded Naming | ✅ Pass | The `run` verb comes from the user's words and the sibling `[create|refine|run]` argument-hint precedents (`team.md`, `goal.md`); test file names follow the existing `test_<area>_*.py` siblings. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The command surface itself is the information dimension: an explicit `run <agent-name> [task]` syntax, a visible role relation and a visible child label; no second information dimension is added. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | New tests are file-read assertions plus one engine call, parallel-safe under the runner's default; no reduced selection, skipping or retry-until-green is introduced. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | No script is added or modified; the consumed `role-edge-check.py` already answers `-h` / `--version` and rejects undeclared options (B-08); the new tests assert its judged output. |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | The stage re-reads its rules after each core step; the two fresh-context audit passes and every applied correction are recorded in `test-evidence/plan-stage-2026-11-24.md`. |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | AI-authored change follows `.specify/workflow/git.md` (temp-branch model, merge to `master`); review reads merged history, no PR and no separate ledger. |

**Gates Status**: ✅ All 23 gates pass; no `Partial` or `Fail` row, so Complexity Tracking is `N/A`.

**Re-check after Phase 1**: re-judged after the Phase 1 artifacts landed (2026-11-24) — every row remains ✅ Pass; two facts sharpened in Phase 1 and are reflected above: the docs merge must delete the two older concatenated copies rather than reword them (row XIV), and the behavior-class clauses cannot be contract-covered, so FR-023's evidence route is encoded in the contracts themselves (row IV/XV).

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`.*

N/A

本计划无承重决策：下列四类触发均不成立，逐类说明如下。

- 不可逆：不适用——交付物是命令模板、技能文本、参考文档与测试；回滚即把两处 authored 源与六个文档面还原、删除新增测试文件，镜像与逐工具副本由生成器回退，工作树可逐字节复原。文档三副本合并是文本合并非数据迁移，历史版本留在 git。
- 跨团队：不适用——不修改任何引擎动作、载荷键、退出码、存储 schema 或共享事实；`role-edge-check.py` / `execution-config.py` / `dispatch.sh` / `exec-quant.py` / `status-digest.py` 零修改，`superagent-definitions.md` 与 `subagent-definitions.md` 保持 owner 原样。
- 高爆炸半径：不适用——一次错误的文本改动只影响 `/speckit.agents` 的呈现与路由文字，且被三条新增契约测试与既有守卫当场拦下；不触碰运行中的数据、共享服务或已冻结基线。
- 与宪法原则相关：不适用——设计遵守而非取舍相关 MUST：单一事实源（按指针引用 owner）、测试先行（契约先于实现）、快速失败（发现第五个枚举面即按 FR-020 程序先改上游）。没有一处以放宽某条 MUST 换取方案成立。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/104-agents-run/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (B-01…B-13 measurements, R-01…R-10 decisions)
├── data-model.md        # Phase 1 output (E1–E9, INV-01…INV-12)
├── quickstart.md        # Phase 1 output (S-0…S-7; per-example premises + pinning tests)
├── contracts/           # Phase 1 output (3 files)
├── feature-ref.md       # Phase 1 output (Feature 019 binding + delivery surface + unit registration verdict)
├── test-evidence/       # stage readings (plan.jsonl, plan-stage-2026-11-24.md, plan-gates/)
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement — NOT created here)
```

### Source Code (repository root)

```text
templates/commands/agents.md                       # argument-hint [[STR-001]], explicit-verb priority, missing-name path, team redirect
skills/internal/run-agent/SKILL.md                 # presentation role disclosure, seven-field downlink, five-element uplink, label rule, probe condition, visibility carriers
docs/reference/commands/agents.md                  # merged to one body; three capabilities, run syntax, run intent row, third skill, no-arg corrected
docs/reference/agents/command-and-skills.md        # three capabilities; run intent row; routing flow covers run; run-agent section
docs/reference/agents/overview.md                  # capability line + skill-count line + diagram gain run-agent
docs/reference/agents/design.md                    # command capability line, workflow step, single-agent skill list gain run-agent
docs/tutorials/installation.md                     # command-table row corrected; stale no-arg "generate seven agents" next step corrected
docs/tutorials/quickstart.md                       # command-table row corrected; three stale no-arg passages corrected
tests/scenarios/agents-command/single-entry-routing-scenario.md  # three-capability scope + explicit run routing samples
tests/contract/test_agents_run_command_contract.py # template + skill input + docs syntax coherence; routing sample set; mutation-pinned literals
tests/contract/test_agents_run_docs_contract.py    # single-copy count, stale-literal zero set, capability sets across the seven named files
tests/contract/test_agents_run_skill_wiring.py     # seven downlink / five uplink / presentation / label / probe condition / no-second-mechanism pointers
tests/contract/test_agents_run_multi_child_edges.py # same-parent two-child fixture through role-edge-check.py; retry/label mutation legs
tests/contract/test_agents_run_scope_contract.py   # static zero-second-mechanism surface + allowed-surface closure assertions (SC-005, INV-12)
.specify/features.md                               # Feature 019 row note (plan artifacts landed; status unchanged)
.specify/features/019-agents-command.md            # Feature 019 detail plan note
```

**Structure Decision**: the feature extends the existing framework layout — two authored sources edited in place, six documentation surfaces and one routing scenario corrected in place, five new test modules in the existing `tests/contract/` tree. No new top-level directory, no new skill directory, no new script, no runtime service. Mirrors and per-tool copies are produced by the existing generators. The `status-digest.py` role view, `role-edge-check.py`, `execution-config.py`, `dispatch.sh` and `exec-quant.py` are consumed read-only and are **not edited**.

### Unit Registration Verdict

**No new unit row is registered.** The feature adds no skill and no command: it edits the existing `/speckit.agents` command template and the existing `skill:run-agent` skill. Both already hold their per-unit registrations — `shared/definitions/flow-class-definitions.md` carries the `/speckit.agents` row (line 145) and the `skill:run-agent` row (line 225), and `shared/definitions/probe-definitions.md` carries `skill-run-agent-wrapup` (line 203). Accordingly, no probe row, flow-class row, glossary entry or Feature row is added; the Feature registry receives only the binding/plan note on its existing 019 row.

### Mirror Obligations *(mandatory — the two edited sources have mirrors or generated copies)*

**Baseline drift measured before any edit** (2026-11-24): `python3 scripts/python/sync-mirrors.py --check` rc 0 (six pairs ok, six projected rows ok, per-tool copies OK) and `python3 scripts/python/regen-command-copies.py --check` rc 0. The Verify cells mean **no NEW drift on the pairs this spec touches**, judged against that baseline — never "all green" as an absolute claim.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/agents.md` | `.claude/commands/speckit.agents.md`; `.github/prompts/speckit.agents.prompt.md`; `.qoder/commands/speckit.agents.md`; `.opencode/command/speckit.agents.md` (via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror — retired) | `regen-command-copies.py` (no argument regenerates in place) then `--check` rc 0; the four copies contain the body's `run <agent-name> [task]` run row (the generator projects the body only — frontmatter `argument-hint` is not a copy face) |
| `skills/internal/run-agent/SKILL.md` (plus `references/` only if an edit there is required) | `.specify/skills/internal/run-agent/**` (pair `skills/internal` ↔ `.specify/skills/internal`) | `sync-mirrors.py --write --only skills/internal` then `--check`; pair `ok`; `diff -q` on the skill file empty |

`docs/**`, `tests/**`, `.specify/specs/104-agents-run/**` and `.specify/features*` have no mirror; `.specify/features*` are single-owner registries and are never split.

## Execution Premises

Owner of this table's shape, its `Status` / `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises. The ids below are the targets cited by `requirements.md` RS-001…RS-008.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | A CPython `>=3.8` interpreter and the existing `pytest` runner are available through the unique entry `scripts/bash/run-tests.sh`, and the new tests need no third-party import. | `pyproject.toml` (`requires-python = ">=3.8"`; pytest is a dev dependency; `testpaths = ["tests"]`), `scripts/bash/run-tests.sh` present; the new modules import `json`/`os`/`re`/`subprocess`/`pathlib` plus pytest only. | verified | — |
| EP-002 | The existing engines consumed by this feature exist and are read-only consumable with the interfaces the design assumes: `role-edge-check.py` (`--action report/query`, exit 0/1/2), `execution-config.py` (`resolve`), `dispatch.sh <label>`, `exec-quant.py --action collect-dispatch`, `status-digest.py`. | `python3 scripts/python/role-edge-check.py --help` (B-08); `b9` dispatch-record carrier read at `scripts/python/role-edge-check.py` `_parse_dispatch_records` (`state/memory/exec-quant/records/*.json`, `unit_type=agent`, `unit_id=agent:<parent>`, `run_id=<label>`, triplet confirmation); `skills/internal/create-team/scripts/dispatch.sh` present; `exec-quant.py --action collect-dispatch` documented in `run-agent`; `status-digest.py` present. None is modified by this feature. | verified | — |
| EP-003 | The two authored sources are the authoritative carriers of the run intent; every mirror or per-tool copy regenerates deterministically from them, and the live tree has zero pre-existing drift on the pairs this spec touches. | `sync-mirrors.py --check` rc 0 and `regen-command-copies.py --check` rc 0 measured 2026-11-24 (B-05/B-06); the run intent lives only in `templates/commands/agents.md` and `skills/internal/run-agent/SKILL.md` (B-02/B-07); `docs/reference/commands/agents.md` is hand-authored (no generator). | verified | — |

## Inherited Blockers

Dependency set: none

No dependency artifact is declared. Feature 019 is this feature's **parent** command surface (the thing being extended), not a dependency whose `verification.md` or deferred rows this plan inherits from; 095 / 061 / 059 / 064 contribute **owners and read-only engines** (role model, config resolution, dispatch carrier, quantification, concurrency facts) consumed by reference, and 095's own verification record carries `deferred_tasks=none` / `final_path_deferred=0` as measured (2026-11-24), so no row is inherited.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | this-slice | No dependency artifact was declared; nothing is inherited. |

## Complexity Tracking

N/A — the Constitution Check has no `Fail` or `Partial` row, so there is nothing to justify.
