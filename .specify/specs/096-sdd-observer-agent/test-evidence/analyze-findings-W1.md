# Analyze Findings — W1（096-sdd-observer-agent）

- **Wave**: W1 / analyze 并发波（detection-only，只读变体）
- **Line / Run**: `096-sdd-observer-agent` / `r20261110T081104Z-b096`
- **Round**: 1（首轮；`test-evidence/` 下无既有 `analyze-findings-W1*`，无 rerun delta）
- **Read domain**: `.specify/specs/096-sdd-observer-agent/requirements.md`（下称 `requirements.md`）、`.specify/specs/096-sdd-observer-agent/checklists/2026-11-10-observer-requirements-quality.md`（下称 `checklist.md`）
- **Authority**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md`；`.specify/constitution.md`（1.19.0）
- **Write surface**: 仅本文件与 Wrap-up 记账；未修改任何制品，未做修复
- **Passes executed**: A duplication · B ambiguity · C underspecification · D constitution alignment · F inconsistency · G feature linkage（名称级）· H checklist accountability；E coverage（requirements↔tasks）与 I decision tension 不在本波读域，见 §Coverage Summary
- **Severity basis**: `detection-and-severity.md` § Severity assignment；每行记录 propagation surface，无 `none` 行（MEDIUM 上限未触发）

## Findings

| ID | Severity | Pass | Anchor | Fact（一句话事实） | Propagation | Suggested disposition（指针） |
|----|----------|------|--------|--------------------|-------------|------------------------------|
| W1-01 | HIGH | F inconsistency | `requirements.md:181`; `requirements.md:142`; `checklist.md:72` | FR-011 规定条目恰好承载九类信息，而 Key Entities 的 Journal Entry 定义称「承载八类信息」；同一制品对同一封闭字段集给出两个计数，清单已记录该矛盾但未收敛。 | plan 数据模型 / checker 字段集 / tasks | `/speckit.requirements`（Key Entities 改为九类并引用 FR-011） |
| W1-02 | HIGH | F inconsistency / acceptance | `requirements.md:191`; `requirements.md:197`; `requirements.md:137`; `requirements.md:144`; `requirements.md:146`; `requirements.md:111` | SC-001 的失败线判据要求「每阶段被 `observer-gap` 点名」、SC-007 要求线收束必须输出 `observer-gap` 条目，但 FR-009 允许以状态脊原因替代 journal 收尾，FR-013/FR-015 未指名收束时缺口条目的写入者，且 Edge Cases 允许 observer 启动前失败时无 journal——失败线的覆盖判据缺少被 FR 支撑的写入义务。 | plan 收束设计 / tasks / 验收测试 | `/speckit.clarify`（指名收束缺口写入者，或改写 SC-001/SC-007 与 FR-009 对齐） |
| W1-03 | HIGH | F containment claim | `requirements.md:196`; `requirements.md:206` | SC-006 以「本特性第一个实现提交之前的一次实测采集」为基线断言字段集零增量，但该基线无持久位置、无复现采集规则，属缺少具名基线指涉的 containment claim，验收不可复现。 | plan 基线制品 / SC-006 测试 | `/speckit.plan`（把基线落为具名、可复现契约）+ `/speckit.clarify` |
| W1-04 | MEDIUM | C underspecification | `requirements.md:129` | FR-004 以 `line_id + spec key` 派生实例身份，但全文未定义 spec key 的派生来源与唯一性范围，身份函数不可求值，SC-005 的「两个不同实例身份」缺少可判定的身份函数。 | plan 身份模型 / driver 修订 / 测试 | `/speckit.clarify`（定义 spec key 的派生与 owner） |
| W1-05 | MEDIUM | C underspecification | `requirements.md:160` | FR-023 规定入口声明键 `observer: on|off`，但「入口声明」的载体、位置、解析格式与 owner 均未定义，关闭开关无法被实现方无歧义解析。 | driver U0 解析 / plan | `/speckit.clarify`（绑定入口声明载体与解析规则） |
| W1-06 | MEDIUM | C underspecification | `requirements.md:145`; `requirements.md:192` | FR-014 要求证据指针携带「留存类别」并在线收束时可解析，SC-002 以「可解析」为验收判据，但留存类别词表与「可解析」的判定（存在 / 类型 / 版本历史可达）未定义为封闭集合，且未覆盖工作树清理后的时点。 | plan checker / 测试夹具 | `/speckit.clarify`（留存类别封闭词表 + 可解析判定） |
| W1-07 | MEDIUM | F inconsistency | `requirements.md:135`; `requirements.md:136` | FR-007 规定上一执行 `.status` 未结算时 driver MUST NOT 派发下一个，FR-008 又允许失败 / 停滞 / 窗口到期后在阶段边界重启；执行崩溃且未留下 `.status` 时既未结算又已结束，两条规则互斥，重启路径被串行规则封死。 | driver 派发逻辑 / plan | `/speckit.clarify`（裁定未结算执行的结算或超时规则） |
| W1-08 | MEDIUM | F inconsistency | `requirements.md:128`; `requirements.md:141`; `requirements.md:158` | FR-003 禁止不同线共享 journal、FR-010 按 spec 目录落一份 journal，但 FR-021 未排除两条线（含嵌套运行）解析到同一 spec 目录的情形，该状态下路径冲突且「不共享」无法成立。 | plan 路径模型 / 双线夹具 | `/speckit.clarify`（排除或消歧同 spec 双线状态） |
| W1-09 | MEDIUM | C underspecification | `requirements.md:144`; `requirements.md:160` | FR-013 的缺口窗口推导未裁决三种边界：零长度窗口（起止同秒）写入还是抑制、连续多个缺口的起点链、以及 `state=disabled` 无启动时间时的起点回退值。 | plan 缺口写入 / checker / 测试 | `/speckit.clarify`（缺口窗口边界裁决） |
| W1-10 | MEDIUM | B ambiguity | `requirements.md:194`; `requirements.md:52` | SC-004(c) 要求 checker 拒绝「自由叙述条目」，但需求层未给出「自由叙述」的结构定义，反例构造只能回落到 checker 自身判定，存在循环判据风险。 | plan 客观性夹具 / checker | `/speckit.clarify`（自由叙述的结构定义） |
| W1-11 | MEDIUM | B ambiguity | `requirements.md:142`; `requirements.md:144` | FR-011 的 `命令` 字段允许「原文或 `-`」，但原文取自哪个载体、字符集 / 长度如何约束均未定义，评价或建议文本可借这个自由文本字段进入条目，与 FR-013 的客观性构造冲突。 | plan journal 格式 owner / driver | `/speckit.clarify`（命令字段的来源与内容约束） |
| W1-12 | MEDIUM | B ambiguity | `requirements.md:144` | FR-013 以「限定为」引出观测输入清单，但未声明该清单是否穷尽、也未指名新增载体的 owner，其他制品引入的 meta 包络是否可读不可判定。 | plan 读域实现 / 定义文本 | `/speckit.clarify` + `/speckit.plan`（封闭清单与扩展 owner） |
| W1-13 | MEDIUM | C underspecification | `requirements.md:150`; `requirements.md:88` | FR-016 把写面界定为 journal 与「自身执行运行产物」（按既有布局引用），但 US4 AS1 要求审计实际写面时，锁文件 / 游标 / 临时文件是否计入写面没有测量规则，单写者协议所需锁文件的位置也未裁定。 | plan 写面声明 / tasks | `/speckit.plan`（写面枚举与审计规则） |
| W1-14 | MEDIUM | E coverage gap | `requirements.md:252` | 「journal MUST NOT 被加入任何阶段 required artifact 集或 `STAGE_ARTIFACTS` 映射」只存在于 Assumptions A12，既无 FR 承载也无带红腿的 SC，规范义务挂在假设上。 | plan / tasks（红腿） | `/speckit.requirements`（提升为 FR）→ `/speckit.tasks` |
| W1-15 | MEDIUM | F inconsistency | `requirements.md:129`; `requirements.md:141`; `requirements.md:234` | FR-004 说身份四元组以「执行 label」记入 journal 头部，FR-010 与 clarify 记录却写「实例 label」；journal 跨多次执行只有一份头部，而派发 label 每次执行不同，头部字段语义悬空。 | plan 头部 schema / 模板 | `/speckit.clarify`（头部 label 字段定名与取值） |
| W1-16 | LOW | H completeness | `requirements.md:126` | FR-001 的 MUST NOT 覆盖 stage executor / reviewer / reporter 三个席位，但这三个角色面没有指向定义 owner 的引用，三条禁令无法按同一谓词独立核对。 | 定义文本 | `/speckit.requirements`（补 owner 引用） |
| W1-17 | LOW | A duplication | `requirements.md:141`; `requirements.md:144`; `requirements.md:191`; `requirements.md:194`; `requirements.md:197`; `requirements.md:217` | FR-010、FR-013、SC-001、SC-004、SC-007 在 `[[STR-00N]]` 标记旁同时复制了字面量，违反本制品自设的「用 `[[STR-NNN]]` 代替复制字面量」约定。 | requirements 文本 | `/speckit.requirements`（仅保留 token） |
| W1-18 | LOW | B ambiguity | `requirements.md:113`; `requirements.md:142` | Edge Cases 称「checker 以文件序判定非递减」但未点名判定对象（序号还是观测时间），而 FR-011 要求序号单调递增，checker 判定谓词存在两种读法。 | plan checker | `/speckit.clarify` 或 `/speckit.plan`（点名判定对象） |

## Checklist Accountability（`[Gap]` 项）

清单 `checklist.md` 共 38 项、全部未勾选；其中带 `[Gap]` 标签 7 项，逐项处置如下（机器可读行）。

| CHK | Anchor | Disposition |
|-----|--------|-------------|
| CHK002 | `checklist.md:14` | raised-as-finding W1-04 |
| CHK003 | `checklist.md:15` | raised-as-finding W1-05 |
| CHK004 | `checklist.md:16` | raised-as-finding W1-13 |
| CHK005 | `checklist.md:17` | raised-as-finding W1-06 |
| CHK008 | `checklist.md:20` | covered-by requirements.md § FR-001（`agents/sdd-observer.agent.md` 模板即角色面单一 owner；FR-002 要求模板与实例文本显式声明） |
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

未带 `[Gap]` 的其余 31 个未勾选项属质量问句，其材料性缺陷已由 W1-01…W1-18 按锚点吸收（如 CHK011→W1-07、CHK013→W1-11、CHK014→W1-10、CHK017/CHK019→W1-09、CHK020/CHK021→W1-08、CHK027→W1-03、CHK038→W1-04）；其余项在 requirements 文本中已有可引用答复，不另立 finding。

## Coverage / Registry / Constitution Summary

- **E pass（requirements ↔ tasks 覆盖）**: 本波读域不含 `plan.md` / `tasks.md` / `contracts/`，`account-clause-coverage.py` 同样需要这些跨波制品；该步**显式延期**到阶段合并波执行，本文件不做 `baseline-missing` 判定。
- **I pass（decision tension）**: 判定对象仅为 `plan.md`，不在 W1 读域 → 本波 N/A，由合并波执行。
- **G pass（feature linkage / registry）**: `Related Feature` 声明 Feature ID `096` 与 Feature Name「SDD 专用观察者与线级观察记录（sdd-observer）」，与清单 `checklist.md:5` 的主题一致；名称级核对显示 `.specify/features.md` 与 `.specify/features/096.md` 均存在。索引行与详情文件的**内容级**阶段记录义务（feature-integration § Core Protocol steps 2–3）超出 W1 读域，标为在该波 `not_evaluated`，不据此立 finding（skill 规则：feature 文件缺席才是治理缺口）。
- **D pass（constitution alignment）**: 两份读域文件中**未发现宪法 MUST 冲突**（0 CRITICAL）。逐项考虑后不立 finding：(a) A5 的 journal 单文件 vs 指令层 Concurrent Development Safety——该规则的「两分支写同一路径」碰撞测试在「每线单写者 + 每 spec 一路径」下不触发，且 A5 已记录裁定理由（指令层亦非宪法）；(b) A10 的 Test-First Partial 仅限定 LLM 行为面，确定性面（引擎 / checker / 定义断言）已声明走契约测试，与宪法 IV / VII 相容；(c) 需求阶段登记的 pending 记录是带日期的澄清记录（`requirements.md:232`），详情文件在名称级已存在，不构成当前治理违约。
- **H pass**: 见上节，阻断计数 0。
- **Zero-finding floor**: 不适用（本波 findings 非空）。

## Metrics

- Findings: **18**（CRITICAL 0 · HIGH 3 · MEDIUM 12 · LOW 3），上限 50 内，无 overflow。
- HIGH 3 条待阶段合并波按 `validation-and-report.md` 走独立只读校验（W1-01 / W1-02 / W1-03）。
- 制品修改数：0；修复动作：0（检测波）。
- `[Gap]` 处置：7 / 7（阻断计数 0）。

## Anomaly

`ANOMALY: none` —— 本波无未处置异常；无 in-passing repair（只读阶段，未触碰制品）。
