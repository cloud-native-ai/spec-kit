# Contract: Feedback Entry Schema(条目 frontmatter 扩展)

**Requirement**: `041-refactor-feedback-probe` | **Consumes**: FR-005, FR-011, FR-020, SC-002, SC-008 | **Pinned by**: `tests/contract/test_feedback_probe_entry_schema.py`(扩展自 `test_feedback_entry_schema.py`)

## C-1 Frontmatter 字段(新版)

```yaml
id: 20260814T154958Z-speckit-requirements   # 不变
unit_id: /speckit.requirements               # 不变
unit_type: command                           # 不变
run_id: 041-refactor-feedback-probe-20260814-1  # 不变
scope: local                                 # 不变
feature: 041-refactor-feedback-probe         # 不变(requirement key)
feature_id: "041"                            # 不变(Feature registry ID,独立编号空间)
probe: speckit-requirements-wrapup           # 新增:Probe Object id(引擎解析写入)
kind: internal                               # 新增:自 Class 继生(internal|external)
slice: commands                              # 新增:自 Class 继承
disposition:                                 # 新增(可选):processed|ignored|缺省=未处置
partial: false
created: 2026-08-14T15:49:58Z
summary: ...
```

- C-1.1 `probe`/`kind`/`slice` MUST 由引擎在 `record` 时写入;三者一致于 registry 解析结果(C-6.2 of probe-registry.md)。
- C-1.2 `disposition` 仅经 `/speckit.feedback` 处置动作变更;MUST NOT 改写 `## Review`/`## Optimization Points` 正文。
- C-1.3 正文结构不变:`## Review` + `## Optimization Points`(≥1 条或显式 no-op 行)。

## C-2 旧格式判定与迁移

- C-2.1 旧格式条目判定 = frontmatter 无 `probe` 字段;`status` 输出 `legacy_remaining` 计数。
- C-2.2 迁移后旧格式残留 MUST 为 0(SC-005);处置记录见 `migration-log.md`(逐条:`id | disposition=delete|re-register | rationale | date`)。
- C-2.3 重登记条目:新 frontmatter + 正文保留原 Review/优化点要点;`created` 保留原时间,附 `migrated_from: <旧id>`。

## C-3 外部条目

- C-3.1 `kind=external` 条目的 `unit_id` 取宿主自定义单元引用(`custom:<owner>/<name>`),`unit_type=custom-unit`;`slice=host-custom`。
- C-3.2 外部条目文件名、去重键、index 镜像与内部条目同构;唯一差异在 package 排除(engine-cli C-4)与 `--kind` 过滤。

## C-4 index.json 扩展

- C-4.1 每条目镜像增加 `probe/kind/slice/disposition` 四键。
- C-4.2 顶层新增 `legacy_remaining: <n>`(迁移完成前后可对比)与 `external_count: <n>`。
- C-4.3 `reindex` 从条目文件全量重建,保留 `submitted_at/upstream_repo/threshold` 既有语义。
