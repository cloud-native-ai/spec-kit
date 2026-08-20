# Contract: `/speckit.docs` 命令模板结构（templates/commands/docs.md）

本契约约束新增命令模板的结构与分发。全部条款为规范性声明；由契约测试钉住。

> 2026-08-10 修订：命令核心逻辑抽取为 `create-docs` 技能（`skills/create-docs/SKILL.md`），命令变为薄调度层。原 C-4/C-5/C-6/C-9 的内联内容要求改钉在技能上；命令侧新增强制委托条款（C-4a/C-12）。同日追加 **Hugo 呈现层**（C-13…C-17）：`docs/` 同时作为 Hugo 项目根，Markdown 挂载不复制，脚手架由 `scaffold-hugo.py` 确定性生成，CI 以文档指引交付。

> 2026-08-20 修订（呈现层解耦）：站点呈现/发布是文档基础结构**之上的可选高阶能力**，归 `create-pages` 技能（`skills/create-pages/`，三阶段流水线「本地文档库 → Hugo 渲染 → Pages 服务」，其中阶段 2 承载原 `scaffold-hugo.py` + `assets/hugo/` + `references/hugo-site.md`）。`create-docs` 只负责基础结构，其期望态基线不再含站点层。据此：C-13 收窄为「非文档目录跳过」这一条保护性要求，C-14…C-17 撤销（能力与其测试随脚本迁往 create-pages，且不得再以 MUST 形式要求任一文档空间存在站点层），C-18 的 `create-docs` 职责删去 Hugo 层。

- **C-1** 源模板 MUST 位于 `templates/commands/docs.md`，并在 `.specify/templates/commands/docs.md` 存在字节一致镜像（`regen-command-copies.py --check` 零漂移）。
- **C-2** frontmatter MUST 含 `description`（一行）与 `handoffs`；引用共享文档 MUST 使用根相对形式（`shared/workflow/...`、`shared/patterns/reconcile-pattern.md`），由再生成器重写为 `.specify/shared/...`（test_shared_reference_rewrite 约定）。
- **C-3** 模板 body MUST 含以下章节（顺序固定）：`## User Input`（含 `$ARGUMENTS` 与 User Input Protocol 引用）、`## Glossary`、`## Outline`、`## Feedback`、`## Documentation`、`## Handoffs`。
- **C-4** 引擎语义 MUST 承载于 `create-docs` 技能：技能 MUST 含作用域判定表（无参全量 / 单目标 / 原始材料扇出 / 写作委托文档写作 / bootstrap 五行，FR-003）与分级确认门禁表（安全写入自动 / 移动归档须计划确认，FR-004）。命令 `## Outline` MUST 点名五个作用域但 MUST NOT 内联完整判定表。
- **C-4a** 命令 `## Outline` MUST 声明对 `create-docs` 技能的强制委托（delegation mandatory），并将技能指认为引擎语义的唯一事实源。
- **C-5** 四件强制产物及其落点 MUST 由技能声明：观察快照（内联）、干跑计划（`.specify/docs/plans/`）、审计日志（`.specify/docs/audit/`，零收敛也落盘）、残差报告（内联）；命令 SHOULD 点名四件产物以稳定用户预期。
- **C-6** 技能 MUST 声明归档区为 `docs/archive/`，且正式区动作词汇中不出现"删除"（notes 区确认删除除外，须引用 FR-006c 语义，即"只归档不删除"）。
- **C-7** 模板 MUST 保持薄调度层：引擎细节引用 `shared/patterns/reconcile-pattern.md` 与 `create-docs` 技能，不内联重复完整 R0–R6 规程（reconcile-pattern §Applying-6）。
- **C-8** `## Feedback` 节 MUST 符合 `shared/workflow/feedback-step.md` 约定（unit-id `/speckit.docs`、unit-type command）；`docs` MUST 加入 `tests/contract/test_feedback_command_classification.py` 的 `COMPLEX_COMMANDS` 清单，计数 13→14，SIMPLE 保持 4。
- **C-9** 期望态基线内容 MUST 与 requirements.md FR-002/FR-010 一致，并由技能承载：六类目录 + notes；特殊名注册表四条种子（README/ARCHITECTURE/CONTRIBUTING/CHANGELOG 及各自语义）。
- **C-10** 运行时副本 MUST 覆盖仓库中已存在的全部工具命令目录（.claude/.github/.qoder/.qwen/.opencode/.codex/.hermes/.iflow 等），由 `regen-command-copies.py` 生成，禁止手改。
- **C-11** 命令参考文档 MUST 新增 `docs/reference/commands/docs.md`（结构对齐既有命令参考文档；dogfooding 重组前路径为 `docs/commands/docs.md`），并在 `docs/tutorials/quickstart.md` 命令表加行。
- **C-12** 技能源 MUST 位于 `skills/create-docs/SKILL.md`，并在 `.specify/skills/create-docs/SKILL.md` 存在字节一致镜像（sync-mirrors 零漂移）；frontmatter MUST 含 `name: create-docs`、带触发词的 `description`、`skill_id`；body MUST 含符合 `shared/workflow/feedback-step.md` 约定的 `## Feedback` 节（unit-id `skill:create-docs`、unit-type skill）。
- **C-13**（2026-08-20 收窄）站点/呈现层 MUST NOT 成为文档空间期望态的一部分——文档空间不含站点层时依然完整合规。仅保留一条保护性要求：技能 MUST 声明站点工具目录（`layouts`/`static`/`public`/`resources`/`themes`/`archetypes`）为「非文档」，调谐环 MUST NOT 将其当作内容分拣或归档；站点/发布请求 MUST 交接 `create-pages`，MUST NOT 在 `create-docs` 内实现。技能 `description` MUST NOT 再携带站点类触发词（触发词归 `create-pages`）。
- **C-14**（2026-08-20 撤销）脚手架脚本与模板资产的位置要求不再约束本域。挂载渲染脚手架（`scaffold-hugo.py` + `assets/hugo/`）现位于 `skills/create-pages/`（阶段 2），其 stdlib-only、单 JSON 输出、四 action 等行为要求由 `create-pages` 自身的测试承载。
- **C-15**（2026-08-20 撤销）挂载而非复制的语义（`content/<dir>` 与 `static/<dir>` 双挂载、`index.md` → `content/<dir>/_index.md` 文件挂载、重新声明 `static → static`、render hook 解析相对链接与图片、禁用 `uglyURLs` 映射）随脚本迁往 `create-pages`，作为该技能阶段 2 的行为约束，不再是本域契约。
- **C-16**（2026-08-20 撤销）零抖动与不覆盖语义（重复运行报 `unchanged`、用户编辑报 `kept`、仅托管 `# >>> speckit:mounts` 块、`hugo` 缺失时跳过 build 不计失败）同随脚本迁往 `create-pages`。
- **C-17**（2026-08-20 撤销）CI 集成以文档指引交付的要求随 `references/hugo-site.md` 迁往 `create-pages`；本域不再对 CI 产物提出要求。
- **C-18** 文档域 MUST 与 tools/agent/team 的 create/improve 成对关系同构：`create-docs` 负责创建与**基础结构**（期望态基线、放置/命名/分类、移动归档、索引、notes 磁盘状态），`improve-docs` 负责**已有文档内容**的证据驱动改进（单文档或单一机械维度的有界批次；九类改进；`--scope improve-docs` 审计留痕），技能本体的改进归 `improve-skills`；基础结构之上的**可选**呈现/发布能力归 `create-pages`。两者 MUST 各自注册且仅注册一行、`skill_id` 为规范形式、含 `## Feedback` 节（unit-id 分别为 `skill:create-docs` / `skill:improve-docs`）、SKILL.md < 500 行、镜像字节一致。`improve-docs` MUST NOT 创建/移动/重命名/归档文档（改为向 `create-docs` 交接），MUST NOT 改写决策历史（只标注 Deprecated / Superseded by），MUST NOT 在无 finding 时做纯样式改动；站点层需求 MUST 交接 `create-pages`。
