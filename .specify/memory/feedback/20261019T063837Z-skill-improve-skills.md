---
id: "20261019T063837Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "sdd-loop-driver-watch-20261019T063708Z-probe-gap"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
disposition: "ignored"
partial: false
created: "2026-10-19T06:38:37Z"
summary: "旁路发现（不影响本次统一监听改进）：sdd-loop-driver 的 SKILL.md 内嵌 Wrap-up 调用 feedback-utils --unit-id skill:sdd-loop-driver，但 probe-definitions 中没有该 unit 的 probe object，执行即报 no probe object for unit。需注册该 unit 或在不可注册时不生"
disposition_reason: "introspection-20261021T133447Z: excluded (no actionable framework finding)"
---

## Review
旁路发现（不影响本次统一监听改进）：sdd-loop-driver 的 SKILL.md 内嵌 Wrap-up 调用 feedback-utils --unit-id skill:sdd-loop-driver，但 probe-definitions 中没有该 unit 的 probe object，执行即报 no probe object for unit。需注册该 unit 或在不可注册时不生成该 Wrap-up；本次未修复（超出监听改进范围）。

## Optimization Points
- 为 skill:sdd-loop-driver 增加 probe object/binding，或重新生成时不输出不可执行的 Wrap-up；当前内嵌命令不可执行。
