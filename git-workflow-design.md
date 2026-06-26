



Git **无法直接在分支合并过程中自动忽略特定文件或目录**（如 `.github`、`.vscode`），因为 Git 的合并操作会**完整同步所有已跟踪文件**。但通过**主干分支预清理 + 自定义合并策略 + CI 自动化拦截**，可以实现“开发分支保留配置文件，主干分支自动过滤”的效果。核心逻辑是：**主干分支必须提前确保目标文件未被跟踪**，后续合并时才能通过规则跳过这些文件。

---

## 一、核心原理与前提条件
### 1. **关键限制**
- `.gitignore` **仅对未跟踪文件生效**，若文件已被提交到开发分支，则合并时仍会传播到主干分支。
- **必须先从主干分支彻底移除目标文件**（包括 Git 历史记录），后续合并才能通过规则跳过这些文件。

### 2. **必要前提**
- **主干分支（如 `main`）必须已清理目标文件**：  
  确保主干分支的 Git 历史中**从未跟踪过**需排除的文件（例如 `.github`、`.vscode`）。若历史中存在这些文件，需先按[彻底移除流程](#二-主干分支预清理目标文件)处理。

---

## 二、主干分支预清理目标文件
若主干分支历史中存在需排除的文件（如 `.vscode`），必须**一次性彻底移除**：
### 1. **从 Git 历史中删除文件**
```bash
# 1. 切换到主干分支（确保本地与远程一致）
git checkout main
git pull origin main

# 2. 从所有历史提交中删除目标目录（示例：.vscode）
git filter-repo --force --invert-paths \
  --path-glob '.vscode/**' \
  --path-glob '.github/**'

# 3. 提交变更并强制推送到远程（谨慎操作！）
git push origin main --force
```
> **注意**：`git filter-repo` 会重写历史，**团队成员需重新克隆仓库**。仅限私有仓库或团队协调后操作。

### 2. **添加 `.gitignore` 规则（可选但推荐）**
在主干分支的 `.gitignore` 中明确声明忽略规则，防止未来误提交：
```gitignore
# 主干分支的 .gitignore
.vscode/
.github/
```
提交此变更到主干分支，确保后续合并时规则生效。

---

## 三、自动化合并过滤方案
### 1. **开发分支配置**
#### （1）保留文件但添加 `.gitignore` 规则
在开发分支中保留 `.vscode` 等文件，但确保 `.gitignore` 包含以下规则（避免误提交新文件）：
```gitignore
# 开发分支的 .gitignore
.vscode/
.github/
```
#### （2）定义分支专属合并策略
在项目根目录创建 `.gitattributes` 文件，**仅对开发分支有效**：
```gitattributes
# 开发分支的 .gitattributes
.vscode/** merge=ours
.github/** merge=ours
```
- **作用**：当从开发分支合并到主干时，Git 会自动跳过这些文件的冲突检测，**保留主干分支的现有状态**（即忽略开发分支的修改）。

### 2. **CI/CD 自动化拦截（关键步骤）**
在 PR 合并到主干前，通过 CI 脚本**强制移除目标文件**（即使 `.gitattributes` 未覆盖所有场景）：
#### 示例：GitHub Actions 工作流（`.github/workflows/pr-filter.yml`）
```yaml
name: Filter Files on Merge
on:
  pull_request:
    branches: [main]  # 监控合并到 main 的 PR

jobs:
  filter-files:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}  # 检出 PR 分支

      - name: Remove excluded files
        run: |
          # 自定义需排除的路径（支持通配符）
          EXCLUDED_PATHS=".vscode/ .github/"
          for path in $EXCLUDED_PATHS; do
            git rm -r --cached $path 2>/dev/null || true
          done
          git commit -m "chore: auto-remove excluded files" --allow-empty

      - name: Push filtered changes
        run: |
          git push "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git" HEAD:${{ github.head_ref }}
```
#### **关键逻辑**：
1. **PR 创建时触发**：自动从 PR 分支中**移除目标文件**（`git rm --cached` 仅取消跟踪，保留本地文件）。
2. **强制提交过滤结果**：将清理后的代码推回 PR 分支，确保合并到主干时**不包含目标文件**。
3. **完全自动化**：开发者无需手动操作，CI 会拦截所有 PR。

---

## 四、验证与维护
### 1. **验证流程**
- **本地测试**：  
  执行 `git merge dev-branch --strategy-option=ours`，检查 `.vscode` 等文件是否未被合并。
- **PR 检查**：  
  在 GitHub PR 的 **Files changed** 标签页中，确认目标文件**不在变更列表中**。

### 2. **长期维护建议**
- **自定义排除列表**：  
  修改 CI 脚本中的 `EXCLUDED_PATHS` 变量即可动态调整规则（如新增 `docs/temp/`）。
- **团队协作规范**：  
  - 所有成员需理解：**主干分支永远不应包含开发配置文件**。
  - 在仓库 `CONTRIBUTING.md` 中声明规则，避免误操作。

---

## 五、为什么这是最佳实践？
1. **严格满足需求**：  
   - **自定义排除**：通过 `EXCLUDED_PATHS` 和 `.gitattributes` 灵活定义规则。
   - **完全自动化**：CI 脚本拦截所有 PR，无需人工干预。
2. **安全可靠**：  
   - 避免重写历史（仅主干预清理需谨慎操作）。
   - **不依赖 `.gitignore` 的局限性**，直接操作 Git 索引层。
3. **开源社区验证**：  
   Kubernetes、VS Code 等项目均采用 **CI 过滤 + 主干预清理** 模式管理分支专属文件。

> **重要提醒**：若主干分支历史中**从未存在过目标文件**，可跳过预清理步骤，直接配置 CI 过滤脚本。但**首次合并前必须确保主干分支的 `.gitignore` 已包含排除规则**，否则新文件会被意外提交。

