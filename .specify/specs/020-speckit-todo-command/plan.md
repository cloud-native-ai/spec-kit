# Implementation Plan: Speckit Todo Command

**Branch**: 020-speckit-todo-command  
**Date**: 2026-06-23  
**Spec**: requirements.md

## Summary

实现 /speckit.todo 双模式命令：
- **Collection**（默认）：扫描 markdown 文件，查找 SPECKIT TODO 块，输出 JSON/人类可读列表
- **Insertion**（--insert）：从 stdin/文件读取 TODO 规范，插入到指定位置

不自动执行 TODO 任务，符合 SDD 安全原则。

## Technical Context

- **Language**: Bash 4.0+ with awk/sed
- **Dependencies**: find, awk, sed, jq（可选）
- **Storage**: 工作空间文件系统
- **Testing**: 30 contract tests + 15 integration tests
- **Platform**: Linux（主要）, macOS（次要）
- **Performance**: 10,000 文件 < 2 秒

## Constitution Check ✅

所有 7 个核心原则通过：
- I. SDD Foundation ✅
- II. Feature-Centric ✅
- III. Intent-Driven ✅
- IV. Test-First ✅
- V. AI Integration ✅
- VI. Quality & Observability ✅
- VII. Spec-Plan-Task-Implementation ✅

## Project Structure

```
.specify/specs/020-speckit-todo-command/
├── plan.md              # 本文件
├── requirements.md      # 已创建
├── data-model.md        # 将创建
├── quickstart.md        # 将创建
├── contracts/todo-markers.md  # 将创建
└── checklists/requirements.md # 已存在

.github/prompts/
└── speckit.todo.prompt.md

.specify/scripts/bash/
├── common-todo.sh       # 已创建
└── search-todo.sh       # 将创建

tests/
├── fixtures/todo-workspaces/  # 5 个 fixtures
├── contract/                  # 30 个测试
└── integration/               # 15 个测试
```

## Collection Mode

1. 解析参数（--json, --workspace）
2. 验证工作空间
3. find 定位 markdown 文件
4. awk 状态机检测 TODO 块
5. 提取内容 + 上下文
6. 验证格式
7. 输出 JSON/文本
8. 退出 0/2

## Insertion Mode

1. 解析 --insert, --file, --todo-file
2. 验证目标文件（退出 1）
3. 验证行号
4. 读取 TODO
5. 格式化
6. sed 插入
7. 确认输出
8. 退出 0

## Exit Codes

- **0**: 成功
- **1**: 硬失败（文件缺失）
- **2**: 软警告（格式错误块）

## Risk Assessment

### High Risk
- 格式错误检测边缘案例
  - 缓解：30 个契约测试

### Medium Risk
- 10,000+ 文件性能
  - 缓解：T066 基准测试

### Low Risk
- 非 UTF8 文件
  - 缓解：is_utf8_file()

## Phase Plan

- ✅ Phase 0: Research（已完成）
- ✅ Phase 1: Design（plan.md 创建中）
- ⏳ Phase 2: Tasks（/speckit.tasks）
- ⏳ Phase 3: Implement（/speckit.implement）
- ⏳ Phase 4: Verify（/speckit.analyze）

## Handoffs

**Before**: requirements → clarify  
**After**: tasks → implement → analyze → review

---

**Status**: 准备 /speckit.tasks
