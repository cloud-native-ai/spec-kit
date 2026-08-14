# Contract: Relocation & Directory Taxonomy

契约对象:三目录的 Worker/Meta 划分(FR-023~FR-026)与 7 角色定义的迁移(D6)。

## T-1 目录级 Worker/Meta 划分

| 目录 | 类别 | 定义 | 占位符 | 可直接运行 | 生产者 → 消费者 |
|------|------|------|--------|-----------|------------------|
| `agents/` | **Meta Agent 预置集** | 操作对象为其他技能与其他 agent;均可独立运行 | 无 | 是 | 框架维护者 → init 渲染管线 → 各工具 agent 目录 |
| `skills/create-agent/templates/` | **Worker 能力模板** | 面向问题域,沿能力维度 | 有(`{{...}}` 白名单内) | 否(需实例化) | create-agent 技能 → 团队组建/单 agent 创作 |
| `skills/create-team/templates/agents/` | **Worker 职责模板** | 面向问题域,沿团队职责维度(阶段席位 + 编排契约) | 有 | 否 | create-team 技能 → 团队组建 |

限定表述(FR-024):指代三处时 MUST 分别使用"Meta Agent 预置集"、"Worker 能力模板"、"Worker 职责模板";文档与术语表 MUST NOT 再以裸 "templates" 指代。

## T-2 组队取件规则(FR-023a)

组建 Team 时:Meta Agent 从 `agents/` 选取;Worker Agent 从技能模板实例化选取。迁移完成后,7 个角色定义 MUST NOT 再以预置形态随 init 分发。

## T-3 迁移规格(D6)

- 7 个文件 `agents/<slug>.agent.md` 逐一**替换** `skills/create-agent/templates/agent-capacity-<slug>-template.md`(同一角色单一真源)。
- frontmatter MUST 转为中立键集(C-1~C-4)。
- 正文保持原样,**仅**允许把项目身份行与 Project Context 段中的 "Spec Kit (specify-cli)" 参数化为 `{{PROJECT_NAME}}`(白名单占位符)。
- 迁移后 `agents/` MUST NOT 残留任何 Worker 定义;`test_shipped_agent_presets.py` 的断言对象改为 T-4 的 Meta 预置集。
- 镜像联动:`sync-mirrors.py` 的 `("agents", ".specify/agents/templates", False)` 与 `("skills", ".specify/skills", False)` 两对 MUST 在迁移后 `--check` 通过。

## T-4 Meta 预置初始集(D7)

`agents/` 新作两个框架维护型 Meta Agent:

| slug | 职责(对应用户示例) | 操作对象 |
|------|---------------------|----------|
| `structure-adjuster` | 调整项目结构 | 目录/文件组织、结构约定 |
| `skill-verifier` | 验证技能执行效果 | 技能定义与执行证据 |

两者 MUST:`user-invocable: true`、中立元信息、正文含六大必备章节、职责限定为操作技能/agent/结构(Meta 判据),MUST NOT 声明业务工件操作。Team Supervisor 留在 create-team 模板,不在本轮进入 `agents/`。

## T-5 不一致裁定(FR-025)

- [[STR-005]](`capacity-scope`)与 [[STR-006]](`role-scope`)并存:实现期 MUST 在差别定义文档中裁定为"有意为之"(单 agent 域 vs 团队域的作用域语义不同)或给出收敛方案;MUST NOT 留白。
- 阶段模板(executor/evaluator/optimizer)缺运行参数字段:记录为"有意为之"(职责席位由团队编排赋参)。

## T-6 术语表锚定

交付时 `.specify/memory/glossary.md` MUST 含:Meta Agent(目录级)、Worker Agent(模板级)、以及"原 Agent"为"元 Agent"语音易混淆的更正条目;写入遵循术语表协议(用户确认后写)。
