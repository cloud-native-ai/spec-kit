# Contract — Seal Engine（引擎调用面、退出码与写入纪律）

**Feature**: 099-speckit-seal | **Date**: 2026-11-10 | **Plan**: [plan.md](../plan.md)
**Owns**: `scripts/python/seal-utils.py` 的动作封闭集、调用面、退出码语义、两阶段写入与写面边界。

**C-001** — 动作集合恰好六个，且不存在第七个。

引擎的 `--action` 取值封闭为 `merge-plan`、`merge-apply`、`seal`、`archive-gate`、`archive-plan`、
`archive-apply`（后两者由 `100-seal-slice-archive` 原地扩展；本条款仍是动作集的唯一 owner，MUST NOT
在别处出现第二份动作表）。`merge-plan`、`archive-gate` 与 `archive-plan` 是只读动作（零写盘）；
`merge-apply`、`seal` 与 `archive-apply` 是写动作。未声明的动作以退出码 `2` 拒绝并回显动作名。

(FR-021)

**C-002** — 退出码是封闭三值，语义专属本引擎。

`0` = 成功或幂等（含 `merge-plan` 计算成功且无开放冲突、`seal` 成功或 `already-sealed`、`archive-gate`
放行）；`1` = 前置条件拒绝（含 `merge-plan` 计算成功但存在开放冲突——只读输出仍完整给出）；`2` = 输入或
环境错误（不可解析的 spec、状态面矛盾 `state-drift`、写入中途失败）。三个值之外的退出码 MUST NOT 出现。

(FR-009, FR-021)

**C-003** — `--help` / `--version` 零副作用，未声明选项非零拒绝。

复用 `scripts/python/script_interface_cli.py` 的守卫：`-h` / `--help` 在解析前回答且不触碰文件系统；
`--version` 打印一行身份并以 `0` 退出；任何未声明选项（含裸 `--` 之后）以 `2` 拒绝，且 MUST NOT
到达任何动作。`configure_parser` 必须携带 `side-effects:` 与 `exit-codes:` 两个标签。

(FR-021)

**C-004** — 调用面封闭。

已声明选项恰为：`--action`、`--spec-dir`、`--repo`、`--feature-detail`、`--feature-registry`、`--json`、
`-h/--help`、`--version`。`--spec-dir` 是目标 spec 目录（必填，无默认；缺失即 `2`）；`--feature-detail` /
`--feature-registry` 仅用于覆盖状态载体路径（测试夹具），生产调用不传。MUST NOT 增加 `--force`、
`--no-verify`、`--waive` 一类旁路选项。

(FR-021)

**C-005** — 判定与写入两阶段，写入按批次原子。

`seal` MUST 先在只读阶段算齐全部前置条件；只有全部成立才进入写入。写入集 = `seal.md` + 注册表行
（`Status` 与 `Last Updated`）+ 特性详情（`Status` 与 `## Latest Review` 记录），同批落盘。任一写入失败
MUST 以原字节恢复本批已写文件并以 `2` 结束；MUST NOT 留下可被读作半封装的状态。

(FR-009, FR-010)

**C-006** — 拒绝零持久化，报告只走 stdout。

退出 `1` 的拒绝 MUST NOT 创建任何文件（无拒绝记录、无第二份台账、无空 manifest）。报告经 stdout
（及调用方的捕获）呈现，逐条点名**全部**未满足条件——不是只报第一条——每条带修复路径与重跑方式。
同输入重跑 MUST 复现同一清单（顺序稳定）。

(FR-009)

**C-007** — 已封装是幂等成功，不是拒绝。

当状态面一致地显示 `Sealed` 时，`seal` MUST 以 `0` 退出并具名报告 `already-sealed`：不产生第二份
`seal.md`、不重复写状态面、不删除既有回执。并发场景下后到者读到先到者回执即走此路径；引擎 MUST NOT
依赖锁文件（以回执与提交判定）。

(FR-005, FR-010)

**C-008** — 写面封闭且可静态审计。

引擎的写动作封顶为：父 spec 目录内的合并产物与两份记录文件；分片 `requirements.md` 的一行
`**Merged into**` 标注；FR-016 记录过解决方式的出厂文档引用修正；`archive-apply` 的**唯一**移动——
分片目录 → 所属父 spec 的 `slices/<原分片目录名>/`（`git mv` 语义，目的地 MUST 限于该子树），以及父 spec
根的 `archive-manifest.json` 写入（schema owner：`100-seal-slice-archive` 的
`contracts/archive-manifest.contract.md`）。动作表 MUST NOT 含删除、`git push` 或调度循环；移动动作恰为
`archive-apply` 一个，MUST NOT 写或移入 `.specify/archive/`。静态审计以引擎源码中的写路径白名单为准，
审计脚本/测试转红即违反。

(FR-020, FR-024)

**C-009** — 仓库与 spec 目录定位只信显式路径。

引擎 MUST 从显式路径确定仓库根与镜像侧：以自身解析路径中的**字面** `.specify` 组件判定镜像位置
（位于镜像内时拒绝运行写动作——经镜像写会违反 FR-021 的源/镜像逐字节一致，与
`regen-command-copies.py` 同侧），MUST NOT 采用「向上找最近 `.specify`」启发式（该启发式在本仓会自匹配，
见 AGENTS.md § Two Hats 路径陷阱）。`--spec-dir` 指向的目录
必须存在且含 `requirements.md`（分片识别按 FR-011 的目录形状，不按 `^\d{3}-` 前缀）。

(FR-021)

**C-010** — 输出有两种形态，机器形态稳定。

默认人类可读渲染；`--json` 输出单一 JSON 负载（`indent=2, sort_keys=True, ensure_ascii=False`）。
两种形态承载同一判定；MUST NOT 出现仅在人类渲染中给出的判定。声明式期望（退出码、计数、拒绝码）
MUST 与负载一致。

(FR-021)
