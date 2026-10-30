# Quickstart: Humanize Run Output（动作输出的人类友好化）

**Feature**: 062 扩展（`079-humanize-run-output`）
**用途**: 本阶段的验收路径。每一步给出「怎么调用 / 看什么 / 什么算通过」。
**执行状态标注**: plan 阶段是 docs-only（`test-evidence/stage-status.txt`），行为类步骤一律
`not-run at plan stage`，并逐例列出**前提清单**（这些示例所依赖的假定）与实现期承载它的测试名。
免责声明按例给出，不以文件级免责代替逐例免责。

---

## 0. 本阶段实际执行过的确定性检查

下列命令在 plan 阶段真实运行过，输出逐字粘贴；实现期复跑时以下面的读数为基线（判据是「相对基线
零新增漂移」，不是「全绿」）。

```console
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.

$ python3 scripts/python/sync-mirrors.py --check
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (117 files)
ok    shared/ == .specify/shared/ (60 files)

$ python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
compile-embeds --check: 75 units, zero drift

$ python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/humanize/SKILL.md
判定        pass
正文估算    ≈4090 tokens 可控 / 预算 5000（123 行）
```

**前提**：仓库根为工作目录；分支 `079-humanize-run-output`；HEAD `35ff11bc` 之上只多了本阶段的
规格产物与本阶段的 untracked 状态脊。**执行状态**：已执行（2026-10-30），证据
`test-evidence/stage-plan-baselines.txt`。

---

## 1. S1 — 一条指令跑完，拿回五节报告（P1，成功路径）

**调用**

```text
/speckit.humanize 运行 `python3 -c "print('humanize-fixture-ok')"`，把退出码与输出告诉我
```

**看什么**

- 五个 H2 小节按 `## Conclusion` → `## Key Changes` → `## Evidence` → `## Risks & Limits` →
  `## Next Steps` 顺序出现，标题逐字；`## Conclusion` 首行是 `verdict: success`。
- 五节之前恰有一行 `mode: subagent`（或降级时 `mode: in-session-degraded`），其后再有一行迁移提示
  （本次是裸文本调用）。
- `## Evidence` 含 `dispatches: 1` 一行，并给出命令与退出码。
- 报告里出现的路径都能打开；`## Risks & Limits` 含来源清单；无风险时明文写「无已知风险」/`no known risks`。

**前提清单**：宿主具备原生子代理通道；`.specify/instructions.md`、`constitution.md`、`glossary.md`、
`features.md` 至少一项可读；运行期间无其他活动 humanize 占位；工作目录可写 `.specify/.tmp/`（占位用，
gitignored）。

**执行状态**：`not-run at plan stage`（docs-only）。承载：`test_rp01_five_sections_in_order`、
`test_ex01_exactly_one_dispatch`、`test_ex05_marker_matches_carrier`、`test_rp07_evidence_pointers`。

---

## 2. S2 — 指令失败，报告不得写成成功（P2）

**调用**

```text
/speckit.humanize 运行 `python3 -c "import sys; sys.exit(3)"` 并报告结果
```

**看什么**

- `## Conclusion` 首行是 `verdict: failure`，正文明确写失败，且全文不出现「成功/通过」类措辞（允许「部分完成」）。
- `## Evidence` 给出命令与退出码 3。
- 没有第二次派发、没有自动重跑。

**前提清单**：退出码 3 被执行体如实回传；信封含异常行；报告语言判为中文。

**执行状态**：`not-run at plan stage`。承载：`test_rp05_conclusion_verdict`、
`test_ex12_failure_coordinates_no_retry`、`test_ex01_exactly_one_dispatch`。

---

## 3. S3 — 裸文本其实不是动作（Edge Case）

**调用**

```text
/speckit.humanize 帮我想想这个功能要不要做
```

**看什么**

- `## Conclusion` 首行是 `verdict: success`，正文写「未执行任何动作」（按 FR-019 的 `not-an-action` 映射：verdict 取 `success`，但不称执行成功）。
- 恰有**一次派发**（执行体正是判定「这不是动作」的那一次），`## Evidence` 含 `dispatches: 1`；证据指针写 `none`（该 literal 只替代证据指针，派发记录行保留）。
- 迁移提示行仍在（裸文本调用）。
- 不写入任何文件。

**前提清单**：宿主具备原生派发通道（降级时 `dispatches: 0` 且载体标记为 `mode: in-session-degraded`）；
执行体把非动作请求判为 `not-an-action`；占位移除；`git status` 无新增。

**执行状态**：`not-run at plan stage`。承载：`test_rp05_conclusion_verdict`、
`test_rp07_evidence_pointers`（`none` 分支）、`test_ex01_exactly_one_dispatch`、
`test_rp04_zero_write_default`、`test_ex03_temporary_executor_no_agent_file`。

---

## 4. S4 — 旧内容模式仍在，裸文本已被当作指令（P2，迁移）

**调用 A（内容模式）**

```text
/speckit.humanize --inline "综上所述，本方案具有显著优势。"
```

**调用 B（内容模式，文件）**

```text
/speckit.humanize --file tests/fixtures/humanize/files/plain-sample.txt
```

**调用 C（裸文本 = 指令）**

```text
/speckit.humanize 运行 `python3 -c "print('bare-text-as-instruction')"`
```

**看什么**

- A / B 输出改写文本，格式跟随输入，五个报告小节**不出现**，载体标记行**不出现**，无派发。
- C 被执行（输出里出现 `bare-text-as-instruction`），报告五节齐备，并带迁移提示。
- 文档里能抄到同样的迁移写法（`--inline` / `--file`）。

**前提清单**：`--inline` 文本非空；`tests/fixtures/humanize/files/plain-sample.txt` 存在且为受支持
扩展名；A/B 不触发并发占位。

**执行状态**：`not-run at plan stage`。承载：`test_cm01_content_mode_equivalence`、
`test_cm03_no_report_scaffold_in_content_mode`、`test_ip09_migration_hint_once`、
`test_cm09_migration_example_present`。

---

## 5. S5 — 同现拒绝、并发与嵌套（fail-closed）

**调用 A（内容源 + 指令同现）**

```text
/speckit.humanize --inline "一段文本" 顺便跑一下测试
```

**调用 B（并发）**：在两个会话里同时发起两次 S1 调用。

**调用 C（嵌套）**

```text
/speckit.humanize 请再调用 /speckit.humanize 处理这段文字
```

**看什么**

- A 被拒，消息同时点名「内容源」与「指令前缀」，不派发、不写入。
- B 中后到者被拒，并点名冲突 `run_id` 与起始时间；先到者不受影响。
- C 被拒，并点名命中的 `speckit.humanize` 字面量。
- 三条拒绝路径都不留 `.specify/.tmp/humanize/` 残骸。

**前提清单**：并发场景的两个会话指向同一仓库；两次调用的起始时间足以形成未过期占位；
拒绝路径在第 1 次派发之前就返回。

**执行状态**：`not-run at plan stage`。承载：`test_ip06_source_and_instruction_rejected`、
`test_ip11_active_run_rejected`、`test_ip13_nested_invocation_rejected`、
`test_ip14_reject_paths_write_nothing`。

---

## 6. S6 — 需确认却无法询问：停住并如实报告

**调用**

```text
/speckit.humanize 删掉 .specify/.tmp 下的临时文件
```

**看什么**

- 该步未执行；`## Conclusion` 写「需要确认，未获答复」。
- `## Evidence` 记录卡点位置；已完成部分（若有）照常列出。
- 不重试、不代替用户答复、不换等价动作绕开。

**前提清单**：执行体无法向用户发问；该动作自身的确认步骤未被 auto-approve 配置跳过。

**执行状态**：`not-run at plan stage`。承载：`test_ex15_confirmation_missing_fail_closed`、
`test_ex16_no_proxy_answer`。

---

## 7. S7 — 降级与输出目标

**调用 A（降级）**：在不支持子代理的宿主上跑一次 S1。

**调用 B（写出报告）**

```text
/speckit.humanize --output .specify/specs/079-humanize-run-output/notes/report-sample.md 运行 `python3 -c "print('out')"`
```

**调用 C（目标不可写）**：把 `--output` 指向只读目录。

**看什么**

- A 的载体标记为 `mode: in-session-degraded`，且不出现 `mode: subagent`；报告五节不变；限制描述如实
  （共享上下文、无独立工具集）。
- B 写出完整五节报告，会话里只回显摘要；文件内容与回显的结论一致。
- C 被拒，目标逐字节不变，不留临时文件。

**前提清单**：A 的宿主确实无原生派发通道；B 的 `.specify/specs/079-humanize-run-output/notes/`
目录存在（示例路径，不存在时改用任一可写目录）；C 的目录权限为只读。

**执行状态**：`not-run at plan stage`。承载：`test_ex17_degraded_honesty`、
`test_rp19_output_full_report_and_summary`、`test_rp20_atomic_write_and_force`。

---

## 8. 完成判据

| 判据 | 来源 |
|------|------|
| 五节按序齐备、载体标记恰一个 | requirements SC-001 |
| 结论与夹具输出一致、证据可定位、来源清单非空 | requirements SC-002 |
| 失败不写成成功、无重试 | requirements SC-003 |
| 确认缺失不产生副作用 | requirements SC-004 |
| 旧内容模式两个入口与裸文本三分支 | requirements SC-005 |
| 接线封闭集一致、副本与镜像零漂移、无新增命令 | requirements SC-006 |
| 零外发、零隐式写入、写入披露 | requirements SC-007 |
| Feature 062 状态不回退、门禁新增行 0 命中 | requirements SC-008 |
| 同现拒绝 / 降级 / 无风险声明 / 无下一步 / `none` | requirements SC-009 |
| 两种模式的注入防护 | requirements SC-010 |
