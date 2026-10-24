# Migration Samples — 069b（SC-002 的 3 个客户项目快照，事先冻结）

**Frozen**: 2026-10-25 · **Criterion contract**: `contracts/migration-distribution.md` C-6 / C-7 / C-8
**用途**: SC-002 的样本在本文件冻结后才允许跑测（requirements SA-12）。事后回选会把「零回归」变成选样结果。
**刷新前状态**: 三个样本均**未刷新**——`.specify/shared/definitions/flow-class-definitions.md` 与
`.specify/scripts/python/flow-class-check.py` 都不存在（实测 `test -f`），即 069a 的载荷尚未到达。

| # | 项目 | 路径 | HEAD | 分支 | 工作树脏文件 | 069a 载荷 | 套件命令 | 跑测前提 |
|---|------|------|------|------|--------------|-----------|----------|----------|
| 1 | xuanji-agent | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-agent` | `3f68b62` | `master` | 195 | 无 | `.venv/bin/python -m pytest tests/ -q` | `.venv/bin/python` 存在（实测）；套件不依赖未跟踪文件 |
| 2 | xuanji-cli | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-cli` | `a0c476d` | `xuanji/develop` | 548 | 无 | `go test ./...` | `go1.27.2` 在 PATH（实测）；模块缓存可用 |
| 3 | xuanji-function | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-function` | `a2fad18` | `main` | 28 | 无 | `.venv/bin/python -m pytest -q` | `.venv/bin/python` 与 `pytest.ini` 存在（实测） |

## 快照与刷新程序（不修改原始项目）

```bash
# 1) 快照：只读导出该提交的树，工作树脏改动不参与
mkdir -p ~/tmp/069b-snap-1 && git -C <project> archive <HEAD> | tar -x -C ~/tmp/069b-snap-1
# 2) 刷新前：跑套件并采集失败名字集
cd ~/tmp/069b-snap-1 && <suite command> ... --names-out before.txt   # 具体形式按套件落地
# 3) 刷新：在临时副本内执行（specify init 或同一发行包的载荷复制）
# 4) 刷新后：同一命令再采一次 after.txt
comm -13 before.txt after.txt   # MUST be empty
# 5) 清理：记录证据后删除临时副本（可复建）
```

## 记录规则

- 名字级比对 MUST 用失败 nodeid 集合（`comm -13`），MUST NOT 用失败条数（C-7）。
- 工作树脏改动**被排除**是设计选择（快照必须可复现），不是遗漏。
- 套件无法启动（缺 `.env` 等未跟踪文件）或 `specify init` 在本机不可执行时，MUST 记 `not-evaluated` + reason（C-8），
  MUST NOT 记 0 新增失败、MUST NOT 以手工拷贝冒充刷新。
- 样本变更 MUST 追加一条新的 dated 记录，MUST NOT 覆盖本表。
