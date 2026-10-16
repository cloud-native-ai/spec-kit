# Contract: 两技能委派化与义务平价（delegation-parity）

**Feature**: 060 | **FR 覆盖**: FR-010, FR-011, FR-012（委派侧）, FR-013, FR-015
**性质**: 结构契约 + 平价对账底册。D 节条款机械判定；P 节（平价映射）是 tasks 期对账依据与 SC-003 证据载体。

## D 节：sdd-loop-driver 委派化

- **D-1**: `skills/external/sdd-loop-driver/SKILL.md` 的「Driver Topology（驱动拓扑，反嵌套红线）」节 MUST 改写为引用形态：反嵌套义务真源移交 run-agent 派发治理（见 skill-enhancements R-6），本节保留**循环视角自检行**（加载者发现自己是"代为驱动"subagent → 显式异常上报）与引用行；HR-6 同步改写为引用+自检形态。义务本体语义零变更（平价：同等强度）。
- **D-2**: `references/dispatch-recipes.md` 的 Preflight 节（五族自持表+失败处置）MUST 清零为引用（指向 run-agent dispatch-preflight.md）；Recipe 0/1/2/3/5 中与 [[STR-006]] 同型的机制正文（断点探测、提示词落盘、runner 派生、脱离派发+轮询、本地变体）MUST 坍缩为引用，仅保留本技能特有的差异面（心跳文件机制、定间隔分级、多线批查判定、双线并行隔离）并注明差异。
- **D-3**: `references/stage-prompts.md` 的**提示词三段骨架内容**（背景/执行要求/完成尾标——SDD 阶段领域知识）MUST 保留（编排本体的组成部分）；其**机制性红线段**（禁止引用技能/禁止加载技能/禁止循环逻辑）改为引用 run-agent 反嵌套义务（保留一行警示+引用，义务本体单一落点）。
- **D-4**: 保留段清单（编排本体，MUST NOT 外移）：U0–U6 循环定义、状态脊先写后动、哨兵与独立校验、卡死处置与上送四要素、收尾合并纪律、驱动者生命周期（HR-5）。委派化后 SKILL.md MUST 增补「子代理创建与派发委派」说明段：实例创建→create-agent、阶段派发→run-agent（附输入/产出说明，057 命令瘦身先例）。

## D 节：sdd-project-setup 委派化

- **D-5**: `references/setup-recipes.md` 的 S4 五族前置检查表 MUST 清零为引用（同 D-2 落点）；软协同契约节中与 run-agent preflight handoff 互为镜像的段落收敛为单侧引用（指向 run-agent 承接的 ⑤ 处置链），软协同契约的其余语义（非强绑定、建议而非强制、职责切分线）保留。
- **D-6**: 远端命令形态（su 约定、路径参数化约定）与 [[STR-006]] 的同型正文 MUST 坍缩为引用；S1 机制矩阵、S2 INSTALL、S3 RECONCILE、S5 候选清单（调协领域独有内容）保留。
- **D-7**: SKILL.md MUST 增补委派说明段（同 D-4 形态：盘点脚本的执行主体、S2/S3 治理命令的派发经 run-agent 可选形态——独立运行时不强制）。

## P 节：义务平价映射（对账底册）

**冻结时机**: tasks 期前提测量步骤冻结"改造前原文清单"后逐行填完本表；本契约落盘时预登记义务枚举下限（与规格 FR-011 一致，实现时若发现额外义务按同格式追加行）。

| # | 义务 | 原落点 | 新落点 | 强度 | 追溯 |
|---|------|--------|--------|------|------|
| P-01 | 五族前置检查表 | loop-driver dispatch-recipes Preflight；setup-recipes S4 | run-agent references/dispatch-preflight.md | 同等（⑤ handoff 语义随迁） | R-3 |
| P-02 | 前置检查失败处置链（①②③停线/④待补/⑤handoff） | 同上两处 | run-agent dispatch-preflight.md | 同等 | R-3 |
| P-03 | 断点探测三信号 | loop-driver Recipe 0 ≈ STR-006 Recipe 1 | [[STR-006]]（引用） | 同等 | D-2 |
| P-04 | 阶段提示词文件落盘机制 | loop-driver Recipe 1 ≈ STR-006 Recipe 2 | [[STR-006]]（引用） | 同等 | D-2 |
| P-05 | runner 脚本与 sed 派生 | loop-driver Recipe 2 ≈ STR-006 Recipe 3 | [[STR-006]]（引用） | 同等 | D-2 |
| P-06 | 脱离派发+定间隔轮询 | loop-driver Recipe 3（nohup 形态独有+心跳） | [[STR-006]]（引用）+ loop-driver 保留差异注 | 同等（心跳/分级为更严差异，保留） | D-2 |
| P-07 | 提示词三段骨架内容 | loop-driver stage-prompts.md | 保留（编排本体） | 同等 | D-3 |
| P-08 | 反嵌套红线 | loop-driver SKILL.md Driver Topology+HR-6+两处红线 | run-agent 派发治理（上收）+原处引用行 | **更严**（公用面拦截+派发前自检扩展） | R-6, D-1 |
| P-09 | 状态脊先写后动 | loop-driver SKILL.md/stage-prompts | 保留（编排本体） | 同等 | D-4 |
| P-10 | 哨兵与独立校验 | loop-driver SKILL.md | 保留（编排本体） | 同等 | D-4 |
| P-11 | 卡死处置+上送四要素 | loop-driver SKILL.md/stage-prompts | 保留（编排本体） | 同等 | D-4 |
| P-12 | push 门控/脏文件纪律 | 两技能既有纪律行 | 保留（随引用网分布） | 同等 | D-4, D-6 |
| P-13 | 并发隔离+窄读法授权 | loop-driver stage-prompts | 保留（编排本体） | 同等 | D-3 |
| P-14 | 驱动者生命周期（HR-5） | loop-driver SKILL.md | 保留（编排本体） | 同等 | D-4 |
| P-15 | 实例创建语义（原两技能内联的"谁来执行"描述） | 两技能 SKILL.md 散述 | create-agent（sdd-executor 模板+实例化） | **更严**（引用绑定替代散述，复述为零） | A-4 |

**副本归零检索判据**（SC-003 机械面，实现期执行并记录模式误中率）：
- 五族检查表：`grep -rn "ConnectTimeout" skills/ .specify/skills/` 成组出现（与 `id <run-user>`/`--version`/`source.json` 同文件共现）恰 1 处（run-agent dispatch-preflight.md）；
- ssh+su 形态：`nohup su -` 形态恰 1 处权威落点（[[STR-006]]）；
- 提示词骨架机制红线："禁止引用 sdd-loop-driver" 字面恰 1 处义务落点（run-agent），其余为引用行。

## 全局非回归

- **D-8**: 两技能对最终用户的入口话术、frontmatter（name/classification/skill_id）、probe-registry 认领（unit-id、编译 Wrap-up 面）MUST 零变更；`/speckit.team`、create-team、各 `/speckit.*` 命令模板零改动（FR-015）。
- **D-9**: 委派化后两技能 MUST 保持自足可加载：引用真源 + 内联最小操作事实（057 FR-006 先例形态），离开本仓 ambient 指令的宿主仅读技能体即可完成委派调用。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| D-1 | FR-009, FR-011 | test_d1_driver_topology_referenced |
| D-2 | FR-012 | test_d2_preflight_and_recipes_collapsed |
| D-3 | FR-010, FR-013 | test_d3_skeleton_kept_mechanics_referenced |
| D-4 | FR-010, FR-013 | test_d4_orchestration_body_retained |
| D-5 | FR-012 | test_d5_setup_preflight_collapsed |
| D-6 | FR-012 | test_d6_remote_forms_referenced |
| D-7 | FR-010 | test_d7_setup_delegation_section |
| D-8 | FR-015 | test_d8_external_behavior_unchanged |
| D-9 | FR-011 | test_d9_skills_still_self_contained |
| P 表 | FR-011, SC-003 | test_p_parity_map_complete（行数≥15、无空新落点） |
