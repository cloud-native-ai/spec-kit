# Feedback 处理纪要 — 2026-07-22

- **来源**: `.specify/memory/feedback/` 自 2026-07-16 提交后累计的 14 条本地反馈（阈值 10 已触发）
- **处理人**: agent（本仓库即 Spec Kit 开发仓，"提交给开发者" = 就地分诊处置）
- **处置结果**: 3 项立即修复 + 11 项登记为结构性改进候选；引擎已 `mark-submitted` 归零计数

## 一、已立即修复（3 项）

| # | 反馈来源 | 问题 | 修复 |
|---|---------|------|------|
| 1 | 20260720 clarify | Feature Integration Protocol 引用不存在的 `feature-template.md`，clarify 建新 Feature 只能临场仿写 | `shared/workflow/feature-integration.md` 改指真实文件 `feature-details-template.md`（该死链在框架健康检查与 feature dogfood 中亦两次独立命中） |
| 2 | 20260720 requirements | requirements 命令「Feature Integration 节说本命令负责绑定」与「Outline 3/6 + Handoffs 说推迟到 clarify」自相矛盾 | 命令文本显式声明 Binding timing：本命令不建不绑，统一推迟到 `/speckit.clarify` 检查点 |
| 3 | 20260720 plan | `feature-ref.md` 只出现在 plan 模板的目录树里，命令正文 Phase 1 Output 未列，产出靠读者注意到 | Phase 1 Output 行显式加入 feature-ref.md 及其用途 |

同步范围：源文件 + `.specify/` 镜像 + 5 套运行时副本（claude/copilot/qoder/opencode/qwen）；`feature-template.md` 引用全仓清零；相关测试 13 passed，`-k "requirements or plan or feature"` 子集与基线一致（7 failed 均预存）。

## 二、登记为结构性改进候选（11 项，按主题聚合）

### 主题 A：模板对 doc/prompt-framework 特性的适配（4 条 → 最高频痛点）
- tasks-template 的示例任务与 Path Conventions 是 app 形状（models/services/endpoints），文档型特性每次都要人工重塑（20260716 tasks、20260720 tasks 两次独立命中）
- 建议：/speckit.tasks 检测 template-only/doc-feature 场景，切换到文档特性任务分类（author-section / mirror-parity / render-verify / refresh-verify）
- tasks 的 test-mode banner 规则应显式引用 Principle VII 的 template-only features 门（20260718 tasks）
- tasks-template 缺「dual-write + diff-verify」成对镜像任务的一等概念（20260716 tasks）

### 主题 B：镜像扇出自动化（2 条 → 本仓最大返工源）
- 命令模板一处修改需触达 4–6 个表面 × N 命令，纯手工同步（20260716 implement）
- 建议：提供从单一源模板重新生成各工具副本的 helper 脚本（本次 dogfood 中 qwen toml 被 git hook 归一化一事佐证已有部分生成机制，应显式化并覆盖全部表面）

### 主题 C：/speckit.implement 健壮性（3 条）
- 前置探测「可运行的 test runner」（venv 无 pytest 时静默假空基线）（20260716 implement）
- 新增文件到目录时主动 grep 脆弱的 count/枚举断言（20260716 implement）
- generate-instructions.sh 提供 render-only/dry-run 路径或让 tools 清单生成非致命、仓锚定（20260720 implement）
- 前置故事写入吞并后置故事内容时的「front-loading closure」显式模式（20260718 implement）

### 主题 D：命令小改进（2 条）
- requirements：起草前查看最高编号既有 spec 以对齐仓内惯例（20260718 requirements）
- clarify：Feature Binding 查找步骤加「查候选 feature 的兄弟 spec 绑定先例」启发式；plan.md 已存在时用户点名上游产物的 Mode 覆盖规则（20260718 clarify ×2）
- plan：$ARGUMENTS 扩需求范围时显式「spec-restructure first」子步骤（20260718 plan）

### 另附：本次 dogfood 新增的命令定义反馈（未入 feedback store，见会话报告）
- feature 命令：Action 7 列定义漂移（6 列 vs 实际 7 列）、name 字数约束矛盾（2–5 vs 2–4）、容忍带×明细清理交互未定义、README Feature List 范围指引缺失
- instructions 命令：Documentation Map 死行删除政策未定义（archive-not-delete 张力）、glossary 冲突的非交互 fallback、setup 脚本副产物清单不全

## 三、遗留

- 主题 A–D 均为模板/命令文本级改动，无运行时代码风险；建议后续以一个「命令模板体验改进」批次统一处理（A+B 优先）。
- rewrite_paths 贪婪重写 bug（research/agents 命令路径被误插 `.specify`）与 qwen TOML 生成格式问题此前已在框架健康检查中登记，不在本批重复。
