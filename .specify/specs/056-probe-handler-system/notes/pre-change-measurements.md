# Pre-Change Measurements — 056-probe-handler-system

> T002 冻结（2026-10-13，implement 启动时全部重跑，非引用 tasks.md 旧值）。后续所有"零新增失败 / 无 NEW drift / 预算不变"对比以本文件为唯一改前锚。

## PM-1 编译单元面与 SC-007 行基线

```text
$ grep -l '^## Feedback' templates/commands/*.md | wc -l
23
$ grep -l '^## Feedback' skills/internal/*/SKILL.md | wc -l
35
$ grep -l '^## Feedback' skills/external/*/SKILL.md | wc -l
11
$ awk 'FNR==1{u++} /^## /{sec=($0~/^## (Feedback|Documentation)( |$)/)} sec&&NF{n++} END{printf "units=%d non-blank_lines=%d\n",u,n}' templates/commands/*.md
units=26 non-blank_lines=90
$ awk '…同规则…' skills/internal/*/SKILL.md
units=35 non-blank_lines=575
$ awk '…同规则…' skills/external/*/SKILL.md
units=11 non-blank_lines=188
```

- 编译单元集 = **69**（23 + 35 + 11）；SC-007 非空行基线 = **853**（90 + 575 + 188）。
- 陷阱注记：命令面 awk 扫 26 个文件（3 个无 `## Feedback` 贡献 0 行）；单元计数以 69 口径为准。

## PM-2 feedback-utils.py 动作封闭集（迁移前 14）

```text
$ grep -n 'choices=' scripts/python/feedback-utils.py | head -1
1936:        choices=["record", "status", "list", "dispose", "mark-submitted", "reindex",
```

（续行含 `"package", "cleanup", "upstream", "probes", "map", "migrate-legacy", "probe-inject", "introspect-register"`，共 14。迁移后：probe-utils.py 承载 probes/map/probe-inject + handlers/compile-embeds；feedback 收缩为 11。）

## PM-3 门控预算

```text
$ python3 scripts/python/scan-confirmation-gates.py
blocking confirmation gates: 23
  destructive: 16
  governance_kept: 7
violations (reversible gates still blocking): 0
```

## PM-4 probe 注册表

```text
$ python3 scripts/python/feedback-utils.py --action probes --validate
Probe registry valid: 6 classes, 72 internal + 0 external objects
```

## PM-5 镜像对

```text
$ python3 scripts/python/sync-mirrors.py --check
ok    skills/internal/ == .specify/skills/internal/ (133 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (106 files)
ok    shared/ == .specify/shared/ (46 files)
（templates 与 skills/external 对同为 ok，EXIT=0）
```

## 改前 failing-test 基线（templates/commands/implement.md § Test runs 口径）

- 命令：`scripts/bash/run-tests.sh --names-out .specify/specs/056-probe-handler-system/baseline-failed.txt`
- 实测（2026-10-13 UTC，108.07s）：**3598 passed, 0 failed**（3 warnings：PytestUnknownMarkWarning ×3，既有状况非本特性引入）
- 基线文件：`.specify/specs/056-probe-handler-system/baseline-failed.txt`（**0 条**）
- 判据形态：基线为空集 ⇒ 后续任何失败均为新增失败（绝对判据）；相界回归对比 `comm -13 baseline current` 必须为空。

## per-unit 差异矩阵（T019 实测，2026-10-13）

> 测量方法（program-first）：脚本枚举 `_embed_candidate_paths` 全集（26 命令 + 46 技能
> = 72 候选）+ H2 face 扫描 + 注册表 Objects 表 `unit → object_id` 解析（106 objects：
> 92 unit-facing + 14 script-facing）。69/69 单元均有注册 Object（reconcile zero-gap）。

### 面分布（实测）

- 单元全集 = **69**（23 命令 + 46 技能）；69/69 带 `## Feedback`；**22 带 `## Documentation`（全部命令面，技能面 0）**；0 个 doc-only；0 个既有 `## Wrap-up`。
- 手工 Feedback 段形态唯一：69/69 同一段式（canonical convention 指针段，仅 `--unit-id` 字面随单元变化；命令面 692–700 字符，技能面 866–876 = 段式 + runtime-mode gate 行）。
- **runtime-mode gate 行：46/46 技能齐备**（编译期 `_SKILL_GATE_LINE` 复刻，FR-013 变体保留）。
- 无反馈面命令 = `agents` / `constitution` / `feature` 3 个 → **结构性无面，非单元**，Q5 零段语义天然覆盖，**无需排除行**。
- `/speckit.history` = 唯一有 Feedback 而无 Documentation 的命令。
- 多 Object 单元 12 个（如 implement/instructions/sanitize/session/tools 并存 confirm-gate 类 Object）；docs-sync 行取各单元 command-wrapup 类 Object。

### handler 适用性（实测 → T020 落行依据）

| handler | 实测适用面 | 依据 |
|---------|-----------|------|
| h-feedback-record | `all`（69/69） | 69/69 均有反馈记录面 |
| h-threshold-notice | `all` | owner 链：threshold protocol = feedback-step.md step 6，随步执行；单元级 0 处独立接线 |
| h-token-reflection | `all` | owner 链：Token 效率自评内嵌于 Reflection procedure step 2 |
| h-run-determination | `all` | owner 链：feedback-step.md § Run Determination "Step 1 runs the engine's `determine` action at wrap-up"；improve 路径 2 处提及均为 `--action history` 读侧（why 步），非 wrap-up 接线 |
| h-docs-sync-eval | 22 命令单元（逐 object_id） | Documentation 面 = 22 命令（技能 0）；正枚举落行，免引擎扣减语义 |

### T020 落行裁定（实测更正 MVP 骨架）

1. h-run-determination：`complex-commands` → **`all`**（原骨架行依据"命令面复杂命令"的预判被实测否定——判定引擎经 owner 链在全部 69 单元的 wrap-up 生效）。
2. h-docs-sync-eval：`skills` → **作废，重落 22 条逐 `object_id` 行**（object 取各单元 `speckit-<stem>-wrapup`；`/speckit.history` 无 Documentation 面，不在列）。
3. **排除语义裁定**：实测矩阵零排除需求 → 引擎 additive 命中语义即实现态；data-model 编译算法第 2 步「扣减覆盖」按空排除集执行（no-op）；"排除"以更窄 scope 的正枚举表达。

### 引擎语义注记（供 T027 守卫设计）

零生效单元的编译会同时移除其手工 Feedback/Documentation 面（wrap-up 段位归编译所有）。当前矩阵下 69 单元均有生效 handler，该状态不可达；守卫设计时按「迁移完成态手工面重现 = 异常」处理（FR-016 唯一形态）。
