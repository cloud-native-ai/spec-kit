# Implementation Plan: Humanize Run Output（动作输出的人类友好化）

**Branch**: `080-humanize-run-output` | **Date**: 2026-10-30 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `080-humanize-run-output` → Feature 062 Humanize Command（动作输出人类友好化）
**Input**: Specification from `.specify/specs/080-humanize-run-output/requirements.md`

## Summary

把 `/speckit.humanize` 从「文本转换命令」重定位为「动作输出的人类友好化命令」：调用者给一条**指令**，
命令经既有 `run-agent` 载体派发**恰好一个**执行体跑完它，再由 humanize 主会话结合动作结果、项目治理与
会话上下文，写成一份五节结构化报告（结论 → 关键变化 → 证据 → 风险与限制 → 下一步）。旧的内容改写
入口 `--file` / `--inline` 保留为显式备用源；裸文本改为指令解释，并在每次裸文本调用时输出一行迁移提示。

技术路线是**零新增运行时**：没有新脚本、没有新命令、没有新技能、没有新的持久存储。可执行面仍然是
一份命令模板 + 一份技能（加 `references/` 细则）+ 一套既有再生成入口。唯一新增的落盘面是一个运行期
占位文件（`.specify/.tmp/humanize/<run_id>.run`，受制裁临时根、gitignored、运行结束即移除），用来让
FR-030 的并发场景可判；报告默认只在会话里，显式 `--output` 才写。

设计上有三处不能默认继承既有资产，必须在设计期裁决并留痕（§ Decision Tensions）：派发走 run-agent 的
哪一半、并发观测用什么载体、命令的复杂度分类是否要变。

## Technical Context

**Language/Version**: Markdown（命令模板 + 技能契约）+ 既有 Python 3.8+ 引擎；本特性不新增脚本
**Primary Dependencies**: `run-agent` 技能（Run Mode 作为派发载体）/ 宿主原生子代理能力（`native`）/ 快速失败注入子句（owner: `shared/guidelines/fast-fail.md` § 子代理派发注入）
**Storage**: 无新持久存储。运行期占位：`.specify/.tmp/humanize/<run_id>.run`（一文一件、gitignored、结束即删）；报告默认不落盘，`--output` 时原子写
**Testing**: `pytest` 契约测试为主（`tests/contract/test_humanize_command_surface.py` 扩展 + `test_stage_class_wiring.py` 钉扎重测）；新增运行夹具 `tests/fixtures/humanize/run/`；确定性检查 `pre-analyze-check.py`、`regen-command-copies.py --check`、`sync-mirrors.py --check`、`probe-utils.py --action compile-embeds --check`、`scan-confirmation-gates.py`、`skill-shape.py`
**Target Platform**: 任何支持 Spec Kit 的 agent 宿主；无原生派发通道时降级为会话内执行并如实标记
**Project Type**: single（框架源码 + 自举运行时双帽；改动落在 `templates/`、`skills/`、`docs/`、`tests/`，`.specify/` 侧由再生成入口产出）
**Performance Goals**: 无吞吐目标。两条可测预算：① 技能正文 ≤ 5000 tokens（基线 ≈4090 / 123 行，实测见 `test-evidence/stage-plan-baselines.txt` § 5，判定工具 `skills/external/improve-skills/scripts/skill-shape.py`）；② 一次运行恰好一次顶层派发（1/1）
**Constraints**: 零新增阻断式确认门（判定单位是 `git diff 35ff11bc` 的新增行，基线 `test-evidence/gate-newline-baseline.txt`：added_lines=0 / blocking_hits=0）；零新增外发；零隐式写入；命令保持 `Simple`（无 `scripts:`、无 `## Feedback`）；类别与 probe 注册表不动；历史语料不改写
**Scale/Scope**: 一份命令模板 + 四份按工具副本（再生成）+ 一份技能源（`SKILL.md` + `references/`）与运行时镜像 + 一页 docs + 主契约测试与钉扎测试；需手改的活接线面由 requirements § Wiring Surface — A11 Closed Set 拥有（发现命令 + 分类规则 + 守卫），成员是基线树上的派生量，由 tasks 阶段按该节实测重算（不手写白名单）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, 18 principles in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每条设计决定都追到 FR：契约的可追溯性表是 FR→条款→测试的唯一映射（`contracts/*.contract.md` § 可追溯性），本文件不复述 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 062（`feature-ref.md`），本阶段只追加 `Latest Review` / `Key Changes` / `Last Updated`，不新建行、不回退状态 |
| III | Intent-Driven Development | ✅ Pass | Summary 与 `contracts/report-assembly.contract.md` 先给「报告要对读者做什么」，实现细节留到 tasks |
| IV | Test-First & Contract-Driven Implementation | ◐ Partial（经 VII 的 template-only 门正当化） | 本特性无运行时，交付物是命令模板与技能正文；Test-First 的形态是**先于模板改写**写/更新结构契约测试（clause→test 映射见五份契约 § 可追溯性），不是 unit/integration 测；本阶段按 docs-only 预算不跑测试（`test-evidence/plan-fix-test-budget.txt`）。判定与 `tasks.md` § Tests Mode 的同一行一致（Partial + template-only 门） |
| V | AI Agent Integration Standards | ✅ Pass | 不动 `AGENT_CONFIG` / `_ASSISTANT_TIERS`；四份按工具副本只经 `regen-command-copies.py` 生成 |
| VI | Continuous Quality & Observability | ✅ Pass | 基线读数冻结于 `test-evidence/stage-plan-baselines.txt`；breaking change 与迁移方式在模板、技能、docs 三处声明（WC-01, WC-08, CM-09） |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | 只推进到 `Planned` 之前的本阶段产物；Feature 复用优先、状态不回退（FR-029）；模板类特性的 Test-First 按 template-only 门判（契约测试验证模板内容与结构） |
| VIII | Code as the Single Source of Truth | ✅ Pass | 设计前实测接线面与注册行（`stage-plan-baselines.txt` § 6–§ 8），不靠记忆；`.specify/` 侧只由再生成入口产出 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新增脚本/服务/依赖/命令；并发机制收窄为一个 gitignored 瞬时占位文件；派发复用既有载体而非新建编排层（T-001 记录了「落一个通用执行 Agent」的替代方案被否） |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件是 `references/run-mode.md`、`references/report-shape.md`（小写、路径即语义）；不触保留名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 改动全部落框架源（`templates/`、`skills/`、`docs/`、`tests/`）；`.specify/skills/` 与四份副本由 `sync-mirrors.py` / `regen-command-copies.py` 产出（WC-05, WC-06） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `run-agent`、`regen-command-copies.py`、`sync-mirrors.py`、`probe-utils.py`、`skill-shape.py`；无新脚本 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution（派发受治理、确认缺失即停）与 Learning Capture（报告把证据与限制摊开，来源可追） |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 五节标题/载体标记 literal owner = requirements § Shared Strings；路由表 owner = IP-05；信封字段 owner = `data-model.md` § E5；封闭接线集 owner = A11；本文件只引用 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 报告本身就是受治理界面：五节结构 + 来源清单 + 语言规则（RP-12…RP-18），术语与上下文按既有 owner 写作 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 派发载荷必须携带拥有者字面量子句并要求显式异常行；缺异常行的回传不得被消费（EX-06, EX-10） |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | `references/` 是 `skills.md` 已文档化的既有形态；临时占位落 `.specify/.tmp/`（已由 `.specify/.gitignore` 匹配，`git check-ignore` 实测见基线 § 8） |
| XVIII | Grounded Naming | ✅ Pass | 用户裁定的定位名「动作输出人类友好化」贯穿 Feature 名、描述、模板与 docs；新文件名取自其承载的概念（`run-mode` / `report-shape`），不发明新术语 |

**Gates Status**: ✅ 无 Fail 行；Principle IV 为 **Partial**，经 Principle VII 的 template-only 门正当化（理由见该行，与 `tasks.md` § Tests Mode 的判定同源）。无其余未证成的 Fail/Partial 行。

**Re-check after Phase 1** (2026-10-30, against `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`): 同一 18 行逐行复核，结论不变（IV 仍为 Partial/正当化，其余 17 行为 Pass）。设计产物只增加了三类内容——把运行模式的行为拆成 `references/` 两个文件（不引入新运行时）、把并发观测收窄为一个 gitignored 占位（宪法 IX/XVII 的边界内）、把 FR→条款映射交给五份契约的可追溯性表（减少本文件的重复定义点）。没有新增门禁、没有新增外部依赖、没有新增命令。

> **说明**：本 plan 的评分与 § Post-Generation 质量自查由同一 agent 完成；按 `.specify/shared/workflow/objective-analysis-gate.md`，同作者条件成立时评分应委派 fresh-context 只读子代理。本线的执行约束明确禁止派发子代理，因此此处**未委派**，该缺口记录在 § Phase 0 的降级证据路径与下方 Handoff 中，供 analyze 阶段以独立上下文复核。

## Decision Tensions

记录形态、可采纳判据、拒绝形态与承重门槛归 `.specify/shared/guidelines/decision-tension.md`（从仓库根读取；本文件不复制判据表）。

### T-001 — 派发走 run-agent 的「机制半边」，执行体是会话级临时执行体

- **decision**: 运行模式经 `run-agent` 的 Run Mode 派发**恰好一个**会话级临时执行体：不落 `.agent.md`、不占 Agent 席位、不声明 SDD 执行席位。继承的是 Run Mode 的机制——模式选择（native / in-session）、present & dispatch、快速失败注入、结果回传；不继承的是「按名解析已存 Agent」与「SDD 席位授权探针」这两条前置（本次派发不声明席位，探针服务于 SDD 阶段派发）。
- **antithesis**: 为 humanize 落一个通用执行 Agent 定义（放在 `.specify/agents/templates/` 下，命名 humanize-executor），让 run-agent 的解析、授权、execution-config 快照与日志三联完整适用；当团队希望 humanize 的执行体也有可审计定义与固定工具集时它更优——派发链看起来就是一次正规 Agent 执行。
- **binding_constraints**:
  - pole_a: FR-007 与 A5 要求经**既有** run-agent 且不引入第二套机制；新增 Agent 定义会随框架分发给所有消费项目，并把一个非 SDD 动作塞进为 SDD 阶段设计的席位授权探针（探针要求 `--agent/--team/--seat`，临时执行体没有席位）。
  - pole_b: run-agent 的按名解析分支假定磁盘上存在定义（否则走 "agent not found"），因此临时执行体必须**显式说明**它不声称已存 Agent，否则实现者会为了「让解析通过」而真的去建一个定义。
- **discriminating_evidence**: 夹具运行结束后 `git status --porcelain` 中不出现任何 `.agent.md`，且报告首行是 `mode: subagent`（或降级时 `mode: in-session-degraded`）；一项契约测试对 `.specify/agents/` 做前后存在性比对。结果二值：出现 / 不出现。
- **expected_sacrifice**: SC-007 Source ↓ 临时执行体没有持久定义，因此拿不到 run-agent 给具名 Agent 的 execution-config 快照与日志三联；humanize 的可观测性止于报告里的派发记录行与证据指针（该审计因此依赖 `git status` + 报告，而不是运行日志）。
- **revision_trigger**: 出现两次以上「执行体需要固定工具集或固定模型档，默认继承不足以完成指令」→ 重开，改为落一个通用执行 Agent 定义，并把席位探针的适用条件写清楚。

### T-002 — 并发观测用受制裁临时根下的一次性占位，而不是「完全不落盘」

- **decision**: 运行模式在派发前建立 `.specify/.tmp/humanize/<run_id>.run`（一文一件），承载 run_id、起始时间与 `--output` 目标；仓库级与目标级各至多一个未过期占位；任何出口都移除本人占位；超过 24h 视为遗弃，只在报告里点名，不自动删除他人文件。
- **antithesis**: 完全不落盘——只在本会话内检测「已有 humanize 在跑」，跨会话/跨分支的并发交给用户判断。当团队把「零写入」理解为字面零文件时它更优：没有任何可见副作用，也不需要 TTL。
- **binding_constraints**:
  - pole_a: FR-030 要求「同一仓库已有活动运行」可判并**点名冲突运行**；纯会话内检测看不见另一个会话或另一条分支上的运行，等于把 fail-closed 降级成「看不见就不管」。
  - pole_b: A9 把零写入范围收窄为「报告或副本」；占位两者都不是，但它仍必须落在受制裁的临时根、被 `.gitignore` 匹配（实测 `git check-ignore` 命中 `.specify/.gitignore` 的 `.tmp/`）、并在运行结束时消失，否则 SC-007 的 `git status` 审计会被自己的机制污染。
- **discriminating_evidence**: 两个并发夹具运行，第二个的拒绝消息含第一个的 run_id 与起始时间；运行结束后 `ls .specify/.tmp/humanize/` 为空且 `git status --porcelain` 无新增。结果二值：点名 / 不点名、为空 / 不为空。
- **expected_sacrifice**: SC-007 Source ↓ 引入一个瞬时文件面与一个 TTL 数值（24h，owner = `contracts/invocation-parse.contract.md` IP-11 所引的 `data-model.md` § E4）；进程被强杀时可能留下遗弃占位，只能靠 TTL 与报告点名兜底。
- **revision_trigger**: 出现两次以上「遗弃占位在 TTL 内阻塞后续运行且无人清理」→ 重开，改为占位携带 pid/时间戳的自动回收，或退回纯会话内检测并把 FR-030 的可判范围写窄。

### T-003 — 命令复杂度分类保持 Simple，不把「读治理文档」算作跨流程消费

- **decision**: `/speckit.humanize` 在 027 的分类表里保持 **Simple**：模板不调用脚本、不带 `## Feedback` 步。运行模式读 `instructions` / `constitution` / `glossary` / `features.md` 被判定为**上下文装配**，不是「消费他流程的每轮制品」。
- **antithesis**: 按判据 (c) 的字面把「读 `instructions.md`（由 `/speckit.instructions` 产出）」算作跨流程消费，升为 Complex 并在模板加 feedback 步；当团队希望命令侧也进反馈通道时它更优——报告质量问题会多一条结构化入口。
- **binding_constraints**:
  - pole_a: 027 判据的既有先例把治理文档读取排除在外：`feature` 读 `features.md`、`constitution` 读宪法，两者仍是 Simple，理由写作「注册表编辑 / 非脚本化链」。
  - pole_b: 「Simple 且无 feedback」被 `tests/contract/test_feedback_command_classification.py` 从 027 表**派生**钉扎；改类必须同时改 027 表、模板与计数，属跨特性变更，不能由本特性顺手做。
- **discriminating_evidence**: 解析 027 表后 humanize 仍为 Simple，且 `templates/commands/humanize.md` 不含 `feedback-utils.py` 标记。结果二值。
- **expected_sacrifice**: SC-008 Source ↓ 命令侧不进反馈通道，humanize 的运行质量只由技能侧 wrap-up 记录；报告质量问题的入口比 Complex 命令少一条。
- **revision_trigger**: 若后续把「报告」正式定义为被某个 `/speckit.*` 消费的跨流程制品，本裁决立即重开（判据 (b) 同时成立，Simple 不再站得住）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/080-humanize-run-output/
├── plan.md              # This file (/speckit.plan command output)
├── requirements.md      # Upstream authority (30 FR / 10 SC / 15 Shared Strings)
├── checklists/          # Requirements-quality checklist (requirements stage)
├── test-evidence/       # Deterministic-check evidence per stage
├── data-model.md        # Phase 1 output (8 entities, 26 validation rules)
├── contracts/           # Phase 1 output (5 contract documents, 88 clauses)
├── quickstart.md        # Phase 1 output (7 scenarios)
├── feature-ref.md       # Phase 1 output (Feature 062 binding)
└── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created here)
```

No standalone `research.md` — Phase 0 findings are inlined below (they resolve entirely from internal
measurement, and the phase produced fewer than 50 lines of new findings).

### Source Code (repository root)

```text
templates/commands/humanize.md            # rewrite: breaking change + routing + migration (framework source)
skills/external/humanize/SKILL.md         # add run-mode routing; keep content-mode stages; stay ≤5000 tokens
skills/external/humanize/references/      # NEW: run-mode.md (dispatch/envelope/concurrency), report-shape.md (five sections)
docs/reference/commands/humanize.md       # rewrite: run-then-report positioning + migration examples
.claude/commands/speckit.humanize.md          # regenerated copy (never hand-edited)
.github/prompts/speckit.humanize.prompt.md    # regenerated copy
.opencode/command/speckit.humanize.md         # regenerated copy
.qoder/commands/speckit.humanize.md           # regenerated copy
.specify/skills/humanize/                 # runtime mirror of the skill source (sync-mirrors.py)
tests/contract/test_humanize_command_surface.py  # primary contract suite for this feature
tests/contract/test_stage_class_wiring.py        # pinned SHA of the template must be re-measured (WC-13)
tests/fixtures/humanize/run/              # NEW run-mode fixtures (success/failure/non-action/confirm/nested/degraded/concurrent)
.specify/memory/features/062.md           # extension record (Latest Review / Key Changes)
.specify/memory/features.md               # 062 row Last Updated (status stays Implemented)
```

**Structure Decision**: 本特性落在既有的「命令模板 → 单一技能」形态上，不新增顶层目录、不新增脚本：
- 命令模板继续做薄入口（保留 062 的薄入口不变式与 077 的类别接线小节），把运行模式的行为放进**同一个**
  `humanize` 技能，从而不出现第二个行为所有者（WC-02）。
- 技能的运行模式细则放进新建的 `references/` 子目录（`skills.md` 已文档化的既有形态），因为正文已经
  ≈4090 tokens / 预算 5000，把载荷字段与报告形态塞进正文会直接超预算（WC-07）。
- 可执行面之外只有三处非代码改动：Feature 登记、docs 页、测试夹具。

### Mirror Obligations

基线（2026-10-30，HEAD `35ff11bc`，实测见 `test-evidence/stage-plan-baselines.txt`）：`regen-command-copies.py --check` 与 `sync-mirrors.py --check` 均为干净树，因此本特性的判据可以写成绝对判据（exit 0），而不是「相对零新增漂移」。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/humanize.md` | `.claude/commands/speckit.humanize.md`；`.github/prompts/speckit.humanize.prompt.md`；`.opencode/command/speckit.humanize.md`；`.qoder/commands/speckit.humanize.md` — per-tool copies via `regen-command-copies.py`；no templates/commands mirror under `.specify/` (retired) | `python3 scripts/python/regen-command-copies.py` 后 `--check` exit 0（基线同样 exit 0，判据为绝对） |
| `skills/external/humanize/SKILL.md` + `skills/external/humanize/references/*.md` | `.specify/skills/humanize/SKILL.md`、`.specify/skills/humanize/references/*.md` via `sync-mirrors.py` | `python3 scripts/python/sync-mirrors.py --write` 后 `--check` exit 0；`skills/external == .specify/skills` 对零差异（基线 406 files ok） |
| `shared/definitions/*`（本特性不改） | `.specify/shared/*` | 不改即无需再生成；`sync-mirrors.py --check` 仍须 exit 0（防止误改） |

*Document Structure 章节未产出*：本线是 execution 类（`requirements.md` 的 `Flow Class: execution`），模板的类条件使该章节只对 expression 类是必需产物；此处不留空标题，以免被结构检查读成 `subsection-missing`。

## Complexity Tracking

N/A — Constitution Check 无 Fail 行；Principle IV 的 Partial 由 Principle VII 的 template-only 门正当化（不是违例，因此不需要复杂度豁免）；三处承重裁决记录在 § Decision Tensions。

## Phase 0: Research Review

**证据路径（降级说明）**：create-plan 技能建议用 Explore/子代理做一轮代码勘察；本线的执行约束禁止派发
子代理，因此改为**有界人工探针**：`git grep` 定位接线面 + 定点读取 `run-agent`、`subagent-definitions.md`、
`fast-fail.md`、027 分类契约、`sync-mirrors.py` MIRROR_PAIRS、`scan-confirmation-gates.py` 的模式表 +
四组确定性检查实跑。降级不影响结论，但同作者评分缺口见 § Constitution Check 的说明。

**无 `[NEEDS CLARIFICATION]`**：requirements 已过 clarify（30 FR / 10 SC / 15 STR），无未决标记。

关键发现（每条都改变了设计，而不是复述已知）：

1. **run-agent 的 Run Mode 有两半**。机制半边（模式选择、present & dispatch、快速失败注入、结果回传）
   正是 FR-007 要的载体；前置半边（按名解析已存 Agent、SDD 席位授权探针）假定磁盘上有定义、有席位。
   直接把指令塞进去会撞上 "agent not found" 或让探针 fail-closed，于是有了 T-001 与 EX-03 的显式排除。
2. **`subagent-definitions.md` 的三种模式与 STR-006/STR-007 不是一一映射**（native / virtual / external vs
   subagent / in-session-degraded）。external 会引入进程、凭据与网络面，与「零新增外发」冲突，因此 EX-04
   明确排除第三种模式，只留 native→`[[STR-006]]`、virtual→`[[STR-007]]`。
3. **模板字节被钉扎**：`test_stage_class_wiring.py` 的 `UNCHANGED_SHA256["humanize"]` 存的是模板的 SHA256，
   改模板必然要重测该行（FR-028 允许，但要求注明日期与理由）→ WC-13。
4. **门控扫描器的阻断模式含英文短语**：`confirmation gate`、`after confirmation`、`Confirm before`、
   `stop and confirm` 以及「确认门禁/确认门控」。本特性的新文案要谈「不绕过确认」，措辞必须绕开这些
   字面量 → WC-04 + 基线 § 判据说明。
5. **`.specify/state/` 是 tracked 的长期状态**（`git check-ignore` 未命中），把并发占位放那里会污染
   `git status` 并让 SC-007 的自审计失效；`.specify/.tmp/` 已被 `.specify/.gitignore` 匹配 → T-002。
6. **技能正文预算**：`skill-shape.py` 实测 ≈4090 / 5000 tokens、123 行，Workflow 单节已 59 行（建议上限
   40）。运行模式再加进正文必然超预算 → `references/` 拆分（WC-07）。
7. **027 分类表的 `humanize` 行是 Simple，且被测试派生钉扎**；运行模式读取治理文档是否算「跨流程消费」
   需要显式裁决 → T-003。
8. **注册面无需改动**：flow-class 台账两行仍是 `expression / reader-oracle`（A2）；probe 编译面 75 单元
   零漂移；`h-docs-sync-eval` 绑定继续有效 → WC-19。

## Phase 1: Design Artifacts Summary

（本节在 Phase 1 产物落盘之后回填；计数取自下表的实测命令输出，非记忆值。）

实测命令与输出：

```console
$ grep -cE '^## E[0-9] ' data-model.md            → 8
$ grep -cE '^\| V-[0-9]{2} \|' data-model.md      → 26
$ grep -cE '^- \*\*[A-Z]{2}-[0-9]{2}\*\*' contracts/*.md
  contracts/content-mode.contract.md        → 10
  contracts/execution-dispatch.contract.md  → 21
  contracts/invocation-parse.contract.md    → 17
  contracts/report-assembly.contract.md     → 20
  contracts/wiring-compat.contract.md       → 20
$ grep -cE '^## [0-9]+\. S[0-9]' quickstart.md     → 7
```

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 8 entities (E1–E8), 26 validation rules (V-01…V-26), 1 run state machine, 3 closed-set tables |
| Contracts | `contracts/` | 5 files / 88 clauses: `invocation-parse` 17 (IP), `execution-dispatch` 21 (EX), `report-assembly` 20 (RP), `content-mode` 10 (CM), `wiring-compat` 20 (WC) |
| Quickstart | `quickstart.md` | 7 scenarios (S1–S7) + 1 section of executed deterministic checks |
| Feature ref | `feature-ref.md` | Feature 062 binding, extension mapping, registration surface |

**契约数量模式的可判别性**：上面 `grep -cE '^- \*\*[A-Z]{2}-[0-9]{2}\*\*'` 只匹配行首的条款定义，不会
命中可追溯性表的行（后者形如 `| IP-01 |`，行首是竖线），因此计数即条款数；`data-model` 的实体计数用
`^## E[0-9] ` 只匹配实体标题，不命中 `### E1 状态机` 这类三级标题。

**FR 覆盖**：FR→条款的唯一权威映射是五份契约各自的 § 可追溯性表；本文件不保留索引副本（索引会与 owner
漂移，且 FR-024 这类跨模式条目本就分属多份契约）。**与 Phase 0 预期的漂移**：原计划 CM 契约只写「等价性」
三条，落盘后发现还需要固定「迁移可发现性」与「检测器诚实」两条，CM 由 3 条增至 10 条；总条款数因此高
于初估。

**FR-014 的 doc-only 声明**（analyze M-04）：上下文装配**不新增契约条款**，显式判定为 doc-only。理由：
装配是提示词步骤，本身没有独立的机器可判面；它的两个可判定面已各有 owner——来源三态由 `data-model.md`
§ E6 拥有并在 V-16 固定，来源清单与缺失声明由 RP-10（FR-015）的 `test_rp10_sources_read_list` 断言。再补
一条装配条款只会让同一事实出现第二个定义点（违反 One Source Of Truth），并不增加任何新断言。

## Handoff

- **下一阶段**：`/speckit.tasks` 按五份契约的 clause→test 映射生成任务；A11 的发现命令由该阶段在基线提交上执行，命中按 § Wiring Surface — A11 Closed Set 的规则重算并分类（派生量，不写白名单）。
- **需独立上下文复核的点**：本文件的宪法自评与质量自查为同作者（§ Constitution Check 的说明），
  `/speckit.analyze` 应以独立上下文复核 18 行判据与三处 Decision Tensions 的可采纳性。
