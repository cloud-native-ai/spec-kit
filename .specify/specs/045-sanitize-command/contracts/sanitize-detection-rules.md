# Contract: 确定性检测规则与证据包形态(需求 045 / Feature 047)

**Requirement → Feature**: `045-sanitize-command` → Feature 047 Framework Material Hygiene  
**消费方**: sanitize-utils.py 引擎、tests/unit/test_sanitize_engine.py、tests/fixtures/sanitize/

程序优先总纲:下列规则全部为固定规则判定,由引擎确定性执行,agent 不参与(SC-004)。语义类别(stale-residue/redundant)仅消费本契约 §5 的证据包。

## 1. 死引用(dead-reference)

- C-1 抽取范围:**存活材料**——memory 层(todo/draft/顶层 .md)、存活 specs(.specify/specs/,排除 .archive)。**冻结历史豁免**:`.specify/archive/**` 与 `.specify/history/**` 不做引用检查——其引用描述归档/蒸馏时点的历史状态,"失效"是按设计而非缺陷。**排除围栏代码块**(fenced code block)内部——与 docs-utils 断链检查的排除惯例一致;行内反引号内容**纳入**抽取。
- C-2 抽取语法(正则可表达,顺序应用):
  1. Markdown 链接 `[text](relpath)` / `[text](<relpath>)` → 相对链接,按所在文件目录解析;
  2. 行内代码/正文中的仓库相对路径:匹配已知根前缀 `scripts/`、`shared/`、`templates/`、`docs/`、`skills/`、`agents/`、`src/`、`tests/`、`.specify/` 开头的路径样式串;
  3. 命令引用 `` speckit.<name> `` → 目标 `templates/commands/<name>.md` 必须存在;
  4. 技能引用 `` `<name>` 技能 `` 或 `skills/<name>` → `skills/<name>/` 必须存在。
- C-3 解析豁免:http(s) URL、纯锚点(`#...`)、mailto、`~` 开头用户路径、占位符形态(`<...>`、`{...}`、`[...]` 单词级)不判定。
- C-4 docs 树与根注册文件的断链:直接复用 docs-utils 链接校验输出(契约 sanitize-engine §5),不重复实现;其结果映射为 dead-reference 发现。
- C-5 每条 dead-reference 发现的 target=被检材料路径,summary 含"引用了不存在的 <目标>"与定位(行号或锚文本)。

## 2. 索引↔存储一致性(index-inconsistency)

双向判定,每个索引族一组规则:

- C-6 features 族:`features.md` 表行(ID、Feature Details 路径、Spec Path)↔ 磁盘文件,双向:行指向的文件缺失 / 磁盘存在 `features/<ID>.md` 而索引无行。
- C-7(需求 055 修订)feedback/session/knowledge 族:三库均已改为**扫描派生**(req 055),维护型索引不复存在;对应 `index.json` **存在本身**即一条 index-inconsistency 发现(target=该文件,处置 repair,修复指向所属引擎 `--action reindex`——落 state 后退役旧文件)。混合版本过渡期旧引擎机器可能合法重建该文件,故 sanitize 只提示、绝不代删;旧的双向判定与簿记文件豁免规则随维护型索引一并废止(条目由引擎扫描识别)。
- C-8 evidence 族:`evidence/index.json` 登记的运行目录 ↔ `ev-*` 目录,双向。
- C-9 索引 JSON 自身不可解析 → 单条 index-inconsistency(target=索引文件),不逐条展开。

## 3. 符号链接有效性(broken-symlink)

- C-10 固定链接集:`CLAUDE.md`、`QODER.md`、`AGENTS.md`、`.github/copilot-instructions.md`、`.github/skills`、`.qoder/skills`、`.claude/skills`(2026-10-12 增补后两项,对齐 CLI `_SKILLS_SYMLINK_ASSISTANTS` 的技能链接面)。判定:断链(链接存在而目标缺失)、形态漂移(被普通文件/目录替换)两种始终为发现;"缺失"仅在**对应工具面存在**时为发现(`CLAUDE.md`↔`.claude/`、`QODER.md`↔`.qoder/`、`AGENTS.md`↔`.specify/instructions.md`、`.github/*`↔`.github/`、`.qoder/skills`↔`.qoder/`、`.claude/skills`↔`.claude/`)——单一 CLI 初始化的客户工作区不得因其他 CLI 的链接缺失而报发现。处置一律 `delegate`(移交 /speckit.instructions 再生成,不在本命令修复)。

## 4. 镜像漂移(mirror-drift)

- C-11 复用 `sync-mirrors.py --check` 的 JSON 输出:MISS/DIFF/ORPHAN 项逐条映射为 mirror-drift 发现(处置:MISS/DIFF → delegate(sync-mirrors);ORPHAN(多余文件)→ delegate)。
- C-12 孤儿目录补检(引擎自实现,sync-mirrors 不覆盖,**仅限 skills 镜像对**——`agents/` 源侧只镜像 `*.agent.md` 而 `.specify/agents/` 另含合法运行时结构 templates/instances/execution,按 agent-definitions 分类法,源侧无对应目录不构成改名残留):`.specify/skills/` 下存在而 `skills/` 源侧已无对应目录 → mirror-drift 发现;若该目录名未登记于 `src/specify_cli/__init__.py` 的 `_OBSOLETE_*` 注册表 → severity=high(未注册改名残留,对齐 AGENTS.md Rename/retire 纪律),处置 `delete`(破坏性,入清理计划)。
- C-13 引擎自身 strict 镜像(`scripts/python/sanitize-utils.py` ↔ `.specify/scripts/python/`)漂移同样报告(自检不豁免镜像纪律)。

## 4a. init 迁移残留(migration residue;2026-10-12 增补)

跨代 `specify init` 之后,客户工作区可能残留前代结构。检查器 `check_legacy_install_residue` 与 `check_flat_internal_duplicates` 承载本节;全部确定性、全量 derivable(不依赖 LLM 判定):

- C-22 **前代安装残留**(category `stale-residue`,处置一律 `archive`,severity 遵默认 high;apply 的 delete 拒绝非空目录且内容性残留遵循 archive-not-delete,故不经 delete):
  - **旧代技能目录**:`.specify/skills/<name>/` 为真实目录(符号链接豁免)且 `<name>` ∈ 旧代退役技能名集;**仅客户工作区适用**——`skills/external/` 源侧存在(框架仓)时该面归 mirror-drift 孤儿检查(C-12)管辖,避免同目标双报冲突处置。名集解析梯级:框架仓内读 `src/specify_cli/__init__.py` 的 OBSOLETE-ASSET-REGISTRY 标记块(活真源);客户工作区(无 `src/`)退回引擎内置 `LEGACY_SKILL_NAMES` 常量(CLI 清单的镜像,契约测试钉住防漂移;引擎侧同样置于注册表标记区内,零退役引用扫描按同一豁免机制剥离)。已知后继者(draw-*×6→draw-diagram、git-*×4→git-workspace、manage-project/visualize-project→summarize-project、sdd-workflow→shared/workflow)在 summary 中点名,供归档后核对引用面迁移。**用户自建技能永不入候选**。
  - **旧代 git-workflow 状态文件**:`.specify/git-workflow.md` 或 `.specify/memory/git-workflow.md` 存在,且 `docs/git-workflow.md` 已存在(新模型状态面已落地——guard:两态皆无或仅旧态时不报,避免误报未迁移的旧代项目);summary 指向 git-workspace bootstrap 核对分支状态迁移。
  - **旧代工具记录目录**:`.specify/tools/` 为目录且新址 `.specify/memory/tools/` 已存在;summary 指向 `shared/definitions/tool-definitions.md` § Terminology(术语与消歧真源)。
- C-23 **内部分层平铺重复**(category `redundant`,处置 `archive`,severity=medium):`.specify/skills/internal/<name>/` 存在且同名平铺目录 `.specify/skills/<name>/` 亦为真实目录——平铺副本即 init 平铺迁移降级态(init 语义:nested 已存在时 flat 判 stale)。可从运行时树直接推导,不依赖任何名集。summary 提示归档前抽查平铺副本无本地独有修改。
- C-24 **注册表优先级**:框架仓内 `load_obsolete_registry` 非空时以其为准(与 CLI 同源);客户工作区退回内置常量。两清单的一致性由契约测试以"常量 ⊇ CLI 清单"钉住(CLI 删除条目属正常收敛,不强制反向)。

## 5. 语义证据包(stale-residue / redundant 的输入)

- C-14 候选材料:memory-todo/memory-draft 根下的 .md(每文件一候选)。
- C-15 claims 抽取(机械):frontmatter 日期字段(parked_at/created/status 等)+ 正文中的状态声明短语(如"未落地""待办""P1–P5"清单行、"status: parked/draft")。抽取为短语列表,不做语义归纳。
- C-16 evidencePack 组装:
  - `gitLog`:`git log --oneline -n 20 -- <pathspecs>`——pathspec 由材料中的根前缀路径 + **文件名片段 glob**(`*<fragment>`,如 `*platforms/opencode.mjs` 匹配深层同尾路径)组成;**无日期过滤**——"未落地"类声明断言工作的缺失,矛盾提交常早于声明日期(结转抄写陈旧结论的典型形态),按计数截断(20 行)而非时间窗;无任何 pathspec 时退化为 `-- .specify/memory`;
  - `pathExistence`:根前缀路径 → 存在/缺失映射(片段不参与,避免无根噪声)。
- C-17 agent 判定输出(经 record 写入):verdict=stale-residue(声明与证据矛盾)/ redundant(内容已完整并入其他存活材料)/ insufficient(证据不足,不写入);每 verdict 附具体证据引用(commit 哈希/路径)。
- C-18 处置映射:stale-residue → delete("已合入即删除"纪律);redundant → archive(被取代材料归档至 `.specify/archive/memory/<原相对路径>`)。

## 6. 判定纪律

- C-19 所有确定性检查在单次 collect 中全量运行;任一检查器崩溃 → 该类别跳过并在 notes 声明,不影响其余类别(失败如实报告)。
- C-20 严重度遵循 data-model §1 默认映射;检测器可上调不得下调。
- C-21 检查器的全部输出走摘要/计数形态;材料原文仅按升级阶梯定向节选(040 纪律)。

## 7. 契约测试锚点

- 夹具 `tests/fixtures/sanitize/` 覆盖:死引用(链接/路径/命令/技能四形态 + 围栏豁免 + 占位符豁免)、索引双向缺项、断链/形态漂移链接、孤儿镜像目录(已注册/未注册两态)、真实案例复刻(过期 parked todo + 已合入提交,SC-001)。
- 迁移残留(§4a,2026-10-12 增补)以 `tests/unit/test_sanitize_checks_migration.py` 承载:旧代技能目录(注册表/常量两解析梯级 + 符号链接豁免)、旧代状态文件(guard 两态)、旧代工具目录(guard 两态)、内部分层平铺重复(正/反例)、`.qoder/skills`/`.claude/skills` 形态漂移(C-10 增补)、LEGACY_SKILL_NAMES ⊇ CLI `_OBSOLETE_SKILLS` 漂移护栏。
- 每条 C 规则至少一个正例断言;C-1/C-3 豁免规则须有反例夹具。
