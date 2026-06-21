---
name: git-workflow
description: |
  This skill helps users establish and maintain a three-tier Git development workflow (trunk / pre-release / development branches). It dynamically discovers or defines branch names, then creates and maintains a `docs/git-workflow.md` document as the single source of truth. It provides pre-checks, rebase synchronization, conflict resolution, and safe push strategies. Use this when the user mentions ["git workflow", "branch sync", "rebase sync", "分支同步", "git rebase", "force-with-lease", "发布流程", "分支策略", "主干分支", "预发分支", "开发分支", "three-tier git", "git workflow setup", "创建git工作流"]
skill_id: "<SKILL:.specify/skills/git-workflow/SKILL.md>"
---

# git-workflow

## Overview

This skill helps teams establish and maintain a **三层 Git 开发工作流**：

| 角色代号 | 含义 | 说明 |
|----------|------|------|
| **`MAIN`** | 主干分支 | 上游主干，只接收已通过版本验证的代码 |
| **`PRE`** | 预发分支 | 预发发布分支，用于版本集成与环境验证 |
| **`DEV`** | 开发分支 | 本地开发分支，所有新改动先在此开发与自测 |

> **关键**：分支名称因项目而异（如 `master` / `xuanji/prepub` / `xuanji/hanzhi`，或 `main` / `staging` / `dev`）。本技能在执行时**动态确认**实际分支名，将其记录到 `${SKILL_WORKDIR}/docs/git-workflow.md`，后续操作以该文档为准。

核心链路（使用角色代号）：

```
代码同步链路：MAIN -> PRE -> DEV
代码合入链路：MAIN <- PRE <- DEV
```

固定 rebase 关系：

1. `PRE` 基于 `MAIN` rebase。
2. `DEV` 基于 `PRE` rebase。

## Workflow / Instructions

### Phase 0: 确定场景并加载/创建分支配置

#### 0.1 判断场景

检查 `${SKILL_WORKDIR}/docs/git-workflow.md` 是否已存在：

- **文档已存在** → 读取已记录的分支名，进入 Phase A（直接使用已记录配置）。
- **文档不存在** → 进入 Phase B（创建工作流，确定分支名）。

#### Phase A: 成熟项目 — 直接使用已记录配置

从 `docs/git-workflow.md` 的 frontmatter 读取分支映射：

```
MAIN = (文档中记录的主干分支名)
PRE  = (文档中记录的预发分支名)
DEV  = (文档中记录的开发分支名)
```

确认信息无误后，跳转至 **Phase 1: 执行分支同步**。

#### Phase B: 新项目或简单项目 — 逐步建立工作流

**Step B1：检测现有分支**

```bash
git branch -a --format='%(refname:short)'
```

**Step B2：交互式确认分支名**

逐一向用户确认（每次只问一个问题）：

1. **主干分支名 `MAIN`**：
   - 从远端分支中推荐最常见的候选（`main`、`master`），询问用户选择或自定义。
   - 问题示例："检测到远端有 `origin/main` 和 `origin/master`，哪个是您的主干分支？"

2. **预发分支名 `PRE`**：
   - 询问是否存在预发分支，若存在请用户提供名称；若不存在，建议一个命名规范（如 `release`、`prepub`、`staging`）。
   - 问题示例："项目的预发分支叫什么？如果还没有，建议命名为 `staging`。"

3. **开发分支名 `DEV`**：
   - 同上逻辑，推荐命名（如 `dev`、`develop`、`hanzhi`）。

**Step B3：创建缺失分支（如需）**

若用户确认需要新建某个层级分支：

```bash
# 基于 MAIN 创建 PRE
git checkout -b <PRE> origin/<MAIN>
git push -u origin <PRE>

# 基于 PRE 创建 DEV
git checkout -b <DEV> origin/<PRE>
git push -u origin <DEV>
```

**Step B4：生成 `docs/git-workflow.md`**

读取模板 `${SKILL_HOME}/assets/git-workflow-template.md`，替换 `<MAIN>` / `<PRE>` / `<DEV>` 为实际分支名，写入 `${SKILL_WORKDIR}/docs/git-workflow.md`。

### Phase 1: 执行分支同步

> 以下所有命令中，`<MAIN>` / `<PRE>` / `<DEV>` 由 Phase 0 确定的实际分支名替换。

#### Step 1: 前置校验（必须先过）

```bash
git fetch origin
git status --short --branch
git for-each-ref --format='%(refname:short) -> %(upstream:short)' refs/heads/<MAIN> refs/heads/<PRE> refs/heads/<DEV>
```

若工作区不干净：

```bash
# 方式1：推荐，提交本地改动
git add .
git commit -m "chore: save local work before sync"

# 方式2：临时保存（含未跟踪文件）
git stash push -u -m "pre-sync-<date>"
```

> **Gate**：`git status --short` 必须为空，才能进入下一步。

#### Step 2: 同步 `MAIN -> PRE`

```bash
git checkout <PRE>
git pull --rebase origin <PRE>
git rebase origin/<MAIN>
git rev-list --left-right --count origin/<PRE>...<PRE>
```

推送策略：

- **仅 ahead（`0 N`）**：`git push origin <PRE>`
- **ahead + behind（`M N` 且 `M>0, N>0`）**：
  1. 在团队同步窗口执行；
  2. 通知所有基于 `<PRE>` 开发的同学先暂停拉取；
  3. 使用：`git push --force-with-lease origin <PRE>`

#### Step 3: 同步 `PRE -> DEV`

```bash
git checkout <DEV>
git pull --rebase origin <DEV>
git rebase origin/<PRE>
git rev-list --left-right --count origin/<DEV>...<DEV>
```

若出现 `skipped previously applied commit`：

1. 记录 commit id；
2. 继续完成 rebase；
3. 执行差异核对：

```bash
git log --left-right --cherry-pick --oneline origin/<DEV>...<DEV>
```

推送策略与 Step 2 相同：`0 N` 正常 push，`M N` 团队确认后 `git push --force-with-lease origin <DEV>`。

#### Step 4: 恢复临时保存（若使用过 stash）

```bash
git stash list
git stash pop
```

### Phase 2: 开发、提测、发布

1. 新修改只进 `<DEV>`，完成本地验证（至少 `lint + test + build`）。
2. 发起 PR `<DEV> -> <PRE>`，在预发做版本测试。
3. 版本测试通过后，发起 PR `<PRE> -> <MAIN>`。

> 规范链路：`DEV`（开发）→ `PRE`（版本测试）→ `MAIN`（最终合入）

### Phase 3: 冲突与异常处理

**rebase 冲突：**

```bash
git add <冲突文件>
git rebase --continue
```

**放弃本次 rebase：**

```bash
git rebase --abort
```

## Security / 发布分支安全底线

1. `<MAIN>` 禁止直接 push 未审查代码。
2. 禁止跳过 `<PRE>` 直接把 `<DEV>` 合入 `<MAIN>`。
3. 禁止 `git push -f`，仅允许 `git push --force-with-lease`。
4. 对共享分支执行强推前，必须完成"通知 + 同步窗口 + 回滚预案"。

## Known Issues & Mitigations

| 异常现象 | 根因分析 | 应对策略 |
|----------|----------|----------|
| `git checkout` 报错，本地改动会被覆盖 | 工作区不干净 | 执行 Phase 1 Step 1 前置校验后再切换分支 |
| rebase 后变为 `M N`（双向分叉） | 共享分支 rebase 重写提交历史 | 使用 `--force-with-lease` 受控推送，走团队同步窗口 |
| rebase 过程出现 `skipped previously applied commit` | 分支存在重复补丁或历史漂移 | 记录 commit id，继续 rebase，执行 `git log --left-right --cherry-pick` 差异核对 |

## docs/git-workflow.md 文档维护

### 创建

- 在 Phase B 完成后，使用模板 `${SKILL_HOME}/assets/git-workflow-template.md` 生成 `${SKILL_WORKDIR}/docs/git-workflow.md`。
- 文档 frontmatter 记录了三个分支的实际名称，作为后续同步操作的唯一数据源。

### 更新

- 若项目分支改名或重构，更新 `docs/git-workflow.md` frontmatter 中的分支映射，后续操作自动适配。
- 若同步流程有新增经验或异常处理经验，追加到文档的"Known Issues"章节。
- 更新完成后在文档末尾更新 `last_updated` 日期。

### instructions.md 引用

技能执行后，需要在归口 instructions 文档的 Documentation Map 中添加引用行：

```markdown
| **Git Workflow** | `docs/git-workflow.md` | 分支同步机制与操作文件 | 三层分支模型、rebase 同步流程、推送策略、安全底线 |
```

目标 instructions 文档的判断逻辑：

1. 优先检查 `${SKILL_WORKDIR}/.specify/instructions.md` 是否存在。若存在，则更新该文件的 Documentation Map 表格。
2. 若 `.specify/instructions.md` 不存在，则检测当前支持的 AI 工具对应的 instructions 文档，在第一个找到的文件中更新 Documentation Map：

| 工具 | 兼容性 instructions 文件 |
|------|--------------------------|
| GitHub Copilot | `${SKILL_WORKDIR}/.github/copilot-instructions.md` |
| Claude Code | `${SKILL_WORKDIR}/CLAUDE.md` |
| Qwen Code | `${SKILL_WORKDIR}/QWEN.md` |
| Qoder | `${SKILL_WORKDIR}/QODER.md` 或 `${SKILL_WORKDIR}/.qoder/project_rules.md` |
| opencode | `${SKILL_WORKDIR}/AGENTS.md` |

> 若以上文件均不存在，则创建 `${SKILL_WORKDIR}/.specify/instructions.md` 并写入引用行。

## Resource ID

- Canonical ID: `<SKILL:.specify/skills/git-workflow/SKILL.md>`
- Canonical Path: `.specify/skills/git-workflow/SKILL.md`

## Path Conventions

This Skill follows the canonical path conventions:

- Use `${SKILL_HOME}/<relative-path>` for every Skill-owned resource reference (scripts, references, assets).
- Use `${SKILL_WORKDIR}/<relative-path>` for every runtime/user-facing path this Skill reads from or writes to (inputs in the user's project, outputs delivered to the user).
- Never conflate the two; never embed agent-specific install paths.

## Resources

### Scripts (`${SKILL_HOME}/scripts/`)
- No scripts currently.

### References (`${SKILL_HOME}/references/`)
- No references currently.

### Assets (`${SKILL_HOME}/assets/`)
- `git-workflow-template.md` — `docs/git-workflow.md` 的生成模板，包含参数化占位符 `<MAIN>` / `<PRE>` / `<DEV>`。
