---
title: 正确性检查夹具材料
status: active
---

本材料用于死引用检查器的正反例验证。

- 链接形态:引用 [不存在的文档](../missing/absent.md) 应报死引用。
- 路径形态:引用 `scripts/python/nope-utils.py` 应报死引用;引用 `scripts/python/feedback-utils.py` 不报。
- 命令形态:引用 `speckit.nonexistent` 应报死引用;引用 `speckit.feedback` 不报。
- 技能形态:引用 `skills/ghost-skill/` 应报死引用;引用 `skills/create-docs/` 不报。
- 占位符形态:引用 `<path-to-file>` 与 `{config_key}` 不报。

```
围栏代码块内的引用 scripts/python/also-missing.py 不报(示例非引用)。
```
