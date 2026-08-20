# Feature Reference: 需求 045 → Feature 047(需求 045 / Feature 047)

**Requirement → Feature**: `045-sanitize-command` → Feature 047 Framework Material Hygiene(框架资料卫生)

## 绑定裁定(2026-08-20,/speckit.clarify)

新建 Feature 而非绑定既有特性:资料卫生为横向能力,治理面横跨 memory/docs/specs/镜像/链接多个域;037 Docs Command 仅覆盖 docs/ 内容收敛、038 Evidence Infrastructure 是证据采集层(过期证据 todo 只是触发实例)、025 Todo Command 管理 TODO 块。同轮决策:发现报告持久化携带 pending 状态(修复后更新状态)、仅手动触发零挂点。

## US → FR → 设计工件映射

| 用户故事 | FR | 设计工件落点 |
|----------|----|--------------|
| US1 过期残留检测(报告持久化先行) | FR-001/002/003/004/007 | 契约 sanitize-engine(collect)、sanitize-detection-rules §5(证据包)、sanitize-findings(台账/合并) |
| US2 关键资料正确性检查 | FR-005/006/007 | 契约 sanitize-detection-rules §1–§4(四类确定性规则)、sanitize-engine §4(范围红线) |
| US3 确认后清理 | FR-008/009/010/011/012 | 契约 sanitize-engine(apply/退出码)、sanitize-command-template(C-8 前置门控/移交分诊/执行报告)、data-model(Cleanup Plan/Execution Report/状态机) |

## 对 Feature 047 的 key changes(登记进 features/047.md 的实现注记)

1. 命令面:`/speckit.sanitize` 模板 + 4 工具副本 + docs/reference/commands/sanitize.md + 复杂命令分类(17→18)。
2. 引擎面:`scripts/python/sanitize-utils.py`(stdlib-only,collect/record/status/apply)×2 镜像 + Tool 记录。
3. 存储面:`.specify/memory/sanitize/findings.json` 累积台账(稳定 ID 合并、pending→resolved 状态机、自动收敛)。
4. 门控面:破坏性清理前置确认(046 两级判据破坏性桶)+ `gate-sanitize-destructive-cleanup` 必要性 probe + baseline total +1。
5. 复用面:docs-utils 断链、sync-mirrors --check 漂移、`.specify/archive/` 归档根——零重复实现。

## 交叉引用义务

- Feature 037(docs 内容收敛移交)、008(符号链接/说明文件再生成移交)、046(门控判据消费)、040(程序优先/摘要优先纪律)——047.md 与 037.md、046.md 已互挂交叉引用。
- 与三查命令的消歧(review/analyze/checklist,glossary 已录):sanitize 是资料卫生检查,非过程质量评审/实现前漂移分析/质量检查单。
