# Quickstart: Speckit Tools Command

**Branch**: 004-speckit-tools-command | **Date**: 2026-03-02

## Goal

验证 `/speckit.tools` 的核心流程：多来源工具发现、记录复用/补全、执行前确认、冲突消歧与重命名。

## Scenarios

1. **MCP 工具首次调用**
   - 调用 `/speckit.tools <mcp-tool-name>`，目标记录不存在。
   - 通过交互补全来源、参数、返回信息并生成记录。
   - 执行前展示摘要，用户确认后执行。

2. **非 MCP 工具调用（System/Shell/Project）**
   - 调用 `/speckit.tools <tool-name>` 指向 system binary 或 project script。
   - 生成同样结构的工具记录并完成确认流程。

3. **已有记录复用**
   - 再次调用已记录工具。
   - 跳过发现与补全过程，直接展示摘要并确认执行。

4. **同名冲突消歧**
   - 构造不同来源下同名工具。
   - 调用时系统要求用户明确选择来源后再继续。

5. **封装与重命名**
   - 对已有工具记录执行重命名/别名封装。
   - 再次调用新名称，验证可检索与可复用。

## Expected Results

- 所有工具来源均可映射到统一 ToolRecord 结构。
- 未确认执行不会触发真实调用。
- 冲突场景必须先消歧，消歧前不可执行。
- 记录重命名后仍可稳定检索，并保留来源可追溯性。
