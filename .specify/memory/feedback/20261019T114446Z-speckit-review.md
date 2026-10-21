---
id: "20261019T114446Z-speckit-review"
unit_id: "/speckit.review"
unit_type: "command"
run_id: "speckit-review-20261019T114047Z"
scope: "local"
probe: "speckit-review-wrapup"
kind: "internal"
slice: "commands"
feature: "062-humanize-command"
feature_id: "062"
disposition: "processed"
partial: false
created: "2026-10-19T11:44:46Z"
summary: "本单元 wrap-up 摩擦（scope: local，仅记 /speckit.review 自身执行面，全局评估见 review.md）：(1) 编译嵌入的 Wrap-up 面 step 1/step 3 仅带 --unit-id/--unit-type：run-determination.py 以 exit 2 报 '--run-id is required'，补 --run-id 后再报 '"
introspection_ref: "introspection-20261021T133447Z#F-11"
disposition_reason: "introspection:introspection-20261021T133447Z#F-11"
---

## Review
本单元 wrap-up 摩擦（scope: local，仅记 /speckit.review 自身执行面，全局评估见 review.md）：(1) 编译嵌入的 Wrap-up 面 step 1/step 3 仅带 --unit-id/--unit-type：run-determination.py 以 exit 2 报 '--run-id is required'，补 --run-id 后再报 '--complexity is required'；feedback-utils.py 同样 exit 2 报 '--run-id is required'，补后再报 'record requires a non-empty --review / --review-file'。两引擎逐参单错，探明必填集需 4 次往返。(2) 二阶后果：按引擎最低要求补齐后，run-determination 记录的 token_consumption / elapsed / artifact_correctness 三轴均落 not_evaluated（面未命名任何 source flag，如 --session-file/--session-rows/--declared-check/--green-check）；而 (unit_id, run_id) 幂等（'duplicate: ... was already determined'，run-determination.py:1411-1413），记录无法事后补源——照面逐字执行的执行者会永久性低报本轮。(3) token-efficiency：上下文压缩后重读 review-template.md 与多处 owner 文档，加上上述逐参探明往返，属可避免消耗；定性量级为数十次工具调用中的约 6 次纯探明性往返，不编造精确 token 数。

## Optimization Points
- run-determination.py:1411-1413|feedback-utils.py record 必填集|compile-embeds 渲染占位约定
