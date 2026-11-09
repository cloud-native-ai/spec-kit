---
id: "20261109T053552Z-skill-review-sdd-process"
unit_id: "skill:review-sdd-process"
unit_type: "skill"
run_id: "r20261109T023000Z-auto-closeout-review"
scope: "local"
probe: "skill-review-sdd-process-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-09T05:35:52Z"
summary: "process segment of the 091 review: the live template still routes the code segment through a shell script that is fed to python3 by the wrapper; gates that report process success alongside a blocking "
---

## Review
process segment of the 091 review: the live template still routes the code segment through a shell script that is fed to python3 by the wrapper; gates that report process success alongside a blocking verdict; review template has no slot for a segment's positive obligation

## Optimization Points
- review-template.md /speckit.review 无 slot 记录『做对了什么』导致 segment 结论只剩负向; closure-acceptance-check 的 verification 读取器只认 SC-NNN_status= 形态而 review 模板未被该读取器反向约束; process 段的 severities 与 artifact/impl 段共用 P0/P1/P2 却无字段标注段来源
