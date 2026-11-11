# Parked — /speckit.migrate（旧版 specify 项目 → 新版预期状态的收尾迁移）

**寄存时间**: 2026-11-10 · **来源**: 用户在 095 运行期间的口述需求 · **状态**: parked（095 收束后立项）

## 需求原文要点

- 创建一个 `speckit.migrate` 命令，用来将旧版本的 specify 项目向新版 specify 改造。
- 当前 `specify init` 命令中已包含一部分 migrate 逻辑；需要再包装一个 migrate 命令做**最终收尾**。
- 用户项目中的执行流程：
  1. 执行 `specify install`（在 python 环境中安装 speckit 新版本）；
  2. 执行 `specify init` 把基础设施安装到项目中（如 `.specify` 目录结构）；
  3. 第二步完成后，`.specify` 可能是**新旧版本混杂**的状态；通过 `speckit.migrate` 命令把混杂状态清理为**最新版本的预期状态**。

## 与既有机制的关系（立项时必须复用，不新造）

- `/speckit.sanitize` 已有 **Migration wrap-up lane (init 迁移收尾)**（sanitize-materials skill，materials collect 里的 migration-residue 检查）——本命令应作为**用户面向的收尾入口**复用该 lane 的确定性检查与处置，而不是第二套迁移逻辑。
- `129aced18` 的 `anchor-layout-migrate.py`（check/apply，anchor 布局收敛）是 anchor 维度的迁移引擎；migrate 命令应把它纳入 lane 编排。
- `src/specify_cli/__init__.py` 里 `init` 的分支逻辑（`migrate_flat_internal_skills` 等）是「部分 migrate 逻辑」的来源；命令收尾时必须以**新版期望态**为判据（模板/生成物/锚点/布局/兼容链接/镜像），而不是猜测旧版结构。
- 三层契约：期望态 owner（模板与声明）、当前态探测（确定性引擎）、收敛动作（archive-not-delete + 前置确认），与 reconcile 家族一致。

## 处理计划

- 095 收束后：以 new feature 立项（096+，与 sdd-observer 一并排期），走 SDD 链。
- 立项时必须回答：命令的入口形态（`/speckit.migrate` 运行期模板 + `specify migrate` CLI 的关系）、`init` 后混杂态的确定性判定清单、与 sanitize Migration lane 的职责边界（migrate = 一次性收尾；sanitize = 周期性治理）、不可逆动作的确认门、跨版本升级（N→N+k）的渐进路径与 `--dry-run` 默认形态。

## 立项记录（2026-11-10）

- 已作为独立 SDD 线启动（见对应的 096/097/098 状态脊与 U5 上送件）；运行至 analyze 门后按「一轮修复回环」规则停线，处置选项见各线 handoff。
