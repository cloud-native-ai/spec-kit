---
id: "rename-retire-init-cd74502f"
scope: "knowledge"
source: "/speckit.instructions"
feature: "instructions"
tags: ["convention", "instructions", "init", "obsolete-asset", "rename"]
title: "Rename/retire 需登记 init 回收清单"
created: "2026-08-13T09:27:49Z"
summary: "持久约定（用户补充，已写入 .specify/instructions.md Recurring Operational Lessons）：每次重命名或废弃命令/技能/脚本时，必须在 src/specify_cli/__init__.py 的 OBSOLETE-ASSET-REGISTRY（_OBSOLETE_SKILLS/_OBSOLETE_COMMANDS/_OBSOLETE_TEMPLATE"
---

持久约定（用户补充，已写入 .specify/instructions.md Recurring Operational Lessons）：每次重命名或废弃命令/技能/脚本时，必须在 src/specify_cli/__init__.py 的 OBSOLETE-ASSET-REGISTRY（_OBSOLETE_SKILLS/_OBSOLETE_COMMANDS/_OBSOLETE_TEMPLATES）登记旧名，扩展 tests/contract/test_cleanup_obsolete_assets.py 覆盖之，并清理 .specify/skills/ 等镜像中的旧目录（sync-mirrors 不删文件）。理由：init 的 additive copytree 不删除陈旧文件，未登记的重命名会在每个升级的工作区留下死结构（实例：extension-e2e-test→browser-extension）。
