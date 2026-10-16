# Setup Recipes — 五步执行细则（sdd-project-setup）

> 本文件是 S1–S5 每步的**操作手册**：判据、命令形态、凭证 schema、依赖契约。全部命令自包含可用；路径/用户/别名全部入口参数化（与 sdd-loop-driver 的参数占位约定一致：`<alias>` `<run-user>` `<project-dir>` `<tool>`）。

## 机制矩阵维度定义（S1）

`scripts/mechanism-inventory.py` 对 `<project-dir>/.specify/` 输出以下维度（每个 ok/missing）：

| 维度 | 判定 | 对应机制 |
|------|------|----------|
| const | `.specify/memory/constitution.md` 存在 | 合法基线（41/41 项目全有） |
| feat | `.specify/memory/features.md` + `features/` 目录 | 特性注册表（fork 扩充核心，fleet 采用率 37/41） |
| gloss | `.specify/memory/glossary.md` | 项目词汇锚（~63% 采用） |
| fb | `.specify/memory/feedback/` 目录 | 反馈库（feedback-utils 引擎载体） |
| reg | `.specify/memory/register.md` | ID 登记（最新机制，fleet 仅 2/41——激活优先级低但不静默） |
| kb | `.specify/memory/knowledge/` | 长期知识库 |
| session | `.specify/memory/session/` | 会话记忆 |
| tools | `.specify/memory/tools.md` + `tools/` | 工具注册表 |
| skills | `.specify/skills/` 非空 | 安装技能集 |
| tmpl | `.specify/templates/` | 阶段模板 |
| specs | `.specify/specs/` | 规格产物目录（计数） |
| src | `.specify/source.json` | 框架版本 provenance（版本+时间戳） |
| compat | `AGENTS.md`/`CLAUDE.md`/`QODER.md`/`.github/copilot-instructions.md` 是指向 `.specify/instructions.md` 的完好符号链接 | 多工具兼容层 |

**状态分级判据**（脚本自动判定）：

- `absent`：`.specify/` 目录不存在。
- `degraded`：const 缺失，或 skills+feat 两者皆缺（fleet 实测形态：asi-podinfo / alert-center / weekly-report-publish 类——只有零星目录）。
- `partial`：const 在位但矩阵有 2+ 项 missing，或 compat 链接断。
- `complete`：const+feat+skills+tmpl 全在位且 compat 完好（其余维度允许按项目需要缺失，但进凭证「未激活清单」）。

## S1 盘点命令形态

本地：`python3 <skill>/scripts/mechanism-inventory.py --project <path> [--json]`
远端：`ssh <alias> "python3 -" < <skill>/scripts/mechanism-inventory.py --project <project-dir>`（或先 scp 脚本再执行；只读，无副作用）

## S2 INSTALL

**absent → 全新安装**：

```bash
# 本地
specify init . --here --ai <tool> --ignore-agent-tools [--force] [--no-git]
# 远端（经 su 与 sdd-loop-driver 同约定）
ssh <alias> "su - <run-user> -c 'cd <project-dir> && specify init . --here --ai <tool> --force'"
```

要点：`--here` 在当前目录初始化、`--force` 跳过非空确认、本地模板直拷（无网络下载）、可选 git 初始化。安装后立即跑一次 S1 复扫确认 baseline。

**partial/degraded → 刷新**：走 `/speckit.instructions`（在目标项目以对应 agent 执行）——非破坏性 reconcile（自定义内容恢复、共享文件先备份、兼容符号链接重建）。**禁止**手工整目录覆盖 `.specify/`。

## S3 RECONCILE（调协模式——按 S1 缺口按需逐项，惯常次序）

**次序固定、按需触发**：以下五个治理命令按此顺序执行，但**只执行 S1 判定存在缺口的项**——已就绪的项跳过并登记；不存在的机制不预建（tools/register 等低频机制缺≠错）。

| 次序 | 命令 | 触发条件（S1 矩缺） | 调协效果 |
|------|------|---------------------|----------|
| 1 | `/speckit.constitution` | const 缺 | 宪法 bootstrap（模板→项目语境→占位填充→版本裁决） |
| 2 | `/speckit.sanitize` | 框架资料存在陈旧残留（过期索引/死链/镜像漂移；complete 状态也可能有） | 框架资料卫生治理，陈旧残留按两级判据清理 |
| 3 | `/speckit.feature` | feat 缺 | 特性注册表种子（对既有代码 reconcile，非空仓常翻出大量 Implemented） |
| 4 | `/speckit.instructions` | compat 断、instructions 过期、partial/degraded 刷新 | 项目指令文件 + 各工具兼容符号链接重建 |
| 5 | `/speckit.docs` | 文档空间与实况漂移（docs 树与代码/特性不一致） | 文档空间治理（委托 create-docs 收敛核对） |

每项执行后登记（执行/已存在/跳过+理由）；全部处理或声明后进 S4。**不做整建**：五项之外的机制（glossary/feedback 目录/知识库目录等）仅在 S1 判缺且项目语境需要时逐个补建，否则进「未处理清单」。

## S4 VERIFY（五族前置检查 + 矩阵 + 链接）

**五族前置检查**（自 sdd-loop-driver/dispatch-recipes.md 迁入——原 Preflight 节，远端形态）：

| # | 检查 | 命令形态 | 判定 |
|---|------|----------|------|
| ① | SSH 连通性（本地拓扑跳过） | `ssh -o ConnectTimeout=5 -o BatchMode=yes <alias> true` | 限时内 0 = ok |
| ② | 非 root 运行用户 | `ssh <alias> "id <run-user>"` | uid≠0 = ok |
| ③ | 子代理 CLI 可用性 | `ssh <alias> "su - <run-user> -c '<cli> --version'"` | 版本串 = ok（记录进凭证） |
| ④ | 大模型配置 | 经宿主 CLI 配置面核验 model/context/effort | 三项齐备 = ok；不可读 = uncertain → 列待补清单 |
| ⑤ | spec-kit 框架可用性 | `test -d .specify && test -f .specify/memory/constitution.md && cat .specify/source.json` | 在位 = ok；本技能处置后仍缺 = fail |

加上：机制矩阵复扫达 complete（或 partial 且缺口已声明）、compat 链接核验 `find <project-dir> -maxdepth 2 -type l ! -exec test -e {} \; -print` 为空。三者齐备才进 S5。

## S5 候选工作清单（建议而非强制）

调协完成后产出一份**候选工作清单**——提示接下来可以做哪些事。三个内部来源（无用户明确指定时）：

1. **未完成的 feature**：`/speckit.feature` 维护的注册表中状态非 Implemented/Completed 的条目（Draft/Planned/Ready for Review 的推进项）；
2. **feedback 反馈的规模较大改进**：feedback 库中反复出现、标记为需要框架级或跨特性处理的条目（高频= toll，已到阈值的上送件也算）；
3. **speckit TODO 事项**：`/speckit.todo` 命令及相关机制维护的 TODO 表（SPECKIT TODO 块 + parked ideas）。

清单 schema（落宿主工作目录）：

```yaml
# sdd-candidates-<project-slug>-<YYYYMMDDTHHMM>.yaml
target: {alias|local-path, run-user, project-dir}
reconcile: {grade_before, grade_after, matrix, actions, unprocessed: [...]}
sources:
  features: [{id, name, status, next: "推进到 <下一状态>"}]
  feedback: [{entry, count_or_signal, suggestion}]
  todos: [{item, location}]
suggestion: >-
  以上为候选工作；如需以 SDD 全流程推进某项，可调用 sdd-loop-driver
  （可选，非强制；sdd-loop-driver 亦可不经本技能独立运行）。
```

**语义红线**：清单是「有哪些可做的事」的提示，不携带任何「必须调用 sdd-loop-driver」的语义；调用与否由用户或上游流程决定。

## 软协同契约（与 sdd-loop-driver）

- **非强绑定**：两技能各自可独立运行。本技能不要求 sdd-loop-driver 存在，sdd-loop-driver 也不依赖本技能先行——其自有必要 preflight（见其 dispatch-recipes.md），检查不通过时才 handoff 给本技能。
- **本技能 → sdd-loop-driver**：S5 候选工作清单是建议入口之一；sdd-loop-driver 的输入源除清单外还包括用户明确指定的特性/切片。
- **sdd-loop-driver → 本技能**：其 preflight 发现 `.specify/` 缺失/宪法不在位/机制退化时，把处置 handoff 给本技能（模式由探测定：缺失=install，退化=refresh），处置完成后回到循环。
- 职责切分线：**框架调协（install/reconcile/verify/候选清单）** = 本技能；**SDD 六阶段循环/状态脊/收尾纪律** = sdd-loop-driver。互不越界，互不强依赖。
