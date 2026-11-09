---
status: active
created: 2026-11-09
updated: 2026-11-09
binding:
  owner: human
  owner_id: human
  origin: 091-auto-git-closeout
---

# Goal: 091-auto-git-closeout

## Objective

每一次留存写入都以同一条 git 收口结束（commit → merge → push），序列完全由 .specify/workflow/git.md 声明的模型推导，无需人工逐次触发，也不得触碰只读上游或强推。

## Success Criteria

1. 四种工作流模型各自的收口序列可在夹具仓库中复现（单分支/双分支/临时分支/三层）。
2. 托管块缺失或 Closeout=ask 时，收口呈报并等待，不自行推送。
3. 推送被拒或合并冲突时，收口在首个失败处停下并记录状态，不自动强推、不二次重试。
4. 产物命令与无人值守运行使用同一条收口步骤（无第二套机制）。

## Boundaries

- 不新增 /speckit.* 命令、守护进程或第二套分支 registry；不做托管平台 PR/MR 自动化；不自动强推。

## History

- 2026-11-09 — created.
