# Implementation Plan: Agent+LLM 执行量化记录(Execution Quant Recording)

**Branch**: `059-exec-quant-recording` | **Date**: 2026-10-16 | **Spec**: `.specify/specs/059-exec-quant-recording/requirements.md`
**Requirement → Feature**: `059-exec-quant-recording` → Feature 059 Agent+LLM 执行量化记录(Execution Quant Recording)
**Input**: Specification from `.specify/specs/059-exec-quant-recording/requirements.md`(无未决 `[NEEDS CLARIFICATION]`;简报 `/tmp/llm-quant-sdd-brief.md` §3 可行性实测为设计输入)

## Summary

为 Feature 059 新增 scripts 层确定性采集引擎 `exec-quant.py`(actions:`collect` / `list-records` / `score`),经伞形 probe 注册表以 engine handler(`h-exec-quant`,non-blocking,order 15 —— 在 `h-run-determination` 的 10 之后、`h-feedback-record` 的 20 之前)挂既有 wrap-up 点,scope=all,不新增每命令模板面、不新增确认门。每次受测单元执行(与运行判定同单元语义)落一条量化记录到**新设专属 durable 存储** `.specify/memory/exec-quant/`(`records.jsonl` + `scores.jsonl`,append-only、机器可读、引擎自有):agent 程序字段(宿主 CLI 身份/版本/启动参数/cwd)、LLM 详细字段(模型名/context window/effort 自宿主配置面,端点只录白名单候选与可判定连接证据)、质量字段(时长与 token 自同 run 运行判定记录**携带**不重测、错误次数自己枚举声明来源、打分双通道按来源标注)。每个字段或为带 provenance 的值、或为显式 `not_evaluated`([[STR-002]]),零空缺、零臆造;记录体封顶截断;凭据零入库;结构性排除于反馈打包与一切上送(feedback `package` 只读 feedback store,已实测)。本期 Recording Only——分析/报表/聚合口径/打分模型/保留策略全部 Out of Scope。

## Technical Context

**Language/Version**: Python ≥ 3.8(仓库基线;引擎仅用标准库,与相邻引擎 `run-determination.py` / `feedback-utils.py` 同形态)
**Primary Dependencies**: 无新增。采集依赖宿主工具 `ps` / `/proc` / `ss`(Linux 实测可用)与子进程版本探测;全部缺省降级为显式 `not_evaluated`。
**Storage**: 新设 `.specify/memory/exec-quant/`(项目 memory 层):`records.jsonl`(append-only,一行一记录)+ `scores.jsonl`(append-only 用户打分,list 时 join)。不入 feedback store、不入 session/knowledge、无上送路径。
**Testing**: pytest,markers `contract` / `integration`;新契约测试 `tests/contract/test_exec_quant_engine.py` + 既有 `test_probe_engine_action_sets.py` 有意扩展(exec-quant 分区)。
**Target Platform**: Linux 同机实测面(ps -ef、/proc、ss 全可用);非 Linux 宿主按字段降级 not_evaluated(适配缺口不阻塞落库,requirements Edge Cases)。
**Project Type**: 框架 scripts 层扩展(引擎脚本 + 注册表行 + 编译面再生),非运行时平台。
**Performance Goals**: 采集单次耗时秒级(子进程超时上界 10s/调用);单记录 64 KiB 封顶。
**Constraints**: 非阻塞(FR-012);确认门控预算零消耗(FR-003);wrap-up 行预算 853(实测 2026-10-16:72 面 / 431 行非空,余量 422,本特性每面 +1 行 → 约 503);凭据型值零出现(FR-010);上送路径零(FR-011)。
**Scale/Scope**: 15 FR / 4 SC / 3 user stories;触及面 = 1 新引擎 + 1 引擎注册行扩展 + 注册表 1 Class/4 Objects/1 Handler/1 Binding + 编译面再生(72 wrap-up 面)+ 契约测试 1 新 1 扩。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**(rendered from `.specify/memory/constitution.md` v1.13.0,16 principles):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | plan D1–D11 逐条映射 FR-001–FR-015;Phase 1 产物由 requirements 实体/FR 派生(feature-ref.md 记录映射) |
| II | Feature-Centric Development | ✅ Pass | Feature 059 已注册(features.md 行 67,Draft;binding 经 clarify Q1 同胞启发式核验);本 run 仅推进 Draft → Planned |
| III | Intent-Driven Development | ✅ Pass | Recording Only 边界与 A1–A6 裁决全部自 requirements 承接;设计不再扩大意图(Out of Scope 七条原样保留) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 引擎为可执行代码 → 测试先行全适用:新契约测试 + action-sets 精确钉扩展入 plan;tasks 期 red-first 取证 |
| V | AI Agent Integration Standards | ✅ Pass | 不改 `AGENT_CONFIG` / `_ASSISTANT_TIERS`;宿主适配为只读采集,不构成新 agent 支持面 |
| VI | Continuous Quality & Observability | ✅ Pass | `schema_version` 字段版本化;采集失败可见(FR-012);Recording Only 本身即 YAGNI 约束(分析面全 Out of Scope) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 全流程依序执行(requirements → clarify → plan);Pre-Status-Flip 门在 implement 期适用;本阶段仅 Draft → Planned |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 全部事实实测自代码(file:line 见 Phase 0 节);三处基线数字为实跑输出(431/853、两 --check exit 0),非预写 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 一只脚本 + 注册表行,复用既有 probe/handler/mirror 先例;零新模板面、零新门;本期明确不做分析/报表/聚合 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 无新保留名;产物落既有 spec 目录布局(contracts/、data-model.md 等);存储目录 `exec-quant` 小写语义路径 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已名:引擎落框架源 `scripts/python/` 经 sync-mirrors 投影;`.specify/` 副本为机器再生副本;本特性自身即为框架吃自狗粮的观测面 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用门已执行:`.specify/memory/tools/` 10 条记录逐一核对(2026-10-16),无一条覆盖「进程/环境遥测采集」能力 → 按 XII 写代码是预期结果;引擎稳定后可评估晋升 Tool(记录于 feature-ref.md) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 服务 Learning Capture 维度;不产判分模型(D5/D9;打分模型 Out of Scope);不援引本原则论证机制存在 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 行为真源在引擎代码,注册表只载接线(probe-definitions L178 约束);STR-001/STR-002 单锚点引用;携带值标注 dated artifact 不作现行事实(A6) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | wrap-up 步骤行标签经机械派生(`h-exec-quant` → "Exec Quant",同 "Run Determination" 规则);词形门 `test_wrap_up_wording_gate_safe` 基线绿 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 采不到 → 显式 `not_evaluated`,归属含糊 → 标注 not guess(D6/D8);基线绿均为实跑而非推定;实现期冲突按快速失败上抛(A5) |

**Gates Status**: ✅ All gates pass(16/16 Pass;无 Partial/Fail,Complexity Tracking 为 N/A)

**Re-check after Phase 1**: 2026-10-16 复核于 Phase 1 产物落盘后,并经**同作者委托复评**(fresh-context 只读子代理,依 objective-analysis-gate)——16 行判定维持 Pass;复评发现 3 处缺陷,**全部属 correction 已就地修复**:① 初稿动作名误留 `list`(与 feedback-utils 既有 `list` 同名,违背 D1 已录的避同名意图)并误写 feedback「14 项」(实为 11,056 迁移后计数)→ 动作名定 `list-records`,计数陈述改为引用真源;② union 读取机制误述(ACTIONS 元组分支仅 name-gated 于 run-determination/trigger-utils,新引擎实走 argparse choices 路径)→ plan Phase 0 #2 / D11 / 两契约按实测校准;③ `RECENT_WINDOW_MINUTES = 90` 在 data-model 构成非合法重复 → 改引用 plan D2 唯一裁决点。逐条确认:D4 的 FR-008 第四元「未采」以字段值字面量 `not_evaluated` 实现(三形 provenance 词域 + 标记值构成四元,FR-008 语义完整);probe 注册 4 Objects 命名在 data-model §1.6 与 contracts/probe-registration.md §1 逐字一致;quickstart 每条引擎示例均附 per-example 免责 + 前提清单(①–⑬)+ 指名钉定测试。无未修复违规。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/059-exec-quant-recording/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # No standalone research.md — Phase 0 findings inlined below (brief, all repo-internal)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
scripts/python/exec-quant.py            # 新引擎(framework source):collect/list/score;ACTIONS 元组供 union 对账
scripts/python/probe-utils.py           # _ENGINE_SIBLINGS 元组追加 "exec-quant.py"(union 对账唯一代码侧改动)
shared/definitions/probe-definitions.md # 注册表:## Classes +1 行、## Objects +4 行、## Handler +1 行、## HandlerBinding +1 行
tests/contract/test_exec_quant_engine.py           # 新契约测试(schema/标记/凭据扫描/append-only/list/score/退出码)
tests/contract/test_probe_engine_action_sets.py    # 有意扩展:_execquant_actions() 进 union 构造 + exact-pin
.specify/specs/056-probe-handler-system/contracts/engine-action-sets.md  # 对账面:新增 exec-quant.py 分区节
templates/commands/*.md                 # compile-embeds 再生(23 面,每面 wrap-up +1 行)
skills/{external,internal}/*/SKILL.md   # compile-embeds 再生(49 面,同上)
docs/reference/skills/probe.md          # 文档核对义务:登记类目变更是否需指针更新(实现期 docs-step 裁定,不盲改)
```

**Structure Decision**: 扩展既有 container-image-factory 式框架布局中的 **scripts 切片**:引擎与四个相邻引擎同层(`scripts/python/`),经 scripts 镜像对自动投影;注册行入伞形 probe 注册表(scripts 切片 Class,unit=引擎脚本路径,行为真源在代码);编译面再生全部经既有 compile → regen → sync 固定顺序(test_compile_propagation_order.py 钉住),无新顶层目录(存储目录 `.specify/memory/exec-quant/` 为数据目录而非代码目录)。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

Baseline drift(2026-10-16 实测):`sync-mirrors.py --check` 全树 **exit 0**(scripts 107 files / shared 48 files 均 ok);`regen-command-copies.py --check` **exit 0**。既有零漂移 → 本表 Verify 列可用**绝对判据**。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/exec-quant.py`(新) | `.specify/scripts/python/exec-quant.py`(scripts 对 rglob 自动吸收;副本缺失 = ORPHAN error) | `sync-mirrors.py --check` exit 0(绝对判据,基线已测) |
| `scripts/python/probe-utils.py`(`_ENGINE_SIBLINGS` +1) | `.specify/scripts/python/probe-utils.py` | 同上 |
| `shared/definitions/probe-definitions.md`(+7 行) | `.specify/shared/definitions/probe-definitions.md` | 同上 |
| `templates/commands/*.md`(23 面 compile 再生) | per-tool copies(`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/` 等,经 regen-command-copies.py;NO `.specify/templates/commands/` 镜像——已退役) | `regen-command-copies.py --check` exit 0(绝对判据,基线已测);再生副本含新 wrap-up 行 |
| `skills/{external,internal}/*/SKILL.md`(49 面 compile 就地再生) | `.specify/skills/` 镜像(sync 对自动吸收) | `sync-mirrors.py --check` exit 0 |

**传播顺序固定**:compile-embeds → regen-command-copies → sync-mirrors(`test_compile_propagation_order.py` 钉住;顺序不可颠倒)。

## Complexity Tracking

N/A(Constitution Check 16/16 Pass,无需 justification 的违规项)

## Phase 0: Research Review

No standalone research.md — findings inlined below(全部仓库内部实测,无外部源;检索执行日 2026-10-16,file:line 为当日实测值)。

**引擎现实核验(与 spec A1–A6 假设逐条对账)**:

1. **run-determination.py**(A1/A6 依赖):actions = `determine/settle/history`(ACTIONS L92);记录 kind 字面量 `speckit.run-determination`、schema_version=1(L88–89);四轴 keys `token_consumption/elapsed/artifact_correctness/satisfaction`(L96);`not_evaluated` 字面确认(L98–100,verdict 封闭集)——STR-002 词形复用成立。`--run-id` **必填**(L1390 InputError),键 = `(unit_id, run_id)`,去重同键 no-op(L1411);unit-id 封闭形 `/speckit.<cmd>` | `skill:<name>` | `custom:<owner>/<name>`(L156–160),unit_type ∈ `command|skill|custom-unit`——A1 单元语义确认。落库经 memory-utils session 适配器 → `.specify/memory/session/`(L150–151, tag=`run-determination`)。
2. **probe-utils.py**(A3 依赖):actions = `probes/map/probe-inject/handlers/compile-embeds`(L1237);注册表路径 `.specify/shared/definitions/probe-definitions.md`(L130);`compile-embeds` 渲染 AUTO-GENERATED `## Wrap-up` 于 `templates/commands/*.md` + `skills/{external,internal}/*/SKILL.md`(L337–355),`scripts/`/`shared/` owner 重写为 `.specify/` 运行时面(L852–859);调用行由 `_render_call_line` 渲染(L874–886):engine kind → `python3 {owner} --action {action} --unit-id "{unit_id}" --unit-type {unit_type}`,标签机械派生 `h-<id>` → Title Case(L860–864)→ `h-exec-quant` 得 "Exec Quant",**渲染器零改动**;fingerprint = handler+binding 的 sha256 前 12 hex(L868–871)。**`_ENGINE_SIBLINGS` 为显式元组**(L620–621:feedback/run-determination/probe/trigger 四引擎)→ 新引擎 union 对账需把它追加进元组(设计 D-12,唯一 probe-utils 代码改动);action 闭包自引擎源码实读(code-first,L632–633):`ACTIONS = (...)` 元组分支仅 name-gated 于 run-determination/trigger-utils 两引擎,其余 sibling 经 argparse `choices=[...]` 正则——新引擎 exec-quant.py 走 choices 路径(D11/契约按此校准)。
3. **probe-definitions.md**(FR-004 契约):Class 7 列、Object 4 列(unit=引擎脚本路径,L24/L56–59)、Handler 6 列封闭集、HandlerBinding `(handler_id, selector, scope)` 身份三元组,selector 封闭集 `@point:wrap-up` 等,scope 含 `all`;先例行 `h-run-determination | engine | determine | non-blocking | 10 | scripts/python/run-determination.py`(L184)+ `@point:wrap-up | all`(L226)。order 冲突规则:同 lifecycle point 内不得同序(L179–180)→ order 15 可用(10 与 20 之间)。派生视图重建不手抄(L13–14);`--action probes --validate` 校验。
4. **feedback-utils.py**(A2/FR-011 结构性排除):`package` 动作(L1151–1262)只读 feedback store 状态 → 独立存储对打包**结构性不可见**,零代码即达成 FR-011;红线在 `shared/workflow/feedback-step.md` § Positioning & Red Lines。
5. **sync-mirrors.py**(镜像义务):scripts 对 `("scripts", ".specify/scripts", True, set())`(L87)rglob 全树走查 → 新文件自动吸收;副本缺失 = ORPHAN error(L205–212)。probe/run-determination/feedback 引擎均在对内。
6. **调用模型确认**:engine handler 编译为**字面命令行**(prompt 执行,非回调);72 面携带 AUTO-GENERATED banner(23 命令 + 49 技能)。
7. **非回归面**(SC-003):tests/contract 下 probe/handler/feedback/run-determination 族 20 个测试文件 + tests/integration 下 feedback 族 5 个(逐名列于 data-model.md § 非回归基面);基线冻结义务由 tasks 期 T1 承担(049/050/051 先例)。
8. **实测基线(2026-10-16,本 run 实跑输出)**:wrap-up 面 72 个 / 非空行 431 / 预算 853(余量 422;每面 +1 行 → 约 503,预算内,无需 re-adjudicate);`sync-mirrors --check` exit 0;`regen-command-copies --check` exit 0;`pytest test_wrap_up_line_budget.py test_probe_engine_action_sets.py` 5 passed。
9. **工具复用门**(Constitution XII):`.specify/memory/tools/` 10 条记录(build-summary-input/derive-utils/evidence-utils/feedback-utils/goal-utils/interview-utils/refresh-tools.sh/sanitize-utils/sync-mirrors/trigger-utils)——无一条覆盖「宿主进程/环境/配置遥测采集」;evidence-utils.py 是证据 lane 归一化引擎,能力不同。**结论:无 Tool 可复用,写代码是预期结果。**
10. **命名冲突**(A5 复核):全仓无 `exec-quant.py` 文件;`speckit.exec-quant` 字面量仅现于本特性 requirements.md——零冲突,定名锁定维持。

**简报 §3 可行性锚点**(dated record,2026-10-16 同机实测,仅作设计输入非运行时保证):agent 程序信息可全采(ps -ef/版本/启动参数/cwd);LLM 分级可采——env 端点变量均为候选非生效(活跃连接指向 qoder.sh 系网关)、模型名/contextWindow/effort 自 `~/.qoder/settings.json` 可读、未设 effort 生效值不回显(不可直接测得)。设计响应:D6(端点只录候选 origin + 可判定连接证据,不判「生效」)、D7(qoder 配置面适配器,未设 effort → not_evaluated 不推断 CLI 默认)。

**Plan 期裁决(D1–D12;承接 requirements A1–A6,记录假设于本节)**:

- **D1 引擎动作名 `collect / list-records / score`**(FR-002/FR-013/FR-014 的动作面):三者与既有四引擎动作名**零交集**——feedback-utils 既有 `record` 与 `list`,两者皆避:同名动作即使引擎未注册也会被既有 union 判真,产生 handler 行归属歧义;`collect` 比 `record` 更诚实(采集+落库一步),`list-records` 连字符形与既有 `mark-submitted` 同风格。A5 只锁引擎名,动作名属 plan 裁决权。
- **D2 run_id 解析**:`--run-id` 可选;缺省时按 `(unit_id)` 查找最近一条运行判定记录,采纳其 run_id 并携带(recent 窗口常量 `RECENT_WINDOW_MINUTES = 90`,有界防误绑陈旧记录);无命中则合成时间戳 run_id 且携带字段落 not_evaluated。理由:编译行是最小形态(agent 按需补参,既有约定),自动采纳消除跨步骤 run_id 传递断链面;显式传参时先做精确 `(unit_id, run_id)` 对账。
- **D3 存储形态**:`records.jsonl`(append-only,永不改写)+ `scores.jsonl`(append-only,重打分追加新行,按时间后者胜)——双文件使记录不可变,打分以 join 呈现(FR-013/FR-014),纯追加语义处处成立。
- **D4 provenance 词域**:`measured / carried / user-given / not_evaluated`(FR-008 四元逐字);satisfaction 自判定记录携带 = `carried`。
- **D5 错误次数来源枚举**:判定记录的 `failed_set_diff` 计数 + 红轴计数(逐来源标注);判定记录缺失 → 整组 not_evaluated;不引入 ANOMALY 行解析(那是会话文本,采集程序不读会话——Program-First 边界)。
- **D6 端点采集**:仅白名单端点变量名,值只取 origin(scheme://host,剥 path/query/凭据面);「生效端点」不作判定,只录可判定证据(宿主进程已建立连接的远端 ip:port,`ss -tnp` 解析,无 DNS 依赖,ss 缺席 → not_evaluated)。
- **D7 LLM 配置面适配器**:qoder 适配器读 `~/.qoder/settings.json`(model.name / contextWindow / per-model reasoning.effort);未设置 → not_evaluated,**禁止**推断 CLI 默认(FR-006);其他宿主整组降级 not_evaluated(适配缺口不阻塞)。
- **D8 agent 归属**:自身进程父链上溯 + 已知宿主 CLI 进程名模式匹配;多宿主/不可识别 → `resolution: ambiguous|unresolved`,可确定部分照录,**MUST NOT 猜测唯一进程**(Edge Cases)。
- **D9 封顶与凭据防御**:单记录 64 KiB 封顶,逐字段截断并在 `truncated` 列表标注;写盘前对序列化记录做凭据形值防御扫描(命中即脱敏标注)——白名单采集(D6)+ 出口扫描双保险(FR-010/SC-004)。
- **D10 probe 注册实体**:1 Class `exec-quant`(scripts 切片,internal,insertion_type=wrap-up,code_anchor 指引擎符号)+ 4 Objects(`eq-collect-execution`、`eq-probe-host-process`、`eq-probe-host-config`、`eq-probe-determination-link`)+ Handler `h-exec-quant`(engine/collect/non-blocking/order 15)+ Binding(`@point:wrap-up`, `all`)。
- **D11 有意测试扩展**:`test_probe_engine_action_sets.py` 的 union 构造追加 exec-quant actions(choices 路径,与既有 sibling 同读法)+ 新增 exact-pin 与跨引擎动作名零交集断言;056 契约对账面 `engine-action-sets.md` 增 exec-quant 分区节(该文件即引擎封闭集登记面,"其他引擎"条款预期此类增长)。
- **D12 score 通道约定**:`--score` 接受 1–5 数值(通道约定非打分模型,模型/阈值 Out of Scope);逐条存 `scores.jsonl` 含来源=user-given 与可选 --note。

## Phase 1: Design Artifacts Summary

<!-- ACTION REQUIRED (backfill ONLY — delete this comment when filling): fill after artifacts land. -->

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 6 实体(§1.1–§1.6)/ 8 校验规则 V1–V8 / 2 派生生命周期线 / 非回归基面 20 contract + 5 integration 测试文件 |
| Contracts | [`contracts/`](contracts/) | 2 文件:`exec-quant-cli.md`(3 动作全契约 + 通用参数 + 交叉约束)、`probe-registration.md`(1 Class + 4 Objects + 1 Handler + 1 Binding 逐字目标行 + `_ENGINE_SIBLINGS` 扩展 + 056 对账面分区 + 传播顺序) |
| Quickstart | [`quickstart.md`](quickstart.md) | 5 场景;引擎示例全部逐示例免责 + 前提清单(①–⑬)+ 指名钉定测试(route b);feedback package 为既有引擎命令(行为前提 ⑪ 实现期复核) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | 15 FR → 落点映射 / 4 SC → 验证映射 / Shared Strings 消费 / Tool 晋升评估留待 implement 期 |

实测备注:上表计数取自落盘产物本体(逐节清点),非预写;本 run 无 research.md(Phase 0 内联于 plan.md,见该节首行声明)。
