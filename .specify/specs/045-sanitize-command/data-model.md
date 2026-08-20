# Data Model: Sanitize Command(需求 045 / Feature 047)

**Requirement → Feature**: `045-sanitize-command` → Feature 047 Framework Material Hygiene

## 实体总览

5 个实体:Sanitize Finding(治理发现)、Sanitize Store(发现台账)、Cleanup Plan(清理计划)、Material Root(资料根)、Execution Report(执行报告)。前两者持久化于 `.specify/memory/sanitize/`,后三者为运行期对象(plan 文件落盘、root/report 为引擎内存态与输出信封)。

## 1. Sanitize Finding(治理发现)

台账中的一条待处理项。字段:

| 字段 | 类型 | 约束 |
|------|------|------|
| `id` | string(12-hex) | 稳定 ID = `sha1(category + "\|" + target)[:12]`;同一问题跨运行同 ID,合并语义的基础 |
| `category` | enum | `stale-residue` / `redundant` / `dead-reference` / `index-inconsistency` / `broken-symlink` / `mirror-drift` |
| `target` | string | 仓库相对路径(可含 `#anchor` 或 `:字段` 限定索引缺项) |
| `severity` | enum | `high` / `medium` / `low` |
| `summary` | string | 一行结论(摘要优先:不含原文大段引用) |
| `evidenceRefs` | list | 每项 `{kind: commit\|path\|output, ref}`;`stale-residue`/`redundant` 必填且至少含一条 commit 或 path 证据(FR-003) |
| `detection` | enum | `programmatic` / `semantic`(SC-004 度量锚点) |
| `disposition` | enum | 建议处置:`delete` / `archive` / `repair` / `delegate` / `dismiss` |
| `reversibility` | enum | `irreversible`(delete/archive)/ `reversible`(repair/delegate)——按 046 两级判据标注(FR-011) |
| `state` | enum | `pending` / `resolved` / `dismissed`(初始必为 pending,FR-012) |
| `firstSeenRun` / `lastSeenRun` | string(UTC ts) | 运行时间戳 |
| `resolvedAt` | string(UTC ts) \| null | 离开 pending 的时点 |
| `notes` | list[string] | 追加式备注(重开/自动收敛/处置留痕) |

**验证规则(源自需求)**:`evidenceRefs` 为空时 category 不得为 `stale-residue`/`redundant`;`target` 必须落在资料根白名单内(FR-006,引擎强制);`disposition=delegate` 时 summary 必须指名被移交命令。

**默认严重度映射**:`stale-residue`=high(误导性状态声明)、`redundant`=low、`dead-reference`/`index-inconsistency`/`broken-symlink`/`mirror-drift`=medium(未注册孤儿镜像 high)。检测器可按上下文上调,不得下调。

**状态机**:

```text
pending ──(处置执行成功)──▶ resolved
pending ──(用户否决该发现)──▶ dismissed
resolved ──(再次检出 = 回归信号)──▶ pending(追加重开备注)
dismissed ──(再次检出)──▶ dismissed(仅刷新 lastSeenRun)
```

自动收敛规则(引擎 merge 时判定,契约 C-2 钉死):pending 发现在本次运行中未再检出 → 自动置 `resolved`(note: "not re-detected this run")。这使外部修复(如经 /speckit.docs 修好死引用)在下次运行自然收敛,无需人工销账。

## 2. Sanitize Store(发现台账)

物理形态:`.specify/memory/sanitize/findings.json`,单一累积台账(对比 feedback 的 index+条目、evidence 的每运行一目录——两者均不满足"跨运行状态合并"语义)。

```json
{
  "version": 1,
  "updated": "<ISO-8601 UTC>",
  "findings": [ { ...Sanitize Finding... } ]
}
```

**写入纪律**:写入仅发生在 `collect`(确定性发现合并)与 `record`/`apply`(语义判定合并/状态更新);`status` 零写入。台账文件自身不属于被检材料(FR 递归豁免,Assumptions 已声明)。

**合并语义(按稳定 ID 匹配)**:

| 既有状态 | 本次检出 | 结果 |
|----------|----------|------|
| 无 | 新发现 | 追加,state=pending |
| pending | 再检出 | 刷新 lastSeenRun 与 evidenceRefs,保持 pending |
| pending | 未检出 | 自动收敛 → resolved |
| resolved | 再检出 | 重开 pending(回归信号) |
| dismissed | 再检出 | 保持 dismissed,刷新 lastSeenRun |
| dismissed/resolved | 未检出 | 原样保留(历史不删) |

**原子写**:`.part` 临时文件 + `os.replace`(沿用 038 P6 原子写纪律)。

## 3. Cleanup Plan(清理计划)

物理形态:`.specify/memory/sanitize/cleanup-plan.json`(每次检查运行整体重写;破坏性动作前置确认的确认对象)。

```json
{
  "created": "<UTC ts>",
  "confirmed": false,
  "items": [ { "findingId": "...", "disposition": "delete|archive|repair|dismiss", "target": "..." } ]
}
```

规则:`confirmed` 初始恒为 `false`;仅当用户在前置确认门控放行后由命令流程(agent)置 `true`;引擎 `apply` 见 `confirmed != true` 一律拒绝(退出码 2)。`delegate` 项不入计划(仅作移交建议呈现)。`delete`/`archive` 由引擎机械执行;`repair` 由 agent 在 apply 前完成内容修改、计划仅作状态更新依据;`dismiss` 仅状态更新。apply 成功后计划标记 `executed` 并保留至下次运行覆盖(审计痕迹)。

## 4. Material Root(资料根)

运行期探测对象,缺失视为空集(FR-002):

| kind | 候选路径 | 用途 |
|------|----------|------|
| memory-todo | `.specify/memory/todo/` | 时间性声明材料(语义判定输入) |
| memory-draft | `.specify/memory/draft/` | 同上 |
| memory-indexes | `features.md`+`features/`、`glossary.md`、`tools.md`+`tools/`、`feedback/`、`evidence/` | 索引↔存储一致性 |
| specs | `.specify/specs/`(排除 `.archive`)+ `.specify/archive/spec/` | 材料/归档引用 |
| history | `.specify/history/` | 材料引用 |
| mirrors | `skills/`↔`.specify/skills/`、`agents/`↔`.specify/agents/`、`shared/`↔`.specify/shared/`、`scripts/`↔`.specify/scripts/` | 镜像漂移 |
| compat-symlinks | `CLAUDE.md`、`QODER.md`、`AGENTS.md`、`.github/copilot-instructions.md`、`.github/skills` | 链接有效性 |
| docs | `docs/` 树 + 根注册文件 | 死引用(复用 docs-utils) |

自检豁免:`.specify/memory/sanitize/`(自身台账)。用户代码/脚本/测试目录永不入根(FR-006);引用解析只判定目标存在性,不构成评估。

## 5. Execution Report(执行报告)

`apply` 的输出信封(会话内呈现,046 三要素):

```json
{
  "executed": [ { "findingId": "...", "disposition": "...", "outcome": "ok|failed" } ],
  "artifacts": [ { "change": "deleted|archived|repaired|state-updated", "path": "..." } ],
  "failures": [ { "findingId": "...", "reason": "..." } ],
  "modifyPaths": [ "..." ]
}
```

失败如实报告:失败的处置不得静默跳过,已产生的中间产物逐项列出(FR-009)。

## 实体关系

Material Root(多)→ 扫描产出 → Sanitize Finding(多,经稳定 ID 并入)→ Sanitize Store(1 聚合);Cleanup Plan(0..1)引用 Finding 子集 → apply 消费 → Execution Report(0..1)+ 状态回写。
