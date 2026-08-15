# Research Findings: Feedback 机制的 Probe 化重构 — 补充深究(零产出 probe vs 失效 probe)

> 定位:本文件为 `/speckit.research` 对 requirements.md **Edge Cases 第 149 行**单一问题的补充深究。该 spec 已有 plan/tasks(plan.md 的 Phase 0 选择内联研究、「No standalone research.md」);本文件不替代 plan,只裁定该开放边界问题的决策依据。生成时 spec 处于已实施状态(Feature 028 = Implemented,34/34 任务闭合)。

## Project Context Analysis

- 041 重构已落地:probe 真源 `shared/definitions/probe-definitions.md`(3 Class + 50 内部 Object),引擎 `feedback-utils.py` 7→13 动作(含 `probes --validate/--reconcile`、`map`、`cleanup`),`/speckit.feedback` 三模式命令已分发;本仓库 store 已完成 140 条旧条目收敛(`legacy_remaining=0`)。
- 关键现状事实(源码实测,本深究的证据基座):
  1. **probe-map.md 为纯定义派生物** — `--action map` 只从真源重建,内容仅含 Class→Object 层级与三类特征,当前**不含任何活性/产出标注**。
  2. **条目即运行回执** — canonical `## Feedback` 步骤(`.specify/shared/workflow/feedback-step.md`)规定干净运行也 MUST 记录一行哨兵文本 `No significant optimization points identified this run.`;因此「目标流程跑过且插点存活」在 store 中留有可程序判定的痕迹。
  3. **静默是合法状态** — 三类按设计的无声:trivial/no-op 跳过(gate 第 1 条)、abort 规则允许跳过记录、standalone runtime-mode gate;且 `cleanup`/`mark-submitted` 会把已打包条目移出活跃库(store 是滑动窗口,不是全量审计日志)。
  4. **结构死亡已有检测器** — `probes --reconcile` 做真源 ↔ 嵌入点双向零缺漏对账(exit 2 报缺口),可判定「插点被删/漂移」型失效。
- 约束:requirements Out of Scope 明确「不扩充新的收集语义」;FR-013/SC-003 钉死结构图的确定性(真源不变 → 重建零差异);红线零网络、条目 `scope: local`。

## References

- `.specify/specs/041-refactor-feedback-probe/requirements.md` — Edge Case L149(本问题)、FR-013、SC-003、Out of Scope、Edge Case L152(外部 probe 悬空)
- `.specify/specs/041-refactor-feedback-probe/plan.md` — Phase 0 内联研究、map 派生语义、Constitution Check VI「probe 零产出可观测」
- `.specify/shared/workflow/feedback-step.md` — 干净运行哨兵行、trivial/abort/runtime-mode 三类合法静默、dedup
- `.specify/memory/tools/feedback-utils.py.md` — `probes --validate/--reconcile`、`map` 确定性重建、`cleanup` 语义(Verified 工具记录)
- `.specify/memory/feedback/probe-map.md` — 当前派生图实样(无活性标注)
- `.specify/memory/feedback/index.json` — 条目字段实样(unit_id/probe/kind/slice/created/disposition)
- `.specify/memory/features.md` — Feature 028(Implemented)与 036(Loop A/B)依赖核对,无冲突
- 外部参考:无(本次为仓库内证据深究,零外部网络源)

## Decisions & Rationale

### 零产出 probe 与失效 probe 的区分:三态观测模型(仅用既有工件,零新遥测)

- **Decision**: 以「证据来源」划界,把边缘问题拆为三个可程序判定的观测态:
  1. **零产出-存活(zero-output, alive)** — 该 probe 在活跃 store 有 ≥1 条条目;特别是全部条目正文为哨兵行 `No significant optimization points identified this run.` 的 probe(稳定字面量,可精确匹配,符合 Program-First 纪律)。流程在跑、插点在收,只是没有可报的优化点 —— 这是**健康静默**。
  2. **失效(dead)** — 结构性断裂:真源里的 Object 在嵌入面无对应 `## Feedback` 步骤(或反之)。由既有 `probes --reconcile` 双向零缺漏对账判定,无需新机制。
  3. **休眠(dormant)** — reconcile 零缺漏但活跃 store 零条目:如实标注为「本工作区未观测到活动」,是**观测陈述而非裁决** —— 因为合法静默(trivial 跳过 / abort 跳过 / standalone gate / 条目已被打包清理)都可能造成零条目,不可判死。
- **Rationale**: feedback-step.md 已强制干净运行也落哨兵条目,故「条目存在性」天然是运行回执,免费充当心跳;Out of Scope 禁止扩充收集语义,排除新增遥测;reconcile 已覆盖结构死亡检测。三态全部由现有真源 + store 派生,零新增存储。
- **Alternatives considered**: (a) 独立心跳 ping 条目 —— 否决:违反 Out of Scope 且污染 store、抬高阈值计数;(b) 探查目标单元最近运行时间戳 —— 否决:跨单元脆弱判断,超出反馈层职责;(c) 零条目直接判失效 —— 否决:与 abort/trivial/cleanup 的合法静默冲突,必产误报。
- **Impact**: 仅读侧逻辑;为下一条 map 标注决策提供状态语义;不触碰引擎写路径与条目 schema。

### 结构图标注落位:map 保持纯定义派生,活性标注放模式一总览的渲染时 join

- **Decision**: `--action map` 维持**仅从真源派生**(FR-013/SC-003 的零漂移契约原样成立);「零产出/休眠/失效/悬空」标注在 `/speckit.feedback` 模式一(probe 总览)渲染层完成 —— 渲染时以 Object 标识 join 活跃 store(`index.json`),逐 Object 附观测徽标:`active[n]` / `dormant[0]` / `dead(reconcile gap)` / 外部 probe 另有 `dangling(target unit missing)`(对应 Edge Case L152,标注不误报损坏)。
- **Rationale**: FR-013 钉死「真源不变时两次重建 MUST 零差异」;若把 store 计数写进 map,则真源不变、store 新增条目时两次重建产出不同 → 直接违反 SC-003 的可程序判定确定性。且 store 是滑动窗口(cleanup/mark-submitted 移出已打包条目),写进 map 的活性数据会随打包静默腐化。渲染时 join 让同一份真源渲染同时回答结构三问与活性观测,且活性数据始终实时取自 store。
- **Alternatives considered**: (a) 活性计数嵌入 map 正文 —— 否决:破 FR-013/SC-003,且打包后腐化;(b) 独立 liveness 报告文件 —— 否决:多一份派生物要对账,违反对「单一派生视图」的收敛意图;(c) 只在模式二状态视图呈现 —— 否决:模式一才是边缘问题所指的「结构图如何标注」的结构性视图。
- **Impact**: 真源、map 契约、条目 schema 均零改动;模式一总览增加一个渲染列(标注明确声明为 store 派生观测,非真源字段);引擎为只读 join 扩展,无写路径变化。

## Open Questions & Risks

- **滑动窗口限制**: 已打包/清理的条目离开活跃库后,`dormant` 判定的置信度随时间下降。倾向接受为观测边界(徽标语义是「当前库内未观测到」);若需更强证据,后续可选 join `packages/` 内 MANIFEST —— 留待需要时裁定,本次不做。
- **trivial 与从未运行不可区分**: 不新增遥测的前提下,「流程从未被触发」与「触发但按规则跳过记录」在证据上同构。这是 Out of Scope 约束下的固有极限,建议在模式一徽标文案中如实表述,不做裁决。
- **外部 probe 悬空的判定源**: dangling 依赖对 `custom:<owner>/<name>` 目标单元存在性的检查,命名/路径约定需在模式三注入契约中保持稳定(已有 edge case L152 跟踪)。
- **阈值计数交互**: 哨兵条目计入 `count_since_submission`(现状即如此);若三态标注被消费后出现「希望哨兵不计入」的诉求,属新决策点,需回到 028 域内裁定,本深究不预支。
