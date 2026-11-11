# 债务审计 D3 — specs 075–099 + studies + archive

**审计日期**: 2026-11-11
**执行体**: SDD Debt Governor（只读审计 + 治理设计；未删除/移动/改写任何项目文件）
**范围**: `.specify/specs/` 编号 075–099（24 个 live spec 目录，092 已迁入 archive）、`.specify/studies/`、`.specify/archive/`
**唯一写入面**: 本文件
**并发读数**: requested=1 / effective=1 / effective_reason=`single-unit`（本域为一个可表示单元；五域并行由编排层承担，派发台账 `.specify/.tmp/sdd-loop/tmp/debt-audit-2026-11-11/manifest.txt`）

---

## 一、方法与口径

1. **分区**: specs 075–099 / studies / archive 三个互不重叠读域；机械读数先行，结论逐条附路径。
2. **关键口径**（本轮机械复现时确认）：
   - 体量的「MB」= `du` **磁盘占用 MiB**（基线的 64.7MB/12MB 按此口径精确复现）；同时给出 apparent size 便于回收估算。
   - 「旧锚」= 文本中 `.specify/memory/` 路径出现次数（基线 30,739 / 25,349 逐字复现）；另做**目标存在性解析**区分「历史引用」与「悬空引用」。
   - 「根裸件」= 位于各 spec 目录根、且不属于标准工件集的普通文件；按基线口径（把 `review-<slug>.md` 视为标准名）复现 69，按更严口径为 73。
3. **交叉复核**: 实跑 `bash scripts/bash/run-tests.sh tests/contract/test_spec_feature_binding_integrity.py -q`（只读，2 failed in 6.23s）；studies 的 target commit 到外部源仓实测解析。
4. **前提纠正**: 基线称「096 详情名 `096.md` 与 slug 不符」——所有者实际声明的是 `<ID>.md`（见 §四·D3-12），该条已改写。

---

## 二、基线逐条复核

| # | 基线项 | 状态 | 本轮实测 |
|---|--------|------|----------|
| 1 | 075–099 合计 64.7MB | 仍存在（口径确认） | 磁盘 64.66 MiB（67,805,184 B）；apparent 58.40 MiB / 61,236,964 B；24 目录 / 2,755 文件 |
| 2 | 096–099 新增 12MB | 仍存在 | 磁盘 12.03 MiB；apparent 11.10 MiB |
| 3 | 32 件 >200KB | 仍存在 | 32 件，合计 26.23 MiB；31 件在 `test-evidence/`，1 件在 `notes/`（098 `notes/pre-change-measurements.md` 966,830 B） |
| 4 | md5 非空重复 72 组/109 冗余 | 仍存在 | 72 组 / 109 个多余副本；**浪费仅 0.67 MiB**——是「件数问题」不是「空间问题」 |
| 5 | 空文件 29 | 仍存在 | 29：075 stall-evidence 夹具 16、088 flag 3、`.gitkeep` 2、失败运行空输出 8（078/081/087×3/090/094/095） |
| 6 | 根裸件 69 | 已变化（口径） | 各 spec 根文件 323；非标准 73；把 `review-<slug>.md` 计为标准名时 = 69 |
| 7 | 旧锚全区间 30,739（090 快照 25,349） | 仍存在（精确复现） | `.specify/memory/` 出现 30,739；其中 090 `history-*.json` 25,349；090 其余文件 1,051；其余 spec 4,339 |
| 8 | 无 test-evidence 保留政策 | 仍存在 | 保留事实 `memory-retention-thresholds.yaml:20` 的 stores 仅 4 个 memory 存储，不含 spec `test-evidence/`；`073` 详情：12 亦只覆盖三套记录 |
| 9 | 090 快照 16.2MB | 仍存在 | `test-evidence/history-*.json` 10 个，16.17 MB decimal / 15.42 MiB；090 test-evidence 合计 17.90 MiB |
| 10 | 097/098 无 features.md 行与详情 | 仍存在 | 两目录 live；`.specify/features.md` 无 097/098 行；`.specify/features/` 无对应详情 |
| 11 | 096 详情名与 slug 不符 | 已变化（前提纠正） | 所有者声明 `<ID>.md`（`skills/internal/manage-features/SKILL.md:29`、`shared/definitions/framework-map.md:9`）；`096.md` 是唯一符合所有者文本的文件，91/92 个 `<ID>-<slug>.md` 才是实践偏离——见 D3-12 |
| 12 | 075/080 同缺行 | 仍存在 | 两目录 live，均无行、无详情（Feature ID 分别绑 058/062，故 C-2 不报红） |
| 13 | 092 行在但已归档 | 仍存在（已加重） | 行 `.specify/features.md:99` 的 spec 路径 `.specify/specs/092-non-disposable/requirements.md` 悬空；行文仍称「artifacts remain under `.specify/specs/092-non-disposable/`」；详情 `092-non-disposable.md:6` 仍 `Status: Planned` |
| 14 | archive 两套命名（spec/ vs specs/） | 仍存在 | `archive/spec/` 8 目录 0.52 MiB；`archive/specs/` 11 目录 + `CONSOLIDATION-LEDGER.md` 2.55 MiB；framework-map 只登记前者 |
| 15 | spec/ 8 目录无台账 | 仍存在（有存档外记录） | `archive/spec/` 无本地台账；8 目录来源只记在 `.specify/memory/session/spec-audit-2026-08-15.md:14-25` |
| 16 | studies 1 项 target 可验证 | 仍存在（外部仓验证） | `target-commit.txt` = `8c32a9dc…`；本仓 `git cat-file` 不识别；在源仓 `/storage/project/cloud-native-ai/dsh-superagent-prototype` 实测 `commit` |
| 17 | 096–099 verification/review 齐备 | 仍存在 | 4/4 均有 `verification.md` + `review.md`；SC 状态行 7/9/11/9 |
| 18 | review 多世代 4–6 份/篇 | 仍存在（并扩散） | 096=6、097=4、098=6、099=4；另 081=8、084=8、095=4；093=4（notes/）、094=5（notes/）；089=0 |
| 19 | 096/099 无 checkpoints | 仍存在（并加重） | 096=0、099=0；097 仅 `03-plan.md`（1/8）；098 有 04–08 共 5 个；协议 owner 为 `skills/sdd-loop-driver/references/checkpoint-protocol.md` |
| 20 | 旧锚 129/437/261/522 | 仍存在（逐数复现） | 096=129、097=437、098=261、099=522（`.specify/memory/` 出现次数） |

---

## 三、债项表

> 处置词取自处置集 keep / archive / delete / regenerate / dedupe / normalize / consolidate；lane = SDD 修复 / `/speckit.sanitize` 回收 / 保持并立政策。

### P0 — 阻塞机制或静默风险

| ID | 状态 | 类别 | 证据路径 | 实测事实 | 处置 | lane |
|----|------|------|----------|----------|------|------|
| D3-01 | 仍存在 | 治理守卫红且盲 | `tests/contract/test_spec_feature_binding_integrity.py:49,69`；`.specify/features.md:99`；`specs/099-speckit-seal/baseline-failed.txt:119-120`；`specs/098-suite-speed-optimizations/baseline-failed.txt:122-123` | 实跑 2 failed/6.23s：C-1 项报 Feature 092（本域）与 Feature 048（D2 域）spec 路径悬空；C-2 报 086/088/089/090/098，但 4 行**存在**——守卫的严格行正则静默跳过 4/92 行（086 末列含裸 `\|`、090 同；088/089 行缺闭合 `\|`），既产生假红又使这 4 行的 C-1 检查失明。该红已被固化进 **8** 份 `baseline-failed.txt`，新破坏不再可见 | regenerate（守卫改为整行 schema 校验 + 含裸 `\|`/缺闭合即失败）+ normalize（修 4 行与 092/048 路径）；**禁止把红守卫无登记地写入基线** | SDD 修复 |

### P1 — 结构性

| ID | 状态 | 类别 | 证据路径 | 实测事实 | 处置 | lane |
|----|------|------|----------|----------|------|------|
| D3-02 | 仍存在 | 注册表可见性 | `.specify/specs/075-*`、`080-*`、`097-*`、`098-*`；`.specify/features.md`；`.specify/features/` | 4 个 live spec 无索引行、无详情；其 Feature ID 分别绑 058/062/024/086（进化切片），C-2 因父行存在而不报红——切片成为注册表盲区 | consolidate（补切片行，或在父特性详情登记切片并给指针，二选一） | SDD 修复 |
| D3-03 | 仍存在 | 092 生命周期漂移 | `.specify/features.md:99`；`.specify/features/092-non-disposable.md:6`；`.specify/archive/specs/092-non-disposable/`；`specs/090-re-anchoring/plan.md:298`；`specs/080-humanize-run-output/verification.md:21`；`specs/090-re-anchoring/tasks.md:314`（`.specify/specs/092-non-disposable` 共 22 处 live 引用） | 行仍指 live 路径（不存在），行文称工件仍在 live；详情 Status=Planned 而行 Status=Relocated；实际工件在 `archive/specs/092-non-disposable/`；080/090/094 的 canonical 工件仍引用旧 live 路径（094 review 已记 D-I1 残留） | normalize（行路径改指归档位置或 `-` + 台账指针；详情状态对齐；live 引用改归档路径） | SDD 修复 |
| D3-04 | 仍存在 | review 权威碎片化 | `specs/096-*/review*.md`（6）、`097-*`（4）、`098-*`（6）、`099-*`（4）、`081-*`（8）、`084-*`（8）、`095-*`（4）；`093-*/notes/review-*.md`（4）；`094-*/notes/review-*.md`（5）+ `verification.md:137-139`；`089-*`（0） | 全区间根级 review 族 **65 文件 / 2.58 MiB**；28 个是 loose 世代（dated/slug/round/slice）。094 已达 RfR 且 `review_records=` 指向 `notes/*`，但 `driver-stage-artifacts` 声明的 review 工件是 `review.md`；093 同形（notes-only）；089 无任何 review 工件（Status=Implemented，无 gate 声明，属豁免候选） | consolidate（采用 §四 单一权威政策；093/094 合并为 `review.md`；其余世代归档） | SDD 修复（政策+守卫测试）+ `/speckit.sanitize`（搬移） |
| D3-05 | 仍存在 | checkpoint 协议覆盖不全 | `skills/sdd-loop-driver/references/checkpoint-protocol.md:5`；`specs/096-*/`、`099-*/`（无 checkpoints）；`097-*/checkpoints/`（仅 03-plan）；`098-*/checkpoints/`（04–08） | 协议自 085 起存在；075–084 无（约定前）；085–095 每篇 5–13 个；**096=0、099=0、097=1/8、098=5/8**。缺失的 checkpoint 是历史协作证据，不能事后伪造 | normalize（closure 记录豁免原因；协议在 closure 时校验存在性或豁免字段） | SDD 修复 |
| D3-06 | 仍存在 | test-evidence 无保留政策 | `shared/declarations/facts/memory-retention-thresholds.yaml:20`；`shared/definitions/non-disposable-definitions.md:472`；`specs/090-*/test-evidence/`；32 件 >200KB | specs scope apparent 58.40 MiB 中 **44.21 MiB（75.7%）是 test-evidence**；090 单篇 17.90 MiB；31/32 个 >200KB 文件在 test-evidence；保留引擎的 store 闭集不含 spec 证据 | keep-with-policy（先定政策参数，再由 sanitize 回收——见裁定 Q4） | SDD 修复（政策）+ `/speckit.sanitize`（回收） |
| D3-07 | 仍存在 | 旧锚悬空（live 工件） | 240 个缺失目标；top：`.specify/memory/features.md`（101）、`constitution.md`（78）、`glossary.md`（35）、`migrate/receipts/`（18）；示例 `specs/082-*/requirements.md`（12）、`090-*/tasks.md`（11）、`089-*/plan.md`（10） | 全区间 3,037 次悬空引用 / 482 文件；按面积：test-evidence 2,186（历史日志）、canonical 工件 721、notes 130；**live canonical 工件子集 = 367 次 / 116 文件**。旧 `memory/` 布局（constitution/features/glossary/register）是主缺失目标。布局引擎实测 `anchor-layout-migrate.py --action check` → `{clean:true}`（布局已收敛；其 L4 明示文档内引用更新归项目自身，引擎不重写） | regenerate（只修 live 工件；历史证据与 dated review 中的引用保持原样） | SDD 修复 |
| D3-08 | 仍存在 | archive 根分裂且无主 | `shared/definitions/framework-map.md:17`；`.specify/archive/spec/`；`.specify/archive/specs/`；`skills/internal/sanitize-materials/SKILL.md`（archive lane owner，未命名任一 archive 路径） | framework-map 只声明 `archive/spec/`（8 目录、0.52 MiB、无本地台账）；`archive/specs/`（11 目录 + 台账、2.55 MiB）在 framework-map / skills / templates / src 中 **0 引用**——违反「无文档含义的目录不得创建」；两套命名同指一类对象 | consolidate（并根 + 台账随迁，或为 `specs/` 立第二个声明层——见裁定 Q5） | SDD 修复（framework-map/技能）+ `/speckit.sanitize`（搬移） |

### P2 — 计划性

| ID | 状态 | 类别 | 证据路径 | 实测事实 | 处置 | lane |
|----|------|------|----------|----------|------|------|
| D3-09 | 仍存在 | 根级残留与重复 | `specs/087-*/closure-*.txt`、`postmerge-*.txt`；`specs/088-*/final-failed-r*.txt`；`specs/081-*/tasks-081{a,b,c}.md`、`review-081*`、`code-review-081*`；`specs/095-*/observation-appendix.md` | 根文件 323；非标准 73（69 按基线口径）；其中失败/修复日志 41、loose review 世代 28、081 切片 tasks 3、附录 1；md5 重复 72 组 / 109 副本（0.67 MiB） | archive（日志入 `test-evidence/`，review 世代入 §四 归档面）+ dedupe（保留首份，后续副本改指针） | `/speckit.sanitize` |
| D3-10 | 已变化 | 075 旧身份残留 | `specs/075-sdd-loop-efficiency/verification.md:1`；`notes/red-first-evidence.md:1`；`notes/pre-change-measurements.md:1`；`notes/quickstart-run.md:1`；7 个 `test-evidence/*.jsonl` | 目录与 requirements 已是 075（绑定 Feature 058），但工件内仍有 5 处 `Feature 063` 与 19 处 `063-sdd-loop-efficiency`（含 E3 证据文件名）；读者/检索会落到不存在的 063 线 | normalize（live 工件改 075/058；历史 jsonl 保留但加注） | SDD 修复 |
| D3-11 | 仍存在 | 092 编号陷阱残留 | `specs/093-concurrency-by-default/tasks.md:235`；`notes/analyze-repair.md:42`；`notes/analyze-round2/v3-trunk-reconciliation.md:54-58` | features.md 已收敛为单 092 行，但 093 内的 `092-goal-team-parallel` 仍指不存在的目录；F-093-019 已登记「不重编号」决定，且前向注记已预言该句在重编号后会反转 | keep-with-policy（已登记的 dated 决定；若再动编号，按注记清单整批扫） | 保持并立政策 |
| D3-12 | 新增（前提纠正） | 详情命名漂移 | `skills/internal/manage-features/SKILL.md:29`；`shared/definitions/framework-map.md:9`；`skills/internal/sanitize-materials/SKILL.md:375-378`；`.specify/features/096.md`；其余 91 个 `<ID>-<slug>.md` | 两名 owner 文本互相冲突：manage-features / framework-map 声明 `<ID>.md`，sanitize 的 layout lane 声明 `<NNN>-<slug>.md`；实践 91/92 用 slug 形式；`096.md` 是唯一符合 manage-features 文本的文件，且行内链接可解析（无死链） | normalize（按裁定 Q6 统一一名 owner 的文本与实践） | SDD 修复 |
| D3-13 | 仍存在 | 090 快照体量 | `specs/090-re-anchoring/test-evidence/history-{w1..w5}-{before,after}*.json` | 10 个互异 JSON（md5 均不同）/ 15.42 MiB；单件 gzip 后 0.09 MiB（≈5.6%）；保留 w1-before + w5-after 明文、其余压缩，可回收 ≈11.4 MiB | archive（压缩/轮转；参数见裁定 Q4） | `/speckit.sanitize` |
| D3-14 | 仍存在 | 超大证据日志 | `specs/093-*/test-evidence/*suite*.txt`（7）、`095-*`（3）、`097-*`（3）、`099-*`（4）、`094-*/wp07-closure-suite.out`、`089-*/closure-*.json` 等 | 32 件 >200KB 合计 26.23 MiB；多为重复全量套件日志；单件 gzip 实测约 0.09 MiB（如 099 `final-suite-20261111.txt` 569,437 B → ≈0.09 MiB） | keep-with-policy（保留 final/被 SC 引用者明文；更早运行压缩） | `/speckit.sanitize` |
| D3-15 | 仍存在 | 空文件分类未治 | `specs/078-*/test-evidence/part4-current-failed.txt`；`081-*/closure-verdict.err`；`087-*/closure-fixed.txt`、`closure-new-failures.txt`、`postmerge-fixed.txt`；`090-*/test-evidence/tmp/tasks-base-failed.txt`；`094-*/repairwave-T079-dryrun.err`；`095-*/review-r2-closure-acceptance.err` | 29 个空文件：21 个应保留（075 夹具 16、088 flag 3、`.gitkeep` 2），8 个是失败运行的空输出（不承载任何断言） | delete（8 个空输出）/ keep（其余） | `/speckit.sanitize` |
| D3-16 | 仍存在 | 归档内旧路径 | `.specify/archive/spec/**`（123 处 `.specify/specs/`）；`.specify/archive/specs/**`（529 处） | 例如 `archive/spec/002-mcp-tool-call/plan.md:5-6` 仍指 `.specify/specs/002-…`；archive/specs 的 092/069a/069b 同形 | keep-with-policy（归档是历史记录，不重写；需要可解析处由台账/摘要承担） | 保持并立政策 |
| D3-17 | 新增 | studies 外部目标依赖 | `.specify/studies/dsh-superagent-prototype-study/target-commit.txt`；`strip-manifest.md:7-12` | 唯一 study 结构合规（`<target>-study/`：overview/outlines/strip-manifest/figures/self-check/target）；target commit 在本仓不可解析，只在外部源仓可验证；manifest 已记录源仓路径与 hash | keep-with-policy（保留；若源仓不可得，按 manifest 明示 unverified，不得升级为事实） | 保持并立政策 |

---

## 四、「唯一权威 review 文件」政策建议

**现状依据**（均为既有 owner，政策不另造事实源）：
- `shared/declarations/facts/driver-stage-artifacts.yaml:64`：review 阶段的产物 = `review.md`。
- `templates/feature-details-template.md:104`：门禁读的是**当前** `code-review.md`；dated `code-review-<ts>.md` 是历史，**never counted**。
- `templates/feature-details-template.md:111`：review 转换在 process + code 两段都完成后判定一次。
- 现状数据：根级 review 族 65 文件 / 2.58 MiB，其中 28 个是非当前世代；093/094 的评审只存在于 `notes/`；089 无评审。

**建议政策（每段唯一当前记录，不合并两段为一文）**：

1. **根级只保留两份当前记录**：`review.md`（process 段 + 最终汇总裁决）与 `code-review.md`（code 段当前记录）。review gate、`verification.md` 的 `review_records=`、feature 详情只读这两个路径。
2. **其余世代一律归档**：`review-<timestamp>.md`、`review-<slug>.md`、`review-rN.md`、`review-<slice>.md`、`code-review-<timestamp>.md` 移入 `<spec>/review-archive/`（单目录），并在首行标注 `Superseded-by: review.md` 或 `Superseded-by: code-review.md`。dated code-review 的归档属性是既有规则的自然延伸，此次把它扩到 review 族。
3. **placement 归一**：评审不得只存在于 `notes/`；093/094 将 `notes/review-*.md` 的结论合并为根级 `review.md`，原件入 `review-archive/`。094 的 `verification.md` `review_records=` 改为两个当前路径。
4. **豁免显式化**：未进入 review gate 的 spec（如 089，Status=Implemented）在 `verification.md` 写明确的 `review_exemption=` 理由，而不是留空。
5. **守卫**：新增契约测试（owner：review 模板 + review 技能），断言 (a) 每个 RfR/sealed spec 根存在且仅存在一个 `review.md`（及需要时的 `code-review.md`）；(b) 根级不存在 dated/slug/round 评审文件；(c) `verification.md` 的 `review_records` ⊆ 上述两个路径。红即阻止 RfR。

**可测收益**：根级 review 族 65 → ≈39（21 `review.md` + 16 `code-review.md` + 093/094 两个新 `review.md`），28 个世代移入归档；根目录「同模板多代并存」消失，评审可检索性由 `review-archive/` 承担。

---

## 五、治理计划（三波，机制先行）

### Wave 1 — 机制修复（SDD 修复 lane；需确认门：`/speckit.plan`→`/speckit.review` 正常 SDD 门）
- 修 `test_spec_feature_binding_integrity.py` 行解析（裸 `|`/缺闭合即失败，禁止静默跳过）；修 features.md 086/088/089/090 四行；修 092/048 的 spec 路径（092 本域，048 移交 D2）。建立「红守卫写入基线必须带登记行」的规则（owner：测试基线实践文档）。
- 落 §四 政策 + 守卫测试；落 checkpoint closure 校验/豁免字段；落 test-evidence 保留政策参数（与 Q4 一起裁）。
- 处置注册表：075/080/097/098 的注册模型（Q2）；096.md 命名（Q6）；092 详情状态与行文（Q1）。
- **验收读数**：binding 两测试绿；0 个不可解析行；RfR spec 0 个缺 `review.md`；政策 owner 文件落盘。
- **中止条件**：任一行的 Feature 映射无法判定，或所有权文件修改与既有 owner 冲突 → 停在该点并上报。

### Wave 2 — 数据回收（`/speckit.sanitize` lane；需确认门：sanitize 干跑计划 + 用户对裁定点的授权）
- 090 快照压缩/轮转（15.42 → ≈4 MiB 保留面）；>200KB 日志压缩（26.23 MiB 的大部分）；109 个重复副本去重；8 个空输出删除；41 个根级失败日志与 28 个 loose review 世代归档；archive 并根（若 Q5 选 A）。
- **验收读数**：scope apparent 58.40 → **≤35 MiB**；文件 2,755 → ≤2,550；090 test-evidence 17.90 → ≤4 MiB；根级 review 族 65 → ≤40。
- **中止条件**：某文件是任一 SC 行验证的唯一证据且无副本/无指针 → 停止并列入待裁清单。

### Wave 3 — 结构收敛（SDD 修复 lane；需确认门：review 段验收）
- 093/094 评审合并为 `review.md`；089 豁免或补评审；096/099 checkpoint 豁免记录；075 旧身份清洗；096.md 重命名（按 Q6）；根裸件布局归一。
- **验收读数**：0 个无文档目录；0 个不可解析行；0 个 RfR spec 缺当前 `review.md`；live canonical 工件 0 悬空 `.specify/memory/*`；双套 archive 根按裁决收敛。
- **中止条件**：任何 features.md 状态回退风险，或需改写 dated 台账（历史记录） → 停止。

---

## 六、裁定点（封闭问题，未自答）

- **Q1 092（及 048）行路径怎么修？** (A) spec 路径改指 `archive/specs/…`（推荐；保留可解析） / (B) 置 `-` 并在行内指向台账。
- **Q2 075/080/097/098 的切片如何入册？** (A) 各补一行并挂父特性（推荐；live spec 可见） / (B) 只写父特性详情 + 指针。
- **Q3 review 政策是否采用 §四？** (A) 采用两文件根模型 + `review-archive/`（推荐） / (B) 保留根级但加 `Superseded-by` 头。
- **Q4 证据保留参数？** (A) 最新 baseline+final 明文、更早运行压缩，30 天宽限（推荐） / (B) 每 spec 明文上限（建议 5 MiB） + 压缩 / (C) 只压缩不设上限。
- **Q5 archive 根收敛？** (A) 并入 `archive/spec/`，台账随迁（推荐；framework-map 已有该 owner） / (B) 在 framework-map 声明 `archive/specs/` 为第二层（consolidation lane）。
- **Q6 详情命名以哪边为准？** (A) 以实践为准改 owner 文本为 `<ID>-<slug>.md` 并重命名 `096.md`（推荐） / (B) 以 owner 文本为准，把 91 个文件改为 `<ID>.md`。
- **Q7 是否授权 Wave 2 的删除/搬移？** (A) 全部授权（含 8 个空输出 + 109 个重复副本，干跑先行） / (B) 仅压缩与搬移，不删除 / (C) 不授权。

---

## 七、已核查健康项（不列债）

- 24/24 spec 均有 `requirements.md` / `plan.md` / `tasks.md` / `verification.md`；096–099 的 `verification.md` 与 `review.md` 齐备。
- `.specify/features.md` 行数 92 = 头部 `Total Features`；092 重复编号已在索引层收敛（仅 093 内保留已登记残句）。
- `archive/specs/CONSOLIDATION-LEDGER.md` 覆盖全部 11 个目录（10 主表 + 054 追加行），085 的 deferred 状态明确。
- `archive/goal-team/`（0.24 MiB）receipts + trees 与 framework-map 声明一致。
- studies 唯一项结构合规、provenance 完整；target 在外部源仓实测可解析。
- 无断裂符号链接；specs/studies/archive 内无空目录（唯一空目录是本报告的输出目录，属进行中产物）。

---

ANOMALY: none — 未发现越出既有债项清单的执行异常；唯一前提反转是基线 #11 的「096 详情名不符」，已按所有者文本纠正为「所有者文本与实践相反」。
DEBT-DONE
