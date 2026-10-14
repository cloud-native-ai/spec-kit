---
id: "20261013T162525Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "routing-20261014-marksubmitted-hazard"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
disposition: "processed"
partial: false
created: "2026-10-13T16:25:25Z"
summary: "空参数调用 → 跑完整 Routing flow。帽子复验：根级 templates/skills/shared/src/specify_cli 均缺失，scripts 经核实为本项目构建脚本（build.sh / generate-mybatis-plus.sh / test.sh）→ 客户项目。清点：open 1 条（/speckit.feedback，kind=internal，slice="
disposition_reason: "consume-20261013-batch4 — FOREIGN entry (client-project consume run mis-resolved into framework store = path-resolution trap live instance, new requirements row); P1 mark_submitted null-selects-all + P2 package dry_run no-op routed to engine dry-run/destructive-selection row (HIGH: reindex unlinks index.json pre-gate); both verified against feedback-utils.py source"
---

## Review
空参数调用 → 跑完整 Routing flow。帽子复验：根级 templates/skills/shared/src/specify_cli 均缺失，scripts 经核实为本项目构建脚本（build.sh / generate-mybatis-plus.sh / test.sh）→ 客户项目。清点：open 1 条（/speckit.feedback，kind=internal，slice=commands，probe=speckit-feedback-wrapup），external_count=0 → Path A 无材料；backlog.md 不存在；outbox 为空（昨日 zip 已由用户手工送达上游 spec-kit/feedback/ 并移出）。step5 单向内容精化：逐条核验该条根因——读引擎源码确认 dry_run 仅在 action_cleanup 被读取、action_package 通篇不读，属框架引擎实现缺陷而非本项目配置/用法 → 维持 upstream-bound，无重分类；因仅 1 条且根因本会话已对源码核验，未另出正式 A3 报告（如实报告为判断而非静默跳过）。执行判定：**不打包**（1 条低于阈值 10，且 Path B step4 要求用户 go-ahead，空参数不构成）；**不跑 mark-submitted**（submitted_at 为 null → 会全选当前唯一那条未投递条目、盖 submitted_at 并多产一个 zip，等于把未投递记成已投递）；不 cleanup（本轮无打包）。已投递那批无需补记：cleanup 已归零计数，审计在 cleanup-log.md + 上游 zip 的 MANIFEST。同时纠正我昨日给用户的错误建议（『投递后再跑一次让我重置计数并清 outbox』）——计数早已被 cleanup 归零、outbox 早已为空，照做只会误伤新条目。全程零网络、零写入（除本条 feedback）。

## Optimization Points
- **Path B 的 step5→step6 次序在客户项目下有「误标已投递」陷阱**（严重度：中高，文档流程与引擎语义交互产生）。
- 实测链条：昨日按 path-b-and-probe.md 执行 step4 `package`（14 条）→ step5 客户项目分支 `cleanup`
- （`remaining_after: 0`，计数器归 0）→ 用户手工把 zip 送到上游 `spec-kit/feedback/` → 今日按 step6
- 准备 `mark-submitted`。读引擎源码发现 `action_mark_submitted` 的选取逻辑是
- `selected = [e for e in entries if created > submitted_at] if submitted_at else list(entries)`，
- 而 **cleanup 只删条目、不写 `submitted_at`**（本次实测 `status` 仍为 `submitted_at: null`）。
- 后果：cleanup 之后新记录的任何条目（本次为 `20261013T124722Z-speckit-feedback`，**尚未投递**）
- 会被 mark-submitted 全量选中、打成新 zip、并盖上 `submitted_at` —— 即**把未投递的发现记成已投递**，
- 同时产出一个多余的第二个 zip。已投递那批反而无需任何补记：cleanup 已把计数归零，
- 审计痕迹在 `cleanup-log.md`（指名归档 zip）+ 上游 zip 内 MANIFEST。
- 期望改进方向（择一或并用）：① `cleanup` 成功后同步写入 `submitted_at`（或独立的
- `last_packaged_at`），使 mark-submitted 的时间窗只覆盖该批之后；② `mark-submitted` 在
- `submitted_at` 为 null 且存在 open 条目时**拒绝或要求 `--all` 显式确认**，而不是静默全选；
- ③ 在 path-b-and-probe.md step6 明确「若 step5 已 cleanup 且其后有新条目，mark-submitted 会
- 连带误标新条目」并给出正确次序（先 package 新批次，或先 dispose 旧批次）。
- 附：`submitted_at: null` 对 `package` 与 `count_since_submission` 均无害（两者都有 null 分支，
- 分别退化为「全选」与「按 entries 计数」），故**不跑 mark-submitted 不会留下功能缺口**。
- **`--action package --dry-run` 是静默 no-op，已定位到源码锚点**（补强昨日条目 `20261013T124722Z-speckit-feedback`）。
- 实测：`grep -n dry_run feedback-utils.py` 仅命中 1564/1567/1590/1591/1597 行，**全部位于
- `action_cleanup` 内**；`action_package`（1132–1166 行）通篇不读 `args.dry_run`，无条件调用
- `write_package(...)`。因此 package 的 `--dry-run` 既不报错也不预览，而是照常落盘 zip，
- 输出文案「sources untouched」只覆盖「不改条目源文件」，极易被读成「无任何产物」。
- 期望改进方向：让 `action_package` 与 `action_cleanup` 对齐 —— dry-run 时只回显将要打包的条目数、
- zip 目标路径与清单预览，不调用 `write_package`；若为兼容必须落盘，则在输出中显式声明
- 「dry-run 已产生文件」并给出路径，避免调用方靠人工比对+删除来消歧（昨日即为此多花一轮）。
