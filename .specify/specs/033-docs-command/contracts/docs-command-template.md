# Contract: `/speckit.docs` 命令模板结构（templates/commands/docs.md）

本契约约束新增命令模板的结构与分发。全部条款为规范性声明；由契约测试钉住。

> 2026-08-10 修订：命令核心逻辑抽取为 `create-docs` 技能（`skills/create-docs/SKILL.md`），命令变为薄调度层。原 C-4/C-5/C-6/C-9 的内联内容要求改钉在技能上；命令侧新增强制委托条款（C-4a/C-12）。同日追加 **Hugo 呈现层**（C-13…C-17）：`docs/` 同时作为 Hugo 项目根，Markdown 挂载不复制，脚手架由 `scaffold-hugo.py` 确定性生成，CI 以文档指引交付。

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
- **C-13** 期望态基线 MUST 含第 5 项 **Hugo 呈现层**：`docs/` 同时是 Hugo 项目根（`docs/hugo.toml` + `layouts/` + `static/` + `.gitignore`）；脚手架自有目录（`layouts`/`static`/`public`/`resources`/`themes`/`archetypes`）MUST 声明为「非文档」，不得被调谐环当作内容分拣或归档；技能 MUST 链接 `references/hugo-site.md`；`description` MUST 携带站点类触发词。
- **C-14** 脚手架 MUST 由确定性脚本承载而非逐次手写 HTML：`skills/create-docs/scripts/scaffold-hugo.py`，stdlib-only、单 JSON 输出、四个 action（`scaffold`/`check`/`mounts`/`build`）；模板资产位于 `assets/hugo/`（`hugo.toml.tmpl` + `layouts/_default/{baseof,list,single}.html` + `layouts/index.html` + `_markup/render-{link,image}.html` + `static/css/site.css` + `dotgitignore`），不依赖外部主题与网络。
- **C-15** 内容 MUST 挂载而非复制（`docs/` 保持纯 Markdown，站点侧不改写任何文档）：含 `.md` 的每个 docs 目录生成 `content/<dir>` 挂载**与**排除 Markdown 的 `static/<dir>` 挂载（并排媒体可访问）；无 `.md` 的目录仅生成 `static/<dir>` 挂载；每个 `index.md` MUST 以文件挂载映射为 `content/<dir>/_index.md` 并从目录挂载 `excludeFiles` 排除（避免 leaf bundle 吞掉同级页面），磁盘上文件名保持 `index.md`；显式挂载会替换组件默认挂载，故 MUST 重新声明 `static → static`。仓库原生相对链接与相对图片路径 MUST 由 render hook（`GetPage` / `path.Join`+`relURL`）在构建期解析——禁止用 `uglyURLs` 映射（Hugo 静默忽略该形式）或改写 Markdown 来解决。
- **C-16** 零抖动与不覆盖：未变更树上重复运行 MUST 全部报 `unchanged` 且零写入；用户编辑过的脚手架文件 MUST 报 `kept` 并保持原样（仅 `--force` 覆盖）；`hugo.toml` MUST 仅托管 `# >>> speckit:mounts` 块，块外内容字节保持，缺少标记时报 `unmanaged` 且不写入；`hugo` 缺失时 `build` MUST 跳过并给出指引且**不**计为收敛失败。
- **C-17** CI 集成 MUST 以文档指引交付（本次决策：仅文档指引）：`references/hugo-site.md` MUST 给出安装 Hugo、从 `docs/` 目录构建、产物 `docs/public` 的步骤；脚本 MUST NOT 生成或写入任何工作流文件。
- **C-18** 文档域 MUST 与 tools/agent/team 的 create/improve 成对关系同构：`create-docs` 负责创建与**结构**（期望态基线、放置/命名/分类、移动归档、索引、notes 磁盘状态、Hugo 层），`improve-docs` 负责**已有文档内容**的证据驱动改进（单文档或单一机械维度的有界批次；九类改进；`--scope improve-docs` 审计留痕），技能本体的改进归 `improve-skills`。两者 MUST 各自注册且仅注册一行、`skill_id` 为规范形式、含 `## Feedback` 节（unit-id 分别为 `skill:create-docs` / `skill:improve-docs`）、SKILL.md < 500 行、镜像字节一致。`improve-docs` MUST NOT 创建/移动/重命名/归档文档（改为向 `create-docs` 交接），MUST NOT 改写决策历史（只标注 Deprecated / Superseded by），MUST NOT 在无 finding 时做纯样式改动。
