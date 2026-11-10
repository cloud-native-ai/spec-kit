# Feature 055: 冲突无关的 Feedback/Memory 存储(Conflict-Free Stores)

**Status**: Implemented(2026-10-08)
**Requirement**: `.specify/specs/055-conflict-free-stores/requirements.md`
**Origin**: 用户报告——client 项目中 `.specify/memory/feedback/index.json` 频繁引发 git 合并冲突;「尽可能不要使用统一文件来记录可能被多个流程同时更新的信息」。

## Overview

feedback 库与 memory 库(session/knowledge)此前都采用「逐条 .md + 单文件 index.json 镜像」的存储,每次 record 整文件重写 index(含易变 `updated` 时间戳)。多条分支各自 wrap-up 落条目时,任何两条分支的 index 写入必冲突——这是用户在下游项目反复撞到的痛点。本特性把两库存储拓扑改为冲突无关:

- **记录即文件**:条目 .md 本身是唯一记录(追加式,天然合并无关);内省报告同理(`introspection/*.md`)。
- **scan-on-read 唯一权威**:条目列表与内省花名册由扫描 frontmatter 派生,永不持久化;`count_since_submission`/`updated` 一律派生。实测 ~70 µs/文件,无需缓存。
- **每标量一文件**:feedback 库仅剩的三个可变标量各住一个微小 `state/` 文件(threshold/submitted-at/upstream-repo),缺文件=默认值;`record` 常规路径零 state 写入 → 并发 record 只触碰互不相交的文件。memory 应 index 本就 100% 派生,无 state/。
- **首写自动迁移**:旧 index.json 读取侧只读回退(`legacy: true`),任一可变动作首次写入时把标量落 state 后退役该文件并在返回值披露 `migrated: true`;`reindex` 兼作显式幂等迁移入口。
- **原子写**:`.part` + `os.replace` 覆盖全部写路径,失败时清理 `.part`。

## Key Changes

| 面 | 改动 |
|---|---|
| `scripts/python/feedback-utils.py` | 删 `save_index`/`empty_index`;新增 `scan_entries`/`scan_introspections`/`read_state`/`write_state_file`/`write_text_atomic`/`load_store_state`/`migrate_legacy_index`;8 个可变动作全部改扫描读写;`load_index` 保留名+形状(派生投影);`introspect-register` 停止维护 `introspections[]`;threshold 仅显式 `--threshold` 落盘 |
| `scripts/python/memory-utils.py` | `load_index(root, scope)` 保留名+形状改扫描(run-determination 进程内依赖零改动);删 `save_index`;record/recall/list/prune/reindex 改扫描;reindex 返回 `migrated` |
| `scripts/python/evidence-utils.py` | `collect_feedback_lane` 弃 index 解析改 `*.md` glob 主路径;`evidenceRefs` 改指最近条目文件 |
| `scripts/python/sanitize-utils.py` | C-7 改为「feedback/session/knowledge 的旧 index.json 存在=过期残留,repair 档,修复指向 reindex」;evidence 腿(C-8)不动 |
| `.specify/specs/045-sanitize-command/contracts/sanitize-detection-rules.md` | C-7 条款按 req 055 修订 |
| 测试 | 新增 `tests/contract/test_store_state_protocol.py`(13 例:迁移全字段/只读回退/幂等/并发隔离哈希证明/双分支 git 合并零冲突演示/原子性);更新 entry-schema/probe-cli/introspection/probe-entry/memory/run-determination/sanitize/evidence-lanes 等既有断言 |
| 文档 | `docs/reference/skills/feedback.md`(布局/threshold 语义/动作表)、`docs/reference/skills/memory.md`(布局/reindex)、`.specify/memory/tools/feedback-utils.py.md`(行为规则) |
| 本仓自迁移 | feedback 22 条 + session 4 + knowledge 6,三个 index.json 退役,state/ 落地 |

## Implementation Notes

- **返回形状稳定,仅增量键**:所有动作的既有键不动,新增 `migrated`(可变动作)/`legacy`(status);测试用 `>=` 子集断言,故安全。
- **「confirmed 不重开」不变量改由文件承载**:旧引擎靠 index.introspections 的影子 status;新引擎中报告文件自身即权威,非 confirm 的 register 不做任何 status 写入,语义等价。
- **双分支合并演示已进契约测试**:临时 git 仓两分支各 record 一条 → merge 零冲突、两条俱在——用户命名的痛点直接成为被测行为。
- **验证**:受影响面 362 测试全绿;全量回归 49 failed = master 干净基线实跑 48 + 特性绑定测试(等本行登记);`sync-mirrors --check` exit 0。

## Status Criteria / Evidence

- 契约套件 `tests/contract/test_store_state_protocol.py` 13/13 绿(含合并演示与迁移夹具)。
- 本仓 reindex 迁移后:三 index.json 消失、state/ 两个标量文件与旧 index 值一致(submitted_at=2026-10-06T18:35:50Z、threshold=10;upstream_repo 未设故不落盘)。
- `python3 scripts/python/sync-mirrors.py --check` exit 0。

## Known Residuals(见 requirements.md § Known Residuals)

1. threshold 持久化语义变化(仅显式 `--threshold` 落盘)——有意,文档已明示。
2. `.specify/memory/features.md` 相邻行与 054 并行分支的一次性手工冲突;治理文件本身仍是共享热点,超出存储层改造范围。
3. 迁移提交删除 index.json 与并行分支 append 在 git 层呈 modify/delete 冲突;语义上以「删除」为正解(新引擎扫描 .md 自愈,两边条目俱在)。
4. 同秒跨分支对同一 unit record 会撞文件名(既有属性;由「必然冲突(index)+ 偶发冲突(文件名)」收敛为仅偶发)。
