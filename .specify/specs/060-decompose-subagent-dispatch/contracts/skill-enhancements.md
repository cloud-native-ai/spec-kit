# Contract: 三技能承接面增强（skill-enhancements）

**Feature**: 060 | **FR 覆盖**: FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-012（承接侧）, FR-014, FR-016
**性质**: 结构契约——条款由契约测试机械判定。

## A 节：create-agent 增强（US1 + 生命周期）

- **A-1**: `agents/sdd-executor.agent.md` MUST 存在且为合法能力模板：frontmatter 含中性词表字段（name/description/user-invocable/model-tier/capability-tools/skills/run-turn-budget），`description` 声明三要素能力面（项目目录工作目录、加载项目上下文、执行 `/speckit.*` 阶段命令），职责字样（setup/requirements 等）零命中（数据模型 V-E1-1）。
- **A-2**: 模板全文 MUST 满足内容判据机械面：无用户名、IP、环境别名、项目路径字面量（V-E1-2）。
- **A-3**: create-agent SKILL.md MUST 增补**模板分发层内容判据**：不含用户/环境/项目专用信息 → 框架分发角色集（`agents/` 源码，`specify init` 安装）；含项目专属信息 → 项目侧容量模板；判据首次应用结论（sdd-executor → 框架分发）随条款记录。
- **A-4**: create-agent SKILL.md MUST 增补**多职责实例化**说明：从同一 capacity 模板产出 ≥2 个职责实例（capacity-scope 引用绑定、一实例一职责、复述为零）；与 create-team 席位实例化的关系（同为 instance 产出路径，team-scope 与 capacity-scope 互斥）MUST 成文。
- **A-5**: create-agent SKILL.md 的 Agent Lifecycle 节 MUST 扩格退役规则：retired 状态标记保留（archive-not-delete）、先解引用校验（活引用=运行中执行/团队席位/其他实例 capacity-scope 引用）、拒绝退役时输出待解引用清单（FR-016；V-E2-3）。
- **A-6**: 镜像义务：`agents/sdd-executor.agent.md` ↔ `.specify/agents/templates/sdd-executor.agent.md` 字节一致（sync-mirrors 对）。

## R 节：run-agent 增强（US2 + FR-012 承接）

- **R-1**: run-agent SKILL.md 的 Run Mode MUST 增补 Execution 拓扑声明输入形态：本地（项目目录+CLI）/远端（目标+身份+目录+CLI）参数集，内联参数与执行配置文件双形态等价（配置 schema 沿用既有 execution-config）。
- **R-2**: 冲突消解条款 MUST 成文：两形态同给且任一要素不一致 → 解析期拒收报错并列冲突字段，MUST NOT 静默取舍（V-E3-3）。
- **R-3**: 新文件 `skills/internal/run-agent/references/dispatch-preflight.md` MUST 存在并承载五族前置检查表+失败处置链（数据模型 E4 全表：①SSH/②非 root/③CLI 版本/④LLM 配置/⑤框架可用性；处置：①②③ fail 停线上送、④ uncertain 列待补清单、⑤ fail handoff sdd-project-setup）。
- **R-4**: run-agent SKILL.md MUST 以引用形态把 dispatch-preflight.md 纳入 Run Mode 程序（检查先于派发；结论 ≤3 行/项入调用方状态脊），MUST NOT 在 SKILL.md 复制检查表正文。
- **R-5**: run-agent 的拓扑配方 MUST 引用 [[STR-006]]，SKILL.md 与 references/ 均 MUST NOT 复制六配方正文；配方未覆盖的形态 MUST 快速失败报告而非就地发明（FR-008）。
- **R-6**: run-agent 的派发时治理节 MUST 增补反嵌套义务：派发提示词不引用驱动/循环技能、不指示加载技能、不含循环逻辑；拦截在派发前（派发前自检扩展）；违反即快速失败（FR-009；V-E5-1）。
- **R-7**: run-agent 既有边界保留：模态选择规则、可见性契约、注入子句校验、单代理单任务边界（多代理编排外派 team）均 MUST NOT 被本次增强改写——新增义务以增补落位，既有条文语义零变更（FR-015 侧）。

## I 节：improve-agent 增强（US4）

- **I-1**: improve-agent SKILL.md 的 Input Contract MUST 增补执行证据输入形态：可见性三元组、执行日志、异常回传行、失败模式记录——回流目标限定 Template/Instance 层（FR-014）。
- **I-2**: Execution 是 own-run 证据而非自改对象的既有边界 MUST 保持成文（Self-Improvement boundary 不动）。

## 镜像与接线（全契约通用）

- **X-1**: 本契约涉及的全部技能源文件变更 MUST 同步镜像：`skills/internal/*` ↔ `.specify/skills/internal/*`、`skills/external/*` ↔ `.specify/skills/*`（sync-mirrors MIRROR_PAIRS）。
- **X-2**: run-agent 新增 reference 文件不改变 probe-registry 认领面（unit 数 73 → 74，因 run-agent 的 references 不新增 unit——unit 按 SKILL.md 计）；compile-embeds --check MUST 维持零漂移。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| A-1/A-2 | FR-003 | test_a1_sdd_executor_template_valid / test_a2_content_criterion_mechanical |
| A-3 | FR-003 | test_a3_distribution_criterion_in_create_agent |
| A-4 | FR-004, FR-005 | test_a4_multi_duty_instantiation |
| A-5 | FR-016 | test_a5_retire_lifecycle_in_create_agent |
| A-6 | FR-003 | test_a6_mirror_pair_byte_identical |
| R-1/R-2 | FR-006 | test_r1_topology_input_forms / test_r2_conflict_rejection |
| R-3/R-4 | FR-012 | test_r3_preflight_reference_file / test_r4_preflight_owned_by_run_agent |
| R-5 | FR-008 | test_r5_recipes_referenced_not_copied |
| R-6 | FR-009 | test_r6_anti_nesting_in_run_agent |
| R-7 | FR-015 | test_r7_existing_rules_unchanged |
| I-1/I-2 | FR-014 | test_i1_evidence_input_forms / test_i2_execution_not_self_edited |
| X-1/X-2 | FR-003, FR-012 | test_x1_mirrors_synced / test_x2_unit_count_and_zero_drift |
