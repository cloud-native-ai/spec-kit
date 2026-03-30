# Quickstart: Validate Qoder Support

## Prerequisites

- 工作区位于仓库根目录。
- 已完成本 feature 的实现任务。
- 若要验证正常 CLI 检查路径，本机已安装 `qoder`；若验证失败路径，则确保 `qoder` 不在 `PATH` 中。

## Scenario 1: New project initialization with Qoder

1. 在临时目录运行 `specify init demo-qoder --ai qoder`。
2. 确认生成结果包含：
   - `.qoder/commands/`
   - `.qoder/project_rules.md`（或实现约定中的等价说明文件）
   - `.specify/` 基础结构
3. 确认命令帮助或生成说明中将 Qoder 视为正式支持助手。

**Expected Result**:
- 初始化成功。
- 用户无需手工复制 Qoder 文件。
- 其他已支持助手行为未回归。

## Scenario 2: Existing-directory initialization with Qoder

1. 在已有文件的目录中运行 `specify init . --ai qoder --ignore-agent-tools`。
2. 选择继续合并现有内容。
3. 检查目录中新增 Qoder 资产，但已有非 Qoder 文件保持原样。

**Expected Result**:
- Qoder 资产被补齐。
- 其他助手目录与用户原有文件未被无关覆盖。

## Scenario 3: Missing Qoder CLI failure path

1. 确保 `qoder` CLI 不可用。
2. 运行 `specify init demo-qoder --ai qoder`。

**Expected Result**:
- 命令失败并明确指出缺少 `qoder`。
- 错误信息提供安装链接与下一步指引。
- 错误信息提示可使用 `--ignore-agent-tools`。

## Scenario 4: Skip validation with existing ignore behavior

1. 在 `qoder` CLI 不可用时运行 `specify init demo-qoder --ai qoder --ignore-agent-tools`。
2. 检查初始化是否继续完成。

**Expected Result**:
- CLI 检查被跳过。
- 生成的 Qoder 资产仍然完整。

## Scenario 5: Refresh instructions and support surfaces

1. 在已初始化项目中执行说明刷新流程（按项目既有方式触发 `generate-instructions.sh` 或对应命令）。
2. 检查以下支持面：
   - `README.md`
   - `docs/installation.md`
   - `.ai/instructions.md`
   - `templates/plan-template.md`
   - `templates/commands/agents.md`
3. 确认 Qoder 名称、安装地址与支持状态一致。

**Expected Result**:
- 所有支持面均列出 Qoder。
- 不再存在“脚本生成了 `.qoder/`，但治理/文档不承认”的漂移。

## Scenario 6: Release/package audit

1. 运行标准打包或发布准备流程。
2. 检查生成资源是否包含 Qoder 所需模板与命令资产。
3. 对照合同文件核验分发清单。

**Expected Result**:
- 所有应包含 CLI 助手变体的发布物都覆盖 Qoder。
- 审计结果可支持 SC-004 与 FR-007。