# US3 Quickstart Walkthrough — T026（2026-10-13）

> 抽样单元：`/speckit.analyze`（复杂命令，含 docs-sync 评估面）。路线：quickstart.md
> Scenario 1 步骤序 + Scenario 3/4 实跑 + 收尾流程引擎调用沙箱执行。与 T002 改前证据
> （pre-change-measurements.md）逐项比对。引擎调用全部进**沙箱存储**（mktemp 工作区），
> 零真实存储污染。

## 1. 编译形态实跑（Scenario 1 落地证据）

- T020 注册行落位 → `handlers --point wrap-up --validate` exit 0（5 handlers / 26 bindings）。
- T021 `compile-embeds`：69 units → 69 written, 0 unchanged；第二次运行 0 written /
  69 unchanged（byte-identical）；`--check` exit 0（zero drift）。
- T024 `regen-command-copies.py` + `sync-mirrors.py` → `--check` 双绿。
- `grep -n '^## Wrap-up' templates/commands/implement.md` 命中（quickstart 步骤 5 判据）。

## 2. 收尾流程执行（编译段调用链，沙箱存储）

对 `/speckit.analyze`（command face）按编译段行序执行：

| 步 | 命令（编译段形态 + 引擎必填申报） | 结果 |
|----|-----------------------------------|------|
| 1 | `run-determination.py --action determine --unit-id "/speckit.analyze" --unit-type command --run-id t026-walkthrough --complexity complex --qualification qualified --workspace-root <sandbox>` | exit 0；`trigger_feedback: false`；落 `session/…-run-determination-speckit-analyze-t026-walkthrough.md` |
| 2 | `feedback-utils.py --action record --unit-id "/speckit.analyze" --unit-type command --notes … --review … --points "No significant optimization points identified this run." --run-id t026-walkthrough --workspace-root <sandbox>` | exit 0；`should_prompt: false`；落 `feedback/20261013T…-speckit-analyze.md` |
| 3–5 | threshold-notice / token-reflection / docs-sync-eval（agent handler） | 锚点在位：`feedback-step.md` § "Threshold prompt protocol…"、§ "Reflection procedure…"、`docs-step.md` § "Evaluation procedure…"（FR-007 锚点校验由 validate 钉住） |

**引擎必填申报注记**：编译段调用行是 kind 固定派生的**最小形态**（FR-020 裁定）；
引擎运行时的 caller-declaration 必填项（determine 的 `--run-id`/`--complexity`/
`--qualification`，record 的 `--review`/`--points`）由 agent 依引擎自身 `--help` 补齐
——行为真源（feedback-step.md § Run Determination）明文禁止把旗标清单抄进 prose，
故编译段不展开它们。两引擎均接受 `--unit-type`（help 实测），调用行形态与引擎契约一致。

## 3. Quickstart Scenario 3/4 实跑

- Scenario 3：`agents` / `constitution` / `feature` → `grep -c '^## Wrap-up'` = **0/0/0**（Q5 零段）。
- Scenario 4：probe-utils choices = `{probes,map,probe-inject,handlers,compile-embeds}`（5）；
  feedback-utils choices = 11 项；`probes --validate` = 9 classes / 106 objects，exit 0。

## 4. GATE-5 手工段清零

- `grep -rl '^## Feedback|^## Documentation'` 于命令模板 + 技能面（69 单元全集）→ **0 文件**。
- AUTO-GENERATED 横幅命中 **69/69**；`## Wrap-up` 命中 **69/69**。
- 既有例外（登记于 T019 矩阵）：`templates/skills-template.md` 保留手工占位段——它不是
  编译单元（占位 unit-id），新技能注册后由编译接管。

## 5. 与 T002 改前证据逐项比对

| 项 | 改前（T002/PM） | 改后（本次实测） | 判定 |
|----|-----------------|------------------|------|
| 单元全集 | 69（23 cmd + 35 int + 11 ext） | 69（面扫描同口径） | 一致 |
| 手工段形态 | 69/69 canonical 指针段 + 46/46 gate 行 | 0 手工段；69/69 编译段（gate 46/46 保留） | 迁移达成（FR-016） |
| 引擎动作封闭集 | 14（合并计） | 5 + 11 = 15（probe 族 + handlers/compile-embeds） | PM-2 预期演进 |
| 门控预算 | total 23 / violations 0 | total 23 / violations 0（test 钉住） | 一致（PM-3） |
| 注册表 | 6 classes / 72 objects | 9 classes / 106 objects（US1 入册 + Handler 章） | PM-4 预期演进 |
| 镜像对 | 全 ok | 全 ok（sync --check exit 0） | 一致（PM-5） |
| SC-007 收尾面非空行 | 853（PM-1 awk 口径，含跨文件渗漏） | **413**（per-file 严格口径；test_wrap_up_line_budget 钉 ≤853） | Token 显著偏优 |
| 测试基线 | 3598 passed / 0 failed | 3704 passed / 0 failed；`comm -13 baseline current` = ∅ | 零新增失败 |

## 6. 结论

迁移完成态成立：加机制 = 注册一行 + 重编译 + 固定次序传播；漂移由 `--check` exit 1
先行；零生效单元保持无段；措辞零 BLOCKING 命中且门控预算不动。编译段为唯一收尾形态
（模板占位段除外，已登记）。
