# Implementation Plan: 084 Harness 三重结构（markdown + yaml + script）

**Branch**: `084-harness-triple-structure` | **Date**: 2026-11-05 | **Spec**: `.specify/specs/084-harness-triple-structure/requirements.md`
**Requirement → Feature**: `084-harness-triple-structure` → Feature 084 Harness 三重结构（markdown + yaml + script）
**Input**: Specification from `.specify/specs/084-harness-triple-structure/requirements.md`
**Flow Class**: `execution`（`source: declaration`，按 `flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` 读取一次，读数为 `execution` / `flow_type: -` / exit 0）

## Summary

把 harness 相关流程的载体从 `markdown + script` 两层升级为 `markdown + yaml + script` 三层：新增一个**声明层**
`shared/declarations/`（`contract.yaml` 拥有全部机器读取取值域，`facts/<fact-slug>.yaml` 一文一件，`exclusions/<reason>.yaml`
按理由一词一文件），新增一个**只读判定引擎** `scripts/python/harness-triple-check.py`（`coverage` / `verify` / `lookup`
三动作、stdlib-only、无模型判断），并新增一个 **stdlib-only 共享读取入口** `scripts/python/declaration_reader.py`，使每个
消费引擎从同一份解析器取值，而不再各自内联一份常量。散文 owner 把取值表换成指针、保留判据；迁移分三批，每批独立可验收；
`specify init` 通过既有的 `shared/` 递归拷贝把声明层带到客户项目，旧项目缺目录时显式降级而不抛异常。

技术路线的三个承重点都写在下面的证据里：① 范围不靠流程清单，而由候选屏幕 S 在树上重算（今日读数：27 个命令模板 + 53
个 SKILL.md + 19 个工作流文档，`research.md` § R4）；② 判定不靠"文件存在"，三层合取里第 (c) 项（引擎读取点可定位）不成立
即 `pending`（假绿红线）；③ 分发不靠新机制，`copy_local_templates()` 已经递归拷贝 `shared/`，实测新子目录随拷贝落地
（`research.md` § R2）。

## Technical Context

**Language/Version**: Python — measured `Python 3.11.13` on this host; the declared floor is `requires-python >= "3.8"`
(`pyproject.toml`). Every file this feature adds is standard library only.
**Primary Dependencies**: none added. `pyproject.toml` `dependencies` stays byte-identical to the baseline (six entries,
none a YAML library) — the layer's subset parser is written, not imported.
**Storage**: files only, one fact per file (`shared/declarations/facts/<fact-slug>.yaml`), one file per exclusion reason,
one `contract.yaml` for value domains. No database, no aggregate ledger, no derived index file.
**Testing**: `pytest 9.2.0` through `scripts/bash/run-tests.sh` (resolves `python3` on this host). New surface:
`tests/contract/test_harness_triple_structure.py` + `tests/fixtures/harness-triple-structure/`.
**Target Platform**: POSIX hosts that run Python 3 — the framework repo, and any client project created by
`specify init` (where paths arrive in their `.specify/`-prefixed form).
**Project Type**: framework source (a code generator / prompt framework): `shared/`, `scripts/`, `templates/`, `skills/`,
`src/`, with `.specify/` as the generated runtime mirror.
**Performance Goals**: `--action coverage` over the current candidate surface (99 unit carriers) completes well inside an
interactive pause and produces byte-identical output on two consecutive runs; determinism is the goal, not throughput.
**Constraints**: stdlib-only; read-only (zero write points); no model judgement; three exit codes closed at `0/1/2`;
findings closed at six verbatim templates; no new gate stage; no change to any frozen gate's criteria or exit codes; must
behave in a client project whose declaration text has been rewritten to the `.specify/` form.
**Scale/Scope**: 99 unit carriers today; batch 1 covers the nine facts whose faces already drift; three batches total; two
new Python files, one new owner document, one new test module and one fixture directory; five owner documents turn into
pointers; one gate host gains an opt-in delegation.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.15.0 — eighteen principles, in
document order, no annotation on any principle heading):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every clause in `contracts/` cites the FR it implements; `feature-ref.md` maps Feature 084's six key changes onto contracts; no design element lacks an FR (the two list deliverables are the spec's A9/FR-011). |
| II | Feature-Centric Development | ✅ Pass | Bound Feature 084 already carries the index row; this plan advances `Draft → Planned` only (`feature-ref.md` § Status movement) and leaves Feature 081 at `Completed`. |
| III | Intent-Driven Development | ✅ Pass | The layer's intent is written once, as chapter names of the owner document (`## Document Structure` § Chapter Tree), not restated per contract; each contract addresses one question. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Every contract clause names the fixture or test that proves it (`contracts/harness-triple-check.contract.md` HC-16, `contracts/declaration-schema.contract.md` § Verification); six negative fixtures and one positive per action are declared before implementation. |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster, tier, or config is touched: `AGENT_CONFIG` / `_ASSISTANT_TIERS` unchanged; per-tool copies untouched (the command templates are not edited). |
| VI | Continuous Quality & Observability | ✅ Pass | Verdicts are produced by program output, not prose (SC-003's rule); the one known-bad environment fact is recorded as `EP-002` with a decision instead of being waived; no `.bak`/`.orig` copies are part of the design. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | `Draft → Planned` is the ceiling here; no status regression; the two `Planned` preconditions named in `features/084.md` are landed (`contracts/migration-batches.contract.md`, `contracts/distribution-and-mirror.contract.md`); decomposition gate read at plan entry. |
| VIII | Code as the Single Source of Truth | ✅ Pass | The migration's authority order is code > generated > authored (`contracts/migration-batches.contract.md` MB-06); every "today" claim rests on a file:line reading (`research.md` § R5), not on a document's word. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | No configuration system, no evaluation engine, no scheduler, no second gate (Non-Goals N1/N2 map to `contracts/declaration-schema.contract.md` DS-08 and `contracts/harness-triple-check.contract.md` HC-15); the engine is a read-only script with three actions. |
| X | Documentation Naming & Location Conventions | ✅ Pass | New documents are lowercase kebab-case at semantic paths (`shared/definitions/harness-triple-definitions.md`); no reserved ALL-CAPS name is used; the `docs/` entry is a pointer page (DM-13). |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two Hats honoured: every change lands in framework sources and reaches `.specify/` only through `sync-mirrors.py` (`## Mirror Obligations`); the gate host's docstring is corrected with its code, so documentation and mechanism do not diverge (Mechanism Fix, not instance patch). |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `sync-mirrors.py`, `doc-consistency-check.py` (duplicate face), `specify init`, `run-tests.sh`; ten Tool records exist and none covers "judge a declaration layer", so writing the two scripts is the expected outcome rather than a shortcut. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | The feature strengthens Change Validation (machine verdicts over prose) and Learning Capture (record schemas in batch 3) and says so instead of inventing categories; A7 applies the same rule to `better-harness.md` itself (seven-state enumeration migrates, five-dimension table stays). |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | `contract.yaml` is the single owner of value domains (E-3, R-5); markdown owners keep criteria and gain pointers (FR-018); the only duplicates are the generated mirror and dated readings in `research.md`/`test-evidence/`. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The six reason templates name the unit, path, or fact the reader must act on (`requirements.md` § Shared Strings form rule), so a failure line is actionable without opening the plan; plan artifacts carry context and reach everything else by path. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | One mid-plan discovery is recorded rather than patched: `EP-002` is `falsified` with `resolve-in-scope`, and the gate host's closed four-name finding set is preserved by making the delegation opt-in (D8) instead of editing an 081 assertion. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | `shared/declarations/` and its two subdirectories are registered in `shared/definitions/framework-map.md` in the same change (DS-11, DM-11); names are kebab-case; the plan's own scratch used `.specify/.tmp/` and was deleted. |
| XVIII | Grounded Naming | ✅ Pass | Names imitate the closest siblings (Grounded Naming order 3): `harness-triple-check.py` ← `closure-acceptance-check.py`, `declaration_reader.py` ← `clause_extract.py` (the importable-module precedent); fact slugs are grounded names, not a new numbering namespace (DS-03). |

**Gates Status**: ✅ All eighteen principles pass; no violation needs a Complexity Tracking row. The two items that could
have read as violations are resolved inside the design instead: the gate host's stated self-containment (delegation is
opt-in and degradation-aware, D8) and the installed-snapshot distribution route (recorded as a falsified premise with a
decision, `EP-002`).

**Re-check after Phase 1**: 2026-11-05. Re-read against the landed design artifacts rather than the intent, three rows
changed their evidence and none changed its verdict — IV points at the fixture roster in `data-model.md` § Fixture set;
XIV points at `contracts/declaration-schema.contract.md` DS-02 (the contract is not a second copy); XVIII points at the
naming note in `contracts/shared-reader.contract.md`. No row regressed to Partial, so Complexity Tracking stays `N/A`.

## Decision Tensions

*Record shape, admissibility criteria, rejection forms and the load-bearing threshold are owned by
`.specify/shared/guidelines/decision-tension.md` — read from the repository root. Fields: `decision`, `antithesis`,
`binding_constraints` (`pole_a` / `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`;
identifier `T-NNN`. Each of the four records below runs `expected_sacrifice` against a source declared in
`requirements.md` § Measurement Sources.*

### T-001 — 消费引擎在运行时读声明层，而不是由声明生成代码

- **decision**: 每个消费引擎通过共享读取入口在运行时读取声明层取值；本特性不引入任何构建期代码生成。
- **antithesis**: 构建期代码生成 —— 由 `facts/*.yaml` 生成一个 `declarations_generated.py`，引擎 `import` 其中的常量。在「CI 已固定构建步骤、引擎需要静态可检查的取值、且客户项目从不直接编辑声明」时它更优：取值成为普通 Python 对象，零运行期解析，取值域在构建期就红。
- **binding_constraints**:
  - pole_a: 一条事实在仓库内只允许存在一份取值，改一处必须让所有面同时生效（否则特性要消灭的漂移仍在）。
  - pole_b: 引擎拿到的取值必须在提交前就可静态检查，坏声明不能等到运行期才暴露。
- **discriminating_evidence**: 在一棵只有声明层的树上改一个取值，不跑任何构建步骤，直接运行消费引擎与 checker；结果二值：读到新值 / 仍读到旧值。
- **expected_sacrifice**: SC-001 Source ↓ 每次 coverage／verify 都要现解析声明（DS-12 禁止缓存文件），单次运行耗时随声明条数线性上升，该次运行记录的耗时读数会高于生成方案。
- **revision_trigger**: coverage 在候选集上的单次运行耗时连续两次超过 5 秒，或出现「声明已改、引擎仍读旧值」的实测漂移 ≥1 次 → 重开，改为构建期生成 + 声明为源的过渡形态。

### T-002 — 单元处置由声明反投影派生，不建聚合台账

- **decision**: 候选单元的处置与完整性状态在每次运行时由声明文件与排除记录反投影派生，仓库内不存在任何处置总表、索引或缓存。
- **antithesis**: 一份 `register.yaml` 集中登记每个候选单元的处置与状态，判定器读它。在「候选单元数量长期稳定、评审需要一眼看全量处置、且各分支几乎不并发修改同一段」时它更优：一次读取给出全表，评审可直接 diff 一行，无需每次重算屏幕。
- **binding_constraints**:
  - pole_a: 两个并行分支各自新增一条事实，合入时 MUST NOT 冲突（写入路径不同）。
  - pole_b: 全量处置 MUST 能一次读取、一眼可审，不能让复核者只能逐文件拼图。
- **discriminating_evidence**: 在两个临时分支上各新增一条事实声明，依次合入，然后各自跑 coverage；结果二值：两次合入均无冲突且两种树上 coverage 都退出 0 / 出现冲突或 coverage 报 `[[STR-013]]`。
- **expected_sacrifice**: SC-001 Source ↑ 每次 coverage 重算屏幕与反投影（今日 27 + 53 + 19 个载体），没有可 diff 的处置总表；复核者必须跑一次命令才能看到全表。
- **revision_trigger**: 出现「人工发现某单元未归类、而 coverage 未报」≥2 次（说明反投影漏读）→ 重开，改为生成式索引（仍 MUST NOT 变成手写总表）。

### T-003 — 判定挂在既有门宿主上，但默认关闭

- **decision**: 声明判定以**默认关闭的显式参数**接入既有门宿主 `pre-analyze-check.py`；不新增门禁阶段，也不默认开启。
- **antithesis**: 默认开启 —— 宿主每次都执行声明判定，并把新 finding 名并入宿主既有的封闭集合。在「仓库已完成迁移、081 的验收断言已被正式修订、且不再有未迁移特性的夹具经过该宿主」时它更优：没有任何调用点能忘记加参数，缺层不可能被静默跳过。
- **binding_constraints**:
  - pole_a: 新判定必须在真实阶段运行中被执行，不能只存在于契约测试里（否则「挂在门宿主上」是空的）。
  - pole_b: 既有门禁的封闭 finding 集合与 081 的验收断言 MUST 由本特性零改动（`tests/contract/test_acceptance_premises.py` 断言 findings ⊆ 既有四名）。
- **discriminating_evidence**: 用 081 的 `positive` 与 `inherited-clean` 夹具，带与不带该参数各跑一次，比较 findings 名字集合；结果二值：不带参数时集合 ⊆ 既有四名（081 断言保持绿）/ 出现第五个名字。
- **expected_sacrifice**: SC-006 Source ↑ 门禁覆盖依赖调用方记得带参数；本特性自己的阶段行会带，但别处漏带即静默跳过——用可观测性换「081 断言零改动」。
- **revision_trigger**: 出现「阶段运行漏带参数导致该次未判定」≥1 次，或 081 的封闭集合被正式修订 → 重开，改为默认开启并把新 finding 名并入封闭集合。

### T-004 — 排除证据是排除记录，不是 in-scope 正向清单

- **decision**: 范围内的判定以「每个候选单元一条记录」表达：in-scope 由事实声明覆盖，out-of-scope 由按理由分文件的排除记录点名；不维护 in-scope 正向清单。
- **antithesis**: 正向 allowlist —— 只有 `in-scope.yaml` 列出的单元参与三层，其余一律不参与。在「范围收敛、单元数少、且希望新单元默认沉默」时它更优：新单元默认不出现在判定里，不会因为漏写排除记录而红。
- **binding_constraints**:
  - pole_a: 新增的 harness 单元 MUST NOT 静默逃过三层结构（这是本特性存在的理由）。
  - pole_b: 与 harness 无关的单元 MUST NOT 因登记义务而制造噪声与误红。
- **discriminating_evidence**: 在临时夹具上新增一个引用框架引擎的新命令，不为它写任何记录，跑 coverage；结果二值：以 `[[STR-013]]` 点名并退出 1 / 退出 0 且无输出。
- **expected_sacrifice**: SC-004 Source ↑ 每个新单元都要留一条记录（声明或排除），拒绝成本落在贡献者身上；allowlist 方案下新单元零成本。
- **revision_trigger**: 若排除记录中「无机器消费事实」「无 harness 资产」两类行数的增速超过候选集增速（噪声大于收益）→ 重开，改为收窄屏幕 S 并引入 allowlist。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/084-harness-triple-structure/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — eight measured readings (R1–R10)
├── data-model.md        # Phase 1 output — E-1…E-10 + fixture roster
├── quickstart.md        # Phase 1 output — S1…S8, each marked executed or route (b)
├── contracts/           # Phase 1 output — five contracts
│   ├── declaration-schema.contract.md
│   ├── harness-triple-check.contract.md
│   ├── shared-reader.contract.md
│   ├── migration-batches.contract.md
│   └── distribution-and-mirror.contract.md
├── feature-ref.md       # Phase 1 output — bound Feature 084 and status movement
├── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created here)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
shared/
├── declarations/                    # NEW — the yaml layer: contract.yaml, facts/, exclusions/
│   ├── contract.yaml                #   value-domain owner (three exit codes, five kinds, two states, three reasons, key sets)
│   ├── facts/                       #   one file per fact, path IS the identity
│   └── exclusions/                  #   one file per reason (at most three), rows carry unit/carrier/anchor
├── definitions/
│   ├── harness-triple-definitions.md  # NEW — the feature's single owner doc (three layers, the three criteria, screen, reasons, authority order, non-goals)
│   ├── framework-map.md             #   register the new directory + two subdirectories (same change)
│   └── flow-class-definitions.md    #   value tables become pointers; criteria stay
├── guidelines/better-harness.md     #   § 证据纪律 item 2 becomes a pointer (five-dimension table stays)
└── workflow/
    ├── feedback-step.md             #   threshold restatement becomes a pointer
    ├── expression-gates.md          #   stage-operator table / six-face set become pointers (batch 2)
    └── acceptance-hardening.md      #   § Closure Verdict keeps its prose; `Path` value set moves (A8(a))

scripts/python/
├── harness-triple-check.py          # NEW — coverage / verify / lookup, read-only, stdlib only
├── declaration_reader.py            # NEW — the only YAML-subset parser; importable by sibling engines
├── feedback-utils.py                #   threshold read through the shared entry (batch 1)
├── evidence-utils.py                #   seven states + lanes read through it (batch 1)
├── flow-class-check.py              #   class / basis / document-type / ledger-column / neutral sets read through it (batch 1)
├── validate-requirements.py         #   `Path` values read through it; checks and messages unchanged (batch 1)
├── closure-acceptance-check.py      #   its inline tuple deleted; behaviour identical (batch 1)
└── …                                #   batch 2 / batch 3 engines by the roster in contracts/migration-batches.contract.md

skills/external/sdd-loop-driver/scripts/pre-analyze-check.py   # opt-in delegation + docstring corrected

tests/
├── contract/test_harness_triple_structure.py   # NEW — contract, three actions, six reasons, dual writer, subset, three states
└── fixtures/harness-triple-structure/          # NEW — one directory per feature, one fixture per reason + positives

docs/                                # one pointer page registered per docs/concepts/documentation-model.md
CHANGELOG.md                         # one entry

.specify/                            # GENERATED — never hand-edited: shared/, scripts/, skills/ mirrors
```

**Structure Decision**: the change lands in the **existing framework-source layout** — no new top-level directory, no new
package. It extends `shared/` with one subtree (`declarations/`), `scripts/python/` with two files, `tests/` with one
module and one fixture directory, and turns five existing owner documents into pointers. `src/specify_cli/__init__.py` is
**not** expected to change: the distribution duty rides the existing recursive copy of `shared/` (verified on the source
route, `research.md` § R2). If the distribution verification fails, the fix lands in `src/` and is recorded as a deviation
from this plan rather than folded in silently.

### Mirror Obligations

Owner of the mirror pairs: `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` (read, not remembered). **Baseline drift
measured before any edit** with `python3 scripts/python/sync-mirrors.py --check`: exit 0, all six pairs `ok`
(`scripts/` 119 files, `shared/` 62 files; `test-evidence/plan-readings.txt` § R4). The criterion below is therefore
"no NEW drift on the pairs this feature touches", not a pre-written absolute.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/declarations/**`, `shared/definitions/harness-triple-definitions.md`, `shared/definitions/framework-map.md`, `shared/definitions/flow-class-definitions.md`, `shared/guidelines/better-harness.md`, `shared/workflow/{feedback-step,expression-gates,acceptance-hardening}.md` | `.specify/shared/…` same relative paths (generated by `sync-mirrors.py`, never hand-edited) | `python3 scripts/python/sync-mirrors.py --check` reports `ok shared/ == .specify/shared/` with no NEW drift against the measured baseline |
| `scripts/python/harness-triple-check.py`, `scripts/python/declaration_reader.py`, plus every engine touched in batches 1–3 | `.specify/scripts/python/` same names — this pair is **strict**: a mirror-only extra file fails | same `--check`, pair `ok scripts/ == .specify/scripts/`, no NEW drift |
| `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` | `.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py` (the `skills/external → .specify/skills` pair flattens the layer name) | same `--check`, pair `ok skills/external/ == .specify/skills/`, no NEW drift |
| `templates/`, `agents/`, `.github/prompts/`, `.claude/commands/`, `.qoder/`, `.opencode/` | **none** — no command template or agent definition is edited by this feature; `templates/commands/` is retired as a mirror and fans out only via `regen-command-copies.py`, which this feature does not touch | not applicable; if a later slice edits a command template it MUST regenerate the per-tool copies |
| `src/`, `tests/`, `docs/`, `CHANGELOG.md` | **none** — these are not in `MIRROR_PAIRS` | `git ls-files` shows a single copy |

## Execution Premises

Owner of this table's shape, its `Status` domain and its `Decision` domain: `shared/workflow/acceptance-hardening.md`
§ Execution Premises. `falsified` MUST carry a `Decision` from `resolve-in-scope` / `fallback` / `user-waiver`. All
readings were taken on this branch at `171c2ff8`; the raw console output is
`test-evidence/plan-readings.txt`.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | 本仓开发检出上存在一条可用的执行链，三层结构的构建与三批迁移的验收全部压在它上面：CPython（满足 `requires-python >= "3.8"`）、与规格 pin 一致的 pytest、以及能把工作树的 `shared/` 分发出去的 `specify init` 路径 | `python3 --version` → `Python 3.11.13`；`python3 -m pytest --version` → `pytest 9.2.0`（与运行栈行 `RS-002` 的 pin 逐字一致）；源检出路由 `PYTHONPATH=<repo>/src … init demo3` → exit 0、`get_resource_path()` 返回本仓、`shared/` 62 个 md 与五个子目录全部落地（`test-evidence/plan-readings.txt` § R1/R6、`test-evidence/specify-init-source-route.txt`） | verified | — |
| EP-002 | **PATH 上的 `specify` 控制台脚本会把工作树的 `shared/` 分发到客户项目** | 同一夹具上 `specify init demo …` → exit 0，但 `.specify/shared/` 只有 55 个 md，等于**安装态快照**的读数，低于工作树的 62（`plan-readings.txt` § R5）。`get_resource_path()` 优先返回模块目录，故控制台入口永远分发安装快照 | falsified | resolve-in-scope |
| EP-003 | `git` 可用且已带版本读数，使「既有测试文件零改动」与镜像差异判定都可压在同一条命令上 | `git --version` → `git version 2.43.7`；`git diff --stat 171c2ff8 -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` → 空输出、exit 0 | verified | — |
| EP-004 | 动手前两处镜像与按工具副本零漂移，因此「本特性关闭时 `--check` 仍 ok」是可达判据 | `python3 scripts/python/sync-mirrors.py --check` → exit 0，六对全 `ok`（`shared/` 62 文件、`scripts/` 119 文件）；逐字输出存 `plan-readings.txt` § R4 | verified | — |
| EP-005 | 规格点名的两个 081 验收测试文件在本解释器上可被收集，故「零新增失败」是一个可测的量而不是口号 | `python3 -m pytest --collect-only -q tests/contract/test_requirements_checker.py` → 40 tests collected；`… test_checker_form.py` → 37（`plan-readings.txt` § R11）。仅收集，未运行：整轮基线属 implement 阶段的预算 | verified | — |
| EP-006 | 残留字面量判定所复用的既有面今天可运行，故 FR-007 (b) 不需要新扫描器 | `python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate --spec-dir .specify/specs/084-harness-triple-structure` → `faces: duplicate=pass`, `files_scanned: 2`, `findings: 0`, exit 0（`plan-readings.txt` § R9） | verified | — |
| EP-007 | 仓内临时落点可用且已被忽略，使 SC-005 的分发夹具不需要裸系统临时目录 | `git check-ignore -v .specify/.tmp/x` → `.specify/.gitignore:30:.tmp/`；本阶段的分发探针即在 `.specify/.tmp/084-plan-probe/` 下创建并在读数后删除（`rm -rf` 已执行，目录不存在） | verified | — |

**Two duties, discharged**: every runtime-stack row in `requirements.md` cites `EP-001` (its `Premises` cell), and
`EP-002` is a known negative conclusion recorded as a falsified premise with a decision — not parked as an
"environment quirk". `EP-002`'s decision is `resolve-in-scope`: the distribution reading is taken on the source route,
the console route's reading is kept as a dated observation, and the assertion in `EP-002` (the console route carries the
working tree) MUST NOT be restored as a passing claim anywhere in this feature's artifacts.

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain (`resolved | inherited | not-applicable`), the `Source row` /
`Carrier` / `Carrier slice` grammar and the carrier's eligibility rule: `shared/workflow/acceptance-hardening.md`
§ Inherited Blockers. Boundary: this table disposes **dependency-inherited** records only; plan-time load-bearing
premises live in § Execution Premises above.

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:

- `081`: `.specify/memory/features/081.md`, `.specify/specs/081-acceptance-hardening/verification.md`

**Why 081 and only 081**: this feature edits a surface 081 owns and accepted — `shared/workflow/acceptance-hardening.md`
§ Closure Verdict (the `Path` value set moves to the declaration layer while its criteria, refusal text and exit-code
meaning stay byte-identical), and it must not disturb 081's acceptance tests. That is a dependency in the strict sense:
the other feature's measured verdicts are the constraint this feature must not falsify. No other feature owns a surface
this plan touches; the pointer-only owners (`flow-class-definitions.md` → 069, `expression-gates.md` → 077/069a,
`feedback-step.md` → 050/072) contribute no measurable record to inherit, so listing them would add disposition rows with
nothing to dispose.

**Extraction readings (measured, closed three sources)**: 081's `verification.md` carries nine `SC-NNN_status` rows and
every one reads `pass`; `deferred_tasks=` is empty on its first line; no `## Deferred` section exists anywhere in the
feature registry (`grep -rln '^## Deferred' .specify/memory/features/` → zero hits). The extraction set therefore yields
**zero rows**, and a zero-row source is a reading, not a disposition — inventing a locator for a row that does not exist
would poison the join key this table exists to protect.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|

**Readings**: 0 extracted records, 0 disposition rows needed, 1 dependency declared with its artifacts named. The
constraint 081 imposes is carried as a **design obligation**, not as an undisposed row: `contracts/migration-batches.contract.md`
MB-01 row 9 (the `Path` value set) plus the zero-diff reading on 081's two acceptance files (`EP-003`, `EP-005`), which
the closure verdict re-reads.

## Document Structure

*This line declares `Flow Class: execution`, so this section is not a required plan output by class condition. It is
produced anyway because the brief asks for it and because this feature genuinely delivers one governed document — the
owner doc `shared/definitions/harness-triple-definitions.md`. The chapter tree below is that document's tree; the plan
stage delivers the tree, the implement stage delivers the document, and `doc-consistency-check.py --action structure
--spec-dir <spec> --path shared/definitions/harness-triple-definitions.md` is the reading that compares the two, after
the document exists.*

### Chapter Tree

*The single structural source for the delivered document: every chapter planned here MUST appear in the delivered
document, and a delivered top-level chapter absent from this table is `chapter-unexpected`. `父节` takes the top-level
marker `—` or the name of another row of this table.*

| 节名 | 父节 | 目的 | 边界 |
|------|------|------|------|
| 本文档的地位与读者 | — | 读者决定「这条规则在哪里改、去哪里找它的取值」时有唯一入口 | 不列取值、不复制契约表 |
| 三层各自拥有什么 | — | 读者判断一条内容该落在 markdown、yaml 还是 script | 不给具体 facts 清单（那是声明层的事） |
| 归 yaml 的判据 | — | 读者对任一候选事实给出可判定的「迁／不迁」结论 | 不重述 FR 编号，不列举已迁事实 |
| 候选屏幕 S 与流程单元 | — | 读者知道哪些载体是候选、范围如何被重算而不是被枚举 | 不列候选名单（屏幕每次重算） |
| 范围判据与排除理由的语义 | — | 读者能为一个单元写出正确的处置记录或正确的排除理由 | 不复述取值域（归 `contract.yaml`） |
| 迁移时的权威取值顺序 | — | 读者在各面已经漂移时知道取哪一面的值、以及要不要留痕 | 不重述批次名单（归迁移契约） |
| 非目标 | — | 读者知道本能力明确不做什么，避免把纪律扩成仪式 | 不承诺未来特性 |

### Reader Baseline

**Readers**: the baseline reader defined once in `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议
— reused by reference, not redefined here.
**Reading scenario**: a maintainer who has just been told "this value now lives in the declaration layer" opens this
document to decide whether their unit is in scope, what record it owes, and which face's value to trust — without
having followed this feature's planning run.

### Evidence List

*One row per factual assertion the delivered document will carry. Grade, as-of and source are a triple:
`shared/workflow/expression-gates.md` § 证据分级与 as-of owns the vocabulary and the marriage rule.*

| 断言 | 证据等级 | as-of | source |
|------|----------|-------|--------|
| 候选屏幕今天覆盖 27 个命令模板、53 个 SKILL.md、19 个工作流文档，且 `shared/definitions/*.md` 不是单元 | 实测 | 2026-11-05 | `test-evidence/plan-readings.txt` § R7 |
| PATH 上的控制台入口分发安装态快照（55 个 md），源检出路由分发工作树（62 个 md，含五个子目录） | 实测 | 2026-11-05 | `test-evidence/plan-readings.txt` § R5/R6；`test-evidence/specify-init-source-route.txt` |
| 写入 `shared/` 的新子目录会随既有递归拷贝到达客户项目，无需新资产清单代码 | 实测 | 2026-11-05 | `research.md` § R2 |
| 五个冻结门禁脚本的既有测试文件集合为 39 个文件，其中两个 081 验收文件分别收集 40 / 37 个用例 | 实测 | 2026-11-05 | `test-evidence/plan-readings.txt` § R10/R11 |
| 复制到客户项目时源形式路径会被重写为 `.specify/` 形式，故声明路径必须两形式可解析 | 实测 | 2026-11-05 | `research.md` § R3（`rewrite_paths()` 与 `copy_tree_with_rewrite()` 的实际行为） |
| 表达类与执行类对本章节的产出义务不同：表达类必产、执行类不被要求 | 引用 | 2026-11-05 | `templates/plan-template.md` § Document Structure（判据 owner 为 `scripts/python/doc-consistency-check.py` 的常量集） |

### Fact Owners

*Each fact has exactly one owner. Two rows owning the same fact is `owner-duplicate`; an owner path that does not exist
in the repository is `owner-path-missing`; an empty anchor is `owner-anchor-missing`. The owner paths below are the
owners **as they stand today** (code wins, per the constitution's code-as-truth principle); after migration each fact's
owner becomes its declaration file `shared/declarations/facts/<fact-slug>.yaml`, and the pre-migration owner becomes a
`former_carrier`. Two states of one fact across time, never two live owners.*

| 事实 | owner 路径 | 章节锚 |
|------|------------|--------|
| feedback 提示阈值 | `scripts/python/feedback-utils.py` | `DEFAULT_THRESHOLD` 常量 |
| 证据七态封闭集 | `scripts/python/evidence-utils.py` | `SEVEN_STATES` 常量 |
| 证据五泳道 | `scripts/python/evidence-utils.py` | `LANE_NAMES` 常量 |
| 流程类别二值 | `scripts/python/flow-class-check.py` | `CLASS_VALUES` 常量 |
| 流程 basis 三值 | `scripts/python/flow-class-check.py` | `BASIS_VALUES` 常量 |
| 文档类型封闭集 | `scripts/python/flow-class-check.py` | `FLOW_TYPE_VALUES` 常量 |
| 台账必需列 | `scripts/python/flow-class-check.py` | `REQUIRED_LEDGER_COLUMNS` 常量 |
| 类中立类别 | `scripts/python/flow-class-check.py` | `NEUTRAL_CATEGORIES` 常量 |
| 成功标准 `Path` 取值二值 | `scripts/python/validate-requirements.py` | `PATH_VALUES` 常量（第二副本 `scripts/python/closure-acceptance-check.py` 的内联元组，迁移时删除，不成为第二 owner） |

## Design Decisions (D1–D13)

Each decision names the artifact that owns its detail; nothing here is a second definition.

- **D1 — Layer layout**: `shared/declarations/` holds exactly `contract.yaml`, `facts/`, `exclusions/`
  (`contracts/declaration-schema.contract.md` DS-01). Reason: path-is-identity kills the second numbering namespace and
  gives the dual-writer property for free.
- **D2 — `contract.yaml` scope**: it owns schema id, subset id, five kinds, two completeness states, three exclusion
  reasons, three exit codes, required key sets and the gate-call-site roster (E-3). Reason: the contract that carries a
  closed set MUST NOT become a second copy of it, so every other document points here.
- **D3 — One parser**: `scripts/python/declaration_reader.py`, importable because every consumer is invoked as
  `python3 scripts/python/<name>.py` (so `sys.path[0]` is that directory) — sibling precedent `clause_extract.py`
  (`contracts/shared-reader.contract.md` SR-01…SR-08).
- **D4 — Engine surface**: one file, three actions (`coverage` / `verify` / `lookup`), `--repo`, `--format`,
  `--json-out`; `lookup` takes `--unit-id` or `--fact` (`contracts/harness-triple-check.contract.md` HC-01…HC-09).
  Reason: FR-016 fixes the three actions; the `--fact` selector is what lets a consumer ask for one value without
  reading raw declarations.
- **D5 — Candidate screen S**: recomputed by text over three carrier surfaces, `shared/definitions/*.md` excluded
  (HC-05). Reason: a list would be a third roster competing with two existing ones; a text test's conservative side is
  retired by an exclusion row.
- **D6 — Disposition and completeness**: reverse projection in a fixed order, three states, and a **textual** definition
  of "locatable read point" (`data-model.md` E-5/E-6, R-6). Reason: the false-green failure this feature exists to
  remove is precisely "the file exists, so we call it migrated".
- **D7 — Exit-2 labels are not findings** (a judgement made here, disclosed): the six-value finding set of FR-017 is
  closed, while FR-013 requires a legacy project's degradation to be explicit and FR-003 gives `contract.yaml` the
  three exit codes. Reading them together, degradation is an **input-error label on exit 2**, not a seventh finding, and
  SC-003's 6/6 counts only the six. Recorded here so review can challenge the boundary rather than discover it later.
- **D8 — Gate wiring is opt-in**: `pre-analyze-check.py` gains `--triple-structure` (default off) because
  `tests/contract/test_acceptance_premises.py` asserts the produced finding names are a subset of the existing four;
  turning the delegation on by default would make an 081 assertion go red, which FR-018 forbids. The host's docstring is
  corrected in the same change (T-003 records the trade-off).
- **D9 — Three batches, each independently acceptable**, with the first roster named in
  `contracts/migration-batches.contract.md` MB-01…MB-10. The `Path` value set (081's surface) is batch-1 row 9 with a
  zero-diff obligation.
- **D10 — Test surface**: `tests/contract/test_harness_triple_structure.py` plus
  `tests/fixtures/harness-triple-structure/` (one directory per feature, one fixture per reason plus positives,
  `data-model.md` § Fixture set). Zero-new-failure selection basis: the 39 test files that reference the five frozen gate
  scripts (`EP-005`, `research.md` § R7) — a rule, not a snapshot list.
- **D11 — Distribution rides the existing copy**; no `src/` change is expected, and the reading is taken on the source
  route (`EP-002` records why). The asset roster and upgrade actions are
  `contracts/distribution-and-mirror.contract.md` § A.
- **D12 — Mirrors**: the pairs in § Mirror Obligations, verified with `sync-mirrors.py --check` against the measured
  zero-drift baseline (`EP-004`). No mirror is hand-edited; `templates/commands/` is untouched so no per-tool copy is
  regenerated.
- **D13 — Decomposition**: `single-package`. `decomposition-check.py --mode plan` returned `proceed` with `fr_count` 19
  against a ceiling of 30; no slice split is declared and no task count is pre-committed.

## Complexity Tracking

N/A — no Constitution Check row is `Fail` or `Partial`, so there is no violation to justify. The two candidate tensions
(gate-host self-containment; the installed-snapshot distribution route) are resolved inside the design and recorded as
T-003 and `EP-002` rather than converted into an exception.

## Phase 0: Research Review

Standalone `research.md` (ten sections, R1–R10 — long enough and evidence-heavy enough that inlining would bury the
plan): toolchain pins; the two `specify init` routes and their opposite readings; the copy-time path rewrite and its
three-form consequence; the candidate screen's measured surfaces; the batch-1 fact sources with file:line; reusable
machinery and its two limits (the host's self-containment sentence and its closed four-name finding set); the
zero-new-failure selection basis and collected counts; the mirror baseline; the decomposition reading; and an explicit
list of what was **not** executed. No unresolved clarification marker remains: the one genuinely open question at plan entry
(A9's asset roster, A8's migration boundary) is answered by artifacts quoted above, not by assumption.

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed (never pre-written).

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 10 entities (E-1…E-10) + 6 fixture families |
| Contracts | `contracts/` | 5 files: `declaration-schema` (DS-01…DS-12), `harness-triple-check` (HC-01…HC-16), `shared-reader` (SR-01…SR-08), `migration-batches` (MB-01…MB-10), `distribution-and-mirror` (DM-01…DM-13) |
| Quickstart | `quickstart.md` | 8 scenarios (S1…S8): 4 executed with pasted output, 4 route (b) with per-example premises |
| Research | `research.md` | 10 sections (R1…R10) |
| Feature reference | `feature-ref.md` | bound Feature 084; status movement `Draft → Planned`; the two `Planned` preconditions |

**Drift from the Phase 0 expectation**: one addition and one correction. Addition — the distribution premise turned out
to be route-dependent (`EP-002` falsified), which added the source-route procedure to
`contracts/distribution-and-mirror.contract.md` § D. Correction — the gate wiring could not be default-on because an
existing 081 assertion closes the finding-name set, which turned a one-line hookup into T-003's opt-in design. Neither
was visible from the requirements alone; both are recorded rather than absorbed.







