# Feature Reference: 072-client-self-improvement

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement）

## 1. Binding

- Feature ID / Name: 072 / 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement）
- Bound at: `/speckit.requirements`（阶段简报授权的绑定时点偏离，记录于 spec Assumptions A2）
- Spec: `.specify/specs/072-client-self-improvement/requirements.md`（29 FR / 7 SC / 6 user stories / 10 Shared Strings）
- Status after this stage: `Draft → Planned`（本阶段完成转换；`Implemented` 属 `/speckit.implement`）

## 2. Delivery surface

| 面 | 文件 | 承载 |
|----|------|------|
| 评审命令模板 | `templates/commands/review.md` | `--client-unit` 参数透传、第五步指针、结论披露 |
| 评审技能 | `skills/internal/code-review/SKILL.md` | 非交互路径四步→五步（唯一修订面）、采集与披露规则 |
| 评审脚本 | `skills/internal/code-review/scripts/git-delta-review.sh` | `capture` 子命令；`report --summary --format json`（可选） |
| 反馈命令模板 | `templates/commands/feedback.md` | 客户侧消化/载体/度量呈报指针 |
| 反馈技能 | `skills/internal/manage-feedback/SKILL.md` + `references/path-a-digest.md` | 载体闭集指派、呈报三项事实 |
| 改进命令模板 | `templates/commands/improve.md` | `custom:` 主体路由（既有承认，补客户观察源指针） |
| 自我提升技能 | `skills/internal/self-improvement/SKILL.md` | why 段客户观察源规则 |
| 共享 owner | `shared/workflow/self-improvement-workflow.md`、`shared/guidelines/dogfooding.md` | SI-1 观察源规则 + 披露字面量；Loop B 配方改写 |
| 反馈引擎 | `scripts/python/feedback-utils.py`（+ `.specify/scripts/` 镜像） | 只读 `client-metrics` 动作 |
| 命令参考 | `docs/reference/commands/{review,feedback,improve}.md` | 同步面 |
| 契约测试 | `tests/contract/test_client_{capture,armed_state,package_exclusion,improve_loop,metrics}.py` | 五组行为（FR-029/SC-006），全部新建、只增不改 |

引擎/台账/命令/评分/依赖：零新增（`client-metrics` 与 `capture` 是既有引擎上的两个有界面，C-62）。

## 3. FR coverage

| FR | 条款 | FR | 条款 |
|----|------|----|------|
| FR-001 | C-1, C-13 | FR-016 | C-37 |
| FR-002 | C-2…C-6, C-9 | FR-017 | C-38 |
| FR-003 | C-7 | FR-018 | C-39 |
| FR-004 | C-8 | FR-019 | C-40 |
| FR-005 | C-10, C-11 | FR-020 | C-41, C-42, C-49, C-60 |
| FR-006 | C-12, C-13 | FR-021 | C-43…C-45, C-49, C-50 |
| FR-007 | C-15…C-18 | FR-022 | C-46, C-47, C-62 |
| FR-008 | C-18…C-20 | FR-023 | C-45, C-48, C-50 |
| FR-009 | C-3, C-4, C-14, C-21…C-23 | FR-024 | C-51, C-52 |
| FR-010 | C-25, C-31 | FR-025 | C-53, C-54, C-61 |
| FR-011 | C-26, C-27, C-30 | FR-026 | C-6, C-11, C-55, C-62 |
| FR-012 | C-28 | FR-027 | C-9, C-36, C-56, C-62 |
| FR-013 | C-29, C-30, C-32 | FR-028 | C-57 |
| FR-014 | C-33 | FR-029 | C-52, C-58…C-60 |
| FR-015 | C-34…C-36 | | |

29/29 FR 均被条款引用组覆盖（`account-clause-coverage.py` FR lane 核验见 test-evidence）。

## 4. SC coverage

| SC | 条款 | 验证载体 |
|----|------|----------|
| SC-001 | C-12, C-15…C-20 | `test_client_capture.py`（计划） |
| SC-002 | C-2…C-6, C-14, C-19, C-21…C-23 | `test_client_armed_state.py`（计划） |
| SC-003 | C-1, C-8, C-13, C-25, C-28, C-31, C-32 | `test_client_package_exclusion.py`（计划） |
| SC-004 | C-33…C-35, C-38, C-39 | `test_client_improve_loop.py`（计划） |
| SC-005 | C-41, C-43…C-50 | `test_client_metrics.py`（计划） |
| SC-006 | C-57, C-58, C-59, C-61 | 五组测试的红先行记录 |
| SC-007 | C-10, C-17, C-24, C-53, C-61 | 071 既有钉 + 新结构断言 |

## 5. Disclosed deviations & adjudications（本阶段裁决，实现期不得再发明）

1. **运行标识**（R2/C-18）：取记录头日期戳，不取收尾运行判定 id。
2. **计数机读面**（R3/C-17）：`report --summary` 新增可选 `--format json`，既有文本与退出码字母表不动。
3. **`--client-unit` 字面量**（R5/C-6）：参数名与值语法；畸形值 = 具名 skip 行 + 零条目 + 不阻断。
4. **框架帽披露形态**（R6/C-13）：`skipped: <帽子依据句>`，不属于五值闭集、不伪装成五值之一。
5. **度量载体**（R7/C-47）：既有反馈引擎的只读 `client-metrics` 动作，口径锁定于 C-43…C-50。
6. **闭环/重复的机械口径**（R7/C-44, C-45, C-50）：owner 文件存在 + mtime 晚于条目 `created`；(文件,严重度) 对从所指记录抽取；不可读记录同排除并披露。
7. **夹具构造**（R8/C-59）：临时 git 仓 + 最小安装 `.specify/`，帽子谓词双向覆盖（客户夹具 + 框架帽孪生）。

## 6. Non-regression statement

071 的六个新套件、`test_expression_compatibility.py` C-5 冻结哈希、`test_review_p1_review_loop.py`、feedback/probe 契约族：本计划只增不改（C-61）。071 闭合面唯一授权修订 = 步骤枚举四步→五步（C-10），其余逐字保留（C-53）。
