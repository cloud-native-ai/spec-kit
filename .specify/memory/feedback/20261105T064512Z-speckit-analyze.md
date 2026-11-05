---
id: "20261105T064512Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261105T033420Z-082a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "083-mechanism-policy-separation"
feature_id: "082"
disposition: "ignored"
partial: false
created: "2026-11-05T06:45:12Z"
summary: "082 的 analyze 读闸完成：确定性引擎侧 pre-analyze(pass,err 0,adv 123)、validate-tasks(PASS 0/0)、flow-class(exit 0)、check-prerequisites(MODE C) 全绿；但 validate-decision-tensions 以 spec 目录重跑后报 5 条 HIGH（dtr-anchor 1 + "
disposition_reason: "text corrupted by unquoted backticks in shell heredoc; entry re-recorded cleanly under the same run_id"
---

## Review
082 的 analyze 读闸完成：确定性引擎侧 pre-analyze(pass,err 0,adv 123)、validate-tasks(PASS 0/0)、flow-class(exit 0)、check-prerequisites(MODE C) 全绿；但 validate-decision-tensions 以 spec 目录重跑后报 5 条 HIGH（dtr-anchor 1 + expected-sacrifice-unmapped 4），且 coverage-baseline.txt 缺失使子句覆盖恒为 0——二者均属 plan/tasks 回落面，不是分析误报。checklist 上呈的四个 medium 全部复现（GM 计数漂移、三个新增+五个改写应为 2+6、11+1=12 的 10 行、GM-12 四类失败名；requirements 第 306 行自相矛盾；GM-12 裸串 vs 需求侧 code span），另新发现模块路由（guard vs consumers）、SW-05 grep 作用域漏 、feature-ref 改写源 9 只列 7、fixture 序数漂移等。本单元流程侧无失效：读闸顺序（先引擎后语义）正确，证据指针逐条可回溯。

## Optimization Points
- **token-efficiency** — 首轮 `validate-decision-tensions.py` 以 plan.md 文件路径作 `--spec`，引擎返回 `status=unreadable` 且全标签 0 错误，误读为"干净"；改以 spec 目录重跑才拿到 5 条 HIGH。确定性工具的入参形态（目录 vs 文件）应比照 `--help`/引擎 manifest 一次对齐，而非以一次试跑当探测。
- 本轮读数来自 10+ 个确定性引擎（pre-analyze / validate-tasks / validate-decision-tensions / account-clause-coverage / audit-test-budget / flow-class-check / check-prerequisites），语义比对留给人工阅读——这是本单元应然分工；但四个 checklist 已报 medium 中，GM 计数漂移一类（"六个模块"对 5 行表）本可由 GM 表的行数断言脚本化，属可下放的确定性工作。
- artifact_correctness 轴为 `not_evaluated (no_declared_checks)`：analyze 单元未声明可机检的核对项，导致每次 analyze 的产物正确性只能由人读背书；建议该单元登记最小声明集（如"findings 表每行带证据指针"的格式断言）。
