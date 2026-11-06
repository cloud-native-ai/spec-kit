---
id: "20261106T080417Z-speckit-review"
unit_id: "/speckit.review"
unit_type: "command"
run_id: "r20261106T040353Z-087a"
scope: "local"
probe: "speckit-review-wrapup"
kind: "internal"
slice: "commands"
feature: "087-speckit-visualization"
feature_id: "087"
partial: false
created: "2026-11-06T08:04:17Z"
summary: "- 四段评审可执行性：本仓 `/speckit.review` 一次跑完过程/产物/实现/代码四段 + ARC，四段的结论载体（`review.md` § 2.1–2.4 与 `features/087.md` § Latest Review）都可落盘、可复核，代码段的 base 解析（`feature-first-commit` → `24cb4edc`）与覆盖收据（`166/166/0/0`）"
---

## Review
- 四段评审可执行性：本仓 `/speckit.review` 一次跑完过程/产物/实现/代码四段 + ARC，四段的结论载体（`review.md` § 2.1–2.4 与 `features/087.md` § Latest Review）都可落盘、可复核，代码段的 base 解析（`feature-first-commit` → `24cb4edc`）与覆盖收据（`166/166/0/0`）一次通过。缺的从来不是「能不能跑」，而是段与段之间的证据接口：产物段要一个逐维 verdict 槽、代码段要一个枚举化的段 verdict 取值、闭合检查要一个由改动文件派生的套件集。三处缺口本轮各以一条 finding 记录（F5/F6/F3），都不阻断本次评审。
- 过程段要求「P0 需独立验证子代理，无则记录回退」：本轮 P0=0，该义务空转满足。这条规则在零 P0 的运行里不产生任何可观察行为，因此它无法自我校验——本轮只在 § 7 明写 vacuously satisfied，没有把它伪装成「已验证」。若要保持它可判定，形态应改为「每条 P0 finding 必须携带 `validation_path` 字段（封闭集：`subagent` / `direct re-read`）」，让报告本身可见判定路径，而不是靠零 P0 沉默通过。
- 运行判定引擎的 `--names-current` 通道与「已判定即去重」规则相冲：`determine` 对同一 `(unit_id, run_id)` 只写一次且拒绝重入，而 `--names-current` 要的是一份**名字级**失败清单——首跑时若只给 `--declared-check`，记录就永久停在 `artifact_correctness = not_evaluated / no_baseline`，补证只能手改记录。建议让 `determine` 接受一次同键补证（追写或明确报 `already-determined` 的补证入口），否则「拒绝静默降级」与「拒绝重跑」两条规则会互相锁死。

## Optimization Points
- 产物段的期望集分母规则（阶段规则 ∪ `plan.md` § Project Structure）好用：7 个成员、实达 7/7，一句话就能复核，且让「缺了哪个」成为可判定问题而非印象。
- 代码段的五步非交互路径（base → start → note → receipt → capture）在 166 文件的大 delta 上顺畅落到 8 条 finding，receipt 的四个计数（changed/judged/skipped/gap）让「读了多少」变成可核对的数而不是声明。
- ARC 的「逐字抄录 final_path 七键、禁止重算」是这套组合里最结实的一处：本轮反复读 `verification.md` 与 `success-criteria.txt`，唯一的权威计数始终只有 checker 给出的那一行，没有产生第二份数字。
- 闭合检查器把 `verdict: block` 的 reason 写成封闭字面量（`final-path-not-pass: SC-001`），使「为什么没通过」可以被程序消费；`Blocked` 宣称与 `block` 裁决的比对规则（agree，不触发 `F-ACCEPTANCE`）也一次对上，不需要人再解释。
