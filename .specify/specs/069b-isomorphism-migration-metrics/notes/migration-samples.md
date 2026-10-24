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
# 2) 刷新前：跑套件并按其原生失败输出采集失败 nodeid 名集（pytest `FAILED <nodeid>` / Go `go test -json` 的 fail 事件）
cd ~/tmp/069b-snap-1 && <suite command> | tee ~/tmp/069b-before.log
# 3) 刷新：在临时副本内由安装器入口执行（见下方 2026-10-25 更正第 4 条）
# 4) 刷新后：同一命令再采一次 after（同样提取失败 nodeid 名集）
comm -13 before.txt after.txt   # MUST be empty
# 5) 清理：记录证据后删除临时副本（可复建）
```

## 记录规则

- 名字级比对 MUST 用失败 nodeid 集合（`comm -13`），MUST NOT 用失败条数（C-7）。
- 工作树脏改动**被排除**是设计选择（快照必须可复现），不是遗漏。
- 套件无法启动（缺 `.env` 等未跟踪文件）或 `specify init` 在本机不可执行时，MUST 记 `not-evaluated` + reason（C-8），
  MUST NOT 记 0 新增失败、MUST NOT 以手工拷贝冒充刷新。
- 样本变更 MUST 追加一条新的 dated 记录，MUST NOT 覆盖本表。

## 2026-10-25 跑测机制更正（不改变上面的样本冻结值）

上面的冻结表仍是权威样本；本节只更正「如何在快照里真跑」，因为快照机制与套件通道有三处实测偏差
（依据：`git archive HEAD | tar -x -C ~/tmp/069b-probe-snap-1` 后逐项探测）：

1. **快照不含 `.venv`**：`xuanji-agent` 与 `xuanji-function` 的 `.gitignore` 都把 `.venv/` 排除，
   `git archive` 不携带它，故冻结表「跑测前提」列的 `.venv/bin/python` 只在原项目存在，不在快照里。
   套件 MUST 用原项目的**绝对解释器路径**（只读使用，不修改原项目），cwd = 快照根；例：
   `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-agent/.venv/bin/python -m pytest tests/ -q`。
2. **editable 安装会把源码指向原项目**：`xuanji-agent` 的 venv 带
   `__editable__.xuanji_agent-0.1.0.pth` → `/Users/.../xuanji-agent/src`（实测）。不设 `PYTHONPATH` 时，
   快照里的测试实际导入**原工作树（含 195 个脏改动）**的源码，快照隔离失效。因此 `xuanji-agent` 的套件
   MUST 加 `PYTHONPATH=<snapshot>/src`（实测导入路径从原项目切到快照：
   `~/tmp/069b-probe-snap-1/src/xuanji_agent/__init__.py`），并实测 `tests/test_adapter_contract.py` 4 passed in 2.23s。
   `xuanji-function` 的 `tests/conftest.py` 以 `__file__` 推导并插入快照的 `src/`，无需 `PYTHONPATH`。
   `xuanji-cli` 是 Go 模块，cwd = 快照根即可。
3. **客户套件没有 `--names-out`**：该 flag 属框架仓的 `scripts/bash/run-tests.sh`，不在客户项目里。
   失败名集 MUST 按套件原生输出提取——pytest：`-q --tb=no -rf` 的 `FAILED <nodeid>` 行；
   Go：`go test ./... -json` 的 `Action=fail` 事件，nodeid 记为 `<package>::<Test>`。提取命令与产物路径
   写进 `notes/quickstart-run.md` 场景 6。
4. **刷新必须用本切片源码构建的 wheel，不能用预装 CLI**：实测 `/Users/liuqiming.lqm/project/profiles/.venv/bin/specify`
   的包内 `specify_cli/shared/definitions/` 无 `flow-class-definitions.md`、`specify_cli/shared/workflow/` 无
   `expression-gates.md`（连 069a 载荷都不在），用它刷新等于没刷新。可行程序（本机实测）：
   `python3 -m pip wheel . --no-deps -w ~/tmp/069b-wheel --trusted-host yum.tbsite.net`
   （构建需 hatchling；本机可从内网 PyPI 取到 1.32.4）→
   `python3 -m pip install --target ~/tmp/069b-pkg --no-deps --upgrade ~/tmp/069b-wheel/specify_cli-*.whl`
   → 断言 `~/tmp/069b-pkg/specify_cli/shared/definitions/flow-class-definitions.md` 与
   `~/tmp/069b-pkg/specify_cli/scripts/python/flow-class-check.py` 在场 →
   在快照根执行 `PYTHONPATH=~/tmp/069b-pkg /Users/liuqiming.lqm/project/profiles/.venv/bin/specify init . --here --force --ai <该项目既有 AI 工具> --no-git --ignore-agent-tools`
   （`--target` 目录优先于 profiles venv 里的旧 `specify_cli`；profiles venv 提供 httpx / typer / rich 等运行时依赖；
   `--force` 跳过非空目录确认，`--ai` 避免交互式选择）。wheel 构建 / 安装 / init 不可执行时按 C-8 记
   `not-evaluated` + reason，MUST NOT 用人工 `cp` / 逐文件复制冒充刷新。
