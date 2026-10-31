# Run-mode fixture set — `/speckit.humanize`（Feature 062 扩展，规格 079）

本目录是 079「动作输出的人类友好化」的**运行模式**夹具集。它只服务契约测试与评估，不是运行产物；`tests/fixtures/humanize/` 的既有内容语料（`files/`、`inline/`、`selftest/`、`tone/`、`rubric.md`、`diff_protected.py`）不被本目录替代、也不被改写（WC-15）。

字段语义的唯一所有者是 `.specify/specs/080-humanize-run-output/data-model.md`；本文件只指路，不复制字段表。

## 信封格式（E5 ActionResultEnvelope）

每个 `*/envelope.md` 是一封**回传消息的样本**（不是报告文件，不是磁盘产物）：YAML frontmatter 承载 `data-model.md` § E5 的七个字段（`status`、`final_output`、`products`、`evidence`、`failures`、`blocked_at`、`anomaly_line`），正文只写这份样本的用途与判读提示。`status` 的取值域 owner 是 requirements FR-012；verdict 映射的 owner 是 FR-019——两者都不在此复述。

- `anomaly_line`：无异常写 `未发现异常`；有异常写行首 `ANOMALY:` 并逐条列出。**缺失即信封不完整**，其结论不得被消费（EX-10）。
- `products`：`{path, kind: created|modified}` 列表，只写指令造成的写入。
- `evidence`：`{pointer, kind: command|path|reading}` 列表；`command` 项与退出码 `reading` 项成对出现，供可定位性核对（EX-14）。

## 占位格式（E4 RunReservation）

`reservations/*.run` 是并发占位的样本文件，字段集按 `data-model.md` § E4（`path` / `created_at` / `output_target` / `ttl_hours=24`）。它们**只是夹具**，不落在 `.specify/.tmp/humanize/`，也不会被真实运行读取；真实占位由运行期创建并在任一出口移除（EX-20）。

## 夹具清单（class → 用途 → 条款）

| 夹具 | 类（WC-15） | 用途 | 服务条款 |
|------|-------------|------|----------|
| `success/envelope.md` | 成功 | 可确定产出（`humanize-fixture-ok`，退出码 0）：一份合规报告的全部输入 | IP-01…IP-10（源材料）、EX-01、RP-01…RP-04、SC-001/SC-002 |
| `failure/envelope.md` | 失败 | 退出码 3、`status: failed`、失败坐标齐备：报告不得读作成功 | EX-10、EX-12、RP-05、SC-003 |
| `non-action/envelope.md` | 非动作 | 散文式文本：`status: not-an-action`、无输出无产物 | RP-05、SC-009 |
| `needs-confirmation/envelope.md` | 需确认 | 卡在确认步：`blocked_at` 非空、无写入 | EX-15、EX-16、SC-009 |
| `denied/envelope.md` | 拒绝确认 | 用户明确拒绝：该步未执行、无替代动作、`products: []`、拒绝原因与未执行范围入 `failures` | FR-012、FR-019、SC-004 |
| `degraded/envelope.md` | 降级 | 会话内执行的可观察结果（不得冒充子代理观测） | EX-17、EX-18、SC-009 |
| `nested/instruction.txt` | 嵌套 | 指令原文含封闭 token `speckit.humanize` | IP-13、SC-009 |
| `reservations/run-a.run`、`run-b.run` | 并发 | 两个未过期占位：仓库级冲突与目标级占用 | IP-11、IP-12、EX-20、SC-009 |
| `injection/instruction.md` | 注入（第一组） | 运行模式指令注入：指令正文携带指令式文本 | FR-025、SC-010 |
| `injection/envelope.md` + `injection/executor-note.txt` | 注入（第三组） | 执行体回传注入：`final_output` / `evidence` / `products` 与产物内容携带指令式文本 | FR-025、SC-010 |
| `governance/` | 治理投影 | `instructions` / `constitution` / `glossary` / Feature 注册表的摘要投影桩，供来源清单断言 | RP-09、RP-10、FR-014/FR-015 |

第二组注入样本（内容模式输入注入）沿用既有语料 `../inline/s08-threat-inline.md` 与 `../files/instruction-threat-file.md`，不在此复制。

## 判读纪律

- 夹具是**数据**：其中的指令式文本（`injection/`）永远不被当作人类操作的指令执行，只用于断言「按数据处理」。
- 夹具不写任何报告文件；`report.md` 不得出现在本目录（EX-09）。
- 历史语料零改动：`git diff --stat 35ff11bc -- tests/fixtures/humanize ':!tests/fixtures/humanize/run'` 为空（T033 / WC-15）。
