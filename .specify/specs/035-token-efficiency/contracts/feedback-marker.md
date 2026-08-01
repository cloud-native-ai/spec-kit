# Contract: 反馈标记与引擎过滤(feedback-marker)

**Consumers**: contract tests、feedback-step 嵌入单元、improve-* 消费层

## C-M1 feedback-step 扩展

- `shared/workflow/feedback-step.md` 的 Canonical block step 2(Reflect)MUST 含 Token 效率自评三问:是否存在 (1) 原文转储 (2) LLM 代做确定性工作 (3) 重复读取同一内容。
- 有发现时,对应优化点条目行 MUST 内嵌字面量 `token-efficiency`([[STR-001]])。
- 干净运行 MUST NOT 追加 Token 观察点;沿用既有句式 `No significant optimization points identified this run.`。
- 自评 MUST NOT 输出编造的 Token 数值(定性或行/字节代理)。
- 嵌入单元(各命令/技能的 `## Feedback` 节)零改动——扩展只落 canonical block 单一事实源。

## C-M2 `list --contains` 过滤(feedback-utils.py)

命令面:

```bash
python3 scripts/python/feedback-utils.py --action list --contains token-efficiency [--limit N] [--unit-id U] [--since D] [--format json]
```

- `--contains <text>` MUST 为 `list` 的可选参数;省略时行为与现状完全一致(向后兼容)。
- 匹配范围 MUST 覆盖条目正文全文(`## Review` + `## Optimization Points`)与 frontmatter `summary`;匹配为大小写不敏感的子串匹配。
- MUST 可与既有过滤器(`--unit-id`/`--unit-type`/`--since`/`--limit`)组合,语义为 AND。
- 文件读取发生在引擎程序侧(程序优先合规);输出仍为摘要级(index 元数据 + summary),MUST NOT 因加过滤而改为输出条目全文。
- 无匹配时 MUST 正常返回空列表(exit 0),不报错。
- 镜像:`scripts/python/feedback-utils.py` ↔ `.specify/scripts/python/feedback-utils.py` 字节一致。

## C-M3 检索完备性

- 以 [[STR-001]] 写入的全部 Token 观察条目,`list --contains token-efficiency --limit 0`(或足够大的 limit)MUST 一次全部返回(SC-005 判据)。
- 证据 feedback 泳道消费路径零改动(recurrence 信号由 038 既有机制产生)。
