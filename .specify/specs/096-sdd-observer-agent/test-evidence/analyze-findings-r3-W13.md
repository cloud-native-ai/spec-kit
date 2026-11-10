# Analyze Findings — Round 3 · Worker W13（requirements · checklist · tasks）

- **轮次 / 波次**: analyze 第三轮（修复后重过门）；并发波 N=2 的 W13 分片（读域互斥）
- **读域**: `.specify/specs/096-sdd-observer-agent/requirements.md`、`.specify/specs/096-sdd-observer-agent/checklists/2026-11-10-observer-requirements-quality.md`、`.specify/specs/096-sdd-observer-agent/tasks.md`
- **命令面**: 只读检测（A 重复 / B 歧义 / C 欠指定 / D 宪法对齐 / E 覆盖缺口 / F 不一致 / H 清单问责）。G 的注册表比对（`.specify/features.md` 等）与 I 的判决对象（`plan.md`）不在本读域，未判；条款覆盖率会计与 C/H 独立校验由编排侧承担。未修改任何产物。
- **结论极性**: 本分片列出本读域内的 findings，不宣布整体 gate 结论。

## Findings（16 行）

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|---|---|---|---|---|
| W13-01 | CRITICAL | tasks.md §Task State Sigil:60、§Notes:381、§GATE-4:33 ↔ `.specify/constitution.md` §VII Workflow Gates:220-225（:223 `verification.log`、:224 行内 `<!-- deferred: reason -->`） | tasks.md 的完成门约定与宪法原则 VII 的 Workflow Gates 文本在记录面上不一致——延迟任务原因（tasks 侧 `verification.md` `deferred_tasks=` vs 宪法行内 `<!-- deferred: reason -->`）与 Pre-Status-Flip 记录（tasks 侧 `verification.md` 且仅 final-path SC + smoke 字段 vs 宪法 `verification.log` 且 every SC）。 | 宪法治理（独立修订，须在 analyze 之外进行）；tasks 侧同时与 `shared/workflow/acceptance-hardening.md` § Gates 条件集对齐后复核。按 analyze 规则：宪法冲突 CRITICAL，不得降级、不得在本技能内稀释。 |
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

## H — Checklist Accountability（`checklists/2026-11-10-observer-requirements-quality.md`）

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

计数：`unchecked [Gap] = 7`；`raised = 6`；`dispositioned = 1`；**未被提升且未被处置的 `[Gap]` 项 = 0**（满足 `unchecked + unraised + undispositioned = 0` 的可观测判据）。

非 `[Gap]` 的未勾选项（31 项）属质量问答题，不落入 H 的门禁范围；其中与本分片 findings 对应的映射：CHK006→W13-05、CHK007/CHK014→W13-08、CHK011→W13-09、CHK017→W13-16、CHK018→W13-02、CHK020/CHK021→W13-06、CHK023→W13-04。

## Evidenced Absences（本读域内已核对、无 findings 的覆盖断言）

- **FR 覆盖**：FR-001…FR-023 逐一核对，每项至少被一条 tasks.md 行引用（无零覆盖 FR）。
- **SC 覆盖**：SC-001…SC-007 均在 tasks.md §SC→row trace 有行与证据路径（SC-001 的失败线判据见 W13-03）。
- **green 归属算术**：19 条带 `[green:]` 的行共声明 58 次；按页核对 journal-engine 13/13、journal-format 13/13、observer-lifecycle 12/12、observer-role 10/10、observer-verification 10/10，各恰好一次，无重复声明。
- **包分区**：T001–T047 共 47 行；包分区 13 + 5 + 9 + 15 + 5(Setup) = 47，无 ID 双属。
- **封闭集声明抽查**：SC-006 的字段集 delta、GATE-1/2/8、T032 的载体边界均具备基线指涉（implement-entry base / test-evidence 冻结文件）与比较单元，属 `closed-set-claims.md` 的合法形态，不报。

## Notes

- 本文件是第三轮的单分片输入：前轮残留的 disposition / delta、C/H 独立校验与整轮合并由编排侧执行；本分片不含对 plan.md、contracts/、data-model.md、feature 注册表的判断。
- 只读边界自检：本执行未修改 requirements.md、checklist、tasks.md 或任何其他产物，唯一位移是写入本 findings 文件。
