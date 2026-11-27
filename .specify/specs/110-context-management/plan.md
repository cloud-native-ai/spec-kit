# Implementation Plan: Context Management（上下文的声明、组合与只读审计）

**Branch**: `110-context-management` | **Date**: 2026-11-27 | **Spec**: `.specify/specs/110-context-management/requirements.md`
**Requirement → Feature**: `110-context-management` → Feature 110 Context Management（上下文管理）
**Input**: Specification from `.specify/specs/110-context-management/requirements.md` (29 FRs / 11 SCs; clarifications of 2026-11-27)

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## Summary

Land the ported context-management capability as one owner document plus one read-only audit engine over the
carriers that already exist: a machine-parsed owner at `shared/definitions/context-management-definitions.md`
(the concept and its bilingual definition sites, two categories, three layers, five materialization forms,
the layer landing contract, the one context layout table, the composition protocol, the closed trigger set,
the composer roles, the concept-pointer slot, the presence vocabulary and the red lines); four closed-set
declaration facts (categories, layers, forms, classes) registered through four append-only keys in
`shared/declarations/contract.yaml` and read through `declaration_reader.py`; and the deterministic stdlib
engine `scripts/python/context-audit.py` (`--action check` / `--action manifest --layer <layer>`) that
validates the layout roster, the layer and form tokens, the form-by-layer matrix and the cap references,
and prints per-row presence tokens (`present` or one of the four absence reasons). The mechanism composes
the invariant baseline once per session or line and the task layer per task, learns its triggers from
project records instead of polling, never restates the caps, never stores a context and never opens a
network connection; it ships with one ambient instructions section and five guard files, and replaces
none of the existing carriers it points at.

## Technical Context

**Language/Version**: Python >= 3.8, standard library only for the new engine; Markdown + the YAML
declaration subset for the owner document and the four facts
**Primary Dependencies**: none new — the engine reads the declaration layer in process through
`scripts/python/declaration_reader.py` and reuses the house script-interface helper
`scripts/python/script_interface_cli.py`; the composing agents reuse `memory-utils.py --action recall`,
the agent render path (`render_agents_for_tool`) and the instructions/constitution generators by pointer,
never by extension
**Storage**: no new store, cache, index or rendered artifact — reads the owner document, the four fact
files and existing workspace paths; writes nothing (FR-011)
**Testing**: `bash scripts/bash/run-tests.sh` (pytest; parallel default); four contract guard files plus
one integration fixture; a seeded-violation fixture per checked rule; the full-suite baseline is captured
once at implement
**Target Platform**: repository tooling (OS-agnostic Python); no per-CLI code
**Project Type**: framework / toolkit (templates + shared docs + declarations + scripts + tests), single
repository
**Performance Goals**: linear in the layout roster and its source paths; byte-identical output across
reruns on an unchanged tree; no network and no write in any action
**Constraints**: read-only containment (SC-002); offline (SC-005); no raw user text or conversation
content in any reading; no numeric cap of this feature's own (SC-006); exit `0` clean or emitted, `1`
integrity findings, `2` usage or unreadable input or an unknown/missing declaration member; a layout-table
token outside its domain is a finding, never an input error; the ambient instructions section MUST fit
the generator's existing budget — measured live `.specify/instructions.md` = 40,170 B against
`INSTRUCTIONS_BUDGET_BYTES=40960` (`scripts/bash/generate-instructions.sh:119`), i.e. ~790 B of headroom;
the budget is neither raised nor are existing sections trimmed — a section that does not fit is an anomaly
to surface (A-10, FR-025)
**Scale/Scope**: 1 owner document, 4 declaration facts + 4 registration keys, 1 read-only engine, 5 design
contracts, 5 guard files, 3 framework-map rows, 1 ambient instructions section, 3 load-bearing tensions,
10 execution premises, 14 inherited-blocker dispositions

**Execution record (concurrency)**: `requested=1`; `effective=not_evaluated`; `effective_reason=single-unit`
— one bounded assignment with no independent units to parallelize, and the stage assignment forbids
dispatching other agents; the host-internal in-process path is not a carrier, so no dispatch intervals
were produced and the reading is `not_evaluated` (never a number).

## Plan Assumptions

Plan-stage adjudications made under the unattended assignment (questions that would otherwise be asked
are answered here so later stages can proceed):

- **PA-1 — Presence is a path/metadata reading, never a content reading**: a row's presence is computed
  from source resolvability, readability and emptiness, plus bounded read-only probes on the system layer;
  the audit never reads document content, never prints discovered host values, and never performs
  relevance selection (FR-022, FR-024). All five presence tokens (`present`, `absent`, `unreachable`,
  `empty`, `not-evaluated`) are defined once in the new owner document because this repository has no
  prior owner for them (A-8); `Unobserved` still reaches its evidence-state owner by pointer.
- **PA-2 — Every layout row names at least one standing resolvable source**: the two `inline-digest` task
  rows keep a standing owner path as their presence witness (`task-statement` → the distillation protocol
  owner; `task-delta` → the ID register and the state root) while their ephemeral inputs contribute no
  standing source and never turn a row absent. This is what makes "every row reads `present` on the
  all-sources-present fixture" mechanically reachable.
- **PA-3 — The classes fact and the layout table are the sanctioned pair**: `context-classes.yaml` owns the
  machine roster (layer → ordered class ids); the owner document's layout table is the only home of the
  per-row data (`source`, `form`, `owner`, `cap reference`); the engine validates them row-for-row and
  reports a mismatch as a finding. No third layout data file exists (FR-004, FR-018); the pair is the
  only two-representation surface and is guarded.
- **PA-4 — The system layer's probes are stdlib-only and side-effect-free**: platform/architecture/
  interpreter identity reads, a `PATH` + shell lookup, and a readability check of the workspace root.
  Network availability is never probed — the audit itself proves offline operation by opening no socket
  (FR-024, SC-005). Probe identifiers are engine schema, not a value domain.
- **PA-5 — Resolution has two roots, and the layer root follows the audited tree**: the workspace root is
  `--workspace-root` or the nearest ancestor holding `.specify/`; the layer root (owner document + facts)
  is **the resolved workspace root's own declaration layer** — `<workspace-root>/shared/` when that
  framework-source layer (`shared/definitions/context-management-definitions.md` plus the four
  `shared/declarations/facts/context-*.yaml` files) is present, else `<workspace-root>/.specify/shared/`
  (installed shape). One rule serves the framework source tree (`shared/…`), a client project or fresh
  init tree (`.specify/shared/…`) and a seeded fixture that carries its own minimal owner document and
  facts. Running without `--workspace-root` inside an install resolves the workspace root to that
  install, so engine, owner document and facts still pair; a tree with no declaration layer under its
  workspace root is the input error of C-016, never a fallback to another root. Mirrors keep the repo's
  two shapes byte-identical.
- **PA-6 — No numeric cap value enters this feature's artifacts**: every `bounded-index` row cites the cap
  owner path plus section, and every content-bearing row (`read-in-full`, `inline-digest`) cites the same
  section as its exception owner (`shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First));
  SC-006's repository scan checks that no new numeric cap literal appears.
- **PA-7 — `--action check`'s rule set is closed at nine**: roster membership and order, layer and form
  token domains, the form-by-layer matrix, class-id uniqueness, non-empty layers, cap-reference presence
  on `bounded-index` rows, and the absence of a category column. Each rule gets its own seeded-violation
  fixture at implement (FR-027); the four fixtures named by SC-001 are the unknown-layer, unknown-form,
  roster-mismatch and layer-form cases. All nine rules are findings (exit `1`); an unknown or missing
  member of a **declaration fact** is the input error of C-016 (exit `2`) and never a finding.
- **PA-8 — Ambience lands through the existing generator, inside the existing budget**: the new
  `## Context Management(上下文管理)` section enters `templates/instructions-template.md` and is propagated
  into the live `.specify/instructions.md` by `scripts/bash/generate-instructions.sh`'s additive reconcile;
  the generator's own `BUDGET:` report is the judge. Per A-10 the constant is not raised and existing
  sections are not trimmed; the measured ~790 B headroom (R-5) bounds the section's size, and a section
  that does not fit is surfaced as an anomaly rather than silently escalated. Any existing contract test
  that pins instructions section counts is re-measured and re-pinned in the same implement change (RU-3).
- **PA-9 — The dispatch payload is untouched**: the plan changes no field, injection, cap, identifier or
  self-check item of `shared/definitions/superagent-definitions.md` § The super↔sub Protocol; the
  concept-pointer slot maps onto existing channels (`authority_ref` pointer field + the child's ambient
  Documentation Map glossary row + the dispatch brief's reading list; A-15), and a guard asserts the
  protocol's declared item set (seven role fields, four injections) is unchanged (C-042).
- **PA-10 — Determinism is designed in**: rows print in roster order, no timestamps or host values enter
  the output, JSON keys are ordered, and multi-source rows report the first failing source in the declared
  source order; the manifest's `source-reading` digest covers declared sources' metadata only.
- **PA-11 — Same-author scoring fallback**: the no-dispatch assignment makes a fresh-context delegated
  review impossible for this run; the Constitution Check and the Post-Generation review are a disclosed
  direct self-read (the objective-analysis gate's fallback path), recorded per row in `research.md` R-10.
- **PA-12 — Exit-code discipline is the house pattern**: `check` uses `0` clean / `1` findings / `2`
  usage, unreadable input or an unknown/missing declaration member; `manifest` uses `0` whenever a
  manifest is emitted (absence rows included) and `2` on usage or declaration failure; an unreadable owner
  document or declaration layer is an input error, never a partial manifest.
- **PA-13 — Registration is deferred by line constraint**: this run writes no `.specify/features.md` row,
  no feature detail, no `.specify/register.md` row and no decision-archive entry (A-2; brief). Feature 110
  is the fixed binding; the index row, detail file, status advance and any decision/register rows are a
  recovery point for the line close-out's Feature Integration Protocol — see § Feature Integration.
- **PA-14 — Fresh-init anchors are measured, not assumed**: a fresh `specify init` tree carries
  `.specify/constitution.md`, `features.md`, `features/`, `workflow/git.md`, `tools.md`, `shared/`,
  `agents/`, `scripts/`, `templates/`, `memory/` and `source.json`, and lacks `instructions.md`,
  `glossary.md`, `register.md`, `skills.md`, `tools/`, `session/`, `knowledge/`, `state/` and `docs/`
  (probe 2026-11-27, R-9); the manifest reports those absences honestly per FR-020 and the plan assumes
  no anchor the CLI does not produce.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0, 23 principles in order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every contract clause serves an FR of `requirements.md` (29 FRs / 11 SCs); `feature-ref.md` carries the FR→clause→carrier map |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 110 (A-2); the registry advance is deferred by the line constraint and recorded in § Feature Integration, not silently skipped |
| III | Intent-Driven Development | ✅ Pass | Requirements plus the 2026-11-27 clarifications drive the design; no code-first choice |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Five guard files planned red-first; a seeded-violation fixture per checked rule (contracts C-040…C-046) |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster or tier change; ships as shared docs + declarations + one stdlib engine |
| VI | Continuous Quality & Observability | ✅ Pass | Deterministic output, documented exit codes, drift guards and the `source-reading` digest; whole-run acceptance via the full suite; no `.bak` copies |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE: Workflow Gates) | ✅ Pass | Phase discipline followed; status ceiling is `Planned`; deferred registrations recorded rather than dropped; no status regression |
| VIII | Code as the Single Source of Truth | ✅ Pass | Value domains read from declarations at run time; the engine fails on drift instead of trusting a copy; every carrier claim re-verified against code (R-1, R-9) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One read-only engine + docs + facts; no store, composer, renderer, scheduler, watcher or network (C-045) |
| X | Documentation Naming & Location Conventions | ✅ Pass | Owner doc lowercase kebab-case under `shared/definitions/`; fact files `<fact-slug>.yaml`; no reserved names; path-is-semantic |
| XI | Dogfooding (Self-Application) | ✅ Pass | Framework-source edits only, riding publish → install → init; guards pin the mechanism, not a live-file patch |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the declaration reader, the script-interface helper, Tool records (`.specify/tools/` preferred for command discovery, FR-006) and existing owners by pointer; one new read-only engine is the requirement's own entry |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Task Understanding (declared baseline) and Change Validation (deterministic audit); absence stays honest |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Owner doc (meanings + layout) + four facts (domains) + engine (schema) split fixed in C-001/C-010/C-030; every other surface points; the sanctioned table/fact pair is guarded (PA-3) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The audit's human output is designed against the comprehension owner by pointer; contract C-033 bounds its vocabulary and absence lines |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Triage owner untouched; the run records its own anomaly line at wrap-up; no anomaly-detection engine |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory is created — every new file lands in an existing, documented directory; no scratch root is added |
| XVIII | Grounded Naming | ✅ Pass | User terms carried verbatim ([[STR-001]]…[[STR-006]]); machine tokens fixed by the declarations; remaining names imitate siblings |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | One documented entry (`context-audit.py` with two actions); names state meaning (`check`, `manifest`, class ids); one information dimension added (the manifest) |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | Guards are fixture-scoped under the runner and executed through `scripts/bash/run-tests.sh`; no serial-only new file |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | The engine answers `-h`/`--help`/`--version`, rejects undeclared options non-zero and writes nothing (C-030/C-031) |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | The stage anchor and rule digest were carried through; rules re-read at step boundaries; the `reentry` trigger maps onto the existing re-anchoring tiers (C-028) |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | AI-written change follows the merged-history AI review; `.specify/workflow/git.md` remains the trunk/branch authority |

**Gates Status**: ✅ All gates pass — no Complexity Tracking entries required.

**Re-check after Phase 1**: 2026-11-27 — re-read against the landed design artifacts (`data-model.md`,
`contracts/` ×5, `quickstart.md`, `feature-ref.md`, `research.md`); every row above still holds; no
Partial/Fail row was produced, so Complexity Tracking stays `N/A`. Scoring was a direct self-read under
the no-dispatch assignment (PA-11), not a delegated fresh-context pass.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing
threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository
root (the same form this template uses for `.specify/constitution.md`); a plan artifact lives
under `.specify/specs/<key>/`, so a plan-directory-relative link would resolve to a path that does
not exist. This section lists the field names and points at that file — it MUST NOT restate the
criteria table, the rejection list or the threshold table.*

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`),
`discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; record identifier `tension_id`
(`T-NNN`).

### T-001 — 布局表以 owner 文档为唯一书写处，类花名册由声明事实机器拥有并逐行核对

- **decision**: 每行的 source、form、owner 与 cap reference 只写在 owner 文档的布局表里；`context-classes.yaml` 只拥有 layer→有序 class id 的机器花名册；引擎解析两者并逐行核对，不匹配即 finding，不新增第三个布局数据文件。
- **antithesis**: 把完整布局行搬进 `context-classes.yaml` 的 mapping statement，owner 文档只留含义说明；当维护者希望改值不碰散文、并让全部值域统一落在声明层时它更优。
- **binding_constraints**:
  - pole_a: FR-004 规定布局表是逐行数据（source / form / owner / cap reference）的唯一书写处并禁止第二个布局数据文件，class-id 列是花名册的投影、必须逐行匹配——阅读者与程序必须面对同一张表。
  - pole_b: FR-018 规定四个声明事实拥有机器值域并经 `declaration_reader.py` 读取，花名册必须可被引擎机器读取。
- **discriminating_evidence**: 一位复核者在 scratch 副本把 `context-classes.yaml` 中某一层的最后一个 class id 与相邻项对调并运行一次 `check`：输出是否恰好出现一条 roster/order finding 且点名该行、且不出现其它 finding；结果二值：是 / 否。
- **expected_sacrifice**: SC-001 Source ↓ 相比纯声明层方案，每次布局修订都要同时触碰 owner 文档表格与花名册，并多付一条表形守卫的维护成本。
- **revision_trigger**: 若连续两次布局修订都因表格形态改动导致引擎解析失败，或花名册核对两次因纯排版调整误红 → 重开，把逐行数据迁入声明事实并在 owner 文档只留含义。

### T-002 — 审计只读路径与在场状态，从不读取内容，也不打印发现到的宿主值

- **decision**: manifest 的在场判定只依据来源路径的可解析、可读与空/非空，加上系统层的只读探针；引擎不读取文档内容、不作相关性选择、不打印探针观察到的值。
- **antithesis**: 内容级校验的审计——读取治理文档与索引内容并校验其形态与关键条目；当使用者更想要语义层面的保证、并接受原文读取时它更优。
- **binding_constraints**:
  - pole_a: FR-024 规定任何 reading 不消费原始用户文本或会话内容，审计只消费路径、元数据与在场状态；FR-022 禁止引擎做语义选择。
  - pole_b: 语义保证能发现「指针仍在但内容已失效」，比只在场判定提供更强的可信度。
- **discriminating_evidence**: 一位复核者把某一 row 的 source 指向一个路径可解析但内容与职责无关的文件并运行 `manifest`：该行是否仍读 `present`、`check` 是否仍 exit 0；结果二值：是 / 否。
- **expected_sacrifice**: SC-010 Source ↓ 一致性声明只覆盖指针在场与可解析，内容陈旧由复审或其它 owner 报告，不由审计声称。
- **revision_trigger**: 若连续两轮复审出现「路径可解析但治理来源已失效」导致下游错误决策，或 FR-024 经修订允许内容读取 → 重开。

### T-003 — 概念指针槽位搭既有通道（基线三行 + `authority_ref` / Documentation Map / 简报阅读清单），不给派发载荷加字段、注入、上限、标识或自检项

- **decision**: glossary / definitions / explanations 三元指针槽位由项目层三行（`project-vocabulary`、`concept-definitions`、`concept-explanations`）在基线中承载，派发边沿用既有 `authority_ref` 指针字段、子代理 ambient 的 Documentation Map glossary 行与派发简报的阅读清单；`superagent-definitions.md` § The super↔sub Protocol 的七角色字段与四项注入一律不变。
- **antithesis**: 在派发载荷里新增一个专用字段或自检标识来携带三元组；当需要每条派发边都显式看到槽位且拥有自己的在场检查时它更优。
- **binding_constraints**:
  - pole_a: FR-028 与 FR-017 明令槽位映射不得给协议增加角色字段、注入、上限、标识或自检项，且载荷 owner 不被重定义。
  - pole_b: 专用槽位能让每条派发边不依赖基线即可显示三元组在场，免去「基线未组合则槽位不可见」的盲点。
- **discriminating_evidence**: 一位复核者在本次改动前后对 `shared/definitions/superagent-definitions.md` § The super↔sub Protocol 的字段清单与注入清单做一次机器比对：集合是否逐项未变；结果二值：未变 / 变化。
- **expected_sacrifice**: SC-010 Source ↓ 槽位在派发边的在场只能通过基线与既有通道证明，不能逐载荷字段核验；跳过基线的派发只能由守卫与复审兜底。
- **revision_trigger**: 若封闭结构集中某一受治理结构经查没有任何既有通道能承载三元组，或载荷 owner 自身修订接纳专用槽位 → 重开。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/110-context-management/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (standalone; findings R-1…R-10 + residual unknowns RU-1…RU-3)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── requirements.md      # /speckit.requirements + /speckit.clarify output
├── checklists/          # requirements-quality checklist
├── checkpoints/         # stage checkpoints (driver-side records)
├── test-evidence/       # stage evidence (this plan's gate captures included)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
shared/definitions/                    # NEW context-management-definitions.md (the owner document; machine-parsed layout table)
                                       # EDIT framework-map.md (owner-doc row, value-domains row, audit-entry row)
shared/declarations/                   # EDIT contract.yaml (four append-only registration keys)
shared/declarations/facts/             # NEW context-categories.yaml, context-layers.yaml, context-forms.yaml, context-classes.yaml
scripts/python/                        # NEW context-audit.py (read-only engine: --action check | manifest)
templates/                             # EDIT instructions-template.md (one ambient section)
.specify/shared/, .specify/scripts/,   # generated mirrors of the above (never hand-edited)
  .specify/templates/
.specify/instructions.md               # regenerated by scripts/bash/generate-instructions.sh (generated copy)
tests/contract/                        # NEW test_context_management_owner.py, test_context_management_declarations.py,
                                       #     test_context_management_engine.py, test_context_management_readonly.py
tests/integration/                     # NEW test_context_management_init.py (fresh init fixture, offline)
tests/fixtures/context-management/     # NEW fixture family; each fixture carries its own minimal owner document + four facts
```

**Structure Decision**: extends the existing framework-source layout (shared docs + declarations + scripts
+ tests + one template edit); no new directory is created, no new runtime store root appears, and
`.specify/` gains only mirror copies plus the regenerated instructions file. The two hats rule applies:
every content edit lands in the framework sources and rides publish → install → init; `.specify/` copies
are generated. `.specify/features.md`, `.specify/features/` and `.specify/register.md` are **not** edited
by this run (PA-13) — the feature registration is deferred to § Feature Integration.

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

Baseline measured before the edit (2026-11-27): `python3 scripts/python/sync-mirrors.py --check` exit 0 —
all six pairs byte-identical (templates 23 files, skills/external 439, skills/internal 139, agents 20,
scripts 133, shared 117) and six per-file projections `ok` (captured in
`test-evidence/mirror-baseline-plan.txt`). The implementation-time criterion is **no NEW drift on the
pairs this spec touches**, judged against that baseline — never a pre-written absolute exit code.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/context-management-definitions.md` (new) | `.specify/shared/definitions/context-management-definitions.md` | `sync-mirrors.py --check` — no NEW drift vs the 2026-11-27 baseline |
| `shared/definitions/framework-map.md` (edit) | `.specify/shared/definitions/framework-map.md` | pair check; the three new rows appear in both copies |
| `shared/declarations/facts/context-categories.yaml`, `context-layers.yaml`, `context-forms.yaml`, `context-classes.yaml` (new) | the same four paths under `.specify/shared/declarations/facts/` | pair check; the engine reads the facts through `declaration_reader` on both copies |
| `shared/declarations/contract.yaml` (edit) | `.specify/shared/declarations/contract.yaml` | pair check; the four registration keys appear in both copies |
| `scripts/python/context-audit.py` (new) | `.specify/scripts/python/context-audit.py` | pair check; `--version` answers on both copies |
| `templates/instructions-template.md` (edit) | `.specify/templates/instructions-template.md` (mirror pair); `.specify/instructions.md` via `bash scripts/bash/generate-instructions.sh`; `AGENTS.md` & other tool files are symlinks into `.specify/instructions.md` (no separate copy) | the section heading appears verbatim in template and live file; the generator's `BUDGET:` line is the judge and MUST read `within` under the unchanged constant (PA-8) |

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this skeleton carries the column set and nothing else, so a value domain written here would be a second definition.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The existing carriers the mechanism composes from are present and are the right base: the super↔sub protocol and its declared payload, the agent render path, memory recall, the declaration layer, the instructions generator and the init/mirror flow (requirements A-14) | `shared/definitions/superagent-definitions.md` § The super↔sub Protocol (measured: seven role fields, four injections); `src/specify_cli/__init__.py:648` `render_agents_for_tool`; `scripts/python/memory-utils.py`; `shared/declarations/contract.yaml`; `sync-mirrors.py --check` exit 0, 2026-11-27 (`test-evidence/mirror-baseline-plan.txt`) | verified | — |
| EP-002 | The declaration layer accepts four new facts (three `closed-set`, one `mapping`) with no code change, and `declaration_reader.py` reads them | `shared/declarations/contract.yaml` `required_fact_keys` / `fact_kinds` / `exit_codes`; sibling facts `memory-types.yaml`, `runtime-store-layout.yaml`; measured `--action get` output 2026-11-27 (`test-evidence/plan-time-reads.txt`) | verified | — |
| EP-003 | The owner document can serve as a machine-parsed registry with fixed table shapes, and an ambient-section guard has a live precedent to imitate | `scripts/python/probe-utils.py` parses the table registry in `shared/definitions/probe-definitions.md`; `tests/contract/test_instructions_section_propagation.py` (section-presence, pointer-shape and template-side mutation legs) | verified | — |
| EP-004 | Mirrors and `specify init` deliver the `shared/`, `scripts/` and `templates/` trees into a client project with no extra step | `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` (six pairs); init copies measured in `src/specify_cli/__init__.py`; `--check` exit 0, 2026-11-27 | verified | — |
| EP-005 | The instructions generator reconciles a new top-level template section into an existing live file additively and reports a budget verdict | `scripts/bash/generate-instructions.sh` (`INSTRUCTIONS_BUDGET_BYTES=40960` line 119; `BUDGET:` line); `tests/contract/test_instructions_section_propagation.py` (live-presence and additive-injection legs); measured live 40,170 B, template 39 / live 40 sections | verified | — |
| EP-006 | The read-only engine can perform its system-layer probes with the Python standard library alone, without network or writes | `platform` / `sys` / `os` / `shutil.which` are stdlib; existing engines (`flow-class-check.py`, `declaration_reader.py`) share the read-only stdlib-only shape; measured `flow-class-check.py --version` → `flow-class-check.py 0.0.22` | verified | — |
| EP-007 | The plan-side gate requirements (Execution Premises, Inherited Blockers, count claims, runtime premises citations) are satisfiable from this artifact set | `pre-analyze-check.py --stage plan` run in this stage; capture `test-evidence/pre-analyze-plan.txt` | verified | — |
| EP-008 | The task-layer standing sources exist on this tree (`register.md`, state root, memory tiers, docs tree) so the repository's own manifest can read every row | measured reads on `.specify/register.md`, `.specify/session/` (579 entries), `.specify/knowledge/` (9 entries), `docs/` (present, 2026-11-27); `.specify/state/` is absent in this worktree — the `task-delta` row reads an absence token with a reason by design | verified | — |
| EP-009 | The four registration keys and the three framework-map rows land in files owned by existing owners that accept append-only edits | `shared/declarations/contract.yaml` lines 64–77 (093/105 append-only precedent); `shared/definitions/framework-map.md` table shape | verified | — |
| EP-010 | A fresh init tree's anchor set is measured, not assumed | scratch init probe 2026-11-27 (R-9): fresh tree carries `constitution.md`, `features.md`, `features/`, `workflow/git.md`, `tools.md`, `shared/`, `agents/`, `scripts/`, `templates/`, `memory/`, `source.json`; lacks `instructions.md`, `glossary.md`, `register.md`, `skills.md`, `tools/`, `session/`, `knowledge/`, `state/`, `docs/`; installed CLI 0.0.22 predates this feature | verified | — |

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain, the `Source row` / `Carrier` / `Carrier slice` grammar and the carrier's eligibility rule: `shared/workflow/acceptance-hardening.md` § Inherited Blockers — this skeleton carries the column set and nothing else. The dependency set these rows are extracted from MUST be declared in this section, either as the literal `**Dependency artifacts (declared, never implied)**` block or as the exact sentence `Dependency set: none`.

The dependency set is declared in the marker block below; the grammar and the extraction set are owned by
`shared/workflow/acceptance-hardening.md` § Inherited Blockers and are not restated here. Feature 055's bound
spec carries requirements only — no `verification.md` exists — so its detail is declared alone.

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:

- `040`: `.specify/features/040-token-efficiency-discipline.md`, `.specify/specs/035-token-efficiency/verification.md`
- `044`: `.specify/features/044-agent-metadata-portability.md`, `.specify/specs/040-agent-metadata-portability/verification.md`
- `051`: `.specify/features/051-user-facing-comprehension.md`, `.specify/specs/051-user-facing-comprehension/verification.md`
- `055`: `.specify/features/055-conflict-free-stores.md`
- `084`: `.specify/features/084-harness-triple-structure.md`, `.specify/specs/084-harness-triple-structure/verification.md`
- `089`: `.specify/features/089-script-interface-contract.md`, `.specify/specs/089-script-interface-contract/verification.md`
- `090`: `.specify/features/090-re-anchoring.md`, `.specify/specs/090-re-anchoring/verification.md`
- `091`: `.specify/features/091-auto-git-closeout.md`, `.specify/specs/091-auto-git-closeout/verification.md`
- `093`: `.specify/features/093-concurrency-by-default.md`, `.specify/specs/093-concurrency-by-default/verification.md`
- `095`: `.specify/features/095-superagent-role.md`, `.specify/specs/095-superagent-role/verification.md`
- `105`: `.specify/specs/105-runtime-store-layout/verification.md`

**Excluded, with basis**: Feature 110's own artifacts are never dependencies of itself; Feature 033
(agent project-context parameterization, `Draft`) is an architectural neighbour only — its target-project
`## Project Context` refresh is not delivered, and this feature references only the standing block the
render path (044) emits; Feature 046 (confirmation gates) and 052 (fast fail) are pointer-only constraint
owners whose measurements are not inherited; Feature 069/077 (flow class) contributes the class
declaration, not a runtime carrier; Feature 086 (efficient test execution) is the test entry, not a runtime
carrier; Feature 008's generator flow is consumed without inheriting its measurements; Feature 094's
`registered_facts` form is not used (the flat append-only keys are 084's precedent). The eleven declared
dependencies are the owners whose carriers the mechanism references: the cap owner (040), the render
pipeline (044), comprehension/glossary (051), memory stores (055), the declaration layer and framework map
(084), the script-interface rule (089), re-anchoring (090), the git-workflow declaration (091), the
concurrency obligation (093), the super↔sub protocol (095) and the store roster (105).

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | `035:SC-004_status` | not-applicable | — | — | The partial leg is a human spot-check of remediation flows adopting the token-efficiency discipline; this feature consumes the discipline only as the cap/exception owner (C-013) and makes no adoption claim — `.specify/specs/035-token-efficiency/verification.md` |
| 2 | `051:SC-001_status` | not-applicable | — | — | The deferred leg is a human sampling review of governance-kept gate prompts; this feature ships no gate-prompt wording — `.specify/specs/051-user-facing-comprehension/verification.md` |
| 3 | `051:SC-002_status` | not-applicable | — | — | The partial leg is a surface-wide prose count of engine-call forms; this feature's new surfaces are machine-checked by its own guards — same file |
| 4 | `051:SC-005_status` | not-applicable | — | — | The partial leg is a downstream bootstrap drill for the comprehension charter; this feature's distribution leg is its own init fixture (SC-005) — same file |
| 5 | `051:SC-006_status` | not-applicable | — | — | The deferred leg needs two independent reviewers' agreement rate; this feature claims pointer presence only and makes no agreement claim (FR-028) — same file |
| 6 | `051:SC-007_status` | not-applicable | — | — | The partial leg is a length-distribution sample of suggestion lines; this feature emits no suggestion line — same file |
| 7 | `051:SC-018_status` | not-applicable | — | — | The partial leg is an unresolved counting interpretation of class-level overrides; this feature declares no reader-baseline override — same file |
| 8 | `051:deferred_tasks` | not-applicable | — | — | The deferred tasks (T034, T060, T061) are human/environment-dependent rows of that feature; this feature takes no dependency on their completion — same file |
| 9 | `084:SC-003_status` | not-applicable | — | — | The deferred leg is a waived negative-fixture run of the triple check's six-reason proof; this feature consumes the declaration layer's reader and facts — live and green for their scope — and runs its own contract suite for the new engine — `.specify/specs/084-harness-triple-structure/verification.md` |
| 10 | `084:SC-005_status` | not-applicable | — | — | The partial leg is a user-waived init scratch-tree proof; this feature re-measures downstream distribution independently in its own init fixture (FR-023) — same file |
| 11 | `084:SC-006_status` | not-applicable | — | — | The partial leg is an unread zero-new-failure count from a waived budget; this feature captures its own full-suite baseline at implement (SC-008) — same file |
| 12 | `093:SC-006_status` | not-applicable | — | — | The blocked leg requires a real ≥2-unit concurrent run with recorded intervals; this port runs single-unit (`effective=not_evaluated`, PA-11) and inherits no concurrency-effectiveness claim — `.specify/specs/093-concurrency-by-default/verification.md` |
| 13 | `093:SC-007_status` | not-applicable | — | — | The partial leg is executable team/loop concurrency fixtures; this feature is a single-line additive port with no team/loop dispatch — same file |
| 14 | `093:SC-010_status` | not-applicable | — | — | The partial leg is whole-suite green on that tree with inherited reds outside its write domain; this feature captures its own baseline at implement (SC-008) — same file |

## Feature Integration

The `create-plan` skill normally advances the bound feature `Draft → Planned` in `.specify/features.md`
and keeps its detail file current. This run is under the line constraint "no spine/registry edits"
(A-2; brief), and Feature 110 currently has **no** row in `.specify/features.md` and no detail file (A-2
records why the binding still stands). Therefore this stage writes neither, and also writes no
`.specify/register.md` row and no decision-archive entry. The registration set — the index row, the
`.specify/features/110-context-management.md` detail (from `.specify/templates/feature-details-template.md`),
the status advance, and any decision/register rows the three tensions would normally coin — is handed to
the line close-out's Feature Integration Protocol as a recovery point, to be reconciled against this spec
and the tree at that time. Downstream stages MUST NOT read the absent row as "the feature does not exist";
the binding is Feature 110, fixed.

## Complexity Tracking

N/A — no Constitution Check violation requires justification.

## Phase 0: Research Review

Phase 0 findings are recorded in `research.md` (standalone): R-1 the existing carrier interfaces (the
super↔sub protocol's real payload, the render path, memory recall, the declaration layer); R-2 the
four-fact fit against `shared/declarations/contract.yaml` with the append-only registration form; R-3 the
machine-parsed owner-document precedent and the ambient-section guard pattern; R-4 the mirror/init
distribution route with its measured 2026-11-27 baseline; R-5 the instructions ambient-section generation
and the measured ~790 B budget headroom; R-6 the script-interface and exit-code rules; R-7 the presence
vocabulary (no prior owner; defined once) and the evidence-state `Unobserved` reading; R-8 the containment
and closed-set-claim disciplines applied to SC-002/SC-008; R-9 the pre-analyze plan-gate mechanics and the
fresh-init anchor probe; R-10 the same-author fallback and the registration deferral. Residual unknowns are
listed there as RU-1…RU-3. No unresolved clarification marker remains.

## Phase 1: Design Artifacts Summary

Counts below were taken from the landed files on disk after the artifacts were written, by the enumeration
commands shown (run 2026-11-27 in this stage, from this spec directory). Each pattern matches only its own
file's structural headings/rows.

```text
$ ls contracts/*.md | wc -l
5
$ grep -cE '^## E-[0-9]+' data-model.md
11
$ grep -cE '^- \*\*I-[0-9]+' data-model.md
14
$ grep -cE '^## Scenario' quickstart.md
6
$ grep -cE '^\| FR-[0-9]{3} ' feature-ref.md
29
$ grep -cE '^\| SC-[0-9]{3} ' feature-ref.md
11
$ grep -cE '^## R-[0-9]+' research.md
10
$ grep -cE '^- \*\*RU-[0-9]+' research.md
3
```

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 11 entities (E-1…E-11) + 14 cross-entity invariants (I-1…I-14) |
| Contracts | [`contracts/`](contracts/) | 5 files: owner-and-layout (C-001…C-007), declarations-and-domains (C-010…C-016), matrix-and-triggers (C-020…C-029), engine-and-distribution (C-030…C-037), guards-and-boundaries (C-040…C-046) |
| Quickstart | [`quickstart.md`](quickstart.md) | 6 scenarios + a measured existing-carrier block |
| Feature reference | [`feature-ref.md`](feature-ref.md) | 29 FR rows, 11 SC rows |
| Phase 0 research | [`research.md`](research.md) | 10 findings (R-1…R-10) + 3 residual unknowns (RU-1…RU-3) |

**Drift from the Phase 0 expectation**: none material. The contract set was partitioned into five files at
writing time (declarations separated from the matrix/triggers), and the guard roster resolved to four
contract files plus one integration fixture. Two adaptations are recorded rather than inherited from the
source: the manifest JSON shape follows requirements FR-021 (`token` / `counts` / `source_reading`),
superseding the source quickstart's `presence` / `summary` naming; and the ambient section's budget
constraint forbids the source's raise procedure (A-10).