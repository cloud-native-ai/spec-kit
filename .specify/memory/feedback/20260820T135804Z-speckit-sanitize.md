---
id: "20260820T135804Z-speckit-sanitize"
unit_id: "/speckit.sanitize"
unit_type: "command"
run_id: "sanitize-20260820-full-run"
scope: "local"
probe: "speckit-sanitize-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-08-20T13:58:04Z"
summary: "本次全量运行达成命令声明目的:采集 695 项(确定性 693 死引用 + 1 镜像漂移)、语义候选 1 项经补充取证后判 stale-residue 并入账、批量门控确认后零失败执行 2 项 destructive 清理,台账 pending 682→680、resolved 13→15。判据链完整(证据引用具体 commit/路径),确认红线与范围红线均未越界;主要摩擦在语义证据包信息量不足与"
---

## Review
本次全量运行达成命令声明目的:采集 695 项(确定性 693 死引用 + 1 镜像漂移)、语义候选 1 项经补充取证后判 stale-residue 并入账、批量门控确认后零失败执行 2 项 destructive 清理,台账 pending 682→680、resolved 13→15。判据链完整(证据引用具体 commit/路径),确认红线与范围红线均未越界;主要摩擦在语义证据包信息量不足与 delete 处置对非空目录不可执行两点。

## Optimization Points
- 语义候选 evidencePack 过薄:仅 3 行 gitLog 摘要 + 空 pathExistence,不足以支撑 stale-residue 判定;本次需 3 轮自行取证(UPSTREAM.md 变更表 + platforms 代码 grep)才达置信。建议引擎把候选材料 frontmatter 的 origin 引用与所指能力路径纳入 pathExistence 映射,降低裁决外取证成本
- token-efficiency 首次 collect 输出经 head -200 原文转储约 200 行 pendingTargets 长串(摘要优先纪律违例);二次采集已改为落盘 + Python 投影消费计数,后续运行应在首次即走投影路径
- mirror-drift 发现建议 delete 与引擎 apply 拒绝非空目录的安全设计相冲突,本次依赖披露式变通(agent 清空 58 桩 + 引擎 rmdir 空目录);建议引擎对非空目录目标改生成 archive 处置或在 apply 支持确认后的目录级删除
- .migration-backups 桩目录由 create-new-skill.sh 迁移备份在测试运行中持续再生成(运行期间新增第 58 个),本次清理属治标;根因(产品脚本备份落点)在命令范围外,仅作复发风险如实披露
