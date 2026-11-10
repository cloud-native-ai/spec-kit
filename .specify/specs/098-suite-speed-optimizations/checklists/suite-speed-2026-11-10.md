# Requirements Quality Checklist: 098 套件提速五项优化的可判据保持（checklist 轮）

**Purpose**: 对 098 规格做一次「需求写作的单元测试」：确认五条优化各自的速度收益都以**可判据保持**为前提（不得缩小选择、跳过、宣告 flaky、重试到绿），并逐面检查 slow 成员判定、缓存失效、注入时钟、进程内直调边界与 086 契约兼容在需求文本中是否可判定。
**Created**: 2026-11-10
**Feature (Requirement Scope)**: [086-efficient-test-execution](../../../features/086-efficient-test-execution.md)（098 为其后续项；状态不回退）
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[contracts/](../contracts/) —— 仅用于发现需求缺口与歧义，不作为评审对象。

**Note**: 本清单由 `/speckit.checklist` 生成，测试的是需求文本的质量（完整性、清晰性、一致性、可测性、覆盖、边界、依赖、歧义），不是实现行为。逐项回答后勾选；对原清单的作答 **MUST NOT 就地改写**，按追加式复核另建 `checklists/recheck-<date>-<topic>.md`，作答条目逐字引用被回答的需求行与其锚点。

## 判据保持与禁止捷径 (Criterion Preservation & Forbidden Shortcuts)

- [ ] CHK001 - Is "宣告 flaky"（把不稳定测试宣告为 flaky 而不修复）defined as a decidable violation class with a named detection surface, given the Overview forbids it but FR-021's closed shortcut list does not include it? [Gap, Req §Overview / §FR-021]
- [ ] CHK002 - Does the forbidden-shortcut check cover non-decorator forms of skip/xfail/retry（函数体内 `pytest.skip()`、条件跳过、手写重跑至绿循环），or only newly added decorators as SC-010's measurement source states? [Coverage, Req §SC-010 / §FR-021]
- [ ] CHK003 - Are "无上限 worker 数" and "随机丢参" each given a decidable detection surface（worker 数的具名上限；丢参的可比较口径），rather than remaining prose prohibitions? [Ambiguity, Req §FR-021]
- [ ] CHK004 - Is "缩小参数化" measured with a defined comparison unit and scope（逐文件 parametrize 条目数前后对比），and does the check fail on any decrease rather than only on decorator removal? [Clarity, Req §FR-021 / §SC-010]
- [ ] CHK005 - Do SC-002 and SC-003 apply the same convention for pre-existing failures（SC-003 写明"既存失败按名称相等处理"，SC-002 只写双向差为空而无该条款）? [Consistency, Req §SC-002 / §SC-003]
- [ ] CHK006 - Is the anti-measurement in SC-004（"把慢档重新并入缺省档时读数应回退"）a pass/fail criterion or an observation — and if a criterion, what regression magnitude counts? [Measurability, Req §SC-004]

## slow 分档与成员判定 (Slow Tier & Membership)

- [ ] CHK007 - Is "少数" in FR-006 quantified or otherwise bounded（成员数的上限或占比上限），so membership growth cannot silently shrink the default tier while still being "disclosed"? [Ambiguity, Req §FR-006]
- [ ] CHK008 - Is "integration 类测试" defined by directory, by marker, or by behaviour — and is a process-boundary test living under `tests/contract/` eligible or excluded as a slow member? [Ambiguity, Req §FR-006]
- [ ] CHK009 - Is the classification rule defined for a test that satisfies both member classes at once（process-boundary 与 corpus-scan 同时成立）? [Gap, Req §FR-006]
- [ ] CHK010 - Is the disclosure arithmetic of FR-024（"披露的排除数 = 本次选择内的 slow 成员数"）well-defined for `tier=caller`, where slow members inside the caller's selection are selected rather than excluded and the disclosed count is 0? [Conflict, Req §FR-024 vs §FR-007 / §FR-009]
- [ ] CHK011 - Is FR-024's clause "[[STR-003]] 时…收集集合回到全量" conditioned on "no caller `-m`", given FR-009 makes the caller's single `-m` own the selection even under `--full`? [Conflict, Req §FR-024 vs §FR-009]
- [ ] CHK012 - Are the machine-consumed literals this feature introduces（登记册类别值、运行形态行新增字段 `tier=` / `excluded_slow=`）pinned to a single owner in the spirit of the Shared Strings convention, since守门测试逐字消费它们? [Gap, Req §Shared Strings / §FR-024]
- [ ] CHK013 - Is the member-removal procedure defined（一条已标记测试不再满足判据时由谁更新登记册，孤儿行规则如何强制它发生）? [Completeness, Req §FR-024]
- [ ] CHK014 - Is the caller-`-m` detection surface defined — command-line spellings only, or also a selection supplied via pytest configuration (`addopts`) — so the "no two competing `-m`" prohibition is decidable for downstream projects running the shipped runner? [Ambiguity, Req §FR-009]

## 会话缓存失效 (Session Scan Cache Invalidation)

- [ ] CHK015 - Is FR-025's cache key complete for deciding entry identity — the design adds `root` and `variant` to（会话，worker，受管扫描面）；are those components owned by the requirement? [Gap, Req §FR-025]
- [ ] CHK016 - Are "受管扫描面" and "框架根文件" enumerated in requirements（哪些语料、哪些根文件），so "each surface built once" is decidable without design lookup? [Ambiguity, Req §FR-012 / §FR-025]
- [ ] CHK017 - Is a detection surface required for FR-013's writer-consumption prohibition（守门如何发现一个改写被扫描树的用例消费了共享缓存）? [Gap, Req §FR-013]
- [ ] CHK018 - Is the in-session freshness rule stated without implying order dependence（不写被扫描树的消费者看到的只能是会话起点快照，只有跨会话重建才观察当前内容）? [Clarity, Req §FR-025]

## 注入时钟与事件等待 (Injected Clock & Event Waits)

- [ ] CHK019 - Is the sleep-scan scope closed in requirements — FR-016 names "runner 相关测试" without an enumerated file set, while FR-017's zero-count claim depends on that scope? [Ambiguity, Req §FR-016 / §FR-017]
- [ ] CHK020 - Is the exemption registry's carrier and row schema（文件、行、理由、日期）specified in requirements, so the scan guard can consume it? [Gap, Req §FR-017]
- [ ] CHK021 - Does the spec state the permissible non-test surface — may the injected clock be a new option on a shipped engine, or must it stay test-side — given A12's out-of-scope list is silent on product-code changes? [Gap, Req §FR-015 / §A12]
- [ ] CHK022 - Is "承担同步或顺序语义的 `time.sleep`" given a decidable classification rule against real-time-semantics sleeps（如 TTL），beyond case-by-case exemption judgement? [Clarity, Req §FR-017]
- [ ] CHK023 - Is the claim that the 30-second deadline "与既有 runner 测试约定一致" validated against the shared wait helper's current default（tasks 阶段实测 5 秒），and is changing that shared default stated as an intended behaviour change? [Assumption, Req §FR-026 / §A16]

## 进程内直调边界 (In-Process Conversion Boundaries)

- [ ] CHK024 - Is the completeness denominator of the conversion manifest defined in requirements — the counting unit（调用点 vs 源码行 vs helper）and the census population（`tests/` 含 fixtures 与 conftest 的 AST 扫描）? [Gap, Req §FR-019]
- [ ] CHK025 - Is the keep-priority rule explicit and exhaustive（"任一保留类成立即保留，其余才转换"），including what to do with a call that fits no listed class yet cannot be converted? [Clarity, Req §FR-027]
- [ ] CHK026 - Is "转换 MUST NOT 弱化断言" made decidable — what comparison of assertions before/after counts as equivalent — given SC-009 demands "同一断言集合全绿" while FR-027 allows assertion forms to change to CliRunner-equivalent results? [Conflict, Req §FR-019 / §SC-009 / §FR-027]
- [ ] CHK027 - Is the classification unit for helper wrappers defined（每个 wrapper 一行还是每个被包裹调用点一行），so manifest completeness is countable? [Gap, Req §FR-019]
- [ ] CHK028 - Does FR-027's enumeration of retained boundary classes include every class the design relies on — the design's closed set adds `copy-topology`，which FR-027 and A11 do not name? [Gap, Req §FR-027]

## 086 契约兼容与 runner 接口 (086 Contract Compatibility)

- [ ] CHK029 - Is "前缀兼容" defined with a decidable invariant（既有字段的位置与拼写不变、新增字段只在尾部追加、分隔符与既有解析不受影响），rather than as a metaphor? [Clarity, Req §FR-023]
- [ ] CHK030 - Is "C-001…C-016 的条款文本 MUST NOT 被重开或改写" made checkable（如 086 契约文件在 diff 中不变），or left as intent? [Measurability, Req §FR-023]
- [ ] CHK031 - Is "驱动者文档" in FR-010 identified by an owner path, so the two-slot `--full` update is traceable to a named file? [Traceability, Req §FR-010]

## 度量、一致性与假设 (Measurement, Consistency & Assumptions)

- [ ] CHK032 - Is the measurement method for "运行期子进程调用数" defined（动态调用计数 vs 静态 AST 普查），so the same figure is reproducible? [Ambiguity, Req §FR-020]
- [ ] CHK033 - Is the wall-clock comparison's tolerance for run-to-run variance defined（单次运行还是重复测量）for the SC-004 50% and SC-005 110% thresholds? [Measurability, Req §SC-004 / §SC-005]
- [ ] CHK034 - Is the sleep-census baseline reconciled across artifacts — §Overview records "20 处（8 个文件）" while the tasks-stage re-derivation records 20 occurrences in 10 files — and does A6 decide which reading acceptance uses? [Consistency, Req §Overview / §A6]

## Notes

- Items are checked only when the requirement text (or a requirement-owned pointer) answers them; an item answered only by a design artifact is recorded as a requirement-level gap reference, not as resolved.
- Recheck answers land in a new `checklists/recheck-<date>-<topic>.md` file, quoting the answered requirement line with its anchor; this file stays as history.
- Traceability: 34/34 items carry a requirement reference or an explicit `[Gap]` / `[Ambiguity]` / `[Conflict]` / `[Assumption]` / `[Consistency]` marker.
- Focus clusters requested by the run: 判据保持（不得缩小选择/跳过/flaky/重试）· slow 成员判定 · 缓存失效 · 注入时钟 · 进程内直调边界 · 086 契约兼容。
- Depth: Standard · Audience: Reviewer（默认值，未被参数覆盖）。
