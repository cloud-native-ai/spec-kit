# Prompt Adherence Definitions(提示遵从度评价定义·真源)

> **Single source of truth(单一真源)**: 本文件是提示遵从度评价(Prompt Adherence Evaluation)的唯一 owner(所有者),框架源在 `shared/definitions/prompt-adherence-definitions.md`,安装为 `.specify/shared/definitions/prompt-adherence-definitions.md`。它拥有受评价的前提链、双层模型、信号目录(行与准入判据)、读取契约字段含义、盲区登记与本特性红线;任何其他承载这些事实的表面 MUST 指向本文件,MUST NOT 复述其表格或枚举。分工(FR-019):本文件拥有**含义**;五个声明事实 `shared/declarations/facts/prompt-adherence-*.yaml` 拥有**值域**,经 `scripts/python/declaration_reader.py` 读取;引擎 `scripts/python/prompt-adherence.py` 拥有 **schema 与行为**;框架地图与任何技能/命令面只携带指针。

## Owner Declaration(所有者声明)

本文件自声明拥有以下六个面,每个面的表格或枚举只在本文件出现一次:

1. **受评价的前提链与假定行为覆盖图** — § Premise Chain & Coverage Map(前提链与覆盖图);
2. **双层模型** — § Two-Layer Model(双层模型);
3. **信号目录、逐行归因与准入判据** — § Signal Catalog(信号目录);
4. **读取契约的字段含义** — § Reading Contract(读取契约);
5. **盲区登记** — § Blind-Spot Register(盲区登记);
6. **本特性红线** — § Red Lines(红线)。

目录、盲区与覆盖图以本文件内的固定表头声明;引擎解析这些表并逐格对照声明集,任何未知令牌是硬错误(退出 2,无读取)。封闭集的变更 MUST 是一次本文件修订加既有镜像再生成,绝不是第二个编辑位置。

## Two-Layer Model(双层模型)

宿主提示层(Host Prompt Layer,令牌 `host-prompt`)是运行期拥有的提示面——宿主系统提示加用户直接提示——不由本框架编写;它的原始文本从不被读取(隐私红线见 § Blind-Spot Register 的 `host-prompt-content` 条目)。

项目规则文件层(Project Rule File Layer,令牌 `project-rules`)是本框架发布的指令面:`.specify/instructions.md` 及其兼容符号链接(`AGENTS.md`、`CLAUDE.md`、`QODER.md`、`.github/copilot-instructions.md`);该指令面的事实 owner 仍是 `.specify/shared/workflow/symlink-model.md`,本文件按路径抵达,MUST NOT 另立第二份定义。

宿主与项目 harness 的既有辨析按路径抵达 `shared/guidelines/better-harness.md` 的术语消歧段;层令牌的值域由 `shared/declarations/facts/prompt-adherence-layers.yaml` 拥有,核心概念行带双语形态(owner: `shared/guidelines/bilingual-expression.md`)。

## Signal Catalog(信号目录)

### Admission Criteria(准入判据)

一个信号类只有同时满足以下五条时才进入目录:(a) 既有机制在既有生命周期点产出它并持久化在既有存储中;(b) 携带机器可读的源标识;(c) 其含义可由封闭词表或声明推导判定;(d) 声明其层归属与强度(值域分别为 `shared/declarations/facts/prompt-adherence-layers.yaml` 与 `shared/declarations/facts/prompt-adherence-strengths.yaml`);(e) 能在证据纪律下诚实表达「不可观察」。不满足 (a) 的信号列入 § Blind-Spot Register(盲区登记);本特性 MUST NOT 通过新采集点合成它。

目录的增删 MUST 是一次 owner 修订(含义、目录行与本文件覆盖图中的 `AB-NN` 映射)加 `shared/declarations/facts/prompt-adherence-signals.yaml` 成员的同一次变更:MUST NOT 存在第二张映射表或注册表;仅当被增行的读取面本身变化时才改引擎,否则经既有所有者引擎读取;退役行的既有日期化记录继续作为日期化记录按自身引用可重放,当前读取遵循新声明集并盖其摘要。

### Rows(目录行)

本表是信号目录的唯一声明处:行 id 的值域见 `shared/declarations/facts/prompt-adherence-signals.yaml`,以下逐行归因按声明报告、绝不于读时重新指派(FR-009)。`store` 的值是 `shared/declarations/facts/runtime-store-layout.yaml#/statement` 声明的 store 名(根为其 `.specify/<store-name>/` 投影),probe 行读注册表而非 store(`registry`)。`allowed_states` 是正状上限;缺席态(`Unobserved`、`not_evaluated`)对每一行普遍可用。`—` 表示该行不声明该项。

| row_id | record_predicate | store | read_surface | identity_fields | timestamp_field | layer | strength | allowed_states | deviation_classes |
|--------|------------------|-------|--------------|-----------------|-----------------|-------|----------|----------------|-------------------|
| run-determination-record | `.specify/session/` 中 tag `run-determination` 的 run-determination 记忆条目(schema `1`) | session | `run-determination.py::load_determinations` | run_id | determined_at | host-prompt | indirect | Exercised | axis-regression, green-unproven |
| exec-quant-record | `kind: speckit.exec-quant` 记录(schema 版本由 `quant-record-schema.yaml` 声明) | exec-quant | `exec-quant.py::load_records` | run_id | collected_at | project-rules | indirect | Exercised | — |
| feedback-entry | `.specify/feedback/` 中 `run_id` 不携带 `gate:` 族前缀的 feedback 条目(仅元数据面) | feedback | `feedback-utils.py::scan_entries` | run_id | created | project-rules | direct | Exercised | — |
| gate-observation-record | 门控观察族的 feedback 条目:`run_id` = `gate:<gate_id>:<UTC ts>`(前缀协议 owner:`shared/guidelines/confirmation-gates.md`) | feedback | `feedback-utils.py::scan_entries` | run_id | created | project-rules | direct | Exercised | — |
| evidence-finding | 证据运行的 finding 项(`kind: speckit.evidence-findings`,`schemaVersion: 1`;项字段钉在 `FINDINGS_PROJECTION_FIELDS`) | evidence | `evidence-utils.py::load_index` + `run-determination.py::FINDINGS_PROJECTION_FIELDS` | runId | created | project-rules | indirect | Exercised | evidence-missing |
| probe-registry-declaration | probe 注册表声明对象(`.specify/shared/definitions/probe-definitions.md`) | registry | `probe-utils.py::load_probe_registry` | — | — | project-rules | indirect | Wired | — |

偏差类的推导引源引擎自身的裁决值域,含义见 § Reading Contract(读取契约)的偏差真实性规则;不声明任何类的行永不产生负面观察。probe 行是声明行:每次读取对当前状态评价一次,run-identity-exempt 且 window-exempt;`Wired` 是它的正状上限(已配置不等于已演练)。instructions reconcile 观察 MUST NOT 进入目录,直到某 store 持久化它们(今天没有)——它们保持 § Blind-Spot Register 的盲区类。

## Blind-Spot Register(盲区登记)

本表是盲区登记的唯一声明处;每个盲区类在每次读取的覆盖节中以不可观察出现。理由列说明「今天为何无持久化传感器观察它」,采集方向列说明「owner 许可的采集变更会走的方向」。声明行的增删只能经本文件修订。

| blind_spot | reason | capture_direction |
|------------|--------|-------------------|
| host-prompt-content | 宿主系统提示原文与用户直接提示文本从不被读取(隐私红线),因此宿主层规则级遵从没有传感器。 | 无——隐私红线:原始宿主与用户提示文本永不读取;任何 owner 许可的变更必须先定义一个宿主发出的、结构化的非文本信号。 |
| host-rule-surfacing | 宿主环境是否真的加载并呈现项目规则文件,不留记录。 | 由宿主在加载/呈现项目规则文件时写出结构化事件记录。 |
| in-turn-rule-behavior | 某一规则节是否在本回合被遵守,没有把回合行为与规则绑定的结构化记录。 | 一个把规则节与观察到的回合行为绑定、且经持久化存储保留的逐回合记录。 |
| anomaly-line-persistence | 派发返回时的 fast-fail anomaly 行不被持久化;被 run-determination 所有者放弃的红状态生产器 MUST NOT 在此重新引入,边界仍归 `shared/guidelines/fast-fail.md`。 | 不得重新引入红状态生产器;任何持久化变更必须先取得 run-determination 所有者的许可。 |
| gate-breach-and-silent-skip | 未过必需确认门就行动、或静默跳过必需步骤,都不记录事件;缺席 MUST NOT 读成违规。 | 在必需确认门被绕过或必需步骤被跳过时写出事件记录——事件本身被记录时才可进入目录。 |
| instruction-drift-between-reconciles | 指令节漂移只在 reconcile 运行时可见,且不持久化观察。 | 在 reconcile 运行时把观察持久化到既有存储(经该存储所有者许可)。 |

**`host-prompt-content` privacy red line**:原始宿主系统提示与用户直接提示文本从不被读取,读取输出永不复制原始用户对话文本。

**`anomaly-line-persistence` boundary**:fast-fail anomaly 行的持久化边界由 `shared/guidelines/fast-fail.md` 拥有;本特性只把它的缺席登记为盲区,不重新引入被放弃的红状态生产器。
## Reading Contract(读取契约)

### Per-run reading fields(按运行读取字段)

| field | meaning |
|-------|---------|
| reading_format | 读取格式版本,整数 `1`(引擎 schema)。 |
| engine | `{path, version}`;版本在运行时从最近的 `pyproject.toml` 重导出,源码中无版本字面量。 |
| declaration_set | `{version, facts[]}`;version 是五个声明事实文件按排序后的仓库相对路径加字节计算的 SHA-256,读时计算,无存储的版本计数器。 |
| scope | 解析出的范围与依据;字段含义见 § Scope and window(范围与窗口)。 |
| status | 读取状态,封闭字面量之一;推导规则见 § Reading status(读取状态)。 |
| observations | 每个目录行恰一条,按 § Signal Catalog 的目录声明顺序;字段:state、deviation_classes、reason(缺席态必有 `{cause, source}`)、sources(可解析源引用 `{store, path, record, field}`)。 |
| coverage | 强制覆盖节:observable 行、not_observable 行、全部六个盲区类及其理由、范围内记录数、invalid 记录数。缺少覆盖节的读取无效。 |
| invalid_sources | `[{path, cause}]`,按 path 排序;cause 见 § Invalid-source causes(无效源原因);绝不静默跳过。 |
| duplicates | `[{row, identity, count, paths[]}]`,按 (row, identity) 排序;每多一次出现计一次并以路径披露。 |

读取不包含 `generated_at` 或任何时钟字段;两种输出形态(人类可读与 `--json`)来自同一份计算结构,JSON 以排序键序列化,相同输入与相同机制版本产出逐字节相同的读取。没有本表之外的字段携带裁决。

### Observation state derivation(观察状态推导)

每次读取用同一四分法,不产生其它状态:

1. 源存储不可读、不可达或缺失 → `not_evaluated`,cause `source-unavailable`;
2. 源可读且至少一条有效匹配记录 → 该行声明的正状上限(`Exercised`;probe 行为 `Wired`)加该行声明的偏差类;
3. 源可读且有匹配记录但全部不可解释 → `not_evaluated`,cause `invalid-source`(细则进 `invalid_sources` 披露);
4. 源可读且零匹配记录 → 显式运行身份范围下 `not_evaluated`、默认或窗口范围下 `Unobserved`,cause 均为 `no-matching-records`。

缺席永远不读成遵从,也永远不读成违规:缺失的记录、缺失的门控观察与缺失的 anomaly 行都只按上表出现;违规式代理只有在既有存储记录了事件本身时才可进入 § Signal Catalog。

### Reason causes(缺席原因)

本表拥有三个缺席原因的含义;令牌是引擎 schema,两面由声明守卫双向钉住(contract C-015)。这三个原因与下列无效源原因有意**不是**声明事实:FR-018 把本特性的声明集固定为五个。

| cause | meaning |
|-------|---------|
| source-unavailable | 源存储不可读、不可达或缺失,读取无法观察该行;原因随附源标识。 |
| no-matching-records | 源可读且零条匹配记录;显式运行身份范围下读 `not_evaluated`,默认或窗口范围下读 `Unobserved`。 |
| invalid-source | 源可读且有匹配记录,但全部不可解释;每一不可解释记录的细则进 `invalid_sources` 披露。 |

### Invalid-source causes(无效源原因)

| invalid-source cause | meaning |
|----------------------|---------|
| unparsable | 记录无法解析(格式或语法损坏),不按任何 schema 解释。 |
| schema-violation | 记录可解析,但其值令牌落在源引擎声明值域之外;不按当前 schema 解释。 |
| unknown-schema-version | 记录由更旧或未知的 schema 版本写入,按当前 schema 不重解释,原样置于 invalid 披露。 |
| invalid-timestamp | 记录的时间戳不可解析,无法参与窗口算术或排序;记录本身不进入观察。 |

### Reading status(读取状态)

读取状态从范围推导,两种输出形态共用同一推导:解析范围内目录记录数为零 → `no-data`;显式 `--run` 匹配零条记录 → `not-found`;否则任一观察为 `not_evaluated` → `partial`,所有观察均已评价 → `complete`。四种状态都以退出 `0` 产出读取。

退出码封闭(owner:`shared/definitions/script-interface-definitions.md`):`0` 已产出读取(含 `no-data` 与 `not-found`)或覆盖检查干净;`1` 覆盖检查报告发现;`2` 无法产出读取——不可用的声明层或 owner 文档、五个声明集或本文件表格中的未知令牌、命令行上的未知选项、目录行点名未声明的 store、非法参数。记录级的未知值令牌不是退出 `2` 的原因:它进入 `invalid_sources`,读取以退出 `0` 继续。

### Ordering, tie-breaks, duplicates and caps(排序、并列决胜、重复与上限)

- 行按目录声明顺序;盲区按登记顺序;源引用按(path, record identity);invalid sources 按 path;duplicates 按(row, identity)。
- 重复以每行声明的身份字段(加该行声明的 timestamp)为键:每多一次出现计一次并以路径披露——绝不合并、绝不静默重复计数。
- 输出上限:每观察源引用 20、invalid sources 50、duplicates 20;每次截断带 shown/total 披露。上限是输出界,绝不是判断阈值。

### Scope and window(范围与窗口)

- 无显式范围时,读取解析目录记录中观测到的最近运行身份:按记录时间戳、并列时依次按 store 名与源路径决胜,并在范围节打印解析出的身份与依据 `{store, path, timestamp}`;不存在此类记录时仍产出,读取状态 `no-data`。
- 显式 `--run <run-id>` 钉住运行身份;匹配零条记录时读取状态 `not-found`(退出 0)。
- `--since` / `--until` 请求纵向读取:窗口按每条记录自身声明的 timestamp 字段取半开 `[since, until)`;省略的边界打印为字面量 `open`(绝不解析成时钟读数),两个边界都出现在输出中;边界只接受 `YYYY-MM-DD` 或 `YYYY-MM-DDTHH:MM:SSZ`(UTC),非法值退出 2;`--run` 与任一边界同时出现是输入错误(退出 2)。
- 边界恰为记录时间戳时按半开规则归属:`since` 计入、`until` 排除。窗口内零条目录记录 → `no-data`(退出 0),六个目录行仍各出现一次并按 § Observation state derivation 读取。
- 纵向读取 = 同一契约加每个目录行的按证据状态计数;声明行(probe)对当前状态评价一次并在范围说明中标注 window-exempt,绝不伪造为时间序列;MUST NOT 对项目、智能体或用户排名或比较。

### Deviation truth(偏差真实性)

偏差类只在声明它的行上、只从下列推导触发,含义与推导引源引擎自身的裁决值域:

- `axis-regression`(`run-determination-record`):某轴判定在 `run-determination.py` 的 comparison / correctness 裁决值域中读作 `regressed`;
- `green-unproven`(`run-determination-record`):artifact correctness 读到引擎的 `GREEN_UNPROVEN_VERDICT` 对(`not_evaluated` / `green_unproven`);
- `evidence-missing`(`evidence-finding`):finding 项的 `evidenceState` 读作 `Missing`。

不声明任何类的行永不产生负面观察。

### Privacy(隐私)

读取只携带结构化字段、封闭令牌与源引用。feedback 条目正文(review 散文、points)、门控决策散文与 finding summary 绝不进入任一输出形态;feedback 条目只经其 frontmatter 元数据面读取,不使用正文读取过滤器。

## Red Lines(红线)

- 不产出复合遵从分、成熟度指数、排名或任何跨项目比较;聚合只有按封闭状态的计数加覆盖。
- 不新增 store、采集点或记录 schema 变更;本特性是纯消费者。
- 不读取原始宿主系统提示或原始用户对话文本。
- 不访问网络、不执行自动传输;读数留在项目内。
- 宿主层观察只服务本框架的集成决策,绝不包装成关于宿主产品的反馈;feedback 目标仍是框架自身。
- feedback 红线(仅框架自身为目标、用户数据可选、零自动传输)由 `shared/workflow/feedback-step.md` 拥有,此处只按引用抵达,MUST NOT 复述。

## Entry(入口)

本机制的唯一文档化调用:

```bash
python3 .specify/scripts/python/prompt-adherence.py
```

框架源是 `scripts/python/prompt-adherence.py`,安装副本是 `.specify/scripts/python/prompt-adherence.py`。裸调用打印默认范围的按运行读取;`--run <run-id>` 钉住运行身份;`--since` / `--until` 请求纵向读取;`--json` 输出机器可读形态;`--workspace-root PATH` 选择项目;`--check-coverage` 运行 § Premise Chain & Coverage Map 的覆盖检查。`-h` / `--help` / `--version` 按脚本接口契约(owner:`shared/definitions/script-interface-definitions.md`)。发现性是框架地图的两行(owner 文档行与读取入口行);本版本不发布 `/speckit.*` 命令或 skill 包装器。
