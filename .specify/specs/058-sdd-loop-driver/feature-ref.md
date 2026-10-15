# Feature Reference: Feature 058 无人值守 SDD 循环驱动机制

**Requirement → Feature**: `058-sdd-loop-driver` → Feature 058（Planned；plan 阶段 2026-10-15 推进）
**Spec**: `.specify/specs/058-sdd-loop-driver/requirements.md`（25 FR / 9 SC / 6 US，clarify 残留 0）
**Feature Registry**: `.specify/memory/features.md` 行 058 + `.specify/memory/features/058.md`

## 绑定与归属

- 本 spec 绑定**现有 Feature 058**（编号 1:1 对应；clarify Session 2026-10-15 Q1 裁定）。绑定先例启发式核验：039（P10 Loop Card 无派发与校验面、P12 单命令进程内长跑）、042（访谈模式，人在环）、046（门控治理）、050（主动建议）、052（异常分流纪律）均无本能力归属——确认为新 Feature 而非绑定既有，注册于 requirements 阶段先行落册（用户指令）。
- Better-Harness 定位（Principle XIII）：本特性强化 **Controlled Execution**（阶段化派发 + 独立校验 + 卡死处置）与 **Reliable Delivery**（状态脊 + 收尾纪律 + 确认门控继承）；Learning Capture 由既有运行判定机制承接（运行期线状态即其输入面，不新增机制）。

## FR → 契约条款映射（25 FR 全覆盖；条款编号 = tasks 阶段重编号后交付序）

| FR | 条款 | FR | 条款 |
|----|------|----|------|
| FR-001（skill 唯一承载+可移植） | C-1, C-11, C-12 | FR-013（合并收尾+git 状态判定） | C-5 |
| FR-002（五类内容内联） | C-3, C-4, C-10 | FR-014（收尾汇总） | C-4（收尾纪律）, data-model E-8 |
| FR-003（参数化零硬编码） | C-4, C-10（形态级）, V-6 | FR-015/FR-016（独立校验） | C-10（校验程序内联）, B-2 |
| FR-004（一遍性入口不变） | C-1（description 触发词）, B-1 | FR-017/FR-018/FR-019（卡死/状态脊） | C-9, C-10 |
| FR-005（断点续跑默认） | C-4, B-1 | FR-020（多线并行） | B-3 |
| FR-006（终态文档消费） | C-4, B-1 | FR-021（并发隔离+窄读法授权） | B-3 |
| FR-007（heredoc prompt 文件） | C-4, C-10 | FR-022/FR-023（变体参数化） | C-10 |
| FR-008（三段骨架+G5+回传契约） | C-7, C-8, C-10 | FR-024（注册面+docs 同步） | C-12, C-13, C-14…C-19 |
| FR-009（尾标必要条件） | C-5 | FR-025（投递形态无关） | C-11, C-14③, C-21 |
| FR-010（runner 派生） | C-4 | FR-011（后台轮询+契约观测） | C-4, C-6 |
| FR-012（自迭代） | B-2 | | |

未覆盖 FR：0。B 类条款（B-1…B-4）与 C-20…C-22 行为类条款为执行期行为，显式不进测试钉死。**重编号披露**：tasks 阶段按条款语法真源（id MUST 为 `C-<数字>`）与交付顺序整体重编号（旧 C-5→C-10、C-6→C-7、C-7→C-9、C-8→C-5、C-9→C-6、C-10→C-11、C-11→C-12、C-12→C-13、C-13→C-8；D-1…D-9→C-14…C-22），映射表已按新号落定。

## SC → 度量来源映射（9 SC）

| SC | 度量来源 | 载体 |
|----|----------|------|
| SC-001 零提醒 | 演练会话记录 + 循环日志介入统计 | Quickstart S3/S4（C-22） |
| SC-002 断点正确率 | 注入断点清单 ↔ 判定记录（E-6）比对 | S4 |
| SC-003 伪完成拒绝率 | 变异演练（破坏产物→校验转红→复原→转绿） | C-10 程序 + S4 |
| SC-004 卡死处置闭环 | 异常注入计时/产物核对 | S4 |
| SC-005 双拓扑等价 | 两拓扑各一轮闭环记录 | S3（本地）/ S4（远端） |
| SC-006 纪律合规 | git 审计（脏文件/远程操作） | S3/S4 |
| SC-007 多线零串扰 | 逐线日志与提交归属核对 | S4（双线） |
| SC-008 零改动实例化 | 机制文件 diff 审计 + 新项目演练 | S3 变体 |
| SC-009 执行侧可移植 | 宿主无 .specify 前置探测留痕 + 闭环记录 | S3 前置探测（C-21） |

## 规格要点速览（实现期必读）

- G1 修订（2026-10-15）：skill **唯一承载**，零 team/preset 面；执行侧宿主 agent 不安装 spec-kit；仅目标项目需要 `.specify/`。
- 合并收尾 = **git 状态判定**（无 MERGE-DONE 哨兵）；阶段哨兵 `<STAGE>-DONE`（[[STR-001]]）仅必要条件，独立校验为充分条件。
- 上送件四要素、禁止缓冲至退出式派发、G5 纪律行、派发注入回传契约：**内联进 skill**（执行侧不解析框架路径），契约测试钉死字面量（宪章 XIV Partial 的缓解）。
- 镜像方向：框架源 `skills/external/sdd-loop-driver/` 为 canonical，`.specify/skills/` 仅投影；触碰对既有 2 条无关 DIFF（git-workspace），判据取无 NEW drift（Quickstart S1 实测基线）。
- 测试必经 `scripts/bash/run-tests.sh`（裸 python3 无 pytest，实测）；`test_run_skills_wiring.py` 当前 12 passed，roster 更新后仍应 12 passed。
