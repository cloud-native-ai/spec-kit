# Feature Reference: 062 Humanize Command（人性化改写命令）

**Feature ID**: 062 | **Feature Name**: Humanize Command（人性化改写命令）
**Requirement**: `.specify/specs/062-humanize-command/requirements.md`（Requirement → Feature 绑定：本规格 ↔ Feature 062 自身，1:1）
**Status at plan time**: Draft → Planned（本 plan 落盘后推进）

## FR → 设计映射

| FR | 条款 | 主要设计落点 | 契约 |
|----|------|--------------|------|
| FR-001 | C-1, C-2 | 薄命令模板（[[STR-001]] 身份）+ 单技能委派 | command-surface.md |
| FR-002 | C-11 | 四维度完整性（无跳过分支） | rewrite-behavior.md |
| FR-003 | C-12 | 语气与风格自然化 | rewrite-behavior.md |
| FR-004 | C-13 | 上下文补全边界（蕴含范围内） | rewrite-behavior.md |
| FR-005 | C-14 | 格式与可读性优化 | rewrite-behavior.md |
| FR-006 | C-15, C-10 | 降低 AI 痕迹 + 检测器诚实措辞 | rewrite-behavior.md, command-surface.md |
| FR-007 | C-16, C-3 | 保真底线（最高优先级）+ 技能体落点 | rewrite-behavior.md, command-surface.md |
| FR-008 | C-17, C-33 | 受保护内容逐字保留 + frontmatter 文件级实例 | rewrite-behavior.md, tone-input-file.md |
| FR-009 | C-18 | 最小改动 | rewrite-behavior.md |
| FR-010 | C-19 | 矛盾保留与报告 | rewrite-behavior.md |
| FR-011 | C-20 | 完整性（不静默截断） | rewrite-behavior.md |
| FR-012 | C-21 | 完整改写文本为主要输出 | rewrite-behavior.md |
| FR-013 | C-22 | 语言保持 | rewrite-behavior.md |
| FR-014 | C-24 | 缺省语气 `professional` | tone-input-file.md |
| FR-015 | C-25, C-3 | 封闭语气集合 + 自由文本受众（[[STR-002]]） | tone-input-file.md, command-surface.md |
| FR-016 | C-26 | 语气不覆盖保真 | tone-input-file.md |
| FR-017 | C-27 | 集合外语气值拒收 | tone-input-file.md |
| FR-018 | C-28 | 单输入源 + 空内联拒收 | tone-input-file.md |
| FR-019 | C-29 | 文件格式与路径解析（[[STR-003]]） | tone-input-file.md |
| FR-020 | C-30, C-3 | 默认不写文件 + 技能体落点 | tone-input-file.md, command-surface.md |
| FR-021 | C-31 | 显式输出路径 + 覆盖确认 + 失败报告 | tone-input-file.md |
| FR-022 | C-32 | 输出格式跟随输入 | tone-input-file.md |
| FR-023 | C-20 | 长文档跨章节一致与重组 | rewrite-behavior.md |
| FR-024 | C-1, C-2, C-3 | 薄入口、单一技能、技能体自足 | command-surface.md |
| FR-025 | C-4, C-5, C-6, C-7 | 按工具副本、docs 页、注册行、编译面 | command-surface.md |
| FR-026 | C-9, C-23 | 确定性契约测试 + 行为评估协议 | command-surface.md, rewrite-behavior.md |
| FR-027 | C-5, C-10 | 文档义务 + 检测器诚实措辞 | command-surface.md |
| FR-028 | C-8, C-34 | 零新增运行时 + 数据不外传 | command-surface.md, tone-input-file.md |

映射完整性：FR-001..FR-028 共 28 条全部被条款正文引用（`clause_blocks` 逐条款检索实跑：covered 28 / missing NONE，2026-10-19）。

## SC → 验证映射

| SC | 验证方式 | 证据落点 |
|----|----------|----------|
| SC-001 | E8 语料（≥8 样本）+ `rubric.md` 两位独立评审量规判定 | verification.md（实现期） |
| SC-002 | 确定性差异脚本逐项比对（invariant set 改变数=0、编造数=0、蕴含标注） | verification.md + 差异脚本输出 |
| SC-003 | 语言矩阵夹具复核 + 受保护 token 清单比对 | verification.md |
| SC-004 | 语气矩阵（同夹具 ×4 语气 + 缺省）两位评审区分度判定 | verification.md |
| SC-005 | 临时目录文件行为测试：逐字节哈希、目录快照、覆盖确认与错误分支断言 | 契约测试运行记录 + verification.md |
| SC-006 | 长文档样本章节对应性检查 + 未处理部分报告断言 | verification.md |
| SC-007 | 命令面清点（模板/4 副本/docs/注册行）+ `regen-command-copies.py --check` | quickstart S1 判据 + 契约测试 |
| SC-008 | `comm -13 notes/baseline-failed-tests.txt <新名单>` 为空；两处下游钉扎测试（C-9：`test_feedback_command_classification.py` 分类表含 humanize=Simple、`test_skill_layer_visibility_guards.py` 外部技能普查 +1）复跑绿；镜像触碰对绝对字节一致、不触碰对零 NEW drift（C-4） | notes/baseline-failed-tests.txt（71 条冻结名单）+ verification.md |
| SC-009 | 模板/技能/docs/输出全量文本检索逐条核对检测器措辞 | 契约测试（test_c10）+ verification.md |
| SC-010 | 依赖清单差异 + 新增网络调用检索 + 无网络环境演练声明 | verification.md |

**交付面清单（17 项，实现期按此对账）**

```text
templates/commands/humanize.md                    # 新增：薄命令模板（源，sanitize/derive 先例形态；Simple → 无 Wrap-up）
.claude/commands/speckit.humanize.md              # 生成：regen-command-copies.py（禁手改）
.github/prompts/speckit.humanize.prompt.md        # 生成：同上
.opencode/command/speckit.humanize.md             # 生成：同上
.qoder/commands/speckit.humanize.md               # 生成：同上
skills/external/humanize/SKILL.md                 # 新增：执行技能（源，external 分类）
.specify/skills/humanize/SKILL.md                 # 镜像：sync-mirrors 平铺对（--only 特性限定同步）
shared/definitions/probe-definitions.md           # 增强：skill-humanize-wrapup 单元行 + 绑定行（源；命令侧零单元）
.specify/shared/definitions/probe-definitions.md  # 镜像：shared 对（基线已漂移 → 同步后绝对字节一致）
docs/reference/commands/humanize.md               # 新增：逐命令参考文档（C-5 内容义务）
.specify/specs/027-feedback-mechanism/contracts/command-classification.md  # 增强：humanize=Simple 行 + Result 计数（C-1）
tests/contract/test_humanize_command_surface.py   # 新增：结构契约测试（C-1..C-10 钉扎）
tests/contract/test_feedback_command_classification.py  # 更新：钉扎 Simple 数 3 → 4（C-9；基线名单中无此节点）
tests/contract/test_skill_layer_visibility_guards.py    # 更新：EXTERNAL_SKILLS + humanize、平铺计数 13 → 14（C-9）
tests/fixtures/humanize/                          # 新增：评估语料 + rubric.md + 确定性差异脚本（E8）
.specify/memory/features.md                       # 状态推进：Draft → Planned（本 plan 已落）
.specify/memory/features/062.md                   # 状态推进 + Latest Review 记录（本 plan 已落）
```

**不触碰**（C-8 边界），除上表明确列出的 027 分类契约与两个既有测试文件外：`src/specify_cli/`（分发机制按原样消费）、`scripts/` 既有引擎、其他 `/speckit.*` 命令模板、其余既有技能、`.specify/templates/`（commands 镜像已退役，模板不落镜像）。

## 基线记录（2026-10-19 实测，实现期相对判据的参照）

| 基线 | 结果 | 留痕 | 实现期判据 |
|------|------|------|-----------|
| 生成面 `regen --check` | 零漂移 | notes/baseline-regen-check.txt | 新副本落位且其余副本零变化 |
| 镜像 `sync-mirrors --check` | 209 条既有 DIFF；触碰对 `shared/definitions/probe-definitions.md` 在列（第 181 行），`skills/external/humanize` 为新增对 | notes/baseline-mirror-check.txt | 不触碰对零 NEW drift（相对）；触碰对同步后绝对字节一致 |
| 编译面 `compile-embeds --check` | 73/73 旧指纹可再生漂移（= 23 Complex 命令 + 50 技能）；`--unit` 不限定范围 | notes/baseline-compile-check.txt、notes/baseline-compile-unit-no-scope.txt | 新增 `skill:humanize` 单元落位带当前指纹；既有 73 单元零新增归因（相对） |
| 测试套件 | 71 failed / 3929 passed | notes/baseline-failed-tests.txt（71 条排序名单） | `comm -13` 为空（零新增失败节点） |
| 需求校验器 | exit 0，0 error / 0 warning | quickstart S6 | 实现期复跑仍 exit 0 |
