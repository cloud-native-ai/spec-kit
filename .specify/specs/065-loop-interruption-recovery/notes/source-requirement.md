# SDD 简报 — spec-kit spec 065 / Feature 065：SDD 循环中断感知与恢复

## 用户目标（原话）
需要在 spec-kit 项目中针对**流程中断**的情况进行修复，最基本的是能够做到**状态感知**和**状态恢复**。

## 问题实证（2026-10-21，xuanji-doc 线 015）
- plan 阶段派发后，驱动者未在同一回合启动 watcher（驱动侧空档）；Mac 休眠导致挂起；实际写盘发生在 15:30–16:04，早越过 90 分钟 deadline，但因无 watcher 未产生 TIMEOUT 判定。
- 16:04:51 qodercli 以 exit=1 退出（无哨兵；plan/data-model/contracts/quickstart/research/feature-ref 产物齐全但未提交）。
- 结果：循环静默停摆约 13 小时；状态脊未写 stalled/reentry-required；恢复只能靠人工逐一检查 pid/status/log/heartbeat/产物与 git 提交。

## 现有机制（需复用，勿重造）
- `skills/external/sdd-loop-driver/references/watch-model.md`：四类信号（哨兵/退出记录/PID+start ticks/心跳）、判定状态机（ANOMALY/FAILED/INCOMPLETE/DEAD/TIMEOUT/NO_SIGNAL/DONE/RUNNING）、窗口 vs deadline、`--once` 重入快照。
- `references/stage-prompts.md`：状态脊字段与“先写后动”、stalled/reentry-required、重入程序。
- `scripts/watch-target.sh`（只读监听）、`scripts/line-registry.py`（线路/租约/orphan 检查）、`scripts/stage-runner.sh`、`scripts/run-stage.sh`、`scripts/hook-stop.sh`/`watch-hook.sh`。
- 现状缺口：**没有面向驱动者的统一“状态感知”入口**（把状态脊 + 四件套 + git/产物聚合成一个可读判定），**没有自动化“状态恢复”程序**（区分已完成/伪完成/中断，决定续派/重试/停线，并在驱动者退出时落 stalled）。

## 建议特性范围（requirements 裁决）
1. **状态感知（state awareness）**：新增/扩展确定性脚本入口（例如 `loop-state.py` 或扩展现有 line-registry/status 动作），只读聚合：状态脊、pid/status/log/heartbeat、spec 产物、git 提交，输出结构化判定（RUNNING/DONE/INCOMPLETE/FAILED/DEAD/TIMEOUT/NO_SIGNAL/STALLED）与证据指针；可被驱动者在每个窗口开始/重入时调用。
2. **中断检测**：识别“已派发但无 watcher / 进程已死无退出记录 / deadline 已过仍在跑 / 心跳停跳”等中断形态，并给出应写状态脊的 stalled/reentry-required 建议。
3. **状态恢复（state recovery）**：提供续跑程序——按状态脊+判定决定 `resume / retry / stop`；resume 时只补缺失产物与提交，不重派已完成阶段；retry 时清理旧 status/信号避免污染（本次实测过旧 status 导致误判）；stop 时生成上送件四要素。
4. **驱动者生命周期约束落地**：SKILL.md 明确“派发与监听同一回合启动”、“驱动者退出前必须落 stalled/reentry-required”；可加确定性检查脚本对状态脊做校验。
5. 约束：不改变 `watch-target.sh` 判定语义（watch-model 是 owner）；不改各 `/speckit.*` 命令内部流程；兼容已有四件套与 line-registry；测试需覆盖失败/中断/重入矩阵（含“旧 status 污染”“产物齐但无哨兵”“进程死无退出记录”）。

## 编号锚点
- 规格编号：**065**；特性 ID：**065**；建议短名：`loop-interruption-recovery`
- 源 skill 位置：`skills/external/sdd-loop-driver/`（框架源；镜像义务按仓库规范）

## 驱动纪律
- 本特性改进对象是 sdd-loop-driver 本身，仍走完整 SDD 阶段链（非技能维护路径）。
- 工作树当前干净；如有他线改动需隔离。
