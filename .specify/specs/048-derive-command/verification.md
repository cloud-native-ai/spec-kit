# Verification Log — 048-derive-command

**Related Feature**: 049 Derivation Command

# -- Baseline (frozen BEFORE any implementation work changed the tree) --

baseline_branch=048-derive-command
baseline_date=2026-09-05
baseline_failed_names=50(`baseline-failed.txt`,冻结于 T001;全套件 50 failed / 2229 passed / 2 skipped,122.44s)
baseline_note=047 的 47 条清单**不可**复用——本分支自冻。差集显示既有失败集本身在漂移(047 的 3 条已消失、5 条新增,归因并行会话),这正是名字级而非数量级比较的理由
baseline_gate_total=23(cap = 93 × 0.25 = 23.25,**零余量**)
baseline_probe_internal=72(`--action probes --validate` exit 0)
baseline_probe_reconcile=exit 2,错误恰为 `skill:git-fleet` + `skill:git-server-init`(既有,与本特性无关)
baseline_complex_commands=18(feedback 分类)/ 15(docs-step 分类)

# -- Per-SC verification --

SC-001_status=pass
SC-001_value=handed-in 清单缺陷检出率 100%,静默丢弃数 0
SC-001_note=dogfood 真实运行(T038,`.specify/derive/rest-architecture/derive.md`)。六条来源逐一联网核实:**1 条落地**(kegel.com/c10k.html,HTTP 200,正文实读,grade=primary);**2 条死链且无存档快照**(tomayko.com/writings/rest-in-plain-text HTTP 404;w3.org/2001/tag/doc/REST.html HTTP 404 —— 二者经 archive availability API 查询均返回无快照);**3 条源站阻塞**(两条 roy.gbiv.com 与 amundsen.com 均 HTTP 403)。五条未落地来源**全部**记入 `## Unverifiable Sources` 并各附理由,静默丢弃数 = 0。清单自己披露的死链(S-003)被确认;**清单未披露的死链(S-005)被检出**——它把该链接作为「权威规范依据」推荐并给了高优先级。清单自述的社区改标题条目(S-001)因源站 403 无法确立原标题,故 `title_mismatch` 计算为 `false` 并出 `unresolved-title` warning,怀疑本身以散文留痕而**不**被编码成本次运行无法支撑的计算事实——这正是「无证据不等于有证据」判据(derivation-model C-28)的正确行为。引擎 `stats` 分组计数:byGrade={primary:1, unverified:5},byAccess={live:1, dead:2, unknown:3},titleMismatch=0。

SC-002_status=pass
SC-002_value=锚定违规 0、不可溯源元素 0、前向引用与环 0
SC-002_note=dogfood 产物 `validate` **exit 0**,`errors[]` 长度 0,`audit.engine` 的 A1–A10 与 A12/A13 **全部 pass**,`audit.semantic`={A11: attested, A14: attested},`semanticChecksPending`=["A11","A14"]。`payload.steps.anchorable`=1(唯一步骤锚定 primary 来源 S-004);两条 community/unverified 候选(S-001、S-005)只出现在该步骤的 `leads` 字段,**未**进入 `premises`——`premise-grade-ineligible` 命中数 0。`payload.elements.untraceable`=0(A-1 的 `derived-from: D-1` 完整解析)。`byGrade`/`byAccess`/`byConfidence` 键集恒为完整枚举(缺项计 0),故本 SC 可直接断言而无需先探形状。**缺陷注入侧(对契约化后的引擎重跑)**:端到端驱动 102 项检查全绿,其中 **41 类违例**逐一断言 exit 4 且命中预期 error code——C1×6(孤儿来源前提 / community 等级 / unverified 等级 / 前向引用 / 自引用 / 未解析 lead)、C2×2(算子数 0 与 2)、C3×3(英文与中文字面量、以及 `industry best practices` 只报最长命中不重复记账)、C4×2(空洞证伪 / 证伪复述结论)、C5×5(contested 无对向 / 非互指 / derived 建立在 contested 上 / 步骤置信度超前提最小秩 / 枚举外值)、C6×4(条件缺失 / 声明预算分歧 / 声明步数分歧 / 超预算)、C7×2(退化 derivation / 结论等于来源标题)、A1×5(枚举外等级 / unknown access 却给已核实等级 / 长度不足 / 裸断言 / agent 断言的 title_mismatch 与重算矛盾)、A2×1(unverified 未记录)、A3×1(改标题来源未按 resolved_title 引用)、A7×2(缺 derived-from / 不可解析)、A8×1(元素置信度不等于最小值)、A9×1(算子不在库)、A10×3(Q→A 非互指 / 被阻塞元素仍称 derived / 未决问题缺 discriminator)、A0×2(自审表形破损 / 自审值与派生值分歧)、降级×1(全 unverified 却带步骤)。该驱动另覆盖信封键集、init no-clobber 与 `--force` 留 `.bak`、`--slug`/`--file` 互斥、`--max-steps 0` 拒绝、warning 集封闭性、`probe-links` 离线容错。**驱动本身暴露了两个引擎缺陷并已修复**:① `verification-bare-attestation` 原为**不可达死码**(见 mechanism notes);② `byAccess` 把参数化形态 `wayback:<ts>` 当成独立键,导致键集不是完整枚举。

SC-003_status=pass
SC-003_value=重复 move_id 0、重复归一化 inference_form 0、第二次运行复用计数 > 0
SC-003_note=**证据分两层,如实区分。** ①**真实运行层(dogfood)**:`.specify/derive/rest-architecture/` 上 `moves-add` 发放 `M-001`(`intent:new`,限定锚点 `rest-architecture.S-004`),产物的 `## Reasoning Moves Applied` 携带处置日志表 `| M-001 | new |`,`stats --slug rest-architecture` 读出 `dispositions={new:1, reused:0, reinforced:0}`、`moves={total:1, byStatus:{active:1,superseded:0}, duplicateIds:0, duplicateForms:0}`、`archives={total:1, topics:[rest-architecture]}`、`lastRun` 非空 —— **SC-003 的量测点在真实档案上是活的**。②**跨运行复用层(夹具)**:「同主题第二次运行 `reused`+`reinforced` > 0」由 `tests/integration/test_derive_us2.py` 以两次顺序运行证明,dogfood 只跑了一次真实运行,故该子项**不**由真实数据支撑。去重与发放语义在活引擎上逐条实测:`intent:new` 发放 `M-001`(appended=1,issued=["M-001"]);同一推理形状换槽位字母(`P`/`D` → `X`/`Y`)再提交 → **槽位同构去重命中**,appended=0、deduped=1、`duplicates[]` 返回 `existingMoveId: M-001`、disposition=`reinforced`(带新锚点),退出码 **0**(拒绝是成功路径);`intent:reuse` → 零写入、disposition=`reused`;`intent:reinforce` 无新锚点 → exit 2 `reinforce-without-new-anchor`;`intent:supersede` → 持久 `status` 迁 `active → superseded`、superseded=1,再次 supersede → exit 2 `illegal-status-transition`(终态)。锚点按「既有 ∪ 新增」排序写回为 `demo.S-004, demo.S-005`(只增不减);库行 `status` 列**始终**为持久二值,`new`/`reused`/`reinforced` 只出现在 payload 的 `dispositions[]`。发放单调性:下一个 ID = 现存最大编号 + 1(非行数 + 1);库单调性被破坏时 `moves-add` 拒绝发放并 exit 2(`moves-library-hand-edited`),MUST NOT 通过重编号让追加「成功」。**实现期修正**:处置日志表原先**未被命令模板要求**,SC-003 的量测点因此在真实运行中根本不会产生——已在模板 Stage 4 补入该表的要求,并说明两列日志不是库行复写(故不需要投影标记),这条区分正是处置日志与投影规则能够共存的原因。

SC-004_status=pass
SC-004_value=禁用论证字面量命中数 0;注入任一字面量 → exit 4 且定位 C3
SC-004_note=引擎 `BANNED_JUSTIFICATIONS` 15 条字面量逐条参数化注入 `derivation`/`conclusion`,各自断言 exit 4 且 `errors[].code == banned-justification`、`rule == C3`、`value` 携带命中字面量。匹配为子串匹配(非词边界),故 `industry best practices` 同时含 `best practice` 与 `best practices`,引擎**只报最长命中**以免同一片段重复记账(derivation-model C-3/C-17)。扫描范围恰为 `derivation` 与 `conclusion` 两字段,不扫 `prevents`/`applies_when`/`falsification`/`A-<k>.statement`——算子的 `prevents` 合法地引用禁用短语来命名它挡住的失败模式。**三方漂移守卫已实测相等**:概念锚 §Banned Justifications 字面量行(按 ` · ` 分隔)= 引擎常量 = requirements.md 的 STR-001 *Value (verbatim)* 单元格,三处均 15 条、集合相等。该相等并非天然成立:STR-001 的值单元格原先携带中文标签前缀 `封闭禁用论证字面量集:`,导致首元素解析为「标签+字面量」而不等于 `best practice`;实现期已把标签移入 *Consumed by* 列、值列保持逐字,守卫才成立。

SC-005_status=pass
SC-005_value=可锚定步骤 0、unverified 来源数 = 全部来源数、建链前停止、无架构产出
SC-005_note=两条独立证据。**①真实环境证据(非夹具)**:本仓运行环境的 `ALL_PROXY`/`HTTPS_PROXY`/`HTTP_PROXY` 均为 `socks5://127.0.0.1:13659`,而 stdlib `urllib` 无 SOCKS 支持(本项目 runtime 正因此依赖 `httpx[socks]`),故 `probe-links` 对六条 URL **全部**失败。引擎行为完全符合离线容错契约:每条结果 `access: unknown`、动作整体 **exit 0**、不崩溃、不抛栈、**且绝不把探测失败伪造成 `dead`**;`payload.online=false`、`payload.degraded=true`、`notes[]` 携带以 `no-online-capability` 开头的降级说明,并额外给出指名环境变量的 `proxyWarning`。**②产物级证据**:降级判据(derivation-model C-45:来源非空且全为 `unverified`、每行 `verification` 归一化后等于 `no-online-capability`、链无任何 `D-` 步骤、架构节为空)满足时 `validate` **exit 0** 且 `payload.degraded=true` 并出 `degraded-run` warning——诚实的空产物不是失败,判成 error 会诱导 agent 编造核实来「变绿」;而在同样的全 `unverified` 来源下**携带任何步骤**的产物被拒(C-47:降级契约不得成为绕过锚定规则的后门)。本次 dogfood 因 S-004 落地成功而未走全降级路径,故降级路径由夹具覆盖、探测降级由真实环境覆盖,二者互补。

SC-006_status=pass
SC-006_value=命令面接线完备且零回流
SC-006_note=逐项实测:**四份工具副本**均存在(`.claude/commands/speckit.derive.md`、`.github/prompts/speckit.derive.prompt.md`、`.qoder/commands/speckit.derive.md`、`.opencode/command/speckit.derive.md`),各携带指向 `templates/commands/derive.md` 的 `AUTO-GENERATED` 标记;Qoder 副本额外带 `description:` frontmatter 且逐字等于模板的 `short-description`(25 字符 ≤ 50);`regen-command-copies.py --check` 输出 OK 零 stale。**probe 注册表**:`speckit-derive-wrapup` 插入 Objects 表 clarify 与 docs 之间(`d-e-r` < `d-o-c`),internal 计数 **72 → 73**,`--validate` exit 0;`--reconcile` exit 2 且错误集**恰为**既有的 `{skill:git-fleet, skill:git-server-init}`,`/speckit.derive` **不**在其中(模板与 probe 行同批落地,双向对账未扩大);`--action map` 重建 `probe-map.md` 为 73 objects。**门控零回流**:`scan-confirmation-gates.py --root . --json` 的 `total` 仍为 **23**(= 基线,cap 23.25),`violations` 为空;`templates/commands/derive.md`、`shared/definitions/derivation-definitions.md`、`shared/definitions/framework-map.md` 三处新增/修改文件的 `BLOCKING_RE` 命中数均为 **0**(守卫测试直接 import 扫描器的 `BLOCKING_RE` 断言,属「钉死漂移」意义上的合法副本)。**分类计数**:复杂命令 18 → **19**、docs-step 15 → **16**,两处 `SIMPLE_COMMANDS` 副本未动(derive 是复杂命令)。**客户中性**:`templates/` 与 `shared/` 内 `Feature 0NN` / `requirement 0NN` / `.specify/specs/0NN-` / `.specify/memory/features/0NN` 命中均为 0,且无真实语料 URL 或标题(示例全部槽位化)。**镜像义务**:`sync-mirrors.py --check` exit 0;概念锚、probe-definitions、framework-map、引擎(严格对)四处 `diff -q` 均一致;`.specify/derive/` 未进 `MIRROR_PAIRS`(引擎源码中 `derive` 于 `sync-mirrors.py` 出现 0 次)且 git **跟踪**(`git check-ignore` 对 `moves.md` 与 `<slug>/derive.md` 均返回非 0),与 `.gitignore:70` 忽略 `.specify/memory/sanitize/` 形成判据对照。**登记面**:framework-map 新增 `.specify/derive/` 行(3 列,合规);glossary 新增 4 行(Derivation / Reasoning Move / Provenance Grade / Derivation Chain),各 5 列、`Origin=auto`、`Status=confirmed`、均指向真源;Tool 记录 `.specify/memory/tools/derive-utils.py.md` 已建(`Status: Draft`)。**全套件名字级回归**:见下 GATE-1。

# -- Completion gates --

GATE-1_status=pass
GATE-1_note=全套件 **47 failed / 2466 passed / 2 skipped**(130.51s)。`comm -13 baseline-failed.txt /tmp/048-final.txt` **为空** —— 名字级零新增失败。较 50 条基线**净减 3 条**:`test_browser_site_exclusions::test_mirror_check_ignores_site_probe`、`test_no_organize_agents_refs::test_skills_mirror_parity`、`test_scripts_distribution_parity::test_repo_has_no_orphan_or_drifted_scripts` —— 三者均因本特性多次运行 `sync-mirrors.py --write` 顺带收敛了既有的陈旧镜像(git-fleet 技能镜像缺失、脚本分发漂移)而转绿,属**附带修复**,非本特性目标。新增通过数 = 232(八个 derive 测试文件全绿,0 xfail),与 mid-run 的 2234 passed 相比恰为 +232,证明新测试全部被收集且全部通过。基线文件**未被修改**。

GATE-2_status=pass
GATE-2_note=镜像义务逐行核验:`diff -q scripts/python/derive-utils.py .specify/scripts/python/derive-utils.py` 一致;`diff -q shared/definitions/derivation-definitions.md .specify/shared/definitions/derivation-definitions.md` 一致;`shared/definitions/probe-definitions.md` 与 `shared/definitions/framework-map.md` 镜像一致;`sync-mirrors.py --check` exit 0;`regen-command-copies.py --check` 输出 OK。

GATE-3_status=pass
GATE-3_note=无未决任务行:`tasks.md` 关闭 48 行、延后 4 行、未决 **0** 行。四条延后项各自附明原因:T019–T021 为 **RED→GREEN 次序倒置**(交付物均已落地且全绿,延后的是次序不是产物),T032 为 `docs/tutorials/quickstart.md` 命令表加行(非契约要求,且该表已缺 session/sanitize/feedback 三行,单独补一行会造成更不一致的部分覆盖,留待统一收敛)。

GATE-4_status=pass
GATE-4_note=verification.md 覆盖全部 SC:SC-001..SC-006 逐条有 `_status` 与 `_note` 行(本文件)。

GATE-5_status=pass
GATE-5_note=门控治理无回流:扫描器 `total` = 23(等于基线,未增)、`violations` = 空。

GATE-6_status=pass
GATE-6_note=命令副本零 stale:四份 `speckit.derive` 副本存在、均带 AUTO-GENERATED 标记、`--check` 输出 OK。

GATE-7_status=pass
GATE-7_note=probe 对账不扩大:`--validate` exit 0 且 internal = 73;`--reconcile` 错误集恰为既有两条,不含 `/speckit.derive`。

# -- Mechanism notes(实现期学到的、下次会再踩的) --

- **`update-feature-index.sh` 是破坏性脚本**:第 150 行 `cat > "$FEATURE_INDEX"` 整体重写;输出 **6 列**(缺 `Spec Path`)而现存 49 行均为 7 列;`count_features()` 数的是 spec 目录(38)而非特性行(49);Name/Description 由目录 slug 与桩文本覆盖;Status 全部重置——而 `test_c3` 仍然通过(38==38),**损坏是静默的**。本特性的索引行与表头计数一律手工编辑。该脚本未在本特性内修复(属范围蔓延),记为交由 `/speckit.sanitize` 或后续守卫测试处理的观察项。
- **两个 ID 命名空间独立**:Feature ID = 049,requirement key / spec 目录 = 048,偏移恒为 −2(047→045、048→046 同构)。混用会让 `features.md` 的 Spec Path 列指向不存在的目录。
- **节序决定合规类别**:`templates/commands/sanitize.md` 把 `## Documentation` 放在 `## Feedback` **之前**,因此无法满足 `test_docs_step_injection.py`(要求 Feedback 在前且相邻),这正是该清单 15 而 feedback 清单 18 的差额来源。`derive.md` 采用 `research.md` 的序,同时进入两个清单。
- **十二个保留标题是子串级扫描**:`shared/**` 与 `templates/**` 内出现 `Resolving a disagreement` 或 `判定边界` 等即失败,与是否为标题无关。故用 `## Contradiction Handling` 与 `## Script / Prompt Boundary`。
- **端到端跑通是不可省略的一步**:引擎首轮实现后立刻以真实管线驱动(init → moves-add → validate),第一发就暴露 `init` 完全不可用——`artifact_skeleton` 用 `str.format()` 而模板里含未提供的 `{budget}` 占位符,抛 KeyError。「文件存在 / 标题齐备」式检查永远发现不了它。改用 `@@TOKEN@@` 替换后不再受花括号碰撞影响。
- **真实环境比夹具更会揭短**:dogfood 一跑就暴露 `probe-links` 在 SOCKS 代理环境下全量失效(而这是本项目的常态环境,不是边缘情形),以及 handed-in 清单自己未披露的死链。二者都不是夹具能预设的。
- **检查次序能让一个 error code 变成死码**:契约 C-31 原先规定 `verification` 的两道硬检为「① 码点数 < 16 → `verification-too-short`;② 归一化后整串 ∈ `BARE_ATTESTATIONS` → `verification-bare-attestation`」。但 `BARE_ATTESTATIONS` 的**每个**成员(`verified`、`已核实`、`无`、`-` …)都不足 16 码点,故 ① 恒先命中、② 永不可达——一个不可达的 error code 等于没有该检查,而它恰恰是信息量更大、更能告诉运行者「你写的是断言不是证据」的那一个。已改为**先判裸断言再判长度下限**,两道硬检遂各自可达,契约 C-31 同步修订并写明理由。教训:凡「多道硬检按序短路」的设计,都要检查后面的检是否被前面的检恒先拦截。
- **分组计数会悄悄破坏「完整枚举」承诺**:契约 C-19 要求 `byAccess` 的键集恒为完整枚举(缺项计 0),这样 SC-001/SC-002 才能直接断言而不必先探形状。但 `access` 有一个**参数化**成员 `wayback:<snapshot-ts>`,直接按原值 tally 会把每个快照时间戳变成一个独立键,枚举承诺当场失效。已引入 `ACCESS_BUCKETS` 与 `access_bucket()`,把 `wayback:*` 归并为 `wayback`。教训:枚举里只要有一个带参数的成员,所有按该字段分组的输出都要显式定义归并规则。
- **命令发现面是四处独立陈旧的,补一行会让覆盖更不一致**:`docs/tutorials/quickstart.md`(缺 4)、`docs/tutorials/installation.md`(缺 6)、`templates/vscode-settings.json` 的 `chat.promptFilesRecommendations`(13/25)、`src/specify_cli/__init__.py` init 后的 `Optional:` 控制台行(10/25)——四处各自漏掉不同批次的历史命令。只把 derive 加进其中一处,会让「哪处该有哪条」更无规律可循,故按全量收敛处理,收敛后四处缺失均为 0(以 25 个模板为基准)。顺带发现两处**不属于本特性**的既有问题,如实记录不顺手修:① `.vscode/settings.json` 是本仓未跟踪的本地安装产物且已与模板漂移,应由 `specify init` 再生成而非手工对齐;② quickstart.md 的 Prerequisites & Next Steps 表对更早命令仍缺多行,属文档空间 reconcile,移交 `/speckit.docs`。另:`tests/contract/test_docs_command_template.py::test_c10` 的既有失败源于 `tmp/e2e-toml/` 与 `tmp/e2e-md/` 两个残留 e2e 工作区(含 `speckit.history.*` 而缺 `speckit.docs.*`),与本特性无关,已在冻结基线内。
- **两条各自合理的规则可以联立不可满足**:C-38 要求元素 confidence **等于**其步骤置信度的最小秩,C-25 要求被未决问题阻塞的元素为 `provisional` / `contested`。若某元素的步骤全为 `derived` 而它又被未决问题阻塞,二者无解。这个矛盾**只有在动手构造一个合法 fixture 时才暴露**——两份契约分别读都无懈可击。裁定:不给任一条开例外,而是认定「未决问题真的落在某元素上 ⇒ 支撑它的链尚不完整 ⇒ 该问题所依附的步骤本身 MUST 为 `provisional`」,元素经最小值传播自然继承,两条规则同时成立;裁定已写入 C-25。若改为给 C-38 开例外,`provisional` 就会退化成可随手标注的装饰,而那正是 C-38 取「等于」而非「至多」所要防的。
