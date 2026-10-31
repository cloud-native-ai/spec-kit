# Quickstart run — 079 humanize run mode（S1–S7）

**日期**: 2026-10-31（本段 implement part 4）
**宿主**: macOS 本地工作区（分支 `080-humanize-run-output`，base `eb736a07`）
**载体声明**: 本段授权明确**不派发子代理**，因此运行模式按 `in-session` 载体执行：每条报告携带
`mode: in-session-degraded` 与 `dispatches: 0`。原生载体（`mode: subagent` / `dispatches: 1`）的
场景在本段**未执行**，其契约面由主契约套件的断言承载（见 § 不可复现场景）。
**记录口径**: 每条给出调用原文、真实执行的命令、真实输出与退出码；报告只摘录判定行与证据行，
全文形态由 `tests/contract/test_humanize_command_surface.py` 的五节断言承载。

---

## S1 — 一条指令跑完，拿回五节报告（成功路径）

**调用**（裸文本 = 待执行指令）

```text
/speckit.humanize 运行 `python3 -c "print('humanize-fixture-ok')"`，把退出码与输出告诉我
```

**真实执行**

```console
$ python3 -c "print('humanize-fixture-ok')"
humanize-fixture-ok
exit=0
```

**留痕**: 占位 `.specify/.tmp/humanize/20261031T001000Z-s10001.run` 建立后于出口释放。

**报告判定行**

```text
mode: in-session-degraded
已按指令执行；改写文本请用 --file/--inline

## Conclusion
verdict: success — 成功：指令已执行，退出码 0，stdout `humanize-fixture-ok`。

## Evidence
- `python3 -c "print('humanize-fixture-ok')"` → exit 0；stdout `humanize-fixture-ok`
- dispatches: 0

## Risks & Limits
- 无已知风险。
- 限制：本次为会话内执行（`mode: in-session-degraded`），无独立上下文与独立工具集。
- 来源清单：instructions / constitution / glossary / features(062 行投影) / 本次会话（均 read）；缺失来源：无。
```

结论行先于细节；五节标题逐字按序；载体标记恰一行；裸文本调用多一行迁移提示；`dispatches: 0` 与降级载体一致。

---

## S2 — 指令失败，报告不得写成成功

**调用**

```text
/speckit.humanize 运行 `python3 -c "import sys; sys.exit(3)"` 并报告结果
```

**真实执行**

```console
$ python3 -c "import sys; sys.exit(3)"
exit=3
```

**留痕**: 占位 `20261031T001001Z-s20002.run` 建立后于出口释放；无第二次派发。

**报告判定行**

```text
verdict: failure — 失败：指令以退出码 3 结束，未产生输出。
## Evidence
- `python3 -c "import sys; sys.exit(3)"` → exit 3
- dispatches: 0
```

全文无「成功/通过」类措辞；无重试；失败坐标（载体 in-session、阶段 execution、退出码 3）可定位。

---

## S3 — 裸文本其实不是动作（Edge Case）

**调用**

```text
/speckit.humanize 帮我想想这个功能要不要做
```

**真实执行**: 无命令可执行（不是动作）；未执行任何动作，未写入任何文件。

**报告判定行**

```text
verdict: success — 未执行任何动作（按 not-an-action 映射取 success，但不称执行成功）。
## Evidence
- none
- dispatches: 0
```

`none` 只替代证据指针，`dispatches:` 行保留；迁移提示行随裸文本调用出现。

---

## S4 — 旧内容模式仍在，裸文本已被当作指令（迁移）

### 调用 A（内容模式，内联）

```text
/speckit.humanize --inline "综上所述，本方案具有显著优势。"
```

**真实输出**（只含改写文本；无五节、无载体标记、无迁移提示；无派发、无占位）

```text
这个方案的优势很明显。
```

### 调用 B（内容模式，文件）

```text
/speckit.humanize --file tests/fixtures/humanize/files/plain-sample.txt
```

**真实输出**（纯文本格式跟随输入；未写入任何文件）

```text
值班交接记录

10 月 18 日白班交接给夜班。白天处理了三件事：报表平台慢查询告警，定位到一条没走索引的统计 SQL，加上索引后恢复了；给市场部开通了活动数据的只读权限；确认备份作业的告警是误报，磁盘空间其实还剩 41%。夜班要留意凌晨 2 点的账务批处理：如果 3 点前还没收到完成通知，先看批处理日志的最后一行，再决定要不要呼叫账务值班。
```

### 调用 C（裸文本 = 指令）

```text
/speckit.humanize 运行 `python3 -c "print('bare-text-as-instruction')"`
```

**真实执行**

```console
$ python3 -c "print('bare-text-as-instruction')"
bare-text-as-instruction
exit=0
```

报告五节齐备（与 S1 同形），并带迁移提示行。docs 与模板中可抄到同样的迁移写法（`--inline` / `--file`）。

---

## S5 — 同现拒绝、并发与嵌套（fail-closed）

### 调用 A（内容源 + 指令同现）

```text
/speckit.humanize --inline "一段文本" 顺便跑一下测试
```

**真实输出**（拒绝，未派发、未写入、未留占位）

```text
reject: both-sources-and-instruction — 内容源 --inline 与非空指令「顺便跑一下测试」同现；一次调用只接受一个输入源。
```

点名了内容源（`--inline`）与指令前缀（「顺便跑一下测试」）。

### 调用 B（并发）— `not-reproducible in this host`

单会话执行无法产生两个并发调用；按任务正文以夹具断言替代：

```console
$ .venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py -k "ip11 or ip12"
2 passed
```

### 调用 C（嵌套）

```text
/speckit.humanize 请再调用 /speckit.humanize 处理这段文字
```

**真实输出**（拒绝，点名命中字面量，未派发、未写入、未留占位）

```text
reject: nested-invocation — 指令命中封闭 token「speckit.humanize」；这是保守判定，宁可误拒提及该名称的指令。
```

三条拒绝路径执行后 `ls -A .specify/.tmp/humanize/` 为空。

---

## S6 — 确认缺失 / 用户拒绝确认

### 调用 A（确认缺失：执行体无法询问）

```text
/speckit.humanize 删掉 .specify/.tmp 下的临时文件
```

**真实执行**: 该步未执行（未删除任何文件）。占位 `20261031T001012Z-a60009.run` 于出口释放。

**报告判定行**

```text
verdict: needs-confirmation — 需要确认，未获答复：删除操作需要用户确认，执行体无法询问。
## Evidence
- blocked_at: 删除 `.specify/.tmp` 下临时文件这一步
- 已完成部分：无
- dispatches: 0
```

不代答、不换等价动作、不绕过；humanize 主会话未代替用户答复。

### 调用 B（用户明确拒绝确认）— `not-reproducible in this unattended run`

无人值守运行没有可转达确认请求的用户，不能伪造「用户拒绝」。按任务正文以夹具断言替代：

```console
$ .venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py -k "sc04"
2 passed
```

两条断言覆盖：该步未执行且无替代动作、副作用快照不变（`test_sc04_denied_no_side_effect`）；
`denied` → `verdict: aborted`、文案含「用户拒绝确认」与未执行范围（`test_sc04_denied_verdict_and_scope`）。

---

## S7 — 降级与输出目标

### 调用 A（降级）— `not-reproducible in this host`（不作为原生对照）

本宿主具备子代理通道，但本段授权禁止派发，故未产生「原生载体 vs 降级载体」的对照运行；
降级契约由夹具断言承载：

```console
$ .venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py -k "ex17 or ex18"
2 passed
```

同时，本页每条真实运行都以 `mode: in-session-degraded` 记录，降级路径本身已被实际执行。

### 调用 B（写出报告）

```text
/speckit.humanize --output .specify/specs/080-humanize-run-output/notes/report-sample.md 运行 `python3 -c "print('out')"`
```

**真实执行**

```console
$ python3 -c "print('out')"
out
exit=0
written: 901 bytes
```

写入采用临时文件 + 重命名（原子写）；文件含完整五节报告、载体标记行、`verdict:` 与 `dispatches:` 行，
**不含**迁移提示行。会话回显摘要：

```text
摘要：verdict: success；1 条证据（exit 0 / stdout `out`）；无已知风险；无下一步。全文见 notes/report-sample.md。
```

### 调用 C（目标不可写）

```text
/speckit.humanize --output .specify/.tmp/humanize/no-such-dir/report.md 运行 `python3 -c "print('unwritable-check')"`
```

**真实执行**（父目录缺失 → 临时文件创建失败 → 拒绝）

```console
$ python3 -c "from pathlib import Path; Path('.specify/.tmp/humanize/no-such-dir/.report.tmp').write_text('report', encoding='utf-8')"
FileNotFoundError: [Errno 2] No such file or directory: '.specify/.tmp/humanize/no-such-dir/.report.tmp'
exit=1
```

目标不存在、无部分文件；既有目标未被触碰。

---

## Teardown 与副作用核对

```console
$ ls -A .specify/.tmp/humanize/ | wc -l
0
```

`git status --porcelain` 只显示本特性产物与既有脏文件（`.specify/memory/session/…-076a-c.md`，本段未触碰）：

```text
 M .claude/commands/speckit.humanize.md
 M .github/prompts/speckit.humanize.prompt.md
 M .opencode/command/speckit.humanize.md
 M .qoder/commands/speckit.humanize.md
 M .specify/memory/features.md
 M .specify/memory/features/062.md
 M .specify/memory/session/20261029T101833Z-run-determination-speckit-checklist-r20261029t172918z-076a-c.md
 M .specify/skills/humanize/SKILL.md
 M docs/reference/commands/humanize.md
 M skills/external/humanize/SKILL.md
 M skills/external/humanize/references/run-mode.md
 M tests/contract/test_humanize_command_surface.py
 M tests/fixtures/humanize/run/injection/executor-note.txt
?? .specify/skills/humanize/references/
?? .specify/specs/080-humanize-run-output/baseline-failed.txt
?? .specify/specs/080-humanize-run-output/notes/report-sample.md
?? .specify/state/080-humanize-run-output.md
```

未出现 `.specify/.tmp/humanize/` 残骸；除 `notes/report-sample.md`（S7 B 的显式输出）外没有新增文件。

## 不可复现场景（如实声明）

| 场景 | 原因 | 替代证据 |
|------|------|----------|
| S5 B 两会话并发 | 单会话执行无法构造两个同时调用 | 夹具占位断言 `test_ip11_active_run_rejected`、`test_ip12_output_occupied_rejected` |
| S6 B 用户拒绝确认 | 无人值守运行没有可转达确认的用户；不得伪造用户答复 | `test_sc04_denied_no_side_effect`、`test_sc04_denied_verdict_and_scope` |
| S7 A 原生载体对照 | 本段授权禁止派发子代理；原生载体未执行 | `test_ex17_degraded_honesty`、`test_ex18_degraded_keeps_report_contract`；且本页所有运行均以真实降级载体记录 |
