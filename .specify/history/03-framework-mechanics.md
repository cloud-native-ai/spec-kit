# 主题：框架机制改进（命令 / 技能 / 模板 / 依赖 / 产物治理）

覆盖会话：217c6503 (2026-06-23, cws-lib-python 移除)、46a705d0 (2026-06-25, git-workflow 三模式)、2a38dcaf (2026-07-15, team 产物四层)、7d64ad76 (2026-07-17, symlink 文档)、cefe2c64 (2026-07-17, instructions 覆盖修复)。相关：[[00-cross-cutting-lessons]]。

## 1. 关键决策与理由

- **instructions 覆盖根因修复**（cefe2c64，commits `97ba056` + `93f240a`）：真正覆盖源不是 `init`（从不写 instructions.md），而是 `generate-instructions.sh` 的 "Smart Fusion" 以模板为基底只融合回 `## Project Overview`。修复：基底改为"当前已存在文件"；脚本层默认非破坏；命令提示词改为逐段对照、仅更新漂移事实。备份命名从日期级改秒级时间戳（同日重跑会覆盖掉唯一未受损原始备份）+ 同秒 PID 兜底。
- **依赖彻底移除**（217c6503）：cws-lib-python 零调用（实际函数来自 cws-lib-bash），删 7 个文件中的检查与示例；只删 python 侧保留 bash 侧；放弃"只删条件 source"（配套 `check_dependency` 强制检查才是有害门槛）。
- **git-workflow 技能三模式**（46a705d0）：Mode 1 Setup / Mode 2 Maintain（健康报告）/ Mode 3 Execute（5 个预置操作 A–E + 触发词意图匹配，不开放任意 git 命令）；`docs/git-workflow.md` frontmatter 作分支名单一事实源；超 500 行内容抽 `references/instructions-lookup.md`。
- **team 运行产物四层结构**（2a38dcaf，commit `03d5aad`）：团队定义 `.specify/teams/<slug>/team.md`（跟踪）+ 运行报告 `runs/<UTC-ts>-report.md`（跟踪累积）+ 交付物落用户目标路径 + 中间态进 git-ignored `.specify/teams/.work/<slug>/`；团队从扁平文件迁为每团队目录（~30 处引用迁移）。忽略目录弃名 `.runs/`（与跟踪子目录 `runs/` 近同名易混淆），对齐既有 `.work/` 约定。
- **symlink 防破坏文档**（7d64ad76）：只在 Instruction 层追加两条 bullet（"Do NOT break the symlinks" + "Detect & repair"），不写入 Constitution——symlink 属框架机制而非用户项目原则，写入违反模板中立性。

## 2. 可复用经验 / 踩坑

- 用户报障归因可能错误：先追查所有写入路径（`_CORE_SPECIFY_ASSETS` 仅用于审计）再修，勿按表象直接改。
- 依赖 AI agent 忠实执行提示词中的补救步骤是脆弱防线；脚本层默认非破坏才是根本解。
- 重生成 per-tool 副本可靠流程：先用确定性变换验证能从 HEAD 精确复现当前副本，再从已编辑源重生成并 diff。
- `gitignore_add_pattern` 定义在外部库 cws-lib-bash 中，不在 common.sh——按调用点定位符号前先确认真实来源。
- 改名备份机制时同步清理文档占位符（`<DATE>` 残留措辞）；改动后做"残留旧措辞"全量扫描。
- 悬空引用修复：feedback 记 1 处实扫出 2 处，第二处更严重（虚构运行结果）；改指真实存在的 `.specify/teams/draw-plantuml-optimizer.team.md` 并删除编造声明。
- skill 必须自包含、不得引用仓库 `docs/`（安装后项目无 docs/）；Resources 章节勿声明不存在的目录（幽灵资源）。
- 大改后用临时 worktree 在 HEAD 建基线比对（95 failed 与工作树完全一致 ⇒ 零回归）。
- symlink 验证法：改 live `.specify/instructions.md` 后 grep 经 symlink 的 `CLAUDE.md` 即时传播——本身就是回归检查。
- per-tool 命令副本必须用生成器（`src/specify_cli/__init__.py:771` `generate_commands`）重生成，勿手改。

## 3. 未完成 / 待办

- `97ba056`/`93f240a`（cefe2c64）与 `03d5aad`（2a38dcaf）等多个 commit 未 push 远端。
- 暂存区遗留 `.specify/runs/draw-plantuml-optimizer/**`（约 30 文件）按新规应属被忽略的 `.specify/teams/.work/`，移出索引待用户确认。
- 7d64ad76 三处编辑（canonical 模板 + 镜像 + live）未提交；git-workflow 三模式技能未实跑演练（Setup/Maintain/Execute 各一次）。
- generate-instructions.sh 系另一作业的未提交改动曾遗留工作区。

## 4. 关键交互流程

- 三处同步顺序（7d64ad76）：canonical `templates/instructions-template.md` → `diff -q` 验证镜像 → 改 live `.specify/instructions.md` → grep 验证 symlink 传播。
- 依赖移除流程（217c6503）：全形态引用排查（env/import/命令调用/模板示例）→ 区分函数真实来源 → 改 canonical + 镜像 + docs + 模板 + 生成副本 → 全项目残留 grep 终验。
- 悬空引用流（2a38dcaf）：核实报告 → 全仓扫同类 → 改指真实产物 → 镜像同步校验。
- 结构重构流：全量探索 → plan mode 请用户拍板设计点 → 逐任务实施 + 每步镜像双写 → 生成器重生成 5+1 份副本并 diff → 验证 → 路径限定提交。

## 5. 用户 ↔ 模型的冲突/分歧点

- instructions 刷新语义（cefe2c64）：用户主张重跑目的是对整文档"逻辑刷新"，流程完整执行、基底换成已存在文件、刷新逻辑从"添加"改为"修改"；模型原本提议旧段落默认不动的纯保守追加；最终按用户方案。
- 依赖移除范围（217c6503）：用户主张移除前重点验证 Python 侧 import 与 shell 调用、范围扩到 pyproject.toml；模型原本仅凭 common.sh 分析即判"可安全移除"；最终全项目搜索确认零引用。
- symlink 文档范围（7d64ad76）：用户主张 Instruction 或 Constitution 等通用文件都要说明；模型勘察后缩小到仅 Instruction 层（Constitution 模板中立性）；最终经确认仅改 Instruction 层。
- team 产物结构（2a38dcaf）：用户将模型的两层方案细化为四层并要求团队目录化（只保留 Report）；模型原方案不动持久化结构；最终升级为扁平→目录化持久化迁移。用户首轮选 `.runs/`，模型指出与跟踪 `runs/` 命名冲突，最终 `.work/`。
- 案例文档前提（2a38dcaf）：用户主张案例文档"已在 skill 中"可直接重指；模型核实前提不成立（文档不存在、无结果数据）；最终最小修复 + 如实标注"结果待实际执行后累积"。
