# Contract: run-skills / run-team 接线结构(contracts/run-skills-wiring.md)

本契约为本特性全部**制品类条款**的机器可判定面;`tests/contract/test_run_skills_wiring.py` 逐条映射。行为类条款单独标注,不得声称由测试覆盖(制品类/行为类条款二分)。

字符串引用:`[[STR-001]]` = `skills/internal/run-skills`、`[[STR-002]]` = `skills/internal/run-team`(真源 requirements.md § Shared Strings)。

## 制品类条款(artifact-class — 契约测试断言落盘文本)

- **C-1 存在与镜像一致**:[[STR-001]]/SKILL.md 与 [[STR-002]]/SKILL.md 存在;`.specify/skills/internal/{run-skills,run-team}/SKILL.md` 与 canonical 逐字节一致。
- **C-2 frontmatter**:两 SKILL.md frontmatter 含 `classification: internal` 与 `skill_id: "<SKILL:.specify/skills/internal/<name>/SKILL.md>"`(run-agent 先例形态);name 与目录名一致。
- **C-3 skills.md 路由表 5 行**:`templates/commands/skills.md` Delegation 路由表恰含——NOT exists → `create-skills`;EXISTS(常规改优)→ `improve-skills`;merge 意图 → `merge-skills`;think/思想演练意图 → `think-skills`;run 意图 → run-skills(runtime path [[STR-001]])。每行含 runtime path 与输入/产出说明;**run 行的输入说明 MUST 钉住调用语法 `run-skills <名称|路径>`**(该语法字面量由本契约钉住,quickstart 场景 A 的 premise ① 引用此处)。
- **C-4 team.md 路由与 run 指向**:`templates/commands/team.md` 中**所有** run 语义的技能指向改为 run-team([[STR-002]])——Modes → Capability Routing 表 run 行、Routing flow 编号步骤中的 run 步、Ambiguous or Unsupported Intent 能力列举中的 run 行;不再有任何 run → create-team 执行路径引用;create → create-team、modify → improve-team 两行不变。
- **C-5 team.md Run Mode 程序性清零**:team.md 的 Run Mode 节不含程序性编号步骤与祈使流程,仅存路由指引与 run-team 的输入/产出说明;散布于其他节的 run 执行指引随 C-4 改指向后不得残留执行细节(判据边界:team.md 其余节——Outline 引言/Modes 表/Default Behavior/Ambiguous Intent/Goal-Based Create/Persistence/Wrap-up/Handoffs——保持各自的信息结构,本条只约束其中 run 执行细节的清零)。
- **C-6 agents.md 核查**:`templates/commands/agents.md` 意图表 3 行分别指向 run-agent/create-agent/improve-agent 的 internal runtime path,路径实存(本特性预期零改动;发现漂移修路由行)。
- **C-7 probe 注册与编译**:`shared/definitions/probe-definitions.md` Object 表含 `skill:run-skills` 与 `skill:run-team` 的 skill-wrapup 行;`probe-utils.py --action compile-embeds --check` 零漂移(71 单元)。
- **C-8 指南例外条目**:`templates/skills.md` 与 `.specify/skills.md` 字节一致,且均载明——run-skills 为「internal 技能不被 agent 发现」规则的具名例外,及多宿主降级路径(`/speckit.skills` run 意图路由显式路径加载)。
- **C-9 无重复语义技能**:`skills/external/` 与 `skills/internal/` 目录清单中,本特性新增目录仅 [[STR-001]]、[[STR-002]];不出现与 improve-skills/merge-skills/think-skills/create-agent/create-team/improve-team 语义重复的新目录(对照实现前基线清单)。

## 行为类条款(behavior-class — 真源文档载明义务 + 评审强制;无制品可观测,不声称测试覆盖)

- **B-1 自足运行**(SC-001):无本仓 ambient 指令的 agent 仅读 [[STR-001]]/SKILL.md 即完成一次未注册技能的解析-加载-执行-转述。评审形式:fresh-context 执行记录。
- **B-2 确定性披露**(SC-002):同一输入恒得同一路径;0 命中输出逐项列出已搜索位置;多命中披露优先级与所选路径。落盘后义务真源 = run-skills 技能体。
- **B-3 行为平价**(SC-003):run-team 对 P-1…P-10 每条义务以同等或更严强度落地(contracts/run-team-parity.md 为对映真源)。评审形式:对映表逐条核对 + 抽样实跑。
- **B-4 派发治理平价**:run-team 编排子代理时携带快速失败注入子句、要求异常回传行、按 subagent-definitions 模态派发;异常停不得原样重派。
- **B-5 尽力检测提示**(FR-007):已注册目标的「可能可直接斜杠调用」提示为非阻断,判不准不阻断执行。

## 红先行取证

测试先于制品撰写:每条 C-条款的失败取证(制品缺失态 FileNotFoundError/标题缺失)留存 `notes/red-first-evidence.md`;区分「测试正确地红」与「测试本身坏」。
