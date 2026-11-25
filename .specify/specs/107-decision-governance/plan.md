# Implementation Plan: Decision Governance（AI Agent 决策项治理）

**Branch**: `107-decision-governance` | **Date**: 2026-11-25 | **Spec**: `.specify/specs/107-decision-governance/requirements.md`
**Requirement → Feature**: `107-decision-governance` → Feature 107 Decision Governance（AI Agent 决策项治理）
**Input**: Specification from `.specify/specs/107-decision-governance/requirements.md`

## Summary

Deliver one normative owner page for general AI-agent decision items (`shared/definitions/decision-definitions.md`) that owns the closed vocabulary, the two by-holder decision classes and their presentation templates, the option-set contract, the decision-record field closure and serialization grammar, the archive-as-projection producer inventory, the superagent→subagent decision block with acknowledgement and `implementation_receipt`, the M/B enforcement boundary, and the legacy/migration rules. The feature lands as framework sources: one new page, pointer lines in adjacent owners, one whole ambient instruction section (≤1,500 B, with a recorded total-budget ruling), one read-only deterministic checker (`validate-decisions.py`), producer-surface additions in `run-agent` / `run-team` / the driver references, and red-first guard fixtures for M-01…M-09. No second registry, queue, store or scheduler is added; `.specify/register.md` remains the sole id index; legacy records are readable, reported `legacy`, never rewritten.

## Technical Context

**Language/Version**: Python >= 3.8 (stdlib only for the new checker; pinned by `pyproject.toml`)
**Primary Dependencies**: none new — consumes the existing CPython stdlib, pytest and POSIX bash stack (RS-001…RS-003)
**Storage**: files only — existing carriers (spec artifacts, checkpoints, run reports, `.specify/register.md`, feedback/evidence files); no new store (FR-004)
**Testing**: pytest through the single entry `bash scripts/bash/run-tests.sh` (interpreter ladder incl. `SPECKIT_PYTHON`); red-first fixtures under `tests/fixtures/decision-governance/`; this stage runs the targeted set only
**Target Platform**: framework repository (framework sources + client-runtime mirrors); downstream client projects receive the instruction section through `specify init` / refresh
**Project Type**: CLI / documentation framework — no application runtime
**Performance Goals**: N/A — the checker is one read-only pass over text files; no service, no resident process
**Constraints**: A-13 section cap 1,500 B; total instructions budget ruling 38,912 → 40,960 B (T-001); zero new `scan-confirmation-gates.py` hits; `regen-command-copies.py --check` stays rc 0; no new mirror drift against the measured baseline; checker is read-only with `--help` / `--version`; no second registry
**Scale/Scope**: 12 producers (P-01…P-12), 9 machine rules (M-01…M-09), 6 behavior rules (B-01…B-06), 6 backward-incompatible rows, 1 new owner page, 21 landing files plus mirrors, 5 contracts

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0 — one row per principle in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every landing file traces to an FR: owner page ([[STR-001]]) ← FR-001; instruction section ← FR-010/FR-026; checker ← FR-022; payload ← FR-018/FR-019 (this plan § Project Structure) |
| II | Feature-Centric Development | ✅ Pass | Feature 107 row advances Draft → Planned with its detail updated in the same change (§ Phase 1 backfill, Feature Integration); no other feature changes status |
| III | Intent-Driven Development | ✅ Pass | What/why precede how: `research.md` records measured carriers, `contracts/` state normative interfaces, § Decision Tensions state trade-offs and reopening conditions |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Each M rule names a red-first fixture and a reverse sample (§ Enforcement below, `contracts/enforcement-boundary.contract.md`); tests precede implementation in the tasks plan |
| V | AI Agent Integration Standards | ✅ Pass | The payload addition rides `run-agent` / `run-team`; supported agent roster and tiers untouched; no new provider or config key |
| VI | Continuous Quality & Observability | ✅ Pass | Root-cause discipline: guards that can go red, legacy reported rather than skipped; no `.bak` copies; machine/behavior split kept honest |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Plan set produced from the validated spec; feature registry updated; status ceiling `Planned` respected (no `Implemented`) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Measurements taken from code/engines (`generate-instructions.sh` constant, scanner patterns, `MIRROR_PAIRS`); the owner page's rules are normative by declaration, not by doc-over-code inference |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | No runtime engine, queue, store or scheduler; one read-only checker; archive-as-projection (FR-004); no speculative infrastructure |
| X | Documentation Naming & Location Conventions | ✅ Pass | New page follows sibling naming (`*-definitions.md` under `shared/definitions/`); docs receive one pointer line; no reserved filename reused |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: edits land in framework sources and ride mirror/init (§ Project Structure, § Mirror Obligations); mirrors regenerated, never hand-edited |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | The plan reuses existing validators, the single test entry, mirror/copy engines and migrate dimensions; no capability is re-implemented ad hoc |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Task Understanding (decision text) and Change Validation (guards + review surfaces); claims rest on measured evidence in `research.md` |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Single owner page; adjacent owners add pointer lines only (FR-002); field→owner mapping table; spec inventory becomes a dated declaration |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `human-interactive` template mandates plain language, context and consequences (FR-008); B-03 review surface owns the truthfulness check |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Silent re-decision is an explicit anomaly; P-07 pointer; invalidation stops at the anomaly point (§ Transmission contract) |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | New directories are `tests/fixtures/decision-governance/` (existing per-feature fixtures convention) and the standard spec `contracts/`; no new top-level directory |
| XVIII | Grounded Naming | ✅ Pass | `decision-definitions.md` chosen by sibling imitation; `D-NNN` reuses the register `D-…` family; field names fixed in Shared Strings |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | Names carry meaning: `resource_locator`, `same_name_conflict`, `implementation_receipt`; ids and paths are projections of the owner page |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | Targeted set via `targeted-set-v1`; no second full suite; stage-status row recorded; independent units default to concurrent carriers |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | New checker answers `--help` / `--version`, rejects undeclared options, declares read-only surface (`contracts/enforcement-boundary.contract.md`) |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | Stage anchor and rules reloaded at each core step; verdicts recorded in the stage record (§ re-anchoring record) |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | The change is AI-written → the AI review flow applies at the review stage (direct merge to trunk + AI review of merged history); this plan adds no review ledger |

**Gates Status**: ✅ All 23 gates pass — no Fail or Partial row; Complexity Tracking is N/A.

**Re-check after Phase 1**: 2026-11-25 — refreshed against the landed design artefacts (`data-model.md`, `contracts/` ×5, `quickstart.md`, `feature-ref.md`, § Phase 1 summary). No row changed status; the design artifacts carry the evidence named above.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`. Fields: `decision`, `antithesis`, `binding_constraints` (`pole_a`, `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; identifier `tension_id` (`T-NNN`).*

Plan-local ids; registered globally as `T-019`…`T-021` in `.specify/register.md` (register-global mapping precedent: T-013…T-018).

### T-001 — 指令落地取整节新增并上调总预算，不并入既有小节

- **decision**: 新增整节 `## Decision Items（决策项）` 到 instruction 模板，并把 `INSTRUCTIONS_BUDGET_BYTES` 从 `38,912` 上调到 `40,960`（+2,048 B）；不把两条生产规则作为 bullet 塞进 `## Fast Fail Discipline` 或 `## ID Register`。
- **antithesis**: 把两条生产规则并入既有小节、总预算不动；当生成器能对既有小节做逐 bullet 增量 reconcile、且既有小节读者面正好覆盖决策项时它更优——改动面最小、零预算变更、无新章节。
- **binding_constraints**:
  - pole_a: 两条生产规则 MUST 到达已初始化的客户项目（FR-026、SC-010）。
  - pole_b: 指令总预算 MUST 保持为可触发的警告面，预算被静默吞掉等于失去膨胀探测。
- **discriminating_evidence**: 在一个含既有 `.specify/instructions.md` 的夹具项目上分别执行两种落地形态并运行 `bash scripts/bash/generate-instructions.sh`，看 new-rules 文本是否进入生成文件、以及生成文件大小与预算的比较结果；结果二值：到达/不到达。
- **expected_sacrifice**: SC-010 Source ↑ 指令总量上限从 38,912 B 抬到 40,960 B，下游项目获得 +2,048 B 常驻预算，膨胀告警触发点被同步推高。
- **revision_trigger**: 连续两个迭代出现「下游项目指令因新预算掩盖 >512 B 真实膨胀」≥2 次，或生成器改为逐 bullet reconcile → 重开，回落 512 B 级增量并改用既有小节内落点。

### T-002 — 记录文法取「标题 + 单行字段」，不取围栏块

- **decision**: 决策记录以 `### D-NNN — 标题` + 单行 `- **field**: value` 文法落在既有载体内，复用承重张力已验证的行文法；不引入带 begin/end 标记的新围栏块。
- **antithesis**: 围栏 `decision-record` begin/end 块；当载体正文已大量使用三级标题（checkpoint、run report）、或记录需要与文档标题层级正交时它更优——块边界不依赖标题层级，解析不受标题冲突影响。
- **binding_constraints**:
  - pole_a: 记录 MUST 由一个确定性解析器在四类载体（requirements / plan / checkpoint / run report）上无歧义解析（M-01、M-04）。
  - pole_b: 记录 MUST NOT 抢占或破坏载体既有标题语义（checkpoint 文件已有固定章节结构）。
- **discriminating_evidence**: 在四类载体夹具各放两条记录，用同一解析脚本分别跑两种文法，看是否在四类载体上都唯一识别记录边界与字段；结果二值：四类全过/任一失败。
- **expected_sacrifice**: SC-005 Source ↑ 记录与载体共用标题层级，重建脚本须按标题首词过滤，载体新增三级标题时需避开 `D-NNN` 形态。
- **revision_trigger**: 出现 ≥2 类载体因标题层级冲突无法放置记录（评审记录点名）→ 重开，改为围栏块形态。

### T-003 — 守卫取独立只读引擎，不并入承重张力校验器

- **decision**: 新建只读引擎 `scripts/python/validate-decisions.py`（`records` / `payload` / `chain` / `inventory` 四个 action），不把决策记录解析并入 `validate-decision-tensions.py`。
- **antithesis**: 扩展 `validate-decision-tensions.py` 增加 `--action decisions`；当两种记录文法保持逐字一致、载体集合不变时它更优——一个解析器、一处文法、少一个脚本入口。
- **binding_constraints**:
  - pole_a: 决策记录的字段闭集与检查标签 MUST 独立演进，不被承重张力契约的封闭标签集与其契约测试锁死。
  - pole_b: 新引擎 MUST NOT 成为第二套语义判定或评分器，只判结构命题（A-9）。
- **discriminating_evidence**: 在不动 `tests/contract/test_decision_tension_contract.py` 任何断言的前提下，为决策记录增加一条不同的必填字段检查，看是否必须修改该契约测试；结果二值：必须修改/不必修改。
- **expected_sacrifice**: SC-007 Source ↑ 多一个脚本入口，并承担 `--help`/`--version`/拒绝未声明选项的接口义务与独立契约测试面。
- **revision_trigger**: 连续两迭代出现「两个解析器对同一文法做同批修订」≥2 次 → 重开，合并为单引擎多 action。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/107-decision-governance/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (standalone: measurements + resolved design points)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (5 contracts)
├── feature-ref.md       # Phase 1 output
├── test-evidence/       # Gate captures, baselines, stage records, glossary proposal
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
└── verification.md     # Derived spec-side from test-evidence/verification-input.md (/speckit.implement)
```

### Source Code (repository root)

```text
shared/definitions/decision-definitions.md        # NEW single owner page ([[STR-001]])
shared/definitions/framework-map.md               # + one row for the owner page (FR-030)
shared/guidelines/confirmation-gates.md           # + one pointer line (P-01 carrier; SELF_REL, no gate count change)
shared/guidelines/decision-tension.md             # + one pointer line (承重决策追加记录并交叉引用 T-NNN)
shared/guidelines/fast-fail.md                    # + one pointer line (裁定之后的记录与传递)
shared/definitions/superagent-definitions.md      # + one pointer line; decision block travels in the existing payload
shared/definitions/goal-definitions.md            # + one pointer line (P-08 carrier)
shared/definitions/anchor-definitions.md          # + one pointer line (P-08 carrier)
shared/definitions/agent-definitions.md           # + one pointer line (P-08 carrier)
skills/external/sdd-loop-driver/references/checkpoint-protocol.md   # + one pointer line (P-04 carrier)
skills/external/sdd-loop-driver/references/dispatch-recipes.md      # + one pointer where dispatches carry decisions (P-09)
skills/external/sdd-loop-driver/references/stage-prompts.md         # + one pointer where dispatches carry decisions (P-09)
skills/internal/run-agent/SKILL.md                # decision block build/validate + receipt duties (P-09)
skills/internal/run-team/SKILL.md                 # same pointer + hand-off duty (P-09)
skills/internal/analyze-artifacts/SKILL.md        # B-04/B-05 named review surface pointer (P-05)
skills/internal/review-feature-quality/SKILL.md   # B-01…B-06 named review surface pointer (P-06)
skills/internal/review-sdd-process/SKILL.md       # B-01…B-06 named review surface pointer (P-06)
templates/instructions-template.md                # + whole section `## Decision Items（决策项）`, cap 1,500 B (A-13)
scripts/bash/generate-instructions.sh             # INSTRUCTIONS_BUDGET_BYTES 38,912 → 40,960 (T-001 ruling)
scripts/python/validate-decisions.py              # NEW read-only checker (M rules; script-interface compliant)
docs/concepts/spec-driven.md                      # + one pointer line to the owner page (FR-030)

tests/fixtures/decision-governance/               # red-first fixtures + reverse samples (per-feature fixture dir)
tests/unit/test_validate_decisions.py             # checker unit tests + M-01/M-03/M-04 reverse samples
tests/contract/test_decision_governance_guards.py # M-02/M-05/M-06/M-07/M-08 + legacy/bridge fixtures
tests/contract/test_decision_governance_contracts.py # owner-page/pointer/field-closure/instruction-section guards
tests/contract/test_decision_governance_migration_map.py # BC-01…BC-06 row→test mapping closure
tests/integration/test_decision_governance_migrate_dryrun.py # specify migrate dry-run convergence + zero rewrite
```

**Structure Decision**: extends the framework's definitions/guidelines + skills + templates + scripts layering: one new owner page under `shared/definitions/`, pointer-only edits in adjacent owners, one new read-only engine under `scripts/python/`, one new whole section in the instruction template, and five contracts under the spec. No new top-level directory; the only new non-spec directory is the per-feature fixture directory `tests/fixtures/decision-governance/`, which follows the declared `tests/fixtures/` area convention (one directory per feature).

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/decision-definitions.md` (new) | `.specify/shared/definitions/decision-definitions.md` | `python3 scripts/python/sync-mirrors.py --check`: no NEW drift vs the pre-edit baseline (`test-evidence/sync-mirrors-baseline.txt`, rc 0, zero DIFF) |
| `shared/definitions/framework-map.md`, `shared/guidelines/{confirmation-gates,decision-tension,fast-fail}.md`, `shared/definitions/{superagent,goal,anchor,agent}-definitions.md` | each file's same relative path under `.specify/shared/` | same mirror check — no NEW drift on the pairs touched here |
| `skills/external/sdd-loop-driver/references/{checkpoint-protocol,dispatch-recipes,stage-prompts}.md` | each file's same relative path under `.specify/skills/` (the `skills/external` mirror) | same mirror check — no NEW drift |
| `skills/internal/{run-agent,run-team,analyze-artifacts,review-feature-quality,review-sdd-process}/SKILL.md` | each file's same relative path under `.specify/skills/internal/` | same mirror check — no NEW drift |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md`; generated `.specify/instructions.md` (+ per-tool instruction symlinks, which point at the generated file) | mirror check + `bash scripts/bash/generate-instructions.sh` regenerates the live file inside the budget; `cmp` template/live section extraction |
| `scripts/bash/generate-instructions.sh` | `.specify/scripts/bash/generate-instructions.sh` (strict pair; projected `bash-version-guard` block preserved) | mirror check — no NEW drift; the regenerated mirror keeps its projected block |
| `scripts/python/validate-decisions.py` (new) | `.specify/scripts/python/validate-decisions.py` | mirror check — no NEW drift; the checker runs from both copies with `--help`/`--version` |
| `docs/concepts/spec-driven.md` | none — `docs/` is this project's development documentation, never shipped | no mirror duty |
| no `templates/commands/` change | per-tool command copies | `python3 scripts/python/regen-command-copies.py --check` rc 0 (baseline rc 0 at `test-evidence/regen-copies-baseline.txt`) |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The existing Python ≥3.8 + pytest + POSIX bash stack, exercised only through `scripts/bash/run-tests.sh` (with its `SPECKIT_PYTHON` ladder), can carry the new guard tests with zero new third-party imports | `pyproject.toml` (`requires-python`, pytest); `scripts/bash/run-tests.sh:65-74`; this stage's targeted selection run | verified | — |
| EP-002 | The existing dispatch payload channel (seven role fields + four injections) and the five-item uplink can carry a `decision_block`, an acknowledgement and an `implementation_receipt` without changing field counts | `shared/definitions/superagent-definitions.md` § The super↔sub Protocol | verified | — |
| EP-003 | The existing deterministic checker surface can host the M guards, and gate neutrality is achievable by wording because the new owner page sits inside the gate scanner's `shared` scan dir | `scripts/python/scan-confirmation-gates.py` (`SCAN_DIRS`, `BLOCKING_PATTERNS`); measured baseline 31 gates / 0 violations at `test-evidence/scan-confirmation-gates-baseline.txt` | verified | — |
| EP-004 | The instruction generator + mirror/copy toolchain can deliver the new whole section to initialized projects and keep mirrors and command copies green | `scripts/bash/generate-instructions.sh` (whole-section reconcile); `MIRROR_PAIRS`; rc-0 baselines at `test-evidence/sync-mirrors-baseline.txt` and `test-evidence/regen-copies-baseline.txt` | verified | — |
| EP-005 | Adding the two production rules as bullets inside an existing instruction section would reach already-initialized projects | Constitution Sync Impact Report 1.13.0 follow-up (b): `generate-instructions.sh` reconciles only WHOLE sections | falsified | resolve-in-scope |
| EP-006 | The legacy corpus (101 `T-NNN` headings / 127 checkpoint files / 43 run reports / register `D-…` rows) is present and readable at base `08b59695c`, and no carrier uses the new three-digit record form | Commands M-9 / M-10 in `research.md`; line-level containment reading over the base-corpus paths: `git diff --numstat 08b59695c..HEAD -- <paths>` shows zero deleted lines and no deleted file (measured 2026-11-26: `.specify/register.md` +3/−0 appended `T-019…T-021` rows; `.specify/specs/107-decision-governance/plan.md` +217/−0 as a new file — additions allowed and expected) | verified | — |
| EP-007 | The instructions total budget has no headroom for a new section (live 38,894 B; budget 38,912 B; the generator reports `over` at `size >= budget`) | `wc -c .specify/instructions.md`; `scripts/bash/generate-instructions.sh:107,160-167` | verified | — |

EP-005 is a known-bad fact recorded with its decision (`resolve-in-scope` = land a whole new section), not parked: it is the measured reason for T-001's chosen form.

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `076`: `.specify/features/076-decision-tension-contract.md`, `.specify/specs/076-decision-tension-contract/verification.md`
- `095`: `.specify/features/095-superagent-role.md`, `.specify/specs/095-superagent-role/verification.md`

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | — | Neither declared dependency has a non-empty `## Deferred` section or a `blocked` / `deferred` / `partial` verification status row; the extraction set is empty, so there is nothing to disposition. Both contracts are consumed as stable interfaces (T-NNN six fields; payload/role edge). |

## Complexity Tracking

N/A — no Constitution Check row is Fail or Partial.

## Backward-Incompatible Change Inventory (closed)

Adopts the requirements § Landing & Compatibility Inventory candidates BC-01…BC-06 as the closed list. Each row names its migration or deterministic-refusal behavior in the existing `/speckit.migrate` surface or at the contract boundary, and the test that pins it. No seventh migrate dimension is added (M-13).

| BC ID | Change | Resolution (closed) | Migration / refusal behavior | Evidence / test (planned) |
|-------|--------|--------------------|------------------------------|---------------------------|
| BC-01 | 既有载体新增决策记录块 | `compatibility-bridge` | 无「`^### D-\d{3}` 标题 + C-201 记录字段文法」块 = `legacy`：可读、不判错、不重写；只有新式块进入 M 检查（id 形态单凭 `D-001` 之类 register 行不判新式） | `tests/contract/test_decision_governance_guards.py`（legacy 夹具）；行级包含读数：`git diff --numstat 08b59695c..HEAD -- <既有记录路径>` 删除列为 0、无删除文件（追加允许） |
| BC-02 | 派发载荷新增 `decision_block` | `compatibility-bridge` + deterministic refusal | 非决策派发无块合法；决策 backed 派发无块/缺字段 → payload 构造处拒绝（M-06）；旧载荷不重写 | `tests/unit/test_validate_decisions.py`（M-06 逆向样本）；`tests/contract/test_decision_governance_guards.py`（拒绝分支） |
| BC-03 | 新增 `D-NNN` 编号族行 | `compatibility-bridge` | 与 `D1–D9` / `D-001` 并存，按载体+区间分组登记；`D-001` 是 legacy register 行（id 形态相符但无记录字段文法，不因形态被当作新式记录）；同载体内重复即红；冲突修复走 `/speckit.sanitize --lane renumber`，不静默改号 | `test_decision_governance_guards.py`（同载体重复 id 夹具）+ register 夹具 |
| BC-04 | instruction 模板新增段 | `compatibility-bridge` | `/speckit.migrate` 的既有 `templates-generated` 维度把 `.specify/instructions.md` 收敛到含新段；自定义内容保留；不新增第七维度 | `tests/integration/test_decision_governance_migrate_dryrun.py`：`specify migrate --format json` 干跑列出该生成物的收敛项并断言不触碰记录正文 |
| BC-05 | 新守卫面对旧记录 | `compatibility-bridge` | 守卫只判新式块；旧记录报告 `legacy`；守卫对 base 语料不得转红 | 同 BC-01 的 legacy 夹具 + `--numstat` 零删除读数（无删除行、无删除文件） |
| BC-06 | 两条生产规则生效 | `compatibility-bridge` | 只约束落地后新建决策；既有决策文本由评审按 B-01/B-02 报告为 legacy，不追溯改写 | `test_decision_governance_contracts.py`（评审承接面指针在场）+ legacy 夹具 |

Row-set closure guard: `tests/contract/test_decision_governance_migration_map.py` asserts the declared set equals `{BC-01…BC-06}` and that every row's named test exists (SC-009's "未映射行使守卫转红").

## Phase 1: Design Artifacts Summary

Filled after the artifacts landed (counts read from the written files):

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 9 entities (Decision Item, Decision Record, Option, Decision Block, Acknowledgement, Implementation Receipt, Decision Producer, Archive Projection, Decision Class), 14 invariants, 1 state domain (`transmission_status`) |
| Contracts | [`contracts/`](./contracts/) | 5 files: `text-and-options.contract.md`, `archive-and-audit.contract.md`, `transmission-and-implementation.contract.md`, `enforcement-boundary.contract.md`, `migration-and-compat.contract.md` |
| Quickstart | [`quickstart.md`](./quickstart.md) | 6 scenarios (record authoring, two production accidents, options closure, transmission round-trip, audit reconstruction, legacy read) |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 107 binding, delivery surfaces, mirror map, BC rows, handoff |
| Research | [`research.md`](./research.md) | 16 baseline measurements + 8 resolved design points |
