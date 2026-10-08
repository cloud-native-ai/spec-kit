# Requirements Specification: 冲突无关的 Feedback/Memory 存储(Conflict-Free Stores)

**Requirement Branch**: `055-conflict-free-stores`
**Created**: 2026-10-08
**Status**: Draft
**Input**: User description: "在其他项目中使用 speckit 经常会遇到 .specify/memory/feedback/index.json 文件导致的 git 合并冲突, 需要针对这一点做优化, 尽可能不要使用统一文件来记录可能被多个流程同时更新的信息."

**用户裁定(2026-10-08,三项约束)**:① 改造范围 = feedback 库 + memory 库同轮(evidence 库无维护型索引,不受影响);② 存量过渡 = 首次写入自动迁移(写侧落地 state/ 后删除 index.json 并在返回值披露 `migrated`;读取侧对旧 index.json 只读回退、绝不再写);③ 治理 = 登记特性 055 直接实现,本规格为轻量记录(不走完整 SDD 仪式)。

## Related Feature *(mandatory)*

**Feature ID**: 055
**Feature Name**: 冲突无关的 Feedback/Memory 存储(Conflict-Free Stores)

绑定依据:新建 Feature 055。候选归属核验——028(Feedback Mechanism)拥有反馈**流程**(probe/路由/打包),本需求改其**存储拓扑**,且同轮改 memory 库(memory-utils 属 038 Memory System 世系),横跨两个既有 Feature 的存储层;以交叉引用(消费关系)记入 `features/055.md`,不构成归属。先例:052 的「投递载体不是归属事实」同理——存储层是共用底座,不是任一流程的特性。

## Overview

客户端项目中,`.specify/memory/feedback/index.json` 是 git 合并冲突热点:多条分支/多个会话各自在 wrap-up 落反馈条目,而引擎每次 `record` 都**整文件重写**该 JSON(含易变 `updated` 时间戳),任何两条分支的写入必冲突。memory 库(`session/`、`knowledge/` 每 scope 一个 index.json,每次 `memory-record` 同样整文件重写)是同款问题。本仓实测 `session/index.json` 只登记 4 条而盘上有 8 个 .md——镜像已经在撒谎。

核心事实:两个库的 index 中 `entries[]`/`introspections[]` 100% 可由逐条 .md frontmatter 派生(两引擎现有 `reindex` 动作即证明);真正的独占标量只有 feedback 库的 `threshold`、`submitted_at`、`upstream_repo`(memory 库一个都没有)。扫描成本实测约 70 µs/文件 → scan-on-read 可行,无需缓存。

**目标存储**:

```
.specify/memory/feedback/
  <YYYYMMDDTHHMMSSZ>-<unit-slug>.md   # 不变:记录本体(追加式,天然合并无关)
  introspection/<report-id>.md        # 不变:内省记录
  state/threshold.json                # {"threshold": N}   — 仅显式设置时存在
  state/submitted-at.json             # {"submitted_at": "..."}
  state/upstream-repo.json            # {"upstream_repo": "..."}
.specify/memory/{session,knowledge}/  # 无 state/;迁移 = 删 index.json
```

## Requirements

### FR-001 布局不变量(需求原句的直接落地)
多流程并发更新的信息 MUST NOT 落在任何共享可变文件中。`record` 的唯一写目标 MUST 是新条目 .md 文件(追加);MUST NOT 触碰 `state/`。每标量一个微小文件,缺文件 = 默认值(threshold 10 / submitted_at None / upstream_repo None)。

### FR-002 scan-on-read 唯一权威
`entries[]` 与 `introspections[]` MUST 由扫描 .md frontmatter 派生,永不持久化;`count_since_submission` 与 `updated` 一律派生。不做缓存。无 frontmatter 的记账文件(backlog/cleanup-log 等)由现有 reindex 跳过行为天然排除。

### FR-003 标量 state 文件语义
`threshold` 仅在显式 `--threshold`(record/reindex)与存量不同时持久化到 `state/threshold.json`——env/CLI 解析值不再被 record 顺手持久化(**有意的行为变化**,写入文档)。`submitted_at` 由 mark-submitted 原子写;`upstream_repo` 由 `upstream --set` 原子写。所有写走 `.part` + `os.replace` 原子模式。

### FR-004 首写自动迁移 + 披露
存量项目的旧 `index.json` 在任一可变动作(record/dispose/mark-submitted/reindex/upstream --set/cleanup/migrate-legacy/introspect-register;memory 的 record/prune/reindex)首次写入时迁移:动作自身写入落地 → 标量落成 state 文件(仅非默认值)→ 删除 index.json → 返回值增量披露 `"migrated": true`。`reindex` 兼作显式迁移入口且幂等。

### FR-005 遗留只读回退
`index.json` 在场时,读取侧把它当**只读回退源**(state 文件优先),置 `"legacy": true`,MUST NOT 删除或改写——过渡期内混合版本机器(旧引擎)可能重建它。

### FR-006 CLI 面与返回形状稳定
两引擎动作集、旗标、退出码、返回形状保持稳定,仅允许增量键(`migrated`/`legacy`)。`load_index` 的名字与返回形状 MUST 保留(run-determination.py 进程内调用 memory 引擎的 `load_index`;tests/unit/test_feedback_package.py 进程内调用 feedback 引擎的同名函数)——实现改为派生,签名不变。`save_index` 删除。

### FR-007 sanitize 残留规则
sanitize C-7 对 feedback/memory 家族的检查改为:对应 `index.json` 存在 = 过期残留,**suggestion 档**(混合版本过渡期合法重建,只提示不自动删),修复指向 `reindex`。evidence 家族(C-8,无维护型索引)不动。契约文本 `.specify/specs/045-sanitize-command/contracts/sanitize-detection-rules.md` 同步修订。

### FR-008 消费方扫描化
evidence-utils `collect_feedback_lane` 弃 index 解析,以 `*.md` glob 为主路径;有 ≥1 条目文件即 lane available;`evidenceRefs` 不再指向 index.json,改指最近条目文件。trigger-utils(stdout-only)与 run-determination(经保留的 `load_index`)零代码改动。

## Known Residuals(如实登记,非本特性范围)

1. **threshold 持久化语义变化**(FR-003):此前 env/CLI 值会被 record 顺手持久化;现在仅显式 `--threshold` 持久化。已在文档明示。
2. **features.md 相邻行冲突**:本特性自身的登记行与 054 并行分支在 `.specify/memory/features.md` 存在一次相邻行文本冲突(治理文件仍为共享热点,超出了存储层改造的范围)。
3. **合并时的 modify/delete**:迁移提交删除 index.json,与并行分支上的 append 在 git 层面表现为 modify/delete 冲突;语义上以「删除」为正解(新引擎扫描 .md 自愈,两边条目俱在),已记入 `features/055.md`。
4. **去重竞态**:两并发 record 同 `(unit_id, run_id)` 的 read-then-write 竞态为既有残留(无锁),本特性未引入新风险(残留风险 ≤ 现状)。
5. **同秒跨分支同名文件**:条目文件名为秒粒度时间戳 + unit-slug(不含 run_id);两条分支在同一秒内对同一 unit 各 record 一条,会在 git 层产生 add/add 文件名冲突。此为**既有属性**(旧体系同样存在,且旧体系还叠加必然的 index.json 冲突);现实多人/多机工作流中同一秒同 unit 的概率可忽略。本特性将其从「必然冲突(index)+ 偶发冲突(文件名)」收敛为「仅偶发冲突(文件名)」。
