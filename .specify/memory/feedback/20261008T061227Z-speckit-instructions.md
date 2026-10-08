---
id: "20261008T061227Z-speckit-instructions"
unit_id: "/speckit.instructions"
unit_type: "command"
run_id: "instructions:20261008-converge"
scope: "local"
probe: "speckit-instructions-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-08T06:12:27Z"
summary: "R1+map-not-manual 收敛 1191 B(32768 预算下余 1871,恰好容下 S3 未落地的 1752 B 小节);ID Register 规则+登记册+三词条落地并提交。一条机制面发现如下。"
---

## Review
R1+map-not-manual 收敛 1191 B(32768 预算下余 1871,恰好容下 S3 未落地的 1752 B 小节);ID Register 规则+登记册+三词条落地并提交。一条机制面发现如下。

## Optimization Points
- 1. 全量 A/B 与并行会话落地的竞态:本轮 7 个新红中 6 个是 A/B 运行窗口(115s)恰逢并行会话写入 todo-in-context 文件集所致 —— 镜像一致性/脚本奇偶类测试在半写文件上必红;复跑即绿。在有多会话并行的仓里,A/B 的新红归因 MUST 先做静止性核查(文件 mtime + 失败测试定向复跑),否则会把并行会话的在制状态误归因为自己的回归,或反向漏掉真红(本轮第 7 个红即是并行落地的真缺陷:shipped 面 client-neutrality 违例,属对方,已上报未代修)
