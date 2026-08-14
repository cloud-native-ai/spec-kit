# Contract: feedback-utils.py Engine CLI(probe 扩展)

**Requirement**: `041-refactor-feedback-probe` | **Consumes**: FR-005~FR-007, FR-009~FR-010, FR-019~FR-021, SC-002/004/007/008 | **Pinned by**: `tests/contract/test_feedback_probe_cli.py`

在既有动作(`record/status/list/mark-submitted/reindex/package/upstream`)之上扩展;既有旗标与退出码语义不变(验证错误 = 2)。全部动作零网络。

## C-1 `record` 扩展

- C-1.1 `record` MUST 按 `--unit-id` 从 probe 合并真源解析 `probe`(Object);解析失败(无对应 Object)→ 退出码 2,错误信息含 `no probe object for unit`。
- C-1.2 条目 frontmatter MUST 写入 `probe`、`kind`、`slice`(自 Object→Class 继承);不接受调用方手工传 `kind`/`slice` 覆盖。
- C-1.3 外部条目(`kind=external`)与内部条目共同计入 `count_since_submission`(阈值为本地提示语义,与上送无关);外部排除仅发生在 package(C-4)。

## C-2 `list` 扩展(过滤)

- C-2.1 新旗标 `--slice <value>`:仅返回 `slice` 匹配的条目。
- C-2.2 新旗标 `--kind <internal|external>`:仅返回对应类别条目。
- C-2.3 既有 `--unit-id/--since/--limit/--contains` 语义不变;过滤为引擎端程序判定,输出保持摘要级。
- C-2.4 新旗标 `--disposition <processed|ignored|open>`:按处置状态过滤(open=缺省)。

## C-3 `probes`(新动作,模式一后端)

- C-3.1 `--action probes --format json`:输出合并真源(Classes + 内外 Objects)的结构化清单,含每 Object 的 `class_id/kind/slice/unit/lifecycle_point`。
- C-3.2 `--action probes --validate`:执行 contracts/probe-registry.md C-2/C-3/C-4 全部校验;违规逐条输出,退出码 2。
- C-3.3 `--action probes --reconcile`:执行 C-5 对账,输出双向缺漏清单;零缺漏退出码 0。

## C-4 `package` 排除(外部隔离)

- C-4.1 `--action package` 产出的 zip MUST 100% 排除 `kind=external` 条目及其在 MANIFEST 中的行。
- C-4.2 MANIFEST 增列 `probe`/`slice`(内部条目);外部排除不产生警告噪声,仅在 JSON 输出附 `excluded_external: <n>` 计数。

## C-5 `cleanup`(新动作,打包后的清理)

- C-5.1 `--action cleanup --package <zip路径|latest>`:将该包实际收录的条目从活跃库删除(条目文件 + index 镜像行),`--dry-run` 仅列清单。
- C-5.2 删除前 MUST 校验目标 zip 存在且 MANIFEST 可读;条目不在包内则不删。
- C-5.3 MUST 追加清理记录到 `.specify/memory/feedback/cleanup-log.md`(时间、包路径、逐条目 id)。
- C-5.4 清理后 `status` 计数按现存活跃条目重算,不重复触发提示。

## C-6 `probe-inject`(新动作,模式三后端)

- C-6.1 `--action probe-inject --unit custom:<owner>/<name> [--lifecycle-point wrap-up] --notes-file <描述>`:生成 `.specify/memory/feedback/probes/ext-<slug>.md`,frontmatter 满足 registry C-4;`object_id` 由引擎从 unit 派生(slug 化 + `ext-` 前缀),冲突 → 退出码 2。
- C-6.2 注入后立即可被 `record`(经 custom unit)与 `list --kind external` 消费。

## C-7 `map`(新动作,结构图重建)

- C-7.1 `--action map`:整体重建 `.specify/memory/feedback/probe-map.md`(Class→Object 树 + Mermaid 源码块 + 明细表,标注内外类别);不读旧文件、无合并语义。
- C-7.2 幂等:同真源两次执行产出逐字节一致(SC-003)。

## C-8 `migrate-legacy`(一次性迁移)

- C-8.1 `--action migrate-legacy --plan-file <处置计划>`:按计划逐条执行 `delete`(删除条目文件并记 `migration-log.md`)或 `re-register`(以新 frontmatter 重写,保留正文要点);计划格式为逐条 `id → delete|re-register`。
- C-8.2 执行后 `--action status` 报 `legacy_remaining: 0`(旧格式判定 = 无 `probe` 字段)。
- C-8.3 计划文件由 agent 整体 review 产出、用户确认后执行;引擎不自行裁定(裁定是 agent 工作,执行是程序工作)。

## 输出与退出码(汇总)

| 场景 | 退出码 |
|------|--------|
| 成功 | 0 |
| 参数/校验失败(无 probe 对象、schema 违规、对账缺漏、id 冲突) | 2 |
| IO/存储错误 | 3 |
