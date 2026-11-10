# Red-First Evidence — 097 /speckit.migrate 一次性迁移收尾命令

红先取证纪律（tasks.md § Tests / owner `.specify/skills/internal/implement-feature/SKILL.md` § TDD 与 § Test runs）：每条新测试先在被测行为实现前运行，并记录**命令、真实输出、退出码**。本文件 append-only，按任务行（T-row）分节追加，先红后续绿。

**落点所有者**: `.specify/specs/097-speckit-migrate-command/tasks.md` § Path Conventions（运行时证据落点固定：本文件 + `notes/quickstart-run.md` + `notes/pre-change-measurements.md` + `test-evidence/` + `coverage-baseline.txt`）。

- canonical runner（唯一测试入口）: `bash scripts/bash/run-tests.sh <targets> -q`
- 多测试文件整行 run 时允许 `-q` 尾随；单测调试同样经 runner 转发
- 迁移/回归例外（tasks.md § Tests）: 本特性无「移植既有行为」的测试行，全部测试行为新，无 `[blockedBy:]` 后置的迁移型测试
- template-only gate（tasks.md § Tests）: `templates/commands/migrate.md` 与其四个副本的断言是结构契约测试，仍按红先纪律执行

## 记录骨架（每条红一行，逐条追加）

---
### § <T-row> — `<test-file>`（red-first）

- 日期: `<YYYY-MM-DD>`
- 命令: `bash scripts/bash/run-tests.sh <targets> -q`
- 退出码: `<n>`
- 真实输出（尾部/决定性节选，逐字粘贴）:

```text
<verbatim output>
```

- 红判据: <该失败为何证明被测行为尚不存在（而非断言自身缺陷）>

---
（以下由后续包逐行追加；本包 T001–T004 无 `[green:]` 声明行，故无红先条目。）
