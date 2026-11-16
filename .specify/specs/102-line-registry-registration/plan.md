# Implementation Plan: 长任务 line 登记与 status 可见性（Line Registry Registration）

**Branch**: `102-line-registry-registration` | **Date**: 2026-11-16 | **Spec**: `.specify/specs/102-line-registry-registration/requirements.md`
**Requirement → Feature**: `102-line-registry-registration` → Feature 088 Speckit 框架可视化（Speckit Framework Visualization）
**Input**: Specification from `.specify/specs/102-line-registry-registration/requirements.md` (23 FR / 9 SC; Clarifications A-14…A-24; Runtime Stack RS-001…RS-006)

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## Summary

`/speckit.status`'s digest reads the environment Line Registry and never scans processes, so any long task that registers no line answers `[[STR-006]]` — an accurate conclusion about an invisible run. This feature closes the gap with one criterion, one carrier and two teeth:

1. the criterion lands in the owner document `shared/guidelines/reporting-obligations.md` § 九 (register at start, heartbeat at stage boundaries, close at the end; unregistered ⇒ not in the digest);
2. the carrier is a new bash wrapper `[[STR-001]]` — `register → execute → close`, fail-closed on registration, `completed` / `failed` on close, `active` residue when it cannot finish;
3. the teeth are a deterministic read-only scanner `[[STR-009]]` whose mechanical criterion is owned by four module constants, plus the behavioural/contract tests that prove the wrapper's lifecycle and the scanner's red leg;
4. the wiring is textual and pointer-only: `templates/commands/status.md` (registry-only sentence), `templates/instructions-template.md` (one ambient bullet), `skills/internal/run-team/SKILL.md` (register / heartbeat / close).

No scheduler, daemon, dependency, second registry or status spine is introduced; the digest engine and the registry engine are consumed unchanged.

## Technical Context

**Language/Version**: POSIX `bash` (constructs must stay bash-3.2 compatible; host measured `GNU bash 5.1.16`), plus CPython `>=3.8` standard library for the scanner.
**Primary Dependencies**: none added. The wrapper consumes `git` and the existing engine `[[STR-002]]`; the scanner consumes only the standard library; tests consume the existing `pytest` runner.
**Storage**: the environment Line Registry (one `<line_id>.json` per line, engine-owned). No new store, no second registry, no journal use.
**Testing**: `pytest` through the unique entry `scripts/bash/run-tests.sh` (parallel default, `contract` / `integration` markers). Isolation is `SPECIFY_LINE_REGISTRY_DIR` under `tmp_path`; the scan fixture root is `.specify/.tmp/line-registry-registration/` (git-ignored).
**Target Platform**: Linux and macOS developer/CI hosts with `bash`, `git` and Python 3.8+.
**Project Type**: framework toolkit (scripts + templates + skills + docs) — no application runtime.
**Performance Goals**: the scanner is one linear pass over the declared roots (hundreds of files), spawns nothing, and must not add measurable test time; `scan-confirmation-gates.py`-class determinism is the bar, not throughput.
**Constraints**: zero new third-party dependencies; wrapper exit codes closed (C-13); scanner exits closed (0/1/2); digest action set, exit codes and `[[STR-006]]` rendering untouched; scanner read-only; no network, no push.
**Scale/Scope**: 3 declared scan roots, 1 wrapper, 1 scanner, 5 test files, 4 text surfaces, 3 contracts, 8 data-model entities.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md`, 23 headings in order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every clause in `research.md` R-01…R-13 traces to an FR; `contracts/` carries the design the spec describes. |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 088 as slice 102; `.specify/features.md` row advanced `Draft → Planned`, parent detail note added, parent status untouched. |
| III | Intent-Driven Development | ✅ Pass | `requirements.md` (what/why) precedes this plan; each decision records its rejected alternative (R-01…R-13). |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Three contracts carry 52 clause ids, and each contract names the test file that pins its examples; the task order authors the tests before the implementation. |
| V | AI Agent Integration Standards | ✅ Pass | No `AGENT_CONFIG` / `_ASSISTANT_TIERS` change; text edits live in agent-neutral templates (`templates/instructions-template.md`, `templates/commands/status.md`). |
| VI | Continuous Quality & Observability | ✅ Pass | Stage gates and executed commands are recorded under `test-evidence/` (plan stage); implementation readings land there per `quickstart.md` S-5; no failing check is skipped or muted. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Phases followed in order; this stage lands at most `Planned`; no status regression, no deferred rows. |
| VIII | Code as the Single Source of Truth | ✅ Pass | Engine, digest and generator behaviour were read in source and re-measured by execution before any design claim (research § Baseline measurements). |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One bash wrapper and one read-only scanner; no runtime platform, scheduler, daemon or speculative infrastructure. |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files sit at conventional paths (`scripts/`, `tests/`); no reserved ALL-CAPS name is coined. |
| XI | Dogfooding (Self-Application) | ✅ Pass | All distributing edits land in framework sources then mirror; the ambient bullet is a mechanism-side template edit, not a live-file patch. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Registry, digest and test runner are reused; the new wrapper/scanner are the feature's declared deliverables, not throwaway scripts. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Reliable Delivery (fail-closed registration) and Change Validation (scanner red leg); evidence claims stay `Unobserved`→`measured`. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Criterion literals owned by `requirements.md` Shared Strings + scanner constants; downstream surfaces are pointers; mirrors are generated duplicates only. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Wrapper/scanner errors name the failed step and the engine path; the ambient bullet carries the consequence, the carrier and the owner path. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The generator's additive-only constraint was measured and recorded (R-10) instead of being papered over; no A-14…A-24 clarification was rewritten. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory; the only runtime path is the sanctioned, git-ignored `.specify/.tmp/` fixture root. |
| XVIII | Grounded Naming | ✅ Pass | `line-run.sh` follows sibling `line-registry.py` and the user-fixed name; the scanner path is fixed by A-16. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | A user wraps one command and reads one scan; names (`line-run`, `line-registration-scan`) state what they do. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | Tests run through the runner's parallel default; per-test temp registries keep them parallel-safe; no `--full` and no reduced selection. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | `[[STR-001]]` answers `-h/--help/--version` with zero side effects and rejects undeclared options (C-01…C-05, C-19); the read-only scanner keeps help plus non-zero unknown-option rejection (scan C-01…C-03). |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | Stage re-read the RULES and the bound clarifications after each core step; one correction applied (R-10 carrier) and disclosed. |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | AI-authored change follows `.specify/workflow/git.md` (temp-branch model, merge to `master`); review reads merged history, no PR, no separate ledger. |

**Gates Status**: ✅ All 23 gates pass; no `Partial` or `Fail` row, so Complexity Tracking is `N/A`.

**Re-check after Phase 1** (2026-11-16): the same 23 rows were re-judged against the landed artifacts (`data-model.md`, three contracts, `quickstart.md`, `feature-ref.md`); no row changed state and no new justification is required.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`.*

### T-001 — 包装器强制登记，而非只写义务让调用方手动登记

- **decision**: 交付 `[[STR-001]]` 包装器，把「登记」变成执行批处理命令的前置条件（fail closed），而不是只在 owner 文档里要求调用方自行调引擎。
- **antithesis**: 只写义务 + 调用方手动调用 `[[STR-002]]`；当团队已把 registry 调用固化进批量脚本模板、且不愿在命令与项目之间再加一层 shell 进程时它更优——少一个进程层，调用方完全掌控 id 与事件序列。
- **binding_constraints**:
  - pole_a: 登记必须先于命令启动，否则长任务在 digest 中仍然不可见。
  - pole_b: 调用方必须保留对命令参数、stdout 与退出码的完全控制，包装器不得改写它们。
- **discriminating_evidence**: 在隔离 registry 下运行同一条批处理命令两次——未包装一次、经包装器一次——运行期各读一次 digest；未包装输出 `[[STR-006]]` 且 exit 3，包装输出列出该 line 且 exit 0。结果二值。
- **expected_sacrifice**: SC-004 Source ↓ 每个长任务多一次登记与关闭调用；双失败时的退出码优先级与 stderr 诊断成为必须长期维护的表面。
- **revision_trigger**: 一个迭代内出现 ≥2 次「包装器 fail-closed 阻止了本应允许的短脚本」且调用方明确要求绕过 → 重开，改为可选包装加义务声明。

### T-002 — 机械判据 owner 取扫描器模块常量，而非声明层 fact

- **decision**: 长任务的机械判据（标记集、自声明标记、合规形态、默认根）由 `[[STR-009]]` 的四个模块级常量唯一拥有，测试以 `import` 读取。
- **antithesis**: 声明层 fact 文件（`shared/declarations/facts/`）；当第二个引擎也必须消费同一判据、且需要机器可读注册与版本化时它更优——一处声明、多处读取。
- **binding_constraints**:
  - pole_a: 判据必须恰有一个机器可读 owner，其他表面只引用。
  - pole_b: 交付面必须封闭：不新增 fact 注册、不扩大 SC-009 的 delta。
- **discriminating_evidence**: 对一次完整实现比对 `shared/declarations/facts/` 的条目数增减与 `git diff --name-only` 的集合：取常量支 → 条目数不变且 delta ⊆ 交付清单；取 fact 支 → 新增一个 fact 条目。结果二值。
- **expected_sacrifice**: SC-002 Source ↓ 判据只能被 Python 直接消费；shell 或其他语言的检查器必须调用扫描器而不是读声明。 
- **revision_trigger**: 出现第二个消费同一判据的引擎且它无法 import 扫描器 → 重开，迁移为声明层 fact 并保留扫描器为执行者。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/102-line-registry-registration/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (R-01…R-13, U-1…U-5, baseline measurements)
├── data-model.md        # Phase 1 output (E1–E8, INV-01…INV-12)
├── quickstart.md        # Phase 1 output (S-1…S-7; S-7 executed)
├── contracts/           # Phase 1 output (3 files, 52 clauses)
├── feature-ref.md       # Phase 1 output (Feature 088 binding + delivery surface)
├── test-evidence/       # stage readings and executed commands
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement — NOT created here)
```

### Source Code (repository root)

```text
scripts/bash/            # line-run.sh (new wrapper) beside the shared script-interface guard
scripts/python/          # line-registration-scan.py (new read-only scanner)
shared/guidelines/       # reporting-obligations.md § 九 gains the criterion (owner edit)
skills/internal/run-team/# SKILL.md gains register / heartbeat / close at §5 / §6 / §7
templates/commands/      # status.md gains the registry-only sentence
templates/               # instructions-template.md gains one ambient bullet
tests/contract/          # CLI contracts + wiring guards (3 new files)
tests/integration/       # wrapper/digest behaviour + live reading (2 new files)
```

**Structure Decision**: the feature extends the existing framework layout — two new scripts in the already-owned `scripts/` trees, four text edits in their existing owners, five test files in the existing `tests/` categories, and mirrors/copies produced by the existing generators. No new top-level directory, no new package, no runtime service.

### Mirror Obligations *(mandatory — every changed file has a mirror or a generated copy)*

**Baseline drift measured before any edit** (`sync-mirrors.py --check`, rc=2): five pre-existing `DIFF` rows under `skills/external/` and two `ORPHAN` mirrors (`.specify/scripts/line-registry.py`, `.specify/scripts/stage-runner.sh`). The Verify cells below mean **no NEW drift on the pairs this spec touches**, judged against that baseline — never "all green".

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/bash/line-run.sh` (new) | `.specify/scripts/bash/line-run.sh` | `sync-mirrors.py --write --only scripts` then `--check`; `diff -q` on this pair empty; baseline drift unchanged |
| `scripts/python/line-registration-scan.py` (new) | `.specify/scripts/python/line-registration-scan.py` | same pair check; the `projected[...]` rows stay ok |
| `shared/guidelines/reporting-obligations.md` | `.specify/shared/guidelines/reporting-obligations.md` | `sync-mirrors.py --check` shows `ok shared/ == .specify/shared/`; `diff -q` empty |
| `skills/internal/run-team/SKILL.md` | `.specify/skills/internal/run-team/SKILL.md` | `ok skills/internal/ == .specify/skills/internal/`; `diff -q` empty |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` | `ok templates/ == .specify/templates/`; `diff -q` empty |
| `templates/commands/status.md` | `.claude/commands/speckit.status.md`; `.github/prompts/speckit.status.prompt.md`; `.qoder/commands/speckit.status.md`; `.opencode/command/speckit.status.md` (via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror — retired) | `regen-command-copies.py --check` rc 0 (measured 2026-11-16) |
| `templates/instructions-template.md` (ambient bullet → live) | `.specify/instructions.md` + `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` (symlinks to it) | The bullet reaches the live file through the `/speckit.instructions` section-level refresh (the generator is additive at top-level-section granularity only — measured, research R-10); verify by a contract test asserting the bullet exactly once in the live file and the four symlinks resolving to it. Generator output alone is **not** the verification. |

## Execution Premises

Owner of this table's shape, its `Status` / `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises. The ids below are the targets cited by `requirements.md` RS-001…RS-006.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | A CPython interpreter `>=3.8` is available and the scanner is implementable with the standard library only. | `pyproject.toml:5` (`requires-python = ">=3.8"`); `python3 --version` → 3.11.0rc1; scan design imports only `os`/`re`/`pathlib`/`argparse`-class stdlib. | verified | — |
| EP-002 | The unique test entry is `scripts/bash/run-tests.sh`, pytest is installed, and new tests can be parallel-safe through per-test temp registries. | `pyproject.toml:21` (`pytest`); `python3 -m pytest --version` → 9.0.3; runner header (parallel default, `--names-out`); `tests/fixtures/line_fixtures.py:50-58` isolates `SPECIFY_LINE_REGISTRY_DIR`. | verified | — |
| EP-003 | The registry engine at both declared candidates exposes `register` / `update` / `deregister` with the documented requirements and terminal-state rule. | `skills/external/sdd-loop-driver/scripts/line-registry.py:81-94,576-700,808-900`; both candidates answer `--version` (`line-registry.py 0.0.22`); `register` requires `--project-dir`/`--repo-root`; `deregister` requires `--reason`; `closed` is terminal. | verified | — |
| EP-004 | The digest reads only the registry, hides closed lines, renders the empty set explicitly, and owns the stale bound. | `scripts/python/status-digest.py:74,81-91,985-989,1097`; executed lifecycle on 2026-11-16: empty → `nothing-running` rc 3, active → listed rc 0, closed → `nothing-running` rc 3. | verified | — |
| EP-005 | A POSIX `bash` plus the shared script-interface guard is available, and the wrapper needs no other runtime. | `bash --version` → 5.1.16(1)-release; `scripts/bash/script-interface.sh` present and already consumed by `scripts/bash/run-tests.sh`; no third-party import planned. | verified | — |

## Inherited Blockers

Dependency set: none

No dependency artifact is declared: the parent Feature 088 is `Completed` and its § 九 contract is extended, not repaired, so no blocked or deferred row is inherited.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | none | not-applicable | — | this-slice | No dependency artifact was declared; nothing is inherited. |

## Complexity Tracking

N/A — the Constitution Check has no `Fail` or `Partial` row, so there is nothing to justify.

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed (2026-11-16):

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | `research.md` | 13 decisions (R-01…R-13), 5 unknown adjudications (U-1…U-5), 10 baseline measurements |
| Data model | `data-model.md` | 8 entities (E1–E8), 12 invariants (INV-01…INV-12) |
| Contracts | `contracts/` | 3 files: `line-run.contract.md` (19 clauses), `line-registration-scan.contract.md` (17), `wiring-surfaces.contract.md` (16) — 52 total |
| Quickstart | `quickstart.md` | 7 scenarios (S-1…S-7); S-7 executed with pasted output, S-1…S-6 carry per-example premises and pinning tests |
| Feature reference | `feature-ref.md` | Feature 088 binding + 24-path delivery surface |

Drift from the Phase 0 expectation: none in scope. One carrier expectation changed during research and is recorded rather than silently applied — the ambient bullet cannot arrive through `generate-instructions.sh` (additive at section granularity), so R-10 routes it through the `/speckit.instructions` section-level refresh; no generator edit is planned and the delivery surface is unchanged.
