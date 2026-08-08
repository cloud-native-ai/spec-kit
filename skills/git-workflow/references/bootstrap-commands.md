# Bootstrap 调谐命令序列

Phase 0（旧文档迁移）与 Phase 1（分支检测、创建、`.gitexcludes` 初始化）的完整命令序列。SKILL.md 保留步骤骨架与交互决策逻辑，此处承载操作细节。

## 旧位置文档迁移

本技能的输出文档已从旧位置 `docs/git-workflow.md` 迁移到 `.specify/memory/git-workflow.md`。执行任何模式前，若检测到旧位置仍有文件而新位置尚不存在，先迁移：

```bash
if [ -f "${SKILL_WORKDIR}/docs/git-workflow.md" ] && [ ! -f "${SKILL_WORKDIR}/.specify/memory/git-workflow.md" ]; then
  mkdir -p "${SKILL_WORKDIR}/.specify/memory"
  git mv "${SKILL_WORKDIR}/docs/git-workflow.md" "${SKILL_WORKDIR}/.specify/memory/git-workflow.md" 2>/dev/null \
    || mv "${SKILL_WORKDIR}/docs/git-workflow.md" "${SKILL_WORKDIR}/.specify/memory/git-workflow.md"
  echo "migrated git-workflow.md -> .specify/memory/"
fi
```

若归口 instructions 文档的 Documentation Map 仍引用旧路径 `docs/git-workflow.md`，同时将其更新为 `.specify/memory/git-workflow.md`。

## 分支检测

```bash
git branch -a --format='%(refname:short)'
```

## 创建缺失分支

若用户确认需要新建某个层级分支：

```bash
git checkout -b <PRE> origin/<MAIN>
git push -u origin <PRE>

git checkout -b <DEV> origin/<PRE>
git push -u origin <DEV>
```

## 初始化 .gitexcludes

`.gitexcludes` 机制详见 [gitexcludes-subroutine.md](./gitexcludes-subroutine.md) 的设计原则。此处仅列出初始化命令。

询问用户：每个分支是否有「仅属于本分支、不应同步到其他分支」的目录或文件。示例提问：「是否有某些目录/文件只属于特定分支？例如 `.github/`、`.claude/`、`.vscode/` 只保留在开发分支，不同步到主干？」

`.gitexcludes` 机制说明：

- 项目根目录的 `.gitexcludes` 文件定义**本分支专属文件**，语法与 `.gitignore` 完全一致。
- 每个分支各自维护自己的 `.gitexcludes`，内容可以不同。
- 无论向哪个分支同步代码（rebase 或 merge），目标分支的 `.gitexcludes` 匹配的文件/目录都会被保护，不被源分支覆盖。
- `.gitexcludes` 文件本身也隐含被排除（不会被其他分支的版本覆盖）。

若用户提供排除列表，为各分支创建对应的 `.gitexcludes`：

```bash
# 示例：在开发分支创建 .gitexcludes（DEV 分支通常不需要排除，因为它接收所有代码）
git checkout <DEV>
echo '# DEV branch: no exclusions (receives all code)' > .gitexcludes
git add .gitexcludes && git commit -m "chore: init .gitexcludes for DEV"

# 在 MAIN 分支创建 .gitexcludes
git checkout <MAIN>
cat > .gitexcludes << 'EOF'
# Files exclusive to dev branches, not synced to main
.github/
.claude/
.vscode/
.qoder/
EOF
git add .gitexcludes && git commit -m "chore: init .gitexcludes for MAIN"

# 在 PRE 分支创建 .gitexcludes（根据需要配置）
git checkout <PRE>
cat > .gitexcludes << 'EOF'
# Files exclusive to dev branches, not synced to pre-release
.vscode/
EOF
git add .gitexcludes && git commit -m "chore: init .gitexcludes for PRE"
```

若用户不需要排除规则，创建空 `.gitexcludes` 文件（留备后续使用）。

## 更新 instructions 文档

在归口 instructions 文档的 Documentation Map 中添加引用行：

```markdown
| **Git Workflow** | `.specify/memory/git-workflow.md` | 分支同步机制与操作文件 | 三层分支模型、rebase 同步流程、推送策略、安全底线、.gitexcludes 机制 |
```

目标文档查找优先级：见 [instructions-lookup.md](./instructions-lookup.md)。
