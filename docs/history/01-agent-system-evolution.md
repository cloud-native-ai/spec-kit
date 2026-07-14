# 01 · Agent 机制与角色体系演进

> 覆盖会话:`46696883`(起点诉求)、`5e7f0ff3`(014 框架重构)、`26d59af9`(015 角色化)、`264ad40c`(code-reviewer 合并)、`5ee06f07`(022 supervisor/EEI 同步 skills)、`12df2298`(系统行为说明)。时间跨度 2026-06-15 → 2026-07-07。

## 演进主线(一句话时间线)

1. **起点诉求**(46696883):现有 agent 机制"不合理",要推倒重建。
2. **014 框架重构**(5e7f0ff3):确立 `.specify/agents/` 为唯一权威源,目录级 symlink 桥接各工具,`specify init` 像 skills 一样预置 bundled agents。
3. **015 角色化**(26d59af9):把 4 个"能力导向"模板换成 6 个"角色导向"模板,配套 create-agent/improve-agent skill。
4. **code-reviewer 合并**(264ad40c):删除独立 code-reviewer agent,code review 降为 module-designer 工作流中的固定动作。
5. **022 supervisor/EEI 同步**(5ee06f07):角色 agent 升级为可派生 EEI 子代理的"角色级 supervisor",并把这套能力同步进 create-agent/improve-agent。

## 用户对 agent 机制的原始设计诉求(46696883)

长期锚点,后续所有 agent 工作都在实现它:

- `/speckit.agents` 执行后,在 `.specify/agents/` 生成一套**通用 agent 结构**,采用一般 AI CLI 工具的标准布局:`AGENTS.md`、`MEMORY.md`、`SOUL.md`、`USER.md`。
- 按**当前使用的工具**通过 **symlink** 适配,而非各工具各存一份。理由:Claude Code 的 subagent 格式兼容 VS Code Copilot custom agent 规范,故可桥接 `.github/agents/<name>.agent.md → .specify/agents/<name>.agent.md`;Qoder 也纳入范围。
- 隐含原则:`.specify/agents/` 单一权威源,各工具目录 symlink 桥接,避免重复维护(与 instructions/skills 的 symlink 模型一致)。

## 关键决策与理由

- **`.specify/agents/` 为唯一权威 + 目录级 symlink**(014):`.github/agents/ → .specify/agents/` 整目录 symlink,与 skills 模式一致、实现简单,自动同时暴露 `.agent.md` 与 workspace 文件。放弃:①只软链单个 `.agent.md`(workspace 文件不暴露);②逐个软链 workspace 文件(要管大量单文件链接)。
- **泛化 symlink 助手**(014):把 `ensure_agent_skills_symlink` 抽成模块级 `ensure_specify_symlink(root, tool_dir, subdir)`,同时服务 skills 和 agents;复用 skills 安装路径(`copy_local_templates()` 加 agents 拷贝块,`.specify/agents` 加入 `_CORE_SPECIFY_ASSETS` 防清理)。
- **agent 以"角色"而非"能力"定义**(015):删除旧 4 个能力模板(`agent-common/knowledge/plan/research-template.md`),改为 6 个 `agent-role-<slug>-template.md`。角色链:需求分析师→系统设计师→模块设计师→测试工程师→质量保障师,知识管理师为横切角色(handoff 链)。
- **命令行为二分 Mode A/B**(015):`/speckit.agents` 无参数→生成全部 6 个角色 agent;有参数→自定义创建(向后兼容)。放弃"始终重新生成"。
- **职责分离**:`/speckit.agents` 只负责按预置模板+项目上下文生成符合工具/目录结构的 agent 配置;**修改模板/逻辑本身**交给 create-agent/improve-agent skill。
- **定制 agent 重生成选 warn+backup**(015):检测内容 hash 变更→先 `.bak` 备份再覆盖。放弃"总是覆盖"(丢用户改动)和"warn+skip"(agent 陈旧)。
- **code review 内嵌角色而非独立 agent**(264ad40c):code review 只是模块实现过程中的固定动作,作为 module-designer 模板 workflow 的 step 5(自审:正确性>可维护性>命名>一致性,correctness bug 优先于 style),输出段加 Code Review 章节(按严重度排序 + file:line)。
- **supervisor 只是 prompt 指令,不是运行时调度器**(022,5ee06f07):显式遵守 "no DFX over-design" 约束(见 [[feedback_no-dfx-overdesign]])。
- **supervisor default-on**(022 OQ-1):生成的角色 agent 默认跑 EEI 循环(`supervisor: true` 默认,`false` 为 opt-out)。
- **supervision snippet 单一 canonical 来源**(022 OQ-2):新建 `templates/agent-supervision-delegation.md`,生成时内联,**不物理编辑 6 个角色模板**——模板系统无 transclusion,copy-per-role 会漂移。

## 用户 ↔ 模型的冲突/分歧点

| 会话 | 用户主张 | 模型原本 | 最终 |
|------|----------|----------|------|
| 015 (Q3 工具权限) | 所有角色都给全读写,行为靠 instructions 引导 | 只读角色(需求/系统设计/QA/知识)vs 读写角色(模块/测试),强制职责分离 | 采纳用户:全读写,后续体现为**省略 `tools` 字段** |
| 014 (symlink 粒度) | per-file 软链 | clarify 提三选项并推荐目录级(C) | 目录级 symlink(per-file 路径在目录 symlink 下仍可解析,兼容原意) |
| 022 (OQ-1) | default-on(全 6 角色默认开 EEI) | opt-in + dormant section(更安全便宜) | default-on(`supervisor:false` 为 opt-out) |
| 022 amend scope | 重构指"角色→supervisor"更深改造,scope=amend 022 | 一度认为前提已满足并暂停,且指出 `create-new-plan.sh` 会覆盖已完成的 plan | 就地修订(不跑破坏性脚本),追加任务保留历史 |

## 可复用经验 / 踩坑

- **就地 amend 时,不要跑无条件覆盖的脚手架脚本**:`create-new-plan.sh` 会无条件 `cp plan-template.md → plan.md`,覆盖已完成的 plan;tasks 同理应**追加**(如 T032–T057)而非重生成,保留历史。
- **`/speckit.agents` 当前把 agent 渲染内联在命令模板里,从不调用技能**——这是 command/skill 逻辑漂移的根源(022 的 review 结论);方向是收敛到调用技能。
- runtime mirror 手动易漏(见 [[00-cross-cutting-lessons]] 第一节)。
- 新技能应端到端 smoke test(如 `git-submodule-edit` 在临时 parent+submodule 真实跑通建分支→提交→bump→记账才算验证)。

## 未完成 / 待办

- **022 上游 artifact 未同步**:`contracts/agent-authoring-contract.md` 的 R2 仍写被 clarify 推翻的 "dormant even when supervisor:false";`plan.md` Open Questions 仍描述被推翻的 dormant-by-default 假设。已在 verification.md + T032 记录,但 implement 不 regen contracts,需下次 `/speckit.plan` regen。
- 014 遗留 4 个 pre-existing 测试失败(plan 模板缺 "Claude Code"/"Qoder" 文本),判为超范围。
- 022 的 `git-submodule-edit` 若要进发行 wheel,需从 `.specify/skills/` 再 mirror 回源 `skills/`。
- 015 T036(quickstart 实景验证)、T038(AGENTS.md 运行时索引)deferred。

## 最终产出 / 现状

- **014**(commit `c1fbe21`,fast-forward 合入 master):`.specify/agents/` 权威 + 目录级 symlink;`ensure_specify_symlink()`;`specify init` 预置 bundled agents;spec `.specify/specs/014-agent-framework-refactor/`。
- **015**(commit `f95f425` 等):6 个 `agent-role-*` 模板 + create-agent/improve-agent skill;删 4 个 legacy 模板;`templates/commands/agents.md` Mode A/B;78 测试通过;spec `015-role-based-agents/`。
- **264ad40c**:删 `agents/code-reviewer.agent.md` + 运行时副本;module-designer 模板加 Review step 5 与 Code Review 输出段;测试 fixture 改用泛化名。
- **022**(commit `f261cea`/后续):6 个角色模板加 `supervisor: true` + `role-scope:`;`templates/agent-supervision-delegation.md`;`templates/agent-subrole-{executor,evaluator,improver}-template.md` + `agent-triad-orchestration-template.md`;`docs/eei-triad-pattern.md`;create-agent 加 Capability Matrix(role·supervisor·triad·custom);spec `022-eei-agent-triad/`。EEI 三元组的抽象来自 draw-plantuml 优化的三角色循环,详见 [[04-draw-plantuml-optimization]]。

## `/speckit.agents` 系统行为(12df2298 的说明快照)

执行时加载 `.claude/commands/speckit.agents.md` 作为 prompt 注入。**注意源模板与 Claude 安装版曾不一致**:源模板双模式(无参→批量 6 角色 / 有参→自定义),而 Claude 安装版当时只保留单模式(自定义创建)。核心流程:解析 `$ARGUMENTS` → 工作区脚手架(AGENTS/MEMORY/SOUL/USER.md)→ 从对话提取上下文 → 分类 → 向用户确认 → 选模板 → 迭代生成 → 写 `.specify/agents/<name>.agent.md` → 注册 Registry → 验证 symlink → 报告。约束:只写 `.specify/agents/`,最小权限工具集,YAML 校验不过则阻止保存。

---

**相关**:[[00-cross-cutting-lessons]] · [[04-draw-plantuml-optimization]](EEI 三元组来源) · [[02-commands-and-cli-tools]]
