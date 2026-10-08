# Contract: Teaching Surfaces, Docs & Guards(教学面、文档与守卫)— 054

**Scope**: FR-001、FR-002、FR-003、FR-009、FR-010、FR-011、FR-012(守卫面);FR-007 的裁定记录已在 spec,本文只引用。

## A. 教学面改写(FR-001..003)

- A-1(`templates/commands/agents.md`,FR-001): 「Tool-specific directories are symlinks — never write to them directly」一句([[STR-001]],spec Shared Strings 表)MUST 改为真实模型陈述:宿主 agent 目录是渲染产出的**真实文件**,由 specify CLI 渲染,legacy 符号链接被替换;per-file 符号链接模型的教学 MUST 移除。
- A-2(`skills/create-agent/SKILL.md`,FR-002): :122 表行的「Per-file symlinked into every officially supported tool's agent config directory on initialization (FR-010/012)」与 :127 段落(「the CLI (re)creates a **per-file** symlink for each `*.agent.md` … `→ ../../.specify/agents/templates/<slug>.agent.md` … a real directory of per-file links」)MUST 同步改为真实渲染模型(同 A-1 语义);其对 FR-010/012 的引用按 spec 040 契约的现行语义更新。注意:这两处的退役措辞与 [[STR-001]] **不同字面**,守卫须分别钉住(见 C-7)。
- A-3(触发真相,FR-003): create 流程终点(agents 命令模板的 create 段 + create-agent 技能的持久化说明)MUST 教授:定义落 `.specify/agents/{templates,instances}/`;上宿主注册面 = 执行 `specify render-agents --ai <tool>`(与已落地触发面一致;不再教「跑一次 specify CLI init/update」的旧措辞——init 是首次安装入口,保留其地位但不作为 re-render 的教法)。

## B. 文档增补(FR-009/010)

- B-1(`shared/definitions/agent-definitions.md`): 新增「宿主注册面 (Host Registration Surface)」定义(概念 owner,clarify 裁定):每渲染模式工具实际读取 agent 定义的目录,路径取自代码映射表,产物为真文件;席位实例子类型与 `team-scope` 键的**分类学**条目一并落地(键集语义 owner 为代码,文档按引用)。
- B-2(`shared/workflow/symlink-model.md`,FR-009): 新增 agent 面 CLI/IDE 关系条目:Qoder IDE 与 CLI **共享**项目级 `.qoder/agents/`(官方来源 `https://docs.qoder.com/extensions/subagent` 与 `https://docs.qoder.com/cli/subagent`,取证 2026-10-08);IDE 另有用户级 `~/.qoder/agents/`,框架不触碰;与 B-1 互指,不重复定义。
- B-3(`docs/reference/cli/supported-agent-tools.md`,FR-010): qoder 条目补 agent 面:共享路径、文件名不决定 agent 名(frontmatter `name` 为准)、用户级作用域边界。
- B-4: 三处文档间只允许指针形引用(B-2/B-3 指向 B-1 的概念与代码映射表),不得三处重述同一事实(One Source of Truth)。

## C. 守卫(FR-011/012)——tests/contract/

- C-7(教学面缺席钉,FR-011): 契约测试断言两类退役字面在对应面与其全部镜像/工具副本中**零命中**(历史档案类文件除外):① [[STR-001]] 字面 —— `templates/commands/agents.md` + 4 份工具副本(2026-10-08 实测:源 :25 与 `.qoder/commands/speckit.agents.md:19` 等副本均在);② `skills/create-agent/SKILL.md` 专属退役措辞 —— :122 表行短语与 :127 段落短语(实测字面:「Per-file symlinked into every officially supported tool's agent config directory」、「the CLI (re)creates a **per-file** symlink for each」;精确禁用正则在实现期按改写后文本定形并附变异演练)。断言形态沿用 `test_shipped_surface_client_neutrality.py` 的 BANNED_PATTERNS 先例。
- C-8(链路闭合,FR-012): 契约测试断言端到端链:「建队引用 stage 帧 → 席位实例落 `.specify/agents/instances/`(占位符全解析、`team-scope` 在)→ 渲染触发 → 宿主注册面出现席位类型」;对 render-agents 子命令另钉参数值域(annotated 工具报错)与 stats 投影。
- C-9(变异演练取证,FR-012 的取证面): 每个守卫 MUST 附变异演练记录:植错一字 → 断言红 → 精确复原 → `diff -q` 字节相等;无取证的守卫视为未交付。演练证据形态沿用 `test_fast_fail_discipline.py:795-814` 先例。
- C-10(对应性断言,SC-003 的守卫化): 守卫断言「manifest 记录集 ↔ 中性层持久定义集」对应(区分框架产物与用户资产);该断言只读 manifest,不改渲染语义。

## D. 死信核销(F-A02)

- D-1: A-1/A-2 落地 + C-7 钉住后,F-A02(2026-09-11 分流 improve-skills 未执行、扩散至三面)具备核销条件;核销动作在 feedback 台账留痕(消费侧流程,不属本契约的代码面)。
