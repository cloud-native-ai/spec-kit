# Quickstart: 「驱动子代理」机制的技能化分解与公用化

**Feature**: 060 | **验证基准日**: 2026-10-16（基线=实现前实跑留痕）
**执行验证纪律**: 本文件每条命令示例都按 `/speckit.plan` Post-Generation Quality Gate 的 execution-verify 规则处置——已实跑的粘贴真实输出；未实现的示例**逐条**声明免责与前提清单，免责不覆盖未点名的示例。

## S1 — 内容判据机械面（已实跑）

判据（FR-003）：模板分发层由内容决定——不含用户/环境/项目专用信息字面量才可进框架分发角色集。机械面 = 对模板全文检索四类专用信息字面量。

```bash
grep -inE "([0-9]{1,3}\.){3}[0-9]{1,3}|/Users/|/home/[a-z]|192\.168|10\.[0-9]+\." agents/*.agent.md | grep -v "^Binary"
```

实跑输出（2026-10-16，对现有 2 个角色文件——skill-verifier、structure-adjuster）：

```text
（空输出，退出码 1）
```

解读：现有角色文件零命中——判据模式在此文件形态上可行（无误中样本）。**前提**：模式针对 IPv4/常见家目录/内网段字面量；sdd-executor 模板落盘后须以同模式复跑并预期空输出（该复跑属实现期义务，本场景对 sdd-executor 本身不构成已验证断言）。

## S2 — 副本归零检索判据（基线已测，实现后复测）

三组判据的**实现前基线**（2026-10-16 实跑，SC-003 的对比基线；实现后同命令复测并按"恰 1 处权威落点"判定）：

```bash
grep -rln "ConnectTimeout" skills/external/ | sort
grep -rln "nohup su -" skills/ shared/ | sort    # scope=框架源侧，排除 .specify/ 镜像（analyze M-06）
grep -rn "不得引用本技能\|禁止引用 sdd-loop-driver" skills/ | cut -d: -f1 | sort | uniq -c
```

实跑输出（2026-10-16）：

```text
skills/external/git-utils/scripts/git_fleet.py        ← 误中样本：git_fleet 的 ssh 超时参数，非前置检查表
skills/external/git-utils/scripts/provision-git-server.sh  ← 同上
skills/external/sdd-loop-driver/references/dispatch-recipes.md
skills/external/sdd-project-setup/references/setup-recipes.md

skills/external/sdd-loop-driver/references/dispatch-recipes.md

   1 skills/external/sdd-loop-driver/references/dispatch-recipes.md
   1 skills/external/sdd-loop-driver/references/stage-prompts.md
```

解读与判据修正：
- `ConnectTimeout` 单独 grep 有 2 个**误中样本**（git-utils 脚本的无关 ssh 参数）——实现期判定 MUST 使用"成组共现"模式（与 `id <run-user>`、`source.json` 同文件共现），单独 `ConnectTimeout` 不作判定；基线记录在此防误判。
- `nohup su -`：基线恰 1 文件（loop-driver Recipe 3）——实现后预期权威落点迁至 `shared/`（配方真源）或维持该文档引用形态，判定标准为"义务正文恰 1 处"。
- 反嵌套字面：基线 2 文件（Recipe 1 红线 + 骨架红线）——实现后预期义务落点 1 处（run-agent）+ 引用行若干（引用行以"见 run-agent"措辞形态区分，grep 判据为义务正文排除引用行）。

## S3 — 确定性引擎基线（已实跑）

```bash
python3 scripts/python/validate-requirements.py .specify/specs/060-decompose-subagent-dispatch/requirements.md
python3 scripts/python/probe-utils.py --action compile-embeds --check
```

实跑输出（2026-10-16）：

```text
status: ok
  [id-contiguous] pass (0) / [doc-order] pass (0) / [ref-resolvable] pass (0)
  [marker-count] pass (0) / [dup-id] pass (0)
scanned: 204 lines, 22 definition rows, 6 shared strings
0 error(s), 0 warning(s)

compile-embeds --check: 73 units, zero drift
```

**前提**：`sync-mirrors.py --check` 同日实测存在**一条既有漂移**（`.specify/templates/instructions-template.md` DIFF，与本特性无关——本特性不触碰 instructions 模板镜像对）；实现期 Verify 判据用相对形式："本特性触碰的镜像对零 NEW drift"，绝对全绿判据不可写（既有漂移未清）。

## S4 — 模板 → 双实例 → 本地派发端到端（未实现——逐条免责）

> **免责（仅覆盖本场景两条示例）**：`agents/sdd-executor.agent.md` 与 create-agent 的多职责实例化/退役能力尚未实现，以下命令当前不可执行。
> **前提清单**（实现期须先复核再执行）：a) sdd-executor 模板 frontmatter 沿用既有词表字段名（`capability-tools`/`model-tier`/`run-turn-budget`——勘探确认的渲染映射面）；b) 实例 slug 形态 `<duty>-executor`；c) run-agent 拓扑输入旗标尚未设计（tasks 期定名后回填本场景）；d) 本地派发依赖目标项目已有 `.specify/`（前置检查⑤ ok）。

```bash
# 创建模板与双实例（create-agent 增强后）
# run-agent 以本地拓扑派发 sdd-requirements-executor 到目标项目
```

预期形态（未验证）：模板落 `agents/` 源并经 `specify render-agents --ai qoder` 渲染至 `.qoder/agents/`；两实例落 `.specify/agents/instances/`；派发结果回传含完成尾标与显式异常行（SC-004 三条件）。**实跑承载：tasks T034（SC-001 引用审计）/ T035（SC-002 双拓扑）/ T036（SC-004 端到端）——实现期由其实跑输出替换本段并回填此处。**

## S5 — 退役走查（未实现——逐条免责）

> **免责（仅覆盖本条）**：create-agent 的退役规则（FR-016）尚未实现。
> **前提**：退役实现为 create-agent 生命周期操作；「活引用」判定可枚举（运行中执行/团队席位/capacity-scope 引用三来源）。

预期形态：对被活引用实例发起退役 → 拒绝并列待解引用清单；解引用后退役 → 实例标记 retired、制品保留。**实跑承载：T034–T036 完成后的退役走查（属 FR-016 验收），由其实跑输出替换本段。**
