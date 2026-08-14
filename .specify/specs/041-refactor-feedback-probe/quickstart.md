# Quickstart — /speckit.feedback 三模式演练

**Requirement**: `041-refactor-feedback-probe` | 命令示例由 `tests/contract/test_feedback_probe_cli.py` / `test_feedback_command_template.py` 钉住(实施后执行应逐条通过;实施前示例即为契约)。

## 0. 前置

在一个 Spec Kit 项目内(specify init 完成),引擎位于 `.specify/scripts/python/feedback-utils.py`。下述 `python3 .specify/scripts/python/feedback-utils.py` 简写为 `fb`。

```bash
alias fb='python3 .specify/scripts/python/feedback-utils.py'
```

## 1. 模式一:无参数 — 全部 probe 总览

对话输入 `/speckit.feedback`(不带参数)→ agent 渲染竖状结构(数据自 `--action probes`):

```bash
fb --action probes --format json          # 合并真源:3 Class + 49 内部 Object + 项目外部 Object
fb --action probes --validate             # 五特征完备性/引用完整性校验(exit 0)
fb --action probes --reconcile            # 与嵌入点清单对账,双向零缺漏(exit 0)
```

预期总览形态(树状):

```text
internal
├── command-wrapup  [slice: commands] — 收集:命令单次运行回顾与 ≥1 优化点 → record→…→mark-submitted
│   ├── speckit-requirements-wrapup   (/speckit.requirements @ wrap-up)
│   └── … (18)
└── skill-wrapup     [slice: skills]  — 同上处理流程
    ├── skill-create-tools-wrapup     (skill:create-tools @ wrap-up)
    └── … (31)
external
└── external-custom  [slice: host-custom] — record→local-consumption(不上送)
    └── ext-myteam-deploy-skill-wrapup (custom:myteam/deploy-skill @ wrap-up)
```

## 2. 模式二:处理已收集反馈(含打包后的清理)

```bash
fb --action status                         # 计数/阈值/legacy_remaining/external_count
fb --action list --slice commands --limit 0   # 按切片过滤(SC-004)
fb --action list --kind external --limit 0    # 外部条目单独过滤(SC-008)
fb --action package                        # 打包:仅内部条目;输出 excluded_external 计数
fb --action cleanup --package latest --dry-run   # 预览将清理的已打包条目
fb --action cleanup --package latest       # 清理:活跃库移除已打包条目,cleanup-log.md 留痕
```

对话路径:`/speckit.feedback 处理反馈` → agent 依次呈现状态/摘要 → 用户选择处置(标记/打包/清理/静默)→ 执行上列对应引擎调用。**手动投递 zip 后**由用户确认,再走 `mark-submitted` + `cleanup`。

## 3. 模式三:注入外部 probe

```bash
fb --action probe-inject --unit custom:myteam/deploy-skill --notes-file notes.md
# → 生成 .specify/memory/feedback/probes/ext-myteam-deploy-skill-wrapup.md
fb --action probes --format json | grep ext-   # 总览即刻可见
fb --action map                                # 重建结构图(含新外部对象)
```

随后该自定义 skill 的运行反馈按其嵌入步骤记录(或由 agent 以 `--unit-id custom:myteam/deploy-skill` 记录),条目 `kind=external`,永不进入上送包。

## 4. 结构图重建与漂移自检

```bash
fb --action map && fb --action map && diff <(git show:probe-map.md) probe-map.md  # 两次重建零差异(SC-003)
```

## 5. 旧格式迁移(一次性)

agent 整体 review 旧条目 → 产出处置计划(逐条 `id → delete|re-register`)→ 用户确认:

```bash
fb --action migrate-legacy --plan-file migration-plan.md   # 执行 + migration-log.md 留痕
fb --action status                                          # legacy_remaining: 0
```
