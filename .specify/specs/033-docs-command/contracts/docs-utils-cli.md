# Contract: docs-utils.py 引擎 CLI（scripts/python/docs-utils.py）

确定性引擎脚本契约（FR-006d/FR-007 确定性维度）。标准库-only；stdout 输出单个 JSON 对象；镜像 `.specify/scripts/python/docs-utils.py` 字节一致。字面量以 requirements.md Shared Strings 为准。

## 调用形态

```bash
python3 scripts/python/docs-utils.py --action <action> [--root <project-root>] [其余 action 特定参数]
```

- **C-1** 参数解析 MUST 为单一 argparse，`--action` 取值集合固定为：`scan | expire | clean | archive-check | stats | validate | audit`。新增动作属契约变更。
- **C-2** `scan` MUST 输出 notes 分组清单 JSON：`{"drafts": [...], "expireds": [...], "archiveds": [...], "invalid": [...]}`；`invalid` 收 frontmatter 缺失/损坏项（含缺失字段名与修复建议，默认 [[STR-004]] = created + 60 天）。
- **C-3** `expire` MUST 将超过 [[STR-004]] 日期的 [[STR-001]] 笔记状态改写为 [[STR-002]]，输出 `{"marked": [...], "count": N}`；MUST NOT 删除任何文件。
- **C-4** `clean` MUST 仅在显式确认参数（`--yes`）存在时删除 status=[[STR-002]] 的笔记，且作用域仅限 notes 区；无 `--yes` 时只输出候选清单（dry-run 默认）。
- **C-5** `archive-check` MUST 校验全部 status=[[STR-003]] 笔记的 `target`：缺失或不存在的输出到 `{"broken": [...]}`。
- **C-6** `stats` MUST 输出 `{"total": N, "drafts": N, "expireds": N, "archiveds": N}`。
- **C-7** `validate` MUST 执行确定性维度校验并输出违规清单：大写保留名合规（FR-010：注册位置外的保留名 → `reserved-name-misplaced`，README 越位建议 `index.md`；大小写变体 → `reserved-name-case`；非注册 ALL-CAPS → `reserved-name-misuse`）、根入口"一屏"尺寸阈值、内部链接可达性（代码块/行内代码中的示例链接与 notes 区豁免）、ADR 编号连续性、frontmatter 完整性；只读不改写。
- **C-8** `audit` MUST 向 `.specify/docs/audit/` 追加一条审计记录（时间戳、作用域、逐项动作、结果），零收敛时记录"全维度在容忍带内"；输出 `{"path": "...", "written": true}`。
- **C-9** 所有动作 exit code：0=成功（含"发现违规但正常报告"）；非 0 仅用于脚本自身错误（参数/IO）。
- **C-10** 引擎 MUST NOT 触碰 feedback 引擎与其存储（零新增循环机器红线，FR-009/FR-011e；由既有 test_dogfooding_practice C-4 类钉点保障）。
- **C-11** quickstart.md 中出现的每个 docs-utils.py 示例命令 MUST 与本契约的 action/参数语法一致（实现阶段以真实执行回验）。
