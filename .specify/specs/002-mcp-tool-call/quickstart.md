# Quickstart: MCP Tool Call Command

**Branch**: 002-mcp-tool-call | **Date**: 2026-02-10

## Goal

验证 `/speckit.mcpcall` 的基本流程：自动发现、交互补全、记录复用与调用输出。

## Scenarios

1. **首次调用新工具**
   - 选择一个未记录的 MCP 工具。
   - 完成 MCP Server、描述、参数与返回值的补全。
   - 生成 `.specify/memory/tools/<mcp tool name>.md` 并成功调用。

2. **复用已有记录**
   - 对已存在记录的工具再次调用。
   - 跳过发现与补全步骤，直接执行并返回结果。

3. **记录缺失字段**
   - 人为移除记录中的必填字段。
   - 再次调用时触发补全提示并完成更新。

## Expected Results

- 工具记录完整且可复用。
- 调用结果包含可核验的成功或错误信息。
