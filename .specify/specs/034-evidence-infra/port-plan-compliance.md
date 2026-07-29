# 方案符合性检查:实现 vs draft/2026-07-29-better-harness-evidence-port-plan.md

> 日期:2026-07-29 | 检查范围:spec 034 全部落地物 + P7-a/P7-b 平台批次(commit f86b8c23 止)
> 结论:**方案骨架(两层分离、五泳道、证据合同、四纪律、D1/D2/D3)全部按设计落地;差异共 12 处**——3 处实质偏离(均有据可依)、5 处实现期修正(方案写错或未预见的事实)、4 处超出方案的增强。无违反方案红线的偏离。

## A. 实质偏离(设计意图层面)

| # | 方案条款 | 实现 | 性质与理由 |
|---|---------|------|-----------|
| A1 | §3.3 扩展顺序 "opencode → Qwen → iFlow → Hermes → Copilot",Claude 仅"资产 provider 自研补齐" | 实际顺序 **claude 核实补齐 → opencode**;qwen/iflow/hermes/copilot 未做 | 遵循方案自己的定序原则("以 doctor 探测现状定序"):本机 claude 有真实落盘、opencode 无;且 clarify Q3 已把新适配器定为后续迭代,本批仅按 P7 调研落地前两步 |
| A2 | §3.3 每平台 = 会话适配器 + 资产 provider("新资产 provider 注册进 providers/index.mjs 分发表") | opencode **只做了会话适配器,无资产 provider**(asset-baseline 对 opencode 报 Unsupported,assets 泳道该平台不可用) | 采纳 P7 调研 §4.4 的显式决策:opencode 配置资产面薄,资产泳道按合同显式降级;方案的"每平台双件套"被调研结论修订 |
| A3 | §1.3/§4.2 evidence-bundle 替代方案:"泳道编排改由 evidence-utils.py 承担——**分别调用各能力的 cli.mjs**" | 实际调用面:session 走**根级 `session-analysis.mjs`**(非目录内 cli.mjs);project 走 core-change-watch **各自可执行脚本**(该目录根本没有 cli.mjs);仅 agent-customize/dependency-governance 真有 cli.mjs | 方案对上游 CLI 结构的假设与源码不符(plan 阶段勘察已发现并入 plan.md);编排职责归属(Python 侧)与方案一致,仅入口路径不同 |

## B. 实现期修正(方案事实性假设 vs 源码实际)

| # | 方案条款 | 实现修正 |
|---|---------|---------|
| B1 | §3.1 复制子集清单(session-analysis / core-change-watch / agent-customize / coding-agent-practices 三文件 / dependency-governance) | 额外纳入 **`agent-lint/`(4 文件)与 `coding-agent-practices/asset-eval/`** ——均为 Node 实际 import 解析暴露的传递依赖,方案清单漏列;已记 UPSTREAM.md 清单(不属边界侵蚀:两者皆事实层) |
| B2 | §3.1 "零 npm 依赖……不在子集内" | 属实,但需**一处代码切除**:agent-lint 顶层 import 了排除项 `findings-recommend.mjs`(裁决层目录),改为恒等透传;方案未预见子集内文件会反向引用排除面 |
| B3 | §3.3 "Claude Code……资产 provider 为首个自研补齐项"(上游"无统一 provider") | 上游源码 **providers/claude.mjs(531 行)已存在并注册**;"自研补齐"改为"核实补齐"——本批实际补的是 **slug 规则缺陷**(上游变体缺"全部非字母数字→-"规则,导致真实落盘 0 发现;修正后 28 episodes)。requirements 阶段 subagent 核实已预告此偏差 |
| B4 | §7 风险表未提 Node 版本约束 | 上游 engines `>=22.20 <25`,本机 Node 25:doctor 如实报 `satisfies: false` 但引擎实测可用(187/187);run.sh 因 Node 25 目录参数行为差异改用 glob |
| B5 | §4.2 "48+ 条历史 feedback" 等时点计数 | 全部改为动态探测口径(clarify 阶段定案,collect 实测 57→60 条随时点增长) |

## C. 超出方案的增强(方案未要求,实现新增)

| # | 增强 | 出处 |
|---|------|------|
| C1 | **doctor 三态探测**(detected / detected-empty / not-detected):方案只有"探测不到落盘标 unavailable"的二元语义;P7 调研发现目录存在性判定产生 opencode 误报后升级,合同测试同步钉死 | P7-a1 |
| C2 | **compare 写回 verdict**:方案 §6.4 只说"干预标 Outcome-supported";实现明确 compare 为唯一写回方、幂等,且增加 targetFinding 不存在的错误路径 | US6 |
| C3 | **runId 同秒碰撞避让后缀**:方案 runId 格式无碰撞语义 | US6 测试暴露 |
| C4 | **`${SKILL_HOME}` 路径变量解析**(agent-lint):消除 4 条 assets 泳道误报;方案未涉及引擎对 spec-kit 资产约定的适配 | dogfood 闭环发现 |

## D. 方案红线逐条核验(全部符合)

- 四纪律:evidenceState 七态全量移植未裁剪 ✓;Unobserved 红线入 evidence-step + 三技能 ✓;计数只路由 ✓;脱敏双闸(引擎漏斗 + Python 白名单)✓
- 两层分离:findings 合同零裁决字段(递归黑名单测试)✓;collect-evidence 技能中立(结构测试)✓
- §8 不移植清单:harness-analysis / better-harness-cli / evidence-bundle / findings-recommend / checkup / packaging / hooks / 渲染链 / WASM 依赖——grep 与目录核验零混入 ✓
- D1 治理:UPSTREAM.md(6 行修改台账)+ LICENSE + 手动 diff 回移策略 ✓;全量镜像(开放问题 1 → clarify 定案 A)✓
- D3:runs/feedback 一等泳道、无 Node 保底、improve-team 原始工件解析下沉 ✓
- §9 开放问题处置:①镜像→全量(clarify);②7 天阈值→默认采纳;③走完整 SDD→已走;④P7 定序→doctor 探测驱动(即 A1)

## 平台支持现状(本批止)

| 平台 | 会话适配器 | 资产 provider | 本批动作 |
|------|-----------|--------------|---------|
| qoder | ✓(上游) | ✓ | — |
| **codex** | ✓(上游,双侧在库) | ✓ | 验证在库、测试覆盖确认;本机无落盘按纪律 not-detected/Unobserved |
| **claude** | ✓(核实补齐:slug 规则修正,真实落盘 1 session/28 episodes 打通) | ✓(上游已有) | P7-a2 |
| **opencode** | ✓(**spec-kit 自研**,provider-runner 模式,5 fixture 测试) | ✗(显式降级,A2) | P7-b |
| cursor | ✓(上游,不在支持矩阵) | ✓ | — |
| qwen / iflow / hermes / copilot | ✗ | ✗ | 待后续迭代(P7-c/P7-d) |
