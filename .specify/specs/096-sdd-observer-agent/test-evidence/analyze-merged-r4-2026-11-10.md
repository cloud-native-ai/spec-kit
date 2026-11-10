# Analyze — Merged Report, Round 4（096-sdd-observer-agent）

- **Line / Run**: `096-sdd-observer-agent` / `r20261110T081104Z-b096`
- **Stage**: analyze（单 Worker 串行；第四轮重过门——r4 修复面复裁 + 全 spec 检测 + 跨制品一致性）
- **Round**: 4（prior report: `test-evidence/analyze-merged-r3-2026-11-10.md`；repair commit: `05491c0a7`；repair 记录: `test-evidence/analyze-repair-dispositions-r4-2026-11-10.md` + `test-evidence/analyze-repair-gates-r4-2026-11-10.txt`）
- **Date**: 2026-11-10
- **Authority**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` + `references/validation-and-report.md`；`.specify/constitution.md`（v1.19.0，22 原则 I–XXII）
- **Read domain（本轮全量）**: `requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`contracts/`（5 页）、`quickstart.md`、`feature-ref.md`、`research.md`、`checklists/`（2 份）、`.specify/constitution.md`、`.specify/features.md` 096 行、`.specify/features/096.md`；外围权威（仅用于验证 spec 引用的事实面）：`shared/workflow/acceptance-hardening.md` § Gates、`templates/commands/implement.md`、`scripts/python/closure-acceptance-check.py`、`.gitignore`
- **Write surface**: 本文件 + `test-evidence/analyze-{clause-coverage,decision-tensions}-r4.txt` + Wrap-up 记账；未修改任何 spec 制品，未执行任何修复（只读阶段）
- **Merge protocol（确定性归并）**: 分节 W13 → W2（本节 + 合并波）；各节内按 ID 字典序；跨波重复 ID **0 条**。**r3 报告存在两处序号复用**（`W2-05`、`W2-13` 同时用于新检出与残项）——本轮残项表保留其 r2 原 ID 并加 `(r2)` 后缀消歧，主表沿用 r3 已分配 ID，不改任何事实、不作重评级。
- **C/H 复核（本轮变体）**: 按编排指令**单 Worker 串行**（`requested=24` / `effective=1` / `effective_reason=budget-reserve`，evidence form `budget-readings`），本轮**未派独立校验波**；`validated` 指锚点事实经本 Worker 直读确认，独立性弱于 fresh-context 校验波，边界在 § C/H 锚点复核 明示。send 3（2 个已修项复裁 + 1 个新检出）· validated 3 · proposed 0。

---

## Top summary — C/H count and per-item pointers（不修复）

**CRITICAL（validated，0 条）**：无。上轮唯一 CRITICAL（W13-01）经 r4 修复并复裁为 **fixed（validated）**。

**HIGH（validated，1 条）**：

| ID | Category | Severity（validated） | Anchor（逐条指针） | Fact pointer（一句话） |
|----|----------|----------------------|--------------------|------------------------|
| W13-17 | 完成门记录面（tasks ↔ 框架 owner 链） | **HIGH**（anchors validated: direct re-read；修复引入的新检出） | `tasks.md:33`（GATE-4：SC 状态行写入 `verification.log`）↔ `.gitignore:37`（`*.log`，`git check-ignore` 实测命中该路径）↔ `shared/workflow/acceptance-hardening.md:46`（四条件第 2 条要求 `verification.md`）↔ `templates/commands/implement.md:50/58/60`（implement 产出 `verification.md`；closure checker 只读 `verification.md`）↔ `scripts/python/closure-acceptance-check.py:18/87`（`REQUIRED_INPUTS` 含 `verification.md`）↔ `.specify/features/096.md` § Status Criteria（写 `verification.md`） | r4 修复把 GATE-4 对齐到宪法 VII 的字面 `verification.log`，但该路径被 `.gitignore` 默认排除（`*.log`；force-add 未在任何任务行声明）、且框架实施链（acceptance-hardening / implement 模板 / closure checker）只认 `verification.md`——同一轮实现要么写两份互相矛盾的记录，要么必有一条门失败。 |

**Severity distribution（本轮主表，validated）**: **CRITICAL 0 · HIGH 1 · MEDIUM 12 · LOW 16 —— 主表 29 行**（≤50 上限）。另有**r2 遗留残项 22 行**（全为 MEDIUM/LOW）逐条列于 § Rerun delta，不聚合、不静默；全量开放账 = **C0 · H1 · M24 · L26 = 51**（51 = 29 现役行 + 22 残项行）。

**门禁结论须双向陈述（不构成「ready to implement」）**：轮 3 的 1 CRITICAL（W13-01，宪法 VII）与 1 HIGH（W2-01，C-09/V-16 可执行性）已在实际树中 **fixed**（repair commit `05491c0a7`；修复后全部门禁 exit 0，r4 证据可复跑）；但**本轮重扫不是 clean rerun**——修复本身在相反方向引入 1 条新 HIGH（W13-17：GATE-4 记录载体与框架实施链互斥），另新增 1 条 MEDIUM（W13-18：FR-004 的 owner 锚点漂移）。按技能 §9 与 headline 规则，**任何 open CRITICAL/HIGH 未处置前不得进入 `/speckit.implement`**；本阶段只读，未修复。

---

## C/H 锚点复核（单 Worker 直读；本轮无独立校验波）

- **方法**：按编排指令采用单 Worker 串行、锚点直读复核（`requested=24` / `effective=1` / `effective_reason=budget-reserve`）；MEDIUM/LOW 不进入复核。标记词：`validated`（锚点事实成立）或 `proposed`（锚点未成立/证据不足）。本轮结果：**send 3 · validated 3 · proposed 0**。**边界**：validated 的独立性弱于 fresh-context 独立校验波——本报告不把「锚点直读」表述为「独立校验」；若需独立确认，应在 `/speckit.implement` 前补派校验波。
- **W13-01（轮 3 CRITICAL）— validated fixed**：`tasks.md:33` 的 GATE-4 现要求「every Success Criterion of `requirements.md` has `SC-NNN_status=`」，载体为 `verification.log`，条件 owner 拆为宪法 VII（every-SC 记录 + zero-open 由 GATE-3 承载）与 acceptance-hardening（final-path pass、smoke 字段）；`:60` § Task State Sigil 与 `:381` § Notes 均改为行内 `<!-- deferred: reason -->`。全 spec 目录（排除 `test-evidence/`）对 `verification.md` / `deferred_tasks=` 的 grep 命中 **0**。**evidence_not_supported**：修复面只覆盖 tasks 侧；框架 owner 链（`acceptance-hardening.md:46`、`implement.md:50/58/60`、closure checker）仍为 `verification.md`——该残差正是新检出 W13-17 的事实面，r4 disposition 已将其登记为「框架级、analyze 之外」但未评估其对 GATE-4 可满足性的影响。
- **W2-01（轮 3 HIGH）— validated fixed**：`contracts/journal-engine.contract.md:55`（C-09：规则集改为 V-1…V-13 与 V-17，明示 V-16 不在其内）、`:43`（C-07 点名为 V-16 唯一执行点）、`data-model.md:160`（V-16 标注 append-time、`check` 不评估）、`tasks.md:168`（T017 同步为 V-1…V-13 与 V-17 + V-16 由 append 承担）。全 spec 中 V-16 的 4 处提及自洽（grep 实测），无 `V-16…V-17` / `V-16/V-17` 残留。**evidence_supported**：该条款现可执行——`check` 不再需要执行身份输入。**evidence_not_supported**：无。
- **W13-17（本轮新检出 HIGH）— validated（anchor re-read）**：`tasks.md:33` 原文要求 SC 状态行落在 `.specify/specs/096-sdd-observer-agent/verification.log`；`git check-ignore -v` 实测 `.gitignore:37` 的 `*.log` 命中该路径（exit 0），`verification.md` 不命中（exit 1）；`.specify/.gitignore:22` 注释明确「lives in the spec's verification.md」；`acceptance-hardening.md:46` 第 2 条要求 `verification.md`；`implement.md:50` 输出 `verification.md`、`:60` 明言 checker「reads `SC-NNN_status=` rows in `REQUIREMENTS_DIR/verification.md` and nothing else」；`closure-acceptance-check.py:87` 的 `REQUIRED_INPUTS` 含 `verification.md`；`.specify/features/096.md` § Status Criteria 第 1 条写 `verification.md`。**evidence_supported**：以上全部首读原文。**evidence_not_supported**：本 spec 内没有任何一种写法能同时满足宪法 VII 字面（`verification.log`）与框架实施链（`verification.md`）——根因在宪法文本与框架 owner 链的词汇漂移（S1），按技能须在 analyze 之外以独立宪法修订处置；本复核只确认锚点事实，不提出修复方向。

---

## Merged findings

### Wave W13 — requirements + checklist + tasks（17 rows；读域 `requirements.md` + `checklists/` + `tasks.md`）

本波未判 G（注册表）与 I（decision-tension 判决对象），条款覆盖率记账与固定步由合并波承接。检测面：A 重复 / B 歧义 / C 欠指定 / D 宪法对齐 / E 覆盖缺口 / F 不一致 / H 清单问责。

| ID | Severity | propagation_surface | 锚点 | 一句话事实 | 建议归属 |
|---|---|---|---|---|---|
| W13-02 | MEDIUM | requirements.md（Key Entities）→ data-model E-5 / tests | requirements.md §FR-011:142 ↔ §Key Entities「记录条目」:181；checklist CHK018:36 | FR-011 要求每个条目恰好承载九类信息（含序号），而 Key Entities 的「记录条目」仍写「承载八类信息」，同一产物内计数矛盾。（carried over） | /speckit.requirements（将 Key Entities 改为九类并同步信息面表述） |
| W13-03 | MEDIUM | SC-001 → 验收测试行 | requirements.md §SC-001:191、§FR-011:142；tasks.md T008:139、T016:162、§SC→row trace:348 | SC-001 的失败线覆盖判据（每个阶段至少有阶段开始条目或被 `observer-gap` 点名）没有契约测试行断言它：T008 只覆盖零失败夹具的 stage 覆盖、T016 只断言单条 gap 行，T045 为端到端 quickstart。（carried over） | /speckit.tasks（补断言行）或 /speckit.requirements（收窄表述） |
| W13-04 | MEDIUM | SC-005 → T037 实现断言 | requirements.md §SC-005:195、§US5 AS2:104、§FR-007:135；tasks.md T037:232；checklist CHK023:41 | SC-005 与 US5 AS2 允许「被拒绝或串行化」两种结果，而 FR-007 的双机制（driver 不派发 + 引擎单写者拒绝）与 T037 的 exit-3 断言只承认「拒绝」一种可观测结果。（carried over；C-09 r4 修复后「拒绝」侧契约更完整，二读仍未收敛） | /speckit.requirements（收敛为单一可观测结果） |
| W13-05 | MEDIUM | FR-013 → T007/T010 投影实现 | requirements.md §FR-013:144；tasks.md T007:125、T010:144；checklist CHK006:18 | FR-013 以「限定为」封闭观测输入清单，但 T007/T010 把「meta 包络」与「两条窄语法」当作投影载体，这两类载体不在 FR-013 的枚举内。（carried over） | /speckit.requirements（扩展清单或按引用指名 owner） |
| W13-06 | MEDIUM | FR-003/FR-010 → driver / engine 路径规则 | requirements.md §FR-003:128、§FR-010:141、§FR-021:158、§Edge Cases:116；checklist CHK020:38、CHK021:39 | FR-003 保证「不同线 MUST NOT 共享 journal」，FR-010 又把 journal 固定为 spec 目录单一文件；两条线指向同一 spec 目录时两条款互相冲突且该状态未被定义。（carried over） | /speckit.requirements（排除该状态或定义同 spec 多线规则） |
| W13-07 | MEDIUM | Edge Cases → 失败夹具 | requirements.md §Edge Cases:112、§FR-009:137、§FR-010:141；tasks.md T023:186、T024:187 | Edge Cases 的「journal 写入失败（权限 / 磁盘）」要求以执行 `.status` 与状态脊取证并按 `observer-gap` 披露，但 T023/T024 只覆盖启动失败与中途终止，没有对应夹具或断言行。（carried over） | /speckit.tasks（补 journal 写失败夹具 / 断言） |
| W13-08 | MEDIUM | FR-011/SC-004 → T008/T017 表示形态 | requirements.md §FR-011:142、§SC-004:194；tasks.md T008:139、T017:168；checklist CHK007:19、CHK014:29 | FR-011 只规定九类信息与封闭性，未定义条目的表示形态（表格行 vs 段落），SC-004(c) 的「自由叙述条目」反例判据因此在需求面不可判定，只存在于 T008/T017 的实现约定（single nine-column table）。（carried over） | /speckit.requirements（为表示形态指定 owner 或写入信息面） |
| W13-09 | MEDIUM | FR-007/FR-008 → driver 派发与夹具 | requirements.md §FR-007:135、§FR-008:136；tasks.md T023:186、T024:187；checklist CHK011:26 | FR-007 以「前一个执行 `.status` 未结算」禁止下一次派发，FR-008 又允许失败后重启；执行崩溃且无 `.status` 的情形既构成「永不结算」也构成「已终止」，两条款互相冲突，T023 的 mid-run-kill 夹具正使用 unsettled / failed status envelope。（carried over） | /speckit.requirements（定义崩溃情形的结算判定与有界阻塞） |
| W13-10 | LOW | FR-004 → journal 头部 / 实例身份 | requirements.md §FR-004:129；checklist CHK002:14 | FR-004 的实例身份函数依赖「spec key」，但 requirements.md 未定义其派生来源与唯一性范围。（carried over） | /speckit.requirements（定义或按引用指明 owner） |
| W13-11 | LOW | FR-023 → T025 driver 文本 | requirements.md §FR-023:160；tasks.md T025:191；checklist CHK003:15 | FR-023 的关闭开关挂在「入口声明」上，但该声明的载体、位置与解析格式在本规格未定义（T025 才落到 driver SKILL.md）。（carried over） | /speckit.requirements（声明 owner 并引用） |
| W13-12 | LOW | FR-016 → T019/T031 写面审计 | requirements.md §FR-016:150、§US4 AS1:88；checklist CHK004:16 | FR-016 的「自身执行运行产物」未被枚举或按引用拥有（A9 仅给布局引用），US4 AS1 的写面审计无法判定锁文件 / 游标 / 临时文件属写面内或写面外。（carried over） | /speckit.requirements（枚举或引用运行产物布局并给审计判据） |
| W13-13 | LOW | FR-014 → T006 journal-format 事实 | requirements.md §FR-014:145、§A9:249；tasks.md T006:124；checklist CHK005:17 | FR-014 的「留存类别」词表与「可解析」判定未在需求面定义为受拥有的封闭集合，只留给实现期 T006 的 journal-format 事实。（carried over） | /speckit.requirements（声明 owner 与可解析判据边界） |
| W13-14 | LOW | A12 → T032/T047/GATE-8 断言 | requirements.md §A12:252；tasks.md T032:211、T047:254、§GATE-8:37；checklist CHK036:63 | 「journal 不进阶段产物表」只作为假设 A12 存在，没有对应的 FR / 门禁条款承载（断言侧由 T032/T047/GATE-8 覆盖）。（carried over） | /speckit.requirements（升为 FR）或 /speckit.tasks（记录 disposition） |
| W13-15 | LOW | FR-001 → 模板文本断言 | requirements.md §FR-001:126；tasks.md T018:163、T019:169；checklist CHK009:21 | FR-001 对「stage executor / reviewer / reporter 席位」的 MUST NOT 未按引用给出三个席位的可核对定义。（carried over） | /speckit.requirements（补三条引用指针） |
| W13-16 | LOW | FR-013 → 引擎缺口逻辑 | requirements.md §FR-013:144；checklist CHK017:32 | 零长度观察缺口（窗口起止同一秒）是否写入或抑制未被裁决，FR-013 只定义端点来源、未定义该边界。（carried over） | /speckit.requirements（显式裁决写入或抑制） |
| W13-17 | **HIGH** (validated: anchors re-checked) | tasks GATE-4 → `/speckit.implement` 与 `closure-acceptance-check.py`（状态翻转） | `tasks.md:33`（`verification.log` every-SC）↔ `.gitignore:37`（`*.log` 命中，check-ignore 实测）↔ `shared/workflow/acceptance-hardening.md:46`（`verification.md`）↔ `templates/commands/implement.md:50/58/60`（产出并只读 `verification.md`）↔ `scripts/python/closure-acceptance-check.py:18/87`（`REQUIRED_INPUTS` 含 `verification.md`）↔ `.specify/features/096.md` § Status Criteria（`verification.md`） | r4 修复把 GATE-4 对齐到宪法 VII 字面 `verification.log`，但该路径被 `.gitignore` 默认排除（force-add 未在任何任务行声明），且框架实施链只认 `verification.md`（closure checker 的输入清单）——GATE-4 与状态翻转门不可同时满足：写 `verification.log` 会被 checker 判缺输入且默认不随提交留痕；写 `verification.md` 则 GATE-4 字面失败。**NEW（修复引入）**。 | 决策项（analyze 之外）：宪法 VII 的 `verification.log` 字面须经独立宪法修订对齐框架 owner 链（`verification.md`），并同步 `.gitignore` 陷阱与 closure checker；在此之前 GATE-4 无法既守宪法字面又通过状态翻转门。本阶段不修复。 |
| W13-18 | MEDIUM | FR-004 → T025 / T027 owner 锚点 | requirements.md §FR-004:129（「键名与形状 owner：`skills/external/sdd-loop-driver/SKILL.md` §状态脊」）↔ `contracts/observer-lifecycle.contract.md` C-04:23-37（「owned by `SKILL.md` § SDD Observer」）↔ `tasks.md` T025:191（新建 H2 `## SDD Observer`）、T027:193（指向 `SKILL.md` 的 record-section owner）↔ `research.md` R-01:6-12 / R-07:52-56（状态脊程序位于 `references/stage-prompts.md`，SKILL.md 无 §状态脊 H2） | FR-004 把记录节的键名与形状 owner 指为 `SKILL.md` §状态脊，但 SKILL.md 没有该 H2（状态脊正文在 `references/stage-prompts.md` §状态脊），plan/tasks/lifecycle 一侧的 owner 是新建的 `SKILL.md` § SDD Observer——同一形状有两个 owner 锚点，且需求侧锚点不存在。**NEW**。 | /speckit.requirements（把 owner 锚点改为 `SKILL.md` § SDD Observer 并按引用持有形状），或 /speckit.plan（统一指向 stage-prompts 指针 + SDD Observer 节） |

**H — Checklist Accountability（W13 分片，`checklists/2026-11-10-observer-requirements-quality.md`）**

清单 38 项全部未勾选（`[ ]` 38 / `[x]` 0）；H 门禁范围是带 `[Gap]` 标签的未勾选项，全部给出处置（处置对象沿用 r3 编号，r4 事实未变）：

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

**Evidenced Absences（W13 读域内已核对、无 findings 的覆盖断言）**：FR-001…FR-023 每项至少被一条 tasks 行引用（无零覆盖 FR）；SC-001…SC-007 均在 §SC→row trace 有行与证据路径（SC-001 的失败线判据见 W13-03）；T001–T047 共 47 行，包分区 13+5+9+15+5(Setup)=47，无 ID 双属；58 条 `[green:]` 认领与 r4 门禁读数一致（claimed 58 / FR 23/23）；GATE-1 的受制裁临时根（`.specify/.tmp/096`）在 tasks.md 全文无裸 `/tmp`（grep 实测 0）；r4 修复未触碰 `[green:]` 标签与包图。

### Wave W2 — plan 与设计产物（12 rows；读域 `plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`research.md`、`contracts/` 5 页）

本波显式移交：条款/FR 覆盖记账与 Checklist H → 合并波；tasks 覆盖 → W13 分片；feature 注册表 → 合并波；往轮残项与重跑增量 → 合并波。确定性判定消费：`validate-decision-tensions.py` → `status: ok`（5 records，六类标签 0，exit 0）。

| ID | Severity | propagation_surface | 锚点 | 一句话事实 | 建议归属 |
|---|---|---|---|---|---|
| W2-02 | MEDIUM | E-6/E-10 → T010 引擎投影 | `data-model.md` E-6 `line-start` 行（L82）、E-10（L141）；`research.md` R-07（L56）；`plan.md` L220；`contracts/journal-engine.contract.md` C-04 | E-6 把状态脊 U0 块声明为 `line-start` 的主载体，但 E-10 / C-04 的封闭载体清单与 R-07「只解析两条窄状态脊 prose 语法」的解析面都不含 U0 块语法，故声明式投影产不出这条 `min_persistent: 1` 行。（carried over） | data-model E-6/E-10 + research R-07（补 U0 语法入封闭解析面或改正载体列） |
| W2-03 | MEDIUM | lifecycle C-04 ↔ data-model E-9 → T025 形状落地 | `contracts/observer-lifecycle.contract.md` C-04（标题 L23、正文 L25–41）；`data-model.md` E-9（L121–137）；`feature-ref.md` 第 9 行（L30） | 同一份八键观察者记录块在 lifecycle C-04 与 data-model E-9 各定义一次，C-04 一边自称「key and shape owner」、一边把形状所有权让给 `SKILL.md` § SDD Observer，该块没有唯一声明所有者。（carried over） | lifecycle C-04 / data-model E-9（择一为 owner，另一处改引用；修正 C-04 标题） |
| W2-04 | MEDIUM | E-3/E-9 → T024 脊记录断言 | `data-model.md` E-3 States（L36）、E-9 state 行（L127）；`contracts/observer-lifecycle.contract.md` C-04 state 行（L31） | E-3 称执行状态 `started → settled \| failed` 会记录在状态脊观察者记录节，但 E-9/C-04 的 `state` 值域是 `started\|failed\|disabled\|closed`，`settled` 没有可记录取值。（carried over） | data-model E-3/E-9（映射执行态到脊记录值域或声明两套状态模型） |
| W2-05 | LOW | quickstart → 读者 | `quickstart.md` L3（对照 S-0…S-7，L5–102）；`plan.md` L31、L236 | quickstart 首句写「Seven walk-through scenarios」，实际列出八个（S-0…S-7），plan 两处均计为 8。（carried over） | quickstart.md 首句（改为 eight） |
| W2-06 | LOW | quickstart S-3 → 读者 | `quickstart.md` S-3（L59）；`contracts/journal-engine.contract.md` C-09（L55） | quickstart S-3 说 `check` 对「`data-model.md` V-1…V-13 中每条规则」报 `file:line`，而 r4 后的 C-09 规则集是 V-1…V-13 **加 V-17**，quickstart 仍少报 V-17 一项。（carried over；r4 修复使缺失面从两项缩为一项） | quickstart S-3（改为引用 C-09 规则集而非枚举子集） |
| W2-07 | LOW | V-12/C-12 → T017 checker | `data-model.md` V-12（L156）；`contracts/journal-format.contract.md` C-12（L71–73） | journal-format C-12 把段落、列表与围栏代码块都判为 finding，而 `check` 被要求实现的 V-12 只点名「叙述性段落」，列表/围栏块处理未规定。（carried over） | data-model V-12（范围对齐 C-12） |
| W2-08 | LOW | feature-ref → 契约映射审计 | `feature-ref.md` L57（FR-001 行）；`contracts/observer-role.contract.md` C-04（L23–27） | Role C-04（承载 SC-004 强制原文的禁止条款）自身引用 FR-001，但 FR→Contract map 的 FR-001 行只列 role C-01…C-03 与 verification C-08，漏掉 C-04。（carried over） | feature-ref FR→Contract map |
| W2-09 | LOW | plan § Risks → 叙述面（none） | `plan.md` L277（§ Risks）；`feature-ref.md` L87（SC-003）、L91（SC-007） | Plan 风险表把「无 journal 收线」的缓解证据写成「SC-001 的 failure-path criterion」，但 feature-ref 的 SC 映射给 SC-001 的是覆盖夹具度量，failure path 属 SC-003/SC-007。（carried over） | plan § Risks |
| W2-10 | LOW | plan row II → 叙述面（none） | `plan.md` L43（Constitution Check 第 II 行） | Constitution 第 II 行证据引用「§ Feature Integration」，但 plan.md 无此章节。（carried over） | plan（补章节或改引用） |
| W2-11 | LOW | plan row XV → 叙述面（none） | `plan.md` L56（Constitution Check 第 XV 行）；`quickstart.md`（全文） | Constitution 第 XV 行证据称 quickstart「在首次使用时定义了 journal / observer / gap」，但 quickstart.md 对这三个词没有任何定义句。（carried over） | plan 第 XV 行或 quickstart（首次出现处各加一句定义） |
| W2-12 | LOW | E-8/C-08 → 引擎首次 append 语义 | `data-model.md` E-8（L114–118）、V-17（L161）；`contracts/journal-engine.contract.md` C-08（L47–51） | E-8 规定「无任何条目时」gap 窗口起点取脊记录节的 `started_at`，但 C-08 与 V-17 只在「存在上一条目的 `observed_at`」时触发 gap，无条目分支永不生效，两处对首次执行是否产生 gap 的语义不一致。（carried over） | data-model E-8 / engine C-08（单点声明首次 append 的 gap 语义） |
| W2-13 | LOW | feature-ref → 交付镜像清单（none） | `feature-ref.md` 第 1–19 行（第 4 行与 L42 的生成器句）；`plan.md` § Mirror Obligations 第 2 行（L175） | feature-ref 的 19 行「file-level inventory」把 agent、engine、skill 的镜像各自列为独立行，却漏掉 plan.md § Mirror Obligations 第 2 行要求「必须同样落地」的 `.specify/shared/declarations/facts/journal-format.yaml` 镜像。（carried over） | feature-ref delivered-path inventory（补镜像行） |

**W2 波系统性观察（原样保留并更新）**：① `check` 的规则集与输入面缺单一所有者——r4 修复后 C-09 ↔ T017 ↔ data-model V 规则的主链已自洽（W2-01 fixed），残项只余 quickstart 子集（W2-06）、V-12/C-12 范围（W2-07）与首次 append 语义（W2-12）；② 两处重复枚举需收敛（W2-03 脊记录节八键、W2-04 执行态 vs 脊 state 值域）；③ 宪法对齐：plan 的 Constitution Check 覆盖宪法 v1.19.0 全部 22 个标题、顺序一致，仅第 II、XV 两行证据事实不支持（W2-10/W2-11，LOW）。

### Merge wave — cross-artifact serial pass（requirements ↔ plan ↔ tasks ↔ contracts ↔ registry；**0 条新 finding**）

**固定步（技能 §3，read-only）判定——phase-visible**：

- `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs` → **`status: ok`，exit 0**（证据：`test-evidence/analyze-clause-coverage-r4.txt`）。读值：claimed clauses **58**；baseline 640 names，0 beyond baseline；`[fr-uncovered]` **23/23**；扫描 291 文件（107 个语料级既有 unparsable，非 096 特有）；0 error / 1 warning（语料级既有）。
- `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/096-sdd-observer-agent` → **`status: ok`**，6 个 label 全 pass（0），5 records，0 error / 0 warning，`high=0`（证据：`test-evidence/analyze-decision-tensions-r4.txt`）。I pass 无 finding。
- **消费既有记录（不重跑）**：`validate-requirements.py` → `status: ok`，6 标签全 pass（254 行 / 30 定义行 / 3 shared strings），0 error / 0 warning，exit 0；`pre-analyze-check.py --stage requirements|plan|tasks` → 均 `decision: pass`，0 error（82 advisory 均为本特性待创建路径）；`decomposition-check.py --mode tasks` → `decision: proceed`（23 FR / 47 tasks）；`validate-tasks.py` → `PASS (with warnings)`，`0 error(s), 4 warning(s)`，exit 0——均取自 `test-evidence/analyze-repair-gates-r4-2026-11-10.txt`（运行于与 HEAD `05491c0a7` 内容相同的树；r4 后 spec 制品未再变化）。

**跨波一致性复核注记（对既有行，不改变其评级；关联对不合并）**：

1. **W13-01（fixed）↔ W13-17（new HIGH）**：同一记录面（SC 状态记录的载体名）在两个方向上都存在冲突——r4 修复前是 tasks×宪法（`verification.md` vs `verification.log`），修复后是 tasks×框架实施链（`verification.log` vs `verification.md`）。**旧账清空 ≠ 重跑干净**：本报告分开陈述。
2. **W13-05 ↔ W2-02（观测载体封闭面）**：需求侧 FR-013「限定为」清单、plan 侧 E-10/C-04 载体清单 + R-07 窄解析面、tasks 侧 T007/T010 投影载体，三处读法互不重合，两侧均 open，互证。
3. **W13-09 ↔ W2-12（缺口 / 崩溃语义）**：需求侧 FR-007/008 崩溃结算悬空 vs plan 侧 E-8/C-08 首次 append gap 分支不可达；同一 lifecycle 面两端 open。
4. **W13-04 ↔ W2-01（fixed）**：SC-005 的「拒绝或串行化」二读与 C-07/C-09 的「拒绝」单一可观测结果同向；r4 修复后契约侧完全收敛到「拒绝」，需求侧二读仍未收敛。
5. **W13-03 / W1-22（残项）/ W3-11（残项）（SC-001 三层）**：需求层判据可满足性（W1-22）、tasks 层断言缺口（W13-03）、trace 记账不一致（W3-11）三层各自 open。
6. **W2-03 ↔ W2-04（同块双缺陷）**：E-9/lifecycle C-04 八键块既缺唯一所有者（W2-03）又有 `settled` 值域缺口（W2-04）；与残项 W2-03(r2)（终态 `closed` vs `failed`）共三层，建议一次收敛。
7. **W13-06 ↔ W2-08（残项，同 spec 双线）**：需求侧未排除同 spec 双线 vs plan 侧 V-19 / 两处 C-05 未写 distinct-spec 前提；两侧 open。
8. **W13-10 / W13-11 / W13-18 ↔ W2 lane（身份与 owner）**：spec key（W13-10）、入口声明（W13-11）在需求面均无 owner；FR-004 的 `§状态脊` 锚点在需求面指向不存在的 H2（W13-18），与 plan/tasks 的 `§ SDD Observer` owner 漂移——同一词汇未收敛面。

**结论**：合并波未发现超出两波读域的新 finding（0 条），故不触发第二轮校验派发；W13-17 来自 W13 波的 r4 修复面复裁。

---

## Cross-artifact consistency（合并波一致性总账）

### Coverage Summary

| 量 | 读值 | 来源 / 判定 |
|----|------|-------------|
| FR 定义 / SC 定义 | 23 / 7 | requirements.md 定义行 |
| FR → 任务文本覆盖 | 23/23 | W13 分片 Evidenced Absences（tasks.md 文本） |
| FR citation groups（条款体） | **23/23** | 固定步读值（`analyze-clause-coverage-r4.txt`） |
| 契约条款 | 58 = 13+13+12+10+10 | 五页 `^## C-` 标题；claimed 58（固定步） |
| `[green:]` 认领 | **58/58 恰一次** | 固定步 + `validate-tasks.py` 0 `green-dangling` / 0 `green-clause-collision` |
| SC → row trace | 7/7 行齐全；3 处与行级 citation 不一致（SC-001 缺 T047、SC-004 多 T019、SC-006 缺 T024） | W3-11（残项，open） |
| data-model 规则 → 任务 | V-1…V-13、V-17 → T017；V-16 → T011（append 身份，C-07）；V-14/15/18/19/20 无显式归属行 | W3-06（残项，open；r4 后 T017 集合已与 C-09 一致） |
| 任务行 / 包 | 47 行、4 包、分区 13+5+9+15+5(Setup)=47；无缺号重号；包链严格串行 wp01→wp02→wp03→wp04 | W13 机器核对 |
| 覆盖门可执行性 | GATE-9/T047 可过（固定步 exit 0）；GATE-4 见 W13-17 | `analyze-clause-coverage-r4.txt` + W13-17 |
| 扫描语料 | 291 文件（含 107 语料级既有 unparsable） | 固定步；非 096 特有 |
| 前提重测面 | 14/14 前提有重测行（11 count/token + 3 guard-baseline） | r3 W3-09 fixed，制品未回退 |

### Feature Linkage Summary（G）

- **名称级**：`requirements.md` 的 Feature ID `096` 与名称「SDD 专用观察者与线级观察记录（sdd-observer）」与清单页眉一致；`.specify/features.md` 096 行与 `.specify/features/096.md` 均存在。
- **内容级 / 阶段记录义务（合并波实测）**：索引行 Status `Planned`、Last Updated `2026-11-10`、备注记录 plan 阶段落册（22 项宪法全 Pass、R-01–R-14、10 实体/20 规则、5 contracts/58 条款、8 场景、19 交付行）；详情文件 Status `Planned`、Last Updated `2026-11-10`。tasks 阶段转场为「Maintain `Planned`」，日粒度下无可见滞后；implement 阶段刷新由 T044 承接。**G 无 finding**。详情文件 § Status Criteria 的 `verification.md` 引用不在 G 面判定，归 W13-17（F/D 面）。

### Constitution Alignment（D）

- **open CRITICAL 0 条**：W13-01 经 r4 修复（tasks 三处记录面对齐宪法 VII 字面），复裁 validated fixed；全 spec 其余面未见宪法 MUST 冲突。
- W13-17 **不是**宪法冲突：GATE-4 按宪法字面执行（`verification.log`），冲突对象是框架实施链（非宪法文本）；故评级 HIGH，不升 CRITICAL，且根因处置属独立的宪法修订（analyze 之外）。
- W2 波：plan Constitution Check 覆盖 22 原则、顺序一致；row II/XV 仅证据事实不支持（W2-10/W2-11 LOW）。

### Checklist accountability（H，全量）

- `checklists/requirements.md`：17/17 已勾选，0 个未勾选。
- `checklists/2026-11-10-observer-requirements-quality.md`：38 项全部未勾选；`[Gap]` 7 项 = raised 6 + covered-by 1，`unraised=0 · undispositioned=0` → 阻断 **0**。
- 合计：`unchecked[Gap]=7 · 阻断=0`。

### Decision Tensions（I pass）

- 判定对象仅 `plan.md`：`## Decision Tensions` 在场、锚点正确、5 条记录（T-001…T-005）字段完整、cost 可映射；确定性程序 6 label 全 pass、0 error / 0 warning（`analyze-decision-tensions-r4.txt`）。**无 finding**。

### Unmapped Tasks / Do-not-flag 复核

- 未映射任务 0；47 行全部落在 story/package 归属。
- 封闭集声明抽查：SC-006 字段集 delta、GATE-1/2/8、T032 载体边界均合法形态（基线指涉 + 比较单元），不报。
- W2 lane 的 duplication 判定：format facts 的重复属合法信息面（owner 持有拼写），不立 finding。
- `validate-tasks.py` 的 4 条 warning 均已在 § Green Attribution 披露；其中 T016→T024 的披露理由与实际子句对不符 → W3-15（残项 LOW），不另作噪音豁免。

---

## Systemic observations（聚合观察，不提升任何单行评级）

- **S1 — SC 状态记录面的词汇漂移（W13-01 fixed → W13-17 new HIGH）**：宪法 VII 写 `verification.log`；框架 owner 链（`acceptance-hardening.md:46`、`implement.md:50/58/60`、`closure-acceptance-check.py:18/87`）与 `.specify/features/096.md` 写 `verification.md`；`.gitignore:37` 的 `*.log` 使前者不可提交，`.specify/.gitignore:22` 注释亦指向后者。r4 修复把 spec 对齐到宪法字面后，GATE-4 与状态翻转门变得互斥。**open（HIGH，决策项）**；根因修复须走独立宪法修订 + 框架链同步，属 analyze 之外。
- **S2 — `check` 的规则集与输入面**：r4 后 C-09/C-07/data-model V-16/T017 主链自洽（W2-01 fixed）；残项 W2-06（quickstart 子集）、W2-07（V-12/C-12 范围）、W2-12（首次 append）仍 open，均 LOW。
- **S3 — 观测载体封闭面三处不重合（W13-05, W2-02, W13-13）**：FR-013 输入清单、E-10/C-04 载体清单、R-07 解析语法、T007/T010 投影载体互不同构；**open**。
- **S4 — 验收判据与测试行 / 契约的间隙（W13-03, W13-04, W13-07, W13-08；残项 W1-20/W1-21/W1-22）**：SC-001 失败线无断言行、SC-005 二读、journal 写失败无夹具、自由叙述表示形态不可判定；**persisted**。
- **S5 — 状态与身份词汇未收敛（W2-03, W2-04, W13-10, W13-11, W13-18；残项 W1-15、W2-03(r2)、W2-12(r2) 同域）**：`settled` 无脊取值、八键块双定义、spec key / 入口声明无 owner、FR-004 owner 锚点指向不存在的 H2、label 词汇多名并存；**persisted，本轮新增 W13-18 一个锚点**。
- **S6 — plan 叙述证据面弱于声明（W2-08, W2-09, W2-10, W2-11, W2-13；残项 W2-11(r2)）**：feature-ref FR map / mirror inventory、plan Risks SC 指针、row II/XV 证据；均为叙述 / 追溯面，封顶 LOW；**persisted**。
- **S7 — 门禁文本修复的两次方向性来回（W3-07/08/09/10 fixed in r3；W13-01/W2-01 fixed in r4；W13-17 new）**：旧门禁缺陷已修，但记录面修复在相反方向引入新冲突；**本轮结论：修复须以「两个 owner 同时可满足」为验收判据，而非单侧字面对齐**。
- **S8 — 同 spec 双线前提缺口（W13-06；残项 W2-08(r2)）**：需求与 plan/契约两侧仍未把「两条线解析到同一 spec 目录」写成显式前提或判定；**open**。
- **S9 — tasks 图叙述与行级权威的残余不一致（残项 W3-12, W3-13, W3-14, W3-15, W3-16, W3-17）**：并行叙述点名无 `[P]` 的行、`[blockedBy: T026]` 与「T026/T027 并行」并存、story-complete 句与包图冲突、披露理由与真实子句对不符、quickstart-run.md 例外未列、T025 的 H2 位置未写；行级 `[blockedBy:]` 仍为唯一顺序权威（CRITICAL 面已于 r3 修复），全部维持 MEDIUM/LOW；**persisted**。

---

## Metrics

- **检测**: 主表 findings 29（W13 17 · W2 12）；delta：fixed 2（W13-01、W2-01）· new 2（W13-17、W13-18）· carried over 27 · residue 22 · rejected 1（Appendix A，维持）；主表 ≤50，无 overflow。
- **评级（validated，主表）**: **CRITICAL 0 · HIGH 1 · MEDIUM 12 · LOW 16**；29 行。全量开放账（含 22 残项）：C0 · H1 · M24 · L26 = **51**。
- **C/H 复核**: 独立校验波 0（按编排指令单 Worker 串行）；锚点复核 send 3 · validated 3 · proposed 0；**方法边界**：anchors re-read by this worker, not a fresh-context wave（已在 § C/H 锚点复核 明示）。
- **并发读数**: `requested=24`（U0 声明）· `effective=1` · `effective_reason=budget-reserve`（evidence form `budget-readings`；编排指令以预算保留裁定单 Worker 串行，本报告的检测/复核单元集即为该单 Worker）。
- **覆盖**: FR 23/23 任务文本覆盖；FR citation **23/23**（fixed-step）；clauses **58/58** claimed；SC 7/7 row trace（3 处 trace 不一致，W3-11 残项）。
- **制品修改数**: 0；修复动作: 0（只读阶段）。
- **H pass**: `[Gap]` 7/7 处置，阻断 0。
- **自轮 3 以来的制品变更面**: `git diff --stat 14a7da094..HEAD` → `tasks.md`（8 行，r4 修复）+ `contracts/journal-engine.contract.md`（4 行）+ `data-model.md`（2 行）+ r4 修复证据 2 文件；requirements / plan / quickstart / feature-ref / research / 其余 4 契约未变。

## Rerun delta

**Resolved Since Last Run（2 条，逐条证据）**：

| Prior ID | R3 severity | Evidence that closed it |
|----------|-------------|--------------------------|
| W13-01 | CRITICAL | `tasks.md:33` GATE-4 改为 `verification.log` + every-SC `SC-NNN_status=`（条件 owner 拆为宪法 VII 与 acceptance-hardening）；`:60` 与 `:381` 均改为行内 `<!-- deferred: reason -->`；全 spec 目录（排除 `test-evidence/`）grep `verification.md` / `deferred_tasks=` 命中 0。复裁 validated fixed。**边界**：框架侧词汇漂移未处置，且该残差引出 W13-17。 |
| W2-01 | HIGH | `journal-engine.contract.md:55` C-09 规则集改为 V-1…V-13 与 V-17（明示 V-16 不在其内）、`:43` C-07 为 V-16 唯一执行点；`data-model.md:160` V-16 标注 append-time；`tasks.md:168` T017 同步。全 spec 无 `V-16…V-17` 残留。复裁 validated fixed。 |

**New Since Last Run（2 条，含修复本身引入的）**：

| ID | Severity | 事实 | 来源 |
|----|----------|------|------|
| W13-17 | **HIGH** | GATE-4 的 `verification.log` 记录载体被 `.gitignore:37` 排除，且与框架实施链（acceptance-hardening / implement 模板 / closure checker 的 `verification.md` 输入）互斥——r4 修复在相反方向引入的新冲突。 | r4 修复面复裁（本节 + § C/H 锚点复核） |
| W13-18 | MEDIUM | FR-004 的 owner 锚点 `SKILL.md` §状态脊 在 SKILL.md 中不存在（状态脊正文在 `references/stage-prompts.md`），plan/tasks/lifecycle 的 owner 是新建 `SKILL.md` § SDD Observer。 | 全量重扫（requirements ↔ plan/tasks/contracts） |

**Persisted（22 条，本轮未重报、制品未变或锚点已复核 → 维持 open）**：

| Prior ID | Sev | 锚点（当前 HEAD）/ 状态 |
|----------|-----|--------------------------|
| W1-11 | MEDIUM | `requirements.md:142`（FR-011 `命令` 字段来源与内容约束未定义；文件自轮 2 未变） |
| W1-15 | MEDIUM | `requirements.md:129/141/234/247`（执行 label vs 实例 label 词汇未定名） |
| W1-17 | LOW | `requirements.md:137/141/144/191/194/197`（`[[STR-NNN]]` 旁复制字面量） |
| W1-18 | LOW | `requirements.md:113/142`（非递减判定对象未点名） |
| W1-20 | MEDIUM | `requirements.md:133/195`（FR-005 谓词无 owner 引用与判定动作） |
| W1-21 | MEDIUM | `requirements.md:134/146/152/153/158/189`（FR-006/015/018/019/021 缺 SC/AS 红腿） |
| W1-22 | MEDIUM | `requirements.md:191/137/111`（SC-001 无 journal 分支不可满足；与 W13-03 为不同层面） |
| W2-03 (r2) | MEDIUM | `data-model.md:137` vs `contracts/observer-lifecycle.contract.md:63`（终态 `closed` vs `failed` 无一致脊规则） |
| W2-05 (r2) | MEDIUM | `feature-ref.md:22-40` vs `:75/:77`（FR-019/FR-021 无交付路径行） |
| W2-07 (r2) | MEDIUM | `data-model.md:82-97` + `contracts/journal-engine.contract.md:31`（E-6 per-event 投影与 C-05 natural keys 未定义） |
| W2-08 (r2) | MEDIUM | `data-model.md:163` + lifecycle C-05:45 + verification C-05:31 + `plan.md:81`（V-19 distinct-spec 前提未写） |
| W2-11 (r2) | LOW | `plan.md:47` vs `data-model.md:110/97`（row VI 证据强于实况） |
| W2-12 (r2) | LOW | `data-model.md:33`（`run_stamp`/`run`/`R1` 三名并存） |
| W2-13 (r2) | LOW | `contracts/journal-engine.contract.md:19`（C-03 互斥/组合规则未决；r3 报告曾复用该序号，本表加 `(r2)` 消歧） |
| W3-06 | LOW | `tasks.md:168`（T017 现为 V-1…V-13 与 V-17；V-14/15/18/19/20 仍无显式归属行 — r4 实测原文已更新，结论不变） |
| W3-11 | MEDIUM | `tasks.md:348/351/353`（SC-001 缺 T047、SC-004 多 T019、SC-006 缺 T024 — 本轮实测不变） |
| W3-12 | MEDIUM | `tasks.md:193`（T027 `[blockedBy: T026]`）vs `:291`（「T026/T027 并行」）— 本轮实测不变 |
| W3-13 | MEDIUM | `tasks.md:284`（「Story complete before moving…」）vs `:96`（wp04 含 T021–T022）与 `:100`（wp03 先于 wp04）— 本轮实测不变 |
| W3-14 | LOW | `tasks.md:286-295`（并行叙述点名 T006/T018/T031/T032）vs 各行无 `[P]`（`:124/:163/:210-211`）— 本轮实测不变 |
| W3-15 | LOW | `tasks.md:372`（披露理由「C-03 before C-04」与实际子句对 T016→T024 不符）— 本轮实测不变 |
| W3-16 | LOW | `tasks.md:98`（`notes/quickstart-run.md` 由 T045 写入、T001 创建，未列入 Setup 例外 — 维持 open） |
| W3-17 | LOW | `tasks.md:191`（T025 未写 H2 位置）vs `:194`（T028 pin「immediately before the compiled Wrap-up」）— 本轮实测不变 |

**Superseded**：本轮 0 条新增；轮 2 的后继关系维持（W3-03 → W3-12 + W3-14；W3-05 → W3-09，已于 r3 回修 fixed）。

**Rejected（维持）**：W1-03 → Appendix A，不重报。

**Headline（双向陈述）**：轮 3 的 1 CRITICAL + 1 HIGH 已全部处置并验证（2 fixed，修复后门禁全绿）；但本轮重扫**不是 clean rerun**——修复本身在相反方向引入 1 条新 HIGH（W13-17：GATE-4 记录载体与框架状态翻转链互斥），另有 1 条新 MEDIUM（W13-18）。**「清空的旧账」与「干净的重跑」是不同声明，本报告两者分列**；按技能 §9，W13-17 未决策前不得进入 `/speckit.implement`。

---

## Appendix A — Rejected findings（轮 1 校验拒绝；维持，不静默丢弃）

| ID | 原 Severity | Verdict | 保留理由 |
|----|-------------|---------|----------|
| W1-03 | HIGH | reject（轮 1 校验波） | 下游制品（`tasks.md:110` T003、`:212` T033、`:22` DoD-6、`plan.md:126` T-005）已把 SC-006 基线落到具名持久路径 `test-evidence/digest-fieldset-baseline.txt`，并给出可复跑采集命令与比较单元；requirements 文本未内联路径属表述性省略。轮 2、3、4 复核均维持 rejected、不重报。原始证据边界见 `test-evidence/analyze-validation-wave.txt`「W1-03」块。 |

## Anomaly

`ANOMALY: none` —— 无未处置异常；无 in-passing repair（只读阶段，未触碰 spec 制品）。固定步本轮 `status: ok`（clause coverage + decision tensions 双绿）；`[clause-unparsable] 107` 为语料级既有条件，已在固定步输出中照实呈现，非静默吸收。C/H 复核按编排指令采用单 Worker 直读（未派独立校验波，已在 § C/H 锚点复核 明示边界与 `budget-reserve` 读数）；W13-17 / W13-18 按任务要求照常出报告、不修复。
