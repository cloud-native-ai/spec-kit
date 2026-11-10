# Implementation Plan: Super Agent as a Relative Logical Role (095-superagent-role)

**Branch**: `095-superagent-role` | **Date**: 2026-11-10 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `095-superagent-role` → Feature 095 Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）
**Input**: Specification from `.specify/specs/095-superagent-role/requirements.md`

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## Summary

Super agent is defined once, as a **relative logical role on a dispatch edge**: the endpoint that created the child execution is the super agent, the endpoint that was created is the subagent, and one execution can hold both roles on different edges ([[STR-002]]). The delivery is definition + protocol + a closed nine-item role-transition injection + projection wiring onto existing carriers — never a new runtime. Concretely: one new owner page (`shared/definitions/superagent-definitions.md`, [[STR-004]]), one new **read-only** judgement engine (`scripts/python/role-edge-check.py`) that answers edge existence, per-edge role sets, depth and violations from existing run records ([[STR-005]] record kind `role-edge`), a role-edge view inside the existing `status-digest.py` renderer, role fields added to the existing dispatch payload channels (`run-agent` injection list, team per-agent payload, driver stage envelope), and a tiny pointer section in `templates/instructions-template.md` inside the measured instruction budget. Concurrency, reporting and authorization keep their existing owners; this feature adds fields and pointers, not mechanisms (FR-035). The run's close-out additionally produces the 080–094 mechanism-observation appendix (FR-038).

## Technical Context

**Language/Version**: Python `>=3.8` (`pyproject.toml:5`); measured interpreter 3.11.11  
**Primary Dependencies**: standard library only for the new engine; `pytest` (existing) for tests; **zero new third-party dependencies** (FR-037)  
**Storage**: **none new** — role edges are projections over existing carriers: `.specify/state/<line>.md` status spines + driver stage envelope sidecars, `.specify/teams/<slug>/runs/<stamp>-report.md` dispatch mapping tables, `<DISPATCH_LOG_DIR>/<label>.status` artifact triplets, and the line-registry entry store (`$SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`) as a cross-check only (FR-003, FR-025, FR-026)  
**Testing**: contract + unit tests, single entry `.specify/scripts/bash/run-tests.sh` (default `-n <effective> --dist load`); tests must run on the `>=3.8` lower bound (FR-036, FR-037)  
**Target Platform**: framework source tree + the same files mirrored into the runtime `.specify/` tree of every downstream project (Two Hats)  
**Project Type**: code generator / prompt framework (docs + templates + engines), **not** a runtime platform (Principle IX)  
**Performance Goals**: N/A — the engine is a single-pass read over local records; the digest keeps its existing entry cap and renders in one pass  
**Constraints**: engine zero write points; digest keeps its single renderer and existing `nothing-running` / `omitted` / `stale` semantics; instruction budget `INSTRUCTIONS_BUDGET_BYTES` = 38,400 B with measured headroom **946 B** (live 37,454 B) — the new template section must fit inside it (FR-033, A13)  
**Scale/Scope**: 1 owner page (+3 pointer lines), 1 read-only engine, 1 digest view, 4 dispatch-surface field additions, 1 instructions section, ~6 contract test modules + 1 fixture set, 1 close-out observation appendix (FR-038)

### Design Decisions

| # | Decision | Rationale / authority |
|---|----------|----------------------|
| D-1 | New definition owner `shared/definitions/superagent-definitions.md` (framework source) mirrored to runtime; `agent-definitions.md`, `subagent-definitions.md`, `framework-map.md` gain **pointer lines only**; `better-harness.md` is **not** modified | FR-001, FR-032; requirements Clarifications (Session 2026-11-10, clarify Q6: `better-harness.md` 不改 — it is the improvement north star, not a role owner). The plan brief's "better-harness.md 增加指针" line contradicts this ruling; the requirements are the declared terminal authority, so the ruling wins (disclosed at wrap-up) |
| D-2 | The judgement face is a **new standalone read-only engine** `scripts/python/role-edge-check.py` (+ `.specify/scripts/python/` mirror), not an action bolted onto `line-registry.py`, `loop-state.py` or `status-digest.py` | FR-005, RS-004, A11; clarify Q1 (engine is the only judgement entry). The line registry owns the **write-line axis** and the clarify ruling requires the two axes to stay separate; `status-digest.py` must stay the only renderer; `loop-state.py` is driver-scoped while role edges are framework-wide. See T-001 |
| D-3 | Engine CLI: `--action report` (default; full model) and `--action query --parent <id> --child <id>` (pair answer); `--state-dir` (default `.specify/state`), `--teams-dir` (default `.specify/teams`), `--logs-dir` (default `.specify/agents/execution/logs`), `--registry-dir` (default as line-registry.py), `--format json\|text` (default json); `--help`, `--version`, undeclared-option rejection (Constitution XXI, applied even though a read-only script is outside the REQUIRED set) | FR-005, RS-004; contract `contracts/role-edge-engine.contract.md` |
| D-4 | Exit codes: `0` = judged clean (an explicitly stated empty set is clean), `1` = one or more violations, `2` = unreadable/malformed input **named** on stderr. Missing input roots are `2`, never a silent empty set | FR-005 ("不可读或缺失输入 MUST 以具名错误失败") |
| D-5 | Edge-record fields resolve to existing carriers: child identity = existing dispatch label (team/dispatch convention, `run-agent` label, driver `<line_id>-<stage>`); parent identity = the parent's own dispatch label, or for a root its existing run identity (status-spine `run_id`, else line-registry `line_id`, else the owner-declared fallback literal `root`); attempt = the existing attempt/iteration identifier. Same field disagreeing between two carriers → `conflict` naming both paths, never a silent pick | FR-003, FR-006; clarify Q1 (parent-side dispatch record is the primary carrier; the rest cross-check) |
| D-6 | Violation set is closed at four kinds — `self-dispatch`, `dangling-parent`, `unbacked-role-claim`, `depth-inconsistent`. The first three are exactly SC-001's red cases. FR-005's "深度越界" is operationalized as `depth-inconsistent` (a declared depth field contradicting the computed shortest distance, or a cycle making depth unresolvable) and **explicitly not** as a second authorization rule: role depth is unbounded and the SDD license-chain depth 2 keeps its owner (`subagent-definitions.md` § Dispatch-Time Governance Obligation) | FR-004, FR-005, SC-001; clarify Q7 (two orthogonal axes). Recorded as an implementation reading of FR-005 so the tasks phase does not invent a fifth kind |
| D-7 | Role depth = shortest edge distance from the root, unbounded; the engine also reports the declared `depth_position` carried in dispatch records and flags `depth-inconsistent` on disagreement | FR-004, SC-001 |
| D-8 | Digest role view: `status-digest.py` `project_entry` gains `parent`, `roles` (set, `dual-role` as the both-roles machine marker), `depth`; table and JSON output gain the corresponding fields; the role model is computed **once per digest run** by importing the engine's pure evaluation function and passing the digest's already-read registry entries (same single state read); `nothing-running`, `omitted`, `stale` semantics are unchanged; no second parser/renderer/dashboard | FR-029, FR-030, FR-031, SC-006; clarify Q4. Import precedent: `status-digest.py` already imports `exec-quant.py` |
| D-9 | Dispatch-surface additions are fields only: `run-agent` dispatch-injection block gains the [[STR-003]] pointer item; `create-team` Per-Agent Payload table gains a `role_fields` row and the report contract gains the mandatory dispatch mapping table `label \| role \| workspace \| parent`; `sdd-loop-driver` Driver Topology/U0.5 gains one [[STR-004]] pointer line and the stage envelope sidecar gains the six role fields; no new gate, no new dispatcher, no changed stage sequence/sentinel | FR-008, FR-030, FR-034, SC-002, SC-009; clarify Q2 |
| D-10 | `templates/instructions-template.md` gains a tiny `## Super Agent (相对逻辑角色)` section between `## Spec Kit Framework Map` and `## Spec Kit Runtime & Symlink Model`: one-sentence role statement + [[STR-004]] path + [[STR-003]] injection-existence declaration, **target ≤ 600 B**, must not contain the budget number or copied rules; order-of-magnitude measured: section ≈ 0.4–0.6 KB vs 946 B headroom. Degradation path: if `scripts/bash/generate-instructions.sh`'s budget report shows `over`, shrink to a one-line pure pointer (~200 B) — raising the budget is not a legal disposition (A7). `.specify/instructions.md` is produced by the generator, never hand-edited | FR-033, SC-007, A7, A13; clarify Q6 |
| D-11 | Zero second mechanism: no new persistence root, registry, renderer, dashboard, dispatcher or scheduler; the engine has zero write points, proven by a structural assertion (source scan for write-mode opens/mutations in the engine module) plus its read-only behaviour on fixtures | FR-035, SC-008 |
| D-12 | Close-out observation appendix lands at `.specify/specs/095-superagent-role/observation-appendix.md`; rows are one per existing 080–094 slice (14 slices measured on this tree), each `exercised` with a resolvable evidence path + reproducible machine record, or the literal `not-observed` ([[STR-006]]) with a reason. Configuration existence, conversation narrative and this feature's own artifacts are not evidence | FR-038, SC-010, A9; clarify Q8 |
| D-13 | Tests: new contract modules under `tests/contract/` + one declarative fixture set under `tests/fixtures/superagent-role/` (existing per-feature fixture convention); existing tests are dispositioned `rewrite / keep / remove` (remove only when the asserted fact is deleted by this feature); every execution goes through `scripts/bash/run-tests.sh` | FR-036, FR-037; Principle IV/XX |
| D-14 | Role-transition injection ([[STR-003]]) is a **closed nine-item pointer list physically present in the dispatch payload**, judged by extending the **existing** pre-dispatch self-check's substring form (`fast-fail.md` § 派发前自检; run-agent SKILL's dispatch-time injection block) to also require the `role-transition` identifier and its item ids — the judged identifier is new, the check form is not; the payload must not carry full manuals or skill-load instructions | FR-017, FR-018, FR-021, SC-002; see T-002 |

## Constitution Check

*GATE: pass before Phase 0 research, re-checked after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md`, all 22 headings in order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every decision D-1…D-14 cites an FR/SC or an owner path; Phase 1 artifacts derive from FR-001…FR-038 |
| II | Feature-Centric Development | ✅ Pass | Feature 095 bound; this plan run advances the index row Draft → Planned and appends the plan notes to `.specify/features/095-superagent-role.md` (create-plan's Feature Integration step) |
| III | Intent-Driven Development | ✅ Pass | Requirements (+10 clarify rulings) → plan; rationale recorded per decision |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Work Packages pair every behavior change with a contract test named before implementation (P1–P6 below) |
| V | AI Agent Integration Standards | ✅ Pass | No supported-agent roster, tier or CLI-flag change touches `src/specify_cli/__init__.py`; surfaces only gain pointer fields |
| VI | Continuous Quality & Observability | ✅ Pass | Read-only engine + digest view make the model observable; contract tests + mutation drills guard it |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This plan stays inside the workflow; status ceiling `Planned`; no `[ ]`-task claims made here |
| VIII | Code as the Single Source of Truth | ✅ Pass | Every referenced engine behaviour is measured on this tree (`status-digest.py --action` set, `loop-state.py` actions, registry record fields, generator budget) and cited in Phase 0 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One read-only script + docs/templates; zero new runtime, scheduler or persistence (FR-035, SC-008) |
| X | Documentation Naming & Location Conventions | ✅ Pass | Owner page under `shared/definitions/` with lowercase kebab-case name; no reserved filename used; spec-dir artifacts follow existing names |
| XI | Dogfooding (Self-Application) | ✅ Pass | All edits land in framework sources and ride the mirror/generator flow; runtime `.specify/` copies are produced by `sync-mirrors.py` / `generate-instructions.sh`, not hand-diverted |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Existing engines reused where they own the capability (`status-digest.py` renderer, `sdd-route.py` authorization); new engine justified under T-001 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | FR-038 appendix uses the evidence discipline (exercised / not-observed); no claim from configuration existence |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | New single owner ([[STR-004]]); all other surfaces carry pointer lines only (D-1, D-9, D-10) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Reader baseline inherited from the `Readers` / `Reading scenario` fields in `requirements.md` frontmatter; digest fields carry user-meaningful columns; quickstart written for the same baseline |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Engine fails named on unreadable input (D-4); the role-transition identifier is added to the **existing** pre-dispatch self-check's substring form (`fast-fail.md` § 派发前自检), as FR-018 requires — the form and its landing are existing, only the judged identifier is new (see D-14) |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | Only existing roots used (`shared/definitions/`, `scripts/python/`, `tests/contract/`, `tests/fixtures/<feature>/`); fixture dir follows the per-feature convention |
| XVIII | Grounded Naming | ✅ Pass | Engine name imitates `*-check.py` siblings and the STR-005 `role-edge` literal; terms follow glossary `Super Agent` entry and clarify A15 |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The role answer is reachable in one command (`role-edge-check.py --action query`); digest shows it directly |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | New tests are small contract/unit modules run through the parallel-default runner; no serial-only marker introduced |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | Engine answers `--help` / `--version` and rejects undeclared options before acting (D-3), pinned by contract test despite read-only exemption |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | Dispatcher anchor summary stays owned by `agent-definitions.md` § Re-Anchoring Obligation; new pointer lines reference it, never restate it |

**Gates Status**: ✅ All gates pass — no Complexity Tracking rows required.

**Re-check after Phase 1**: 2026-11-10 — re-verified against the landed Phase 1 artifacts: the engine contract keeps zero write points (XXI, IX); the four contracts reference rule owners by path and carry no copied owner tables (XIV — after the same-author gate's repair pass removed the restated budget literal, stale-bound literal and anti-nesting enumeration); the instructions section stays inside the measured budget (VII, A7). No row changed verdict; no Partial/Fail.

## Decision Tensions

Owner of the record shape, admissibility criteria, rejection forms and load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`. Fields used here: `decision`, `antithesis`, `binding_constraints` (`pole_a` / `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`.

### T-001 — 角色判定面是新独立只读引擎，而不是并入既有状态引擎

- **decision**: 角色-边判定落在新的独立只读引擎 `scripts/python/role-edge-check.py`，不并入 `line-registry.py`、`loop-state.py` 或 `status-digest.py`。
- **antithesis**: 给 `line-registry.py` 增加一个 `roles` 只读动作；当角色边与写线轴被同一批载体、同一批读者使用、且团队愿意只维护一个状态引擎入口时它更优——少一个入口、少一份解析代码，注册表记录里已有的 `parent_line_id` 可直接复用。
- **binding_constraints**:
  - pole_a: 角色边必须能横跨三种父侧载体（team 运行报告映射表、驱动状态脊 line+stage、`run-agent` label）判定，而 line registry 只读它自己的注册表存储。
  - pole_b: 写线轴与角色边轴必须分离（clarify 裁定）——把角色判定塞进写线引擎会让「扇出子项不是写线」这一事实被引擎结构暗示为可写线化。
- **discriminating_evidence**: 用一条与任何 `parent_line_id` 都不对应的角色边夹具运行两个设计：正确设计在独立引擎输出该边与角色集且 line registry 无新增记录；错误设计会迫使该边获得一条 line-registry 记录或拒绝判定。结果二值：分别成立 / 互相污染。
- **expected_sacrifice**: SC-008 Source ↓ 变更集结构审计将记录 **+1 个可执行引擎**（非 store、非 renderer、非 dispatcher）；多一个需要学习与维护的入口，是该取舍的直接代价。
- **revision_trigger**: 若两个独立父侧载体在同一事务范围内要求角色判定、或独立引擎与 line registry 的读取出现无法用只读协调解决的重复读取 ≥2 次 → 重开，重新评估并入方案。

### T-002 — 身份转变注入以派发载荷内的指针清单承载，而不是引用式按需加载

- **decision**: [[STR-003]] 九项以指针清单**物理存在**于派发载荷正文，由既有派发前自检按子串判定。
- **antithesis**: 载荷只带 owner 路径，子执行体在首次派发时自行加载 `superagent-definitions.md`；当载荷字节是唯一约束、且子运行时能可靠跟随引用时它更优——载荷最小、规则永远单点。
- **binding_constraints**:
  - pole_a: 常驻指令层到不了子代理（FR-018）——不物理存在就等于没注入。
  - pole_b: 反嵌套红线——载荷不得要求加载任何技能、不得携带完整驱动手册或循环逻辑（FR-017/FR-008）。
- **discriminating_evidence**: 夹具载荷删去九项之一 → 派发前自检（子串判定）非零阻断；夹具载荷加入「加载 superagent-definitions.md」指令 → 反嵌套契约测试转红。结果二值：两次判定各自成立 / 任一不成立。
- **expected_sacrifice**: SC-002 Source ↓ 载荷夹具将显示每次授职派发的载荷较无注入时增长（九项指针的固定字节）；代价按每次授职派发重复支付。
- **revision_trigger**: 若载荷体积在连续两个迭代中成为派发失败或截断的首要原因 ≥2 次 → 重开，评估压缩为标识符 + 单指针的形态。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/095-superagent-role/
├── plan.md              # This file
├── data-model.md        # Phase 1 output
├── contracts/           # Phase 1 output — 4 contracts
├── quickstart.md        # Phase 1 output
├── feature-ref.md       # Phase 1 output
├── observation-appendix.md  # implement close-out output (FR-038)
├── checklists/          # requirements-quality checklist (already present)
└── test-evidence/       # evidence captured by this feature's runs
No standalone research.md — Phase 0 findings are inlined in § Phase 0 below.
```

### Source Code (repository root)

```text
shared/definitions/                        # NEW owner page superagent-definitions.md; pointer lines in agent-definitions.md, subagent-definitions.md, framework-map.md
.specify/shared/definitions/               # runtime mirrors of the four definition pages (sync-mirrors.py, file-scoped)
scripts/python/                            # NEW read-only engine role-edge-check.py; role view in status-digest.py
.specify/scripts/python/                   # engine mirrors
templates/instructions-template.md         # tiny pointer section (§ D-10)
.specify/templates/instructions-template.md  # mirror (source → mirror)
skills/internal/run-agent/                 # dispatch-injection block + STR-003 pointer item
skills/internal/create-team/               # Per-Agent Payload role fields + report-contract dispatch mapping table
skills/external/sdd-loop-driver/           # SKILL.md topology pointer line + references/stage-prompts.md stage-envelope role fields
.specify/skills/internal/, .specify/skills/sdd-loop-driver/  # mirrors of the three skill surfaces
tests/fixtures/superagent-role/            # NEW declarative fixture set (edge/role/depth/violation + payload fixtures)
tests/contract/                            # NEW contract test modules (role edge, payload, digest view, definitions, budget, zero-mechanism)
.specify/features.md                       # Feature 095 row: Draft → Planned
.specify/features/095-superagent-role.md   # plan notes appended
.specify/specs/095-superagent-role/        # plan + Phase 1 artifacts + observation appendix (implement close-out)
```

**Structure Decision**: this feature extends the framework's existing document+engine surfaces in place — it adds one owner page beside its sibling definitions, one read-only engine beside its sibling `*-check.py` engines, one view inside the existing digest renderer, and field rows inside existing payload contracts. No new top-level directory is created; the only new directories are `tests/fixtures/superagent-role/` (per-feature fixture convention) and none elsewhere.

### Mirror Obligations

Baseline measured **before** any edit (2026-11-10): `python3 scripts/python/sync-mirrors.py --check` reports **428** DIFF/ORPHAN lines tree-wide. `.specify/shared/` carries **100** pre-existing modified files whose diff is a path-prefix rewrite inside prose (e.g. `shared/` → `.specify/shared/`, `scripts/` → `.specify/scripts/`), unrelated to this feature. The criterion below is therefore **"no NEW drift on the pairs this spec touches"**, not a global green.

> **Premises / execution status (per Verify row)**: the per-file sync commands are **executed during implementation** (P1–P5) and **pinned by `tests/contract/test_mirror_parity_suite.py`**, which is parametrized from `sync-mirrors.py`'s `MIRROR_PAIRS` and asserts each mirror twin is present and equal (or a declared projection). Premises: `--only` accepts an exact repo-relative source path as a prefix (measured `scripts/python/sync-mirrors.py:37-38`); the new `shared/definitions/superagent-definitions.md` resolves under the `shared` pair; the three pre-existing-dirty definition mirrors are normalized to source content by the same file-scoped sync (disclosed below). No exit code is pre-written — the criterion is **"no NEW drift on the pairs this spec touches"**, judged against the measured 428-line baseline.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify (criterion; pinned by) |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/superagent-definitions.md` (NEW) | `.specify/shared/definitions/superagent-definitions.md` | file-scoped sync → that pair clean under `--check --only`; parity pinned by `test_mirror_parity_suite.py` |
| `shared/definitions/agent-definitions.md` | `.specify/shared/definitions/agent-definitions.md` (pre-existing dirty — see baseline note) | same; the sync normalizes this file's pre-existing prefix rewrite as a disclosed side effect |
| `shared/definitions/subagent-definitions.md` | `.specify/shared/definitions/subagent-definitions.md` (pre-existing dirty — see baseline note) | same |
| `shared/definitions/framework-map.md` | `.specify/shared/definitions/framework-map.md` (pre-existing dirty — see baseline note) | same |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` | file-scoped sync → pair clean; live-file budget judged by the generator report, pinned by `test_instructions_budget_superagent_section.py` |
| `scripts/python/role-edge-check.py` (NEW) | `.specify/scripts/python/role-edge-check.py` | file-scoped sync → pair clean; mirror `--help` / `--version` pinned by `test_role_edge_engine.py` |
| `scripts/python/status-digest.py` | `.specify/scripts/python/status-digest.py` | file-scoped sync → pair clean; mirror digest behaviour pinned by `test_status_digest_roles.py` |
| `skills/internal/run-agent/SKILL.md` | `.specify/skills/internal/run-agent/SKILL.md` | file-scoped sync → pair clean; content pinned by `test_role_transition_payload.py` |
| `skills/internal/create-team/SKILL.md`, `references/patterns.md` | `.specify/skills/internal/create-team/…` | same |
| `skills/external/sdd-loop-driver/SKILL.md`, `references/stage-prompts.md` | `.specify/skills/sdd-loop-driver/…` | same |

No `.specify/templates/commands/` mirror exists (retired); this feature changes no `/speckit.*` command file, so `regen-command-copies.py` is not invoked. Disclosed: syncing the three pre-existing-dirty definition mirrors necessarily commits their pre-existing path-prefix drift in normalized (source) form; every other dirty file in the tree is left untouched and uncommitted.

## Execution Premises

Owner of this table's shape, its `Status` / `Decision` value domains and the invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this table carries the column set and measured values only.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | CPython `>=3.8` stdlib delivers everything the engine needs (path globbing, JSON, markdown-table line parsing) with zero new third-party dependency | `pyproject.toml:5` `requires-python = ">=3.8"`; measured interpreter `Python 3.11.11` | verified | — |
| EP-002 | The test suite runs through the single runner on the declared lower bound | `scripts/bash/run-tests.sh:319` exec line; `pyproject.toml` `testpaths = ["tests"]`; `tests/contract/` populated | verified | — |
| EP-003 | The four carrier families exist and are readable on this tree: status spine + stage artifact four-piece set under `.specify/state/`; team run reports under `.specify/teams/<slug>/runs/`; artifact triplets under `.specify/agents/execution/logs/`; line-registry entries at `~/.local/state/spec-kit/lines/*.json` | measured: `ls .specify/state/` shows `095-superagent-role.md` + `{pid,status,log,heartbeat,raw}-<line>-<stage>` files; `ls .specify/teams/skill-layer-install-separation/runs/` shows three reports; `.specify/agents/execution/logs` exists; registry dir holds `*.json` entries with `line_id` / `run_id` / `parent_line_id` / `line_role` fields | verified | — |
| EP-004 | The engine is new: no existing file occupies the chosen path, and no existing literal collision with `role-edge` as a record-kind slug | `ls scripts/python/role-edge-check.py` → no such file; STR-005 `role-edge` first registered by this spec | verified | — |
| EP-005 | Instruction budget headroom covers a ≤600 B pointer section | measured `wc -c`: `.specify/instructions.md` = 37,454 B, `templates/instructions-template.md` = 32,975 B, `INSTRUCTIONS_BUDGET_BYTES` = 38,400 (`scripts/bash/generate-instructions.sh:107`) → 946 B headroom | verified | — |
| EP-006 | `status-digest.py` is today a three-action engine (`digest` / `guard` / `report`) with an import precedent for shared engines (`exec-quant.py`) | measured `status-digest.py:2279` action choices; import site for exec-quant documented at `:100` | verified | — |

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain, the `Source row` / `Carrier` / `Carrier slice` grammar and the carrier's eligibility rule: `shared/workflow/acceptance-hardening.md` § Inherited Blockers.

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:

- `064`: `.specify/features/064-subagent-concurrency.md`, `.specify/specs/064-subagent-concurrency/verification.md`
- `088`: `.specify/features/088-speckit-visualization.md`, `.specify/specs/088-speckit-visualization/verification.md`
- `089`: `.specify/features/089-script-interface-contract.md`, `.specify/specs/089-script-interface-contract/verification.md`
- `090`: `.specify/features/090-re-anchoring.md`, `.specify/specs/090-re-anchoring/verification.md`
- `093`: `.specify/features/093-concurrency-by-default.md`, `.specify/specs/093-concurrency-by-default/verification.md`

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | `088:SC-009_status` | not-applicable | — | — | parent status `blocked` (supporting path): 088's blocked row asks for a real multi-minute dogfood run; 095 reuses the already-passing digest renderer and neither carries nor closes 088's supporting criterion |
| 2 | `093:SC-006_status` | not-applicable | — | — | parent status `blocked` (final path): 093's unblock condition is "a real run that dispatches ≥2 units and records their intervals". 095's own implementation run may incidentally produce such a reading, but 095's success criteria do not include carrying 093's row; claiming it here would be a configuration-existence inference |
| 3 | `093:SC-007_status` | not-applicable | — | — | parent status `partial` (supporting path): 093's missing team/loop concurrency fixture is 093's supporting gap; 095 adds no team/loop concurrency fixture and does not claim the row |
| 4 | `093:SC-010_status` | not-applicable | — | — | parent status `partial` (supporting path): 093's frozen-baseline reds sit outside 095's write domain; 095's own suites are judged on their own criterion (FR-036: no NEW red caused by this feature) |

## Complexity Tracking

N/A — no Constitution Check row is Fail or Partial; no justification table required.

## Phase 0: Research Review

Findings that shaped the design (all measured on this tree, 2026-11-10):

1. **Engines and their axes** — `line-registry.py` exposes 24 actions over `$REGISTRY/<line_id>.json` with `parent_line_id` / `line_role` fields and enforces parent-depth exactly one (write-line axis); `loop-state.py` exposes `snapshot` (read-only) / `recover` / `check-spine` (refusals) scoped to one line; `status-digest.py` exposes `digest` / `guard` / `report`, reads only line-registry entries + triplets, and already imports `exec-quant.py`. Conclusion: none of them owns a framework-wide role-edge judgement; the new standalone engine (D-2) is the only placement that keeps the axes separate.
2. **Digest contract surface** — `NOTHING_RUNNING = "nothing-running"` (`status-digest.py:94`), per-row `stale=yes|no` + "beyond the stale bound" note, `omitted=%d` + "另有 N 条未显示", JSON keys `entries` / `all_entries` / `omitted` / `state_summary`; contract owned by `.specify/specs/088-speckit-visualization/contracts/status-digest.contract.md` (C-41…C-46, DG-01…DG-07). The role view extends `project_entry` (`:310-328`) rather than adding a renderer (D-8).
3. **Dispatch surfaces** — `run-agent` SKILL has one bolded "Dispatch-time injection (mandatory)" block (only the fast-fail clause); concurrency / reporting / re-anchor obligations are cited from their owners. `create-team` builds member briefs from a Per-Agent Payload table (`references/patterns.md:102-113`) and writes run reports to `.specify/teams/<slug>/runs/<stamp>-report.md` with fixed sections — the mapping table must land **inside** `## Execution Detail` (no new top-level section). The driver builds stage prompts from `references/stage-prompts.md` with a `.meta.json` envelope sidecar and four-piece state artifacts named `<line_id>-<stage>` under `.specify/state/`.
4. **Artifact triplet + attribution** — label convention `<team-slug>--<run-stamp>--<member-role>`; triplet `<label>.live.log` / `.jsonl` / `.status` under `DISPATCH_LOG_DIR` (default `.specify/agents/execution/logs`); attribution values `own|foreign|stale-run|unattributed|legacy` and wait thresholds are owned by `watch-model.md` — referenced, never restated.
5. **Instruction generation** — the generator reconciles **missing whole sections** keyed by exact heading, inserts them in template order, never touches existing sections; budget report prints `BUDGET: <size> <budget> (over|within)` plus a per-section byte table; `INSTRUCTIONS_BUDGET_BYTES` is the only definition of the number; no contract test pins the section count (only set-containment). The new section therefore propagates by adding it to the template and running the generator (D-10).
6. **Mirror baseline** — 428-drift baseline with 100 pre-existing dirty `.specify/shared/` files carrying a path-prefix rewrite; file-scoped `--only` sync is available (exact path prefix match) and is the only safe write form. Disclosed in § Mirror Obligations.
7. **Feature registry** — row 095 exists (Draft); detail file carries the planned change list and the clarify notes; this run advances status to `Planned` and appends plan notes only.

**Subagent-unavailable fallback**: not triggered — three read-only Explore agents returned; their facts are cited above with paths.

## Work Packages (task boundaries for /speckit.tasks)

Six packages, each with disjoint write domain, ordered by dependency. Target ≤ 16 tasks per package.

| Package | Scope (write domain) | Depends on | Paired verification |
|---------|----------------------|------------|---------------------|
| **P1 — Definition owner + pointer lines** | `shared/definitions/superagent-definitions.md` (new); pointer lines in `agent-definitions.md` / `subagent-definitions.md` / `framework-map.md`; mirrors | — | `tests/contract/test_superagent_definitions.py`: owner exists both sides, declared ownership, required sections (role/edge/depth/protocol/injection/state/visualization/zero-mechanism/terminology), nine-item closed list, pointer-only discipline (no rule copy), depth-vs-license-chain sentence present |
| **P2 — Read-only role-edge engine** | `scripts/python/role-edge-check.py` (new); `tests/fixtures/superagent-role/`; mirrors | P1 (field semantics) | `tests/contract/test_role_edge_engine.py`: `--help`/`--version`/unknown-option; report/query JSON schema; role sets incl. `dual-role`; depth; four violation kinds; `conflict` with both paths; named error on unreadable input; determinism (same input twice); zero-write structural assertion; mutation drills (type-based classification red; injected violation red; self-dispatch red) |
| **P3 — Protocol & transition-injection wiring** | `skills/internal/run-agent/SKILL.md`; `skills/internal/create-team/SKILL.md` + `references/patterns.md`; `skills/external/sdd-loop-driver/SKILL.md` + `references/stage-prompts.md`; mirrors | P1 | `tests/contract/test_role_transition_payload.py`: nine-item presence in the injection template; delete-one → pre-dispatch self-check blocks; anti-nesting red (skill-load instruction); team mapping-row shape; driver envelope fields; dual-role return contract fields |
| **P4 — Digest role view** | `scripts/python/status-digest.py`; mirror | P1, P2 | `tests/contract/test_status_digest_roles.py`: identity/parent/roles/depth/status/age/stale fields in table + JSON; `omitted` on truncation; `nothing-running`; single-reader (import, no second store read); no second renderer (structural assertion) |
| **P5 — Harness landing** | `templates/instructions-template.md`; mirror; generated `.specify/instructions.md` (by generator) | P1 | `tests/contract/test_instructions_budget_superagent_section.py`: section present between the two fixed neighbours; pointer form (owner path, no budget literal, no copied rules); generator report `within`; live file carries the section |
| **P6 — Close-out: observation appendix + suite disposition** | `.specify/specs/095-superagent-role/observation-appendix.md`; existing-test disposition ledger in `verification.md` | P1–P5 | Row check: every existing 080–094 slice has an `exercised` row with resolvable path + machine record, or `not-observed`; mutation: mark an unobserved row `exercised` → check red; `tests/contract/test_superagent_zero_mechanism.py` (the six C-3 assertions of `contracts/harness-landing.contract.md`); full contract suite via `run-tests.sh` |

## Execution Record (this stage)

| Field | Value |
|-------|-------|
| `requested` | 3 (research wave: three read-only Explore subagents dispatched in one block) |
| `effective` | `not_evaluated` (no per-unit `dispatched_at` / `settled_at` interval record was captured for the research wave) |
| `effective_reason` | intervals absent — recorded per `effective-concurrency.yaml` `missing_interval_rule`; the write units (plan fill, Phase 1 artifacts, registry update, verification) ran serially under `dependency-edge` (each artifact depends on the previous) |

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed on disk (2026-11-10):

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 10 sections; 5 core entities (Role set, Role Edge, Executor node, Violation, Downlink fields) + 3 closed enumerations (violations 4, role-transition items 9, message classes 4) |
| Contracts | [`contracts/`](./contracts/) | 4 files: `role-edge-engine.contract.md`, `role-transition-payload.contract.md`, `status-digest-role-view.contract.md`, `harness-landing.contract.md` |
| Quickstart | [`quickstart.md`](./quickstart.md) | 4 scenarios (query, digest view, payload injection, budget verification) |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 095 binding + 6-row mapping (detail items → plan packages/contracts) |

Drift from the Phase 0 expectation: the artifact set matches the planned P1–P6 verification columns; the same-author gate then found and this run repaired 11 defects (wording overstatement about the self-check's existence, one unowned test module, three copied owner literals/enumerations, citation errors, and command-example coverage gaps — see `test-evidence/plan-stage-evidence.md` § Gate readings). Every command example in `quickstart.md` and in the three contract files that carry shell examples (`role-edge-engine`, `status-digest-role-view`, `harness-landing`; `role-transition-payload` carries none) has a per-example premise/status line (the engine and digest fields are not implemented yet; each example is pinned by the named contract test — deferred-execution route). The runnable-today facts quoted in this plan were measured, not assumed: the current digest output, `wc -c` sizes 37,454 / 32,975 / 38,400 B, and the 428-line mirror-drift baseline (captured in `test-evidence/plan-stage-evidence.md`).
