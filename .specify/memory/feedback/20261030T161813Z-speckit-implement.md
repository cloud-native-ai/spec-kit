---
id: "20261030T161813Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "r20261030T110000Z-079a"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
feature: "079-humanize-run-output"
partial: false
created: "2026-10-30T16:18:13Z"
summary: "Part 5/5 (T033–T036) closed the feature: the T036 WC-05…WC-20 group and the clause↔test map judge are green (17 passed), the nine frozen surfaces and the 38 frozen-verification files are byte-identica"
---

## Review
Part 5/5 (T033–T036) closed the feature: the T036 WC-05…WC-20 group and the clause↔test map judge are green (17 passed), the nine frozen surfaces and the 38 frozen-verification files are byte-identical to 35ff11bc, both derived-face engines exit 0, and verification.md indexes SC-001…SC-010. Measured axes: token and elapsed had no sensor (not evaluated, no number invented); artifact correctness had no comparable names baseline because the budget keeps the full suite at the segment start, so only the 5 declared green checks are recorded; satisfaction is unsettled until the next turn. Three optimization points follow.

## Optimization Points
- # /speckit.implement — 079-humanize-run-output, part 5/5（T033–T036）优化点
- **正确性轴的可证性缺口（执行面）**：本轮 303 条定向用例全绿、`validate-tasks` 与 `pre-analyze-check` 均 pass，但 运行判定 的 `artifact_correctness` 只能报 `not_evaluated / no_baseline`——implement 的测试预算把全量套件放在起点，段尾只留定向读数，`--names-current` 与全量 `--names-baseline` 不可比。建议 Test Budget 段承认「同名定向集」为一种可比对象（段起点同记一次），或明确以 `declared green checks` 作为正确性轴的合法证据形态。
- **判定器自认领（判据面）**：`test_wc12_clause_test_map_is_total` 的反向认领断言会把判定器自身判成孤儿，本轮靠 `tasks.md` § Clause Test Waivers 临时补一行豁免。tasks 模板可预置「判定器自身」的豁免形态，避免每个特性重复发明同一条豁免。
- **重复读取（token-efficiency）**：`test_wc12_clause_test_map_is_total` 与 `_waiver_rows()` 各读一次 `tasks.md`，同一文件在同一测试里被整份读取两次（当前数百行量级）；合并为一次读取即可，属可避免的重复消耗，未做精确 Token 计数。
