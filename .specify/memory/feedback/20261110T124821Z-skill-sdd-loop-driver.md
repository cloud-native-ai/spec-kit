---
id: "20261110T124821Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "096-sdd-observer-agent-analyze-repair-r5-20261110"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
feature: "096-sdd-observer-agent"
feature_id: "096"
partial: false
created: "2026-11-10T12:48:21Z"
summary: "**Review**: 框架级反馈（owner `skill:sdd-loop-driver`）——完成门 SC 状态记录载体三方互斥。事实：(1) 宪法 VII `.specify/constitution.md:223` 的 Pre-Status-Flip Gate 要求每个 Success Criterion 在 `verification.log` 有状态行；(2) 仓库根 `.gitig"
---

## Review
**Review**: 框架级反馈（owner `skill:sdd-loop-driver`）——完成门 SC 状态记录载体三方互斥。事实：(1) 宪法 VII `.specify/constitution.md:223` 的 Pre-Status-Flip Gate 要求每个 Success Criterion 在 `verification.log` 有状态行；(2) 仓库根 `.gitignore:37` 的 `*.log` 使该路径默认不可提交（`git check-ignore -v` exit 0；同目录 `verification.md` exit 1），且无任务行声明 force-add；(3) 框架实施链只认 `verification.md`——`shared/workflow/acceptance-hardening.md:46`（四条件第 2 条）、`templates/commands/implement.md:50/58/60`（产出 `verification.md`，明言 closure checker 只读 `REQUIREMENTS_DIR/verification.md`）、`scripts/python/closure-acceptance-check.py:18/87`（`REQUIRED_INPUTS` 含 `verification.md`），词汇 owner `templates/verification-log-template.md` 同向。另有 `shared/guidelines/better-harness.md:27/39` 仍以 `verification.log` 作示例传感器名——漂移不限于本仓宪法。本线（096-sdd-observer-agent）处置：GATE-4 统一为 `verification.md`（框架链唯一输入名）并在行内披露宪法字面待框架级裁定；不写 `verification.log`、不改宪法（属独立修订）。建议裁定：宪法 VII 字面改为 `verification.md`（与 closure checker、verification-log-template、implement 模板一致），并同步 `shared/guidelines/better-harness.md:27/39`；若坚持 `.log` 名，则须同时修订 acceptance-hardening / implement 模板 / closure checker / verification-log-template 并为根 `.gitignore` 加例外——前者与既有机器判据一致、改动面最小。

## Optimization Points
- 宪法 VII 不应点名框架实施链不接受的载体名——`closure-acceptance-check.py` 的 `REQUIRED_INPUTS` 是机器可判定的 owner；建议宪法改为 `verification.md`，或改为不点名载体并指向 `templates/verification-log-template.md`。
- 根 `.gitignore:37` 的 `*.log` 与任何 `.log` 型证据载体先天互斥；若保留 `verification.log` 名称，需为根 `.gitignore` 加 `!.../verification.log` 例外或强制任务行 force-add，二者都会制造第二处漂移。
- 建议在 `acceptance-hardening.md` / `implement.md` / `closure-acceptance-check.py` 与宪法 VII 之间收敛到单一 owner 指针（词汇 owner 已是 `templates/verification-log-template.md`），避免载体名在四处各自书写。
