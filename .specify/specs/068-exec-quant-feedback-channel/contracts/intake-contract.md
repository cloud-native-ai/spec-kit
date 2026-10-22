# Contract: 接收腿（Intake — Path A 承接）

**Feature**: 068 | **File scope**: `scripts/python/feedback-utils.py`（新动作）+
`skills/internal/manage-feedback/` Path A 文档面 | **FR served**: FR-006 ~ FR-010
| **引擎动作**: `--action ingest-exec-quant --package <zip>`（新增）

## C-IN-01 动作签名与定位

- 新增 feedback-utils.py 动作 `ingest-exec-quant`，参数：`--package <zip 路径>`
  （必选）、`--workspace-root`（既有全局旗标）。
- 只处理包内 `exec-quant/` 载荷段；feedback 条目、introspection、SUBMISSION-NOTES
  零触碰（语义属既有 Path A agent 流程，FR-009）。
- 调用点：Path A A2 对每个入站 bundle 执行一次（技能文档面更新，零新增命令，
  FR-006）。

## C-IN-02 载荷识别与解出

- 以 zip 成员路径前缀 `exec-quant/` 识别载荷；无该前缀 → `record_count: 0`、
  exit 0（无载荷既有包行为零差异，FR-009）。
- `exec-quant/payload-manifest.json` 不可读或缺失：成员记录仍逐条尝试解出，
  动作计 `manifest_unreadable` 降级（非阻塞）；`identity` 缺失 → unknown-project
  分组，MUST NOT 从路径或内容猜测身份（FR-006 / Edge Cases）。
- 单条记录不可 `json.loads` 或 `kind != [[STR-001]]` → `skipped_unreadable` 计数，
  非阻塞（FR-010）。

## C-IN-03 归因与分组

- 归因取 `payload-manifest.json.identity`（C-PL-05）；`identity_status ==
  "unknown-project"` 或身份字段缺失 → 落字面 `unknown-project` 组。
- 分组目录：`aggregated/<source-slug>/records/`（data-model § E6；slug 规则同节）。

## C-IN-04 幂等身份键与去重

- `identity_key = sha256(source_project ␟ unit_id ␟ unit_type ␟ run_id ␟
  collected_at ␞ content_hash)`（␟ = `\x1f` 分隔，␞ = `\x1e`；canonical JSON
  sha256 为 content_hash；D6）。
- 去重窗口 = 全聚合层既有信封的 `identity_key` 集合；重复（同 key 同
  content_hash）→ 跳过 + `duplicates_skipped` 计数，零重复条目（FR-008）。
- 同 key 异 content_hash → keep-first + `identity_conflicts` 计数（D6）。
- 去重检查 + 写入 MUST 在一个 flock 临界区内（沿用 `append_record_locked` 形态，
  锁文件 `aggregated/.write.lock`），两流程并写零冲突（并发开发安全纪律）。

## C-IN-05 写入形态

- 信封文件 = data-model § E6；`record` 键封入解析后的源记录（字段级 verbatim，
  未知字段零丢弃，FR-007）；tmp+rename 原子写。
- 文件名沿用接收时刻 `entry_filename()` 形态（时间戳-uuid），与源名解耦
  （源名不保证跨包唯一）。
- exec-quant 记录 MUST NOT 进入 feedback store（`.specify/memory/feedback/`）
  ——059 FR-009 存储分界保留（FR-006）。

## C-IN-06 兼容归一（读取侧）

- schema v1/v2 并存、`{value, provenance}` 与裸 `[[STR-002]]` 并存、逐条目录与
  遗留流并存：接收侧不做字段补全，**归一发生在读取与派生视图**（FR-007 / A4）。
- 接收动作 MUST NOT 改写、补齐或丢弃源记录任何字段；未知字段原样进入信封。

## C-IN-07 降级计数与退出码

- 输出（`--format json` 缺省 JSON）MUST 含：`record_count`（本包载荷条数）、
  `ingested`（新写入）、`duplicates_skipped`、`skipped_unreadable`、
  `identity_conflicts`、`groups_touched`、`manifest_unreadable`（bool）。
- 「有降级但完成」exit 0；动作整体不可执行（`--package` 文件缺失、zip 无法按
  zip 打开、聚合层存储不可写）exit 2（D10）。
- feedback 条目处理 MUST NOT 因载荷问题受阻（FR-010）：本动作对 feedback 面
  零写零判。

## C-IN-08 接收不自动汇总

- `ingest-exec-quant` MUST NOT 触发 `aggregate`（FR-011 显式动作裁定）；Path A
  文档面把汇总列为**建议的显式后续步骤**，不并入接收流程。
