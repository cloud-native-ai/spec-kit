# Feature Reference: `079-humanize-run-output` → Feature 062

**Requirement branch**: `079-humanize-run-output`
**Bound Feature**: 062 — Humanize Command（动作输出人类友好化）
**Binding kind**: 扩展（extension），不是新 Feature
**Status contract**: Feature 062 MUST 保持 `Implemented`（FR-029）；本阶段（plan）不做状态迁移

---

## 1. 绑定事实

| 事实 | 值 | 来源 |
|------|-----|------|
| Feature ID | 062 | requirements § Related Feature |
| Feature 详情 | `.specify/memory/features/062.md` | requirements FR-029 |
| Feature 索引行 | `.specify/memory/features.md` 062 行 | requirements FR-029 |
| 首个规格 | `.specify/specs/062-humanize-command/requirements.md` | 062 详情 `## Related Specifications/Requirements` |
| 本规格 | `.specify/specs/079-humanize-run-output/requirements.md` | requirements 头 |
| 绑定裁决 | clarify 2026-10-30（改名/描述更新，状态不回退） | requirements § Clarifications |

一个 Feature 承接两个规格是宪法 VII 的 **Feature reuse-first** 形态（many-specs-to-one-feature）：
062 提供内容模式的既有能力与评估资产，079 把同一命令重定位为「先执行、后报告」。**没有新建 Feature**
的理由是：命令身份、技能身份、docs 页与评估语料都是同一套；另立 Feature 会把一个命令拆成两条互相
竞争的登记线。

## 2. 本 plan 对 Feature 062 的映射

| 062 既有资产 | 079 的动作 | 结果 |
|--------------|-----------|------|
| 命令语义（文本改写） | 入口语义改为「裸文本 = 指令」；改写改为显式入口 | 破坏性变更 + 迁移提示（FR-005） |
| 技能工作流（四维度改写） | 保留原样，成为**内容模式**分支 | 不回归（FR-023） |
| 技能（单一技能承载） | 同一技能新增**运行模式**分支 + `references/` 细则 | 仍为单一技能（FR-026） |
| 五节报告 | 新模式新增；内容模式不生成 | FR-018, FR-024 |
| 评估语料 `tests/fixtures/humanize/` | 历史语料不改写；新增 `run/` 运行夹具 | A11, WC-15 |
| Feature 详情 / 索引 | 追加扩展记录，状态保持 `Implemented` | FR-029 |

## 3. 本阶段（plan）实际落到的登记面

- `features/062.md`：`## Latest Review` 追加 plan 扩展记录；`## Key Changes` 追加扩展条目。
- `features.md` 062 行：`Last Updated` 追加 plan 扩展标记（名称/描述已在 clarify 阶段对齐为「动作输出人类友好化」）。
- 状态列：保持 `Implemented`，不写 `Planned`。

## 4. 阶段产物与需求的对应

| 产物 | 承接 |
|------|------|
| `plan.md` | 技术路线、宪法检查、决策张力、镜像义务、Phase 1 汇总 |
| `data-model.md` | 8 实体 + 26 条校验规则；运行状态机；信封与报告映射 |
| `contracts/invocation-parse.contract.md` | FR-001…FR-006、FR-030（入口态） |
| `contracts/execution-dispatch.contract.md` | FR-007…FR-013、FR-030（嵌套） |
| `contracts/report-assembly.contract.md` | FR-014…FR-022、FR-024 |
| `contracts/content-mode.contract.md` | FR-023…FR-025（不回归 + 共存） |
| `contracts/wiring-compat.contract.md` | FR-026…FR-029 + A2/WC-19 |
| `quickstart.md` | SC-001…SC-010 的可执行验收路径 |

## 5. 不在本特性范围

- 新命令、新技能、新派发机制、新确认门（FR-027）。
- 内容模式的改写质量、语气取值域、文件写入规则的变更（FR-004, FR-023）。
- 历史记录、062 的既有规格与评估语料的改写（A11）。
- 远程/外部 CLI 派发（EX-04 明确排除）。
