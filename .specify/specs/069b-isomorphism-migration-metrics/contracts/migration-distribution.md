# Contract: 迁移兼容与分发（Migration Compatibility & Distribution）

**Feature**: 069b（父 069） | **File scope**: 全局约束（无单一文件） | **FR served**: FR-006、FR-007、FR-008；SC-002

- **C-1** 未刷新项目行为不变

未刷新的既有项目 MUST 维持原有行为：命令副本仍是旧版（无任何新动作调用）、技能仍是旧版、
`.specify/shared/` 无本次新增章节、`.specify/scripts/` 无新动作。本切片 MUST NOT 在任何命令模板或技能中
新增对 `check` / `delegation` / `faces` / `isomorphism` 的调用——新增动作的执行面**只有**框架源仓的测试与人工核验，
因此未刷新项目**没有新调用点**。未刷新项目也不得因框架升级而在本地产生新的读取、缓存或校验。

（FR-006）

- **C-2** 刷新后原子到位

刷新（`specify init` 的覆盖式合并复制；框架无独立 refresh 子命令）MUST 一次带来四类载荷：分类所有者（含映射与边界章节）、门禁 owner（069a 已交付，本切片不改）、
引擎（`scripts/python/flow-class-check.py` 新动作）、命令副本（内容不变，因为本切片不改模板）。
四类载荷 MUST 出自**同一个发行包**；「有新引擎但没有新 owner」与「有新 owner 但没有新引擎」
都不是受支持的状态，出现时按 `owner-unavailable` 降级（`lookup`）或 `framework-source-required`（框架源动作）显式报出。

（FR-006、FR-008）

- **C-3** 新增动作不是调用点

`check` / `delegation` / `faces` / `isomorphism` MUST NOT 被登记为任何命令模板或技能的调用点：
`shared/workflow/expression-gates.md` § 调用点表 MUST 保持不变（四个既有调用点 W1–W4）；
`templates/commands/**` 与 `skills/**` MUST 零改动。若将来要把它们接入某个流程，必须先修订门禁 owner 与调用点表——
属后续特性，MUST NOT 由本切片就地扩面。

（FR-006、FR-008）

- **C-4** 零项目侧存储与零项目侧读取点

本切片 MUST NOT 在客户项目新增任何存储路径、数据文件、缓存、索引或注册表；MUST NOT 新增读取项目侧数据的代码路径。
项目自建流程按默认类运行；项目若在自己的知识空间（其自身文档系统）记录类别，框架 MUST NOT 读取、MUST NOT 因此改变门禁。
`--action lookup` 是唯一面向客户运行时的读取入口，其行为与 069a 一致（含 `source: default` + 固定标记、
`owner-unavailable` 与标记互斥）。

（FR-008）

- **C-5** 分发路径实测（不新增机制）

四类载荷 MUST 走既有路径，实测依据（2026-10-24/25）：

| 载荷 | 源 | 客户落点 | 实测证据 |
|------|----|----------|----------|
| 分类所有者 + 门禁 owner | `shared/` | `.specify/shared/` | `pyproject.toml` 第 37 行 `"shared" = "specify_cli/shared"`；`src/specify_cli/__init__.py` 第 2462 行起的 shared 复制段（`shared_dest = project_path / ".specify" / "shared"`） |
| 引擎 | `scripts/` | `.specify/scripts/` | `pyproject.toml` 第 34 行 `"scripts" = "specify_cli/scripts"` |
| 技能（本切片不改） | `skills/external`、`skills/internal` | `.specify/skills/` | `src/hatch_build.py` 的 `_stage_skills` 阶段拷贝 |
| 命令副本（本切片不改） | `templates/commands/` | 每工具副本 | `generate_commands()` 由模板生成；本切片零模板改动 |

刷新与验证使用的发行包 MUST 由本切片源码构建（wheel）；机器上预装的旧 `specify` 不作为刷新入口——2026-10-25 实测其包内
`specify_cli/shared/definitions/` 不含 `flow-class-definitions.md`、`specify_cli/shared/workflow/` 不含 `expression-gates.md`。
构建后 MUST 先断言包内四类载荷在场，再用于刷新。
MUST NOT 通过手写 `.specify/` 副本分发；`.specify/` 侧 MUST 与源同字节（`sync-mirrors.py` 投影）。

（FR-008）

- **C-6** 三个客户项目快照（事先冻结）

SC-002 的样本 MUST 在跑测前落盘到 `notes/migration-samples.md`，逐项记录：项目路径、`git rev-parse HEAD`、
分支、工作树脏文件数、是否已有 069a 载荷、套件命令、跑测前提。
样本 MUST 满足：未刷新（无 069a owner/引擎）、有可执行的套件入口、可从提交直接复现。
当前冻结的三个样本见该文件；样本变更 MUST 以新的一条 dated 记录追加，MUST NOT 事后回选。

（FR-007；SC-002）

- **C-7** 名字级基线比对

新增失败 MUST 以**失败 nodeid 集合**比对：刷新前与刷新后各跑一次套件，并按该套件的原生失败输出采集 nodeid 名集
（pytest 取 `FAILED <nodeid>`；Go 取 `go test -json` 的 fail 事件 `<package>::<Test>`；框架仓自身的 `run-tests.sh --names-out`
只是框架仓基线通道，不是客户套件的通道），`comm -13 <before> <after>` MUST 为空。MUST NOT 用失败条数比对（条数相同可以掩盖「修好一个、弄坏一个」）。
套件命令 MUST 原样取自 `notes/migration-samples.md`；比对 MUST 使用同一台机器、同一个解释器、同一组环境变量。

（FR-007；SC-002）

- **C-8** 快照刷新程序与降级

快照 MUST 用 `git archive <HEAD> | tar -x -C <tmp>` 建立**临时副本**；原始项目与工作树 MUST NOT 被修改。
刷新 MUST 在临时副本内由发行包安装入口执行（`specify init . --here --force --ai <tool> --no-git --ignore-agent-tools`，
或等价的安装器入口），并在刷新前后各跑一次套件。该发行包 MUST 由本切片源码构建（C-5），MUST NOT 使用预装的旧 CLI。
若套件因缺少未跟踪文件（`.env`、本地缓存等）而无法启动，MUST 记 `not-evaluated` + reason，
MUST NOT 记 0 新增失败；若 `specify init` 在本机不可执行，MUST 同样记 `not-evaluated`，MUST NOT 以人工 `cp` / 逐文件复制冒充刷新。
临时副本 MUST 在记录证据后清理（可复建）。

（FR-006、FR-007；SC-002）

- **C-9** 框架仓基线不替代客户快照

069a 的 `notes/test-baseline-contract.txt` / 069b 的 `notes/test-baseline-contract.txt` 是**框架仓**契约套件的基线，
MUST NOT 被当作 SC-002 的客户项目基线；两者对象不同，不得互相顶替。

（FR-007；SC-002）

- **C-10** 镜像与命令副本判据

本切片触碰的镜像对只有两对：`shared/definitions/flow-class-definitions.md` → `.specify/shared/definitions/flow-class-definitions.md`，
`scripts/python/flow-class-check.py` → `.specify/scripts/python/flow-class-check.py`。判据是「**零新增差异**」：
`python3 scripts/python/sync-mirrors.py --check` 在编辑前实测六对全绿 + 命令副本 `OK`（exit 0），
编辑后 MUST 重新投影并复跑 `--check`，MUST NOT 出现新的不一致。
命令副本 MUST 保持零改动（本切片不改 `templates/commands/`）；`regen-command-copies.py --check` MUST 继续 `OK`。

（FR-008）

- **C-11** 零新命令与零新门禁面

本切片 MUST NOT 新增 `/speckit.*` 命令（`templates/commands/` 文件集不变），
MUST NOT 新增门禁面（六面封闭集不变），MUST NOT 改阶段集合、门禁数量或 P0/P1 定义。

（FR-006、FR-008）
