# Quickstart: Skill Install Layout

## Purpose

验证“项目级 skills 主副本统一到 `.specify/skills/`，并通过工具兼容入口暴露”的新布局在安装、迁移、冲突和降级场景下行为正确。

## Prerequisites

- 当前分支：`007-skill-install-layout`
- 已存在可用于安装的样例 skill（可通过 `/speckit.skills` 创建）
- 工作区具备读写权限
- 若要验证降级路径，可在不支持软链接或禁用软链接能力的环境执行

## Validation Scenarios

### Scenario 1: 新安装写入主副本目录（P1）

1. 执行一次项目级 skill 安装流程。
2. 检查主目录是否创建在 `.specify/skills/<skill-name>/`。
3. 检查 skill 内容完整且可被后续刷新识别。

**Expected Result**: 主副本仅出现在 `.specify/skills/`，不直接落在 `.github/skills/` 或其他工具目录。

### Scenario 2: GitHub 兼容入口创建（P2）

1. 在启用 GitHub 兼容入口的项目中安装同一 skill。
2. 检查 `.github/skills/<skill-name>` 是否创建为兼容入口。
3. 验证入口目标指向 `.specify/skills/<skill-name>/`。

**Expected Result**: `.github/skills/<skill-name>` 不是独立副本；其访问被路由到主副本。

### Scenario 3: 软链接不可用时占位降级（P2）

1. 在不可创建软链接的环境执行安装。
2. 检查工具入口是否创建占位目录与指引文件。
3. 检查输出是否报告“入口需人工处理”。

**Expected Result**: 主副本安装成功；兼容入口不复制主内容；结果为可观察的 `partial-success`。

### Scenario 4: 旧布局迁移 + 备份后删除（P3）

1. 预置旧版真实目录 `.github/skills/<skill-name>/`（非软链接）。
2. 执行新流程安装或刷新。
3. 检查是否先生成备份，再删除旧目录，并保留主副本和兼容入口。

**Expected Result**: 迁移完成后仅保留 `.specify/skills/<skill-name>/` 作为主副本，旧真实目录被安全收敛。

### Scenario 5: 备份失败时禁止删除旧目录（P3）

1. 预置可触发备份失败的环境（如备份目录无写权限）。
2. 触发旧布局迁移。
3. 检查旧目录删除步骤是否被跳过。

**Expected Result**: 主副本可用但迁移标记为“需人工处理”；旧目录保留且有明确后续指引。

### Scenario 6: 入口冲突阻断覆盖（Edge）

1. 在目标兼容入口路径预置普通文件或普通目录。
2. 执行安装或刷新。
3. 检查系统是否停止自动覆盖并返回冲突详情。

**Expected Result**: 发生 `conflict-entry-path` 错误；无静默覆盖行为。

### Scenario 7: 重复安装幂等（Edge）

1. 对同一 skill 连续执行两次安装/刷新。
2. 检查主副本与入口数量和指向关系。

**Expected Result**: 结果收敛且无重复偏离副本；第二次执行输出 `reused` 或等价幂等状态。

## Regression Expectations

## Automated Coverage Mapping

- Scenario 1, Scenario 7 → `tests/contracts/test_skill_install_layout_contract.py`, `tests/integration/test_skill_install_layout_integration.py`
- Scenario 2, Scenario 3 → `tests/contracts/test_skill_install_layout_contract.py`, `tests/integration/test_skill_install_layout_integration.py`
- Scenario 4, Scenario 5, Scenario 6 → `tests/contracts/test_skill_install_layout_contract.py`, `tests/integration/test_skill_install_layout_integration.py`
- 状态枚举与路径识别基础能力 → `tests/unit/test_skills_utils_layout.py`

- 现有 `/speckit.skills` 的创建与刷新体验保持可用
- 旧项目不会因新布局导致 skill 内容丢失
- 仅在正式支持工具范围内创建兼容入口
- 输出结果始终报告主副本、入口状态、失败原因与迁移摘要
