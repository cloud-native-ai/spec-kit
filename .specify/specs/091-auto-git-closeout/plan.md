# Implementation Plan: Automatic git Close-out（自动收口）

**Branch**: `master` | **Date**: 2026-11-09 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `091-auto-git-closeout` → Feature 091 Automatic git Close-out（自动收口）
**Input**: Specification from `.specify/specs/091-auto-git-closeout/requirements.md` (28 FR / 8 SC / 3 runtime rows; clarify settled with C-1…C-16)

## Summary

Today every retained write ends with a *manually spoken* "commit, merge, push". This plan makes it a **fixed last
step of the write lifecycle**, driven entirely by the workflow model the project already declared:

```text
declaration   .specify/workflow/git.md managed block  +  Closeout / Closeout remotes   (owner: git-utils scope A)
lifecycle     Artifact Commit  ->  Feedback / Documentation  ->  Close-out step        (owner: the canonical commit step)
executor      git-utils scope A `closeout`  ->  sequence derived per declared model   (owner: the skill)
unattended    SDD driver U6 / house-keeping / feedback digest  ->  the same step      (pointer, never a second mechanism)
```

The plan changes **no** new command, engine script, daemon, branch registry or store. It adds two declaration rows to an
existing block and its shipped template, one named operation to an existing skill, one lifecycle section to an existing
owner, one probe handler row (whose compiled faces are generated), and one contract-test module plus a fixture helper. The
receiver of the receipt is a **close-out receipt file** — one file per run, timestamp-named — because the records the
step settles are one-file-per-entry and already retired by `record-retention.py` on their own schedule (clarify C-10).

The plan's largest open risk is not design: it is that **`push` sits in the existing destructive list**. The feature's
answer is architectural, not an exemption — the declaration in the managed block *is* the standing authorization
(FR-017), the destructive class and its owner stay untouched (FR-018), and every push still resolves its remote through
the block's read-only role marking (FR-013).

## Technical Context

**Language/Version**: Markdown for every rule surface (managed block, block asset, skill scope A + one reference, the
commit-step owner, the probe registry, the instructions template); Python `>=3.8` for the contract tests and the fixture
helper (`pyproject.toml:5`; measured interpreter CPython 3.11.0rc1, `git version 2.43.5`, `pytest 8.4.2`).
**Primary Dependencies**: none new — zero third-party imports; the executor is `git` itself, provided by the host
(`requirements.md` RS-001), plus the stdlib-only test helper.
**Storage**: one new per-run artifact class — the **close-out receipt**, `one file per run`, timestamp-named, under the
record root the retention engine already owns (`.specify/memory/` sibling of `exec-quant/` / `feedback/` / `session/`),
written once and never rewritten (FR-028; Concurrent Development Safety). No aggregate, index, ledger or second registry.
**Testing**: `tests/contract/` — a new module `test_git_closeout_contract.py` (declaration, value domain, four model
sequences, pointer duties, no-second-branch-table, SC-004/SC-008 closed-set claims) plus a fixture helper in the
new `git-closeout` fixture directory that builds one throwaway repo + local bare remote per model in a sanctioned temp root.
**Target Platform**: any host with `git` and the framework installed; the surfaces are plain Markdown shipped by
`specify init`, the fixture runs on Linux/macOS with CPython and no network.
**Project Type**: SDD framework (shared workflow + definitions + a bundled skill + templates + contract tests), a
self-hosting repository. Two hats named per FR: rows 1–4 are *framework-source* edits that reach this repo's `.specify/`
through the mirror machinery; row 5 onwards is shared content the same machinery projects.
**Performance Goals**: no runtime performance surface. The only cost target is **invocation cost**: a `closeout` that has
nothing to do (read-only run, or a model whose target state is already current) MUST exit after the block read and one
status probe, and a dry run MUST write nothing (FR-016 / FR-019 / SC-006).
**Constraints**: zero new `/speckit.*` command; zero new engine script; zero second branch table or branch registry
(FR-003 / FR-027); never `git add -A` (FR-014); no automatic force-push (FR-012); never push the read-only upstream
(FR-013); the confirmation-gate owner is referenced, never copied (FR-018).
**Scale/Scope**: 28 FR / 8 SC; 11 delivery-surface rows in `feature-ref.md` (7 edited files this plan lands, 1 contingent,
3 generated/test rows); 4 contract pages under `contracts/`; 8 quickstart scenarios.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Rendered by enumerating every `### <numeral>. <name>` heading of `.specify/memory/constitution.md` (v1.19.0) in file
order; the `(NON-NEGOTIABLE)` annotation is carried verbatim where the principle block holds it (principle VII alone).

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design clause below cites FR/SC; the 28 FR / 8 SC spec is the input and the § Contract Index maps each page to the FRs it discharges. |
| II | Feature-Centric Development | ✅ Pass | Feature 091 has no row yet in `.specify/memory/features.md` (measured: 85 rows, last is 090) — this plan **creates** the row and the matching detail page under the feature memory tree, and lands status `Planned` (§ Feature Integration), never `Implemented`. |
| III | Intent-Driven Development | ✅ Pass | The user's verbatim goal ("提交,合并,推送 … 不需要每次都手动触发 … 需要和 git workflow 相结合") is the § Summary shape and the `T-001`/`T-004` decisions; the design brief's two open questions were settled at clarify (A5 / A6) and are not re-opened. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Every clause in `contracts/` names its guard, and no guard is claimed here — they are `tasks` work with a red-first obligation; the measured baseline for the modules this plan touches is `835 passed` (evidence `test-evidence/plan-gates.txt` § 4), so the criterion is *no NEW failure*, never "green". |
| V | AI Agent Integration Standards | ✅ Pass | No host-specific surface is hand-written; the one new compiled face is rendered by `probe-utils.py --action compile-embeds` (FR-021), and per-tool command copies are regenerated, never edited. |
| VI | Continuous Quality & Observability | ✅ Pass | The close-out **report** (commit hash, merge result, push target and result, or the failing stage plus exact command) is specified as an output contract (`contracts/closeout-lifecycle.contract.md` C-4); nothing is fabricated — an unrun step reports itself unrun. |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | requirements → clarify (settled, U4 pass) → this plan; feature status advances `(n/a) → Planned` only. The feature-reuse-first gate is satisfied by a *new* feature row because no existing feature owns git close-out (searched: 090/089/088 are re-anchoring / script interface / visualization). |
| VIII | Code as the Single Source of Truth | ✅ Pass | Every fact below was measured today against the tree (§ Phase 0), including the negative facts: `closeout` does not exist in `SKILL.md`, the block carries no `Closeout` row, and `artifact-commit-step.md` still says the step "does not push". |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Zero new command/engine/daemon/scheduler/registry; the whole feature is declarations + one lifecycle section + one skill operation, and the receipt reuses the existing per-entry store shape instead of a new mechanism. |
| X | Documentation Naming & Location Conventions | ✅ Pass | The four contract pages use the established `<topic>.contract.md` shape under the spec's `contracts/`; the fixture lives under the existing `tests/fixtures/<feature>/` convention; no new top-level directory. |
| XI | Dogfooding (Self-Application) | ✅ Pass | **Two hats named**: `skills/external/git-utils/*` and `shared/*` are framework sources (they reach this repo's `.specify/` by mirror projection — § Mirror Obligations); the single client-side instance in row 1 is this project's own state file, which deliberately carries an instance rather than the template. Dogfood rule applied: the defect class "one operation's prose lives in a second place" is fixed at the mechanism (the skill scope A + one reference), not patched per example. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `sync-mirrors.py`, `regen-command-copies.py`, `probe-utils.py`, `workspace-guard.py`, `scan-confirmation-gates.py`, the driver's `pre-analyze-check.py` / `decomposition-check.py` / `overlap-check.py`; the executor is the skill's own reconcile engine, not a second script. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Targets **Reliable Delivery** (the artifact+records reach trunk without a spoken command, and a failed push is surfaced rather than swallowed) and **Controlled Execution** (the sequence is derived from a declaration, not improvised per run). |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Model/branch roles/remote roles stay owned by the managed block; the close-out semantics by the commit-step owner; the destructive list by `confirmation-gates.md`; the four-model menu by the skill. Each consumer is a pointer — § Complexity Tracking row XIV records the one place where the *reverse* holds (the skill is the menu owner the block reuses by reference). |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `quickstart.md` defines 收口 / `Closeout` / receipt / 只读上游 at first use and gives the exact command and expected reading for each scenario; the close-out report's shape is specified in plain terms (hash, branch, remote, result). |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | § Phase 0 records six measured premises; three decide-class findings (`F-1` `git add .` in the execute reference, `F-2` SC-004's existing `== 27` pin, `F-3` the missing 091 feature row) are dispositioned as in-scope work or escalated, not silently swept. The clarify stage's outstanding gate defect (`pre-analyze` `clean_cell`) is carried as a framework observation, not repaired from here. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | Fixture repos are created under `tempfile.TemporaryDirectory()` (A10; `temp-directory-discipline.md` § 5 exception) and teardown is verified; evidence lands in the already-sanctioned `test-evidence/`. |
| XVIII | Grounded Naming | ✅ Pass | 收口 / `close-out` come from the user's own wording and the existing block's phrasing ("close-out discipline"); `Closeout` / `Closeout remotes` are the clarify-fixed literals (STR-001/002); `closeout` is the git-utils operation-name convention (`sync`, `merge`, `push` are the existing family). |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | Execution class ⇒ § Document Structure is **not** required and is omitted (the template says an execution-class line MUST NOT be asked for it); the one user-visible surface added is a declaration row the user fills in, a dimension they already read. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | The new contract module is a pure-read collection test plus a fixture test that builds 4 repos in a temp root; the fixture builds are independent and `pytest -n` safe (each test gets its own `tmp_path`), no serial-only resource is introduced. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | This feature adds **no** script. The fixture helper is a pytest helper module (outside the required set); if implement finds it must become executable, `script_interface_cli.py` applies. |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | The plan's rules-in-force are re-read at each section (unattended / no approval request / spine-before-action / workspace guard / fast-fail / gates / budget); § Direction audit at stage end carries the verdict. |

**Gates Status**: ✅ All 22 principles pass; no `Fail` and no `Partial` row ⇒ § Complexity Tracking carries no violation row (it records one design tension note instead, which is not a violation).

**Re-check after Phase 1** (2026-11-09, after `research.md` / `data-model.md` / `contracts/` / `quickstart.md` /
`feature-ref.md` update landed): the table was re-read against the Phase 1 artifacts — no row moved. Two rows were
strengthened by measurement rather than weakened: row IV's baseline is now the measured `835 passed` on the three
modules this plan touches, and row XIV gained the explicit reverse-reference note that `T-005` records.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold:
`.specify/shared/guidelines/decision-tension.md` — read from the repository root. This section lists the field names
and points at that file; it does not restate the criteria table, the rejection list or the threshold table.*

Five decisions in this plan clear the owner's load-bearing threshold (irreversible / cross-team / high blast radius /
touches a constitution MUST). They are recorded below; `T-005` is the one that touches a MUST.

### T-001 — 收口写“回执”，不重写也不删除记录文件

- **decision**: 收口的记录提交写一条**收口回执**（一文一件、时间戳命名），列出本次涵盖的记录路径 + 动作 + 占用它们的提交哈希 + 读法指针；不重写、不删除任何 `exec-quant/records/`、`memory/feedback/` 等记录文件本身。
- **antithesis**: 让收口把本次运行的记录文件**再提交一次**（或在收口时删除已提交的记录），使“记录提交”真的包含记录内容；当一个项目希望 `git log` 里一次运行的记录可以整体检出、且没有独立的记录保留引擎时它更优——历史自解释，不依赖回执索引。
- **binding_constraints**:
  - pole_a: FR-006 要求记录提交可归因且同一条记录不得同时出现在两个提交里；记录文件若再提交一次即违反。
  - pole_b: A19 要求收口不与 `record-retention.py` 的退役泳道争写同一文件——删改记录文件就是争写。
- **discriminating_evidence**: 在夹具仓库里跑一次收口，对 `git log --name-only` 中被记录提交触达的路径取集合：结果二值——集合里出现任何 `exec-quant/records/*.json` 或 `memory/feedback/*.md` 原始记录文件（否）／只出现回执文件（是）。为“否”时回执读法成立。
- **expected_sacrifice**: SC-001 Source ↓ “提交归属”只能断言到回执层，`git show <commit>` 不再直接展开记录正文，读者要多一跳才能看到被涵盖的记录。
- **revision_trigger**: 若两个迭代内出现 ≥2 次“回执存在但无法据其定位被涵盖记录”的事故（路径或哈希失效）→ 重开，改为在回执中内联记录摘要并重建定位规则。

### T-002 — 标准授权落在托管块的一个值上，而不是扩一张破坏性白名单

- **decision**: `Closeout: commit+merge+push` 是写在 `.specify/workflow/git.md` 托管块里的**项目级标准授权**，收口序列内的常规推送据此免去逐次确认；破坏性清单与治理保留清单本身一字不改。
- **antithesis**: 在 `confirmation-gates.md` 的破坏性清单里为“收口推送”增加一条白名单/豁免项，让推送天然不属破坏性桶；当想让“某类推送永不确认”跨项目统一成立、且不依赖任何状态文件时它更优——规则集中在一处。
- **binding_constraints**:
  - pole_a: FR-018 要求确认门 owner 保持唯一真源且任何面不得复制其清单；开一条豁免就是在本特性面里改判破坏性桶。
  - pole_b: FR-017 要求标准授权可被撤回为 `ask`，且撤回后行为立即回到“呈现并等待”——白名单形态没有可撤回的粒度（删条目即全局改判）。
- **discriminating_evidence**: 在一个夹具项目里把 `Closeout` 从 `commit+merge+push` 改成 `ask` 并重跑收口：结果二值——收口不再推送且不阻塞（是）／仍推送（否）。为“是”时“值即授权”成立；为“否”时授权另有来源。
- **expected_sacrifice**: SC-004 Source ↓ 破坏性清单无法表达“某类推送在特定声明下免确认”，只能由收口的实现层解释该声明；跨项目读者读清单时看不到这条授权的存在。
- **revision_trigger**: 若后续出现第二个特性也想以“声明即授权”跳过确认，且两者语义不同 → 重开，把授权形态上提到 `confirmation-gates.md` 作为一等条目，而不是各自解释。

### T-003 — 远端推送目标只从 `Closeout remotes` 取，并对每个目标复核只读角色

- **decision**: 收口的推送目标集合**只**来自 `Closeout remotes`；每个目标在推送前按托管块的角色标记复核，标为只读上游的远端一律排除，即使它出现在声明里或调用方指令里。
- **antithesis**: 复用仓库已配置的 `git remote` 列表（或 `branch.<name>.remote`）作为推送目标发现来源；当项目没有维护声明、或声明与远端实际情况不一致时它更优——推送目标永远与 `git remote -v` 一致。
- **binding_constraints**:
  - pole_a: FR-002 声明之外的任何位置 MUST NOT 参与推送目标判定；本仓 `origin` 指向上游且只读（实测 `git remote -v`），按 `remote` 发现会直接推只读上游。
  - pole_b: 声明可能与远端实际存在偏差（远端被改名/删除）；不读取实际远端会让收口在不存在或误命名的远端上失败。
- **discriminating_evidence**: 在夹具里声明 `Closeout remotes: origin, upstream`，其中 `origin` 被标只读上游、`upstream` 为可推送：结果二值——推送只落 `upstream` 且报告中 `origin` 未被触达（是）／任一调用把 `origin` 当目标（否）。为“是”时“声明 + 复核”成立。
- **expected_sacrifice**: SC-006 Source ↓ 本仓干跑只能证明“推导出的目标集合不含只读上游”，不能证明远端真实可推送（干跑不推）。
- **revision_trigger**: 若两个迭代内出现 ≥2 次“声明了不存在的远端导致收口首个失败” → 重开，增加一个可选的远端发现回退（仍受只读复核约束）。

### T-004 — 收口是既有提交步骤之后的**同一**步骤序列里新增的一段，不是新的命令或引擎

- **decision**: 收口作为 `shared/workflow/artifact-commit-step.md` 之后的**新生命周期段**落在同一 owner 内，执行器是 `git-utils` 作用域 A 的一个具名操作；无人值守机制调用同一段。
- **antithesis**: 新增一个 `/speckit.closeout` 命令（或一个独立的 closeout 脚本引擎），由用户或调度器调用；当需要“独立触发一次收口而不做任何其他事”、或需要脱离任何命令包装地复用收口时它更优——收口成为一等入口。
- **binding_constraints**:
  - pole_a: FR-027 / A2 明确禁止新增 `/speckit.*` 命令与第二套引擎；宪法 IX 禁止为同一谓词造第二实现。
  - pole_b: FR-020 要求无人值守机制全部收敛到同一收口步骤；独立入口会让“谁在收口”出现两个答案。
- **discriminating_evidence**: 在仓库中检索“除 `git-utils` 作用域 A 的 `closeout` 外，是否还存在第二个可执行收口入口”：结果二值——检索到第二入口（否，则不成立）／只检索到同一操作及其指针（是）。为“是”时单一步骤成立。
- **expected_sacrifice**: SC-005 Source ↓ 用户不能“只收口不做别的”，必须走某个命令或技能的 wrap-up；临时的纯收口诉求要靠手动执行推导出的命令。
- **revision_trigger**: 若两个迭代内出现 ≥3 次“用户请求单独执行收口而框架无入口” → 重开，评估是否把收口暴露为一个轻量命令（并同步修订 FR-027）。

### T-005 — 标准授权触及宪法 VII 的 MUST：授权来自声明，确认门不被削弱

- **decision**: 把“推送免逐次确认”做成**可撤回的声明值**（`Closeout`），并在同一变更里用结构不变量测试（SC-004 / SC-008）证明破坏性边界**未缩小**。
- **antithesis**: 保持推送永远是逐次确认，收口只做到“合并 + 呈现推送命令”；当一个组织的安全规范要求“任何推送都必须有人在场”、或项目还没有可信的声明维护纪律时它更优——自动化不越过人工闸门。
- **binding_constraints**:
  - pole_a: 宪法 VII / `confirmation-gates.md` 的 MUST 要求破坏性动作保留前置确认，且扩展/收窄清单只能以修订 owner 的形式进行。
  - pole_b: 用户目标是“不需要每次都手动触发”；若推送永远要确认，收口对无人值守运行的价值只剩本地合并，故事 US2 / US3 的核心价值不成立。
- **discriminating_evidence**: 对照本特性第一个实现提交前后的 `scan-confirmation-gates.py` 读数，并按名比较门控集合：结果二值——集合不缩小且无任何面复制清单纯文本（是，则授权未削弱边界）／任一门消失或出现复制（否）。为“是”时 T-005 成立。
- **expected_sacrifice**: SC-004 Source ↓ 若未来某条治理门被无关特性新增，`== 27` 的既有 pin 与本特性的“集合不缩小”断言会同时存在两套维护纪律，须同批处理（`F-2`）。
- **revision_trigger**: 若 `scan-confirmation-gates.py` 的基线在任一后续特性中下降，或出现任何面复制确认门清单 → 立即重开，把标准授权降级为 `commit+merge` 并把推送恢复为逐次确认。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/091-auto-git-closeout/
├── plan.md              # This file
├── research.md          # Phase 0 — R1…R10 measurement record
├── data-model.md        # Phase 1 — 6 entities (E-1…E-6), 14 validation rules (V-1…V-14)
├── quickstart.md        # Phase 1 — 8 scenarios (S-0…S-7)
├── contracts/           # Phase 1 — 4 pages, 26 clauses
│   ├── closeout-declaration.contract.md
│   ├── closeout-lifecycle.contract.md
│   ├── closeout-executor.contract.md
│   └── closeout-verification.contract.md
├── feature-ref.md       # Phase 1 — updated delivery surface + FR→contract map
└── tasks.md             # Phase 2 (/speckit.tasks — not created here)
```

### Source Code (repository root)

Only the directories this spec actually touches, one line each:

```text
.specify/workflow/                      # git.md — this project's state file: the two declaration rows land in its managed block
skills/external/git-utils/              # scope A: SKILL.md (the named `closeout` operation) + references/ (the command surface)
skills/external/git-utils/assets/       # git-workflow-block.md — the shipped block template gains both rows in placeholder form
shared/workflow/                        # artifact-commit-step.md — the close-out lifecycle section; external-dispatch-recipes.md (contingent)
shared/definitions/                     # probe-definitions.md — one Handler row (+ bindings) for the close-out step
templates/                              # instructions-template.md — at most one pointer line in `## Git Workflow`
tests/contract/                         # the feature's guard module (test_git_closeout_contract.py)
tests/fixtures/                         # the new git-closeout fixture directory: repo + fake-remote builder for the guard module
.specify/memory/                        # features.md row 091 + the feature's detail page; per-run receipts at run time
```

**Structure Decision**: the feature extends three existing frameworks trees by additive rows/sections and adds exactly
one new test module plus one fixture directory. It creates **no** new top-level directory, no new skill, and no new
engine. The one new *runtime* path is the close-out receipt directory, which is a sibling of the record stores the
retention engine already owns — the store layout is decided in `data-model.md` § E-4 and is a `tasks` item to create,
not a plan-time directory.

### Mirror Obligations

Baseline measured **before** this plan's edits — per the template's BASELINE DRIFT rule the criterion is *no NEW
drift*, never an absolute exit code. The three mirror pairs this spec touches are `shared` → `.specify/shared`,
`skills/external` → `.specify/skills`, `templates` → `.specify/templates` (`scripts/python/sync-mirrors.py` `MIRROR_PAIRS`).

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/workflow/artifact-commit-step.md` | `.specify/shared/workflow/artifact-commit-step.md`; `.specify/shared/workflow/external-dispatch-recipes.md` only if that file is also edited | `diff -q` on the pair after `sync-mirrors.py`; judged as *no NEW drift* against the baseline captured in the same run |
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md`; **plus** every `## Wrap-up` face rendered by `probe-utils.py --action compile-embeds` (the shipped command templates and their runtime mirror, plus the per-tool command copies; the shipped skill sources and their runtime mirror, plus the per-tool skill copies) | `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` reports zero drift **after** the compile run; never hand-edit a face |
| `skills/external/git-utils/SKILL.md` | `.specify/skills/git-utils/SKILL.md` | `sync-mirrors.py`; `diff -q`; no NEW drift |
| `skills/external/git-utils/assets/git-workflow-block.md` | `.specify/skills/git-utils/assets/git-workflow-block.md` | same |
| the new sibling close-out reference under `skills/external/git-utils/references/`, plus a one-line pointer in the existing three-tier reference | `.specify/skills/git-utils/references/…` | same; a **new** reference file MUST also be listed in `SKILL.md` § Resources, and the `skills/external` → `.specify/skills` pair covers it |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md`; then `.specify/instructions.md` via `/speckit.instructions` (deliberately **not** run from a stage worker) | `diff -q` on the mirror pair; the live instructions refresh is declared as an explicit `tasks` item with the command named — measured today: the `## Git Workflow` section is byte-identical between template and live |
| `.specify/workflow/git.md` | none — it is this project's runtime instance, not a shipped template | no mirror expected; the **shipped** placeholder form lives in the block asset above |

## Execution Premises

Owner of this table's shape, of the `Status` and `Decision` value domains and of the invalid-row rule:
`shared/workflow/acceptance-hardening.md` § Execution Premises — this table carries the column set and nothing else.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The host provides a `git` new enough for `--force-with-lease`, `merge --no-ff`, `branch -d` and `ls-remote`; no network is needed for the fixtures | `git --version` → `git version 2.43.5` (`test-evidence/plan-gates.txt` § 0); fixtures use a local bare remote on the filesystem | verified | — |
| EP-002 | `pytest` and `>=3.8` interpreters run the guard module and the fixture helper with no new third-party import | `pytest 8.4.2`; `pyproject.toml:5` `requires-python = ">=3.8"`; zero imports beyond stdlib + pytest in the design | verified | — |
| EP-003 | The three modules this plan's clauses touch are green **before** the edit, so "no NEW failure" is a meaningful criterion | `pytest tests/contract/test_git_workflow_instructions_block.py tests/contract/test_wrap_up_wording_gate_safe.py tests/contract/test_mirror_parity_suite.py -q` → `835 passed in 1.23s` (`test-evidence/plan-gates.txt` § 4) | verified | — |
| EP-004 | The managed block's read-only marking is machine-readable enough for the executor to exclude a remote by role, not by name | `.specify/workflow/git.md` carries `⚠ Remote roles` with the read-only upstream named; `assets/git-workflow-block.md` carries the same shape as guidance | verified | — |
| EP-005 | A record receipt can live beside the record stores without a new store or index | `.specify/memory/retention/` already exists as the retention engine's home (`RETENTION_REL = .specify/memory/retention`); `exec-quant/records/` (243 files), `feedback/`, `session/` are per-entry stores | verified | — |
| EP-006 | The feature has no row yet in the feature index, so this plan must create it (not advance a stale one) | `.specify/memory/features.md` carries 85 feature rows; the highest bound id is 090 — no 091 row exists | verified | — |
| EP-007 | The user's authorization for this plan stage covers local commits of this feature's artifacts but **not** a push | assignment brief § Execution Requirements ("不要 push（除非明确授权）"); `confirmation-gates.md` § 破坏性动作清单 lists push | verified | — |

## Inherited Blockers

**Dependency artifacts (declared, never implied)**: `requirements.md` (28 FR / 8 SC, clarify-settled) and
`feature-ref.md` (delivery surface, clarify-created). Neither carries an unresolved `blocked` / `deferred` / `partial`
row — `requirements.md` has 8 SCs all on the plan path and no `[~]` rows, because it is a spec and not a task list.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| — | (none) | not-applicable | — | — | No dependency record with an open disposition exists. The clarify stage's one outstanding *gate* defect (`pre-analyze-check.py` `clean_cell` on the RS-001 Contract cell) was corrected at clarify by making the cell bare, so nothing is inherited here; the parser defect itself is a framework observation owned by the driver skill. |

## Complexity Tracking

> No constitution violation exists: all 22 rows pass and no row is `Partial`, so this section carries **no** violation
> row. It records one design tension that is not a violation but that a reader would otherwise mistake for one.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none — informational: the four-model menu's owner is the git-utils skill, and the managed block references it) | FR-003 forbids the block from gaining a second branch table, so the block cannot restate the four models; the block names its model and the skill holds the menu. This is the correct direction (one owner + a reference), but it means a project reading **only** its state file cannot enumerate the models. | Copying the menu into the block is the second definition point FR-003 bans. Citing the skill's path from the block (a one-line pointer) is the admissible repair and is specified in `contracts/closeout-declaration.contract.md` C-2 — it is a reference, not a copy, so no violation is claimed. |

## Phase 0: Research Review

Standalone research is warranted: the study evaluated four external-to-the-template surfaces (an existing skill's
operation vocabulary, a probe registry's row grammar, a retention engine's receipt shape, and a destructive-action
governance list) and needed a measurement record separable from the design. Findings live in
[`research.md`](research.md) (`R1`…`R10`); the load-bearing conclusions are:

1. **The insertion point already has a "does not push" sentence, and it is the right thing to amend** (R1). Measured:
   `shared/workflow/artifact-commit-step.md` § Boundaries says *"This step commits locally. Pushing is a shared-state
   action … requires its own authorization"*. FR-008's revision is therefore a rewrite of one boundary sentence in the
   file that already owns it — no second owner.
2. **`closeout` has no existence today** (R2). No `closeout` token appears in `git-utils/SKILL.md`, the block asset, or
   `.specify/workflow/git.md`; the only occurrence in the tree is the block asset's prose "close-out discipline". The
   feature creates the name, not a duplicate of it.
3. **The Phase 0 three-way dispatch table needs no new row** (R3, confirm of clarify C-6). `SKILL.md` § Phase 0 selects
   Bootstrap / 全维度体检 / 定向收敛 by two axes (block filled? operation argument present?). `closeout` is the third
   row (filled + argument) and joins operations A–G.
4. **The command surface's home is a decision, not an inheritance** (R4). `references/execute-commands.md` is titled
   "定向收敛命令序列" and covers three-tier operations A–C plus D–G; the four close-out model sequences are not
   three-tier operations. Decision: **add a new sibling reference** `references/closeout-commands.md` and list it in
   `SKILL.md` § Resources, keeping `execute-commands.md` about its own subject (this is the mechanism fix: one
   reference per subject, not a growing miscellany). The existing file gains only a one-line pointer.
5. **The probe registry's row grammar admits one new Handler with no new Object** (R5). The `wrap-up` lifecycle point
   already binds `h-run-determination` (order 10), `h-exec-quant` (15), `h-feedback-record` (20), `h-threshold-notice`
   (30), `h-token-reflection` (40), `h-docs-sync-eval` (50). A close-out handler takes the next free order in that
   sequence; `kind=agent` with a `behavior_owner` pointer to the commit-step owner keeps the rule out of the registry.
6. **The destructive class is sound and its owner needs no edit** (R6). `scan-confirmation-gates.py` reads 27 blocking
   gates (destructive 20 / governance_kept 7 / violations 0); FR-017/FR-018 keep that file untouched. SC-004's baseline
   is therefore the 27 reading taken today.
7. **An existing test pins the gate total by equality** (R7 = finding `F-2`). `tests/contract/test_wrap_up_wording_gate_safe.py::test_confirmation_gate_budget_unchanged`
   asserts `== 27` with a comment calling it "owner fact = live scan total". This feature's gate clauses MUST assert
   *set non-shrink by name* and MUST NOT re-assert a total constant; if a future change moves the total, that pin's
   owner re-rules first. Carried as a task-level constraint, not edited here.
8. **The record stores are per-entry and `record-retention.py` already models "consume → receipt → retire"** (R8). Its
   receipts live at `.specify/memory/retention/receipts/<stamp>-<hash>.json` keyed `(store, entry_id)` and gate deletion
   with a grace window. The close-out receipt is a **different subject** (a commit's coverage, not a record's
   retirement), so it must not reuse that key or that directory — but it MUST borrow the shape: one file per run,
   timestamp-named, never rewritten (FR-028 / A19).
9. **The reference examples in the git skill contradict this repo's remote roles** (R9 = finding `F-1`).
   `execute-commands.md` opens `## 前置校验` with `git fetch origin`, and the preset push guidance pushes `origin`; in
   this repo `origin` is the read-only upstream (`git remote -v`). This is a pre-existing document-level inconsistency
   that the close-out must not inherit. Disposition: the new `closeout-commands.md` uses **no remote literal** (it names
   `<remote>` substituted from the declaration); the pre-existing examples are left as an upstream deviation recorded in
   the report, and only the one line this feature's parser consumes is corrected.
10. **The instructions surface already points at close-out, so only a pointer can be added** (R10). Measured: the
    `## Git Workflow` section of `templates/instructions-template.md` and `.specify/instructions.md` are byte-identical
    and already name `close-out` as a mechanism with a cadence. FR-022 therefore permits at most one pointer line to
    *where the step is*; the plan's decision is to add it only if implement finds the existing line insufficient, and
    the default is **no edit** (row 8 of `feature-ref.md` is marked contingent).

## Phase 1: Design Artifacts Summary

Counts below were backfilled **after** the artifacts landed on disk (never pre-written).

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | `R1`…`R10`, the measurement record behind § Phase 0 |
| Data model | [`data-model.md`](data-model.md) | 6 entities (`E-1`…`E-6`), 14 validation rules (`V-1`…`V-14`) |
| Contracts | [`contracts/`](contracts/) | 4 files, **26 clauses**: `closeout-declaration.contract.md` (C-1…C-7), `closeout-lifecycle.contract.md` (C-1…C-7), `closeout-executor.contract.md` (C-1…C-7), `closeout-verification.contract.md` (C-1…C-5) |
| Quickstart | [`quickstart.md`](quickstart.md) | 8 scenarios (`S-0`…`S-7`) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | updated delivery surface (plan-refined), FR→contract map, SC→measurement map, disclosed rulings |

**Stage gate readings (run during this stage; verbatim record in `test-evidence/plan-gates.txt`)**:

| Command | Reading |
|---------|---------|
| `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/091-auto-git-closeout --stage plan --repo .` | see `test-evidence/pre-analyze-plan.json` (re-run after the Phase 1 artifacts landed; the reading below § Phase 1 is the post-landing one) |
| `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/091-auto-git-closeout/requirements.md` | `{"decision": "proceed", "measured": {"fr_count": 28, "fr_ceiling": 120, "task_ceiling": 160}}` — no split |
| `python3 .specify/skills/sdd-loop-driver/scripts/overlap-check.py --spec-dir .specify/specs/091-auto-git-closeout --repo .` | `decision=overlap checked=82 overlaps=36` — identical to clarify C-16 (all against completed lines, 0 active) |
| `/usr/bin/python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/091-auto-git-closeout --json` | see `test-evidence/decision-tensions-plan.json` |
| `/usr/bin/python3 scripts/python/validate-requirements.py .specify/specs/091-auto-git-closeout/requirements.md` | `status: ok`, 0 error / 0 warning |
