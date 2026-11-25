---
id: "20261019T063816Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "sdd-loop-driver-watch-20261019T063708Z"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
disposition: "ignored"
partial: false
created: "2026-10-19T06:38:16Z"
summary: "统一监听模型落地（目标 skill: sdd-loop-driver）：长轮询窗口替代固定 cadence 空等；完成判定改为正证据（退出记录/哨兵/PID/心跳）；修复 pgrep -c 零匹配加 || echo 0 造成 clarify 已完成却误判超时的缺陷；新增 watch-target.sh（16 项自测 + 端到端 mock 验证）。"
disposition_reason: "introspection-20261021T133447Z: excluded (no actionable framework finding)"
---

## Review
统一监听模型落地（目标 skill: sdd-loop-driver）：长轮询窗口替代固定 cadence 空等；完成判定改为正证据（退出记录/哨兵/PID/心跳）；修复 pgrep -c 零匹配加 || echo 0 造成 clarify 已完成却误判超时的缺陷；新增 watch-target.sh（16 项自测 + 端到端 mock 验证）。

## Optimization Points
- 窗口到期只返回 RUNNING，只有阶段 deadline 产生 TIMEOUT；不再用 pgrep 零匹配推断完成。
- 存活判定优先 PID 文件 + kill -0（含 start ticks/PID 复用与僵尸检查），pgrep 仅作布尔兜底。
- 心跳绑定 runner PID 生命周期，避免孤儿心跳伪造存活；runner 原子写 exit/sentinel 状态。
- 多线 manifest 一次连接批量监听，任一线终止即返回全部快照。
- 宿主原生监视器仅作唤醒补充；未证明可自动恢复同一运行时不得结束驱动者会话。
