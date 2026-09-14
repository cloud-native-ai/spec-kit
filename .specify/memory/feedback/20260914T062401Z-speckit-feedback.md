---
id: "20260914T062401Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "speckit-feedback-consume-20260914T022054Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-09-14T06:24:01Z"
summary: "Mode 4 resumed run: the previous invocation had completed Steps 1-3 (4 parallel read-only verifiers over 21 self-dogfooding entries → 64 points: 35 STILL-VALID / 13 PARTIAL / 13 ALREADY-FIXED / 3 ack "
---

## Review
Mode 4 resumed run: the previous invocation had completed Steps 1-3 (4 parallel read-only verifiers over 21 self-dogfooding entries → 64 points: 35 STILL-VALID / 13 PARTIAL / 13 ALREADY-FIXED / 3 ack / 1 NOT-OURS, 0 conflicts) and received explicit user confirmation of the report, but was interrupted before Step 4. This run re-enumerated (1 bundle, already-logged cross-check negative), recognized the batch as already-processed-by-session-record (NOT re-verified/re-routed — batch discipline preserved), and executed the confirmed cleanup exactly per the newly codified preserve-first rule: mkdir under ${TMPDIR} (macOS resolves to /var/folders/.../T, not /tmp), md5-verified copy, bundle removed, intake empty, consume-log batch-2 row appended with full routing breakdown (5 direct fixes executed, 11 improve-skills, 1 improve-docs, 6 requirements-candidates, 22 queued direct-fix with named owners, 17 acknowledge-only, orphan mark + preserve path recorded). Earlier in this run: 5 direct fixes landed in framework source (feedback.md x4 + git-workflow execute-commands dirty-gate) with per-tool copies regenerated and 52/52 targeted contract tests green.

## Optimization Points
- 确认后的「preserve→删除→记账」序列缺乏中断可见性：Mode 4 的 consume-log 行只在 Step 4 写入，若运行在用户确认报告之后、清理完成之前中断（本次即发生：模型切换打断），再次调用时 intake 仍有包而日志无对应行——新 invocation 无法区分「已处理待清理」与「新输入」，本次仅靠会话记忆判定为续跑。建议在命令模板 Step 4 明确：确认后 preserve/删除/追加行须作为一个不间断序列执行，其间不插入其他工作；并将「consume-log 已出现该包行」定义为批次已提交标记，供中断后续跑识别。
