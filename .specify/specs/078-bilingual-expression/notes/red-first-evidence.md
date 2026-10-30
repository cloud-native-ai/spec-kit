# 红先行证据 — 078 双语表述（Bilingual Expression）

**测试对象（唯一）**：`tests/contract/test_bilingual_expression.py`（含夹具 `tests/fixtures/bilingual/*`）

**起点实测（2026-10-30，HEAD `cc508bfe`，分支 `078-bilingual-expression`）**：五个交付物路径均不在树
（owner 文档 `shared/guidelines/bilingual-expression.md`、检查器 `scripts/python/bilingual-expression-check.py`、
契约测试、夹具目录、本 `notes/` 目录），红先行起点 = 本次实测的红。

## 失败运行记录（四字段）

> 每次红先行运行必填以下四字段；只写「已执行」不算记录。

| 字段 | 值 |
|------|-----|
| 重放命令 | `python3 -m pytest tests/contract/test_bilingual_expression.py -q`（仓库根目录；系统解释器 Python 3.11.11 / pytest 8.2.2） |
| 真实输出 | 末行摘要 `14 failed, 1 passed in 0.18s`；15 tests collected；失败清单 = owner 结构腿 ×5（owner document missing: shared/guidelines/bilingual-expression.md）+ scan 夹具腿 ×3（checker missing: scripts/python/bilingual-expression-check.py）+ coverage / census / SC-001 关键词 / 镜像一致 / ambient 形态 / sample_lines 腿（FileNotFoundError: bilingual-expression-check.py 或断言失败）；唯一通过 = `test_drift_str_literal_unique_consumers`（语料中三字面量尚不存在，空集通过，T003 落文后转为实质断言） |
| 退出码 | `1`（PYTEST_RC=1） |
| 失败计数 | `14` failed / 15 collected（`test_drift_str_literal_unique_consumers` 1 passed） |
