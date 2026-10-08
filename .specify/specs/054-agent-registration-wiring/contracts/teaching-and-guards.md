# Contract: Teaching Surfaces, Docs & Guards(教学面、文档与守卫)— 054

**Scope**: FR-001、FR-002、FR-003、FR-009、FR-010、FR-011、FR-012(守卫面);FR-007 的裁定记录已在 spec,本文只引用。从句形态:`md-bold-closed`(语法真源 `shared/definitions/contract-clause-definitions.md`)。

## § 教学面改写(FR-001..003)与其缺席守卫(FR-011)

**C-1**: `templates/commands/agents.md` 的「Tool-specific directories are symlinks — never write to them directly」一句([[STR-001]],spec Shared Strings 表)MUST 改为真实模型陈述:宿主 agent 目录是渲染产出的**真实文件**,由 specify CLI 渲染,legacy 符号链接被替换;per-file 符号链接模型的教学 MUST 移除。(FR-001)

**C-2**: `skills/create-agent/SKILL.md` :122 表行(「Per-file symlinked into every officially supported tool's agent config directory on initialization (FR-010/012)」)与 :127 段落(「the CLI (re)creates a **per-file** symlink for each `*.agent.md` … a real directory of per-file links」)MUST 同步改为真实渲染模型(同 C-1 语义);其对 FR-010/012 的引用按 spec 040 契约的现行语义更新。注意:这两处的退役措辞与 [[STR-001]] **不同字面**,守卫须分别钉住(见 C-4)。(FR-002)

**C-3**: create 流程终点(agents 命令模板的 create 段 + create-agent 技能的持久化说明)MUST 教授触发真相:定义落 `.specify/agents/{templates,instances}/`;上宿主注册面 = 执行 `specify render-agents --ai <tool>`;不再教「跑一次 specify CLI init/update」的旧措辞——init 是首次安装入口,保留其地位但不作为 re-render 的教法。(FR-003)

**C-4**: 契约测试 MUST 钉两类退役字面在对应面与其全部镜像/工具副本中**零命中**(历史档案类文件除外):① [[STR-001]] 字面 —— `templates/commands/agents.md` + 4 份工具副本(2026-10-08 实测:源 :25 与 `.qoder/commands/speckit.agents.md:19` 等副本均在);② `skills/create-agent/SKILL.md` 专属退役措辞 —— :122 表行短语与 :127 段落短语(实测字面见 C-2;精确禁用正则按改写后文本定形并附变异演练)。断言形态沿用 `test_shipped_surface_client_neutrality.py` 的 BANNED_PATTERNS 先例。(FR-011)

## § 文档增补(FR-009/010)

**C-5**: `shared/definitions/agent-definitions.md` MUST 新增「宿主注册面 (Host Registration Surface)」定义(概念 owner,clarify 裁定):每渲染模式工具实际读取 agent 定义的目录,路径取自代码映射表,产物为真文件;席位实例子类型与 `team-scope` 键的**分类学**条目一并落地(键集语义 owner 为代码,文档按引用)。(FR-009 前半)

**C-6**: `shared/workflow/symlink-model.md` MUST 新增 agent 面 CLI/IDE 关系条目:Qoder IDE 与 CLI **共享**项目级 `.qoder/agents/`(官方来源 `https://docs.qoder.com/extensions/subagent` 与 `https://docs.qoder.com/cli/subagent`,取证 2026-10-08);IDE 另有用户级 `~/.qoder/agents/`,框架不触碰;与 C-5 的定义互指、不重复定义。(FR-009 后半)

**C-7**: `docs/reference/cli/supported-agent-tools.md` 的 qoder 条目 MUST 补 agent 面说明:共享路径、文件名不决定 agent 名(frontmatter `name` 为准)、用户级作用域边界。(FR-010)

**C-8**: 三处文档间只允许指针形引用(C-6/C-7 指向 C-5 的概念与代码映射表),不得三处重述同一事实(One Source of Truth)。

## § 守卫聚合(FR-012)

**C-9**: 契约测试 MUST 钉链路闭合:断言「建队引用 stage 帧 → 席位实例落 `.specify/agents/instances/`(占位符全解析、`team-scope` 在)→ 渲染触发 → 宿主注册面出现席位类型」;对 render-agents 子命令钉参数值域(annotated 工具报错)与 stats 投影。(FR-012)

**C-10**: 契约测试 MUST 钉对应性(SC-003 的守卫化):「manifest 记录集 ↔ 中性层持久定义集」一一对应(区分框架产物与用户资产);断言只读 manifest,不改渲染语义;用户自有的第三方文件不被计入(边界情形)。

**C-11**: 每个守卫 MUST 附变异演练取证:植错一字 → 断言红 → 精确复原 → `diff -q` 字节相等;无取证的守卫视为未交付。演练证据形态沿用 `test_fast_fail_discipline.py:795-814` 先例。(FR-012 的取证面)

## § 死信核销(F-A02)

**C-12**: C-1/C-2 落地 + C-4 钉住后,F-A02(2026-09-11 分流 improve-skills 未执行、扩散至三面)具备核销条件;核销动作在 feedback 台账留痕(消费侧流程,不属代码面)。
