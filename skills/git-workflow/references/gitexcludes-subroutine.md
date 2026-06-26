# .gitexcludes 通用排除子程序

所有同步/合并操作均自动调用此子程序。**目标分支**的 `.gitexcludes` 决定哪些文件被保护。

## 设计原则

- **谁接收代码（目标分支），谁的 `.gitexcludes` 说了算。**
- 方向无关——无论 MAIN→DEV 还是 DEV→MAIN，目标分支的专属文件始终受保护。
- `.gitexcludes` 文件本身隐含被保护，不会被其他分支版本覆盖。
- `.gitexcludes` 语法与 `.gitignore` 完全一致（支持 glob 模式、注释行 `#`、否定模式 `!`）。

## 前置（sync 前）

切换到目标分支后，读取其 `.gitexcludes` 并记录被保护文件的当前状态：

```bash
if [ -f .gitexcludes ]; then
  # 解析 .gitexcludes 并列出匹配的已跟踪文件
  EXCLUDED_FILES=$(while IFS= read -r pattern; do
    [[ "$pattern" =~ ^[[:space:]]*#.*$ || -z "${pattern// }" ]] && continue
    [[ "$pattern" == '!'* ]] && continue
    git ls-files -- "$pattern" 2>/dev/null
  done < .gitexcludes)

  # 清理可能残留的旧标签（防止上次异常中断后指向错误 commit）
  git tag -d _gitexcludes_pre_sync 2>/dev/null || true
  # 保存当前状态（创建临时标签）
  git tag _gitexcludes_pre_sync HEAD
fi
```

## 后置（sync 后）

同步操作完成后，恢复被保护文件到同步前的状态，并移除不应存在的新引入文件：

```bash
if git rev-parse _gitexcludes_pre_sync >/dev/null 2>&1; then
  if [ -f .gitexcludes ]; then
    while IFS= read -r pattern; do
      [[ "$pattern" =~ ^[[:space:]]*#.*$ || -z "${pattern// }" ]] && continue
      [[ "$pattern" == '!'* ]] && continue
      # 恢复 tag 中存在的文件到旧状态
      git checkout _gitexcludes_pre_sync -- "$pattern" 2>/dev/null || true
      # 移除 tag 中不存在但被 sync 引入的新文件（排除路径中的新增）
      git ls-files -- "$pattern" 2>/dev/null | while IFS= read -r f; do
        git show _gitexcludes_pre_sync:"$f" >/dev/null 2>&1 || git rm --cached "$f" 2>/dev/null || true
      done
    done < .gitexcludes
  fi

  # 始终恢复 .gitexcludes 文件本身
  git checkout _gitexcludes_pre_sync -- .gitexcludes 2>/dev/null || true

  # 若有变更则提交
  git diff --cached --quiet || git commit -m "chore: restore branch-exclusive files after sync"

  # 清理临时标签
  git tag -d _gitexcludes_pre_sync
fi
```

## 使用方式

在每个同步/合并操作中：

1. 切换到目标分支后执行**前置**
2. 执行 rebase 或 merge
3. 执行**后置**

## 示例：完整操作序列

```bash
# 同步 MAIN → PRE 的完整流程
git checkout <PRE>

# ── 前置 ──
git tag -d _gitexcludes_pre_sync 2>/dev/null || true
git tag _gitexcludes_pre_sync HEAD

# ── 同步 ──
git pull --rebase origin <PRE>
git rebase origin/<MAIN>

# ── 后置 ──
if [ -f .gitexcludes ]; then
  while IFS= read -r pattern; do
    [[ "$pattern" =~ ^[[:space:]]*#.*$ || -z "${pattern// }" ]] && continue
    [[ "$pattern" == '!'* ]] && continue
    git checkout _gitexcludes_pre_sync -- "$pattern" 2>/dev/null || true
    # 移除 sync 引入的新文件
    git ls-files -- "$pattern" 2>/dev/null | while IFS= read -r f; do
      git show _gitexcludes_pre_sync:"$f" >/dev/null 2>&1 || git rm --cached "$f" 2>/dev/null || true
    done
  done < .gitexcludes
  git checkout _gitexcludes_pre_sync -- .gitexcludes 2>/dev/null || true
  git diff --cached --quiet || git commit -m "chore: restore branch-exclusive files after sync"
fi
git tag -d _gitexcludes_pre_sync 2>/dev/null || true
```

## 注意事项

- 临时标签 `_gitexcludes_pre_sync` 仅存在于操作过程中，完成后立即清理。
- 若 rebase 产生冲突，需先解决冲突再执行后置。
- 否定模式 `!` 当前被跳过（简化处理），未来可按需扩展。
- `git ls-files -- "$pattern"` 使用 pathspec 匹配，对目录级 pattern（如 `.github/`）会匹配其下所有文件。
