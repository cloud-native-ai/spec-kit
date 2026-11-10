# Analyze Findings — W1（096-sdd-observer-agent）

- **Wave**: W1 / analyze 并发波（第二轮：修复后重过门；detection-only，只读变体）
- **Line / Run**: `096-sdd-observer-agent` / `r20261110T081104Z-b096`
- **Round**: 2（full severity set；重判 round-1 findings + 全量检测）
- **Read domain**: `.specify/specs/096-sdd-observer-agent/requirements.md`（下称 `requirements.md`）、`.specify/specs/096-sdd-observer-agent/checklists/2026-11-10-observer-requirements-quality.md`（下称 `checklist.md`）
- **重判输入（lane-local evidence，非跨波读域）**: `test-evidence/analyze-findings-W1.md`（round 1 被本文件取代）、`test-evidence/analyze-validation-wave.txt`（round-1 C/H 校验裁决）、`test-evidence/analyze-repair-dispositions-2026-11-10.md`（修复处置）
- **Authority**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md`；`.specify/constitution.md`（1.19.0）
- **Write surface**: 仅本文件与 Wrap-up 记账；未修改任何制品，未做修复
- **Passes executed**: A duplication · B ambiguity · C underspecification · D constitution alignment · E coverage（requirements↔SC/AS 内部）· F inconsistency · G feature linkage（名称级）· H checklist accountability；I decision tension 不在本波读域（judged object 仅 `plan.md`）
- **Severity basis**: `detection-and-severity.md` § Severity assignment（`propagation_surface` 决定上限；`none` 封顶 MEDIUM）
- **Boundary note**: `plan.md` / `contracts/` / `data-model.md` / `tasks.md` 不在本波读域；下游是否已消解某条 finding 由合并波按跨制品证据裁定（W1-01 的 round-1 降级即此类裁定先例）

## Rerun delta（round 1 → round 2）

| Prior ID | R1 severity | R1 verdict | R2 status | Round-2 handling |
|----------|-------------|-----------|-----------|------------------|
| W1-01 | HIGH | downgrade → MEDIUM | open | 以 **MEDIUM** 重报（缺陷 `requirements.md:181` 未修复；校验波认定下游无八类传播） |
| W1-02 | HIGH | confirm HIGH | fixed | 关闭；复核 FR-009/FR-013/FR-020/SC-001/SC-007 文本已按收束写入义务对齐。残余无 journal 分支另立 W1-22 |
| W1-03 | HIGH | reject（Appendix A） | rejected | 不重报（校验波：基线已由 plan T-005 / tasks T003、T033 / DoD-6 具名落地） |
| W1-04 … W1-18 | MEDIUM ×12, LOW ×3 | 未校验（仅 C/H 过校验波） | open | 以原 ID 重报（修复轮未处置；本轮按当前文本逐条复核仍成立） |
| W1-19 … W1-22 | — | — | new | 本轮全量检测新发现 |

Counts: round-1 18 条 = fixed 1 + rejected 1 + persisted 16；round-2 新增 4；round-2 有效 findings 20。

## Findings（round 2，full severity）

| ID | Severity | Pass | Anchor | Fact（一句话事实） | Propagation surface | Suggested disposition（指针） |
|----|----------|------|--------|--------------------|---------------------|------------------------------|
| W1-01 | MEDIUM | F inconsistency | `requirements.md:181`; `requirements.md:142`; `checklist.md:36`; `checklist.md:72` | FR-011 规定条目恰好承载九类信息，而 Key Entities 的 Journal Entry 仍称「承载八类信息」，同一制品对同一封闭字段集给出两个计数；round-1 校验波以「下游 plan/data-model/contracts/tasks 均按九类落地、无下游传播」降级 MEDIUM，但缺陷本身未修复。 | `none`（下游已按九类落地，round-1 校验证据） | `/speckit.requirements`（Key Entities 改为九类或引用 FR-011） |
| W1-04 | MEDIUM | C underspecification | `requirements.md:129`; `requirements.md:195` | FR-004 以 `line_id` + spec key 派生实例身份，但全文未定义 spec key 的派生来源、唯一性范围与 owner，身份函数不可求值，SC-005 的「两个不同实例身份」缺可判定函数。 | plan 身份模型 / driver 修订 / SC-005 测试 | `/speckit.clarify`（定义 spec key 派生与 owner） |
| W1-05 | MEDIUM | C underspecification | `requirements.md:160` | FR-023 规定入口声明键 `observer: on\|off`，但「入口声明」的载体、位置、解析格式与 owner 均未定义，关闭开关无法被实现方无歧义解析。 | driver U0 解析 / plan | `/speckit.clarify`（绑定入口声明载体与解析规则） |
| W1-06 | MEDIUM | C underspecification | `requirements.md:145`; `requirements.md:192` | FR-014 要求证据指针携带「留存类别」并在线收束时可解析，SC-002 以「可解析」为判据，但留存类别词表与可解析判定（存在 / 类型 / 版本历史可达）未定义为受拥有的封闭集合，也未覆盖工作树清理后的时点。 | plan checker / 测试夹具 | `/speckit.clarify` + `/speckit.plan`（留存类别封闭词表与可解析判定） |
| W1-07 | MEDIUM | F inconsistency | `requirements.md:135`; `requirements.md:136` | FR-007 规定上一执行 `.status` 未结算时 driver MUST NOT 派发下一个，FR-008 又允许失败 / 停滞 / 窗口到期后在阶段边界重启；执行崩溃且未留 `.status` 时既未结算又已结束，两条规则互斥。 | driver 派发逻辑 / plan | `/speckit.clarify`（裁定未结算执行的结算或超时规则） |
| W1-08 | MEDIUM | F inconsistency | `requirements.md:128`; `requirements.md:141`; `requirements.md:158` | FR-003 禁止不同线共享 journal、FR-010 按 spec 目录落一份 journal，但全文未排除两条线（含嵌套运行）解析到同一 spec 目录的状态，该状态下路径冲突且「不共享」无法成立。 | plan 路径模型 / 双线夹具 | `/speckit.clarify`（排除或消歧同 spec 双线状态） |
| W1-09 | MEDIUM | C underspecification | `requirements.md:144`; `requirements.md:160` | FR-013 未裁决缺口窗口的三种边界：零长度窗口（起止同秒）写入还是抑制、连续多个缺口的起点链、以及 `state=disabled` 无启动时间时的起点回退值。 | plan 缺口写入 / checker / 测试 | `/speckit.clarify`（缺口窗口边界裁决） |
| W1-10 | MEDIUM | B ambiguity | `requirements.md:194`; `requirements.md:52` | SC-004(c) 要求 checker 拒绝「自由叙述条目」，但需求层未给出自由叙述的结构定义，反例构造只能回落到 checker 自身判定，存在循环判据风险。 | plan 客观性夹具 / checker | `/speckit.clarify`（自由叙述的结构定义） |
| W1-11 | MEDIUM | B ambiguity | `requirements.md:142`; `requirements.md:144` | FR-011 的 `命令` 字段允许「原文或 `-`」，但原文取自哪个载体、字符集 / 长度如何约束均未定义，评价或建议文本可借这个自由文本字段进入条目，与 FR-013 客观性构造冲突。 | plan journal 格式 owner / driver | `/speckit.clarify`（命令字段来源与内容约束） |
| W1-12 | MEDIUM | B ambiguity | `requirements.md:144` | FR-013 以「限定为」引出观测输入清单，但未声明该清单是否穷尽，也未指名新增载体的 owner，其他制品引入的 meta 包络是否可读不可判定。 | plan 读域实现 / 定义文本 | `/speckit.clarify` + `/speckit.plan`（封闭清单与扩展 owner） |
| W1-13 | MEDIUM | C underspecification | `requirements.md:150`; `requirements.md:88` | FR-016 把写面界定为 journal 与「自身执行运行产物」，但 US4 AS1 的写面审计未定义锁文件 / 游标 / 临时文件的归属，而 FR-007 的单写者协议需要协调状态。 | plan 写面声明 / tasks | `/speckit.plan`（写面枚举与审计规则） |
| W1-14 | MEDIUM | E coverage gap | `requirements.md:252` | 「journal MUST NOT 被加入任何阶段 required artifact 集或 `STAGE_ARTIFACTS` 映射」只存在于 Assumptions A12，既无 FR 承载也无带红腿的 SC。 | plan / tasks（红腿） | `/speckit.requirements`（提升为 FR）→ `/speckit.tasks` |
| W1-15 | MEDIUM | F inconsistency | `requirements.md:129`; `requirements.md:141`; `requirements.md:234`; `requirements.md:247` | FR-004 与 A7 把身份第四项写作「执行 label」，FR-010 与 clarify 记录写作「实例 label」；journal 跨多次执行只有一份头部，而派发 label 每次执行不同，头部字段语义悬空。 | plan 头部 schema / 模板 | `/speckit.clarify`（头部 label 字段定名与取值） |
| W1-16 | LOW | H completeness | `requirements.md:126` | FR-001 的 MUST NOT 覆盖 stage executor / reviewer / reporter 三个席位，但三者没有指向定义 owner 的引用，禁令无法按同一谓词独立核对。 | 定义文本 | `/speckit.requirements`（补 owner 引用） |
| W1-17 | LOW | A duplication | `requirements.md:137`; `requirements.md:141`; `requirements.md:144`; `requirements.md:191`; `requirements.md:194`; `requirements.md:197` | FR-009、FR-010、FR-013、SC-001、SC-004、SC-007 在 `[[STR-00N]]` 标记旁同时复制了字面量，违反本制品自设的「用 `[[STR-NNN]]` 代替复制字面量」约定（FR-010 路径语句中的文件名属位置定义，可从宽）。 | requirements 文本 | `/speckit.requirements`（仅保留 token） |
| W1-18 | LOW | B ambiguity | `requirements.md:113`; `requirements.md:142` | Edge Cases 称「checker 以文件序判定非递减」但未点名判定对象（序号还是观测时间），与 FR-011 的序号单调递增并列时存在两种读法。 | plan checker | `/speckit.clarify` 或 `/speckit.plan`（点名判定对象） |
| W1-19 | MEDIUM | F inconsistency（新） | `requirements.md:195`; `requirements.md:104`; `requirements.md:135`; `checklist.md:41` | SC-005 与 US5 AS2 把同线第二个并发执行的期望写成「被拒绝或串行化」，而 FR-007 规定 driver MUST NOT 派发且引擎 MUST 以单写者协议拒绝第二 writer；验收判据未收敛为恰一个可观测结果（CHK023）。 | driver 派发 / SC-005 测试 / tasks | `/speckit.requirements`（与 FR-007 对齐为单一可观测结果） |
| W1-20 | MEDIUM | E coverage gap（新） | `requirements.md:133`; `requirements.md:195`; `checklist.md:13` | FR-005 的「唯一机械判据」依赖 `line 已登记` 与 `U2 派发` 两个无 owner 引用的谓词，而 SC-005 只断言「首个 journal 条目早于首个阶段完成条目」，该弱代理无法证明「U2 派发前启动」（CHK001）。 | driver 启动步骤 / SC-005 测试 | `/speckit.requirements`（补谓词 owner 引用与判定动作）+ SC 红腿 |
| W1-21 | MEDIUM | E coverage gap（新） | `requirements.md:134`; `requirements.md:146`; `requirements.md:152`; `requirements.md:153`; `requirements.md:158`; `requirements.md:189` | FR-006（承载模态）、FR-015（脚本接口契约）、FR-018（不发用户可见汇报 / 提问 / 审批）、FR-019（triplet 引用不复制 / 不新造通道）、FR-021（非 SDD 命令与非 SDD team 运行不产生 observer / journal）均无对应 SC 或 Acceptance Scenario 红腿。 | tasks 验收夹具 / contracts | `/speckit.requirements`（补 SC/AS 红腿）→ `/speckit.tasks` |
| W1-22 | MEDIUM | F inconsistency（新） | `requirements.md:191`; `requirements.md:137`; `requirements.md:111` | SC-001 的失败线覆盖判据在「线在 observer 启动前即失败、按 Edge Cases 允许无 journal」分支不可满足（既无阶段开始条目也无 `observer-gap` 条目），判据未引用 FR-009 的无 journal 回退。 | 验收测试 / SC-001 | `/speckit.requirements`（SC-001 增补无 journal 分支回退引用） |

## Checklist Accountability（`[Gap]` 项）

清单 `checklist.md` 共 38 项、仍全部未勾选；其中 `[Gap]` 标签 7 项，逐项处置如下（与 round 1 一致，本轮复核仍成立）。

| CHK | Anchor | Disposition |
|-----|--------|-------------|
| CHK002 | `checklist.md:14` | raised-as-finding W1-04 |
| CHK003 | `checklist.md:15` | raised-as-finding W1-05 |
| CHK004 | `checklist.md:16` | raised-as-finding W1-13 |
| CHK005 | `checklist.md:17` | raised-as-finding W1-06 |
| CHK008 | `checklist.md:20` | covered-by requirements.md § FR-001（`agents/sdd-observer.agent.md` 模板即角色面单一 owner） |
| CHK009 | `checklist.md:21` | raised-as-finding W1-16 |
| CHK036 | `checklist.md:63` | raised-as-finding W1-14 |

```
CHK002 disposition: raised-as-finding W1-04
CHK003 disposition: raised-as-finding W1-05
CHK004 disposition: raised-as-finding W1-13
CHK005 disposition: raised-as-finding W1-06
CHK008 disposition: covered-by requirements.md § FR-001
CHK009 disposition: raised-as-finding W1-16
CHK036 disposition: raised-as-finding W1-14
```

`unchecked[Gap]=7 · raised=6 · covered-by=1 · unraised=0 · undispositioned=0` → 阻断计数 **0**。

非 `[Gap]` 项中本轮新吸收：CHK001→W1-20、CHK018→W1-01、CHK023→W1-19；其余材料性缺陷已由既有 finding 按锚点吸收（CHK011→W1-07、CHK013→W1-11、CHK014→W1-10、CHK017/CHK019→W1-09、CHK020/CHK021→W1-08、CHK027→W1-03（rejected，下游具名基线））。剩余项在需求文本中已有可引用答复，不另立 finding（CHK010→FR-007/FR-008 + A4 具名参数；CHK012→FR-009/FR-020；CHK015/CHK016→FR-011 + A8 格式 owner；CHK022→FR-004 的 §状态脊 owner 指针；CHK024→FR-015 单一引擎 + FR-016 写面审计；CHK025→FR-013 + A10；CHK026→SC-003；CHK028→SC-007 + FR-013/FR-009；CHK029→W1-21；CHK030→FR-009 收束义务；CHK031→Edge Cases + FR-023；CHK032→Edge Cases 五路失败载体分配；CHK033→FR-022 + FR-013（扩展 owner 问题见 W1-12）；CHK034→US5 AS3 + A10；CHK035→FR-002 具名词表 + A2；CHK037→FR-018 枚举；CHK038→W1-04/W1-08）。

## Coverage / Registry / Constitution Summary

- **E pass（内部覆盖）**: requirements ↔ SC/AS 覆盖已检测（W1-20/W1-21/W1-22）；requirements ↔ tasks 的跨波覆盖不在本波读域，`account-clause-coverage.py` 固定步由合并波执行（round-1 先例）。
- **I pass（decision tension）**: 判定对象仅为 `plan.md`，不在 W1 读域 → 本波 N/A。
- **G pass（feature linkage / registry）**: `Related Feature` 声明 Feature ID `096` 与名称「SDD 专用观察者与线级观察记录（sdd-observer）」，与清单 `checklist.md:5` 一致；本轮实测 `.specify/features.md` 与 `.specify/features/096.md` 均存在（存在性核对，2026-11-10）。索引行与详情文件的内容级阶段记录义务超出 W1 读域，标为 `not_evaluated`，不据此立 finding。
- **D pass（constitution alignment）**: 两份读域文件中未发现宪法 MUST 冲突（0 CRITICAL）。复核：A5（journal 单文件 vs 指令层 Concurrent Development Safety）由用户点名单文件路径优先且 A5 已记录裁定理由，非宪法冲突；A10（Test-First Partial）只限定 LLM 行为面，确定性面已声明走契约测试，与宪法 IV / VII 相容；A12 的规范义务缺口按 W1-14 计 finding，不升级为宪法冲突。
- **Zero-finding floor**: 不适用（findings 非空）。

## Metrics

- Findings: **20**（CRITICAL 0 · HIGH 0 · MEDIUM 17 · LOW 3），上限 50 内，无 overflow。
- Rerun delta: fixed 1（W1-02）· rejected 1（W1-03，Appendix A 保留）· persisted 16 · new 4。
- C/H 独立校验：本波 C/H = 0，无需触发校验波；合并波如新增 C/H 按其协议处理。
- H pass: 阻断计数 0（见上）。
- 制品修改数：0；修复动作：0（检测波）。

## Anomaly

`ANOMALY: none` —— 本波无未处置异常；无 in-passing repair（只读阶段，未触碰制品）。重判所依据的 round-1 证据（W1 findings / validation wave / repair dispositions）与状态脊为 lane-local 记账输入，不属于跨波读域扩张。
