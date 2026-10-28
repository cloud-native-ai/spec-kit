# sdd-house-keeping（SDD 项目管家）

**机制一句话**：对已初始化的目标项目执行周期性维护——确定性盘点（H1）、按缺口或 owner 自检漂移调协（H2）、按需强化（H3）、验证（H4）并报告（H5）；记录消费回收通过目标项目的 `/speckit.sanitize` retention lane 完成。真源：`skills/external/sdd-house-keeping/SKILL.md`（+ `references/maintenance-recipes.md`、`scripts/`）。

## 三段循环

```text
sdd-project-setup   S0–S2 + HANDOFF   bootstrap
sdd-house-keeping   H0–H5             周期维护（本页）
sdd-loop-driver     U0–U6             SDD 开发阶段循环
```

## 何时加载

用户说「项目管家」「house keeping」「定期维护」「清理并核对目标项目」「记录回收」「retention cleanup」；或 `sdd-project-setup` 完成 bootstrap 后 handoff。全新项目安装仍走 `sdd-project-setup`，SDD 开发阶段推进仍走 `sdd-loop-driver`。

## 入口参数

| 参数 | 解析 |
|------|------|
| 目标项目 | 遵循 `shared/workflow/target-resolution.md`：**强依赖 `.specify/`**，从显式路径/会话 cwd **向上搜索**最近的合法 `.specify/` 根；找不到 → 拒绝执行并提示 `sdd-project-setup`/`specify init` |
| 模式 | 未给 → `check`（只扫描/报告）；用户明确要求清理 → `cleanup` |
| 命令面 | 不假设 `/speckit.*` 副本存在；缺失时按 `.specify/skills/internal/<name>/SKILL.md` 加载 owner 技能 |

目标项目缺 `.specify/` 或 constitution → 停止并 handoff `sdd-project-setup`。

## H0–H5

```text
H0 ENTRY     目标/模式/命令面解析
H1 ASSESS    mechanism-inventory.py + logical-framework.py 双盘点（只读）
H2 RECONCILE 执行 H1 缺口 OR owner 自检漂移：
             sanitize（materials + retention）→ feature → instructions → docs
H3 STRENGTHEN history → docs 深化 → research → feature 生成
H4 VERIFY    五族前置检查（本地仅④⑤）+ 双矩阵复扫 + 符号链接 + hook health
H5 REPORT    候选工作清单 + 运行报告（宿主工作目录 YAML）
```

**触发口径**：H1 只回答“资产在不在”；sanitize 残留、feature 注册表漂移、instructions 预算/过期、docs 漂移由各自 owner 判定。H2 执行 **H1 缺口 OR owner 自检报告的漂移**，每项登记 `executed / existing / skipped + reason`，未处理项进入 H5 清单。

## 记录回收（retention lane）

- `check` 模式：同时跑 `/speckit.sanitize check`（materials）与 `/speckit.sanitize --lane retention check`，两份摘要一起报告，不删除。
- `cleanup` 模式：跑 `/speckit.sanitize --lane all`；一个调用内呈现 materials 与 retention 两个计划，破坏性确认仍由 sanitize 既有门处理，**不新增第二道门**。
- 本 skill **不直接调用** `sanitize-utils.py apply` 或 `record-retention.py apply`。
- 旧框架缺 `record-retention.py`：只跑 materials lane，报告 `retention=not_evaluated`，不删除；缺 `sanitize-utils.py`：回交 setup。
- 没有 retention receipt 不删除；open feedback、unsettled run-determination、不可解析 exec-quant、无 promotion/ephemeral 决策的 session 笔记永不回收；默认宽限 30 天；目标路径 git 脏时拒绝 apply。

## 软协同

- **sdd-project-setup**：一次性 bootstrap（init/refresh + constitution + 首次 feature/docs/goal/agents/team）；bootstrap 完成后 handoff 给本 skill。若 H1 发现 goal/agents/team bootstrap-gap，回交 setup。
- **sdd-loop-driver**：SDD 开发阶段循环；本 skill 不推进任何阶段，只做治理、维护、强化与报告。候选清单是建议，不携带「必须调用 sdd-loop-driver」的语义。
- **sanitize/docs/history/feature/instructions**：各自 owner 的流程不被重写；本 skill 只决定何时、按什么次序、以什么模式调用。
- **候选清单**：本 skill H5 是唯一所有者；setup 不再产出 `sdd-candidates-*.yaml`。

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/mechanism-inventory.py` | 物理机制盘点（只读） |
| `scripts/logical-framework.py` | 逻辑框架盘点（只读） |
| `scripts/hook-health.py` | 宿主 hook 体检（`--fix` 仅在 cleanup 模式） |

`mechanism-inventory.py` 与 `logical-framework.py` 与 `sdd-project-setup` 的副本保持字节一致（provenance 三行除外），以保证本 skill 独立可运行。

## 边界

- 不安装/不 init/不 bootstrap constitution；不做 SDD 阶段推进。
- 不新增调度器/守护进程；周期由用户或宿主循环触发。
- 不自动上送数据；不评估用户源码/产品脚本/测试。
- 不在目标项目创建 ad-hoc 目录；不借用 `.specify/state/`。
- 运行报告只落宿主工作目录 `sdd-housekeeping-<project-slug>-<UTC-ts>.yaml`。
