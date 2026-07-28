# 05 · 文档、依赖与项目治理

> 覆盖会话:`f265adf7`(命令文档 + 引用方向重构)、`40cdddea`(上游同步价值分析)、`217c6503`(移除 cws-lib-python 依赖)、`eac5d261` 的衍生部分(team goal 概念 + sdd-workflow 重构评估)。

## A. 命令文档与引用方向(f265adf7)

- 在 `docs/commands/` 为 15 个 `/speckit.*` 命令各写一份详细说明(使用场景、语法、执行流程、产出、前置、后续)。
- 把 `docs/usage.md` 内容合并进 `docs/quickstart.md`,`usage.md` 改为 redirect stub。
- **关键治理决策(用户纠正)**:引用方向必须是 **`README.md` → `docs/quickstart.md` → `docs/commands/*.md`**,不能反向(quickstart 引用 README)。把 README 详细内容尽量下沉到 `docs/`,README 只留精简入口 + 链接(190 行 → 90 行)。
  - `用户主张 README 引用 docs、内容下沉到 docs;模型原本 让 quickstart 反向引用 README#command-reference;最终 统一为 README→docs 单向,消除反向引用`。
- 注意:docs 中仍保留的对 README.md 的提及,是"命令执行时会读/更新 README"的上下文描述(运行时交互),不是文档引用,属正确。

## B. 上游 main 分支同步价值分析(40cdddea)

分析上游 `main` 近 3 个月(2026-03-18→06-18,250+ commits,v0.3.2→v0.11.1),判断哪些值得同步到自己的 master。

- **最终结论:整批不同步。** 判断标尺:**是否契合本项目定位(文档/prompt 框架)vs 上游方向(多 agent 运行时平台)**。方向不匹配则不同步。
- **Integration 插件化架构 → 不同步**:虽是架构级基础(OOP 插件化替代硬编码 if/else,支持 30+ agent),但用户不需要广泛多 agent 适配。
- **Workflow Engine(YAML 流程编排)→ 不同步**:用户手动逐步使用,不需要自动化 spec→plan→implement。
- **安全修复 → 最终也不同步**:路径遍历、URL 重定向降级、URL scheme 验证、catalog payload 验证等**都围绕远程下载/catalog 安装路径**,用户版本不用这些远程功能,故不适用。**安全修复并非无条件同步——若不用对应功能则不适用**。
- **Bug 修复 → 不同步**:多绑定 workflow/Copilot integration/Windows 场景。

### 用户 ↔ 模型的冲突/分歧点
- `用户主张 Integration 架构对自定义版无意义;模型原本 列为"最高优先级、后续所有功能的基础"强烈建议同步;最终 接受用户判断`。
- `用户主张 整批没有有价值 patch;模型原本 建议安全修复"全部同步"、部分 Bug"强烈建议同步";最终 认同(不用远程功能则安全修复不适用,方向不匹配)`。

### 可复用经验
- 大批量 commits 分析法:先按"高价值核心/安全/Bug/新集成/Breaking Changes/可忽略"分类,再逐类深入。
- **Breaking Changes 备忘**(v0.10.0):移除 `--ai`/`--ai-commands-dir`/`--ai-skills`;git extension 改 opt-in、移除 `--no-git`;`--ai` 废弃改 `--integration`。
- **通用坑**:`yaml.safe_dump()` 默认 `allow_unicode=False` 会把中文转成 `\uXXXX`,处理中文 YAML frontmatter 需显式 `allow_unicode=True`。

## C. 移除 cws-lib-python 依赖(217c6503)

- **诉求**:检查项目对 `cws-lib-python` 的依赖,`common.sh` 的 `CWS_LIB_PYTHON_HOME` 检查能否去除。
- **关键发现**:该依赖**完全空载**——`common.sh` source 了 `cws_py_env` 但从未调用其任何函数;真正被用的 `git_repo_root`/`git_current_branch`/`has_git` 来自 `cws_bash_env`(`CWS_LIB_BASH_HOME`,不同的库)。而 `check_dependency` 里对 `CWS_LIB_PYTHON_HOME` 的**强制检查反而是障碍**,会让没装该库的用户无法运行任何脚本。
- **最终彻底移除**:改两份 `common.sh`(`scripts/bash/` + `.specify/scripts/bash/`)删条件 source 和强制检查;`docs/overview.md` 去引用;`templates/commands/implement.md` + 3 个生成副本移除示例中的 `cws_py_cmd`。全项目零残留。
- 经验:清理"空载依赖"要分两步确认——①无 Python `import cws*`;②无 shell `cws_py_cmd` 调用。二者皆空才能安全移除。

## D. team goal 概念 & sdd-workflow 重构评估(eac5d261 衍生)

draw-plantuml 优化会话尾部衍生出的治理讨论:

- **为 `/speckit.team` 引入 goal 一等概念**:改 `templates/commands/team.md` 新增 `### Goal` 段(北极星/可验证/区别 description/可改不漂移),create"goal 先行"、modify"redefine goal 为一等编辑并 realign 结构"、run"Restate the Goal"步,持久化加 `goal` frontmatter + `## Goal` 段。
  - `用户主张 goal 应能对已存在 team 修改;模型原本 定为"Invariant 不变式";最终 "可改不漂移"(运行期稳定,modify 可重定义并级联 realign)`。
  - **传播缺口(未完成)**:仅改了 team.md;`create-team`/`improve-team` skill、`026-agent-team-management/data-model.md`、`docs/commands/team.md` 镜像均未同步(goal 与 description 仍混淆)。
- **sdd-workflow 重构评估**:该"技能"自称 "NOT invoked directly",本质是**不可调用的共享参考/去重层**(让各 `/speckit.*` 通过 `${SKILL_HOME}/references/<file>.md` 引用公共协议),不应待在 `skills/`(污染 skill 注册表、有误调用风险)。
  - 倾向用户方案:`share/workflow → .specify/share/workflow`(与 source→.specify 模式一致),建议命名改 `.specify/shared/` 或 `.specify/references/`。放弃:①保持现状(误调用风险)②并入 memory(memory 是演进知识非静态协议)③并入 templates(模板≠协议,只是换个命名谎言)。
  - **未实施**:待用户拍板走 `/speckit.feature` 流程还是机械改写,以及最终命名。~100 处 `sdd-workflow` 引用需改写,以 `grep -rn sdd-workflow` 零命中作为验收门。
  - git 史澄清:sdd-workflow 于 2026-07-10 `0207fdf`(commit 标题误为 "fix gitignore")首次加入,次日 `09ea0bf` 精修。
  - **条件删除 `docs/summary/01` 文档被拒**:两个删除条件(无人引用 ∧ 内容已覆盖)均不成立(被 README+goal.md 引用、含唯一实战细节),按"与"关系不删。→ 这是 [[feedback_no-dfx-overdesign]] 之外的另一处"用户设了删除条件、模型核查后按条件不执行"的谨慎范例。

> 注:这部分是当前分支 `028-sdd-workflow-refactor` 的直接前置背景。

## 可复用经验汇总

- 判断"是否采纳/同步/保留"的核心标尺是**契合本项目定位**(文档/prompt 框架,非运行时平台)——见 [[feedback_no-dfx-overdesign]]。
- 文档引用方向应单向收敛(README→docs→细分),避免循环引用。
- 移除依赖/删除文件前,先核查引用与覆盖条件是否**真的**成立,条件为"与"关系时任一不成立即不执行。

---

**相关**:[[00-cross-cutting-lessons]] · [[04-draw-plantuml-optimization]] · [[feedback_no-dfx-overdesign]]
