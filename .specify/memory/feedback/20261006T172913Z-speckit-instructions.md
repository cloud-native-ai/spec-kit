---
id: "20261006T172913Z-speckit-instructions"
unit_id: "/speckit.instructions"
unit_type: "command"
run_id: "speckit-instructions-team-discoverability-20261007"
scope: "local"
probe: "speckit-instructions-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-06T17:29:13Z"
summary: "partial update 运行（用户请求＝同步新建团队的可发现性）。结论为无操作：setup 脚本 exit 0、未改动任何被跟踪文件（live 与新建备份逐字节相同）、20 个节全在容忍带内、尺寸 30944/32768 B 余量 1824 B 未触发收敛、17 个备份的标题集合差只有已被取代的 ## Resource Registry（归因为收敛非丢失）。团队可发现性经三处依据判定为无需登"
---

## Review
partial update 运行（用户请求＝同步新建团队的可发现性）。结论为无操作：setup 脚本 exit 0、未改动任何被跟踪文件（live 与新建备份逐字节相同）、20 个节全在容忍带内、尺寸 30944/32768 B 余量 1824 B 未触发收敛、17 个备份的标题集合差只有已被取代的 ## Resource Registry（归因为收敛非丢失）。团队可发现性经三处依据判定为无需登记（framework-map.md 的 Teams 是位置行、Skills & Tools 明写无注册表、Framework Map 须保持 summary+pointer）。符号链接五个全 OK，四套命令副本树各 25 文件。本命令无产物，故 Artifact Commit 步跳过；用户另 requested 的提交属上一轮 /speckit.team 审计的产物，单独成一个提交、不折进本命令。

## Optimization Points
- **备份保留规则会把「已被刻意取代」的标题永久钉成 load-bearing。** Action 3 的 keep-set = 最新 5 个 + 任何仍持有 live 文件所无的 `## ` 标题的备份。本次实测：17 个备份里有 3 个（2026-07-11、2026-08-15-141412、2026-08-17-103748）持有 `## Resource Registry`，而该节按 Action 5 的「Supersede legacy registry」条款是**机器维护、非用户撰写**、已由 `## Skills & Tools` 的目录发现模型取代、其行可从 `.specify/skills/` 与 `.specify/memory/tools/` 重新导出——即它的缺席是收敛而非丢失。但保留规则只做标题集合差、不认「该标题是被取代的」，于是这 3 个备份永久留在 keep-set，`.specify/instructions.md-*` 永远剪不到 5 个以下。建议：保留规则增加一条「已被模板显式取代的标题不计入 load-bearing」，取代名单由 Action 5 的 supersede 条款持有（当前是 `## Resource Registry` 与内联 `## Git Workflow`），使剪枝集能真正收敛。
- **一个备份是被 git 跟踪的，用户按可剪清单动手时会撞上它。** `.gitignore:56` 已忽略 `.specify/instructions.md-*`，但 `.specify/instructions.md-2026-07-11` 在忽略规则之前就已提交，故仍在版本控制里，且它恰是 3 个 load-bearing 之一。残余报告点名可剪集时若不区分「未跟踪/已跟踪」，用户 `rm` 之后会留下一个待提交的删除。建议报告里对可剪集标注跟踪状态。
