# Analyze — Merged Report, Round 3（096-sdd-observer-agent）

- **Line / Run**: `096-sdd-observer-agent` / `r20261110T081104Z-b096`
- **Stage**: analyze（串行集成者；第三轮修复后重过门：两路并发检测波 W13/W2 + 合并波 + C/H 锚点复核）
- **Round**: 3（prior report: `test-evidence/analyze-merged-round2-2026-11-10.md`；repair commit: `32e83b95e`；repair 记录: `test-evidence/analyze-repair-dispositions-r3-2026-11-10.md` + `test-evidence/analyze-repair-gates-r3-2026-11-10.txt`）
- **Date**: 2026-11-10
- **Authority**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` + `references/validation-and-report.md`；`.specify/constitution.md`（v1.19.0，22 原则 I–XXII）
- **Read domain（合并波）**: `requirements.md`（锚点段）、`tasks.md`（全量复核残项）、`checklists/`（2 份）、`data-model.md` / `contracts/journal-engine.contract.md` 的 C/H 锚点段、`constitution.md` VII、`shared/workflow/acceptance-hardening.md` § Gates、`shared/workflow/feature-integration.md`（deferred 约定）、`.specify/features.md` 096 行、`.specify/features/096.md`；plan 域细节以 W2 波读值为准
- **Write surface**: 本文件 + `test-evidence/analyze-{clause-coverage,decision-tensions}-r3.txt` + Wrap-up 记账；未修改任何 spec 制品，未执行任何修复（只读阶段）
- **Merge protocol（确定性归并）**: 分节 W13→W2（本节 + 合并波）；各节内按 ID 字典序；跨波重复 ID 检查 **0 条**（`W13-*` / `W2-*` 前缀互斥）——「先声明先得 + 指针」规则本轮无触发；跨波语义重复 **0 对**（两对同面关联 W13-05↔W2-02、W13-09↔W2-12 仅作交叉注记，不合并、不改级）。W13/W2 表格按原文逐字保留，不重写、不重评级；C/H 行以 `(validated: …)` 标注，方法见 § C/H 锚点复核。
- **C/H 复核（本轮变体）**: 按编排指令采用**集成者锚点直读复核**，本轮未派独立外部校验波；send 2 · validated 2 · proposed 0。

---

## Top summary — C/H count and per-item pointers（不修复）

**CRITICAL（validated，1 条）**：

| ID | Category | Severity（validated） | Anchor（逐条指针） | Fact pointer（一句话） |
|----|----------|----------------------|--------------------|------------------------|
| W13-01 | 宪法对齐（VII Workflow Gates） | **CRITICAL**（anchors validated: direct re-read；宪法变体不可降级） | `tasks.md:60`（§Task State Sigil）、`:33`（GATE-4）、`:381`（§Notes）↔ `constitution.md:220-225`（`:223` `verification.log`、`:224` 行内 `<!-- deferred: reason -->`）；旁证 `shared/workflow/acceptance-hardening.md:40-50`、`shared/workflow/feature-integration.md:44` | tasks.md 的完成门与延迟约定在**记录面**上与宪法 VII 文本不一致：延迟原因 tasks 侧 `verification.md` `deferred_tasks=` vs 宪法行内 `<!-- deferred: reason -->`；Pre-Status-Flip 记录 tasks 侧 `verification.md`（GATE-4 仅 final-path SC + smoke 字段）vs 宪法 `verification.log`（every SC）。 |

**HIGH（validated，1 条）**：

| ID | Category | Severity（validated） | Anchor（逐条指针） | Fact pointer（一句话） |
|----|----------|----------------------|--------------------|------------------------|
| W2-01 | 契约可执行性（`check` 的规则集与输入面） | **HIGH**（anchors validated: direct re-read；轮 2 同面为 W2-04 MEDIUM，本轮升为 HIGH） | `contracts/journal-engine.contract.md` §C-09（L54–55）、§C-07（L41–43）；`data-model.md` V-16（L160） | C-09 要求 `check`（仅声明 `--spec-dir` / `--repo` 两个输入）校验 V-16，但 V-16 是「外来/过期执行不得 append」的追加时拒绝规则、C-07 已把它归给 append；`check` 未被声明任何执行身份或状态脊输入，该条款按原文不可执行。 |

**Severity distribution（本轮主表，validated）**: **CRITICAL 1 · HIGH 1 · MEDIUM 11 · LOW 16 —— 主表 29 行**（≤50 上限）。另有**轮 2 遗留残项 22 行**（全为 MEDIUM/LOW）逐条列于 § Rerun delta，不聚合、不静默；全量开放账 = **C1 · H1 · M23 · L26 = 51**（51 = 29 现役行 + 22 残项行）。

**门禁结论须双向陈述（不构成「ready to implement」）**：轮 2 的 1 CRITICAL + 3 HIGH 积压（W3-07/08/09/10）已全部 **fixed**（repair commit `32e83b95e`；修复后全部门禁 exit 0，见 repair-gates 证据），且本轮复核未见回退；但**本轮重扫不是 clean rerun**——新增 1 CRITICAL（W13-01，宪法 VII）+ 1 HIGH（W2-01，C-09/V-16，较轮 2 同面 findings 升一档）。按技能 §9，**CRITICAL 须在 `/speckit.implement` 前处置**；本阶段只读，未修复。

---

## C/H 锚点复核（集成者直读；本轮无独立校验波）

- **方法**：按编排指令，C/H 各行的**锚点事实**由集成者直读原文复核（非独立 fresh-context 校验波）；MEDIUM/LOW 不进入复核。标记词：`validated`（锚点事实成立）或 `proposed`（锚点未成立/证据不足）。本轮结果：**send 2 · validated 2 · proposed 0**。
- **W13-01 — validated**：`constitution.md:223` 原文为 "requires zero open `[ ]` tasks AND a status line for every Success Criterion in `verification.log`"；`:224` 原文为 "`[~]` with `<!-- deferred: reason -->`"。`tasks.md:60` 原文为 "`[~]` deferred with the reason in `verification.md` `deferred_tasks=`"；GATE-4（`:33`）以 `verification.md` + 仅 `final`-path SC + smoke 字段为检查面，并自注 "Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates"；§Notes（`:381`）再次要求 `verification.md` `deferred_tasks=`。旁证：`acceptance-hardening.md:44-50` 的四条件使用 `verification.md`；`feature-integration.md:44` 仍用行内 `<!-- deferred: <reason> -->`。**evidence_not_supported**：修复面不只在 tasks——宪法文本（`verification.log`）自身落后于框架 owner 链（acceptance-hardening / feature-integration），按技能须在 analyze 之外以独立宪法修订处置；另 feature-integration 的行内注释形式与 tasks/acceptance-hardening 的 `deferred_tasks=` 约定之间的分歧，锚点在 feature-integration 而非宪法逐字文本。
- **W2-01 — validated**：`journal-engine.contract.md` C-09（L54–55）原文 "`check` takes `--spec-dir` and `--repo`. It validates every rule in `data-model.md` V-1…V-13 and V-16…V-17"；`data-model.md:160` V-16 原文为追加时拒绝规则（"is refused (exit 2) — a foreign or stale execution cannot append"）；C-07（L41–43）把身份检查归给追加操作（读状态脊、比对 `execution_label`、不匹配 exit 2 且不追加）。`check` 无执行身份 / 状态脊输入 → V-16 由 `check` 执行按原文不可达。**evidence_not_supported**：finding 未评估静态代理读法（逐行标签 vs 脊最新记录）是否满足意图；V-17 原则上可由 `check` 读 journal + 脊执行。轮 2 同面（W2-04）为 MEDIUM、本轮升 HIGH 属检测方评级，本复核只确认锚点事实、不另立升档理由。
- **边界声明**：若后续需要独立确认，可在 `/speckit.implement` 前补派 fresh-context 校验波；本报告不把「锚点复核」表述为「独立校验」。

---

## Merged findings

### Wave W13 — requirements + checklist + tasks（16 rows；读域 `requirements.md` + `checklists/2026-11-10-observer-requirements-quality.md` + `tasks.md`）

本波未判 G（注册表）与 I（decision-tension 判决对象），条款覆盖率记账与 C/H 独立校验按分片边界移交编排侧（合并波已承接）。检测面：A 重复 / B 歧义 / C 欠指定 / D 宪法对齐 / E 覆盖缺口 / F 不一致 / H 清单问责。

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|---|---|---|---|---|
| W13-01 | **CRITICAL** (validated: anchors re-checked) | tasks.md §Task State Sigil:60、§Notes:381、§GATE-4:33 ↔ `.specify/constitution.md` §VII Workflow Gates:220-225（:223 `verification.log`、:224 行内 `<!-- deferred: reason -->`） | tasks.md 的完成门约定与宪法原则 VII 的 Workflow Gates 文本在记录面上不一致——延迟任务原因（tasks 侧 `verification.md` `deferred_tasks=` vs 宪法行内 `<!-- deferred: reason -->`）与 Pre-Status-Flip 记录（tasks 侧 `verification.md` 且仅 final-path SC + smoke 字段 vs 宪法 `verification.log` 且 every SC）。 | 宪法治理（独立修订，须在 analyze 之外进行）；tasks 侧同时与 `shared/workflow/acceptance-hardening.md` § Gates 条件集对齐后复核。按 analyze 规则：宪法冲突 CRITICAL，不得降级、不得在本技能内稀释。 |
| W13-02 | MEDIUM | requirements.md §FR-011:142 ↔ §Key Entities「记录条目」:181；checklist CHK018:36 | FR-011 要求每个条目恰好承载九类信息（含序号），而 Key Entities 的「记录条目」仍写「承载八类信息」，同一产物内计数矛盾。 | /speckit.requirements（将 Key Entities 改为九类并同步信息面表述） |
| W13-03 | MEDIUM | requirements.md §SC-001:191、§FR-011:142；tasks.md T008:139、T016:162、§SC→row trace:348 | SC-001 的失败线覆盖判据（每个阶段至少有阶段开始条目或被 `observer-gap` 点名）没有契约测试行断言它：T008 只覆盖零失败夹具的 stage 覆盖、T016 只断言单条 gap 行，T045 为端到端 quickstart 而非该判据的断言。 | /speckit.tasks（为失败线覆盖判据补断言行）或 /speckit.requirements（收窄 SC-001 表述到可测范围） |
| W13-04 | MEDIUM | requirements.md §SC-005:195、§US5 AS2:104、§FR-007:135；tasks.md T011:145、T037:232；checklist CHK023:41 | SC-005 与 US5 AS2 允许「被拒绝或串行化」两种结果，而 FR-007 的双机制（driver 不派发 + 引擎单写者拒绝）与 T037 的 exit-3 断言只承认「拒绝」这一种可观测结果，验收文本与实现契约不一致。 | /speckit.requirements（收敛 SC-005 / US5 AS2 为单一可观测结果） |
| W13-05 | MEDIUM | requirements.md §FR-013:144；tasks.md T007:125、T010:144；checklist CHK006:18 | FR-013 以「限定为」封闭观测输入清单，但 T007/T010 把「meta 包络（meta envelopes）」与「两条窄语法」当作投影载体，这两类载体不在 FR-013 的枚举内，封闭清单与投影实现漂移。 | /speckit.requirements（扩展观测输入清单，或声明其为按引用拥有并指名新增载体 owner） |
| W13-06 | MEDIUM | requirements.md §FR-003:128、§FR-010:141、§FR-021:158、§Edge Cases:116；checklist CHK020:38、CHK021:39 | FR-003 保证「不同线 MUST NOT 共享 journal」，FR-010 又把 journal 固定为 spec 目录单一文件；两条线（含同 spec 的内层团队运行，FR-021 只保证内层有自己的 journal，未排除同 spec 目录）指向同一 spec 目录时两条款互相冲突且该状态未被定义。 | /speckit.requirements（排除该状态，或定义同 spec 多线的身份 / 路径规则） |
| W13-07 | MEDIUM | requirements.md §Edge Cases:112、§FR-009:137、§FR-010:141；tasks.md T023:186、T024:187 | Edge Cases 的「journal 写入失败（权限 / 磁盘）」要求以执行 `.status` 与状态脊观察者记录节取证且下一次执行按 `observer-gap` 披露，但 tasks.md 的 T023/T024 只覆盖启动失败与中途终止，没有对应夹具或断言行。 | /speckit.tasks（补 journal 写失败夹具 / 断言） |
| W13-08 | MEDIUM | requirements.md §FR-011:142、§SC-004:194；tasks.md T008:139、T017:168；checklist CHK007:19、CHK014:29 | FR-011 只规定九类信息与封闭性，未定义条目的表示形态（表格行 vs 段落），SC-004(c) 的「自由叙述条目」反例判据因此在需求面不可判定，只存在于 T008/T017 的实现约定（single nine-column table）。 | /speckit.requirements（为条目表示形态指定 owner 或写入信息面） |
| W13-09 | MEDIUM | requirements.md §FR-007:135、§FR-008:136；tasks.md T023:186、T024:187；checklist CHK011:26 | FR-007 以「前一个执行 `.status` 未结算」禁止下一次派发，FR-008 又允许失败后在阶段边界重启，而执行崩溃且无 `.status` 的情形既构成「永不结算」也构成「已终止」，两条款对该情形互相冲突（重启被 FR-007 永久阻塞），T023 的 mid-run-kill 夹具正使用 unsettled / failed status envelope。 | /speckit.requirements（定义「已结算」对崩溃情形的判定与有界阻塞规则） |
| W13-10 | LOW | requirements.md §FR-004:129；checklist CHK002:14 | FR-004 的实例身份函数依赖「spec key」，但 requirements.md 未定义其派生来源与唯一性范围，身份无法仅由需求文本求值。 | /speckit.requirements（定义或按引用指明 spec key 的 owner） |
| W13-11 | LOW | requirements.md §FR-023:160；tasks.md T025:191；checklist CHK003:15 | FR-023 的关闭开关挂在「入口声明」上，但该声明的载体、位置与解析格式在本规格未定义（tasks T025 才把它落到 driver SKILL.md）。 | /speckit.requirements（声明入口声明的 owner 并引用） |
| W13-12 | LOW | requirements.md §FR-016:150、§US4 AS1:88；checklist CHK004:16 | FR-016 的「自身执行运行产物」未被枚举或按引用拥有，US4 AS1 的写面审计无法判定锁文件 / 游标 / 临时文件属写面内或写面外。 | /speckit.requirements（枚举或引用运行产物布局并给审计判据） |
| W13-13 | LOW | requirements.md §FR-014:145、§A9:249；tasks.md T006:124；checklist CHK005:17 | FR-014 的「留存类别」词表与「可解析」判定（存在 / 类型 / 版本历史可达）未在需求面定义为受拥有的封闭集合，只留给实现期 T006 的 journal-format 事实。 | /speckit.requirements（声明 owner 与可解析判据边界） |
| W13-14 | LOW | requirements.md §A12:252；tasks.md T032:211、T047:254、§GATE-8:37；checklist CHK036:63 | 「journal 不进阶段产物表」只作为假设 A12 存在，没有对应的 FR / 门禁条款承载（断言侧由 T032/T047/GATE-8 覆盖）。 | /speckit.requirements（升为 FR）或 /speckit.tasks（保持当前覆盖并记录 disposition） |
| W13-15 | LOW | requirements.md §FR-001:126；tasks.md T018:163、T019:169；checklist CHK009:21 | FR-001 对「stage executor / reviewer / reporter 席位」的 MUST NOT 未按引用给出三个席位的可核对定义，判定依赖这些席位在别处的定义文本。 | /speckit.requirements（补三条引用指针） |
| W13-16 | LOW | requirements.md §FR-013:144；checklist CHK017:32 | 零长度观察缺口（窗口起止同一秒）是否写入或抑制未被裁决，FR-013 只定义端点来源、未定义该边界。 | /speckit.requirements（显式裁决写入或抑制） |

**H — Checklist Accountability（W13 分片，`checklists/2026-11-10-observer-requirements-quality.md`）**

清单 38 项全部未勾选（`[ ]` 38 / `[x]` 0）；H 门禁范围是带 `[Gap]` 标签的未勾选项，全部给出处置：

```
CHK002 disposition: raised-as-finding W13-10
CHK003 disposition: raised-as-finding W13-11
CHK004 disposition: raised-as-finding W13-12
CHK005 disposition: raised-as-finding W13-13
CHK008 disposition: covered-by requirements.md §FR-001, §FR-002
CHK009 disposition: raised-as-finding W13-15
CHK036 disposition: raised-as-finding W13-14
```

计数：`unchecked [Gap] = 7`；`raised = 6`；`dispositioned = 1`；**未被提升且未被处置的 `[Gap]` 项 = 0**（`unchecked + unraised + undispositioned = 0` 可观测）。

**Evidenced Absences（W13 读域内已核对、无 findings 的覆盖断言）**：FR-001…FR-023 每项至少被一条 tasks 行引用（无零覆盖 FR）；SC-001…SC-007 均在 §SC→row trace 有行与证据路径（SC-001 的失败线判据见 W13-03）；19 条带 `[green:]` 的行共声明 58 次，按页核对 journal-engine 13/13、journal-format 13/13、observer-lifecycle 12/12、observer-role 10/10、observer-verification 10/10，各恰好一次；T001–T047 共 47 行，包分区 13+5+9+15+5(Setup)=47，无 ID 双属；SC-006 字段集 delta、GATE-1/2/8、T032 的载体边界均具备基线指涉与比较单元（`closed-set-claims.md` 合法形态，不报）。

### Wave W2 — plan 与设计产物（13 rows；读域 `plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`research.md`、`contracts/` 5 页）

本波显式移交：条款/FR 覆盖记账与 Checklist H → 编排侧（合并波已承接）；tasks 覆盖 → W13 分片；feature 注册表 → 合并波；往轮残项与重跑增量 → 合并波。确定性判定消费：`validate-decision-tensions.py` → `status: ok`（5 records，六类标签均 0，exit 0）。

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|----|----------|------|------------|----------|
| W2-01 | **HIGH** (validated: anchors re-checked) | `contracts/journal-engine.contract.md` §C-09（L54–55）、§C-07（L41–43）；`data-model.md` V-16（L160） | `check`（仅声明 `--spec-dir` / `--repo` 两个输入）被 C-09 要求校验 V-16，但 V-16 是“外来/过期执行不得 append”的追加时拒绝规则、C-07 已把它归给 `append`；`check` 未被声明任何执行身份或状态脊输入，因此该条款按原文不可执行。 | journal-engine 合同 C-09（把 V-16 移出 `check` 的规则集，或为其声明可校验的输入与语义） |
| W2-02 | MEDIUM | `data-model.md` E-6 `line-start` 行（L82）、E-10（L141）；`research.md` R-07（L56）；`plan.md` L220；`contracts/journal-engine.contract.md` C-04 | E-6 把状态脊 U0 块声明为 `line-start` 的主载体，但引擎的封闭载体清单（E-10 / C-04）与 R-07“只解析两条窄状态脊 prose 语法”的解析面都不含 U0 块语法，故声明式投影产不出这条 `min_persistent: 1` 行。 | data-model E-6/E-10 + research R-07（把 U0 语法补入封闭解析面，或改正载体列） |
| W2-03 | MEDIUM | `contracts/observer-lifecycle.contract.md` C-04（标题 L23、正文 L25–41）；`data-model.md` E-9（L121–137）；`feature-ref.md` 第 9 行（L30） | 同一份八键观察者记录块在 lifecycle C-04 与 data-model E-9 各定义一次，而 C-04 一边自称“key and shape owner”、一边把形状所有权让给 `SKILL.md` § SDD Observer，导致该块没有唯一声明所有者、也无从防止与未来 SKILL.md 文本漂移。 | lifecycle C-04 / data-model E-9（择一为 owner，另一处改为引用；修正 C-04 标题） |
| W2-04 | MEDIUM | `data-model.md` E-3 States（L36）、E-9 state 行（L127）；`contracts/observer-lifecycle.contract.md` C-04 state 行（L31） | E-3 称执行状态 `started → settled \| failed` 会“记录在状态脊观察者记录节”，但 E-9/C-04 的 `state` 值域是 `started\|failed\|disabled\|closed`，`settled` 没有可记录取值。 | data-model E-3/E-9（把执行态映射到脊记录值域，或明确声明两套状态模型） |
| W2-05 | LOW | `quickstart.md` L3（对照 S-0…S-7，L5–102）；`plan.md` L31、L236 | `quickstart.md` 首句写“Seven walk-through scenarios”，实际列出八个（S-0…S-7），而 plan.md 两处均计为 8。 | quickstart.md 首句（改为 eight） |
| W2-06 | LOW | `quickstart.md` S-3（L59）；`contracts/journal-engine.contract.md` C-09 | Quickstart S-3 说 `check` 对“`data-model.md` V-1…V-13 中每条规则”报 `file:line`，而 C-09 声明的规则集是 V-1…V-13 加 V-16…V-17，quickstart 少报了两条规则。 | quickstart S-3（改为引用 C-09 的规则集而非枚举子集） |
| W2-07 | LOW | `data-model.md` V-12（L156）；`contracts/journal-format.contract.md` C-12（L71–73） | Journal-format C-12 把段落、列表与围栏代码块都判为 finding，而 `check` 被要求实现的 V-12 只点名“叙述性段落”，列表/围栏块的处理未被规定。 | data-model V-12（把范围对齐到 C-12） |
| W2-08 | LOW | `feature-ref.md` L57（FR-001 行）；`contracts/observer-role.contract.md` C-04（L23–27） | Role C-04（承载 SC-004 强制原文的「不评价、不建议、不推断」禁止条款）自身引用 FR-001，但 FR→Contract map 的 FR-001 行只列 role C-01…C-03 与 verification C-08，漏掉 C-04。 | feature-ref FR→Contract map |
| W2-09 | LOW | `plan.md` L277（§ Risks）；`feature-ref.md` L87（SC-003）、L91（SC-007） | Plan 风险表把“无 journal 收线”的缓解证据写成“SC-001 的 failure-path criterion”，但 feature-ref 的 SC 映射给 SC-001 的是覆盖夹具度量，failure path 属 SC-003/SC-007。 | plan § Risks |
| W2-10 | LOW | `plan.md` L43（Constitution Check 第 II 行） | Constitution 第 II 行证据引用“§ Feature Integration”，但 plan.md 无此章节，门证据指向不存在的锚点（注册表职责实际由 R-10、WP-4、feature-ref 第 18 行承载）。 | plan（补章节或改引用） |
| W2-11 | LOW | `plan.md` L56（Constitution Check 第 XV 行）；`quickstart.md`（全文） | Constitution 第 XV 行证据称 quickstart“在首次使用时定义了 journal / observer / gap”，但 quickstart.md 对这三个词没有任何定义句。 | plan 第 XV 行，或 quickstart（首次出现处各加一句定义） |
| W2-12 | LOW | `data-model.md` E-8（L114–118）、V-17（L161）；`contracts/journal-engine.contract.md` C-08 | E-8 规定“无任何条目时”gap 窗口起点取脊记录节的 `started_at`，但 C-08 与 V-17 只在“存在上一条目的 `observed_at`”时才触发 gap，故该无条目分支永不生效，两处对首次执行是否产生 gap 的语义不一致。 | data-model E-8 / engine C-08（单点声明首次 append 的 gap 语义） |
| W2-13 | LOW | `feature-ref.md` 第 1–19 行（第 4 行与 L42 的生成器句）；`plan.md` § Mirror Obligations 第 2 行（L175） | feature-ref 的 19 行“file-level inventory”把 agent、engine、skill 的镜像各自列为独立行，却漏掉 plan.md § Mirror Obligations 第 2 行要求“必须同样落地”的 `.specify/shared/declarations/facts/journal-format.yaml` 镜像。 | feature-ref delivered-path inventory（补镜像行） |

**W2 波系统性观察（原样保留）**：① `check` 的规则集与输入面缺单一所有者（W2-01、W2-06、W2-07、W2-12 四个方向同指 engine C-09 / format C-12 / data-model V 规则的对应关系需一处收敛）；② 两处重复枚举需收敛（W2-03 脊记录节八键、W2-04 执行态 vs 脊 state 值域——与 plan 第 XIV 原则「单一所有者、其余引用」自评存在张力，设计期声明可解释，实现前应收敛）；③ 宪法对齐：plan 的 Constitution Check 恰好覆盖宪法 v1.19.0 全部 22 个 `### <numeral>. <name>` 标题、顺序一致；本 lane 未派生 CRITICAL 级宪法冲突，仅第 II、XV 两行证据事实不支持（W2-10/W2-11 同类，LOW）。

### Merge wave — cross-artifact serial pass（requirements ↔ plan ↔ tasks ↔ contracts；**0 条新 finding**）

**固定步（技能 §3，read-only）判定——phase-visible**：

- `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs` → **`status: ok`，exit 0**（证据：`test-evidence/analyze-clause-coverage-r3.txt`）。读值：claimed clauses **58**；baseline 640 names，0 beyond baseline；`[fr-uncovered]` **23/23** FRs cited from citation groups；扫描 291 文件（107 个语料级既有 unparsable，非 096 特有）；0 error / 1 warning（语料级既有）。轮 2 的两条 blocking lane 维持清零。
- `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/096-sdd-observer-agent` → **`status: ok`**，6 个 label 全 pass（0），5 records，0 error / 0 warning，`high=0`（证据：`test-evidence/analyze-decision-tensions-r3.txt`）。I pass 无 finding。
- **消费既有记录（不重跑）**：`validate-tasks.py` → `PASS (with warnings)`，`0 error(s), 4 warning(s)`，exit 0；`pre-analyze-check.py --stage tasks` → `decision: pass`，0 error；`decomposition-check.py --mode tasks` → `decision: proceed`（23 FR / 47 tasks）——均取自 `test-evidence/analyze-repair-gates-r3-2026-11-10.txt`（HEAD `32e83b95e`，本报告 HEAD 相同且 tasks.md 此后未再变）。

**跨波一致性复核注记（对既有行，不改变其评级；关联对不合并）**：

1. **W13-01 ↔ W2-10/W2-11（宪法面）**：本轮唯一宪法 MUST 冲突在 tasks×宪法 VII（W13-01）；W2 lane 判 plan 的 Constitution Check 22 原则全覆盖、顺序一致，仅 row II / XV 证据事实不支持（LOW）。即宪法一致性风险集中在**门禁文本与宪法逐字文本之间**，不在 plan 自查表。
2. **W13-05 ↔ W2-02（观测载体封闭面）**：需求侧 FR-013「限定为」清单 vs plan 侧 E-10/C-04 封闭载体清单 + R-07 窄解析面 vs tasks 侧 T007/T010 投影载体——同一载体面的三处读法互不重合，两侧均 open，互证。
3. **W13-09 ↔ W2-12（缺口 / 崩溃语义）**：需求侧 FR-007/008 崩溃结算悬空 vs plan 侧 E-8/C-08 首次 append gap 分支不可达；同一 lifecycle 面两端 open。
4. **W13-04 ↔ W2-01（拒绝语义）**：SC-005 的「拒绝或串行化」二读与 C-09/V-16 的「拒绝」单一可观测结果同向——验收文本、任务断言（T037 exit-3）与契约规则彼此支持收敛。
5. **W13-03 / W1-22（残项）/ W3-11（残项）（SC-001 三层）**：需求层判据可满足性（W1-22）、tasks 层断言缺口（W13-03）、trace 记账不一致（W3-11）三层各自 open，任一单层修复不足以关闭该面。
6. **W2-04 ↔ W2-03（同块双缺陷）**：E-9/lifecycle C-04 八键块既缺唯一所有者（W2-03）又有 `settled` 值域缺口（W2-04）；与轮 2 残项 W2-03（终态 `closed` vs `failed`）共三层，建议一次收敛。
7. **W13-06 ↔ W2-08（残项，同 spec 双线）**：需求侧未排除同 spec 双线 vs plan 侧 V-19 / 两处 C-05 未写 distinct-spec 前提；两侧 open（S1 延续）。
8. **W13-10 / W13-11 ↔ W2 lane（身份与开关）**：spec key（W13-10）与入口声明（W13-11）在需求面均无 owner；plan 侧 identity 模型与 E-3 未回指需求 owner，属同一词汇未收敛面（S5）。

**结论**：合并波未发现超出两波读域的新 CRITICAL/HIGH/MEDIUM/LOW finding（0 条），故不触发第二轮校验派发；跨制品一致性总账见下节。

---

## Cross-artifact consistency（合并波一致性总账）

### Coverage Summary

| 量 | 读值 | 来源 / 判定 |
|----|------|-------------|
| FR 定义 / SC 定义 | 23 / 7 | requirements.md 定义行 |
| FR → 任务文本覆盖 | 23/23 | W13 分片 Evidenced Absences（tasks.md 文本） |
| FR citation groups（条款体） | **23/23** | 固定步读值（`analyze-clause-coverage-r3.txt`） |
| 契约条款 | 58 = 13+13+12+10+10 | 五页 `^## C-` 标题；与 plan / feature-ref / tasks 三处计数一致 |
| `[green:]` 认领 | **58/58 恰一次** | W13 按页核对 13/13+13/13+12/12+10/10+10/10；`validate-tasks.py` 0 `green-dangling` / 0 `green-clause-collision` |
| SC → row trace | 7/7 行齐全；3 处与行级 citation 不一致（SC-001 缺 T047、SC-004 多 T019、SC-006 缺 T024） | W3-11（残项，open） |
| data-model 规则 → 任务 | V-1…V-13/V-16/V-17 → T017；V-14/V-15/V-18/V-19/V-20 无显式归属行 | W3-06（残项，open） |
| 任务行 / 包 | 47 行、4 包、分区 13+5+9+15+5(Setup)=47；无缺号重号；包链严格串行 wp01→wp02→wp03→wp04 | W13 机器核对 |
| 覆盖门可执行性 | GATE-9/T047 可过（固定步 exit 0） | `analyze-clause-coverage-r3.txt` |
| 扫描语料 | 291 文件（含 107 语料级既有 unparsable） | 固定步；非 096 特有 |

### Feature Linkage Summary（G）

- **名称级**：`requirements.md` 的 Feature ID `096` 与名称「SDD 专用观察者与线级观察记录（sdd-observer）」与清单页眉一致；`.specify/features.md` 096 行与 `.specify/features/096.md` 均存在。
- **内容级 / 阶段记录义务（合并波实测）**：索引行 Status `Planned`、Last Updated `2026-11-10`、备注记录 plan 阶段落册（22 项宪法全 Pass、R-01–R-14、10 实体/20 规则、5 contracts/58 条款、8 场景、19 交付行）；详情文件 Status `Planned`、Last Updated `2026-11-10`。tasks 阶段转场为「Maintain `Planned`」，日粒度下无可见滞后；implement 阶段刷新由 T044 承接。**无 finding**（名称级 + 内容级均无 index/detail 漂移）。

### Constitution Alignment（D）

- **CRITICAL 1 条**：W13-01（tasks 的完成门与延迟约定对宪法 VII Workflow Gates 的记录面偏离；宪法变体不可降级；锚点复核 validated）。
- 其余：W2 波 0 CRITICAL（plan Constitution Check 覆盖 22 原则、顺序一致；row II/XV 仅证据事实不支持 → W2-10/W2-11 LOW）；W13 波其余 0；合并波 0。
- 层级提示：W2-01 为契约可执行性问题（非宪法）；W13-01 的修复面按技能须拆为「analyze 之外的独立宪法修订 + tasks 侧对齐复核」两步。

### Checklist accountability（H，全量）

- `checklists/requirements.md`：17/17 已勾选，0 个未勾选。
- `checklists/2026-11-10-observer-requirements-quality.md`：38 项全部未勾选；`[Gap]` 7 项 = raised 6 + covered-by 1，`unraised=0 · undispositioned=0` → 阻断 **0**（明细见 W13 节）。
- 合计：`unchecked[Gap]=7 · 阻断=0`。

### Decision Tensions（I pass）

- 判定对象仅 `plan.md`：`## Decision Tensions` 在场、锚点正确、5 条记录（T-001…T-005）字段完整、cost 可映射；确定性程序 6 label 全 pass、0 error / 0 warning（`analyze-decision-tensions-r3.txt`）。**无 finding**。

### Unmapped Tasks / Do-not-flag 复核

- 未映射任务 0；47 行全部落在 story/package 归属。
- 封闭集声明抽查（W13）：SC-006 字段集 delta、GATE-1/2/8、T032 载体边界均合法形态（基线指涉 + 比较单元），不报。
- W2 lane 的 duplication 判定：format facts 的重复属合法信息面（owner 持有拼写），不立 finding。
- `validate-tasks.py` 的 4 条 warning 均已在 § Green Attribution 披露；其中 T016→T024 的披露理由与实际子句对不符 → W3-15（残项 LOW），不另作噪音豁免。

---

## Systemic observations（聚合观察，不提升任何单行评级）

- **S1 — 宪法文本与框架 owner 链的词汇漂移（W13-01）**：宪法 VII 写 `verification.log` 与行内 `<!-- deferred: reason -->`；框架 owner 链（`acceptance-hardening.md` 四条件、tasks GATE-4/§Notes）用 `verification.md` 与 `deferred_tasks=`，`feature-integration.md` 又保留行内注释形式。三方并存，修复须走独立宪法修订 + 对齐复核；**open（CRITICAL）**。
- **S2 — `check` 的规则集与输入面缺单一所有者（W2-01, W2-06, W2-07, W2-12）**：engine C-09 / format C-12 / data-model V 规则的对应关系需一处收敛，其余引用；四个方向互证；**open（含 1 HIGH）**。
- **S3 — 观测载体封闭面三处不重合（W13-05, W2-02, W13-13）**：FR-013 输入清单、E-10/C-04 载体清单、R-07 解析语法、T007/T010 投影载体互不同构；**open**。
- **S4 — 验收判据与测试行 / 契约的间隙（W13-03, W13-04, W13-07, W13-08；残项 W1-20/W1-21/W1-22）**：SC-001 失败线无断言行、SC-005 二读、journal 写失败无夹具、自由叙述表示形态不可判定；**persisted**。
- **S5 — 状态与身份词汇未收敛（W2-03, W2-04, W13-10, W13-11；残项 W1-15、W2-12、W2-03、W2-11/W2-13 同域）**：`settled` 无脊取值、八键块双定义、spec key / 入口声明无 owner、label 词汇三名并存；**persisted**。
- **S6 — plan 叙述证据面弱于声明（W2-08, W2-09, W2-10, W2-11, W2-13；残项 W2-11）**：feature-ref FR map / mirror inventory、plan Risks SC 指针、row II/XV 证据；均为叙述 / 追溯面，封顶 LOW；**persisted**。
- **S7 — 轮 2 门禁文本缺陷已修（W3-07/08/09/10）**：GATE-1 落点回到受制裁根、包含性声明获得具名基线、DoD-8 获得重测行、单一顺序权威成立；修复后全部门禁 exit 0；**resolved this round**。
- **S8 — 同 spec 双线前提缺口（W13-06；残项 W2-08）**：需求与 plan/契约两侧仍未把「两条线解析到同一 spec 目录」写成显式前提或判定；**open**。

---

## Metrics

- **检测**: 主表 findings 29（W13 16 · W2 13）；delta-only：fixed 4 · re-detected 18 · persisted 22 · new 11 · rejected 1（Appendix A）；主表 ≤50，无 overflow。
- **评级（validated，主表）**: **CRITICAL 1 · HIGH 1 · MEDIUM 11 · LOW 16**；29 行。全量开放账（含 22 残项）：C1 · H1 · M23 · L26 = **51**。
- **C/H 复核**: send 2 · validated 2 · proposed 0；本轮为集成者锚点直读（无独立校验波，见 § C/H 锚点复核）。
- **覆盖**: FR 23/23 任务文本覆盖；FR citation **23/23**（fixed-step）；clauses **58/58** claimed；SC 7/7 row trace（3 处 trace 不一致，W3-11 残项）。
- **制品修改数**: 0；修复动作: 0（只读阶段）。
- **H pass**: `[Gap]` 7/7 处置，阻断 0。
- **自轮 2 以来的制品变更面**: `git diff --stat 60c78e773..HEAD` → 仅 `tasks.md`（24 行，r3 修复）+ r3 修复证据；requirements / plan / data-model / contracts / quickstart / feature-ref 未变。

## Rerun delta

**Resolved Since Last Run（4 条，逐条证据）**：

| Prior ID | R2 severity | Evidence that closed it |
|----------|-------------|--------------------------|
| W3-07 | CRITICAL | `tasks.md:30` GATE-1 改写：`git check-ignore -q .specify/.tmp && mkdir -p .specify/.tmp/096` 前置 + scratch 落 `.specify/.tmp/096/current-names.txt`（比较命令同路径），文末明示受制裁仓库内根；全文件无裸 `/tmp` 字样；`git check-ignore` 实测命中 `.specify/.gitignore:30` 的 `.tmp/` |
| W3-08 | HIGH | `tasks.md:22`（DoD-6 基线指涉）、`:37`（GATE-8 `<implement-entry-base>..HEAD` 四路径 diff）、`:42`（§ Environment Prerequisites 定义 implement-entry base）、`:111`（T004 记录 base sha）、`:211`（T032 基线 diff + 结构不变量）；比较单元覆盖 `STAGE_ARTIFACTS` 双面载体 |
| W3-09 | HIGH | `tasks.md:24`（DoD-8 点名两条重测行与证据落点）、`:68`（§ Premises 引言落点）、`:111`（T004 扩展：11 个计数/token 前提按各自 re-derivation 命令重测，落 `test-evidence/premises-entry.txt`）；合计 14/14 前提有重测行 |
| W3-10 | HIGH | `tasks.md:120`（Foundational 改指引句）、`:122`（行级 `[blockedBy:]` 为唯一顺序权威）、`:161`（T014 增 T006 边）、`:263`（Phase Dependencies 同口径）；`validate-tasks.py` 0 error |
| — 共同证据 | — | `test-evidence/analyze-repair-dispositions-r3-2026-11-10.md` + `analyze-repair-gates-r3-2026-11-10.txt`：validate-requirements ok / pre-analyze requirements·plan·tasks 全 pass / decomposition proceed / validate-tasks 0 error(4 disclosed warn) / clause coverage ok，全 exit 0 |

**Re-detected（18 条：轮 2 ID → 轮 3 ID；同一事实的再检出，评级按轮 3 检测方读值）**：

| R2 ID | R2 sev | R3 ID | R3 sev | 变化 |
|-------|--------|-------|--------|------|
| W1-01 | MEDIUM | W13-02 | MEDIUM | 持平（FR-011 九/八类） |
| W1-07 | MEDIUM | W13-09 | MEDIUM | 持平（崩溃结算） |
| W1-08 | MEDIUM | W13-06 | MEDIUM | 持平（同 spec 双线） |
| W1-10 | MEDIUM | W13-08 | MEDIUM | 持平（自由叙述表示形态） |
| W1-12 | MEDIUM | W13-05 | MEDIUM | 持平（FR-013 封闭输入清单） |
| W1-16 | LOW | W13-15 | LOW | 持平（席位引用） |
| W1-19 | MEDIUM | W13-04 | MEDIUM | 持平（SC-005 二读） |
| W2-02 | MEDIUM | W2-04 | MEDIUM | 持平（`settled` 无脊取值） |
| W1-04 | MEDIUM | W13-10 | LOW | **降级**（spec key owner） |
| W1-05 | MEDIUM | W13-11 | LOW | **降级**（入口声明 owner） |
| W1-06 | MEDIUM | W13-13 | LOW | **降级**（留存类别） |
| W1-09 | MEDIUM | W13-16 | LOW | **降级**且收窄（仅零长度窗口一面） |
| W1-13 | MEDIUM | W13-12 | LOW | **降级**（写面枚举） |
| W1-14 | MEDIUM | W13-14 | LOW | **降级**（A12 无 FR 承载） |
| W2-01 | MEDIUM | W2-05 | LOW | **降级**（quickstart Seven/eight） |
| W2-09 | MEDIUM | W2-11 | LOW | **降级**（plan row XV 证据） |
| W2-14 | MEDIUM | W2-12 | LOW | **降级**（E-8/C-08 首 append） |
| W2-04 | MEDIUM | W2-01 | **HIGH** | **升级**（C-09/V-16 可执行性；锚点复核 validated） |

评级变化合计：降级 9（均 MEDIUM→LOW，事实与锚点未变，属检测方评级差异，如实并列、不主张任一方高估/低估）+ 升级 1（W2-04→W2-01 M→H，锚点复核确认）+ 持平 8。

**Persisted（22 条，轮 3 波未重报、制品未变 → 维持 open；W3 组已在当前 HEAD 逐条复核锚点）**：

| Prior ID | Sev | 锚点（当前 HEAD）/ 状态 |
|----------|-----|--------------------------|
| W1-11 | MEDIUM | `requirements.md:142`（FR-011 `命令` 字段来源与内容约束未定义；文件自轮 2 未变） |
| W1-15 | MEDIUM | `requirements.md:129/141/234/247`（执行 label vs 实例 label 词汇未定名） |
| W1-17 | LOW | `requirements.md:137/141/144/191/194/197`（`[[STR-NNN]]` 旁复制字面量） |
| W1-18 | LOW | `requirements.md:113/142`（非递减判定对象未点名） |
| W1-20 | MEDIUM | `requirements.md:133/195`（FR-005 谓词无 owner 引用与判定动作） |
| W1-21 | MEDIUM | `requirements.md:134/146/152/153/158/189`（FR-006/015/018/019/021 缺 SC/AS 红腿） |
| W1-22 | MEDIUM | `requirements.md:191/137/111`（SC-001 无 journal 分支不可满足；与 W13-03 为不同层面） |
| W2-03 | MEDIUM | `data-model.md:137` vs `contracts/observer-lifecycle.contract.md:63`（终态 `closed` vs `failed` 无一致脊规则；文件自轮 2 未变） |
| W2-05 | MEDIUM | `feature-ref.md:22-40` vs `:75/:77`（FR-019/FR-021 无交付路径行） |
| W2-07 | MEDIUM | `data-model.md:82-97` + `contracts/journal-engine.contract.md:31`（E-6 per-event 投影与 C-05 natural keys 未定义） |
| W2-08 | MEDIUM | `data-model.md:163` + lifecycle C-05:45 + verification C-05:31 + `plan.md:81`（V-19 distinct-spec 前提未写） |
| W2-11 | LOW | `plan.md:47` vs `data-model.md:110/97`（row VI 证据强于实况） |
| W2-12 | LOW | `data-model.md:33`（`run_stamp`/`run`/`R1` 三名并存） |
| W2-13 | LOW | `contracts/journal-engine.contract.md:19`（C-03 互斥/组合规则未决） |
| W3-06 | LOW | `tasks.md:168`（T017 仅 V-1…V-13/V-16/V-17；V-14/15/18/19/20 无归属行 — 本轮实测原文未变） |
| W3-11 | MEDIUM | `tasks.md:348/351/353`（SC-001 缺 T047、SC-004 多 T019、SC-006 缺 T024 — 本轮实测不变） |
| W3-12 | MEDIUM | `tasks.md:193`（T027 `[blockedBy: T026]`）vs `:291`（「T026/T027 并行」）— 本轮实测不变 |
| W3-13 | MEDIUM | `tasks.md:284`（「Story complete before moving…」）vs `:96`（wp04 含 T021–T022）与 `:100`（wp03 先于 wp04）— 本轮实测不变 |
| W3-14 | LOW | `tasks.md:286-295`（并行叙述点名 T006/T018/T031/T032）vs 各行无 `[P]`（`:124/:163/:210-211`）；T004 `[P]` 的 T001 边问题维持 — 本轮实测不变 |
| W3-15 | LOW | `tasks.md:372`（披露理由「C-03 before C-04」与实际子句对 T016→T024 不符）— 本轮实测不变 |
| W3-16 | LOW | `tasks.md:98`（pre-change-measurements 已披露为 Setup 例外，但 `notes/quickstart-run.md` 由 T045 写入、T001 创建，仍未列入例外 — 部分收窄，维持 open） |
| W3-17 | LOW | `tasks.md:191`（T025 未写 H2 位置）vs `:194`（T028 pin「immediately before the compiled Wrap-up」）— 本轮实测不变 |

**New Since Last Run（11 条）**：W13-01（CRITICAL）、W13-03（MEDIUM）、W13-07（MEDIUM）；W2-02（MEDIUM）、W2-03（MEDIUM）；W2-06、W2-07、W2-08、W2-09、W2-10、W2-13（LOW）。

**Superseded**：本轮 0 条新增；轮 2 的后继关系维持（W3-03 → W3-12 + W3-14；W3-05 → W3-09〔已于本轮回修 fixed〕）。

**Rejected（维持）**：W1-03 → Appendix A，不重报。

**Headline（双向陈述）**：轮 2 的 1 CRITICAL + 3 HIGH 已全部处置并验证（4 fixed，修复后门禁全绿）；但本轮重扫**不是 clean rerun**——新增 1 CRITICAL（W13-01）与 1 HIGH（W2-01，同面升级并锚点确认）。**「清空的旧账」与「干净的重跑」是不同声明，本报告两者分列**；按技能 §9，CRITICAL 未处置前不得进入 `/speckit.implement`。

---

## Appendix A — Rejected findings（轮 1 校验拒绝；维持，不静默丢弃）

| ID | 原 Severity | Verdict | 保留理由 |
|----|-------------|---------|----------|
| W1-03 | HIGH | reject（轮 1 校验波） | 下游制品（`tasks.md:110` T003、`:212` T033、`:22` DoD-6、`plan.md:126` T-005）已把 SC-006 基线落到具名持久路径 `test-evidence/digest-fieldset-baseline.txt`，并给出可复跑采集命令与比较单元；requirements 文本未内联路径属表述性省略。轮 2、轮 3 复核均维持 rejected、不重报。原始证据边界见 `test-evidence/analyze-validation-wave.txt`「W1-03」块。 |

## Anomaly

`ANOMALY: none` —— 无未处置异常；无 in-passing repair（只读阶段，未触碰 spec 制品）。固定步本轮 `status: ok`（clause coverage + decision tensions 双绿）；`[clause-unparsable] 107` 为语料级既有条件，已在固定步输出中照实呈现，非静默吸收。C/H 复核按编排指令采用集成者锚点直读（未派独立校验波，已在 § C/H 锚点复核明示边界）；W13-01 / W2-01 按任务要求照常出报告、不修复。
